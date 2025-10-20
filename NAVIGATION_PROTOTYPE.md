# ERA Admin Navigation Prototype
**Purpose:** Working prototype of documentation navigation system  
**Status:** Testing design - click through scenarios to validate  
**Date:** October 20, 2025

---

## 📖 How to Use This Prototype

This single document simulates the entire documentation hierarchy using anchor links.

**Test these scenarios:**
1. [New AI assistant arrives](#scenario-1-new-ai)
2. [Working on FathomInventory authentication](#scenario-2-fathom-auth)
3. [Understanding Git workflow](#scenario-3-git-workflow)
4. [Lost in integration_scripts](#scenario-4-integration-lost)

**Or browse the hierarchy:**
- [Level 0: Main README](#level-0-readme)
- [Level 1: Orientation Docs](#level-1-orientation)
- [Level 2: Principles & Practices](#level-2-principles)
- [Level 3: Component READMEs](#level-3-components)
- [Level 4: Specialized Docs](#level-4-specialized)

---

## 🎬 Test Scenarios

<a name="scenario-1-new-ai"></a>
### Scenario 1: New AI Assistant Arrives

**User says:** "Read the docs and help me with this project"

**Path:**
1. Start → [README.md](#level-0-readme)
2. README directs AI to → [AI_HANDOFF_GUIDE.md](#ai-handoff-guide)
3. AI guide references → [WORKING_PRINCIPLES.md](#working-principles)
4. Ready to work on specific component → [Component READMEs](#level-3-components)

**Test:** Does AI find everything they need? Is anything redundant?

[Back to scenarios](#-how-to-use-this-prototype)

---

<a name="scenario-2-fathom-auth"></a>
### Scenario 2: Working on FathomInventory Authentication

**User says:** "The Fathom cookies expired, help me fix it"

**Path:**
1. Deep in → [FathomInventory/authentication/README](#fathom-auth)
2. References principle → [WORKING_PRINCIPLES.md](#working-principles) (testing approach)
3. Back to component → [FathomInventory/README](#fathom-readme)
4. Back to main → [README.md](#level-0-readme)

**Test:** Can you find principles without duplication? Can you get back to main?

[Back to scenarios](#-how-to-use-this-prototype)

---

<a name="scenario-3-git-workflow"></a>
### Scenario 3: Understanding Git Workflow

**User asks:** "What's our PR workflow?"

**Path:**
1. From → [README.md](#level-0-readme)
2. References → [WORKING_PRINCIPLES.md](#working-principles) (Git/PR section)
3. Also mentioned in → [AI_HANDOFF_GUIDE.md](#ai-handoff-guide)

**Test:** Is Git workflow findable? Is it explained once, referenced everywhere else?

[Back to scenarios](#-how-to-use-this-prototype)

---

<a name="scenario-4-integration-lost"></a>
### Scenario 4: Lost in integration_scripts

**User is confused:** "I'm in integration_scripts and don't know which README to read"

**Path:**
1. Lost in → [integration_scripts/README](#integration-readme)
2. Can find → [AI_WORKFLOW_GUIDE](#ai-workflow-specific) for Phase 4B-2
3. Can go back to → [README.md](#level-0-readme)

**Test:** Clear which doc to read when? Easy to get back?

[Back to scenarios](#-how-to-use-this-prototype)

---
---

# DOCUMENTATION HIERARCHY

---
---

<a name="level-0-readme"></a>
# Level 0: README.md (Front Door)

**Purpose:** System overview + entry point routing  
**Audience:** Everyone (humans & AI)

---

## 🚨 STARTING POINT - READ THIS FIRST

### 👥 **For Everyone:**

**If you're resuming work or just arriving:**
1. **Current state** → [CONTEXT_RECOVERY.md](#context-recovery) ← What's working, what's in progress
2. **For AI assistants** → [AI_HANDOFF_GUIDE.md](#ai-handoff-guide) ← Your role and conventions
3. **Strategic direction** → [ERA_ECOSYSTEM_PLAN.md](#era-ecosystem-plan) ← Long-term integration plan
4. **How we work** → [WORKING_PRINCIPLES.md](#working-principles) ← Philosophy, Git workflow, testing
5. **Then come back** to this README for system overview

---

## 🎯 What Is This?

ERA Admin is the **integration hub** for connecting four separate ERA data systems:

1. **Google Docs Agendas** - Meeting notes with participant lists (ground truth)
2. **Airtable** - Membership database (630 people, member/donor tracking)
3. **Fathom Inventory** - Automated meeting analysis (1,953 participants, AI-extracted)
4. **ERA Landscape** - Network visualization (350+ organizations/people/projects)

**Goal:** Connect these systems to create a unified view of the ERA community.

---

## 📂 Components (Self-Contained)

Each component has its own README with details:

- [**airtable/**](#airtable-readme) - Manual membership tracking and exports
- [**FathomInventory/**](#fathom-readme) - Automated meeting analysis
- [**integration_scripts/**](#integration-readme) - Cross-component bridging scripts

---

## 📚 Documentation Navigation

**Where to go next:**
- Current state → [CONTEXT_RECOVERY.md](#context-recovery)
- For AI → [AI_HANDOFF_GUIDE.md](#ai-handoff-guide)
- Principles → [WORKING_PRINCIPLES.md](#working-principles)
- Components → [See above](#-components-self-contained)

[Back to top](#era-admin-navigation-prototype)

---
---

<a name="level-1-orientation"></a>
# Level 1: Orientation Documents

Documents that orient you to current state, strategic direction, and how to work here.

---

<a name="context-recovery"></a>
## CONTEXT_RECOVERY.md

**Purpose:** Quickly understand current state and resume integration work  
**Audience:** Humans resuming work + AI assistants getting oriented  
**Last Updated:** October 20, 2025

---

### 📍 Navigation

**Path:** [README.md](#level-0-readme) → **CONTEXT_RECOVERY**

**Related:**
- For AI workflow → [AI_HANDOFF_GUIDE.md](#ai-handoff-guide)
- For principles → [WORKING_PRINCIPLES.md](#working-principles)

**Component-specific context:**
- [FathomInventory context](#fathom-context)
- [integration_scripts context](#integration-context)

---

### 🎯 Current System State

**What's Working:**
- ✅ **Airtable exports operational** - 630 people (+58 from Phase 4B-2)
- ✅ **Landscape deployed** - https://jonschull.github.io/ERA_Landscape_Static/
- ✅ **Fathom automation running** - Daily at 3 AM, 1,953 participants tracked
- ✅ **Phase 4B-2 87% complete** - 409 participants validated (Oct 20)

### Recent Completions

**Oct 18:** Configuration Centralization complete  
**Oct 19:** Phase 4B-1 Automated Fuzzy Matching - 364 enriched  
**Oct 20:** Monorepo consolidation - FathomInventory absorbed, GitHub backup established

### What's In Progress

**Phase 4B-2 Final Batch:**
- 87% complete (1,698/1,953 validated)
- 255 remaining participants
- Next: Final review round

---

### Next Steps

**For further details:**
- Component status → [FathomInventory](#fathom-context), [airtable](#airtable-context)
- Strategic plan → [ERA_ECOSYSTEM_PLAN.md](#era-ecosystem-plan)
- How we work → [WORKING_PRINCIPLES.md](#working-principles)

**Back to:** [README.md](#level-0-readme)

---

<a name="ai-handoff-guide"></a>
## AI_HANDOFF_GUIDE.md

**Purpose:** Guide for AI assistants working on ERA data integration  
**Audience:** AI assistants  
**Last Updated:** October 18, 2025

---

### 📍 Navigation

**Path:** [README.md](#level-0-readme) → **AI_HANDOFF_GUIDE**

**Related:**
- Current state → [CONTEXT_RECOVERY.md](#context-recovery)
- Principles → [WORKING_PRINCIPLES.md](#working-principles) ← Git workflow, testing approach

**Specialized workflows:**
- Phase 4B-2 workflow → [integration_scripts/AI_WORKFLOW_GUIDE](#ai-workflow-specific)

---

### 🧭 Your Role: Advisor and Crew

**The Human Is:**
- **Captain** - Sets direction, makes final decisions
- **Navigator** - Chooses which problems to solve and when
- **Authority** - Approves or rejects all actions

**You (AI) Are:**
- **Advisor** - Research options, explain trade-offs, recommend approaches
- **Crew** - Execute approved tasks, run tests, implement solutions
- **Scout** - Explore codebases, find patterns, surface relevant information

### What This Means in Practice

**DO:**
- ✅ Read README first to understand the system
- ✅ Research thoroughly before proposing solutions
- ✅ Ask "Should I proceed?" before implementing
- ✅ Test your work before claiming success
- ✅ Reference relevant docs: "See [WORKING_PRINCIPLES](#working-principles) for Git workflow"

**DON'T:**
- ❌ Assume approval from discussion
- ❌ Declare victory without validation
- ❌ Ignore existing patterns

**For detailed principles:** See [WORKING_PRINCIPLES.md](#working-principles)

---

### ⚠️ CRITICAL: Core Principles

**Vigilance against self-delusion and premature declarations of victory.**

1. **Discussion ≠ Directive**
   - User comments during exploration are **not** implementation requests
   - Ask: "Should I implement this approach?" before proceeding

2. **Proactive Validation Before Declaring Success**
   - Think: "What test will the user apply?"
   - Run that test FIRST
   - Show results, THEN ask user to verify

**See [WORKING_PRINCIPLES.md](#working-principles) for full philosophy**

---

### Specialized Workflows

**This guide covers general AI workflow patterns.**

**For specific tasks:**

#### Phase 4B-2 Collaborative Data Review
Complex multi-phase human-AI workflow for data curation.

→ **See:** [integration_scripts/AI_WORKFLOW_GUIDE.md](#ai-workflow-specific)

[Provides: 6-phase cycle, mental states, decision trees specific to Phase 4B-2]

---

### Next Steps

**Understand principles:** [WORKING_PRINCIPLES.md](#working-principles)  
**Check current state:** [CONTEXT_RECOVERY.md](#context-recovery)  
**Work on component:** [FathomInventory](#fathom-readme) | [airtable](#airtable-readme) | [integration_scripts](#integration-readme)

**Back to:** [README.md](#level-0-readme)

---

<a name="era-ecosystem-plan"></a>
## ERA_ECOSYSTEM_PLAN.md

**Purpose:** Strategic vision for multi-system integration  
**Audience:** Anyone understanding long-term direction  

---

### 📍 Navigation

**Path:** [README.md](#level-0-readme) → **ERA_ECOSYSTEM_PLAN**

**Quick Navigation:**
- New to project → [README.md](#level-0-readme)
- Lost context → [CONTEXT_RECOVERY.md](#context-recovery)
- Working on integration → You're in the right place

---

### Strategic Vision

[System integration phases 4-7 details would go here - not duplicating for prototype]

**Key insight:** This doc provides VISION, not current state (that's CONTEXT_RECOVERY)

**Back to:** [README.md](#level-0-readme)

---
---

<a name="level-2-principles"></a>
# Level 2: Principles & Practices

How we work, what we value, workflows we follow.

---

<a name="working-principles"></a>
## WORKING_PRINCIPLES.md

**Purpose:** Philosophy, architecture principles, Git/PR workflow, testing approach  
**Audience:** Humans and AIs working on the system  
**Last Updated:** October 18, 2025

---

### 📍 Navigation

**Path:** [README.md](#level-0-readme) → **WORKING_PRINCIPLES**

**Referenced by:**
- [AI_HANDOFF_GUIDE.md](#ai-handoff-guide) - For AI collaboration model
- [Component READMEs](#level-3-components) - When following/deviating from principles

**Related:**
- Current state → [CONTEXT_RECOVERY.md](#context-recovery)
- System overview → [README.md](#level-0-readme)

---

### 🧭 Core Philosophy

#### Human-AI Collaboration

**The Captain-Advisor Model:**

- **Human is Captain** - Sets direction, makes decisions, approves actions
- **AI is Critical Collaborator** - Questions assumptions, proposes alternatives, executes approved tasks
- **Not compliance, but collaboration** - AI should challenge, not just obey

**In Practice:**
- ✅ AI asks: "Should I proceed?" before implementing
- ✅ AI says: "Here's a risk you may have overlooked..."
- ❌ AI assumes approval from discussion
- ❌ AI declares success without validation

#### Vigilance Against Self-Delusion

**Proactive Validation Before Declaring Success:**

1. Think: "What test will the user apply?"
2. Run that test yourself FIRST
3. Show results, THEN ask user to verify
4. Never declare "done" without user confirmation

---

### 📦 Component Architecture

**Principles:**
- **Component Independence** - Each can function standalone
- **Clear Boundaries** - Well-defined interfaces
- **Centralized Config** - `era_config.py` manages paths
- **Respect Autonomy** - Don't break component internals

**See components:**
- [FathomInventory/](#fathom-readme) - Meeting analysis
- [airtable/](#airtable-readme) - Membership tracking
- [integration_scripts/](#integration-readme) - Cross-component bridges

---

### 🔀 Git & Version Control

#### Protected Main Branch

**Never commit directly to `main`**

All changes via Pull Requests to enable review and discussion.

#### PR Workflow

1. **Create feature branch:** `git checkout -b fix-description`
2. **Make changes, test locally**
3. **Commit with clear message**
4. **Push and create PR:** `gh pr create`
5. **After merge, update local:** `git pull origin main`

#### Commit Message Guidelines

**Format:**
```
Short summary (50 chars or less)

More detailed explanation if needed:
- What changed
- Why changed
- Impact on system

References: Issue #123, Doc XYZ
```

**Good examples:**
- "Fix test_recent_logs.py path after migration"
- "Documentation: Navigation design and audits"

**Bad examples:**
- "updates" (what updates?)
- "fix bug" (which bug?)

---

### 🧪 Testing Discipline

**Before declaring "done":**

1. ✅ Run relevant tests
2. ✅ Test the happy path
3. ✅ Test error conditions
4. ✅ Verify no regressions
5. ✅ Show user the test results

**Philosophy:** Trust but verify. Proactive validation prevents self-delusion.

---

### 📝 Documentation Practices

**Hierarchy matters:**
- Each doc has clear scope
- Links up (context) and down (details)
- No redundant explanations
- See [NAVIGATION_DESIGN.md](#navigation-design) for architecture

**Examples:**
- This doc: Principles (how we work)
- [AI_HANDOFF_GUIDE](#ai-handoff-guide): AI role (references this doc for principles)
- [Component READMEs](#level-3-components): Component details (apply these principles)

---

### Next Steps

**Apply to specific work:**
- [FathomInventory/](#fathom-readme) - See how principles apply
- [integration_scripts/](#integration-readme) - Bridging work
- [AI_HANDOFF_GUIDE](#ai-handoff-guide) - AI-specific workflow

**Back to:** [README.md](#level-0-readme)

---
---

<a name="level-3-components"></a>
# Level 3: Component READMEs

Each component is self-contained with its own README.

---

<a name="fathom-readme"></a>
## FathomInventory/README.md

**Part of:** [ERA_Admin](#level-0-readme) - Data integration hub  
**This component:** Automated meeting analysis system

---

### 📍 Navigation

**Path:** [README.md](#level-0-readme) → **FathomInventory**

**Working principles:** See [WORKING_PRINCIPLES.md](#working-principles) for:
- Component boundaries
- Testing approach
- Git workflow

**Within this component:**
- [authentication/](#fathom-auth) - Cookie/token management
- [analysis/] - Participant analysis
- [docs/] - Technical documentation

**Back to:** [Main README](#level-0-readme)

---

### 🎯 What This Does

**Automatically downloads, processes, and analyzes Fathom meeting summaries**

1. **Discovers** new Fathom calls from jschull@e-nable.org account
2. **Shares** calls to automated receiver
3. **Downloads** summary emails with public URLs
4. **Processes** emails into structured database
5. **Reports** daily status with health checks

### Current Health

- ✅ **1,953 participants** tracked
- ✅ **Automation active** - Daily runs at 3:00 AM
- ✅ **Enhanced failure detection**

---

### Quick Start

```bash
# From FathomInventory directory
source ../ERA_Admin_venv/bin/activate
./run_all.sh  # Runs full pipeline
```

**For details:** See [DEVELOPMENT.md](FathomInventory/DEVELOPMENT.md)

---

### Component-Specific Context

<a name="fathom-context"></a>
#### Context Recovery

**See:** [Main CONTEXT_RECOVERY.md](#context-recovery) for system-wide status

**FathomInventory-specific:**
- Recent: Monorepo consolidation (Oct 20) - absorbed into ERA_Admin
- Status: Fully operational, automation running
- Next: Continue Phase 4B-2 validation

---

### Related Documentation

**Specialized:**
- [authentication/README](#fathom-auth) - Cookie/token setup
- [docs/TECHNICAL_DOCUMENTATION.md] - Full technical specs

**Broader context:**
- [WORKING_PRINCIPLES](#working-principles) - How we work
- [ERA_ECOSYSTEM_PLAN](#era-ecosystem-plan) - Strategic vision

**Back to:** [Main README](#level-0-readme)

---

<a name="airtable-readme"></a>
## airtable/README.md

**Part of:** [ERA_Admin](#level-0-readme) - Data integration hub  
**This component:** Manual membership tracking and exports

---

### 📍 Navigation

**Path:** [README.md](#level-0-readme) → **airtable**

**Working principles:** See [WORKING_PRINCIPLES.md](#working-principles) for testing approach

**Back to:** [Main README](#level-0-readme)

---

### 🎯 What This Does

Manual membership database with exports for cross-correlation.

**Current:** 630 people tracked, 17 Town Hall attendance columns

### Quick Start

```bash
cd airtable
python3 export_people.py
```

---

<a name="airtable-context"></a>
#### Context

**See:** [Main CONTEXT_RECOVERY.md](#context-recovery) for system status

**airtable-specific:**
- Recent: +58 people added from Phase 4B-2
- Status: Exports operational

**Back to:** [Main README](#level-0-readme)

---

<a name="integration-readme"></a>
## integration_scripts/README.md

**Part of:** [ERA_Admin](#level-0-readme) - Data integration hub  
**This component:** Cross-component bridging scripts

---

### 📍 Navigation

**Path:** [README.md](#level-0-readme) → **integration_scripts**

**Multiple READMEs in this directory:**
- **This file (README.md):** Overview of integration scripts
- **README_PHASE4B.md:** Phase 4B system details
- **README_PHASE4B_DETAILED.md:** Deep technical details

**For AI workflow:**
- [AI_WORKFLOW_GUIDE.md](#ai-workflow-specific) - Phase 4B-2 collaborative process

**Back to:** [Main README](#level-0-readme)

---

### 🎯 What This Does

Bridges FathomInventory ↔ Airtable for participant enrichment.

**Phases:**
- **Phase 4B-1:** Automated fuzzy matching (✅ 364 enriched)
- **Phase 4B-2:** Collaborative human-AI review (✅ 87% complete, 409 enriched)

---

<a name="integration-context"></a>
#### Context

**See:** [Main CONTEXT_RECOVERY.md](#context-recovery) for overall status

**integration_scripts-specific:**
- Current: Phase 4B-2 Round 8 complete
- Progress: 87% validated (1,698/1,953)
- Next: Final batch review

---

### Related Documentation

**Specialized:**
- [AI_WORKFLOW_GUIDE.md](#ai-workflow-specific) - 6-phase collaborative workflow
- [PHASE4B2_PROGRESS_REPORT.md] - 8-round detailed analysis

**Broader context:**
- [WORKING_PRINCIPLES](#working-principles) - Testing, Git workflow
- [ERA_ECOSYSTEM_PLAN](#era-ecosystem-plan) - Where this fits

**Back to:** [Main README](#level-0-readme)

---
---

<a name="level-4-specialized"></a>
# Level 4: Specialized Documents

Deep dives on specific functionality.

---

<a name="fathom-auth"></a>
## FathomInventory/authentication/README.md

**Component:** [FathomInventory/README.md](#fathom-readme)  
**Applies principles from:** [WORKING_PRINCIPLES.md](#working-principles) - Testing approach

---

### 📍 Path

[README](#level-0-readme) → [FathomInventory](#fathom-readme) → authentication → **This Guide**

**Scope:** Cookie and token management for Fathom authentication

**For broader FathomInventory context:** See [FathomInventory/README](#fathom-readme)

---

### 🔐 Authentication Setup

[Technical details about cookies and tokens...]

**Key files:**
- `credentials.json` - Google API credentials
- `token.json` - OAuth access token
- `fathom_cookies_*.json` - Browser session cookies

**All gitignored for security** - See [WORKING_PRINCIPLES](#working-principles) for Git workflow

---

### Related

**Broader context:** [FathomInventory/README](#fathom-readme)  
**Related:** [docs/AUTHENTICATION_GUIDE.md]  
**Principles:** [WORKING_PRINCIPLES.md](#working-principles) - Security practices

**Back to:** [FathomInventory](#fathom-readme) | [Main README](#level-0-readme)

---

<a name="ai-workflow-specific"></a>
## integration_scripts/AI_WORKFLOW_GUIDE.md

**Part of:** [AI_HANDOFF_GUIDE.md](#ai-handoff-guide) - General AI workflow  
**Component:** [integration_scripts/README.md](#integration-readme)

---

### 📍 Path

[README](#level-0-readme) → [AI_HANDOFF_GUIDE](#ai-handoff-guide) → [integration_scripts](#integration-readme) → **This Workflow**

**Scope:** Specialized workflow for Phase 4B-2 collaborative data review

**For general AI patterns:** See [AI_HANDOFF_GUIDE.md](#ai-handoff-guide)

---

### 🔄 Phase 4B-2 Specific Workflow

**This is a specialized 6-phase workflow for human-AI data curation.**

**General AI principles:** See [AI_HANDOFF_GUIDE](#ai-handoff-guide)  
**Working principles:** See [WORKING_PRINCIPLES](#working-principles)

[6-phase cycle, mental states, decision trees specific to Phase 4B-2...]

---

### Related

**General AI workflow:** [AI_HANDOFF_GUIDE.md](#ai-handoff-guide)  
**Component context:** [integration_scripts/README](#integration-readme)  
**Principles applied:** [WORKING_PRINCIPLES.md](#working-principles)  
**Progress:** [PHASE4B2_PROGRESS_REPORT.md]

**Back to:** [integration_scripts](#integration-readme) | [Main README](#level-0-readme)

---

<a name="navigation-design"></a>
## NAVIGATION_DESIGN.md

**Purpose:** Architecture document for this very navigation system  
**Audience:** Anyone implementing or maintaining documentation

---

### 📍 Path

[README](#level-0-readme) → **NAVIGATION_DESIGN** (meta-document)

**Scope:** Defines hierarchy, redundancy rules, navigation patterns

---

### Key Principles

1. **Hierarchy = Abstraction levels** (0-4)
2. **Each level answers different questions**
3. **Link, don't duplicate**
4. **Bidirectional navigation**

[Full design details in actual NAVIGATION_DESIGN.md file]

**Back to:** [README](#level-0-readme)

---
---

## 🔍 Validation Questions

**After clicking through scenarios, ask:**

1. **Coverage:** Can you find everything you need from any starting point?
2. **No dead ends:** Can you always get back to README?
3. **No redundancy:** Is content repeated, or just referenced?
4. **Clear scope:** Does each doc have bounded responsibility?
5. **Complementary:** Do levels add context without duplicating?
6. **Findable:** Can you discover specialized docs when needed?

---

## 📝 Notes for Implementation

**What works in this prototype:**
- [ ] Navigation clarity
- [ ] Scope boundaries
- [ ] Non-redundant content
- [ ] Bidirectional links
- [ ] Easy to get back to main

**What needs fixing:**
- [ ] [Document issues found]

**Ready for real implementation when:**
- [ ] All scenarios work
- [ ] No redundancy detected
- [ ] Clear which doc to read when
- [ ] User validates design

---

**This is a PROTOTYPE. Do not implement across real files until validated.**

[Back to top](#era-admin-navigation-prototype)
