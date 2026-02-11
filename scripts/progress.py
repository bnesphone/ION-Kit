"""
Progress Bar and User Feedback Utilities
Provides visual feedback for long-running operations
"""

import sys
import time
import os
from typing import Optional, Callable
from pathlib import Path

# Try to import colorama for cross-platform colors
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    class Fore:
        GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""

# Detect if running on Windows and if console supports Unicode
IS_WINDOWS = sys.platform == 'win32'
SUPPORTS_UNICODE = False

if IS_WINDOWS:
    # Try to enable UTF-8 mode on Windows
    try:
        # Set console to UTF-8
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        SUPPORTS_UNICODE = True
    except:
        SUPPORTS_UNICODE = False
else:
    # Non-Windows systems typically support Unicode
    SUPPORTS_UNICODE = True

# Safe icon sets - use ASCII fallbacks on Windows without Unicode support
if SUPPORTS_UNICODE:
    ICONS = {
        "info": "ℹ",
        "success": "✓",
        "warning": "⚠",
        "error": "✗",
        "processing": "⚙"
    }
    SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    BAR_FILLED = "█"
    BAR_EMPTY = "░"
else:
    # ASCII fallbacks for Windows console
    ICONS = {
        "info": "i",
        "success": "+",
        "warning": "!",
        "error": "X",
        "processing": "*"
    }
    SPINNER_FRAMES = ["|", "/", "-", "\\"]
    BAR_FILLED = "#"
    BAR_EMPTY = "-"


class ProgressBar:
    """Simple, elegant progress bar with Windows compatibility"""
    
    def __init__(self, total: int, desc: str = "", width: int = 40):
        self.total = total
        self.current = 0
        self.desc = desc
        self.width = width
        self.start_time = time.time()
        
    def update(self, n: int = 1, desc: Optional[str] = None):
        """Update progress by n steps"""
        self.current = min(self.current + n, self.total)
        if desc:
            self.desc = desc
        self._render()
    
    def _render(self):
        """Render the progress bar"""
        if self.total == 0:
            percent = 0
        else:
            percent = (self.current / self.total) * 100
        
        filled = int(self.width * self.current / max(self.total, 1))
        bar = BAR_FILLED * filled + BAR_EMPTY * (self.width - filled)
        
        elapsed = time.time() - self.start_time
        if self.current > 0:
            eta = (elapsed / self.current) * (self.total - self.current)
            eta_str = f"ETA: {self._format_time(eta)}"
        else:
            eta_str = "ETA: --:--"
        
        # Color the bar based on progress
        if HAS_COLOR:
            if percent < 33:
                color = Fore.RED
            elif percent < 66:
                color = Fore.YELLOW
            else:
                color = Fore.GREEN
        else:
            color = ""
        
        try:
            sys.stdout.write(f"\r{self.desc} |{color}{bar}{Style.RESET_ALL}| {percent:5.1f}% {eta_str}")
            sys.stdout.flush()
        except (UnicodeEncodeError, UnicodeDecodeError):
            # Fallback for encoding issues
            sys.stdout.write(f"\r{self.desc} Progress: {percent:5.1f}% {eta_str}")
            sys.stdout.flush()
    
    def complete(self, message: str = "Complete!"):
        """Mark as complete and show final message"""
        self.current = self.total
        self._render()
        safe_print(f"\n{ICONS['success']} {message}", "success")
    
    def _format_time(self, seconds: float) -> str:
        """Format seconds into readable time"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            mins = seconds / 60
            return f"{mins:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"


class Spinner:
    """Simple spinner for indefinite operations with Windows compatibility"""
    
    def __init__(self, desc: str = "Processing..."):
        self.desc = desc
        self.frame_idx = 0
        self.active = False
    
    def start(self):
        """Start the spinner"""
        self.active = True
        self._spin()
    
    def _spin(self):
        """Update spinner frame"""
        if not self.active:
            return
        
        frame = SPINNER_FRAMES[self.frame_idx % len(SPINNER_FRAMES)]
        try:
            if HAS_COLOR:
                sys.stdout.write(f"\r{Fore.CYAN}{frame}{Style.RESET_ALL} {self.desc}")
            else:
                sys.stdout.write(f"\r{frame} {self.desc}")
            sys.stdout.flush()
        except (UnicodeEncodeError, UnicodeDecodeError):
            sys.stdout.write(f"\r{self.desc}...")
            sys.stdout.flush()
        self.frame_idx += 1
    
    def update(self, desc: str):
        """Update description"""
        self.desc = desc
        self._spin()
    
    def stop(self, message: str = "Done!"):
        """Stop the spinner"""
        self.active = False
        safe_print(f"\r{ICONS['success']} {message}", "success")


def safe_print(message: str, msg_type: str = "info"):
    """Print with fallback for Unicode issues"""
    try:
        if HAS_COLOR and msg_type in ICONS:
            icon = ICONS[msg_type]
            color = {
                "info": Fore.BLUE,
                "success": Fore.GREEN,
                "warning": Fore.YELLOW,
                "error": Fore.RED,
                "processing": Fore.CYAN
            }.get(msg_type, "")
            print(f"{color}{icon}{Style.RESET_ALL} {message}")
        else:
            prefix = {
                "info": "[INFO]",
                "success": "[OK]",
                "warning": "[WARN]",
                "error": "[ERROR]",
                "processing": "[...]"
            }.get(msg_type, "[*]")
            print(f"{prefix} {message}")
    except (UnicodeEncodeError, UnicodeDecodeError):
        # Final ASCII-only fallback
        prefix = {
            "info": "[INFO]",
            "success": "[OK]",
            "warning": "[WARN]",
            "error": "[ERROR]",
            "processing": "[...]"
        }.get(msg_type, "[*]")
        # Strip any remaining problematic characters
        safe_msg = message.encode('ascii', 'ignore').decode('ascii')
        print(f"{prefix} {safe_msg}")


def with_progress(func: Callable, total: int, desc: str = "Processing"):
    """Decorator to add progress bar to a function"""
    def wrapper(*args, **kwargs):
        progress = ProgressBar(total, desc)
        result = func(progress, *args, **kwargs)
        progress.complete()
        return result
    return wrapper


def status(message: str, type: str = "info"):
    """Print a status message with icon - Windows compatible"""
    safe_print(message, type)


# Test/demo
if __name__ == "__main__":
    print("Testing progress utilities...\n")
    
    # Test status messages
    status("Starting operation", "info")
    time.sleep(0.5)
    status("Processing files", "processing")
    time.sleep(0.5)
    status("Operation successful", "success")
    time.sleep(0.5)
    status("Warning: deprecated feature", "warning")
    time.sleep(0.5)
    status("Error occurred", "error")
    
    print("\n")
    
    # Test progress bar
    progress = ProgressBar(100, "Downloading")
    for i in range(100):
        time.sleep(0.02)
        progress.update(1)
    progress.complete("Download finished!")
    
    print("\n")
    
    # Test spinner (simulated)
    spinner = Spinner("Loading resources")
    spinner.start()
    for i in range(20):
        time.sleep(0.1)
        spinner._spin()
    spinner.stop("Resources loaded!")
