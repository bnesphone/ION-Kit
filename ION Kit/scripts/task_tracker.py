#!/usr/bin/env python3
"""
ION Kit - Task & Workflow Tracker
Track progress, tasks, and workflow executions
"""
import sys
import json
from pathlib import Path
from datetime import datetime
import hashlib

class TaskTracker:
    def __init__(self, project_dir="."):
        self.project_dir = Path(project_dir).resolve()
        self.tasks_file = self.project_dir / '.ionkit' / 'tasks.json'
        self.tasks_file.parent.mkdir(exist_ok=True)
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from file"""
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r') as f:
                    return json.load(f)
            except:
                return {'tasks': [], 'workflows': []}
        return {'tasks': [], 'workflows': []}
    
    def save_tasks(self):
        """Save tasks to file"""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, title, description='', agent='', priority='medium'):
        """Add a new task"""
        task_id = hashlib.md5(f"{title}{datetime.now()}".encode()).hexdigest()[:8]
        
        task = {
            'id': task_id,
            'title': title,
            'description': description,
            'agent': agent,
            'priority': priority,
            'status': 'pending',
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat(),
            'completed': None
        }
        
        self.tasks['tasks'].append(task)
        self.save_tasks()
        print(f"[OK] Task added: {task_id}")
        return task_id
    
    def list_tasks(self, status_filter=None, agent_filter=None):
        """List all tasks with optional filters"""
        tasks = self.tasks['tasks']
        
        if status_filter:
            tasks = [t for t in tasks if t['status'] == status_filter]
        
        if agent_filter:
            tasks = [t for t in tasks if t['agent'] == agent_filter]
        
        if not tasks:
            print("\n[INFO] No tasks found")
            return
        
        print("\n" + "=" * 80)
        print("TASK LIST")
        print("=" * 80)
        
        # Group by status
        statuses = {}
        for task in tasks:
            status = task['status']
            if status not in statuses:
                statuses[status] = []
            statuses[status].append(task)
        
        for status, task_list in statuses.items():
            print(f"\n[{status.upper()}] ({len(task_list)} tasks)")
            print("-" * 80)
            
            for task in task_list:
                priority_icon = {'high': '!!!', 'medium': '!!', 'low': '!'}
                icon = priority_icon.get(task['priority'], '!')
                agent_info = f" [@{task['agent']}]" if task['agent'] else ""
                
                print(f"  [{icon}] {task['id']}: {task['title']}{agent_info}")
                if task['description']:
                    print(f"      {task['description'][:60]}...")
    
    def update_task(self, task_id, **updates):
        """Update task properties"""
        for task in self.tasks['tasks']:
            if task['id'] == task_id:
                task.update(updates)
                task['updated'] = datetime.now().isoformat()
                
                if updates.get('status') == 'completed':
                    task['completed'] = datetime.now().isoformat()
                
                self.save_tasks()
                print(f"[OK] Task {task_id} updated")
                return
        
        print(f"[X] Task not found: {task_id}")
    
    def complete_task(self, task_id):
        """Mark task as completed"""
        self.update_task(task_id, status='completed')
    
    def delete_task(self, task_id):
        """Delete a task"""
        self.tasks['tasks'] = [t for t in self.tasks['tasks'] if t['id'] != task_id]
        self.save_tasks()
        print(f"[OK] Task {task_id} deleted")
    
    def get_task(self, task_id):
        """Get task details"""
        for task in self.tasks['tasks']:
            if task['id'] == task_id:
                print("\n" + "=" * 80)
                print(f"TASK: {task['title']}")
                print("=" * 80)
                print(f"ID: {task['id']}")
                print(f"Status: {task['status']}")
                print(f"Priority: {task['priority']}")
                print(f"Agent: {task['agent'] or 'Not assigned'}")
                print(f"Created: {task['created']}")
                print(f"Updated: {task['updated']}")
                if task['completed']:
                    print(f"Completed: {task['completed']}")
                print(f"\nDescription:\n{task['description']}")
                return
        
        print(f"[X] Task not found: {task_id}")
    
    def log_workflow(self, workflow_name, agent, result):
        """Log workflow execution"""
        entry = {
            'workflow': workflow_name,
            'agent': agent,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        
        self.tasks['workflows'].append(entry)
        self.save_tasks()
    
    def show_history(self, limit=10):
        """Show recent workflow history"""
        workflows = self.tasks['workflows'][-limit:]
        
        if not workflows:
            print("\n[INFO] No workflow history")
            return
        
        print("\n" + "=" * 80)
        print(f"WORKFLOW HISTORY (last {limit})")
        print("=" * 80)
        
        for entry in reversed(workflows):
            timestamp = entry['timestamp'].split('T')[0] + ' ' + entry['timestamp'].split('T')[1][:8]
            result_icon = '[OK]' if entry['result'] == 'success' else '[X]'
            print(f"{result_icon} {timestamp} | {entry['workflow']} [@{entry['agent']}]")
    
    def generate_report(self):
        """Generate progress report"""
        tasks = self.tasks['tasks']
        
        if not tasks:
            print("\n[INFO] No tasks to report")
            return
        
        total = len(tasks)
        completed = len([t for t in tasks if t['status'] == 'completed'])
        in_progress = len([t for t in tasks if t['status'] == 'in-progress'])
        pending = len([t for t in tasks if t['status'] == 'pending'])
        
        print("\n" + "=" * 80)
        print("PROJECT PROGRESS REPORT")
        print("=" * 80)
        print(f"\nTotal Tasks: {total}")
        print(f"Completed: {completed} ({completed/total*100:.1f}%)")
        print(f"In Progress: {in_progress} ({in_progress/total*100:.1f}%)")
        print(f"Pending: {pending} ({pending/total*100:.1f}%)")
        
        # By agent
        agents = {}
        for task in tasks:
            agent = task['agent'] or 'unassigned'
            if agent not in agents:
                agents[agent] = {'total': 0, 'completed': 0}
            agents[agent]['total'] += 1
            if task['status'] == 'completed':
                agents[agent]['completed'] += 1
        
        print("\nBy Agent:")
        for agent, stats in agents.items():
            completion = stats['completed'] / stats['total'] * 100 if stats['total'] > 0 else 0
            print(f"  {agent}: {stats['completed']}/{stats['total']} ({completion:.0f}%)")

def main():
    print("=" * 80)
    print("ION Kit - Task & Workflow Tracker")
    print("=" * 80)
    
    if len(sys.argv) < 2:
        print("\nCommands:")
        print("  add <title> [description] [agent] [priority]")
        print("  list [status] [agent]")
        print("  show <task-id>")
        print("  update <task-id> <status>")
        print("  complete <task-id>")
        print("  delete <task-id>")
        print("  history [limit]")
        print("  report")
        return
    
    tracker = TaskTracker()
    command = sys.argv[1]
    
    if command == 'add':
        title = sys.argv[2] if len(sys.argv) > 2 else input("Title: ")
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        agent = sys.argv[4] if len(sys.argv) > 4 else ""
        priority = sys.argv[5] if len(sys.argv) > 5 else "medium"
        tracker.add_task(title, description, agent, priority)
    
    elif command == 'list':
        status = sys.argv[2] if len(sys.argv) > 2 else None
        agent = sys.argv[3] if len(sys.argv) > 3 else None
        tracker.list_tasks(status, agent)
    
    elif command == 'show':
        if len(sys.argv) < 3:
            print("[X] Usage: task show <task-id>")
        else:
            tracker.get_task(sys.argv[2])
    
    elif command == 'update':
        if len(sys.argv) < 4:
            print("[X] Usage: task update <task-id> <status>")
        else:
            tracker.update_task(sys.argv[2], status=sys.argv[3])
    
    elif command == 'complete':
        if len(sys.argv) < 3:
            print("[X] Usage: task complete <task-id>")
        else:
            tracker.complete_task(sys.argv[2])
    
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("[X] Usage: task delete <task-id>")
        else:
            tracker.delete_task(sys.argv[2])
    
    elif command == 'history':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        tracker.show_history(limit)
    
    elif command == 'report':
        tracker.generate_report()
    
    else:
        print(f"[X] Unknown command: {command}")

if __name__ == "__main__":
    main()
