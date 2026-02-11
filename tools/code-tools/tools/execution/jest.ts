/**
 * Jest Test Runner
 * Run Jest tests and collect coverage
 */

import { exec } from 'child_process';
import { promisify } from 'util';
import { resolve } from 'path';
import type { TestResult } from '../types.js';

const execAsync = promisify(exec);

export async function runJestTests(options: {
  rootDir: string;
  collectCoverage?: boolean;
  timeout?: number;
}): Promise<TestResult> {
  const { rootDir, collectCoverage = false, timeout = 60000 } = options;

  const result: TestResult = {
    success: false,
    totalTests: 0,
    passedTests: 0,
    failedTests: 0,
    skippedTests: 0,
    testFiles: [],
    failures: []
  };

  try {
    const jestPath = resolve(rootDir, 'node_modules', '.bin', 'jest');
    const coverageFlag = collectCoverage ? '--coverage --coverageReporters=json' : '';
    const command = `"${jestPath}" --json ${coverageFlag}`;

    try {
      const { stdout } = await execAsync(command, {
        cwd: rootDir,
        timeout,
        maxBuffer: 10 * 1024 * 1024
      });
      
      const jestResults = JSON.parse(stdout);
      parseJestResults(jestResults, result);

      if (collectCoverage) {
        await parseCoverage(rootDir, result);
      }
    } catch (error: any) {
      if (error.stdout) {
        const jestResults = JSON.parse(error.stdout);
        parseJestResults(jestResults, result);
      } else {
        result.failures.push({
          test: 'Jest execution',
          message: error.message || 'Failed to run tests'
        });
      }
    }
  } catch (error) {
    result.failures.push({
      test: 'Setup',
      message: 'Jest not found or error running tests'
    });
  }

  return result;
}

function parseJestResults(jestResults: any, result: TestResult): void {
  result.success = jestResults.success || false;
  result.totalTests = jestResults.numTotalTests || 0;
  result.passedTests = jestResults.numPassedTests || 0;
  result.failedTests = jestResults.numFailedTests || 0;
  result.skippedTests = jestResults.numPendingTests || 0;

  if (jestResults.testResults) {
    for (const fileResult of jestResults.testResults) {
      result.testFiles.push(fileResult.name);

      if (fileResult.assertionResults) {
        for (const assertion of fileResult.assertionResults) {
          if (assertion.status === 'failed') {
            result.failures.push({
              test: assertion.fullName || assertion.title,
              message: assertion.failureMessages?.join('\n') || 'Test failed'
            });
          }
        }
      }
    }
  }
}

async function parseCoverage(rootDir: string, result: TestResult): Promise<void> {
  try {
    const { readFile } = await import('fs/promises');
    const coveragePath = resolve(rootDir, 'coverage', 'coverage-final.json');
    const coverageData = JSON.parse(await readFile(coveragePath, 'utf-8'));

    let totalLines = 0, coveredLines = 0;
    let totalBranches = 0, coveredBranches = 0;
    let totalFunctions = 0, coveredFunctions = 0;
    let totalStatements = 0, coveredStatements = 0;

    const files = new Map();

    for (const [file, data] of Object.entries(coverageData)) {
      const fileCoverage: any = data;
      
      totalLines += Object.keys(fileCoverage.statementMap || {}).length;
      totalBranches += Object.keys(fileCoverage.branchMap || {}).length;
      totalFunctions += Object.keys(fileCoverage.fnMap || {}).length;
      totalStatements += Object.keys(fileCoverage.statementMap || {}).length;

      coveredLines += Object.values(fileCoverage.s || {}).filter((v: any) => v > 0).length;
      coveredBranches += Object.values(fileCoverage.b || {}).flat().filter((v: any) => v > 0).length;
      coveredFunctions += Object.values(fileCoverage.f || {}).filter((v: any) => v > 0).length;
      coveredStatements += Object.values(fileCoverage.s || {}).filter((v: any) => v > 0).length;

      files.set(file, fileCoverage);
    }

    result.coverage = {
      lines: totalLines > 0 ? (coveredLines / totalLines) * 100 : 0,
      branches: totalBranches > 0 ? (coveredBranches / totalBranches) * 100 : 0,
      functions: totalFunctions > 0 ? (coveredFunctions / totalFunctions) * 100 : 0,
      statements: totalStatements > 0 ? (coveredStatements / totalStatements) * 100 : 0,
      files
    };
  } catch (error) {
    // Coverage data not available
  }
}

export function formatTestResults(result: TestResult): string {
  let output = '🧪 Test Results\n\n';
  output += `Status: ${result.success ? '✅ Pass' : '❌ Fail'}\n`;
  output += `Total: ${result.totalTests}\n`;
  output += `Passed: ${result.passedTests}\n`;
  output += `Failed: ${result.failedTests}\n`;
  output += `Skipped: ${result.skippedTests}\n\n`;

  if (result.coverage) {
    output += `📊 Coverage:\n`;
    output += `  Lines: ${result.coverage.lines.toFixed(2)}%\n`;
    output += `  Branches: ${result.coverage.branches.toFixed(2)}%\n`;
    output += `  Functions: ${result.coverage.functions.toFixed(2)}%\n`;
    output += `  Statements: ${result.coverage.statements.toFixed(2)}%\n\n`;
  }

  if (result.failures.length > 0) {
    output += `❌ Failures:\n`;
    for (const failure of result.failures.slice(0, 5)) {
      output += `\n  ${failure.test}\n`;
      output += `  ${failure.message.split('\n')[0]}\n`;
    }
    if (result.failures.length > 5) {
      output += `\n  ... and ${result.failures.length - 5} more failures\n`;
    }
  }

  return output;
}
