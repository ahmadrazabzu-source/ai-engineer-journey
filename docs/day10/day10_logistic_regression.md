# Day 10 — Logistic Regression Baseline

## Prediction problem

**Target:** `death_event`

**Prediction time:** Baseline.

The goal is to use patient information available at baseline to estimate the probability of `death_event = 1`.

## Model inputs

The model uses the following features:

### Numeric features

* `age`
* `creatinine_phosphokinase`
* `ejection_fraction`
* `platelets`
* `serum_creatinine`
* `serum_sodium`

### Categorical features

* `anaemia`
* `diabetes`
* `high_blood_pressure`
* `sex`
* `smoking`

## Excluded features

### `death_event`

Excluded because it is the prediction target. Including it in the model inputs would give the model the answer it is supposed to predict.

### `time`

Excluded because our Day 8 hypothetical prediction is made at baseline, while `time` represents future follow-up duration. Including it would not match the intended baseline prediction setup.

## Pipeline

The complete pipeline follows this sequence:

```text
Raw input
    ↓
Numeric/categorical preprocessing
    ↓
Logistic Regression
    ↓
Probability
    ↓
Decision threshold
    ↓
Class prediction
```

The preprocessing is fitted only on the training data. Validation data is transformed using the preprocessing already learned from training data.

## Baseline configuration

**Model:** Logistic Regression

**C:** `1.0`

**Solver:** `lbfgs`

**Training split:** Training data only

**Evaluation split:** Validation

**Protected test set:** Not used for Day 10 model decisions.

The dataset was split into:

* Training: 179 rows
* Validation: 60 rows
* Protected test: 60 rows

## Baseline metrics

At the default threshold of **0.50**, the validation results were:

| Metric    | Validation |
| --------- | ---------: |
| Accuracy  |     0.7167 |
| Precision |     0.5625 |
| Recall    |     0.4737 |
| F1        |     0.5143 |
| ROC-AUC   |     0.7792 |

The ROC-AUC of approximately **0.779** indicates that the model has useful ability to distinguish between the two classes on the validation set.

## Threshold comparison

Changing the decision threshold changed the balance between precision and recall.

### Threshold = 0.30

* Predicted positive: 32
* Accuracy: 0.6500
* Precision: 0.4688
* Recall: 0.7895
* F1: 0.5882
* ROC-AUC: 0.7792

At `0.30`, the model predicts more positive cases. This increases recall substantially, meaning the model identifies more of the actual positive cases. However, precision decreases.

### Threshold = 0.50

* Predicted positive: 16
* Accuracy: 0.7167
* Precision: 0.5625
* Recall: 0.4737
* F1: 0.5143
* ROC-AUC: 0.7792

This is the standard baseline threshold. It provides a middle point between the lower and higher thresholds.

### Threshold = 0.70

* Predicted positive: 8
* Accuracy: 0.7167
* Precision: 0.6250
* Recall: 0.2632
* F1: 0.3704
* ROC-AUC: 0.7792

At `0.70`, the model is more conservative about predicting the positive class. Precision increases, but recall falls substantially.

### Overall threshold observation

The threshold controls the trade-off between precision and recall.

```text
Lower threshold → more positive predictions → higher recall

Higher threshold → fewer positive predictions → higher precision
```

ROC-AUC stayed at `0.7792` because changing the threshold does not change the underlying predicted probabilities or their ranking.

## Coefficient interpretation

The largest positive coefficient was:

**`serum_creatinine` = +0.7497**

This means that, within this fitted Logistic Regression model, higher values of `serum_creatinine` push the model score toward class 1, holding the other model inputs constant.

The largest negative coefficient was:

**`ejection_fraction` = -0.6950**

This means that, within this fitted model, higher values of `ejection_fraction` push the model score toward class 0, holding the other model inputs constant.

These coefficients should be interpreted as **associations learned by the predictive model**, not as proof that either variable causes or prevents death.

The coefficient values can also be affected by scaling, correlations between features, encoding choices, regularization, sample composition, and model specification.

## Regularization

The effect of changing `C` was examined using the coefficient L2 norm:

|    C | Coefficient L2 norm |
| ---: | ------------------: |
|  0.1 |              1.0027 |
|  1.0 |              1.6197 |
| 10.0 |              1.7871 |

A smaller `C` means **stronger regularization**, which pushes coefficients toward zero more strongly.

Therefore:

```text
C = 0.1 → stronger regularization → smaller coefficients

C = 1.0 → less regularization

C = 10.0 → weaker regularization → larger coefficients
```

This demonstrates that regularization affects the size of the model's learned coefficients.

## Limitations

* Small historical dataset.
* No external validation.
* No hyperparameter tuning yet.
* The prediction threshold is not clinically validated.
* Coefficients are predictive model parameters, not causal effects.
* The protected test performance has not yet been inspected.
* This is an educational portfolio project and is not a clinically validated prediction system.
