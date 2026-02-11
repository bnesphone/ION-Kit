---
name: dev-utilities
description: Advanced development utilities, including CLI-based coding tools and MCP server.
---

# Dev Utilities Skill

This skill provides access to a suite of advanced TypeScript-based coding tools for analysis, testing, and refactoring.

## Capabilities

1.  **Project Analysis**: detailed stats on structure, dependencies, and git status.
2.  **Code Quality**: Automated linting, type checking, and formatting.
3.  **MCP Server**: Connects these tools to AI assistants (Claude, etc.).

## Tools & Usage

### 1. Coding Tools CLI

Located at: `tools/code-tools/cli.ts` (Run with `npx ts-node`)

**Commands:**

- **Analyze Project**
  ```bash
  npx ts-node tools/code-tools/cli.ts analyze
  ```
  Returns: Frameworks detected, dependency count, loc stats.

- **Check Code Quality**
  ```bash
  # Run Linter (ESLint)
  npx ts-node tools/code-tools/cli.ts lint --fix
  
  # Check Types (TypeScript)
  npx ts-node tools/code-tools/cli.ts types
  ```

- **Dependency Graph**
  ```bash
  npx ts-node tools/code-tools/cli.ts deps
  ```

- **Run Tests**
  ```bash
  npx ts-node tools/code-tools/cli.ts test
  ```

### 2. MCP Server

For connecting to an external AI client (like Claude Desktop).
- Entry point: `tools/code-tools/mcp-server.ts`
- Transport: stdio

## Setup

Ensure dependencies are installed:
```bash
cd tools/code-tools
npm install
```
