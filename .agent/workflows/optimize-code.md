---
description: analyze and optimize code quality using the integrated coding tools
---

# Optimize Code Workflow

This workflow guides you through analyzing and optimizing your codebase using the Claude Coding Tools suite.

## Prerequisites
- `tooling-specalist` or `dev-utilities` skill enabled
- Node.js dependencies installed in `integrated_tools/coding_tools`

## Steps

### 1. Setup
Ensure the tools are ready.
```bash
cd integrated_tools/coding_tools && npm install && cd ../..
```

### 2. Analyze Structure
Get a high-level overview of the project structure and frameworks.
```bash
npx ts-node integrated_tools/coding_tools/cli.ts analyze
```

### 3. Check for Issues
Run the linter and type checker to identify potential bugs.
```bash
# Check types
npx ts-node integrated_tools/coding_tools/cli.ts types

# Run linter
npx ts-node integrated_tools/coding_tools/cli.ts lint
```

### 4. Dependency Analysis
Check for circular dependencies or complex import chains.
```bash
npx ts-node integrated_tools/coding_tools/cli.ts deps
```

### 5. Optimization (Auto-Fix)
Automatically fix linting issues and format code.
```bash
# Fix lint errors
npx ts-node integrated_tools/coding_tools/cli.ts lint --fix

# Format code (Prettier/Black)
npx ts-node integrated_tools/coding_tools/cli.ts format
```

### 6. Verify
Run tests to ensure no regressions were introduced.
```bash
npx ts-node integrated_tools/coding_tools/cli.ts test
```

## Example
To perform a full cleanup of the project:
```bash
npx ts-node integrated_tools/coding_tools/cli.ts lint --fix
npx ts-node integrated_tools/coding_tools/cli.ts format
npx ts-node integrated_tools/coding_tools/cli.ts test
```
