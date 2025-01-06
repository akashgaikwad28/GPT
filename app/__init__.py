from flask import Flask
import os
import yaml
from dotenv import load_dotenv
from logger import CustomLogger  # Import your custom logger

# Load environment variables from .env file
load_dotenv()

class AppConfig:
    """Class to handle application configuration."""
    
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from config.yaml."""
        config_path = os.getenv('CONFIG_PATH', 'config/config.yaml')
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
        except FileNotFoundError:
            raise RuntimeError(f"{config_path} not found. Please ensure the file exists.")
        except yaml.YAMLError as e:
            raise RuntimeError(f"Error parsing {config_path}: {e}")
        
        # Replace API key placeholder with actual value from environment variables
        config['api']['key'] = os.getenv('API_KEY', config.get('api', {}).get('key'))
        
        return config

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, template_folder='templates')  # Initialize the Flask app

    # Set up logging
    logger = CustomLogger().get_logger()  # Initialize your custom logger
    logger.info("Flask application starting...")

    # Load configuration
    try:
        app_config = AppConfig()
        app.config.update(app_config.config)
    except RuntimeError as e:
        logger.error(f"Error during app initialization: {e}")
        raise

    # Register routes
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
