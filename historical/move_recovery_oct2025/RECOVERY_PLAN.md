# Recovery Plan - FathomInventory Move to ERA_Admin

**Date:** Oct 18, 2025 10:46 AM  
**Status:** DRAFT - Awaiting Approval  
**Last Successful Automation:** NONE since move (Oct 17 evening)

---

## Verified Timeline

1. **Oct 9, 10:10 AM**: Automation failed (venv Dropbox file-locking issue)
2. **Oct 9-17**: Automation down for ~8 days due to venv issue
3. **Oct 17, evening**: Fixed venv issue, moved FathomInventory into ERA_Admin
4. **Oct 18, 10:00 AM**: Launchd automation attempted but failed (broken paths from move)
5. **Oct 18, 10:00 AM**: Manual run succeeded (36 minutes to complete, 0 new calls)

**Launchd Monitor Evidence:**
- Monitor attempts every 30 minutes since 6:00 AM today
- ALL attempts fail: "❌ Error: Fathom script failed to start or crashed immediately"
- The 10:00 AM successful run in cron.log was MANUAL, not automated

**Evidence:**
- Backup created: `/Users/admin/FathomInventory 17-10-2025.zip` (Oct 17 20:34)
- Wrapper updated: `/Users/admin/.local/bin/run_fathom_daily.sh` (Oct 17 20:36)
- Manual success: `ERA_Admin/FathomInventory/cron.log` (Oct 18 10:36)

---

## Problem Statement

FathomInventory was successfully moved into `ERA_Admin` last night (Oct 17), but hardcoded venv paths in `run_all.sh` still reference the old location `/Users/admin/FathomInventory_venv`. Manual execution works, but launchd automation is broken.

**Root Cause:** Two hardcoded venv paths in `run_all.sh` not updated after folder reorganization.

---

## Impact

- ⚠️ **Automation broken since Oct 17 move** (~12 hours)
- ✅ **Manual execution works** (verified Oct 18 10:36 AM)
- ⚠️ **Cookie refresh tool broken** (venv path issue)
- ℹ️ **Documentation outdated**
- 📊 **No calls missed yet** (manual run this morning succeeded)

---

## Recovery Strategy

### Phase 1: Fix Critical Issues (Restore Automation)
1. Update venv paths in `run_all.sh`
2. Update launchd plist log paths
3. Reload launchd configs

### Phase 2: Fix Manual Tools
4. Update `refresh_fathom_auth.sh` venv path

### Phase 3: Update Documentation
5. Update `CONTEXT_RECOVERY.md` location
6. Update `DEVELOPMENT.md` venv notes

### Phase 4: Test & Validate
7. Run component tests
8. Run full system test (`run_all.sh`)
9. Verify launchd can execute

---

## Detailed Steps

### Step 1: Fix `run_all.sh` venv paths

**File:** `FathomInventory/run_all.sh`

**Line 70 - Change:**
```bash
# OLD
VENV_PATH="/Users/admin/FathomInventory_venv/bin/activate"

# NEW
VENV_PATH="/Users/admin/ERA_Admin_venv/bin/activate"
```

**Line 82 - Change:**
```bash
# OLD
PYTHON="/Users/admin/FathomInventory_venv/bin/python3"

# NEW
PYTHON="/Users/admin/ERA_Admin_venv/bin/python3"
```

---

### Step 2: Fix launchd log paths

**File:** `~/Library/LaunchAgents/com.era.admin.fathom.run.plist`

**Lines 19-21 - Change:**
```xml
<!-- OLD -->
<key>StandardOutPath</key>
<string>/Users/admin/FathomInventory/logs/fathom_run.log</string>
<key>StandardErrorPath</key>
<string>/Users/admin/FathomInventory/logs/fathom_run.log</string>

<!-- NEW -->
<key>StandardOutPath</key>
<string>/Users/admin/Library/Logs/fathom_run.log</string>
<key>StandardErrorPath</key>
<string>/Users/admin/Library/Logs/fathom_run.log</string>
```

---

### Step 3: Reload launchd

```bash
# Unload the old config
launchctl unload ~/Library/LaunchAgents/com.era.admin.fathom.run.plist

# Load the updated config
launchctl load ~/Library/LaunchAgents/com.era.admin.fathom.run.plist

# Verify it's loaded
launchctl list | grep fathom
```

---

### Step 4: Fix `refresh_fathom_auth.sh`

**File:** `FathomInventory/scripts/refresh_fathom_auth.sh`

**Line 15 - Change:**
```bash
# OLD
PYTHON="${PROJECT_ROOT}/venv/bin/python3"

# NEW
PYTHON="/Users/admin/ERA_Admin_venv/bin/python3"
```

---

### Step 5: Update `CONTEXT_RECOVERY.md`

**File:** `FathomInventory/CONTEXT_RECOVERY.md`

**Line 13 - Change:**
```markdown
# OLD
**Location:** `/Users/admin/FathomInventory`

# NEW
**Location:** `/Users/admin/Library/CloudStorage/Dropbox-.../ERA_Admin/FathomInventory`
```

---

### Step 6: Update `DEVELOPMENT.md`

**File:** `FathomInventory/DEVELOPMENT.md`

**Around line 31 - Change:**
```markdown
# OLD
- venv still in Dropbox (causes warnings but works when run manually)

# NEW
- venv moved outside Dropbox to `/Users/admin/ERA_Admin_venv` (shared with ERA_Admin components)
```

---

## Testing Plan

### Pre-Test: Verify venv exists and has dependencies

```bash
# Check venv exists
ls -la /Users/admin/ERA_Admin_venv/bin/python3

# Check fuzzywuzzy installed (for cross_correlate.py)
/Users/admin/ERA_Admin_venv/bin/python3 -c "import fuzzywuzzy; print('OK')"

# Check playwright installed (for FathomInventory)
/Users/admin/ERA_Admin_venv/bin/python3 -c "from playwright.sync_api import sync_playwright; print('OK')"
```

If missing dependencies:
```bash
/Users/admin/ERA_Admin_venv/bin/pip install -r FathomInventory/requirements.txt
/Users/admin/ERA_Admin_venv/bin/playwright install chromium
```

---

### Component Tests (in `ERA_Admin/tests/`)

Create test suite to validate:

#### Test 1: Virtual Environment
- ✓ Venv exists at `/Users/admin/ERA_Admin_venv`
- ✓ Python executable works
- ✓ Required packages installed

#### Test 2: FathomInventory Scripts
- ✓ `run_all.sh` can find venv
- ✓ `run_daily_share.py` runs without error
- ✓ Database accessible at correct path
- ✓ Authentication files accessible

#### Test 3: Airtable Scripts
- ✓ `export_people.py` runs
- ✓ `cross_correlate.py` runs
- ✓ Can access FathomInventory data

#### Test 4: Era Config
- ✓ All paths resolve
- ✓ FathomInventory DB path correct
- ✓ Airtable paths correct

#### Test 5: Launchd Config
- ✓ Wrapper script points to correct location
- ✓ Plist files reference correct paths
- ✓ Log directories exist

---

### Integration Test: Full System Run

```bash
cd ERA_Admin/FathomInventory
./run_all.sh
```

**Expected:** 
- ✅ Script completes without "Resource deadlock" error
- ✅ Venv activates successfully
- ✅ All steps execute (share, wait, download, analyze, report)
- ✅ Logs written to correct location

---

### Final Test: Launchd Execution

```bash
# Manually trigger launchd job
launchctl start com.era.admin.fathom.run

# Wait 2 minutes, then check logs
tail -50 /Users/admin/Library/Logs/fathom_run.log

# Check for success
launchctl list | grep fathom
```

**Expected:**
- ✅ Job runs without "Resource deadlock" error
- ✅ Completes successfully
- ✅ Logs written correctly

---

## Rollback Plan

If recovery fails:

1. **Revert file changes** (git restore)
2. **Check backups** in `FathomInventory/backups/`
3. **Manual run** as temporary workaround:
   ```bash
   cd ERA_Admin/FathomInventory
   /Users/admin/ERA_Admin_venv/bin/python3 run_daily_share.py --use-db
   ```

---

## Success Criteria

- [ ] All component tests pass
- [ ] Full system test (`run_all.sh`) completes successfully  
- [ ] Launchd test executes without errors
- [ ] Documentation updated
- [ ] Next scheduled run (10 AM next day) succeeds automatically

---

## Post-Recovery

1. **Monitor next 3 automated runs** (10 AM daily)
2. **Update ERA_Admin/CONTEXT_RECOVERY.md** with new state
3. **Archive this recovery plan** to `Historical/`
4. **Create memory/note** about venv location for future reference

---

## Questions Before Proceeding

1. **Venv dependencies:** Should I install all FathomInventory requirements in ERA_Admin_venv?
2. **Test location:** Confirm tests go in `ERA_Admin/tests/` (not `ERA_Admin/FathomInventory/tests/`)?
3. **Execution:** Fix critical issues first, then test? Or write tests first?

---

**Status:** ⏸️ AWAITING APPROVAL TO PROCEED
