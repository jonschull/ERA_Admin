# Other_Data_Sources/README.md

### 1. Overview

**Purpose:** Member verification and historical activity tracking

This component consolidates multiple data sources used to verify ERA membership status and track member activities and histories. It addresses the historical problem that the Airtable `era_member` flag was unreliable, leading to incomplete member records in the Fathom database.

**What this component does:**
- Provides authoritative data sources for member verification
- Tracks historical member activities (donations, group participation, pre-Fathom records)
- Enables cross-referencing to confirm member status with confidence
- Documents member engagement patterns across multiple platforms

**Key insight:** No single source is perfect. Cross-referencing multiple authoritative sources (Google Groups, Zeffy donations, Wix records, pre-Fathom Google Docs, Airtable Publish status) provides high-confidence member verification.

### 2. Orientation - Where to Find What

**You are at:** Other_Data_Sources component

**What you might need:**
- **Parent** → [/README.md](../README.md) - Overall ERA Admin architecture
- **Integration** → [integration_scripts/member_enrichment/](../integration_scripts/member_enrichment/) - Member bio enrichment
- **Database** → [FathomInventory/fathom_emails.db](../FathomInventory/fathom_emails.db) - Member records
- **Legacy** → [airtable/](../airtable/) - Historical membership data

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)

**Other_Data_Sources specific:**

**1. Multiple Sources Required for Verification**
- No single source is definitive for member status
- Cross-reference at least 2-3 sources before flagging someone as a member
- Priority sources: Google Groups membership, Zeffy donations, Airtable Publish=True
- Secondary sources: Pre-Fathom docs, Wix records, GDrive documents

**2. Historical Context Matters**
- Membership evolved over time - early criteria were different
- Pre-Fathom members (before ~2023) may not appear in Fathom DB
- Donor status != member status (but suggests engagement)
- Published bios in Airtable indicate human-vetted membership

**3. Data Provenance**
- Document where each piece of information came from
- Track dates of data exports/snapshots
- Note data quality issues and limitations
- Keep raw exports separate from processed data

**4. Integration with Existing Systems**
- These sources augment, don't replace, existing databases
- Used for verification, not as primary record storage
- Feed into member_enrichment workflow
- Cross-reference with Fathom DB and Airtable

### 4. Specialized Topics

#### Reference Models

**BROWSER_COOKIE_AUTH_PATTERN.md** - Proven authentication pattern
- **Purpose:** Reference implementation for browser cookie-based authentication
- **Source:** FathomInventory production system
- **Status:** READ-ONLY MODEL - Do not edit
- **Usage:** Copy and adapt for services without API access (e.g., Google Groups)
- **Includes:** Complete workflow, verbatim scripts, troubleshooting guide

**Reference Scripts (READ-ONLY):**
- `REFERENCE_convert_edge_cookies.py` - Edge DevTools → JSON converter
- `REFERENCE_sanitize_cookies.py` - Playwright compatibility fixes
- `REFERENCE_refresh_auth.sh` - Guided refresh workflow

**These are proven, stable implementations. Copy and adapt, don't modify originals.**

---

#### Data Sources

**GGroups/** - Google Groups membership lists
- **Purpose:** Official ERA communication groups
- **Content:** Membership lists, join dates, participation
- **Usage:** Primary source for member verification
- **Quality:** High - managed by ERA administrators
- **Example groups:** ERA main list, ERA updates, working groups
- **Authentication:** Use BROWSER_COOKIE_AUTH_PATTERN.md as reference

**Zeffy/** - Donation records
- **Purpose:** Track financial supporters and donors
- **Content:** Donor names, amounts, dates, contact info
- **Usage:** Identify supporters, cross-reference membership
- **Quality:** High - transactional data
- **Note:** Donor != member, but suggests engagement level

**Wix/** - Pre-Fathom member records
- **Purpose:** Historical member data from Wix-era website
- **Content:** Early member registrations, profiles
- **Usage:** Verify long-standing members not in Fathom DB
- **Quality:** Variable - depends on Wix export quality
- **Timeframe:** Pre-2023 primarily

**GDrive/** - Pre-Fathom Google Docs
- **Purpose:** Historical meeting notes, member lists, documents
- **Content:** Early Town Hall notes, member rosters, project docs
- **Usage:** Verify membership for people active before Fathom tracking
- **Quality:** Variable - depends on document maintenance
- **Timeframe:** 2020-2023 primarily

**[LinkedIn/](LinkedIn/README.md)** - Profile scraping
- **Purpose:** Fetch LinkedIn profiles for member bio enrichment
- **Content:** Names, headlines, full profile text (About, Experience, etc.)
- **Usage:** Enrich Airtable bios with professional background data
- **Quality:** High - direct from LinkedIn profiles
- **Status:** ✅ Operational (Oct 30, 2025)
- **Authentication:** Cookie-based, follows BROWSER_COOKIE_AUTH_PATTERN.md

#### Verification Workflow

**High-Confidence Member (3+ sources):**
```
Airtable Publish=True + Google Groups member + Zeffy donor
→ VERIFIED MEMBER - add to Fathom DB with era_member=1
```

**Medium-Confidence Member (2 sources):**
```
Airtable Publish=True + Pre-Fathom GDocs mention
→ LIKELY MEMBER - review, then add to Fathom DB
```

**Needs Investigation (1 source or conflicting):**
```
Airtable bio exists, but era_member=False, not in Google Groups
→ VERIFY - check Town Hall agendas, email history
```

#### Integration Points

**With member_enrichment:**
- Use these sources to verify members lacking bios
- Cross-reference published Airtable bios with membership sources
- Identify members in Fathom DB but era_member=0 incorrectly

**With participant_reconciliation:**
- Verify member status during Fathom participant processing
- Identify Fathom participants who should be flagged as members
- Track historical members not yet in Fathom DB

**With Fathom Database:**
- Update era_member flags based on cross-referenced data
- Add missing members found through source verification
- Document provenance in bio or notes field

#### Common Patterns

**Pattern 1: Published but not in DB**
```
Airtable: Publish=True, good bio, era_member flag unreliable
Fathom DB: Not present
Action: Check Google Groups → if member, add to Fathom DB
```

**Pattern 2: Early member, no Fathom presence**
```
GDrive docs: Mentioned in 2021-2022 Town Halls
Fathom DB: Not present (Fathom started later)
Action: Add to Fathom DB as era_member=1 with historical note
```

**Pattern 3: Donor but unclear member status**
```
Zeffy: Multiple donations
Fathom DB: Appears in calls but era_member=0
Action: Check Google Groups + Airtable → update if confirmed
```

#### File Organization

**Data Files (keep in respective subdirectories):**
- Raw exports (CSV, JSON, etc.)
- Processed/cleaned versions
- Cross-reference reports
- Date-stamped snapshots

**Scripts (when created):**
- Export/download utilities
- Parsing and cleaning scripts
- Cross-reference analyzers
- Member verification reports

**Documentation:**
- Data source descriptions
- Export procedures
- Quality notes
- Integration guides

#### Future Enhancements

**Planned consolidations:**
- Move Airtable utilities from `airtable/` to `Other_Data_Sources/Airtable/`
- Create GDrive export automation
- ✅ COMPLETE: LinkedIn utilities in `Other_Data_Sources/LinkedIn/` (Oct 30, 2025)
- Create Gmail search utilities in `Other_Data_Sources/Gmail/`

**This would create a unified location for all external data source integrations.**

**Possible future structure:**
```
Other_Data_Sources/
├── README.md (this file)
├── GGroups/          # Google Groups
├── Zeffy/            # Donations
├── Wix/              # Legacy website
├── GDrive/           # Google Docs/Drive
├── Airtable/         # Consolidated Airtable utils
├── LinkedIn/         # Profile scraping
└── Gmail/            # Email searches
```

#### Current Status (October 30, 2025)

**Immediate need:**
- Verify 230+ people with Airtable bios but not in Fathom DB
- Cross-reference with Google Groups, Zeffy, pre-Fathom docs
- Update era_member flags for verified members
- Rewrite bios for 45+ members with poor bio quality

**Next steps:**
1. Gather Google Groups membership exports
2. Export Zeffy donor records
3. Locate and organize pre-Fathom GDrive docs
4. Export Wix member records (if accessible)
5. Create cross-reference analysis script
6. Generate member verification report

### Related Components

**Upstream (data sources):**
- Google Groups
- Zeffy donation platform
- Wix website (historical)
- Google Drive (pre-Fathom docs)
- LinkedIn (profile data)

**Downstream (consumers):**
- [FathomInventory/](../FathomInventory/) - Update member flags
- [integration_scripts/member_enrichment/](../integration_scripts/member_enrichment/) - Verify members needing bios
- [airtable/](../airtable/) - Cross-reference and validate

**Back to:** [/README.md](../README.md)
