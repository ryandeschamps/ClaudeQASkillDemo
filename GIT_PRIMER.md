# Git Primer - Essential Concepts and Commands

A practical guide to Git version control, focusing on the workflows and commands you'll use most often.

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Basic Workflow](#basic-workflow)
3. [Branching](#branching)
4. [Remote Repositories](#remote-repositories)
5. [Common Commands Reference](#common-commands-reference)
6. [Best Practices](#best-practices)
7. [Real-World Scenarios](#real-world-scenarios)

---

## Core Concepts

### What is Git?
Git is a **version control system** that tracks changes to your files over time. Think of it as a sophisticated "save game" system for your code.

### Key Terms

**Repository (Repo)**: A folder containing your project and its complete history
- **Local repo**: On your computer
- **Remote repo**: On a server (like GitHub)

**Commit**: A snapshot of your project at a specific point in time
- Like a save point in a video game
- Contains: changes made, author, timestamp, message

**Branch**: A parallel version of your code
- `main` (or `master`): The primary/production branch
- Feature branches: For developing new features

**Working Directory**: The files you're currently editing

**Staging Area (Index)**: A preparation area for commits
- You choose which changes to include in the next commit

**HEAD**: A pointer to your current position (branch + commit)

---

## Basic Workflow

### The Three States of Files

```
Working Directory → Staging Area → Repository
    (edit)           (git add)      (git commit)
```

### Example Workflow

```bash
# 1. Check current status
git status

# 2. Make changes to files
# (edit files in your editor)

# 3. Stage changes
git add file1.txt file2.py          # Stage specific files
git add .                            # Stage all changes
git add folder/                      # Stage entire folder

# 4. Review what's staged
git status
git diff --staged                    # See exactly what will be committed

# 5. Commit changes
git commit -m "Add user authentication feature"

# 6. Push to remote repository
git push origin main
```

---

## Branching

### Why Use Branches?
- Isolate work on new features
- Experiment without affecting main code
- Enable parallel development
- Review changes before merging

### Branch Commands

```bash
# List branches
git branch                           # Local branches
git branch -r                        # Remote branches
git branch -a                        # All branches

# Create and switch to new branch
git checkout -b feature-name         # Old way
git switch -c feature-name           # New way (Git 2.23+)

# Switch between branches
git checkout main                    # Old way
git switch main                      # New way

# Delete local branch
git branch -d feature-name           # Safe delete (only if merged)
git branch -D feature-name           # Force delete (use with caution)

# Delete remote branch
git push --delete origin feature-name
```

### Branch Naming Conventions

```
feature/add-login                    # New feature
bugfix/fix-navbar-overlap            # Bug fix
hotfix/security-patch                # Urgent fix for production
refactor/restructure-database        # Code refactoring
docs/update-readme                   # Documentation
```

---

## Remote Repositories

### Understanding Remotes

A **remote** is a version of your repository hosted on the internet (e.g., GitHub).

```bash
# View configured remotes
git remote -v

# Output example:
# origin  https://github.com/username/repo.git (fetch)
# origin  https://github.com/username/repo.git (push)
```

### Common Remote Operations

```bash
# Fetch changes from remote (doesn't merge)
git fetch origin

# Pull changes from remote (fetch + merge)
git pull origin main

# Push changes to remote
git push origin main
git push origin feature-branch

# Push and set upstream tracking
git push -u origin feature-branch    # First time
git push                             # Subsequent pushes

# Delete remote branch
git push --delete origin branch-name
```

---

## Common Commands Reference

### Checking Status and History

```bash
# Current status
git status                           # Full status
git status -s                        # Short format

# Commit history
git log                              # Full log
git log --oneline                    # Compact view
git log --oneline -5                 # Last 5 commits
git log --graph --oneline --all      # Visual branch graph

# Show changes
git diff                             # Unstaged changes
git diff --staged                    # Staged changes
git diff HEAD~1                      # Compare with previous commit
git diff main..feature-branch        # Compare branches
```

### Undoing Changes

```bash
# Unstage file (keep changes)
git restore --staged file.txt        # New way
git reset HEAD file.txt              # Old way

# Discard changes in working directory
git restore file.txt                 # New way (DESTRUCTIVE!)
git checkout -- file.txt             # Old way (DESTRUCTIVE!)

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) - DESTRUCTIVE!
git reset --hard HEAD~1

# Revert a commit (creates new commit)
git revert <commit-hash>             # Safer for shared branches
```

### Merging

```bash
# Merge branch into current branch
git merge feature-branch

# Merge without fast-forward (preserves branch history)
git merge --no-ff feature-branch

# Abort merge if conflicts
git merge --abort

# During conflict resolution
# 1. Edit files to resolve conflicts
# 2. git add resolved-files
# 3. git commit
```

---

## Best Practices

### Commit Messages

**Format:**
```
<type>: <short summary> (50 chars or less)

<optional detailed description>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code restructuring (no functionality change)
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Good Examples:**
```
feat: Add user authentication with OAuth2
fix: Resolve navbar overlap on mobile devices
docs: Update installation instructions for Windows
refactor: Extract validation logic into separate module
```

**Bad Examples:**
```
"fixed stuff"                        # Too vague
"Updated files"                      # Not descriptive
"asdfasdf"                          # Meaningless
```

### When to Commit

✅ **Do commit when:**
- Completing a logical unit of work
- Finishing a feature or fix
- Before switching tasks
- Before experimenting with risky changes

❌ **Don't commit:**
- Half-finished work (unless on feature branch)
- Code that doesn't compile/run
- Sensitive data (passwords, API keys)

### Branching Strategy

**Feature Branch Workflow:**
```
main (production)
  ↓
  └─→ feature-branch (development)
        ↓
        (work, commit, push)
        ↓
        merge back to main when complete
        ↓
        delete feature-branch
```

---

## Real-World Scenarios

### Scenario 1: Starting New Feature

```bash
# 1. Ensure main is up to date
git switch main
git pull origin main

# 2. Create feature branch
git switch -c feature/add-payment-gateway

# 3. Work and commit
# (edit files)
git add .
git commit -m "feat: Add PayPal integration"

# 4. Push feature branch
git push -u origin feature/add-payment-gateway

# 5. Create Pull Request on GitHub (via web interface)

# 6. After approval and merge, cleanup
git switch main
git pull origin main
git branch -d feature/add-payment-gateway
git push --delete origin feature/add-payment-gateway
```

### Scenario 2: Fixing Urgent Bug

```bash
# 1. Create hotfix branch from main
git switch main
git pull origin main
git switch -c hotfix/security-patch

# 2. Fix bug and commit
# (edit files)
git add .
git commit -m "fix: Patch SQL injection vulnerability"

# 3. Push and merge immediately
git push -u origin hotfix/security-patch
# (merge via GitHub Pull Request or directly)
git switch main
git merge --no-ff hotfix/security-patch
git push origin main

# 4. Cleanup
git branch -d hotfix/security-patch
git push --delete origin hotfix/security-patch
```

### Scenario 3: Syncing with Team Changes

```bash
# Daily workflow - stay in sync
git switch main
git pull origin main               # Get latest changes

git switch feature-branch
git merge main                     # Incorporate team changes
# OR
git rebase main                    # Alternative (rewrites history)

# Resolve conflicts if any, then continue working
```

### Scenario 4: Reviewing Changes Before Commit

```bash
# See what you've changed
git status                         # Overview
git diff                           # Detailed changes

# Stage selectively
git add specific-file.py           # Only files you want

# Review staged changes
git diff --staged

# Commit
git commit -m "feat: Add user profile editing"
```

### Scenario 5: Oops, I Committed to the Wrong Branch

```bash
# You committed to main instead of feature branch
git log --oneline -1               # Note the commit hash

# Undo commit on main (keep changes)
git reset --soft HEAD~1

# Create/switch to correct branch
git switch -c feature/correct-branch

# Commit again
git add .
git commit -m "feat: Add feature on correct branch"
```

---

## Quick Reference Cheat Sheet

### Most Used Commands

```bash
# Status & Info
git status                         # Check status
git log --oneline -5               # Recent commits
git diff                           # See changes

# Branching
git switch -c new-branch           # Create and switch
git switch main                    # Switch branch
git branch -d old-branch           # Delete local branch

# Staging & Committing
git add .                          # Stage all
git commit -m "message"            # Commit with message

# Remote Operations
git pull origin main               # Get updates
git push origin main               # Send updates
git push --delete origin branch    # Delete remote branch

# Merging
git merge feature-branch           # Merge into current branch
git merge --no-ff feature-branch   # Preserve branch history
```

### Emergency Commands

```bash
# I messed up - go back!
git restore file.txt               # Discard file changes
git restore --staged file.txt      # Unstage file
git reset --soft HEAD~1            # Undo last commit (keep changes)
git merge --abort                  # Abort merge

# I need to see what's different
git diff                           # Working vs staged
git diff --staged                  # Staged vs last commit
git diff main..feature             # Compare branches
```

---

## Understanding What We Did in Your Session

### Our Workflow

1. **Added progress bars** to `combinatorial.py`
   ```bash
   git add skill/scripts/combinatorial.py
   git commit -m "Add progress bars to combinatorial.py"
   git push origin main
   ```

2. **Reviewed all remote branches**
   ```bash
   git branch -r                   # Listed remote branches
   git log origin/branch-name      # Checked commit history
   ```

3. **Cleaned up old branches**
   ```bash
   git push --delete origin branch-name-1 branch-name-2 ...
   # Deleted 10 old branches
   ```

4. **Merged refactor branch**
   ```bash
   git merge origin/claude/refactor-skill-variants-structure-01DMffVxaTgvRjCV6wDCrvc6
   git push origin main
   git push --delete origin claude/refactor-skill-variants-structure-01DMffVxaTgvRjCV6wDCrvc6
   ```

### Why We Deleted Branches

- **After merging**: Branch changes are preserved in main
- **Keeps repository clean**: Easier to see active work
- **Still recoverable**: Git history retains everything
- **Best practice**: Delete branches after successful merge

---

## Tips for Success

1. **Commit often**: Small, focused commits are better than large ones
2. **Write clear messages**: Your future self will thank you
3. **Pull before push**: Avoid conflicts by staying current
4. **Review before commit**: Use `git diff` and `git status`
5. **Use branches**: Keep main stable, experiment on branches
6. **Don't panic**: Most Git operations can be undone
7. **Ask for help**: `git help <command>` or Google the error

---

## Additional Resources

- [Official Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Git Cheat Sheet (PDF)](https://education.github.com/git-cheat-sheet-education.pdf)
- [Learn Git Branching (Interactive)](https://learngitbranching.js.org/)
- [Oh Shit, Git!?!](https://ohshitgit.com/) - Fixing common mistakes

---

## Getting Help

```bash
# Built-in help
git help                           # General help
git help commit                    # Help for specific command
git commit --help                  # Same as above

# Check Git version
git --version
```

**Remember**: Git has a learning curve, but once you understand the concepts, it becomes an invaluable tool. Don't be afraid to experiment on a test branch!
