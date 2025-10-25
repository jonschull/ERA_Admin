# docs/GIT_COMMIT_GUIDELINES.md

# Git Commit Message Guidelines

## Problem

Long commit messages (>25 lines) cause `gh pr create` to hang indefinitely when using `--body` or `--fill` flags.

## Solution

### 1. Keep Commit Messages Short

**Good commit message format:**
```
feat: Brief one-line summary

Optional paragraph explaining what/why.
Keep total under 25 lines.

Details go in PR description or documentation.
```

**Bad (causes hangs):**
```
feat: Summary

## Long Section 1
- Bullet point 1
- Bullet point 2
...
[30+ lines of detail]
```

### 2. Use Web PR Creation for Complex Changes

```bash
# Always works, no CLI hangs:
git push origin branch-name
gh pr create --web  # Opens browser, avoids CLI prompts
```

### 3. Git Hook Protection

Installed at `.git/hooks/commit-msg` - automatically rejects commits >25 lines.

To bypass temporarily (not recommended):
```bash
git commit --no-verify -m "message"
```

## Best Practices

1. **Commit message**: Brief summary (1-5 lines)
2. **PR description**: Detailed changes, reasoning
3. **Documentation**: Complete context (README updates)

## Safe PR Creation Workflow

```bash
# 1. Commit with short message
git add files
git commit -m "feat: brief summary

Optional short explanation"

# 2. Push
git push origin branch-name

# 3. Create PR via web (NO CLI HANGS)
gh pr create --web

# 4. Edit PR description in browser with full details
```

## Why This Matters

- `gh pr create --body "long text"` → hangs indefinitely
- `gh pr create --fill` with long commit → hangs indefinitely  
- `gh pr create --web` → always works, uses browser

The git hook catches this **before** you push, saving time debugging hangs.

**Back to:** [docs/README.md](README.md) | [/README.md](../README.md)