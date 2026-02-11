/**
 * Code Formatter
 * Format code using Prettier, Black, gofmt, or rustfmt
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import { resolve } from 'path';
import type { FormatResult } from '../types.js';

const execAsync = promisify(exec);

export async function formatCode(options: {
  rootDir: string;
  formatter: 'prettier' | 'black' | 'gofmt' | 'rustfmt';
  checkOnly?: boolean;
}): Promise<FormatResult> {
  const { rootDir, formatter, checkOnly = false } = options;

  const result: FormatResult = {
    success: false,
    filesFormatted: 0,
    errors: new Map()
  };

  try {
    switch (formatter) {
      case 'prettier':
        await runPrettier(rootDir, checkOnly, result);
        break;
      case 'black':
        await runBlack(rootDir, checkOnly, result);
        break;
      case 'gofmt':
        await runGoFmt(rootDir, checkOnly, result);
        break;
      case 'rustfmt':
        await runRustFmt(rootDir, checkOnly, result);
        break;
    }
  } catch (error) {
    result.errors.set('general', error instanceof Error ? error.message : 'Unknown error');
  }

  return result;
}

async function runPrettier(rootDir: string, checkOnly: boolean, result: FormatResult): Promise<void> {
  const prettierPath = resolve(rootDir, 'node_modules', '.bin', 'prettier');
  const checkFlag = checkOnly ? '--check' : '--write';
  const command = `"${prettierPath}" ${checkFlag} "**/*.{js,ts,jsx,tsx,json,css,md}"`;

  try {
    const { stdout } = await execAsync(command, { cwd: rootDir });
    const lines = stdout.split('\n').filter(l => l.trim());
    result.filesFormatted = lines.length;
    result.success = true;
  } catch (error: any) {
    if (error.stdout) {
      const lines = error.stdout.split('\n').filter((l: string) => l.trim());
      result.filesFormatted = lines.length;
    }
    result.errors.set('prettier', error.message);
  }
}

async function runBlack(rootDir: string, checkOnly: boolean, result: FormatResult): Promise<void> {
  const checkFlag = checkOnly ? '--check' : '';
  const command = `black ${checkFlag} .`;

  try {
    const { stdout } = await execAsync(command, { cwd: rootDir });
    const match = stdout.match(/(\d+) files? (would be )?reformatted/);
    result.filesFormatted = match ? parseInt(match[1]) : 0;
    result.success = true;
  } catch (error: any) {
    result.errors.set('black', error.message);
  }
}

async function runGoFmt(rootDir: string, checkOnly: boolean, result: FormatResult): Promise<void> {
  const command = checkOnly ? 'gofmt -l .' : 'gofmt -w .';

  try {
    const { stdout } = await execAsync(command, { cwd: rootDir });
    result.filesFormatted = stdout.split('\n').filter(l => l.trim()).length;
    result.success = true;
  } catch (error: any) {
    result.errors.set('gofmt', error.message);
  }
}

async function runRustFmt(rootDir: string, checkOnly: boolean, result: FormatResult): Promise<void> {
  const checkFlag = checkOnly ? '--check' : '';
  const command = `cargo fmt ${checkFlag}`;

  try {
    await execAsync(command, { cwd: rootDir });
    result.success = true;
  } catch (error: any) {
    result.errors.set('rustfmt', error.message);
  }
}

export function formatFormatResults(result: FormatResult): string {
  let output = '🎨 Code Formatting\n\n';
  output += `Status: ${result.success ? '✅ Success' : '❌ Failed'}\n`;
  output += `Files Formatted: ${result.filesFormatted}\n\n`;

  if (result.errors.size > 0) {
    output += 'Errors:\n';
    for (const [tool, errors] of result.errors.entries()) {
      output += `  ${tool}: ${errors}\n`;
    }
  }

  return output;
}
