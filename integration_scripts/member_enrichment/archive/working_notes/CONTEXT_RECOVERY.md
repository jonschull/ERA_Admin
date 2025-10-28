# CONTEXT RECOVERY: Member Bio Enrichment

**Purpose:** When Claude shows signs of degradation (hallucinations, inconsistencies, loss of standards), use this to restore clean context.

**Last Updated:** October 26, 2025  
**Version:** 1.0

---

## Context Recovery Checklist

When user says "recover context" or "reload standards," Claude MUST:

### 0. Regain the Big Picture

**What is ERA?**
- **EcoRestoration Alliance** - Network of practitioners, scientists, and advocates
- Mission: Ecological restoration to cool the planet, restore water cycles, rebuild ecosystems
- Connected to Bio4Climate (Biodiversity for a Livable Climate)
- Jon Schull is key leader/organizer
- Town Halls are primary engagement mechanism

**Why are we writing bios?**
- **Member directory** - Help members discover each other's expertise
- **Community building** - Show the diversity and depth of the network
- **Engagement tool** - Make people feel seen and valued
- **Recruitment** - Show potential members the caliber of the community
- **NOT resume collection** - These are narrative bios showing mission connection

**How does this fit larger ERA admin work?**
- Part of member enrichment initiative
- Follows Phase 4B-2 participant reconciliation (database cleanup)
- Builds on Town Hall transcript analysis (who said what, who attended)
- Feeds into member directory, website, communications
- Pattern: AI does mechanical work, human does intelligent synthesis

**Philosophy of this approach:**
- **Context-rich over template-filling** - Each bio tells a story
- **Intelligent synthesis over automation** - Human judgment essential
- **Multiple sources over single source** - Cross-check for accuracy
- **Specific over generic** - Projects, philosophies, quotes matter
- **Connected over credentials** - Show HOW they engage with ERA mission

**What makes a good ERA bio different from LinkedIn?**
- LinkedIn = career summary for job search
- ERA bio = mission connection + unique value to restoration community
- LinkedIn focuses on "what I do"
- ERA bio focuses on "what I bring to restoration" + "why I'm here"

### 1. Read Core Documents (in order)
```
☐ PROCESS.md - Full workflow and standards
☐ approved_bios.md - Current approved examples
☐ BATCH3_SUMMARY.md (or latest) - Recent progress
☐ batch3.md (or latest) - Latest aggregated data
```

### 2. Internalize Bio Standards

**Length:**
- Students/Early career: 400-600 chars
- Mid-career: 600-800 chars
- Established leaders: 800-1000 chars
- **MAX:** 950 chars

**Voice:**
- Third person, conversational
- Professional but warm
- Narrative flow (not resume-style)

**Required Elements:**
1. Current work/role
2. Professional background (brief)
3. ERA connection/engagement (specific, not generic)
4. Unique value/perspective
5. Optional: Philosophy/personal touch

**Quality Checks:**
- ✅ Accurate (verified against sources)
- ✅ Contextual (shows HOW they engage, not just credentials)
- ✅ Current (database often more current than LinkedIn)
- ✅ Specific (projects, philosophies, not generic)
- ✅ Connected (ERA relevance clear)

### 3. Review Approved Examples

**Read and internalize tone/style from:**
- Ben Rubin (839 chars) - Teacher, nature classroom project
- Noura Angulo (836 chars) - Student, quantitative research

**Note patterns:**
- Concrete projects mentioned ("nature peace classroom")
- Philosophy quotes ("taking nature to kids")
- Technical skills when relevant (R, Stata, GIS)
- Career transitions explained (pandemic career change)
- ERA engagement specific (internship with B4C)

### 4. Review Data Sources Priority

**Source reliability (most → least):**
1. **Town Hall transcripts** - Person's own words, current projects
2. **Database** - Current affiliation, contact info
3. **Airtable** - Existing records, affiliated orgs
4. **LinkedIn** - Often outdated, verify with #1-2
5. **Google Contacts** - Phone numbers only

**Critical Rule:** If LinkedIn contradicts Town Hall/Database, trust Town Hall/Database.

**Example:** Ben Rubin's LinkedIn says "Media Coordinator at E-nable" (volunteer work), but database + transcripts show he's actually a full-time teacher. The bio leads with teacher role.

### 4B. THE CORE DISCIPLINE: INTELLIGENT READING

**Your job is NOT to:**
- ❌ Count metrics (321 mentions!)
- ❌ Trust database entries blindly
- ❌ Infer from patterns without verification
- ❌ Add ERA posturing ("demonstrates that restoration requires...")
- ❌ Puff up credentials ("navigate complex institutional landscapes")

**Your job IS to:**
1. **READ what the person actually SAID in transcripts**
   - Their self-introduction
   - Their presentation content
   - Their contributions to discussions
   
2. **VALIDATE your understanding against sources**
   - Does LinkedIn match transcripts?
   - Does database match reality?
   - Is "Craig McNamara" actually "Craig Erickson"?
   
3. **SYNTHESIZE into concise, accurate bio**
   - Simple factual statements
   - Direct quotes when powerful
   - No mission statements added
   - No embellishment
   - **Don't embellish what we know**

**Specific Rules (from Batch 4, 5 & 6 feedback):**

✅ **DO:**
- Use "promotes/works on/focuses on" for unverified roles
- Make bios timeless (present tense, no specific dates unless critical)
- Focus on their work, not ERA process
- Add specificity when context clearly supports it
- Use specific skills from LinkedIn (e.g., "algae cultivation") not generic terms
- Add member collaborations when known and verified
- **CHECK era_member field** - flag non-members for review (but field can be wrong!)
- **Validate LinkedIn fuzzy matches** - if <90%, flag as uncertain
- **Use their own words** - If LinkedIn is only source, use verbatim (don't AI-rewrite)
- **VERIFY before trusting database** - especially for .edu emails, well-known names, minimal descriptions
- **Web search well-known names** - don't assume database knows who they are
- **Search Town Hall agendas** - grep for names if membership unclear

❌ **DON'T:**
- Use "leads/spearheads/pioneers" without verification
- Include "attended Town Hall on [date]" - exception: if presentation IS their defining achievement
- Include "introduced by [person]" or "connected through [person]"
- Include future projections ("upcoming project will...")
- Add ERA meta-commentary ("reflects ERA's recognition...")
- Speculate about skills not verified in sources
- Write bios for non-members without flagging/confirming
- Trust fuzzy LinkedIn matches <90% without verification
- **Trust database descriptions blindly** - they can be completely wrong

**🚨 DATABASE CAN BE WRONG (Batch 6 lesson):**
- Charles Eisenstein: Database said "water consultant", reality: famous author
- Mark Luckenbach: Database said "Connecticut behavior change", reality: Virginia marine scientist
- Rayan Farhoumand: Database said `era_member: false`, reality: ERA intern

**Verification triggers:**
- .edu email → Research institution + LinkedIn
- Famous-sounding name → Web search
- Minimal database description → Probably incomplete
- Geographic mismatch → Verify location

**Example of wrong approach:**
- Saw "321 transcript mentions"
- Claimed "one of ERA's most engaged members"
- Never READ the transcripts
- 321 was aggregator bug (each timestamp = separate entry)
- Confabulated "consistently contributing insights on tropical restoration"

**Example of right approach:**
- Read Eduardo's June 2025 presentation
- He presented "Greening Central American Pacific Coast"
- He connected migration crisis to desertification
- Bio: "Eduardo proposes [project name] to address [problem]"
- No claims about engagement level without verification
- No "presented at Town Hall" - just the work itself

**Exception for Town Hall mention:**
If member's ONLY verified achievement is a Town Hall presentation (no LinkedIn, no org, just the presentation), then mentioning it provides necessary context:
- WRONG: "John attended ERA's Town Hall"
- RIGHT: "John presented his watershed restoration framework at ERA"
- Context: The presentation itself IS the achievement worth noting

**When to use their own words verbatim:**
If LinkedIn is the only substantive source (no transcripts, minimal database info):
- WRONG: "Scott is a research scientist focused on environmental and climate research" (generic AI rewrite)
- RIGHT: Use LinkedIn About section verbatim or lightly edited
- Rationale: Respect their self-description; don't "AI-wash" their words
- Only synthesize when you can add value from multiple sources

### 5. Remember Key Patterns

**From PROCESS.md "Key Patterns (Hard-Won)":**

1. **Database Often More Current Than LinkedIn**
   - LinkedIn shows past/volunteer work as primary
   - Database + transcripts = current reality

2. **Transcripts Are Gold**
   - Self-introductions reveal current projects
   - Philosophy in their own words
   - Prioritize members with Town Hall attendance

3. **Phone Numbers Rare**
   - Only ~25% have phones in Google Contacts
   - Note when found, but don't wait for them

4. **LinkedIn Content in HTML**
   - `full_text` field has 5-30K chars
   - Don't just read structured fields
   - About, Experience, Education all in there

### 6. State Readiness

After completing checklist, Claude responds:
```
✅ Context recovered. Ready to write bios.

BIG PICTURE:
- ERA = EcoRestoration Alliance (restoration practitioners + scientists)
- Purpose: Member directory showing mission connection + unique value
- Philosophy: Context-rich narratives, not LinkedIn summaries
- Approach: Intelligent synthesis from multiple sources

CORE DISCIPLINE:
- READ what person said in transcripts
- VALIDATE understanding against sources
- SYNTHESIZE into concise, accurate bio
- NO metrics shortcuts (321 mentions!)
- NO ERA posturing ("demonstrates that...")
- NO puffing credentials ("navigate complex...")

STANDARDS:
- Length: 600-950 chars (target ~800)
- Voice: Third person, conversational, warm
- Required: Current role, background, ERA engagement, unique value
- Quality: Accurate, contextual, specific, connected

EXAMPLES:
- Ben Rubin (teacher, nature classroom)
- Noura Angulo (student, quantitative research)

DATA PRIORITY: 
TH transcripts > Database > Airtable > LinkedIn

Ready for batch [N] - [X] members
```

---

## When to Trigger Context Recovery

**Signs of Degradation:**

**Quality Issues:**
- ❌ Hallucinations (inventing info not in sources)
- ❌ Wrong tone (too formal/resume-like)
- ❌ Wrong length (too short <400 or too long >1000)
- ❌ Generic language ("skilled professional," "passionate about")
- ❌ Missing ERA connection (reads like LinkedIn copy)
- ❌ Data inconsistencies (LinkedIn contradicting database)
- ❌ Loss of specificity (no projects, philosophies, quotes)

**Loss of Big Picture:**
- ❌ Treating bios as LinkedIn summaries (not mission-connected narratives)
- ❌ Focusing on credentials over engagement
- ❌ Missing the "why they're here" element
- ❌ Not showing unique value to restoration community
- ❌ Forgetting this is for member discovery, not job search

**Recommended Frequency:**
- After every 4-6 bios (quality check)
- Before starting new batch (reset context)
- Anytime quality concerns arise
- **When losing sight of why we're doing this** (big picture check)

---

## Sub-Agent Mode Protocol

When acting as BioWriter sub-agent (testing Deep Agents pattern):

### Clean Context Rules
1. **Only read:** Task file + CONTEXT_RECOVERY.md
2. **Don't reference:** Previous conversation, unrelated files
3. **Output:** Bio + char count + concerns ONLY
4. **No explanations:** Just the deliverable

### Task File Format
```json
{
  "member_name": "Jane Doe",
  "aggregated_data": { ... },
  "linkedin_text": "...",
  "examples": [
    {"name": "...", "bio": "..."},
    {"name": "...", "bio": "..."}
  ],
  "standards": {
    "length": "600-950 chars",
    "voice": "Third person, conversational",
    "required": ["current role", "background", "ERA engagement", "unique value"]
  }
}
```

### Response Format
```
BIO:
[bio text here]

CHAR COUNT: 842

DATA CONCERNS: 
- LinkedIn shows "consultant" but database says "professor" - used database
- No Town Hall mentions found - relied on LinkedIn + database only
```

---

## Quality Verification After Recovery

User should spot-check first bio after recovery:
- ✅ Length in range?
- ✅ Tone matches examples?
- ✅ ERA engagement specific?
- ✅ Data verified against sources?
- ✅ No hallucinations?

If YES to all → continue batch  
If NO → point out issues, repeat recovery

---

## Session Boundaries

**Start of session:**
1. User: "Recover context for bio enrichment"
2. Claude: Runs checklist, confirms ready
3. User: Proceeds with batch

**Mid-session degradation:**
1. User: "Quality dropping, recover context"
2. Claude: Runs checklist, confirms ready
3. Continue from where we were

**End of session:**
1. Save progress to `batch[N]_progress.md`
2. Next session starts with context recovery
3. Review progress file, continue

---

## Files to Keep Current

**Update after each session:**
- `approved_bios.md` - Add newly approved bios
- `BATCH[N]_SUMMARY.md` - Progress tracking
- `PROCESS.md` - Any new patterns learned

**Version control:**
- Context recovery version tracked in this file
- Major changes = new version number
- Minor updates = update "Last Updated" date

---

## Emergency Reset

If context recovery fails (quality still poor):

1. **Stop bio generation**
2. **User creates checkpoint:**
   ```
   Current status: [X] bios complete, [Y] pending
   Issues observed: [specific problems]
   Big picture lost: [what's being forgotten]
   ```
3. **New session (fresh context)**
4. **Start with context recovery (including big picture)**
5. **Review checkpoint, continue**

---

## Big Picture Mantras (Read When Lost)

When you forget why you're doing this or start treating bios like LinkedIn copies:

**Remember:**
1. **ERA members are restoration practitioners** - Not job seekers
2. **Bios show mission connection** - Not career achievements
3. **Unique value matters** - What do they bring to restoration community?
4. **Stories > credentials** - "Nature peace classroom" > "Visual arts teacher"
5. **Engagement > position** - Town Hall participation, projects, philosophy
6. **Community building** - Help members discover each other's expertise
7. **Human connection** - Make people feel seen and valued

**Ask yourself for each bio:**
- Does this show WHY they're part of ERA?
- Would another member reading this understand their unique value?
- Does this feel like a person with a mission, or a LinkedIn summary?
- Is there a story here, or just facts?

**Examples of getting it right:**
- Ben: "nature peace classroom" + "taking nature to kids and kids to nature" = STORY + PHILOSOPHY
- Noura: Student discovering connection between data and restoration = JOURNEY + UNIQUE PERSPECTIVE

**Examples of getting it wrong:**
- "Experienced professional with skills in X, Y, Z" = GENERIC, NO STORY
- "Member of ERA interested in restoration" = VAGUE, NO UNIQUE VALUE
- Just listing credentials without mission connection = LINKEDIN, NOT ERA

---

**Context recovery is NOT admission of failure - it's discipline for maintaining quality at scale.**

**Big picture recovery is NOT hand-holding - it's preventing mission drift during detailed work.**
