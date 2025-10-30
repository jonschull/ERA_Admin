# Reference Models Index

**Last Updated:** October 28, 2025

This directory contains **read-only reference implementations** extracted from proven production systems. These are **models to copy and adapt**, not living code to modify.

---

## Available Reference Models

### 1. Browser Cookie Authentication Pattern

**File:** `BROWSER_COOKIE_AUTH_PATTERN.md`

**Source:** FathomInventory production system (October 2025)

**Purpose:** Complete reference implementation for authenticating with web services that lack API access using browser cookies and Playwright automation.

**What's Included:**
- Complete workflow documentation
- Step-by-step process (export → convert → sanitize → load)
- Troubleshooting guide
- Security considerations
- Hard-won lessons from production use

**Use Cases:**
- Google Groups data extraction
- Any web service without API access
- Services requiring complex auth (MFA, SSO)
- Maintaining session state across automation runs

**Status:** ✅ Proven in production, stable since October 2025

---

## Reference Scripts

All scripts are **read-only** (permissions: `r--r--r--`). To use:
1. **Copy** the script to your project
2. **Adapt** for your specific service
3. **Keep** the core logic intact

### REFERENCE_convert_edge_cookies.py

**Purpose:** Convert Edge DevTools cookie export to Playwright-compatible JSON

**Source:** `/FathomInventory/scripts/convert_edge_cookies.py`

**What it does:**
- Accepts tab-separated cookie data from Edge DevTools
- Parses cookie fields (name, value, domain, path, expires)
- Converts ISO timestamps to Unix epoch
- Outputs Playwright-compatible JSON format

**Usage:**
```bash
python convert_edge_cookies.py
# Paste cookies from Edge DevTools
# Press Enter twice to finish
```

**Adaptations needed:**
- Change output filename (currently `fathom_cookies.json`)
- Adjust default domain (currently `.fathom.video`)
- Customize success messages

---

### REFERENCE_sanitize_cookies.py

**Purpose:** Fix cookie format issues for Playwright compatibility

**Source:** `/FathomInventory/sanitize_cookies.py`

**What it does:**
- Fixes invalid `sameSite` values (must be Strict, Lax, or None)
- Removes malformed `partitionKey` fields
- Ensures Playwright can load cookies without errors

**Usage:**
```bash
python sanitize_cookies.py
```

**Adaptations needed:**
- Change input/output filename (currently `fathom_cookies_enable.json`)
- Add any service-specific sanitization rules

**Note:** Core sanitization logic rarely needs changes - it handles Playwright's requirements.

---

### REFERENCE_refresh_auth.sh

**Purpose:** Guided workflow for refreshing browser cookies

**Source:** `/FathomInventory/scripts/refresh_fathom_auth.sh`

**What it does:**
- Backs up existing cookies (timestamped)
- Guides user through cookie export process
- Runs cookie converter
- Tests authentication
- Confirms success or suggests rollback

**Usage:**
```bash
./refresh_auth.sh
```

**Adaptations needed:**
- Update service name and URLs (currently Fathom)
- Adjust paths to converter and test scripts
- Customize instructions for your service
- Update test validation logic

---

## How to Use These Models

### For Google Groups (Example)

1. **Copy the pattern:**
   ```bash
   cd /Users/admin/ERA_Admin/Other_Data_Sources/GGroups
   cp ../REFERENCE_convert_edge_cookies.py convert_ggroups_cookies.py
   cp ../REFERENCE_sanitize_cookies.py sanitize_ggroups_cookies.py
   cp ../REFERENCE_refresh_auth.sh refresh_ggroups_auth.sh
   ```

2. **Adapt for Google Groups:**
   - Change domain to `.google.com` or `.groups.google.com`
   - Update output filename to `ggroups_cookies.json`
   - Modify test validation (check for Groups UI elements)
   - Update instructions for Groups-specific navigation

3. **Create test script:**
   ```python
   # test_ggroups_cookies.py
   from playwright.sync_api import sync_playwright
   import json
   
   def test_ggroups_auth():
       with sync_playwright() as p:
           browser = p.chromium.launch(headless=True)
           context = browser.new_context()
           
           # Load cookies
           with open('ggroups_cookies.json', 'r') as f:
               cookies = json.load(f)
           context.add_cookies(cookies)
           
           # Test navigation
           page = context.new_page()
           page.goto('https://groups.google.com/my-groups')
           
           # Verify authentication
           if page.locator('text=My groups').is_visible(timeout=10000):
               print("✅ Google Groups authentication successful")
               return True
           else:
               print("❌ Authentication failed")
               return False
   ```

4. **Follow the workflow:**
   - Run `./refresh_ggroups_auth.sh` weekly
   - Monitor for authentication failures
   - Keep backups of working cookies

---

## File Permissions

All reference files are **read-only** to prevent accidental modification:

```bash
$ ls -la REFERENCE_*
-r--r--r--  REFERENCE_convert_edge_cookies.py
-r--r--r--  REFERENCE_sanitize_cookies.py
-r--r--r--  REFERENCE_refresh_auth.sh
-r--r--r--  BROWSER_COOKIE_AUTH_PATTERN.md
```

**To modify:** You must explicitly change permissions (which signals you're deviating from the proven model).

**Better approach:** Copy to your project and adapt the copy.

---

## Why Reference Models?

### The Problem
- Proven patterns get lost in project-specific implementations
- Hard-won solutions are buried in working code
- New projects reinvent the wheel
- Knowledge doesn't transfer between components

### The Solution
- Extract proven patterns as read-only references
- Document in centralized location
- Make them easy to find and copy
- Preserve battle-tested logic

### Benefits
1. **Faster development** - Start with working code
2. **Fewer bugs** - Use proven implementations
3. **Knowledge transfer** - Patterns documented and accessible
4. **Consistency** - Similar problems solved similarly
5. **Trust** - Reference models are stable and tested

---

## Adding New Reference Models

When you have a proven pattern worth preserving:

1. **Extract the pattern** - Pull out the core logic
2. **Document thoroughly** - Explain what, why, how
3. **Add verbatim scripts** - Include working implementations
4. **Make read-only** - `chmod 444 REFERENCE_*`
5. **Update this index** - Add to the catalog
6. **Link from README** - Make discoverable

**Criteria for reference models:**
- ✅ Proven in production (not experimental)
- ✅ Solves a general problem (not project-specific)
- ✅ Stable and tested (not changing frequently)
- ✅ Well-documented (can be understood standalone)
- ✅ Reusable (applicable to multiple projects)

---

## Related Documentation

**In this directory:**
- `README.md` - Other_Data_Sources overview
- `BROWSER_COOKIE_AUTH_PATTERN.md` - Complete auth pattern guide

**Source systems:**
- `/FathomInventory/docs/AUTHENTICATION_GUIDE.md` - Full Fathom auth system
- `/FathomInventory/authentication/cookie_export_guide.md` - Detailed export guide
- `/FathomInventory/README.md` - FathomInventory overview

**Integration points:**
- `/integration_scripts/member_enrichment/` - Uses these patterns
- `/Other_Data_Sources/GGroups/` - Will use for Google Groups

---

**Maintained by:** ERA_Admin project
**Review frequency:** Quarterly (or when source systems change significantly)
**Contact:** See project README for current maintainer
