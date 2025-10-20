# Backup and Recovery Guide

**Purpose:** Protect FathomInventory database from corruption, loss, or mistakes  
**Critical:** Database is 296MB with 1,620+ participants, 1,619 calls, 3,240 emails  
**Last Updated:** October 19, 2025

---

## 🔒 Automated Backup System

### Quick Backup (Before Any Modifications)

```bash
cd /Users/admin/ERA_Admin/FathomInventory
./scripts/backup_database.sh
```

**Creates:**
- `backups/fathom_emails.backup_YYYYMMDD_HHMM.db` (full SQLite copy, ~296MB)
- `backups/fathom_tables_YYYYMMDD_HHMM.zip` (compressed CSV exports, ~44MB)

**Compression:** CSV files are automatically zipped (7x compression ratio)

---

## ✅ Enforcing Backup Discipline

### 1. Pre-Modification Scripts Must Backup

**All Phase 4B enrichment scripts follow this pattern:**

```python
#!/usr/bin/env python3
"""
enrich_from_airtable.py - Enrich Fathom participants with Airtable data
"""

import subprocess
import sys
from pathlib import Path

def require_backup():
    """Enforce backup before any database modifications."""
    print("🔒 Checking for backup requirement...")
    
    # Run backup script
    backup_script = Path(__file__).parent.parent / "FathomInventory" / "scripts" / "backup_database.sh"
    
    try:
        result = subprocess.run([backup_script], check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Backup failed: {e}")
        print("Cannot proceed without backup. Exiting.")
        sys.exit(1)

def main():
    # ALWAYS backup first
    require_backup()
    
    print("✅ Backup complete - proceeding with enrichment...")
    
    # ... rest of script
    
if __name__ == "__main__":
    main()
```

**This ensures:**
- ✅ Cannot modify database without backup
- ✅ Backup failure stops script
- ✅ Timestamped recovery points
- ✅ Both SQLite and CSV safety nets

### 2. Manual Operations Checklist

**Before running any database modification:**
- [ ] Run: `./scripts/backup_database.sh`
- [ ] Verify: Backup files created in `backups/`
- [ ] Check: Database integrity OK
- [ ] Then: Proceed with modification

### 3. Daily Automation Backup

**Add to `run_all.sh` (before Step 3.6 - Airtable sync):**

```bash
# Step 3.5.1: Backup before daily enrichment
echo "🔒 Creating backup before enrichment..."
./scripts/backup_database.sh
```

---

## 🌐 Off-Site Backup Strategy

### Problem: Computer Dies

**Risk:** All local backups lost if computer/disk fails

**Solution:** Three-tier backup strategy

### Tier 1: Local Backups (Immediate Recovery)

**Location:** `/Users/admin/ERA_Admin/FathomInventory/backups/`  
**Retention:** Keep last 7 days of timestamped backups  
**Recovery Time:** Instant (copy file)

```bash
# Automated cleanup (keep last 7 days)
find backups/ -name "*.db" -mtime +7 -delete
find backups/ -name "*.zip" -mtime +7 -delete
```

### Tier 2: Google Drive (Automated Cloud Backup) ☁️

**Location:** fathomizer@ecorestorationalliance.org Google Drive  
**Folder:** `FathomInventory_Backups/`  
**Retention:** 30 days (automatic cleanup)  
**Recovery Time:** 10-30 minutes (download + restore from CSV)

**What Gets Uploaded:**
- Latest CSV archive only (~44MB compressed)
- Contains: participants.csv, calls.csv, emails.csv
- **NOT the .db file** (kept local only for instant recovery)
- 7x smaller/faster than uploading full DB

**Rationale:**
- Local backups/ folder has full .db for instant local recovery
- Cloud backup only needs CSV safety net for disaster recovery
- Can rebuild database from CSV if needed
- Optimizes upload speed and Drive storage

**Daily Automated Upload:**

**Separate launchd job** (runs daily at 4:00 AM):
- Job: `com.era.admin.fathom.backup_drive`
- Schedule: Daily at 4:00 AM (1 hour after main backup)
- Plist: `~/Library/LaunchAgents/com.era.admin.fathom.backup_drive.plist`

**Manual upload:**
```bash
cd /Users/admin/ERA_Admin/FathomInventory
./scripts/upload_backup_to_drive.py
```

**First Time Setup:**
1. Run: `./scripts/upload_backup_to_drive.py`
2. Browser opens for OAuth authorization
3. **CRITICAL:** Sign in as `fathomizer@ecorestorationalliance.org`
4. Grant Drive access (needs Drive API enabled)
5. Credentials saved to `token.json`
6. launchd job auto-runs daily

**Check launchd status:**
```bash
launchctl list | grep backup_drive
# Should show: com.era.admin.fathom.backup_drive

tail ~/Library/Logs/fathom_backup_drive.log
# Should show recent uploads
```

**Daily Report Verification:**

Daily report emails automatically include backup status:

```
💾 BACKUP STATUS
- Local backup: Oct 19, 02:10 PM (2 hours ago)
  Size: 43.7MB (CSV archive)
- Google Drive: Oct 19, 02:26 PM (1 hour ago)
  Size: 43.7MB
```

**What it verifies:**
- Queries Drive API to confirm cloud uploads succeeded
- Shows timestamp and size of most recent Drive backup
- Alerts if either backup is >30 hours old
- Provides confidence both backup tiers are operational

### Tier 3: External Drive (Optional)

**For extra paranoia - manual weekly copy:**

```bash
# Backup to external USB drive (if mounted)
EXTERNAL="/Volumes/Backup_Drive/ERA_Admin_Backups"

if [ -d "$EXTERNAL" ]; then
    cd /Users/admin/ERA_Admin/FathomInventory
    rsync -av --progress backups/ "$EXTERNAL/FathomInventory/"
    echo "✅ Backed up to external drive"
fi
```

---

## 🆘 Recovery Procedures

### Scenario 1: Bad Data After Script Run

**Symptoms:** Script ran, but results look wrong

**Recovery:**
```bash
cd /Users/admin/ERA_Admin/FathomInventory

# Find most recent pre-operation backup
ls -t backups/fathom_emails.backup_*.db | head -1

# Restore (example)
cp backups/fathom_emails.backup_20251019_1410.db fathom_emails.db

# Verify restoration
sqlite3 fathom_emails.db "SELECT COUNT(*) FROM participants;"
# Should show count before modification
```

**Time:** < 1 minute

### Scenario 2: Database Corruption

**Symptoms:** SQLite errors, can't open database

**Recovery:**
```bash
# Check integrity
sqlite3 fathom_emails.db "PRAGMA integrity_check;"

# If corrupt, restore from backup
cp backups/fathom_emails.backup_20251019_1410.db fathom_emails.db

# Verify
sqlite3 fathom_emails.db "PRAGMA integrity_check;"
```

**Time:** < 1 minute

### Scenario 3: Backup Also Corrupt (Rare)

**Recovery from CSV:**
```bash
# Create new empty database
mv fathom_emails.db fathom_emails.CORRUPT.db
sqlite3 fathom_emails.db < schema.sql  # TODO: Export schema

# Restore from CSV
cd backups
unzip fathom_tables_20251019_1410.zip

# Import participants
sqlite3 ../fathom_emails.db <<EOF
.mode csv
.import participants.csv participants
EOF

# Import calls
sqlite3 ../fathom_emails.db <<EOF
.mode csv
.import calls.csv calls
EOF

# Import emails
sqlite3 ../fathom_emails.db <<EOF
.mode csv
.import emails.csv emails
EOF
```

**Time:** 5-10 minutes

### Scenario 4: Computer Dies / Disk Failure

**Recovery:**

1. **Get new computer**

2. **Clone repository and setup:**
   ```bash
   # Clone FathomInventory from GitHub
   cd /Users/admin
   mkdir ERA_Admin
   cd ERA_Admin
   git clone https://github.com/jonschull/ERA_fathom_inventory.git FathomInventory
   cd FathomInventory
   
   # Create venv
   python3 -m venv ../ERA_Admin_venv
   source ../ERA_Admin_venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Restore from Google Drive:**
   ```bash
   # Get credentials (from secure backup or re-setup OAuth)
   # Copy your backup credentials.json if you have it saved somewhere
   
   # Run Drive restore script
   ./scripts/upload_backup_to_drive.py --download-latest
   # Or manually: Go to drive.google.com → FathomInventory_Backups folder
   # Download latest .db and .zip files to backups/
   
   # Restore database
   cd /Users/admin/ERA_Admin/FathomInventory
   cp backups/fathom_emails.backup_YYYYMMDD_HHMM.db fathom_emails.db
   
   # Verify restoration
   sqlite3 fathom_emails.db "SELECT COUNT(*) FROM participants;"
   # Should show 1,620+
   ```

4. **Alternative: Restore from external drive backup** (if you have one)

**Time:** 30-60 minutes (setup + download)

**Data Loss:** Depends on last Google Drive backup (daily = up to 24 hours)

---

## 📊 Backup Retention Policy

### Local Backups (backups/)
- **Frequency:** Before each modification + daily automation
- **Retention:** 7 days (auto-cleanup)
- **Size:** ~340MB per backup (DB + CSV)

### Cloud Backups (Google Drive)
- **Frequency:** Daily automated upload (via separate launchd at 4 AM)
- **Retention:** 30 days (automatic cleanup)
- **Size:** ~44MB per backup (~1.3GB total for 30 days)
- **Account:** fathomizer@ecorestorationalliance.org
- **Upload time:** ~40 seconds (vs 5+ minutes for full DB)

---

## 🔍 Verification Checklist

### Before Phase 4B Operations

- [ ] Backup script tested: `./scripts/backup_database.sh`
- [ ] Backup created successfully
- [ ] Database integrity check passed
- [ ] Backup files exist in `backups/`
- [ ] CSV archive created (~44MB)
- [ ] Google Drive upload configured: `./scripts/upload_backup_to_drive.py`
- [ ] Drive backup folder created: `FathomInventory_Backups`
- [ ] Test Drive upload successful

### Daily Verification

**Automatic (in daily report email):**
- ✅ Local backup timestamp and size
- ✅ Google Drive backup timestamp and size  
- ✅ Alerts if either backup is >30 hours old

**Manual checks (if concerned):**
```bash
# Check local backups
ls -lht backups/ | head -5

# Check Drive backups (via web)
# https://drive.google.com → FathomInventory_Backups folder
```

### Weekly Maintenance

- [ ] Review daily reports for backup alerts
- [ ] Test restore procedure (once a month)
- [ ] Document any schema changes

---

## 🚨 Red Flags - Stop Immediately

**If you see:**
- ❌ Backup script fails
- ❌ Database integrity check fails
- ❌ No backups/ directory
- ❌ Backup older than 24 hours before modification

**Action:** DO NOT PROCEED until backup issue resolved

---

## 📝 Recovery Test Log

**Test restores monthly to ensure process works:**

```
2025-10-19: Initial backup system created, tested successfully
YYYY-MM-DD: Tested restore from local backup - OK
YYYY-MM-DD: Tested restore from Google Drive - OK
YYYY-MM-DD: Tested restore from CSV - OK
```

---

**This backup system protects against:**
- ✅ Script bugs creating bad data (local restore: 1 minute)
- ✅ Database corruption (local restore: 1 minute)
- ✅ Accidental deletions (local restore: 1 minute)
- ✅ Disk failure (cloud restore: 30 minutes)
- ✅ Computer loss/theft (cloud restore: 30-60 minutes)
- ✅ User mistakes (rollback to any backup point)

**Monitoring & Verification:**
- ✅ Daily report verifies both local and cloud backups
- ✅ Queries Google Drive API to confirm uploads succeeded
- ✅ Alerts if backups are stale (>30 hours old)
- ✅ Shows timestamp and size for both backup tiers

**Recovery time: 1 minute (local) to 60 minutes (disaster)**

**Data loss: Maximum 24 hours (daily cloud backups)**

**Storage cost: ~1.3GB Google Drive space (30 days of CSV backups)**
