# path/to/NEW_DOC.md

### 1. Overview
**Purpose:** [one-line purpose]
[Full explanation]

### 2. Orientation - Where to Find What
**You are at:** [location description]
**What you might need:**
- [Parent link]
- [Related links]

### 3. Principles
**System-wide:** See [/WORKING_PRINCIPLES.md](../../WORKING_PRINCIPLES.md)
[Document-specific principles]

### 4. Specialized Topics
[Main content]

**Back to:** [Parent](#link) | [/README.md](../../README.md)
```

**Steps to add:**
1. Add `## FILE:` section to NAVIGATION_WIREFRAME.md
2. Update link map in generate_from_wireframe.py (if needed)
3. Run `./docs/update_docs.sh`
4. Update parent README to reference new doc
5. Test navigation
6. Commit via PR

**Link naming convention:**
- File: `path/to/NEW_DOC.md`
- Anchor: `#file-pathtonew_docmd` (lowercase, no punctuation)

#### Helper Scripts

**update_docs.sh** - Regenerate production docs from wireframe
```bash
./docs/update_docs.sh
# - Cleans docs_generated/
# - Runs generate_from_wireframe.py
# - Copies to production locations
# - Shows git diff summary
```

**archive_and_replace.py** - Safe replacement with backup (rare use)
```bash
python3 docs/archive_and_replace.py
# - Creates timestamped backup in historical/
# - Generates rollback script
# - Replaces all 10 files
# Use for: major overhauls, structural changes
```

**test_navigation.py** - Validate navigation integrity
```bash
python3 docs/test_navigation.py docs_generated
# - Checks for orphans
# - Verifies all paths to root
# - Tests link conversion
```

#### Design Documents

**Current (Active):**
- NAVIGATION_WIREFRAME.md - Complete doc system (single source of truth)
- generate_from_wireframe.py - Production generator
- update_docs.sh - Regeneration helper

**Historical (Reference):**
- NAVIGATION_DESIGN.md - Original design rationale
- NAVIGATION_PROTOTYPE.md - Single-doc clickable prototype
- docs_prototype/ - Early experiments

#### Validation & Testing

**Pre-commit checks:**
```bash
# Regenerate and check
./docs/update_docs.sh
git diff --stat

# Test navigation
python3 docs/test_navigation.py docs_generated

# Test script references
python3 docs/test_script_references.py
```

**Validation reports:**
- WIREFRAME_VALIDATION_REPORT.md - Coverage and consistency
- NAVIGATION_TEST_RESULTS.md - Navigation integrity
- SCRIPT_COVERAGE_REPORT.md - Script reference analysis

**Back to:** [/README.md](../../README.md)