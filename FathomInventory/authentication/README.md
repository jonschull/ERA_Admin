# FathomInventory/authentication/README.md

### 1. Overview

**Purpose:** Cookie and token management for FathomInventory authentication

The FathomInventory system uses a sophisticated three-tier authentication system that represents hard-won solutions to complex authentication challenges across different platforms:

1. **Google API Authentication** (`credentials.json` + `token.json`)
2. **Fathom.video Session Authentication** (`fathom_cookies.json`)
3. **OAuth Token Management** (automatic refresh mechanisms)

**This document contains:**
- The three authentication files (purpose, structure, how they work)
- Authentication flow analysis (Google API, Fathom cookies)
- Troubleshooting guide (common problems & solutions)
- Maintenance schedule (regular checks, emergency recovery)
- Security considerations (permissions, backups, access scope)
- Hard-won lessons (from historical evolution)

**Key Insight:** This authentication system represents significant engineering effort and iterative refinement to handle the complexities of modern web authentication across multiple platforms.

### 2. Orientation - Where to Find What

**You are at:** FathomInventory authentication/ subdirectory

**Use this when:**
- Setting up authentication for first time
- Troubleshooting auth failures
- Understanding cookie/token management
- Planning maintenance schedule

**What you might need:**
- **Parent component** → [../README.md](../README.md) - FathomInventory overview
- **Component context** → [../CONTEXT_RECOVERY.md](../CONTEXT_RECOVERY.md) - Component state
- **System principles** → [/WORKING_PRINCIPLES.md](../../WORKING_PRINCIPLES.md) - Overall philosophy
- **Technical docs** → ../docs/AUTHENTICATION_GUIDE.md - Comprehensive auth setup

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../../WORKING_PRINCIPLES.md)

**Component-specific:** See [../README.md](../README.md) Section 3

**Authentication-specific principles:**

**1. Hard-Won Solutions**
- Cookie sanitization for Playwright compatibility
- Auto-refresh logic prevents constant user intervention
- Graceful degradation when auth fails
- Minimal necessary permissions (read-only Gmail)

**2. Weekly Maintenance Required**
- Fathom cookies expire frequently (some daily)
- System detects failures immediately (as of Oct 17)
- Refresh weekly with `./scripts/refresh_fathom_auth.sh`

**3. Security First**
- File permissions: `chmod 600` for all auth files
- Never commit to version control (use .gitignore)
- Keep secure backups of working auth files
- Rotate credentials periodically

**4. Battle-Tested Patterns**
- Timeouts discovered through trial (Fathom page load: 60s)
- HTML selector stability (call-gallery-thumbnail remains stable)
- Process reliability monitoring (watchdog patterns)
- Authentication evolution from manual → fully automated

### 4. Specialized Topics

#### The Three Authentication Files

**1. credentials.json - Google API Client Credentials**

*Purpose:* Contains OAuth 2.0 client credentials for Google API access

*Structure:*
```json
{
  "installed": {
    "client_id": "57881875374-jtkkfj4s4cbo4dji31pun9td87gt0nba.apps.googleusercontent.com",
    "project_id": "fathomizer-email-analysis", 
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "YOUR_CLIENT_SECRET_HERE",
    "redirect_uris": ["http://localhost"]
  }
}
```

*How it got here:*
- Created through Google Cloud Console
- Project: "fathomizer-email-analysis"
- Gmail API enabled with read-only scope
- Downloaded as client secrets file from Google Cloud Console

*Expiration:* Does not expire (client credentials are permanent)

*Usage:* Used by `download_emails.py` to initiate OAuth flow

**2. token.json - OAuth Access Token**

*Purpose:* Contains the actual OAuth token for Gmail API access

*Structure:*
```json
{
  "token": "YOUR_ACCESS_TOKEN_HERE",
  "refresh_token": "YOUR_REFRESH_TOKEN_HERE",
  "token_uri": "https://oauth2.googleapis.com/token",
  "client_id": "YOUR_CLIENT_ID_HERE",
  "client_secret": "YOUR_CLIENT_SECRET_HERE",
  "scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
  "universe_domain": "googleapis.com",
  "account": "",
  "expiry": "2025-09-19T15:05:14.437249Z"
}
```

*How it got here:*
- Generated automatically by first run of `download_emails.py`
- User completed OAuth flow in browser
- Google returned access token and refresh token
- System saved both tokens to this file

*Expiration:*
- **Access token:** Expires every ~1 hour (see "expiry" field)
- **Refresh token:** Long-lived (months/years) but can be revoked
- **Auto-refresh:** System automatically refreshes access token using refresh token

*Usage:* Used by `download_emails.py` for all Gmail API calls

**3. fathom_cookies.json - Browser Session Cookies**

*Purpose:* Contains browser cookies for authenticated Fathom.video session

*Structure:* Array of cookie objects with domains, expiration dates, and values
```json
[
  {
    "domain": ".fathom.video",
    "expirationDate": 1775094135,
    "hostOnly": false,
    "httpOnly": false,
    "name": "AMP_MKTG_12e56792f7",
    "path": "/",
    "sameSite": "lax",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "JTdCJTdE"
  }
  // ... many more cookies
]
```

*How it got here:*
- Manually extracted from browser after logging into Fathom.video
- Used browser developer tools or cookie export extension
- Represents authenticated session with Fathom.video
- **Hard-won solution:** Bypasses complex Fathom authentication

*Expiration:*
- **Individual cookies expire** at different times (see expirationDate)
- **Session cookies:** Expire when browser closes
- **Persistent cookies:** Have specific expiration dates
- **No auto-refresh:** Must be manually updated when expired

*Usage:* Used by `run_daily_share.py` to access Fathom.video as authenticated user

#### Authentication Flows

**Google API (download_emails.py):** Automatic OAuth with token refresh

**Fathom Cookies (run_daily_share.py):** Manual cookie management with sanitization

#### Troubleshooting

**Common Issues:**
- credentials.json not found → Set up in Google Cloud Console
- token.json expired → Delete and re-run OAuth flow
- Fathom access denied → Refresh cookies manually
- Cookie format errors → Code handles automatically

#### Testing Scripts

**test_all_auth.py** - Test all authentication
**test_fathom_cookies.py** - Test Fathom only
**test_google_auth.py** - Test Gmail only

**Usage:**
```bash
cd authentication
python test_all_auth.py        # Test everything
python test_fathom_cookies.py  # Fathom only
python test_google_auth.py     # Gmail only
```

#### Maintenance & Security

**Weekly Tasks:**
- Check cookie expiration
- Run test scripts
- Refresh if needed

**Security:**
```bash
chmod 600 credentials.json token.json fathom_cookies.json
```

**Emergency Recovery:**
1. Backup auth files
2. Google: Delete token.json, re-run OAuth
3. Fathom: Export fresh cookies from browser
4. Test incrementally

#### Hard-Won Lessons

**From Historical Evolution:**
- Cookie sanitization critical for Playwright
- Auto-refresh prevents user intervention
- Graceful error handling essential
- Session persistence requires careful maintenance
- Browser automation can hang - monitoring essential
- Fathom selectors have remained stable

**Key Timeouts (discovered through trial):**
- Fathom page load: 60 seconds
- Authentication verification: 15 seconds
- Process inactivity: 5 minutes

**Evolution:** Manual → Automated → Fully integrated (3 phases)

**Back to:** [FathomInventory/README.md](../README.md) | [/README.md](../../README.md)