from app.api_client import GroqClient

class ChatManager:
    """Class to manage chat interactions."""

    def __init__(self):
        self.client = GroqClient()  # Initialize the Groq client
        self.conversation_history = []  # Store conversation history

    def add_message(self, role, content):
        """
        Add a message to the conversation history.

        :param role: The role of the sender ("user" or "assistant").
        :param content: The content of the message.
        """
        self.conversation_history.append({"role": role, "content": content})

    def get_response(self, user_message):
        """
        Get a concise or detailed response based on user input.

        :param user_message: The message input from the user.
        :return: AI response as a string.
        """
        try:
            # Validate user_message
            if not user_message or not isinstance(user_message, str):
                raise ValueError("Invalid user message. Please provide a valid string.")

            # Add user's message to history
            self.add_message("user", user_message)

            # Determine prompt type based on keywords in the user's message
            if any(keyword in user_message.lower() for keyword in ["what is", "define"]):
                prompt = f"Provide a concise definition of: {user_message}"
            elif any(keyword in user_message.lower() for keyword in ["explain", "code"]):
                prompt = f"Explain clearly with examples: {user_message}"
            else:
                prompt = f"Respond concisely to: {user_message}"

            # Prepare messages for the API call
            messages = [{"role": "user", "content": prompt}]

            # Get AI response
            ai_response = self.client.get_response(messages)

            # Validate AI response
            if not ai_response:
                raise ValueError("Empty response received from the AI.")

            # Add AI's response to history
            self.add_message("assistant", ai_response)

            return ai_response

        except Exception as e:
            # Handle any errors gracefully
            error_message = f"An error occurred: {str(e)}"
            self.add_message("assistant", error_message)
            return error_message
