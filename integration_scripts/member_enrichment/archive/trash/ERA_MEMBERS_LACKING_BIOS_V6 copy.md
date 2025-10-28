# Summary

**Document:** ERA Members Lacking Bios - Version 6
**Date:** October 27, 2025
**Status:** 🚀 Active - Ongoing enrichment

## Stats

- **Total ERA Members Needing Bios:** 46
- **With Bio Drafts:** 3
- **Removed This Iteration:** 5 APPROVED + 4 non-members

## Recent Changes

- ✅ **Byamukama Nyansio, Geodisio Castillo, Jennifer Koster** - Bios completed and added to database
- 🔄 **LinkedIn scraping in progress** - 18 profiles being collected (scrape_v5_18.py)
- 📊 **V6 ready** - 46 members remaining

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

## 1. Angelique Garcia [do RESEARCH from ourRecords]

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Unknown

**Notes:**

_[No research notes yet]_

---

## 2. Arun Bangura [do RESEARCH from ourRecords]

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

## 4. Chris Pilley [do RESEARCH from ourRecords]

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Safari company, SOTOP camp

**Notes:**

- Research needed from ERA records

---

## 5. Delkhwa habibi [do RESEARCH from ourRecords]

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research needed from ERA records

---

## 6. Dushime Ange Leo clevis [do RESEARCH from ourRecords]

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 7. Elizabeth Morgan Tyler

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Activist, focused on water issues

**Notes:**

_[No research notes yet]_

---

## 8. Emmanuel URAMUTSE APPROVED

**Bio:**

Emmanuel Uramutse is a high school science teacher in Uganda focused on environmental education and youth engagement. He brings science education expertise to ERA Africa, working to inspire the next generation of environmental stewards.

**Fields:**

- **Affiliation:** Environmental studies master's student
- **LinkedIn:** https://www.linkedin.com/in/emmanuel-uramutse-b18a53219

**Notes:**

- Database needs case correction DO THIS!!

---

## 9. Fadja Robert APPROVED;

**Bio:**

Fadja Robert-Carr, DHA, is a healthcare executive, consultant, and wellness advocate focused on health equity and community empowerment. She leads interdisciplinary teams delivering health services and wellness initiatives that expand access to quality care for underserved populations. Her work integrates evidence-based models with community-centered approaches to create measurable health outcomes.

**Fields:**

- **Affiliation:** Not listed
- **LinkedIn:** https://www.linkedin.com/in/fadja-robert-carr-dha-5b0421154

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 10. Fred Ogden APPROVED

**Bio:**

Fred L. Ogden is Chief Scientist for Water Prediction at NOAA (National Oceanic & Atmospheric Administration). His research focuses on hydrologic model development, tropical hydrology, and infiltration modeling, advancing the science of water prediction and management in the face of climate change. He brings expertise in hydraulics and ecohydrology to understanding water-ecosystem interactions.

**Fields:**

- **Affiliation:** NOAA
- **LinkedIn:** https://www.linkedin.com/in/fred-l-ogden-03078273

**Notes:**

_[No research notes yet]_

---

## 11. Gary Glass

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Open Future Coalition

**Notes:**

_[No research notes yet]_

---

## 12. Gwen [do RESEARCH from ourRecords]

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

_[No research notes yet]_

---

## 13. Hadziqah [do RESEARCH from ourRecords]

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Brunei

**Notes:**

_[No research notes yet]_

---

## 14. Hashim Yussif

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 15. Heraclio Herrera [Save this but, he's not an ERA Member]

**Bio:**

**LinkedIn Headline:** Especialista en Gestión Medio ambiental

**Bio (Improved - ERA Standards):**

Heraclio Herrera R. is an environmental management specialist at Congreso General Kuna in Panama. His work focuses on indigenous environmental governance and sustainable resource management within Kuna communities.

**Fields:**

- **Affiliation:** Congreso General Kuna (CUNA Institute)
- **LinkedIn:** https://www.linkedin.com/in/heraclio-herrera-r-b7b05531

**Notes:**

_[No research notes yet]_

---

## 16. Ilarion (3) [This is Ilarion Larry Merculief, for whom we should have a linkedIn]

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- ⚠️ This has been fixed multiple times - verify carefully

---

## 17. Ivan Owen

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Social Glassa

**Notes:**

_[No research notes yet]_

---

## 18. Jerald Katch

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Retired, working with local arboretum

**Notes:**

_[No research notes yet]_

---

## 19. Juan Bernal

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Obama Fellow, Executive Director of Geiversity Panama's Ecological University

**Notes:**

- Collect info from ERA records

---

## 20. Julia Lindley APPROVED

**Bio:**

**LinkedIn Headline:** Environmental Educator and Conservation Communicator

**LinkedIn About:** Passionate Florida conservation advocate and wildlife educator with exceptional communication skills, dedicated to inspiring others to protect and appreciate our wild spaces.

**Bio (Improved - ERA Standards):**

Julia Lindley is an environmental educator and conservation communicator at Florida Oceanographic Society. She specializes in marine conservation education and public engagement, helping communities understand and protect coastal ecosystems.

**Fields:**

- **Affiliation:** Florida Oceanographic Society
- **LinkedIn:** https://www.linkedin.com/in/julialindley1

**Notes:**

_[No research notes yet]_

---

## 21. Kaluki Paul Mutuku APPROVED

**Bio:**

**LinkedIn Headline:** 2x Founder | Consultant | Visionary | Events Host & Moderator 🔟 yrs in: Nature-based Solutions🌱|Restoration Projects🌳|Impact Storytelling🗣|Advocacy🌍 Currently: Philanthropy 🌐 | Movements support✨️

**LinkedIn About:** LinkedIn most definitely wants me to tell you what I'm great at. Honestly, I'd rather tell you who I am. I am a stubborn optimist and proud son of the Afrikan soil. Yes, as a climate advocate and restoration expert, I centre optimism, courage and meaningful engagement of communities and youth who are leading the solutions for both the climate and biodiversity crises. Hope is a tiny seed 🫘 that thrives through care and nurturing, and when embraced among people, becomes a strong, towering tree 🌳 t

**Bio (Improved - ERA Standards):**

Kaluki Paul Mutuku is a two-time founder, consultant, and visionary with 10 years of experience in nature-based solutions and sustainable development. He works at the intersection of entrepreneurship, conservation, and community empowerment.  He describes himself as "Ia stubborn optimist and proud son of the Afrikan soil."

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/kaluki-paul-mutuku%F0%9F%95%8A-2a8400105

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 22. Kathia Burillo

**Bio:**

**LinkedIn Headline:** Executive Director en Fundación Imaginari

**Bio (Improved - ERA Standards):**

Kathia Burillo R. is Executive Director of Fundación Imaginari in Costa Rica. She leads initiatives at the intersection of art, imagination, and social transformation, fostering creative approaches to community development and environmental awareness.

**Fields:**

- **Affiliation:** Imaginary
- **LinkedIn:** https://www.linkedin.com/in/kathia-burillo-r-a90a4576

**Notes:**

_[No research notes yet]_

---

## 23. Kevin A.

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Florida International University

**Notes:**

- Collect info from ERA records

---

## 24. Kevin Li

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** USDA (based in Penn State)

**Notes:**

- Verify Town Hall attendance/presentation

---

## 25. Lauren Miller

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Not listed

**Notes:**

- Research from ERA records needed

---

## 26. Lisa Merton

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Greenbelt Movement International

**Notes:**

- Verify Town Hall attendance/presentation

---

## 27. Malaika Patricia

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research from ERA records needed
- ERA Africa participant - check Africa Town Hall transcripts

---

## 28. Mary Ann Edwards

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Email:** maedwardsrn@gmail.com
- **Affiliation:** Unknown

**Notes:**

_[No research notes yet]_

---

## 29. Matthew Hooper

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Verify Town Hall attendance/presentation

---

## 30. Maxime Weidema APPROVED

**Bio:**

**LinkedIn Headline:** From Ego to Eco | From gray to 🏳️‍🌈

**Bio (Improved - ERA Standards):**

Maxime Weidema is a transition facilitator and project coordinator focused on shifting "from Ego to Eco" through regenerative practices and systems change. Her work bridges personal transformation and collective ecological action.

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/maxime-weidema-82863239

**Notes:**

- Verify Town Hall attendance/presentation

---

## 31. Minot Weld APPROVED

**Bio:**

**LinkedIn Headline:** Managing Partner at Wivern Management

**LinkedIn About:** I work in project finance. At present we are favoring large projects in the following areas: development and/or prefabrication of low-cost/high-performance housing, mixed-use infill and redevelopment projects, renewable energy, water cycle restoration, reclamation of degraded landscapes at scale as well as regenerative forestry, agro-forestry and agriculture projects.

**Bio (Improved - ERA Standards):**

Minot Weld is Managing Partner at Wivern Management and Hammerhead Capital. He brings investment and management expertise to sustainable and regenerative business ventures, focussing on large projects in the following areas: development and/or prefabrication of low-cost/high-performance housing, mixed-use infill and redevelopment projects, renewable energy, water cycle restoration, reclamation of degraded landscapes at scale as well as regenerative forestry, agro-forestry and agriculture projects.

**Fields:**

- **Affiliation:** Hammerhead Capital
- **LinkedIn:** https://www.linkedin.com/in/minot-weld-921385223

**Notes:**

_[No research notes yet]_

---

## 32. Missy Lahren

**Bio:**

**LinkedIn Headline:** Chair of Board of Directors @ Earth Law Center | Public Interest Lawyer, Producer, and Writer

**LinkedIn About:** Missy Lahren has worked as an activist and public interest lawyer in the San Francisco Bay Area since 1993. She has a Ph.D. in Philosophy and Religion and a M.Ed. in Integral Education, both of which focus on the emerging field of “ecozoic education.” She has been working to expand enforceable human and ecological rights since 1997 through participatory media and board positions at Earth Law Center, Unite for Rights, Planetary Advocates, and Eleanor Lives.

**Bio (Improved - ERA Standards):**

Missy Lahren is Chair of the Board of Directors at Earth Law Center and a public interest lawyer. She advances Earth-centered governance and legal frameworks that recognize the rights of nature and ecosystems.  She has a Ph.D. in Philosophy and Religion and a M.Ed. in Integral Education, both of which focus on the emerging field of “ecozoic education.” She has been working to expand enforceable human and ecological rights since 1997 through participatory media and board positions at Earth Law Center, Unite for Rights, Planetary Advocates, and Eleanor Lives.

**Fields:**

- **Affiliation:** Earth Law Center, Unite for Rights, Planetary Advocates
- **LinkedIn:** https://www.linkedin.com/in/missy-lahren-earthlawyer

**Notes:**

_[No research notes yet]_

---

## 33. Mr. Kipilangat Kaura -TAWI [ENRICH WITH ERA AFRICA INFO]

**Bio:**

**LinkedIn Headline:** Conservation Intern at no

**Bio (Improved - ERA Standards):**

Kipilangat Kaura is a conservation intern working on biodiversity protection and community-based conservation initiatives. He is building expertise in wildlife conservation and sustainable land management.

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/kipilangat-kaura-2425702bb

**Notes:**

_[No research notes yet]_

---

## 34. Mtokani Saleh

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Agri-Hope, Initiative for Resilience

**Notes:**

- ERA Africa participant - check Africa Town Hall transcripts

---

## 35. Munyembabazi Aloys

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research from ERA records needed
- ERA Africa participant - check Africa Town Hall transcripts

---

## 36. Mutasa Brian

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Email:** brianmutasa256@gmail.com
- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research from ERA records needed
- ERA Africa participant - check Africa Town Hall transcripts

---

## 37. Myra Jackson

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Unknown

**Notes:**

_[No research notes yet]_

---

## 38. Penny Heiple APPROVED

**Bio:**

**LinkedIn Headline:** Co-Founder Design School for Regenerating Earth

**LinkedIn About:**  WAS TRUNCATED


**Bio (Improved - ERA Standards):**

Penny L. Heiple is Co-Founder of Design School for Regenerating Earth. She works at the nexus of design, education, and regenerative systems, helping people develop the skills and mindsets needed to restore planetary health.  

Currently living in Barichara, Colombia, and a native of Boulder, Colorado, I have a passion for serving life and our beautiful planet Earth. I moved to Colombia to live out my dream of helping to regenerate the earth alongside my life partner, Joe Brewer. Together, we are doing ecosystem restoration work and helping to create a local regenerative economy in our bioregion in and around Barichara. We also co-founded the Design School for Regenerating Earth where we are helping to activate bioregional organizing and facilitating learning journeys and learning exchanges between bioregions across the planet.

Penny is  passionate about integrating and applying unified science, integral philosophy, regenerative practices, and biodynamic healing and trauma resolution. Combined with her comprehensive background in operations, project management, accounting, and administration she brings a unique combination of heart and organizational expertise to the various initiatives and organizations in which I'm involved.

**Fields:**

- **Affiliation:** [Design School for Regenerating Earth](https://design-school-for-regenerating-earth.mn.co/)
- **LinkedIn:** https://www.linkedin.com/in/pennyheiple

**Notes:**

_[No research notes yet]_

---

## 39. Roberto Forte APPROVED

**Bio:**

**LinkedIn Headline:** Thought leader and Ph.D.; ready to employ expertise as ESG & Sustainability Director, Climate Change and Decarbonization Manager

**LinkedIn About:** With a track record as a passionate and influential minded professional, Roberto has  expertise in  sustainability, ESG, and climate change initiatives.  He leads  sustainability integration within core business operations, ensuring alignment with ESG objectives,  driving meaningful change throughout the value chain.  

**Bio (Improved - ERA Standards):**

Roberto Forte, Ph.D., is Principal Researcher at CITEC [(Centro de Innovación, Investigación y Tecnología Hidroambiental) ·](https://www.linkedin.com/company/98387059/)Panama.  A thought leader in ESG (Environmental, Social, and Governance) and sustainability,  brings academic expertise and strategic vision to corporate sustainability initiatives and responsible business practices.

**Fields:**

- **Affiliation:** SciTech
- **LinkedIn:** https://www.linkedin.com/in/roberto-forte-ph-d-ba2b2121

**Notes:**

_[No research notes yet]_

---

## 40. Roberto Pedraza Ruiz APPROVED

**Bio:**

**LinkedIn Headline:** Jefe del Programa de Tierras Silvestres en Grupo Ecológico Sierra Gorda I.A.P., fotógrafo de naturaleza

**Bio (Improved - ERA Standards):**

Roberto Pedraza Ruiz leads the Wilderness Program (Programa de Tierras Silvestres) at Grupo Ecológico Sierra Gorda in Mexico. His work focuses on wilderness conservation, biodiversity protection, and sustainable land management in the Sierra Gorda Biosphere Reserve.

**Fields:**

- **Affiliation:** Grupo Ecológico Sierra Gorda
- **LinkedIn:** https://www.linkedin.com/in/roberto-pedraza-ruiz-281483166

**Notes:**

_[No research notes yet]_

---

## 41. Scott Schulte APPROVED

**Bio:**

**LinkedIn Headline:** Associate Professor of the Practice, KU Edwards Campus

**Bio (Improved - ERA Standards):**

Scott Schulte has 30+ years of professional, academic, and not-for-profit experience in the revitalization of natural and human communities and the built environment. His focus is multi-benefit, nature-based solutions for water resources management and community and climate resilience. Schulte is an associate professor of the practice in the environmental assessment Professional Science Master (PSM) and bachelor’s environmental studies programs at the KU Edwards Campus, having previously served as a lecturer for the Urban Planning Program from 2010 to 2015, and the PSM since 2015. He is also a senior environmental planner for Vireo, a community planning, landscape architecture, natural resource management, and public engagement consulting firm. Schulte also serves on the board and was the founding president of the Heartland Conservation Alliance, a not-for-profit alliance and urban land trust that helps regional organizations conserve land for natural and community benefits. He earned a Master of Urban Planning with an Environmental and Land Use Planning emphasis from the University of Kansas in 2002.

**Fields:**

- **Affiliation:** University of Kansas
- **LinkedIn:** https://www.linkedin.com/in/scott-schulte-6a75a97

**Notes:**

_[No research notes yet]_

---

## 42. Steffie Rijpkema

**Bio:**

**LinkedIn Headline:** Project Manager & Team Facilitator | Connecting People, Technology, and Sustainable Impact

**LinkedIn About:** Turning societal challenges into tangible, impactful solutions is what drives me. Whether it is sustainable agriculture, ecosystem restoration, or combatting food waste — my interests are broad, but always rooted in purpose. I thrive in organisations and businesses with a sustainable mission. I enjoy translating complex challenges into clear, pragmatic solutions, bridging the gap between technology and the people it serves. I am energized by bringing people together — aligning teams, improving c

**Bio (Improved - ERA Standards):**

Steffie Rijpkema is a Project Manager and Team Facilitator at FarmTree, connecting people, technology, and sustainability. She specializes in regenerative agriculture initiatives and collaborative approaches to food system transformation.

**Fields:**

- **Affiliation:** FarmTree
- **LinkedIn:** https://www.linkedin.com/in/steffie-rijpkema-49b457105

**Notes:**

_[No research notes yet]_

---

## 43. Stella Nakityo

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event

**Notes:**

- Research from ERA records needed

---

## 44. Theopista Abalo APPROVED

**Bio:**

**LinkedIn Headline:** FAO Young Forest Champion| Passionate about Sustainable Forest Resource Utilization

**LinkedIn About:** I am Abalo Theopista, a final year forestry student at Makerere University. I served as the regional representative of Southern Africa with the International Forestry Students Association, and currently an FAO Young Forest Champion 2025. I am passionate about research in areas of sustainable forest resource management and utilization. I am always eager to contribute to a more sustainable world for a better mother nature and the life it houses. I'm a skilled communicator and collaborative team le

**Bio (Improved - ERA Standards):**

Theopista Abalo is an FAO Young Forest Champion in her final year as a forestry student at Makerer univresity in Uganda.  she is currently represents of Southern Africaat the International Forestry Students Association, and is  an FAO Young Forest Champion 2025.   Passionate about sustainable forest resource utilization, she works on forest conservation, community forestry, and sustainable livelihoods linked to forest ecosystems.

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/theopistaabalo35

**Notes:**

_[No research notes yet]_

---

## 45. Wambui Muthee

**Bio:**

_[No bio draft yet]_

**Fields:**

- **Affiliation:** Greenbelt Movement

**Notes:**

_[No research notes yet]_

---

## 46. nding'a ndikon APPROVED

**Bio:**

**LinkedIn Headline:** Climate activist | Regenerative consultant | storyteller |Land right activist | Nature-Based Solution | DRR expert

**LinkedIn About:** As Senior Project Coordinator at Soil4Climate Inc. Tanzania, I contribute to climate change mitigation through strategic project management and climate action planning. My work aligns with the organization's mission to promote sustainable solutions, leveraging my expertise in environmental disaster management and grassroots mobilization. With a Bachelor's degree in Environmental Disaster Management from the University of Dodoma, my commitment to fostering climate resilience and empowering commun

**Bio (Improved - ERA Standards):**

nding'a (Laizer) Orkeyaroi is a climate activist, regenerative consultant, storyteller, and land rights activist. He works at the intersection of indigenous rights, climate justice, and regenerative land stewardship, amplifying marginalized voices in environmental movements.

As Senior Project Coordinator at Soil4Climate Inc. Tanzania, nding'a contributes to climate change mitigation through strategic project management and climate action planning. his  work aligns with the organization's mission to promote sustainable solutions, leveraging his expertise in environmental disaster management and grassroots mobilization.

With a Bachelor's degree in Environmental Disaster Management from the University of Dodoma, he is also Director at Tanzania Eco Warriors Initiative (TEWI). 

**Fields:**

- **Affiliation:** This participant's company is not listed in the calendar event
- **LinkedIn:** https://www.linkedin.com/in/nding-a-orkeyaroi-8a73081b7
- ERA Africa

**Notes:**

_[No research notes yet]_

---
