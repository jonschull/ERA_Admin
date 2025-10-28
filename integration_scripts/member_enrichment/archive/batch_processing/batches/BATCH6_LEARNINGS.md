# Batch 6 Learnings

**Date:** October 26, 2025  
**Bios Reviewed:** 5 (Charles, Jacob, Mark, Mary, Rayan)  
**Method:** AI generated → Human flagged errors → AI researched & corrected

---

## CRITICAL LEARNING: DATABASE CAN BE COMPLETELY WRONG

**Problem:** Trusted database descriptions without verification  
**Impact:** Generated completely fictional bios for 2 members

---

## Major Issues Identified

### 1. **Charles Eisenstein - Database Fiction**
**Database said:** "Decentralized water consultant, Abundant Earth Foundation"  
**Reality:** Famous author ("Sacred Economics", "Climate: A New Story"), cultural philosopher

**How I should have known:**
- Name "Charles Eisenstein" is well-known in regenerative/environmental circles
- Should have done web search before trusting minimal database description
- No LinkedIn found should have triggered research, not acceptance

**Corrected bio:** 658 chars based on Wikipedia research
- Author of multiple influential books on gift economics, interbeing, climate narratives
- Yale graduate in Mathematics and Philosophy
- Challenges separation worldview, proposes sacred economics

---

### 2. **Mark Luckenbach - Database Complete Fabrication**
**Database said:** "Long Island south of Connecticut... behavior change programs"  
**Reality:** Marine ecologist, Associate Dean at Virginia Institute of Marine Science, 35+ years shellfish restoration

**How I should have known:**
- Email `luck@vims.edu` → VIMS = Virginia Institute of Marine Science
- Should have searched "Mark Luckenbach VIMS LinkedIn" immediately
- Geographic mismatch: Connecticut vs. Virginia

**Corrected bio:** 490 chars verbatim from LinkedIn
- Marine ecologist specializing in shellfish restoration
- Former Director of VIMS Eastern Shore Laboratory (21 years)
- Associate Dean of Research and Advisory Service

**User question:** "Where did the Connecticut behavior/change story come from?"
**Answer:** Complete fiction in the database. No idea where it originated.

---

### 3. **Rayan Farhoumand - Database Membership Flag Wrong**
**Database said:** `era_member: false`  
**Reality:** ERA Intern (listed in Town Hall agendas)

**How I found the truth:**
- User said: "he IS (or should be) an ERA member, and he has introduced himself at past meetings"
- Searched Town Hall agendas for "Rayan"
- Found: "Rayan Farhoumand, ERA Intern" in May 2024 Town Hall

**Learning:** `era_member` field can have false negatives. Always verify against Town Hall agendas if user challenges.

---

### 4. **Mary Minton - Minor Edit**
**Change:** "an observer focused on restoration," → "interested in restoration. She"
**Pattern:** Simpler, more direct language

---

## NEW VERIFICATION PROTOCOL

### **When to NOT trust database:**

1. **Email domain suggests institutional affiliation**
   - `.edu` email → Research the institution
   - Example: `luck@vims.edu` → Should have searched "VIMS" immediately

2. **Name matches well-known figure**
   - "Charles Eisenstein" → Famous author → Web search required
   - Don't assume database knows who they are

3. **Database description is minimal/generic**
   - "Decentralized water consultant" for a famous author = red flag
   - Minimal info likely means database doesn't know them

4. **Geographic inconsistencies**
   - Email says Virginia, database says Connecticut → Verify

5. **Membership flag contradicts context**
   - Listed in Town Hall agendas but `era_member: false` → Check agendas

---

## THE VERIFICATION WORKFLOW

### **Step 1: Check Email Domain**
```
.edu email → Identify institution → Search LinkedIn with institution name
.org email → Identify organization → Research role
Famous-sounding name → Web search first
```

### **Step 2: Web Search for Well-Known Names**
```
If name appears in regenerative/environmental circles:
1. Search "[Name] bio"
2. Check Wikipedia
3. Check official website
4. Use verified bio, not database fiction
```

### **Step 3: Cross-Reference Town Hall Agendas**
```
If era_member flag seems wrong:
1. grep Town Hall agendas for name
2. Check "Present:" lists
3. Check agenda intro sections
4. Verify actual participation
```

### **Step 4: When Database Seems Wrong, VERIFY**
```
Don't trust database descriptions blindly
Especially for:
- Well-known individuals
- Institutional emails (.edu, .gov)
- Minimal descriptions
- Geographic inconsistencies
```

---

## Changes Applied to Each Bio

### Charles Eisenstein
- **REWROTE COMPLETELY** from Wikipedia
- Database description was 100% wrong
- New bio: 658 chars covering his books, philosophy, key themes

### Jacob Denlinger
- ✅ No changes (approved as written)
- Used transcript data well

### Mark Luckenbach  
- **REWROTE COMPLETELY** from LinkedIn
- Database description was 100% fiction
- New bio: 490 chars verbatim from his LinkedIn About section

### Mary Minton
- Minor simplification of language
- Removed "an observer focused on" → "interested in"

### Rayan Farhoumand
- **CORRECTED membership status**
- Found he was ERA Intern in Town Hall agendas
- Rewrote bio to reflect internship

---

## Rules to Apply Going Forward

### ✅ ALWAYS VERIFY when:

1. **Email has institutional domain** (.edu, .org, .gov)
   → Search "[Name] [Institution] LinkedIn"

2. **Name sounds well-known**
   → Web search before trusting database

3. **Database description is minimal**
   → Probably incomplete, research further

4. **Geographic mismatch**
   → Email says one location, database says another

5. **era_member flag seems questionable**
   → Search Town Hall agendas for "[Name]"

### ✅ RESEARCH SOURCES (in order):

1. Web search for well-known names
2. LinkedIn direct search (not just fuzzy matching)
3. Town Hall agendas (grep for name)
4. Database (least reliable for details)

### ❌ DON'T TRUST DATABASE BLINDLY

- Database can be completely wrong
- Database descriptions may be outdated
- Database may not know who famous people are
- Always verify against external sources

---

## Impact on Future Batches

**Batch 7+ must:**
1. Check email domains FIRST (before trusting database)
2. Web search any well-known or famous-sounding names
3. Never trust database for institutional affiliations
4. Cross-reference Town Hall agendas when membership unclear
5. Use external verification as primary source

**This prevents:**
- Fictional bios for well-known individuals
- Wrong institutional affiliations
- Missed interns/members due to database flags
- Embarrassing errors ("water consultant" for famous author)

---

## Technical Debt Identified

**Database Cleanup Needed:**
1. Charles Eisenstein - completely wrong description
2. Mark Luckenbach - completely wrong description + location
3. Rayan Farhoumand - wrong `era_member` flag

**Question:** Where did these wrong descriptions come from? Data entry errors? Automated imports gone wrong?

---

## Files Updated

- `batch6_review.AI.md` - Corrected with research
- `batch6_review.JS.md` - User's corrections + my research
- `BATCH6_LEARNINGS.md` - This document

---

## Success Metrics

**Batch 5 → Batch 6:**
- ✅ Applied all previous rules (no "leads", no TH mentions, verbatim LinkedIn)
- ✅ Caught database errors through user feedback
- ✅ Researched and corrected all errors
- ❌ Should have caught database errors BEFORE generating bios
- ❌ Should have verified institutional emails immediately

**Key lesson:** Database is NOT ground truth. External verification required for:
- Well-known individuals
- Institutional affiliations
- Minimal descriptions

**New workflow:** Email domain → Web search → LinkedIn → Town Hall agendas → Database (last resort)
