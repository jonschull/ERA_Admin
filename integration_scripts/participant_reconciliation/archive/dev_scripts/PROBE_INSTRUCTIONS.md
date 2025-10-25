# Instructions for Cascade: Phase 4B-2 Probing

**When user says:** "Please probe probe_list_XXXXX.json"

---

## Your Mission

Manually investigate each person in the probe list using **thoughtful analysis**, not automatic pattern matching.

---

## Methodology (5 Steps)

### 1. ANALYZE NAME STRUCTURE
- Identify person vs organization components
- Clean punctuation and formatting
- Extract meaningful tokens
- Look for patterns: "Name, Organization" or "Title Name Abbrev."

### 2. SEARCH AIRTABLE VARIATIONS
```bash
# Use fuzzy matching on:
- Full name
- Individual words (if ambiguous)
- Common variations (Mike/Michael, etc)
# Check organization field for context clues
```

### 3. SEARCH GMAIL FOR CONTEXT
```bash
python3 /Users/admin/ERA_Admin/integration_scripts/gmail_research.py "[Name]"
```
- Look for mentions and context
- Identify relationships, projects, affiliations
- Verify if ERA-related work

### 4. CROSS-REFERENCE EVIDENCE
- Compare Airtable org field with name components
- Check if Gmail context matches Airtable data
- Look for corroborating details across sources

### 5. MAKE RECOMMENDATION

**Format:**
```
🔍 Probing [Name]...

1. Analysis: [name structure breakdown]
2. Airtable: [search results with scores]
3. Gmail: [findings from email search]
4. Cross-ref: [verification across sources]

RECOMMENDATION: [action]
CONFIDENCE: [0-100]%
EVIDENCE: [supporting facts list]
METHOD: [how you reached conclusion]
```

---

## Decision Criteria

| Action | When to Use |
|--------|-------------|
| **merge with: [Name]** | High confidence match (>85%) + corroborating evidence from multiple sources |
| **add_to_airtable** | Real person + ERA-related work + not currently in Airtable |
| **ignore** | Not ERA-related, organizational junk, or duplicate |
| **needs_more_info** | Insufficient evidence to make confident decision |

---

## Tools Available

- **Gmail Research:** `/Users/admin/ERA_Admin/integration_scripts/gmail_research.py`
- **Airtable CSV:** `/Users/admin/ERA_Admin/airtable/people_export.csv` (592 people)
- **Fathom DB:** `/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db`
- **Fuzzy Matching:** `from fuzzywuzzy import fuzz`

---

## Example Probing

**Input:** "Moses GFCCA" (flagged: not in Airtable, contains org name)

**Your Investigation:**
```
🔍 Probing Moses GFCCA...

1. Analysis:
   - "MOSES" appears to be a person's name
   - "GFCCA" is an organization acronym
   - Format suggests: Person, Organization

2. Airtable search:
   Word "Moses" → Moses Ojunju (100% match)
   Check org field: Moses Ojunju org = "GFCCA" ✅

3. Gmail verification:
   python3 gmail_research.py "Moses GFCCA"
   → 5 emails found
   → Subjects mention "Moses from GFCCA"
   → Context: Food security, climate adaptation projects

4. Cross-reference:
   - Moses Ojunju works with GFCCA ✅
   - Project areas align with Gmail mentions ✅
   - Multiple corroborating data points ✅

RECOMMENDATION: merge with: Moses Ojunju
CONFIDENCE: 95%
EVIDENCE: Name match (100%) + org field match + Gmail context (5 emails)
METHOD: Word-based search + org cross-reference + Gmail verification
```

---

## Important Reminders

1. **This is thoughtful investigation** - Not automatic pattern matching!
2. **Show your work** - Explain reasoning at each step
3. **Cross-reference** - One data point isn't enough for high confidence
4. **Be honest about uncertainty** - Use "needs_more_info" if evidence is weak
5. **Consider context** - ERA-related? Real person? Organizational junk?

---

## After Probing All Items

Create `probe_results_XXXXX.json` with:
```json
{
  "probed_at": "2025-10-20 00:15:00",
  "results": [
    {
      "name": "Moses GFCCA",
      "recommendation": "merge with: Moses Ojunju",
      "confidence": 95,
      "evidence": ["Name match 100%", "Org field: GFCCA", "5 Gmail emails"],
      "method": "Word search + org cross-ref + Gmail"
    }
  ]
}
```

Then tell user: "Probing complete! Review results in probe_results_XXXXX.json"
