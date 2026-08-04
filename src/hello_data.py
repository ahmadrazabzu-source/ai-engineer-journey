"""Day 1 environment verification using synthetic healthcare data."""

import sys
import pandas as pd


def create_demo_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "record_id": ["SYN-001", "SYN-002", "SYN-003"],
            "age": [42, 57, 35],
            "heart_rate": [78, 92, 71],
            "risk_group": ["low", "moderate", "low"],
        }
    )


def main() -> None:
    data = create_demo_data()

    print("AI Engineer Journey — Day 1")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Pandas version: {pd.__version__}")
    print("\nSynthetic data:")
    print(data.to_string(index=False))
    print(f"\nMean age: {data['age'].mean():.1f}")
    print(f"Number of records: {len(data)}")


if __name__ == "__main__":
    main()