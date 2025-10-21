# Authentication System Documentation

## Overview

The FathomInventory system uses a sophisticated three-tier authentication system that represents hard-won solutions to complex authentication challenges across different platforms:

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
    "client_secret": "YOUR_CLIENT_SECRET_HERE",
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
  },
  // ... many more cookies
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
- **No auto-refresh**: Must be manually updated when expired

**Usage**: Used by `run_daily_share.py` to access Fathom.video as authenticated user

## Authentication Flow Analysis

### Google API Flow (download_emails.py)

```python
def get_gmail_service():
    creds = None
    
    # 1. Try to load existing token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # 2. Check if token is valid/expired
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # 3a. Auto-refresh expired token
            creds.refresh(Request())
        else:
            # 3b. Full OAuth flow (requires user interaction)
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 4. Save refreshed/new token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    # 5. Create authenticated service
    return build('gmail', 'v1', credentials=creds)
```

### Fathom Cookie Flow (run_daily_share.py)

```python
# 1. Load cookies from file
with open(COOKIES_FILE, 'r') as f:
    cookies = json.load(f)

# 2. Sanitize cookies for Playwright compatibility
valid_same_site_values = {'Strict', 'Lax', 'None'}
for cookie in cookies:
    if cookie.get('sameSite') not in valid_same_site_values:
        cookie['sameSite'] = 'Lax'
    if 'partitionKey' in cookie and not isinstance(cookie.get('partitionKey'), str):
        del cookie['partitionKey']

# 3. Add cookies to browser context
await context.add_cookies(cookies)

# 4. Navigate to Fathom with authenticated session
await page.goto("https://fathom.video/home")
```

## Troubleshooting Authentication Issues

### Google API Authentication Problems

#### Symptom: "credentials.json not found"
**Cause**: Missing Google API credentials file
**Solution**: 
1. Go to Google Cloud Console
2. Create new project or select existing "fathomizer-email-analysis"
3. Enable Gmail API
4. Create OAuth 2.0 credentials for desktop application
5. Download client secrets and save as `credentials.json`

#### Symptom: "token.json expired" or "refresh token invalid"
**Cause**: OAuth tokens have expired or been revoked
**Solution**:
1. Delete `token.json` file
2. Run `download_emails.py`
3. Complete OAuth flow in browser when prompted
4. New `token.json` will be generated

#### Symptom: "insufficient permissions" or "scope errors"
**Cause**: Token was created with wrong scopes
**Solution**:
1. Delete `token.json`
2. Ensure SCOPES in code includes required permissions
3. Re-run OAuth flow

### Fathom Cookie Authentication Problems

#### Symptom: "Access denied" or redirected to login page
**Cause**: Cookies have expired or are invalid
**Solution**:
1. Manually log into Fathom.video in browser
2. Export cookies using browser developer tools or extension
3. Replace `fathom_cookies.json` with fresh cookies
4. Test with `run_daily_share.py`

#### Symptom: "sameSite" or cookie format errors
**Cause**: Cookie format incompatibility with Playwright
**Solution**: The code already handles this with sanitization:
```python
if cookie.get('sameSite') not in valid_same_site_values:
    cookie['sameSite'] = 'Lax'
```

## Maintenance Schedule

### Regular Maintenance (Monthly)
- **Check token expiry**: Monitor `token.json` "expiry" field
- **Test authentication**: Run scripts to verify access
- **Monitor cookie expiration**: Check Fathom cookies for upcoming expiry

### When Things Break
- **Google API issues**: Usually auto-resolve with token refresh
- **Fathom access issues**: Requires manual cookie refresh
- **Permission changes**: May require new OAuth consent

### Emergency Recovery
1. **Backup all auth files** before making changes
2. **Google API**: Delete token.json, re-run OAuth flow
3. **Fathom**: Export fresh cookies from working browser session
4. **Test incrementally**: Verify each component works before full automation

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

## Hard-Won Lessons

### From Current System:
1. **Cookie Sanitization**: Playwright requires specific cookie formats
2. **Auto-refresh Logic**: Prevents constant user intervention
3. **Error Handling**: Graceful degradation when auth fails
4. **Scope Management**: Minimal necessary permissions
5. **Session Persistence**: Cookies must be carefully maintained

### From Historical Evolution (see HISTORICAL_INSIGHTS_FROM_ARCHIVE.md):
6. **Manual → Automated**: Early system required manual scrolling and HTML saving
7. **Watchdog Patterns**: Long-running processes need timeout monitoring and restart logic
8. **HTML Selector Stability**: Fathom UI selectors (`call-gallery-thumbnail`) have remained stable
9. **Process Reliability**: Browser automation can hang - robust monitoring is essential
10. **Data Format Consistency**: TSV format with standard columns enables reliable processing

### Key Timeouts Discovered Through Trial:
- **Fathom page load**: 60 seconds (can be slow)
- **"My Calls" selector**: 15 seconds for authentication verification
- **Process inactivity**: 5 minutes before restart (from watchdog experience)

### Authentication Evolution:
- **Phase 1**: Manual cookie export → manual scrolling → offline HTML parsing
- **Phase 2**: Automated scrolling → real-time parsing → watchdog monitoring
- **Phase 3**: Fully automated daily operation → smart error handling → integrated workflows

This authentication system represents significant engineering effort and iterative refinement to handle the complexities of modern web authentication across multiple platforms. The current system preserves battle-tested patterns while eliminating manual intervention points.
