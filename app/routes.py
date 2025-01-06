from flask import Blueprint, render_template, request, jsonify
import re
from app.chat import ChatManager

# Create a Blueprint for the main application
main = Blueprint('main', __name__)

# Initialize the ChatManager
chat_manager = ChatManager()  # Ensure this class is defined in app/chat.py

@main.route('/')
def index():
    """
    Render the main chat interface.
    """
    return render_template('chat.html')  # Renders the chat.html template

@main.route('/test')
def test():
    """
    Test route to render base.html.
    Useful for checking if the base template is loading correctly.
    """
    return render_template('base.html')  # Assuming base.html exists in templates/

@main.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from users via API.
    Expects JSON payload with a "message" field.
    """
    try:
        # Extract the user message from the request
        user_message = request.json.get('message')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Get AI response using ChatManager logic
        ai_response = chat_manager.get_response(user_message)
        
        # Format the AI's response for better display
        formatted_response = format_response(ai_response)
        
        return jsonify({"response": formatted_response})  # Return the formatted response as JSON
    except Exception as e:
        # Handle unexpected errors gracefully
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

def format_response(response):
    """
    Format the AI's response for rendering in HTML.
    Includes support for headings, bold, italic, lists, and code blocks.

    :param response: Raw response from the AI.
    :return: HTML-formatted string.
    """
    try:
        # Replace newlines with <br> for line breaks
        response = response.replace('\n', '<br>')
        
        # Convert bold text (e.g., **text**) to <strong> tags
        response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response)
        
        # Convert italic text (e.g., *text*) to <em> tags
        response = re.sub(r'\*(.*?)\*', r'<em>\1</em>', response)

        # Detect and format headings (e.g., "## Heading" or "# Heading")
        response = re.sub(r'(?m)^(#+)\s*(.*)', lambda m: f'<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>', response)

        # Handle unordered and ordered lists
        response = re.sub(r'(?m)^\d+\.\s*(.*)', r'<li>\1</li>', response)  # Ordered lists
        response = re.sub(r'(?m)^\-\s*(.*)', r'<li>\1</li>', response)  # Unordered lists
        if '<li>' in response:
            response = '<ul>' + response + '</ul>'  # Wrap list items in <ul> tags

        # Handle code blocks (using triple backticks)
        if "```" in response:
            parts = response.split("```")
            formatted_response = ""
            for i, part in enumerate(parts):
                if i % 2 == 1:  # Odd index means it's code
                    formatted_response += f'<pre class="code-block"><code>{part}</code></pre>'
                else:
                    formatted_response += part.replace('\n', '<br>')  # Replace newlines with <br>
            response = formatted_response

        return response
    except Exception as e:
        # Log and return the raw response if formatting fails
        print(f"Error formatting response: {e}")
        return response
