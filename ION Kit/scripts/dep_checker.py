#!/usr/bin/env python3
"""
ION Kit - Dependency Health Checker
Check and report on project dependencies and versions
"""
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

class DependencyChecker:
    def __init__(self, project_dir="."):
        self.project_dir = Path(project_dir).resolve()
        self.results = {
            'python': [],
            'node': [],
            'issues': [],
            'recommendations': []
        }
    
    def check_python_deps(self):
        """Check Python dependencies"""
        requirements = self.project_dir / 'requirements.txt'
        
        if not requirements.exists():
            self.results['issues'].append("No requirements.txt found")
            return
        
        print("\n[CHECK] Analyzing Python dependencies...")
        
        with open(requirements, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parse package name and version
                if '>=' in line:
                    package, version = line.split('>=')
                elif '==' in line:
                    package, version = line.split('==')
                else:
                    package = line
                    version = 'any'
                
                package = package.strip()
                version = version.strip()
                
                # Check if installed
                try:
                    result = subprocess.run(
                        [sys.executable, '-m', 'pip', 'show', package],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if result.returncode == 0:
                        installed_version = None
                        for line in result.stdout.split('\n'):
                            if line.startswith('Version:'):
                                installed_version = line.split(':')[1].strip()
                                break
                        
                        self.results['python'].append({
                            'package': package,
                            'required': version,
                            'installed': installed_version,
                            'status': 'ok'
                        })
                    else:
                        self.results['python'].append({
                            'package': package,
                            'required': version,
                            'installed': None,
                            'status': 'missing'
                        })
                        self.results['issues'].append(f"Python package missing: {package}")
                except:
                    pass
    
    def check_node_deps(self):
        """Check Node.js dependencies"""
        package_json = self.project_dir / 'package.json'
        
        if not package_json.exists():
            return
        
        print("\n[CHECK] Analyzing Node.js dependencies...")
        
        with open(package_json, 'r') as f:
            data = json.load(f)
        
        dependencies = data.get('dependencies', {})
        dev_dependencies = data.get('devDependencies', {})
        all_deps = {**dependencies, **dev_dependencies}
        
        for package, version in all_deps.items():
            node_modules = self.project_dir / 'node_modules' / package
            
            status = 'ok' if node_modules.exists() else 'missing'
            if status == 'missing':
                self.results['issues'].append(f"Node package missing: {package}")
            
            self.results['node'].append({
                'package': package,
                'required': version,
                'installed': status == 'ok',
                'status': status
            })
    
    def analyze_security(self):
        """Analyze for security issues"""
        print("\n[CHECK] Analyzing security...")
        
        # Check for outdated Python packages
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'list', '--outdated'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.stdout:
                outdated_count = len(result.stdout.strip().split('\n')) - 2  # Minus header
                if outdated_count > 0:
                    self.results['recommendations'].append(
                        f"{outdated_count} Python packages have updates available"
                    )
        except:
            pass
        
        # Check for common security files
        security_files = ['.env', '.env.local', 'secrets.json', 'credentials.json']
        for file in security_files:
            if (self.project_dir / file).exists():
                gitignore = self.project_dir / '.gitignore'
                if gitignore.exists():
                    with open(gitignore, 'r') as f:
                        if file not in f.read():
                            self.results['issues'].append(
                                f"Security file '{file}' not in .gitignore"
                            )
    
    def generate_report(self):
        """Generate dependency report"""
        print("\n" + "=" * 80)
        print("DEPENDENCY HEALTH REPORT")
        print("=" * 80)
        print(f"Project: {self.project_dir.name}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Python dependencies
        if self.results['python']:
            print("\n" + "-" * 80)
            print(f"PYTHON DEPENDENCIES ({len(self.results['python'])})")
            print("-" * 80)
            
            missing = [d for d in self.results['python'] if d['status'] == 'missing']
            ok = [d for d in self.results['python'] if d['status'] == 'ok']
            
            print(f"Installed: {len(ok)}")
            print(f"Missing: {len(missing)}")
            
            if missing:
                print("\nMissing packages:")
                for dep in missing:
                    print(f"  [X] {dep['package']} ({dep['required']})")
        
        # Node dependencies
        if self.results['node']:
            print("\n" + "-" * 80)
            print(f"NODE.JS DEPENDENCIES ({len(self.results['node'])})")
            print("-" * 80)
            
            missing = [d for d in self.results['node'] if d['status'] == 'missing']
            ok = [d for d in self.results['node'] if d['status'] == 'ok']
            
            print(f"Installed: {len(ok)}")
            print(f"Missing: {len(missing)}")
            
            if missing:
                print("\nMissing packages:")
                for dep in missing[:10]:  # Show first 10
                    print(f"  [X] {dep['package']}")
                if len(missing) > 10:
                    print(f"  ... and {len(missing) - 10} more")
        
        # Issues
        if self.results['issues']:
            print("\n" + "-" * 80)
            print(f"ISSUES FOUND ({len(self.results['issues'])})")
            print("-" * 80)
            for issue in self.results['issues']:
                print(f"  [!] {issue}")
        
        # Recommendations
        if self.results['recommendations']:
            print("\n" + "-" * 80)
            print("RECOMMENDATIONS")
            print("-" * 80)
            for rec in self.results['recommendations']:
                print(f"  [TIP] {rec}")
        
        # Summary
        print("\n" + "=" * 80)
        total_issues = len(self.results['issues'])
        if total_issues == 0:
            print("[OK] All dependencies are healthy!")
        else:
            print(f"[!] Found {total_issues} issues - review and fix")
        print("=" * 80)
    
    def fix_suggestions(self):
        """Provide fix suggestions"""
        if not self.results['issues']:
            return
        
        print("\n" + "=" * 80)
        print("FIX SUGGESTIONS")
        print("=" * 80)
        
        # Python fixes
        missing_python = [d for d in self.results['python'] if d['status'] == 'missing']
        if missing_python:
            packages = ' '.join([d['package'] for d in missing_python])
            print("\nInstall missing Python packages:")
            print(f"  pip install {packages}")
        
        # Node fixes
        missing_node = [d for d in self.results['node'] if d['status'] == 'missing']
        if missing_node:
            print("\nInstall missing Node packages:")
            print(f"  npm install")

def main():
    print("=" * 80)
    print("ION Kit - Dependency Health Checker")
    print("=" * 80)
    
    project_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    checker = DependencyChecker(project_dir)
    checker.check_python_deps()
    checker.check_node_deps()
    checker.analyze_security()
    checker.generate_report()
    checker.fix_suggestions()

if __name__ == "__main__":
    main()
