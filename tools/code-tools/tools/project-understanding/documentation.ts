/**
 * Documentation Extractor
 * Extract and parse documentation files
 */

import { readFile } from 'fs/promises';
import { join } from 'path';
import { glob } from 'glob';

export interface DocumentationResult {
  readme?: string;
  docs: Map<string, string>;
  codeComments?: Map<string, string[]>;
}

/**
 * Extract documentation from project
 */
export async function extractDocumentation(options: {
  rootDir: string;
  extractReadme?: boolean;
  extractDocs?: boolean;
}): Promise<DocumentationResult> {
  const { rootDir, extractReadme = true, extractDocs = true } = options;

  const result: DocumentationResult = {
    docs: new Map()
  };

  try {
    // Extract README
    if (extractReadme) {
      const readmeFiles = ['README.md', 'readme.md', 'README.MD', 'README'];
      for (const filename of readmeFiles) {
        try {
          const path = join(rootDir, filename);
          const content = await readFile(path, 'utf-8');
          result.readme = content;
          break;
        } catch {
          continue;
        }
      }
    }

    // Extract other documentation
    if (extractDocs) {
      const docFiles = await glob('**/*.md', {
        cwd: rootDir,
        ignore: ['**/node_modules/**', '**/dist/**'],
        nodir: true
      });

      for (const file of docFiles) {
        const content = await readFile(join(rootDir, file), 'utf-8');
        result.docs.set(file, content);
      }
    }

  } catch (error) {
    throw new Error(`Failed to extract documentation: ${error}`);
  }

  return result;
}
