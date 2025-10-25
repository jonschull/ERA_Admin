# WORKING_PRINCIPLES.md

### 1. Overview

**Purpose:** Explicit articulation of implicit principles guiding ERA Admin development

**Audience:** Humans and AIs working on the system

**This document contains:**
- Core philosophy (human-AI collaboration, vigilance against self-delusion)
- Component architecture (self-contained, modular approach)
- Documentation & recoverability (3-level hierarchy, quality principles)
- Version control & collaboration (Git/PR practices, living documents)
- Testing & validation (test before claiming success, incremental testing)
- Quality & pragmatism (trust working solutions, avoid over-engineering)
- Decision-making framework (when to pause vs proceed, debugging methodology)
- Context & communication (respect time, preserve context)

**This document IS the principles** - referenced by README, AI_HANDOFF_GUIDE, and component docs

### 2. Orientation - Where to Find What

**You are at:** System-wide principles document

**Referenced by:**
- [README.md](README.md) - Section 3 references these principles
- [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md) - Section 3 references these principles
- Component READMEs - Section 3 references these, then adds component-specific principles

**What you might need:**
- Main entry → [README.md](README.md)
- Current state → [CONTEXT_RECOVERY.md](CONTEXT_RECOVERY.md)
- AI guidance → [AI_HANDOFF_GUIDE.md](AI_HANDOFF_GUIDE.md)
- Component-specific principles → See component READMEs (they reference this, then add specifics)

### 3. Principles

**This document IS the principles.**

The content below in Section 4 contains all the principles. They are organized into:

1. **Core Philosophy** - Human-AI collaboration, vigilance against self-delusion
2. **Component Architecture** - Self-contained components, modular approach
3. **Documentation & Recoverability** - 3-level hierarchy, quality over quantity
4. **Version Control & Collaboration** - Git/PR workflow, living documents
5. **Testing & Validation** - Test before declaring success, generate evidence
6. **Quality & Pragmatism** - Working > perfect, simple > clever
7. **Decision-Making** - When to pause vs proceed, debugging methodology
8. **Context & Communication** - Respect time, preserve context

**Components should:**
- Reference this document in their Section 3
- Add component-specific principles (not duplicate these)
- Follow "System: See WORKING_PRINCIPLES.md" + "Component-specific: ..." pattern

### 4. Specialized Topics

#### 1. Core Philosophy

**Human-AI Collaboration**

**The Captain-Advisor Model:**
- **Human is Captain** - Sets direction, makes decisions, approves actions
- **AI is Critical Collaborator** - Questions assumptions, proposes alternatives, executes approved tasks
- **Not compliance, but collaboration** - AI should challenge, not just obey

**In Practice:**
- ✅ AI asks: "Should I proceed?" before implementing
- ✅ AI says: "Here's a risk you may have overlooked..."
- ✅ Human says: "Does this make sense?" expecting two answers:
  1. "Do you understand?"
  2. "What considerations am I overlooking?"
- ❌ AI assumes approval from discussion
- ❌ AI declares success without validation
- ❌ AI moves forward without explicit go-ahead

**Vigilance Against Self-Delusion**

**Proactive Validation Before Declaring Success:**
1. Think: "What test will the user apply?"
2. Run that test yourself FIRST
3. Show results, THEN ask user to verify
4. Never declare "done" without user confirmation

**Wait for Guidance:**
- User silence ≠ approval
- Discussion ≠ directive to implement
- Don't hallucinate user assent
- Don't advance without explicit approval

#### 2. Component Architecture

**Self-Contained Components**

**What is a Component:**
- **Self-documenting:** Has README.md and (for complex ones) AI_HANDOFF_GUIDE.md
- **Self-contained:** Can be understood without reading other components
- **Clear interfaces:** Exposes data via documented formats (CSV, database, API)
- **Minimal coupling:** Integration happens at integration layer, not within components

**Current Components:**
- `airtable/` - Manual membership tracking
- `FathomInventory/` - Automated meeting analysis
- `integration_scripts/` - Integration workflows (participant_reconciliation/, future types)
- `ERA_Landscape/` - Network visualization (Town Halls, interactive graph)

**Principle:** You should NOT need to understand all component internals to work at integration level.

**Modular, Incremental Approach**

**Incremental over Big-Bang:**
- Build in small, testable steps
- Validate each step before proceeding
- Update documentation as you go
- Prefer working solutions over perfect solutions

**Modular over Monolithic:**
- Components have clear boundaries
- Integration happens through documented interfaces
- Changes in one component don't cascade to others
- Each component can evolve independently

#### 3. Documentation & Recoverability

**Context Recovery is Critical**

**Problem:** Humans (and AI contexts) forget. Work gets interrupted.

**Solution:** Documentation that enables resuming work quickly.

**Three Levels of Documentation:**

*Level 1: System Overview (ERA_Admin level)*
- `README.md` - What is this? Where do I start?
- `CONTEXT_RECOVERY.md` - Current state, what's in progress, how to resume
- `AI_HANDOFF_GUIDE.md` - AI workflow and conventions
- `ERA_ECOSYSTEM_PLAN.md` - Strategic direction and integration roadmap

*Level 2: Component Level*
- Each component has `README.md` (overview, quick start)
- Complex components have `CONTEXT_RECOVERY.md` (component state)
- Complex components have `DEVELOPMENT.md` (dev workflow)

*Level 3: Implementation Details*
- Component-specific configuration files
- Inline code comments for complex logic
- Validation reports from data operations

**Navigation Rule:** Start at highest level needed. Deep-dive only when necessary.

**Documentation Quality Principles**

**Accuracy Over Aspiration:**
- Document actual state, not desired state
- Update docs when system changes
- Archive outdated docs (don't delete history)
- Mark plans as "COMPLETE" or "IN PROGRESS" clearly

**Actionable Over Descriptive:**
- Show commands to run, not just concepts
- Include expected outputs
- Provide troubleshooting steps
- Link to relevant resources

**Concise Over Comprehensive:**
- Respect reader's time
- Use bullet points over paragraphs
- Bold key information
- Reference detailed docs rather than duplicating

#### 4. Version Control & Collaboration

**Git & PR Practices**

**Protected Main Branch:**
- Never commit directly to `main`
- All changes via Pull Requests
- PRs enable review and discussion

**PR Workflow:**
1. Create feature branch: `git checkout -b fix-description`
2. Make changes, test locally
3. Commit with clear message
4. Push and create PR: `gh pr create`
5. After merge, update local: `git pull origin main`

**Commit Message Quality:**
- **First line:** Brief, actionable summary
- **Body:** What changed, why it changed, what was tested
- **Reference:** Related issues, PRs, or documents

**Git Hygiene:**
- `.gitignore` protects secrets (cookies, tokens, databases)
- Check before commit: `git status`, look for sensitive files
- Use `.gitignore` patterns for generated files

**Enforcement: Branch Protection (Two Layers)**

Documentation alone is insufficient. Enforce PR protocol at both local and remote:

*Layer 1: Local Pre-Commit Hook (blocks commits before they happen)*

After cloning, install the pre-commit hook:
```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
branch=$(git symbolic-ref HEAD 2>/dev/null | sed 's!refs/heads/!!')
if [ "$branch" = "main" ]; then
    cat << 'MSG'
❌ ERROR: Direct commits to 'main' branch are not allowed

✅ Proper workflow:
   1. Create feature branch: git checkout -b feature/description
   2. Make commits on that branch
   3. Create PR: gh pr create
   4. After merge: git checkout main && git pull

See WORKING_PRINCIPLES.md Section 4 (Git & PR Practices)
MSG
    exit 1
fi
EOF
chmod +x .git/hooks/pre-commit
```

*Layer 2: GitHub Branch Protection (blocks pushes)*

Setup (one-time):
```bash
# Via GitHub CLI:
gh api repos/OWNER/REPO/branches/main/protection -X PUT --input - << 'EOF'
{
  "required_status_checks": null,
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0
  },
  "restrictions": null
}
EOF
```

*Or via web UI:*
1. Go to: https://github.com/OWNER/REPO/settings/branches
2. Add rule for `main`
3. Check: "Require pull request before merging"
4. Check: "Include administrators" (enforces for everyone)
5. Set required approvals to 0 (for solo work)

*Result:* Direct commits to main blocked locally; pushes blocked remotely.

**Living Documents**

**Documents Evolve:**
- Update `CONTEXT_RECOVERY.md` after significant state changes
- Mark plans as "COMPLETE" when done
- Archive outdated docs to `historical/` with context
- Keep current docs minimal and accurate

#### 5. Testing & Validation

**Test Before Claiming Success**

**Testing Discipline:**
1. **Run the actual code** - Don't assume it works
2. **Check the output** - Verify results match expectations
3. **Test edge cases** - What happens with 0 results? Errors?
4. **Validate end-to-end** - Does the whole workflow work?

**Validation Before Declaration:**
- ❌ "I've implemented X" (untested)
- ✅ "I've implemented X. Tested with Y inputs, got Z outputs. Please verify."

**Incremental Testing**

**Test as You Build:**
- Don't build entire feature then test
- Test each component as it's built
- Catch bugs early when context is fresh
- Update CONTEXT_RECOVERY.md after each validated step

**What to Test:**
- **Syntax:** Does it run?
- **Logic:** Does it produce correct results?
- **Integration:** Do components work together?
- **Edge cases:** What breaks it?

**Validation Reports**

**Generate Evidence:**
- Create markdown reports for data operations
- Include metrics: matched, updated, inserted, errors
- Show sample data for verification
- Enable user to validate without re-running

**Example:**
```python
print(f"✅ Processed {count} records")
print(f"📊 Report saved to: enrichment_report.md")
print(f"🎯 Next step: Review report, then run Phase 5")
```

#### 6. Quality & Pragmatism

**Trust Working Solutions**

**Principles:**
- **Working > Perfect** - Ship tested, working code over elegant, untested code
- **Standard > Custom** - Use standard tools/patterns over custom solutions
- **Simple > Clever** - Prefer obvious code over clever tricks
- **Tested > Assumed** - Working code beats elegant design

**Avoid Over-Engineering:**
- Solve actual problems, not hypothetical ones
- Add complexity only when needed
- Keep configurations minimal
- Respect YAGNI (You Aren't Gonna Need It)

**Clean Implementation**

**Directory Structure:**
- Root minimal - only essential files
- `docs/` clearly identified
- `historical/` preserves context
- Each component self-contained

**Code Quality:**
- Follow existing patterns
- Use descriptive names
- Comment complex logic
- Avoid clever one-liners

#### 7. Decision-Making Framework

**When to Pause vs Proceed**

**Proceed Without Asking:**
- Reading documentation
- Running read-only test queries
- Creating validation reports
- Following documented patterns
- Implementing approved work

**Pause and Ask:**
- Modifying database schema
- Changing component architecture
- Making technology choices
- Deviating from documented plan
- Unsure about approach

**Rule:** If documented in plan for current Phase, proceed. If not documented, ask.

**When Things Go Wrong**

**Debug Methodically:**
1. **Identify scope** - Which component is failing?
2. **Read component docs** - CONTEXT_RECOVERY.md, DEVELOPMENT.md
3. **Reproduce issue** - Can you trigger it reliably?
4. **Diagnose before fixing** - Do not make changes in the uninvestigated hope that it might fix things
5. **Fix within component boundary** - Don't create cross-component dependencies
6. **Test the fix** - Verify it actually works
7. **Update documentation** - Record what broke and how you fixed it

**Escalate When:**
- Issue spans multiple components
- Architectural decision needed
- Uncertain about root cause
- Fix might break other things

#### 8. Context & Communication

**Respect Human's Valuable Time**

**Before Presenting Results:**
- Test thoroughly yourself
- Generate validation evidence
- Anticipate questions
- Provide actionable next steps

**Communication Style:**
- **Concise** - Brief but substantive
- **Factual** - Show evidence, not claims
- **Structured** - Use headings, bullets, code blocks
- **Actionable** - What should user do next?

**Preserve Context**

**For Future You/AI:**
- Update CONTEXT_RECOVERY.md after significant work
- Remember: when context recovery is needed, implicit knowledge has been lost
- Create validation reports for data operations
- Commit with detailed messages
- Archive plans when complete

**For Current Collaboration:**
- Reference docs rather than re-explaining
- Point to relevant sections: "See README.md section 3.2"
- Give clickable references when possible
- Share test outputs, not just descriptions
- Ask clarifying questions early

#### Quick Reference Checklists

**Component Self-Containment:**
- [ ] Has README.md (overview, quick start)
- [ ] Has clear input/output interfaces
- [ ] Minimal dependencies on other components
- [ ] Can be tested independently
- [ ] Documentation stays current

**Before Declaring Success:**
- [ ] Code runs without errors
- [ ] Output matches expectations
- [ ] Edge cases tested
- [ ] Validation report generated
- [ ] User confirms independent verification
- [ ] Documentation updated

**PR Quality:**
- [ ] Tested locally before pushing
- [ ] No secrets in git (check `.gitignore`)
- [ ] Clear commit messages
- [ ] Documentation updated if behavior changed
- [ ] Ready for review

#### Meta

**Living Document:** These principles evolve. When you discover new working patterns or encounter edge cases, propose updates to this document.

**Meta-Principle:** The principles themselves should follow these principles - be concise, actionable, tested in practice, and regularly validated.

**Back to:** [README.md](README.md)