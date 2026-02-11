/**
 * Jest Test Runner
 * Run Jest tests and collect coverage
 */

import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export interface JestTestResult {
  success: boolean;
  totalTests: number;
  passedTests: number;
  failedTests: number;
  skippedTests: number;
  duration: number;
  coverage?: {
    lines: number;
    statements: number;
    functions: number;
    branches: number;
    files: Map<string, FileCoverage>;
  };
  failures: TestFailure[];
  output: string;
}

export interface TestFailure {
  test: string;
  message: string;
  stack?: string;
}

export interface FileCoverage {
  lines: number;
  statements: number;
  functions: number;
  branches: number;
}

/**
 * Run Jest tests
 */
export async function runJestTests(options: {
  rootDir: string;
  collectCoverage?: boolean;
  timeout?: number;
}): Promise<JestTestResult> {
  const { rootDir, collectCoverage = false, timeout = 60000 } = options;

  const result: JestTestResult = {
    success: false,
    totalTests: 0,
    passedTests: 0,
    failedTests: 0,
    skippedTests: 0,
    duration: 0,
    failures: [],
    output: ''
  };

  try {
    const coverageFlag = collectCoverage ? '--coverage' : '';
    const { stdout, stderr } = await execAsync(
      `npx jest --json ${coverageFlag}`,
      {
        cwd: rootDir,
        maxBuffer: 10 * 1024 * 1024,
        timeout
      }
    );

    result.output = stdout || stderr;

    // Parse JSON output
    try {
      const jestResult = JSON.parse(stdout);
      
      result.success = jestResult.success;
      result.totalTests = jestResult.numTotalTests || 0;
      result.passedTests = jestResult.numPassedTests || 0;
      result.failedTests = jestResult.numFailedTests || 0;
      result.skippedTests = jestResult.numPendingTests || 0;

      // Parse failures
      if (jestResult.testResults) {
        for (const testFile of jestResult.testResults) {
          for (const assertion of testFile.assertionResults || []) {
            if (assertion.status === 'failed') {
              result.failures.push({
                test: assertion.fullName,
                message: assertion.failureMessages?.[0] || 'Unknown failure'
              });
            }
          }
        }
      }

      // Parse coverage if available
      if (collectCoverage && jestResult.coverageMap) {
        result.coverage = parseCoverage(jestResult.coverageMap);
      }

    } catch (parseError) {
      // Continue if JSON parsing fails
    }

  } catch (error: any) {
    result.output = error.stdout || error.stderr || error.message;
    // Mark as failed but continue
    result.success = false;
  }

  return result;
}

/**
 * Parse coverage data
 */
function parseCoverage(coverageMap: any): JestTestResult['coverage'] {
  const files = new Map<string, FileCoverage>();
  let totalLines = 0, coveredLines = 0;
  let totalStatements = 0, coveredStatements = 0;
  let totalFunctions = 0, coveredFunctions = 0;
  let totalBranches = 0, coveredBranches = 0;

  for (const [file, data] of Object.entries(coverageMap)) {
    const cov = data as any;
    
    files.set(file, {
      lines: cov.lines?.pct || 0,
      statements: cov.statements?.pct || 0,
      functions: cov.functions?.pct || 0,
      branches: cov.branches?.pct || 0
    });

    totalLines += cov.lines?.total || 0;
    coveredLines += cov.lines?.covered || 0;
    totalStatements += cov.statements?.total || 0;
    coveredStatements += cov.statements?.covered || 0;
    totalFunctions += cov.functions?.total || 0;
    coveredFunctions += cov.functions?.covered || 0;
    totalBranches += cov.branches?.total || 0;
    coveredBranches += cov.branches?.covered || 0;
  }

  return {
    lines: totalLines > 0 ? (coveredLines / totalLines) * 100 : 0,
    statements: totalStatements > 0 ? (coveredStatements / totalStatements) * 100 : 0,
    functions: totalFunctions > 0 ? (coveredFunctions / totalFunctions) * 100 : 0,
    branches: totalBranches > 0 ? (coveredBranches / totalBranches) * 100 : 0,
    files
  };
}

/**
 * Format test results
 */
export function formatTestResults(result: JestTestResult): string {
  let output = `Jest Test Results\n`;
  output += `=================\n\n`;
  
  if (result.success) {
    output += `✓ All tests passed!\n`;
  } else {
    output += `✗ Some tests failed\n`;
  }

  output += `\nTests: ${result.passedTests} passed, ${result.failedTests} failed, ${result.skippedTests} skipped, ${result.totalTests} total\n`;

  if (result.coverage) {
    output += `\nCoverage:\n`;
    output += `  Lines: ${result.coverage.lines.toFixed(1)}%\n`;
    output += `  Statements: ${result.coverage.statements.toFixed(1)}%\n`;
    output += `  Functions: ${result.coverage.functions.toFixed(1)}%\n`;
    output += `  Branches: ${result.coverage.branches.toFixed(1)}%\n`;
  }

  if (result.failures.length > 0) {
    output += `\nFailures:\n`;
    for (const failure of result.failures.slice(0, 5)) {
      output += `  ✗ ${failure.test}\n`;
      output += `    ${failure.message}\n`;
    }
    if (result.failures.length > 5) {
      output += `  ... and ${result.failures.length - 5} more failures\n`;
    }
  }

  return output;
}
