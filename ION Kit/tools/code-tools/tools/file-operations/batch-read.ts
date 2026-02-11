/**
 * Batch Pattern File Reader
 * Read multiple files matching glob patterns in a single operation
 */

import { glob } from 'glob';
import { readFile } from 'fs/promises';
import { join, relative } from 'path';

export interface BatchReadOptions {
  rootDir: string;
  patterns: string | string[];
  ignore?: string[];
  maxFiles?: number;
  maxFileSize?: number; // in bytes
}

export interface FileContent {
  path: string;
  relativePath: string;
  content: string;
  size: number;
  error?: string;
}

export interface BatchReadResult {
  files: FileContent[];
  filesRead: number;
  totalSize: number;
  skipped: string[];
  errors: Map<string, string>;
}

/**
 * Read multiple files matching glob patterns
 */
export async function batchReadFiles(options: BatchReadOptions): Promise<BatchReadResult> {
  const {
    rootDir,
    patterns,
    ignore = ['**/node_modules/**', '**/.git/**'],
    maxFiles = 100,
    maxFileSize = 10 * 1024 * 1024 // 10MB default
  } = options;

  const result: BatchReadResult = {
    files: [],
    filesRead: 0,
    totalSize: 0,
    skipped: [],
    errors: new Map()
  };

  try {
    // Convert patterns to array
    const patternArray = Array.isArray(patterns) ? patterns : [patterns];
    
    // Find all matching files
    const matchedFiles = await glob(patternArray, {
      cwd: rootDir,
      ignore,
      nodir: true,
      absolute: false
    });

    // Limit number of files
    const filesToRead = matchedFiles.slice(0, maxFiles);
    if (matchedFiles.length > maxFiles) {
      result.skipped = matchedFiles.slice(maxFiles);
    }

    // Read each file
    for (const relativePath of filesToRead) {
      const absolutePath = join(rootDir, relativePath);
      
      try {
        const content = await readFile(absolutePath, 'utf-8');
        const size = Buffer.byteLength(content, 'utf-8');
        
        // Check file size
        if (size > maxFileSize) {
          result.errors.set(relativePath, `File too large: ${(size / 1024 / 1024).toFixed(2)}MB`);
          continue;
        }

        result.files.push({
          path: absolutePath,
          relativePath,
          content,
          size
        });
        
        result.filesRead++;
        result.totalSize += size;
        
      } catch (error) {
        const errorMsg = error instanceof Error ? error.message : 'Unknown error';
        result.errors.set(relativePath, errorMsg);
      }
    }

  } catch (error) {
    const errorMsg = error instanceof Error ? error.message : 'Unknown error';
    throw new Error(`Failed to read files: ${errorMsg}`);
  }

  return result;
}

/**
 * Helper: Read all files with a specific extension
 */
export async function readFilesByExtension(
  rootDir: string, 
  extension: string
): Promise<BatchReadResult> {
  const pattern = `**/*.${extension.replace(/^\./, '')}`;
  return batchReadFiles({ rootDir, patterns: pattern });
}

/**
 * Helper: Read specific files by name
 */
export async function readFilesByName(
  rootDir: string,
  filenames: string[]
): Promise<BatchReadResult> {
  const patterns = filenames.map(name => `**/${name}`);
  return batchReadFiles({ rootDir, patterns });
}
