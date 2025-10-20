# ERA Admin - Data Integration Hub

**Status:** 🧪 Documentation Prototype - Testing 4-section navigation structure

---

## 1. Overview and Context Recovery

ERA Admin integrates 4 ERA data systems:

- **Google Docs Agendas** - Meeting notes with participant lists
- **Airtable** - 630 people, XX organizations
- **Fathom Inventory** - 1,953 participants tracked
- **ERA Landscape** - Network visualization

**Goal:** Unified view of the ERA community

**Current Status:** ✅ Operational, monorepo established (Oct 20, 2025)

**Recent:**
- Oct 20: Monorepo consolidation, GitHub backup established
- Oct 20: Phase 4B-2 87% complete (1,698/1,953)
- Oct 18: Configuration centralization

**What's Working:**
- ✅ Airtable exports - 630 people
- ✅ Fathom automation - Daily 3 AM runs
- ✅ Landscape deployed - https://jonschull.github.io/ERA_Landscape_Static/

---

## 2. Orientation

**You are here:** Main entry point for ERA_Admin documentation

**For newcomers:**
1. Read this overview
2. Check current state → [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md)
3. For AI assistants → [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md)
4. Understand how we work → [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md)

**For returning users:**
- Current state → [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md)
- Pick up where you left off

---

## 3. Principles

**How We Work:**

- **Human-AI Collaboration** - Human is captain, AI is critical advisor
- **Component Independence** - Clear boundaries, self-contained
- **Git/PR Workflow** - All changes via pull requests
- **Testing Discipline** - Validate before declaring done
- **Documentation Hierarchy** - 4-section structure, reference don't duplicate

**Full details:** [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md)

---

## 4. Specialized Topics

### Documentation

- [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) - Current state, resume work here
- [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md) - Guide for AI assistants
- [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md) - Philosophy, Git workflow, testing
- [NAVIGATION_DESIGN.md](../NAVIGATION_DESIGN.md) - Documentation architecture (parent folder)

### Components

- [FathomInventory/](FathomInventory/) - Automated meeting analysis
- [airtable/](airtable/) - Manual membership tracking
- [integration_scripts/](integration_scripts/) - Cross-component bridges

---

**This is a prototype.** Original documentation in parent folder remains authoritative until this is validated.
