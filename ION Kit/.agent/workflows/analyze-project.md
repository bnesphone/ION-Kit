---
description: analyze project structure and health metrics
---

# Analyze Project Workflow

This workflow provides a deep dive into the project's structure, health, and dependencies using the Coding Tools.

## Prerequisites
- Node.js dependencies installed in `integrated_tools/coding_tools`

## Steps

### 1. General Analysis
Understand the frameworks, languages, and size of the codebase.
```bash
npx ts-node integrated_tools/coding_tools/cli.ts analyze
```

### 2. Dependency Graph
Visualize the import structure and detect circular dependencies.
```bash
npx ts-node integrated_tools/coding_tools/cli.ts deps
```

### 3. Type Health (TypeScript)
Check the number of type errors and overall type safety.
```bash
npx ts-node integrated_tools/coding_tools/cli.ts types
```

### 4. Git Health
Review the recent commit history and status (if strictly analysis is needed).
```bash
# Git status wrapper
git status
```

## Report Generation
The output of these commands provides a comprehensive health report for the project.
