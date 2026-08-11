"""Build a leakage-safe preprocessing pipeline for mixed healthcare data.

Educational portfolio project only. No model is trained on Day 9.
"""

# Step 1: Import libraries

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# Step 2: Define file paths

'''PROJECT_ROOT = Path(__file__).resolve().parent''' ### When writing/running a .py file

"""PROJECT_ROOT = Path.cwd().parent ### When typing in  >>> Python shell"""

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "day05"
    / "processed"
    / "heart_failure_cleaned.csv"
)

print(DATA_PATH)
print(DATA_PATH.exists())

SUMMARY_PATH = (
    PROJECT_ROOT
    / "output"
    / "day09"
    / "day09_preprocessing_summary.csv"
)

print(SUMMARY_PATH)
print(SUMMARY_PATH.exists())

SCHEMA_PATH = (
    PROJECT_ROOT
    / "output"
    / "day09"
    / "day09_feature_schema.csv"
)

print(SCHEMA_PATH)
print(SCHEMA_PATH.exists())

PREVIEW_PATH = (
    PROJECT_ROOT
    / "output"
    / "day09"
    / "day09_transformed_preview.csv"
)

print(PREVIEW_PATH)
print(PREVIEW_PATH.exists())


# Step 3 — Define target and columns

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

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


# Step 4 — Load dataset

def load_dataset() -> tuple[pd.DataFrame, pd.Series]:
    """Return the leakage-audited feature matrix and target."""
    df = pd.read_csv(DATA_PATH)

    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    return X, y


assert TARGET not in FEATURES
assert "time" not in FEATURES


# Step 5 — Build train/validation/test split

'''Create a function to split dataset into train, validation and test sets. Function will take in feature matrix
X and target vector y and return splits. Splits will be stratified based on target variable to ensure that
distribution of classes is similar across splits.'''


def split_dataset(
    X: pd.DataFrame,
    y: pd.Series,
):
    """Return reproducible stratified train, validation and test splits."""
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    X_train, X_val, y_train, y_val = train_test_split(
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


'''____________________________________________CORRECTIONS IN STEP 5____________________________________________'''

X, y = load_dataset()

print(X, y)

(
    X_train,
    X_val,
    X_test,
    y_train,
    y_val,
    y_test,
) = split_dataset(X, y)



# Step 6–9 — Build preprocessing pipeline

def build_preprocessor() -> ColumnTransformer:
    """Return an unfitted leakage-safe preprocessing pipeline."""

    # Step 6 — Numeric pipeline
    # Imputer first, scaler second
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

    # Step 7 — Categorical pipeline
    # Imputer first, encoder second
    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent"),
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

    # Step 8 — Combine numeric and categorical pipelines
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

    # Step 9 — Request pandas output
    preprocessor.set_output(
        transform="pandas"
    )

    return preprocessor


# Used later in Step 16
def feature_group(feature_name: str) -> str:
    """Return the broad preprocessing group."""
    if feature_name in NUMERIC_FEATURES:
        return "numeric_scaled"

    return "categorical_one_hot"


def main() -> None:
    """Run the Day 9 leakage-safe preprocessing demonstration."""

    # Load dataset
    X, y = load_dataset()

    # Split BEFORE preprocessing
    (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
    ) = split_dataset(X, y)

    print("X:", X.shape)
    print("y:", y.shape)

    print("X_train:", X_train.shape)
    print("X_val:", X_val.shape)
    print("X_test:", X_test.shape)

    # Build an unfitted preprocessor
    preprocessor = build_preprocessor()

    # IMPORTANT:
    # Train = fit + transform
    X_train_processed = preprocessor.fit_transform(
        X_train
    )

    # Validation = transform only
    X_val_processed = preprocessor.transform(
        X_val
    )

    # Test = transform only
    X_test_processed = preprocessor.transform(
        X_test
    )

    # Step 10 — Inspect transformed shapes

    print("\nRaw shapes")
    print("Train:", X_train.shape)
    print("Validation:", X_val.shape)
    print("Test:", X_test.shape)

    print("\nProcessed shapes")
    print("Train:", X_train_processed.shape)
    print("Validation:", X_val_processed.shape)
    print("Test:", X_test_processed.shape)

    assert list(X_train_processed.columns) == list(
        X_val_processed.columns
    )

    assert list(X_train_processed.columns) == list(
        X_test_processed.columns
    )

    print("\nFeature schemas identical: True")

    # Step 11 — Inspect transformed feature names

    print("\nTransformed features:")

    for feature in X_train_processed.columns:
        print(feature)

    # Step 12 — Prove scaler statistics came from training data

    fitted_numeric_pipeline = (
        preprocessor
        .named_transformers_["numeric"]
    )

    fitted_scaler = (
        fitted_numeric_pipeline
        .named_steps["scaler"]
    )

    print("\nScaler means learned during fit:")
    print(fitted_scaler.mean_)

    training_means = (
        X_train[NUMERIC_FEATURES]
        .mean()
        .to_numpy()
    )

    print("\nTraining means:")
    print(training_means)

    assert np.allclose(
        fitted_scaler.mean_,
        training_means,
    )

    print("\nScaler statistics match training data: True")

    # Step 13 — Compare with full-dataset means

    full_dataset_means = (
        X[NUMERIC_FEATURES]
        .mean()
        .to_numpy()
    )

    print("\nFull dataset means:")
    print(full_dataset_means)

    print(
        "\nMaximum absolute difference:",
        np.max(
            np.abs(
                fitted_scaler.mean_
                - full_dataset_means
            )
        ),
    )

    # Step 14 — Inspect learned categories

    fitted_categorical_pipeline = (
        preprocessor
        .named_transformers_["categorical"]
    )

    encoder = (
        fitted_categorical_pipeline
        .named_steps["encoder"]
    )

    print("\nCategories learned from training data:")

    for column, categories in zip(
        CATEGORICAL_FEATURES,
        encoder.categories_,
    ):
        print(column, categories)

    # Missing-value stress test

    stress_test = X_val.head(3).copy()

    stress_test.loc[
        stress_test.index[0],
        "age",
    ] = np.nan

    stress_test.loc[
        stress_test.index[1],
        "serum_creatinine",
    ] = np.nan

    stress_test.loc[
        stress_test.index[2],
        "diabetes",
    ] = np.nan

    print("\nControlled stress test:")
    print(stress_test)

    print(
        "\nMissing values before pipeline:",
        stress_test.isna().sum().sum(),
    )

    # Transform only — DO NOT fit_transform stress_test
    stress_processed = preprocessor.transform(
        stress_test
    )

    remaining_missing = (
        stress_processed
        .isna()
        .sum()
        .sum()
    )

    print(
        "Missing values after pipeline:",
        remaining_missing,
    )

    # Step 15 — Save preprocessing summary

    summary_df = pd.DataFrame(
        {
            "split": [
                "train",
                "validation",
                "test",
            ],
            "raw_rows": [
                len(X_train),
                len(X_val),
                len(X_test),
            ],
            "raw_features": [
                X_train.shape[1],
                X_val.shape[1],
                X_test.shape[1],
            ],
            "processed_features": [
                X_train_processed.shape[1],
                X_val_processed.shape[1],
                X_test_processed.shape[1],
            ],
            "target_positive_rate": [
                y_train.mean(),
                y_val.mean(),
                y_test.mean(),
            ],
        }
    )

    # Create output/day09 folder
    SUMMARY_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary_df.to_csv(
        SUMMARY_PATH,
        index=False,
    )

    # Step 16 — Save feature schema

    feature_schema = pd.DataFrame(
        {
            "processed_feature":
                X_train_processed.columns
        }
    )

    feature_schema["processing"] = (
        feature_schema[
            "processed_feature"
        ].map(feature_group)
    )

    feature_schema.to_csv(
        SCHEMA_PATH,
        index=False,
    )

    # Step 17 — Save transformed preview

    X_train_processed.head(10).to_csv(
        PREVIEW_PATH,
        index=False,
    )

    print("\nFiles saved:")
    print(SUMMARY_PATH)
    print(SCHEMA_PATH)
    print(PREVIEW_PATH)

    print("\nFile checks:")
    print("Summary:", SUMMARY_PATH.exists())
    print("Schema:", SCHEMA_PATH.exists())
    print("Preview:", PREVIEW_PATH.exists())


if __name__ == "__main__":
    main()