# integration_scripts

---

## 1. Overview and Context Recovery

integration_scripts is one of three components in ERA_Admin.

**Purpose:** Cross-component bridging for participant enrichment

**What it does:**
Bridges FathomInventory ↔ Airtable to enrich participant data

**Phases:**

- **Phase 4B-1:** Automated fuzzy matching (✅ Complete - 364 enriched)
- **Phase 4B-2:** Collaborative human-AI review (✅ 87% complete - 409 enriched)

**Current Progress:**
- Round 8 complete
- 1,698/1,953 participants validated (87%)
- 255 remaining

---

## 2. Orientation

**Path:** [/README.md](../README.md) → **integration_scripts**

**When to use:**
- Working on Phase 4B-2 collaborative review
- Understanding participant enrichment workflow
- Bridging FathomInventory and Airtable data

**Multiple READMEs in this directory:**

- **This file (README.md):** Overview of integration scripts
- **README_PHASE4B.md:** Phase 4B system details
- **README_PHASE4B_DETAILED.md:** Deep technical details

**Choose based on need:**
- Quick overview → This file
- System understanding → README_PHASE4B.md
- Implementation details → README_PHASE4B_DETAILED.md

---

## 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)

**integration_scripts-specific:**

1. **Collaborative Human-AI Workflow**
   - 6-phase cycle for data curation
   - Human has final approval on all matches
   - See [AI_WORKFLOW_GUIDE.md](AI_WORKFLOW_GUIDE.md) for details
   - See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) for human-AI philosophy

2. **Data Validation**
   - Fuzzy matching with human verification
   - Clear approval tracking
   - Batch processing for efficiency

3. **Progress Tracking**
   - Detailed round-by-round analysis
   - See PHASE4B2_PROGRESS_REPORT.md

---

## 4. Specialized Topics

### AI Workflow

- [AI_WORKFLOW_GUIDE.md](AI_WORKFLOW_GUIDE.md) - Phase 4B-2 collaborative process
  - Part of [/AI_HANDOFF_GUIDE.md](../AI_HANDOFF_GUIDE.md) system
  - Specialized for Phase 4B-2 6-phase workflow

### Progress & Analysis

- PHASE4B2_PROGRESS_REPORT.md - 8-round detailed analysis
- Round-by-round metrics and insights

### Scripts

- generate_phase4b2_table.py - Generate review tables
- process_approved_matches.py - Process human approvals
- add_to_airtable.py - Add validated participants to Airtable

### Archive

- archive/ - Historical scripts, test outputs, early rounds
  - See archive/README.md for organization

### Related

**Components:**
- [../FathomInventory/](../FathomInventory/) - Source of participant data
- [../airtable/](../airtable/) - Target for enriched data

**AI Guidance:**
- [/AI_HANDOFF_GUIDE.md](../AI_HANDOFF_GUIDE.md) - General AI workflow
- [AI_WORKFLOW_GUIDE.md](AI_WORKFLOW_GUIDE.md) - Phase 4B-2 specific

**Back to:** [Main README](../README.md)
