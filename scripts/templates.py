"""
Template Manager for ION Kit
Handles project scaffolding from templates
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


class Template:
    """Represents a project template"""
    
    def __init__(self, template_path: Path):
        with open(template_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.name = self.data.get('name', '')
        self.display_name = self.data.get('displayName', self.name)
        self.description = self.data.get('description', '')
        self.type = self.data.get('type', 'web')
        self.framework = self.data.get('framework', '')
        self.language = self.data.get('language', 'javascript')
        self.files = self.data.get('files', {})
        self.directories = self.data.get('directories', [])
    
    def render(self, variables: Dict[str, str]) -> Dict[str, str]:
        """Render template with variables"""
        rendered = {}
        
        for path, content in self.files.items():
            # Substitute variables in path
            rendered_path = self._substitute(path, variables)
            
            # Substitute variables in content
            if isinstance(content, str):
                rendered_content = self._substitute(content, variables)
            else:
                rendered_content = json.dumps(content, indent=2)
                rendered_content = self._substitute(rendered_content, variables)
            
            rendered[rendered_path] = rendered_content
        
        return rendered
    
    def _substitute(self, text: str, variables: Dict[str, str]) -> str:
        """Replace {{variable}} with actual values"""
        for key, value in variables.items():
            text = text.replace(f"{{{{{key}}}}}", value)
        return text


class TemplateManager:
    """Manages all available templates"""
    
    def __init__(self, templates_dir: Path = TEMPLATES_DIR):
        self.templates_dir = templates_dir
        self.templates: Dict[str, Template] = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load all template files"""
        if not self.templates_dir.exists():
            return
        
        for template_file in self.templates_dir.glob("*.json"):
            try:
                template = Template(template_file)
                self.templates[template.name] = template
            except Exception as e:
                print(f"Warning: Failed to load template {template_file}: {e}")
    
    def list_templates(self) -> List[Dict[str, str]]:
        """Get list of all templates"""
        return [
            {
                'name': t.name,
                'display_name': t.display_name,
                'description': t.description,
                'type': t.type,
                'framework': t.framework,
                'language': t.language
            }
            for t in self.templates.values()
        ]
    
    def get_template(self, name: str) -> Optional[Template]:
        """Get template by name"""
        return self.templates.get(name)
    
    def create_project(self, template_name: str, project_path: Path, 
                      variables: Dict[str, str]) -> bool:
        """Create a new project from template"""
        template = self.get_template(template_name)
        if not template:
            print(f"Template not found: {template_name}")
            return False
        
        # Create project directory
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Create directories
        for directory in template.directories:
            dir_path = project_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Render and write files
        rendered_files = template.render(variables)
        for file_path, content in rendered_files.items():
            full_path = project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return True


# CLI interface
if __name__ == "__main__":
    import sys
    
    manager = TemplateManager()
    
    if len(sys.argv) < 2:
        print("Available templates:")
        for template in manager.list_templates():
            print(f"  - {template['name']}: {template['description']}")
    else:
        command = sys.argv[1]
        
        if command == "list":
            for template in manager.list_templates():
                print(f"\n{template['display_name']}")
                print(f"  Type: {template['type']}")
                print(f"  Framework: {template['framework']}")
                print(f"  Language: {template['language']}")
                print(f"  {template['description']}")
        elif command == "create" and len(sys.argv) >= 5:
            template_name = sys.argv[2]
            project_name = sys.argv[3]
            project_path = Path(sys.argv[4])
            
            variables = {
                'project_name': project_name,
                'description': f'{project_name} - Created with ION Kit'
            }
            
            if manager.create_project(template_name, project_path, variables):
                print(f"Project created: {project_path}")
            else:
                print("Failed to create project")
        else:
            print("Usage:")
            print("  python templates.py list")
            print("  python templates.py create <template> <name> <path>")
