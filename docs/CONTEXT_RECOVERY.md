# docs - Context Recovery

**Last Updated:** October 20, 2025 8:17 PM  
**Purpose:** Track documentation work progress

---

## 1. Overview

**Purpose:** Context recovery for documentation work

**This document tracks:**
- Current phase of documentation work
- Which sections completed
- Which sections remain
- Design decisions made
- Patterns established

**Read this:** Before starting each component to stay oriented

---

## 2. Orientation - Where to Find What

**You are at:** Documentation work context

**What you might need:**
- Department README → [README.md](README.md)
- Main system → [/README.md](../README.md)
- Wireframe being enriched → [NAVIGATION_WIREFRAME.md](NAVIGATION_WIREFRAME.md)
- System principles → [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)

---

## 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)

**Documentation:** See [README.md](README.md) for doc-specific principles

**Applied here:**
- Update this file after each component enriched
- Record design decisions and patterns
- Track what's working / what needs revision

---

## 4. Specialized Topics

### Current Phase

**Phase:** Enriching NAVIGATION_WIREFRAME.md with original content

**Goal:** Systematic integration of good explanatory content from original docs into 4-section structure

**Status:** Component READMEs in progress (1/3, 33%)

---

### Completed Work (Oct 20, 2025)

**Setup:**
- ✅ Created docs/ as proper component with 4-section structure
- ✅ Moved wireframes into docs/
- ✅ Removed telegraphic docs_prototype/
- ✅ Established context recovery checkpoint pattern

**Design Decisions:**
- Navigation tree integrity principles documented (no orphans, navigate up, mandatory TOC)
- Section 2 pattern: "You are at" + "What you might need" (no false breadcrumbs)
- Section 1 = pure overview (no status), status only in CONTEXT_RECOVERY docs
- Assume no foreknowledge (write for newcomers)

---

### Work Plan

**Enrichment Order:**

1. **Root Docs** (4 files) - ✅ COMPLETE
   - [x] README.md - ✅ COMPLETE
   - [x] CONTEXT_RECOVERY.md - ✅ COMPLETE
   - [x] AI_HANDOFF_GUIDE.md - ✅ COMPLETE
   - [x] WORKING_PRINCIPLES.md - ✅ COMPLETE
   
   **Before starting:** Read this CONTEXT_RECOVERY
   **Sources:** Original files in parent directory
   **Goal:** Comprehensive 4-section docs with good explanations

2. **Component READMEs** (3 files) - IN PROGRESS
   - [x] FathomInventory/README.md - ✅ COMPLETE
   - [ ] airtable/README.md - NEXT
   - [ ] integration_scripts/README.md
   
   **Before starting each:** Read this CONTEXT_RECOVERY
   **Sources:** Original component READMEs
   **Goal:** Component overview + principles (reference root + add specifics)

3. **Specialized Docs** (as needed)
   - [ ] FathomInventory/authentication/README.md
   - [ ] integration_scripts/AI_WORKFLOW_GUIDE.md
   - [ ] Others as discovered
   
   **Before starting:** Read this CONTEXT_RECOVERY
   **Sources:** Original specialized docs
   **Goal:** Deep-dive guides maintaining 4-section structure

---

### Checkpoint Protocol

**When to read this CONTEXT_RECOVERY:**
1. ✅ At start of each component
2. After any long tool operation
3. Before proposing next steps

**When to update this CONTEXT_RECOVERY:**
1. After completing each component
2. When making design decisions
3. When discovering patterns

---

### Design Patterns to Maintain

**From wireframe work:**

1. **Section 1: Overview**
   - Pure description (what is this, what it does)
   - NO status information
   - Assume no foreknowledge

2. **Section 2: Orientation - Where to Find What**
   - "You are at: [location]"
   - "What you might need:" with links
   - Parent README link always present
   - No false breadcrumbs

3. **Section 3: Principles**
   - "System-wide: See /WORKING_PRINCIPLES.md"
   - Component-specific additions only
   - Reference, don't duplicate

4. **Section 4: Specialized Topics**
   - Mandatory TOC of all files in folder
   - Brief descriptions
   - "Back to: [parent]" at end

---

### Completed This Session

**README.md enrichment** ✅ (Oct 20, 8:20 PM)
- Section 1: Full system explanations, connection diagram, integration status
- Section 2: Windsurf context, detailed navigation paths
- Section 3: Principle explanations (not just bullets)
- Section 4: Component details, quick start, system requirements, gotchas
- Pattern: Assume no foreknowledge, explain concepts
- Commit: 38ed6e0

**CONTEXT_RECOVERY.md enrichment** ✅ (Oct 20, 8:35 PM)
- Section 1: Clear purpose, audience (humans vs AI), what's contained
- Section 2: When to use, related docs with descriptions
- Section 3: Applied principles (validation, maintenance, context, time)
- Section 4: Comprehensive content (state, inventory, status, resume commands, tasks, locations, issues, metrics, AI recovery)
- Pattern: Rich explanatory content, copy-paste commands, historical context
- Commit: 0a785d6

**AI_HANDOFF_GUIDE.md enrichment** ✅ (Oct 20, 8:50 PM)
- Section 1: Captain-advisor model, role explanation, critical philosophy
- Section 2: First session checklist, 3-level doc hierarchy, navigation rule
- Section 3: 5 critical principles, DO/DON'T lists, red flags/green lights
- Section 4: 3 workflows, code conventions, constraints, validation checklist, best practices, quick reference
- Pattern: Practical guidance with code examples, when to ask vs proceed
- Commit: 9244714

**WORKING_PRINCIPLES.md enrichment** ✅ (Oct 20, 9:05 PM)
- Section 1: Purpose, audience, 8 categories of principles
- Section 2: Referenced by, component usage pattern
- Section 3: Self-referential (this IS the principles), organization preview
- Section 4: 8 comprehensive categories (philosophy, architecture, documentation, git, testing, quality, decision-making, communication) + checklists + meta
- Pattern: Complete principles with practical guidance, living document
- Commit: 8ae4ebc

**ROOT DOCS ENRICHMENT COMPLETE** ✅ (4/4, 100%)

**FathomInventory/README.md enrichment** ✅ (Oct 20, 9:15 PM)
- Section 1: Full system description, health metrics, recent improvements
- Section 2: User paths (first-time, resuming, making changes), related docs
- Section 3: System-wide reference + 4 component-specific principles
- Section 4: Quick start, advanced config, daily operation, troubleshooting, files, help, organization
- Pattern: Practical guidance with copy-paste commands
- Commit: aa579a6

### Next Action

**Current:** Component READMEs enrichment (3 files)

**Current:** airtable/README.md (2/3 components)

**Read:** Original /airtable/README.md
**Extract:** Component purpose, Airtable structure, export scripts
**Integrate:** Into wireframe 4-section structure
**Pattern:** Reference /WORKING_PRINCIPLES.md + add airtable-specific principles

**Then:** integration_scripts/README.md (3/3, final component)

---

**Back to:** [docs README](README.md) | [Main README](../README.md)
