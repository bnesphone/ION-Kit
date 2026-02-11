---
name: workflow-template
description: Template for creating new workflows. Copy this file and customize for your workflow.
trigger: /command-name
agents: [agent1, agent2]
skills: [skill1, skill2]
---

# Workflow Name

> Brief one-line description of what this workflow does

## 📋 Purpose

Detailed explanation of:
- What problem this workflow solves
- When to use it
- What it automates

## 🎯 Prerequisites

List what must exist or be true before this workflow can run:
- [ ] Prerequisite 1 (e.g., Project initialized)
- [ ] Prerequisite 2 (e.g., Dependencies installed)
- [ ] Prerequisite 3 (e.g., Configuration files present)

## 🔄 Workflow Steps

### Step 1: [Action Name]
**Agent:** `agent-name`  
**Skills:** skill-name

**What happens:**
- Detailed description of what occurs
- Any files created/modified
- Expected outcomes

**Example:**
```bash
# Command or code example
```

### Step 2: [Action Name]
**Agent:** `agent-name`  
**Skills:** skill-name

**What happens:**
- Description
- Files affected
- Outcomes

### Step 3: [Final Action]
**Agent:** `agent-name`
**Skills:** skill-name

**What happens:**
- Final steps
- Deliverables
- Success criteria

## ✅ Validation

How to verify the workflow succeeded:
- [ ] Check 1: Description of what to verify
- [ ] Check 2: Expected result
- [ ] Check 3: Success indicator

## 💡 Usage Examples

### Example 1: Basic Usage
```
/command-name simple param
```
**Result:** What happens with basic usage

### Example 2: Advanced Usage
```
/command-name --option value --flag
```
**Result:** What happens with options

### Example 3: Complex Scenario
```
/command-name complex scenario with multiple params
```
**Result:** What happens in complex cases

## 🚫 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Error message 1 | Why it happens | How to fix |
| Error message 2 | Why it happens | How to fix |

## 📊 Expected Output

```
Example of what the workflow produces:
- File structure
- Console output
- Generated artifacts
```

## 🔧 Configuration

Optional: If workflow has configurable parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| param1 | string | "value" | What it controls |
| param2 | boolean | true | What it toggles |

## 📚 Related

- Related workflow 1
- Related workflow 2
- Relevant documentation

---

**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD  
**Maintainer:** Agent/Role responsible
