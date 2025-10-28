# ERA Members Lacking Bios

**Date:** October 27, 2025

## Summary

- **Total ERA Members:** 391
- **With Bios:** 329 (84.1%)
- **Without Bios:** 62 (15.9%)

# Context:

Member Enrichment

**Purpose:** Complete member onboarding by enriching profiles and bios and preparing for public directory publication

**Status:** 🚀 Active (Oct 25, 2025) derived from member_enrichment/README

---

## Overview

### The ERA Onboarding Process

When someone becomes an ERA member (introduced at Town Hall, no objections, week passes):

**Full onboarding should include:**

1. NOW ✅ Update profile (Bio, email, phone, affiliated organizations) in Database
2. LATER ✅ Publish in public directory (https://www.ecorestorationalliance.org/public-directory)
3. LATER ✅ Add to ERA Landscape visualization
4. LATER ✅ Send welcome email (+ invite to become supporting member)
5. LATER ✅ Add to Google Groups mailing lists

**Reality:** We've been sloppy. There's a backlog.

### Immediate Scope

**This integration focuses on steps 1-2:**

1. **Complete profiles** for members who attended Town Halls
   - Bios (contextual, personalized)
   - Email addresses
   - Phone numbers (where available)
   - Affiliated organizations
2. **Prepare for updating Airtable and public directory publication** (human activates "Publish" field)

**Current State:**

- The Challenge

**Hand-authored bios work best** because they:

- Capture what makes each person unique to ERA
- Integrate professional background with ERA engagement
- Reflect actual contributions and interests discussed in Town Halls
- Avoid generic LinkedIn summary language

**Sources of information:**

1. **LinkedIn profiles** (provided by user) → Professional background.  ADAPT THESE WHEN POSSIBLE
2. **Town Hall participation** (from Fathom database) → Meeting attendance, engagement
3. **Town Hall and ** (era_townhalls_complete.md) → What they said, context, interests
   1. if that is inadequate, there are often other fathom recordings with rich conversations.
4. **Email search** (user's email) → Contact info (email, phone), affiliated organizations, background
5. **Airtable member data** (existing records) → Current affiliations, projects, notes

---

## Approach: Intelligent Assistant Pattern

Following the participant_reconciliation model:

**Human-AI Collaboration:**

1. AI identifies members needing profiles (SEE BELOW)
2. Human provides LinkedIn URLs for batch of members (SEE BELOW.  When Linkedin profile is lacking we need further resarch)
3. FUrther research Read LinkedIn profile
   - Search Town Hall and other transcripts for mentions
   - Search user's email for contact info, org affiliations, background
   - Query Fathom database for participation details
4. AI compiles research notes with sources.  Insert them in line in this document, including responses to my queries.
5. AI drafts complete profile updates:
   - Bio (personalized, contextual - not generic summaries)
   - Email address (from email search or existing data)
   - Phone number (if found in email)
   - Affiliated organizations (from email, LinkedIn, or existing data)
6. Human reviews, edits, approves
   1. we will do these iteratively.  Every time we iterate you will create a NEW numbered version of this document.  Augmented as requested and removing one that I say are ready for inclusion in the database or removed because of other directions I give.  For those, you will add them thoughtfully to the database.

      Eventually there will be no members left.
7. **THIS IS NOT automated profile generation** - This is collaborative curation with AI providing:

- Multi-source synthesis (LinkedIn + TH context + email correspondence)
- Pattern recognition (similar members, common themes)
- Draft generation for human refinement
- Contact info extraction from email

---

## Key Principles

**1. Context-Rich Bios**

- NOT: BLIND Generic LinkedIn summary copy-paste
- YES:  Curated for consistency of Tone and relevance to ERA.

**2. Prioritization**

* **act on those where action is clear.  insert questions for those where you don't know what to do**

**3. Human Oversight**

- AI collects data, drafts Bios, human edits and approves every bio, AI learns from the process and improves.
- 

**4. Quality Over Speed**

- Intelligent Solutions via Intelligence not via scripts.
- Thoughtful, personalized bios
- Multiple source synthesis
- Reflect actual ERA engagement

---

## Data Sources

**Airtable:** `/Users/admin/ERA_Admin/airtable/people_export.csv. `

- We are using Airtable for information but not writing to it at the moment.

**Database:** `/Users/admin/ERA_Admin/FathomInventory/fathom_emails.db`

**Town Hall Transcripts:** `/Users/admin/ERA_Admin/fathom/output/era_townhalls_complete.md`

- Complete transcripts of all Town Halls
- Search for mentions, contributions, questions, context

**Email Archive:** (user's email - Gmail search)

- Contact info (email addresses, phone numbers)
- Affiliated organizations mentioned in correspondence
- Background context, introductions, conversations
- **Access via:** Gmail API or search tools (to be determined)

**LinkedIn:** (provided by user)

- Professional background
- Current position, education
- Organizations, skills, interests

---

## Process

### Phase 1.  AI: Read this document, ask questions,

1. To facilitate my navigation using the sidebar outline,  organiza heading. so that we have Three H1 headings:  Summary, Context, and Members Without Bios
   Each Member name is H2, with subordinate H3s for

   * Bio (draft, if any)
   * Fields [bullet list of field names and values from Database: Email, Phone, Affiliated Organizations (populated in part from this ongoing research)]
   * Notes. Information concisley curated as requrested.

## Phase 2: Multi-Source Research (AI):

For each member flagged as NEXT, you will populate the fields

1. Read LinkedIn profile (professional background)
2. Query Town Hall participation from Fathom database
3. Search era_townhalls_complete.md for mentions, contributions
4. Search user's email for:
   - Email address
   - Phone number
   - Affiliated organizations
   - Background context, introductions
5. Review existing Airtable data
6. Synthesize into contextual research notes with sources

### Update Complete profile when marked APPROVED:

Generate complete profile updates:

- **Bio:** 2-3 sentences, personalized
  - Lead with professional background (from LinkedIn)
  - Integrate ERA context (from Town Halls)
  - Highlight contributions/interests
- **Email:** From email search or existing data
- **Phone:** If found in email correspondence
- **Affiliated Orgs:** From email, LinkedIn, or existing data

## Success Metrics

**Immediate Goal:**

- Profiles enriched.
- Fields updated: Bio, Email, Phone (where available), Affiliated Orgs
- Quality: Human-reviewed and edited each field
- Context integration: LinkedIn + TH transcripts + other conversations +  email correspondence
- Ready for publication: Profiles complete, awaiting manual "Publish" activation

**Quality Criteria:**

- Contact info is accurate and sourced
- Affiliated orgs reflect current/relevant organizations. [Collect these as you edit.]
- 

**Pattern to follow:**

- AI proposes, human edits, AI disposes
- Iterative process with numbered versions of this document.
- Thoughtful, intelligence evidence-rich outputs (links to sources)
- Learn from corrections

---

## Members Without Bios (62)

### ✅ With LinkedIn URLs (1 - Ready to Scrape)

**Celia Francis**

- LinkedIn: https://www.linkedin.com/in/celiafrancis/
- Email: celia@ponterra.eco
- Affiliation: Pantera

---

### ⚠️ Without LinkedIn URLs (61 - Need Manual Search)

**Abbie Dusseldorp**

- Affiliation: Groundwork USA
- https://www.linkedin.com/in/abigail-dusseldorp-10a58964/

**Adela Castro**

- Affiliation: Imaginary
- https://www.linkedin.com/in/adela-castro-22ba47b6/

**Alisa Keesey**

- Affiliation: Give Love
- https://www.linkedin.com/in/alisakeesey/

**Angelique Garcia**

- Affiliation: Unknown

**Anna Akpe**

- Affiliation: This participant's company is not listed in the calendar event
- https://www.linkedin.com/in/anna-akpe-24374b321/

**Arun Bangura**

- Affiliation: This participant's company is not listed in the calendar event
- ERA Africa.  SEARCH The relevant meeting and extract biographical informaton

**Aviv Green**

- Affiliation: Founder of EcoNomads YouTube channel, involved in Pastoralist Savannah Restoration Center in Kenya
- GENERATE from Town Hall transcript

**Byamukama nyansio**

- Affiliation: Gwindi EcoFarm, Ready for Change
- https://www.linkedin.com/in/byamukama-nyansio-46a485292/

**Chris Pilley**

- Affiliation: Safari company, SOTOP camp
- RESEARCH from our records

**Delkhwa habibi**

- Affiliation: This participant's company is not listed in the calendar event
- RESEARCH from our records

**Dushime Ange Leo clevis**

- Affiliation: This participant's company is not listed in the calendar event
- ERA Africa

**Elizabeth Morgan Tyler. [DROP HER. NOT A MEMBER]**

- Affiliation: Activist, focused on water issues

**Emmanuel Renegade**

- Email: emmanuel@picinguaba.com
- Affiliation: Regenerative land project
- https://www.linkedin.com/in/emmanuel-rengade-%F0%9F%8C%8E-9712441/
  FIX SPELLING.  WE'VE DOE THIS BEFORE

**Emmanuel URAMUTSE**

- Affiliation: Environmental studies master's student
  https://www.linkedin.com/in/emmanuel-uramutse-b18a53219/
  FIX CASE

**Fadja Robert**

- Affiliation: Not listed
- https://www.linkedin.com/in/fadja-robert-carr-dha-5b0421154/
- ERA Africa

**Fred Ogden**

- Affiliation: NOAA
- https://www.linkedin.com/in/fred-l-ogden-03078273/

**Gary Glass**

- Affiliation: Open Future Coalition
- No BIO

**Geodisio Castillo**

- Affiliation: This participant's company is not listed in the calendar event
- https://www.linkedin.com/in/geodisio-castillo-52269728/

**George Sendero**

- Affiliation: For the Oceans Foundation
- Bio:

  Board Member - Chief Executive Officer

  Jorge Serendero as former Costa Rican Sea Shepherd Conservation director has played different operational and organizational roles in campaigns in Coco’s Island and other biological corridor areas of the Pacific. He also was leading the PR and communications team that released Captain Paul Watson from criminal charges in Costa Rica, together with Sea Shepherds Lawyer, Abraham Stern. Thanks to his thorough works he was able to detect and fully understand the need to protect marine sanctuaries from Costa Rica to Ecuador, at the Eastern Tropical Pacific Marine Corridor including the South Pacific. These marine habitats are seriously threatened by large foreign fleets of illegal fishing, such as the Chinese fleet with hundreds of factory boats, extracting wildlife indiscriminately without giving migrant populations and species the opportunity to reproduce. In addition to being the CEO of For the Oceans Foundation, Jorge Serendero also directs the “Front for the Protected Wild Areas”, as a permanent advisory organization linked to the Ministry of the Environment of Costa Rica and SINAC, the National System of Conservation Areas.

**Gwen**

- Affiliation: This participant's company is not listed in the calendar event
- [THIS IS ONE NAME.  Research our records for clues.]

**Hadziqah**

- Affiliation: Brunei
- one of Mooyoung Han's Students.
- [THIS IS ONE NAME.  Research our records for clues.]

**Hashim Yussif**

- Affiliation: This participant's company is not listed in the calendar event
- ERA Africa GET INFORMATION FROM TRANSCRIPTS

**Heraclio Herrera**

- Affiliation: Congreso General Kuna (CUNA Institute)
- https://www.linkedin.com/in/heraclio-herrera-r-b7b05531/

**Hilary Hart**

- Affiliation: Calliopeia
- NOT AN ERA MEMBER

**Ilarion (3)**

- Affiliation: This participant's company is not listed in the calendar event
- WE HAVE FIXED THIS MANY TIMES>. GET IT RIGHT.

**Ivan Owen**

- Affiliation: Social Glass
- An artist and innovator, Ivan is co-Founder of Enabling The Future (free, 3D printed open source prosthetics). Now residing in Limerick, Ireland, he continues to create innovative and whimsical artwork, including giant puppeteer hands and captivating stop-motion videos. Self-taught in engineering and animation, Ivan draws inspiration from music, society, and technology. Though his groundbreaking prosthetic design remains a highlight of his career, he is now focused on artistic exploration while sharing his creations on YouTube and TikTok.

**Jennifer Koster**

- Affiliation: Workwall Project Services, Regenerative Communities
- https://www.linkedin.com/in/jennifer-koster-a2b5331/

**Jerald Katch**

- Affiliation: Retired, working with local arboretum
- Jed holds a Ph. D. in Developmental and Educational Psychology from the University of Chicago and an M. Ed. in Special Education from Boston University.  He has taught in grades K-12, college, and graduate school programs.  Jed specializes in connecting student interests with real world activities.  At Bio4Climate, he is working to create opportunities for young environmental activists to combine their interests in eco-restoration with gaining academic credit in schools and in higher education.

**Jeremiah Agnew**

- Affiliation: Involved with Master Minding Eden  [NOTE Minding]
  Bio:

With over a decade of experience in trauma resolution and personal development, I have guided numerous individuals through transformative journeys. My work integrates diverse modalities, including men’s work, sacred sexuality, and plant medicine, all aimed at fostering deep, lasting change.

Some tangible awards have been:

* Winner of the EDF Energy Sustainable Challenge Award 2012 for redesigning the Paris Metro
* Youngest designer to have placed a public art exhibition in Place De Republique in Paris (at the time)
* Winner of Young Enterprise of the Year Award 2004 for my first company
* I have two University degrees. A diploma on psychotropic plants in progress. I am a Regenerative Leadership Academy Alumni. Level 2 TRE practioner & Reiki Level 1.

**Jeremy Simon**

- Affiliation: Unknown
- not an ERA Member

**Juan Bernal**

- Affiliation: Obama Fellow, Executive Director of Geoversity Panama's Ecological University
- COLLECT INFO FROM OUR RECORDS

**Judith Rosen**

- Affiliation: Writer, translator of her father Robert Rosen's work
- NOT AN ERA MEMBER

**Julia Lindley**

- Affiliation: Florida Oceanographic Society
- https://www.linkedin.com/in/julialindley1/

**Justin Ritchie**

- Affiliation: Transition US
- Bio:

  **Justin Ritchie** is a PhD candidate at the University of British Columbia’s Institute for Resources, Environment and Sustainability as well as a producer for the Energy Transition Show. His academic work focuses on the economics of decarbonization, scenarios of transitions to future technologies and cognitive approaches to model-based science.

**Kaluki Paul Mutuku**

- Affiliation: This participant's company is not listed in the calendar event
- ERA Africa https://www.linkedin.com/in/kaluki-paul-mutuku%F0%9F%95%8A-2a8400105/

**Katharine King**

- Affiliation: Threshold Foundation
- NOT A MEMBER

**Kathia Burillo**

- Affiliation: Imaginari
- https://www.linkedin.com/in/kathia-burillo-r-a90a4576/

**Kevin A.**

- Affiliation: Florida International University
- COLLECT INFO FROM OUR RECORDS

**Kevin Li**

- Affiliation: USDA (based in Penn State)
- HAS HE PRESENTED AT A TOWN HALL.

**Lauren Miller**

- Affiliation: Not listed
- GATHER INFO FROM OUR RECORDS

**Lisa Merton**

- Affiliation: Greenbelt Movement International
  HAS HE PRESENTED AT A TOWN HALL

**Malaika Patricia**

- Affiliation: This participant's company is not listed in the calendar event
- ERA AFRICA GATHER INFO

**Mary Ann Edwards**

- Email: maedwardsrn@gmail.com
- Affiliation: Unknown

**Matthew Hooper**

- Affiliation: This participant's company is not listed in the calendar event
- HAS HE PRESENTED AT A TOWN HALL

**Maxime Weidema**

- Affiliation: This participant's company is not listed in the calendar event
- https://www.linkedin.com/in/maxime-weidema-82863239/
- HAS SHE PRESENTED AT A TOWN HALL

**Minot Weld**

- Affiliation: Hammerhead Capital
- https://www.linkedin.com/in/minot-weld-921385223/

**Missy Lahren**

- Affiliation: Earth Law Center
- https://www.linkedin.com/in/missy-lahren-earthlawyer/

**Mr. Kipilangat Kaura -TAWI**

- Affiliation: This participant's company is not listed in the calendar event
- https://www.linkedin.com/in/kipilangat-kaura-2425702bb/

**Mtokani Saleh**

- Affiliation: Agri-Hope, Initiative for Resilience
- **Saleh Mtokani** who has a project at Kakuma Refugee Settlement called AgriHope Initiative in Kenya,
- ERA Africa Gather more Info

**Munyembabazi Aloys**

- Affiliation: This participant's company is not listed in the calendar event
- ERA AFRICA.  GATHER INFO
- Aloys is a graduate of the University of Rwanda and is currently leading local regenerative agriculture practices while building a new youth-based organization that will focus on skill and competency development while implementing different methodologies.

**Mutasa Brian**

- Email: brianmutasa256@gmail.com
- Affiliation: This participant's company is not listed in the calendar event
- ERA AFRICA GATHER INFO

**Myra Jackson**

- Affiliation: Earth Regeneration Alliance https://www.earthregenerationalliance.com/
- BIO:

  Myra served from 2012 to 2015 on the UN Open Working Group on Sustainable Development Goals (SDGs), where after being adopted by 192 member states, she helped communicate the 17 SDGs from the global fora to local communities and subnational governments. She initially served as a UN Representative and focal point on Climate Change for the UN Major Groups Commons Cluster, a Senior Advisor on Whole Earth Civics, and is currently the UNFCCC Head of Delegation for Earth Law Center, as well as a member of the UN Harmony with Nature Expert Platform.

  Myra is currently focused on the regeneration of Earth’s most critical ecosystems in what she calls the Great Work of our time — a call that summons all who are alive today to recognize that the well-being of the Earth is inextricably linked to the well-being of humanity and all life forms.

  As Founder and Global Lead of the Global Freshwaters Summit, an initiative of the Global Being Foundation, Myra focuses on non-anthropocentric approaches to restoring the Earth’s freshwaters and advancing Earth Jurisprudence. She carries the aspirational title of Diplomat of the Biosphere, awarded by the Stockholm Resilience Centre’s Planetary Boundaries initiative, and speaks internationally on the restoration of broken human bonds with Nature, land and water regeneration and ecological succession.

**nding'a ndikon**

- Affiliation: This participant's company is not listed in the calendar event
- https://www.linkedin.com/in/nding-a-orkeyaroi-8a73081b7/
- CHECK SPELLING; SEE IF NEEDS SMART MERGING WITH LAIZER

**Penny Heiple**

- Affiliation:Design School for Regenerating Earth
  https://www.linkedin.com/in/pennyheiple/

**Roberto Forte**

- Affiliation: SciTech
- https://www.linkedin.com/in/roberto-forte-ph-d-ba2b2121/

**Roberto Pedraza Ruiz**

- Affiliation: This participant's company is not listed in the calendar event
- https://www.linkedin.com/in/roberto-pedraza-ruiz-281483166/

**Scott Schulte**

- Affiliation: University of Kansas
- https://www.linkedin.com/in/scott-schulte-6a75a97/
- DID HE ATTEND TOWN HALL?

**Steffie Rijpkema**

- Affiliation: FarmTree
- https://www.linkedin.com/in/steffie-rijpkema-49b457105/

**Stella Nakityo**

- Affiliation: This participant's company is not listed in the calendar event
- GATHER INFO FROM OUR RECORDS

**Theopista Abalo**

- Affiliation: This participant's company is not listed in the calendar event
  https://www.linkedin.com/in/theopistaabalo35/

**Wambui Muthee**

- Affiliation: Greenbelt Movement

---

## Next Steps

1. **Scrape LinkedIn profiles** for the 1 members with URLs
2. **Manual LinkedIn search** for the 61 members without URLs
3. Use email domains and affiliations as search hints
4. Check Airtable for additional LinkedIn URLs not yet in database
