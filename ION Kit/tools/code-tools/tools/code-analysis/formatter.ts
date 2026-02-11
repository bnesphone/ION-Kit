/**
 * Code Formatter
 * Format code using various formatters
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export interface FormatResult {
  success: boolean;
  filesFormatted: number;
  errors: Map<string, string>;
  output: string;
}

/**
 * Format code using specified formatter
 */
export async function formatCode(options: {
  rootDir: string;
  formatter: 'prettier' | 'black' | 'gofmt' | 'rustfmt';
  checkOnly?: boolean;
}): Promise<FormatResult> {
  const { rootDir, formatter, checkOnly = false } = options;

  const result: FormatResult = {
    success: false,
    filesFormatted: 0,
    errors: new Map(),
    output: ''
  };

  try {
    let command: string;

    switch (formatter) {
      case 'prettier':
        command = checkOnly
          ? 'npx prettier --check .'
          : 'npx prettier --write .';
        break;
      case 'black':
        command = checkOnly
          ? 'black --check .'
          : 'black .';
        break;
      case 'gofmt':
        command = checkOnly
          ? 'gofmt -l .'
          : 'gofmt -w .';
        break;
      case 'rustfmt':
        command = checkOnly
          ? 'rustfmt --check src/**/*.rs'
          : 'rustfmt src/**/*.rs';
        break;
      default:
        result.errors.set('formatter', `Unknown formatter: ${formatter}`);
        return result;
    }

    const { stdout, stderr } = await execAsync(command, { cwd: rootDir });
    result.output = stdout + stderr;
    result.success = true;

    // Count formatted files from output
    const fileMatches = result.output.match(/\.(ts|tsx|js|jsx|py|go|rs)$/gm);
    result.filesFormatted = fileMatches ? fileMatches.length : 0;

  } catch (error: any) {
    result.errors.set('execution', error.message);
    result.output = error.stdout || error.stderr || error.message;
  }

  return result;
}

export function formatFormatResults(result: FormatResult): string {
  let output = `\n=== Format Results ===\n`;
  output += `Success: ${result.success}\n`;
  output += `Files Formatted: ${result.filesFormatted}\n`;

  if (result.errors.size > 0) {
    output += `\nErrors:\n`;
    result.errors.forEach((msg, key) => {
      output += `  ${key}: ${msg}\n`;
    });
  }

  if (result.output) {
    output += `\nOutput:\n${result.output}\n`;
  }

  return output;
}
