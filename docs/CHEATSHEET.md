# Documentation Cheat Sheet

Quick reference for common documentation tasks.

---

## 🚀 Most Used Commands

```bash
# Validate everything
python doc_helper.py validate

# Check what's documented
python doc_helper.py check-coverage

# Add new knowledge topic
python doc_helper.py add-topic "Topic Name"

# Add API endpoint docs
python doc_helper.py add-endpoint "endpoint-name"

# Generate changelog entry
python doc_helper.py changelog
```

---

## 📋 When to Use Which Template

| Task | Template | Command |
|------|----------|---------|
| 🎯 **New Feature** | `feature_template.md` | Copy manually from `docs/templates/` |
| 🔌 **API Endpoint** | `api_endpoint_template.md` | `python doc_helper.py add-endpoint "name"` |
| 📚 **Knowledge Topic** | `knowledge_topic_template.md` | `python doc_helper.py add-topic "Name"` |

---

## 📖 Documentation Files Quick Reference

| File | Purpose | When to Update |
|------|---------|----------------|
| `README.md` (root) | User guide & setup | Adding features, changing setup |
| `docs/API.md` | API reference | Adding/changing endpoints |
| `docs/CHANGELOG.md` | Version history | Every release, major changes |
| `docs/TROUBLESHOOTING.md` | Common issues | Finding/fixing bugs |

---

## ⚡ Quick Workflows

### Adding a Knowledge Topic (2 minutes)

```bash
# 1. Generate template
python doc_helper.py add-topic "Boundary Setting"

# 2. Edit: docs/topics/boundary_setting.md
nano docs/topics/boundary_setting.md

# 3. Add to chatbot_backend.py
# - Add to knowledge_base dict

# 4. Add to chatbot.html  
# - Add to knowledgeBase object

# 5. Validate
python doc_helper.py validate
```

### Adding a Feature (5 minutes)

```bash
# 1. Copy template
cp docs/templates/feature_template.md my_feature.md

# 2. Fill out planning sections

# 3. Code the feature

# 4. Update README.md
nano README.md

# 5. Validate
python doc_helper.py validate
```

### Preparing for Release (3 minutes)

```bash
# 1. Generate changelog entry
python doc_helper.py changelog

# 2. Edit CHANGELOG.md with your changes
nano docs/CHANGELOG.md

# 3. Update version in relevant files

# 4. Final validation
python doc_helper.py validate

# 5. Check coverage
python doc_helper.py check-coverage
```

---

## 🎯 Before You Commit Checklist

```bash
# Quick pre-commit checks
□ python doc_helper.py validate     # Docs match code?
□ All examples tested?               # Do they work?
□ CHANGELOG.md updated?              # What changed?
□ No broken links?                   # Links valid?
□ Used templates?                    # Consistent format?
```

---

## 📁 File Organization

```
Your Project/
│
├── README.md                    ← Main user guide
├── chatbot_backend.py          ← Backend code
├── chatbot.html                ← Frontend code
├── doc_helper.py               ← Documentation automation
│
└── docs/                       ← All documentation
    │
    ├── README.md               ← Docs overview (start here)
    ├── QUICK_START.md          ← 5-minute setup guide
    ├── DOCUMENTATION_WORKFLOW.md ← Your process
    ├── CHANGELOG.md            ← Version history
    ├── TROUBLESHOOTING.md      ← Common issues
    ├── CHEATSHEET.md          ← This file!
    │
    ├── templates/              ← Copy these!
    │   ├── api_endpoint_template.md
    │   ├── feature_template.md
    │   └── knowledge_topic_template.md
    │
    ├── guides/                 ← In-depth guides
    │   └── knowledge_base_guide.md
    │
    ├── api/                    ← API endpoint docs (auto-created)
    │   └── [endpoint].md
    │
    └── topics/                 ← Knowledge topic docs (auto-created)
        └── [topic].md
```

---

## 💡 Common Scenarios

### "I'm adding a new chatbot topic"
```bash
python doc_helper.py add-topic "Your Topic"
# Then edit both chatbot_backend.py and chatbot.html
python doc_helper.py validate
```

### "I'm fixing a bug"
```bash
# 1. Fix the bug
# 2. Add to docs/TROUBLESHOOTING.md
# 3. Update docs/CHANGELOG.md under "Fixed"
```

### "I'm changing an API endpoint"
```bash
# 1. Update the code
# 2. Update docs/API.md
# 3. Run: python doc_helper.py validate
```

### "I found undocumented code"
```bash
# 1. Check: python doc_helper.py check-coverage
# 2. Use appropriate template
# 3. Document it
# 4. Validate
```

### "Documentation is out of sync"
```bash
python doc_helper.py validate
# Fix the issues it reports
python doc_helper.py validate  # Confirm fixed
```

---

## 🔧 Troubleshooting the Docs

| Problem | Solution |
|---------|----------|
| Validation fails | Run `python doc_helper.py validate` to see specific issues |
| Don't know what to document | Run `python doc_helper.py check-coverage` |
| Template not found | Check `docs/templates/` directory exists |
| Helper script won't run | Make sure it's executable: `chmod +x doc_helper.py` |

---

## 📚 Where to Find Help

| Question Type | Resource |
|--------------|----------|
| "How do I start?" | [QUICK_START.md](QUICK_START.md) |
| "What's the process?" | [DOCUMENTATION_WORKFLOW.md](DOCUMENTATION_WORKFLOW.md) |
| "How do I add topics?" | [Knowledge Base Guide](guides/knowledge_base_guide.md) |
| "Something's broken!" | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| "What changed?" | [CHANGELOG.md](CHANGELOG.md) |

---

## ⚡ Speed Tips

1. **Alias the validator**
   ```bash
   alias valdocs="python doc_helper.py validate"
   # Now just run: valdocs
   ```

2. **Git pre-commit hook**
   ```bash
   # Add to .git/hooks/pre-commit
   #!/bin/bash
   python doc_helper.py validate || exit 1
   ```

3. **Keyboard shortcut** (VS Code)
   ```json
   {
     "key": "ctrl+shift+d",
     "command": "workbench.action.terminal.sendSequence",
     "args": { "text": "python doc_helper.py validate\n" }
   }
   ```

---

## 📊 Documentation Quality Checklist

**Good documentation is:**
- [ ] **Accurate** - Matches current code
- [ ] **Complete** - Covers all features
- [ ] **Clear** - Beginner-friendly
- [ ] **Concise** - No fluff
- [ ] **Current** - Recently updated
- [ ] **Consistent** - Uses templates
- [ ] **Actionable** - Provides examples
- [ ] **Tested** - Examples work

---

## 🎓 Learning Resources

**Internal:**
- [Quick Start](QUICK_START.md) - 5 min read
- [Full Workflow](DOCUMENTATION_WORKFLOW.md) - 15 min read
- [Knowledge Base Guide](guides/knowledge_base_guide.md) - 20 min read

**External:**
- [Markdown Guide](https://www.markdownguide.org/)
- [Google Tech Writing](https://developers.google.com/tech-writing)

---

## 🎯 Remember

> "Documentation is a love letter to your future self."

Key principles:
1. **Document as you code** (not after)
2. **Use templates** (for consistency)
3. **Validate often** (catch issues early)
4. **Keep it simple** (clear beats comprehensive)
5. **Test everything** (ensure examples work)

---

## 🔄 Daily Routine

**Morning:**
```bash
python doc_helper.py check-coverage  # What needs docs?
```

**During coding:**
```bash
# Update docs as you go
```

**Before commit:**
```bash
python doc_helper.py validate  # Everything in sync?
```

**Before release:**
```bash
python doc_helper.py changelog     # Document changes
python doc_helper.py validate      # Final check
python doc_helper.py check-coverage  # Full coverage?
```

---

**Print this out and keep it handy! 🖨️**

---

**Last Updated:** 2026-07-12
