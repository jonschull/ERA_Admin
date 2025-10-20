# Configuration Errors and Recovery

This document records critical configuration errors discovered during system operation and how to detect/fix them.

## Critical Error: Wrong Gmail Account (Discovered Oct 9, 2025)

### The Error

**System was downloading emails from the WRONG Gmail account.**

- **Configured:** Shares sent TO `fathomizer@ecorestorationalliance.org` ✅
- **Actual:** Emails downloaded FROM `jschull@gmail.com` ❌

### How It Happened

The `token.json` file was initially authenticated with `jschull@gmail.com` instead of `fathomizer@ecorestorationalliance.org`. The OAuth flow doesn't validate which account matches the intended configuration.

### Symptoms

All symptoms pointed to this root cause, though they appeared as separate issues:

1. **Wrong URL Format**
   - Expected: `/share/` URLs (public, no login required)
   - Got: `/calls/` URLs (require Fathom login)
   - Why: Personal email forwards contain call URLs, automated shares contain share URLs

2. **Date Format Mismatches**
   - Calls table: "Oct 7, 2025" (from webpage scrape)
   - Emails table: "October 07, 2025" (from email HTML)
   - Why: Different accounts receive different email formats

3. **Missing Recent Emails**
   - Oct 7-9 calls shared successfully
   - No corresponding emails in database
   - Why: Emails sent to fathomizer@, but system downloading from jschull@

4. **Data Corruption Indicators**
   - 1,469 emails missing metadata
   - Stale data alerts (showing Sept instead of Oct)
   - Public URL coverage only 0-14%

### How to Detect

**Quick Check:**
```bash
./venv/bin/python -c "
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('token.json')
service = build('gmail', 'v1', credentials=creds)
profile = service.users().getProfile(userId='me').execute()
print(f'Gmail account: {profile[\"emailAddress\"]}')
"
```

**Expected output:** `fathomizer@ecorestorationalliance.org`

**If wrong:** Follow recovery steps below

### Recovery Steps

1. **Backup current token:**
   ```bash
   cp token.json token.json.backup
   ```

2. **Force re-authentication:**
   ```bash
   rm token.json
   ```

3. **Re-authenticate with correct account:**
   ```bash
   ./venv/bin/python scripts/download_emails.py
   ```
   
   **CRITICAL:** When browser opens, authenticate with `fathomizer@ecorestorationalliance.org`, NOT your personal account

4. **Verify correct account:**
   ```bash
   ./venv/bin/python -c "
   from google.oauth2.credentials import Credentials
   from googleapiclient.discovery import build
   
   creds = Credentials.from_authorized_user_file('token.json')
   service = build('gmail', 'v1', credentials=creds)
   profile = service.users().getProfile(userId='me').execute()
   print(f'✅ Authenticated as: {profile[\"emailAddress\"]}')
   "
   ```

5. **Download new emails:**
   ```bash
   ./venv/bin/python scripts/download_emails.py
   ```

6. **Parse new emails:**
   ```bash
   ./venv/bin/python scripts/batch_database_converter.py
   ```

7. **Link public URLs:**
   ```bash
   ./venv/bin/python -c "
   import sqlite3
   from scripts.download_emails import link_public_urls
   conn = sqlite3.connect('fathom_emails.db')
   link_public_urls(conn)
   conn.close()
   "
   ```

### Prevention

**Add to weekly maintenance checklist:**

```bash
# Verify correct Gmail account
./venv/bin/python -c "
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('token.json')
service = build('gmail', 'v1', credentials=creds)
profile = service.users().getProfile(userId='me').execute()
expected = 'fathomizer@ecorestorationalliance.org'

if profile['emailAddress'] == expected:
    print(f'✅ Correct account: {expected}')
else:
    print(f'❌ WRONG ACCOUNT: {profile[\"emailAddress\"]}')
    print(f'   Expected: {expected}')
    print(f'   Run: rm token.json && python scripts/download_emails.py')
    exit(1)
"
```

**Add to daily health check script:**

This verification should be added to `scripts/check_auth_health.py` and included in daily automated reports.

### Configuration Files

**Critical files and their purposes:**

| File | Purpose | Correct Value |
|------|---------|---------------|
| `credentials.json` | Google API project config | Project: "fathomizer-email-analysis" |
| `token.json` | OAuth token for Gmail access | Account: fathomizer@ecorestorationalliance.org |
| `fathom_cookies_enable.json` | Fathom.video auth (e-NABLE) | Account: jschull@e-nable.org (default) |
| `fathom_cookies_era.json` | Fathom.video auth (ERA) | Account: ecorestorationalliance@gmail.com |
| `../era_config.py` | Active account configuration | `FATHOM_ACTIVE_ACCOUNT = 'enable'` (or 'era') |
| `run_daily_share.py` | Share destination (from config) | Reads from `era_config.py` |

**Note the distinction:**
- **Fathom account** (cookies): Configured in `../era_config.py`
  - Default: `jschull@e-nable.org` (e-NABLE account, for scraping calls)
  - Alternative: `ecorestorationalliance@gmail.com` (ERA account)
  - Switch: `FATHOM_ACCOUNT=era` env var or edit era_config.py
- **Gmail account** (token): `fathomizer@ecorestorationalliance.org` (for receiving shares)

### Related Issues

After fixing the account configuration, additional fixes were required:

1. **Date Normalization** - See section below
2. **URL Prioritization** - Parser must prefer `/share/` over `/calls/` URLs
3. **Report Display** - Must use actual share URLs, not call URLs

These are documented separately but all originated from downloading from the wrong email account.

---

## Date Normalization (To Be Implemented)

### The Problem

Dates are written in different formats at different entry points:

- **Calls table** (from web scrape): "Oct 7, 2025"
- **Emails table** (from email parse): "October 07, 2025"
- **Causes:** Linking failures, date comparison bugs

### Solution (Pending)

Normalize all dates to ISO format (YYYY-MM-DD) at write time:

1. In `run_daily_share.py`: Normalize scraped dates before writing to calls table
2. In `email_conversion/fathom_email_2_md.py`: Normalize parsed dates in stats
3. In `scripts/download_emails.py`: Verify normalization before DB write

**Target format:** `YYYY-MM-DD` for all date fields

---

## URL Prioritization (To Be Implemented)

### The Problem

Emails contain both `/calls/` and `/share/` URLs. Parser currently grabs the first "View Meeting" link, which may be either format.

### Solution (Pending)

Update `email_conversion/fathom_email_2_md.py` to:

1. Extract both URL types separately
2. Prioritize `/share/` URLs for `meeting_url` field
3. Store `/calls/` URL in separate field if needed
4. Add validation: warn if no `/share/` URL found

---

## Configuration Verification Script

**Create:** `scripts/verify_configuration.py`

Should check:
1. Gmail account = fathomizer@ecorestorationalliance.org
2. Fathom cookies account = jschull@e-nable.org
3. Share email in code = fathomizer@ecorestorationalliance.org
4. Recent emails have `/share/` URLs
5. Date formats are consistent
6. Database health metrics within acceptable range

**Add to:**
- Weekly maintenance checklist
- Daily automated health check
- Pre-deployment validation

