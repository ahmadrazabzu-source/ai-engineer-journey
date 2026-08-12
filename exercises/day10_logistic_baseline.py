"""Train a leakage-safe Logistic Regression baseline.

Educational portfolio project only.
The protected test set is not used for model-development decisions.
"""

# Step 1 — Import

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
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


# Step 2 — Paths

PROJECT_ROOT = Path(__file__).resolve().parent.parent

"""PROJECT_ROOT = Path.cwd().resolve().parent"""

print(PROJECT_ROOT)

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "day05"
    / "processed"
    / "heart_failure_cleaned.csv"
)

METRICS_PATH = (
    PROJECT_ROOT
    / "output"
    / "day10"
    / "day10_baseline_metrics.csv"
)

THRESHOLD_PATH = (
    PROJECT_ROOT
    / "output"
    / "day10"
    / "day10_threshold_comparison.csv"
)

COEFFICIENT_PATH = (
    PROJECT_ROOT
    / "output"
    / "day10"
    / "day10_coefficients.csv"
)

PROBABILITY_PATH = (
    PROJECT_ROOT
    / "output"
    / "day10"
    / "day10_probability_preview.csv"
)

# Step 3 — Use exactly the same feature definition as Day 9

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


# Step 4 — Load data

def load_dataset() -> tuple[pd.DataFrame, pd.Series]:
    """Return leakage-audited features and target."""
    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    assert TARGET not in X.columns
    assert "time" not in X.columns

    return X, y


# Step 5 — Reproduce Day 8/9 split

def split_dataset(
    X: pd.DataFrame,
    y: pd.Series,
):
    """Return stratified train, validation and test partitions."""
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


# Step 6 — Rebuild/reuse Day 9 preprocessor

def build_preprocessor() -> ColumnTransformer:
    """Return the unfitted Day 9 preprocessing system."""
    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                ),
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

X, y = load_dataset()

(
    X_train,
    X_val,
    X_test,
    y_train,
    y_val,
    y_test,
) = split_dataset(X, y)

# Step 7 — Build the complete ML pipeline

def build_model() -> Pipeline:
    """Return an unfitted Logistic Regression baseline pipeline."""
    return Pipeline(
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


# Step 8 — Fit ONLY on training data

model_pipeline = build_model()

model_pipeline.fit(
    X_train,
    y_train,
)

# Step 9 — Obtain validation probabilities

validation_probabilities_all = (
    model_pipeline.predict_proba(
        X_val
    )
)

print(
    validation_probabilities_all[:5]
)

fitted_classifier = (
    model_pipeline
    .named_steps["model"]
)

print(
    "Classes:",
    fitted_classifier.classes_,
)

positive_index = (
    list(
        fitted_classifier.classes_
    ).index(1)
)

validation_probabilities = (
    validation_probabilities_all[
        :,
        positive_index,
    ]
)

# Step 10 — Preview probabilities

probability_preview = pd.DataFrame(
    {
        "actual": y_val.to_numpy(),
        "predicted_probability_class_1":
            validation_probabilities,
    }
)

probability_preview[
    "prediction_threshold_0_50"
] = (
    validation_probabilities > 0.50
).astype(int)

PROBABILITY_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

probability_preview.head(15).to_csv(
    PROBABILITY_PATH,
    index=False,
)


# Step 11 — Compare with .predict()

default_predictions = (
    model_pipeline.predict(
        X_val
    )
)

manual_default_predictions = (
    validation_probabilities > 0.50
).astype(int)

assert np.array_equal(
    default_predictions,
    manual_default_predictions,
)

# Step 12 — Calculate baseline validation metrics

def calculate_metrics(
    y_true: pd.Series,
    predictions: np.ndarray,
    probabilities: np.ndarray,
) -> dict[str, float]:
    """Return baseline binary-classification metrics."""
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

'''Build baseline table'''

baseline_metrics = calculate_metrics(
    y_val,
    default_predictions, # type: ignore
    validation_probabilities,
)

baseline_table = pd.DataFrame(
    [
        {
            "model":
                "logistic_regression",
            "split":
                "validation",
            "threshold":
                0.50,
            **baseline_metrics,
        }
    ]
)

print(
    "\nBaseline validation metrics:"
)

print(
    baseline_table.to_string(
        index=False
    )
)

baseline_table.to_csv(
    METRICS_PATH,
    index=False,
)

# Threshold effects

THRESHOLDS = [
    0.30,
    0.50,
    0.70,
]
threshold_rows = []

for threshold in THRESHOLDS:
    predictions = (
        validation_probabilities
        > threshold
    ).astype(int)

    metrics = calculate_metrics(
        y_val,
        predictions,
        validation_probabilities,
    )

    threshold_rows.append(
        {
            "threshold": threshold,
            "predicted_positive_count":
                int(predictions.sum()),
            **metrics,
        }
    )


threshold_table = pd.DataFrame(
    threshold_rows
)

print(
    "\nThreshold comparison:"
)

print(
    threshold_table.to_string(
        index=False
    )
)


threshold_table.to_csv(
    THRESHOLD_PATH,
    index=False,
)


### Coefficient inspection

fitted_preprocessor = (
    model_pipeline
    .named_steps["preprocessor"]
)

fitted_classifier = (
    model_pipeline
    .named_steps["model"]
)

feature_names = (
    fitted_preprocessor
    .get_feature_names_out()
)

coefficients = (
    fitted_classifier
    .coef_[0]
)

coefficient_table = pd.DataFrame(
    {
        "feature": feature_names,
        "coefficient": coefficients,
    }
)

coefficient_table[
    "absolute_coefficient"
] = (
    coefficient_table[
        "coefficient"
    ].abs()
)


coefficient_table = (
    coefficient_table
    .sort_values(
        "absolute_coefficient",
        ascending=False,
    )
)

print(
    "\nLargest coefficient magnitudes:"
)

print(
    coefficient_table
    .head(10)
    .to_string(index=False)
)


coefficient_table.to_csv(
    COEFFICIENT_PATH,
    index=False,
)


### Inspect intercept

print(
    "Intercept:",
    fitted_classifier.intercept_[0],
)

### Small regularization experiment

REGULARIZATION_VALUES = [
    0.1,
    1.0,
    10.0,
]

for c_value in REGULARIZATION_VALUES:
    comparison_pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                build_preprocessor(),
            ),
            (
                "model",
                LogisticRegression(
                    C=c_value,
                    solver="lbfgs",
                    max_iter=1000,
                ),
            ),
        ]
    )

    comparison_pipeline.fit(
        X_train,
        y_train,
    )

    comparison_model = (
        comparison_pipeline
        .named_steps["model"]
    )

    coefficient_norm = np.linalg.norm(
        comparison_model.coef_
    )

    print(
        f"C={c_value}: "
        f"coefficient L2 norm="
        f"{coefficient_norm:.4f}"
    )


def main() -> None:
    """Train and inspect the Day 10 Logistic Regression baseline."""
    X, y = load_dataset()

    (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
    ) = split_dataset(X, y)

    print(
        "Train:",
        X_train.shape,
    )
    print(
        "Validation:",
        X_val.shape,
    )
    print(
        "Protected test:",
        X_test.shape,
    )

    model_pipeline = build_model()

    model_pipeline.fit(
        X_train,
        y_train,
    )

    probabilities_all = (
        model_pipeline.predict_proba(
            X_val
        )
    )

    fitted_classifier = (
        model_pipeline
        .named_steps["model"]
    )

    positive_index = (
        list(
            fitted_classifier.classes_
        ).index(1)
    )

    probabilities = probabilities_all[
        :,
        positive_index,
    ]

    predictions = (
        model_pipeline.predict(
            X_val
        )
    )

    # Create baseline metrics.
    # Create threshold comparison.
    # Extract coefficients.
    # Save all outputs.

    print(
        "\nProtected test set was "
        "not used for model decisions."
    )


if __name__ == "__main__":
    main()