# Documentation Prototype

**Purpose:** Test the 4-section navigation structure in practice  
**Status:** Prototype - Do not use as authoritative source  
**Date:** October 20, 2025

---

## What This Is

A parallel documentation tree implementing the 4-section structure:

1. **Overview and Context Recovery** - What is this? Where are we now?
2. **Orientation** - Path to here, who uses this, when to read
3. **Principles** - How we work (reference root + add specifics)
4. **Specialized Topics** - Links to all other docs (mandatory TOC)

## Structure

```
docs_prototype/
├── README.md                           # Root - 4 sections
├── CONTEXT_RECOVERY.md                 # Current state
├── AI_HANDOFF_GUIDE.md                 # AI guide
├── WORKING_PRINCIPLES.md               # Principles
├── FathomInventory/
│   ├── README.md                       # Component - 4 sections
│   ├── CONTEXT_RECOVERY.md             # Component context
│   └── authentication/
│       └── README.md                   # Specialized - 4 sections
├── airtable/
│   └── README.md                       # Component - 4 sections
└── integration_scripts/
    ├── README.md                       # Component - 4 sections
    └── AI_WORKFLOW_GUIDE.md            # Specialized - 4 sections
```

## Test Scenarios

**Scenario 1: New AI arrives**
1. Start at [README.md](README.md)
2. Follow to [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md)
3. Check [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md)
4. Ready to work on [component](FathomInventory/README.md)

**Scenario 2: Working on FathomInventory auth**
1. Deep in [FathomInventory/authentication/](FathomInventory/authentication/README.md)
2. References [FathomInventory principles](FathomInventory/README.md#3-principles)
3. References [root principles](WORKING_PRINCIPLES.md)
4. Can navigate back to [main](README.md)

**Scenario 3: Finding Git workflow**
1. From any component README
2. Follow to [WORKING_PRINCIPLES.md](WORKING_PRINCIPLES.md)
3. Find Git/PR section
4. No duplication elsewhere

## Validation Questions

- [ ] Can you find everything from any starting point?
- [ ] Is anything duplicated vs referenced?
- [ ] Are component principles clearly additive (not repetitive)?
- [ ] Can you get back to main from anywhere?
- [ ] Do the 4 sections work in practice?

## Comparison with Original

**Original docs:** `/ERA_Admin/*.md` (parent folder)  
**This prototype:** `/ERA_Admin/docs_prototype/*.md`

**Original remains authoritative** until this is validated and migrated.

## Next Steps

1. **User validates:** Click through scenarios, test navigation
2. **Identify issues:** What's confusing? What's redundant?
3. **Iterate design:** Fix problems in prototype
4. **When confident:** Decide whether/how to migrate to main docs

---

**This is a safe sandbox. Original documentation unchanged.**
