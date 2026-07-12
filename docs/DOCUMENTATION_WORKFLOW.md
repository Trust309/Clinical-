# Documentation Workflow Guide

This guide provides a streamlined process for maintaining documentation in this project.

## Quick Start

1. **Before making code changes**: Update relevant docs first (TDD for docs)
2. **After making code changes**: Run `python doc_helper.py validate` to check consistency
3. **Adding new features**: Use templates from `docs/templates/`
4. **Weekly**: Review and update the CHANGELOG

## Documentation Structure

```
docs/
├── DOCUMENTATION_WORKFLOW.md  (This file - your documentation process guide)
├── API.md                      (API endpoint documentation)
├── ARCHITECTURE.md             (System design & knowledge base structure)
├── DEPLOYMENT.md               (Deployment guides)
├── TROUBLESHOOTING.md          (Common issues & solutions)
├── CUSTOMIZATION.md            (How to extend the chatbot)
├── CHANGELOG.md                (Version history)
├── templates/                  (Documentation templates)
│   ├── feature_template.md
│   ├── api_endpoint_template.md
│   └── knowledge_topic_template.md
└── guides/                     (Additional guides)
    └── knowledge_base_guide.md
```

## Documentation Types & When to Use Them

### 1. API Documentation (`docs/API.md`)
**Update when**: Adding/modifying API endpoints

**Template**: `docs/templates/api_endpoint_template.md`

**Quick command**:
```bash
python doc_helper.py add-endpoint "endpoint_name"
```

### 2. Knowledge Base Topics
**Update when**: Adding new chatbot knowledge

**Template**: `docs/templates/knowledge_topic_template.md`

**Quick command**:
```bash
python doc_helper.py add-topic "topic_name"
```

### 3. Features (`README.md`)
**Update when**: Adding user-facing features

**Template**: `docs/templates/feature_template.md`

### 4. Troubleshooting (`docs/TROUBLESHOOTING.md`)
**Update when**: Solving a tricky bug or common issue

**Format**: Problem → Solution pairs

### 5. Changelog (`docs/CHANGELOG.md`)
**Update when**: Preparing for a release

**Format**: Semantic versioning with categories (Added/Changed/Fixed/Removed)

## Automated Documentation Helpers

### `doc_helper.py` - Your Documentation Assistant

```bash
# Validate all documentation is consistent
python doc_helper.py validate

# Generate API docs from code
python doc_helper.py generate-api

# Add a new knowledge topic with template
python doc_helper.py add-topic "Ethics in Supervision"

# Add a new API endpoint documentation
python doc_helper.py add-endpoint "export-history"

# Check for missing documentation
python doc_helper.py check-coverage

# Generate CHANGELOG entry
python doc_helper.py changelog
```

## Daily Workflow

### When Adding a Feature

1. **Start with docs** (prevents forgetting later):
   ```bash
   # Copy the feature template
   cp docs/templates/feature_template.md docs/temp_feature.md
   # Fill it out while planning
   ```

2. **Implement the feature**

3. **Update relevant docs**:
   - README.md → Features section
   - API.md → If API changed
   - ARCHITECTURE.md → If structure changed

4. **Validate**:
   ```bash
   python doc_helper.py validate
   ```

### When Fixing a Bug

1. **Document the issue** in TROUBLESHOOTING.md:
   - What was the problem?
   - What caused it?
   - How to fix it?

2. **Fix the bug**

3. **Update CHANGELOG.md** under "Fixed" section

### When Answering Questions

If you find yourself explaining something that's not documented:
1. Add it to the appropriate doc immediately
2. This prevents answering the same question twice

## Documentation Best Practices

### ✅ Do's

- **Write for beginners**: Assume readers are new to the project
- **Use examples**: Show, don't just tell
- **Keep it current**: Update docs with code changes
- **Use templates**: Consistency helps readability
- **Test your examples**: Ensure code examples actually work
- **Link liberally**: Cross-reference related documentation

### ❌ Don'ts

- **Don't duplicate**: Link to existing docs instead of copying
- **Don't assume knowledge**: Explain acronyms and jargon
- **Don't skip validation**: Always run `doc_helper.py validate`
- **Don't write novels**: Be concise and scannable
- **Don't commit broken links**: Check all references

## Quick Reference Commands

| Task | Command |
|------|---------|
| Validate all docs | `python doc_helper.py validate` |
| Add API endpoint docs | `python doc_helper.py add-endpoint "name"` |
| Add knowledge topic | `python doc_helper.py add-topic "name"` |
| Check documentation coverage | `python doc_helper.py check-coverage` |
| Generate changelog entry | `python doc_helper.py changelog` |
| Preview docs locally | `python -m http.server 8000` (then open README) |

## Documentation Review Checklist

Before committing documentation changes:

- [ ] All code examples are tested and working
- [ ] Links are valid (no 404s)
- [ ] Spelling and grammar checked
- [ ] Consistent formatting (headings, code blocks, lists)
- [ ] Images/diagrams have alt text
- [ ] Version numbers updated if applicable
- [ ] CHANGELOG.md updated
- [ ] No sensitive information (API keys, passwords)
- [ ] Cross-references are accurate

## Tips for Effective Documentation

1. **Use the 5-minute test**: Can a new developer understand and use your feature in 5 minutes from reading the docs?

2. **Document the "why"**: Code shows "what", comments show "how", docs should show "why"

3. **Visual aids**: A diagram is worth a thousand words
   - Use ASCII diagrams for simple flows
   - Use tools like draw.io for complex architectures

4. **Version your docs**: When making breaking changes, document migration paths

5. **Get feedback**: Ask teammates if docs are clear

## Maintaining Documentation

### Weekly Tasks
- Review open issues for documentation needs
- Check for outdated screenshots or examples
- Update CHANGELOG for upcoming release

### Monthly Tasks
- Review all documentation for accuracy
- Check for broken links
- Update dependency versions in installation guides

### Release Tasks
- Finalize CHANGELOG
- Update version numbers
- Review README for accuracy
- Tag documentation with release version

## Getting Help

- **For documentation questions**: See this workflow guide
- **For technical writing tips**: Check out [Google's Technical Writing Guide](https://developers.google.com/tech-writing)
- **For templates**: Use files in `docs/templates/`
- **For automation**: Use `doc_helper.py --help`

---

**Remember**: Good documentation is a gift to your future self and your users. Keep it simple, keep it current, and keep it useful!
