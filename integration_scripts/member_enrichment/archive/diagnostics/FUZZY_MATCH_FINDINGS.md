# Fuzzy Match Analysis: ERA Africa Transcripts vs V6 Members

**Date:** October 27, 2025  
**Method:** Fuzzy string matching between all transcript speakers and V6 member names

---

## Summary

- **V6 Members Analyzed:** 36
- **Transcript Speakers Found:** 59
- **Exact/High Matches Found:** 5
- **New Potential Members to Investigate:** 4

---

## ✅ CONFIRMED MATCHES (Already in V6)

### 1. Hashim Yussif
- **Transcript Name:** Hashim Yussif (152 mentions)
- **Similarity:** 1.000 (exact match)
- **Status:** ✅ Already enriched and marked APPROVED

### 2. Mtokani Saleh  
- **Transcript Names:** 
  - Mtokani Saleh (127 mentions, 1.000 similarity)
  - Mtokani (193 mentions, 0.950 similarity)
- **Total Mentions:** 320
- **Status:** ✅ Already enriched and marked APPROVED
- **Note:** "Mtokani" is shortened form used in earlier meetings

### 3. Mutasa Brian
- **Transcript Name:** MUTASA BRIAN (283 mentions)
- **Similarity:** 1.000 (exact match, case variation)
- **Status:** ⚠️ IN V6 but NOT YET ENRICHED
- **Action Needed:** Should extract bio information from 283 mentions

### 4. Kaluki Paul Mutuku
- **Transcript Name:** Kaluki Paul Mutuku (7 mentions)
- **Similarity:** 1.000 (exact match)
- **Status:** ⚠️ IN V6 but only 7 mentions (limited data)
- **Note:** Also fuzzy matched to "Edward Paul Munaaba" (0.750) - sharing "Paul" - NOT same person

---

## 🔍 POTENTIAL NEW MEMBERS TO INVESTIGATE

High-frequency African speakers NOT currently in V6:

### 1. Edward Paul Munaaba ⭐⭐⭐
- **Mentions:** 525 (5th most frequent speaker!)
- **Context:** ERA Africa participant, appears throughout transcripts
- **Recommendation:** HIGH PRIORITY - extract bio
- **Note:** Very active participant, likely ERA member

### 2. Leonce Bulonze ⭐⭐
- **Mentions:** 239 (15th most frequent)
- **Context:** ERA Africa participant, mentioned as inviting Emmanuel URAMUTSE
- **Recommendation:** MEDIUM PRIORITY - extract bio
- **Note:** Active connector/coordinator

### 3. mbilizi Kalombo / MBILIZI KALOMBO ⭐⭐
- **Mentions:** 314 + 23 = 337 total (case variations)
- **Context:** ERA Africa participant
- **Recommendation:** MEDIUM PRIORITY - extract bio
- **Note:** Significant participation

### 4. Moses Ojunju / MOSES, GFCCA ⭐
- **Mentions:** 46 + 202 = 248 total
- **Context:** GFCCA affiliation, ERA Africa participant
- **Recommendation:** MEDIUM PRIORITY - check if already in main database
- **Organization:** GFCCA (Global Faith Climate Change Alliance?)

### 5. Joshua Laizer ⭐
- **Mentions:** 59
- **Context:** Arusha, Tanzania - ERA Africa participant
- **Recommendation:** LOW PRIORITY (already noted in nding'a's bio)
- **Note:** Potential connection to nding'a (Laizer) Orkeyaroi - needs investigation

### 6. Folorunsho DAyo Oluwafemi / Folorunsho Dayo Oluwafemi
- **Mentions:** 133 + 10 = 143 total
- **Context:** ERA Africa participant
- **Recommendation:** LOW PRIORITY
- **Note:** Moderate participation

### 7. Ansiima Casinga Rolande
- **Mentions:** 84
- **Context:** ERA Africa participant
- **Recommendation:** LOW PRIORITY

### 8. Byamukama nyansio
- **Mentions:** 78
- **Context:** ERA Africa participant
- **Recommendation:** LOW PRIORITY

### 9. john Magugu
- **Mentions:** 44
- **Context:** ERA Africa participant
- **Recommendation:** LOW PRIORITY

### 10. Enoch M. Totimeh
- **Mentions:** 34
- **Context:** ERA Africa participant  
- **Recommendation:** LOW PRIORITY

### 11. Sumaidi Angale
- **Mentions:** 31
- **Context:** ERA Africa participant
- **Recommendation:** LOW PRIORITY

---

## 🚫 FALSE POSITIVE (Not Same Person)

### Ivan Owen vs Diana Doheny
- **Fuzzy Match:** 0.667 similarity
- **Status:** NOT SAME PERSON (coincidental word overlap)
- **Action:** Ignore

---

## 📊 HIGH-PRIORITY ACTIONS

### Immediate Actions:

1. **MUTASA BRIAN** (283 mentions) ✅ IN V6
   - Extract bio information from transcripts
   - Add italicized enrichments
   - Mark as APPROVED

2. **Edward Paul Munaaba** (525 mentions) ⚠️ NOT IN V6
   - Check if in main ERA database
   - If not, consider adding (5th most frequent speaker!)
   - Extract comprehensive bio from transcripts

3. **Leonce Bulonze** (239 mentions) ⚠️ NOT IN V6
   - Check if in main ERA database
   - Active connector/coordinator
   - Extract bio information

4. **mbilizi Kalombo** (337 total mentions) ⚠️ NOT IN V6
   - Check if in main ERA database
   - Extract bio information

---

## 📋 V6 MEMBERS NOT FOUND IN TRANSCRIPTS

The following V6 members had **0 transcript mentions** (confirmed from earlier analysis):

- Fadja Robert
- Theopista Abalo
- Kipilangat Kaura
- Wambui Muthee
- (Plus ~25+ others with no transcript presence)

**Note:** These may be:
- Town Hall participants only
- Inactive ERA Africa members
- Members who joined after transcript period
- Name spelling variations not caught by fuzzy matching

---

## 🎯 RECOMMENDED NEXT STEPS

1. **Extract bio for MUTASA BRIAN** (already in V6, 283 mentions)
2. **Investigate Edward Paul Munaaba** (525 mentions - very high!)
3. **Investigate Leonce Bulonze** (239 mentions - key connector)
4. **Investigate mbilizi Kalombo** (337 mentions)
5. **Check if Moses Ojunju/MOSES GFCCA** is already in main database

---

## 🔧 METHODOLOGY NOTES

**Fuzzy Matching Algorithm:**
- Exact match: 1.000
- Substring match: 0.950
- Word overlap: 0.700-0.950 (Jaccard similarity)
- String similarity: 0.000-1.000 (SequenceMatcher)
- **Threshold:** 0.650

**Quality Control:**
- Case-insensitive matching
- Removed noise (Dr., Mr., punctuation)
- Considered word-level overlaps
- Avoided false positives from coincidental similarity

