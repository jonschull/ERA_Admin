# Summary

**Document:** ERA Members Lacking Bios - Version 7
**Date:** October 27, 2025
**Status:** 🚀 Active - Ongoing enrichment

## Stats

- **Total ERA Members Needing Bios:** 30
- **With Bio Drafts:** 3
- **Removed This Iteration:** 16 APPROVED (processed to database)

## Recent Changes (V7 - October 27, 2025)

- ✅ **V6 Processing Complete** - 16 APPROVED members processed to database
  - 6 ERA Africa participants tagged (Emmanuel Uramutse, Fadja Robert, Hashim Yussif, Mtokani Saleh, Mutasa Brian, Theopista Abalo)
  - 5 database corruptions fixed (Kaluki Paul Mutuku, Minot Weld, Roberto Forte, Roberto Pedraza Ruiz, Scott Schulte)
  - 2 non-members corrected (Fred Ogden, Scott Schulte - era_member set to 0)
  - 1 duplicate merged (nding'a ndikon merged into Joshua Laizer)
- 📊 **V7 ready** - 30 members remaining (non-APPROVED entries from V6)

---

## Recent Changes (V6)

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

## 1. Angelique Garcia [APPROVED]

**Bio:**

Angelique Rodriguez is a water activist and regenerative community developer based in Crestone, Colorado. Through her organization Water-Unite, she travels on "water tours" sharing water wisdom and innovative purification technologies. Angelique works at the intersection of water activism, women's health, and ecosystem restoration. Her reusable menstrual pads project brings sustainable business models, manufacturing capacity, and economic opportunity to women in Uganda, Kenya, and South Africa. Passionate about mycoremediation, she collaborates with mycologists to explore mushroom-based solutions for water purification and ecosystem healing. Working with Maasai communities, Angelique trains local citizens as environmental scientists. Her philosophy centers on listening to "Source Mother Water" for guidance in creating regenerative solutions. She was invited to ERA by Elizabeth Herald.

**Fields:**

- **Affiliation:** Water-Unite (water activism organization)
- **Location:** Crestone, Colorado
- **Full Name:** Angelique Rodriguez (uses Angelique Garcia in some contexts)

**Notes:**

🔍 **RESEARCH FINDINGS (Pass 1):**

**Fathom Database (ID: 2684):**

- Location: Crestone, Colorado
- Source calls: ERA Town Hall Meeting (2 calls)
- Collaborating with: Michael Mayer, Jon Schull, Eliza Herald, Mitchell Rabin, Lisa Merton, Wambui Muthee, and others

**Town Hall Transcripts - EXTENSIVE PARTICIPATION:**

- Presented at Town Hall on water projects and regenerative work
- **Water-Unite.com** - water activism/education platform
- **Reusable menstrual pads project** in Uganda, Kenya, South Africa - bringing business model, capacity, machines to communities
- **Mycelium/mycoremediation work** - collaborating with mycologist, exploring mushroom potential for restoration
- **"Water tour"** - traveling and "sharing water messages"
- Philosophy: "I only listen to the wisdom Source Mother Water gives me. She showed me how to do this."
- Works with Maasai communities
- Invited to ERA by Elizabeth

**Town Hall Quotes:**

- "I am working with Maasai community...it is an opportunity to train the locals to be citizen scientists"
- Russ Speer: "Angelique - you're an Ingenious Angel!!!"
- Colin Grant: "Angelique, I pioneered mycoremediation in the 90s"

**RECOMMENDATION:** ✅ **ERA MEMBER - CREATE BIO**

- Strong Town Hall participation with presentation
- Multi-faceted work: water activism, menstrual health, mycoremediation, community development
- Active collaborator in ERA network
- Ready for comprehensive bio focusing on water/community/regenerative work

---

---

## 2. Arun Bangura [**ERA Africa, not a member]**

_[Draft needed - limited information available]_

**Fields:**

- **Affiliation:** Not listed
- **Location:** Kenya

**Notes:**

🔍 **RESEARCH FINDINGS (Pass 1):**

**Fathom Database (ID: 1492):**

- Location: Kenya
- Source call: ERA Africa
- Collaborating with: nding'a ndikon (Joshua Laizer), Jon Schull, Leonard IYAMUREME, Richard Tusabe, Theopista Abalo, Malaika Patricia, Anna Akpe, Mr. Kipilangat Kaura, mbilizi Kalombo

**ERA Africa Transcripts:**

- ❌ No speaking mentions found in transcripts
- Attended ERA Africa meeting but did not speak (or wasn't captured in transcript)

**RECOMMENDATION:** ⚠️ **NEED MORE INFO - ERA AFRICA ATTENDEE**

- Confirmed attendance at ERA Africa meeting
- No bio-worthy information in transcripts
- **Question for USER:** Do you have any other records (emails, notes) about Arun Bangura from Kenya? Without additional context, difficult to create meaningful bio.

---

---

## 3. Aviv Green [APPROVED]

**Bio:**

Aviv Green is an Israeli filmmaker and ecosystem restoration advocate who founded the EcoNomads YouTube channel to document regenerative projects worldwide. With a degree in agroecology and experience in food forests and permaculture, Aviv creates short films showcasing successful ecological initiatives, from an Indian village planting 111 trees for every baby girl born to indigenous land stewardship practices. His current focus is a partnership with a Samburu semi-nomadic pastoralist community in one of Kenya's most remote regions, where families live dispersed across wild savannah alongside elephants, hyenas, and lions. Working with a young Samburu woman named Priscilla, Aviv documents how pure pastoralist communities who never plowed their land are adapting traditional livestock practices to changing climate patterns. His work bridges filmmaking, ecosystem restoration, and indigenous partnerships, demonstrating his vision that "places where people live should be the places where they bring back the ecosystem." Aviv collaborates with John D. Liu and Ian Redmond.

**Fields:**

- **Affiliation:** Founder of EcoNomads YouTube channel, Pastoralist Savannah Restoration Center (Kenya)
- **Location:** Israel (working in Kenya)
- **Age:** 31

**Notes:**

🔍 **RESEARCH FINDINGS (Pass 1):**

**Fathom Database (ID: 16):**

- Source call: ERA Town Hall Meeting
- Collaborating with: John D. Liu, Priscilla (Samburu woman), Ian Redmond

**Town Hall Presentation - EXTENSIVE CONTENT:**

- **EcoNomads YouTube channel** - documenting ecological projects worldwide
- **Background:** Agroecology degree, worked in food forests/permaculture
- **Current work:** Partnering with Samburu semi-nomadic pastoralist community in remote Kenya
- **Key innovation:** Connecting indigenous land stewardship with ecosystem restoration
- Samburu are pure pastoralists (meat/milk/blood diet until 20 years ago, never plowed land)
- Working on climate adaptation as weather patterns change
- Philosophy: Merging places where people live with biodiversity/ecosystem restoration
- First film: Indian village planting 111 trees per baby girl born

**Presentation highlights:**

- "Places where people live should be the places where they bring back the ecosystem"
- Works in "one of the most remote places in Kenya" - 1 hour motorbike through savannah
- Community lives among elephants, hyenas, lions in vast unaltered savannah
- Brings filmmaking/documentation to amplify indigenous conservation practices

**RECOMMENDATION:** ✅ **ERA MEMBER - CREATE COMPREHENSIVE BIO**

- Excellent presentation with clear narrative arc
- Unique niche: filmmaker + ecosystem restoration + indigenous partnerships
- Strong ERA engagement (Ian Redmond connection, Global Hall of Heroes mention)
- Ready for detailed bio highlighting EcoNomads work and Samburu partnership

---

---

## 4. Chris Pilley [ERA_Africa not a member]

**Bio:**

_[Draft needed - limited info]_

**Fields:**

- **Affiliation:** Safari company, SOTOP camp
- **Location:** Tanzania

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** ERA Town Hall Meeting attendee (Tanzania)
**Transcripts:** ❌ No speaking mentions found

**RECOMMENDATION:** ⚠️ **NEED MORE INFO**

- Safari company/SOTOP camp suggests tourism/conservation connection
- **Question for USER:** Any emails or context about Chris Pilley's ERA involvement?

---

---

## 5. Delkhwa habibi [remove from database]

**Bio:**

_[Draft needed]_

**Fields:**

- **Affiliation:** Not listed
- **Location:** Kabul, Afghanistan

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** Private meeting with Mazharudin habibi / Jon Schull
**Transcripts:** Not in Town Hall transcripts (private meeting)

**RECOMMENDATION:** ⚠️ **LIKELY NOT ERA MEMBER - PRIVATE MEETING ONLY**

- Appears in private meeting context, not Town Hall
- May be related to Mazharudin habibi
- **Question for USER:** Was this person introduced at a Town Hall, or just a private conversation participant?

---

---

## 6. Dushime Ange Leo Clevis [APPROVED and  ERA AFRICA]

**Bio:**

Ange Leo Clevis Dushime is an environmental activist from the University of Rwanda College of Science and Technology in Kigali, Rwanda. He is part of the growing network of young African environmental leaders engaged in ecosystem restoration and climate action.

**Fields:**

- **Affiliation:** Not listed
- **Location:** Rwanda

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** ERA Town Hall Meeting (Rwanda)
**Transcripts:** ❌ No speaking mentions found in Town Hall or ERA Africa

**RECOMMENDATION:** ⚠️ **NEED MORE INFO - TOWN HALL ATTENDEE**

- Attended Town Hall from Rwanda
- **Question for USER:** Any other records about Dushime Ange Leo clevis? Email correspondence?

---

---

## 7. Elizabeth Morgan Tyler [APPROVED - MINIMAL BIO]

**Bio:**

Elizabeth Morgan Tyler is a water activist based in Shimakum, Washington. She is particularly focused on water issues and participates in the EcoRestoration Alliance network.

**Fields:**

- **Affiliation:** Water activism
- **Location:** Shimakum, Washington, USA

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** ERA Town Hall Meeting (Shimakum, Washington)
**Town Hall Transcripts:** ✅ Brief intro only - water activist

- Attended 6am her time, just woke up
- "particularly focused on water issues"
- Lives near Michael Polarski

**RECOMMENDATION:** ✅ **ERA MEMBER - MINIMAL BIO**

- Limited information available
- Generic water activism bio appropriate

**⚠️ NOTE:** Initially confused with Eliza Herald (who does nanofibers work with Angelique/James). They are two different people.

---

---

## 8. Eliza Herald (goes by "Elizabeth") [ALREADY HAS BIO IN DATABASE]

**Bio:**

**Existing bio in Airtable (ID: 218):**

• **WATER STEWARD:** TIME IS NOW to remember our core sacred relationship with Our Essential Source Water. The crystalline Water flowing through the beautiful lakes and rivers of the world's high mountains has been a beacon for me since early childhood. The gift of being a child growing up nourished by one of the Sacred Water Hearts of the World, Da ow ga (Lake Tahoe), has defined and guided my life journey and inspired me to co-create whole system design to connect and support Water Stewards across the planet in a network of Water Sanctuaries and Water Wisdom Councils ~ What a Concept!

• **SCREENWRITER:** Streaming TV Series in development / I AM WATER ~ Our World's Love Song / Telling an epic story of remembrance for the human relationship to Water, offering audacious hope for evolution by celebrating our innate capacity to affect beneficial change (together) drawing upon our collective intelligence to shift our species fatal Water Amnesia.

• **MEDIA PRODUCTION:** 27 years in the media production field with well-established skills as a content writer, editor, graphic artist, and camera operator. Working primarily as a video editor and camera operator.

• **TAHOE INTERNATIONAL FILM FESTIVAL:** Founder, Executive Director, Program Director co-creating this innovative showcase for filmmakers committed to affecting beneficial change through transformational media.

**Fields:**

- **Affiliation:** Watershed Wisdom Councils
- **Email:** watershedwisdomcouncils@gmail.com
- **Location:** Lake Tahoe region

**Notes:**

✅ **BIO ALREADY IN DATABASE - NO ACTION NEEDED**

🔍 **RESEARCH FINDINGS:**

**Town Hall Presentation:** Extended presentation on Watershed Wisdom Councils, radical collaboration, water wisdom
**Works with:** Angelique Rodriguez, James Bowen on nanofibers/water purification
**Philosophy:** "Water is source, not resource"
**Background:** Lived 7 years on Yuba River, meditative relationship with water, worked with Grandmother Agnes (13 Indigenous Grandmothers)
**Called "Elizabeth" by:** Russ Speer, Jake Fairbanks Kelley in transcripts

**Key quote:** "I hear water talking to me in the simplest terms...recognizing that water is source, not resource, very simply that water is source."

---

---

## 11. Gary Glass [not member]

**Bio:**

_[Draft needed]_

**Fields:**

- **Affiliation:** Open Future Coalition (possibly)
- **Location:** Unknown

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** Source call "Kaiti, Gary, Deb" (private meeting, not Town Hall)
**Transcripts:** ❌ Not found in Town Hall transcripts

**RECOMMENDATION:** ⚠️ **LIKELY NOT ERA MEMBER - PRIVATE MEETING ONLY**

- Appears only in private meeting context
- No Town Hall attendance record
- **Question for USER:** Was Gary Glass introduced at a Town Hall? Or just private conversation?

---

---

## 12. Gwen [remove from database]

**Bio:**

_[No bio needed]_

**Fields:**

- **Affiliation:** Not listed

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** Private meeting "Gwendolyn Wheatley / Jon Schull"
**Transcripts:** ❌ Not in Town Hall

**RECOMMENDATION:** ❌ **NOT ERA MEMBER - REMOVE**

- Only appears in private meeting, never introduced at Town Hall

---

---

## 13. Hadziqah [drop from database]

**Bio:**

_[Draft needed - minimal info]_

**Fields:**

- **Affiliation:** Brunei (country affiliation)
- **Location:** Brunei

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** ERA Town Hall Meeting (Brunei)
**Transcripts:** ❌ No speaking mentions

**RECOMMENDATION:** ⚠️ **NEED MORE INFO**

- Rare: Brunei participant
- **Question for USER:** Any context about Hadziqah from Brunei? Emails?

---

---

## 15. Heraclio Herrera [APPROVED]

**Bio:**

**Bio (Improved - ERA Standards):**

Heraclio Herrera is an environmental management specialist at Congreso General Kuna in Panama. His work focuses on indigenous environmental governance and sustainable resource management within Kuna communities.

**Fields:**

- **Affiliation:** Congreso General Kuna (CUNA Institute)
- **LinkedIn:** https://www.linkedin.com/in/heraclio-herrera-r-b7b05531

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** Private meeting "Heraclio Hererra and the Guna"

**RECOMMENDATION:** ⚠️ **CHECK ERA MEMBER STATUS**

- Bio already exists (good quality)
- LinkedIn already captured
- **Question for USER:** Was Heraclio introduced at Town Hall? Or just private meeting? If only private meeting, may not be ERA member.

---

---

## 16. Ilarion Larry Merculief [APPROVED]

**Bio:**

Ilarion "Larry" Merculief is an Unangan (Aleut) indigenous leader, wisdom keeper, and author of "Wisdom Keeper: One Man's Journey to Honor the Untold Story of the Unangan People." Larry's work preserves and amplifies Unangan indigenous knowledge systems and perspectives on ecosystem stewardship and cultural wisdom, connecting traditional ecological knowledge with contemporary restoration movements. His book and presentations bridge indigenous wisdom with global efforts toward regenerative practices and cultural preservation.

**Fields:**

- **Affiliation:** Author, Indigenous wisdom keeper
- **LinkedIn:** https://www.linkedin.com/in/ilarion-larry-merculief-15b6429/

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** ERA Town Hall Meeting + GERC meeting
**Town Hall Transcripts:** ✅ Mentioned as scheduled speaker

- Author of "[Wisdom Keeper: One Man&#39;s Journey to Honor the Untold Story of the Unangan People](https://www.northatlanticbooks.com/shop/wisdom-keeper/)"
- Unangan (Aleut) indigenous leader
- Was scheduled to present at Town Hall

**RECOMMENDATION:** ✅ **ERA MEMBER - CREATE BIO**

- Prominent indigenous leader and author
- Scheduled Town Hall presenter
- Strong credentials
- Ready for bio highlighting Unangan wisdom keeper role and book

---

---

## 17. Ivan Owen [APPROVED]

**Bio:**

Ivan Owen is an artist and innovator based in Limerick, Ireland.  Co-founder of Enabling The Future), which provides free, open-source 3D printed prosthetics, he is self-taught in engineering and animation.  These days, Ivan creates innovative and whimsical artwork including giant puppeteer hands and captivating stop-motion videos depicting ecosystem restoration efforts aroudn the world. Drawing inspiration from music, society, and technology, he shares his artistic creations on YouTube and TikTok.

**Fields:**

- **Affiliation:** Social Glassa, Enabling The Future (co-founder)
- **Location:** Limerick, Ireland

**Notes:**

🔍 **Bio found in ERA_MEMBERS_LACKING_BIOS.md**

---

---

## 18. Jerald Katch. [Approved]

**Bio:**

Jed holds a Ph. D. in Developmental and Educational Psychology from the University of Chicago and an M. Ed. in Special Education from Boston University.  He has taught in grades K-12, college, and graduate school programs.  Jed specializes in connecting student interests with real world activities.  At Bio4Climate, he is working to create opportunities for young environmental activists to combine their interests in eco-restoration with gaining academic credit in schools and in higher education.

**Fields:**

- **Affiliation:** Biodiversity for Livable Climate

**Notes:**

_[No research notes yet]_

---

---

## 19. Juan Bernal [APPROVED]

**Bio:**

Juan Bernal is Executive Director of Geoversity, Panama's Ecological University, and an Obama Fellow. He leads initiatives in ecological education and sustainable development, bridging traditional knowledge with contemporary environmental challenges. Through Geoversity, Juan advances transformative learning experiences that connect students with Panama's rich biodiversity and indigenous wisdom, fostering a new generation of environmental leaders committed to regenerative practices and ecosystem stewardship.

**Fields:**

- **Affiliation:** Obama Fellow, Executive Director of Geiversity Panama's Ecological University
- **Location:** Panama

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** ERA Town Hall Meeting (Panama)
**Transcripts:** ⚠️ Limited mentions

**RECOMMENDATION:** ✅ **ERA MEMBER - CREATE BIO**

- Obama Fellow
- Executive Director of Geiversity (Panama's Ecological University)
- Town Hall attendee
- Ready for bio on ecological education leadership

---

---

## 22. Kathia Burillo APPROVED

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

---

## 23. Kevin A. [remove from databadse]

**Bio:**

_[No bio needed]_

**Fields:**

- **Affiliation:** Florida International University
- **Location:** Florida

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** Private meeting only "Kevin A. Adkins, Ph.D. / Jon Schull"
**Transcripts:** ❌ Not in Town Hall

**RECOMMENDATION:** ❌ **NOT ERA MEMBER - REMOVE**

- Only appears in private meeting context

---

---

## 24. Kevin Li [NOT ERA MEMBER]

**Bio:**

_[No bio needed]_

**Fields:**

- **Affiliation:** USDA (based in Penn State)
- **Location:** Michigan

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** Private meeting only (same meeting as Kevin A.)
**Transcripts:** ❌ Not in Town Hall

**RECOMMENDATION:** ❌ **NOT ERA MEMBER - REMOVE**

- Only appears in private meeting context
- V7 already marked "[NOT A MEMBER]"

---

---

## 25. Lauren Miller [NEED MORE INFO]

**Bio:**

_[Draft needed if member]_

**Fields:**

- **Affiliation:** Not listed
- **Location:** New York, Hudson Valley

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** ERA Town Hall Meeting (New York, Hudson Valley)
**Transcripts:** ❌ No speaking mentions

**RECOMMENDATION:** ⚠️ **NEED MORE INFO**

- Attended Town Hall from Hudson Valley
- No bio-worthy content found
- **Question for USER:** Any context about Lauren Miller?  [NO. HOW DID SHE GET INTO THE DATABASE?]

---

---

## 26. Lisa Merton [APPROVED]

**Bio:**

Lisa Merton is affiliated with Greenbelt Movement International based in Vermont, continuing the legacy of Nobel Peace Prize laureate Wangari Maathai. She works to expand the Greenbelt Movement's mission of environmental conservation, community empowerment, and women's rights beyond Kenya to a global audience. Lisa connects grassroots tree-planting initiatives with broader movements for climate justice, democratic governance, and sustainable development, helping communities worldwide adopt the Greenbelt model of linking environmental restoration with social transformation.

**Fields:**

- **Affiliation:** Greenbelt Movement International
- **Location:** Vermont

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** ERA Town Hall Meeting (Vermont)
**Town Hall Transcripts:** ✅ Appears in collaborators (with Angelique Garcia)

**RECOMMENDATION:** ✅ **ERA MEMBER - CREATE BIO**

- Greenbelt Movement International (Wangari Maathai legacy)
- Town Hall attendee
- Ready for bio on Greenbelt work

---

---

## 27. Malaika Patricia [ERA AFRICA; Not a ERA]

**Bio:**

_[Draft needed if info found]_

**Fields:**

- **Affiliation:** Not listed
- **Location:** Uganda

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** ERA Africa (Uganda)
**Transcripts:** ❌ No speaking mentions
**Collaborators:** Theopista Abalo, Arun Bangura, nding'a ndikon, others

**RECOMMENDATION:** ⚠️ **NEED MORE INFO - ERA AFRICA ATTENDEE**

- Attended ERA Africa from Uganda
- **Question for USER:** Any context about Malaika Patricia?

---

---

## 28. Mary Ann Edwards [ERA MEMBER - IN AIRTABLE, NOT IN FATHOM DB]

**Bio:**

_[No bio yet - need to research]_

**Fields:**

- **Email:** maedwardsrn@gmail.com
- **Affiliation:** Author (per Airtable)
- **Airtable ID:** rec4ZE6kCrw8JggG6

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Airtable:** ✅ Confirmed ERA member, listed as "Author"
**Fathom Database:** ❌ NOT in Fathom database (no call records)
**Previous error:** "Nakavali" location was from a DIFFERENT participant (from Iuri Herzfeld meeting)

**RECOMMENDATION:** ✅ **ERA MEMBER - NEEDS BIO RESEARCH**

- Confirmed in Airtable as ERA member
- No Fathom call records found
- Action needed: Find bio information from other sources

---

---

## 29. Matthew Hooper [dig deeper]

**Bio:**

_[No bio needed]_

**Fields:**

- **Affiliation:** Not listed
- **Location:** Southwestern Connecticut

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** Private meeting only "Matthew Hooper / Jon Schull"
**Transcripts:** ❌ Not in Town Hall

**RECOMMENDATION:** ❌ **NOT ERA MEMBER - REMOVE**

- Only appears in private meeting context

---

---

## 32. Missy Lahren [APPROVED]

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

---

## 33. Mr. Kipilangat Kaura -TAWI [APPROVED]

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

---

## 35. Munyembabazi Aloys [ERA AFRICA - NEED MORE INFO]

**Bio:**

_[Draft needed if info found]_

**Fields:**

- **Affiliation:** Not listed
- **Location:** Unknown

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** ERA Africa
**Transcripts:** ❌ No speaking mentions

**RECOMMENDATION:** ⚠️ **NEED MORE INFO - ERA AFRICA ATTENDEE**

- Attended ERA Africa meeting
- No bio-worthy content found
- **Question for USER:** Any context about Munyembabazi Aloys?

---

---

## 37. Myra Jackson [APPROVED]

**Bio:**

Myra Jackson served from 2012 to 2015 on the UN Open Working Group on Sustainable Development Goals (SDGs), where after being adopted by 192 member states, she helped communicate the 17 SDGs from global fora to local communities and subnational governments. She initially served as a UN Representative and focal point on Climate Change for the UN Major Groups Commons Cluster, a Senior Advisor on Whole Earth Civics, and is currently the UNFCCC Head of Delegation for Earth Law Center, as well as a member of the UN Harmony with Nature Expert Platform. Myra is currently focused on the regeneration of Earth's most critical ecosystems in what she calls the Great Work of our time — a call that summons all who are alive today to recognize that the well-being of the Earth is inextricably linked to the well-being of humanity and all life forms.

**Fields:**

- **Affiliation:** Earth Regeneration Alliance, Earth Law Center
- **Website:** https://www.earthregenerationalliance.com/

**Notes:**

🔍 **Bio found in ERA_MEMBERS_LACKING_BIOS.md**

---

---

## 42. Steffie Rijpkema [Approved]

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

---

## 43. Stella Nakityo [ERA AFRICA - NEED MORE INFO]

**Bio:**

_[Draft needed if info found]_

**Fields:**

- **Affiliation:** Not listed
- **Location:** Unknown

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** ERA Africa
**Transcripts:** ❌ No speaking mentions

**RECOMMENDATION:** ⚠️ **NEED MORE INFO - ERA AFRICA ATTENDEE**

- Attended ERA Africa meeting
- **Question for USER:** Any context about Stella Nakityo?

---

---

## 45. Wambui Muthee [APPROVED. ERA_member and ERA_africa ]

**Bio:**

Wambui Muthee works with the Greenbelt Movement in Nairobi, Kenya, the grassroots environmental organization founded by Nobel laureate Wangari Maathai. The Greenbelt Movement has planted over 51 million trees across Kenya while empowering communities, particularly women, through environmental conservation and advocacy. Wambui continues this vital work connecting tree planting with livelihood improvement, climate resilience, and democratic space, carrying forward Maathai's vision that environmental conservation and social justice are inseparable.

**Fields:**

- **Affiliation:** Greenbelt Movement
- **Location:** Nairobi, Kenya

**Notes:**

🔍 **RESEARCH FINDINGS:**

**Fathom Database:** ERA Town Hall Meeting (Nairobi, Kenya)
**Town Hall Transcripts:** ✅ Appears in collaborators (with Angelique Garcia)

**RECOMMENDATION:** ✅ **ERA MEMBER - CREATE BIO**

- Greenbelt Movement (Wangari Maathai's organization)
- Town Hall attendee
- Kenya-based
- Ready for bio on Greenbelt Movement work

---
