#!/usr/bin/env python3
"""
Test Suite for ION Kit CLI
Tests all commands and validates functionality
"""
import unittest
import subprocess
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestCLICommands(unittest.TestCase):
    """Test all CLI commands"""
    
    def setUp(self):
        """Set up test environment"""
        self.root_dir = Path(__file__).parent.parent
        self.kit_py = self.root_dir / "kit.py"
        
    def run_command(self, *args):
        """Helper to run kit.py commands"""
        cmd = [sys.executable, str(self.kit_py)] + list(args)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=self.root_dir
        )
        return result
    
    def test_check_command(self):
        """Test system check command"""
        result = self.run_command("check")
        self.assertEqual(result.returncode, 0, "Check command should succeed")
        self.assertIn("Python Environment", result.stdout)
        self.assertIn("Node.js", result.stdout)
        
    def test_help_command(self):
        """Test help output"""
        result = self.run_command("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage", result.stdout.lower())
        self.assertIn("setup", result.stdout)
        self.assertIn("check", result.stdout)
        
    def test_version_script(self):
        """Test version.py script"""
        version_py = self.root_dir / "version.py"
        result = subprocess.run(
            [sys.executable, str(version_py)],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("ION Kit", result.stdout)
        self.assertIn("Version", result.stdout)

class TestToolValidation(unittest.TestCase):
    """Test tool existence validation"""
    
    def setUp(self):
        self.root_dir = Path(__file__).parent.parent
        self.tools_dir = self.root_dir / "tools"
        
    def test_required_tools_exist(self):
        """Verify all required tools exist"""
        required_tools = [
            "bg-remover/cli_remove_bg.py",
            "app-packager/make_portable.js",
            "code-tools/cli.ts",
            "scraper/scraper.py",
            "api-mocker/server.py"
        ]
        
        for tool_path in required_tools:
            full_path = self.tools_dir / tool_path
            self.assertTrue(
                full_path.exists(),
                f"Required tool not found: {tool_path}"
            )

class TestVersionConsistency(unittest.TestCase):
    """Test version consistency across files"""
    
    def setUp(self):
        self.root_dir = Path(__file__).parent.parent
        sys.path.insert(0, str(self.root_dir))
        import version
        self.version_module = version
        
    def test_version_file_exists(self):
        """Verify version.py exists"""
        version_file = self.root_dir / "version.py"
        self.assertTrue(version_file.exists())
        
    def test_version_values_valid(self):
        """Verify version values are valid"""
        self.assertIsNotNone(self.version_module.VERSION)
        self.assertIsNotNone(self.version_module.AGENT_COUNT)
        self.assertIsNotNone(self.version_module.SKILL_COUNT)
        self.assertIsNotNone(self.version_module.TOOL_COUNT)
        self.assertIsNotNone(self.version_module.WORKFLOW_COUNT)
        
        # Check that counts are reasonable
        self.assertGreater(self.version_module.AGENT_COUNT, 0)
        self.assertGreater(self.version_module.SKILL_COUNT, 0)
        self.assertGreater(self.version_module.TOOL_COUNT, 0)
        self.assertGreater(self.version_module.WORKFLOW_COUNT, 0)

if __name__ == '__main__':
    print("🧪 Running ION Kit Test Suite\n")
    unittest.main(verbosity=2)
