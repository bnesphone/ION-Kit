/**
 * Dependency Graph Generator
 * Analyze project dependencies and detect circular dependencies
 */

import { glob } from 'glob';
import { readFile } from 'fs/promises';
import { join, dirname, relative, resolve } from 'path';

export interface DependencyNode {
  file: string;
  imports: string[];
  importedBy: string[];
}

export interface DependencyGraph {
  nodes: Map<string, DependencyNode>;
  circularDependencies: string[][];
  orphanedFiles: string[];
  externalPackages: Set<string>;
  stats: {
    totalFiles: number;
    totalImports: number;
    maxDepth: number;
  };
}

/**
 * Generate dependency graph for project
 */
export async function generateDependencyGraph(options: {
  rootDir: string;
}): Promise<DependencyGraph> {
  const { rootDir } = options;

  const graph: DependencyGraph = {
    nodes: new Map(),
    circularDependencies: [],
    orphanedFiles: [],
    externalPackages: new Set(),
    stats: {
      totalFiles: 0,
      totalImports: 0,
      maxDepth: 0
    }
  };

  try {
    // Find all source files
    const files = await glob('**/*.{ts,tsx,js,jsx}', {
      cwd: rootDir,
      ignore: ['**/node_modules/**', '**/dist/**', '**/build/**'],
      nodir: true
    });

    graph.stats.totalFiles = files.length;

    // Build nodes
    for (const file of files) {
      const absolutePath = join(rootDir, file);
      const content = await readFile(absolutePath, 'utf-8');
      const imports = extractImports(content, rootDir, file);

      const node: DependencyNode = {
        file,
        imports: [],
        importedBy: []
      };

      for (const imp of imports) {
        if (imp.isExternal) {
          graph.externalPackages.add(imp.module);
        } else {
          node.imports.push(imp.module);
          graph.stats.totalImports++;
        }
      }

      graph.nodes.set(file, node);
    }

    // Build reverse dependencies
    for (const [file, node] of graph.nodes) {
      for (const imported of node.imports) {
        const importedNode = graph.nodes.get(imported);
        if (importedNode) {
          importedNode.importedBy.push(file);
        }
      }
    }

    // Detect circular dependencies
    graph.circularDependencies = detectCircularDependencies(graph.nodes);

    // Find orphaned files
    for (const [file, node] of graph.nodes) {
      if (node.importedBy.length === 0 && !file.match(/^(index|main|app)\.(ts|tsx|js|jsx)$/)) {
        graph.orphanedFiles.push(file);
      }
    }

  } catch (error) {
    throw new Error(`Failed to generate dependency graph: ${error}`);
  }

  return graph;
}

/**
 * Extract imports from file content
 */
function extractImports(content: string, rootDir: string, currentFile: string): Array<{
  module: string;
  isExternal: boolean;
}> {
  const imports: Array<{ module: string; isExternal: boolean }> = [];
  
  // Match import statements
  const importRegex = /import\s+(?:[\w\s{},*]*\s+from\s+)?['"]([^'"]+)['"]/g;
  const requireRegex = /require\s*\(\s*['"]([^'"]+)['"]\s*\)/g;
  
  let match;
  
  while ((match = importRegex.exec(content)) !== null) {
    const modulePath = match[1];
    const isExternal = !modulePath.startsWith('.') && !modulePath.startsWith('/');
    
    if (isExternal) {
      imports.push({ module: modulePath.split('/')[0], isExternal: true });
    } else {
      // Resolve relative path
      const resolvedPath = resolveModulePath(modulePath, currentFile);
      imports.push({ module: resolvedPath, isExternal: false });
    }
  }

  while ((match = requireRegex.exec(content)) !== null) {
    const modulePath = match[1];
    const isExternal = !modulePath.startsWith('.') && !modulePath.startsWith('/');
    
    if (isExternal) {
      imports.push({ module: modulePath.split('/')[0], isExternal: true });
    } else {
      const resolvedPath = resolveModulePath(modulePath, currentFile);
      imports.push({ module: resolvedPath, isExternal: false });
    }
  }

  return imports;
}

/**
 * Resolve relative module path
 */
function resolveModulePath(modulePath: string, currentFile: string): string {
  const currentDir = dirname(currentFile);
  let resolved = join(currentDir, modulePath);
  
  // Normalize path separators
  resolved = resolved.replace(/\\/g, '/');
  
  // Add extension if missing
  if (!resolved.match(/\.(ts|tsx|js|jsx)$/)) {
    // Try common extensions
    const extensions = ['.ts', '.tsx', '.js', '.jsx', '/index.ts', '/index.tsx', '/index.js'];
    for (const ext of extensions) {
      resolved = resolved + ext;
      break; // Use first extension for simplicity
    }
  }
  
  return resolved;
}

/**
 * Detect circular dependencies using DFS
 */
function detectCircularDependencies(nodes: Map<string, DependencyNode>): string[][] {
  const circular: string[][] = [];
  const visited = new Set<string>();
  const stack = new Set<string>();

  function dfs(file: string, path: string[]): void {
    if (stack.has(file)) {
      // Found circular dependency
      const cycleStart = path.indexOf(file);
      if (cycleStart !== -1) {
        circular.push([...path.slice(cycleStart), file]);
      }
      return;
    }

    if (visited.has(file)) {
      return;
    }

    visited.add(file);
    stack.add(file);

    const node = nodes.get(file);
    if (node) {
      for (const imported of node.imports) {
        dfs(imported, [...path, file]);
      }
    }

    stack.delete(file);
  }

  for (const file of nodes.keys()) {
    if (!visited.has(file)) {
      dfs(file, []);
    }
  }

  return circular;
}

/**
 * Format dependency graph for display
 */
export function formatDependencyGraph(graph: DependencyGraph): string {
  let output = `Dependency Graph Analysis\n`;
  output += `========================\n\n`;
  output += `Total Files: ${graph.stats.totalFiles}\n`;
  output += `Total Imports: ${graph.stats.totalImports}\n`;
  output += `External Packages: ${graph.externalPackages.size}\n`;
  output += `Circular Dependencies: ${graph.circularDependencies.length}\n`;
  output += `Orphaned Files: ${graph.orphanedFiles.length}\n\n`;

  if (graph.circularDependencies.length > 0) {
    output += `Circular Dependencies:\n`;
    for (const cycle of graph.circularDependencies) {
      output += `  ${cycle.join(' -> ')}\n`;
    }
    output += '\n';
  }

  if (graph.orphanedFiles.length > 0) {
    output += `Orphaned Files:\n`;
    for (const file of graph.orphanedFiles.slice(0, 10)) {
      output += `  ${file}\n`;
    }
    if (graph.orphanedFiles.length > 10) {
      output += `  ... and ${graph.orphanedFiles.length - 10} more\n`;
    }
  }

  return output;
}
