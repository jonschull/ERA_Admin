# integration_scripts/README.md

# integration_scripts/

**Purpose:** Integration workflows between ERA's various data systems

---

## Overview

ERA Admin manages data across multiple systems that need to be integrated and kept in sync:
- **Fathom**: Video call transcripts and participant data
- **Airtable**: Curated member database
- **ERA Landscape**: Network visualization
- **Future**: Surveys, grants, projects, etc.

This component provides integration workflows for cross-system data synchronization.

---

## Current Integrations

### participant_reconciliation/

**Status:** ✅ Production-ready  
**Purpose:** Reconcile Fathom participant data with Airtable member database

Integrates:
- Fathom video call participants (682 people, AI-generated names)
- Airtable members (630 people, human-curated)
- Town Hall attendance tracking
- Alias resolution system

**Achievements:**
- Phase 4B-1: 364 participants enriched via fuzzy matching
- Phase 4B-2: 459 participants validated through collaborative review (11 batches)
- Alias resolution: 38 duplicates merged, 77% redundancy reduction
- 100% validation achieved

**See:** [participant_reconciliation/README.md](#file-integration_scriptsparticipant_reconciliationreadmemd)

**Active for:**
- Phase 5T: Town Hall visualization in ERA Landscape
- Phase 4C (future): Processing additional participants as they join

---

## Future Integrations

**Candidates for future integration types:**

- **Survey Integration**: Sync ERA member survey responses
- **Project Data Integration**: Connect project databases
- **Grant Tracking Integration**: Coordinate grant management across systems
- **Content Integration**: Sync articles, resources, publications
- **Event Data Integration**: Coordinate event attendance and outcomes

**Pattern to follow:**
1. Create subdirectory (e.g., `survey_integration/`)
2. Include README.md documenting purpose, status, achievements
3. Separate reusable tools from one-time execution scripts
4. Archive completed work in `archive/` subdirectory
5. Document learnings and patterns for future similar work

---

## Architecture Principles

**From participant_reconciliation learnings:**

1. **Human-AI Collaboration**
   - AI applies intelligent judgment (pattern recognition, multi-factor analysis)
   - Human provides guidance and corrections
   - Scripts execute approved decisions mechanically

2. **Reusability Over One-Time Scripts**
   - Separate generic tools from batch-specific execution
   - Archive completed work but preserve patterns
   - Document what worked vs what didn't

3. **Data Safety**
   - Automatic backups before changes
   - Comprehensive validation
   - Reversible operations
   - Audit trails

4. **Incremental Processing**
   - Process in batches with human review
   - Generate evidence-rich HTML for decisions
   - CSV for feedback and corrections
   - Learn from corrections

**See:** [/HOW_TO_BE_AN_INTELLIGENT_ASSISTANT.md](#file-how_to_be_an_intelligent_assistantmd) for AI collaboration patterns

---

## What You Might Need

**System overview:**
- [/README.md](../README.md) - ERA Admin system architecture
- [/CONTEXT_RECOVERY.md](../CONTEXT_RECOVERY.md) - Current status across all components
- [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) - System-wide philosophy

**Related components:**
- [FathomInventory/README.md](../FathomInventory/README.md) - Video call data
- [airtable/README.md](../airtable/README.md) - Member database
- [ERA_Landscape/README.md](#file-era_landscapereadmemd) - Network visualization

---

## For New Integrations

**When creating a new integration type:**

1. **Review participant_reconciliation/ as template**
   - Reusable tools vs one-time scripts
   - Archive structure
   - Documentation patterns

2. **Document clearly**
   - What systems are being integrated?
   - What problem does this solve?
   - What's the current status?
   - What patterns emerged?

3. **Separate concerns**
   - Tools (reusable)
   - Data (active state)
   - Archive (completed work)
   - Documentation (guides and summaries)

4. **Follow safety principles**
   - Backups before modifications
   - Validation of results
   - Human oversight for decisions
   - Audit trails

---

**Component structure managed:** October 25, 2025  
**Current integrations:** 1 (participant_reconciliation)

**Back to:** [README.md](../README.md)