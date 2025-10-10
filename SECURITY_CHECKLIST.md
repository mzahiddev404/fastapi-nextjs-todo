# Security Checklist

## Before Committing to GitHub

### ✅ Check for Sensitive Data
- [ ] No `.env` files in commit
- [ ] No hardcoded passwords or API keys
- [ ] No database connection strings with credentials
- [ ] No JWT secrets or private keys
- [ ] No personal information or emails

### ✅ Documentation Safety
- [ ] Use placeholder values in examples
- [ ] Replace real credentials with `username:password@cluster.mongodb.net`
- [ ] Use generic example URLs and endpoints
- [ ] Remove any real API keys or tokens from examples

### ✅ File Exclusions
- [ ] `.env*` files are in `.gitignore`
- [ ] `Codebase Design Evaluation.txt` is excluded
- [ ] Any files with `*secret*`, `*password*`, `*credential*` are excluded
- [ ] Internal documentation files are excluded

## Quick Commands

```bash
# Check for sensitive data before committing
grep -r "password\|secret\|key\|credential" . --exclude-dir=.git --exclude="*.pyc" --exclude=".env*"

# Check what will be committed
git status --porcelain

# Review staged changes
git diff --cached
```

## Emergency Response

If sensitive data is accidentally committed:
1. Remove the sensitive data from files
2. Commit the fix immediately
3. Consider rotating any exposed credentials
4. Check GitHub security alerts
5. Update `.gitignore` to prevent future issues
