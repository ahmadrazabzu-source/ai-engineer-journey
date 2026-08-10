"""Demonstrate a leakage-aware train/validation/test split.

No model is trained on Day 8.
"""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "day05"
    / "processed"
    / "heart_failure_cleaned.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "output"
    / "day08_split_summary.csv"
)

TARGET = "death_event"


def main() -> None:
    """Create reproducible stratified train, validation and test splits."""
    df = pd.read_csv(DATA_PATH)

    y = df[TARGET]

    # Hypothetical prediction time = baseline.
    # 'time' represents future follow-up duration, so it is excluded here.
    X = df.drop(
        columns=[
            TARGET,
            "time",
        ]
    )

    # First: hold out 20% as untouched test data.
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    # Second: split remaining 80% into 60% train + 20% validation.
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val,
        y_train_val,
        test_size=0.25,
        random_state=42,
        stratify=y_train_val,
    )

    split_summary = pd.DataFrame(
        {
            "split": ["train", "validation", "test"],
            "rows": [
                len(X_train),
                len(X_val),
                len(X_test),
            ],
            "positive_rate": [
                y_train.mean(),
                y_val.mean(),
                y_test.mean(),
            ],
        }
    )

    print("Feature matrix:", X.shape)
    print("Target:", y.shape)

    print("\nFeatures:")
    print(X.columns.tolist())

    print("\nSplit summary:")
    print(split_summary.to_string(index=False))

    print("\nOverlap checks:")
    print(
        "Train/validation:",
        len(set(X_train.index) & set(X_val.index)),
    )
    print(
        "Train/test:",
        len(set(X_train.index) & set(X_test.index)),
    )
    print(
        "Validation/test:",
        len(set(X_val.index) & set(X_test.index)),
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    split_summary.to_csv(
        OUTPUT_PATH,
        index=False,
    )


if __name__ == "__main__":
    main()