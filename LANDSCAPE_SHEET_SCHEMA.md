# ERA Landscape Google Sheet Schema
**Documented:** October 21, 2025  
**Source:** Cloned from https://github.com/jonschull/ERA_Landscape_Static  
**Sheet ID:** 1cR5X2xFSGffivfsMjyHDDeDJQv6R0kQpVUJsEJ2_1yY

---

## Overview

The ERA Landscape visualization reads from a Google Sheet with two tabs: **`nodes`** and **`edges`**. The data is loaded via Google Sheets API and rendered as an interactive network graph.

**Live Site:** https://jonschull.github.io/ERA_Landscape_Static/

---

## Tab 1: `nodes`

### Column Structure

| Column | Type | Required | Example | Notes |
|--------|------|----------|---------|-------|
| `id` | string | ✅ YES | `person::Jon Schull` | **UNIQUE KEY**. Format: `type::label` |
| `label` | string | ✅ YES | `Jon Schull` | Display name |
| `type` | string | No | `person` | Ignored (parsed from ID prefix) |
| `url` | string | No | `https://example.com` | Optional URL |
| `notes` | string | No | `Founder of ERA` | Optional notes |
| `member` | string/bool | No | `true` | ERA member flag |
| `origin` | string | No | `fathom_export` | Data provenance |
| `hidden` | string/bool | No | `false` | Hide from visualization |
| `created_at` | ISO datetime | No | `2025-10-21T15:30:00Z` | Audit trail |
| `updated_at` | ISO datetime | No | `2025-10-21T15:30:00Z` | Audit trail |
| `created_by` | email | No | `user@example.com` | **Future:** User tracking |
| `updated_by` | email | No | `user@example.com` | **Future:** User tracking |
| `fields_changed` | JSON array | No | `["label","notes"]` | **Future:** Change tracking |

### Node ID Format

**Critical:** IDs must follow the pattern `type::label` where type is one of:

- `person::` - Individual people
- `org::` - Organizations
- `project::` - Projects/initiatives/meetings

**Examples:**
```
person::Jon Schull
person::Mary Olson
org::EcoRestoration Alliance
org::Rebalance Earth
project::Town Hall Meetings
project::TH 1-08-2025
project::TH 9-17-25
```

**Note:** The visualization parses `type` from the ID prefix, so the `type` column is technically redundant but preserved for backward compatibility.

### Visual Mapping

Based on type prefix:

| Type | Shape | Color | Border |
|------|-------|-------|--------|
| `person` | circle | Blue (#6495ED) | #4169E1 |
| `org` | box | Teal (#20B2AA) | #008B8B |
| `project` | diamond | Purple (#9370DB) | #6A5ACD |

### Node Scaling

Nodes are automatically sized based on connection count:
- **Min size:** 12px (1 connection)
- **Max size:** 60px (17+ connections)
- Calculated dynamically on load

---

## Tab 2: `edges`

### Column Structure

| Column | Type | Required | Example | Notes |
|--------|------|----------|---------|-------|
| `source` | string | ✅ YES | `person::Jon Schull` | From node ID (must exist in nodes tab) |
| `target` | string | ✅ YES | `project::TH 1-08-2025` | To node ID (must exist in nodes tab) |
| `relationship` | string | No | `organizer` | Edge label/type |
| `role` | string | No | `host` | Optional role description |
| `url` | string | No | `https://...` | Optional URL |
| `notes` | string | No | `Organized monthly` | Optional notes |
| `created_at` | ISO datetime | No | `2025-10-21T15:30:00Z` | Audit trail |
| `updated_at` | ISO datetime | No | `2025-10-21T15:30:00Z` | Audit trail |

### Relationship Types

Common relationship labels:

**Person-to-Organization:**
- `works_at`
- `affiliated_with`
- `member_of`
- `founder`
- `director`

**Person-to-Project:**
- `organizer`
- `attended`
- `participant`
- `lead`

**Organization-to-Project:**
- `sponsor`
- `partner`
- `host`

**Project-to-Project:**
- `part_of` (e.g., TH 1-08-2025 → Town Hall Meetings)
- `follows` (temporal sequence)
- `related_to`

---

## Auto-Healing

The visualization automatically creates missing nodes if referenced by edges:

```javascript
// If edge references node ID that doesn't exist in nodes tab:
{
  id: "person::Jane Doe",  // from edge reference
  label: "Jane Doe",        // stripped prefix
  title: "Jane Doe\n(auto-created from edge reference)",
  origin: "auto-healed",
  created_at: <current timestamp>
}
```

**Implication for export:** You can create edges first, and missing person nodes will be auto-created. But better to explicitly create both for data quality.

---

## Export Pattern for Fathom → Landscape

### Town Hall Meeting Chain

**Goal:** Create a chain of Town Hall meetings with attendees.

**Structure:**
```
Town Hall Meetings (project umbrella)
  ↓ (part_of)
  ├─> TH 1-08-2025 (project)
  │     ↓ (attended)
  │     ├─> Jon Schull (person)
  │     ├─> Mary Olson (person)
  │     └─> ... (35 attendees)
  │
  ├─> TH 9-17-25 (project)
  │     ↓ (attended)
  │     └─> ... (attendees)
  │
  └─> Jon Schull (organizer edge to umbrella)
```

### Node Exports

**1. Umbrella Project Node:**
```python
{
    'id': 'project::Town Hall Meetings',
    'label': 'Town Hall Meetings',
    'type': 'project',
    'url': '',
    'notes': 'Monthly ERA community gatherings',
    'member': '',
    'origin': 'fathom_export',
    'hidden': 'false',
    'created_at': '2025-10-21T15:30:00Z',
    'updated_at': '2025-10-21T15:30:00Z'
}
```

**2. Individual Meeting Node:**
```python
{
    'id': 'project::TH 1-08-2025',
    'label': 'TH 1-08-2025',
    'type': 'project',
    'url': '<fathom_video_url>',  # from fathom_emails.db
    'notes': f'Town Hall meeting on 2025-01-08, {participant_count} attendees',
    'member': '',
    'origin': 'fathom_export',
    'hidden': 'false',
    'created_at': '2025-10-21T15:30:00Z',
    'updated_at': '2025-10-21T15:30:00Z'
}
```

**3. Person Node (from Fathom DB):**
```python
{
    'id': f'person::{name}',
    'label': name,  # from participants.name
    'type': 'person',
    'url': '',
    'notes': affiliation or '',  # from participants.affiliation
    'member': 'true' if era_member else '',  # from participants.era_member
    'origin': 'fathom_export',
    'hidden': 'false',
    'created_at': '2025-10-21T15:30:00Z',
    'updated_at': '2025-10-21T15:30:00Z'
}
```

### Edge Exports

**1. Meeting → Umbrella (part_of):**
```python
{
    'source': 'project::TH 1-08-2025',
    'target': 'project::Town Hall Meetings',
    'relationship': 'part_of',
    'role': '',
    'url': '',
    'notes': '',
    'created_at': '2025-10-21T15:30:00Z',
    'updated_at': '2025-10-21T15:30:00Z'
}
```

**2. Person → Meeting (attended):**
```python
{
    'source': 'person::Jon Schull',
    'target': 'project::TH 1-08-2025',
    'relationship': 'attended',
    'role': '',
    'url': '',
    'notes': '',
    'created_at': '2025-10-21T15:30:00Z',
    'updated_at': '2025-10-21T15:30:00Z'
}
```

**3. Person → Umbrella (organizer):**
```python
{
    'source': 'person::Jon Schull',
    'target': 'project::Town Hall Meetings',
    'relationship': 'organizer',
    'role': '',
    'url': '',
    'notes': '',
    'created_at': '2025-10-21T15:30:00Z',
    'updated_at': '2025-10-21T15:30:00Z'
}
```

---

## Deduplication Strategy

**Before exporting:**

1. **Read existing nodes** from sheet
2. **Build ID lookup:** `{node.id: node}`
3. **For each person to export:**
   - Check if `person::{name}` exists
   - If exists: Skip or update `landscape_node_id` in Fathom DB
   - If missing: Add to export batch

**Prevent duplicates:**
- Use exact ID matching: `person::Jon Schull` vs existing IDs
- **Note:** Name variations ("Jon" vs "Jonathan") require fuzzy matching
- Consider: Email as secondary key if available

---

## Update Strategy

**Append-only:**
- Read existing sheet data
- Add new nodes/edges
- Write entire dataset back (clear + update)

**Warning:** Google Sheets API `clear` + `update` pattern means:
- All data replaced on each write
- No incremental updates
- Must merge existing + new data

**Better approach:**
- Use `append` API for new rows only
- But requires row-level change tracking

---

## Query Example (Python)

```python
from googleapiclient.discovery import build

# Read nodes tab
result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID,
    range='nodes!A:Z'
).execute()

rows = result.get('values', [])
headers = rows[0]
nodes = [dict(zip(headers, row)) for row in rows[1:]]

# Check if person exists
person_ids = {node['id'] for node in nodes if node['id'].startswith('person::')}
if f'person::Jon Schull' in person_ids:
    print("Already exists!")
```

---

## Next Steps

1. ✅ Schema documented
2. Create `export_to_landscape.py` script
3. Test with 5-10 people (prototype)
4. Test with 1 meeting + attendees
5. Scale to full 17 Town Halls

---

**References:**
- Code: `/Users/admin/ERA_Admin/landscape_working/`
- Live site: https://jonschull.github.io/ERA_Landscape_Static/
- GitHub: https://github.com/jonschull/ERA_Landscape_Static
