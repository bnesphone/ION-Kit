#!/usr/bin/env python3
"""
ION Kit - Configuration Manager
Interactive configuration and settings management
"""
import sys
import json
from pathlib import Path
import os

class ConfigManager:
    def __init__(self):
        self.config_file = Path.home() / '.ionkit' / 'config.json'
        self.config_file.parent.mkdir(exist_ok=True)
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return self.get_default_config()
        return self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            'user': {
                'name': '',
                'email': '',
                'preferred_language': 'JavaScript',
                'preferred_framework': 'React'
            },
            'project': {
                'default_license': 'MIT',
                'git_init': True,
                'npm_init': True,
                'create_readme': True
            },
            'tools': {
                'default_port': 8000,
                'auto_cleanup': False,
                'verbose_mode': False
            },
            'ai': {
                'default_agent': 'orchestrator',
                'enable_suggestions': True,
                'context_aware': True
            },
            'docker': {
                'auto_build': False,
                'default_registry': ''
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"\n[OK] Configuration saved to: {self.config_file}")
    
    def display_config(self):
        """Display current configuration"""
        print("\n" + "=" * 70)
        print("ION KIT CONFIGURATION")
        print("=" * 70)
        print(f"\nConfig file: {self.config_file}\n")
        
        for section, settings in self.config.items():
            print(f"[{section.upper()}]")
            for key, value in settings.items():
                print(f"  {key}: {value}")
            print()
    
    def get_value(self, section, key):
        """Get a configuration value"""
        return self.config.get(section, {}).get(key)
    
    def set_value(self, section, key, value):
        """Set a configuration value"""
        if section not in self.config:
            self.config[section] = {}
        
        # Type conversion
        if value.lower() in ['true', 'false']:
            value = value.lower() == 'true'
        elif value.isdigit():
            value = int(value)
        
        self.config[section][key] = value
        print(f"\n[OK] Set {section}.{key} = {value}")
    
    def interactive_setup(self):
        """Interactive configuration setup"""
        print("\n" + "=" * 70)
        print("ION Kit Configuration Setup")
        print("=" * 70)
        print("\nPress Enter to keep current value\n")
        
        # User info
        print("[USER INFORMATION]")
        name = input(f"Name [{self.config['user']['name']}]: ").strip()
        if name:
            self.config['user']['name'] = name
        
        email = input(f"Email [{self.config['user']['email']}]: ").strip()
        if email:
            self.config['user']['email'] = email
        
        # Preferences
        print("\n[PREFERENCES]")
        print("Languages: JavaScript, TypeScript, Python")
        lang = input(f"Preferred language [{self.config['user']['preferred_language']}]: ").strip()
        if lang:
            self.config['user']['preferred_language'] = lang
        
        print("Frameworks: React, Next.js, Vue, Angular, Express")
        framework = input(f"Preferred framework [{self.config['user']['preferred_framework']}]: ").strip()
        if framework:
            self.config['user']['preferred_framework'] = framework
        
        # Project defaults
        print("\n[PROJECT DEFAULTS]")
        git_init = input(f"Auto-initialize git? [{self.config['project']['git_init']}] (y/n): ").strip().lower()
        if git_init:
            self.config['project']['git_init'] = git_init == 'y'
        
        # Tools
        print("\n[TOOLS]")
        port = input(f"Default API port [{self.config['tools']['default_port']}]: ").strip()
        if port and port.isdigit():
            self.config['tools']['default_port'] = int(port)
        
        verbose = input(f"Enable verbose mode by default? [{self.config['tools']['verbose_mode']}] (y/n): ").strip().lower()
        if verbose:
            self.config['tools']['verbose_mode'] = verbose == 'y'
        
        self.save_config()
        print("\n[OK] Configuration complete!")
    
    def reset_config(self):
        """Reset configuration to defaults"""
        confirm = input("\nReset all configuration to defaults? (y/N): ").strip().lower()
        if confirm == 'y':
            self.config = self.get_default_config()
            self.save_config()
            print("[OK] Configuration reset to defaults")
        else:
            print("[INFO] Reset cancelled")
    
    def export_config(self, output_file):
        """Export configuration to file"""
        path = Path(output_file)
        with open(path, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"[OK] Configuration exported to: {output_file}")
    
    def import_config(self, input_file):
        """Import configuration from file"""
        path = Path(input_file)
        if not path.exists():
            print(f"[X] File not found: {input_file}")
            return
        
        try:
            with open(path, 'r') as f:
                self.config = json.load(f)
            self.save_config()
            print(f"[OK] Configuration imported from: {input_file}")
        except Exception as e:
            print(f"[X] Error importing config: {e}")

def main():
    print("=" * 70)
    print("ION Kit - Configuration Manager")
    print("=" * 70)
    
    manager = ConfigManager()
    
    if len(sys.argv) < 2:
        manager.display_config()
        print("\nCommands:")
        print("  show              - Display current configuration")
        print("  setup             - Interactive configuration")
        print("  get <section> <key> - Get specific value")
        print("  set <section> <key> <value> - Set value")
        print("  reset             - Reset to defaults")
        print("  export <file>     - Export configuration")
        print("  import <file>     - Import configuration")
        return
    
    command = sys.argv[1]
    
    if command == 'show':
        manager.display_config()
    
    elif command == 'setup':
        manager.interactive_setup()
    
    elif command == 'get':
        if len(sys.argv) < 4:
            print("[X] Usage: config get <section> <key>")
        else:
            value = manager.get_value(sys.argv[2], sys.argv[3])
            print(f"{sys.argv[2]}.{sys.argv[3]} = {value}")
    
    elif command == 'set':
        if len(sys.argv) < 5:
            print("[X] Usage: config set <section> <key> <value>")
        else:
            manager.set_value(sys.argv[2], sys.argv[3], sys.argv[4])
            manager.save_config()
    
    elif command == 'reset':
        manager.reset_config()
    
    elif command == 'export':
        if len(sys.argv) < 3:
            print("[X] Usage: config export <file>")
        else:
            manager.export_config(sys.argv[2])
    
    elif command == 'import':
        if len(sys.argv) < 3:
            print("[X] Usage: config import <file>")
        else:
            manager.import_config(sys.argv[2])
    
    else:
        print(f"[X] Unknown command: {command}")

if __name__ == "__main__":
    main()
