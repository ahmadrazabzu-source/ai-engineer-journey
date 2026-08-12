# Day 10 Learning Log

## Purpose

Train my first leakage-safe Logistic Regression baseline.

The goal was to build a simple classification baseline while keeping preprocessing leakage-safe. The preprocessing was fitted only on the training data, while validation data was used for evaluation.

## Logistic Regression

Logistic Regression is a **classifier** despite its name because it predicts a class probability and then uses a decision threshold to produce a class prediction.

For this project:

```text
Patient features
      ↓
Logistic Regression
      ↓
Probability of death_event = 1
      ↓
Decision threshold
      ↓
Class 0 or 1
```

It is not predicting an unrestricted continuous value like ordinary linear regression.

## Probability

`predict_proba()` returns the model's estimated probability for each class.

For example:

```text
[0.375, 0.625]
```

means:

* Probability of class 0 = 0.375
* Probability of class 1 = 0.625

In this project, the second value represents the estimated probability of `death_event = 1`.

## Prediction

`predict()` returns the final predicted class.

Using the default threshold of 0.5:

```text
Probability < 0.5 → class 0
Probability ≥ 0.5 → class 1
```

For example:

```text
Probability = 0.62
Prediction = 1
```

## Default threshold

The default threshold is **0.5**.

This means that if the predicted probability of class 1 is at least 50%, the model predicts class 1.

```text
0.20 → 0
0.49 → 0
0.50 → 1
0.80 → 1
```

The threshold is a decision rule; it does not change the underlying probabilities produced by the model.

## Model pipeline

The complete process is:

```text
Raw X
 ↓
Separate numeric and categorical features
 ↓
Numeric:
    SimpleImputer → StandardScaler
 ↓
Categorical:
    SimpleImputer → OneHotEncoder
 ↓
ColumnTransformer
 ↓
Logistic Regression
 ↓
predict_proba()
 ↓
Decision threshold
 ↓
Class prediction
```

The preprocessing and model are combined into one scikit-learn `Pipeline`.

The preprocessing is fitted only on the training data. Validation data is transformed using the preprocessing learned from training.

## Regularization

`C` controls the strength of regularization in Logistic Regression.

In my own words:

> **C controls how much the model is allowed to keep large coefficients.**

### Smaller C:

**Stronger regularization → coefficients are pushed more toward zero.**

### Larger C:

**Weaker regularization → coefficients can become larger.**

My experiment showed:

|    C | Coefficient L2 norm |
| ---: | ------------------: |
|  0.1 |              1.0027 |
|  1.0 |              1.6197 |
| 10.0 |              1.7871 |

So the coefficient magnitude increased as `C` increased.

## Coefficients

### Positive coefficient

A positive coefficient means that, within this fitted model, increasing that feature tends to push the model's score toward **class 1**, holding the other features constant.

For example:

```text
serum_creatinine = +0.7497
```

This means `serum_creatinine` has a positive association with the model's class-1 score.

### Negative coefficient

A negative coefficient means that, within this fitted model, increasing that feature tends to push the model's score toward **class 0**, holding the other features constant.

For example:

```text
ejection_fraction = -0.6950
```

This means `ejection_fraction` has a negative association with the model's class-1 score.

### Why coefficient does not mean causation

A coefficient is a parameter learned by a predictive model. It does not prove that a feature causes the outcome.

Coefficients can be affected by feature scaling, correlations between features, encoding, regularization, sample composition, and the model specification.

Therefore, I should describe coefficients as **model associations**, not causal clinical effects.

## Validation baseline

Using a threshold of **0.50**, my validation results were:

**Accuracy:** 0.7167

**Precision:** 0.5625

**Recall:** 0.4737

**F1:** 0.5143

**ROC-AUC:** 0.7792

These are validation results only. The protected test set was not used for model-development decisions.

## Threshold 0.30

At a threshold of **0.30**:

* Predicted positives: 32
* Accuracy: 0.6500
* Precision: 0.4688
* Recall: 0.7895
* F1: 0.5882
* ROC-AUC: 0.7792

Lowering the threshold made the model predict class 1 more often.

The main change was that **recall increased substantially**, while precision decreased.

In simple terms:

> The model became more willing to call someone positive, so it caught more actual positives but also produced more false positives.

## Threshold 0.50

At the default threshold of **0.50**:

* Predicted positives: 16
* Accuracy: 0.7167
* Precision: 0.5625
* Recall: 0.4737
* F1: 0.5143
* ROC-AUC: 0.7792

This was my baseline decision threshold.

It produced fewer positive predictions than the 0.30 threshold and more than the 0.70 threshold.

## Threshold 0.70

At a threshold of **0.70**:

* Predicted positives: 8
* Accuracy: 0.7167
* Precision: 0.6250
* Recall: 0.2632
* F1: 0.3704
* ROC-AUC: 0.7792

Increasing the threshold made the model more conservative about predicting class 1.

Precision increased, but recall decreased substantially.

In simple terms:

> The model only predicted positive when it was more confident, so its positive predictions were more precise, but it missed more actual positives.

## Protected test set

I did not use the protected test set today because it should represent **unseen data**.

The training data was used to fit the model and preprocessing. The validation set was used to evaluate and understand model-development choices such as the decision threshold.

The protected test set was kept separate so that I can use it later for a more honest final evaluation.

If I repeatedly inspect the test results and make decisions based on them, the test set is no longer truly protected.

## Real error encountered

The actual error I encountered was:

```text
NameError: name 'X_train' is not defined
```

It occurred when I tried to run:

```python
model_pipeline.fit(
    X_train,
    y_train,
)
```

## Root cause

I had defined the `split_dataset()` function, but I had not actually **called the function** to create `X_train`, `X_val`, `X_test`, `y_train`, `y_val`, and `y_test`.

Defining a function only creates the instructions. It does not execute them.

## Fix

I loaded the data and then actually called the split function:

```python
X, y = load_dataset()

(
    X_train,
    X_val,
    X_test,
    y_train,
    y_val,
    y_test,
) = split_dataset(X, y)
```

After that, `X_train` and `y_train` existed, so the model could be fitted:

```python
model_pipeline.fit(
    X_train,
    y_train,
)
```

## Next smallest action

**Day 11:** Compare the Logistic Regression baseline against Decision Trees and Random Forests, and investigate overfitting and feature importance.
