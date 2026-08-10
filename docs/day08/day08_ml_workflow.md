flowchart TD
    A[Define business / research problem] --> B[Define prediction time]
    B --> C[Define target y]
    C --> D[Identify candidate features X]
    D --> E[Leakage audit]
    E --> F[Freeze independent test set]
    F --> G[Create train / validation sets]
    G --> H[Fit preprocessing on training data only]
    H --> I[Train baseline model]
    I --> J[Evaluate on validation data]
    J --> K{Need improvement?}
    K -- Yes --> L[Change features / model / hyperparameters]
    L --> H
    K -- No --> M[Freeze all decisions]
    M --> N[Evaluate once on test set]
    N --> O[Error analysis and limitations]
    O --> P[Package / deploy if acceptable]
    P --> Q[Monitor data and model behavior]
    Q --> R[Retrain when justified]


## Core rule

The test set is not development data.

All learned preprocessing, feature selection and model fitting must be based
only on training data. Validation data guides model-development decisions.
The test set is reserved for final evaluation after the workflow is frozen.

This reflects current scikit-learn and Google ML guidance.