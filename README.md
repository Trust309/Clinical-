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
2. **Modify Branding**: Update headers, colors, and styling in the HTML/CSS
3. **Add New Topics**: Extend the knowledge base with organization-specific policies
4. **Integrate with Systems**: Use the Flask API to connect with existing platforms

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

1. Add new topics to the knowledge base
2. Improve response accuracy
3. Enhance UI/UX design
4. Add multilingual support
5. Integrate with AI/ML models for advanced responses

## Support

For questions, issues, or feature requests related to clinical supervision practices, consult with your organization's clinical supervision lead or professional development team.

## License

This project is designed for educational and professional development purposes in healthcare settings.

## Acknowledgments

Developed for NWLVH (Clinical Supervision) to support excellence in clinical supervision practices and professional development.

---

**Note**: This chatbot provides general guidance on clinical supervision. Always refer to your organization's specific policies, professional code of ethics, and regulatory requirements for your jurisdiction

---

# NWLVH New Starter Progress Tracker

A tool for monitoring the onboarding progress of new starters at NWLVH, from pre-employment checks through to the end of probation. It tracks each new starter against a structured checklist and flags anyone falling behind.

## Features

- **Per-starter onboarding checklist** covering:
  - Pre-employment checks (DBS, references, occupational health, right to work, registration)
  - IT & systems access
  - Day 1 induction
  - Mandatory training
  - Local induction & orientation
  - Clinical supervision & competency sign-off
  - Probation review milestones (4-week, 12-week, 6-month)
- **Automatic progress tracking**: percentage complete per starter, calculated live from checked-off items
- **At-risk detection**: starters whose progress lags well behind where they should be by their week-in-post are automatically flagged "At Risk"
- **Dashboard stats**: total starters, in progress, completed, at risk, and average progress across the team
- **Search & filter** by name, role, department, or status
- **Notes** field per starter for anything that doesn't fit the checklist
- **Export/Import** as JSON for backup or sharing
- **Flexible Deployment**: standalone HTML (offline, no install) or Flask-based backend for shared/multi-user tracking

## Getting Started

### Option 1: Standalone HTML Version (Simplest)

1. Open `tracker.html` in any modern web browser
2. Click **+ Add New Starter** to begin tracking

Data is saved automatically to your browser's local storage, so it persists between visits on the same device. Use **Export Data** to back up or hand off the tracker's data as a JSON file, and **Import Data** to load it elsewhere.

### Option 2: Flask Backend Version (Shared/Multi-user)

For teams that need a shared, server-side tracker:

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask Server**
   ```bash
   python tracker_backend.py
   ```

3. **Access the API**
   - API will be available at `http://localhost:5001`
   - Data is persisted to `tracker_data.json` next to the script
   - Build your own frontend against the API, or adapt `tracker.html` to call it instead of local storage

## API Endpoints (Flask Version)

- `GET /starters` - List all new starters, with computed progress and status
- `GET /starters/summary` - Aggregate stats (totals, average progress, at-risk count)
- `POST /starters` - Add a new starter (`name`, `role`, `department`, `startDate` required; `supervisor` optional)
- `GET /starters/<id>` - Get a single starter
- `PUT /starters/<id>` - Update a starter's details
- `PATCH /starters/<id>/checklist/<item_id>` - Toggle a checklist item (`{"done": true}`)
- `PUT /starters/<id>/notes` - Update notes
- `DELETE /starters/<id>` - Remove a starter

## How Progress & Risk Are Calculated

- **Progress** is the percentage of checklist items marked done out of the total across all onboarding stages.
- **Status** is one of:
  - **Completed** - 100% of checklist items done
  - **At Risk** - progress is significantly behind the expected pace for a standard 12-week probation period
  - **In Progress** - everything else

## Customization

1. **Update the Checklist**: Edit `CHECKLIST_TEMPLATE` in `tracker.html` (and the matching copy in `tracker_backend.py` if using the backend) to match your organization's exact onboarding policy
2. **Adjust the Probation Period**: Change `PROBATION_WEEKS` to match your organization's probation length
3. **Modify Branding**: Update headers, colors, and styling in the HTML/CSS
4. **Integrate with Systems**: Use the Flask API to connect the tracker to HR or rostering systems

## Security & Privacy

- The standalone version stores data only in your browser's local storage - nothing is sent to external servers
- The Flask backend stores data in a local JSON file - secure this file and the server according to your organization's data protection policies
- Avoid entering sensitive personal or health information beyond what's needed to track onboarding status

---

**Note**: This tracker is a general-purpose onboarding aid. Always follow your organization's official HR onboarding policy, probation procedures, and data protection requirements.

