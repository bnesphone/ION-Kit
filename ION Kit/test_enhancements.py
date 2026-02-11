#!/usr/bin/env python3
"""
Test script for ION Kit v6.2.0 enhancements
Verifies all new features work correctly
"""

import sys
import subprocess
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def test(name, passed):
    """Print test result"""
    if passed:
        print(f"{GREEN}✓{RESET} {name}")
        return True
    else:
        print(f"{RED}✗{RESET} {name}")
        return False

def main():
    print("\n" + "="*60)
    print("ION Kit v6.2.0 Enhancement Tests")
    print("="*60 + "\n")
    
    root = Path(__file__).parent
    passed = 0
    failed = 0
    
    # Test 1: Config module
    try:
        sys.path.insert(0, str(root / "scripts"))
        from config import Config
        config = Config()
        test("Config module loads", True)
        passed += 1
    except Exception as e:
        test(f"Config module loads: {e}", False)
        failed += 1
    
    # Test 2: Progress module
    try:
        from progress import ProgressBar, Spinner, status
        test("Progress module loads", True)
        passed += 1
    except Exception as e:
        test(f"Progress module loads: {e}", False)
        failed += 1
    
    # Test 3: Errors module
    try:
        from errors import IONKitError, ToolNotFoundError, handle_error
        test("Errors module loads", True)
        passed += 1
    except Exception as e:
        test(f"Errors module loads: {e}", False)
        failed += 1
    
    # Test 4: Templates module
    try:
        from templates import Template, TemplateManager
        manager = TemplateManager()
        test("Templates module loads", True)
        passed += 1
    except Exception as e:
        test(f"Templates module loads: {e}", False)
        failed += 1
    
    # Test 5: Config file exists
    config_file = root / ".ionkit.json"
    test("Config file exists", config_file.exists())
    if config_file.exists():
        passed += 1
    else:
        failed += 1
    
    # Test 6: Templates directory exists
    templates_dir = root / "templates"
    test("Templates directory exists", templates_dir.exists())
    if templates_dir.exists():
        passed += 1
    else:
        failed += 1
    
    # Test 7: React template exists
    react_template = templates_dir / "react-typescript.json"
    test("React template exists", react_template.exists())
    if react_template.exists():
        passed += 1
    else:
        failed += 1
    
    # Test 8: Express template exists
    express_template = templates_dir / "express-api.json"
    test("Express template exists", express_template.exists())
    if express_template.exists():
        passed += 1
    else:
        failed += 1
    
    # Test 9: Config operations
    try:
        config = Config()
        value = config.get("preferences.verbose")
        config.set("test.key", "test_value")
        is_valid, errors = config.validate()
        test("Config operations work", True)
        passed += 1
    except Exception as e:
        test(f"Config operations: {e}", False)
        failed += 1
    
    # Test 10: Template operations
    try:
        manager = TemplateManager()
        templates = manager.list_templates()
        test(f"Template operations work ({len(templates)} templates found)", True)
        passed += 1
    except Exception as e:
        test(f"Template operations: {e}", False)
        failed += 1
    
    # Results
    print("\n" + "="*60)
    total = passed + failed
    print(f"Results: {passed}/{total} tests passed")
    
    if failed == 0:
        print(f"{GREEN}All tests passed!{RESET}")
        print("="*60 + "\n")
        return 0
    else:
        print(f"{YELLOW}{failed} tests failed{RESET}")
        print("="*60 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
