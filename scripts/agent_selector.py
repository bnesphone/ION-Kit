#!/usr/bin/env python3
"""
ION Kit - Agent Selector
Interactive agent selection and information tool
"""
import sys
from pathlib import Path

# Agent information database
AGENTS = {
    'orchestrator': {
        'name': 'Orchestrator',
        'domain': 'Management',
        'description': 'Team Lead. Coordinates multiple agents on complex tasks.',
        'use_when': 'Task requires multiple specialists or parallel analysis',
        'skills': ['parallel-agents', 'behavioral-modes', 'plan-writing']
    },
    'project-planner': {
        'name': 'Project Planner',
        'domain': 'Management',
        'description': 'The Manager. Breaks down tasks into actionable plans.',
        'use_when': 'Need to plan large features or create roadmaps',
        'skills': ['plan-writing', 'architecture', 'brainstorming']
    },
    'frontend-specialist': {
        'name': 'Frontend Specialist',
        'domain': 'Development',
        'description': 'The Designer. React, Tailwind, UI/UX implementation expert.',
        'use_when': 'Building user interfaces, components, or styling',
        'skills': ['react-patterns', 'tailwind-patterns', 'frontend-design']
    },
    'backend-specialist': {
        'name': 'Backend Specialist',
        'domain': 'Development',
        'description': 'The Architect. API, Database, Server logic expert.',
        'use_when': 'Building APIs, server logic, or database operations',
        'skills': ['api-patterns', 'nodejs-best-practices', 'database-design']
    },
    'mobile-developer': {
        'name': 'Mobile Developer',
        'domain': 'Development',
        'description': 'iOS/Android/React Native/Flutter expert.',
        'use_when': 'Building mobile applications',
        'skills': ['mobile-design', 'react-patterns']
    },
    'test-engineer': {
        'name': 'Test Engineer',
        'domain': 'Quality',
        'description': 'The QA. Writes and runs tests (Unit, Integration, E2E).',
        'use_when': 'Need to test code or improve test coverage',
        'skills': ['testing-patterns', 'webapp-testing', 'tdd-workflow']
    },
    'security-auditor': {
        'name': 'Security Auditor',
        'domain': 'Security',
        'description': 'The Shield. Finds vulnerabilities and security issues.',
        'use_when': 'Security review, vulnerability scanning, or hardening',
        'skills': ['vulnerability-scanner', 'red-team-tactics']
    },
    'debugger': {
        'name': 'Debugger',
        'domain': 'Support',
        'description': 'The Detective. Systematic root cause analysis.',
        'use_when': 'Finding and fixing bugs',
        'skills': ['systematic-debugging']
    },
    'devops-engineer': {
        'name': 'DevOps Engineer',
        'domain': 'Operations',
        'description': 'CI/CD, Docker, Cloud Infrastructure expert.',
        'use_when': 'Setting up deployments, CI/CD, or infrastructure',
        'skills': ['docker-expert', 'deployment-procedures']
    },
    'database-architect': {
        'name': 'Database Architect',
        'domain': 'Data',
        'description': 'SQL/NoSQL schema design and optimization expert.',
        'use_when': 'Designing databases or optimizing queries',
        'skills': ['database-design', 'prisma-expert']
    },
    'performance-optimizer': {
        'name': 'Performance Optimizer',
        'domain': 'Support',
        'description': 'The Speedster. Web Vitals and bundle optimization.',
        'use_when': 'Improving performance or reducing load times',
        'skills': ['performance-profiling']
    }
}

def list_agents_by_domain():
    """List all agents grouped by domain"""
    print("\n" + "=" * 60)
    print("Available ION Kit Agents (12 of 20 shown)")
    print("=" * 60)
    
    domains = {}
    for agent_id, info in AGENTS.items():
        domain = info['domain']
        if domain not in domains:
            domains[domain] = []
        domains[domain].append((agent_id, info))
    
    for domain, agents in sorted(domains.items()):
        print(f"\n[{domain.upper()}]")
        for agent_id, info in agents:
            print(f"  * {info['name']}: {info['description']}")

def show_agent_details(agent_id):
    """Show detailed information about a specific agent"""
    if agent_id not in AGENTS:
        print(f"[X] Agent '{agent_id}' not found")
        return
    
    agent = AGENTS[agent_id]
    print("\n" + "=" * 60)
    print(f"{agent['name']} Agent")
    print("=" * 60)
    print(f"Domain: {agent['domain']}")
    print(f"Description: {agent['description']}")
    print(f"\nUse When: {agent['use_when']}")
    print(f"\nSkills: {', '.join(agent['skills'])}")
    print("\nHow to Use:")
    print(f'  "Use the {agent_id} agent to [your task]"')

def recommend_agent(task_description):
    """Recommend agents based on task description"""
    task_lower = task_description.lower()
    recommendations = []
    
    keywords = {
        'frontend-specialist': ['ui', 'component', 'react', 'style', 'page', 'interface'],
        'backend-specialist': ['api', 'server', 'database', 'endpoint', 'route'],
        'mobile-developer': ['mobile', 'ios', 'android', 'app', 'native'],
        'test-engineer': ['test', 'testing', 'coverage', 'unit', 'e2e'],
        'security-auditor': ['security', 'vulnerability', 'auth', 'secure'],
        'debugger': ['bug', 'error', 'debug', 'fix', 'issue'],
        'performance-optimizer': ['slow', 'performance', 'optimize', 'speed'],
        'devops-engineer': ['deploy', 'docker', 'ci/cd', 'pipeline'],
        'database-architect': ['database', 'schema', 'query', 'sql'],
        'project-planner': ['plan', 'roadmap', 'organize', 'structure']
    }
    
    for agent_id, words in keywords.items():
        if any(word in task_lower for word in words):
            recommendations.append(agent_id)
    
    if not recommendations:
        recommendations = ['orchestrator']  # Default to orchestrator
    
    return recommendations

def main():
    print("=" * 60)
    print("ION Kit - Agent Selector")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'list':
            list_agents_by_domain()
        elif command == 'info':
            if len(sys.argv) < 3:
                print("[X] Usage: agent_selector.py info <agent-id>")
            else:
                show_agent_details(sys.argv[2])
        elif command == 'recommend':
            if len(sys.argv) < 3:
                print("[X] Usage: agent_selector.py recommend <task>")
            else:
                task = ' '.join(sys.argv[2:])
                agents = recommend_agent(task)
                print(f"\n[RECOMMEND] For task: '{task}'")
                print("\nSuggested agents:")
                for agent_id in agents:
                    agent = AGENTS[agent_id]
                    print(f"  * {agent['name']}: {agent['description']}")
        else:
            print(f"[X] Unknown command: {command}")
            print("\nUsage:")
            print("  agent_selector.py list")
            print("  agent_selector.py info <agent-id>")
            print("  agent_selector.py recommend <task>")
    else:
        # Interactive mode
        list_agents_by_domain()
        print("\n" + "=" * 60)
        print("\nCommands:")
        print("  list                - List all agents")
        print("  info <agent-id>     - Show agent details")
        print("  recommend <task>    - Get agent recommendation")

if __name__ == "__main__":
    main()
