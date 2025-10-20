# Recovery Guide

This document describes how to safely revert changes and restore the working local system if anything goes wrong during GitHub setup or future refactors.

## Local backups
- Backups are stored under `backups/backup_pre_github_YYYYMMDD_HHMMSS/`
- Structure:
  - `code/` – Python, shell scripts, plist, and docs
  - `data/` – `all_fathom_calls.tsv`, `fathom_emails.db`, `fathom_cookies.json`, `credentials.json`, `token.json`
  - `logs/` – `cron.log`, `monitor.log`, `catch_up_run.log`
  - `manifest.txt`, `python_version.txt`, `pip_freeze.txt`

## Quick local rollback (Git)
1. Ensure the repo has an annotated tag for the baseline (e.g., `v0.1.0-local-baseline`).
2. To revert the working directory to the baseline:
   ```bash
   git fetch --all --tags
   git checkout main
   git reset --hard v0.1.0-local-baseline
   ```
3. To recover a specific file from the baseline tag:
   ```bash
   git checkout v0.1.0-local-baseline -- path/to/file
   ```

## Restore from backup snapshot
If Git is unavailable or the repo becomes corrupted:
```bash
# Replace <STAMP> with the actual timestamp
cp -a backups/backup_pre_github_<STAMP>/code/. .
cp -a backups/backup_pre_github_<STAMP>/data/. .
cp -a backups/backup_pre_github_<STAMP>/logs/. .
```

## GitHub PR rollback
If a PR merged causes issues:
- Use GitHub UI "Revert" to create a rollback PR, or
- Locally:
  ```bash
  # Revert the merge commit
  git revert -m 1 <merge_commit_sha>
  git push origin main
  ```

## Operational safety
- Do not delete or rename `all_fathom_calls.tsv` or `fathom_emails.db` without a verified backup.
- Do not modify `com.fathominventory.run.plist` or `run_all.sh` without review.
- Keep secrets (`fathom_cookies.json`, `credentials.json`, `token.json`) out of Git.

## Verification checklist after recovery
- `./run_all.sh` completes successfully.
- `cron.log` shows expected daily run entries.
- `all_fathom_calls.tsv` and `fathom_emails.db` record counts are unchanged from the last healthy state.
