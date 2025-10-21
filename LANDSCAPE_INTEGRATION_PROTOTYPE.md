# Landscape Integration Prototype Plan
## Fathom → Landscape Linkage Testing & Implementation

**Created:** October 21, 2025  
**Status:** Prototype Planning  
**Phase:** 5T Preparation

---

## 🎯 Goal

Test and prototype the integration pipeline from FathomInventory database to ERA Landscape visualization.

**Target Flow:**
```
FathomInventory DB (1,698 validated participants)
    ↓
Export Script (new)
    ↓
Google Sheet (ID: 1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY)
    ↓
ERA Landscape Visualization
    ↓
https://jonschull.github.io/ERA_Landscape_Static/
```

---

## 📊 Current State Assessment

### FathomInventory Database
- **Location:** `/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db`
- **Participants:** 2,507 total
  - 1,698 validated (67.7%) via Airtable matching
  - 1,604 ERA members identified
  - 255 remaining for Phase 4B-2 review
- **Key Fields:**
  - `name` - Participant name
  - `location` - Geographic location
  - `affiliation` - Organization/affiliation
  - `landscape_node_id` - **EMPTY** (ready to populate)
  - `validated_by_airtable` - Boolean (1 = validated)
  - `era_member` - Boolean (1 = ERA member)
  - `email` - Email address (where available)
  - `airtable_id` - Link to Airtable record

### ERA Landscape
- **Location (local):** `/Users/admin/Library/CloudStorage/Dropbox-EcoRestorationAllianceLLC/Jon Schull/CascadeProjects/ERA_Landscape_Static`
- **Live Site:** https://jonschull.github.io/ERA_Landscape_Static/
- **Data Source:** Google Sheet (ID: 1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY)
- **Current Nodes:** 350+ organizations, people, projects
- **Technology:** Static HTML/JS with Google Sheets API
- **Access Issues:** Dropbox directory timing out (CloudStorage sync issue)

---

## 🧪 Prototype Test Plan

### Phase 1: Understand Landscape Data Format (2 hours)

**Objective:** Reverse-engineer the Google Sheet structure that Landscape expects

**Tasks:**
1. ✅ Access Google Sheet directly (bypass Dropbox timeout)
2. Document sheet structure:
   - Column names and types
   - Node types (person, organization, project)
   - Edge/relationship format
   - Required vs optional fields
3. Identify key patterns:
   - How people nodes are formatted
   - How meeting/project nodes are structured
   - How relationships (edges) are defined

**Deliverable:** `LANDSCAPE_SHEET_SCHEMA.md` documenting structure

### Phase 2: Small Prototype Export (2-3 hours)

**Objective:** Test export of 5-10 validated participants to Landscape

**Scope (Conservative Start):**
- Export 5-10 validated ERA members
- No meetings yet (just people nodes)
- Test node creation and deduplication
- Verify visualization updates

**Tasks:**
1. Create `prototype_landscape_export.py` script
2. Query 5-10 validated participants from DB
3. Format as Landscape nodes (matching sheet schema)
4. Write to Google Sheet (test mode - separate tab)
5. Verify in Landscape visualization
6. Test `landscape_node_id` backfill

**Success Criteria:**
- [ ] Participants appear in Landscape
- [ ] No duplicate nodes created
- [ ] Proper node type (person)
- [ ] landscape_node_id updated in DB

### Phase 3: Meeting Node Prototype (3-4 hours)

**Objective:** Add one Town Hall meeting with attendees

**Scope:**
- Pick one recent TH meeting with ~10 validated attendees
- Create meeting as project node
- Link attendees to meeting (edges)
- Test temporal chain concept

**Tasks:**
1. Query one TH meeting with validated participants
2. Create project node for the meeting
3. Create person-to-meeting edges (attended relationship)
4. Export to Google Sheet
5. Verify in Landscape (interactive exploration)
6. Document any issues

**Success Criteria:**
- [ ] Meeting appears as project node
- [ ] Attendees linked to meeting
- [ ] Can click meeting and see connections
- [ ] Temporal metadata preserved (date)

### Phase 4: Full Integration (After Prototype Success)

**Deferred until prototype validated**

---

## 🚧 Known Challenges

### Challenge 1: Dropbox Timeout
**Issue:** Cannot access Landscape directory via CloudStorage path  
**Impact:** Can't directly read Landscape code/documentation  
**Workaround:**
- Access Google Sheet directly (bypass Dropbox)
- Reference live site for testing
- Git clone if needed: https://github.com/jonschull/ERA_Landscape_Static

### Challenge 2: Sheet Schema Unknown
**Issue:** Don't know exact format Landscape expects  
**Impact:** May create incompatible nodes  
**Mitigation:**
- Phase 1 focuses on schema discovery
- Test in separate sheet tab first
- Validate before production export

### Challenge 3: Node Deduplication
**Issue:** Landscape already has 350+ nodes - avoid duplicates  
**Impact:** Could create duplicate person nodes  
**Mitigation:**
- Query existing nodes from sheet
- Match by name/email before creating
- Populate landscape_node_id to track linkage

### Challenge 4: Data Completeness
**Issue:** Only 67.7% of participants validated  
**Impact:** May have incomplete data for some attendees  
**Mitigation:**
- Start with validated participants only
- Phase 4B-2 continues to improve validation rate
- Can add more as validation completes

---

## 📦 Deliverables

### Immediate (Prototype Phase)
1. **LANDSCAPE_SHEET_SCHEMA.md** - Document Google Sheet structure
2. **prototype_landscape_export.py** - Test export script (5-10 people)
3. **Test Results Document** - Validation of prototype
4. **Issues Log** - Any problems encountered

### After Prototype Success
5. **export_townhalls_to_landscape.py** - Full Phase 5T implementation
6. **Integration Documentation** - Complete workflow guide
7. **Monitoring Script** - Health checks for sync

---

## 🔄 Integration with Existing Work

### Relationship to Phase 4B-2
- Phase 4B-2 continues enriching participants (87% → 95%)
- Prototype can proceed with current 1,698 validated
- As more validated, they flow into Landscape
- No blocking dependencies

### Relationship to Phase 5T
- This prototype IS Phase 5T testing
- Start small (5-10 people) before full 17 meetings
- Prove concept before scaling up
- Establishes pattern for future expansions

---

## 📋 Next Steps

### Immediate Actions
1. **Access Google Sheet directly**
   - Bypass Dropbox timeout
   - Document current structure
   - Understand node/edge format

2. **Clone Landscape Repo (if needed)**
   ```bash
   cd /Users/admin/ERA_Admin
   git clone https://github.com/jonschull/ERA_Landscape_Static.git landscape_reference
   ```

3. **Create Phase 1 Script**
   - Read Google Sheet structure
   - Generate schema documentation
   - Identify integration points

### Questions to Answer
- [ ] What columns exist in the Google Sheet?
- [ ] How are person nodes represented?
- [ ] How are project nodes represented?
- [ ] How are edges/relationships defined?
- [ ] Is there a node ID system already?
- [ ] How does Landscape handle duplicates?
- [ ] What's the update frequency/trigger?

---

## 📝 Success Metrics

### Prototype Success
- [ ] 5-10 people successfully exported
- [ ] Appear in Landscape visualization
- [ ] No duplicate nodes created
- [ ] landscape_node_id field populated
- [ ] Can query "who's in Landscape" from DB

### Integration Success (Full Phase 5T)
- [ ] 17 TH meetings as project nodes
- [ ] "Town Hall Meetings" umbrella project
- [ ] 300+ person-to-meeting connections
- [ ] Jon Schull → TH organizer edge
- [ ] Loads in <3 seconds
- [ ] Data flow documented

---

## 🔗 References

- **Parent Plan:** [ERA_ECOSYSTEM_PLAN.md](ERA_ECOSYSTEM_PLAN.md) (Phase 5T)
- **System Status:** [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md)
- **FathomInventory:** [FathomInventory/README.md](FathomInventory/README.md)
- **Integration Scripts:** [integration_scripts/README.md](integration_scripts/README.md)
- **Live Landscape:** https://jonschull.github.io/ERA_Landscape_Static/
- **Landscape Repo:** https://github.com/jonschull/ERA_Landscape_Static

---

**Status:** Ready for Phase 1 (Schema Discovery)  
**Blocker:** None - can proceed with Google Sheets access  
**Timeline:** 2-3 days for full prototype (assuming 4-6 hours total work)
