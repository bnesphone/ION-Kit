#!/usr/bin/env node

/**
 * Claude Coding Tools - MCP Server
 * 
 * This MCP server exposes all 13 coding tools to Claude Desktop
 * allowing Claude to use them directly in conversations.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

// Import all tools
import {
  batchReadFiles,
  searchFileContents,
  searchForImports,
  searchForComments,
  applyMultiFileEdits,
  previewMultiFileEdits,
  generateDependencyGraph,
  formatDependencyGraph,
  runTypeCheck,
  formatTypeCheckResults,
  runESLint,
  formatESLintResults,
  runJestTests,
  formatTestResults,
  executeSandbox,
  formatSandboxResults,
  analyzeProject,
  formatProjectInfo,
  extractDocumentation,
  getCommitHistory,
  getStatus,
  formatGitStatus,
  formatCode,
  formatFormatResults
} from './tools/index.js';

// Create server
const server = new Server(
  {
    name: 'claude-coding-tools',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      // File Operations
      {
        name: 'batch_read_files',
        description: 'Read multiple files matching glob patterns. Eliminates file-by-file reading.',
        inputSchema: {
          type: 'object',
          properties: {
            rootDir: { type: 'string', description: 'Root directory' },
            patterns: { 
              type: 'array', 
              items: { type: 'string' },
              description: 'Glob patterns like "**/*.ts"'
            },
            maxFiles: { type: 'number', description: 'Max files (default: 100)' }
          },
          required: ['rootDir', 'patterns']
        }
      },
      {
        name: 'search_contents',
        description: 'Search file contents with context. Find code patterns instantly.',
        inputSchema: {
          type: 'object',
          properties: {
            rootDir: { type: 'string' },
            pattern: { type: 'string' },
            literalSearch: { type: 'boolean' },
            contextLines: { type: 'number' }
          },
          required: ['rootDir', 'pattern']
        }
      },
      {
        name: 'multi_file_edit',
        description: 'Edit multiple files safely with preview and rollback.',
        inputSchema: {
          type: 'object',
          properties: {
            rootDir: { type: 'string' },
            edits: { type: 'array' },
            dryRun: { type: 'boolean' },
            createBackups: { type: 'boolean' }
          },
          required: ['rootDir', 'edits']
        }
      },
      
      // Code Analysis
      {
        name: 'dependency_graph',
        description: 'Analyze dependencies, detect circular deps.',
        inputSchema: {
          type: 'object',
          properties: {
            rootDir: { type: 'string' }
          },
          required: ['rootDir']
        }
      },
      {
        name: 'type_check',
        description: 'Run TypeScript type checker.',
        inputSchema: {
          type: 'object',
          properties: {
            rootDir: { type: 'string' }
          },
          required: ['rootDir']
        }
      },
      {
        name: 'lint',
        description: 'Run ESLint with auto-fix support.',
        inputSchema: {
          type: 'object',
          properties: {
            rootDir: { type: 'string' },
            fix: { type: 'boolean' }
          },
          required: ['rootDir']
        }
      },
      
      // Testing & Execution
      {
        name: 'run_tests',
        description: 'Run Jest tests with coverage.',
        inputSchema: {
          type: 'object',
          properties: {
            rootDir: { type: 'string' },
            collectCoverage: { type: 'boolean' }
          },
          required: ['rootDir']
        }
      },
      {
        name: 'execute_code',
        description: 'Execute JS/TS/Python safely.',
        inputSchema: {
          type: 'object',
          properties: {
            code: { type: 'string' },
            language: { type: 'string', enum: ['javascript', 'typescript', 'python'] }
          },
          required: ['code', 'language']
        }
      },
      
      // Project Understanding
      {
        name: 'analyze_project',
        description: 'Analyze project structure and dependencies.',
        inputSchema: {
          type: 'object',
          properties: {
            rootDir: { type: 'string' }
          },
          required: ['rootDir']
        }
      },
      {
        name: 'extract_docs',
        description: 'Extract and parse documentation.',
        inputSchema: {
          type: 'object',
          properties: {
            rootDir: { type: 'string' }
          },
          required: ['rootDir']
        }
      },
      {
        name: 'git_history',
        description: 'Get Git commit history.',
        inputSchema: {
          type: 'object',
          properties: {
            rootDir: { type: 'string' },
            limit: { type: 'number' }
          },
          required: ['rootDir']
        }
      },
      {
        name: 'git_status',
        description: 'Get Git status.',
        inputSchema: {
          type: 'object',
          properties: {
            rootDir: { type: 'string' }
          },
          required: ['rootDir']
        }
      },
      
      // Formatting
      {
        name: 'format_code',
        description: 'Format code with Prettier/Black/etc.',
        inputSchema: {
          type: 'object',
          properties: {
            rootDir: { type: 'string' },
            formatter: { type: 'string', enum: ['prettier', 'black', 'gofmt', 'rustfmt'] },
            checkOnly: { type: 'boolean' }
          },
          required: ['rootDir', 'formatter']
        }
      }
    ]
  };
});

// Serialize Maps and Sets to JSON
function serialize(obj: any): any {
  if (obj instanceof Map) {
    return Object.fromEntries(obj);
  }
  if (obj instanceof Set) {
    return Array.from(obj);
  }
  if (Array.isArray(obj)) {
    return obj.map(serialize);
  }
  if (obj && typeof obj === 'object') {
    const result: any = {};
    for (const [key, value] of Object.entries(obj)) {
      result[key] = serialize(value);
    }
    return result;
  }
  return obj;
}

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result: any;

    switch (name) {
      case 'batch_read_files':
        result = await batchReadFiles(args);
        break;

      case 'search_contents':
        result = await searchFileContents(args);
        break;

      case 'multi_file_edit':
        result = args.dryRun 
          ? await previewMultiFileEdits(args)
          : await applyMultiFileEdits(args);
        break;

      case 'dependency_graph':
        const graph = await generateDependencyGraph(args);
        result = {
          formatted: formatDependencyGraph(graph),
          data: graph
        };
        break;

      case 'type_check':
        const types = await runTypeCheck(args);
        result = {
          formatted: formatTypeCheckResults(types),
          data: types
        };
        break;

      case 'lint':
        const lint = await runESLint(args);
        result = {
          formatted: formatESLintResults(lint),
          data: lint
        };
        break;

      case 'run_tests':
        const tests = await runJestTests({ ...args, timeout: 60000 });
        result = {
          formatted: formatTestResults(tests),
          data: tests
        };
        break;

      case 'execute_code':
        const exec = await executeSandbox(args);
        result = {
          formatted: formatSandboxResults(exec),
          data: exec
        };
        break;

      case 'analyze_project':
        const project = await analyzeProject(args);
        result = {
          formatted: formatProjectInfo(project),
          data: project
        };
        break;

      case 'extract_docs':
        result = await extractDocumentation({
          ...args,
          extractReadme: true,
          extractDocs: true
        });
        break;

      case 'git_history':
        result = await getCommitHistory({
          ...args,
          limit: args.limit || 10
        });
        break;

      case 'git_status':
        const status = await getStatus(args);
        result = {
          formatted: formatGitStatus(status),
          data: status
        };
        break;

      case 'format_code':
        const format = await formatCode(args);
        result = {
          formatted: formatFormatResults(format),
          data: format
        };
        break;

      default:
        throw new Error(`Unknown tool: ${name}`);
    }

    // Serialize and return
    const serialized = serialize(result);
    
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(serialized, null, 2)
        }
      ]
    };

  } catch (error) {
    console.error(`Error in ${name}:`, error);
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error instanceof Error ? error.message : 'Unknown error'}`
        }
      ],
      isError: true
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Claude Coding Tools MCP Server v1.0.0 running');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
