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

**Status:** In progress - 1/4 root docs enriched

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

1. **Root Docs** (4 files)
   - [x] README.md - ✅ COMPLETE
   - [ ] CONTEXT_RECOVERY.md - NEXT
   - [ ] AI_HANDOFF_GUIDE.md
   - [ ] WORKING_PRINCIPLES.md
   
   **Before starting:** Read this CONTEXT_RECOVERY
   **Sources:** Original files in parent directory
   **Goal:** Comprehensive 4-section docs with good explanations

2. **Component READMEs** (3 files)
   - [ ] FathomInventory/README.md
   - [ ] airtable/README.md
   - [ ] integration_scripts/README.md
   
   **Before starting:** Read this CONTEXT_RECOVERY
   **Sources:** Original component READMEs
   **Goal:** Component context + principles (reference root + add specifics)

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

### Next Action

**Current:** CONTEXT_RECOVERY.md enrichment

**Read:** Original /CONTEXT_RECOVERY.md
**Extract:** Current state explanations, resuming work guidance
**Integrate:** Into wireframe 4-section structure
**Maintain:** Status information (no status in Section 1 Overview)

**Then:** Read this file before AI_HANDOFF_GUIDE.md

---

**Back to:** [docs README](README.md) | [Main README](../README.md)
