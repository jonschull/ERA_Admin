# FathomInventory Authentication

---

## 1. Overview and Context Recovery

FathomInventory authentication subdirectory

**Purpose:** Cookie and token management for Fathom authentication

**Key Files:**
- `credentials.json` - Google API credentials (gitignored)
- `token.json` - OAuth access token (gitignored)
- `fathom_cookies_*.json` - Browser session cookies (gitignored)

**Current Status:** ✅ Authentication working (enable account)

---

## 2. Orientation

**Path:** [/README.md](../../README.md) → [FathomInventory](../README.md) → authentication → **This Guide**

**When to use:**
- Setting up new authentication
- Cookies expired (login required)
- Token refresh needed
- Switching Fathom accounts

**Scope:** This covers authentication setup. For component overview, see [../README.md](../README.md)

---

## 3. Principles

**System:** [/WORKING_PRINCIPLES.md](../../WORKING_PRINCIPLES.md)

**Component:** [../README.md](../README.md) - See FathomInventory principles

**Authentication-specific:**

1. **Security First**
   - Never commit credentials
   - All auth files in `.gitignore`
   - Use templates for examples
   - Backup tokens before changes
   - See [/WORKING_PRINCIPLES.md](../../WORKING_PRINCIPLES.md) for secret management

2. **Pre-flight Checks**
   - Test authentication before automation
   - Fail fast with clear messages
   - See [../README.md](../README.md) for component testing approach

3. **Account Management**
   - Multiple account support via cookie files
   - Switch accounts in era_config.py
   - See guides below for details

---

## 4. Specialized Topics

### Setup Guides

- cookie_export_guide.md - Export cookies from browser
- google_api_setup_guide.md - Set up Gmail API
- HISTORICAL_INSIGHTS_FROM_ARCHIVE.md - Lessons from past issues

### Related Component Docs

- ../docs/AUTHENTICATION_GUIDE.md - Detailed authentication guide
- ../scripts/check_auth_health.py - Health check script
- ../scripts/refresh_fathom_auth.sh - Auth refresh script

### Related Root Docs

**Principles:**
- [/WORKING_PRINCIPLES.md](../../WORKING_PRINCIPLES.md) - Security practices, testing

**Configuration:**
- /era_config.py - Active account selection

**Back to:** [FathomInventory README](../README.md) | [Main README](../../README.md)
