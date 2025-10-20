# ERA_Admin Test Suite

Tests for the FathomInventory move recovery and ongoing system health.

## Test Structure

### Component Tests (Run First)
These verify individual components without triggering full runs:

1. **`test_venv.py`** - Virtual environment setup
   - Venv exists at `/Users/admin/ERA_Admin_venv`
   - Python executable works
   - Required packages installed (fuzzywuzzy, playwright, etc.)

2. **`test_fathom_paths.py`** - File system paths
   - FathomInventory directory accessible
   - Database file exists and not corrupted
   - Scripts exist and are executable
   - Authentication files present

3. **`test_era_config.py`** - Configuration system
   - era_config.py imports correctly
   - All paths resolve
   - Fathom DB path correct

4. **`test_recent_logs.py`** - Log analysis
   - **Detects crash loops** (monitor failing repeatedly)
   - **Verifies recent successful run** (within 24h)
   - **Catches silent failures** (marked success but had errors)

### Execution Tests (Run After Components Pass)

5. **`test_launchd_execution.py`** - Live launchd test
   - Launchd job loaded
   - Monitor not in crash loop
   - **Triggers launchd job** and verifies it doesn't crash
   - Tests actual automation execution

### Full System Test

6. **`test_all.py`** - End-to-end system test
   - Runs all component tests
   - Runs full `run_all.sh` (5-10 minutes)
   - Verifies complete FathomInventory workflow

## Usage

### Quick Component Test
```bash
cd ERA_Admin
python3 tests/test_component_tests.py
```

### Test Launchd Execution (Safe - triggers one run)
```bash
python3 tests/test_launchd_execution.py
```

### Full System Test (5-10 minutes)
```bash
python3 tests/test_all.py
```

### Individual Test
```bash
python3 tests/test_venv.py
python3 tests/test_recent_logs.py
```

## What Gets Caught

### ❌ Things These Tests WILL Catch:
- Missing or broken virtual environment
- Wrong venv paths in scripts
- Database corruption or missing
- Scripts not executable
- **Launchd crash loops** (NEW)
- **Silent failures** (marked success but failed) (NEW)
- **Stale system** (no run in 24h) (NEW)
- Full system execution failures

### ✅ Things Verified:
- All paths resolve correctly
- Venv has required packages
- Scripts can execute
- Recent successful runs
- Launchd can trigger jobs
- Complete workflow works end-to-end

## Test Philosophy

**"Silence is not success"** - Tests actively verify execution, not just file existence.

Tests are designed to:
1. Fail loudly when something is broken
2. Detect crash loops and silent failures
3. Verify actual execution, not just configuration
4. Provide clear error messages for debugging

## Adding New Tests

When adding tests:
1. Make them fail if the system is broken (not just pass if files exist)
2. Check logs for actual execution results
3. Verify end-to-end workflows, not just components
4. Add to `test_component_tests.py` if it's a pre-flight check
5. Update this README with what the test catches
