# NWLVH Clinical Supervision Chatbot

An intelligent chatbot assistant designed to provide guidance and support for clinical supervision practices. This tool helps supervisors and supervisees navigate the complexities of clinical supervision through an interactive, knowledge-based interface.

## Features

- **Interactive Chat Interface**: Modern, user-friendly web interface with real-time responses
- **Comprehensive Knowledge Base**: Covers key topics including:
  - Clinical supervision fundamentals
  - Best practices and guidelines
  - Effective feedback techniques
  - Ethical considerations
  - Supervision models and frameworks
  - Common challenges and solutions
  - Documentation requirements
  - Session frequency recommendations
  - Group supervision approaches

- **Quick Actions**: Pre-configured buttons for common questions
- **Professional Design**: Clean, accessible interface suitable for healthcare professionals
- **Flexible Deployment**: Available as standalone HTML or Flask-based backend

## Getting Started

### Option 1: Standalone HTML Version (Simplest)

1. Open `chatbot.html` in any modern web browser
2. Start chatting immediately - no installation required!

This version runs entirely in your browser with no server setup needed.

### Option 2: Flask Backend Version (Advanced)

For a more robust deployment with API capabilities:

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask Server**
   ```bash
   python chatbot_backend.py
   ```

3. **Access the Chatbot**
   - API will be available at `http://localhost:5000`
   - Use the HTML interface to interact with the backend
   - Or integrate with your own frontend using the API endpoints

## 📚 Documentation

Comprehensive documentation is available in the `docs/` folder:

- **[Quick Start Guide](docs/QUICK_START.md)** - Get started with documentation in 5 minutes
- **[Documentation Workflow](docs/DOCUMENTATION_WORKFLOW.md)** - Complete guide to maintaining docs
- **[API Documentation](docs/API.md)** - Detailed API reference (auto-generated)
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Changelog](docs/CHANGELOG.md)** - Version history and changes
- **[Cheat Sheet](docs/CHEATSHEET.md)** - Quick reference for common tasks

### Documentation Helper Tool

We provide an automated documentation helper:

```bash
# Validate documentation is consistent
python doc_helper.py validate

# Check what's documented
python doc_helper.py check-coverage

# Add new knowledge topic
python doc_helper.py add-topic "Topic Name"

# Generate API documentation
python doc_helper.py generate-api
```

For more details, see [docs/README.md](docs/README.md).

## API Endpoints (Flask Version)

- `POST /chat` - Send a message and receive a response
  ```json
  {
    "message": "What is clinical supervision?"
  }
  ```

- `GET /history` - Retrieve conversation history

- `POST /reset` - Reset the conversation

## Usage Examples

### Common Questions

- "What is clinical supervision?"
- "What are the best practices for supervision sessions?"
- "How do I provide effective feedback?"
- "What are the ethical considerations in supervision?"
- "How often should supervision sessions occur?"
- "What supervision models are available?"
- "How should I document supervision sessions?"

### Use Cases

1. **New Supervisors**: Learn fundamentals and best practices
2. **Experienced Supervisors**: Quick reference for specific situations
3. **Supervisees**: Understand what to expect from supervision
4. **Training Programs**: Educational resource for supervision training
5. **Quality Assurance**: Reference for organizational policies

## Topics Covered

### Clinical Supervision Fundamentals
- Definition and purpose
- Key components
- Importance for patient safety and clinician wellbeing

### Best Practices
- Structure and scheduling
- Creating a safe environment
- Documentation standards
- Professional development focus

### Effective Feedback
- SMART-F framework
- Constructive delivery
- Follow-up strategies

### Ethics
- Confidentiality and boundaries
- Professional competence
- Cultural sensitivity
- Duty of care

### Supervision Models
- Developmental models
- Process-based approaches
- Reflective practice
- Competency-based frameworks
- Integrated approaches

### Common Challenges
- Time management
- Performance issues
- Boundary violations
- Cultural differences
- Remote supervision

## Customization

The chatbot can be easily customized to fit your organization's needs:

1. **Update Knowledge Base**: Edit the `knowledge_base` in `chatbot_backend.py` or the JavaScript in `chatbot.html`
   - Use `python doc_helper.py add-topic "Topic Name"` to generate a template
   - See [Knowledge Base Guide](docs/guides/knowledge_base_guide.md) for details
2. **Modify Branding**: Update headers, colors, and styling in the HTML/CSS
3. **Add New Topics**: Extend the knowledge base with organization-specific policies
4. **Integrate with Systems**: Use the Flask API to connect with existing platforms

For detailed customization guides, see the [documentation](docs/).

## Technical Details

- **Frontend**: HTML5, CSS3, JavaScript (vanilla - no dependencies)
- **Backend**: Python 3.7+, Flask, Flask-CORS
- **Architecture**: Rule-based natural language processing with keyword matching
- **Deployment**: Can run locally, on internal servers, or cloud platforms

## Security & Privacy

- No data is sent to external servers in standalone mode
- Conversation history stored in memory only (resets on page refresh)
- No personal health information should be entered
- Follow your organization's data security policies

## Contributing

To enhance the chatbot:

1. **Add new topics** to the knowledge base - Use `python doc_helper.py add-topic "Name"`
2. **Improve response accuracy** - Follow the [Knowledge Base Guide](docs/guides/knowledge_base_guide.md)
3. **Enhance UI/UX design** - Document changes using [Feature Template](docs/templates/feature_template.md)
4. **Add multilingual support**
5. **Integrate with AI/ML models** for advanced responses

Before contributing:
- Read the [Documentation Workflow](docs/DOCUMENTATION_WORKFLOW.md)
- Use the provided templates in `docs/templates/`
- Run `python doc_helper.py validate` before committing
- Update the [Changelog](docs/CHANGELOG.md)

## Support

For questions, issues, or feature requests related to clinical supervision practices, consult with your organization's clinical supervision lead or professional development team.

## License

This project is designed for educational and professional development purposes in healthcare settings.

## Acknowledgments

Developed for NWLVH (Clinical Supervision) to support excellence in clinical supervision practices and professional development.

---

**Note**: This chatbot provides general guidance on clinical supervision. Always refer to your organization's specific policies, professional code of ethics, and regulatory requirements for your jurisdiction 
