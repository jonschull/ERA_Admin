# Context Recovery Guide

**Purpose:** Enable any AI (or human) to quickly understand the project state and resume work.

---

## Project Overview

**Goal:** Migrate Fathom call tracking from TSV file to SQLite database while maintaining zero downtime and full reversibility.

**Repo:** `https://github.com/jonschull/ERA_fathom_inventory` (private)

**Current Production System:**
- Automated daily job (10:00 AM via macOS launchd)
- Scrapes new Fathom calls, shares them to email, processes responses
- Data: `all_fathom_calls.tsv` (1594 calls), `fathom_emails.db` (1588 emails)
- Location: `/Users/admin/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon Schull/CascadeProjects/ERA_Admin/FathomInventory`

---

## Where We Are (Oct 5, 2025)

**✅ Completed:**
- Phase 0: GitHub repo, CI, baseline backup (`v0.1.0-local-baseline`)
- Phase 1: Refactored into clean modules (no behavior change)
- Phase 2: Added DB migration tools (not yet integrated)
- Root directory cleanup (docs → `docs/`, scripts → `scripts/`)

**🚀 Next:**
- Add feature-flagged `--use-db` mode to orchestrator
- Test DB mode on copy of database
- Parallel run both TSV and DB modes for validation

**📊 Status:**
- 6 PRs merged (all phases 0–2)
- Production system unchanged, running on `main` branch
- All tests passing (4/4), CI green

---

## Key Files (Quick Reference)

### Documentation (START HERE)
- **`docs/planning/IMPLEMENTATION_STATUS.md`** - Authoritative plan, phase status, PR history
- **`docs/planning/eliminate_tsv_plan.md`** - Original plan (superseded, kept for reference)
- **`README.md`** - User guide for production system
- **`DEVELOPMENT.md`** - Developer setup

### Production Code
- **`run_daily_share.py`** - Current orchestrator (TSV-based)
- **`run_all.sh`** - Called by launchd, orchestrates full pipeline
- **`com.fathominventory.run.plist`** - Scheduler config

### New Modules (Phase 1)
- **`fathom_ops/browser.py`** - Cookie sanitizer, HTML harvester
- **`fathom_ops/parser.py`** - Call extraction from HTML
- **`fathom_ops/share.py`** - Sharing wrapper
- **`data_access/tsv_io.py`** - TSV read/write utilities
- **`scripts/run_daily_share_v2.py`** - New orchestrator (not yet feature-complete)

### DB Migration Tools (Phase 2)
- **`scripts/migration_create_calls_table.sql`** - Creates standalone `calls` table
- **`scripts/import_tsv_to_calls.py`** - Idempotent TSV → DB importer

### Tests
- **`tests/test_parser_unit.py`** - Parser extraction tests
- **`tests/test_browser_sanitize.py`** - Cookie sanitizer test
- **`tests/test_smoke.py`** - Smoke test placeholder

### Safety
- **`backups/backup_pre_github_20251004_122809/`** - Full local snapshot
- **Tag:** `v0.1.0-local-baseline` - Git rollback point

---

## System Architecture (Current)

```
Daily Automation (10:00 AM):
  run_all.sh
    → run_daily_share.py (TSV-based)
      → Scrape Fathom for new calls
      → Share via fathom_ops/share.py → scripts/share_fathom_call2.py
      → Update all_fathom_calls.tsv
    → 5 minute wait
    → scripts/download_emails.py
      → Fetch Gmail responses
      → Parse and insert into fathom_emails.db
```

**Data Files (gitignored):**
- `all_fathom_calls.tsv` - 1594 calls (TSV = current source of truth)
- `fathom_emails.db` - 1588 emails (SQLite)
- `fathom_cookies.json` - Auth for Fathom.video
- `credentials.json`, `token.json` - Gmail OAuth

---

## How to Resume Work

### 1. Verify Local State
```bash
cd /Users/admin/Library/.../FathomInventory
git status
git log --oneline -5
python -m pytest tests/ -q
```

Expected: on `main` branch, clean working tree, 4 tests passing.

### 2. Review Current Plan
Read: `docs/planning/IMPLEMENTATION_STATUS.md`

### 3. Next Implementation Step
Create feature-flagged DB mode:
- Open: `scripts/run_daily_share_v2.py`
- Add: `--use-db` CLI argument
- If set: use `data_access/db_io.py` (create this) to read/write `calls` table
- If not set: use existing `data_access/tsv_io.py` (default)

### 4. Testing Before PR
```bash
# Create test DB copy
cp fathom_emails.db fathom_emails.db.test

# Apply migration
sqlite3 fathom_emails.db.test < scripts/migration_create_calls_table.sql

# Import historical data
python scripts/import_tsv_to_calls.py --db fathom_emails.db.test

# Test new mode (dry run, no real shares)
python scripts/run_daily_share_v2.py --use-db --db fathom_emails.db.test --dry-run
```

### 5. Open PR
```bash
git checkout -b phase3-db-mode
git add [files]
git commit -m "feat(db): add feature-flagged DB mode to orchestrator"
git push -u origin phase3-db-mode
gh pr create -B main -H phase3-db-mode -t "feat(db): feature-flagged DB mode" -b "[description]"
```

---

## Rollback Procedures

### Quick Rollback (Git)
```bash
# Revert last commit
git revert HEAD

# Reset to baseline
git reset --hard v0.1.0-local-baseline
```

### Full Restore (Emergency)
```bash
# Restore all code
cp -r backups/backup_pre_github_20251004_122809/code/* .

# Restore data (if needed)
cp backups/backup_pre_github_20251004_122809/data/all_fathom_calls.tsv .
cp backups/backup_pre_github_20251004_122809/data/fathom_emails.db .
```

---

## Key Principles (Follow These)

1. **PR-driven:** All changes via small, focused PRs
2. **Behavior-preserving:** No functional changes until feature flag
3. **Reversible:** Every step can be undone
4. **Test first:** Validate on copies, never production DB
5. **CI gated:** All PRs must pass tests
6. **TSV remains default:** Until parallel run validates DB mode

---

## Common Commands

### Check scheduled job status
```bash
launchctl list | grep era
```

### View recent logs
```bash
tail -f cron.log
```

### Run tests
```bash
python -m pytest tests/ -v
```

### Check PR status
```bash
gh pr list
gh pr view <number>
```

### Verify DB state (test only)
```bash
sqlite3 fathom_emails.db.test "SELECT COUNT(*) FROM calls;"
sqlite3 fathom_emails.db.test ".schema calls"
```

---

## Contact / Resources

- **User:** Jon Schull
- **Repo:** https://github.com/jonschull/ERA_fathom_inventory
- **Memory tags:** `windsurf`, `github_setup`, `codex`, `preferences`

---

## AI-Specific Recovery Instructions

If you are an AI resuming this work:

1. **Read this file first**, then `docs/planning/IMPLEMENTATION_STATUS.md`
2. **Check git state:** Verify on `main`, all PRs merged, tests passing
3. **Understand the goal:** TSV → DB migration with zero downtime
4. **Follow the principles:** Small PRs, reversible, behavior-preserving
5. **Next concrete step:** Implement `--use-db` flag in `scripts/run_daily_share_v2.py`
6. **Don't assume user approval:** Wait for explicit go-ahead before PRs/merges
7. **Validate proactively:** Test thoroughly before declaring success

**Memory keywords to search:** `windsurf`, `github_setup`, `ERA_fathom_inventory`

---

**Last Updated:** October 5, 2025, 8:10 PM  
**Last AI Session:** Cascade (Windsurf) - Oct 4–5, 2025
