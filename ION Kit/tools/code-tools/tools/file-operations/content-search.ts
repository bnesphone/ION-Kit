/**
 * Content Search Across Files
 * Search for patterns in file contents with context
 */

import { glob } from 'glob';
import { readFile } from 'fs/promises';
import { join } from 'path';

export interface SearchOptions {
  rootDir: string;
  pattern: string;
  literalSearch?: boolean;
  contextLines?: number;
  filePattern?: string;
  maxMatches?: number;
}

export interface SearchMatch {
  line: number;
  column: number;
  text: string;
  context: {
    before: string[];
    after: string[];
  };
}

export interface SearchFileResult {
  path: string;
  relativePath: string;
  matches: SearchMatch[];
  totalMatches: number;
}

export interface SearchResult {
  files: SearchFileResult[];
  totalMatches: number;
  searchedFiles: number;
  pattern: string;
}

/**
 * Search for pattern in file contents
 */
export async function searchFileContents(options: SearchOptions): Promise<SearchResult> {
  const {
    rootDir,
    pattern,
    literalSearch = false,
    contextLines = 2,
    filePattern = '**/*',
    maxMatches = 1000
  } = options;

  const result: SearchResult = {
    files: [],
    totalMatches: 0,
    searchedFiles: 0,
    pattern
  };

  try {
    // Create regex or literal pattern
    const searchRegex = literalSearch 
      ? new RegExp(escapeRegex(pattern), 'gi')
      : new RegExp(pattern, 'gi');

    // Find files to search
    const files = await glob(filePattern, {
      cwd: rootDir,
      ignore: ['**/node_modules/**', '**/.git/**', '**/dist/**', '**/build/**'],
      nodir: true
    });

    result.searchedFiles = files.length;

    // Search each file
    for (const relativePath of files) {
      if (result.totalMatches >= maxMatches) break;

      const absolutePath = join(rootDir, relativePath);
      
      try {
        const content = await readFile(absolutePath, 'utf-8');
        const lines = content.split('\n');
        const matches: SearchMatch[] = [];

        // Search each line
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          const lineMatches = Array.from(line.matchAll(searchRegex));

          for (const match of lineMatches) {
            if (result.totalMatches >= maxMatches) break;

            matches.push({
              line: i + 1,
              column: match.index ?? 0,
              text: line.trim(),
              context: {
                before: lines.slice(Math.max(0, i - contextLines), i).map(l => l.trim()),
                after: lines.slice(i + 1, i + 1 + contextLines).map(l => l.trim())
              }
            });

            result.totalMatches++;
          }
        }

        if (matches.length > 0) {
          result.files.push({
            path: absolutePath,
            relativePath,
            matches,
            totalMatches: matches.length
          });
        }

      } catch (error) {
        // Skip files that can't be read
        continue;
      }
    }

  } catch (error) {
    const errorMsg = error instanceof Error ? error.message : 'Unknown error';
    throw new Error(`Search failed: ${errorMsg}`);
  }

  return result;
}

/**
 * Escape special regex characters for literal search
 */
function escapeRegex(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Helper: Search for imports of a specific module
 */
export async function searchForImports(
  rootDir: string,
  moduleName: string
): Promise<SearchResult> {
  const pattern = `import\\s+.*from\\s+['"]${escapeRegex(moduleName)}['"]`;
  return searchFileContents({ 
    rootDir, 
    pattern,
    filePattern: '**/*.{ts,tsx,js,jsx}'
  });
}

/**
 * Helper: Search for TODO/FIXME comments
 */
export async function searchForComments(
  rootDir: string,
  commentType: 'TODO' | 'FIXME' | 'HACK' | 'NOTE'
): Promise<SearchResult> {
  const pattern = `//\\s*${commentType}:|/\\*\\s*${commentType}:`;
  return searchFileContents({ rootDir, pattern });
}

/**
 * Format search results for display
 */
export function formatSearchResults(result: SearchResult): string {
  let output = `Found ${result.totalMatches} matches in ${result.files.length} files\n`;
  output += `Searched ${result.searchedFiles} files\n\n`;

  for (const file of result.files) {
    output += `${file.relativePath} (${file.totalMatches} matches)\n`;
    
    for (const match of file.matches.slice(0, 5)) { // Show first 5 matches per file
      output += `  Line ${match.line}: ${match.text}\n`;
    }
    
    if (file.totalMatches > 5) {
      output += `  ... and ${file.totalMatches - 5} more matches\n`;
    }
    output += '\n';
  }

  return output;
}
