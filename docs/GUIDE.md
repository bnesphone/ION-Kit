# ION Kit - The Master Guide

> **The Official "Operating System" for your AI Agent.**

This toolkit transforms your AI coding environment into a fully staffed development agency. It provides **Specialist Agents**, **Automated Workflows**, and **Integrated Tools**.

---

## ⚡ Quick Reference (Cheatsheet)

### CLI Commands (`kit.py`)
Run these from your terminal in the project root.

| Command | Usage | Description |
|---------|-------|-------------|
| `setup` | `python kit.py setup` | **Install**: Setup environment & dependencies |
| `check` | `python kit.py check` | **Diagnose**: Check Python, Node, & Tools status |
| `analyze`| `python kit.py analyze` | **Code**: Analyze project structure & health |
| `lint` | `python kit.py lint --fix` | **Quality**: Lint and auto-fix code style |
| `bg` | `python kit.py bg [in] [out]` | **Media**: Remove image backgrounds |
| `pack` | `python kit.py pack ...` | **Distribute**: Create Windows .exe app |
| `scrape` | `python kit.py scrape [url]` | **Web**: Download URL as Markdown |
| `mock` | `python kit.py mock [json]` | **API**: Serve mock API from schema |

---

## 1. Integration Guide

**How to use this toolkit with Antigravity & Claude Code**

This toolkit is designed to be the "Operating System" for your AI agent.

### 🚀 Integration Steps

1.  **Clone/Copy**: Place this `kit-Working` folder as the root of your new project.
    *   *Alternative*: Copy `.agent/`, `tools/`, `scripts/`, `kit.py` into your existing project.
    
2.  **Activate**:
    *   Open your AI IDE (Antigravity/Cursor/VS Code with Claude).
    *   **Crucial Step**: Tell the AI to read the rules.
    *   *Prompt*: "Please read `.agent/rules/GEMINI.md` to understand your instructions."

3.  **Verify**:
    *   Ask: "What agents do you have available?"
    *   The AI should list the 20 agents found in `docs/ARCHITECTURE.md`.

### 🔄 The Development Loop

1.  **Plan**: Start every big feature with `/brainstorm` or `/plan`.
    *   *Example*: `/plan e-commerce cart`
2.  **Build**: Use agents to execute the plan.
    *   *Example*: "Use `frontend-specialist` to build the Cart component."
3.  **Verify**: Use tools to check work.
    *   *Example*: `python kit.py lint --fix`

---

## 2. Installation (Local Env)

**Prerequisites**: Python 3.7+ and Node.js.

1.  **Setup**:
    ```bash
    python kit.py setup
    ```
2.  **Verify**:
    ```bash
    python kit.py check
    ```

---

## 3. Workflows (Slash Commands)

Trigger these automations by typing the command in your chat.

### 🧠 Planning & Discovery
| Command | Description |
|---------|-------------|
| **/brainstorm** | Structured Deep Discovery. Use this before coding to explore 3+ options for a feature. |
| **/plan** | Project Planning Mode. Breaks down a request into a `PLAN-{slug}.md` file with tasks. |
| **/analyze-project** | Health Check. Runs analysis on imports, frameworks, and file structure. |
| **/status** | Progress Tracker. Summarizes the current state of tasks and agents. |

### 🔨 Creation & Modification
| Command | Description |
|---------|-------------|
| **/create** | **New Project Wizard**. Guides you through building a new app from scratch. |
| **/enhance** | **Feature Adder**. Use this to add features to an existing application. |
| **/optimize-code** | Auto-Formatter. Runs linter, type-checker, and prettifier on your codebase. |
| **/ui-ux-pro-max** | **Design Studio**. Generates premium, modern UI designs/codes for web/mobile. |

### 🚀 Deployment & Operations
| Command | Description |
|---------|-------------|
| **/deploy** | Production Deployment. checks code quality, builds, and deploys. |
| **/build-portable-app** | **EXE Builder**. Documentation/Workflow on how to package your app. |
| **/preview** | Local Server Manager. Starts/Stops dev servers for previewing work. |
| **/setup-workspace** | Context Repair. Re-runs environment setup if things get broken. |

### 🛠️ Debugging & maintenance
| Command | Description |
|---------|-------------|
| **/debug** | **CSI Mode**. Systematic 4-step debugging (Reproduce -> Analyze -> Fix -> Verify). |
| **/test** | Test Generator. Generates unit/integration tests for your files. |
| **/remove-background** | Image Workflow. Guide to using the integrated background remover. |
| **/orchestrate** | **Team Lead**. Use this to coordinate multiple agents on a huge task. |

---

## 4. The 20 Specialist Agents

Don't do everything yourself. Ask an expert.

**Core Team**
- **`project-planner`**: The Manager. Breaks down tasks. Always start here for big jobs.
- **`orchestrator`**: The Team Lead. Manages multiple agents working together.
- **`frontend-specialist`**: The Designer. React, Tailwind, UI/UX expert.
- **`backend-specialist`**: The Architect. Node, Python, DBs, APIs.

**Quality & Security**
- **`security-auditor`**: The Shield. Finds vulnerabilities and secrets.
- **`penetration-tester`**: The Attacker. Tries to break your app to find flaws.
- **`test-engineer`**: The QA. Writes and runs tests (files & E2E).
- **`debugger`**: The Detective. Finds root causes of bugs.
- **`performance-optimizer`**: The Speedster. Web Vitals and bundle optimization.
- **`tooling-specialist`**: The Mechanic. Configs, linters, env files.

**Mobile & Game**
- **`mobile-developer`**: iOS/Android/React Native/Flutter expert.
- **`game-developer`**: Game logic, physics, and mechanics.

**Specialized Roles**
- **`database-architect`**: SQL/NoSQL schema design and optimization.
- **`devops-engineer`**: CI/CD, Docker, Cloud Infrastructure.
- **`release-engineer`**: Packaging, Installers, GitHub Releases.
- **`seo-specialist`**: Search Engine Optimization and Visibility.
- **`documentation-writer`**: Creates READMEs, Guides, and Manuals.
- **`data-scientist`**: Data analysis, Python pandas, ML.
- **`media-specialist`**: Image/Video processing and optimization.
- **`explorer-agent`**: Codebase Navigator. Maps out existing large projects.

---

## 5. Integrated Tools Manual

Your toolkit includes standalone software capabilities located in `tools/`.

### A. Web Scraper (`tools/scraper`)
*Extract content from websites and convert to Markdown.*
```bash
python kit.py scrape https://example.com --out docs/context.md
```

### B. API Mocker (`tools/api-mocker`)
*Instant fake backend for prototyping.*
1. Create `schema.json`: `{"users": [{"id":1, "name":"Alice"}]}`
2. Run: `python kit.py mock schema.json`
3. Access: `http://localhost:8000/users`

### C. Background Remover (`tools/bg-remover`)
*Pro-grade AI removal of image backgrounds.*
```bash
# Single file
python kit.py bg photo.jpg no-bg.png

# Entire folder
python kit.py bg ./raw-photos/ ./clean-photos/
```

### D. App Packager (`tools/app-packager`)
*Convert Web/Node apps to Windows .exe files.*
```bash
python kit.py pack --source ./my-app --name "CoolApp"
```

### E. Code Tools (`tools/code-tools`)
*Static Analysis Engine.*
- **Analysis**: `python kit.py analyze`
- **Linting**: `python kit.py lint --fix`
- **Testing**: `python kit.py test`
- **Format**: `python kit.py format`
- **Deps**: `python kit.py deps`

---

## 6. Troubleshooting

**"Command not found"?**
- Ensure you are in the project root.
- Ensure `python kit.py setup` finished successfully.

**"AI doesn't know X agent"?**
- Remind the AI: "Please read `docs/ARCHITECTURE.md` to see your available agents."

**Q: Background Remover crashed?**
- It needs a good internet connection on the FIRST run to download models (~150MB).

**Q: Do I need to manually run an MCP Server?**
- **No.** The Toolkit runs fully via `kit.py` CLI commands.
- *Advanced Users*: There is an optional `mcp-server.ts` in `tools/code-tools` if you want to connect this directly to Claude Desktop, but it is **not required** for normal usage.
