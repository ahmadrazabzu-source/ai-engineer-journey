"""Compare Logistic Regression, Decision Trees and Random Forests.

The experiment uses validation data for model-development comparison.
The protected test set remains untouched.
"""

# Step 1 — Imports

from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
)
from sklearn.tree import DecisionTreeClassifier

# Step 2 — Paths

PROJECT_ROOT = Path(__file__).resolve().parent.parent

'''PROJECT_ROOT = Path.cwd().parent'''
print(PROJECT_ROOT)

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "day05"
    / "processed"
    / "heart_failure_cleaned.csv"
)
print(DATA_PATH)

MODEL_COMPARISON_PATH = (
    PROJECT_ROOT
    / "output"
    / "day11"
    / "day11_model_comparison.csv"
)
print(MODEL_COMPARISON_PATH)

DEPTH_COMPARISON_PATH = (
    PROJECT_ROOT
    / "output"
    / "day11"
    / "day11_depth_comparison.csv"
)
print(DEPTH_COMPARISON_PATH)

IMPORTANCE_PATH = (
    PROJECT_ROOT
    / "output"
    / "day11"
    / "day11_feature_importance.csv"
)
print(IMPORTANCE_PATH)

PLOT_PATH = (
    PROJECT_ROOT
    / "output"
    / "day11"
    / "day11_model_comparison.png"
)
print(PLOT_PATH)

# Step 3 — Keep your Day 10 feature definition unchanged

TARGET = "death_event"

NUMERIC_FEATURES = [
    "age",
    "creatinine_phosphokinase",
    "ejection_fraction",
    "platelets",
    "serum_creatinine",
    "serum_sodium",
]

CATEGORICAL_FEATURES = [
    "anaemia",
    "diabetes",
    "high_blood_pressure",
    "sex",
    "smoking",
]

FEATURES = (
    NUMERIC_FEATURES
    + CATEGORICAL_FEATURES
)

# Step 4 — Dataset loader

def load_dataset() -> tuple[pd.DataFrame, pd.Series]:
    """Return the leakage-audited feature matrix and target."""
    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    assert TARGET not in X.columns
    assert "time" not in X.columns

    return X, y


# Step 5 — Reuse the same split

def split_dataset(
    X: pd.DataFrame,
    y: pd.Series,
):
    """Return reproducible train, validation and protected test splits."""
    (
        X_train_val,
        X_test,
        y_train_val,
        y_test,
    ) = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    (
        X_train,
        X_val,
        y_train,
        y_val,
    ) = train_test_split(
        X_train_val,
        y_train_val,
        test_size=0.25,
        random_state=42,
        stratify=y_train_val,
    )

    return (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
    )

# Step 6 — Preprocessor

def build_preprocessor() -> ColumnTransformer:
    """Return an unfitted mixed-type preprocessing system."""
    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median"),
            ),
            (
                "scaler",
                StandardScaler(),
            ),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                ),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_pipeline,
                NUMERIC_FEATURES,
            ),
            (
                "categorical",
                categorical_pipeline,
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    preprocessor.set_output(
        transform="pandas"
    )

    return preprocessor


# Step 7 — Metrics function

def calculate_metrics(
    y_true: pd.Series,
    predictions,
    probabilities,
) -> dict[str, float]:
    """Return classification metrics used for Day 11 comparison."""
    return {
        "accuracy": accuracy_score(
            y_true,
            predictions,
        ),
        "precision": precision_score(
            y_true,
            predictions,
            zero_division=0,
        ),
        "recall": recall_score(
            y_true,
            predictions,
            zero_division=0,
        ),
        "f1": f1_score(
            y_true,
            predictions,
            zero_division=0,
        ),
        "roc_auc": roc_auc_score(
            y_true,
            probabilities,
        ),
    } # type: ignore

# Step 8 — Generic evaluation function

def evaluate_pipeline(
    model_name: str,
    pipeline: Pipeline,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_val: pd.DataFrame,
    y_val: pd.Series,
) -> dict[str, float | str]:

    start_time = perf_counter()

    pipeline.fit(
        X_train,
        y_train,
    )

    fit_seconds = (
        perf_counter()
        - start_time
    )

    train_probabilities = (
        pipeline.predict_proba(
            X_train
        )[:, 1]
    )

    train_predictions = (
        pipeline.predict(
            X_train
        )
    )

    val_probabilities = (
        pipeline.predict_proba(
            X_val
        )[:, 1]
    )

    val_predictions = (
        pipeline.predict(
            X_val
        )
    )

    train_metrics = calculate_metrics(
        y_train,
        train_predictions,
        train_probabilities,
    )

    val_metrics = calculate_metrics(
        y_val,
        val_predictions,
        val_probabilities,
    )

    return {
        "model": model_name,
        "train_accuracy": train_metrics["accuracy"],
        "validation_accuracy": val_metrics["accuracy"],
        "train_f1": train_metrics["f1"],
        "validation_f1": val_metrics["f1"],
        "train_roc_auc": train_metrics["roc_auc"],
        "validation_roc_auc": val_metrics["roc_auc"],
        "fit_seconds": fit_seconds,
    }

# Step 9 — Logistic Regression baseline

'''Recreate Day 10 model:'''

X, y = load_dataset()

(
    X_train,
    X_val,
    X_test,
    y_train,
    y_val,
    y_test,
) = split_dataset(X, y)

logistic_pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            build_preprocessor(),
        ),
        (
            "model",
            LogisticRegression(
                C=1.0,
                solver="lbfgs",
                max_iter=1000,
            ),
        ),
    ]
)

'''Evaluate:'''

comparison_rows = []

comparison_rows.append(
    evaluate_pipeline(
        "logistic_regression",
        logistic_pipeline,
        X_train,
        y_train,
        X_val,
        y_val,
    )
)

# Step 10 — Decision Tree depth experiment

'''Use:'''

TREE_DEPTHS = [
    1,
    2,
    3,
    5,
    None,
]

'''Create:'''

depth_rows = []

'''For every depth:'''

for depth in TREE_DEPTHS:
    tree_pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                build_preprocessor(),
            ),
            (
                "model",
                DecisionTreeClassifier(
                    max_depth=depth,
                    random_state=42,
                ),
            ),
        ]
)

result = evaluate_pipeline(
        f"decision_tree_depth_{depth}",
        tree_pipeline,
        X_train,
        y_train,
        X_val,
        y_val,
)

result["max_depth"] = (
        "None"
        if depth is None
        else depth
)

depth_rows.append(result)


'''Build depth table'''

depth_table = pd.DataFrame(
    depth_rows
)

'''Display only the important columns:'''

print(
    "\nDecision Tree depth comparison:"
)

print(
    depth_table[
        [
            "max_depth",
            "train_f1",
            "validation_f1",
            "train_roc_auc",
            "validation_roc_auc",
        ]
    ].to_string(index=False)
)

'''Save:'''

DEPTH_COMPARISON_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

depth_table.to_csv(
    DEPTH_COMPARISON_PATH,
    index=False,
)

# Step 11 — Calculate generalization gap

'''Add:'''

depth_table[
    "roc_auc_gap"
] = (
    depth_table["train_roc_auc"]
    - depth_table[
        "validation_roc_auc"
    ]
)

'''And:'''

depth_table[
    "f1_gap"
] = (
    depth_table["train_f1"]
    - depth_table[
        "validation_f1"
    ]
)

'''Interpret:

small gap
→ train and validation behavior relatively similar

large positive gap
→ possible overfitting'''

# Step 12 — Choose one tree for the comparison table

best_tree_row = (
    depth_table
    .sort_values(
        "validation_roc_auc",
        ascending=False,
    )
    .iloc[0]
)

# Step 13 — Random Forest

random_forest_pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            build_preprocessor(),
        ),
        (
            "model",
            RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                n_jobs=-1,
            ),
        ),
    ]
)

'''Evaluate:'''

comparison_rows.append(
    evaluate_pipeline(
        "random_forest",
        random_forest_pipeline,
        X_train,
        y_train,
        X_val,
        y_val,
    )
)

'''Better:'''

best_depth_value = (
    depth_table
    .sort_values(
        "validation_roc_auc",
        ascending=False,
    )
    .iloc[0]["max_depth"]
)

'''Create:'''

all_results = (
    comparison_rows
    + depth_rows
)

comparison_table = pd.DataFrame(
    all_results
)

'''Then:'''

comparison_table[
    "roc_auc_gap"
] = (
    comparison_table[
        "train_roc_auc"
    ]
    - comparison_table[
        "validation_roc_auc"
    ]
)

'''Save:'''

comparison_table.to_csv(
    MODEL_COMPARISON_PATH,
    index=False,
)

'''key comparison columns
Display:'''

display_columns = [
    "model",
    "train_f1",
    "validation_f1",
    "train_roc_auc",
    "validation_roc_auc",
    "roc_auc_gap",
    "fit_seconds",
]

print(
    comparison_table[
        display_columns
    ].to_string(index=False)
)

### Comparison plot

'''Create:'''

plot_df = comparison_table[
    [
        "model",
        "train_roc_auc",
        "validation_roc_auc",
    ]
].copy()

'''Then:'''

plot_df = plot_df.set_index(
    "model"
)

'''Plot:'''

ax = plot_df.plot(
    kind="bar",
    figsize=(11, 6),
)

ax.set_title(
    "Day 11 — Training vs Validation ROC-AUC"
)

ax.set_xlabel(
    "Model"
)

ax.set_ylabel(
    "ROC-AUC"
)

ax.set_ylim(
    0.0,
    1.05,
)

ax.tick_params(
    axis="x",
    rotation=45,
)

plt.tight_layout()

plt.savefig(
    PLOT_PATH,
    dpi=160,
)

plt.close()

''''An even better depth plot'''

depth_plot_df = (
    depth_table
    .copy()
)

'''Feature importance from Random Forest'''

'''Fit the forest if not already retained:'''

random_forest_pipeline.fit(
    X_train,
    y_train,
)

'''Retrieve the fitted preprocessor:'''

fitted_preprocessor = (
    random_forest_pipeline
    .named_steps["preprocessor"]
)

'''Feature names:'''

feature_names = (
    fitted_preprocessor
    .get_feature_names_out()
)

'''Forest:'''

fitted_forest = (
    random_forest_pipeline
    .named_steps["model"]
)

'''Importances:'''

importances = (
    fitted_forest
    .feature_importances_
)

'''Create:'''

importance_table = pd.DataFrame(
    {
        "feature": feature_names,
        "importance": importances,
    }
)

'''Sort:'''

importance_table = (
    importance_table
    .sort_values(
        "importance",
        ascending=False,
    )
)

'''Print:'''

print(
    "\nRandom Forest impurity-based "
    "feature importance:"
)

print(
    importance_table
    .head(10)
    .to_string(index=False)
)

'''Save:'''

importance_table.to_csv(
    IMPORTANCE_PATH,
    index=False,
)

### Check importance sum

print(
    "Importance sum:",
    importance_table[
        "importance"
    ].sum(),
)
