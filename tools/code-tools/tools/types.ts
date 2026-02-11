/**
 * Type definitions for Claude Coding Tools
 */

// File Operations Types
export interface BatchReadOptions {
  rootDir: string;
  patterns: string | string[];
  ignore?: string | string[];
  maxFiles?: number;
}

export interface FileContent {
  path: string;
  content: string;
  size: number;
}

export interface BatchReadResult {
  files: FileContent[];
  filesRead: number;
  totalSize: number;
  errors: string[];
}

export interface SearchOptions {
  rootDir: string;
  pattern: string;
  literalSearch?: boolean;
  contextLines?: number;
  maxMatches?: number;
  filePattern?: string;
}

export interface SearchMatch {
  line: number;
  column: number;
  text: string;
  context: {
    before: string[];
    after: string[];
  };
}

export interface FileSearchResult {
  path: string;
  matches: SearchMatch[];
  totalMatches: number;
}

export interface SearchResult {
  files: FileSearchResult[];
  totalMatches: number;
  searchPattern: string;
  isLiteral: boolean;
}

export interface EditOperation {
  filePath: string;
  oldText: string;
  newText: string;
}

export interface MultiEditOptions {
  rootDir: string;
  edits: EditOperation[];
  dryRun?: boolean;
  createBackups?: boolean;
}

export interface EditResult {
  filePath: string;
  success: boolean;
  changes: number;
  error?: string;
}

export interface MultiEditResult {
  edits: EditResult[];
  totalChanges: number;
  filesModified: number;
  backupsCreated?: string[];
}

// Code Analysis Types
export interface DependencyNode {
  imports: string[];
  importedBy: string[];
}

export interface DependencyGraph {
  nodes: Map<string, DependencyNode>;
  circularDependencies: string[][];
  orphanedFiles: string[];
  externalPackages: Set<string>;
}

export interface TypeCheckResult {
  success: boolean;
  errorCount: number;
  warningCount: number;
  errors: Map<string, string[]>;
}

export interface ESLintResult {
  success: boolean;
  errorCount: number;
  warningCount: number;
  errors: Map<string, string[]>;
  fixableErrors: number;
}

export interface TestResult {
  success: boolean;
  totalTests: number;
  passedTests: number;
  failedTests: number;
  skippedTests: number;
  testFiles: string[];
  failures: Array<{ test: string; message: string }>;
  coverage?: {
    lines: number;
    branches: number;
    functions: number;
    statements: number;
    files: Map<string, any>;
  };
}

// Execution Types
export interface SandboxOptions {
  code: string;
  language: 'javascript' | 'typescript' | 'python';
  timeout?: number;
}

export interface SandboxResult {
  success: boolean;
  output: string;
  error?: string;
  executionTime: number;
}

// Project Understanding Types
export interface ProjectInfo {
  name: string;
  version: string;
  description: string;
  languages: string[];
  frameworks: string[];
  hasTests: boolean;
  hasLinter: boolean;
  hasTypeScript: boolean;
  scripts: Map<string, string>;
  dependencies: Map<string, string>;
  devDependencies: Map<string, string>;
  requirements?: Map<string, string>;
}

export interface DocumentationResult {
  readme: string | null;
  docs: Map<string, string>;
  codeComments?: Map<string, string[]>;
}

export interface GitCommit {
  hash: string;
  author: string;
  date: string;
  message: string;
}

export interface GitStatusResult {
  branch: string;
  modified: string[];
  added: string[];
  deleted: string[];
  untracked: string[];
}

export interface FormatResult {
  success: boolean;
  filesFormatted: number;
  errors: Map<string, string>;
}
