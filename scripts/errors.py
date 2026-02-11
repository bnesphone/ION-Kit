"""
Enhanced Error Handling System
Provides helpful, actionable error messages with suggestions
"""

import sys
import traceback
from typing import Optional, List, Dict
from pathlib import Path

try:
    from colorama import Fore, Style
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class Fore:
        RED = YELLOW = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = RESET_ALL = ""


class IONKitError(Exception):
    """Base exception for ION Kit errors"""
    
    def __init__(self, message: str, suggestions: Optional[List[str]] = None, 
                 details: Optional[str] = None):
        self.message = message
        self.suggestions = suggestions or []
        self.details = details
        super().__init__(message)
    
    def display(self):
        """Display error with formatting"""
        print("\n" + "="*60)
        if HAS_COLOR:
            print(f"{Fore.RED}{Style.BRIGHT}ERROR{Style.RESET_ALL}")
        else:
            print("[ERROR]")
        print("="*60)
        print(f"\n{self.message}\n")
        
        if self.details:
            print(f"Details: {self.details}\n")
        
        if self.suggestions:
            if HAS_COLOR:
                print(f"{Fore.CYAN}Suggestions:{Style.RESET_ALL}")
            else:
                print("Suggestions:")
            for i, suggestion in enumerate(self.suggestions, 1):
                print(f"  {i}. {suggestion}")
        
        print("\n" + "="*60 + "\n")


class ToolNotFoundError(IONKitError):
    """Raised when a required tool is not found"""
    
    def __init__(self, tool_name: str, tool_path: Path):
        super().__init__(
            message=f"Tool not found: {tool_name}",
            suggestions=[
                "Run 'python kit.py setup' to install all tools",
                f"Check if {tool_path} exists",
                "Verify you're in the ION Kit directory"
            ],
            details=f"Expected path: {tool_path}"
        )


class DependencyError(IONKitError):
    """Raised when a dependency is missing"""
    
    def __init__(self, dependency: str, package_type: str = "python"):
        install_cmd = {
            "python": f"pip install {dependency}",
            "node": f"npm install {dependency}",
            "system": f"Install {dependency} from your system package manager"
        }.get(package_type, f"Install {dependency}")
        
        super().__init__(
            message=f"Missing dependency: {dependency}",
            suggestions=[
                f"Run: {install_cmd}",
                "Run 'python kit.py setup' to install all dependencies",
                "Check requirements.txt or package.json"
            ]
        )


class ConfigurationError(IONKitError):
    """Raised when configuration is invalid"""
    
    def __init__(self, issue: str):
        super().__init__(
            message=f"Configuration error: {issue}",
            suggestions=[
                "Run 'python scripts/config.py validate' to check config",
                "Run 'python scripts/config.py reset' to restore defaults",
                "Check .ionkit.json for syntax errors"
            ]
        )


class CommandError(IONKitError):
    """Raised when a command fails"""
    
    def __init__(self, command: str, exit_code: int, stderr: Optional[str] = None):
        super().__init__(
            message=f"Command failed with exit code {exit_code}: {command}",
            suggestions=[
                "Check if all dependencies are installed",
                "Run with verbose mode: python kit.py -v <command>",
                "Check the command syntax with --help"
            ],
            details=stderr[:200] if stderr else None
        )


def handle_error(error: Exception, verbose: bool = False) -> int:
    """
    Global error handler
    Returns appropriate exit code
    """
    if isinstance(error, IONKitError):
        error.display()
    else:
        print("\n" + "="*60)
        if HAS_COLOR:
            print(f"{Fore.RED}{Style.BRIGHT}UNEXPECTED ERROR{Style.RESET_ALL}")
        else:
            print("[UNEXPECTED ERROR]")
        print("="*60)
        print(f"\n{type(error).__name__}: {str(error)}\n")
        
        if verbose:
            print("Traceback:")
            traceback.print_exc()
            print()
        
        if HAS_COLOR:
            print(f"{Fore.CYAN}Suggestions:{Style.RESET_ALL}")
        else:
            print("Suggestions:")
        print("  1. Run with verbose mode: python kit.py -v <command>")
        print("  2. Check if you're in the ION Kit directory")
        print("  3. Report this issue with the error message above")
        print("\n" + "="*60 + "\n")
    
    return 1


def safe_execute(func, *args, verbose: bool = False, **kwargs):
    """
    Execute a function with error handling
    Returns (success: bool, result: any)
    """
    try:
        result = func(*args, **kwargs)
        return (True, result)
    except Exception as e:
        exit_code = handle_error(e, verbose)
        return (False, None)


# Common error messages
ERRORS = {
    "tool_not_found": lambda tool: ToolNotFoundError(tool, Path(f"tools/{tool}")),
    "dep_missing": lambda dep, type="python": DependencyError(dep, type),
    "config_invalid": lambda msg: ConfigurationError(msg),
}

# Additional Error Types

class ValidationError(IONKitError):
    """Raised when validation fails"""
    
    def __init__(self, validation_type: str, failures: List[str]):
        super().__init__(
            message=f"{validation_type} validation failed",
            suggestions=[
                "Check the validation output above",
                "Run 'python kit.py lint --fix' to auto-fix some issues",
                "Run 'python kit.py validate' for full validation"
            ],
            details=f"Failed checks: {', '.join(failures[:3])}"
        )


class TemplateError(IONKitError):
    """Raised when template operations fail"""
    
    def __init__(self, template_name: str, issue: str):
        super().__init__(
            message=f"Template error: {template_name}",
            suggestions=[
                "Check if template exists in templates/ directory",
                "Run 'python kit.py templates list' to see available templates",
                "Verify template syntax and placeholders"
            ],
            details=issue
        )


class AgentError(IONKitError):
    """Raised when agent operations fail"""
    
    def __init__(self, agent_name: str, issue: str):
        super().__init__(
            message=f"Agent error: {agent_name}",
            suggestions=[
                "Run 'python kit.py agents list' to see available agents",
                "Check .agent/ directory structure",
                "Verify agent configuration"
            ],
            details=issue
        )


# Helper functions for common scenarios

def suggest_similar_commands(invalid_cmd: str, valid_commands: List[str]) -> List[str]:
    """Suggest similar commands using simple string distance"""
    def levenshtein_distance(s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    # Find commands within edit distance of 3
    suggestions = []
    for cmd in valid_commands:
        distance = levenshtein_distance(invalid_cmd.lower(), cmd.lower())
        if distance <= 3:
            suggestions.append((cmd, distance))
    
    # Sort by distance and return top 3
    suggestions.sort(key=lambda x: x[1])
    return [cmd for cmd, _ in suggestions[:3]]


def create_command_not_found_error(invalid_cmd: str, valid_commands: List[str]) -> IONKitError:
    """Create a helpful error for unknown commands"""
    similar = suggest_similar_commands(invalid_cmd, valid_commands)
    
    suggestions = []
    if similar:
        suggestions.append(f"Did you mean one of these: {', '.join(similar)}?")
    suggestions.extend([
        "Run 'python kit.py --help' to see all commands",
        "Run 'python kit.py help search <keyword>' to search commands"
    ])
    
    return IONKitError(
        message=f"Unknown command: {invalid_cmd}",
        suggestions=suggestions
    )


# Error recovery helpers

def try_auto_fix(error_type: str, context: Dict) -> bool:
    """Attempt to automatically fix common errors"""
    fixes = {
        "missing_dependency": _fix_missing_dependency,
        "invalid_config": _fix_invalid_config,
        "tool_not_found": _fix_tool_not_found,
    }
    
    if error_type in fixes:
        try:
            return fixes[error_type](context)
        except Exception:
            return False
    return False


def _fix_missing_dependency(context: Dict) -> bool:
    """Try to install missing dependency"""
    import subprocess
    dep = context.get("dependency")
    pkg_type = context.get("type", "python")
    
    if pkg_type == "python":
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            return True
        except:
            return False
    return False


def _fix_invalid_config(context: Dict) -> bool:
    """Try to fix configuration"""
    # Could implement auto-fix for common config issues
    return False


def _fix_tool_not_found(context: Dict) -> bool:
    """Try to setup missing tool"""
    import subprocess
    try:
        subprocess.check_call([sys.executable, "scripts/setup.py"])
        return True
    except:
        return False
