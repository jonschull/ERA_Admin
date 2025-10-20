# FathomInventory

---

## 1. Overview and Context Recovery

FathomInventory is one of three components in ERA_Admin.

**Purpose:** Automated meeting analysis system

**What it does:**
1. Discovers new Fathom calls from jschull@e-nable.org
2. Shares calls to automated receiver
3. Downloads summary emails with public URLs
4. Processes emails into structured database
5. Reports daily status with health checks

**Current Health:**
- ✅ **1,953 participants** tracked
- ✅ **Automation active** - Daily 3 AM runs via launchd
- ✅ **Enhanced failure detection** - Pre-flight auth checks

**Recent:**
- Oct 20: Monorepo consolidation - absorbed into ERA_Admin
- Oct 20: test_recent_logs.py path fixed

**Status:** ✅ Fully operational

---

## 2. Orientation

**Path:** [/README.md](../README.md) → **FathomInventory**

**When to use:**
- Working on meeting data processing
- Fixing authentication issues
- Understanding participant tracking

**Quick Start:**
```bash
cd ../FathomInventory  # Go to actual component in parent
source ../ERA_Admin_venv/bin/activate
./run_all.sh
```

---

## 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)

**FathomInventory-specific:**

1. **Authentication Health Checks**
   - Test authentication before automation runs
   - Fail fast with clear error messages
   - Cookie expiry handled gracefully
   - See [authentication/](authentication/) for details

2. **Pipeline Reliability**
   - Bash pipeline exit codes properly propagated
   - No silent failures
   - Enhanced daily reports with log analysis

3. **Date Normalization**
   - All dates in ISO format (YYYY-MM-DD)
   - Normalized at all entry points
   - Consistent across database

4. **Testing Approach**
   - Pre-flight checks before operations
   - Daily health checks in reports
   - Integration tests in /tests
   - See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) for testing discipline

---

## 4. Specialized Topics

### Subdirectories

- [authentication/](authentication/) - Cookie/token management
- analysis/ - Participant analysis scripts
- docs/ - Technical documentation
- email_conversion/ - Email to markdown conversion
- scripts/ - Utility scripts
- tests/ - Component tests

### Documentation Files

- [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) - Component-specific context
- BACKUP_AND_RECOVERY.md - Disaster recovery procedures
- DEVELOPMENT.md - Developer workflow
- zoom_fathom_crosscheck_report.md - Data validation report

### Related

**Broader context:**
- [/README.md](../README.md) - Main system overview
- [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) - How we work
- Parent folder's ERA_ECOSYSTEM_PLAN.md - Strategic vision

**Integration:**
- [../integration_scripts/](../integration_scripts/) - Cross-component bridges

**Back to:** [Main README](../README.md)
