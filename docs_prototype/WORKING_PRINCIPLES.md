# Working Principles - ERA Admin

**Last Updated:** October 20, 2025

---

## 1. Overview and Context Recovery

**Purpose:** Philosophy, architecture principles, Git/PR workflow, testing approach

**Current Application:**
- All recent work follows PR workflow (monorepo consolidation, doc fixes)
- Component boundaries maintained during consolidation
- Documentation using 4-section structure (prototype in docs_prototype/)

---

## 2. Orientation

**Path:** [README.md](README.md) → **WORKING_PRINCIPLES**

**Referenced by:**
- [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md) - AI collaboration model
- All component READMEs - When applying/extending principles

**When to read:**
- Before making architectural decisions
- When setting up Git workflow
- When component principles reference this

---

## 3. Principles

*This document IS the principles - detailed in Specialized Topics below*

---

## 4. Specialized Topics

### Human-AI Collaboration

**The Captain-Advisor Model:**

- **Human is Captain** - Sets direction, makes decisions, approves actions
- **AI is Critical Collaborator** - Questions assumptions, proposes alternatives, executes tasks
- **Not compliance, but collaboration** - AI should challenge, not just obey

**In Practice:**
- ✅ AI asks: "Should I proceed?" before implementing
- ✅ AI says: "Here's a risk you may have overlooked..."
- ✅ Human asks: "Does this make sense?" expecting both understanding AND considerations
- ❌ AI assumes approval from discussion
- ❌ AI declares success without validation
- ❌ AI moves forward without explicit go-ahead

### Vigilance Against Self-Delusion

**Proactive Validation Before Declaring Success:**

1. Think: "What test will user apply?"
2. Run that test yourself FIRST
3. Show results, THEN ask user to verify
4. Never declare "done" without user confirmation

**Wait for Guidance:**
- User silence ≠ approval
- Discussion ≠ directive to implement
- Don't hallucinate user assent
- Don't advance without explicit approval

### Component Architecture

**Principles:**

- **Component Independence** - Each can function standalone
- **Clear Boundaries** - Well-defined interfaces
- **Centralized Config** - `era_config.py` manages paths
- **Respect Autonomy** - Don't break component internals

**Components:**
- [FathomInventory/](FathomInventory/) - Meeting analysis
- [airtable/](airtable/) - Membership tracking
- [integration_scripts/](integration_scripts/) - Cross-component bridges

### Git & Version Control

#### Protected Main Branch

**Never commit directly to `main`**

All changes via Pull Requests to enable review and discussion.

#### PR Workflow

```bash
# 1. Create feature branch
git checkout -b fix-description

# 2. Make changes, test locally

# 3. Commit with clear message
git commit -m "Short summary

Detailed explanation:
- What changed
- Why changed
- Impact"

# 4. Push and create PR
git push origin fix-description
gh pr create

# 5. After merge, update local
git checkout main
git pull origin main
```

#### Commit Message Guidelines

**Good examples:**
- "Fix test_recent_logs.py path after migration"
- "Documentation: Navigation design and audits"
- "Create navigation prototype for testing"

**Bad examples:**
- "updates" (what updates?)
- "fix bug" (which bug?)
- "changes" (what changes?)

#### Secret Management

- All secrets in `.gitignore`
- Use templates (e.g., `config.py.template`)
- Never commit credentials
- Check before pushing: `git diff --cached`

### Testing Discipline

**Before declaring "done":**

1. ✅ Run relevant tests
2. ✅ Test the happy path
3. ✅ Test error conditions
4. ✅ Verify no regressions
5. ✅ Show user the test results

**Philosophy:** Trust but verify. Proactive validation prevents self-delusion.

**Example from Oct 20:**
- Fixed test_recent_logs.py
- Ran test to verify fix
- Showed passing results
- Then committed

### Documentation Practices

**4-Section Structure:**

Every README has:

1. **Overview and Context Recovery** - What is this? Where are we now?
2. **Orientation** - Path to here, who uses this, when to read
3. **Principles** - How do we work? (reference root + add specifics)
4. **Specialized Topics** - Links to all other docs in folder

**Rules:**
- Link, don't duplicate
- Component principles reference root principles, add specifics
- Every file must be listed in Specialized Topics
- Bidirectional navigation (up to context, down to details)

**See:** [NAVIGATION_DESIGN.md](../NAVIGATION_DESIGN.md) (parent folder) for full architecture

### Related Documentation

**This principle applied:**
- [README.md](README.md) - System overview follows structure
- [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md) - References this for principles
- All component READMEs - Reference and extend these principles

**Back to:** [README.md](README.md)
