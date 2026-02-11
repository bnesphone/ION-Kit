/**
 * Multi-File Editor
 * Apply edits to multiple files safely with preview and rollback
 */

import { readFile, writeFile, copyFile } from 'fs/promises';
import { join, dirname } from 'path';
import { mkdir } from 'fs/promises';

export interface FileEdit {
  filePath: string;
  oldText: string;
  newText: string;
}

export interface MultiEditOptions {
  rootDir: string;
  edits: FileEdit[];
  dryRun?: boolean;
  createBackups?: boolean;
}

export interface EditResult {
  filePath: string;
  success: boolean;
  changes: number;
  preview?: string;
  error?: string;
  backupPath?: string;
}

export interface MultiEditResult {
  results: EditResult[];
  totalChanges: number;
  successCount: number;
  failureCount: number;
  backupsCreated: string[];
}

/**
 * Apply edits to multiple files
 */
export async function applyMultiFileEdits(options: MultiEditOptions): Promise<MultiEditResult> {
  const {
    rootDir,
    edits,
    dryRun = false,
    createBackups = false
  } = options;

  const result: MultiEditResult = {
    results: [],
    totalChanges: 0,
    successCount: 0,
    failureCount: 0,
    backupsCreated: []
  };

  for (const edit of edits) {
    const absolutePath = join(rootDir, edit.filePath);
    const editResult: EditResult = {
      filePath: edit.filePath,
      success: false,
      changes: 0
    };

    try {
      // Read original content
      const content = await readFile(absolutePath, 'utf-8');
      
      // Count occurrences
      const regex = new RegExp(escapeRegex(edit.oldText), 'g');
      const matches = content.match(regex);
      const changeCount = matches ? matches.length : 0;
      
      if (changeCount === 0) {
        editResult.error = 'Pattern not found in file';
        result.results.push(editResult);
        result.failureCount++;
        continue;
      }

      // Apply changes
      const newContent = content.replace(regex, edit.newText);
      
      editResult.changes = changeCount;
      editResult.preview = generatePreview(content, newContent);

      // If dry run, just preview
      if (dryRun) {
        editResult.success = true;
        result.results.push(editResult);
        result.successCount++;
        result.totalChanges += changeCount;
        continue;
      }

      // Create backup if requested
      if (createBackups) {
        const backupPath = `${absolutePath}.backup`;
        await copyFile(absolutePath, backupPath);
        editResult.backupPath = backupPath;
        result.backupsCreated.push(backupPath);
      }

      // Write new content
      await writeFile(absolutePath, newContent, 'utf-8');
      
      editResult.success = true;
      result.successCount++;
      result.totalChanges += changeCount;

    } catch (error) {
      editResult.error = error instanceof Error ? error.message : 'Unknown error';
      result.failureCount++;
    }

    result.results.push(editResult);
  }

  return result;
}

/**
 * Preview edits without applying them
 */
export async function previewMultiFileEdits(options: MultiEditOptions): Promise<MultiEditResult> {
  return applyMultiFileEdits({ ...options, dryRun: true });
}

/**
 * Rollback from backup files
 */
export async function rollbackFromBackups(backupPaths: string[]): Promise<void> {
  for (const backupPath of backupPaths) {
    const originalPath = backupPath.replace('.backup', '');
    await copyFile(backupPath, originalPath);
  }
}

/**
 * Generate preview of changes
 */
function generatePreview(oldContent: string, newContent: string): string {
  const oldLines = oldContent.split('\n');
  const newLines = newContent.split('\n');
  
  let preview = '';
  const maxLines = 10;
  let changesShown = 0;

  for (let i = 0; i < Math.min(oldLines.length, newLines.length); i++) {
    if (oldLines[i] !== newLines[i] && changesShown < maxLines) {
      preview += `Line ${i + 1}:\n`;
      preview += `- ${oldLines[i]}\n`;
      preview += `+ ${newLines[i]}\n\n`;
      changesShown++;
    }
  }

  if (changesShown >= maxLines) {
    preview += '... (more changes not shown)\n';
  }

  return preview;
}

/**
 * Escape special regex characters
 */
function escapeRegex(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Validate edits before applying
 */
export function validateEdits(options: MultiEditOptions): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (!options.rootDir) {
    errors.push('rootDir is required');
  }

  if (!options.edits || options.edits.length === 0) {
    errors.push('At least one edit is required');
  }

  for (const edit of options.edits || []) {
    if (!edit.filePath) {
      errors.push('Each edit must have a filePath');
    }
    if (!edit.oldText) {
      errors.push(`Edit for ${edit.filePath}: oldText is required`);
    }
  }

  return {
    valid: errors.length === 0,
    errors
  };
}
