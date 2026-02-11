# ION Kit - Quick Command Reference

**Updated:** January 21, 2026 | **Version:** 6.1.0

---

## 🚀 Setup & System

```bash
python kit.py setup              # Install all dependencies (Python + Node.js)
python kit.py check              # System health check
python version.py                # Show version info
```

---

## 🔍 Analysis & Validation

```bash
python kit.py analyze            # Analyze project structure
python kit.py validate           # Run all validation checks ⭐ NEW
python kit.py validate-boundaries # Check agent boundaries ⭐ NEW
python tests/run_tests.py       # Run test suite ⭐ NEW
```

---

## 🧹 Code Quality

```bash
python kit.py lint               # Check code style
python kit.py lint --fix         # Auto-fix style issues
python kit.py format             # Format code
python kit.py format --check     # Check format only
python kit.py test               # Run project tests
python kit.py deps               # Generate dependency graph
```

---

## 🛠️ Tools

```bash
# Background Remover
python kit.py bg input.jpg output.png
python kit.py bg input/ output/  # Batch process

# Web Scraper
python kit.py scrape https://example.com
python kit.py scrape https://example.com --out docs/page.md

# App Packager
python kit.py pack --source ./my-app --name "MyApp"

# API Mocker
python kit.py mock schema.json
python kit.py mock schema.json --port 3000
```

---

## 📋 Workflows (Slash Commands)

Use these in your AI IDE:

### Planning
```
/brainstorm [idea]       # Deep discovery & exploration
/plan [feature]          # Create structured plan
/status                  # Check progress
/analyze-project         # Health check
```

### Building
```
/create [app]            # New project wizard
/enhance [feature]       # Add to existing
/ui-ux-pro-max          # Design studio
/optimize-code           # Auto-format & lint
```

### Deployment
```
/deploy                  # Production deploy
/build-portable-app     # Create .exe
/preview                # Start dev server
```

### Debugging
```
/debug [issue]          # Systematic debugging
/test                   # Generate tests
```

---

## 📁 File Structure

```
.agent/
├── agents/           # 20 specialist agents
├── skills/           # 40+ skill modules
├── workflows/        # 16 automated workflows
│   └── _TEMPLATE.md  # Create new workflows ⭐ NEW
└── rules/
    └── GEMINI.md     # AI behavior rules

tools/
├── bg-remover/       # AI background removal
├── app-packager/     # Web to EXE
├── code-tools/       # Analysis & linting
├── scraper/          # Web to Markdown
└── api-mocker/       # Mock API server

scripts/
├── setup.py                  # Setup script
└── validate_boundaries.py    # Boundary checker ⭐ NEW

tests/                # Test infrastructure ⭐ NEW
├── test_cli.py       # CLI tests
├── run_tests.py      # Test runner
└── README.md         # Test docs
```

---

## 🎯 Common Workflows

### First Time Setup
```bash
1. python kit.py setup
2. python kit.py check
3. python version.py
```

### Before Committing Code
```bash
python kit.py validate    # Run all checks
```

### Creating New Workflow
```bash
cp .agent/workflows/_TEMPLATE.md .agent/workflows/my-workflow.md
# Edit my-workflow.md with your steps
```

### Running Tests
```bash
python tests/run_tests.py
```

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Tool not found | Run `python kit.py setup` |
| Node.js missing | Install Node.js, then run setup |
| Test failures | Check `tests/README.md` for details |
| Boundary violations | Run `python kit.py validate-boundaries` |
| Version mismatch | Check `python version.py` |

---

## 📚 Documentation

- **README.md** - Overview & quick start
- **docs/GUIDE.md** - Complete user manual
- **docs/ARCHITECTURE.md** - System design
- **SYSTEM_REVIEW.md** - Full analysis
- **PROGRESS.md** - Recent improvements
- **tests/README.md** - Testing guide

---

## ⭐ New Features (Jan 21, 2026)

- ✅ Workflow template system
- ✅ Agent boundary validation
- ✅ Comprehensive test suite
- ✅ Unified validation command
- ✅ Version consistency system

---

**Tip:** Run `python kit.py --help` for full command list
