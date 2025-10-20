# Phase 4B: Fathom-Airtable Reconciliation System

**Complete workflow for enriching Fathom participant data with Airtable member information.**

---

## Overview

This system matches Fathom video participants to Airtable members, enriches Fathom records with authoritative data, and manages unmatched/problematic entries.

**Key Principle:** Airtable is ground truth. Fathom has AI-generated names (often misspelled). This system corrects Fathom to match Airtable.

---

## Components

### **Phase 4B-1: Match & Enrich**
**Script:** `phase4b1_enrich_from_airtable.py`

**Purpose:** Fuzzy match Fathom → Airtable, get human approval, enrich database

**Features:**
- Fuzzy matching (80% threshold) using multiple algorithms
- Enhanced HTML approval interface with sortable columns, CSV export
- Skips already-enriched participants (prevents re-matching)
- Deletes "drop" entries from Fathom
- Updates Fathom with Airtable data (name, email, member/donor status)

**Workflow:**
1. Load Fathom participants (skip if `validated_by_airtable = 1`)
2. Load Airtable people from CSV export
3. Fuzzy match unenriched participants
4. Generate interactive HTML approval table
5. User reviews, checks boxes, adds comments, exports CSV
6. Script processes CSV:
   - Deletes entries marked "drop"
   - Enriches approved matches
   - Sets `validated_by_airtable = 1`

**Key Files:**
- Input: `/Users/admin/ERA_Admin/airtable/people_export.csv`
- Database: `/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db`
- Output: `phase4b1_APPROVALS_YYYYMMDD_HHMM.html`
- CSV: User exports from HTML interface

---

### **Phase 4B-2: Review Unmatched** (TBD)
**Purpose:** Handle participants that didn't match at 80% threshold

**Categories:**
1. Organizations (delete)
2. Phone numbers (delete)
3. Duplicates/variants (merge)
4. Low-score matches (manual review)
5. Not in Airtable (add to Airtable or ignore)

---

### **Phase 4B-3: Add Airtable-Only People** (TBD)
**Purpose:** Insert Airtable members who aren't in Fathom yet

---

## Database Schema

### Fathom `participants` Table - Enrichment Columns

Added by `add_enrichment_columns()`:

| Column | Type | Purpose |
|--------|------|---------|
| `validated_by_airtable` | BOOLEAN | 1 = enriched, prevents re-matching |
| `era_member` | BOOLEAN | 1 = Airtable member |
| `is_donor` | BOOLEAN | 1 = Airtable donor |
| `email` | TEXT | From Airtable |
| `airtable_id` | TEXT | Airtable record ID |
| `projects` | TEXT | Airtable projects |
| `data_source` | TEXT | 'both' after enrichment |
| `landscape_node_id` | TEXT | For future use |

**Note:** `name` field gets updated to Airtable spelling (corrects AI errors)

---

## Comment Terminology (Approval Interface)

Users can add these keywords in the Comments column:

| Term | Meaning |
|------|---------|
| `drop` | Remove from Fathom database (bad match/contamination) |
| `Correct Name` | Real name to associate with Airtable entry |
| `email@example.com` | Correct email to use |
| `needs reunion` | Multiple accounts need merging/contact |
| `add to airtable` | Person in Fathom but not Airtable, create entry |
| `investigate` | Needs manual research |

Comments are free-form - these are recommendations.

---

## Results (As of 2025-10-19)

### **Session 1: Initial Enrichment**

**Input:**
- 651 unique Fathom participants
- 592 Airtable people

**Fuzzy Matching:**
- 426 matched at ≥80% threshold
- 225 below threshold (Phase 4B-2)

**User Review:**
- 363 approved
- 63 rejected
- 1 manual match added (Rolanda → Ansima Casinga Rolande)

**Actions Taken:**
- **Deleted 9 participants** (11 records):
  - Abdulganiyu Jimoh (4 variants)
  - Nikko, admin, Brendah, Bianca, Julia

- **Enriched 364 participants** (1229 records):
  - 188 names corrected (AI → Airtable)
  - 351 members identified
  - 64 donors identified
  - 360 emails added

**Current State:**
- 527 unique participants remain (down from 651)
- 248 validated (enriched)
- 279 unenriched (53 rejected + 226 never matched)

---

## Usage

### **First Run (Generate Approval Table)**

```bash
cd /Users/admin/ERA_Admin
/Users/admin/ERA_Admin_venv/bin/python3 integration_scripts/phase4b1_enrich_from_airtable.py
```

**Opens HTML table in browser automatically.**

### **Review & Export**

1. Open `phase4b1_APPROVALS_*.html` in browser
2. Click video links (🎥) to verify identities
3. Check/uncheck ☑ boxes to approve/reject
4. Add comments for special cases
5. Click column headers to sort
6. Click "📥 Export to CSV" button
7. Save CSV file

### **Process Approved Matches**

**Option A: Use specialized script (recommended for batch processing):**

Edit `process_approved_matches.py`:
- Update `CSV_PATH`
- Update `DROP_NAMES` list
- Update `MANUAL_MATCHES` dict

```bash
/Users/admin/ERA_Admin_venv/bin/python3 integration_scripts/process_approved_matches.py
```

**Option B: Re-run main script with CSV:**

(Future enhancement - parse CSV from command line)

---

## Safety Features

### **Automatic Backups**

Before any database modifications:
- Full DB backup: `fathom_emails.backup_YYYYMMDD_HHMM.db`
- CSV export: `fathom_tables_YYYYMMDD_HHMM.zip`
- Integrity check before and after
- Location: `/Users/admin/ERA_Admin/FathomInventory/backups/`

### **Transaction Rollback**

All modifications use transactions:
```python
try:
    conn.execute("BEGIN TRANSACTION")
    # ... modifications ...
    conn.commit()
except:
    conn.rollback()  # Undo everything
```

### **Skip Already-Enriched**

Participants with `validated_by_airtable = 1` are automatically excluded from future fuzzy matching. Prevents:
- Duplicate processing
- Wasted review time
- Re-showing already-approved matches

---

## Files & Locations

### **Scripts**
- `phase4b1_enrich_from_airtable.py` - Main enrichment script
- `process_approved_matches.py` - Batch processor for CSV approvals
- `generate_improved_approval_table.py` - Standalone HTML generator (deprecated)

### **Data**
- Airtable export: `/Users/admin/ERA_Admin/airtable/people_export.csv`
- Fathom DB: `/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db`
- Backups: `/Users/admin/ERA_Admin/FathomInventory/backups/`

### **Outputs**
- Approval tables: `phase4b1_APPROVALS_*.html`
- Exported CSVs: User's Downloads folder
- Reports: `phase4b1_enrichment_report.md` (future)

### **Documentation**
- This README: `integration_scripts/README_PHASE4B.md`
- Summary: `integration_scripts/PHASE4B1_ENHANCEMENTS_SUMMARY.md`
- Email draft: `integration_scripts/needs_reunion_email.md`

---

## Future Enhancements

### **Phase 4B-2 (Next)**
1. Generate approval table for <80% matches
2. Enhanced Gmail API lookup for research
3. Categorize: delete, merge, add-to-airtable, ignore

### **Phase 4B-3**
1. Identify Airtable-only people (not in Fathom)
2. Insert into Fathom as potential contacts

### **Automation**
1. Command-line CSV processing (no manual script editing)
2. Batch operations from comment keywords
3. Auto-generate follow-up emails

---

## Troubleshooting

### **"No matches found" after enrichment**

✅ **Expected!** Script skips `validated_by_airtable = 1` participants. 

Run only shows new/unenriched people. To verify:

```sql
SELECT COUNT(DISTINCT name) FROM participants WHERE validated_by_airtable = 1;
```

### **Need to re-process someone**

Set `validated_by_airtable = 0` for that person:

```sql
UPDATE participants SET validated_by_airtable = 0 WHERE name = 'Person Name';
```

### **Restore from backup**

```bash
cp /Users/admin/ERA_Admin/FathomInventory/backups/fathom_emails.backup_YYYYMMDD_HHMM.db \
   /Users/admin/ERA_Admin/FathomInventory/fathom_emails.db
```

---

## Dependencies

- Python 3.8+
- `fuzzywuzzy` (fuzzy string matching)
- `python-Levenshtein` (faster fuzzy matching)
- SQLite3 (built-in)

Install:
```bash
pip install fuzzywuzzy python-Levenshtein
```

---

**Last Updated:** 2025-10-19  
**Author:** Jon Schull & Claude  
**Status:** Phase 4B-1 Complete ✅ | Phase 4B-2 Next ➡️
