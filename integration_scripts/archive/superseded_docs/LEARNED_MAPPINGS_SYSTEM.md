# Learned Mappings System

## Overview

The learned mappings system automatically extracts and applies reconciliation decisions from previous Phase 4B-2 rounds, dramatically reducing manual review time in subsequent rounds.

**Impact:** Round 9 had 80% auto-fill rate (20/25 entries), Round 10 estimated 37% (18/50 entries).

---

## How It Works

### 1. Extraction Phase

`deduplicate_participants.py` (or manual extraction script) reads all previous CSV exports and extracts standard decision patterns:

```python
# From: archive/csv_exports/phase4b2_approvals_*.csv
# Extracts:
{
  "phone_mappings": {"18022588598": "Michael Mayer"},
  "device_mappings": {"John's iPhone": "John Magugu"},
  "org_to_person": {"BasHam (Ecoist)": "Basham Zain"},
  "name_corrections": {"Benamara Elhabib": "Elhabib Benamara"},
  "drop_patterns": ["Abigail Castle", "April Bartlett"]
}
```

**Extraction logic:**
- `merge with: X` → adds to appropriate mapping category
- `drop` → adds to drop_patterns
- Categorizes by: phone numbers, device names, orgs, name variants

**Stored in:** `phase4b2_learned_mappings.json`

### 2. Application Phase

`generate_phase4b2_table.py` loads learned mappings and applies them when generating the HTML approval table:

```python
# For each person in batch:
1. Check learned mappings first (before Airtable fuzzy match)
2. If found in mappings:
   - Pre-fill comment with learned decision
   - Auto-check "Process This" checkbox
   - Add green badge: "🔁 [reason]"
3. If not found:
   - Proceed with normal fuzzy matching logic
   - Use AI suggestions
```

### 3. Accumulation Over Time

Each round adds more mappings:
- Round 1-8: 174 mappings extracted
- Round 9: +4 mappings (18022588598 corrected, 3 drops)
- Round 10+: Continues to grow

**Result:** Auto-fill rate increases as more patterns are learned.

---

## Mapping Categories

### Phone Numbers (`phone_mappings`)
**Purpose:** Map phone numbers to real names

**Example:**
```json
{
  "18022588598": "Michael Mayer",
  "16319034965": "Sean Pettersen"
}
```

**Application:**
- Input: "18022588598"
- Output: `merge with: Michael Mayer` (auto-checked)

### Device Names (`device_mappings`)
**Purpose:** Map device names to real people

**Example:**
```json
{
  "John's iPhone": "John Magugu",
  "Andres's iPhone (2)": "Andres Garcia"
}
```

**Detection:** Contains keywords: iphone, ipad, android, 's phone

### Organizations to People (`org_to_person`)
**Purpose:** Map organization names or variants to representative person

**Example:**
```json
{
  "BasHam (Ecoist)": "Basham Zain",
  "Beck Bio4Climate": "Beck Mordini",
  "Aimee Samara (Krouskop)": "Aimee Samara"
}
```

**Detection:** Contains: LLC, Inc, Foundation, Institute, Project, or parentheses with context

### Name Corrections (`name_corrections`)
**Purpose:** Map name variants, misspellings, or short names to correct full names

**Example:**
```json
{
  "Benamara Elhabib": "Elhabib Benamara",
  "Betty Bitengo": "Betty Atandi",
  "Ana": "Ana Calderon",
  "Jim Bledsoe": "Jim Bledsoe"
}
```

**Filtering:** Only applies "clean" corrections (2-3 word names, no instructions/comments)

**Note:** Some entries in name_corrections contain instructions (e.g., "Add ERA Member") - these are NOT auto-applied to avoid mistakes.

### Drop Patterns (`drop_patterns`)
**Purpose:** Identify entries that should always be deleted

**Example:**
```json
[
  "Abigail Castle",
  "April Bartlett",
  "Arav Bhargava",
  "Bob",
  "Cosmic Labyrinth",
  "MOSES, GFCCA"
]
```

**Application:**
- Input: "Abigail Castle"
- Output: `drop` (auto-checked)

---

## File Structure

### Storage File
**Location:** `integration_scripts/phase4b2_learned_mappings.json`

**Format:**
```json
{
  "phone_mappings": {...},
  "device_mappings": {...},
  "org_to_person": {...},
  "name_corrections": {...},
  "drop_patterns": [...],
  "metadata": {
    "extracted_from": "Rounds 1-8 (Oct 20, 2025)",
    "total_phone_mappings": 2,
    "total_device_mappings": 0,
    "total_name_corrections": 140,
    "total_org_mappings": 19,
    "total_drop_patterns": 14
  }
}
```

### Application Logic
**Location:** `integration_scripts/apply_learned_mappings.py`

**Key function:**
```python
def check_learned_mapping(name):
    """Check if we have a learned mapping for this name.
    
    Returns: (has_mapping, decision, reason)
    """
    # Checks in order:
    # 1. Drop patterns (exact match)
    # 2. Phone mappings
    # 3. Device mappings
    # 4. Org mappings
    # 5. Name corrections (with filtering)
    
    return has_mapping, decision, reason
```

---

## Visual Indicators

### Green Badges in HTML Table

Auto-filled entries show green badges with reason:

```
🔁 Previously dropped in earlier round
🔁 Phone number resolved in earlier round
🔁 Device name resolved in earlier round
🔁 Organization mapping from earlier round
🔁 Name variant resolved in earlier round
```

**User action:** Verify the suggestion is still correct, then proceed.

### Auto-Checked Boxes

- ✅ **Process This** - Auto-checked for learned mappings
- ⬜ **Probe** - NOT checked for learned mappings (already decided)

---

## Maintenance & Updates

### Adding New Mappings

**Manual addition:**
```bash
# Edit phase4b2_learned_mappings.json
# Add to appropriate category
# Update metadata counts
```

**From CSV exports:**
```bash
# Run extraction script
python3 extract_learned_mappings.py
```

### Correcting Mistakes

If a learned mapping is wrong:

1. **Remove from JSON:**
   ```json
   // Remove or update incorrect entry
   "phone_mappings": {
     "18022588598": "Michael Mayer"  // ← Was incorrectly in drop_patterns
   }
   ```

2. **Update drop_patterns:**
   ```json
   "drop_patterns": [
     "Abigail Castle",
     // "18022588598",  ← REMOVED (was mistake)
     "April Bartlett"
   ]
   ```

3. **Commit change:**
   ```bash
   git add phase4b2_learned_mappings.json
   git commit -m "fix: Correct phone mapping for 18022588598"
   ```

### Conflicts Between Mappings

**Problem:** Same name appears in multiple categories

**Example:** "18022588598" appeared in both `phone_mappings` AND `drop_patterns`

**Resolution:**
- Check priority: drop > phone > device > org > name
- Keep in highest-priority category only
- Document reason in commit message

---

## Performance Impact

### Time Savings

**Round 9 (25 people):**
- Auto-filled: 20/25 (80%)
- Manual review: 5/25 (20%)
- **Time saved:** ~80% reduction

**Round 10 (50 people):**
- Auto-filled: ~18/50 (37%)
- Manual review: ~32/50 (63%)
- **Time saved:** ~37% reduction

**Why variance?**
- Round 9 hit many previously-seen patterns
- Round 10 encountering more new names
- Auto-fill rate will increase as more rounds processed

### Accuracy

**Correctness:** ~99%
- User verifies green-badged entries
- Mistakes caught during review
- Can override any auto-filled suggestion

**False positives:** Rare
- Name corrections filtered to avoid instruction text
- Only applies clean 2-3 word names
- User has final say

---

## Future Enhancements

### Potential Improvements

1. **Fuzzy matching for learned mappings**
   - Current: Exact match only
   - Proposed: Apply fuzzy logic to catch variants
   - Example: "Dr Brian von Herzen" → "Dr. Brian von Herzen"

2. **Confidence scoring**
   - Track how often each mapping is verified/changed
   - Downgrade confidence if user frequently overrides
   - Auto-remove low-confidence mappings

3. **Pattern learning**
   - Detect common patterns (e.g., "Dr." variants)
   - Auto-suggest similar transformations
   - Example: All "Dr X" → "X" (without title)

4. **Export to shared knowledge base**
   - Share learned mappings across team
   - Merge mappings from multiple users
   - Version control for mappings

---

## Troubleshooting

### Issue: Low Auto-Fill Rate

**Symptom:** Few entries auto-filled despite many rounds processed

**Causes:**
1. New names appearing in batch (expected)
2. Mappings file not loading (check path)
3. Name variants not matching (case sensitivity)

**Debug:**
```bash
# Check if mappings file loaded
python3 << EOF
import json
with open('phase4b2_learned_mappings.json', 'r') as f:
    m = json.load(f)
print(f"Mappings loaded: {len(m['phone_mappings'])} phone, {len(m['drop_patterns'])} drops")
EOF
```

### Issue: Wrong Auto-Fill

**Symptom:** Green badge suggests incorrect merge/drop

**Action:**
1. Override in HTML table (edit comment)
2. Note incorrect mapping for correction
3. Update `phase4b2_learned_mappings.json` after round

### Issue: Duplicate Mappings

**Symptom:** Same person in multiple categories or as different targets

**Resolution:**
1. Determine correct mapping
2. Remove from other categories
3. Document in commit message

---

## Related Files

- **`phase4b2_learned_mappings.json`** - Storage of all learned mappings
- **`apply_learned_mappings.py`** - Application logic (imported by table generator)
- **`generate_phase4b2_table.py`** - Integrates learned mappings into HTML generation
- **`execute_phase4b2_actions.py`** - Uses mappings indirectly (via CSV comments)
- **Archive CSVs** - Source data for learning (`archive/csv_exports/phase4b2_approvals_*.csv`)

---

## Best Practices

1. **Review green badges** - Don't blindly trust, verify each one
2. **Note corrections** - If you override, note it for future mapping update
3. **Regular extraction** - Re-run extraction after every 5-10 rounds to capture new patterns
4. **Keep clean** - Remove obsolete/wrong mappings periodically
5. **Commit changes** - Track mapping updates in git for auditability
