# Code Audit Findings - FathomInventory Move Recovery

**Date:** Oct 18, 2025 10:41 AM  
**Purpose:** Map all broken paths/configs from moving FathomInventory into ERA_Admin

## Timeline Verification (Evidence-Based)

### Database Evidence
- **Oct 9**: 7 calls added to database
- **Oct 10-16**: NO automation (venv Dropbox file-locking issue)
- **Oct 17, 10:00-10:05 AM**: Manual runs succeeded, caught up 8 missed calls (Oct 10-17 dates)
- **Oct 17, 11:40 AM**: Run attempted, finished with errors
- **Oct 17, 20:34 PM**: Created backup (FathomInventory 17-10-2025.zip)
- **Oct 17, 20:36 PM**: Updated wrapper script, moved FathomInventory into ERA_Admin
- **Oct 17, 20:42-20:48 PM**: Manual run succeeded (post-move, 1 new call added)
- **Oct 18, 06:00-10:30 AM**: Launchd monitor tried every 30 min, all FAILED ("crashed immediately")
- **Oct 18, 10:00-10:36 AM**: Manual run succeeded (0 new calls)

### Key Findings

1. **System retrieved missed calls successfully** on Oct 17 morning (8 calls from Oct 10-17)
2. **Manual execution WORKS** post-move (verified Oct 17 PM & Oct 18 AM)
3. **Launchd automation BROKEN** post-move (all attempts crash immediately)
4. **Venv path issues FIXED** but launchd still failing (11:00 AM investigation)

### Root Cause Analysis (Updated 11:10 AM)

**Initial hypothesis:** Venv paths pointing to wrong location
- Status: ✅ FIXED (lines 70, 82 in run_all.sh)
- Result: Manual execution works, launchd still fails

**Second hypothesis:** Dropbox not ready when launchd starts
- Status: ⚠️ POSSIBLE but not primary cause
- Evidence: Test wrapper with Dropbox-ready check works manually

**ACTUAL ROOT CAUSE (11:10 AM):** Monitor script path bug
- **File:** `scripts/monitor_fathom.sh`
- **Issue:** Line 68 tries to run `$SCRIPT_DIR/run_all.sh`
- **Problem:** `$SCRIPT_DIR` = `.../FathomInventory/scripts/`
- **But run_all.sh is at:** `.../FathomInventory/run_all.sh` (parent dir!)
- **Result:** Monitor tries to execute non-existent file, crashes immediately
- **Why manual works:** Wrapper script (`run_fathom_daily.sh`) correctly cd's to FathomInventory root

---

## Audit Status

- [x] Shell scripts checked
- [x] Python scripts checked  
- [x] Config files checked
- [x] Launchd configs checked
- [x] Documentation checked

**Audit Complete: 10:46 AM**

---

## Findings

### 1. Shell Scripts

#### `FathomInventory/run_all.sh` ❌ BROKEN
- **Line 70:** `VENV_PATH="/Users/admin/FathomInventory_venv/bin/activate"`
  - Points to OLD venv location
  - Should be: `/Users/admin/ERA_Admin_venv/bin/activate`
- **Line 82:** `PYTHON="/Users/admin/FathomInventory_venv/bin/python3"`
  - Points to OLD venv location  
  - Should be: `/Users/admin/ERA_Admin_venv/bin/python3`
- **Impact:** Launchd fails with "Resource deadlock avoided" when trying to access old venv

#### `FathomInventory/scripts/refresh_fathom_auth.sh` ❌ BROKEN
- **Line 15:** `PYTHON="${PROJECT_ROOT}/venv/bin/python3"`
  - Looks for venv in project root (inside Dropbox)
  - Should be: `/Users/admin/ERA_Admin_venv/bin/python3`
- **Impact:** Cookie refresh will fail, falls back to system Python

#### `FathomInventory/scripts/verify_daily_run.sh` ✅ OK
- Uses relative paths, should work

#### `FathomInventory/scripts/monitor_fathom.sh` ✅ OK
- Uses relative paths, should work

### 2. Launchd Configuration

#### `.local/bin/run_fathom_daily.sh` ✅ OK
- Correctly points to new location (updated Oct 17 20:36)
- Path: `ERA_Admin/FathomInventory`

#### `com.era.admin.fathom.run.plist` ❌ BROKEN
- **Lines 19-21:** Log paths point to OLD location
  - Current: `/Users/admin/FathomInventory/logs/fathom_run.log`
  - Should be: `/Users/admin/Library/Logs/fathom_run.log` (outside Dropbox)

#### `com.era.admin.fathom.verify.plist` ✅ OK
- Correctly points to new location in ERA_Admin

#### `com.era.admin.fathom.monitor.plist` ✅ OK
- Correctly points to new location in ERA_Admin

### 3. Python Scripts & Config Files

#### `FathomInventory/README.md` ✅ OK
- **Line 45:** Already updated to reference `../ERA_Admin_venv`
- Documentation correct for new location

#### `era_config.py` ✅ OK (verified earlier)
- Already points to correct FathomInventory location inside ERA_Admin
- All paths verified working

### 4. Documentation

#### `FathomInventory/CONTEXT_RECOVERY.md` ❌ OUTDATED
- **Line 13:** Says location is `/Users/admin/FathomInventory` (OLD)
- Should say: Inside ERA_Admin (Dropbox)

#### `FathomInventory/DEVELOPMENT.md` ⚠️ OUTDATED
- References venv being in Dropbox (line 31)
- Needs update to reflect venv at `/Users/admin/ERA_Admin_venv`

---

## Summary of Issues

### CRITICAL (Blocks Automation) - UPDATED 11:10 AM
1. ~~**`run_all.sh` lines 70, 82**~~ - ✅ FIXED (venv paths corrected)
2. ~~**`com.era.admin.fathom.run.plist` lines 19-21**~~ - ✅ FIXED (log paths corrected)
3. **`scripts/monitor_fathom.sh` line 68** - ❌ UNFIXED - Tries to run `scripts/run_all.sh` (doesn't exist!)
   - Should be: `PROJECT_ROOT/run_all.sh` (parent directory)
   - This is why launchd crashes immediately

### MEDIUM (Breaks Manual Tools) 
4. ~~**`refresh_fathom_auth.sh` line 15**~~ - ✅ FIXED (venv path corrected)

### LOW (Documentation Only)
5. **`CONTEXT_RECOVERY.md` line 13** - Location outdated
6. **`DEVELOPMENT.md` line 31** - Venv location outdated

---

## Next Step: Write Recovery Plan
