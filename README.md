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

---------------------------------------------------------------------------------------------------------------------

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


---------------------------------------------------------------------------------------------------------------------

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

---------------------------------------------------------------------------------------------------------------------

## Day 3: Data structures and lookup complexity

I built a synthetic healthcare-record summarizer using Python lists, tuples,
dictionaries, sets, a list-based stack and `collections.deque`.

### Structure choices

- A list stores the ordered collection of synthetic records.
- Each record is represented by a dictionary.
- A tuple stores the fixed required-field names.
- A set tracks unique and duplicate record IDs.
- A list demonstrates LIFO stack behavior.
- A deque demonstrates FIFO queue behavior.
- A dictionary index supports direct lookup by record ID.

### Lookup experiment

Dataset size: 10,000 synthetic records

| Target | List lookup | Dictionary lookup |
|---|---:|---:|
| First record | 0.000012 s | 0.000025 s |
| Last record | 0.098431 s | 0.000026 s |
| Missing record | 0.097812 s | 0.000026 s |

A list search is O(n) because it may inspect records sequentially. A dictionary
lookup is O(1) on average because the record ID is used as a hash-based key.

The measured values are specific to my computer and experiment. They illustrate
the expected behavior but do not independently prove the theoretical complexity.

### Privacy and limitations

All records are synthetic. The program contains no real patient identifiers and
must not be used for clinical decisions.

---------------------------------------------------------------------------------------------------------------------

## Day 4: Robust CSV ingestion

I built a deterministic CSV intake validator using Python's standard library.

Loader behavior'''

The loader:

- Reads rows using `csv.DictReader`.
- Validates required column names.
- Cleans and validates individual fields.
- Separates valid and rejected rows.
- Records CSV line numbers and rejection reasons.
- Writes a structured JSON ingestion report.
- Uses logging for operational and failure information.
- Returns different status codes for different failure types.

### Validation result

Input file: `data/day04/mixed_records.csv`

- Total rows: 6
- Valid rows: 2
- Rejected rows: 4

### Failure tests

1. Missing input file
2. Missing required `department` column

Both failures are detected explicitly and do not produce misleading successful
results.

### Privacy and limitations

All records are synthetic. The loader is an educational portfolio project and
has not been validated for real clinical or production data.

---------------------------------------------------------------------------------------------------------------------
## Day 5 — NumPy, pandas and healthcare EDA

I analyzed the public UCI Heart Failure Clinical Records dataset using NumPy
and pandas.

### Workflow

1. Preserved the original raw CSV.
2. Inspected dataset dimensions, column names and data types.
3. Audited missing values.
4. Audited duplicate rows.
5. Checked categorical/binary values.
6. Standardized column naming in a copied DataFrame.
7. Used NumPy for numerical summaries.
8. Used pandas `describe()` for descriptive statistics.
9. Used `groupby()` for category-level summaries.
10. Used `merge()` to combine numerical summaries with a feature dictionary.
11. Exported a cleaned CSV.
12. Re-read the exported file to verify reproducibility.
13. Exported a machine-readable cleaned schema.

### Data source

Heart Failure Clinical Records — UCI Machine Learning Repository  
DOI: 10.24432/C5Z89R  
License: CC BY 4.0

### Limitations

The work is descriptive and educational. No clinical conclusions or causal
claims are made, and no predictive model is trained on Day 5.

---------------------------------------------------------------------------------------------------------------------

## Day 6 — SQL Analytics with SQLite

I loaded the cleaned Day 5 healthcare dataset into an SQLite relational
database and answered ten analytical questions using SQL.

### SQL concepts demonstrated

- SELECT
- WHERE
- AND
- ORDER BY
- LIMIT
- COUNT
- AVG
- GROUP BY
- aliases
- INNER JOIN
- subqueries

### Database design

The SQLite database contains:

- `heart_failure_records` — cleaned analytical dataset
- `outcome_lookup` — lookup table used to demonstrate relational joins

### Reproducibility

The database is rebuilt from the Day 5 cleaned CSV using
`exercises/day06_load_sqlite.py`.

The analytical SQL is stored separately in:

`sql/day06_queries.sql`

### Limitations

Queries are descriptive and educational. They do not establish causality,
clinical thresholds or treatment recommendations.

---------------------------------------------------------------------------------------------------------------------

## Week 1 mini package

Reusable validation logic from the first week has been extracted into:

`src/ai_engineer_journey/`

### Development installation

```powershell
python -m pip install -e ".[dev]"

---------------------------------------------------------------------------------------------------------------------

## Day 8 — Machine Learning Foundations

Day 8 focused on designing a valid machine-learning experiment before model
training.

### Concepts

- Features (`X`)
- Labels (`y`)
- Supervised learning
- Unsupervised learning
- Train/validation/test separation
- Stratified splitting
- Reproducibility
- Prediction-time reasoning
- Target leakage
- Preprocessing leakage
- Entity leakage
- Temporal leakage

### Artifacts

- `docs/day08_ml_workflow.md`
- `docs/day08_leakage_checklist.md`
- `exercises/day08_split_demo.py`
- `output/day08_split_summary.csv`

No predictive model was trained on Day 8. Model development begins after the
experiment and preprocessing design have been defined.

---------------------------------------------------------------------------------------------------------------------

