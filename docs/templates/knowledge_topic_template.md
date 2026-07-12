# Knowledge Topic Template

Use this template when adding a new knowledge topic to the chatbot.

---

## Topic: [Topic Name]

### Category
[e.g., Clinical Supervision, Ethics, Best Practices, etc.]

### Keywords/Triggers
List the keywords that should trigger this topic:
- [keyword1]
- [keyword2]
- [keyword3]
- [phrase example]
- [another trigger]

### Purpose
[Why is this topic important? What user need does it address?]

---

## Content Structure

### Main Response
[The primary information that should be provided when this topic is triggered]

**Example response**:
```
[Write the actual chatbot response here as users will see it]
```

### Follow-up Information
[Additional details for deeper questions]

### Related Topics
- [Related Topic 1] - [How it relates]
- [Related Topic 2] - [How it relates]

---

## Response Variations

Different ways to present this information based on context:

### Variation 1: Brief Summary
**Trigger**: [When to use - e.g., "quick overview", "summarize"]
```
[Concise version of the response]
```

### Variation 2: Detailed Explanation
**Trigger**: [When to use - e.g., "explain in detail", "tell me more"]
```
[Comprehensive version with examples]
```

### Variation 3: Practical Examples
**Trigger**: [When to use - e.g., "give me an example", "how do I"]
```
[Response focused on real-world application]
```

---

## Code Implementation

### Backend (`chatbot_backend.py`)

#### 1. Add to Knowledge Base
```python
"[topic_key]": {
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "responses": [
        "[Main response text]",
        "[Alternative response 1]",
        "[Alternative response 2]"
    ]
}
```

#### 2. Specific Matching Logic (if needed)
```python
# If this topic needs special matching beyond keywords
def _match_[topic_name](self, message: str) -> bool:
    """
    Custom matching logic for [topic name]
    
    Args:
        message: User's message
        
    Returns:
        True if this topic should be triggered
    """
    # Custom logic here
    pass
```

### Frontend (`chatbot.html`)

#### Add to Local Knowledge Base
```javascript
[topic_key]: {
    keywords: ["keyword1", "keyword2", "keyword3"],
    responses: [
        "[Main response text]",
        "[Alternative response 1]",
        "[Alternative response 2]"
    ]
}
```

---

## Examples & Test Cases

### Example 1: Basic Question
**User Input**: "[typical user question]"  
**Expected Response**: "[what the bot should say]"  
**Reason**: [why this response is appropriate]

### Example 2: Follow-up Question
**User Input**: "[follow-up question]"  
**Expected Response**: "[what the bot should say]"  
**Reason**: [why this response is appropriate]

### Example 3: Edge Case
**User Input**: "[unusual or edge case question]"  
**Expected Response**: "[what the bot should say]"  
**Reason**: [how to handle this edge case]

---

## Validation

### Quality Checklist
- [ ] **Accurate**: Information is factually correct and up-to-date
- [ ] **Clear**: Language is simple and easy to understand
- [ ] **Concise**: No unnecessary jargon or verbosity
- [ ] **Complete**: Addresses the question fully
- [ ] **Actionable**: Provides practical guidance when applicable
- [ ] **Empathetic**: Tone is supportive and professional
- [ ] **Unbiased**: Presents balanced information
- [ ] **Safe**: No harmful or inappropriate content

### Testing
- [ ] Tested with exact keywords
- [ ] Tested with variations of keywords
- [ ] Tested with related questions
- [ ] Tested edge cases
- [ ] Verified response quality
- [ ] Checked for typos/grammar

---

## Sources & References

### Expert Sources
- [Reference 1: Book, article, or expert source]
- [Reference 2]
- [Reference 3]

### Internal References
- [Link to related documentation]
- [Link to research notes]

### Verification
- [ ] Content reviewed by subject matter expert
- [ ] References verified and current
- [ ] Aligns with professional standards

---

## Maintenance

### Review Schedule
- [ ] Quarterly review
- [ ] Annual deep review
- [ ] As-needed when policies/practices change

### Update Triggers
When should this topic be reviewed/updated?
- [Trigger 1: e.g., "New guidelines published"]
- [Trigger 2: e.g., "User feedback indicates confusion"]
- [Trigger 3: e.g., "Related regulations change"]

### Version History
| Version | Date | Changes | Reviewer |
|---------|------|---------|----------|
| 1.0 | YYYY-MM-DD | Initial creation | [Name] |

---

## Analytics & Feedback

### Success Metrics
How will we measure if this topic is helpful?
- [ ] User satisfaction (thumbs up/down if implemented)
- [ ] Follow-up question rate
- [ ] Topic engagement frequency
- [ ] User feedback comments

### User Feedback
[Placeholder for user feedback once implemented]

### Improvement Ideas
- [Idea 1 for how to make this topic better]
- [Idea 2]

---

## Special Considerations

### Sensitivity
- [ ] This topic involves sensitive information
- [ ] This topic requires disclaimers
- [ ] This topic may need content warnings

[If yes, explain how to handle sensitively]

### Disclaimers Needed
```
[Any legal or professional disclaimers that should accompany this information]
```

### Limitations
What this topic doesn't cover:
- [Limitation 1]
- [Limitation 2]

### Escalation
When should this topic recommend users seek additional help?
- [Scenario 1: e.g., "If crisis situation"]
- [Scenario 2: e.g., "If legal question"]

---

## Integration

### Links to Other Features
- [ ] Quick action button on frontend
- [ ] Mentioned in welcome message
- [ ] Part of help menu
- [ ] Linked from related topics

### Documentation Updates
- [ ] Added to README features list
- [ ] Added to API documentation
- [ ] Added to knowledge base guide
- [ ] Updated CHANGELOG

---

**Created**: [Date]  
**Last Updated**: [Date]  
**Created By**: [Your Name]  
**Reviewers**: [Names]  
**Status**: [Draft / In Review / Approved / Live]
