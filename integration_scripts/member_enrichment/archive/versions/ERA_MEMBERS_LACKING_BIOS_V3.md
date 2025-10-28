# Summary

**Document:** ERA Members Lacking Bios - Version 3
**Date:** October 27, 2025
**Status:** 🚀 Active - Research in progress

## Stats

- **Total ERA Members Needing Bios:** 61
- **With LinkedIn URLs:** 27
- **With Bio Drafts:** 5  (3 new drafts)
- **Flagged as Non-Members:** 3 (need removal)

## Recent Changes

- ✅ **Jorge Sendero** - Bio completed and added to database (name corrected from George)
- 🔬 **Abbie Dusseldorp, Adela Castro, Alisa Keesey** - Research completed, bio drafts added

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

## Data Sources (File Paths)

- **Airtable:** `/Users/admin/ERA_Admin/airtable/people_export.csv`
- **Database:** `/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db`
- **Town Hall Transcripts:** `/Users/admin/ERA_Admin/fathom/output/era_townhalls_complete.md`
- **Other Transcripts: accessible via the Fathom API**
- **Email Archive:** Gmail search (contact info, affiliations, background)

## Document Structure

For sidebar navigation, this document uses:

- **H1:** Summary, Context, Members Without Bios
- **H2:** Each member name (only H2 in sidebar for easy navigation)
- **Member sections:** Bio, Fields, Notes (bolded, not headers)

---

# Members Without Bios

## 1. Abbie Dusseldorp APPROVED

**Bio:**

Abigail (Abbie) Dusseldorp is Director of Development and Communications at Groundwork USA, a national network advancing environmental justice and equity in underserved communities.

**Fields:**

- **Affiliation:** Groundwork USA
- **LinkedIn:** https://www.linkedin.com/in/abigail-dusseldorp-10a58964

**Notes:**

- LinkedIn: Director of Development and Communications at Groundwork USA
- Database: Attended 'Groundwork.us' call (https://fathom.video/calls/22592996)
- No mentions in Town Hall transcripts - likely attended focused meetings
- Affiliation confirmed: Groundwork USA

---

## 2. Adela Castro APPROVED

**Bio:**

Adela Castro brings extensive commercial and international relations experience from her role as Legal Representative in Cuba for Copa Airlines. Passionate about sustainability, she focuses on creating alliances and sustainable development, leading multidisciplinary, multicultural teams.

**Fields:**

- **Affiliation:** Imaginari [NOTE LAST LETTER i si]
- **LinkedIn:** https://www.linkedin.com/in/adela-castro-22ba47b6

**Notes:**

- LinkedIn: Legal Representative Cuba for Copa Airlines, passionate about sustainability
- Database: Attended 'Imagineri' call (https://fathom.video/calls/168111809)
- No mentions in Town Hall transcripts
- Affiliation: Copa Airlines (primary), Imaginary (database shows 'Imaginary' - likely variation)

---

## 3. Alisa Keesey APPROVED

**Bio:**

Alisa is a WASH and agroecology specialist with 25+ years of experience designing and scaling international development programs for climate-resilient agriculture and food security. Her work focuses on container-based sanitation, composting, soil health, and nutrient recovery. She works with smallholder farmers and community organizations in Uganda and California to promote regenerative practices, circular economy jobs, and ecological sanitation solutions.

**Fields:**

- **Affiliation:** Give Love
- **LinkedIn:** https://www.linkedin.com/in/alisakeesey

**Notes:**

- LinkedIn: WASH & Agroecology Specialist, Environmental Anthropologist, PhD candidate UC Santa Cruz
- Database: Attended GCDC1 calls (https://fathom.video/calls/220172326, https://fathom.video/calls/220163703)
- No mentions in Town Hall transcripts
- Affiliation: Give Love (database), UC Santa Cruz (LinkedIn), works in Uganda and California
- Key expertise: container-based sanitation, composting, soil health, nutrient recovery, regenerative agriculture

---

## 4. Angelique Garcia NEXT

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Unknown

**Notes:**

_[No research notes yet]_

---

## 5. Anna Akpe

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/anna-akpe-24374b321

**Notes:**

_[No research notes yet]_

---

## 6. Arun Bangura

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 7. Aviv Green

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Founder of EcoNomads YouTube channel, involved in Pastoralist Savannah Restoration Center in Kenya

**Notes:**

_[No research notes yet]_

---

## 8. Byamukama nyansio

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Gwindi EcoFarm, Ready for Change
- **LinkedIn:** https://www.linkedin.com/in/byamukama-nyansio-46a485292

**Notes:**

_[No research notes yet]_

---

## 9. Celia Francis

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Email:** celia@ponterra.eco
- **Affiliation:** Pantera
- **LinkedIn:** https://www.linkedin.com/in/celiafrancis/

**Notes:**

_[No research notes yet]_

---

## 10. Chris Pilley

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Safari company, SOTOP camp

**Notes:**

- Research needed from ERA records

---

## 11. Delkhwa habibi

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research needed from ERA records

---

## 12. Dushime Ange Leo clevis

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 13. Elizabeth Morgan Tyler

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Activist, focused on water issues

**Notes:**

_[No research notes yet]_

---

## 14. Emmanuel Renegade

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Email:** emmanuel@picinguaba.com
- **Affiliation:** Regenerative land project
- **LinkedIn:** https://www.linkedin.com/in/emmanuel-rengade-%F0%9F%8C%8E-9712441

**Notes:**

- Database needs spelling correction

---

## 15. Emmanuel URAMUTSE

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Environmental studies master's student
- **LinkedIn:** https://www.linkedin.com/in/emmanuel-uramutse-b18a53219

**Notes:**

- Database needs case correction

---

## 16. Fadja Robert

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Not listed
- **LinkedIn:** https://www.linkedin.com/in/fadja-robert-carr-dha-5b0421154

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 17. Fred Ogden

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** NOAA
- **LinkedIn:** https://www.linkedin.com/in/fred-l-ogden-03078273

**Notes:**

_[No research notes yet]_

---

## 18. Gary Glass

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Unknown

**Notes:**

_[No research notes yet]_

---

## 19. Geodisio Castillo

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/geodisio-castillo-52269728

**Notes:**

_[No research notes yet]_

---

## 20. Gwen

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

_[No research notes yet]_

---

## 21. Hadziqah

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Brunei

**Notes:**

_[No research notes yet]_

---

## 22. Hashim Yussif

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 23. Heraclio Herrera

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Congreso General Kuna (CUNA Institute)
- **LinkedIn:** https://www.linkedin.com/in/heraclio-herrera-r-b7b05531

**Notes:**

_[No research notes yet]_

---

## 24. Hilary Hart

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Calliopeia

**Notes:**

- ⚠️ NOT AN ERA MEMBER - should be removed

---

## 25. Ilarion (3)

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- ⚠️ This has been fixed multiple times - verify carefully

---

## 26. Ivan Owen

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Social Glassa

**Notes:**

_[No research notes yet]_

---

## 27. Jennifer Koster

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Workwall Project Services, Regenerative Communities
- **LinkedIn:** https://www.linkedin.com/in/jennifer-koster-a2b5331

**Notes:**

_[No research notes yet]_

---

## 28. Jerald Katch

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Retired, working with local arboretum

**Notes:**

_[No research notes yet]_

---

## 29. Jeremiah Agnew

**Bio:**

With over a decade of experience in trauma resolution and personal development, I have guided numerous individuals through transformative journeys. My work integrates diverse modalities, including men’s work, sacred sexuality, and plant medicine, all aimed at fostering deep, lasting change. Some tangible awards have been: * Winner of the EDF Energy Sustainable Challenge Award 2012 for redesigning the Paris Metro * Youngest designer to have placed a public art exhibition in Place De Republique in Paris (at the time) * Winner of Young Enterprise of the Year Award 2004 for my first company * I have two University degrees. A diploma on psychotropic plants in progress. I am a Regenerative Leadership Academy Alumni. Level 2 TRE practioner & Reiki Level 1.

**Fields:**

- **Affiliation:** Involved with Master Mining Eden

**Notes:**

_[No research notes yet]_

---

## 30. Jeremy Simon

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Unknown

**Notes:**

_[No research notes yet]_

---

## 31. Juan Bernal

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Obama Fellow, Executive Director of Geiversity Panama's Ecological University

**Notes:**

- Collect info from ERA records

---

## 32. Judith Rosen

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Writer, translator of her father Robert Rosen's work

**Notes:**

- ⚠️ NOT AN ERA MEMBER - should be removed

---

## 33. Julia Lindley

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Florida Oceanographic Society
- **LinkedIn:** https://www.linkedin.com/in/julialindley1

**Notes:**

_[No research notes yet]_

---

## 34. Justin Ritchie

**Bio:**

**Justin Ritchie** is a PhD candidate at the University of British Columbia’s Institute for Resources, Environment and Sustainability as well as a producer for the Energy Transition Show. His academic work focuses on the economics of decarbonization, scenarios of transitions to future technologies and cognitive approaches to model-based science.

**Fields:**

- **Affiliation:** Transition US

**Notes:**

_[No research notes yet]_

---

## 35. Kaluki Paul Mutuku

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/kaluki-paul-mutuku%F0%9F%95%8A-2a8400105

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 36. Katharine King

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Threshold Foundation

**Notes:**

- ⚠️ NOT AN ERA MEMBER - should be removed

---

## 37. Kathia Burillo

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Imaginary
- **LinkedIn:** https://www.linkedin.com/in/kathia-burillo-r-a90a4576

**Notes:**

_[No research notes yet]_

---

## 38. Kevin A.

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Florida International University

**Notes:**

- Collect info from ERA records

---

## 39. Kevin Li

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** USDA (based in Penn State)

**Notes:**

- Verify Town Hall attendance/presentation

---

## 40. Lauren Miller

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Not listed

**Notes:**

- Research from ERA records needed

---

## 41. Lisa Merton

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Greenbelt Movement International

**Notes:**

- Verify Town Hall attendance/presentation

---

## 42. Malaika Patricia

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research from ERA records needed
- ERA Africa participant - check Africa Town Hall transcripts

---

## 43. Mary Ann Edwards

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Email:** maedwardsrn@gmail.com
- **Affiliation:** Unknown

**Notes:**

_[No research notes yet]_

---

## 44. Matthew Hooper

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Verify Town Hall attendance/presentation

---

## 45. Maxime Weidema

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/maxime-weidema-82863239

**Notes:**

- Verify Town Hall attendance/presentation

---

## 46. Minot Weld

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Hammerhead Capital
- **LinkedIn:** https://www.linkedin.com/in/minot-weld-921385223

**Notes:**

_[No research notes yet]_

---

## 47. Missy Lahren

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Earth Law Center
- **LinkedIn:** https://www.linkedin.com/in/missy-lahren-earthlawyer

**Notes:**

_[No research notes yet]_

---

## 48. Mr. Kipilangat Kaura -TAWI

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/kipilangat-kaura-2425702bb

**Notes:**

_[No research notes yet]_

---

## 49. Mtokani Saleh

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Agri-Hope, Initiative for Resilience

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 50. Munyembabazi Aloys

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research from ERA records needed
- ERA Africa participant - check Africa Town Hall transcripts

---

## 51. Mutasa Brian

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Email:** brianmutasa256@gmail.com
- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research from ERA records needed
- ERA Africa participant - check Africa Town Hall transcripts

---

## 52. Myra Jackson

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Unknown

**Notes:**

_[No research notes yet]_

---

## 53. Penny Heiple

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Unknown
- **LinkedIn:** https://www.linkedin.com/in/pennyheiple

**Notes:**

_[No research notes yet]_

---

## 54. Roberto Forte

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** SciTech
- **LinkedIn:** https://www.linkedin.com/in/roberto-forte-ph-d-ba2b2121

**Notes:**

_[No research notes yet]_

---

## 55. Roberto Pedraza Ruiz

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/roberto-pedraza-ruiz-281483166

**Notes:**

_[No research notes yet]_

---

## 56. Scott Schulte

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** University of Kansas
- **LinkedIn:** https://www.linkedin.com/in/scott-schulte-6a75a97

**Notes:**

_[No research notes yet]_

---

## 57. Steffie Rijpkema

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** FarmTree
- **LinkedIn:** https://www.linkedin.com/in/steffie-rijpkema-49b457105

**Notes:**

_[No research notes yet]_

---

## 58. Stella Nakityo

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research from ERA records needed

---

## 59. Theopista Abalo

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/theopistaabalo35

**Notes:**

_[No research notes yet]_

---

## 60. Wambui Muthee

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Greenbelt Movement

**Notes:**

_[No research notes yet]_

---

## 61. nding'a ndikon

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/nding-a-orkeyaroi-8a73081b7

**Notes:**

_[No research notes yet]_

---
