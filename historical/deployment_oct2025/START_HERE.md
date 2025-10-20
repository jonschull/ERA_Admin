# Welcome to ERA Admin - Fresh Deployment

**You are:** A new AI assistant in a fresh Windsurf session  
**Location:** `/Users/admin/ERA_Admin/` (outside cloud sync)  
**Date:** October 18, 2025  
**Status:** Directory just created - needs deployment from Dropbox backup

---

## 🎯 Your Immediate Context

### What Happened Before You
The human (Jon) just worked with another AI to:
1. Fix FathomInventory automation issues after a move
2. Update documentation with human-captain/AI-crew philosophy
3. Discover that Dropbox file-locking breaks Git and automation
4. **Decision:** Move ERA_Admin outside cloud sync entirely

### What Needs to Happen Now
**Deploy ERA_Admin from Dropbox backup to this location**

---

## 📋 Deployment Checklist

### Step 1: Read the Plan
```bash
# View the full deployment plan from Dropbox backup
cat ~/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon\ Schull/CascadeProjects/ERA_Admin/DEPLOYMENT_PLAN.md
```

**Key sections:**
- Phase 2: Clone & Deploy (what to do now)
- Success criteria (how to validate)

### Step 2: Clone FathomInventory
```bash
cd /Users/admin/ERA_Admin
git clone https://github.com/jonschull/ERA_fathom_inventory.git FathomInventory

# Use PR branch with enhanced logging
cd FathomInventory
git fetch origin refactor/docs-and-logging-oct2025
git checkout refactor/docs-and-logging-oct2025
```

### Step 3: Copy Non-Git Files
**Credentials (NEVER commit these):**
```bash
DROPBOX_PATH="~/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon Schull/CascadeProjects/ERA_Admin"

cp "$DROPBOX_PATH/FathomInventory/credentials.json" FathomInventory/
cp "$DROPBOX_PATH/FathomInventory/token.json" FathomInventory/
cp "$DROPBOX_PATH/FathomInventory"/fathom_cookies*.json FathomInventory/
```

**Database (296 MB - takes a minute):**
```bash
cp "$DROPBOX_PATH/FathomInventory/fathom_emails.db" FathomInventory/
```

### Step 4: Copy Other Components
```bash
cd /Users/admin/ERA_Admin

cp -r "$DROPBOX_PATH/airtable" .
cp -r "$DROPBOX_PATH/integration_scripts" .
cp -r "$DROPBOX_PATH/tests" .
cp -r "$DROPBOX_PATH/historical" .
cp "$DROPBOX_PATH"/*.md .
cp "$DROPBOX_PATH/era_config.py" .
cp "$DROPBOX_PATH/requirements.txt" .
cp "$DROPBOX_PATH/.gitignore" .
```

### Step 5: Validate Paths
```bash
cd /Users/admin/ERA_Admin
python3 era_config.py
# Should show all paths exist
```

### Step 6: Test FathomInventory
```bash
cd /Users/admin/ERA_Admin/FathomInventory
./run_all.sh
# Watch for enhanced logging: "(X new calls)" etc.
```

### Step 7: Update Launchd
```bash
# Update plist to point here
sed -i '' 's|/Users/admin/Library/CloudStorage.*ERA_Admin|/Users/admin/ERA_Admin|g' \
   ~/Library/LaunchAgents/com.era.admin.fathom.run.plist

# Reload
launchctl unload ~/Library/LaunchAgents/com.era.admin.fathom.run.plist
launchctl load ~/Library/LaunchAgents/com.era.admin.fathom.run.plist
```

---

## 🧭 Your Role (Read This)

**The human is the captain.** You are advisor and crew.

### DO:
- ✅ Ask "Should I proceed with Step X?" before each major action
- ✅ Read existing docs (DEPLOYMENT_PLAN.md, README.md) before explaining
- ✅ Test your work, show results, ask for validation
- ✅ Point human to docs: "See DEPLOYMENT_PLAN.md Phase 2"

### DON'T:
- ❌ Assume what human wants - ask
- ❌ Explain what's already documented - point to docs
- ❌ Declare "done" without validation
- ❌ Make decisions without approval

**Why this matters:** Humans read README then forget. Your job is navigation, not re-explanation.

---

## 📚 Key Documents (After Deployment)

Once components are copied, read these **in order:**

1. **README.md** - System overview, quick start
2. **AI_HANDOFF_GUIDE.md** - Your role and conventions in detail
3. **CONTEXT_RECOVERY.md** - Current state of the project
4. **DEPLOYMENT_PLAN.md** - What we're doing right now

---

## ⚠️ Important Notes

### About Git
- **FathomInventory** is a Git submodule (already has repo)
- **ERA_Landscape_Static** is separate (different location)
- **ERA_Admin** (this folder) will become Git repo after deployment
- Don't try to Git anything until files are copied

### About Dropbox Backup
- **Location:** `~/Library/CloudStorage/Dropbox-.../ERA_Admin/`
- **Status:** Kept as backup until this deployment is validated
- **Don't delete** until human confirms new location works (1+ week)

### About Virtual Environment
- **Location:** `/Users/admin/ERA_Admin_venv/` (already exists, outside this folder)
- Shared by all components
- Already has all required packages

---

## 🎓 Quick Orientation

**What is ERA Admin?**
Integration hub connecting 4 ERA data systems:
1. Google Docs Agendas (manual notes)
2. Airtable (membership database)
3. FathomInventory (automated meeting analysis)
4. ERA Landscape (network visualization)

**Why the move?**
Dropbox file-locking breaks automation. Python scripts fail with "Resource deadlock" during launchd execution.

**What's the goal?**
Get FathomInventory automation working reliably at 10 AM daily.

---

## 🚀 Ready to Start?

**First Question to Ask Human:**
"Should I proceed with Step 2: Clone FathomInventory from GitHub?"

Then work through checklist, asking approval at each major step.

---

**This Document:** `/Users/admin/ERA_Admin/START_HERE.md`  
**Created:** October 18, 2025 3:15 PM  
**For:** Fresh AI assistant after Windsurf restart  
**Status:** Ready for deployment
