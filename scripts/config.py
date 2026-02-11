"""
Configuration Manager for ION Kit
Handles loading, saving, and validating user preferences.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

class Config:
    """Configuration manager with defaults and user overrides"""
    
    DEFAULT_CONFIG = {
        "version": "1.0.0",
        "preferences": {
            "verbose": False,
            "colorOutput": True,
            "autoUpdate": True,
            "telemetry": False
        },
        "tools": {
            "backgroundRemover": {
                "defaultModel": "u2net",
                "outputFormat": "png",
                "quality": 95
            },
            "scraper": {
                "timeout": 30000,
                "userAgent": "ION-Kit-Scraper/1.0",
                "maxRetries": 3
            },
            "packager": {
                "defaultIcon": "",
                "compression": "normal"
            },
            "mocker": {
                "defaultPort": 8000,
                "cors": True,
                "logging": True
            }
        },
        "validation": {
            "strictMode": False,
            "autoFix": True,
            "ignoreWarnings": False
        },
        "templates": {
            "customTemplatesPath": "./templates",
            "defaultTemplate": "react-typescript"
        },
        "performance": {
            "showTimings": False,
            "maxConcurrentTasks": 4,
            "cacheEnabled": True
        }
    }
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize config with optional custom path"""
        if config_path is None:
            # Look for config in current dir, then home dir, then ION Kit root
            self.config_path = self._find_config()
        else:
            self.config_path = Path(config_path)
        
        self.config = self._load_config()
    
    def _find_config(self) -> Path:
        """Find config file in standard locations"""
        search_paths = [
            Path.cwd() / ".ionkit.json",
            Path.home() / ".ionkit.json",
            Path(__file__).parent.parent / ".ionkit.json"
        ]
        
        for path in search_paths:
            if path.exists():
                return path
        
        # Default to ION Kit root
        return Path(__file__).parent.parent / ".ionkit.json"
    
    def _load_config(self) -> Dict[str, Any]:
        """Load config from file or use defaults"""
        if not self.config_path.exists():
            return self.DEFAULT_CONFIG.copy()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            
            # Merge with defaults (user overrides defaults)
            return self._deep_merge(self.DEFAULT_CONFIG.copy(), user_config)
        except Exception as e:
            print(f"Warning: Failed to load config from {self.config_path}: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get config value using dot notation (e.g., 'tools.scraper.timeout')"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any) -> None:
        """Set config value using dot notation"""
        keys = key_path.split('.')
        current = self.config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def save(self) -> bool:
        """Save current config to file"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def reset(self) -> None:
        """Reset to default configuration"""
        self.config = self.DEFAULT_CONFIG.copy()
    
    def validate(self) -> tuple[bool, list[str]]:
        """Validate configuration and return (is_valid, errors)"""
        errors = []
        
        # Check version
        if 'version' not in self.config:
            errors.append("Missing version field")
        
        # Check required sections
        required = ['preferences', 'tools', 'validation', 'templates', 'performance']
        for section in required:
            if section not in self.config:
                errors.append(f"Missing required section: {section}")
        
        return (len(errors) == 0, errors)
    
    def show(self) -> None:
        """Display current configuration"""
        print("\n" + "="*60)
        print("ION Kit Configuration")
        print("="*60)
        print(f"\nConfig file: {self.config_path}")
        print(f"Exists: {'Yes' if self.config_path.exists() else 'No (using defaults)'}")
        print("\n" + json.dumps(self.config, indent=2))
        print("="*60 + "\n")


# Global config instance
_config_instance: Optional[Config] = None

def get_config() -> Config:
    """Get or create global config instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance


if __name__ == "__main__":
    import sys
    
    config = get_config()
    
    if len(sys.argv) < 2:
        config.show()
    else:
        command = sys.argv[1]
        
        if command == "show":
            config.show()
        elif command == "get":
            if len(sys.argv) < 3:
                print("Usage: python config.py get <key.path>")
            else:
                value = config.get(sys.argv[2])
                print(f"{sys.argv[2]}: {value}")
        elif command == "set":
            if len(sys.argv) < 4:
                print("Usage: python config.py set <key.path> <value>")
            else:
                # Try to parse value as JSON, fallback to string
                try:
                    value = json.loads(sys.argv[3])
                except:
                    value = sys.argv[3]
                
                config.set(sys.argv[2], value)
                if config.save():
                    print(f"Set {sys.argv[2]} = {value}")
                else:
                    print("Failed to save config")
        elif command == "reset":
            config.reset()
            if config.save():
                print("Configuration reset to defaults")
            else:
                print("Failed to save config")
        elif command == "validate":
            is_valid, errors = config.validate()
            if is_valid:
                print("Configuration is valid")
            else:
                print("Configuration errors:")
                for error in errors:
                    print(f"  - {error}")
        else:
            print("Unknown command")
            print("Usage: python config.py [show|get|set|reset|validate]")
