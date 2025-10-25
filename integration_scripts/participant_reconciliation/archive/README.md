# Archive Directory

**Purpose:** Historical files from Phase 4B development and execution

---

## Directory Structure

```
archive/
├── early_rounds/      # Rounds 1-3 execution scripts (prototypes)
├── rounds_4_8/        # Rounds 4-8 execution scripts (production pattern)
├── test_outputs/      # 22 TEST HTML files from development
├── csv_exports/       # 9 CSV exports from review sessions
├── docs/              # Obsolete documentation superseded by current docs
└── dev_scripts/       # Test scripts and development artifacts
```

---

## What's Archived

### **Execution Scripts**

**`early_rounds/`** - Rounds 1-3 (Oct 20, 2025)
- Prototype execution scripts
- Evolved into production pattern
- See README in folder for details

**`rounds_4_8/`** - Rounds 4-8 (Oct 20, 2025)
- Production pattern scripts
- 125 people processed
- Use `execute_round8_actions.py` as template for new rounds

### **Data Files**

**`test_outputs/`** - Test HTML files
- 22 files generated during development
- Not used for actual reviews
- Development artifacts only

**`csv_exports/`** - Review session exports
- 9 CSV files from Rounds 1-8
- Human decisions recorded
- Audit trail of actions taken

### **Documentation**

**`docs/`** - Superseded documentation
- Early planning docs
- Status snapshots from development
- Replaced by current comprehensive docs

### **Development**

**`dev_scripts/`** - Test & experimental scripts
- Unit tests
- Probe functionality experiments
- Development notes

---

## Why Archive?

Following the principle: **Clean root directory, preserve history**

Benefits:
- ✅ Root directory uncluttered (17 files vs 67)
- ✅ Historical context preserved
- ✅ Easy to find active vs historical files
- ✅ Clear documentation of what moved where

---

## Active Files (in ../)

**Production Scripts:**
- `phase4b1_enrich_from_airtable.py` - Phase 4B-1 workflow
- `generate_batch_data.py` - Select next batch
- `generate_phase4b2_table.py` - Create review HTML
- `parse_phase4b2_csv.py` - Parse decisions
- `add_to_airtable.py` - Add people module
- `gmail_research.py` - Gmail research tool

**Documentation:**
- `README.md` - Main overview
- `README_PHASE4B.md` - Phase 4B system guide
- `AI_WORKFLOW_GUIDE.md` - Workflow for naive AI
- `PHASE4B2_PROGRESS_REPORT.md` - 8-round analysis

**Configuration:**
- `credentials.json` - OAuth credentials
- `token_jschull.json` - Gmail API token
- `TEMPLATE_database_script.py` - Script template

---

**Created:** 2025-10-20  
**Purpose:** Organize Phase 4B files - keep root clean while preserving history  
**Impact:** 67 files → 17 active + 50 archived
