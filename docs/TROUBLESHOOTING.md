# Troubleshooting Guide

Common issues and their solutions for the Clinical Supervision Chatbot.

## Table of Contents
- [Backend Issues](#backend-issues)
- [Frontend Issues](#frontend-issues)
- [API Issues](#api-issues)
- [Knowledge Base Issues](#knowledge-base-issues)
- [Deployment Issues](#deployment-issues)

---

## Backend Issues

### Issue: Flask app won't start

**Symptoms:**
- Error: `ModuleNotFoundError: No module named 'flask'`
- Server fails to start

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or install Flask specifically
pip install Flask==3.0.0 flask-cors==4.0.0
```

**Verification:**
```bash
python -c "import flask; print(flask.__version__)"
```

---

### Issue: CORS errors when connecting frontend to backend

**Symptoms:**
- Browser console shows: `Access-Control-Allow-Origin` error
- Chat messages don't reach the backend

**Solution:**
Ensure Flask-CORS is properly installed and configured:

```python
# In chatbot_backend.py, verify this exists:
from flask_cors import CORS
CORS(app)
```

**Workaround:**
Use the standalone HTML version which doesn't require backend.

---

### Issue: Port 5000 already in use

**Symptoms:**
- Error: `Address already in use`
- Can't start Flask server

**Solution:**
```bash
# Option 1: Kill the process using port 5000
lsof -ti:5000 | xargs kill -9

# Option 2: Use a different port
python chatbot_backend.py --port 5001
```

Or modify the code:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change port here
```

---

## Frontend Issues

### Issue: Chatbot doesn't respond in standalone HTML mode

**Symptoms:**
- Messages sent but no response
- No errors in console

**Solution:**
Standalone HTML mode uses local knowledge base. Verify JavaScript is enabled:

1. Open browser console (F12)
2. Check for JavaScript errors
3. Ensure you're opening the file via a web server or using `file://` protocol

**Better approach:**
```bash
# Serve HTML via simple web server
python -m http.server 8000
# Then open: http://localhost:8000/chatbot.html
```

---

### Issue: Typing indicator doesn't disappear

**Symptoms:**
- "Typing..." animation stays visible
- Response appears but indicator remains

**Solution:**
This is usually a timing issue. Refresh the page or check browser console for errors.

**Code fix:**
Look for the `hideTypingIndicator()` call in the JavaScript and ensure it's being called.

---

### Issue: Chat history not displaying

**Symptoms:**
- Previous messages don't show up
- Chat appears empty after refresh

**Cause:**
Chat history is not persisted by default. It's stored in memory only.

**Solution:**
This is expected behavior. To persist chat history, you need to:
1. Use backend mode (not standalone)
2. Implement session storage or database persistence

---

## API Issues

### Issue: `/chat` endpoint returns 500 error

**Symptoms:**
```json
{
  "success": false,
  "error": "Internal server error"
}
```

**Debugging steps:**
```bash
# 1. Check server logs
# Look for Python traceback in terminal where Flask is running

# 2. Verify request format
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

**Common causes:**
- Missing `message` field in request
- Invalid JSON format
- Backend crashed (check terminal)

---

### Issue: `/history` endpoint returns empty array

**Symptoms:**
```json
{
  "success": true,
  "history": []
}
```

**Cause:**
This is normal if:
- No messages have been sent yet
- Server was restarted (history is in-memory only)

**Solution:**
Send a message first, then check history:
```bash
# 1. Send a message
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'

# 2. Check history
curl http://localhost:5000/history
```

---

## Knowledge Base Issues

### Issue: Chatbot doesn't recognize keywords

**Symptoms:**
- Known keywords don't trigger responses
- Bot gives generic "I don't understand" response

**Debugging:**
```python
# Add debug logging to chatbot_backend.py
print(f"User message: {message}")
print(f"Detected keywords: {self._extract_keywords(message)}")
```

**Solution:**
1. Check keyword spelling in `knowledge_base` dictionary
2. Verify case sensitivity (keywords should be lowercase)
3. Ensure keywords are in the correct topic

**Test:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "what is clinical supervision"}'
```

---

### Issue: Backend and frontend knowledge bases are out of sync

**Symptoms:**
- Standalone mode works but backend mode doesn't (or vice versa)
- Different responses for same query

**Solution:**
```bash
# Use the documentation helper to validate
python doc_helper.py validate
```

This will show which topics differ between backend and frontend.

**Manual fix:**
Ensure both `chatbot_backend.py` and `chatbot.html` have the same:
- Topic names
- Keywords
- Responses

---

## Deployment Issues

### Issue: Backend works locally but not on server

**Symptoms:**
- Works on `localhost` but not on deployed server
- Connection refused errors

**Checklist:**
- [ ] Firewall allows traffic on Flask port
- [ ] Server is binding to `0.0.0.0` not `127.0.0.1`
- [ ] CORS is configured for production domain
- [ ] Dependencies are installed on server

**Solution:**
```python
# Change this:
app.run(debug=True)

# To this for production:
app.run(host='0.0.0.0', port=5000, debug=False)
```

---

### Issue: Standalone HTML doesn't work after deployment

**Symptoms:**
- Works locally but not when deployed to web server
- Mixed content warnings (HTTP/HTTPS)

**Solution:**
Ensure all resources are loaded via HTTPS if your site uses HTTPS:

```html
<!-- Don't use HTTP resources on HTTPS site -->
```

For standalone mode, all resources should be embedded or relative paths.

---

## Performance Issues

### Issue: Slow response times

**Symptoms:**
- Chatbot takes several seconds to respond
- High CPU usage

**Debugging:**
```python
# Add timing to chatbot_backend.py
import time

@app.route('/chat', methods=['POST'])
def chat():
    start_time = time.time()
    # ... existing code ...
    print(f"Response time: {time.time() - start_time:.2f}s")
```

**Common causes:**
- Large conversation history
- Complex keyword matching
- Server resource constraints

**Solutions:**
- Limit conversation history size
- Optimize keyword matching logic
- Add response caching for common queries

---

## Documentation Helper Issues

### Issue: `doc_helper.py` validation fails

**Symptoms:**
```
⚠️ Knowledge base topics differ between backend and frontend
```

**Solution:**
This means the topics in `chatbot_backend.py` and `chatbot.html` don't match.

1. Run coverage check to see what's missing:
   ```bash
   python doc_helper.py check-coverage
   ```

2. Add missing topics to both files

3. Validate again:
   ```bash
   python doc_helper.py validate
   ```

---

## Still Having Issues?

If your issue isn't listed here:

1. **Check the logs**: Look for error messages in:
   - Browser console (F12)
   - Flask terminal output
   - System logs

2. **Test in isolation**:
   - Try standalone HTML mode
   - Try backend with curl
   - Test individual components

3. **Check dependencies**:
   ```bash
   pip list | grep -i flask
   ```

4. **Reset and retry**:
   ```bash
   # Reset conversation
   curl -X POST http://localhost:5000/reset
   ```

5. **Document the issue**:
   - What did you do?
   - What did you expect?
   - What actually happened?
   - Add your issue to this file to help others!

---

## How to Report Issues

When reporting issues, include:

1. **Environment**:
   - OS and version
   - Python version
   - Browser and version (for frontend issues)

2. **Steps to reproduce**:
   - Numbered list of exact steps

3. **Expected vs Actual**:
   - What you expected to happen
   - What actually happened

4. **Error messages**:
   - Full error text
   - Stack traces
   - Console output

5. **What you've tried**:
   - Troubleshooting steps already attempted

---

**Last Updated:** 2026-07-12
