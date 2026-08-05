AI Engineer Journey

A hands-on learning repository documenting my preparation for an Associate AI Engineer role, with emphasis on Python, machine learning, healthcare data, PyTorch, SQL, Git and n8n automation.
Current status

Day 1 completed: development environment, virtual environment, Git repository and first synthetic-data Python script.
Environment

    Windows
    Python 3.12
    Visual Studio Code
    Git
    JupyterLab

-------------------------------------------------------------------------------------------------------------------------------------------------------------

## Day 1 — Environment Setup & First Data Script

Establishes the Python development environment, configures virtual environment isolation, installs project dependencies, and verifies toolchain setup with an initial data script.

### Quick Start (Day 1)

#### Windows (PowerShell)
```powershell
# 1. Clone repository & enter directory
git clone REPOSITORY_URL
cd ai-engineer-journey

# 2. Create and activate virtual environment
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Upgrade pip and install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 4. Run Day 1 verification script
python src/hello_data.py


-------------------------------------------------------------------------------------------------------------------------------------------------------------

## Day 2 — Python Fundamentals & Input Validation

Demonstrates string cleaning, range validation, conditional classification, function refactoring, and interactive while loops using synthetic healthcare data.

### Quick Start (Day 2)

#### Windows (PowerShell)
```powershell
# 1. Clone repository & enter directory (if not already done)
git clone REPOSITORY_URL
cd ai-engineer-journey

# 2. Create and activate virtual environment
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Upgrade pip and install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 4. Run Day 2 exercises
python exercises/day02.py

