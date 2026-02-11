---
description: standard procedure for setting up the development workspace
---

# Setup Workspace Workflow

This workflow ensures the development environment is correctly configured with all necessary dependencies and tools.

## Prerequisites
- Git
- Python 3.10+
- Node.js 18+

## Steps

### 1. Verification
// turbo-all
Run the verification script to check for missing dependencies.
```bash
python scripts/verify_all.py
```

### 2. Python Environment
Ensure the virtual environment is active and dependencies are installed.
```bash
pip install -r requirements.txt
```

### 3. Node.js Environment
Install Node.js dependencies for the integrated tools.
```bash
# Root package.json (if exists) or tool-specific
cd integrated_tools/coding_tools && npm install
cd ../portable_app_kit && npm install
```

### 4. Environment Variables
Check for `.env` file. If missing, copy `.env.example` to `.env` and fill in necessary keys (e.g., OPENAI_API_KEY, ANTHROPIC_API_KEY).

### 5. Tool Check
Verify that major tools are accessible:
- `python --version`
- `node --version`
- `docker --version` (if using containers)

## Troubleshooting
- If `pip` fails, check for permission issues or Python version mismatch.
- If `npm` fails, try clearing cache: `npm cache clean --force`.
