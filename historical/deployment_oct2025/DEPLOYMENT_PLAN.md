# ERA Admin - Git Deployment Plan

**Goal:** Move ERA_Admin outside Dropbox to `/Users/admin/ERA_Admin/` for reliable automation  
**Status:** In Progress - Phase 1 Complete  
**Date:** October 18, 2025

---

## Why This Move?

**Problem:** Dropbox file-locking breaks launchd automation
- FathomInventory automation fails with "Resource deadlock avoided"
- Python imports fail during daemon execution
- Venv outside Dropbox not enough - scripts must be outside too

**Solution:** Git-based deployment outside all cloud sync

---

## ✅ Phase 1: Documentation & PR (COMPLETE)

### Completed:
1. ✅ **FathomInventory reorganization** - PR #21 created
   - Moved historical docs to `historical/analysis_2024_2025/`
   - Enhanced logging (count reporting for calls/emails/analyses)
   - Fixed bash compatibility issues
   - https://github.com/jonschull/ERA_fathom_inventory/pull/21

2. ✅ **Updated ERA_Admin docs**
   - README.md - Human-captain/AI-crew philosophy
   - AI_HANDOFF_GUIDE.md - Advisor/crew role model
   - CONTEXT_RECOVERY.md - Role-based navigation
   - All saved to Dropbox (backed up)

3. ✅ **Recovery documentation**
   - `historical/move_recovery_oct2025/README.md` - Full move history
   - All recovery docs archived

### Blocked (Skip):
- ❌ ERA_Admin Git init in Dropbox - Dropbox locks prevent it
- **Decision:** Skip Git-in-Dropbox, go straight to deployment

---

## 🎯 Phase 2: Clone & Deploy (NEXT - After Restart)

### Step 2.1: Create Production Location
```bash
cd /Users/admin

# Clone FathomInventory
git clone https://github.com/jonschull/ERA_fathom_inventory.git ERA_Admin/FathomInventory

# Checkout PR branch to test enhanced logging
cd ERA_Admin/FathomInventory
git fetch origin refactor/docs-and-logging-oct2025
git checkout refactor/docs-and-logging-oct2025
```

### Step 2.2: Copy Non-Git Files
```bash
# Credentials (NEVER in Git)
cp ~/Library/CloudStorage/.../ERA_Admin/FathomInventory/credentials.json \
   /Users/admin/ERA_Admin/FathomInventory/

cp ~/Library/CloudStorage/.../ERA_Admin/FathomInventory/token.json \
   /Users/admin/ERA_Admin/FathomInventory/

cp ~/Library/CloudStorage/.../ERA_Admin/FathomInventory/fathom_cookies*.json \
   /Users/admin/ERA_Admin/FathomInventory/

# Database (296 MB)
cp ~/Library/CloudStorage/.../ERA_Admin/FathomInventory/fathom_emails.db \
   /Users/admin/ERA_Admin/FathomInventory/
```

### Step 2.3: Copy Other Components
```bash
cd /Users/admin/ERA_Admin

# Copy integration components
cp -r ~/Library/CloudStorage/.../ERA_Admin/airtable .
cp -r ~/Library/CloudStorage/.../ERA_Admin/integration_scripts .
cp -r ~/Library/CloudStorage/.../ERA_Admin/tests .

# Copy docs
cp ~/Library/CloudStorage/.../ERA_Admin/*.md .
cp ~/Library/CloudStorage/.../ERA_Admin/era_config.py .
cp ~/Library/CloudStorage/.../ERA_Admin/requirements.txt .
cp ~/Library/CloudStorage/.../ERA_Admin/.gitignore .
```

### Step 2.4: Initialize ERA_Admin Git (Outside Dropbox)
```bash
cd /Users/admin/ERA_Admin

# Now safe - no Dropbox interference
git init
git add .
git commit -m "Initial deployment outside cloud sync"

# Create GitHub repo
gh repo create jonschull/ERA_Admin --public
git remote add origin https://github.com/jonschull/ERA_Admin.git
git push -u origin main
```

### Step 2.5: Update launchd
```bash
# Update plist to point to new location
sed -i '' 's|/Users/admin/Library/CloudStorage.*ERA_Admin|/Users/admin/ERA_Admin|g' \
   ~/Library/LaunchAgents/com.era.admin.fathom.run.plist

# Reload
launchctl unload ~/Library/LaunchAgents/com.era.admin.fathom.run.plist
launchctl load ~/Library/LaunchAgents/com.era.admin.fathom.run.plist
```

---

## 🧪 Phase 3: Validation

### Tests to Run:
1. ✅ Verify paths: `python /Users/admin/ERA_Admin/era_config.py`
2. ✅ Test FathomInventory: `cd FathomInventory && ./run_all.sh`
3. ✅ Check launchd: Schedule test run for 10 minutes from now
4. ✅ Verify no Dropbox locks: Check logs for "Resource deadlock"

### Success Criteria:
- [ ] run_all.sh completes all 4 steps
- [ ] Enhanced logging shows counts (X new calls, Y new emails)
- [ ] No "Resource deadlock" errors
- [ ] Launchd automation completes successfully

---

## 📋 Current Status After Restart

**What's Safe:**
- All documentation saved to disk in Dropbox
- FathomInventory PR #21 on GitHub
- Recovery docs in place

**What to Do:**
- Skip fighting Dropbox Git locks
- Go directly to Phase 2 (deployment outside Dropbox)
- Keep Dropbox copy as backup until validated

**Next Action:**
Start Phase 2.1 after restart - clone FathomInventory to `/Users/admin/ERA_Admin/`

---

## 🗂️ Backup Strategy

**Keep Dropbox Copy As:**
- `ERA_Admin_BACKUP_20251018` - Full snapshot before deployment
- Don't delete until new location validated (1 week minimum)

**ERA_Landscape_Static:**
- Remains separate (already has own GitHub repo + Pages deployment)
- Not moving - works fine where it is

---

**Document:** `DEPLOYMENT_PLAN.md`  
**Owner:** Jon Schull  
**Last Updated:** October 18, 2025 3:13 PM
