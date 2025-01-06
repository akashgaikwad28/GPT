# app/utils.py

import logging, re

def log_error(message):
    """Log an error message."""
    logger = logging.getLogger(__name__)
    logger.error(message)

def format_response(response):
    # Replace newlines with <br> for line breaks
    response = response.replace('\n', '<br>')
    
    # Convert bold text (e.g., **text**) to <strong> tags
    response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response)
    
    # Convert italic text (e.g., *text*) to <em> tags
    response = re.sub(r'\*(.*?)\*', r'<em>\1</em>', response)

    # Detect headings (e.g., "## Heading" or "# Heading")
    response = re.sub(r'(?m)^(#+)\s*(.*)', lambda m: f'<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>', response)

    # Handle lists (e.g., "1. Item" or "- Item")
    response = re.sub(r'(?m)^\d+\.\s*(.*)', r'<li>\1</li>', response)
    response = re.sub(r'(?m)^\-\s*(.*)', r'<li>\1</li>', response)
    
    # Wrap list items in <ul>
    if '<li>' in response:
        response = '<ul>' + response + '</ul>'

    # Handle code blocks (using triple backticks)
    if "```" in response:
        parts = response.split("```")
        formatted_response = ""
        for i, part in enumerate(parts):
            if i % 2 == 1:  # Odd index means it's code
                formatted_response += f'<pre class="code-block"><code>{part}</code></pre>'
            else:
                formatted_response += part.replace('\n', '<br>')  # Replace newlines with <br>
        return formatted_response

    return response