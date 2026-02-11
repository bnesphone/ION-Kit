#!/usr/bin/env python3
"""
ION Kit - Project Statistics Analyzer
Analyze project metrics and generate reports
"""
import os
import sys
from pathlib import Path
from collections import defaultdict
import json

class ProjectAnalyzer:
    def __init__(self, root_dir="."):
        self.root = Path(root_dir).resolve()
        self.stats = {
            'files': defaultdict(int),
            'lines': defaultdict(int),
            'size': defaultdict(int),
            'total_files': 0,
            'total_lines': 0,
            'total_size': 0
        }
        
    def analyze(self):
        """Analyze the project directory"""
        print(f"[ANALYZE] Scanning project: {self.root}")
        
        extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.jsx': 'JavaScript',
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript',
            '.html': 'HTML',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.json': 'JSON',
            '.md': 'Markdown',
            '.yml': 'YAML',
            '.yaml': 'YAML',
            '.sh': 'Shell',
            '.ps1': 'PowerShell'
        }
        
        ignore_dirs = {'node_modules', '.git', 'dist', 'build', '__pycache__', 
                      '.vscode', '.idea', 'venv', 'env'}
        
        for path in self.root.rglob('*'):
            # Skip ignored directories
            if any(ignored in path.parts for ignored in ignore_dirs):
                continue
                
            if path.is_file():
                ext = path.suffix.lower()
                file_type = extensions.get(ext, 'Other')
                
                # Count file
                self.stats['files'][file_type] += 1
                self.stats['total_files'] += 1
                
                # Count size
                try:
                    size = path.stat().st_size
                    self.stats['size'][file_type] += size
                    self.stats['total_size'] += size
                except:
                    pass
                
                # Count lines for text files
                if ext in extensions:
                    try:
                        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = len(f.readlines())
                            self.stats['lines'][file_type] += lines
                            self.stats['total_lines'] += lines
                    except:
                        pass
    
    def format_size(self, bytes):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024:
                return f"{bytes:.1f}{unit}"
            bytes /= 1024
        return f"{bytes:.1f}TB"
    
    def print_report(self):
        """Print detailed statistics report"""
        print("\n" + "=" * 70)
        print("PROJECT STATISTICS REPORT")
        print("=" * 70)
        
        print(f"\nProject: {self.root.name}")
        print(f"Path: {self.root}")
        
        print("\n" + "-" * 70)
        print("OVERALL SUMMARY")
        print("-" * 70)
        print(f"Total Files: {self.stats['total_files']:,}")
        print(f"Total Lines: {self.stats['total_lines']:,}")
        print(f"Total Size: {self.format_size(self.stats['total_size'])}")
        
        if self.stats['files']:
            print("\n" + "-" * 70)
            print("BY FILE TYPE")
            print("-" * 70)
            print(f"{'Type':<15} {'Files':<10} {'Lines':<15} {'Size':<10}")
            print("-" * 70)
            
            # Sort by line count
            sorted_types = sorted(
                self.stats['files'].keys(),
                key=lambda x: self.stats['lines'][x],
                reverse=True
            )
            
            for file_type in sorted_types:
                files = self.stats['files'][file_type]
                lines = self.stats['lines'][file_type]
                size = self.stats['size'][file_type]
                
                print(f"{file_type:<15} {files:<10} {lines:<15,} {self.format_size(size):<10}")
        
        print("\n" + "=" * 70)
        
    def export_json(self, output_file):
        """Export stats to JSON"""
        data = {
            'project': str(self.root),
            'summary': {
                'total_files': self.stats['total_files'],
                'total_lines': self.stats['total_lines'],
                'total_size': self.stats['total_size']
            },
            'by_type': {}
        }
        
        for file_type in self.stats['files'].keys():
            data['by_type'][file_type] = {
                'files': self.stats['files'][file_type],
                'lines': self.stats['lines'][file_type],
                'size': self.stats['size'][file_type]
            }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n[OK] Stats exported to: {output_file}")

def main():
    print("=" * 70)
    print("ION Kit - Project Statistics Analyzer")
    print("=" * 70)
    
    # Parse arguments
    project_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    export_json = "--json" in sys.argv
    
    # Analyze
    analyzer = ProjectAnalyzer(project_dir)
    analyzer.analyze()
    analyzer.print_report()
    
    # Export if requested
    if export_json:
        json_file = Path(project_dir) / "project-stats.json"
        analyzer.export_json(json_file)
    
    print("\n[TIP] Run with --json to export stats to JSON")

if __name__ == "__main__":
    main()
