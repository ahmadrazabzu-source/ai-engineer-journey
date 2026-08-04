# Day 1 Learning Log

## What I completed

* Verified Python, Git, VS Code and JupyterLab installations.
* Configured Git with my GitHub username and no-reply email.
* Created and activated a Python virtual environment (`.venv`).
* Installed pandas and JupyterLab inside the virtual environment.
* Created a local Git repository and initialized the `main` branch.
* Created a `requirements.txt` file using `pip freeze`.
* Created a `.gitignore` file to exclude unnecessary files such as `.venv`.
* Learned the purpose of `README.md` and project documentation.

## Commands I can explain

* `py -3.12 -m venv .venv`
* `.\.venv\Scripts\Activate.ps1`
* `python -m pip install -r requirements.txt`
* `python -m pip freeze > requirements.txt`
* `git init`
* `git branch -M main`
* `git status`
* `git config --global`
* `git add`
* `git commit`
* `git push`

## Problems encountered

### Problem 1: `py` command was not recognized

**Error**

```text
py : The term 'py' is not recognized...
```

### How I diagnosed it

* Ran `python --version` and confirmed Python was installed.
* Opened a new PowerShell window and checked `py --version` again.

### How I fixed it

Restarted PowerShell. The Python Launcher (`py`) became available, and I verified it using:

```powershell
py --version
```

---

### Problem 2: Git command was not recognized

**Error**

```text
git : The term 'git' is not recognized...
```

### How I diagnosed it

Ran:

```powershell
where.exe git
```

It showed Git was installed at:

```text
C:\Program Files\Git\cmd\git.exe
```

which indicated a PATH issue.

### How I fixed it

Restarted PowerShell so the updated PATH was loaded. Then verified with:

```powershell
git --version
```

---

### Problem 3: `.venv` was appearing in `git status`

### How I diagnosed it

After running:

```powershell
git status
```

Git listed `.venv/` as an untracked folder.

### How I fixed it

Created a `.gitignore` file and added:

```text
.venv/
```

After running `git status` again, `.venv` no longer appeared.

---

### Problem 4: Understanding Git concepts

I was initially confused about:

* Difference between Git and GitHub
* Purpose of `git init`
* Meaning of the `main` branch
* Why virtual environments are ignored by Git

### How I fixed it

Read the documentation, practiced the commands, and understood the concepts through real examples and analogies.