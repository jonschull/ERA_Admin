# Authentication Modernization Plan

**Created:** October 28, 2025  
**Purpose:** Guide future AI to modernize FathomInventory authentication without breaking the current system

---

## Executive Summary

**IMPORTANT:** This is a **FUTURE MODERNIZATION PLAN**, not the current system.

The current FathomInventory system uses **browser cookie authentication** for Fathom access, which requires **weekly manual refresh**. This folder documents a path to modernize to **API-based authentication** that is more robust and requires no maintenance.

**Key Discovery:** Fathom now has an API (as of 2025) that is already being used successfully in the **integration_scripts component** (NOT in FathomInventory yet). This folder shows how to adopt it.

---

## Current State (October 2025)

### What Works Now

**Fathom Authentication (Browser Cookies):**
- Location: `/FathomInventory/fathom_cookies_enable.json`
- Method: Manual export from Microsoft Edge DevTools
- Maintenance: Weekly refresh required (some cookies expire daily)
- Process: Documented in `/Other_Data_Sources/BROWSER_COOKIE_AUTH_PATTERN.md`
- Scripts: `run_daily_share.py` uses Playwright with cookies

**Gmail Authentication (OAuth):**
- Location: `/FathomInventory/token.json` + `credentials.json`
- Method: Google OAuth 2.0
- Maintenance: Auto-refresh (set once, works indefinitely)
- Account: `fathomizer@ecorestorationalliance.org`
- Scripts: `scripts/download_emails.py` uses Gmail API

### The Problem

**Fathom cookies are fragile:**
- Expire daily/weekly
- Require manual browser export
- Break without warning
- No automation possible

**Gmail OAuth is robust:**
- Auto-refreshes access tokens
- Set once, works forever
- No manual maintenance
- API-based (reliable)

---

## The Modernization Opportunity

**CRITICAL:** The Fathom API is **NOT currently used in FathomInventory**. It is used in integration_scripts and represents a future improvement path.

### Fathom API Discovery

**Location:** `/integration_scripts/participant_reconciliation/api_enrich_remaining.py` (NOT in FathomInventory)

**What it does:**
```python
# Uses Fathom API with API key
API_KEY = os.environ.get('FATHOM_API_KEY')
API_BASE = 'https://api.fathom.ai/external/v1'

# Query meetings
response = requests.get(f'{API_BASE}/meetings', headers={'X-Api-Key': API_KEY})

# Get participant emails from calendar_invitees
invitees = meeting.get('calendar_invitees', [])
for invitee in invitees:
    email = invitee.get('email')
    name = invitee.get('name')
```

**Benefits over cookies:**
- ✅ No expiration (API key is long-lived)
- ✅ No browser automation needed
- ✅ Direct API access (faster, more reliable)
- ✅ Get participant emails directly (no scraping)
- ✅ No weekly maintenance

### Better Gmail OAuth Pattern

**Location:** `/integration_scripts/participant_reconciliation/archive/experimental/setup_gmail_auth.py`

**What it does better:**
- Explicit account selection guidance
- Separate token files per account (`token_jschull.json` vs `token_fathomizer.json`)
- Verification step after authentication
- Clear error messages

---

## Reference Files in This Folder

### REFERENCE_fathom_api_usage.py

**Source:** `/integration_scripts/participant_reconciliation/api_enrich_remaining.py`  
**Copied:** October 28, 2025  
**Status:** Working production code

**What to learn from it:**
- How to authenticate with Fathom API (API key in env var)
- How to query meetings by date range
- How to extract participant emails from `calendar_invitees`
- How to handle pagination with cursors
- Error handling patterns

**Note:** Original may change, this is a canonical reference copy.

### REFERENCE_gmail_oauth_setup.py

**Source:** `/integration_scripts/participant_reconciliation/archive/experimental/setup_gmail_auth.py`  
**Copied:** October 28, 2025  
**Status:** Working production code

**What to learn from it:**
- How to set up Gmail OAuth with explicit account selection
- How to use separate token files for different accounts
- How to verify authentication after setup
- How to handle token refresh
- Clear user guidance patterns

**Note:** Original may change, this is a canonical reference copy.

---

## Modernization Strategy

### Phase 1: Parallel Implementation (DO NOT BREAK CURRENT SYSTEM)

**Goal:** Create new API-based system alongside existing cookie-based system

**Steps:**
1. **Get Fathom API key**
   - Go to https://fathom.video/customize
   - Generate API key
   - Store as environment variable: `export FATHOM_API_KEY="..."`

2. **Create new script: `run_daily_share_api.py`**
   - Copy from `REFERENCE_fathom_api_usage.py`
   - Adapt to query all new calls (not just date range)
   - Share calls via API (if available) or keep browser method
   - Write to same database: `fathom_emails.db`

3. **Test in parallel**
   - Run both systems for 1 week
   - Compare results (should be identical)
   - Verify no calls missed
   - Check database consistency

4. **Keep existing system as fallback**
   - Don't delete cookie-based scripts
   - Keep as backup if API has issues

### Phase 2: Gmail OAuth Improvement

**Goal:** Make Gmail authentication more robust and explicit

**Steps:**
1. **Rename token file to be explicit**
   - `token.json` → `token_fathomizer.json`
   - Makes it clear which account it's for

2. **Add verification step**
   - Check account after authentication
   - Fail fast if wrong account
   - Use pattern from `REFERENCE_gmail_oauth_setup.py`

3. **Create refresh script**
   - `scripts/refresh_gmail_auth.sh`
   - Guides user through re-authentication
   - Verifies correct account

### Phase 3: Cutover (Only After Proven)

**Goal:** Switch to API-based system as primary

**Steps:**
1. **Update `run_all.sh`**
   - Call `run_daily_share_api.py` instead of `run_daily_share.py`
   - Keep old script available with `--legacy` flag

2. **Update documentation**
   - Mark cookie method as "legacy fallback"
   - Document API method as primary
   - Keep both documented

3. **Monitor for 1 month**
   - Watch for any issues
   - Keep cookie method ready if needed
   - Document any API limitations

---

## Key Differences: Cookie vs API

### Current Cookie Method (IN USE NOW in FathomInventory)

**Pros:**
- ✅ Works now in production
- ✅ Well-documented
- ✅ Proven reliable (when cookies fresh)

**Cons:**
- ❌ Weekly manual refresh required
- ❌ Browser automation (slower, more fragile)
- ❌ Cookies expire without warning
- ❌ Scraping HTML (breaks if UI changes)

### Future API Method (USED in integration_scripts, NOT in FathomInventory yet)

**Pros:**
- ✅ No expiration (API key long-lived)
- ✅ Direct API access (faster)
- ✅ Structured data (no HTML parsing)
- ✅ Get emails directly (no scraping)
- ✅ No maintenance needed

**Cons:**
- ❌ Requires API key setup (one-time)
- ❌ API may have rate limits
- ❌ API may not support all features (e.g., sharing?)
- ❌ **Not yet implemented in FathomInventory** (this is the modernization goal)

---

## Critical Constraints

### DO NOT BREAK CURRENT SYSTEM

**The existing system works and is in production use.**

**Rules for modernization:**
1. **Build in parallel** - New system alongside old
2. **Test thoroughly** - 1+ week of parallel operation
3. **Keep fallback** - Old system available if new fails
4. **Gradual cutover** - Switch only after proven
5. **Document both** - Keep old method documented

### Preserve Data Integrity

**The database is the source of truth.**

**Rules:**
1. Both systems must write to same database
2. No duplicate entries
3. No data loss during transition
4. Verify consistency between methods

### Maintain Automation

**The system runs daily at 3:00 AM via launchd.**

**Rules:**
1. New system must work unattended
2. Error handling must be robust
3. Logging must be clear
4. Failures must be detectable

---

## Links to Related Documentation

### Current System Documentation

**In FathomInventory:**
- `/FathomInventory/README.md` - System overview
- `/FathomInventory/docs/AUTHENTICATION_GUIDE.md` - Current auth system
- `/FathomInventory/docs/TECHNICAL_DOCUMENTATION.md` - Architecture
- `/FathomInventory/authentication/cookie_export_guide.md` - Cookie export process

**Reference Models:**
- `/Other_Data_Sources/BROWSER_COOKIE_AUTH_PATTERN.md` - Cookie pattern (for services without APIs)
- `/Other_Data_Sources/REFERENCE_convert_edge_cookies.py` - Cookie converter
- `/Other_Data_Sources/REFERENCE_sanitize_cookies.py` - Cookie sanitization

### Integration Scripts (Where API is Used)

**Fathom API:**
- `/integration_scripts/participant_reconciliation/api_enrich_remaining.py` - Production API usage
- `/integration_scripts/participant_reconciliation/archive/experimental/test_api.py` - API tests

**Gmail OAuth:**
- `/integration_scripts/participant_reconciliation/archive/experimental/setup_gmail_auth.py` - Better OAuth setup
- `/integration_scripts/participant_reconciliation/generate_member_review_html.py` - Gmail API usage

### Current Scripts to Modernize

**Fathom access:**
- `/FathomInventory/run_daily_share.py` - Main script (uses cookies)
- `/FathomInventory/fathom_ops/browser.py` - Browser automation layer

**Gmail access:**
- `/FathomInventory/scripts/download_emails.py` - Email download (uses OAuth)

---

## API Capabilities to Investigate

### Known Fathom API Endpoints

**From `api_enrich_remaining.py`:**
```
GET https://api.fathom.ai/external/v1/meetings
  - Query meetings by date range
  - Get meeting metadata
  - Get calendar_invitees (with emails)
  - Supports pagination (cursor-based)
```

### Questions for Future Investigation

1. **Can we share calls via API?**
   - Current: Browser automation clicks "Share" button
   - Desired: API endpoint to share call to email
   - If not available: Keep browser method for sharing

2. **Can we get call URLs via API?**
   - Current: Scrape from HTML
   - Desired: API returns call URL
   - Check: `meeting` object structure

3. **What are API rate limits?**
   - Need to know for daily automation
   - May need to throttle requests

4. **What metadata is available?**
   - Current: Scrape title, date, participants
   - Desired: All metadata from API
   - Check: Full `meeting` object schema

5. **How to get API key?**
   - Document the process
   - Where in Fathom UI?
   - Any permissions needed?

---

## Testing Checklist

### Before Cutover to API Method

- [ ] API key obtained and tested
- [ ] Can query all meetings (not just date range)
- [ ] Can get participant emails
- [ ] Can share calls (or keep browser method)
- [ ] Parallel run for 1+ week successful
- [ ] No calls missed vs cookie method
- [ ] Database consistency verified
- [ ] Error handling tested
- [ ] Logging is clear
- [ ] Documentation updated

### Gmail OAuth Improvements

- [ ] Token renamed to `token_fathomizer.json`
- [ ] Verification step added
- [ ] Wrong account detection works
- [ ] Refresh script created
- [ ] Documentation updated

---

## Success Criteria

### Modernization is Complete When:

1. **Fathom API is primary method**
   - No weekly cookie refresh needed
   - API calls work reliably
   - Fallback to cookies available

2. **Gmail OAuth is explicit**
   - Token file name indicates account
   - Wrong account detected immediately
   - Easy to re-authenticate

3. **System is more robust**
   - Less manual maintenance
   - Fewer failure modes
   - Better error messages

4. **Documentation is current**
   - Both methods documented
   - Migration path clear
   - Troubleshooting updated

---

## Context Recovery for Future AI

### If You're Reading This

**You are probably:**
- Tasked with modernizing FathomInventory authentication
- Trying to reduce manual maintenance
- Investigating why cookies keep expiring

**What you need to know:**
1. **Fathom has an API** - See `REFERENCE_fathom_api_usage.py`
2. **Cookie method works** - Don't break it while modernizing
3. **Build in parallel** - Test thoroughly before cutover
4. **Gmail OAuth is good** - Just needs explicit account handling

**Start here:**
1. Read this entire README
2. Study `REFERENCE_fathom_api_usage.py`
3. Get Fathom API key from https://fathom.video/customize
4. Create `run_daily_share_api.py` alongside existing script
5. Test in parallel for 1 week
6. Only then consider cutover

**Don't:**
- Delete or modify existing cookie-based scripts
- Change database schema without testing
- Cut over before parallel testing
- Skip documentation updates

---

## Maintenance Notes

### This Folder

**Reference files are snapshots** (October 28, 2025):
- `REFERENCE_fathom_api_usage.py` - May diverge from original
- `REFERENCE_gmail_oauth_setup.py` - May diverge from original

**If originals have changed significantly:**
- Check `/integration_scripts/participant_reconciliation/` for updates
- Consider updating reference copies
- Document what changed and why

### Original Locations

**Fathom API usage:**
- Primary: `/integration_scripts/participant_reconciliation/api_enrich_remaining.py`
- Tests: `/integration_scripts/participant_reconciliation/archive/experimental/test_api*.py`

**Gmail OAuth setup:**
- Primary: `/integration_scripts/participant_reconciliation/archive/experimental/setup_gmail_auth.py`
- Usage: `/integration_scripts/participant_reconciliation/generate_member_review_html.py`

**Note:** These may move or change. Reference copies here are canonical for this modernization effort.

---

**Last Updated:** October 28, 2025  
**Status:** Planning phase - no changes to production system yet  
**Next Step:** Get Fathom API key and create parallel implementation
