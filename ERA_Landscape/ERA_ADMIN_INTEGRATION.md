# ERA_Landscape Integration with ERA_Admin

**Date:** October 21, 2025  
**Status:** Integrated as component

---

## Overview

ERA_Landscape is now a **component within ERA_Admin**, integrated into the unified version control system.

**Previous Location:** `/Users/admin/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon Schull/CascadeProjects/ERA_Landscape_Static`  
**Current Location:** `/Users/admin/ERA_Admin/ERA_Landscape/`  
**Upstream Repo:** https://github.com/jonschull/ERA_Landscape_Static

---

## Why Integration?

### Working Principles Alignment

Per ERA_Admin working principles:

1. **Component Independence** - Each component self-contained with clear interfaces
2. **Centralized Configuration** - Paths managed in `era_config.py`
3. **Version Control** - All components under Git for tracking and collaboration
4. **Clear Documentation** - Component README + integration docs

### Integration Benefits

- ✅ **Unified version control** - All ERA systems in one Git repo
- ✅ **Centralized config** - `era_config.py` manages all paths
- ✅ **Simpler deployment** - Single repo to clone/deploy
- ✅ **Cross-component exports** - Direct path references for Fathom → Landscape
- ✅ **Consistent docs** - Same structure as other components

---

## Configuration

### In era_config.py

```python
LANDSCAPE_DIR = ERA_ADMIN_ROOT / "ERA_Landscape"
LANDSCAPE_SHEET_ID = "1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY"
```

### Verify Integration

```bash
cd /Users/admin/ERA_Admin
python3 era_config.py
# Should show: Landscape dir: /Users/admin/ERA_Admin/ERA_Landscape
# Should show: ✅ All paths verified
```

---

## Deployment Notes

### GitHub Pages Deployment

The **live site** remains deployed from the **upstream repo**:
- Live URL: https://jonschull.github.io/ERA_Landscape_Static/
- Deployed from: https://github.com/jonschull/ERA_Landscape_Static

### Workflow for Updates

**Option A: Work in ERA_Admin, push to upstream**
```bash
# Work in ERA_Admin component
cd /Users/admin/ERA_Admin/ERA_Landscape
git checkout -b feat/my-change

# Make changes
code index.html

# Test locally
python3 -m http.server 8000

# Commit to ERA_Admin
cd /Users/admin/ERA_Admin
git add ERA_Landscape/
git commit -m "feat(landscape): Update visualization"
git push origin feat/my-change

# Create PR and merge to ERA_Admin main

# Then push to upstream for deployment
cd ERA_Landscape
git remote add upstream https://github.com/jonschull/ERA_Landscape_Static.git
git push upstream HEAD:feat/my-change
# Create PR in upstream repo
```

**Option B: Sync from upstream periodically**
```bash
cd /Users/admin/ERA_Admin/ERA_Landscape
git remote add upstream https://github.com/jonschull/ERA_Landscape_Static.git
git fetch upstream
git merge upstream/main
cd ..
git add ERA_Landscape/
git commit -m "sync: Pull latest from upstream Landscape repo"
```

---

## Data Flow Integration

### Phase 5T: Fathom → Landscape Export

With ERA_Landscape integrated, export scripts can reference paths directly:

```python
from era_config import Config

# Access Landscape directory
landscape_dir = Config.LANDSCAPE_DIR

# Access Google Sheet
sheet_id = Config.LANDSCAPE_SHEET_ID

# Query Fathom data
db_path = Config.FATHOM_DB_PATH

# Export participants to Landscape
# (See integration_scripts/export_to_landscape.py)
```

---

## Component Status

**Within ERA_Admin:**
- Location: `/Users/admin/ERA_Admin/ERA_Landscape/`
- Version Control: Part of ERA_Admin Git repo
- Configuration: Managed in `era_config.py`
- Documentation: This file + README.md + VISION.md

**Upstream GitHub Pages:**
- Repo: https://github.com/jonschull/ERA_Landscape_Static
- Deployment: GitHub Pages (auto from main branch)
- Live Site: https://jonschull.github.io/ERA_Landscape_Static/

**Schema Documentation:**
- Sheet Structure: `/Users/admin/ERA_Admin/LANDSCAPE_SHEET_SCHEMA.md`
- Integration Plan: `/Users/admin/ERA_Admin/LANDSCAPE_INTEGRATION_PROTOTYPE.md`

---

## References

- **ERA_Admin Root:** [/README.md](../README.md)
- **Integration Scripts:** [/integration_scripts/README.md](../integration_scripts/README.md)
- **Schema Docs:** [/LANDSCAPE_SHEET_SCHEMA.md](../LANDSCAPE_SHEET_SCHEMA.md)
- **Landscape README:** [README.md](README.md)
- **Landscape Vision:** [VISION.md](VISION.md)

---

**Status:** ✅ Integrated  
**Next Steps:** Create export scripts in integration_scripts/ for Fathom → Landscape pipeline
