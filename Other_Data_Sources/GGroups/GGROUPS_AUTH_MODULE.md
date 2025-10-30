# GGroups Authentication Module

**File:** `ggroups_auth.py`  
**Purpose:** Reusable authentication module for Google Groups automation (DRY principle)

---

## Usage

```python
from ggroups_auth import authenticate_ggroups, verify_authentication

# Basic usage - context manager handles browser lifecycle
with authenticate_ggroups() as page:
    page.goto("https://groups.google.com/g/ecorestoration-alliance/members")
    
    # Verify authentication
    if verify_authentication(page, "EcoRestoration Alliance"):
        print("Authenticated successfully")
    
    # Your automation code here
    # ...

# Browser automatically closes when exiting context
```

---

## Features

**Authentication:**
- Loads cookies from `ggroups_cookies.json`
- Sanitizes cookies for Playwright compatibility
- Launches Microsoft Edge (following BROWSER_COOKIE_AUTH_PATTERN)
- Handles downloads automatically

**Context Manager:**
- Automatic browser setup and teardown
- No manual cleanup required
- Exception-safe (browser closes even on errors)

**Configuration:**
```python
with authenticate_ggroups(
    headless=False,           # Show browser window (default)
    downloads_path="./downloads"  # Optional download directory
) as page:
    # ...
```

---

## Functions

### `authenticate_ggroups(headless=False, downloads_path=None)`

Returns a context manager for authenticated Google Groups sessions.

**Parameters:**
- `headless` (bool): Run browser in headless mode (default: False)
- `downloads_path` (str/Path): Directory for downloads (default: None)

**Returns:** `GGroupsAuth` context manager

**Example:**
```python
with authenticate_ggroups(downloads_path="./data") as page:
    page.goto("https://groups.google.com/...")
```

### `verify_authentication(page, group_name="EcoRestoration Alliance", timeout=5000)`

Verify that the page is authenticated to Google Groups.

**Parameters:**
- `page`: Playwright page object
- `group_name` (str): Expected group name to verify
- `timeout` (int): Timeout in milliseconds

**Returns:** `bool` - True if authenticated, False otherwise

**Example:**
```python
if verify_authentication(page, "My Group Name"):
    print("Logged in successfully")
```

### `load_cookies()`

Load and sanitize cookies from `ggroups_cookies.json`.

**Returns:** `list` - Sanitized cookies ready for Playwright

**Raises:** `SystemExit` if cookie file not found

---

## Implementation Details

**Cookie Sanitization:**
- Fixes `sameSite` values (must be 'Strict', 'Lax', or 'None')
- Removes problematic `partitionKey` fields
- Ensures Playwright compatibility

**Browser Configuration:**
- Uses Microsoft Edge (`channel="msedge"`)
- Enables download handling
- Non-headless by default (visible for debugging)

**Error Handling:**
- Exits with helpful message if cookies not found
- Provides guidance on how to export cookies
- Screenshots saved on authentication failure

---

## Example Scripts

### Basic Download

```python
from ggroups_auth import authenticate_ggroups

with authenticate_ggroups() as page:
    page.goto("https://groups.google.com/g/my-group/members")
    
    # Find and click download button
    download_btn = page.locator('button[aria-label*="Download"]').first
    
    with page.expect_download() as download_info:
        download_btn.click()
    
    download = download_info.value
    download.save_as("members.csv")
```

### Network Monitoring

```python
from ggroups_auth import authenticate_ggroups

requests = []

def log_request(request):
    requests.append({
        'method': request.method,
        'url': request.url
    })

with authenticate_ggroups() as page:
    page.on('request', log_request)
    page.goto("https://groups.google.com/g/my-group/members")
    
    # Analyze requests
    print(f"Captured {len(requests)} requests")
```

---

## Testing

Run the module directly to test authentication:

```bash
python ggroups_auth.py
```

This will:
1. Load cookies
2. Launch Edge
3. Navigate to members page
4. Verify authentication
5. Take screenshot if failed
6. Close browser after 3 seconds

---

## Dependencies

```bash
pip install playwright
playwright install msedge
```

---

## Cookie Management

**Location:** `ggroups_cookies.json` (same directory as module)

**Format:** JSON array of cookie objects

**Expiration:** Google Groups cookies expire within minutes - export fresh cookies before each run

**Export Methods:**
1. **Preferred:** Browser cookie extension (e.g., "Cookie Editor")
2. **Alternative:** Edge DevTools → Application → Cookies → Copy

---

## Related Files

- `download_members.py` - Main script using this module
- `BROWSER_COOKIE_AUTH_PATTERN.md` - Authentication pattern documentation
- `COOKIE_EXPORT_METHODS.md` - Cookie export guide

---

## Benefits of This Module

**DRY (Don't Repeat Yourself):**
- Single source of truth for authentication
- Consistent cookie handling across scripts
- Easier to maintain and update

**Reliability:**
- Tested cookie sanitization
- Proper error handling
- Context manager ensures cleanup

**Flexibility:**
- Reusable for any Google Groups automation
- Configurable (headless, downloads)
- Easy to extend for new use cases

---

**Created:** October 29, 2025  
**Pattern:** Browser Cookie Authentication (see `/Other_Data_Sources/BROWSER_COOKIE_AUTH_PATTERN.md`)
