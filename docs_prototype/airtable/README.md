# airtable

---

## 1. Overview and Context Recovery

airtable is one of three components in ERA_Admin.

**Purpose:** Manual membership tracking and exports

**What it does:**
- Manual database of ERA members and donors
- Export data for cross-correlation with FathomInventory
- Ground truth for member/donor status

**Current Data:**
- **630 people** tracked
- **17 Town Hall attendance columns**
- **Recent:** +58 people added from Phase 4B-2 (Oct 20)

**Status:** ✅ Exports operational

---

## 2. Orientation

**Path:** [/README.md](../README.md) → **airtable**

**When to use:**
- Exporting membership data
- Adding new members/donors
- Checking member status

**Quick Start:**
```bash
cd ../airtable  # Go to actual component in parent
python3 export_people.py
```

---

## 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)

**airtable-specific:**

1. **Manual Data Entry**
   - Human-curated membership database
   - Ground truth for member/donor status
   - Cross-referenced with automated systems (FathomInventory)

2. **Export Hygiene**
   - Regular exports for integration
   - Timestamped export files
   - See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) for testing approach

3. **Configuration Security**
   - API keys in config.py (gitignored)
   - Template provided: config.py.template
   - See SAFETY_NOTICE.md for guidelines
   - See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) for secret management

---

## 4. Specialized Topics

### Files

- config.py.template - Configuration template
- export_people.py - Main export script
- SAFETY_NOTICE.md - Security guidelines
- people_export.csv - Latest export (gitignored)
- airtable_summary.txt - Export metadata

### Related

**Integration:**
- [../integration_scripts/](../integration_scripts/) - Phase 4B-2 workflow uses airtable data

**Principles:**
- [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) - Security, testing, documentation

**Back to:** [Main README](../README.md)
