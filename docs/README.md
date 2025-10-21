# docs - Department of Documentation

---

## 1. Overview

docs is one of the components in ERA_Admin.

**Purpose:** Documentation system design, prototyping, and validation

**What this department does:**
- Design documentation structure and navigation
- Prototype and test new documentation patterns
- Validate navigation integrity (no orphans, always can navigate up)
- Manage documentation wireframes and templates

---

## 2. Orientation - Where to Find What

**You are at:** Documentation department README

**What you might need:**
- Parent README → [/README.md](../README.md)
- Current doc work status → [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md)
- System principles → [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)
- What we're building → See Specialized Topics below

---

## 3. Principles

**System-wide:** See [/WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)

**Documentation-specific:**

1. **Navigation Tree Integrity**
   - No orphan documents (every doc reachable from a README)
   - Always navigate up (every README references parent)
   - Mandatory TOC (all files listed in Specialized Topics)

2. **4-Section Structure**
   - Section 1: Overview (what is this, what it does - no status)
   - Section 2: Orientation - Where to Find What (you are at, what you might need)
   - Section 3: Principles (reference system + add specifics)
   - Section 4: Specialized Topics (mandatory TOC of all other docs)

3. **No Redundancy**
   - Reference up to root principles
   - Add component-specific details only
   - Don't duplicate explanations

4. **Assume No Foreknowledge**
   - Write for newcomers
   - Explain concepts, don't just bullet them
   - Cherry-pick good explanations from original docs

---

## 4. Specialized Topics

### Design Documents

- [NAVIGATION_WIREFRAME.md](NAVIGATION_WIREFRAME.md) - Complete documentation structure with 4-section pattern
- [NAVIGATION_DESIGN.md](NAVIGATION_DESIGN.md) - Original design document (historical)
- [NAVIGATION_PROTOTYPE.md](NAVIGATION_PROTOTYPE.md) - Single-doc clickable prototype (historical)

### Working Files

- [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md) - Current status of documentation work

### Tests (Future)

- test_navigation_integrity.py - Validate no orphans, parent links
- test_toc_completeness.py - Verify all files in Specialized Topics

### Prototype Folder

- prototype/ - Generated test documentation (safe sandbox)

---

**Back to:** [Main README](../README.md)
