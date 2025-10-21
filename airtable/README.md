# airtable/README.md

### 1. Overview

**Purpose:** Self-contained Airtable integration for ERA administrative functions

This component provides easy, routine access to the current ERA membership database in Airtable. It is one of four components in ERA_Admin and serves as the **ground truth** for member and donor status.

**What it does:**
- **Manual membership tracking** - 630 people (members and donors)
- **Town Hall attendance** - 17 TH columns, 324 attendance records
- **Export data** - CSV exports for cross-correlation with FathomInventory
- **Ground truth** - Source of truth for member/donor status, contact info
- **Read-only mode** - All scripts export only, no writes to Airtable

**Base Configuration:**
- **Base ID**: `appe7aXupdvB4xXzu`
- **Primary Table**: `People` (membership database)
- **API Access**: Via pyairtable library
- **Security**: READ-ONLY MODE - database modifications disabled

**Current Status:**
- ✅ **630 people** in database (+58 from Phase 4B-2 reconciliation)
- ✅ **17 Town Hall attendance columns** (manually tracked)
- ✅ **Read-only scripts** operational (export_people.py, airtable_summary.py)
- ✅ **Cross-correlation ready** (export_for_fathom_matching.py)

**Key Features:**
- **API rate limiting** - 5 requests/second for Airtable
- **Weekly updates** - Run update_all.sh before major analysis
- **Backup recommended** - Before major changes
- **Key rotation** - Regular API key rotation recommended

### 2. Orientation - Where to Find What

**You are at:** airtable component README

**First-time users:**
1. Read this Overview (Section 1)
2. Follow Quick Start in Section 4
3. Run `python export_people.py` to test

**Routine usage:**
1. Weekly: Run `./update_all.sh` to refresh data
2. Before analysis: Check `people_export.csv` timestamp
3. Cross-correlation: Use `export_for_fathom_matching.py`

**What you might need:**
- **Parent system** → [/README.md](../README.md) - Overall ERA Admin architecture
- **System-wide status** → [/CONTEXT_RECOVERY.md](../CONTEXT_RECOVERY.md) - Integration status
- **System principles** → [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) - Overall philosophy
- **Integration** → [/integration_scripts/README.md](../integration_scripts/README.md) - Cross-component workflows

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)

**airtable-specific:**

**1. Manual Data Entry (Ground Truth)**
- **Human-curated data** - Airtable is source of truth for member/donor status
- **Manual TH tracking** - 17 Town Hall attendance columns updated by hand
- **Keep until automated** - Continue updating TH columns until Interactive Agenda App ready (Q2 2026)
- **Validation source** - Provides baseline for fuzzy matching accuracy

**2. Export Hygiene**
- **Weekly refresh** - Run `update_all.sh` before major analysis to get latest data
- **Timestamp checks** - Verify `people_export.csv` is fresh before using
- **Backup before changes** - Save previous exports before running updates
- **Compare exports** - Use `compare_exports.py` to see what changed

**3. Read-Only Mode**
- **NO WRITES TO AIRTABLE** - All scripts configured for export only
- **Database safety** - Modifications disabled to prevent accidental changes
- **Manual updates** - All Airtable changes done via web interface
- **Future enhancement** - Bidirectional sync capabilities planned

**4. Config Security**
- **API key protection** - Stored in `config.py` (not version controlled)
- **Template provided** - `config.py.template` shows structure
- **Regular rotation** - Rotate API keys periodically
- **Rate limiting** - Respect Airtable 5 req/sec limit

### 4. Specialized Topics

#### Quick Start

**1. Setup Environment**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**2. Configure API Access**
```bash
# Copy template and add your API key
cp config.py.template config.py
# Edit config.py with your Airtable API key
```

**3. Get Current Data**
```bash
# Export all People records to CSV
python export_people.py

# Get summary statistics
python airtable_summary.py

# Export for cross-correlation with Fathom data
python export_for_fathom_matching.py
```

#### Core Scripts

**export_people.py** - Export People table to CSV with all fields
- Output: `people_export.csv`
- Contains: All 630 people with all fields
- Use: Primary data source for analysis

**airtable_summary.py** - Generate database statistics and health check
- Output: `airtable_summary.txt`
- Contains: Record counts, field summaries, data quality metrics
- Use: Quick health check before major work

**export_for_fathom_matching.py** - Export optimized for name matching
- Output: `people_for_matching.csv`
- Contains: Cleaned names, member status, donor flags
- Use: Cross-correlation with FathomInventory participants

**config.py** - Centralized configuration and credentials
- Contains: Base ID, API key, table names
- Security: NOT version controlled (use config.py.template)

#### Data Files

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `people_export.csv` | Latest full export | Weekly or before analysis |
| `people_for_matching.csv` | Cleaned names for matching | Before Phase 4B runs |
| `airtable_summary.txt` | Latest database statistics | Weekly |
| `config.py` | API credentials | One-time setup, rotate periodically |

#### Routine Usage

**Daily/Weekly Updates:**
```bash
# Quick update - get latest data
./update_all.sh

# Check what changed
python compare_exports.py people_export.csv people_export_previous.csv
```

**Cross-Correlation with Fathom:**
```bash
# Prepare Airtable data for matching
python export_for_fathom_matching.py

# Run cross-correlation (from integration_scripts/)
cd ../integration_scripts
python cross_correlate.py
```

#### Integration Points

**With FathomInventory:**
- **Name matching** - Between Airtable People and Fathom participants
- **Enrichment** - Add membership status, donor flags to Fathom data
- **Identification** - Find active participants not yet in membership database
- **Validation** - Airtable provides ground truth for fuzzy matching accuracy

**With ERA Admin Workflows:**
- **Member communication** - Export email lists for outreach
- **Donor tracking** - Identify and track donor engagement
- **Engagement patterns** - Analyze TH attendance over time
- **Geographic distribution** - Map member locations

**With integration_scripts:**
- Phase 4B-1: Automated fuzzy matching (364 participants enriched)
- Phase 4B-2: Collaborative review (409 validated, 58 new people added)
- Phase 5T: Town Hall visualization (ready when 95%+ complete)

#### Maintenance

**Keep Data Fresh:**
- Run `./update_all.sh` weekly or before major analysis
- Monitor API rate limits (5 requests/second for Airtable)
- Backup exports before major changes
- Check timestamps on CSV files before using

**Security & Data Protection:**
- ✅ **READ-ONLY MODE** - All scripts configured for data export only
- ✅ **NO WRITES TO AIRTABLE** - Database modifications disabled
- ✅ **API key security** - Stored in `config.py` (not version controlled)
- ✅ **Regular key rotation** - Recommended for security
- ✅ **Backup recommended** - Before major changes

**Troubleshooting:**

*"API key error" or "Authentication failed"*
- Check `config.py` has correct API key
- Verify API key hasn't expired
- Rotate key in Airtable web interface if needed

*"Rate limit exceeded"*
- Scripts respect 5 req/sec limit
- Wait a few minutes and try again
- Reduce frequency if running multiple scripts

*"Export file empty or outdated"*
- Re-run `python export_people.py`
- Check `people_export.csv` timestamp
- Verify Airtable base accessible

#### Future Enhancements

- [ ] Automated daily sync with ERA_Admin automation
- [ ] Real-time change detection
- [ ] Bidirectional sync capabilities
- [ ] Integration with email systems
- [ ] Advanced matching algorithms for name variations

#### File Organization

**Core Scripts:**
- `export_people.py` - Full People table export
- `airtable_summary.py` - Database statistics
- `export_for_fathom_matching.py` - Matching-optimized export
- `cross_correlate.py` - Name matching analysis
- `compare_exports.py` - Track changes between exports
- `config.py` - API configuration (not in git)

**Data Files:**
- `people_export.csv` - Latest full export (630 people)
- `people_for_matching.csv` - Cleaned for fuzzy matching
- `airtable_summary.txt` - Database statistics
- `cross_correlation_report.txt` - Match analysis results

**Utilities:**
- `requirements.txt` - Python dependencies (pyairtable)
- `config.py.template` - Configuration template
- `update_all.sh` - Run all exports and updates
- `SAFETY_NOTICE.md` - Read-only mode explanation
- `venv/` - Virtual environment (created on setup)

**Back to:** [/README.md](../README.md)