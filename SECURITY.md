# Security Policy

## 🔐 AI-Based Purchasing Tendency

The security and responsible handling of project data are important for this project.

This document explains how security issues and sensitive information should be handled.

---

## 🛡️ Supported Version

| Version        | Security Support |
| -------------- | ---------------- |
| 1.0.x          | ✅ Supported      |
| Older versions | ⚠️ Best effort   |

---

## 🚨 Reporting a Security Issue

If you discover a security vulnerability, please do not publicly disclose sensitive details through a GitHub issue.

Instead, contact the project maintainer privately through the contact information available on the author's GitHub or LinkedIn profile.

### Author

**Nikile Eines Dhoni J**

GitHub:

https://github.com/Dhonijd12345

LinkedIn:

https://www.linkedin.com/in/dhoni-j-7b73b92a2

---

## 🔑 Sensitive Information

Never commit the following information to the repository:

* API keys
* Passwords
* Authentication tokens
* Database credentials
* Private certificates
* Private customer information
* Personally identifiable information
* Confidential transaction data
* Private datasets

Use environment variables or secure secret-management systems when credentials are required.

---

## 📊 Customer and Transaction Data

If real-world purchasing data is used:

* Remove personally identifiable information.
* Anonymize sensitive fields.
* Use only data that you are authorized to process.
* Do not publish confidential business information.
* Avoid committing large private datasets to GitHub.

For public demonstrations, prefer:

* Public datasets
* Synthetic datasets
* Properly anonymized datasets

---

## 🤖 AI/ML Security

When developing or extending the models:

* Validate input data.
* Check for malformed datasets.
* Monitor unexpected model behavior.
* Avoid exposing private training data.
* Validate model outputs before using them for business decisions.
* Keep experimental model artifacts out of the repository when they contain sensitive information.

---

## 📦 Dependency Security

Keep project dependencies updated.

Review dependencies periodically for known security vulnerabilities.

Use:

```bash
pip list --outdated
```

and update dependencies carefully after testing compatibility.

---

## 📝 Responsible Disclosure

Security researchers are encouraged to report issues responsibly.

Please provide:

* Vulnerability description
* Reproduction steps
* Potential impact
* Suggested mitigation, if available

Thank you for helping keep the project secure.
