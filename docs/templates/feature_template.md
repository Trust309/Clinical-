# Feature Template

Use this template when planning or documenting a new feature.

---

## Feature Name: [Your Feature Name]

### Overview
[2-3 sentence description of what this feature does and why it exists]

### User Story
**As a** [type of user]  
**I want** [goal/desire]  
**So that** [benefit/value]

### Status
- [ ] Planning
- [ ] In Development
- [ ] Testing
- [ ] Completed
- [ ] Deployed

### Priority
- [ ] Critical (P0)
- [ ] High (P1)
- [ ] Medium (P2)
- [ ] Low (P3)

---

## Technical Details

### Architecture
[How does this feature fit into the existing system?]

```
[Optional: ASCII diagram or flowchart]
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Feature    │
└─────────────┘
```

### Components Modified
- [ ] `chatbot_backend.py` - [What changes?]
- [ ] `chatbot.html` - [What changes?]
- [ ] `README.md` - [Documentation updates]
- [ ] Other: [Specify]

### New Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| [package-name] | [version] | [why it's needed] |

### Database Changes
- [ ] No database changes
- [ ] New tables/collections
- [ ] Schema modifications

[If yes, describe the changes]

### API Changes
- [ ] New endpoints
- [ ] Modified endpoints
- [ ] Deprecated endpoints

[List the endpoints and changes]

---

## Implementation Plan

### Step 1: [First step]
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

### Step 2: [Second step]
- [ ] Task 1
- [ ] Task 2

### Step 3: [Final step]
- [ ] Task 1
- [ ] Task 2

**Estimated Time**: [X hours/days]

---

## User Interface

### Before
[Screenshot or description of current state]
```
Current behavior or UI
```

### After
[Screenshot or description of new state]
```
New behavior or UI
```

### User Flow
1. User does [action 1]
2. System responds with [response 1]
3. User does [action 2]
4. System completes [final action]

---

## Configuration

### Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VAR_NAME` | Yes/No | `default` | What it controls |

### Settings
```python
# Example configuration
FEATURE_ENABLED = True
FEATURE_OPTION = "value"
```

---

## Testing

### Test Cases

#### Test Case 1: [Happy path]
**Given**: [Initial state]  
**When**: [Action]  
**Then**: [Expected result]

#### Test Case 2: [Edge case]
**Given**: [Initial state]  
**When**: [Action]  
**Then**: [Expected result]

#### Test Case 3: [Error handling]
**Given**: [Initial state]  
**When**: [Invalid action]  
**Then**: [Expected error handling]

### Manual Testing Checklist
- [ ] Feature works as expected
- [ ] Error handling works correctly
- [ ] UI is responsive
- [ ] Works on different browsers (if applicable)
- [ ] Existing features not broken
- [ ] Performance is acceptable

### Automated Tests
- [ ] Unit tests written
- [ ] Integration tests written
- [ ] Test coverage > 80%

---

## Documentation Updates

### Files to Update
- [ ] `README.md` - Add to features list
- [ ] `docs/API.md` - Document new endpoints
- [ ] `docs/ARCHITECTURE.md` - Update system design
- [ ] `docs/TROUBLESHOOTING.md` - Add common issues
- [ ] `docs/CHANGELOG.md` - Add entry

### Code Comments
- [ ] Added docstrings to new functions
- [ ] Commented complex logic
- [ ] Updated existing comments if changed

---

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [How to prevent/handle] |
| [Risk 2] | High/Med/Low | High/Med/Low | [How to prevent/handle] |

---

## Rollback Plan

If this feature causes issues, here's how to roll it back:

1. [Step 1 to disable/remove feature]
2. [Step 2]
3. [Step 3]

**Rollback Time Estimate**: [X minutes]

---

## Success Metrics

How will we know this feature is successful?

- [ ] [Metric 1: e.g., User engagement increases by X%]
- [ ] [Metric 2: e.g., Support tickets decrease by Y%]
- [ ] [Metric 3: e.g., Feature used by Z% of users]

### Monitoring
- [ ] Logging added for key actions
- [ ] Error tracking configured
- [ ] Performance metrics tracked

---

## Open Questions

1. [Question 1 that needs answering?]
2. [Question 2?]

---

## References

- [Link to related issue/ticket]
- [Link to design mockups]
- [Link to research/documentation]

---

## Timeline

| Milestone | Date | Status |
|-----------|------|--------|
| Planning Complete | YYYY-MM-DD | ✅ Done / 🔄 In Progress / ⏳ Todo |
| Development Complete | YYYY-MM-DD | ⏳ Todo |
| Testing Complete | YYYY-MM-DD | ⏳ Todo |
| Documentation Complete | YYYY-MM-DD | ⏳ Todo |
| Deployed to Production | YYYY-MM-DD | ⏳ Todo |

---

**Created**: [Date]  
**Last Updated**: [Date]  
**Owner**: [Your Name]  
**Reviewers**: [Names of people who should review]
