# ION Kit Architecture

> **Version 6.1.0** - The "Concise System" Architecture  
> *Architecture v6.0 | See `version.py` for component counts*

## 📋 Overview

This toolkit is designed as a modular **Operating System for AI Agents**. It decouple intelligence (Agents) from capabilities (Tools) and processes (Workflows).

### System Components
1.  **Agents (20)**: The "Who". Specialized personas with defined roles.
2.  **Tools (5)**: The "What". Standalone software capabilities.
3.  **Workflows (16)**: The "How". Automated procedures triggered by slash commands.
4.  **CLI (`kit.py`)**: The "Interface". Unified entry point for all operations.

---

## 🏗️ Directory Structure

```text
kit-Working/
├── .agent/              # Intelligence Layer
│   ├── agents/          # Agent Definitions (.md)
│   ├── skills/          # Knowledge Modules
│   └── workflows/       # Slash Command Definitions
│
├── tools/               # Capability Layer
│   ├── api-mocker/      # Mock REST API Server
│   ├── app-packager/    # Web-to-EXE Converter
│   ├── bg-remover/      # AI Background Removal
│   ├── code-tools/      # Static Analysis & Linting
│   └── scraper/         # Web Content Extractor
│
├── scripts/             # Maintenance Layer (setup.py)
├── docs/                # Documentation Layer (GUIDE.md)
└── kit.py               # Unified CLI Entry Point
```

---

## 🤖 Agents (20)

Specialist personas loaded by the Orchestrator.

| Agent | Domain | Key Responsibility |
|-------|--------|-------------------|
| `orchestrator` | **Management** | Team Lead. Coordinates other agents. |
| `project-planner` | **Management** | Breaks down tasks. Creates PLAN.md. |
| `frontend-specialist` | **Web** | React, Tailwind, UI/UX implementation. |
| `backend-specialist` | **Backend** | API, Database, Server logic. |
| `mobile-developer` | **Mobile** | iOS/Android/React Native development. |
| `database-architect` | **Data** | SQL/NoSQL schema design. |
| `data-scientist` | **Data** | Analysis, ML, Python pandas. |
| `security-auditor` | **Security** | Defensive coding, vulnerability checks. |
| `penetration-tester` | **Security** | Offensive testing, red-teaming. |
| `test-engineer` | **Quality** | Unit, Integration, E2E Testing. |
| `devops-engineer` | **Ops** | CI/CD, Docker, Cloud Infra. |
| `release-engineer` | **Ops** | Packaging (`app-packager`) and Shipping. |
| `debugger` | **Support** | Root cause analysis. |
| `performance-optimizer`| **Support** | Speed, bundle size, Web Vitals. |
| `tooling-specialist` | **Support** | Linter/Prettier configs, dev env. |
| `seo-specialist` | **Growth** | Search ranking, meta tags. |
| `media-specialist` | **Media** | Image (`bg-remover`) & Video processing. |
| `game-developer` | **Specialized** | Game logic, canvas, physics. |
| `documentation-writer` | **Docs** | Maintaining this documentation. |
| `explorer-agent` | **Analysis** | Reading and mapping existing code. |

---

## 🧠 Skills (Knowledge Modules)

The toolkit contains **160+ Skills** located in `.agent/skills/`.

### How Skills Work (Auto-Assignment)
Skills are **automatically assigned** to Agents. You do **NOT** need to call skills manually.

1.  **Agent Activation**: When you ask for the `frontend-specialist`, the system loads that agent's definition.
2.  **Skill Loading**: The agent definition lists required skills (e.g., `react-patterns`, `tailwind-patterns`).
3.  **Context Injection**: The skill's instructions (BEST PRACTICES) are injected into the AI's context.

**Example**:
- The `database-architect` automatically loads `database-design` and `prisma-expert` skills.
- The `security-auditor` automatically loads `vulnerability-scanner`.

### Skill Categories
- **Frontend**: `react-patterns`, `nextjs-best-practices`, `tailwind-patterns`
- **Backend**: `api-patterns`, `nodejs-best-practices`, `python-patterns`
- **Testing**: `testing-patterns`, `tdd-workflow`, `webapp-testing`
- **Ops**: `docker-expert`, `deployment-procedures`, `aws-cloud`
- **Security**: `vulnerability-scanner`, `red-team-tactics`

---

## 🛠️ Integrated Tools (5)

Standalone software modules located in `tools/`.

| Tool | Path | Function | CLI Access |
|------|------|----------|------------|
| **Code Tools** | `tools/code-tools/` | Analysis, Lint, Test, Format | `analyze`, `lint`, `test`, `deps`, `format` |
| **Bg Remover** | `tools/bg-remover/` | AI Background Removal (U2Net) | `kit.py bg` |
| **App Packager**| `tools/app-packager/`| Web → EXE Conversion | `kit.py pack` |
| **Scraper** | `tools/scraper/` | Web → Markdown Conversion | `kit.py scrape` |
| **API Mocker** | `tools/api-mocker/` | JSON Schema → REST API | `kit.py mock` |

---

## 🔄 Workflows (16)

Automated procedures invoked via slash commands.

| Category | Commands |
|----------|----------|
| **Plan** | `/plan`, `/brainstorm`, `/analyze-project`, `/status` |
| **Build** | `/create`, `/enhance`, `/optimize-code`, `/ui-ux-pro-max`, `/build-portable-app`, `/remove-background` |
| **Run** | `/preview`, `/setup-workspace` |
| **Verify** | `/deploy`, `/test`, `/debug`, `/orchestrate` |

---

## 🧩 Protocol: How It Works

1.  **User Request**: User sends a prompt to Antigravity/Claude.
2.  **Rule Check**: AI reads `.agent/rules/GEMINI.md`.
3.  **Agent Selection**: AI selects the best Agent from the list above.
4.  **Workflow Trigger**: If user used `/slash`, AI loads `.agent/workflows/slash.md`.
5.  **Execution**:
    *   **Planning**: Agent writes `PLAN-{slug}.md`.
    *   **Coding**: Agent writes/edits files.
    *   **Tooling**: Agent runs `python kit.py [command]`.
    *   **Verification**: Agent running `python kit.py check` or `npm test`.

---
*Generated for AI Agent Toolkit v6.0*
