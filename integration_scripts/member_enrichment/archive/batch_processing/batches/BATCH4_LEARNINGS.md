# Batch 4 Learnings

**Date:** October 26, 2025  
**Bios Reviewed:** 5 (Alex Carlin, Bill Reed, Eduardo Marino, Jim Bledsoe, Jimmy Pryor)  
**Method:** AI generated → Human edited → Diff analysis → Rule extraction

---

## Editorial Patterns Identified

### 1. Verb Softening
**Pattern:** "leads" → "promotes"  
**Rationale:** Don't embellish what we know. "Leads" implies organizational authority we can't verify from transcripts alone.  
**Rule:** Use "promotes/works on/focuses on" for unverified roles.

**Example:**
- ❌ "Alex Carlin leads ocean plankton restoration initiatives"
- ✅ "Alex Carlin promotes ocean plankton restoration initiatives"

---

### 2. Remove ERA Process Details
**Pattern:** Deleted "attended Town Hall on [date]", "introduced by [person]"  
**Rationale:** Focus on their work, not ERA metadata. Makes bios feel less insular, more professional.  
**Exception:** If Town Hall presentation IS their defining achievement (no other verified work).

**Examples:**
- ❌ "Introduced to ERA by Russ Spear in May 2024"
- ❌ "attended ERA's August 2024 Town Hall, connecting"
- ❌ "His participation in ERA's January 2024 Town Hall connected him..."
- ✅ [Just describe their work without the ERA process]

---

### 3. Remove Future Projections
**Pattern:** Deleted "upcoming project will..."  
**Rationale:** Stick to what's already done/happening. Future plans may not materialize, bio becomes dated.

**Example:**
- ❌ "His upcoming project will film the anthem with African singing stars"
- ✅ [Only mention completed work or current ongoing projects]

---

### 4. Remove ERA Meta-Commentary
**Pattern:** Deleted "reflects ERA's recognition that..."  
**Rationale:** No ERA posturing. Let their work speak for itself.

**Example:**
- ❌ "Jim's participation reflects ERA's recognition that restoration requires diverse skills"
- ✅ [Let Jim's work speak without ERA commentary]

---

### 5. Add Specificity When Context Supports
**Pattern:** "designer" → "landscape designer"  
**Rationale:** When context (Napa wine country + regenerative systems) clearly suggests specialty, add it.

**Example:**
- ❌ "Jim Bledsoe is a designer"
- ✅ "Jim Bledsoe is a landscape designer"

---

### 6. Cut Unverified Speculation
**Pattern:** Removed entire sentences about skills not verified in transcripts.  
**Rationale:** If no speaking turns in transcripts, don't speculate about "visual communication, systems thinking."

**Example:**
- ❌ "His professional background in design offers perspectives on visual communication, systems thinking, and spatial planning for ecosystem recovery."
- ✅ [Cut - these skills aren't verified from any source]

---

## Changes Applied to Each Bio

### Alex Carlin (3 changes)
1. "leads" → "promotes" (verb softening)
2. Deleted "Introduced to ERA by Russ Spear in May 2024" (ERA process)
3. Deleted "His upcoming project will film..." (future projection)

### Bill Reed (1 change)
1. "attended ERA's August 2024 Town Hall, connecting" → "Bill connects" (removed date, made timeless)

### Eduardo Marino (1 change)
1. "presented... at ERA's June 2025 Town Hall. His project addresses" → "proposes... to address" (removed TH mention, past→present)
2. Note: Typo in edit - "sicne" should be "since"

### Jim Bledsoe (3 changes)
1. "designer" → "landscape designer" (added specificity)
2. Deleted speculation about visual communication/systems thinking (unverified)
3. Deleted ERA meta-commentary sentence (posturing)

### Jimmy Pryor (1 change)
1. Deleted entire sentence about "participation in ERA's January 2024 Town Hall connected him..." (ERA process)

---

## Rules to Apply Going Forward

### ✅ DO:
- Use "promotes/works on/focuses on" for unverified leadership
- Make bios timeless (present tense, no dates)
- Focus on their work, not ERA process
- Add specificity when context clearly supports it
- Cut sentences that don't add verified value

### ❌ DON'T:
- Use "leads/spearheads/pioneers" without verification
- Include "attended Town Hall" or "introduced by" details
- Include future projections
- Add ERA meta-commentary
- Speculate about skills not in sources

### EXCEPTION:
- If Town Hall presentation IS the defining achievement (only verified work), mention it:
  - "John presented his watershed restoration framework at ERA"

---

## Questions Still Open

1. **Future projects:** Completely banned? Or okay if imminent/funded/concrete?
2. **Typos in feedback:** Should AI flag them for correction or assume human will catch?
3. **Inference boundaries:** What level of context-supported inference is acceptable?
   - Example: Napa + regenerative → "landscape designer" was okay
   - When would this NOT be okay?

---

## Impact on Next Batch

**Batch 5 should:**
1. Default to softer verbs (promotes, works on, focuses on)
2. Skip all ERA process details by default
3. No future tense project claims
4. No ERA commentary layer
5. Only add specificity when context is clear
6. Cut aggressively when skills aren't verified

**This should result in:**
- Shorter, tighter bios (less cruft)
- More factual (less embellishment)
- More professional (less insular ERA focus)
- More timeless (no dates)

---

## Files Updated

- `CONTEXT_RECOVERY.md` - Added Batch 4 learned rules to section 4B
- `BATCH4_LEARNINGS.md` - This document (for future reference)

---

## Next Steps

1. Fix typo in batch4_review.JS.md (sicne → since)
2. Apply these rules to Batch 5 generation
3. Continue feedback loop to refine further
