import sys
import json
from typing import Dict, Any
from src.utils.menu import Menu
from src.utils.validators import validate_url, validate_json
from src.utils.config import Config
from src.api_client.http_client import HttpClient

def main():
    try:
        # Initialize core components
        menu = Menu()
        config = Config()
        
        # Load saved configuration
        settings = config.load_config()
        
        # Start the menu system
        menu.run()
        
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        sys.exit(1)

def setup_logging():
    """Configure logging for the application"""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('api_tester.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

if __name__ == "__main__":
    logger = setup_logging()
    try:
        main()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)