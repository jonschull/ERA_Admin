# Browser Cookie Authentication Pattern

**STATUS: REFERENCE MODEL - DO NOT EDIT**

This document captures the proven pattern from FathomInventory for authenticating with web services that lack API access. Use this as a reference implementation for similar challenges (e.g., Google Groups).

---

## The Problem

Many web services (Fathom, Google Groups, etc.) don't provide APIs or have limited API access. To automate data extraction, we need to:
1. Authenticate as a logged-in user
2. Maintain session state across automated browser sessions
3. Handle cookie expiration gracefully

## The Solution: Cookie-Based Browser Automation

### Core Approach

1. **Manual Login** → Use real browser (Microsoft Edge recommended)
2. **Cookie Export** → Extract session cookies using browser DevTools
3. **Cookie Conversion** → Transform to Playwright-compatible JSON format
4. **Cookie Sanitization** → Fix compatibility issues (sameSite, partitionKey)
5. **Automated Replay** → Load cookies into Playwright browser for automation

### Why This Works

- **Bypasses complex auth flows** - No need to reverse-engineer login mechanisms
- **Maintains full session state** - All cookies preserved, not just auth tokens
- **Works with MFA/SSO** - Human handles complex auth, automation uses result
- **Stable over time** - Cookie format changes less than auth APIs

---

## Reference Implementation: Fathom

### File Structure

```
FathomInventory/
├── fathom_cookies.json          # Active cookies (gitignored)
├── scripts/
│   ├── convert_edge_cookies.py  # Edge DevTools → JSON converter
│   └── refresh_fathom_auth.sh   # Guided refresh workflow
├── sanitize_cookies.py          # Playwright compatibility fixes
└── authentication/
    └── test_fathom_cookies.py   # Validation script
```

### Workflow Scripts

See companion files in this directory:
- `REFERENCE_convert_edge_cookies.py` - Verbatim cookie converter
- `REFERENCE_sanitize_cookies.py` - Verbatim sanitization logic
- `REFERENCE_refresh_auth.sh` - Verbatim refresh workflow

**THESE ARE READ-ONLY REFERENCE MODELS** - Copy and adapt, don't modify originals.

---

## Step-by-Step Process

### 1. Initial Setup (One-Time)

**Browser Choice:** Microsoft Edge recommended
- Has best DevTools cookie export
- Tab-separated format is easiest to parse
- Consistent timestamp formatting

**Required Tools:**
```bash
pip install playwright
playwright install chromium  # Or your preferred browser
```

### 2. Cookie Export Process

**Manual Steps:**
1. Open Microsoft Edge
2. Navigate to target site (e.g., `https://fathom.video/home`)
3. Log in normally (handle MFA, SSO, etc.)
4. Open Developer Tools (F12)
5. Go to **Application** tab → **Cookies** → Select site
6. Select all cookies (Ctrl+A)
7. Copy (Ctrl+C)

**What You Get:**
```
Name	Value	Domain	Path	Expires	Size	HttpOnly	Secure	SameSite	Partition Key	Priority
session_token	abc123...	.fathom.video	/	2025-12-31T23:59:59.000Z	256	✓		Lax		Medium
user_id	xyz789...	.fathom.video	/	Session	64				
```

### 3. Cookie Conversion

**Use the converter script** (see `REFERENCE_convert_edge_cookies.py`):

```bash
python convert_edge_cookies.py
# Paste cookies when prompted
# Press Enter twice to finish
```

**What It Does:**
- Parses tab-separated format from Edge
- Converts ISO timestamps to Unix epoch
- Sets proper domain prefixes (`.domain.com`)
- Creates Playwright-compatible JSON structure
- Saves as `cookies.json`

**Output Format:**
```json
[
  {
    "name": "session_token",
    "value": "abc123...",
    "domain": ".fathom.video",
    "path": "/",
    "secure": true,
    "httpOnly": false,
    "sameSite": "Lax",
    "session": false,
    "expirationDate": 1735689599
  }
]
```

### 4. Cookie Sanitization

**Why Needed:** Playwright has strict cookie requirements that browser exports often violate.

**Common Issues:**
- Invalid `sameSite` values (must be: `Strict`, `Lax`, or `None`)
- Malformed `partitionKey` (Playwright doesn't support objects)
- Missing required fields

**Use sanitization** (see `REFERENCE_sanitize_cookies.py`):

```python
def sanitize_cookies(cookies):
    """Fix sameSite values for Playwright."""
    valid_same_site_values = {'Strict', 'Lax', 'None'}
    
    for cookie in cookies:
        # Fix sameSite values
        if cookie.get('sameSite') not in valid_same_site_values:
            cookie['sameSite'] = 'Lax'
        
        # Remove problematic partitionKey
        if 'partitionKey' in cookie and not isinstance(cookie.get('partitionKey'), str):
            del cookie['partitionKey']
    
    return cookies
```

### 5. Loading Cookies in Playwright

**In your automation script:**

```python
from playwright.sync_api import sync_playwright
import json

def load_cookies(context, cookie_file='cookies.json'):
    """Load cookies into browser context."""
    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
    
    # Sanitize before loading
    cookies = sanitize_cookies(cookies)
    
    # Add to browser context
    context.add_cookies(cookies)

# Usage
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    
    # Load cookies BEFORE navigating
    load_cookies(context)
    
    # Now navigate - you'll be authenticated
    page = context.new_page()
    page.goto('https://fathom.video/home')
    
    # Verify authentication
    if page.locator('text=My Calls').is_visible():
        print("✅ Authenticated successfully")
    else:
        print("❌ Authentication failed")
```

### 6. Maintenance & Refresh

**Cookie Expiration:**
- Some cookies expire **daily** (e.g., Cloudflare `__cf_bm`)
- Session cookies expire when browser closes
- Long-term cookies may last 90+ days

**Refresh Schedule:**
- **Weekly refresh recommended** for production systems
- Set calendar reminders
- Monitor for authentication failures

**Refresh Workflow** (see `REFERENCE_refresh_auth.sh`):
1. Backup existing cookies
2. Guide user through export process
3. Convert new cookies
4. Test authentication
5. Confirm success or rollback

---

## Testing & Validation

### Pre-Flight Check

**Before running automation:**

```python
def test_authentication(cookie_file='cookies.json'):
    """Test if cookies provide valid authentication."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        
        # Load cookies
        with open(cookie_file, 'r') as f:
            cookies = json.load(f)
        cookies = sanitize_cookies(cookies)
        context.add_cookies(cookies)
        
        # Test navigation
        page = context.new_page()
        page.goto('https://your-site.com')
        
        # Check for authenticated element
        if page.locator('text=Expected Element').is_visible(timeout=10000):
            print("✅ Authentication successful")
            return True
        else:
            print("❌ Authentication failed")
            return False
```

### Health Monitoring

**In production automation:**
- Check for redirect to login page
- Verify expected UI elements are present
- Log authentication failures
- Alert on repeated failures

---

## Security Considerations

### Cookie Storage

**Treat cookies like passwords:**
```bash
# Set restrictive permissions
chmod 600 cookies.json

# Add to .gitignore
echo "cookies.json" >> .gitignore
echo "*_cookies.json" >> .gitignore
```

**Never commit cookies to version control** - they provide full account access.

### Access Scope

**Cookies grant full user access:**
- Can perform any action the user can
- No scope limitations like API tokens
- Use dedicated service accounts when possible

### Rotation

**Regular rotation reduces risk:**
- Weekly refresh limits exposure window
- Invalidate old cookies after refresh
- Monitor for unauthorized access

---

## Troubleshooting

### "Authentication Failed" Errors

**Symptoms:**
- Redirected to login page
- "Access denied" messages
- Missing authenticated UI elements

**Solutions:**
1. **Refresh cookies** - Most common cause
2. **Check cookie expiration** - Inspect `expirationDate` fields
3. **Verify domain** - Must match site (`.domain.com` vs `domain.com`)
4. **Test in real browser** - Ensure manual login still works

### "Invalid Cookie Format" Errors

**Symptoms:**
- Playwright throws cookie validation errors
- `sameSite` or `partitionKey` errors

**Solutions:**
1. **Run sanitization** - Use `sanitize_cookies()` function
2. **Check JSON validity** - Use `jsonlint.com`
3. **Verify required fields** - name, value, domain, path

### "Session Expired" Errors

**Symptoms:**
- Works initially, then fails
- Cookies expire during long-running processes

**Solutions:**
1. **Refresh mid-run** - Re-export cookies during execution
2. **Shorten run duration** - Break into smaller batches
3. **Monitor expiration** - Check timestamps before critical operations

---

## Adapting for New Services

### Checklist for New Implementation

- [ ] Identify target service (e.g., Google Groups)
- [ ] Test manual login in Edge
- [ ] Export cookies using DevTools
- [ ] Copy `convert_edge_cookies.py` and adapt for service
- [ ] Copy `sanitize_cookies.py` (usually no changes needed)
- [ ] Create test script to verify authentication
- [ ] Document service-specific selectors/patterns
- [ ] Set up refresh workflow
- [ ] Schedule weekly maintenance

### Service-Specific Adaptations

**For each new service, document:**
1. **Login URL** - Where to authenticate
2. **Verification selector** - How to confirm auth success
3. **Cookie lifetime** - How often to refresh
4. **Special requirements** - MFA, SSO, etc.

---

## Hard-Won Lessons from Fathom

### What Worked

1. **Edge over Chrome** - Better cookie export format
2. **Automated converter** - Eliminates manual JSON formatting
3. **Sanitization layer** - Handles Playwright quirks
4. **Weekly refresh** - Prevents surprise failures
5. **Backup before refresh** - Easy rollback on failure
6. **Test after refresh** - Catch issues immediately

### What Didn't Work

1. **API attempts** - Fathom has no public API
2. **Selenium** - Playwright more reliable for modern sites
3. **Manual JSON editing** - Error-prone, slow
4. **Monthly refresh** - Too infrequent, cookies expired
5. **Assuming success** - Always test after changes

### Key Timeouts

- **Page load:** 60 seconds (sites can be slow)
- **Authentication check:** 15 seconds (wait for UI elements)
- **Cookie refresh:** Weekly (some expire daily)

---

## Related Documentation

**In FathomInventory:**
- `/FathomInventory/docs/AUTHENTICATION_GUIDE.md` - Full auth system
- `/FathomInventory/authentication/cookie_export_guide.md` - Detailed export instructions
- `/FathomInventory/README.md` - System overview

**Reference Scripts (this directory):**
- `REFERENCE_convert_edge_cookies.py` - Cookie converter
- `REFERENCE_sanitize_cookies.py` - Sanitization logic
- `REFERENCE_refresh_auth.sh` - Refresh workflow

---

**Last Updated:** October 28, 2025
**Source System:** FathomInventory (proven in production)
**Status:** Reference model - stable and tested
