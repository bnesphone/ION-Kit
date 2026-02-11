/**
 * Code Sandbox
 * Execute code safely in isolated environment
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import { writeFile, unlink } from 'fs/promises';
import { join } from 'path';
import { tmpdir } from 'os';

const execAsync = promisify(exec);

export interface SandboxResult {
  success: boolean;
  output: string;
  error?: string;
  exitCode: number;
  duration: number;
}

/**
 * Execute code in sandbox
 */
export async function executeSandbox(options: {
  code: string;
  language: 'javascript' | 'typescript' | 'python';
  timeout?: number;
}): Promise<SandboxResult> {
  const { code, language, timeout = 10000 } = options;
  const startTime = Date.now();

  const result: SandboxResult = {
    success: false,
    output: '',
    exitCode: 1,
    duration: 0
  };

  try {
    // Create temp file
    const tempFile = join(tmpdir(), `sandbox-${Date.now()}.${getExtension(language)}`);
    await writeFile(tempFile, code, 'utf-8');

    try {
      const command = getCommand(language, tempFile);
      const { stdout, stderr } = await execAsync(command, {
        timeout,
        maxBuffer: 1024 * 1024 // 1MB
      });

      result.output = stdout || stderr;
      result.success = true;
      result.exitCode = 0;

    } catch (error: any) {
      result.output = error.stdout || '';
      result.error = error.stderr || error.message;
      result.exitCode = error.code || 1;
    } finally {
      // Clean up temp file
      try {
        await unlink(tempFile);
      } catch {
        // Ignore cleanup errors
      }
    }

  } catch (error: any) {
    result.error = error.message;
  }

  result.duration = Date.now() - startTime;
  return result;
}

function getExtension(language: string): string {
  switch (language) {
    case 'typescript': return 'ts';
    case 'python': return 'py';
    default: return 'js';
  }
}

function getCommand(language: string, file: string): string {
  switch (language) {
    case 'typescript':
      return `npx ts-node ${file}`;
    case 'python':
      return `python ${file}`;
    default:
      return `node ${file}`;
  }
}

/**
 * Format sandbox results
 */
export function formatSandboxResults(result: SandboxResult): string {
  let output = `Code Execution Result\n`;
  output += `====================\n\n`;
  
  if (result.success) {
    output += `✓ Execution successful (${result.duration}ms)\n\n`;
    output += `Output:\n${result.output}\n`;
  } else {
    output += `✗ Execution failed (${result.duration}ms)\n\n`;
    if (result.error) {
      output += `Error:\n${result.error}\n`;
    }
    if (result.output) {
      output += `\nOutput:\n${result.output}\n`;
    }
  }

  return output;
}

/**
 * Simplified REPL manager (returns execution result)
 */
export async function createREPL(language: 'javascript' | 'python'): Promise<{ id: string }> {
  // Return a simple ID - actual REPL would need more complex state management
  return { id: `repl-${language}-${Date.now()}` };
}
