# Security Best Practices for Antigravity Workspace

## Overview

This document outlines security best practices for managing credentials, API keys, and sensitive data in the Antigravity Workspace.

## Credential Management

### API Keys

#### Google Gemini API Key

1. **Obtain your API key**:
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in with your Google account
   - Create a new API key or use an existing one

2. **Configure your environment**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your API key
   # Replace 'your_google_api_key_here' with your actual key
   GOOGLE_API_KEY=AIzaSy...
   ```

3. **Never commit `.env` to git**:
   - The `.env` file is already in `.gitignore`
   - Always use `.env.example` for templates
   - Never share your actual API keys in code or documentation

#### OpenAI API Key (Optional)

If using OpenAI-compatible endpoints:

1. **Obtain your API key**:
   - For OpenAI: Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - For local models (Ollama): No API key needed

2. **Configure in `.env`**:
   ```bash
   OPENAI_API_KEY=sk-...
   OPENAI_BASE_URL=https://api.openai.com/v1
   OPENAI_MODEL=gpt-4o-mini
   ```

### Environment Variables

All sensitive configuration should be stored in environment variables:

- ✅ **DO**: Use `.env` file for local development
- ✅ **DO**: Use environment variables in production
- ✅ **DO**: Use `.env.example` as a template
- ❌ **DON'T**: Commit `.env` to version control
- ❌ **DON'T**: Hard-code API keys in source code
- ❌ **DON'T**: Share API keys in chat, email, or documentation

## Security Checklist

### Before Committing Code

- [ ] No API keys in source code
- [ ] No passwords in source code
- [ ] `.env` file is in `.gitignore`
- [ ] Only `.env.example` is committed (with placeholders)
- [ ] No sensitive data in commit messages
- [ ] No secrets in configuration files

### Before Deploying

- [ ] Environment variables are set in deployment environment
- [ ] API keys are rotated if exposed
- [ ] Secrets are stored in secure secret management system
- [ ] Access logs are enabled
- [ ] Rate limiting is configured

### Regular Maintenance

- [ ] Rotate API keys periodically (every 90 days recommended)
- [ ] Review access logs for suspicious activity
- [ ] Update dependencies for security patches
- [ ] Audit `.gitignore` for completeness

## File Patterns to Ignore

The following patterns are automatically ignored by `.gitignore`:

```
.env                # Environment variables
*.key               # Private keys
*.pem               # Certificates
*.cert              # Certificates
*.p12               # PKCS12 keystores
secrets/            # Secrets directory
.secrets/           # Hidden secrets directory
credentials/        # Credentials directory
.credentials/       # Hidden credentials directory
```

## What to Do If You Expose a Secret

If you accidentally commit a secret to git:

1. **Immediately rotate the exposed credential**:
   - Generate a new API key
   - Revoke the old key
   - Update your `.env` file

2. **Remove from git history**:
   ```bash
   # Use git filter-branch or BFG Repo-Cleaner
   # WARNING: This rewrites history
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push (coordinate with team first!)
   git push origin --force --all
   ```

3. **Notify your team**:
   - Inform team members of the exposure
   - Ensure everyone updates their local repositories
   - Document the incident

## Additional Resources

- [Google AI Studio API Keys](https://aistudio.google.com/app/apikey)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [Git Secrets Tool](https://github.com/awslabs/git-secrets)

## Contact

For security concerns or to report vulnerabilities, please contact the project maintainers.
