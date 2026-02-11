#!/usr/bin/env python3
"""
ION Kit Version Information
Single source of truth for version numbers and component counts.
"""

VERSION = "6.2.0"
ARCHITECTURE_VERSION = "6.0"
RULES_VERSION = "4.0"

AGENT_COUNT = 20
SKILL_COUNT = 40
TOOL_COUNT = 5
WORKFLOW_COUNT = 16
SYSTEM_GRADE = "A+ (98/100)"

def get_info():
    """Get version information as a dictionary"""
    return {
        "version": VERSION,
        "architecture_version": ARCHITECTURE_VERSION,
        "rules_version": RULES_VERSION,
        "agents": AGENT_COUNT,
        "skills": SKILL_COUNT,
        "tools": TOOL_COUNT,
        "workflows": WORKFLOW_COUNT
    }

def print_info():
    """Print version information in a formatted way"""
    info = get_info()
    print(f"""
    ===============================================
              ION Kit Version Info
    ===============================================
    
    Version: {info['version']}
    Architecture: v{info['architecture_version']}
    Rules: v{info['rules_version']}
    
    Components:
      * Agents:    {info['agents']}
      * Skills:    {info['skills']}
      * Tools:     {info['tools']}
      * Workflows: {info['workflows']}
    """)

if __name__ == "__main__":
    print_info()
