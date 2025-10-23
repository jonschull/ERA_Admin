# PR Checklist

Quick reference for creating pull requests in ERA_Admin.

## Before You Start

```bash
# Create feature branch from main
git checkout main
git pull
git checkout -b feature/brief-description
```

## During Development

- Edit files normally
- Commit to your feature branch
- **If you edit NAVIGATION_WIREFRAME.md:** Run `./docs/update_docs.sh` to regenerate

## Before Push

The pre-push hook automatically checks:
- ✓ Not on main branch
- ✓ Docs in sync (if wireframe edited, production docs regenerated)
- ✓ Navigation integrity passes

## Create PR

```bash
git push origin feature/your-branch
gh pr create
```

GitHub will show a checklist in the PR description.

## After Merge

```bash
git checkout main
git pull
git branch -d feature/your-branch  # cleanup
```

## When Blocked

**"Can't commit to main"**
→ You're on main. Create feature branch: `git checkout -b feature/name`

**"Docs out of sync"**
→ Run `./docs/update_docs.sh` to regenerate from wireframe

**"Navigation test failed"**
→ Run `python3 docs/test_navigation.py` for details

**"Pre-push hook not installed"**
→ See WORKING_PRINCIPLES.md "Enforcement: Branch Protection"

---

📖 **Full details:** [WORKING_PRINCIPLES.md](../WORKING_PRINCIPLES.md)  
🏗️ **Architecture:** [README.md](../README.md)  
🔄 **Current state:** [CONTEXT_RECOVERY.md](../CONTEXT_RECOVERY.md)
