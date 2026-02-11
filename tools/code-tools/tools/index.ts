/**
 * Claude Coding Tools - Main Export
 * 
 * This file exports all tools for use by the MCP server
 */

// File Operations
export {
  batchReadFiles,
  readFilesByExtension,
  readFilesByName
} from './file-operations/batch-read.js';

export {
  searchFileContents,
  searchForImports,
  searchForComments,
  formatSearchResults
} from './file-operations/content-search.js';

export {
  applyMultiFileEdits,
  previewMultiFileEdits,
  rollbackFromBackups
} from './file-operations/multi-edit.js';

// Code Analysis
export {
  generateDependencyGraph,
  formatDependencyGraph
} from './code-analysis/dependency-graph.js';

export {
  runTypeCheck,
  formatTypeCheckResults
} from './code-analysis/type-check.js';

export {
  runESLint,
  formatESLintResults
} from './code-analysis/eslint.js';

export {
  formatCode,
  formatFormatResults
} from './code-analysis/format.js';

// Execution
export {
  runJestTests,
  formatTestResults
} from './execution/jest.js';

export {
  executeSandbox,
  formatSandboxResults
} from './execution/sandbox.js';

// Project Understanding
export {
  analyzeProject,
  formatProjectInfo
} from './project-understanding/analyze.js';

export {
  extractDocumentation
} from './project-understanding/documentation.js';

export {
  getCommitHistory,
  getStatus,
  formatGitStatus
} from './project-understanding/git.js';

// Types
export * from './types.js';
