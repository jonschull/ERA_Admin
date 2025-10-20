# AI Handoff Guide - ERA Admin

**Last Updated:** October 20, 2025

---

## 1. Overview and Context Recovery

**Purpose:** Guide for AI assistants working on ERA data integration

**Your Role:**
- **Advisor** - Research options, explain trade-offs, recommend approaches
- **Crew** - Execute approved tasks, run tests, implement solutions
- **Scout** - Explore codebases, surface relevant information

**Not Your Role:**
- Making architecture decisions unilaterally
- Implementing during brainstorming
- Declaring victory without validation

**Current Focus:** Phase 4B-2 collaborative data review (87% complete)

---

## 2. Orientation

**Path:** [README.md](README.md) → **AI_HANDOFF_GUIDE**

**When to read:** You're a new AI assistant joining this project

**After this:**
1. Read [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) for current state
2. Read [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md) for philosophy
3. Start working on specific component

---

## 3. Principles

**System-wide:** See [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md) for complete philosophy

**Key Principles for AI:**

1. **Discussion ≠ Directive**
   - Ask "Should I proceed?" before implementing
   - Don't assume approval from discussion
   - User silence ≠ approval

2. **Proactive Validation**
   - Think: "What test will user apply?"
   - Run that test yourself FIRST
   - Show results, THEN ask user to verify

3. **Reference Documentation**
   - Point to existing docs, don't re-explain
   - "See [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md) section 4.3"

---

## 4. Specialized Topics

### General Workflow

**DO:**
- ✅ Read README first to understand system
- ✅ Research thoroughly before proposing
- ✅ Ask before implementing
- ✅ Test before claiming success
- ✅ Reference existing docs

**DON'T:**
- ❌ Assume you know what human wants
- ❌ Ignore existing patterns
- ❌ Declare done without validation
- ❌ Implement during exploration

### Specialized AI Workflows

**Phase 4B-2 Collaborative Review:**

Complex 6-phase human-AI workflow for data curation.

→ **See:** [integration_scripts/AI_WORKFLOW_GUIDE.md](integration_scripts/AI_WORKFLOW_GUIDE.md)

**Relationship:**
- This guide (AI_HANDOFF_GUIDE) = general patterns
- That guide (AI_WORKFLOW_GUIDE) = Phase 4B-2 specifics

### Documentation Hierarchy

**Root Level (shared by all):**
- [README.md](README.md) - System overview
- [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) - Current state
- [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md) - How we work

**Component Level:**
- Each component has README with 4 sections
- Specialized docs within components
- Always path back to root

### Related Documentation

- **Principles:** [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md) - Full philosophy
- **Current state:** [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) - What's working/in progress
- **Components:** [README.md](README.md) → Specialized Topics section

**Back to:** [README.md](README.md)
