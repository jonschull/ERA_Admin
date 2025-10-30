# Other_Data_Sources/GDrive/README.md

### 1. Overview

**Purpose:** Access pre-Fathom historical documents for member verification and historical context

This component provides tools to search and download historical Google Drive documents from ERA's pre-Fathom era (2020-2023). It enables member verification for people active before comprehensive Fathom tracking began, using meeting notes, member rosters, and project documentation.

**What this component does:**
- Lists all documents in ERA Historical Documents folder
- Downloads pre-Fathom docs as searchable markdown file
- Searches for names across 349 historical items (240 Google Docs, 72 folders)
- Skips Town Hall meetings (already in database)
- Provides fast grep-based searching after initial download

**Key insight:** Pre-Fathom documents (2020-2023) contain evidence of member activity before automated tracking. By consolidating ~150 non-Town Hall docs into one searchable file, we can instantly verify historical membership without repeated API calls.

### 2. Orientation - Where to Find What

**You are at:** Other_Data_Sources/GDrive component

**What you might need:**
- **Parent** → [../README.md](../README.md) - Other_Data_Sources overview
- **Root** → [../../README.md](../../README.md) - Overall ERA Admin architecture
- **Integration** → [../../integration_scripts/member_enrichment/](../../integration_scripts/member_enrichment/) - Member verification workflows
- **Database** → [../../FathomInventory/fathom_emails.db](../../FathomInventory/fathom_emails.db) - Current member records
- **Credentials** → [../../FathomInventory/token.json](../../FathomInventory/token.json) - Shared Google auth (fathomizer account)

### 3. Principles

**System-wide:** See [../../WORKING_PRINCIPLES.md](../../WORKING_PRINCIPLES.md)

**GDrive-specific:**

**1. Historical Context Matters**
- Pre-Fathom members (2020-2023) may not appear in current database
- Early membership criteria were different
- Document quality varies (informal notes, partial names)
- Use as supporting evidence, not primary verification

**2. Download Once, Search Many Times**
- Initial download takes 2-3 minutes (~150 docs)
- Saves as single `pre_fathom_docs.md` file (~5-10MB)
- Subsequent searches via grep (milliseconds)
- Much faster than API-based searching

**3. Town Halls Excluded**
- Town Hall meetings already in Fathom database
- Script automatically skips TH docs during download
- Focus on working groups, projects, other meetings
- Avoid redundant data processing

**4. Testing and Validation**
- No automated tests (Google Drive API rate limits)
- Validation via successful download and grep searches
- Manual spot-check of name searches in output
- File size confirms successful download

### 4. Specialized Topics

#### Expected Data
- Early Town Hall meeting notes (pre-Fathom)
- Historical member rosters
- Project documentation mentioning members
- Meeting agendas and attendance records
- Working group documents

#### Timeframe
Primarily **2020-2023** (before comprehensive Fathom tracking)

#### Quality Notes
- Quality varies by document
- Some documents may be incomplete or outdated
- Attendance records may be informal
- Names may be inconsistent (nicknames, partial names)

#### Example Use Cases
1. **Person has Airtable bio but not in Fathom DB**
   → Check GDrive for Town Hall attendance 2020-2022
   
2. **Published member with no recent Fathom activity**
   → Verify historical participation in GDrive docs
   
3. **Name mentioned in old agendas**
   → Confirm member status and add to Fathom DB

## Tools Available

### `list_historical_docs.py`
List all documents in the historical folder. Generates an inventory with file IDs, types, and links.

**Usage:**
```bash
cd Other_Data_Sources/GDrive
python3 list_historical_docs.py
```

**Output:**
- Console display of folder structure
- `gdrive_historical_inventory.txt` - Full inventory with links

### `download_historical_docs.py` ⭐ **RECOMMENDED**
Download all pre-Fathom documents into one searchable markdown file.

**Strategy:**
- Skips Town Hall meetings (already in database)
- Downloads remaining ~150 documents
- Concatenates into `pre_fathom_docs.md`
- Then use standard grep for instant searches

**Usage:**
```bash
cd Other_Data_Sources/GDrive

# One-time download (~2-3 minutes)
python3 download_historical_docs.py

# Then search instantly with grep
grep -i "Valer Clark" pre_fathom_docs.md
grep -i "Jan Pokorny" pre_fathom_docs.md

# Case-insensitive with context
grep -i -C 3 "Valer Clark" pre_fathom_docs.md

# Search for multiple names
grep -i -E "Valer Clark|Jan Pokorny|Paulo Carvalho" pre_fathom_docs.md
```

**Output:**
- `pre_fathom_docs.md` - All docs in one file (~5-10MB)
- Each document has metadata header (filename, link, modified date)
- Fast grep searches (milliseconds vs minutes)

### `search_historical_docs.py` (Legacy - API-based, slower)
Search for names via Google Drive API. **Use download approach instead.**

**Note:** This tool exports each document individually via API, which is slow (5-10 minutes for full search). The download approach is much faster after initial setup.

## Authentication

Both tools use the existing FathomInventory Google authentication:
- **Account:** fathomizer@ecorestorationalliance.org
- **Token:** `/Users/admin/ERA_Admin/FathomInventory/token.json`
- **First run:** Will prompt for Drive access authorization

## Data Source

**Folder:** ERA Historical Documents (Pre-Fathom)
- **ID:** `1qEimCuk-usUdBFDUtYb8Y0x_BDWQFQ_s`
- **URL:** https://drive.google.com/drive/folders/1qEimCuk-usUdBFDUtYb8Y0x_BDWQFQ_s
- **Contents:** 349 items (240 Google Docs, 72 folders, 2 slides, 35 other files)
- **Date range:** 2022-2023 (pre-Fathom era)

**Back to:** [Other_Data_Sources README](../README.md)
