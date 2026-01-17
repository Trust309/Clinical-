# NHS Network Access Guide

## Imperial College Healthcare NHS Trust Network Access

This guide provides comprehensive information for staff members at Imperial College Healthcare NHS Trust who need to access the NHS network for work purposes.

## Table of Contents

- [On-Site Network Access](#on-site-network-access)
- [Remote Access (VPN)](#remote-access-vpn)
- [Device Registration](#device-registration)
- [Credentials and Authentication](#credentials-and-authentication)
- [Common NHS Systems](#common-nhs-systems)
- [Security Requirements](#security-requirements)
- [Troubleshooting](#troubleshooting)
- [Support Contacts](#support-contacts)

---

## On-Site Network Access

### WiFi Networks

Imperial College Healthcare NHS Trust provides multiple WiFi networks:

1. **NHS-Staff WiFi**
   - Primary network for NHS staff
   - Requires NHS credentials
   - Provides access to internal systems and resources
   - Available across all trust sites

2. **NHS-Guest WiFi**
   - Limited access for visitors
   - No access to internal NHS systems
   - Internet access only

3. **Eduroam** (Selected sites)
   - For academic and research staff
   - Uses institutional credentials
   - Roaming access across educational institutions

### Connecting to NHS-Staff WiFi

1. Select **NHS-Staff** from available WiFi networks
2. Enter your credentials:
   - **Username**: `ICHNT\YourUsername` or `YourUsername@ic.nhs.uk`
   - **Password**: Your NHS network password
3. Accept any security certificates if prompted
4. You should now be connected to the NHS network

### Wired Network (Ethernet)

- Available at workstations and designated areas
- Automatically connects when you log in with NHS credentials
- More stable connection for bandwidth-intensive tasks
- Preferred for accessing electronic health records (EHR)

---

## Remote Access (VPN)

### VPN Overview

Virtual Private Network (VPN) access allows you to securely connect to the NHS network from outside the organization.

### Supported VPN Solutions

Imperial College Healthcare NHS Trust typically uses:

1. **FortiClient VPN**
   - Most common solution for remote access
   - Supports Windows, macOS, iOS, and Android
   - Download from NHS IT Service Desk portal

2. **NHS VPN Services**
   - Alternative access method
   - Web-based portal options available
   - Contact IT for specific setup instructions

### Setting Up VPN Access

#### Step 1: Request VPN Access

1. Contact your **IT Service Desk** or line manager
2. Complete VPN access request form
3. Provide business justification for remote access
4. Await approval (typically 2-5 working days)

#### Step 2: Install VPN Client

1. Download FortiClient VPN from:
   - Internal IT portal (when on-site)
   - Link provided by IT Service Desk
   - Official Fortinet website (verify version with IT)

2. Install the application on your device

#### Step 3: Configure VPN Connection

You'll receive configuration details from IT, typically including:

- **VPN Server Address**: `vpn.ichnt.nhs.uk` (example)
- **Port**: Usually 443 or 10443
- **Username**: Your NHS network username
- **Password**: Your NHS network password
- **Two-Factor Authentication**: May be required

#### Step 4: Connect to VPN

1. Open FortiClient VPN
2. Select your configured VPN connection
3. Enter your credentials
4. Complete MFA if prompted
5. Wait for connection confirmation
6. You should now have access to NHS resources

### VPN Best Practices

- Connect to VPN **only when needed**
- Disconnect when finished to free up licenses
- Use secure, private networks (avoid public WiFi)
- Keep VPN client updated
- Report connection issues immediately

---

## Device Registration

### Personal Device Registration (BYOD)

If using personal devices for NHS work:

1. **Security Assessment**
   - Device must meet minimum security standards
   - Antivirus software required
   - Disk encryption mandatory
   - Operating system must be up-to-date

2. **Registration Process**
   - Submit device details to IT Service Desk
   - Complete BYOD agreement form
   - Install required security software
   - Configure mobile device management (MDM) if required

3. **Compliance**
   - Regular security scans
   - Automatic updates enabled
   - No jailbroken/rooted devices permitted

### NHS-Issued Devices

Trust-issued devices come pre-configured with:
- Network access credentials
- VPN client
- Security software
- Required applications
- Encryption

---

## Credentials and Authentication

### NHS Network Credentials

Your NHS credentials typically consist of:

- **Username**:
  - Format: `ICHNT\firstname.lastname` or `firstname.lastname@ic.nhs.uk`
  - Case-sensitive in some systems

- **Password Requirements**:
  - Minimum 12 characters
  - Mix of uppercase, lowercase, numbers, and symbols
  - Changed every 90 days
  - Cannot reuse last 12 passwords

### Multi-Factor Authentication (MFA)

MFA is increasingly required for NHS access:

1. **SMS-Based**
   - One-time code sent to registered mobile
   - Enter code when prompted

2. **Authenticator Apps**
   - Microsoft Authenticator (recommended)
   - Google Authenticator
   - Setup via IT Service Desk

3. **Hardware Tokens**
   - Physical devices generating codes
   - Issued for high-security access

### NHS Smartcard

For clinical systems access:

- **Purpose**: Authentication for patient record systems
- **Registration**: Via Registration Authority (RA) at your site
- **Usage**: Insert card and enter passcode
- **Security**: Never share your card or passcode
- **Lost/Stolen**: Report immediately to RA and IT

---

## Common NHS Systems

### Systems Accessible via NHS Network

1. **Electronic Health Records (EHR)**
   - Cerner Millennium / EPR
   - Requires NHS Smartcard
   - On-site or VPN access

2. **NHSmail**
   - Email: `firstname.lastname@nhs.net`
   - Web access: https://www.nhs.net/
   - Outlook client configuration available

3. **ESR (Electronic Staff Record)**
   - HR and payroll system
   - Training records
   - E-learning platform

4. **Clinical Systems**
   - PACS (imaging)
   - Pathology results
   - Prescribing systems
   - Varies by department

5. **Office 365 / Microsoft Teams**
   - Email, calendar, collaboration
   - NHS tenant specific
   - SSO with NHS credentials

---

## Security Requirements

### Mandatory Security Measures

1. **Device Security**
   - Full disk encryption (BitLocker/FileVault)
   - Password-protected lock screen
   - Automatic screen lock after 5 minutes
   - Antivirus software with real-time protection

2. **Network Security**
   - No unauthorized software installation
   - No file sharing services (Dropbox, etc.) without approval
   - No connection to untrusted networks while accessing NHS data
   - VPN required for all remote access

3. **Data Protection**
   - No patient data on personal devices without approval
   - Encrypted USB drives only (if permitted)
   - Secure disposal of printed materials
   - Follow GDPR and NHS data policies

### Information Governance Training

- Mandatory annual training
- Complete via ESR
- Required for network access
- Covers:
  - Data protection
  - Confidentiality
  - Information security
  - Incident reporting

---

## Troubleshooting

### Common Connection Issues

#### Cannot Connect to NHS-Staff WiFi

**Symptoms**: Authentication fails, unable to connect

**Solutions**:
1. Verify username format: `ICHNT\username`
2. Check CAPS LOCK is off
3. Reset password via self-service portal
4. Forget network and reconnect
5. Check device is registered
6. Contact IT Service Desk

#### VPN Connection Fails

**Symptoms**: "Connection timeout" or "Authentication failed"

**Solutions**:
1. Check internet connection
2. Verify VPN server address
3. Ensure VPN client is up-to-date
4. Try different network (mobile hotspot)
5. Check if MFA code is current
6. Restart VPN client
7. Contact IT Service Desk if persistent

#### Slow Network Performance

**Symptoms**: Pages load slowly, timeouts

**Solutions**:
1. Check local internet speed
2. Disconnect from VPN if not needed
3. Close unnecessary applications
4. Clear browser cache
5. Use wired connection if possible
6. Report persistent issues to IT

#### Access Denied to Specific Systems

**Symptoms**: "Access denied" or "Insufficient permissions"

**Solutions**:
1. Verify you have authorization for the system
2. Check NHS Smartcard is inserted (if required)
3. Request access via line manager
4. Ensure training/competencies completed
5. Contact system administrator

---

## Support Contacts

### IT Service Desk

**Primary Contact for All Technical Issues**

- **Phone**: 020 3311 1234 (example - verify with your site)
- **Email**: ithelpdesk@ic.nhs.uk
- **Portal**: https://itsupport.ichnt.nhs.uk
- **Hours**: 24/7 for critical issues, 8am-6pm for general support

### What to Provide When Contacting Support

1. Your full name and staff ID
2. Department and location
3. Contact number
4. Detailed description of issue
5. Error messages (screenshot if possible)
6. Steps already taken to resolve
7. Urgency level

### Registration Authority (for Smartcard Issues)

- Located at each main site
- Book appointments via IT Service Desk
- Bring photo ID
- Required for new cards, renewals, passcode resets

### Information Governance Team

- **Email**: ig.support@ic.nhs.uk
- **Phone**: Extension 12345
- For questions about:
  - Data access permissions
  - GDPR compliance
  - Information security policies
  - Data breach reporting

### Local IT Support

Many departments have dedicated IT support staff:
- Check with your department administrator
- Often faster for simple issues
- Can escalate to central IT if needed

---

## Additional Resources

### Self-Service Tools

- **Password Reset**: https://passwordreset.ic.nhs.uk
- **VPN Portal**: https://vpn.ichnt.nhs.uk
- **IT Knowledge Base**: https://kb.ichnt.nhs.uk
- **Software Downloads**: https://software.ichnt.nhs.uk (on-site only)

### Training Resources

- **ESR**: https://www.esr.nhs.uk
- **Data Security Awareness**: Mandatory annual training
- **System-Specific Training**: Via ESR or department leads

### Policies and Guidelines

- NHS Information Governance Policy
- Acceptable Use Policy
- Remote Working Policy
- BYOD Policy
- Data Protection Impact Assessments

---

## Important Notes

- **Patient Data**: Never access or store patient-identifiable data on unauthorized devices
- **Password Sharing**: Never share your credentials with anyone
- **Suspicious Activity**: Report immediately to IT Security
- **Lost Devices**: Report immediately if device with NHS access is lost/stolen
- **Off-Site Access**: Only use VPN on trusted, secure networks
- **Compliance**: Failure to follow policies may result in access revocation

---

## Quick Reference Card

| Task | Action |
|------|--------|
| Connect to WiFi | Network: NHS-Staff, Credentials: ICHNT\username |
| Reset Password | https://passwordreset.ic.nhs.uk |
| VPN Issues | Restart client, verify credentials, call IT |
| Smartcard Problems | Contact Registration Authority |
| New System Access | Request via line manager |
| IT Support | 020 3311 1234 / ithelpdesk@ic.nhs.uk |
| Report Security Incident | IT Security Team immediately |

---

**Last Updated**: January 2026
**Document Owner**: IT Services, Imperial College Healthcare NHS Trust
**Review Date**: July 2026

For the most current information, always check the internal IT portal or contact the IT Service Desk.
