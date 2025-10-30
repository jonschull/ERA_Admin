# Other_Data_Sources/Zeffy/README.md

### 1. Overview

**Purpose:** Automate download of donor payment records from Zeffy donation platform

This component provides automated downloading of donation records using browser automation with OAuth authentication. It handles Zeffy's Google OAuth flow, organization profile switching, and exports payment data as Excel files.

**What this component does:**
- Downloads payment records via browser automation
- Handles Google OAuth authentication (bypasses bot detection)
- Switches between organization profiles automatically
- Exports donor data with contact info and payment details
- Successfully downloads complete payment history from EcoRestoration Alliance Inc

**Key insight:** Zeffy has no public API. OAuth-based authentication with stealth flags bypasses Google's bot detection and provides long-lasting cookies (weeks vs minutes). This makes automation reliable without constant re-authentication.

### 2. Orientation - Where to Find What

**You are at:** Other_Data_Sources/Zeffy component

**What you might need:**
- **Parent** → [../README.md](../README.md) - Other_Data_Sources overview
- **Root** → [../../README.md](../../README.md) - Overall ERA Admin architecture
- **Integration** → [../../integration_scripts/member_enrichment/](../../integration_scripts/member_enrichment/) - Member verification workflows
- **Reference pattern** → [../BROWSER_COOKIE_AUTH_PATTERN.md](../BROWSER_COOKIE_AUTH_PATTERN.md) - Cookie-based auth pattern
- **Database** → [../../FathomInventory/fathom_emails.db](../../FathomInventory/fathom_emails.db) - For cross-referencing donors with members

### 3. Principles

**System-wide:** See [../../WORKING_PRINCIPLES.md](../../WORKING_PRINCIPLES.md)

**Zeffy-specific:**

**1. OAuth with Stealth Flags**
- Use OAuth login script to capture cookies (bypasses Google bot detection)
- Stealth flags required to avoid "Google couldn't sign you in" errors
- Manual passkey/2FA completion during OAuth flow
- Cookies last weeks (much longer than Google Groups)

**2. Organization Profile Switching**
- Must switch from "EcoRestoration Alliance" to "EcoRestoration Alliance Inc"
- Script automates profile switching
- Verify correct organization before exporting data
- Payment data only available in specific organization profile

**3. Donor ≠ Member**
- Donation records indicate engagement, not membership status
- Cross-reference with Google Groups and Airtable for member verification
- Some donors are not members; some members are not donors
- Use as secondary verification source

**4. Testing and Validation**
- No automated tests (OAuth flow requires human interaction)
- Validation via successful Excel download and manual inspection
- Screenshots saved on errors for debugging
- Success confirmed by file size and column headers

### 4. Specialized Topics

---

## Quick Start

```bash
# 1. First time only: Login and save cookies
cd /Users/admin/ERA_Admin/Other_Data_Sources/Zeffy
python login_zeffy_oauth.py
# (Click "Log in with Google", select jschull@gmail.com, complete passkey auth)

# 2. Download payments (uses saved cookies)
python download_zeffy_payments.py
```

**Result:** `zeffy_payments_YYYYMMDD_HHMMSS.xlsx` with all payment records

---

## Files

**Active Scripts:**
- `download_zeffy_payments.py` - Main download script (automated)
- `login_zeffy_oauth.py` - OAuth login to capture fresh cookies
- `sanitize_cookies.py` - Cookie sanitization for Playwright
- `convert_edge_cookies.py` - Alternative: Convert Edge DevTools cookies
- `refresh_zeffy_auth.sh` - Alternative: Guided cookie refresh workflow

**Data:**
- `zeffy_cookies.json` - Browser cookies (refreshed via OAuth)
- `zeffy_payments_*.xlsx` - Downloaded payment data (gitignored)
- `zeffy_logged_in.png` - Screenshot from last OAuth login

**Archive:**
- `archive/` - Development/test scripts

---

## What This Does

The `download_zeffy_payments.py` script:

1. Loads cookies from `zeffy_cookies.json`
2. Launches Microsoft Edge (with stealth flags to avoid detection)
3. Navigates to Zeffy payments page
4. Switches organization profile to "EcoRestoration Alliance Inc"
5. Clicks Export button
6. Clicks Export in the dialog
7. Downloads payment data as Excel file
8. Saves as `zeffy_payments_YYYYMMDD_HHMMSS.xlsx`

**Typical runtime:** ~45 seconds

---

## Authentication Process

**PREFERRED METHOD: OAuth Login (Easiest & Most Reliable)**

Zeffy uses Google OAuth, so we automate the OAuth flow once to capture cookies:

```bash
python login_zeffy_oauth.py
```

This script:
- Launches Edge with stealth flags (avoids Google bot detection)
- Navigates to Zeffy login
- Clicks "Log in with Google"
- YOU manually select `jschull@gmail.com` and complete passkey auth
- Script captures all cookies automatically
- Sanitizes cookies for Playwright
- Saves to `zeffy_cookies.json`

**Why this works:**
- ✅ Bypasses Google's bot detection
- ✅ Handles passkey/2FA authentication
- ✅ Captures all necessary cookies automatically
- ✅ Cookies last for weeks (not minutes like Google Groups)

**Alternative: Manual Cookie Export**

If OAuth method fails, you can manually export cookies:
1. Use cookie-editor extension in Edge
2. Navigate to zeffy.com (logged in)
3. Export cookies as JSON
4. Paste into `zeffy_cookies.json`
5. Run `python sanitize_cookies.py`

---

## Expected Data

**Excel file columns:**
- Payment Date
- Total Amount
- Payment Method
- First Name, Last Name, Email
- Company Name
- Address, City, Postal Code, State, Country
- Recurring Status
- Eligible Amount (for tax receipts)

**Example data:**
- Monthly donations ($5-$50)
- One-time donations
- Donor contact information
- Campaign information

---

## Integration with Member Verification

**Next steps after download:**

1. **Cross-reference with Fathom DB:**
   - Compare donor emails with `fathom_emails.db`
   - Identify donors who are also members

2. **Cross-reference with Airtable:**
   - Compare with `people_export.csv`
   - Flag highly engaged supporters

3. **Member enrichment:**
   - Feed into `/integration_scripts/member_enrichment/`
   - Track financial support patterns

**Note:** **Donor ≠ Member** - Some donors may not be members, some members may not be donors.

---

## Troubleshooting

**"Cookies may have expired":**
- Run `python login_zeffy_oauth.py` to refresh cookies via OAuth
- This is the most reliable method

**"Google couldn't sign you in" during OAuth:**
- The script uses stealth flags to avoid detection
- If it still fails, try closing all Edge windows first
- Make sure you're using the correct Google account (jschull@gmail.com)

**"Export button not found":**
- Check screenshot: `zeffy_auth_test.png`
- Cookies may have expired → re-run OAuth login
- Verify you're on the correct organization (EcoRestoration Alliance Inc)

**"Profile switch failed":**
- The script automatically switches from "EcoRestoration Alliance" to "EcoRestoration Alliance Inc"
- If it fails, check if the organization names have changed
- Update the script's organization name check if needed

**Script hangs:**
- Zeffy pages load slowly (15-30 seconds is normal)
- Check the browser window for any unexpected dialogs
- Press Ctrl+C to cancel

---

## Reference Pattern

This implementation follows:
- `/Other_Data_Sources/BROWSER_COOKIE_AUTH_PATTERN.md` - Complete pattern guide
- OAuth automation with stealth flags (Google bot detection bypass)
- Playwright browser automation with Microsoft Edge

**Why this approach:**
- Zeffy has no public API
- OAuth provides reliable authentication
- Cookie-based automation avoids repeated logins
- Stealth flags bypass Google's bot detection

---

## Priority

**MEDIUM** - Donors are not necessarily members, but donation history indicates engagement level.

---

**Back to:** [Other_Data_Sources README](../README.md)
