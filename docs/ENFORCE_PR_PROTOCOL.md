# Enforcing PR Protocol with Branch Protection

**Problem:** Documentation of PR protocol is insufficient - we keep committing directly to main

**Solution:** GitHub Branch Protection Rules (technical enforcement)

---

## Option 1: GitHub Branch Protection (Recommended)

### Setup Steps

**Via GitHub Web UI:**
1. Go to: https://github.com/jonschull/ERA_Admin/settings/branches
2. Click "Add branch protection rule"
3. Branch name pattern: `main`
4. Enable these settings:
   - ☑️ **Require a pull request before merging**
     - ☑️ Require approvals: 0 (for solo work)
     - ☐ Dismiss stale PR approvals (not needed for solo)
   - ☑️ **Require status checks to pass** (optional)
   - ☐ Require conversation resolution (optional)
   - ☐ Require signed commits (optional)
   - ☑️ **Include administrators** (CRITICAL - enforces for you too!)

5. Click "Create" or "Save changes"

**Result:**
```bash
# This will now FAIL:
git commit -m "message"
git push origin main
# Error: refusing to allow a protected branch to be updated without a pull request

# Must do this instead:
git checkout -b feature/my-change
git commit -m "message"
git push origin feature/my-change
gh pr create
gh pr merge
```

---

## Option 2: Pre-Push Git Hook (Local Enforcement)

**For local safety before GitHub push:**

Create `.git/hooks/pre-push`:
```bash
#!/bin/bash
# Prevent direct push to main

protected_branch='main'
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [ "$current_branch" = "$protected_branch" ]; then
    echo "🚫 Direct push to main is not allowed!"
    echo "Please use a feature branch and PR:"
    echo "  git checkout -b feature/your-feature"
    echo "  git push origin feature/your-feature"
    echo "  gh pr create"
    exit 1
fi
```

**Setup:**
```bash
chmod +x .git/hooks/pre-push
```

**Limitation:** Hooks are local only (not committed to repo)

---

## Option 3: GitHub Action (CI Enforcement)

**For automated checks:**

Create `.github/workflows/enforce-pr.yml`:
```yaml
name: Enforce PR Protocol
on:
  push:
    branches: [main]

jobs:
  check-pr:
    runs-on: ubuntu-latest
    steps:
      - name: Check if commit came via PR
        run: |
          if [ "${{ github.event_name }}" = "push" ] && [ -z "${{ github.event.pull_request }}" ]; then
            echo "❌ Direct commit to main detected!"
            echo "Please use Pull Requests"
            exit 1
          fi
```

**Limitation:** Runs after push (alerts but doesn't prevent)

---

## Comparison

| Method | Enforcement | Solo-Friendly | Setup Effort |
|--------|-------------|---------------|--------------|
| **Branch Protection** | ✅ Hard block | ✅ Yes (0 approvals) | Low (web UI) |
| **Git Hook** | ⚠️ Local only | ✅ Yes | Medium (manual) |
| **GitHub Action** | ⚠️ Post-push alert | ✅ Yes | Medium (YAML) |

---

## Recommended: Branch Protection + Git Hook

**Why both:**
1. **Branch Protection** = Final enforcement (can't bypass)
2. **Git Hook** = Early warning (fails before push attempt)

**Setup:**
```bash
# 1. Set up branch protection on GitHub (see above)

# 2. Create local pre-push hook
cat > .git/hooks/pre-push << 'EOF'
#!/bin/bash
protected_branch='main'
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [ "$current_branch" = "$protected_branch" ]; then
    echo "🚫 Direct push to main is not allowed!"
    echo ""
    echo "Please use a feature branch and PR workflow:"
    echo "  git checkout -b feature/descriptive-name"
    echo "  # make your changes"
    echo "  git commit -m 'description'"
    echo "  git push origin feature/descriptive-name"
    echo "  gh pr create"
    echo ""
    echo "See docs/ENFORCE_PR_PROTOCOL.md for details"
    exit 1
fi
EOF

chmod +x .git/hooks/pre-push

# 3. Test it
git checkout main
echo "test" > test.txt
git add test.txt
git commit -m "test direct commit"
git push  # Should fail with friendly message
git reset --hard HEAD~1  # Undo test
```

---

## For Solo Developers

**Branch Protection Settings for Solo Work:**
- ✅ Require pull request: YES
- ⚠️ Require approvals: **0** (you can self-merge)
- ✅ Include administrators: YES (enforce for yourself)
- ⚠️ Allow force pushes: NO
- ⚠️ Allow deletions: NO

**Workflow becomes:**
```bash
# Every time you want to work:
git checkout main
git pull
git checkout -b feature/brief-description

# Make changes, commit normally
git add .
git commit -m "Clear description"

# Push feature branch
git push origin feature/brief-description

# Create and merge PR (can be immediate for solo work)
gh pr create --fill
gh pr merge --squash --delete-branch

# Back to main
git checkout main
git pull
```

---

## Emergency Override

**If you absolutely need to bypass (rare):**

With branch protection, you can temporarily disable it:
1. GitHub settings → Branches → Edit rule
2. Uncheck "Include administrators"
3. Make emergency commit
4. Re-enable immediately

**But this defeats the purpose!** Better to use PR even for urgent fixes.

---

## Benefits of Enforcement

**Technical:**
- ✅ Impossible to accidentally commit to main
- ✅ All changes have PR history
- ✅ Can revert via PR if needed
- ✅ Clear audit trail

**Process:**
- ✅ Forces you to think in feature units
- ✅ Natural checkpoint before merging
- ✅ Better commit messages (PR descriptions)
- ✅ CI/CD can run on PRs

**Collaboration:**
- ✅ Ready for future collaborators
- ✅ Sets good example in public repos
- ✅ Professional git hygiene

---

## Recommended Action

1. **Now:** Set up GitHub branch protection
   - Go to repo settings → Branches
   - Protect `main` with PR requirement
   - Include administrators
   - Set approvals to 0 (solo work)

2. **Optional:** Add pre-push hook for early warning

3. **Verify:** Try to commit to main (should fail)

4. **Practice:** Use feature branch for next change

---

## Testing the Setup

```bash
# Should FAIL (good):
git checkout main
echo "test" >> README.md
git commit -am "test direct commit"
git push origin main
# Expected: Error about protected branch

# Should WORK (correct workflow):
git checkout -b test/pr-enforcement
echo "test" >> README.md
git commit -am "test via PR"
git push origin test/pr-enforcement
gh pr create --fill
gh pr merge --squash --delete-branch

# Clean up
git checkout main
git pull
```

---

**Bottom Line:** Branch protection + git hook = can't accidentally violate protocol!
