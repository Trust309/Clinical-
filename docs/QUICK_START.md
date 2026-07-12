# Quick Start Guide - Documentation System

Welcome to the streamlined documentation system for the Clinical Supervision Chatbot! This guide will get you up and running in 5 minutes.

## What You Get

This documentation system provides:
- ✅ **Automated helpers** - Scripts to validate and generate docs
- ✅ **Ready-to-use templates** - For features, APIs, and knowledge topics
- ✅ **Clear workflow** - Step-by-step process for all doc tasks
- ✅ **Quality checks** - Validation to keep docs consistent

## 5-Minute Setup

### 1. Understand the Structure

```
docs/
├── QUICK_START.md              ← You are here!
├── DOCUMENTATION_WORKFLOW.md   ← Full workflow guide
├── templates/                  ← Copy these when documenting
│   ├── api_endpoint_template.md
│   ├── feature_template.md
│   └── knowledge_topic_template.md
└── guides/                     ← Additional resources
```

### 2. Run the Documentation Helper

```bash
# Make the helper executable
chmod +x doc_helper.py

# Validate your documentation
python doc_helper.py validate

# Check what's documented
python doc_helper.py check-coverage
```

### 3. Try Creating Something

**Add a new knowledge topic:**
```bash
python doc_helper.py add-topic "Supervision Models"
```

**Add API endpoint documentation:**
```bash
python doc_helper.py add-endpoint "export-chat"
```

**Generate API docs:**
```bash
python doc_helper.py generate-api
```

## Common Tasks

### Task 1: Document a New Feature

```bash
# 1. Copy the feature template
cp docs/templates/feature_template.md my_feature.md

# 2. Fill it out (use your editor)
nano my_feature.md

# 3. Implement the feature
# ... code here ...

# 4. Update relevant docs
# - README.md
# - docs/API.md (if API changed)

# 5. Validate
python doc_helper.py validate
```

### Task 2: Add a Knowledge Topic to Chatbot

```bash
# 1. Generate the topic documentation
python doc_helper.py add-topic "New Topic Name"

# 2. Edit the generated file in docs/topics/new_topic_name.md

# 3. Add to chatbot_backend.py:
#    - Add keywords and responses to knowledge_base

# 4. Add to chatbot.html:
#    - Add to local knowledge_base

# 5. Test and validate
python doc_helper.py validate
```

### Task 3: Document API Changes

```bash
# 1. Generate API docs from current code
python doc_helper.py generate-api

# 2. Review and enhance docs/API.md

# 3. For detailed endpoint docs:
python doc_helper.py add-endpoint "endpoint-name"
```

### Task 4: Prepare for Release

```bash
# 1. Generate changelog entry
python doc_helper.py changelog

# 2. Fill in the changelog with your changes

# 3. Validate everything
python doc_helper.py validate

# 4. Review documentation coverage
python doc_helper.py check-coverage
```

## The Helper Commands

| Command | What It Does | Example |
|---------|--------------|---------|
| `validate` | Checks docs are consistent with code | `python doc_helper.py validate` |
| `generate-api` | Creates API docs from backend code | `python doc_helper.py generate-api` |
| `add-topic` | Creates new knowledge topic with template | `python doc_helper.py add-topic "Ethics"` |
| `add-endpoint` | Creates API endpoint docs from template | `python doc_helper.py add-endpoint "reset"` |
| `check-coverage` | Shows what's documented vs what exists | `python doc_helper.py check-coverage` |
| `changelog` | Generates changelog entry template | `python doc_helper.py changelog` |

## Daily Workflow (30 seconds)

**Before coding:**
```bash
# 1. Think: "What am I changing?"
# 2. Copy appropriate template if needed
# 3. Jot down what the feature/change does
```

**After coding:**
```bash
# 1. Update relevant docs (README, API, etc.)
# 2. Run validation
python doc_helper.py validate

# 3. Fix any issues found
```

## Documentation Cheat Sheet

### When to Use Which Template

| Situation | Template | Command |
|-----------|----------|---------|
| Adding user-facing feature | `feature_template.md` | Copy manually |
| Adding API endpoint | `api_endpoint_template.md` | `python doc_helper.py add-endpoint "name"` |
| Adding knowledge topic | `knowledge_topic_template.md` | `python doc_helper.py add-topic "name"` |
| Fixing a bug | Update `TROUBLESHOOTING.md` | Edit manually |
| Release prep | Update `CHANGELOG.md` | `python doc_helper.py changelog` |

### Quick Doc Locations

| What | Where |
|------|-------|
| User guide | `README.md` |
| API reference | `docs/API.md` |
| System design | `docs/ARCHITECTURE.md` |
| Deployment | `docs/DEPLOYMENT.md` |
| Common issues | `docs/TROUBLESHOOTING.md` |
| How to extend | `docs/CUSTOMIZATION.md` |
| Version history | `docs/CHANGELOG.md` |

## Tips for Success

1. **Document as you code** - Don't leave it for later
2. **Use the templates** - They ensure consistency
3. **Run validation often** - Catch issues early
4. **Keep it simple** - Short and clear beats long and comprehensive
5. **Link, don't duplicate** - Reference existing docs

## Getting Help

- **Full workflow**: Read `docs/DOCUMENTATION_WORKFLOW.md`
- **Templates**: Browse `docs/templates/`
- **Helper usage**: Run `python doc_helper.py --help`

## Next Steps

1. ✅ Read the full [Documentation Workflow Guide](DOCUMENTATION_WORKFLOW.md)
2. ✅ Run `python doc_helper.py validate` to see current state
3. ✅ Browse the templates to understand what's available
4. ✅ Try creating a sample topic: `python doc_helper.py add-topic "Test"`

---

**That's it!** You now have a streamlined documentation process. The key is to use it consistently - document early, validate often, and keep it simple.

Happy documenting! 📚
