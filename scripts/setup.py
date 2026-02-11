#!/usr/bin/env python3
"""
Quick Setup Script for AI Agent Toolkit
Installs dependencies and verifies installation
"""
import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"[*] {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        print(f"[SUCCESS] {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FAILED] {description}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is 3.7+"""
    version = sys.version_info
    print(f"\n[*] Python Version: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 7:
        print("[SUCCESS] Python version is compatible")
        return True
    else:
        print("[FAILED] Python 3.7+ required")
        return False

def main():
    print("""
    ============================================================
                                                          
              ION Kit - Quick Setup                 
                                                          
    ============================================================
    """)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if os.path.exists('requirements.txt'):
        success = run_command(
            f'"{sys.executable}" -m pip install -r requirements.txt',
            "Installing Python dependencies"
        )
        if not success:
            print("\n[WARNING] Trying with --user flag...")
            run_command(
                f'"{sys.executable}" -m pip install --user -r requirements.txt',
                "Installing Python dependencies (user mode)"
            )
    else:
        print("\n[WARNING] requirements.txt not found")
    
    # Install Playwright browsers
    print("\n" + "="*60)
    print("[*] Installing Playwright browsers...")
    print("This may take a few minutes (downloading ~200MB)")
    print("="*60)
    
    success = run_command(
        f'"{sys.executable}" -m playwright install chromium',
        "Installing Chromium browser"
    )
    
    # Install Node.js dependencies for code-tools
    code_tools_pkg = os.path.join(os.path.dirname(__file__), '..', 'tools', 'code-tools', 'package.json')
    if os.path.exists(code_tools_pkg):
        print("\n" + "="*60)
        print("[*] Installing Node.js dependencies for Code Tools")
        print("This may take a few minutes...")
        print("="*60)
        
        # Change to code-tools directory and install
        code_tools_dir = os.path.dirname(code_tools_pkg)
        success = run_command(
            f'cd "{code_tools_dir}" && npm install',
            "Installing npm packages"
        )
        
        if success:
            # Build TypeScript
            run_command(
                f'cd "{code_tools_dir}" && npm run build',
                "Building TypeScript code"
            )
        else:
            print("[WARNING] Code Tools may not work without Node.js dependencies")
            print("[INFO] Make sure Node.js and npm are installed on your system")
    else:
        print("\n[INFO] Code Tools package.json not found, skipping Node.js setup")
    
    # Verify installation
    print("\n" + "="*60)
    print("[*] Verifying Installation")
    print("="*60)
    
    try:
        from playwright.sync_api import sync_playwright
        print("[SUCCESS] Playwright installed successfully")
    except ImportError:
        print("[WARNING] Playwright not installed (optional for E2E testing)")
    
    # Final summary
    print("""
    ============================================================
                                                          
                    Setup Complete!                       
                                                          
    ============================================================
    
    Next Steps:
    
    1. Read the documentation:
       - README.md - Overview
       - docs/GUIDE.md - Detailed setup & Usage
       - docs/ARCHITECTURE.md - Full agent/skill documentation
    
    2. Test an automation script:
       python kit.py check
    
    3. Configure your AI to use the toolkit:
       - Point it to read docs/ARCHITECTURE.md on session start
       - Invoke agents: "Use the security-auditor agent"
       - Use workflows: "/create landing page"
    
    4. Explore the toolkit:
       - Agents: .agent/agents/ (16 specialists)
       - Skills: .agent/skills/ (40 domain modules)
       - Workflows: .agent/workflows/ (11 commands)
    
    Happy coding!
    """)

if __name__ == "__main__":
    main()
