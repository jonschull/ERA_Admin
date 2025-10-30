# Other_Data_Sources/Wix/README.md

### 1. Overview

**Purpose:** Access and process historical member data from ERA's Wix-era website (pre-Fathom)

This component stores historical member data from ERA's Wix website database, providing access to early member registrations, profiles, and rosters from before Fathom tracking began. This data helps verify long-standing members who may not appear in current databases.

**What this component does:**
- Stores Wix database exports and backups
- Provides access to member registrations and profiles (pre-2023)
- Contains historical member bios and website user accounts
- Enables verification of early members missing from Fathom DB
- Documents historical member engagement patterns

**Key insight:** ERA's Wix website (pre-2023) captured early member registrations before automated tracking. These records are critical for verifying long-standing members and understanding historical membership patterns, though data quality varies based on export format.

**Status:** Data collection phase - No automated scripts yet. Manual exports and processing.

### 2. Orientation - Where to Find What

**You are at:** Other_Data_Sources/Wix component

**What you might need:**
- **Parent** → [../README.md](../README.md) - Other_Data_Sources overview
- **Root** → [../../README.md](../../README.md) - Overall ERA Admin architecture
- **Integration** → [../../integration_scripts/member_enrichment/](../../integration_scripts/member_enrichment/) - Member verification workflows
- **Database** → [../../FathomInventory/fathom_emails.db](../../FathomInventory/fathom_emails.db) - Current member records
- **Wix Database** → [Wix Dashboard](https://manage.wix.com/dashboard/096a9056-12e0-4a89-b78e-41797407eda2/database/data/EraPortolio1) - Source database

### 3. Principles

**System-wide:** See [../../WORKING_PRINCIPLES.md](../../WORKING_PRINCIPLES.md)

**Wix-specific:**

**1. Historical Verification Source**
- Wix records cover pre-2023 (before Fathom tracking)
- Use to verify long-standing members not in current databases
- Cross-reference with Google Groups and Airtable for confidence
- Member status may have changed since Wix era

**2. Variable Data Quality**
- Export format determines data quality
- Contact information may be outdated
- Member status may not reflect current reality
- Use as supporting evidence, not primary source

**3. Manual Processing Currently**
- No automated scripts yet (unlike GGroups, Zeffy, LinkedIn)
- Manual exports from Wix dashboard required
- Future: Automate if Wix provides export API
- Priority: MEDIUM (other sources more reliable)

**4. Testing and Validation**
- No automated tests (manual processing phase)
- Validation via cross-reference with other sources
- Verify member status changes since Wix era
- Document data quality issues as discovered

### 4. Specialized Topics

#### Expected Data
- Member registrations and profiles
- Early member rosters
- Website user accounts
- Historical member bios or profiles

#### Timeframe
Primarily **pre-2023** (before Fathom tracking began)

#### Usage
- Verify membership for people active before Fathom
- Identify early members missing from current databases
- Cross-reference with current member lists
- Document historical engagement

#### Quality Notes
- Data quality may vary depending on Wix export format
- May contain outdated contact information
- Member status may have changed since records were created

#### Data Sources
- [Wix database exports](https://manage.wix.com/dashboard/096a9056-12e0-4a89-b78e-41797407eda2/database/data/EraPortolio1)
- Member database backups
- Historical snapshots

#### Future Enhancements
- Automate Wix data export if API becomes available
- Create cross-reference script with Fathom DB
- Develop data quality assessment tool
- Document member status changes over time

**Back to:** [Other_Data_Sources README](../README.md)
