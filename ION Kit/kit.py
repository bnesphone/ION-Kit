#!/usr/bin/env python3
"""
ION Kit - Unified CLI
The single entry point for all toolkit capabilities.

Usage:
    python kit.py <command> [options]
    python kit.py --help           # Show all commands
    python kit.py <command> --help # Command-specific help

Examples:
    python kit.py setup            # Install dependencies
    python kit.py check            # System diagnostics
    python kit.py validate         # Run all checks
    python kit.py bg image.jpg     # Remove background
"""
import sys
import subprocess
import os
import argparse
from pathlib import Path

# Import version info
sys.path.insert(0, str(Path(__file__).parent))
import version

# Import new utilities
sys.path.insert(0, str(Path(__file__).parent / "scripts"))
try:
    from config import get_config
    from progress import ProgressBar, Spinner, status
    from errors import handle_error, safe_execute, IONKitError
    HAS_ENHANCEMENTS = True
except ImportError:
    HAS_ENHANCEMENTS = False
    def get_config():
        return None
    def status(msg, type="info"):
        print(f"[{type.upper()}] {msg}")

# Paths
ROOT_DIR = Path(__file__).parent.absolute()
TOOLS_DIR = ROOT_DIR / "tools"
SCRIPTS_DIR = ROOT_DIR / "scripts"

# Global verbose flag
VERBOSE = False

def safe_print(message):
    """Print with fallback for Unicode issues on Windows"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Fallback: Remove emojis and special characters
        safe_msg = message.encode('ascii', 'ignore').decode('ascii')
        print(safe_msg)

def validate_tool_exists(tool_path):
    """Check if a tool file exists before running"""
    if not tool_path.exists():
        print(f"❌ Tool not found: {tool_path}")
        print(f"💡 Run 'python kit.py setup' to install all tools")
        return False
    return True

def log_verbose(message):
    """Print message only if verbose mode is enabled"""
    if VERBOSE:
        print(f"[VERBOSE] {message}")

def run_command(cmd_list, cwd=None):
    """Run a subprocess command with enhanced feedback"""
    log_verbose(f"Running command: {' '.join(str(c) for c in cmd_list)}")
    log_verbose(f"Working directory: {cwd or 'current'}")
    
    if HAS_ENHANCEMENTS:
        status("Executing command...", "processing")
    
    try:
        # On Windows, use shell=True for npm/npx/node/python detection
        is_windows = sys.platform == "win32"
        subprocess.check_call(cmd_list, cwd=cwd, shell=is_windows)
        
        if HAS_ENHANCEMENTS:
            status("Command completed successfully", "success")
        return True
    except subprocess.CalledProcessError as e:
        if HAS_ENHANCEMENTS:
            status(f"Command failed with exit code {e.returncode}", "error")
        else:
            print(f"❌ Command failed: {' '.join(cmd_list)}")
        return False
    except KeyboardInterrupt:
        if HAS_ENHANCEMENTS:
            status("Operation cancelled by user", "warning")
        else:
            print("\n⚠️  Operation cancelled.")
        return False

def cmd_setup(args):
    """Run the setup script"""
    setup_script = SCRIPTS_DIR / "setup.py"
    print(f"🔧 Running Setup from {setup_script}...")
    run_command([sys.executable, str(setup_script)])

def cmd_analyze(args):
    """Run coding tools analysis"""
    cli_tool = TOOLS_DIR / "code-tools" / "cli.ts"
    cwd = TOOLS_DIR / "code-tools"
    
    cmd = ["npx", "ts-node", str(cli_tool), "analyze"]
    print(f"🔍 Analyzing project structure...")
    run_command(cmd, cwd=ROOT_DIR)

def cmd_codetool_relay(command_name, args):
    """Relay command to code-tools cli.ts"""
    cli_tool = TOOLS_DIR / "code-tools" / "cli.ts"
    cmd = ["npx", "ts-node", str(cli_tool), command_name]
    
    # Forward common flags
    if hasattr(args, 'check') and args.check:
        cmd.append("--check")
        
    print(f"🔧 Running {command_name}...")
    run_command(cmd, cwd=ROOT_DIR)

def cmd_lint(args):
    """Run coding tools linter"""
    cli_tool = TOOLS_DIR / "code-tools" / "cli.ts"
    cmd = ["npx", "ts-node", str(cli_tool), "lint"]
    if args.fix:
        cmd.append("--fix")
    
    print(f"🧹 Linting code...")
    run_command(cmd, cwd=ROOT_DIR)

def cmd_bg(args):
    """Run background remover"""
    bg_tool = TOOLS_DIR / "bg-remover" / "cli_remove_bg.py"
    
    if not validate_tool_exists(bg_tool):
        return
    
    cmd = [sys.executable, str(bg_tool)]
    if args.input:
        cmd.append(args.input)
    if args.output:
        cmd.append(args.output)
    if args.model:
        cmd += ["--model", args.model]
    
    # Pass through other flags if user used -- (not fully implemented in this simple wrapper)
    
    print(f"🎨 Running Background Remover...")
    run_command(cmd, cwd=ROOT_DIR)

def cmd_pack(args):
    """Run app packager"""
    pack_tool = TOOLS_DIR / "app-packager" / "make_portable.js"
    
    if not validate_tool_exists(pack_tool):
        return
    
    cmd = ["node", str(pack_tool)]
    if args.source:
        cmd += ["--source", args.source]
    if args.name:
        cmd += ["--name", args.name]
        
    print(f"📦 Packaging application...")
    run_command(cmd, cwd=ROOT_DIR)

def cmd_scrape(args):
    """Run web scraper"""
    scraper_tool = TOOLS_DIR / "scraper" / "scraper.py"
    
    if not validate_tool_exists(scraper_tool):
        return
    
    cmd = [sys.executable, str(scraper_tool), args.url]
    if args.out:
        cmd += ["--out", args.out]
        
    print(f"🌐 Scraping {args.url}...")
    run_command(cmd, cwd=ROOT_DIR)

def cmd_mock(args):
    """Run API mocker"""
    mocker_tool = TOOLS_DIR / "api-mocker" / "server.py"
    
    if not validate_tool_exists(mocker_tool):
        return
    
    cmd = [sys.executable, str(mocker_tool), args.schema]
    if args.port:
        cmd += ["--port", str(args.port)]
        
    print(f"🧪 Starting Mock API from {args.schema}...")
    run_command(cmd, cwd=ROOT_DIR)

def cmd_test(args):
    """Run system diagnostics"""
    safe_print("\n[TEST] ION Kit System Check\n")
    
    # Check 1: Python
    safe_print(f"[OK] Python Environment: {sys.version.split()[0]}")
    
    # Check 2: Node
    try:
        node_v = subprocess.check_output(["node", "-v"], shell=True).decode().strip()
        safe_print(f"[OK] Node.js: {node_v}")
    except:
        safe_print(f"[X] Node.js: Not found")

    # Check 3: Playwright exist?
    try:
        import playwright
        safe_print(f"[OK] Playwright: Installed")
    except:
        safe_print(f"[!] Playwright: Not installed (Functional but limited)")

    # Check 4: Tools existence
    tools_check = [
        ("Background Remover", TOOLS_DIR / "bg-remover" / "cli_remove_bg.py"),
        ("App Packager", TOOLS_DIR / "app-packager" / "make_portable.js"),
        ("Code Tools", TOOLS_DIR / "code-tools" / "cli.ts"),
        ("Scraper", TOOLS_DIR / "scraper" / "scraper.py"),
        ("API Mocker", TOOLS_DIR / "api-mocker" / "server.py")
    ]
    
    for name, path in tools_check:
        if path.exists():
            safe_print(f"[OK] Tool Found: {name}")
        else:
            safe_print(f"[X] Tool Missing: {name} at {path}")

def cmd_validate_boundaries(args):
    """Run agent boundary validation"""
    validate_script = SCRIPTS_DIR / "validate_boundaries.py"
    
    if not validate_script.exists():
        print("❌ Boundary validator not found")
        return
    
    print("🔍 Running Agent Boundary Validation...")
    run_command([sys.executable, str(validate_script)], cwd=ROOT_DIR)

def cmd_validate(args):
    """Run all validation checks"""
    print("\n🔍 ION Kit Validation Suite\n")
    print("=" * 60)
    
    # 1. Run boundary validation
    print("\n1️⃣ Agent Boundary Validation")
    print("-" * 60)
    cmd_validate_boundaries(args)
    
    # 2. Run tests
    print("\n2️⃣ Running Test Suite")
    print("-" * 60)
    test_runner = ROOT_DIR / "tests" / "run_tests.py"
    if test_runner.exists():
        run_command([sys.executable, str(test_runner)], cwd=ROOT_DIR)
    else:
        print("⚠️  Test suite not found")
    
    print("\n" + "=" * 60)
    print("✅ Validation complete!")

def cmd_clean(args):
    """Run cleanup utility"""
    cleanup_script = SCRIPTS_DIR / "cleanup.py"
    
    if not cleanup_script.exists():
        print("❌ Cleanup script not found")
        return
    
    safe_print("[CLEAN] Running cleanup utility...")
    run_command([sys.executable, str(cleanup_script)], cwd=ROOT_DIR)

def cmd_init(args):
    """Initialize new project"""
    init_script = SCRIPTS_DIR / "init_project.py"
    
    if not init_script.exists():
        safe_print("[X] Project init script not found")
        return
    
    safe_print("[INIT] Starting project wizard...")
    run_command([sys.executable, str(init_script)], cwd=ROOT_DIR)

def cmd_agents(args):
    """Show agent information"""
    agent_script = SCRIPTS_DIR / "agent_selector.py"
    
    if not agent_script.exists():
        safe_print("[X] Agent selector not found")
        return
    
    cmd = [sys.executable, str(agent_script)]
    if hasattr(args, 'subcommand') and args.subcommand:
        cmd.append(args.subcommand)
        if hasattr(args, 'args') and args.args:
            cmd.extend(args.args)
    
    run_command(cmd, cwd=ROOT_DIR)

def cmd_stats(args):
    """Show project statistics"""
    stats_script = SCRIPTS_DIR / "project_stats.py"
    
    if not stats_script.exists():
        safe_print("[X] Stats script not found")
        return
    
    cmd = [sys.executable, str(stats_script)]
    if hasattr(args, 'path'):
        cmd.append(args.path)
    if hasattr(args, 'json') and args.json:
        cmd.append("--json")
    
    run_command(cmd, cwd=ROOT_DIR)

def cmd_config(args):
    """Configuration management"""
    if hasattr(args, 'subcommand') and args.subcommand == 'validate':
        # Use dedicated validator
        validator_script = SCRIPTS_DIR / "config_validator.py"
        cmd = [sys.executable, str(validator_script)]
        if hasattr(args, 'fix') and args.fix:
            cmd.append("--fix")
        run_command(cmd, cwd=ROOT_DIR)
        return
    
    if not HAS_ENHANCEMENTS:
        print("Config system requires enhanced modules")
        return
    
    config = get_config()
    
    if hasattr(args, 'subcommand') and args.subcommand:
        if args.subcommand == 'show':
            config.show()
        elif args.subcommand == 'get' and hasattr(args, 'key'):
            value = config.get(args.key)
            print(f"{args.key}: {value}")
        elif args.subcommand == 'set' and hasattr(args, 'key') and hasattr(args, 'value'):
            config.set(args.key, args.value)
            if config.save():
                status(f"Set {args.key} = {args.value}", "success")
            else:
                status("Failed to save configuration", "error")
        elif args.subcommand == 'reset':
            config.reset()
            if config.save():
                status("Configuration reset to defaults", "success")
            else:
                status("Failed to save configuration", "error")
    else:
        config.show()

def cmd_templates(args):
    """Template management"""
    templates_script = SCRIPTS_DIR / "templates.py"
    
    if not templates_script.exists():
        status("Templates system not found", "error")
        return
    
    cmd = [sys.executable, str(templates_script)]
    if hasattr(args, 'subcommand') and args.subcommand:
        cmd.append(args.subcommand)
        if hasattr(args, 'args') and args.args:
            cmd.extend(args.args)
    
    run_command(cmd, cwd=ROOT_DIR)

def cmd_tasks(args):
    """Task tracking"""
    task_script = SCRIPTS_DIR / "task_tracker.py"
    
    if not task_script.exists():
        safe_print("[X] Task tracker not found")
        return
    
    cmd = [sys.executable, str(task_script)]
    if hasattr(args, 'subcommand') and args.subcommand:
        cmd.append(args.subcommand)
        if hasattr(args, 'args') and args.args:
            cmd.extend(args.args)
    
    run_command(cmd, cwd=ROOT_DIR)

def cmd_deps(args):
    """Check dependencies"""
    deps_script = SCRIPTS_DIR / "dep_checker.py"
    
    if not deps_script.exists():
        safe_print("[X] Dependency checker not found")
        return
    
    cmd = [sys.executable, str(deps_script)]
    if hasattr(args, 'path'):
        cmd.append(args.path)
    
    run_command(cmd, cwd=ROOT_DIR)

def main():
    global VERBOSE
    
    parser = argparse.ArgumentParser(
        prog="kit",
        description=f"ION Kit v{version.VERSION} - AI Development Studio",
        epilog=f"""
Examples:
  %(prog)s setup              Install all dependencies
  %(prog)s check              System health check
  %(prog)s validate           Run all validations
  %(prog)s bg image.jpg       Remove background from image
  %(prog)s -v analyze         Analyze with verbose output

For more info: python %(prog)s <command> --help
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Global flags
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Enable verbose output')
    parser.add_argument('--version', action='version',
                       version=f'ION Kit v{version.VERSION}')
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Setup
    setup_parser = subparsers.add_parser("setup", 
        aliases=['install'],
        help="Initialize environment and dependencies")

    # Analyze
    analyze_parser = subparsers.add_parser("analyze",
        aliases=['analyse'],
        help="Analyze project structure")

    # Lint
    lint_parser = subparsers.add_parser("lint",
        aliases=['check-style'],
        help="Lint and fix code")
    lint_parser.add_argument("--fix", action="store_true", help="Auto-fix issues")

    # Background Remover
    bg_parser = subparsers.add_parser("bg",
        aliases=['remove-bg', 'rembg'],
        help="Remove image backgrounds")
    bg_parser.add_argument("input", nargs="?", help="Input file or folder")
    bg_parser.add_argument("output", nargs="?", help="Output file or folder")
    bg_parser.add_argument("--model", default="u2net", help="Model type")

    # Packager
    pack_parser = subparsers.add_parser("pack",
        aliases=['package', 'build-exe'],
        help="Create portable .exe")
    pack_parser.add_argument("--source", required=True, help="Source directory")
    pack_parser.add_argument("--name", required=True, help="App Name")

    # Scraper
    scrape_parser = subparsers.add_parser("scrape",
        aliases=['fetch', 'download'],
        help="Convert URL to Markdown")
    scrape_parser.add_argument("url", help="URL to scrape")
    scrape_parser.add_argument("--out", help="Output file")

    # Mocker
    mock_parser = subparsers.add_parser("mock",
        aliases=['mock-api', 'serve'],
        help="Run mock API server")
    mock_parser.add_argument("schema", help="JSON schema file")
    mock_parser.add_argument("--port", type=int, default=8000, help="Port number")
    
    # Extra Code Tools
    test_parser = subparsers.add_parser("test",
        aliases=['run-tests'],
        help="Run project tests")
    deps_parser = subparsers.add_parser("deps",
        aliases=['dependencies'],
        help="Generate dependency graph")
    
    format_parser = subparsers.add_parser("format",
        aliases=['fmt'],
        help="Format code")
    format_parser.add_argument("--check", action="store_true", help="Check only")

    # System Check
    check_parser = subparsers.add_parser("check",
        aliases=['diagnose', 'health'],
        help="Run system diagnostics")
    
    # Cleanup
    clean_parser = subparsers.add_parser("clean",
        aliases=['cleanup', 'clear'],
        help="Remove temporary files and caches")
    
    # Validation
    validate_parser = subparsers.add_parser("validate",
        aliases=['verify'],
        help="Run all validation checks (boundaries, tests)")
    validate_boundaries_parser = subparsers.add_parser("validate-boundaries",
        aliases=['check-boundaries'],
        help="Validate agent file boundaries")
    
    # New Features
    init_parser = subparsers.add_parser("init",
        aliases=['new', 'create-project'],
        help="Initialize new project (wizard)")
    
    agents_parser = subparsers.add_parser("agents",
        aliases=['agent'],
        help="Agent selector and information")
    agents_parser.add_argument("subcommand", nargs='?', choices=['list', 'info', 'recommend'],
                              help="Subcommand")
    agents_parser.add_argument("args", nargs='*', help="Additional arguments")
    
    stats_parser = subparsers.add_parser("stats",
        aliases=['statistics', 'metrics'],
        help="Analyze project statistics")
    stats_parser.add_argument("path", nargs='?', default=".", help="Project path")
    stats_parser.add_argument("--json", action="store_true", help="Export to JSON")
    
    # Configuration management
    config_parser = subparsers.add_parser("config",
        aliases=['cfg', 'settings'],
        help="Manage configuration")
    config_parser.add_argument("subcommand", nargs='?', 
                              choices=['show', 'get', 'set', 'reset', 'validate'],
                              help="Config subcommand")
    config_parser.add_argument("key", nargs='?', help="Config key (for get/set)")
    config_parser.add_argument("value", nargs='?', help="Config value (for set)")
    config_parser.add_argument("--fix", action="store_true", help="Auto-fix configuration issues (for validate)")
    
    # Template management
    templates_parser = subparsers.add_parser("templates",
        aliases=['template', 'tpl'],
        help="Manage project templates")
    templates_parser.add_argument("subcommand", nargs='?', choices=['list', 'create'],
                                 help="Template subcommand")
    templates_parser.add_argument("args", nargs='*', help="Additional arguments")

    args = parser.parse_args()
    
    # Set global verbose flag
    if hasattr(args, 'verbose') and args.verbose:
        VERBOSE = True
        log_verbose("Verbose mode enabled")

    if args.command in ["setup", "install"]:
        cmd_setup(args)
    elif args.command in ["init", "new", "create-project"]:
        cmd_init(args)
    elif args.command in ["analyze", "analyse"]:
        cmd_analyze(args)
    elif args.command in ["lint", "check-style"]:
        cmd_lint(args)
    elif args.command in ["test", "run-tests"]:
        cmd_codetool_relay("test", args)
    elif args.command in ["deps", "dependencies"]:
        cmd_codetool_relay("deps", args)
    elif args.command in ["format", "fmt"]:
        cmd_codetool_relay("format", args)    
    elif args.command in ["bg", "remove-bg", "rembg"]:
        cmd_bg(args)
    elif args.command in ["pack", "package", "build-exe"]:
        cmd_pack(args)
    elif args.command in ["scrape", "fetch", "download"]:
        cmd_scrape(args)
    elif args.command in ["mock", "mock-api", "serve"]:
        cmd_mock(args)
    elif args.command in ["check", "diagnose", "health"]:
        cmd_test(args)
    elif args.command in ["clean", "cleanup", "clear"]:
        cmd_clean(args)
    elif args.command in ["validate", "verify"]:
        cmd_validate(args)
    elif args.command in ["validate-boundaries", "check-boundaries"]:
        cmd_validate_boundaries(args)
    elif args.command in ["init", "new", "create-project"]:
        cmd_init(args)
    elif args.command in ["agents", "agent"]:
        cmd_agents(args)
    elif args.command in ["stats", "statistics", "metrics"]:
        cmd_stats(args)
    elif args.command in ["config", "cfg", "settings"]:
        cmd_config(args)
    elif args.command in ["templates", "template", "tpl"]:
        cmd_templates(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
