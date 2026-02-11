#!/usr/bin/env node

/**
 * CLI Wrapper for Claude Coding Tools
 * Allows running tools directly from the command line.
 */

import {
    analyzeProject, formatProjectInfo,
    runESLint, formatESLintResults,
    runTypeCheck, formatTypeCheckResults,
    generateDependencyGraph, formatDependencyGraph,
    runJestTests, formatTestResults,
    formatCode, formatFormatResults
} from './tools/index.js';

const args = process.argv.slice(2);
const command = args[0];
const rootDir = process.cwd();

async function main() {
    if (!command) {
        console.log(`
Usage: node cli.js <command> [options]

Commands:
  analyze       Analyze project structure
  lint          Run ESLint (use --fix to autofix)
  types         Run TypeScript type checker
  deps          Generate dependency graph
  test          Run tests
  format        Format code (prettier/black)    
`);
        return;
    }

    try {
        switch (command) {
            case 'analyze':
                console.log('Analyzing project...');
                const analysis = await analyzeProject({ rootDir });
                console.log(JSON.stringify(formatProjectInfo(analysis), null, 2));
                break;

            case 'lint':
                const fix = args.includes('--fix');
                console.log(`Running ESLint${fix ? ' (fixing)' : ''}...`);
                const lintResults = await runESLint({ rootDir, fix });
                console.log(formatESLintResults(lintResults));
                break;

            case 'types':
                console.log('Checking types...');
                const typeResults = await runTypeCheck({ rootDir });
                console.log(formatTypeCheckResults(typeResults));
                break;

            case 'deps':
                console.log('Analyzing dependencies...');
                const graph = await generateDependencyGraph({ rootDir });
                console.log(formatDependencyGraph(graph));
                break;

            case 'test':
                console.log('Running tests...');
                const testResults = await runJestTests({ rootDir, timeout: 60000 });
                console.log(formatTestResults(testResults));
                break;

            case 'format':
                const formatter = args.includes('--black') ? 'black' : 'prettier';
                const formatted = await formatCode({ rootDir, formatter, checkOnly: false });
                console.log(formatFormatResults(formatted));
                break;

            default:
                console.error(`Unknown command: ${command}`);
                process.exit(1);
        }
    } catch (error) {
        console.error('Error:', error);
        process.exit(1);
    }
}

main();
