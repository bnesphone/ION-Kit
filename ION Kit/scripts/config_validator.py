#!/usr/bin/env python3
"""
Configuration Validator for ION Kit
Validates .ionkit.json against schema and provides helpful feedback
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

try:
    from colorama import Fore, Style
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class Fore:
        GREEN = RED = YELLOW = CYAN = RESET = ""
    class Style:
        BRIGHT = RESET_ALL = ""

# Configuration schema definition
CONFIG_SCHEMA = {
    "version": {"type": "string", "required": False},
    "description": {"type": "string", "required": False},
    "preferences": {
        "type": "object",
        "required": True,
        "properties": {
            "verbose": {"type": "boolean", "default": False},
            "colorOutput": {"type": "boolean", "default": True},
            "autoUpdate": {"type": "boolean", "default": True},
            "telemetry": {"type": "boolean", "default": False}
        }
    },
    "tools": {
        "type": "object",
        "required": True,
        "properties": {
            "backgroundRemover": {
                "type": "object",
                "properties": {
                    "defaultModel": {"type": "string", "enum": ["u2net", "u2net_human_seg", "u2netp"], "default": "u2net"},
                    "outputFormat": {"type": "string", "enum": ["png", "jpg"], "default": "png"},
                    "quality": {"type": "integer", "min": 1, "max": 100, "default": 95}
                }
            },
            "scraper": {
                "type": "object",
                "properties": {
                    "timeout": {"type": "integer", "min": 1000, "max": 120000, "default": 30000},
                    "userAgent": {"type": "string", "default": "ION-Kit-Scraper/1.0"},
                    "maxRetries": {"type": "integer", "min": 0, "max": 10, "default": 3}
                }
            },
            "packager": {
                "type": "object",
                "properties": {
                    "defaultIcon": {"type": "string", "default": ""},
                    "compression": {"type": "string", "enum": ["none", "normal", "maximum"], "default": "normal"}
                }
            },
            "mocker": {
                "type": "object",
                "properties": {
                    "defaultPort": {"type": "integer", "min": 1024, "max": 65535, "default": 8000},
                    "cors": {"type": "boolean", "default": True},
                    "logging": {"type": "boolean", "default": True}
                }
            }
        }
    },
    "validation": {
        "type": "object",
        "required": False,
        "properties": {
            "strictMode": {"type": "boolean", "default": False},
            "autoFix": {"type": "boolean", "default": True},
            "ignoreWarnings": {"type": "boolean", "default": False}
        }
    },
    "templates": {
        "type": "object",
        "required": False,
        "properties": {
            "customTemplatesPath": {"type": "string", "default": "./templates"},
            "defaultTemplate": {"type": "string", "default": "react-typescript"}
        }
    },
    "performance": {
        "type": "object",
        "required": False,
        "properties": {
            "showTimings": {"type": "boolean", "default": False},
            "maxConcurrentTasks": {"type": "integer", "min": 1, "max": 16, "default": 4},
            "cacheEnabled": {"type": "boolean", "default": True}
        }
    }
}


class ConfigValidator:
    """Validates configuration against schema"""
    
    def __init__(self, config_path: Path = None):
        self.config_path = config_path or Path(".ionkit.json")
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.suggestions: List[str] = []
    
    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """
        Validate configuration file
        Returns: (is_valid, errors, warnings)
        """
        if not self.config_path.exists():
            self.errors.append(f"Configuration file not found: {self.config_path}")
            self.suggestions.append("Run 'python scripts/config_manager.py init' to create default config")
            return (False, self.errors, self.warnings)
        
        # Load and parse JSON
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON syntax: {e}")
            self.suggestions.append("Use a JSON validator to find syntax errors")
            return (False, self.errors, self.warnings)
        except Exception as e:
            self.errors.append(f"Failed to read config: {e}")
            return (False, self.errors, self.warnings)
        
        # Validate against schema
        self._validate_object(config, CONFIG_SCHEMA, "")
        
        is_valid = len(self.errors) == 0
        return (is_valid, self.errors, self.warnings)
    
    def _validate_object(self, obj: Dict, schema: Dict, path: str):
        """Recursively validate object against schema"""
        for key, rules in schema.items():
            current_path = f"{path}.{key}" if path else key
            
            # Check if required
            if rules.get("required", False) and key not in obj:
                self.errors.append(f"Missing required field: {current_path}")
                continue
            
            if key not in obj:
                continue
            
            value = obj[key]
            value_type = rules.get("type")
            
            # Type validation
            if value_type == "object" and isinstance(value, dict):
                if "properties" in rules:
                    self._validate_object(value, rules["properties"], current_path)
            elif value_type == "string" and not isinstance(value, str):
                self.errors.append(f"{current_path}: Expected string, got {type(value).__name__}")
            elif value_type == "integer" and not isinstance(value, int):
                self.errors.append(f"{current_path}: Expected integer, got {type(value).__name__}")
            elif value_type == "boolean" and not isinstance(value, bool):
                self.errors.append(f"{current_path}: Expected boolean, got {type(value).__name__}")
            
            # Enum validation
            if "enum" in rules and value not in rules["enum"]:
                self.errors.append(f"{current_path}: Invalid value '{value}'. Must be one of: {', '.join(map(str, rules['enum']))}")
            
            # Range validation for integers
            if value_type == "integer":
                if "min" in rules and value < rules["min"]:
                    self.errors.append(f"{current_path}: Value {value} is below minimum {rules['min']}")
                if "max" in rules and value > rules["max"]:
                    self.errors.append(f"{current_path}: Value {value} exceeds maximum {rules['max']}")
        
        # Check for unknown fields
        for key in obj.keys():
            if key not in schema:
                self.warnings.append(f"Unknown field: {f'{path}.{key}' if path else key}")
    
    def display_results(self, is_valid: bool, errors: List[str], warnings: List[str]):
        """Display validation results with formatting"""
        print("\n" + "="*70)
        print("Configuration Validation Report")
        print("="*70 + "\n")
        
        if is_valid and not warnings:
            if HAS_COLOR:
                print(f"{Fore.GREEN}{Style.BRIGHT}✓ Configuration is valid!{Style.RESET_ALL}\n")
            else:
                print("[OK] Configuration is valid!\n")
        else:
            if errors:
                if HAS_COLOR:
                    print(f"{Fore.RED}{Style.BRIGHT}ERRORS ({len(errors)}):{Style.RESET_ALL}")
                else:
                    print(f"ERRORS ({len(errors)}):")
                for i, error in enumerate(errors, 1):
                    print(f"  {i}. {error}")
                print()
            
            if warnings:
                if HAS_COLOR:
                    print(f"{Fore.YELLOW}WARNINGS ({len(warnings)}):{Style.RESET_ALL}")
                else:
                    print(f"WARNINGS ({len(warnings)}):")
                for i, warning in enumerate(warnings, 1):
                    print(f"  {i}. {warning}")
                print()
            
            if self.suggestions:
                if HAS_COLOR:
                    print(f"{Fore.CYAN}SUGGESTIONS:{Style.RESET_ALL}")
                else:
                    print("SUGGESTIONS:")
                for i, suggestion in enumerate(self.suggestions, 1):
                    print(f"  {i}. {suggestion}")
                print()
        
        print("="*70 + "\n")
    
    def auto_fix(self) -> bool:
        """Attempt to auto-fix common configuration issues"""
        if not self.config_path.exists():
            return False
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            return False
        
        fixed = False
        
        # Add missing required sections
        if "preferences" not in config:
            config["preferences"] = {}
            fixed = True
        
        if "tools" not in config:
            config["tools"] = {}
            fixed = True
        
        # Add default values for missing properties
        for section, rules in CONFIG_SCHEMA.items():
            if section in config and rules.get("type") == "object" and "properties" in rules:
                for prop, prop_rules in rules["properties"].items():
                    if prop not in config[section] and "default" in prop_rules:
                        config[section][prop] = prop_rules["default"]
                        fixed = True
        
        if fixed:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            return True
        
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate ION Kit configuration")
    parser.add_argument("--config", default=".ionkit.json", help="Config file path")
    parser.add_argument("--fix", action="store_true", help="Auto-fix common issues")
    parser.add_argument("--quiet", action="store_true", help="Only show errors")
    
    args = parser.parse_args()
    
    validator = ConfigValidator(Path(args.config))
    
    if args.fix:
        if HAS_COLOR:
            print(f"{Fore.CYAN}Attempting auto-fix...{Style.RESET_ALL}")
        else:
            print("Attempting auto-fix...")
        
        if validator.auto_fix():
            if HAS_COLOR:
                print(f"{Fore.GREEN}Configuration fixed!{Style.RESET_ALL}\n")
            else:
                print("Configuration fixed!\n")
        else:
            if HAS_COLOR:
                print(f"{Fore.YELLOW}No fixes applied{Style.RESET_ALL}\n")
            else:
                print("No fixes applied\n")
    
    is_valid, errors, warnings = validator.validate()
    
    if not args.quiet or errors:
        validator.display_results(is_valid, errors, warnings)
    
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
