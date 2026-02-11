/**
 * Project Analyzer
 * Analyze project structure, dependencies, and frameworks
 */

import { readFile } from 'fs/promises';
import { resolve } from 'path';
import { glob } from 'glob';
import type { ProjectInfo } from '../types.js';

export async function analyzeProject(options: { rootDir: string }): Promise<ProjectInfo> {
  const { rootDir } = options;

  const info: ProjectInfo = {
    name: '',
    version: '',
    description: '',
    languages: [],
    frameworks: [],
    hasTests: false,
    hasLinter: false,
    hasTypeScript: false,
    scripts: new Map(),
    dependencies: new Map(),
    devDependencies: new Map()
  };

  try {
    // Read package.json if it exists
    const packageJsonPath = resolve(rootDir, 'package.json');
    try {
      const packageJson = JSON.parse(await readFile(packageJsonPath, 'utf-8'));
      
      info.name = packageJson.name || '';
      info.version = packageJson.version || '';
      info.description = packageJson.description || '';

      // Parse scripts
      if (packageJson.scripts) {
        for (const [key, value] of Object.entries(packageJson.scripts)) {
          info.scripts.set(key, value as string);
        }
      }

      // Parse dependencies
      if (packageJson.dependencies) {
        for (const [key, value] of Object.entries(packageJson.dependencies)) {
          info.dependencies.set(key, value as string);
        }
      }

      if (packageJson.devDependencies) {
        for (const [key, value] of Object.entries(packageJson.devDependencies)) {
          info.devDependencies.set(key, value as string);
        }
      }

      // Detect frameworks from dependencies
      info.frameworks = detectFrameworks(info.dependencies, info.devDependencies);
      
      // Check for common tools
      info.hasTests = info.scripts.has('test') || info.devDependencies.has('jest') || info.devDependencies.has('mocha');
      info.hasLinter = info.devDependencies.has('eslint') || info.devDependencies.has('tslint');
      info.hasTypeScript = info.devDependencies.has('typescript') || info.dependencies.has('typescript');
    } catch {
      // No package.json
    }

    // Detect languages from file extensions
    const files = await glob('**/*', {
      cwd: rootDir,
      nodir: true,
      ignore: ['**/node_modules/**', '**/dist/**', '**/build/**']
    });

    const extensions = new Set<string>();
    for (const file of files) {
      const ext = file.split('.').pop();
      if (ext) extensions.add(ext);
    }

    info.languages = detectLanguages(extensions);

    // Check for Python requirements
    try {
      const requirementsPath = resolve(rootDir, 'requirements.txt');
      const requirements = await readFile(requirementsPath, 'utf-8');
      info.requirements = new Map();
      
      for (const line of requirements.split('\n')) {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('#')) {
          const [pkg, version] = trimmed.split('==');
          info.requirements.set(pkg.trim(), version?.trim() || 'latest');
        }
      }
    } catch {
      // No requirements.txt
    }

  } catch (error) {
    // Return partial info on error
  }

  return info;
}

function detectFrameworks(deps: Map<string, string>, devDeps: Map<string, string>): string[] {
  const frameworks: string[] = [];
  const allDeps = new Map([...deps, ...devDeps]);

  const frameworkMap: Record<string, string> = {
    'react': 'React',
    'vue': 'Vue',
    'angular': 'Angular',
    'svelte': 'Svelte',
    'next': 'Next.js',
    'nuxt': 'Nuxt',
    'express': 'Express',
    'fastify': 'Fastify',
    'nest': 'NestJS',
    'django': 'Django',
    'flask': 'Flask',
    'rails': 'Ruby on Rails'
  };

  for (const [dep] of allDeps) {
    for (const [key, name] of Object.entries(frameworkMap)) {
      if (dep.includes(key) && !frameworks.includes(name)) {
        frameworks.push(name);
      }
    }
  }

  return frameworks;
}

function detectLanguages(extensions: Set<string>): string[] {
  const languages: string[] = [];

  const langMap: Record<string, string> = {
    'ts': 'TypeScript',
    'tsx': 'TypeScript',
    'js': 'JavaScript',
    'jsx': 'JavaScript',
    'py': 'Python',
    'rb': 'Ruby',
    'go': 'Go',
    'rs': 'Rust',
    'java': 'Java',
    'cpp': 'C++',
    'c': 'C',
    'cs': 'C#',
    'php': 'PHP',
    'swift': 'Swift',
    'kt': 'Kotlin'
  };

  for (const ext of extensions) {
    const lang = langMap[ext];
    if (lang && !languages.includes(lang)) {
      languages.push(lang);
    }
  }

  return languages;
}

export function formatProjectInfo(info: ProjectInfo): string {
  let output = `📦 ${info.name} v${info.version}\n`;
  if (info.description) output += `${info.description}\n`;
  output += '\n';

  output += `Languages: ${info.languages.join(', ') || 'None detected'}\n`;
  output += `Frameworks: ${info.frameworks.join(', ') || 'None detected'}\n`;
  output += `TypeScript: ${info.hasTypeScript ? 'Yes' : 'No'}\n`;
  output += `Tests: ${info.hasTests ? 'Yes' : 'No'}\n`;
  output += `Linter: ${info.hasLinter ? 'Yes' : 'No'}\n\n`;

  output += `Dependencies: ${info.dependencies.size}\n`;
  output += `Dev Dependencies: ${info.devDependencies.size}\n\n`;

  if (info.scripts.size > 0) {
    output += 'Scripts:\n';
    for (const [name, cmd] of Array.from(info.scripts.entries()).slice(0, 5)) {
      output += `  ${name}: ${cmd}\n`;
    }
    if (info.scripts.size > 5) {
      output += `  ... and ${info.scripts.size - 5} more\n`;
    }
  }

  return output;
}
