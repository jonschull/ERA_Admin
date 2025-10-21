# Landscape Integration Context & Summary
**Created:** October 21, 2025

## 📍 Current Situation

I've successfully regained context on both the FathomInventory data enrichment project and the ERA Landscape project. Here's what I found:

### FathomInventory Data (Source)
**Location:** `/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db`

**Current State:**
- **2,507 total participants** across all meetings
- **1,698 validated participants** (67.7%) enriched with Airtable data
- **1,604 ERA members** identified
- **255 remaining** for Phase 4B-2 collaborative review

**Key Database Fields Ready for Landscape:**
```
name                  - Participant name (validated)
location              - Geographic location
affiliation           - Organization/affiliation
collaborating_people  - Relationships
collaborating_orgs    - Organization relationships
landscape_node_id     - EMPTY (ready to populate for linkage)
validated_by_airtable - Boolean (quality flag)
era_member           - Boolean (membership flag)
email                - Email address (where available)
airtable_id          - Link to Airtable record
```

**Phase 4B-2 Progress:**
- ✅ 8 rounds completed (409 participants validated)
- ✅ 58 new people added to Airtable (+10% growth)
- 🔄 87% complete, targeting 95%

### ERA Landscape (Destination)
**Live Site:** https://jonschull.github.io/ERA_Landscape_Static/  
**Data Source:** Google Sheet ID: `1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY`  
**Local Directory:** `/Users/admin/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon Schull/CascadeProjects/ERA_Landscape_Static`

**Current State:**
- **350+ nodes** (organizations, people, projects)
- **Technology:** Static HTML/JS with Google Sheets data source
- **Issue:** Dropbox directory timing out (CloudStorage sync latency)

## 🎯 Integration Goal

Create automated pipeline to export FathomInventory participants and meetings to ERA Landscape visualization, enabling:

1. **People nodes** - 1,698 validated participants appear in network
2. **Meeting nodes** - Town Hall meetings as project nodes
3. **Relationships** - Participant-to-meeting connections (attended)
4. **Temporal chain** - Sequential meeting structure
5. **Bidirectional linkage** - `landscape_node_id` field tracks sync

## 🚧 Current Blockers

### 1. Dropbox Timeout
**Issue:** Cannot access Landscape directory via CloudStorage path  
**Impact:** Can't directly inspect Landscape code/schema  
**Options:**
- Access Google Sheet directly (bypasses Dropbox)
- Clone GitHub repo: https://github.com/jonschull/ERA_Landscape_Static
- Wait for Dropbox sync to stabilize

### 2. OAuth Token Expired
**Issue:** Google Sheets API token expired/revoked  
**Impact:** Can't read sheet structure yet  
**Solution:** Re-authenticate with proper scopes:
- Gmail API (already configured)
- **Google Sheets API** (needs to be added)

### 3. Sheet Schema Unknown
**Issue:** Don't know exact format Landscape expects  
**Impact:** Can't export data in correct format  
**Next Step:** Run `inspect_landscape_sheet.py` after OAuth refresh

## 📦 Deliverables Created

### 1. LANDSCAPE_INTEGRATION_PROTOTYPE.md
- Complete 4-phase prototype plan
- Conservative approach (5-10 people → 1 meeting → full export)
- Success metrics and validation criteria
- Timeline: 2-3 days for full prototype

### 2. inspect_landscape_sheet.py
- Script to examine Google Sheet structure
- Documents columns, node types, edge formats
- Generates schema documentation
- **Status:** Ready to run after OAuth re-authentication

## 🔄 Next Steps

### Immediate (Your Decision)

**Option A: OAuth Re-authentication**
1. Re-authenticate Google OAuth with Sheets scope
2. Run `inspect_landscape_sheet.py` to document schema
3. Proceed with Phase 1 (schema discovery)

**Option B: Clone Landscape Repo**
1. Clone from GitHub: `git clone https://github.com/jonschull/ERA_Landscape_Static.git`
2. Inspect code directly to understand format
3. Access Google Sheet as read-only (public view)

**Option C: Wait for Dropbox**
1. Let Dropbox CloudStorage sync stabilize
2. Access local directory directly
3. Examine code and documentation

### After Schema Discovery

**Phase 2: Small Prototype** (2-3 hours)
- Export 5-10 validated participants
- Test node creation and deduplication
- Verify in live Landscape
- Validate `landscape_node_id` backfill

**Phase 3: Meeting Node Prototype** (3-4 hours)
- Add one Town Hall meeting
- Link ~10 attendees
- Test temporal chain visualization
- Document any issues

**Phase 4: Full Integration** (deferred until prototype success)
- Export all 17 validated Town Hall meetings
- Connect 300+ participants
- Create umbrella project structure
- Implement Phase 5T fully

## 📊 Data Quality Assessment

**Validation Status:**
- **Validated (1,698):** Ready for export - high confidence
- **Remaining (255):** Phase 4B-2 will continue enriching
- **Total (2,507):** Growing daily with new meetings

**Integration Readiness:**
- ✅ Database structure ready
- ✅ `landscape_node_id` field available
- ✅ Validated participants identified
- ⏳ Sheet schema needs discovery
- ⏳ OAuth needs refresh with Sheets scope

## 🎓 Recommendations

1. **Start Conservative:** Prototype with 5-10 people before scaling
2. **Validate Early:** Test deduplication logic before bulk export
3. **Iterate Quickly:** Small batches, validate, adjust, repeat
4. **Track Linkage:** Use `landscape_node_id` to avoid re-processing
5. **Document Schema:** Create LANDSCAPE_SHEET_SCHEMA.md for reference

## 📞 Questions for You

1. **Which approach do you prefer?**
   - OAuth re-auth (I can guide through it)
   - Clone GitHub repo (faster, but may miss latest changes)
   - Wait for Dropbox (simplest if it works)

2. **Prototype scope OK?**
   - Start with 5-10 people, then 1 meeting?
   - Or jump straight to full 17 meetings?

3. **Timeline acceptable?**
   - 2-3 days for full prototype (4-6 hours work)
   - Or prefer faster/more cautious approach?

## 🔗 References

- **Prototype Plan:** [LANDSCAPE_INTEGRATION_PROTOTYPE.md](LANDSCAPE_INTEGRATION_PROTOTYPE.md)
- **System Status:** [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md)
- **Strategic Plan:** [ERA_ECOSYSTEM_PLAN.md](ERA_ECOSYSTEM_PLAN.md) (Phase 5T)
- **FathomInventory:** [FathomInventory/README.md](FathomInventory/README.md)
- **Integration Scripts:** [integration_scripts/README.md](integration_scripts/README.md)

---

**Status:** Context fully regained, prototype plan ready, awaiting your direction on next steps.
