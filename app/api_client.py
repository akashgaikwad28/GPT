import os
from groq import Groq
from logger import CustomLogger  # Import your custom logger
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    """Class to interact with the Groq API."""

    def __init__(self):
        self.api_key = os.getenv('API_KEY')  # Get the actual API key from environment
        if not self.api_key:
            raise ValueError("API_KEY environment variable is not set. Ensure it's defined in your .env file.")
        
        self.model = os.getenv('GROQ_MODEL', 'llama3-8b-8192')  # Default to a specific model if not set
        self.logger = CustomLogger().get_logger()  # Initialize your custom logger

        try:
            self.client = Groq(api_key=self.api_key)
            self.logger.info("Groq client initialized successfully.")
        except Exception as e:
            self.logger.error(f"Failed to initialize Groq client: {e}")
            raise

    def get_response(self, messages):
        """
        Send messages to the Groq API and return the response.

        :param messages: List of messages for the conversation.
        :return: AI response as a string.
        """
        if not isinstance(messages, list) or not all("role" in m and "content" in m for m in messages):
            self.logger.error("Invalid message format. Each message must have 'role' and 'content' keys.")
            return "Invalid message format."

        try:
            self.logger.info(f"Sending messages to Groq API: {messages}")
            # Sending the request to the Groq API
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model
            )
            response = chat_completion.choices[0].message.content
            self.logger.info("Received response from Groq API.")
            return response
        except TimeoutError:
            self.logger.error(f"Request to Groq API timed out for messages: {messages}")
            return "The request timed out. Please try again later."
        except Exception as e:
            self.logger.error(f"Unexpected error for messages: {messages}. Error: {e}")
            return "Sorry, I couldn't get a response at this time."
