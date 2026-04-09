# Global Grant Intelligence Platform — Git Workflow

**Branch Strategy | Commit Standards | Merge Process**

---

## 1. Branch Strategy

### Main Branch
- **`main`** — Production-ready code only
- Protected branch — no direct commits
- Only Marina merges to `main`
- Always deployable

### Personal Branches
Each team member works in their own branch:

| Team Member | Branch Naming | Purpose |
|-------------|---------------|---------|
| Arvin | `arvin/backend-mvp` | Backend development |
| Nazar | `nazar/frontend-mvp` | Frontend development |
| Marina | `marina/intelligence-and-coordination` | Intelligence + coordination |
| Marina | `marina/project-structure` | Initial setup (Day 1 only) |

### Creating Your Branch

```bash
# Start from main
git checkout main
git pull origin main

# Create your branch
git checkout -b <your-branch-name>

# Example:
git checkout -b arvin/backend-mvp
```

---

## 2. Day 1: Project Kickoff (Marina Creates Structure)

**IMPORTANT:** This section applies only to Day 1. Marina must complete this before Arvin and Nazar begin work.

### Step 1: Marina Creates and Merges Structure

Marina creates the project foundation and merges it to `main` first:

```bash
# Create structure branch
git checkout -b marina/project-structure

# ... create all initial files (directories, docs, workflow) ...

# Commit and push
git add .
git commit -m "Initial project structure and documentation"
git push origin marina/project-structure

# Merge to main
git checkout main
git merge marina/project-structure
git push origin main
```

**Only after this is complete** should Arvin and Nazar proceed to Step 2.

### Step 2: Arvin and Nazar Create Branches FROM main

Arvin and Nazar must create their branches **after** Marina's structure is in `main`:

```bash
# Arvin's commands
git checkout main
git pull origin main                    # Get Marina's structure
git checkout -b arvin/backend-mvp       # Create from updated main
git push -u origin arvin/backend-mvp

# Nazar's commands  
git checkout main
git pull origin main                    # Get Marina's structure
git checkout -b nazar/frontend-mvp      # Create from updated main
git push -u origin nazar/frontend-mvp
```

### Why This Order Matters

- Arvin and Nazar need the directory structure Marina creates
- They need `MASTER-PROMPT.md` for the data structure
- They need `WORKFLOW.md` for Git protocols
- Creating branches before Marina merges means they'll be missing dependencies

---

## 4. Daily Workflow

### Start of Day (Every Day)

```bash
# 1. Switch to main and get latest
git checkout main
git pull origin main

# 2. Switch to your branch
git checkout <your-branch-name>

# 3. Bring in any changes from main
git rebase main

# If conflicts occur, resolve them:
# 1. Edit conflicted files
# 2. git add <file>
# 3. git rebase --continue
```

### During Work

```bash
# See what files changed
git status

# Stage files for commit
git add <file>           # Add specific file
git add .                # Add all changed files

# Commit with descriptive message
git commit -m "Your commit message here"

# Push to remote
git push origin <your-branch-name>
```

### End of Day (Every Day)

```bash
# Push all commits
git push origin <your-branch-name>

# Verify push succeeded
git log --oneline --graph --all
```

---

## 5. Commit Standards

### When to Commit
- **After completing each discrete task**
- **Before stopping work for the day**
- **Before switching to a different task**

### Commit Message Format

```
<type>: <short description>

[optional longer description]
```

### Types

| Type | Use When |
|------|----------|
| `feat` | Adding new functionality |
| `fix` | Fixing a bug |
| `docs` | Documentation changes |
| `refactor` | Code restructuring without feature change |
| `test` | Adding tests |
| `chore` | Maintenance, setup, dependencies |

### Good Commit Messages

```bash
git commit -m "feat: add GET /grants endpoint with mock data"
git commit -m "fix: resolve CORS issue for frontend access"
git commit -m "docs: add API usage examples to backend README"
git commit -m "feat: implement topic detection with keyword matching"
git commit -m "refactor: extract scoring logic into separate module"
git commit -m "chore: add requirements.txt with dependencies"
```

### Bad Commit Messages

```bash
git commit -m "stuff"                          # Too vague
git commit -m "updates"                        # No information
git commit -m "fixed stuff and added things"   # Multiple changes, unclear
git commit -m "WIP"                            # Work-in-progress, incomplete
```

### Multi-Line Commit (When Needed)

```bash
git commit -m "feat: add opportunity scoring engine" -m "- Base score of 50 points" -m "- Add/subtract based on funding amount and deadline" -m "- Clamp final score to 0-100 range"
```

---

## 6. Regular Pushes

### Push Frequency
- **At least once per day**
- **After completing a task**
- **Before asking for help or review**

### Why Regular Pushes Matter
- Backup your work
- Allow team visibility into progress
- Enable code review
- Prevent data loss

### Push Commands

```bash
# Normal push
git push origin <your-branch-name>

# If remote branch doesn't exist yet
git push -u origin <your-branch-name>

# Force push (use with caution — only on your own branch)
git push --force-with-lease origin <your-branch-name>
```

---

## 7. No Work in Main Branch

### This Rule is Absolute

**Never do this:**
```bash
git checkout main
git add .
git commit -m "quick fix"
git push origin main
```

**Always do this instead:**
```bash
git checkout main
git pull origin main
git checkout -b <your-branch>/quick-fix
git add .
git commit -m "fix: correct typo in documentation"
git push origin <your-branch>/quick-fix
# Then ask Marina to merge
```

### If You Accidentally Commit to Main

```bash
# Don't panic — this can be fixed

# 1. Create a new branch from main (saves your work)
git checkout -b recovery-branch

# 2. Switch back to main
git checkout main

# 3. Reset main to previous commit (WARNING: coordinate with team)
git log --oneline          # Find the last good commit
git reset --hard <commit-hash>

# 4. Push the reset main (requires force — Marina must do this)
git push --force origin main

# 5. Continue working in your recovery-branch
```

---

## 8. Marina Coordinates Final Merge

### Merge Process

1. **Team members complete their work**
   - All tasks finished
   - All tests passing
   - Code reviewed (informally)

2. **Team members push their branches**
   ```bash
   git push origin <your-branch-name>
   ```

3. **Marina reviews all branches**
   - Code quality check
   - Verify acceptance criteria
   - Confirm no direct main commits

4. **Marina merges to main**
   ```bash
   git checkout main
   git pull origin main
   
   # Merge each branch in order
   git merge arvin/backend-mvp
   git merge nazar/frontend-mvp
   git merge marina/intelligence-and-coordination
   
   # Push to remote
   git push origin main
   ```

5. **Handle merge conflicts if they occur**
   ```bash
   # If conflict occurs during merge:
   # 1. Git will show conflicted files
   # 2. Edit files to resolve conflicts
   # 3. git add <resolved-files>
   # 4. git commit (no message needed)
   ```

6. **Tag the release**
   ```bash
   git tag -a v0.1-mvp -m "MVP Release 0.1"
   git push origin v0.1-mvp
   ```

### Merge Order Recommendation

```
main (base)
  ↓
arvin/backend-mvp → main
  ↓
nazar/frontend-mvp → main
  ↓
marina/intelligence-and-coordination → main
  ↓
tag v0.1-mvp
```

---

## 9. Conflict Resolution

### When Conflicts Happen

Conflicts occur when the same file is modified in two branches. Git will show:

```
Auto-merging filename.txt
CONFLICT (content): Merge conflict in filename.txt
Automatic merge failed; fix conflicts and commit the result.
```

### How to Resolve

1. **Find conflicted files**
   ```bash
   git status
   ```

2. **Open conflicted file** — you'll see:
   ```
   <<<<<<< HEAD
   Content from current branch
   =======
   Content from branch being merged
   >>>>>>> branch-name
   ```

3. **Edit the file** — keep the correct content, remove markers:
   ```
   Content from current branch
   Content from branch being merged
   ```
   Or choose one side:
   ```
   Content from branch being merged
   ```

4. **Mark as resolved**
   ```bash
   git add <filename>
   ```

5. **Complete the merge**
   ```bash
   git commit  # No message needed — Git provides default
   ```

### Prevention

- **Pull main frequently** and rebase your branch
- **Communicate** when working on shared files
- **Make small, focused changes** rather than large refactors
- **Don't modify other team members' files** without coordination

---

## 10. Communication Guidelines

### Daily Check-in (Text/Slack/Discord)

Each team member posts:

```
**Yesterday:** Completed Task 4 (API client)
**Today:** Working on Task 5 (dynamic rendering)
**Blockers:** Waiting for backend CORS config from Arvin
**Branch:** nazar/frontend-mvp
```

### When to Speak Up

- **Stuck for >30 minutes** — Ask for help
- **Found a bug in someone else's code** — Notify them politely
- **Need to modify a shared file** — Coordinate with owner
- **Discovered a better approach** — Share with the team
- **Falling behind schedule** — Tell Marina ASAP

### Code Review Requests

```
Hey @Arvin, could you review my latest commits in nazar/frontend-mvp?
Specifically the API client in js/app.js — want to make sure I'm handling
errors correctly before I move on.
```

---

## 11. Quick Reference

### Essential Commands

```bash
# Check status
git status

# See commit history
git log --oneline --graph --all

# Switch branch
git checkout <branch-name>

# Create and switch to new branch
git checkout -b <new-branch-name>

# Get latest from main
git checkout main
git pull origin main

# Update your branch with main
git checkout <your-branch>
git rebase main

# See what changed in a file
git diff <filename>

# Undo uncommitted changes
git checkout -- <filename>

# Undo last commit (keep changes)
git reset --soft HEAD~1

# See branches
git branch -a
```

### File Locations

```
backend/        → Arvin's code
frontend/       → Nazar's code
intelligence/   → Marina's code
docs/           → Documentation (all)
admin/          → Project management (Marina)
```

### Who to Ask

| Topic | Ask |
|-------|-----|
| Git workflow | Marina |
| Backend/API | Arvin |
| Frontend/UI | Nazar |
| Intelligence/scoring | Marina |
| Data structure | Marina |
| Merge conflicts | Marina |
| Project priorities | Marina |

---

## 12. Rules Summary

### The Golden Rules

1. **✅ DO** work in your own branch
2. **❌ DON'T** commit to `main`
3. **✅ DO** commit after each task
4. **✅ DO** write clear commit messages
5. **✅ DO** push at least once per day
6. **✅ DO** pull main and rebase daily
7. **✅ DO** communicate blockers immediately
8. **❌ DON'T** modify other members' files without asking
9. **✅ DO** follow the shared data structure exactly
10. **✅ DO** ask for help when stuck

### Branch Checklist

Before starting work:
- [ ] I'm in my branch, not main
- [ ] My branch is up to date with main
- [ ] I know which task I'm working on

After completing work:
- [ ] I've committed with a clear message
- [ ] I've pushed to remote
- [ ] I've updated the team on progress

---

*Workflow Version: 1.0*  
*Enforced by: Marina*  
*Questions: Ask Marina*
