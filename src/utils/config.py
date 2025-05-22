import json
import os
from typing import Dict, Any, Optional

class Config:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.api-tester")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.default_config = {
            "default_headers": {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            "timeout": 30,
            "verify_ssl": True,
            "history_size": 50
        }
        self._ensure_config_dir()

    def _ensure_config_dir(self) -> None:
        """Create configuration directory if it doesn't exist"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or create default if not exists
        
        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            return self.save_config(self.default_config)
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            return self.default_config

    def save_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save configuration to file
        
        Args:
            config (Dict[str, Any]): Configuration to save
            
        Returns:
            Dict[str, Any]: Saved configuration
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            return config
        except Exception as e:
            print(f"Error saving config: {str(e)}")
            return self.default_config

    def update_config(self, key: str, value: Any) -> Dict[str, Any]:
        """
        Update specific configuration value
        
        Args:
            key (str): Configuration key to update
            value (Any): New value
            
        Returns:
            Dict[str, Any]: Updated configuration
        """
        config = self.load_config()
        config[key] = value
        return self.save_config(config)

    def get_value(self, key: str) -> Optional[Any]:
        """
        Get specific configuration value
        
        Args:
            key (str): Configuration key to retrieve
            
        Returns:
            Optional[Any]: Configuration value if exists, None otherwise
        """
        config = self.load_config()
        return config.get(key)