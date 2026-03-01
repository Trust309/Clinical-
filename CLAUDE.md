# CLAUDE.md — NWLVH Clinical Supervision Chatbot

This file provides guidance for AI assistants (Claude Code and similar tools) working in this repository.

---

## Project Overview

**NWLVH Clinical Supervision Chatbot** is a rule-based conversational assistant for clinical supervision guidance at NWLVH (North West London Veterinary Hospital or equivalent healthcare organisation). It helps supervisors and supervisees navigate clinical supervision best practices, ethics, feedback techniques, documentation, and more.

The system ships in two independent deployment modes that share the same domain knowledge but have separate implementations:

| Mode | Entry point | Backend | Notes |
|---|---|---|---|
| Standalone | `chatbot.html` | None (browser-only) | Open in any browser, zero setup |
| Flask API | `chatbot_backend.py` | Python + Flask | REST API on `localhost:5000` |

---

## Repository Structure

```
Clinical-/
├── chatbot.html          # Standalone frontend + embedded JS knowledge base
├── chatbot_backend.py    # Flask backend with REST API and Python knowledge base
├── requirements.txt      # Python dependencies: Flask 3.0.0, flask-cors 4.0.0
├── README.md             # End-user documentation
└── .gitignore            # (currently a generic ActionScript template — Python/Node entries are absent)
```

There is no build system, no test suite, and no package.json. The project has minimal tooling by design.

---

## Architecture & Key Conventions

### Dual knowledge base (important)

The knowledge base exists in **two places** that must be kept in sync:

1. **`chatbot_backend.py`** — `ClinicalSupervisionChatbot.knowledge_base` dict (Python, server-side)
2. **`chatbot.html`** — `knowledgeBase` JS object inside the `<script>` block (client-side)

When adding or editing a knowledge-base topic, update **both** files. The Python version is slightly more detailed (e.g. includes `group_supervision`); the JS version is a condensed mirror.

### Knowledge base schema

Each entry follows this pattern:

```python
# Python (chatbot_backend.py)
'topic_key': {
    'keywords': ['list', 'of', 'trigger', 'words'],
    'response': "Full response text shown to user."
}
```

```js
// JavaScript (chatbot.html)
'topic key': {
    keywords: ['list', 'of', 'trigger', 'words'],
    response: "Full response text shown to user."
}
```

Matching is **case-insensitive substring search** — the first matching keyword wins. Keyword order within each entry matters; more specific phrases should appear before generic ones.

### Response logic order (both implementations)

1. Greeting detection (`hello`, `hi`, `hey`, `good morning`, `good afternoon`)
2. Thanks detection (`thank`, `thanks`, `appreciate`)
3. Short help request (`help` + fewer than 5 words)
4. Knowledge base scan (first keyword match wins)
5. Default fallback response

In the standalone HTML version, the JS `generateResponse()` function checks the knowledge base **first**, then greetings/thanks/help. This ordering differs slightly from the Python backend — keep this in mind when debugging response inconsistencies.

### Flask backend (`chatbot_backend.py`)

- **Class**: `ClinicalSupervisionChatbot` — instantiated once as a module-level singleton (`chatbot = ClinicalSupervisionChatbot()`).
- **State**: `conversation_history` is in-memory only; it resets when the server restarts.
- **Routes**:
  - `GET /` — Returns an HTML info page (not the chat UI)
  - `POST /chat` — JSON `{"message": "..."}` → JSON `{"response": "...", "timestamp": "..."}`
  - `GET /history` — Returns `{"history": [...]}`
  - `POST /reset` — Clears history, returns confirmation
- **CORS**: Enabled globally via `flask_cors.CORS(app)` — all origins accepted.
- **Port**: `5000` (configurable in the `app.run()` call at the bottom of the file).
- **Debug mode**: `debug=True` is set for local development. Disable for any production deployment.

### Frontend (`chatbot.html`)

- Pure HTML/CSS/JS — **no external libraries or CDN dependencies**.
- All logic is in a single `<script>` block at the bottom.
- The frontend operates **completely offline** — it never calls the Flask backend. The two implementations are parallel, not integrated.
- UI colour scheme: purple gradient `#667eea → #764ba2`.
- Simulates a typing delay of 1–2 seconds (`1000 + Math.random() * 1000` ms) before showing responses.
- Messages are rendered with `textContent` (not `innerHTML`), so markdown in responses is displayed as plain text. Do not rely on markdown formatting for the HTML frontend.

---

## Development Workflow

### Running the standalone version

```bash
# Just open the file — no server needed
open chatbot.html   # macOS
xdg-open chatbot.html  # Linux
```

### Running the Flask backend

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
python chatbot_backend.py
# → http://localhost:5000
```

### Testing the API manually

```bash
# Send a chat message
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is clinical supervision?"}'

# Get conversation history
curl http://localhost:5000/history

# Reset conversation
curl -X POST http://localhost:5000/reset
```

There are no automated tests. When adding features, manually verify both the standalone HTML version and the Flask API endpoints.

---

## Adding a New Knowledge Base Topic

1. Add the entry to `ClinicalSupervisionChatbot.knowledge_base` in `chatbot_backend.py`:

```python
'new_topic': {
    'keywords': ['keyword one', 'keyword two'],
    'response': """Response text here."""
}
```

2. Add the matching entry to `knowledgeBase` in `chatbot.html`:

```js
'new topic': {
    keywords: ['keyword one', 'keyword two'],
    response: "Response text here."
}
```

3. Add a quick-action button to the `#quickActions` div in `chatbot.html` if the topic is commonly queried:

```html
<button class="quick-action-btn" onclick="sendQuickMessage('Your question here')">Label</button>
```

---

## Known Limitations & Technical Debt

- **No tests**: There is no test suite. Add `pytest` tests before introducing complex logic changes.
- **Duplicate knowledge bases**: The JS and Python knowledge bases diverge over time. Consider making the HTML version call the Flask API instead of maintaining its own copy.
- **In-memory conversation state**: The Flask chatbot's `conversation_history` is on a global singleton and is shared across all users. Multi-user deployments will mix conversation histories.
- **`.gitignore` is wrong**: The current `.gitignore` is a Flash/ActionScript template. It does not exclude Python artefacts (`__pycache__/`, `*.pyc`, `venv/`, `.env`). Add these before committing any Python build artefacts.
- **Debug mode enabled**: `app.run(debug=True)` must be changed to `debug=False` before any non-local deployment.
- **No input sanitisation on the backend**: The `/chat` endpoint does not enforce message length limits. Add validation if deploying beyond local use.

---

## Security & Privacy Notes

- The standalone HTML version stores nothing server-side; conversation data lives in the browser's DOM only.
- The Flask backend stores conversation history in memory — no database, no disk writes.
- Do not enter real patient data or personally identifiable information (PII) into the chatbot.
- CORS is fully open (`*`). Restrict this before any networked deployment.

---

## Dependency Management

```
Flask==3.0.0
flask-cors==4.0.0
```

Python 3.7+ is required. No JavaScript package manager is used. To update dependencies, edit `requirements.txt` directly and re-run `pip install -r requirements.txt`.

---

## Git Conventions

- Main branch: `master`
- Feature/task branches: `claude/<description>-<session-id>` (used for AI-assisted development)
- Commit messages are descriptive and written in imperative mood (e.g. "Add group supervision topic")
- No CI/CD pipeline is configured
