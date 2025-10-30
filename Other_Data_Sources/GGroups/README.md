# Other_Data_Sources/GGroups/README.md

### 1. Overview

**Purpose:** Download Google Groups membership lists for ERA member verification

This component provides automated downloading of Google Groups member lists using browser cookie-based authentication. It handles Google's authentication requirements and exports CSV files with member emails, names, roles, and join dates.

**What this component does:**
- Downloads Google Groups member lists via browser automation
- Handles cookie-based authentication (cookies expire within minutes)
- Exports member data as CSV files
- Provides primary source for member verification
- Successfully downloads 369 member records from ERA main groups

**Key insight:** Google Groups has no public API, requiring browser automation. Cookie-based authentication avoids repeated manual logins, but cookies expire quickly (within minutes) and must be refreshed before each run.

### 2. Orientation - Where to Find What

**You are at:** Other_Data_Sources/GGroups component

**What you might need:**
- **Parent** → [../README.md](../README.md) - Other_Data_Sources overview
- **Root** → [../../README.md](../../README.md) - Overall ERA Admin architecture
- **Integration** → [../../integration_scripts/member_enrichment/](../../integration_scripts/member_enrichment/) - Member verification workflows
- **Reference pattern** → [../BROWSER_COOKIE_AUTH_PATTERN.md](../BROWSER_COOKIE_AUTH_PATTERN.md) - Cookie-based auth pattern
- **Reference scripts** → [../REFERENCE_convert_edge_cookies.py](../REFERENCE_convert_edge_cookies.py) - Cookie conversion utility

### 3. Principles

**System-wide:** See [../../WORKING_PRINCIPLES.md](../../WORKING_PRINCIPLES.md)

**GGroups-specific:**

**1. Cookies Expire Quickly (Critical)**
- Google Groups cookies expire within **minutes** (not hours/days)
- **Always export fresh cookies immediately before each run**
- Authentication errors = expired cookies 99% of the time
- Use cookie export extension for fastest refresh

**2. Authentication Pattern**
- Follow BROWSER_COOKIE_AUTH_PATTERN.md (proven reference model)
- Use Microsoft Edge + Playwright (stable, well-tested)
- Visible browser (headless blocked by Google)
- Cookie sanitization required for Playwright compatibility

**3. Primary Data Source**
- Google Groups membership is authoritative for ERA membership
- Cross-reference with Airtable and Fathom DB
- Use for high-confidence member verification
- Priority source for member_enrichment workflows

**4. Testing and Validation**
- No automated tests (cookie expiry makes testing impractical)
- Validation via successful CSV download and manual inspection
- Screenshot saved on errors for debugging
- Success confirmed by member count and data preview

### 4. Specialized Topics

---

## Quick Start

```bash
# 1. Export fresh cookies (they expire quickly - within minutes)
#    Open Edge → groups.google.com → Use cookie extension → Export JSON
#    Paste into ggroups_cookies.json

# 2. Download members
cd /Users/admin/ERA_Admin/Other_Data_Sources/GGroups
python download_members.py
```

**Result:** `members_YYYYMMDD_HHMMSS.csv` with all group members

---

## Files

**Active Scripts:**
- `download_members.py` - Main download script (uses Playwright + Edge)
- `ggroups_auth.py` - Reusable authentication module (DRY)
- `convert_edge_cookies.py` - Convert Edge DevTools cookies to JSON (alternative method)
- `refresh_ggroups_auth.sh` - Guided cookie refresh workflow (alternative method)

**Data:**
- `ggroups_cookies.json` - Browser cookies (⚠️ expire quickly - refresh before each run)
- `members_*.csv` - Downloaded member lists (gitignored)
- `network_capture.json` - Network traffic capture (for debugging)

**Archive:**
- `archive/` - Experimental scripts (network monitoring, refactored versions)

---

## What This Does

Based on the screenshot you provided, the script will:

1. Load cookies from `ggroups_cookies.json`
2. Navigate to https://groups.google.com/g/ecorestorationalliance/members
3. Find the download button (shown in your screenshot)
4. Click it to download the CSV
5. Save as `members_YYYYMMDD_HHMMSS.csv`

The CSV will contain all 299 members with their emails and names.

---

## Authentication Process

**PREFERRED METHOD: Cookie Extension (Easiest)**

1. **Install a cookie export extension** (e.g., "Cookie Editor" or "EditThisCookie")
2. **Navigate to** https://groups.google.com in Edge
3. **Export cookies as JSON** using the extension
4. **Paste into** [`ggroups_cookies.json`](file:///Users/admin/ERA_Admin/Other_Data_Sources/GGroups/ggroups_cookies.json)
5. **Save and run:** `python download_members.py`

**Why this is preferred:**
- ✅ Already in JSON format (no conversion needed)
- ✅ One-click export from extension
- ✅ No manual copy/paste from DevTools
- ✅ Faster and less error-prone

**Alternative: Edge DevTools Method**

If you don't have a cookie extension:
```bash
./refresh_ggroups_auth.sh  # Guides through DevTools export
```

This converts tab-separated DevTools format to JSON.

---

## Usage

**Download members now:**
```bash
python download_members.py
```

**The script will:**
- Open browser (visible, so you can see progress)
- Load cookies for authentication
- Navigate to members page
- Click download button
- Save CSV automatically

**If authentication fails:**
- Cookies may have expired
- Run: `./refresh_ggroups_auth.sh`
- Re-export cookies from Edge

---

## Expected Output

**CSV columns:**
- Email
- Name  
- Role (member/manager/owner)
- Join date

**Example:**
```csv
Email,Name,Role,Joined
person@example.com,John Doe,Member,Oct 15 2024
...
```

---

## Integration with Member Verification

**Next steps after download:**

1. **Cross-reference with Fathom DB:**
   - Compare emails in CSV with `fathom_emails.db`
   - Identify members not in Fathom

2. **Cross-reference with Airtable:**
   - Compare with `people_export.csv`
   - Update `era_member` flags

3. **Member enrichment:**
   - Feed into `/integration_scripts/member_enrichment/`
   - Verify 230+ people with bios but not in Fathom

---

## Troubleshooting

**⚠️ IMPORTANT: Google Groups cookies expire within minutes**

If you see any authentication errors, **export fresh cookies first**.

**"Download button not found" or "Timeout waiting for download":**
- ✅ **Most common:** Cookies expired → Export fresh cookies from Edge
- Check GROUP_URL in script matches your group
- Verify you're logged into the correct Google account

**"Authentication failed":**
- Check screenshot saved (e.g., `auth_failed.png`, `timeout_error.png`)
- Export fresh cookies from groups.google.com in Edge
- Ensure cookie extension exports all cookies (not just current domain)

**Script hangs or times out:**
- Cookies likely expired during execution
- Browser may be showing login page
- Check the visible browser window
- Press Ctrl+C to cancel, export fresh cookies, retry

---

## Reference Pattern

This implementation follows:
- `/Other_Data_Sources/BROWSER_COOKIE_AUTH_PATTERN.md` - Complete pattern guide
- `/Other_Data_Sources/REFERENCE_convert_edge_cookies.py` - Cookie converter
- `/Other_Data_Sources/REFERENCE_sanitize_cookies.py` - Cookie sanitization

**Why this approach:**
- Google Groups has no public API
- Browser automation is the only option
- Cookie-based auth avoids repeated logins

---

**Back to:** [Other_Data_Sources README](../README.md)
