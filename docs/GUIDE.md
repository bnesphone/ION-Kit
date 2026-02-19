# ION-Kit - The Master Guide

> **The Official "Operating System" for your AI Agent - Now Powered by OpenCode.**

This guide provides in-depth instructions on using ION-Kit with OpenCode for autonomous AI development. For overviews, features, and quick starts, see [README.md](file:///c:/Users/User/Desktop/ION-Kit/README.md). Here, we dive into detailed setup, workflows, agents, tools, autonomy loops, examples, and troubleshooting.

---

## ⚡ Quick Reference (Cheatsheet)

Cross-reference with [QUICK_REFERENCE.md](file:///c:/Users/User/Desktop/ION-Kit/QUICK_REFERENCE.md) for full command lists. Key OpenCode commands:

| Command | Usage | Description |
|---------|-------|-------------|
| `/init` | `opencode --agent ION "/init"` | **Initialize**: Load ION agents with autonomy loops |
| `--agent ION` | `opencode --agent ION "Task"` | **Run Task**: Autonomous execution via ION |
| `kit.py setup` | `python kit.py setup` | **Install**: Setup dependencies (Python/Node) |
| `kit.py check` | `python kit.py check` | **Diagnose**: Verify environment & tools |

---

## 1. Integration Guide

**How to use ION-Kit with OpenCode**

ION-Kit is natively ported to OpenCode, transforming it into an autonomous development studio. Agents operate in self-correcting loops with minimal user input.

### 🚀 Integration Steps

1. **Install from GitHub** (Detailed in README.md):
   - Clone: `git clone <repo-url> my-project`
   - Setup: `cd my-project && python kit.py setup`

2. **OpenCode Configuration**:
   - Ensure OpenCode is installed: `opencode --version`
   - The core config is [.opencode/ion-kit.jsonc](file:///c:/Users/User/Desktop/ION-Kit/.opencode/ion-kit.jsonc) - Defines 20 agents with autonomy settings.
   - Customize: Edit prompts, models, or budgets in ion-kit.jsonc (JSONC format allows comments).

3. **Initialize Autonomy**:
   - Run: `opencode --agent ION "/init"`
   - This loads ION as the coordinator, enabling loops for all agents.

4. **Verify**:
   - List agents: `opencode agent list`
   - Check config: `opencode debug config`
   - Test: `opencode --agent ION "Show available agents"`

### 🔄 Understanding Autonomy Loops

The port embeds "ION on steroids" logic: Agents reduce user input by looping through **plan -> think -> build -> test -> debug** until tasks complete.

- **Key Behaviors**:
  - **Self-Correction**: Auto-retry on errors with adjusted strategies.
  - **Boundary Enforcement**: Agents stay in domains (e.g., frontend-specialist handles UI only) and delegate via ION.
  - **Minimal Input**: Auto-approvals for safe actions; low verbosity outputs.
  - **Budgeting**: Token limits (e.g., 200k-300k) prevent infinite loops.

- **Customization**:
  - In ion-kit.jsonc, adjust `"thinking": { "type": "enabled", "budgetTokens": X }` for loop depth.
  - Set `"textVerbosity": "low"` for concise feedback.

Example Prompt in Config: "Operate autonomously: plan, think, build, test, debug in loops until done. Minimize user input."

---

## 2. Installation (Local Env)

Detailed steps (supplements README.md):

1. **Prerequisites**: Python 3.9+, Node.js, OpenCode.
2. **Setup Command**:
   ```
   python kit.py setup
   ```
   - Installs Python deps (via requirements.txt), Node deps (via package.json), and tools.
3. **OpenCode-Specific**:
   - If issues: `opencode debug config` to validate ion-kit.jsonc.
4. **Docker Alternative** (See DOCKER.md):
   ```
   docker build -t ion-kit .
   docker run -it ion-kit opencode --agent ION "/init"
   ```

---

## 3. Workflows (Slash Commands)

Trigger via OpenCode: `opencode --agent ION "/command Task description"`. Workflows are enhanced for autonomy - agents loop until resolved.

### 🧠 Planning & Discovery
| Command | Description | Example |
|---------|-------------|---------|
| **/brainstorm** | Explore options autonomously. | `opencode --agent ION "/brainstorm e-commerce features"` |
| **/plan** | Generate PLAN.md with tasks. Loops for refinements. | `opencode --agent ION "/plan secure auth system"` |
| **/analyze-project** | Autonomous health check. | `opencode --agent ION "/analyze-project"` |
| **/status** | Summarize progress (loops if incomplete). | `opencode --agent ION "/status"` |

### 🔨 Creation & Modification
| Command | Description | Example |
|---------|-------------|---------|
| **/create** | Build new projects autonomously. | `opencode --agent ION "/create React app"` |
| **/enhance** | Add features with loops. | `opencode --agent ION "/enhance add cart"` |
| **/optimize-code** | Auto-optimize in loops. | `opencode --agent ION "/optimize-code"` |
| **/ui-ux-pro-max** | Design premium UIs. | `opencode --agent ION "/ui-ux-pro-max dashboard"` |

### 🚀 Deployment & Operations
| Command | Description | Example |
|---------|-------------|---------|
| **/deploy** | Autonomous build/deploy. | `opencode --agent ION "/deploy to Vercel"` |
| **/build-portable-app** | Package to EXE. | `opencode --agent ION "/build-portable-app"` |
| **/preview** | Manage dev servers. | `opencode --agent ION "/preview"` |
| **/setup-workspace** | Re-setup environment. | `opencode --agent ION "/setup-workspace"` |

### 🛠️ Debugging & Maintenance
| Command | Description | Example |
|---------|-------------|---------|
| **/debug** | Loop through debugging steps. | `opencode --agent ION "/debug login bug"` |
| **/test** | Generate/run tests autonomously. | `opencode --agent ION "/test API endpoints"` |
| **/remove-background** | Process images. | `opencode --agent ION "/remove-background photo.jpg"` |
| **/orchestrate** | Coordinate agents. | `opencode --agent ION "/orchestrate full app build"` |

---

## 4. The 20 Specialist Agents

For high-level list, see README.md. Here: Detailed roles with autonomy notes.

**Management**:
- **ION (orchestrator)**: Coordinates loops across agents. Use for all tasks.
- **project-planner**: Plans with autonomous breakdowns.

**Development**:
- **frontend-specialist**: UI loops (plan/build/test).
- **backend-specialist**: Server logic loops.
- **mobile-developer**: App loops for iOS/Android.

(And so on for all 20 - see ARCHITECTURE.md for full boundaries and delegation logic.)

**Usage Example**: `opencode --agent frontend-specialist "Build secure login UI" - Loops until complete, delegates to ION if needed.

---

## 5. Integrated Tools Manual

Usable via kit.py or OpenCode agents (e.g., `opencode --agent media-specialist "Use bg tool on image"`).

### A. Web Scraper
```
python kit.py scrape https://example.com --out docs/context.md
```

### B. API Mocker
```
python kit.py mock schema.json
```

(Details as in original, but add: In OpenCode, agents can invoke these in loops.)

---

## 6. Usage Examples

- **Simple Task**: `opencode --agent ION "Build React button" - ION delegates to frontend, loops until tested/debugged.`
- **Complex Project**: `/init` then `opencode --agent ION "/plan e-commerce site" - Follows with autonomous build.`
- **Debugging**: `opencode --agent bug-hunter "Fix crash in API" - Persistent loops.`

---

## 7. Troubleshooting

- **CLI Parsing Issues**: Use single quotes for multi-word prompts: `opencode --agent ION 'Task description'`.
- **Config Errors**: Run `opencode debug config`; fix JSON in ion-kit.jsonc.
- **Agent Not Found**: Re-init with `/init`; verify with `opencode agent list`.
- **Loop Stalls**: Increase budgetTokens in config; check model (opencode/zen).
- **Fallback to CLI**: If OpenCode issues, use `python kit.py` for tools.

For more, see SYSTEM_REVIEW.md.

---

**Built for Autonomous AI - Minimize Input, Maximize Output!**