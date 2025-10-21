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
- NAVIGATION_WIREFRAME.md contains all content
- Production docs generated from wireframe
- Never edit production docs directly
- Always edit wireframe → regenerate → commit

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

#### Documentation Workflow

**Normal workflow (incremental edits):**

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