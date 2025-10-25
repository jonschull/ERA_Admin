# Phase 4B-2: Iterative Probing Workflow

**Goal:** Process 279 unenriched Fathom participants using iterative human-AI collaboration

---

## **The Workflow**

### **Round 1: Initial Review**

**1. Generate Table**
```bash
python3 integration_scripts/generate_phase4b2_table.py
```

**2. Review in Browser**
- Opens HTML table with 25 people (or current batch)
- Two checkboxes per person:
  - **Process This** - Auto-checked for high confidence (>80%)
  - **Probe** - Auto-checked for unclear cases

**3. Make Decisions**
You decide for each person:
- ✅ **Process This** - Clear case, handle it (merge/delete/add)
- 🔍 **Probe** - Unclear, needs investigation
- ⏭️ **Neither** - Skip for now, revisit later

**4. Export CSV**
- Click "Export to CSV" button
- Saves with ProcessThis and Probe flags

---

### **Round 2: Process & Probe**

**5. Run Processor**
```bash
python3 integration_scripts/process_phase4b2_round.py
```

**Shows:**
- ✅ Items marked for processing
- 🔍 Items marked for probing
- Saves probe_list_XXXXX.json

**6. Cascade Probes Unclear Cases**

**You ask in chat:**
> "Please probe the items in probe_list_20251020_0000.json"

**Cascade investigates MANUALLY and THOUGHTFULLY:**

**Example - Moses GFCCA:**
```
🔍 Probing Moses GFCCA...

1. Analysis:
   - "MOSES" appears to be a person's name
   - "GFCCA" is an organization acronym
   - Comma suggests: Person, Organization format

2. Airtable search for "Moses":
   - Moses Ojunju (100% match on "Moses")
   - Check organization field: "GFCCA" ✅

3. Gmail verification:
   - 5 emails found mentioning "Moses GFCCA"
   - Most say "Moses from GFCCA"
   - Context: Food security projects

4. Cross-reference:
   - Moses Ojunju works with GFCCA ✅
   - Same project areas ✅

RECOMMENDATION: merge with: Moses Ojunju
CONFIDENCE: 95%
EVIDENCE: Name match + org match + Gmail context
METHOD: word-match + cross-verification
```

**7. Cascade Regenerates Table**

After probing, Cascade creates new table with:
- **Processed items** - Removed (already handled)
- **Probed items** - Now show recommendations with confidence
- **Skipped items** - Still there, unchanged

**New table columns:**
- Probe Result
- Confidence
- Evidence
- Process This (re-evaluated based on probe)

---

### **Round 3+: Iterate Until Complete**

**8. Review Probe Results**
- Check Cascade's reasoning
- Agree/disagree with recommendations
- Mark "Process This" for good probes
- Mark "Probe Again" for questionable ones

**9. Repeat Process**
- Process approved items
- Re-probe flagged items
- Continue until all 25 done

---

## **Auto-Flagging Logic**

### **Process This** (Auto-Checked When):
- Airtable match with confidence ≥80%
- Clear merge or delete case

### **Probe** (Auto-Checked When):
- Not in Airtable BUT found in Gmail (real person?)
- Single name only (ambiguous)
- Has special chars: `,`, `.`, `(`, `www`, `Locations:` (messy data)
- In Airtable but low confidence <90% (verify match)

---

## **Cascade's Probing Process**

**Not automatic pattern matching - actual investigation:**

1. **Analyze name structure**
   - Identify person vs organization parts
   - Clean punctuation/formatting
   - Extract meaningful tokens

2. **Search variations**
   - Try full name
   - Try individual words
   - Try common variations (Mike/Michael)

3. **Cross-reference sources**
   - Airtable: fuzzy match + org field check
   - Gmail: search for context and mentions
   - Look for corroborating evidence

4. **Reason about confidence**
   - Strong evidence = high confidence
   - Weak/conflicting = low confidence
   - Show reasoning transparently

5. **Make recommendation**
   - Action: merge/add/delete/ignore
   - Matched name (if merge)
   - Confidence score
   - Evidence summary
   - Method used

---

## **Example Full Round**

**Start:** 25 people

**After Round 1 Review:**
- 15 checked "Process This" (clear cases)
- 7 checked "Probe" (unclear)
- 3 unchecked (skip for now)

**After Round 2 Processing:**
- 15 processed automatically ✅
- 7 probed by Cascade 🔍
- 3 deferred ⏭️

**Cascade's Probe Results:**
- 5 high confidence recommendations (merge/add)
- 2 low confidence (need more review)

**After Round 3 Review:**
- 5 checked "Process This" (accept Cascade's probes)
- 2 checked "Probe Again" (re-investigate)
- 3 still deferred

**After Round 4:**
- 5 more processed ✅
- 2 re-probed with different approach
- Eventually all 25 resolved

---

## **Files Generated**

Each round creates:
- `phase4b2_TEST_APPROVALS_YYYYMMDD_HHMM.html` - Review table
- `phase4b2_approvals_YYYYMMDD_HHMM.csv` - Your decisions
- `probe_list_YYYYMMDD_HHMM.json` - Items needing probing
- `probe_results_YYYYMMDD_HHMM.json` - Cascade's findings

---

## **Benefits**

1. **Efficient:** Clear cases processed immediately
2. **Thorough:** Unclear cases investigated properly
3. **Transparent:** You see Cascade's reasoning
4. **Iterative:** Refine until confident
5. **Collaborative:** Human judgment + AI investigation

---

## **Ready to Test**

The table is open in your browser with 25 people.

**Try the workflow:**
1. Review the table
2. Check/uncheck ProcessThis and Probe boxes
3. Export CSV
4. Run `process_phase4b2_round.py`
5. Ask Cascade to probe the flagged items
6. See how it works!
