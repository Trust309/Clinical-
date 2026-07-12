# Knowledge Base Guide

A comprehensive guide to understanding, maintaining, and extending the Clinical Supervision Chatbot's knowledge base.

## Table of Contents
1. [Overview](#overview)
2. [Knowledge Base Structure](#knowledge-base-structure)
3. [Adding New Topics](#adding-new-topics)
4. [Keyword Matching](#keyword-matching)
5. [Response Strategy](#response-strategy)
6. [Best Practices](#best-practices)
7. [Testing](#testing)

---

## Overview

The chatbot uses a **rule-based NLP system** with keyword matching to provide responses about clinical supervision topics. The knowledge base is duplicated in two places:

- **Backend** (`chatbot_backend.py`) - For Flask API mode
- **Frontend** (`chatbot.html`) - For standalone mode

Both must be kept in sync for consistent behavior.

---

## Knowledge Base Structure

### Format

```python
knowledge_base = {
    "topic_name": {
        "keywords": ["keyword1", "keyword2", "phrase"],
        "responses": [
            "Main response text...",
            "Alternative response...",
            "Another variation..."
        ]
    }
}
```

### Current Topics

1. **clinical_supervision** - Fundamentals and definition
2. **best_practices** - Guidelines for effective supervision
3. **feedback** - SMART-F feedback framework
4. **ethics** - Professional and ethical standards
5. **models** - Different supervision approaches
6. **challenges** - Common issues and solutions
7. **documentation** - Record-keeping guidelines
8. **group** - Group supervision specifics

---

## Adding New Topics

### Method 1: Using the Documentation Helper (Recommended)

```bash
# Generate template
python doc_helper.py add-topic "Trauma-Informed Supervision"

# This creates: docs/topics/trauma_informed_supervision.md
```

### Method 2: Manual Addition

#### Step 1: Plan the Topic

Answer these questions:
- What user need does this address?
- What keywords would users naturally use?
- What's the most helpful response format?
- How does it relate to existing topics?

#### Step 2: Add to Backend

Edit `chatbot_backend.py`:

```python
self.knowledge_base = {
    # ... existing topics ...
    
    "trauma_informed": {
        "keywords": [
            "trauma",
            "trauma-informed",
            "traumatic",
            "ptsd",
            "trauma sensitive"
        ],
        "responses": [
            """Trauma-informed supervision recognizes the widespread impact of trauma...
            
            Key principles:
            • Safety - Physical and emotional
            • Trustworthiness - Transparency in operations
            • Peer support - Mutual self-help
            • Collaboration - Shared decision-making
            • Empowerment - Recognizing strengths
            • Cultural sensitivity - Addressing biases
            
            In supervision, this means creating a safe space..."""
        ]
    }
}
```

#### Step 3: Add to Frontend

Edit `chatbot.html`, find the `knowledgeBase` object:

```javascript
const knowledgeBase = {
    // ... existing topics ...
    
    trauma_informed: {
        keywords: [
            "trauma",
            "trauma-informed",
            "traumatic",
            "ptsd",
            "trauma sensitive"
        ],
        responses: [
            `Trauma-informed supervision recognizes the widespread impact of trauma...
            
            Key principles:
            • Safety - Physical and emotional
            • Trustworthiness - Transparency in operations
            • Peer support - Mutual self-help
            • Collaboration - Shared decision-making
            • Empowerment - Recognizing strengths
            • Cultural sensitivity - Addressing biases
            
            In supervision, this means creating a safe space...`
        ]
    }
};
```

#### Step 4: Validate

```bash
# Check that both backend and frontend match
python doc_helper.py validate

# Test the new topic
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "tell me about trauma-informed supervision"}'
```

---

## Keyword Matching

### How It Works

The chatbot uses **simple keyword matching**:

1. User message is converted to lowercase
2. Message is checked against keywords for each topic
3. If any keyword matches, that topic's response is returned
4. Multiple keyword matches = topic with most matches wins
5. No matches = generic "I don't understand" response

### Keyword Selection Best Practices

#### ✅ Good Keywords

```python
"keywords": [
    "ethics",           # Core term
    "ethical",          # Variation
    "professional standards",  # Common phrase
    "boundaries",       # Related concept
    "confidentiality"   # Specific aspect
]
```

**Why good:**
- Mix of single words and phrases
- Includes variations (ethics, ethical)
- Covers related concepts
- Natural language users would use

#### ❌ Poor Keywords

```python
"keywords": [
    "e",               # Too short, matches too much
    "standards",       # Too generic
    "ethical guidelines for clinical supervision in healthcare"  # Too specific
]
```

**Why poor:**
- Too short (high false positive rate)
- Too generic (matches unintended queries)
- Too long (users won't type exact phrase)

### Keyword Tips

1. **Use 5-10 keywords per topic** - Balance coverage and specificity

2. **Include variations**:
   ```python
   ["supervise", "supervision", "supervisor", "supervisee"]
   ```

3. **Add common phrases**:
   ```python
   ["how to give feedback", "providing feedback", "feedback techniques"]
   ```

4. **Think like users**:
   - What would they type?
   - What words would they use?
   - What questions would they ask?

5. **Avoid overlap** with other topics (if possible)

6. **Test edge cases**:
   - Typos: "supervison" (common misspelling)
   - Abbreviations: "CBT" vs "cognitive behavioral therapy"
   - Synonyms: "mentor" vs "supervisor"

---

## Response Strategy

### Response Format

#### Structure

```
[Opening statement - what this is]

[Key points in bullet or numbered format]
• Point 1
• Point 2
• Point 3

[Practical application or example]

[Optional: Related information or next steps]
```

#### Example - Good Response

```python
"responses": [
    """Clinical supervision is a formal process of professional support and learning.

    Key components:
    • Regular meetings between supervisor and supervisee
    • Reflection on practice and professional development
    • Skill development and competency building
    • Emotional support and self-care
    • Quality assurance and accountability

    Effective supervision creates a safe space for practitioners to:
    - Discuss challenging cases
    - Develop clinical skills
    - Process emotional responses
    - Ensure ethical practice

    Would you like to know more about supervision models or best practices?"""
]
```

**Why good:**
- Clear opening definition
- Organized bullet points
- Practical application
- Inviting follow-up

#### Example - Poor Response

```python
"responses": [
    "Clinical supervision is important and you should do it regularly."
]
```

**Why poor:**
- Too brief
- No actionable information
- No structure
- Doesn't invite engagement

### Multiple Responses

You can provide multiple response variations:

```python
"responses": [
    "Detailed comprehensive response...",
    "Brief summary version...",
    "Example-focused version..."
]
```

Currently, the chatbot randomly selects one. Future versions could select based on context.

---

## Best Practices

### Content Quality

1. **Be accurate**:
   - Cite sources when possible
   - Use established frameworks (like SMART-F)
   - Avoid personal opinions

2. **Be practical**:
   - Include real-world applications
   - Provide actionable steps
   - Give specific examples

3. **Be concise**:
   - Use bullet points
   - Break up long paragraphs
   - Highlight key information

4. **Be supportive**:
   - Use encouraging language
   - Acknowledge challenges
   - Offer next steps

### Maintenance

1. **Review quarterly**:
   ```bash
   # Check what topics exist
   python doc_helper.py check-coverage
   ```

2. **Update when needed**:
   - New professional guidelines
   - User feedback suggests gaps
   - Best practices evolve

3. **Keep in sync**:
   ```bash
   # Always validate after changes
   python doc_helper.py validate
   ```

4. **Document changes**:
   - Update `docs/CHANGELOG.md`
   - Note in topic documentation

### Organization

1. **Group related topics**:
   ```python
   # Ethics-related
   "ethics": {...},
   "confidentiality": {...},
   "boundaries": {...},
   ```

2. **Avoid duplication**:
   - Reference other topics instead of repeating
   - "See also: our ethics guidelines"

3. **Use clear naming**:
   - `clinical_supervision` not `cs`
   - `group_supervision` not `group_stuff`

---

## Testing

### Manual Testing

```bash
# Test each topic with its primary keywords
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "what is clinical supervision"}'

curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "tell me about ethics"}'

# Test variations
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "how do I give good feedback"}'
```

### Test Checklist

For each new topic:

- [ ] Test primary keyword
- [ ] Test each keyword variation
- [ ] Test common phrases
- [ ] Test edge cases (typos, synonyms)
- [ ] Test in both backend and frontend mode
- [ ] Verify response quality
- [ ] Check for conflicts with other topics
- [ ] Validate knowledge base sync

### Validation

```bash
# Automated validation
python doc_helper.py validate

# Manual checks
1. Same number of topics in backend and frontend?
2. Same topic names in both?
3. Same keywords in both?
4. Responses make sense?
5. No sensitive information?
```

---

## Advanced Topics

### Custom Matching Logic

For complex topics, you can add custom matching in `chatbot_backend.py`:

```python
def _match_complex_query(self, message: str) -> str:
    """Custom matching for complex queries"""
    if "supervision" in message and "group" in message:
        return "group"
    elif "supervision" in message and "individual" in message:
        return "clinical_supervision"
    return None
```

### Context Awareness

Future enhancement - remember previous topics:

```python
def _get_context_aware_response(self, message: str) -> str:
    """Consider conversation history for better responses"""
    # Check last topic discussed
    if self.conversation_history:
        last_topic = self.conversation_history[-1].get('topic')
        # Provide related information
```

### Response Personalization

Future enhancement - adapt based on user role:

```python
"responses": {
    "supervisor": "As a supervisor, you should...",
    "supervisee": "As a supervisee, you can...",
    "default": "In clinical supervision..."
}
```

---

## Examples

### Complete Topic Example

```python
"difficult_conversations": {
    "keywords": [
        "difficult conversation",
        "challenging conversation",
        "confrontation",
        "hard to talk about",
        "uncomfortable discussion",
        "performance issue"
    ],
    "responses": [
        """Navigating difficult conversations in supervision requires preparation and empathy.

        **Before the conversation:**
        • Clarify the issue and your objectives
        • Consider the supervisee's perspective
        • Choose an appropriate time and private setting
        • Review relevant policies or documentation
        
        **During the conversation:**
        • Start with positive intent and shared goals
        • Be specific about observed behaviors (not character)
        • Listen actively and validate emotions
        • Collaborate on solutions
        • Agree on concrete next steps
        
        **After the conversation:**
        • Document key points and agreements
        • Follow up on commitments
        • Provide ongoing support
        • Monitor progress
        
        Remember: Most difficult conversations are difficult because they've been avoided. Addressing issues early prevents escalation.
        
        Would you like specific strategies for performance issues or boundary violations?"""
    ]
}
```

---

## Quick Reference

### Adding a Topic Checklist

- [ ] Plan topic scope and keywords
- [ ] Generate template: `python doc_helper.py add-topic "Name"`
- [ ] Fill out template documentation
- [ ] Add to `chatbot_backend.py`
- [ ] Add to `chatbot.html`
- [ ] Validate: `python doc_helper.py validate`
- [ ] Test manually
- [ ] Update `docs/CHANGELOG.md`
- [ ] Commit changes

### Common Commands

```bash
# Create topic
python doc_helper.py add-topic "Topic Name"

# Validate knowledge base
python doc_helper.py validate

# Check coverage
python doc_helper.py check-coverage

# Test endpoint
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "your test message"}'
```

---

**Last Updated:** 2026-07-12  
**Maintained By:** Clinical Supervision Chatbot Team
