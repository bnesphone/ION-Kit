/**
 * ESLint Runner
 * Run ESLint and get linting errors
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export interface ESLintResult {
  success: boolean;
  errorCount: number;
  warningCount: number;
  fixableCount: number;
  errors: Map<string, ESLintError[]>;
  output: string;
}

export interface ESLintError {
  line: number;
  column: number;
  rule: string;
  message: string;
  severity: 'error' | 'warning';
  fixable: boolean;
}

/**
 * Run ESLint
 */
export async function runESLint(options: {
  rootDir: string;
  fix?: boolean;
}): Promise<ESLintResult> {
  const { rootDir, fix = false } = options;

  const result: ESLintResult = {
    success: false,
    errorCount: 0,
    warningCount: 0,
    fixableCount: 0,
    errors: new Map(),
    output: ''
  };

  try {
    const fixFlag = fix ? '--fix' : '';
    const { stdout } = await execAsync(`npx eslint . ${fixFlag} --format json`, {
      cwd: rootDir,
      maxBuffer: 10 * 1024 * 1024
    });

    result.output = stdout;
    
    // Parse JSON output
    const lintResults = JSON.parse(stdout);
    
    for (const fileResult of lintResults) {
      if (fileResult.messages.length === 0) continue;

      const errors: ESLintError[] = [];
      
      for (const msg of fileResult.messages) {
        const severity = msg.severity === 2 ? 'error' : 'warning';
        
        errors.push({
          line: msg.line,
          column: msg.column,
          rule: msg.ruleId || 'unknown',
          message: msg.message,
          severity,
          fixable: msg.fix !== undefined
        });

        if (severity === 'error') {
          result.errorCount++;
        } else {
          result.warningCount++;
        }

        if (msg.fix) {
          result.fixableCount++;
        }
      }

      result.errors.set(fileResult.filePath, errors);
    }

    result.success = result.errorCount === 0;

  } catch (error: any) {
    result.output = error.stdout || error.message;
    // Continue processing even on error
  }

  return result;
}

/**
 * Format ESLint results
 */
export function formatESLintResults(result: ESLintResult): string {
  let output = `ESLint Analysis\n`;
  output += `===============\n\n`;
  
  if (result.success) {
    output += `✓ No linting errors!\n`;
  } else {
    output += `✗ Found ${result.errorCount} errors and ${result.warningCount} warnings\n`;
    output += `${result.fixableCount} issues can be auto-fixed\n\n`;

    for (const [file, errors] of result.errors) {
      output += `${file}:\n`;
      for (const error of errors.slice(0, 5)) {
        const icon = error.severity === 'error' ? '✗' : '⚠';
        output += `  ${icon} Line ${error.line}:${error.column} - ${error.rule}: ${error.message}`;
        if (error.fixable) output += ' [fixable]';
        output += '\n';
      }
      if (errors.length > 5) {
        output += `  ... and ${errors.length - 5} more issues\n`;
      }
      output += '\n';
    }
  }

  return output;
}
