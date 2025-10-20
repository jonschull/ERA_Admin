# Failure Detection & Remediation Improvements

**Date:** October 17, 2025  
**Issue:** System was failing silently for 8 days due to expired Fathom cookies

## Problems Identified

### 1. **Silent Failures in Bash Pipeline**
**Problem:** Exit codes from Python scripts were lost in bash pipelines
```bash
# OLD - BROKEN
"$PYTHON" script.py 2>&1 | tee log1 | tee log2
EXIT_CODE=$?  # This captured tee's exit code (always 0), not Python's!
```

**Impact:** Script reported "✅ completed successfully" even when Python exited with error code 1

### 2. **No Pre-Flight Authentication Check**
**Problem:** Script attempted to scrape Fathom.video without verifying cookies work
- Would timeout after 15 seconds waiting for page elements
- Reported ambiguous "No new calls found" (could mean auth failure OR legitimately no calls)

### 3. **Weak Daily Report Alerts**
**Problem:** Alerts were vague and not actionable
- "may indicate auth issue (or legitimately no new calls)" - too uncertain
- No log analysis to confirm failures
- Critical issues buried in warnings

## Solutions Implemented

### 1. Fixed Bash Pipeline Exit Code Handling

**File:** `run_all.sh`

```bash
# NEW - WORKING
set -o pipefail  # Enable at top of script

set +e  # Temporarily disable exit on error
"$PYTHON" -u run_daily_share.py --use-db 2>&1 | tee -a "${PRIMARY_LOG}" >> "${CONSOLE_LOG}"
SHARE_EXIT_CODE=${PIPESTATUS[0]}  # Get Python's exit code from pipeline array
set -e  # Re-enable exit on error

if [ $SHARE_EXIT_CODE -ne 0 ]; then
    log_and_echo "❌ Error: run_daily_share.py failed with exit code $SHARE_EXIT_CODE."
    log_and_echo "   This usually indicates authentication failure or network issues."
    exit 1  # Stop automation
fi
```

**Result:** Automation now stops immediately when authentication fails

### 2. Added Pre-Flight Authentication Check

**File:** `run_daily_share.py`

New function `verify_authentication()`:
- Navigates to Fathom.video before attempting to scrape
- Checks for login page redirects
- Verifies "My Calls" link is present
- **Exits with code 1 if authentication fails** (stops automation)

```python
async def verify_authentication(page):
    """Pre-flight check: Verify authentication before attempting to scrape."""
    print("🔐 Pre-flight authentication check...")
    await page.goto("https://fathom.video/home", timeout=30000)
    
    # Check for login redirect
    login_indicators = await page.query_selector_all('a[href*="login"], ...')
    if login_indicators:
        print("❌ AUTHENTICATION FAILED: Redirected to login page")
        print("   → Run: ./scripts/refresh_fathom_auth.sh")
        return False
    
    # Verify authenticated state
    my_calls = await page.query_selector('a:has-text("My Calls")')
    if not my_calls:
        print("❌ AUTHENTICATION FAILED: Cannot find 'My Calls' link")
        return False
    
    print("✅ Authentication verified")
    return True
```

**Result:** Clear, immediate failure detection with actionable remediation steps

### 3. Enhanced Daily Report Alerts

**File:** `scripts/send_daily_report.py`

**Added log analysis:**
```python
def check_recent_auth_failures():
    """Check recent log files for authentication failures."""
    log_patterns = [
        "TimeoutError: Page.wait_for_selector",
        "AUTHENTICATION FAILED",
        "Redirected to login",
        "Timeout 15000ms exceeded"
    ]
    # Analyzes last 200 lines of logs
```

**Separated critical vs. warnings:**
- **🚨 CRITICAL ISSUES** - Authentication failures, wrong account
- **⚠️ WARNINGS** - Cookie age, stale data (non-blocking)

**Result:** Unmistakable alerts with specific root cause

## Before vs. After

### Before (Oct 9-17: Silent Failure)
```
✅ run_daily_share.py completed successfully.
No new calls found.
⚠️ Zero new calls found - may indicate auth issue (or legitimately no new calls)
```
- Automation continued running
- No clear indication of problem
- Daily emails said "may indicate" but weren't definitive

### After (Oct 17: Immediate Detection)
```
🔐 Pre-flight authentication check...
❌ AUTHENTICATION FAILED: Cannot find 'My Calls' link
   → Fathom site may have changed or cookies expired

============================================================
❌ CRITICAL: Authentication failure - cannot proceed
============================================================
❌ Error: run_daily_share.py failed with exit code 1.
   This usually indicates authentication failure or network issues.
Run finished with errors at Fri Oct 17 11:40:34 EDT 2025
```

**Daily Report:**
```
🚨 CRITICAL ISSUES - IMMEDIATE ACTION REQUIRED

🔴 AUTHENTICATION FAILURE DETECTED: Found 'AUTHENTICATION FAILED' in logs
   ACTION REQUIRED: Run ./scripts/refresh_fathom_auth.sh
   → New calls cannot be discovered until cookies are refreshed
```

## Testing Verification

Tested with expired cookies (Oct 17, 2025):

1. ✅ Python script exits with code 1 on auth failure
2. ✅ Bash pipeline correctly captures exit code
3. ✅ Automation stops immediately (doesn't continue to steps 2-4)
4. ✅ Logs show clear failure message
5. ✅ Daily report will flag critical issue with log analysis

## Maintenance Impact

**Weekly cookie refresh still required** - this is a Fathom.video limitation

**What changed:**
- Failures are now **detected within seconds** (not days)
- Clear **actionable remediation** steps provided
- System **stops trying** instead of wasting time/resources
- Daily email will have **unmistakable critical alerts**

## Files Modified

1. `run_all.sh` - Fixed exit code handling, improved error messages
2. `run_daily_share.py` - Added pre-flight authentication check
3. `scripts/send_daily_report.py` - Added log analysis, critical alert separation

## Future Improvements

Consider:
1. Automated cookie refresh (requires Playwright or browser automation)
2. Slack/SMS alerts for critical failures (not just email)
3. Health check endpoint for external monitoring
4. Cookie expiration prediction (warn before failure)
