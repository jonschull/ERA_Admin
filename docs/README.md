# docs/README.md

### 1. Overview

**Purpose:** Documentation system design, prototyping, and maintenance

The docs/ component manages ERA_Admin's documentation infrastructure, including the wireframe-based generation system and protocols for maintaining documentation consistency.

**What this component does:**
- Maintains NAVIGATION_WIREFRAME.md (single source of truth)
- Generates production documentation via generate_from_wireframe.py
- Validates navigation integrity (no orphans, all paths work)
- Provides protocols for adding/updating documentation

**Key files:**
- NAVIGATION_WIREFRAME.md - Complete documentation content (3,400+ lines)
- generate_from_wireframe.py - Parser/generator for production docs
- update_docs.sh - Helper script for regeneration workflow
- test_navigation.py - Navigation integrity validator

### 2. Orientation - Where to Find What

**You are at:** Documentation department README

**Use this when:**
- Adding new documentation
- Updating existing docs
- Understanding doc structure
- Troubleshooting navigation

**What you might need:**
- **Parent** → [/README.md](../README.md) - System overview
- **Wireframe** → NAVIGATION_WIREFRAME.md - Full documentation content
- **Principles** → [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md) - System-wide philosophy
- **Current state** → CONTEXT_RECOVERY.md - Documentation work status

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)

**Documentation-specific principles:**

**1. Single Source of Truth**
- NAVIGATION_WIREFRAME.md contains all internal documentation (see "What Goes Where" below)
- Production docs generated from wireframe
- Never edit production docs directly
- Always edit wireframe → regenerate → commit
- Exception: During active development, create docs in component folders, consolidate to wireframe before PR merge

**2. 4-Section Structure**
- Section 1: Overview (what/purpose)
- Section 2: Orientation (navigation help)
- Section 3: Principles (reference up + add specifics)
- Section 4: Specialized Topics (details)

**3. Navigation Integrity**
- No orphan documents (every doc reachable)
- Always navigate up (back to parent/root)
- Cross-references work at all levels

**4. No Redundancy**
- Reference up to system principles
- Add component-specific details only
- Don't duplicate explanations

### 4. Specialized Topics

#### Documentation Policy: What Goes Where

**ALL internal documentation goes in NAVIGATION_WIREFRAME.md:**

**Include (with full content):**
- ✅ Component READMEs (external interface)
- ✅ Architecture docs (NETWORK_ARCHITECTURE.md, DEVELOPMENT.md, etc.)
- ✅ Context recovery docs (CONTEXT_RECOVERY.md, AI_HANDOFF_GUIDE.md)
- ✅ Testing strategies (TESTING.md)
- ✅ Deployment guides (DEPLOYMENT_GUIDE.md)
- ✅ Current status docs (KNOWN_ISSUES.md, NEXT_STEPS.md)
- ✅ Design decisions (VISION.md)

**Goal:** Future developer/AI can understand entire system from wireframe alone

**Exclude → move to /historical:**
- ❌ Temporary session notes (SESSION_SUMMARY_2025-10-15.md)
- ❌ Obsolete/superseded documentation
- ❌ One-time work products
- ❌ Archived context (preserved but not active)

**Why full wireframe approach:**
1. **Internal consistency** - Update terminology everywhere at once
2. **No drift** - Production docs always match source
3. **AI context** - One file contains complete structure
4. **Navigation validation** - Automated tests catch orphans
5. **Cross-component refactoring** - See all dependencies

**Cost:** ~5 seconds per edit (edit wireframe → regenerate)
**Benefit:** Guaranteed consistency, no lost docs, complete context recovery

#### Documentation Workflow

**During active development (feature branch):**
```bash
# Create docs in component directories as you work
vim ERA_Landscape/NETWORK_ARCHITECTURE.md
git add ERA_Landscape/
git commit -m "docs: Document Town Hall physics"
```

**Before merging PR (consolidation checkpoint):**
```bash
# 1. Review what docs were created
ls -la ERA_Landscape/*.md

# 2. Identify: Internal (→ wireframe) vs Temporary (→ historical)
# Internal: Needed to understand/develop system
# Temporary: Session notes, obsolete content

# 3. Move temporary/obsolete to historical
mv ERA_Landscape/SESSION_SUMMARY_*.md historical/

# 4. Add internal docs to wireframe
vim docs/NAVIGATION_WIREFRAME.md
# Add ## FILE: sections with full content

# 5. Regenerate
./docs/update_docs.sh

# 6. Commit together
git add -A
git commit -m "docs: Consolidate ERA_Landscape docs into wireframe"
```

**PR checklist:**
- [ ] New internal docs added to NAVIGATION_WIREFRAME.md?
- [ ] Temporary/obsolete docs moved to /historical?
- [ ] Component README lists all files in "Specialized Topics"?
- [ ] Regenerated: `./docs/update_docs.sh`
- [ ] Navigation validated (all links resolve)

**Normal workflow (incremental edits to existing docs):**

```bash
# 1. Create feature branch
git checkout -b docs/update-something

# 2. Edit the wireframe
vim docs/NAVIGATION_WIREFRAME.md

# 3. Regenerate docs
./docs/update_docs.sh

# 4. Review changes
git diff

# 5. Commit and PR
git add -A
git commit -m "Update documentation: [description]"
git push origin docs/update-something
gh pr create --fill
gh pr merge --squash --delete-branch
```

**For major overhauls only:**
```bash
python3 docs/archive_and_replace.py  # Creates backup, replaces all
```

#### Adding New Documents

**Template for new document in wireframe:**

```markdown