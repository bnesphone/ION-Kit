/**
 * TypeScript Type Checker
 * Run TypeScript compiler and get structured errors
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export interface TypeCheckResult {
  success: boolean;
  errorCount: number;
  warningCount: number;
  errors: TypeCheckError[];
  output: string;
}

export interface TypeCheckError {
  file: string;
  line: number;
  column: number;
  code: string;
  message: string;
  severity: 'error' | 'warning';
}

/**
 * Run TypeScript type checker
 */
export async function runTypeCheck(options: {
  rootDir: string;
}): Promise<TypeCheckResult> {
  const { rootDir } = options;

  const result: TypeCheckResult = {
    success: false,
    errorCount: 0,
    warningCount: 0,
    errors: [],
    output: ''
  };

  try {
    const { stdout, stderr } = await execAsync('npx tsc --noEmit', {
      cwd: rootDir,
      maxBuffer: 10 * 1024 * 1024 // 10MB
    });

    result.output = stdout || stderr;
    result.success = true;

  } catch (error: any) {
    // TypeScript errors are in stderr
    result.output = error.stdout || error.stderr || '';
    
    // Parse errors
    const errorRegex = /(.+?)\((\d+),(\d+)\):\s+(error|warning)\s+(TS\d+):\s*(.+)/g;
    let match;

    while ((match = errorRegex.exec(result.output)) !== null) {
      const severity = match[4] as 'error' | 'warning';
      
      result.errors.push({
        file: match[1],
        line: parseInt(match[2]),
        column: parseInt(match[3]),
        code: match[5],
        message: match[6],
        severity
      });

      if (severity === 'error') {
        result.errorCount++;
      } else {
        result.warningCount++;
      }
    }

    result.success = result.errorCount === 0;
  }

  return result;
}

/**
 * Format type check results
 */
export function formatTypeCheckResults(result: TypeCheckResult): string {
  let output = `TypeScript Type Check\n`;
  output += `====================\n\n`;
  
  if (result.success) {
    output += `✓ No type errors found!\n`;
  } else {
    output += `✗ Found ${result.errorCount} errors and ${result.warningCount} warnings\n\n`;
    
    // Group errors by file
    const errorsByFile = new Map<string, TypeCheckError[]>();
    for (const error of result.errors) {
      if (!errorsByFile.has(error.file)) {
        errorsByFile.set(error.file, []);
      }
      errorsByFile.get(error.file)!.push(error);
    }

    for (const [file, errors] of errorsByFile) {
      output += `${file}:\n`;
      for (const error of errors.slice(0, 5)) {
        output += `  Line ${error.line}:${error.column} - ${error.code}: ${error.message}\n`;
      }
      if (errors.length > 5) {
        output += `  ... and ${errors.length - 5} more errors\n`;
      }
      output += '\n';
    }
  }

  return output;
}
