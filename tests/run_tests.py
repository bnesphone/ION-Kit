#!/usr/bin/env python3
"""
Run all ION Kit tests
"""
import sys
import subprocess
from pathlib import Path

def main():
    tests_dir = Path(__file__).parent
    
    print("=" * 60)
    print("ION Kit Test Runner")
    print("=" * 60)
    print()
    
    # Run Python tests
    print("[TEST] Running Python Tests...")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(tests_dir), "-p", "test_*.py", "-v"],
        cwd=tests_dir.parent
    )
    
    if result.returncode == 0:
        print("\n[OK] All tests passed!")
        return 0
    else:
        print("\n[X] Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
