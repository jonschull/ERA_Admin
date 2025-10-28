# Summary

**Document:** ERA Members Lacking Bios - Version 5
**Date:** October 27, 2025
**Status:** 🚀 Active - Ongoing enrichment

## Stats

- **Total ERA Members Needing Bios:** 49
- **With Bio Drafts:** 3
- **Removed This Iteration:** 5 APPROVED + 4 non-members

## Recent Changes

- ✅ **Anna Akpe, Celia Francis, Emmanuel Rengade, Jeremiah Agnew, Justin Ritchie** - Bios approved (pending quality fixes)
- 🗑️ **Jeremy Simon, Judith Rosen, Hilary Hart, Katharine King** - Non-members removed
- 📝 **Geodisio Castillo, Jennifer Koster** - New LinkedIn bios added
- 🔧 **In progress:** Fixing V4 quality issues (Jeremiah bio first-person, Emmanuel spelling, case corrections)

---

# Context

## Purpose

Complete member onboarding by enriching profiles and bios, preparing for public directory publication.

## ERA Member Definition

**CRITICAL:** A person is an ERA member if and only if:

1. They attended a Town Hall meeting (introduced, no objections, week passed), OR
2. Special decision from Jon Schull

**The database contains non-members.** We must verify Town Hall attendance before treating someone as a member.

## The ERA Onboarding Process

When someone becomes an ERA member:

1. ✅ **NOW:** Update profile in Database (Bio, email, phone, affiliated organizations)
2. **LATER:** Publish in public directory
3. **LATER:** Add to ERA Landscape visualization
4. **LATER:** Send welcome email (+ invite to become supporting member)
5. **LATER:** Add to Google Groups mailing lists

**Reality:** We've been sloppy. There's a backlog.

## Immediate Scope

**This integration focuses on steps 1-2:**

1. **Complete profiles** for members who attended Town Halls
   - Bios (contextual, personalized)
   - Email addresses
   - Phone numbers (where available)
   - Affiliated organizations
2. **Prepare for public directory publication** (human activates "Publish" field)

## Why Hand-Authored Bios

**Hand-authored bios work best** because they:

- Capture what makes each person unique to ERA
- Integrate professional background with ERA engagement
- Reflect actual contributions and interests discussed in Town Halls
- Avoid generic LinkedIn summary language

## Information Sources

1. **LinkedIn profiles** → Professional background (ADAPT when possible, don't copy-paste)
2. **Town Hall participation** (Fathom database) → Meeting attendance, engagement
3. **Town Hall transcripts** (era_townhalls_complete.md) → What they said, context, interests
4. **Other Fathom recordings** → When Town Hall context is inadequate
5. **Email search** (user's email) → Contact info, affiliated organizations, background
6. **Airtable** (people_export.csv) → Existing affiliations, projects, notes

## Approach: Intelligent Assistant Pattern

Following the participant_reconciliation model for **Human-AI Collaboration:**

1. AI identifies members needing profiles
2. Human provides LinkedIn URLs and flags members as "NEXT"
3. AI conducts multi-source research:
   - Read LinkedIn profile
   - Search Town Hall and other transcripts for mentions
   - Search user's email for contact info, org affiliations, background
   - Query Fathom database for participation details
4. AI compiles research notes with sources **inline in this document**
5. AI drafts complete profile updates:
   - Bio (personalized, contextual - not generic summaries)
   - Email address (from email search or existing data)
   - Phone number (if found in email)
   - Affiliated organizations (from email, LinkedIn, or existing data)
6. Human reviews, edits, approves (marks "APPROVED")
7. AI updates database for approved profiles
8. AI creates new numbered version removing completed members

**Eventually there will be no members left.**

## Procedural Guidelines

### 1. LinkedIn Profile Harvesting

- AI initiates rate-limit-aware scraping (10-15 second delays)
- Runs in background, monitored periodically
- Creates batch files with scraped profiles

### 2. Document Versioning

- Each iteration creates new numbered version: `...V2.md`, `...V3.md`, etc.
- Completed members are removed the NEXT VERSION OF THE  document when marked APPROVED
- Document versions shrink each iteration until empty

### 3. Member Verification

- Database contains non-members
- MUST verify Town Hall attendance before treating as member
- Remove flagged non-members immediately (with documentation)

### 4. Quality Control

- AI proposes, human edits, AI updates database
- No "bad apples" - fix issues permanently so they don't resurface
- Document fixes in PAST_LEARNINGS.md

### 5. Data Preservation

- When removing members, document WHY
- Database corrections (spelling, case, merges) done immediately
- All changes tracked AND REVERTABLE

## Key Principles

**1. Context-Rich Bios**

- NOT: Generic LinkedIn summary copy-paste
- YES: Curated for consistency of tone and relevance to ERA

**2. Prioritization**

- Act on those where action is clear
- Insert questions for those where you don't know what to do
- Human flags members as "NEXT" for AI to research

**3. Human Oversight**

- AI collects data, drafts bios
- Human edits and approves every bio
- AI learns from the process and improves

**4. Quality Over Speed**

- Intelligent solutions via intelligence, not scripts
- Thoughtful, personalized bios
- Multiple source synthesis
- Reflect actual ERA engagement

## Document Structure

For sidebar navigation, this document uses:

- **H1:** Summary, Context, Members Without Bios
- **H2:** Each member name (only H2 in sidebar for easy navigation)
- **Member sections:** Bio, Fields, Notes (bolded, not headers)

---

# Members Without Bios

## 1. Angelique Garcia NEXT

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Unknown

**Notes:**

_[No research notes yet]_

---

## 2. Arun Bangura

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 3. Aviv Green

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Founder of EcoNomads YouTube channel, involved in Pastoralist Savannah Restoration Center in Kenya

**Notes:**

_[No research notes yet]_

---

## 4. Byamukama nyansio APPROVED

**Bio:**

Byamukama Nyansio is a farmer and project planner at Bwindi Eco Farm and Batwa Village Experience in Kisoro, Uganda. He leads The Mindset Village Walk initiative, focused on community-based transformation, regenerative agriculture, and biodiversity conservation. His work includes fish farming extension services, pollinator conservation, and supporting sustainable livelihoods in the Bwindi region.

**Fields:**

- **Affiliation:** Gwindi EcoFarm, Ready for Change
- **LinkedIn:** https://www.linkedin.com/in/byamukama-nyansio-46a485292

**Notes:**

- LinkedIn: THE MINDSET VILLAGE WALK
- Bio drafted from LinkedIn profile

---

## 5. Chris Pilley

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Safari company, SOTOP camp

**Notes:**

- Research needed from ERA records

---

## 6. Delkhwa habibi

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research needed from ERA records

---

## 7. Dushime Ange Leo clevis

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 8. Elizabeth Morgan Tyler

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Activist, focused on water issues

**Notes:**

_[No research notes yet]_

---

## 9. Emmanuel URAMUTSE

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Environmental studies master's student
- **LinkedIn:** https://www.linkedin.com/in/emmanuel-uramutse-b18a53219

**Notes:**

- Database needs case correction DO THIS!!

---

## 10. Fadja Robert

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Not listed
- **LinkedIn:** https://www.linkedin.com/in/fadja-robert-carr-dha-5b0421154

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 11. Fred Ogden

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** NOAA
- **LinkedIn:** https://www.linkedin.com/in/fred-l-ogden-03078273

**Notes:**

_[No research notes yet]_

---

## 12. Gary Glass

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Unknown

**Notes:**

_[No research notes yet]_

---

## 13. Geodisio Castillo APPROVED

**Bio:**

Geodisio Castillo is a facilitator, researcher and planner at Centro de Desarrollo Ambiental y Humano (Center for Environmental and Human Development) in Panama. His work focuses on indigenous knowledge systems, climate-resilient agriculture, and biodiversity preservation, particularly with the Guna people of Gunayala, including research on traditional root and tuber crops as nature-based solutions to climate change.

**Fields:**

- **Affiliation:** Centro de Desarrollo Ambiental y Humano
- **LinkedIn:** https://www.linkedin.com/in/geodisio-castillo-52269728

**Notes:**

- LinkedIn: Facilitador, investigador y planificador en Centro de Desarrollo Ambiental y Humano
- Bio drafted from LinkedIn profile

---

## 14. Gwen

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

_[No research notes yet]_

---

## 15. Hadziqah

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Brunei

**Notes:**

_[No research notes yet]_

---

## 16. Hashim Yussif

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 17. Heraclio Herrera

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Congreso General Kuna (CUNA Institute)
- **LinkedIn:** https://www.linkedin.com/in/heraclio-herrera-r-b7b05531

**Notes:**

_[No research notes yet]_

---

## 18. Ilarion (3)

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- ⚠️ This has been fixed multiple times - verify carefully

---

## 19. Ivan Owen

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Social Glassa

**Notes:**

_[No research notes yet]_

---

## 20. Jennifer Koster APPROVED.

**Bio:**

Jennifer Koster is a serial entrepreneur and systems integrator transforming the global built environment through innovation, precision, and execution. As Founder and CEO of WerkWell Holdings, she leads a vertically integrated group of companies advancing circular construction, sustainable real estate, and next-generation infrastructure. She is also Co-Founder of LivWell, pioneering a wellness-driven development model rooted in regenerative systems and resilient design. She has led over $500M in executed projects across healthcare, hospitality, data centers, and residential real estate.

**Fields:**

- **Affiliation:** Workwall Project Services, Regenerative Communities
- **LinkedIn:** https://www.linkedin.com/in/jennifer-koster-a2b5331

**Notes:**

- LinkedIn: Serial Entrepreneur Re-Engineering How We Live, Work and Play
- Bio drafted from LinkedIn profile

---

## 21. Jerald Katch

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Retired, working with local arboretum

**Notes:**

_[No research notes yet]_

---

## 22. Juan Bernal

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Obama Fellow, Executive Director of Geiversity Panama's Ecological University

**Notes:**

- Collect info from ERA records

---

## 23. Julia Lindley

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Florida Oceanographic Society
- **LinkedIn:** https://www.linkedin.com/in/julialindley1

**Notes:**

_[No research notes yet]_

---

## 24. Kaluki Paul Mutuku

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/kaluki-paul-mutuku%F0%9F%95%8A-2a8400105

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 25. Kathia Burillo

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Imaginary
- **LinkedIn:** https://www.linkedin.com/in/kathia-burillo-r-a90a4576

**Notes:**

_[No research notes yet]_

---

## 26. Kevin A.

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Florida International University

**Notes:**

- Collect info from ERA records

---

## 27. Kevin Li

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** USDA (based in Penn State)

**Notes:**

- Verify Town Hall attendance/presentation

---

## 28. Lauren Miller

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Not listed

**Notes:**

- Research from ERA records needed

---

## 29. Lisa Merton

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Greenbelt Movement International

**Notes:**

- Verify Town Hall attendance/presentation

---

## 30. Malaika Patricia

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research from ERA records needed
- ERA Africa participant - check Africa Town Hall transcripts

---

## 31. Mary Ann Edwards

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Email:** maedwardsrn@gmail.com
- **Affiliation:** Unknown

**Notes:**

_[No research notes yet]_

---

## 32. Matthew Hooper

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Verify Town Hall attendance/presentation

---

## 33. Maxime Weidema

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/maxime-weidema-82863239

**Notes:**

- Verify Town Hall attendance/presentation

---

## 34. Minot Weld

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Hammerhead Capital
- **LinkedIn:** https://www.linkedin.com/in/minot-weld-921385223

**Notes:**

_[No research notes yet]_

---

## 35. Missy Lahren

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Earth Law Center
- **LinkedIn:** https://www.linkedin.com/in/missy-lahren-earthlawyer

**Notes:**

_[No research notes yet]_

---

## 36. Mr. Kipilangat Kaura -TAWI

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/kipilangat-kaura-2425702bb

**Notes:**

_[No research notes yet]_

---

## 37. Mtokani Saleh

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Agri-Hope, Initiative for Resilience

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 38. Munyembabazi Aloys

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research from ERA records needed
- ERA Africa participant - check Africa Town Hall transcripts

---

## 39. Mutasa Brian

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Email:** brianmutasa256@gmail.com
- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research from ERA records needed
- ERA Africa participant - check Africa Town Hall transcripts

---

## 40. Myra Jackson

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Unknown

**Notes:**

_[No research notes yet]_

---

## 41. Penny Heiple

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Unknown
- **LinkedIn:** https://www.linkedin.com/in/pennyheiple

**Notes:**

_[No research notes yet]_

---

## 42. Roberto Forte

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** SciTech
- **LinkedIn:** https://www.linkedin.com/in/roberto-forte-ph-d-ba2b2121

**Notes:**

_[No research notes yet]_

---

## 43. Roberto Pedraza Ruiz

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/roberto-pedraza-ruiz-281483166

**Notes:**

_[No research notes yet]_

---

## 44. Scott Schulte

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** University of Kansas
- **LinkedIn:** https://www.linkedin.com/in/scott-schulte-6a75a97

**Notes:**

_[No research notes yet]_

---

## 45. Steffie Rijpkema

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** FarmTree
- **LinkedIn:** https://www.linkedin.com/in/steffie-rijpkema-49b457105

**Notes:**

_[No research notes yet]_

---

## 46. Stella Nakityo

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research from ERA records needed

---

## 47. Theopista Abalo

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/theopistaabalo35

**Notes:**

_[No research notes yet]_

---

## 48. Wambui Muthee

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Greenbelt Movement

**Notes:**

_[No research notes yet]_

---

## 49. nding'a ndikon

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/nding-a-orkeyaroi-8a73081b7

**Notes:**

_[No research notes yet]_

---
