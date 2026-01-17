# Developer Configuration Guide for NHS Network Access

## Overview

This guide is specifically for developers working on the NWLVH Clinical Supervision Chatbot who need to access NHS network resources, deploy the application within NHS infrastructure, or test on NHS systems.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Development Environment Setup](#development-environment-setup)
- [NHS Network Configuration](#nhs-network-configuration)
- [Local Development on NHS Network](#local-development-on-nhs-network)
- [Deployment to NHS Infrastructure](#deployment-to-nhs-infrastructure)
- [Testing and Quality Assurance](#testing-and-quality-assurance)
- [Security Best Practices](#security-best-practices)
- [Common Development Issues](#common-development-issues)
- [CI/CD on NHS Infrastructure](#cicd-on-nhs-infrastructure)

---

## Prerequisites

### Required Access

Before starting development, ensure you have:

1. **NHS Network Credentials**
   - Valid ICHNT network account
   - VPN access approved and configured
   - Appropriate permissions for development servers

2. **Development Tools Access**
   - Git repository access
   - Development server access
   - Testing environment credentials
   - Deployment pipeline permissions

3. **Mandatory Training**
   - Information Governance training completed
   - Data Security Awareness (via ESR)
   - Developer-specific security training

4. **Software and Hardware**
   - Laptop/workstation meeting NHS security standards
   - Required development tools installed
   - VPN client configured

### Skills Required

- Python 3.7+ development
- Flask framework knowledge
- HTML/CSS/JavaScript
- Git version control
- Basic networking concepts
- Understanding of healthcare data sensitivity

---

## Development Environment Setup

### Step 1: Verify Network Access

Test your NHS network connection before starting development:

```bash
# Connect to NHS VPN first, then test connectivity

# Test internal network access
ping internal-server.ichnt.nhs.uk

# Test DNS resolution
nslookup internal-server.ichnt.nhs.uk

# Verify you can reach internal git repository
git ls-remote https://git.ichnt.nhs.uk/clinical-supervision/chatbot.git
```

### Step 2: Clone the Repository

#### From NHS Internal Git (Preferred)

```bash
# If repository is hosted on NHS internal Git
git clone https://git.ichnt.nhs.uk/clinical-supervision/chatbot.git
cd chatbot

# Configure Git with your NHS email
git config user.name "Your Name"
git config user.email "your.name@nhs.net"
```

#### From External Repository (with VPN)

```bash
# If using external Git (GitHub, GitLab) while on VPN
git clone https://github.com/Trust309/Clinical-.git
cd Clinical-

# Ensure you're working on correct branch
git checkout claude/nhs-network-access-2EMUj
```

### Step 3: Python Environment Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import flask; print(f'Flask {flask.__version__} installed')"
```

### Step 4: Configure Development Settings

Create a local configuration file for NHS-specific settings:

```bash
# Create .env file (never commit this!)
cat > .env << 'EOF'
# Flask Configuration
FLASK_APP=chatbot_backend.py
FLASK_ENV=development
FLASK_DEBUG=1

# Network Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# NHS Network Settings
NHS_NETWORK=ICHNT
NHS_PROXY_HOST=proxy.ichnt.nhs.uk
NHS_PROXY_PORT=8080

# Security
SECRET_KEY=your-secret-key-here
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True

# Logging
LOG_LEVEL=DEBUG
LOG_FILE=/var/log/clinical-supervision/app.log
EOF
```

Create `.gitignore` to protect sensitive files:

```bash
cat > .gitignore << 'EOF'
# Environment and credentials
.env
.env.local
*.pem
*.key
credentials.json

# Python
__pycache__/
*.py[cod]
*$py.class
venv/
.Python
*.so

# IDE
.vscode/
.idea/
*.swp
*.swo

# NHS Specific
nhs_config.local.json
patient_data/
test_data/

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db
EOF
```

---

## NHS Network Configuration

### Proxy Configuration

NHS networks typically use proxy servers. Configure your development environment:

#### For Python/Pip

```bash
# Set proxy environment variables
export HTTP_PROXY="http://proxy.ichnt.nhs.uk:8080"
export HTTPS_PROXY="http://proxy.ichnt.nhs.uk:8080"
export NO_PROXY="localhost,127.0.0.1,.ichnt.nhs.uk"

# For pip specifically
pip install --proxy http://proxy.ichnt.nhs.uk:8080 package-name
```

#### For Git

```bash
# Configure Git to use NHS proxy
git config --global http.proxy http://proxy.ichnt.nhs.uk:8080
git config --global https.proxy http://proxy.ichnt.nhs.uk:8080

# Bypass proxy for internal NHS domains
git config --global http.https://git.ichnt.nhs.uk.proxy ""
```

#### For npm/Node.js (if needed)

```bash
# Configure npm proxy
npm config set proxy http://proxy.ichnt.nhs.uk:8080
npm config set https-proxy http://proxy.ichnt.nhs.uk:8080
npm config set registry http://registry.npmjs.org/
```

### Firewall Rules

Common ports you may need access to:

| Port | Service | Request Access From |
|------|---------|-------------------|
| 22 | SSH | IT Service Desk |
| 80 | HTTP | Usually open |
| 443 | HTTPS | Usually open |
| 5000 | Flask Dev Server | Firewall team |
| 3306 | MySQL (if used) | Database team |
| 5432 | PostgreSQL (if used) | Database team |
| 6379 | Redis (if used) | Infrastructure team |

Contact IT Service Desk to request firewall rules if needed.

### SSL/TLS Certificates

NHS networks may require internal CA certificates:

```bash
# Download NHS internal CA certificate
# (Obtain from IT Service Desk)

# Install certificate (Ubuntu/Debian)
sudo cp ICHNT-Root-CA.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# For Python requests library
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# For Git
git config --global http.sslCAInfo /etc/ssl/certs/ca-certificates.crt
```

---

## Local Development on NHS Network

### Running the Application Locally

```bash
# Ensure VPN is connected
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run Flask backend
python chatbot_backend.py

# Application should start on http://localhost:5000
```

### Testing the Standalone HTML Version

```bash
# Option 1: Direct file open (simplest)
# Open chatbot.html in browser

# Option 2: Local web server (recommended for testing)
python -m http.server 8000

# Then visit: http://localhost:8000/chatbot.html
```

### Accessing from Other Devices on NHS Network

To test from other devices on the NHS network:

```bash
# Find your IP address
# Windows:
ipconfig

# macOS/Linux:
ifconfig  # or: ip addr show

# Run Flask with network access
python chatbot_backend.py --host 0.0.0.0 --port 5000

# Access from other device:
# http://your-ip-address:5000
```

**Security Note**: Only bind to 0.0.0.0 in development environments. Never in production.

### Development with NHS Smartcard Testing

If your application will integrate with NHS Smartcard authentication:

```bash
# Install smartcard libraries (Linux)
sudo apt-get install pcscd pcsc-tools libpcsclite-dev

# Install Python smartcard library
pip install pyscard

# Test smartcard reader
pcsc_scan
```

---

## Deployment to NHS Infrastructure

### Deployment Environments

Typical NHS deployment pipeline:

1. **Development** (DEV)
   - Your local machine or shared dev server
   - Frequent changes, testing new features
   - Access: All developers

2. **Testing** (TEST/UAT)
   - Shared testing environment
   - User acceptance testing
   - Access: Developers, testers, clinical staff

3. **Pre-Production** (PREPROD)
   - Production-like environment
   - Final validation before release
   - Access: Senior developers, release managers

4. **Production** (PROD)
   - Live environment serving end users
   - Strict change control
   - Access: Authorized personnel only

### Deployment to NHS Server

#### Prerequisites

1. Request server access from IT Service Desk
2. Obtain deployment credentials
3. Get firewall rules approved
4. Complete deployment checklist

#### Deployment Steps

```bash
# 1. SSH to NHS deployment server (via VPN)
ssh your.name@app-server.ichnt.nhs.uk

# 2. Navigate to application directory
cd /opt/clinical-supervision-chatbot

# 3. Pull latest code
git pull origin main

# 4. Activate virtual environment
source venv/bin/activate

# 5. Install/update dependencies
pip install -r requirements.txt

# 6. Run database migrations (if applicable)
# python manage.py db upgrade

# 7. Restart application service
sudo systemctl restart clinical-supervision-chatbot

# 8. Check status
sudo systemctl status clinical-supervision-chatbot

# 9. Verify logs
sudo tail -f /var/log/clinical-supervision/app.log
```

### Using Systemd Service

Create a systemd service file for the application:

```bash
# Create service file
sudo nano /etc/systemd/system/clinical-supervision-chatbot.service
```

```ini
[Unit]
Description=NWLVH Clinical Supervision Chatbot
After=network.target

[Service]
Type=simple
User=app-user
Group=app-user
WorkingDirectory=/opt/clinical-supervision-chatbot
Environment="PATH=/opt/clinical-supervision-chatbot/venv/bin"
Environment="FLASK_ENV=production"
ExecStart=/opt/clinical-supervision-chatbot/venv/bin/python chatbot_backend.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable clinical-supervision-chatbot
sudo systemctl start clinical-supervision-chatbot
```

### Nginx Configuration

Typical Nginx setup for the chatbot:

```nginx
# /etc/nginx/sites-available/clinical-supervision-chatbot

server {
    listen 80;
    server_name chatbot.ichnt.nhs.uk;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name chatbot.ichnt.nhs.uk;

    ssl_certificate /etc/ssl/certs/ichnt.nhs.uk.crt;
    ssl_certificate_key /etc/ssl/private/ichnt.nhs.uk.key;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000" always;

    # Logging
    access_log /var/log/nginx/chatbot-access.log;
    error_log /var/log/nginx/chatbot-error.log;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /opt/clinical-supervision-chatbot/static;
        expires 30d;
    }
}
```

---

## Testing and Quality Assurance

### Unit Testing

Create tests for the chatbot functionality:

```python
# tests/test_chatbot.py
import unittest
from chatbot_backend import app, get_response

class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_chat_endpoint(self):
        response = self.app.post('/chat', json={
            'message': 'What is clinical supervision?'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('response', data)

    def test_history_endpoint(self):
        response = self.app.get('/history')
        self.assertEqual(response.status_code, 200)

    def test_reset_endpoint(self):
        response = self.app.post('/reset')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

Run tests:

```bash
# Run all tests
python -m unittest discover tests

# Run with coverage
pip install coverage
coverage run -m unittest discover tests
coverage report
coverage html  # Generate HTML report
```

### Integration Testing on NHS Network

Test network connectivity and integration:

```python
# tests/test_nhs_network.py
import unittest
import os
import requests

class NHSNetworkTestCase(unittest.TestCase):

    def test_proxy_connectivity(self):
        """Test connection through NHS proxy"""
        proxies = {
            'http': os.getenv('HTTP_PROXY'),
            'https': os.getenv('HTTPS_PROXY')
        }
        try:
            response = requests.get('http://example.com', proxies=proxies, timeout=5)
            self.assertEqual(response.status_code, 200)
        except requests.exceptions.RequestException as e:
            self.fail(f"Proxy connection failed: {e}")

    def test_internal_dns_resolution(self):
        """Test NHS internal DNS resolution"""
        import socket
        try:
            socket.gethostbyname('internal-server.ichnt.nhs.uk')
        except socket.gaierror:
            self.fail("Cannot resolve NHS internal hostnames")
```

### Security Testing

```bash
# Install security testing tools
pip install bandit safety

# Run Bandit (Python security linter)
bandit -r . -f json -o security-report.json

# Check for known vulnerabilities in dependencies
safety check

# Run OWASP dependency check (if Java/Node dependencies exist)
```

### Load Testing

Test application performance:

```bash
# Install locust for load testing
pip install locust

# Create locustfile.py
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between

class ChatbotUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def chat_message(self):
        self.client.post("/chat", json={
            "message": "What is clinical supervision?"
        })

    @task
    def get_history(self):
        self.client.get("/history")
EOF

# Run load test
locust -f locustfile.py --host http://localhost:5000
```

---

## Security Best Practices

### Code Security

1. **Never Commit Sensitive Data**
   ```bash
   # Check for secrets before committing
   git diff --cached

   # Use git-secrets to prevent committing credentials
   pip install git-secrets
   git secrets --install
   git secrets --register-aws
   ```

2. **Input Validation**
   ```python
   # Always validate and sanitize user input
   from flask import request, escape

   @app.route('/chat', methods=['POST'])
   def chat():
       message = request.json.get('message', '')
       # Sanitize input
       message = escape(message)
       # Limit message length
       if len(message) > 1000:
           return jsonify({'error': 'Message too long'}), 400
   ```

3. **CORS Configuration**
   ```python
   # Restrict CORS to trusted domains only in production
   from flask_cors import CORS

   if app.config['ENV'] == 'production':
       CORS(app, resources={r"/*": {"origins": "https://chatbot.ichnt.nhs.uk"}})
   else:
       CORS(app)  # Allow all in development
   ```

4. **Rate Limiting**
   ```python
   from flask_limiter import Limiter
   from flask_limiter.util import get_remote_address

   limiter = Limiter(
       app,
       key_func=get_remote_address,
       default_limits=["200 per day", "50 per hour"]
   )

   @app.route('/chat', methods=['POST'])
   @limiter.limit("10 per minute")
   def chat():
       pass
   ```

### Data Protection

1. **No Patient Data in Code**
   - Never include patient identifiable information in code, logs, or tests
   - Use synthetic/anonymized data for testing only
   - Follow NHS Data Security standards

2. **Secure Logging**
   ```python
   import logging

   # Configure secure logging
   logging.basicConfig(
       filename='/var/log/clinical-supervision/app.log',
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )

   # Never log sensitive data
   logger.info(f"Chat request received")  # Good
   # logger.info(f"Message: {message}")  # Bad - might contain sensitive info
   ```

3. **Encryption**
   ```python
   # Use HTTPS only in production
   if app.config['ENV'] == 'production':
       @app.before_request
       def force_https():
           if not request.is_secure:
               return redirect(request.url.replace('http://', 'https://'))
   ```

### Access Control

```python
# Example: Simple authentication decorator
from functools import wraps
from flask import request, jsonify

def require_nhs_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not validate_nhs_token(auth_header):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin', methods=['GET'])
@require_nhs_auth
def admin_panel():
    pass
```

---

## Common Development Issues

### Issue 1: Cannot Access External Resources

**Problem**: Unable to install packages or access external APIs

**Solution**:
```bash
# Set proxy environment variables
export HTTP_PROXY="http://proxy.ichnt.nhs.uk:8080"
export HTTPS_PROXY="http://proxy.ichnt.nhs.uk:8080"
export NO_PROXY="localhost,127.0.0.1,.ichnt.nhs.uk"

# Retry operation
pip install --proxy http://proxy.ichnt.nhs.uk:8080 package-name
```

### Issue 2: SSL Certificate Verification Fails

**Problem**: `SSL: CERTIFICATE_VERIFY_FAILED` errors

**Solution**:
```bash
# Option 1: Install NHS CA certificate (recommended)
sudo cp ICHNT-Root-CA.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# Option 2: Disable verification (DEVELOPMENT ONLY)
export PYTHONHTTPSVERIFY=0
# or in code:
# requests.get(url, verify=False)
```

### Issue 3: Port Already in Use

**Problem**: `Address already in use` when starting Flask

**Solution**:
```bash
# Find process using port 5000
lsof -i :5000
# or
netstat -ano | findstr :5000

# Kill the process
kill -9 <PID>

# Or use a different port
python chatbot_backend.py --port 5001
```

### Issue 4: VPN Disconnects During Development

**Problem**: VPN connection drops, breaking development workflow

**Solution**:
```bash
# Enable automatic VPN reconnection in FortiClient

# Or use a script to monitor and reconnect
while true; do
    if ! ping -c 1 internal-server.ichnt.nhs.uk > /dev/null 2>&1; then
        echo "VPN down, reconnecting..."
        # Trigger VPN reconnect
        fortivpn-connect.sh
    fi
    sleep 60
done
```

### Issue 5: Permission Denied on NHS Servers

**Problem**: Cannot write to directories or restart services

**Solution**:
```bash
# Check current permissions
ls -la /opt/clinical-supervision-chatbot

# Request appropriate permissions from IT
# Or use sudo for authorized operations
sudo systemctl restart clinical-supervision-chatbot

# Add your user to app group
sudo usermod -a -G app-group your.name
```

---

## CI/CD on NHS Infrastructure

### GitLab CI/CD Pipeline (Example)

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  HTTP_PROXY: "http://proxy.ichnt.nhs.uk:8080"
  HTTPS_PROXY: "http://proxy.ichnt.nhs.uk:8080"

test:
  stage: test
  image: python:3.9
  before_script:
    - pip install -r requirements.txt
  script:
    - python -m unittest discover tests
    - bandit -r . -f json -o security-report.json
  artifacts:
    reports:
      junit: test-results.xml
    paths:
      - security-report.json

build:
  stage: build
  script:
    - echo "Building application..."
    # Add build steps if needed

deploy_dev:
  stage: deploy
  environment:
    name: development
  script:
    - ssh deploy@dev-server.ichnt.nhs.uk "cd /opt/chatbot && git pull && systemctl restart chatbot"
  only:
    - develop

deploy_prod:
  stage: deploy
  environment:
    name: production
  script:
    - ssh deploy@prod-server.ichnt.nhs.uk "cd /opt/chatbot && git pull && systemctl restart chatbot"
  only:
    - main
  when: manual
```

### Deployment Checklist

Before deploying to production:

- [ ] All tests passing
- [ ] Security scan completed (Bandit, Safety)
- [ ] Code review approved
- [ ] Documentation updated
- [ ] Change request approved (if required)
- [ ] Backup taken
- [ ] Rollback plan prepared
- [ ] Stakeholders notified
- [ ] Deployment window scheduled
- [ ] Post-deployment tests ready

---

## Getting Help

### Internal Support

1. **Development Team Lead**
   - Technical questions about the chatbot
   - Architecture decisions
   - Code review feedback

2. **IT Service Desk**
   - Network access issues
   - VPN problems
   - Server access requests
   - **Phone**: 020 3311 1234
   - **Email**: ithelpdesk@ic.nhs.uk

3. **Information Governance Team**
   - Data handling questions
   - Compliance requirements
   - **Email**: ig.support@ic.nhs.uk

4. **DevOps/Infrastructure Team**
   - Deployment pipeline issues
   - Server configuration
   - CI/CD problems

### External Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **Python Best Practices**: https://docs.python-guide.org/
- **NHS Digital Developer Hub**: https://digital.nhs.uk/developer
- **NHS Data Security Standards**: https://digital.nhs.uk/data-and-information/looking-after-information/data-security-and-information-governance

---

## Appendix: Development Tools

### Recommended IDE Setup

**VS Code with Extensions**:
- Python (Microsoft)
- Pylance
- Flask Snippets
- GitLens
- Better Comments
- Todo Tree

**PyCharm**:
- Professional edition recommended for Flask
- Configure remote interpreter for NHS servers
- Enable code inspections

### Useful Commands

```bash
# Quick development server restart
pkill -f chatbot_backend.py && python chatbot_backend.py &

# Watch logs in real-time
tail -f /var/log/clinical-supervision/app.log

# Quick git status
alias gs='git status'
alias gp='git pull'
alias gc='git commit -m'

# Virtual environment shortcuts
alias activate='source venv/bin/activate'
alias deactivate='deactivate'

# NHS VPN status check
alias vpncheck='ping -c 1 internal-server.ichnt.nhs.uk && echo "VPN: Connected" || echo "VPN: Disconnected"'
```

---

**Document Version**: 1.0
**Last Updated**: January 2026
**Maintained By**: Development Team, Imperial College Healthcare NHS Trust
**Next Review**: July 2026

For updates to this guide or to report issues, contact the development team lead or submit a merge request to the documentation repository.
