# AI Assistant Context Recovery - Phase 4B-2 Participant Reconciliation

**Last Updated:** 2025-10-23
**Status:** Active workflow - 280 participants remaining

---

## 🎯 PRIMARY OBJECTIVE

Reconcile 650+ Fathom participant names with the ERA Airtable database using AI-human collaboration.

**NOT automation.** This is:
- AI makes intelligent recommendations
- Human reviews and teaches
- AI learns and improves judgment
- Human maintains control

---

## 📋 THE WORKFLOW (CRITICAL - READ FIRST)

### **Step 1: AI Generates HTML Report**
```bash
python3 generate_batch_CANONICAL.py
# Then investigate items and update /tmp/batch_intermediate.json
python3 generate_html_from_intermediate.py
```

**Before generating, AI MUST:**
1. ✅ Read `PAST_LEARNINGS.md` for known patterns
2. ✅ Query Airtable for each participant (get full canonical names)
3. ✅ Gather ALL evidence:
   - 🎥 Fathom recording links (from DB)
   - 📧 Gmail query links (generated)
   - 📅 Town Hall links (from database)
4. ✅ Apply intelligent pattern matching (see below)

**Output:** HTML with recommendations + complete evidence

#### **🔍 CRITICAL: AI MUST REVIEW OWN WORK BEFORE PRESENTING**

**SELF-PROMPT FOR CLAUDE:**

After generating HTML, **STOP**. Do NOT present it yet. Instead:

1. **Open the HTML you just generated** and read through decisions
2. **Ask yourself for EACH decision:**
   - "Did I actually READ the Town Hall agenda, or just check if it exists?"
   - "Did I actually EXTRACT the organization from the Fathom title?"
   - "Would the user complain this is vague or incomplete?"
   - "Is this a single name I should have found the full name for?"

3. **Look for these RED FLAGS:**
   - ❌ "add to airtable (Town Hall participant)" without full name
   - ❌ "add to airtable" without "as [specific name]"
   - ❌ Single lowercase names being added (sasi, pedro, etc.)
   - ❌ Device names not converted to person names
   - ❌ Missing organization context when it's available
   - ❌ "She's IN Airtable" situations (claiming no match when person exists)

4. **If you find ANY red flags:**
   - Go back and ACTUALLY read the sources
   - Extract the real information
   - Fix the decisions
   - Regenerate HTML
   - **Review again** until clean

5. **Only when you find ZERO issues** that user would complain about → Present HTML

**Why this matters:** You tend to show progress checkmarks (✅ TH Agenda) without actually extracting information. This self-review forces you to catch your own shortcuts before the user sees them.

### **Step 2: Human Reviews HTML**
- Click evidence links to verify
- Uncheck "Approve" if wrong
- Add feedback/corrections in comments
- Export to CSV (path copies to clipboard)

### **Step 3: Human Sends CSV Back**
- AI reads ALL comments (even if approved)
- AI learns from corrections
- AI updates PAST_LEARNINGS.md

### **Step 4: AI Processes Approved Actions**
```bash
python3 execute_phase4b2_actions.py
```
- **Creates automatic backup BEFORE any changes**
- Executes merges, adds, drops
- Updates Fathom database
- Adds to Airtable (automated via add_to_airtable module)

#### **🔒 AUTOMATIC BACKUPS**

**Location:** `/Users/admin/ERA_Admin/FathomInventory/backups/`

**Format:** `fathom_emails.backup_YYYYMMDD_HHMM.db`

**Created:** Automatically before EVERY execution of `execute_phase4b2_actions.py`

**How to Restore from Backup:**

If you need to undo changes (e.g., accidentally dropped records):

1. **Find the relevant backup:**
   ```bash
   ls -lht /Users/admin/ERA_Admin/FathomInventory/backups/*.db | head -5
   ```

2. **Extract records from backup:**
   ```sql
   sqlite3 /path/to/backup.db
   SELECT * FROM participants WHERE name = '[name to restore]';
   ```

3. **Restore to current database:**
   ```sql
   sqlite3 /Users/admin/ERA_Admin/FathomInventory/fathom_emails.db
   INSERT INTO participants (...) VALUES (...);
   -- Or use ON CONFLICT to merge
   ```

**Example Recovery:**
- Batch 8: Accidentally dropped "Restor Eco" 
- Found backup: `backups/fathom_emails.backup_20251023_1950.db`
- Restored record as "Gwynant Watson" with Fathom call URL preserved

**⚠️ Important:** Backups are your safety net - they're created automatically every time, so you can always recover from mistakes!

### **Step 5: Repeat for Next Batch**
- 50 participants at a time
- Each batch improves AI judgment

---

## 🧠 AI JUDGMENT RULES (APPLY EVERY TIME)

### **1. Check PAST_LEARNINGS.md FIRST**
**Location:** `/Users/admin/ERA_Admin/integration_scripts/PAST_LEARNINGS.md`

Contains:
- Phone numbers → people mappings
- Organizations → people mappings  
- Name variants → canonical names
- Critical patterns learned from user feedback

**ALWAYS check this before making any decision.**

### **2. Query Airtable for Full Canonical Names**
```python
# WRONG
decision = "merge with: Billimarie"

# RIGHT
decision = "merge with: Billimarie Lubiano Robinson"
```

**Process:**
- Query Airtable CSV for exact match
- If found: use FULL canonical name from Airtable
- If fuzzy match (85%+): suggest with confidence note
- If not found: recommend "add to airtable as [name]"

### **3. Pattern Recognition**

#### **Person in Parentheses**
```
"Bio4Climate1 (Beck Mordini)" → Extract: Beck Mordini
"Cosmic Labyrinth (Indy Boyle-Rhymes)" → Extract: Indy Boyle-Rhymes
"Aimee Samara (Krouskop)" → Base name: Aimee Samara
```

#### **Number Variants**
```
"Name (2)", "Name (4)", "Name (7)" → Same person as "Name"
ALWAYS merge with base name
```

#### **Comma Patterns** (CRITICAL - Often wrong!)
```
"Name, City, State" → Location metadata (merge with Name)
"Organization, Person" → Extract Person

Examples:
"Charlie Shore, Gaithersburg, MD" → merge with Charles Shore
"Agri-Tech Producers LLC, Joe James" → add/merge Joe James
```

#### **Username Patterns**
```
"andreaseke" → Andreas Eke (check Fathom, don't auto-drop)
"afmiller09" → Check Fathom for context
```

#### **Device Names**
```
"Andres's iPhone (2)" → Check past learnings (may be Andres Garcia)
"Lastborn's Galaxy A11" → Check past learnings (may be Ilarion Merculief)

DON'T auto-drop - check past rounds first!
```

#### **Geographic Metadata**
```
"aniqa Locations: Bangladesh, Egypt, Sikkim" → Person is "aniqa"
"Locations:" is metadata, not a person name
```

### **4. Confidence Levels**

**HIGH Confidence** (auto-approve):
- Found in PAST_LEARNINGS.md
- Exact match in Airtable
- 3+ Town Hall meetings
- Clear number variants
- Phone numbers from past rounds

**MEDIUM Confidence** (needs review):
- 1-2 Town Hall meetings
- Fuzzy Airtable match (85-95%)
- Partial context
- User comments suggest identity

**LOW/DROP**:
- No Town Hall presence
- No Gmail context
- Device names (unless identified in past)
- System accounts (admin, etc.)

---

## 📊 EVIDENCE REQUIREMENTS (NEVER FORGET THESE)

**Every HTML report MUST include for EVERY participant:**

### **1. Fathom Recording Links** 🎥
```python
def get_fathom_links(name):
    # Query: SELECT DISTINCT source_call_url FROM participants WHERE name = ?
    # Return: <a href="{url}">🎥</a> links (up to 5)
```

### **2. Gmail Query Link** 📧
```python
def get_gmail_link(name):
    return f"https://mail.google.com/mail/u/0/#search/{name.replace(' ', '%20')}"
```

### **3. Town Hall Links** 📅
```python
def get_townhall_links(name):
    # Query town_hall_agendas table for meeting dates
    # Return: Links to Google Doc with date anchors
```

### **4. Airtable Status** 📋
```
✓ In Airtable (canonical name)
✗ Not in Airtable
⚠️ Possible match: [names]
```

**If ANY of these are missing → REGRESSION. Review this document.**

---

## ⚠️ COMMON MISTAKES TO AVOID

### **1. "Check if already in Airtable"**
❌ **WRONG:** Saying this in the HTML
✅ **RIGHT:** Actually query Airtable BEFORE generating HTML

### **2. Forgetting Evidence Links**
❌ **WRONG:** Missing Fathom, Gmail, or Town Hall links
✅ **RIGHT:** ALL three always present

### **3. Short Names**
❌ **WRONG:** "merge with: Billimarie"
✅ **RIGHT:** "merge with: Billimarie Lubiano Robinson"

### **4. Auto-Dropping Usernames**
❌ **WRONG:** "afmiller09" → drop (username)
✅ **RIGHT:** Check Fathom recordings for real person

### **5. Misreading Comma Patterns**
❌ **WRONG:** "Charlie Shore, Gaithersburg, MD" → add as MD
✅ **RIGHT:** This is location data, merge with Charles Shore

### **6. Generating Code On The Fly**
❌ **WRONG:** Writing new HTML generator each time
✅ **RIGHT:** Use generate_html_from_intermediate.py (standard tool)

---

## 🔄 PROCESS CHECKPOINTS

### **Before Generating HTML:**
- [ ] **🔒 USE THE CANONICAL PIPELINE ONLY** - DO NOT create new scripts
  - Script: `generate_batch_CANONICAL.py` (forces safeguards)
  - NEVER bypass by writing new scripts
  - The pipeline has mandatory checkpoints you cannot skip
- [ ] **READ PAST_LEARNINGS.md COMPLETELY** (not just load in script)
  - **INTERNALIZE the patterns** - script can only match exact strings
  - **YOU (Claude) recognize variations** - "bk" = Brian Krawitz pattern
  - **Organization comma patterns** need YOUR intelligence to extract person
  - Scripts are dumb; YOU are smart - act like it
- [ ] Read this document (AI_ASSISTANT_CONTEXT_RECOVERY.md)
- [ ] The canonical script will:
  - Strip number variants (3), (10) before fuzzy matching
  - Filter already-processed items (no repeats)
  - Check Airtable with base names
  - STOP and force you to review NEEDS_REVIEW items
- [ ] You MUST review items with intelligence:
  - Check Town Hall agendas for initials (JS, MC)
  - Apply username patterns (georgeorbelian → George Orbelian)
  - Use PAST_LEARNINGS for single names (jon, juliet)
  - Check organization patterns

### **During HTML Generation:**
- [ ] Include ALL evidence links (Fathom, Gmail, Town Hall)
- [ ] Use full canonical Airtable names
- [ ] Apply confidence levels correctly
- [ ] Export button copies path to clipboard

### **After User Feedback:**
- [ ] Read ALL comments (even if approved)
- [ ] **UPDATE PAST_LEARNINGS.md IMMEDIATELY** with:
  - New phone numbers → people mappings
  - New organization → person identifications
  - New name variants discovered
  - New patterns learned (IP addresses, usernames, etc.)
  - Any mistakes you made (so you don't repeat them)
- [ ] Document mistakes in this file
- [ ] Process approved actions
- [ ] **CRITICAL:** If people keep coming back (like "aniqa"), investigate why validation isn't working

---

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `PAST_LEARNINGS.md` | Phone numbers, organizations, name variants |
| `AI_ASSISTANT_CONTEXT_RECOVERY.md` | This file - the process |
| `generate_html_from_intermediate.py` | HTML generator from intermediate JSON |
| `execute_phase4b2_actions.py` | Processes approved actions |
| `add_to_airtable.py` | Automated Airtable additions |

---

## 🎓 LEARNING HISTORY

### **Batch 1 (50 items)**
- ✅ Phone numbers mapped to people
- ✅ Organizations mapped to representatives
- ✅ Name variants recognized
- ❌ Regression: Forgot Fathom links initially

### **Batch 2 (50 items, 19 processed so far)**
- ✅ Fixed: Added Fathom links back
- ❌ Regression: Forgot Gmail and Town Hall links
- ✅ Learned: Person in parentheses extraction
- ✅ Learned: Location vs organization comma patterns
- ✅ Learned: Full canonical names required
- ✅ Learned: Don't auto-drop usernames
- ⚠️ Created this document to prevent future regressions

**Remaining:** 280 participants (5-6 more batches)

---

## 🚨 IF YOU FORGET SOMETHING

**Read this checklist:**
1. Did you read PAST_LEARNINGS.md before deciding?
2. Did you query Airtable for full canonical names?
3. Did you include Fathom links for every participant?
4. Did you include Gmail query links for every participant?
5. Did you include Town Hall links where available?
6. Did you check for person names in parentheses?
7. Did you distinguish location vs organization commas?

**If NO to any → Go back and fix it.**

---

## 💡 WHY THIS WORKFLOW

**User's feedback:**
- "You lose the larger picture in your context memory"
- "Every name came from a Fathom recording - provide links"
- "That's what YOU should have done before generating the HTML"
- "You should be able to catch this" (person in parentheses)

**This document exists because:**
- Long conversations → context loss
- Multiple batches → need consistency
- User's time is valuable → no regressions
- Learning compounds → each batch better than last

---

## ✅ SUCCESS CRITERIA

**A good batch means:**
1. User reviews HTML in < 30 minutes
2. Few corrections needed (judgment improving)
3. All evidence links work
4. No regressions from previous batches
5. User learns I'm getting better, not forgetting basics

**End goal:**
- All 650+ participants reconciled
- High-quality Airtable data
- AI that learned the patterns
- Process documented for future use

---

**REMINDER: Read this document EVERY TIME before generating a new batch.**
