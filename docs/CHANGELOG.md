# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation system with templates and automation
- `doc_helper.py` - Documentation automation tool
- Documentation templates for features, API endpoints, and knowledge topics
- Documentation workflow guide
- Quick start guide for documentation system
- Organized docs folder structure

### Changed
- Improved documentation organization

### Fixed
- N/A

### Removed
- N/A

---

## [1.0.0] - 2024-XX-XX

### Added
- Initial release of Clinical Supervision Chatbot
- Flask backend with rule-based NLP
- HTML/JavaScript frontend with chat interface
- 8 knowledge base topics:
  - Clinical Supervision fundamentals
  - Best Practices
  - Feedback techniques (SMART-F framework)
  - Ethics and professional standards
  - Supervision Models
  - Common Challenges and solutions
  - Documentation guidelines
  - Group Supervision
- API endpoints: /chat, /history, /reset
- Standalone HTML mode (no backend required)
- Conversation history with timestamps
- Quick action buttons for common questions
- Responsive design with modern UI
- Comprehensive README documentation

### Changed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Removed
- N/A (initial release)

---

## How to Update This Changelog

1. Add new entries under `[Unreleased]` as you make changes
2. Use these categories:
   - **Added** for new features
   - **Changed** for changes in existing functionality
   - **Deprecated** for soon-to-be removed features
   - **Removed** for now removed features
   - **Fixed** for any bug fixes
   - **Security** for vulnerability fixes

3. When releasing a new version:
   - Change `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD`
   - Create a new `[Unreleased]` section
   - Update version numbers following semantic versioning:
     - MAJOR version (X) - incompatible API changes
     - MINOR version (Y) - new functionality (backwards-compatible)
     - PATCH version (Z) - bug fixes (backwards-compatible)

### Quick Command
Generate a changelog entry template:
```bash
python doc_helper.py changelog
```
