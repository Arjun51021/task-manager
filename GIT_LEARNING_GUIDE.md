# Git & GitHub Hands-On Learning Guide
## Using the Task Manager Django Project

---

## SETUP (Do This First)

### Step 1: Create a GitHub Repo
1. Go to github.com → Click **New** repository
2. Name it `task-manager` — keep it **empty** (no README, no .gitignore)

### Step 2: Clone to TWO Folders (simulating 2 developers)
```bash
# Developer A (you as "Dev A")
git clone https://github.com/YOUR_USERNAME/task-manager.git dev-a-task-manager
cd dev-a-task-manager

# Copy all project files into this folder, then:
git add .
git commit -m "Initial commit: Django task manager app"
git push origin main

cd ..

# Developer B (you as "Dev B" — simulating a teammate)
git clone https://github.com/YOUR_USERNAME/task-manager.git dev-b-task-manager
```

Now you have 2 folders pointing to the same remote repo. You'll switch between them to simulate 2 people.

---

## EXERCISE 1: Basic Push & Pull (No Conflicts)

**Goal:** Understand push, pull, and staying in sync.

### As Dev A:
```bash
cd dev-a-task-manager

# Edit views.py — change the page title
# In task_list.html, change <h1>Task Manager</h1> to <h1>Task Manager v2</h1>

git add .
git commit -m "Update page title to v2"
git push origin main
```

### As Dev B:
```bash
cd ../dev-b-task-manager

# Try editing something and pushing WITHOUT pulling first
# Edit requirements.txt — add a comment at the bottom: # added by dev b
git add .
git commit -m "Update requirements"
git push origin main   # ← THIS WILL FAIL! (remote has new commits)

# Fix it:
git pull origin main   # pulls Dev A's changes first
git push origin main   # now it works
```

**What you learned:** Always `git pull` before `git push` when others are working.

---

## EXERCISE 2: Branching & Merging (Clean Merge)

**Goal:** Learn feature branches and merging without conflicts.

### As Dev A — Add a "delete task" feature:
```bash
cd dev-a-task-manager
git pull origin main

git checkout -b feature/delete-task
```

Edit `tasks/views.py` — add at the bottom:
```python
def delete_task(request, task_id):
    Task.objects.filter(id=task_id).delete()
    return redirect("task_list")
```

Edit `taskapp/urls.py` — add:
```python
path("delete/<int:task_id>/", views.delete_task, name="delete_task"),
```

```bash
git add .
git commit -m "Add delete task feature"
git push origin feature/delete-task
```

### On GitHub:
1. Go to your repo → you'll see "Compare & pull request"
2. Create a Pull Request (PR)
3. Review the changes → Merge it

### As Dev B — Pull the merged changes:
```bash
cd ../dev-b-task-manager
git pull origin main
# You now have the delete feature!
```

**What you learned:** Feature branches isolate work. PRs let you review before merging.

---

## EXERCISE 3: Merge Conflict! (The Important One)

**Goal:** Both devs edit the SAME line → conflict → resolve it.

### As Dev A:
```bash
cd dev-a-task-manager
git pull origin main
git checkout -b feature/style-update
```

Edit `tasks/templates/tasks/task_list.html` — change the `<h1>` line to:
```html
<h1 style="color: blue;">Task Manager - Dev A Style</h1>
```

```bash
git add .
git commit -m "Dev A: blue heading"
git push origin feature/style-update
```

### As Dev B (before merging Dev A's PR):
```bash
cd ../dev-b-task-manager
git pull origin main
git checkout -b feature/new-heading
```

Edit the SAME `<h1>` line in `task_list.html` to:
```html
<h1 style="color: red;">Task Manager - Dev B Style</h1>
```

```bash
git add .
git commit -m "Dev B: red heading"
git push origin feature/new-heading
```

### Now merge both on GitHub:
1. Merge Dev A's PR first (will merge cleanly)
2. Try to merge Dev B's PR → **CONFLICT!**

### Resolve the conflict (as Dev B):
```bash
cd ../dev-b-task-manager
git checkout feature/new-heading
git pull origin main   # brings in Dev A's merged changes

# Git will say: CONFLICT in tasks/templates/tasks/task_list.html
# Open the file — you'll see:
# <<<<<<< HEAD
# <h1 style="color: red;">Task Manager - Dev B Style</h1>
# =======
# <h1 style="color: blue;">Task Manager - Dev A Style</h1>
# >>>>>>> main
```

**Fix it** — pick one, or combine both:
```html
<h1 style="color: purple;">Task Manager - Combined Style</h1>
```

Remove the `<<<<<<<`, `=======`, `>>>>>>>` markers completely, then:
```bash
git add .
git commit -m "Resolve merge conflict: combined heading styles"
git push origin feature/new-heading
```

Now the PR on GitHub will merge cleanly!

**What you learned:** Conflicts happen when 2 people edit the same line. You resolve them manually.

---

## EXERCISE 4: Rebase vs Merge

**Goal:** Understand `git rebase` as an alternative to merge.

### As Dev A:
```bash
cd dev-a-task-manager
git checkout main && git pull

git checkout -b feature/priority-field
```

Edit `tasks/models.py` — add a field:
```python
priority = models.CharField(max_length=10, choices=[("low","Low"),("med","Medium"),("high","High")], default="med")
```

```bash
git add .
git commit -m "Add priority field to Task model"
```

Meanwhile, suppose `main` got updated (Dev B pushed something). Before merging:
```bash
# Instead of merge, use rebase to keep history clean:
git fetch origin
git rebase origin/main

# If conflicts occur, fix them, then:
# git add .
# git rebase --continue

git push origin feature/priority-field
```

**What you learned:** `rebase` replays your commits on top of the latest main. Cleaner history than merge commits.

---

## EXERCISE 5: Useful Commands Cheat Sheet

Practice each of these during your exercises:

```bash
# See what's changed
git status
git diff
git diff --staged

# See commit history
git log --oneline --graph --all

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git checkout -- .

# Stash changes temporarily
git stash
git stash pop

# See all branches
git branch -a

# Delete a branch
git branch -d feature/old-branch
git push origin --delete feature/old-branch

# See who changed what
git blame tasks/views.py

# Cherry-pick a specific commit
git cherry-pick <commit-hash>

# See remote info
git remote -v
```

---

## EXERCISE 6: .gitignore & Sensitive Files

Already included in the project. Try this:

```bash
# Create a fake secret file
echo "PASSWORD=abc123" > .env

git status   # .env should NOT appear (it's in .gitignore)

# What if you accidentally committed a secret?
# Remove it from tracking (file stays on disk):
git rm --cached .env
git commit -m "Remove .env from tracking"
```

---

## RECOMMENDED ORDER

1. Exercise 1 → Push & Pull basics
2. Exercise 2 → Branching & clean merge
3. Exercise 3 → **Merge conflicts** (most important!)
4. Exercise 4 → Rebase
5. Exercise 5 → Practice commands during all exercises
6. Exercise 6 → Gitignore

After completing all exercises, you'll be confident with real-world Git collaboration!
