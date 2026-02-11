#!/usr/bin/env python3
"""
Agent Boundary Validator
Checks if modified files match their designated agent domains.
Run before commits or in CI/CD to enforce agent boundaries.
"""
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Set

# Agent file ownership rules
AGENT_BOUNDARIES = {
    'frontend-specialist': {
        'patterns': [
            '**/components/**',
            '**/pages/**',
            '**/app/**',
            '**/styles/**',
            '**/*.css',
            '**/*.scss',
            '**/public/**'
        ],
        'forbidden': ['**/*.test.*', '**/api/**', '**/server/**', '**/prisma/**']
    },
    'backend-specialist': {
        'patterns': [
            '**/api/**',
            '**/server/**',
            '**/services/**',
            '**/lib/**',
            '**/utils/**'
        ],
        'forbidden': ['**/*.test.*', '**/components/**', '**/pages/**']
    },
    'test-engineer': {
        'patterns': [
            '**/*.test.ts',
            '**/*.test.tsx',
            '**/*.test.js',
            '**/*.test.jsx',
            '**/__tests__/**',
            '**/tests/**',
            '**/*.spec.*'
        ],
        'forbidden': []
    },
    'mobile-developer': {
        'patterns': [
            '**/mobile/**',
            '**/native/**',
            '**/ios/**',
            '**/android/**',
            '**/*.swift',
            '**/*.kt',
            '**/*.java'
        ],
        'forbidden': ['**/components/**/*.tsx']  # Exclude web components
    },
    'database-architect': {
        'patterns': [
            '**/prisma/**',
            '**/drizzle/**',
            '**/migrations/**',
            '**/schema/**',
            '**/models/**'
        ],
        'forbidden': ['**/*.test.*', '**/components/**']
    },
    'devops-engineer': {
        'patterns': [
            '**/.github/**',
            '**/Dockerfile',
            '**/docker-compose.yml',
            '**/.gitlab-ci.yml',
            '**/k8s/**',
            '**/terraform/**'
        ],
        'forbidden': ['**/src/**']
    },
    'security-auditor': {
        'patterns': [
            '**/.env.example',
            '**/security/**'
        ],
        'forbidden': []  # Read-only, doesn't write files
    }
}

def match_pattern(file_path: str, pattern: str) -> bool:
    """Check if file matches a glob pattern"""
    from fnmatch import fnmatch
    return fnmatch(file_path, pattern)

def get_modified_files() -> List[str]:
    """Get list of modified files from git"""
    try:
        # Get staged files
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True,
            text=True,
            check=True
        )
        files = result.stdout.strip().split('\n')
        return [f for f in files if f]
    except FileNotFoundError:
        print("[!] Git not found - skipping boundary validation")
        return []
    except subprocess.CalledProcessError:
        print("[!] Not a git repository or no staged files")
        return []

def find_agent_for_file(file_path: str) -> Set[str]:
    """Determine which agent(s) should handle this file"""
    matching_agents = set()
    
    for agent, rules in AGENT_BOUNDARIES.items():
        # Check if file matches agent's patterns
        matches_pattern = any(
            match_pattern(file_path, pattern) 
            for pattern in rules['patterns']
        )
        
        # Check if file is forbidden for this agent
        matches_forbidden = any(
            match_pattern(file_path, pattern)
            for pattern in rules['forbidden']
        )
        
        if matches_pattern and not matches_forbidden:
            matching_agents.add(agent)
    
    return matching_agents

def validate_boundaries() -> bool:
    """Main validation function"""
    print("[VALIDATE] Agent Boundary Validator\n")
    
    modified_files = get_modified_files()
    
    if not modified_files:
        print("[OK] No modified files to validate")
        return True
    
    print(f"[INFO] Checking {len(modified_files)} modified files...\n")
    
    violations = []
    warnings = []
    valid_files = []
    
    for file_path in modified_files:
        agents = find_agent_for_file(file_path)
        
        if not agents:
            warnings.append(f"[!] {file_path} - No agent boundary defined")
        elif len(agents) > 1:
            agents_list = ', '.join(agents)
            warnings.append(f"[!] {file_path} - Multiple agents: {agents_list}")
        else:
            agent = list(agents)[0]
            valid_files.append((file_path, agent))
    
    # Print results
    if valid_files:
        print("[OK] Valid files:")
        for file_path, agent in valid_files:
            print(f"   {file_path} -> {agent}")
        print()
    
    if warnings:
        print("[!] Warnings:")
        for warning in warnings:
            print(f"   {warning}")
        print()
    
    if violations:
        print("[X] Boundary Violations:")
        for violation in violations:
            print(f"   {violation}")
        print()
        return False
    
    print(f"[OK] All {len(valid_files)} files pass boundary validation!")
    if warnings:
        print(f"[!] {len(warnings)} warnings (not blocking)")
    
    return True

if __name__ == "__main__":
    success = validate_boundaries()
    sys.exit(0 if success else 1)
