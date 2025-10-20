# FathomInventory Automation Monitoring Guide

**Last Updated:** October 3, 2025  
**System Status:** ✅ OPERATIONAL

## Quick Health Check

### 1. Check if automation is running:
```bash
launchctl list | grep fathom
```
**Expected output:** `- 0 com.fathominventory.run`

### 2. Check recent activity:
```bash
tail -20 /Users/admin/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon Schull/CascadeProjects/ERA_Admin/FathomInventory/cron.log
```
**Look for:** Daily entries with timestamps around 10:00 AM EDT

### 3. Check for successful completion:
```bash
grep "finished successfully" cron.log | tail -5
```

## Detailed Monitoring

### Log File Analysis

**Location:** `cron.log` (in the project root)

**Healthy Log Pattern:**
```
==================================================
Starting Fathom Inventory run at [DATE TIME]
==================================================
Activating virtual environment...

--- Running run_daily_share.py ---
Found [NUMBER] existing calls in the master list.
Navigating to Fathom home page...
[... processing details ...]
run_daily_share.py completed successfully.

--- Waiting for 300 seconds for emails to be processed ---

--- Running download_emails.py ---
Found [NUMBER] emails already in the local database.
[... email processing ...]
download_emails.py completed successfully.

==================================================
Fathom Inventory run finished successfully at [DATE TIME]
==================================================
```

### Key Metrics to Monitor

1. **Daily Execution**
   - Should run every day at 10:00 AM EDT
   - Look for "Starting Fathom Inventory run" messages

2. **Call Discovery**
   - "Found X existing calls in the master list"
   - "Found X new calls to add" (when new calls exist)
   - "No new calls found" (normal when no new calls)

3. **Email Processing**
   - "Found X emails already in the local database"
   - "No new emails to download" or "Downloading X new emails"

4. **Success Indicators**
   - "run_daily_share.py completed successfully"
   - "download_emails.py completed successfully"
   - "finished successfully at [timestamp]"

### Warning Signs

🚨 **Critical Issues:**
- No log entries for 24+ hours
- "Error:" messages in logs
- "failed with exit code" messages
- Python tracebacks/exceptions

⚠️ **Minor Issues (monitor but not critical):**
- SSL warnings (urllib3 with LibreSSL - cosmetic only)
- "Could not click" or "Could not find" (may indicate UI changes)
- Network timeout warnings

### Data Growth Monitoring

**Check database growth:**
```bash
# Check database file size and modification time
ls -la fathom_emails.db

# Check number of calls tracked
wc -l all_fathom_calls.tsv

# Check recent database activity
sqlite3 fathom_emails.db "SELECT COUNT(*) FROM emails;"
```

**Expected patterns:**
- `all_fathom_calls.tsv` should grow when new calls are discovered
- `fathom_emails.db` should grow when new emails are processed
- Database should be modified daily (even if no new data)

## Troubleshooting

### If Automation Stops Running

1. **Check if job is loaded:**
   ```bash
   launchctl list | grep fathom
   ```

2. **If not loaded, reload it:**
   ```bash
   launchctl load ~/Library/LaunchAgents/com.fathominventory.run.plist
   ```

3. **Check job status:**
   ```bash
   launchctl print gui/$(id -u)/com.fathominventory.run
   ```

### Manual Testing

**Run the automation manually:**
```bash
cd /Users/admin/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon Schull/CascadeProjects/ERA_Admin/FathomInventory
./run_all.sh
```

**Test individual components:**
```bash
# Test call discovery and sharing
python run_daily_share.py

# Test email download
python download_emails.py
```

### Common Issues & Solutions

**Issue:** "Virtual environment not found"
- **Solution:** Check that `../venv/` exists relative to project directory
- **Command:** `ls -la ../venv/bin/activate`

**Issue:** "Cookies file not found"
- **Solution:** Update browser cookies in `fathom_cookies.json`
- **See:** Project README for cookie export instructions

**Issue:** "Gmail API authentication failed"
- **Solution:** Re-authenticate Google API
- **Command:** `rm token.json` then run `python download_emails.py`

## Current System Status (as of Oct 3, 2025)

✅ **Automation:** Running daily at 10:00 AM  
✅ **Call Discovery:** Working (found 2 new calls on Oct 3)  
✅ **Email Processing:** Working (1588 emails in database)  
✅ **Database:** Healthy and growing  
✅ **Authentication:** Credentials for `jschull@e-nable.org` are confirmed working.

### Recent Activity Summary
- **Last successful run:** Oct 3, 2025 at 18:51 PM
- **New calls discovered:** 2 calls found and shared
- **Email database:** 1588 emails processed
- **System health:** Fully operational

## Architecture Overview

```
macOS `launchd` scheduler (the standard macOS equivalent of `cron`)
    ↓ (daily at 10:00 AM)
~/Library/LaunchAgents/com.fathominventory.run.plist
    ↓ (executes)
run_all.sh (in project directory)
    ↓ (runs sequence)
    1. run_daily_share.py → discovers new calls → shares to fathomizer@ecorestorationalliance.org
    2. sleep 300 seconds (5 minutes for email delivery)
    3. download_emails.py → fetches emails → converts to markdown → stores in database
    ↓ (all output logged to)
cron.log (in project directory)
```

## Emergency Contacts & Resources

- **Project Directory:** `/Users/admin/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon Schull/CascadeProjects/ERA_Admin/FathomInventory/`
- **Log File:** `cron.log` (in project directory)
- **Configuration:** `~/Library/LaunchAgents/com.fathominventory.run.plist`
- **Documentation:** `README.md`, `PROJECT_REVIEW_ANALYSIS.md`, `SYSTEMATIC_FIXES_ANALYSIS.md`
