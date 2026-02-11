/**
 * Project Analyzer
 * Analyze project structure, dependencies, and frameworks
 */

import { readFile } from 'fs/promises';
import { join } from 'path';
import { glob } from 'glob';

export interface ProjectInfo {
  name: string;
  version: string;
  description: string;
  type: 'node' | 'python' | 'unknown';
  frameworks: string[];
  languages: string[];
  dependencies: Map<string, string>;
  devDependencies: Map<string, string>;
  scripts: Map<string, string>;
  requirements?: Map<string, string>;
  fileCount: number;
  totalSize: number;
}

/**
 * Analyze project structure and metadata
 */
export async function analyzeProject(options: {
  rootDir: string;
}): Promise<ProjectInfo> {
  const { rootDir } = options;

  const info: ProjectInfo = {
    name: 'Unknown',
    version: '0.0.0',
    description: '',
    type: 'unknown',
    frameworks: [],
    languages: [],
    dependencies: new Map(),
    devDependencies: new Map(),
    scripts: new Map(),
    fileCount: 0,
    totalSize: 0
  };

  try {
    // Check for package.json
    try {
      const packagePath = join(rootDir, 'package.json');
      const packageContent = await readFile(packagePath, 'utf-8');
      const packageJson = JSON.parse(packageContent);

      info.type = 'node';
      info.name = packageJson.name || 'Unknown';
      info.version = packageJson.version || '0.0.0';
      info.description = packageJson.description || '';

      // Parse dependencies
      if (packageJson.dependencies) {
        for (const [name, version] of Object.entries(packageJson.dependencies)) {
          info.dependencies.set(name, version as string);
        }
      }

      if (packageJson.devDependencies) {
        for (const [name, version] of Object.entries(packageJson.devDependencies)) {
          info.devDependencies.set(name, version as string);
        }
      }

      if (packageJson.scripts) {
        for (const [name, script] of Object.entries(packageJson.scripts)) {
          info.scripts.set(name, script as string);
        }
      }

      // Detect frameworks
      info.frameworks = detectFrameworks(packageJson);

    } catch {
      // Not a Node project or package.json missing
    }

    // Check for Python project
    try {
      const reqPath = join(rootDir, 'requirements.txt');
      const reqContent = await readFile(reqPath, 'utf-8');
      
      info.type = info.type === 'unknown' ? 'python' : info.type;
      info.requirements = new Map();
      
      for (const line of reqContent.split('\n')) {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('#')) {
          const [pkg, version] = trimmed.split('==');
          info.requirements.set(pkg, version || 'latest');
        }
      }
    } catch {
      // Not a Python project
    }

    // Detect languages by file extensions
    const files = await glob('**/*', {
      cwd: rootDir,
      ignore: ['**/node_modules/**', '**/dist/**', '**/build/**', '**/.git/**'],
      nodir: true
    });

    info.fileCount = files.length;
    const languageSet = new Set<string>();

    for (const file of files) {
      if (file.endsWith('.ts') || file.endsWith('.tsx')) languageSet.add('TypeScript');
      else if (file.endsWith('.js') || file.endsWith('.jsx')) languageSet.add('JavaScript');
      else if (file.endsWith('.py')) languageSet.add('Python');
      else if (file.endsWith('.java')) languageSet.add('Java');
      else if (file.endsWith('.go')) languageSet.add('Go');
      else if (file.endsWith('.rs')) languageSet.add('Rust');
    }

    info.languages = Array.from(languageSet);

  } catch (error) {
    throw new Error(`Failed to analyze project: ${error}`);
  }

  return info;
}

/**
 * Detect frameworks from package.json
 */
function detectFrameworks(packageJson: any): string[] {
  const frameworks: string[] = [];
  const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };

  if (deps.react) frameworks.push('React');
  if (deps.vue) frameworks.push('Vue');
  if (deps.angular || deps['@angular/core']) frameworks.push('Angular');
  if (deps.next) frameworks.push('Next.js');
  if (deps.express) frameworks.push('Express');
  if (deps.nest || deps['@nestjs/core']) frameworks.push('NestJS');
  if (deps.typescript) frameworks.push('TypeScript');
  if (deps.jest) frameworks.push('Jest');
  if (deps.vitest) frameworks.push('Vitest');

  return frameworks;
}

/**
 * Format project info
 */
export function formatProjectInfo(info: ProjectInfo): string {
  let output = `Project Analysis\n`;
  output += `================\n\n`;
  output += `Name: ${info.name}\n`;
  output += `Version: ${info.version}\n`;
  output += `Type: ${info.type}\n`;
  output += `Languages: ${info.languages.join(', ')}\n`;
  output += `Frameworks: ${info.frameworks.join(', ') || 'None detected'}\n`;
  output += `Files: ${info.fileCount}\n`;
  output += `Dependencies: ${info.dependencies.size}\n`;
  output += `Dev Dependencies: ${info.devDependencies.size}\n`;
  
  if (info.scripts.size > 0) {
    output += `\nAvailable Scripts:\n`;
    for (const [name, script] of info.scripts) {
      output += `  ${name}: ${script}\n`;
    }
  }

  return output;
}
