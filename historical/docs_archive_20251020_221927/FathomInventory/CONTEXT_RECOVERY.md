# Context Recovery Guide

**Purpose:** Enable any AI or human to quickly understand the project state and resume work.

**Critical Requirement:** This file MUST be updated with every significant PR.

---

## 🎯 Project Overview

**Name:** Fathom Inventory System  
**Repo:** https://github.com/jonschull/ERA_fathom_inventory (private)  
**Location:** `/Users/admin/FathomInventory`

**Purpose:** Automatically downloads, processes, and analyzes Fathom meeting summaries from jschull@e-nable.org account.

**Production Status:** ✅ FULLY OPERATIONAL (Oct 17, 2025)

---

## 📊 Current System State (Oct 19, 2025)

### What's Working
- ✅ **1,620 calls** tracked in SQLite database
- ✅ **3,240 emails** processed with full metadata
- ✅ **Database mode** active (TSV migration complete)
- ✅ **Enhanced failure detection** - catches auth failures immediately
- ✅ **Daily automation** at 3:00 AM via macOS launchd
- ✅ **Automated backups** - Local (daily 3 AM) + Google Drive (daily 4 AM)
- ✅ **Backup verification** - Daily report queries Drive API to confirm uploads
- ✅ **Fresh authentication** - cookies refreshed Oct 17

### Recent Work

**Oct 19, 2025: Automated Backup System**
- **Problem:** No disaster recovery if computer dies or disk fails
- **Solution:** 3-tier backup system with verification
  1. Local backups (daily, 7-day retention)
  2. Google Drive backups (daily at 4 AM, 30-day retention, ZIP only)
  3. Daily report verifies both tiers via Drive API
- **Scripts:** `backup_database.sh`, `upload_backup_to_drive.py`
- **Launchd:** `com.era.admin.fathom.backup_drive` (separate job at 4 AM)
- **Docs:** `BACKUP_AND_RECOVERY.md`
- **Impact:** Max data loss reduced from ∞ to 24 hours

**Oct 17, 2025: Enhanced Failure Detection**
- **Problem:** System failed silently for 8 days due to expired cookies
- **Solution:** Pre-flight checks, bash exit code fixes, enhanced alerts
- **PR:** #19
- **Impact:** Discovered 8 missed calls, system fully restored

---

## 🗺️ System Architecture

```
Daily Automation:

3:00 AM - run_all.sh (launchd: com.era.admin.fathom.run)
  │
  ├─> Step 0: scripts/backup_database.sh (NEW Oct 19)
  │   ├─> SQLite backup (296MB)
  │   ├─> CSV export + compress (44MB ZIP)
  │   └─> Integrity check
  │
  ├─> Step 1: run_daily_share.py --use-db
  │   ├─> Pre-flight auth check (NEW Oct 17)
  │   ├─> Scrape Fathom for new calls
  │   ├─> Share to fathomizer@ecorestorationalliance.org
  │   └─> Update fathom_emails.db (calls table)
  │
  ├─> Step 2: Wait 5 minutes (for emails)
  │
  ├─> Step 3: scripts/download_emails.py
  │   ├─> Fetch Gmail responses
  │   ├─> Parse with fathom_email_2_md.py
  │   └─> Update fathom_emails.db (emails table)
  │
  └─> Step 4: scripts/send_daily_report.py
      ├─> Analyze logs for failures (NEW Oct 17)
      ├─> Check database health
      ├─> Verify local backup timestamp (NEW Oct 19)
      ├─> Query Google Drive for cloud backup (NEW Oct 19)
      └─> Email report to jschull@gmail.com

4:00 AM - upload_backup_to_drive.py (launchd: com.era.admin.fathom.backup_drive)
  ├─> Upload latest ZIP to Google Drive (NEW Oct 19)
  ├─> Auto-delete backups >30 days old
  └─> Log: ~/Library/Logs/fathom_backup_drive.log
```

---

## 📁 Key Files

### Root Documentation (Read These First)
- **`README.md`** - User guide, quick start, current status
- **`DEVELOPMENT.md`** - Developer workflow, testing, constraints
- **`CONTEXT_RECOVERY.md`** - This file (context for resuming work)
- **`BACKUP_AND_RECOVERY.md`** - Backup system, disaster recovery (NEW Oct 19)

### Core Scripts
- **`run_all.sh`** - Main orchestrator (called by launchd)
- **`run_daily_share.py`** - Call discovery and sharing
- **`scripts/download_emails.py`** - Email fetching and processing
- **`scripts/send_daily_report.py`** - Daily health report (includes backup verification)
- **`scripts/backup_database.sh`** - Local backup creation (NEW Oct 19)
- **`scripts/upload_backup_to_drive.py`** - Google Drive upload (NEW Oct 19)

### Technical Documentation
- **`docs/FAILURE_DETECTION_IMPROVEMENTS.md`** - Oct 17 improvements (NEW)
- **`docs/TECHNICAL_DOCUMENTATION.md`** - Complete system architecture
- **`docs/AUTHENTICATION_GUIDE.md`** - Cookie/OAuth setup
- **`docs/AUTOMATION_MONITORING_GUIDE.md`** - Scheduling and monitoring

### Data Files (gitignored)
- **`fathom_emails.db`** - SQLite database (calls + emails tables)
- **`fathom_cookies_enable.json`** - Fathom.video auth (e-NABLE account)
- **`fathom_cookies_era.json`** - Fathom.video auth (ERA account)
- **`token.json`** - Gmail OAuth credentials
- **`credentials.json`** - Google API credentials
- Active account configured in `../era_config.py`

---

## 🚀 How to Resume Work

### 1. Verify System Health
```bash
cd /Users/admin/FathomInventory
git status                    # Should be on main branch
git log --oneline -5          # Check recent commits
python -m pytest tests/ -q    # Run tests (if any)
```

### 2. Check Production System
```bash
# View recent automation runs
tail -50 cron.log

# Check scheduled job
launchctl list | grep fathom

# Verify database state
sqlite3 fathom_emails.db "SELECT COUNT(*) FROM calls;"
sqlite3 fathom_emails.db "SELECT MAX(created_at) FROM calls;"
```

### 3. Test Authentication
```bash
cd authentication
python test_fathom_cookies.py    # Should show ✅ OK
python test_google_auth.py        # Should show ✅ OK
```

### 4. Review Recent Activity
- Check GitHub PRs: https://github.com/jonschull/ERA_fathom_inventory/pulls
- Review daily email reports sent to jschull@gmail.com
- Read `docs/FAILURE_DETECTION_IMPROVEMENTS.md` for latest improvements

---

## 🔧 Common Tasks

### Refresh Fathom Cookies (Weekly)
```bash
./scripts/refresh_fathom_auth.sh
# Follow prompts to export cookies from Edge browser
```

### Manual Run (Testing)
```bash
# Run discovery and sharing
python run_daily_share.py --use-db

# Download emails (wait 5 min after sharing)
python scripts/download_emails.py

# Send daily report
python scripts/send_daily_report.py
```

### Check for Authentication Failures
```bash
# Pre-flight check will fail immediately if cookies expired
python run_daily_share.py --use-db
# Exit code 1 = auth failure, clear error message
```

### Create PR
```bash
git checkout -b feature/description
# Make changes
git add -A
git commit -m "feat: description"
git push -u origin feature/description
gh pr create --title "feat: description" --body "..."
```

---

## ⚠️ Known Issues & Constraints

### Weekly Maintenance Required
- **Fathom cookies expire** - Refresh weekly with `./scripts/refresh_fathom_auth.sh`
- System will detect failures immediately (as of Oct 17)

### Dropbox File Locking
- Project located in Dropbox (historic reasons)
- Launchd has file locking issues with Dropbox
- Logs moved to `/Users/admin/Library/Logs/` to mitigate
- Consider moving entire project out of Dropbox if issues persist

### Multi-Account Setup
- **Configuration:** `../era_config.py` (FATHOM_ACTIVE_ACCOUNT = 'enable')
- **e-NABLE:** `fathom_cookies_enable.json` → jschull@e-nable.org (active)
- **ERA:** `fathom_cookies_era.json` → ecorestorationalliance@gmail.com
- **Switch:** Set `FATHOM_ACCOUNT=era` env var or edit era_config.py

---

## 🤖 Analysis Automation (NEW - Oct 17, 2025)

### Participant Database
- **1,560 participant records** from 619 unique individuals
- **1,270 ERA community members** tracked
- **Automated daily analysis** of new ERA meetings
- **Database:** `participants` table in `fathom_emails.db`

### Daily Workflow Enhancement
```
Step 3.5 (NEW): ERA Meeting Analysis
  - Syncs ERA meetings from database
  - Analyzes new meetings with Fathom AI
  - Extracts participant data
  - Updates database automatically
  - Adds stats to daily report
```

### Query Participant Data
```bash
sqlite3 fathom_emails.db << SQL
-- Most active ERA participants
SELECT name, COUNT(*) as meetings 
FROM participants 
WHERE source_call_title LIKE '%ERA%'
GROUP BY name ORDER BY meetings DESC LIMIT 10;
SQL
```

### Files
- `analysis/CONTEXT_RECOVERY.md` - Analysis module details
- `analysis/analyze_new_era_calls.py` - Daily automation script
- See `analysis/PHASE3_COMPLETE.md` for full documentation

---

## 🔄 Rollback Procedures

### Revert Last Commit
```bash
git revert HEAD
git push origin main
```

### Emergency Rollback
```bash
# View available tags
git tag

# Rollback to specific tag
git reset --hard v0.1.0-local-baseline

# Check backups
ls backups/
```

---

## 🧪 Testing Guidelines

### Before Every PR
- [ ] Run `python run_daily_share.py --use-db` successfully
- [ ] Check `cd authentication && python test_fathom_cookies.py` shows ✅
- [ ] Verify no secrets in git: `git status` shows no `.json` or `.db` files
- [ ] Update this CONTEXT_RECOVERY.md if system state changed
- [ ] Update README.md if user-facing behavior changed

### After Merging PR
- [ ] Monitor next automation run (check cron.log at 3 AM)
- [ ] Verify daily email report received
- [ ] Check database updated: `sqlite3 fathom_emails.db "SELECT COUNT(*) FROM calls;"`

---

## 🎓 Project Principles

1. **PR-driven development** - All changes via focused PRs
2. **Clean documentation** - Root minimal, docs/ organized, archive/ for history
3. **Fail fast** - Detect problems immediately with clear errors
4. **Weekly maintenance** - Cookie refresh is required
5. **Proactive validation** - Test before declaring success
6. **Context preservation** - Update this file with every significant change

---

## 📝 AI-Specific Recovery Instructions

If you are an AI resuming this work:

1. **Read this file completely** before asking questions
2. **Check system health** with commands in "How to Resume Work" section
3. **Review recent PRs** to understand what changed
4. **Follow project principles** - especially "proactive validation"
5. **Don't assume user approval** - wait for explicit go-ahead
6. **Update this file** if you make significant changes

### Quick Context Questions to Ask Yourself
- What's the current system status? (Check README.md § System Status)
- When was the last successful run? (Check cron.log)
- Are there any open PRs? (Check GitHub)
- Is authentication working? (Test with authentication/test_fathom_cookies.py)
- What was the last major change? (Check this file's history)

---

## 📞 Contact

**User:** Jon Schull  
**Email:** jschull@gmail.com (receives daily reports)  
**Repo:** https://github.com/jonschull/ERA_fathom_inventory

---

**Last Updated:** October 17, 2025  
**Last Major Change:** Analysis automation integrated (Phase 1-3 complete)  
**System Status:** ✅ Fully Automated, 1,616 calls tracked, 1,560 participants analyzed  
**Next Maintenance:** Refresh cookies by Oct 24, 2025
