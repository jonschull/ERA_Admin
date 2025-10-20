# Move Recovery - October 2025

**Context:** FathomInventory was moved into ERA_Admin on Oct 17, 2025

**Result:** Successful recovery completed Oct 18, 2025

## Files in This Directory

Investigation and fix documentation from the move recovery:

- `AUDIT_FINDINGS.md` - Initial audit of what broke
- `RECOVERY_PLAN.md` - Step-by-step fix plan
- `RECOVERY_STATUS.md` - Progress tracking
- `CONTRADICTION_CHECK.md` - Investigation of launchd failures
- `MOVE_RECOVERY_PROOF.md` - Evidence-based validation
- `RECOVERY_COMPLETE.md` - Final status summary

## What Broke

1. **Venv paths** - Scripts referenced old standalone venv location
2. **Launchd logs** - Plist pointed to old log directory
3. **Missing dependencies** - New shared venv missing Google API packages
4. **Output capturing** - Command substitution caused hangs in bash

## What Was Fixed

1. Updated all venv paths to `/Users/admin/ERA_Admin_venv`
2. Updated launchd log paths to `/Users/admin/Library/Logs/`
3. Installed FathomInventory requirements in shared venv
4. Fixed bash output capturing to use temp files
5. Enhanced logging to show counts (new calls, new emails, etc.)

## Key Lessons

- **Test venv completeness:** Both paths AND packages must be correct
- **Bash gotchas:** Command substitution with multiple pipes can hang
- **Launchd debugging:** System logs show spawn/exit, but not reasons
- **Validation matters:** Don't assume fixes work - prove with tests

## Test Suite Created

Located in `ERA_Admin/tests/`:
- `test_venv.py` - Validates venv and packages
- `test_fathom_paths.py` - Checks file accessibility
- `test_era_config.py` - Validates configuration
- `test_recent_logs.py` - Detects crash loops
- `test_launchd_execution.py` - Tests launchd jobs
- `test_component_tests.py` - Runs all tests
- `run_all_tests.py` - Full system validation

---

**Moved to historical:** Oct 18, 2025  
**Current system status:** See `ERA_Admin/README.md`
