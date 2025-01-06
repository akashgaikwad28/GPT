# config/__init__.py

import os
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AppConfig:
    """Class to handle application configuration."""
    
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from config.yaml."""
        with open('config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        
        # Replace API key placeholder with actual value from environment variables
        if 'api' in config and 'key' in config['api']:
            config['api']['key'] = os.getenv('API_KEY')  # Get the actual API key from environment
        
        return config

# Load the configuration
app_config = AppConfig()
config = app_config.config  # This is now accessible throughout your application

# Example usage: Accessing API key from config
API_KEY = config['api']['key']

