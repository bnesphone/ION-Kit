#!/usr/bin/env python3
"""
ION Kit Cleanup Utility
Removes temporary files, caches, and build artifacts
"""
import sys
import shutil
from pathlib import Path

def main():
    print("🧹 ION Kit Cleanup Utility\n")
    print("=" * 60)
    
    root_dir = Path(__file__).parent.parent
    removed_count = 0
    freed_space = 0
    
    # Patterns to clean
    patterns = [
        # Python
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        "**/.pytest_cache",
        "**/pip-log.txt",
        "**/pip-delete-this-directory.txt",
        "**/.tox",
        "**/.coverage",
        "**/.coverage.*",
        "**/htmlcov",
        "**/*.egg-info",
        "**/dist",
        "**/build",
        "**/.eggs",
        
        # Node.js
        "**/node_modules/.cache",
        "**/.npm",
        "**/.yarn-cache",
        "**/coverage",
        
        # IDE
        "**/.vscode/.ropeproject",
        "**/.idea/workspace.xml",
        "**/*.swp",
        "**/*.swo",
        "**/*~",
        
        # OS
        "**/.DS_Store",
        "**/Thumbs.db",
        "**/*.tmp",
        
        # Logs
        "**/*.log",
        
        # Temp directories
        "**/temp",
        "**/tmp",
        "**/.cache"
    ]
    
    print("\n📁 Scanning for cleanable files...\n")
    
    for pattern in patterns:
        for path in root_dir.glob(pattern):
            try:
                if path.is_file():
                    size = path.stat().st_size
                    path.unlink()
                    removed_count += 1
                    freed_space += size
                    print(f"  🗑️  Removed: {path.relative_to(root_dir)}")
                elif path.is_dir():
                    # Calculate directory size
                    dir_size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                    shutil.rmtree(path)
                    removed_count += 1
                    freed_space += dir_size
                    print(f"  🗑️  Removed: {path.relative_to(root_dir)}/")
            except Exception as e:
                print(f"  ⚠️  Could not remove {path.relative_to(root_dir)}: {e}")
    
    print("\n" + "=" * 60)
    print(f"✅ Cleanup complete!")
    print(f"📊 Removed: {removed_count} items")
    print(f"💾 Freed: {freed_space / (1024*1024):.2f} MB")
    
    # Optional: Clean specific tool caches
    print("\n💡 Tip: To clean node_modules, run:")
    print("   rm -rf tools/code-tools/node_modules")
    print("   (This is not done automatically to preserve dependencies)")

if __name__ == "__main__":
    main()
