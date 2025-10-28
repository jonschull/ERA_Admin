# Documentation Navigation Design
**Date:** October 20, 2025  
**Status:** Design document - Implementation pending  
**Purpose:** Architecture for bidirectional, non-redundant navigation

---

## Design Principles

### 1. Hierarchy = Abstraction Levels

```
Level 0: README.md
         ↓ (purpose, audience, quick links)
Level 1: Orientation docs (CONTEXT_RECOVERY, AI_HANDOFF_GUIDE, ERA_ECOSYSTEM_PLAN)
         ↓ (current state, role, strategy)
Level 2: Principles & Practices (WORKING_PRINCIPLES, GIT_WORKFLOW)
         ↓ (how we work, what we value)
Level 3: Component READMEs (airtable/, FathomInventory/, integration_scripts/)
         ↓ (what component does, how to use it)
Level 4: Specialized docs (authentication/, analysis/, specific workflows)
         ↓ (detailed how-to, technical specs)
```

**Rule:** Each level can reference UP (to context) and DOWN (to specifics), but **adds information**, never repeats.

### 2. Complementary Content Strategy

**Each level answers different questions:**

| Level | Question Answered | Example |
|-------|-------------------|---------|
| 0 | What is this entire system? | "ERA Admin integrates 4 data systems" |
| 1 | Where are we now / How do I work here? | "Phase 4B-2 is 87% complete" |
| 2 | What principles guide our work? | "All changes via PRs, not direct to main" |
| 3 | How do I use this component? | "FathomInventory tracks meeting participants" |
| 4 | How do I solve this specific problem? | "To export cookies from browser..." |

**Anti-pattern:** Level 4 doc repeating "ERA Admin is..." (that's Level 0's job)

### 3. Bidirectional Navigation Pattern

**Every document includes:**

```markdown
# Title

**Purpose:** [One line]
**Audience:** [Who reads this]
**Context:** [Link up to parent/broader context]

---

## 📍 You Are Here

**Path:** [README](README.md) → [Parent Doc] → **This Doc**

**Related at this level:**
- [Sibling doc 1] - [Why you'd read it instead]
- [Sibling doc 2] - [Why you'd read it instead]

**Dig deeper:**
- [Child doc 1] - [What it details]
- [Child doc 2] - [What it details]

**Broader context:**
- [Up to parent] - [What it provides]

---

[Content - focused on THIS level's questions]

---

## Next Steps

**If you need to:** [action] → **See:** [doc link]

**Back to:** [Parent doc]
```

### 4. Redundancy Rules

**What CAN repeat (stability):**
- Doc title in breadcrumb
- Purpose statement
- Key file paths that define scope

**What MUST NOT repeat (divergence risk):**
- Detailed explanations
- Current status/metrics
- Implementation details
- Historical context

**Strategy:** Link, don't duplicate. Summarize, don't explain.

---

## Document Scope Definitions

### Level 0: README.md (The Front Door)

**Scope:**
- System purpose (1 paragraph)
- Components overview (bullet list)
- Entry point routing (by role/need)
- Quick start (minimal)

**NOT included:**
- How we work (→ WORKING_PRINCIPLES)
- Current status (→ CONTEXT_RECOVERY)
- Historical context (→ individual docs)
- Detailed component info (→ component READMEs)

**Links TO:** Level 1 docs (orientation)  
**Links FROM:** All component READMEs ("Back to main")

---

### Level 1: Orientation Documents

#### CONTEXT_RECOVERY.md (Current State)

**Scope:**
- What's working now
- Recent completions (last 2 weeks)
- What's in progress
- Immediate next steps
- Quick health checks

**NOT included:**
- How to work with AI (→ AI_HANDOFF_GUIDE)
- Why we made decisions (→ specific docs)
- Historical completions (→ historical/)
- Detailed metrics (→ component CONTEXT_RECOVERY files)

**Links TO:** Component docs, status docs  
**Links FROM:** README, all component CONTEXT_RECOVERY files

---

#### AI_HANDOFF_GUIDE.md (AI Role & Workflow)

**Scope:**
- Human-AI relationship model
- General workflow patterns
- Documentation hierarchy overview
- When to ask vs proceed
- Common workflows (examples)

**NOT included:**
- Specific component workflows (→ component AI docs)
- Git mechanics (→ WORKING_PRINCIPLES)
- Phase-specific workflows (→ integration_scripts/AI_WORKFLOW_GUIDE)
- Testing procedures (→ component docs)

**Bridge statement needed:**
```markdown
## Specialized Workflows

For **Phase 4B-2 collaborative review:**
→ See [integration_scripts/AI_WORKFLOW_GUIDE.md](../integration_scripts/participant_reconciliation/archive/superseded_docs/AI_WORKFLOW_GUIDE.md)

This guide provides the general framework; that guide provides specific 6-phase workflow for human-AI data curation.
```

**Links TO:** WORKING_PRINCIPLES, component READMEs, specialized guides  
**Links FROM:** README, specialized AI guides

---

#### ERA_ECOSYSTEM_PLAN.md (Strategic Vision)

**Scope:**
- Multi-system integration vision
- Phase definitions
- Success metrics per phase
- Dependencies & sequencing
- Long-term roadmap

**NOT included:**
- Current progress (→ CONTEXT_RECOVERY)
- Implementation details (→ component docs)
- How to work (→ WORKING_PRINCIPLES)
- Historical decisions (→ completed plan docs)

**Links TO:** Component READMEs, phase docs  
**Links FROM:** README, component READMEs (for context)

---

### Level 2: Principles & Practices

#### WORKING_PRINCIPLES.md (How We Work)

**Scope:**
- Philosophy (human-AI model)
- Component architecture principles
- Documentation practices
- Testing discipline
- Decision-making framework
- Git/PR workflow

**NOT included:**
- Specific git commands (provide examples, not tutorials)
- Component-specific practices (→ component docs)
- Current status (→ CONTEXT_RECOVERY)
- Project vision (→ ERA_ECOSYSTEM_PLAN)

**Referenced BY:** AI_HANDOFF_GUIDE, component docs (when they follow/deviate)  
**References TO:** README (for context), component examples

---

### Level 3: Component READMEs

**Pattern for all component READMEs:**

**Scope:**
- What this component does (purpose)
- How it fits in system (→ README for overview)
- Quick start (minimal commands)
- File structure
- Links to specialized docs within component

**NOT included:**
- System-wide context (→ README)
- Principles (→ WORKING_PRINCIPLES, but can say "following X principle...")
- Other components' details
- Historical evolution (→ component/historical/)

**Navigation template:**
```markdown
# Component Name

**Part of:** [ERA_Admin](../README.md) - [System purpose one-liner]

**This component:** [One paragraph purpose]

---

## 📍 Navigation

**From main system:** [README](../README.md) → **This Component**

**Working principles:** See [WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) for:
- Component boundaries
- Testing approach
- Documentation standards

**Within this component:**
- [Subdir/] - [What it contains]
- [Specialized.md] - [What it covers]

**Back to:** [Main README](../README.md)
```

---

### Level 4: Specialized Documents

**Examples:**
- FathomInventory/authentication/README.md
- integration_scripts/AI_WORKFLOW_GUIDE.md
- FathomInventory/docs/TECHNICAL_DOCUMENTATION.md

**Scope:**
- Deep dive on specific functionality
- Step-by-step procedures
- Technical specifications
- Troubleshooting

**Navigation requirements:**
- **Breadcrumb** showing path from main README
- **References UP** to component README and relevant principles
- **Clear scope** statement (what this covers, what it doesn't)

**Template:**
```markdown
# Specialized Topic

**Component:** [Component README](../README.md)  
**Applies principles from:** [WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) - [Which sections]

---

## 📍 Path

[README](../README.md) → [Component](../README.md) → [Subarea] → **This Guide**

**Scope:** This covers [specific topic]. For [related topic] see [other doc].

---

[Detailed content]

---

## Related

**Broader context:** [Component README](../README.md)  
**Related tasks:** [Other specialized doc]  
**Principles applied:** [WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)
```

---

## Special Cases

### Multiple CONTEXT_RECOVERY Files

**Problem:** 3 files with same name, risk of redundancy

**Design:**

**Main (root):**
- System-wide status
- Cross-component work
- Recent major changes

**Component (FathomInventory/):**
```markdown
# FathomInventory - Context Recovery

**See also:** [Main CONTEXT_RECOVERY.md](../CONTEXT_RECOVERY.md) - System-wide status

**This document:** FathomInventory-specific context

---

## 📍 Scope

This adds FathomInventory-specific details to the main CONTEXT_RECOVERY.

For system-wide status → see [main doc](../CONTEXT_RECOVERY.md)

[FathomInventory-specific content only]
```

**Sub-component (analysis/):**
```markdown
# Analysis Module - Context Recovery

**See:**
- [Main CONTEXT_RECOVERY.md](../CONTEXT_RECOVERY.md) - System status
- [FathomInventory CONTEXT_RECOVERY.md](../CONTEXT_RECOVERY.md) - Component status

**This document:** Analysis module specific context

[Module-specific content only]
```

### Multiple AI Guides

**AI_HANDOFF_GUIDE.md (general):**
```markdown
## Specialized Workflows

This guide covers general AI workflow patterns.

**For specific tasks:**

### Phase 4B-2 Collaborative Data Review
Complex multi-phase human-AI workflow for data curation.
→ **See:** [integration_scripts/AI_WORKFLOW_GUIDE.md](../integration_scripts/participant_reconciliation/archive/superseded_docs/AI_WORKFLOW_GUIDE.md)

[Provides: 6-phase cycle, mental states, decision trees]
```

**integration_scripts/AI_WORKFLOW_GUIDE.md (specific):**
```markdown
# AI Workflow Guide - Phase 4B-2

**Part of:** [AI_HANDOFF_GUIDE.md](../AI_HANDOFF_GUIDE.md) - General AI workflow

**This guide:** Specific workflow for Phase 4B-2 collaborative data review

---

## 📍 Context

This is a specialized workflow. For general AI patterns, see [AI_HANDOFF_GUIDE.md](../AI_HANDOFF_GUIDE.md).

**Path:** [README](../README.md) → [AI_HANDOFF_GUIDE](../AI_HANDOFF_GUIDE.md) → [integration_scripts](README.md) → **This Workflow**

[Specific Phase 4B-2 content]
```

---

## Implementation Checklist

**Phase 1: Core Structure (Next session)**
- [ ] Add navigation section to README.md
- [ ] Add navigation section to CONTEXT_RECOVERY.md
- [ ] Add navigation section to AI_HANDOFF_GUIDE.md
- [ ] Add bridge between AI_HANDOFF_GUIDE ↔ AI_WORKFLOW_GUIDE
- [ ] Add navigation section to WORKING_PRINCIPLES.md
- [ ] Link WORKING_PRINCIPLES from README and AI_HANDOFF_GUIDE

**Phase 2: Component Integration**
- [ ] Add navigation template to FathomInventory/README.md
- [ ] Add navigation template to airtable/README.md
- [ ] Add navigation template to integration_scripts/README.md
- [ ] Sync 3 CONTEXT_RECOVERY files with scope statements
- [ ] Add breadcrumbs to specialized docs

**Phase 3: Verification**
- [ ] Walk through each navigation path
- [ ] Check for circular references
- [ ] Verify no redundant explanations
- [ ] Test "lost user" scenarios
- [ ] Update NAVIGATION_DESIGN with lessons learned

---

## Testing Navigation

**Scenarios to verify:**

1. **New AI arrives**
   - README → AI_HANDOFF_GUIDE → WORKING_PRINCIPLES → ready
   - Can they find specialized guides when needed?

2. **Working on FathomInventory auth**
   - FathomInventory/authentication/README → can they find principles? parent context?

3. **Lost in integration_scripts**
   - Can they get back to main README?
   - Can they find relevant AI guide?

4. **Understanding current state**
   - CONTEXT_RECOVERY → can they find component-specific details?
   - Can they avoid redundant explanations?

5. **Following Git workflow**
   - Can they find it from README? From AI guide?
   - Is it linked when needed, not repeated?

---

## Maintenance Rules

1. **When adding new doc:**
   - Determine its level (0-4)
   - Add navigation section following template
   - Link from parent
   - Link to children

2. **When updating content:**
   - Check links still accurate
   - Verify no duplication with parent/child
   - Update "Last updated" date

3. **When archiving doc:**
   - Remove from navigation paths
   - Add pointer in parent to historical location
   - Update CONTEXT_RECOVERY if relevant

---

## Success Criteria

**Good navigation means:**
- ✅ User can always find their way back to README
- ✅ User knows where they are in hierarchy
- ✅ User can find related docs at same level
- ✅ User can drill down for details
- ✅ User can look up for context
- ✅ No content is duplicated across levels
- ✅ Each doc has clear, bounded scope
- ✅ Specialized docs reference principles without repeating them

**Poor navigation looks like:**
- ❌ Dead ends (no way back)
- ❌ Orphans (not linked from anywhere)
- ❌ Circular references (A→B→C→A)
- ❌ Redundant explanations (same content at multiple levels)
- ❌ Unclear scope (don't know if this doc covers X)
- ❌ Missing bridges (related docs don't reference each other)

---

**This design should be implemented carefully, testing each path as we go. Not tonight.**
