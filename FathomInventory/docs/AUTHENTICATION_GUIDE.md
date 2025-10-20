# Fathom Inventory Authentication Guide

## Quick Authentication Setup

### New User Setup (5 minutes)
1. **Fathom cookies:** Run `./refresh_fathom_auth.sh` and follow prompts
2. **Gmail access:** Run `python download_emails.py` and complete OAuth in browser
3. **Test:** Run `python check_auth_health.py`

### Weekly Maintenance
```bash
./refresh_fathom_auth.sh
```

---

## Authentication System Overview

The FathomInventory system uses a three-tier authentication system:

1. **Google API Authentication** (`credentials.json` + `token.json`)
2. **Fathom.video Session Authentication** (`fathom_cookies.json`)  
3. **OAuth Token Management** (automatic refresh mechanisms)

## The Three Authentication Files

### 1. credentials.json - Google API Client Credentials

**Purpose**: Contains OAuth 2.0 client credentials for Google API access

**Structure**:
```json
{
  "installed": {
    "client_id": "57881875374-jtkkfj4s4cbo4dji31pun9td87gt0nba.apps.googleusercontent.com",
    "project_id": "fathomizer-email-analysis", 
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "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",
    "redirect_uris": ["http://localhost"]
  }
}
```

**How it got here**: 
- Created through Google Cloud Console
- Project: "fathomizer-email-analysis"
- Gmail API enabled with read-only scope
- Downloaded as client secrets file from Google Cloud Console

**Expiration**: Does not expire (client credentials are permanent)

**Usage**: Used by `download_emails.py` to initiate OAuth flow

### 2. token.json - OAuth Access Token

**Purpose**: Contains the actual OAuth token for Gmail API access

**Structure**:
```json
{
  "token": "ya29.a0AQQ_BDSAEq-_NAkFr0EMX12qrXfPLHMrAunETi...",
  "refresh_token": "1//05rjsJVJfTmNgCgYIARAAGAUSNgF-L9IrK0-u8mgm...",
  "token_uri": "https://oauth2.googleapis.com/token",
  "client_id": "57881875374-jtkkfj4s4cbo4dji31pun9td87gt0nba.apps.googleusercontent.com",
  "client_secret": "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",
  "scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
  "universe_domain": "googleapis.com",
  "account": "",
  "expiry": "2025-09-19T15:05:14.437249Z"
}
```

**How it got here**: 
- Generated automatically by first run of `download_emails.py`
- User completed OAuth flow in browser
- Google returned access token and refresh token
- System saved both tokens to this file

**Expiration**: 
- **Access token**: Expires every ~1 hour (see "expiry" field)
- **Refresh token**: Long-lived (months/years) but can be revoked
- **Auto-refresh**: System automatically refreshes access token using refresh token

**Usage**: Used by `download_emails.py` for all Gmail API calls

### 3. fathom_cookies.json - Browser Session Cookies

**Purpose**: Contains browser cookies for authenticated Fathom.video session

**Structure**: Array of cookie objects with domains, expiration dates, and values
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
]
```

**How it got here**:
- Manually extracted from browser after logging into Fathom.video
- Used browser developer tools or cookie export extension
- Represents authenticated session with Fathom.video
- **Hard-won solution**: Bypasses complex Fathom authentication

**Expiration**: 
- **Individual cookies expire** at different times (see expirationDate)
- **Session cookies**: Expire when browser closes
- **Persistent cookies**: Have specific expiration dates
- **Critical cookies expire daily** (Cloudflare, session tokens)
- **No auto-refresh**: Must be manually updated when expired

**Usage**: Used by `run_daily_share.py` to access Fathom.video as authenticated user

---

# Cookie Export Methods

## When You Need This

- Setting up authentication for the first time
- Cookies have expired (authentication fails)
- Moving to a new environment
- Fathom access is being denied

Four methods are presented below. If you are using Microsoft Edge, **Method 4 is recommended**.

## Method 1: Browser Developer Tools

### Chrome/Edge Steps:

1. **Log into Fathom.video** in your browser
2. **Navigate to** https://fathom.video/home
3. **Open Developer Tools** (F12 or right-click → Inspect)
4. **Go to Application tab** (or Storage in Firefox)
5. **Click on Cookies** in left sidebar
6. **Select https://fathom.video**
7. **Right-click in cookie list** → "Select All"
8. **Copy all cookies** (Ctrl+C)
9. **Manually format as JSON** (complex process)

### Firefox Steps:

1. **Log into Fathom.video** in your browser
2. **Open Developer Tools** (F12)
3. **Go to Storage tab**
4. **Click on Cookies** → https://fathom.video
5. **Right-click** → "Select All"
6. **Copy** and format as JSON

## Method 2: Browser Extension (Easier)

### Recommended Extensions:

- **"Cookie-Editor"** (Chrome/Firefox)
- **"EditThisCookie"** (Chrome)
- **"Export Cookies"** (Firefox)

### Using Cookie-Editor:

1. **Install Cookie-Editor** from browser store
2. **Log into Fathom.video**
3. **Click Cookie-Editor icon**
4. **Click "Export"** button
5. **Choose "JSON format"**
6. **Copy the exported JSON**
7. **Save as fathom_cookies.json**

## Method 3: Manual Export Script

Save this as `export_cookies.js` and run in browser console:

```javascript
// Run this in browser console on fathom.video
function exportCookies() {
    const cookies = document.cookie.split(';').map(cookie => {
        const [name, value] = cookie.trim().split('=');
        return {
            name: name,
            value: value,
            domain: '.fathom.video',
            path: '/',
            secure: true,
            httpOnly: false,
            sameSite: 'Lax'
        };
    });
  
    console.log('Copy this JSON:');
    console.log(JSON.stringify(cookies, null, 2));
  
    // Also copy to clipboard if possible
    navigator.clipboard.writeText(JSON.stringify(cookies, null, 2));
}

exportCookies();
```

## Method 4: Edge Cookie Converter Script (Recommended for Edge)

For Microsoft Edge users, there's an automated converter script:

### Using convert_edge_cookies.py:

1. **Log into Fathom.video** in Microsoft Edge
2. **Open Developer Tools** (F12) → Application tab → Cookies → https://fathom.video
3. **Select all cookies** (Ctrl+A) and **copy** (Ctrl+C)
4. **Run the converter**:
   ```bash
   python convert_edge_cookies.py
   ```
5. **Paste the copied cookie data** when prompted
6. **Press Enter twice** to finish
7. **Script automatically saves** as `fathom_cookies.json`

### Converter Features:

- ✅ Handles Edge's tab-separated cookie format
- ✅ Converts expiration dates to Unix timestamps
- ✅ Sets proper domain and security attributes
- ✅ Validates and formats JSON correctly

---

# Authentication Troubleshooting

## Google API Authentication Problems

### Symptom: "credentials.json not found"
**Cause**: Missing Google API credentials file
**Solution**: 
1. Go to Google Cloud Console
2. Create new project or select existing "fathomizer-email-analysis"
3. Enable Gmail API
4. Create OAuth 2.0 credentials for desktop application
5. Download client secrets and save as `credentials.json`

### Symptom: "token.json expired" or "refresh token invalid"
**Cause**: OAuth tokens have expired or been revoked
**Solution**:
1. Delete `token.json` file
2. Run `download_emails.py`
3. Complete OAuth flow in browser when prompted
4. New `token.json` will be generated

### Symptom: "insufficient permissions" or "scope errors"
**Cause**: Token was created with wrong scopes
**Solution**:
1. Delete `token.json`
2. Ensure SCOPES in code includes required permissions
3. Re-run OAuth flow

## Fathom Cookie Authentication Problems

### Symptom: "Access denied" or redirected to login page
**Cause**: Cookies have expired or are invalid
**Solution**:
1. Manually log into Fathom.video in browser
2. Export cookies using browser developer tools or extension
3. Replace `fathom_cookies.json` with fresh cookies
4. Test with `./refresh_fathom_auth.sh`

### Symptom: "sameSite" or cookie format errors
**Cause**: Cookie format incompatibility with Playwright
**Solution**: The code already handles this with sanitization:
```python
if cookie.get('sameSite') not in valid_same_site_values:
    cookie['sameSite'] = 'Lax'
```

## Cookie Expiration Analysis

**Critical Short-Term Cookies (expire frequently):**
- `__cf_bm` (Cloudflare bot management) - **expires daily**
- `_dd_s` (DataDog session) - **expires daily** 
- `DSID` (Google) - **7 days**
- `_fathom_session` - **Session cookie (most critical)**

**Long-term Cookies (90+ days):** These are stable and rarely cause issues

**Maintenance Frequency**: Weekly cookie refresh recommended due to daily-expiring cookies

---

# Testing Authentication

## Quick Health Check
```bash
python check_auth_health.py
```

## Individual Component Tests
```bash
cd authentication
python test_fathom_cookies.py  # Test Fathom access
python test_google_auth.py     # Test Gmail access  
python test_all_auth.py        # Comprehensive test
```

## Expected Test Output

### Successful Fathom Test:
```
✅ fathom_cookies.json found with 39 cookies
✅ All cookies are current
✅ Successfully authenticated with Fathom
🎉 Fathom cookie authentication is fully functional!
```

### Successful Google Test:
```
✅ Google API credentials found
✅ OAuth token valid
✅ Gmail API access confirmed
🎉 Google authentication is fully functional!
```

---

# Security and Maintenance

## Security Considerations

### File Permissions
```bash
chmod 600 credentials.json token.json fathom_cookies.json
```

### Backup Strategy
- **Keep secure backups** of working authentication files
- **Never commit to version control** (use .gitignore)
- **Rotate credentials** periodically for security

### Access Scope
- **Google API**: Limited to read-only Gmail access
- **Fathom**: Full user session access (powerful but necessary)

## Maintenance Schedule

### Weekly (Required)
```bash
./refresh_fathom_auth.sh
```

### Monthly (Recommended)
- **Check token expiry**: Monitor `token.json` "expiry" field
- **Test authentication**: Run comprehensive tests
- **Monitor cookie expiration**: Check for upcoming expiry dates

### Emergency Recovery
1. **Backup all auth files** before making changes
2. **Google API**: Delete token.json, re-run OAuth flow
3. **Fathom**: Export fresh cookies from working browser session
4. **Test incrementally**: Verify each component works before full automation

---

# Hard-Won Lessons

## From Current System:
1. **Cookie Sanitization**: Playwright requires specific cookie formats
2. **Auto-refresh Logic**: Prevents constant user intervention
3. **Error Handling**: Graceful degradation when auth fails
4. **Scope Management**: Minimal necessary permissions
5. **Session Persistence**: Cookies must be carefully maintained

## From Historical Evolution:
6. **Manual → Automated**: Early system required manual scrolling and HTML saving
7. **Watchdog Patterns**: Long-running processes need timeout monitoring and restart logic
8. **HTML Selector Stability**: Fathom UI selectors (`call-gallery-thumbnail`) have remained stable
9. **Process Reliability**: Browser automation can hang - robust monitoring is essential
10. **Data Format Consistency**: TSV format with standard columns enables reliable processing

## Key Timeouts Discovered Through Trial:
- **Fathom page load**: 60 seconds (can be slow)
- **"My Calls" selector**: 15 seconds for authentication verification
- **Process inactivity**: 5 minutes before restart (from watchdog experience)

## Authentication Evolution:
- **Phase 1**: Manual cookie export → manual scrolling → offline HTML parsing
- **Phase 2**: Automated scrolling → real-time parsing → watchdog monitoring
- **Phase 3**: Fully automated daily operation → smart error handling → integrated workflows

This authentication system represents significant engineering effort and iterative refinement to handle the complexities of modern web authentication across multiple platforms. The current system preserves battle-tested patterns while eliminating manual intervention points.
