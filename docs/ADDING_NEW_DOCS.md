# Protocol: Adding New Documentation

**Department of Documentation Standard Operating Procedure**

---

## Overview

When adding a new document to the ERA_Admin documentation system, follow this protocol to maintain:
- Single source of truth (NAVIGATION_WIREFRAME.md)
- Consistent 4-section structure
- Working navigation
- Proper git workflow

---

## The Protocol

### Step 1: Identify Where the Document Belongs

**Decision tree:**

**Root-level document?**
- System-wide guide (e.g., SECURITY_GUIDE.md)
- Cross-component reference
- → Add to root section of wireframe

**Component document?**
- Specific to FathomInventory, airtable, or integration_scripts
- → Add to component's section in wireframe

**Specialized document?**
- Deep-dive guide within a component
- Technical detail document
- → Add as subsection under component

---

### Step 2: Add to NAVIGATION_WIREFRAME.md

**Template to use:**

```markdown
---

## FILE: path/to/NEW_DOCUMENT.md

**Path:** `path/to/NEW_DOCUMENT.md`

### 1. Overview

**Purpose:** [Brief one-line purpose]

[Comprehensive explanation of what this document covers]

**This document contains:**
- [Bullet point]
- [Bullet point]
- [Bullet point]

### 2. Orientation - Where to Find What

**You are at:** [Describe location in hierarchy]

**Use this when:**
- [Scenario 1]
- [Scenario 2]

**What you might need:**
- **Parent** → [link] - [description]
- **Related** → [link] - [description]
- **System-wide** → [/WORKING_PRINCIPLES.md](#file-working_principlesmd) - Overall philosophy

### 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](#file-working_principlesmd)

**Component-specific:** See [../README.md](#file-componentreadmemd) Section 3

**Document-specific principles:**

[Add any principles specific to this document's domain]

### 4. Specialized Topics

[Main content sections here]

**Back to:** [Parent README](#link) | [/README.md](#file-readmemd)
```

**Critical elements:**
- ✅ Use `## FILE: path.md` header (for parser)
- ✅ Include `**Path:**` line (for clarity)
- ✅ Follow 4-section structure exactly
- ✅ Use anchor links: `#file-filename` (lowercase, no punctuation)
- ✅ Include "Back to:" navigation at end
- ✅ Reference up to principles (don't duplicate)

---

### Step 3: Update Link Map in Generator

Edit `docs/generate_from_wireframe.py`:

```python
def convert_links(content: str, current_file: str) -> str:
    # ...
    link_map = {
        # ... existing links ...
        'file-new_documentmd': 'path/to/NEW_DOCUMENT.md',  # ADD THIS
    }
```

**Link naming convention:**
- Lowercase
- Replace `/` with nothing
- Replace `.` with nothing  
- Example: `path/to/NEW_DOCUMENT.md` → `file-pathtonew_documentmd`

---

### Step 4: Create Feature Branch

**Always use feature branch + PR workflow:**

```bash
git checkout main
git pull
git checkout -b docs/add-new-document
```

---

### Step 5: Make Changes & Test

**Edit wireframe:**
```bash
# Edit docs/NAVIGATION_WIREFRAME.md
vim docs/NAVIGATION_WIREFRAME.md

# Add your new ## FILE: section
```

**Update generator if needed:**
```bash
# Update link map
vim docs/generate_from_wireframe.py
```

**Regenerate docs:**
```bash
cd docs
rm -rf ../docs_generated
python3 generate_from_wireframe.py
```

**Test navigation:**
```bash
# Check the generated file
cat ../docs_generated/path/to/NEW_DOCUMENT.md

# Verify links work
grep "Back to:" ../docs_generated/path/to/NEW_DOCUMENT.md

# Run navigation test
python3 test_navigation.py ../docs_generated
```

---

### Step 6: Update References

**Update parent document to reference new doc:**

In the parent README (e.g., `FathomInventory/README.md` section of wireframe):

```markdown
**Specialized Documentation:**
- [NEW_DOCUMENT.md](#file-pathtonew_documentmd) - Brief description
```

**Update root README if relevant:**

If it's a major new guide, mention in root README navigation.

---

### Step 7: Commit & Push Feature Branch

```bash
git add docs/NAVIGATION_WIREFRAME.md
git add docs/generate_from_wireframe.py  # if modified
git commit -m "Add NEW_DOCUMENT.md to documentation

Added complete 4-section documentation for [topic]:

Section 1: [Overview summary]
Section 2: [Orientation summary]  
Section 3: [Principles summary]
Section 4: [Specialized topics summary]

Updated:
- NAVIGATION_WIREFRAME.md - New FILE section
- generate_from_wireframe.py - Link map (if needed)

Navigation tested: All links working, no orphans"

git push origin docs/add-new-document
```

---

### Step 8: Create & Merge PR

```bash
gh pr create --title "Add NEW_DOCUMENT.md to documentation" --body "
## What This Adds

New documentation: path/to/NEW_DOCUMENT.md

## Purpose
[Brief explanation]

## Structure
- ✅ Full 4-section structure
- ✅ Navigation links added
- ✅ Referenced from parent README
- ✅ Tests passing

## Testing
- ✅ Regenerated docs successfully
- ✅ Navigation integrity verified
- ✅ Links working at all levels
"

# After review/approval:
gh pr merge --squash --delete-branch
```

---

### Step 9: Generate Production Docs

**After PR merged:**

```bash
git checkout main
git pull

# Regenerate with new content
cd docs
rm -rf ../docs_generated
python3 generate_from_wireframe.py

# Replace production docs
python3 archive_and_replace.py
# Type "yes" at prompt

# Commit the generated files
git checkout -b docs/regenerate-after-new-document
git add [all modified files]
git commit -m "Regenerate documentation after adding NEW_DOCUMENT.md"
git push origin docs/regenerate-after-new-document

gh pr create --fill
gh pr merge --squash --delete-branch
```

---

## Quick Reference Checklist

**Adding a new document:**

- [ ] Identify where it belongs (root/component/specialized)
- [ ] Add `## FILE:` section to NAVIGATION_WIREFRAME.md
- [ ] Use full 4-section structure
- [ ] Add to link map in generate_from_wireframe.py (if needed)
- [ ] Create feature branch
- [ ] Test generation (regenerate docs_generated)
- [ ] Test navigation (run test_navigation.py)
- [ ] Update parent README to reference new doc
- [ ] Commit to feature branch with clear message
- [ ] Create PR with description
- [ ] Merge PR
- [ ] Regenerate production docs via another PR

---

## Common Mistakes to Avoid

❌ **Don't:** Add document directly to repo without wireframe
- **Why:** Bypasses single source of truth
- **Fix:** Always add to wireframe first

❌ **Don't:** Forget to update link map
- **Why:** Links won't convert properly
- **Fix:** Add to convert_links() in generator

❌ **Don't:** Skip navigation testing
- **Why:** Could create orphan documents
- **Fix:** Always run test_navigation.py

❌ **Don't:** Commit directly to main
- **Why:** Violates PR protocol, protection will reject
- **Fix:** Use feature branch + PR workflow

❌ **Don't:** Duplicate principles content
- **Why:** Creates maintenance burden
- **Fix:** Reference up to parent/system principles

---

## Special Cases

### Adding a docs/ Subdirectory Document

Example: `docs/TESTING_GUIDE.md` (about docs themselves)

**Add self-referential section:**
```markdown
## FILE: docs/TESTING_GUIDE.md

### 2. Orientation
**You are at:** Department of Documentation guide
- **Parent** → [docs/README.md](#file-docsreadmemd)
```

### Adding to FathomInventory/docs/

Example: `FathomInventory/docs/NEW_TECHNICAL_GUIDE.md`

**Note:** These are deep technical docs, may not need wireframe section if they're truly implementation details. But if they're important for understanding the system, add them.

### Removing a Document

**Process:**
1. Remove `## FILE:` section from wireframe
2. Remove from link map
3. Regenerate docs
4. Archive old version
5. Update any references to removed doc

---

## Example: Adding SECURITY_GUIDE.md

**Step-by-step walkthrough:**

```bash
# 1. Create feature branch
git checkout -b docs/add-security-guide

# 2. Edit wireframe
vim docs/NAVIGATION_WIREFRAME.md
# Add after WORKING_PRINCIPLES.md section:

## FILE: SECURITY_GUIDE.md

**Path:** `SECURITY_GUIDE.md`

### 1. Overview
**Purpose:** Security practices and credential management

[Full content...]

### 2. Orientation
**You are at:** Root-level security guide
**What you might need:**
- [WORKING_PRINCIPLES.md](#file-working_principlesmd) - System principles
- [AI_HANDOFF_GUIDE.md](#file-ai_handoff_guidemd) - AI security protocols

### 3. Principles
**System-wide:** See [/WORKING_PRINCIPLES.md](#file-working_principlesmd)

**Security-specific:**
[Security principles...]

### 4. Specialized Topics
[Security details...]

**Back to:** [README.md](#file-readmemd)

# 3. Update generator
vim docs/generate_from_wireframe.py
# Add to link_map: 'file-security_guidemd': 'SECURITY_GUIDE.md',

# 4. Test
cd docs
python3 generate_from_wireframe.py
cat ../docs_generated/SECURITY_GUIDE.md  # Verify
python3 test_navigation.py ../docs_generated

# 5. Commit and PR
git add docs/NAVIGATION_WIREFRAME.md docs/generate_from_wireframe.py
git commit -m "Add SECURITY_GUIDE.md to documentation"
git push origin docs/add-security-guide
gh pr create --fill
```

---

## Summary

**The Golden Rule:** Wireframe first, generate second, PR always

**Every new document:**
1. Add to NAVIGATION_WIREFRAME.md
2. Update generator (if needed)
3. Test generation
4. Feature branch + PR
5. After merge, regenerate production docs

**This ensures:**
- ✅ Single source of truth maintained
- ✅ Consistent structure enforced
- ✅ Navigation integrity preserved
- ✅ PR protocol followed
- ✅ Changes documented and reviewable

---

**Next:** See [ENFORCE_PR_PROTOCOL.md](ENFORCE_PR_PROTOCOL.md) for git workflow details
