My prediction:

As max_depth increases, training performance will generally increase.
Validation performance may improve initially but can plateau or decline if the
tree begins fitting noise.

# Day 11 Learning Log

## Purpose

I learned how tree-based models make nonlinear decisions, how increasing tree complexity can cause overfitting, and how Decision Trees and Random Forests compare with my Logistic Regression baseline.

## Decision Tree

A Decision Tree makes predictions by asking a sequence of questions about the features. Each decision splits the data into smaller groups until the model reaches a final prediction.

## Root

The **root** is the first decision point of the tree. It contains the complete training dataset and makes the first split.

## Internal node

An **internal node** is a decision point in the middle of the tree. It applies a condition to a feature and sends observations down different branches.

## Leaf

A **leaf** is the final node of the tree. It contains the final prediction made by the model.

## max_depth

`max_depth` controls how deep a Decision Tree can grow.

A larger `max_depth` allows the tree to make more complex decisions. A small depth can cause underfitting, while a very large depth can cause overfitting.

## Underfitting

Underfitting happens when the model is too simple to capture important patterns in the data. The model performs poorly even on the training data.

## Overfitting

Overfitting happens when the model learns the training data too closely. It can achieve excellent training performance but perform much worse on unseen validation data.

## Generalization gap

The generalization gap is the difference between training performance and validation performance.

For ROC-AUC, my gap is:

**Training ROC-AUC − Validation ROC-AUC**

A large positive gap indicates that the model performs much better on training data than validation data and may be overfitting.

## My prediction before the depth experiment

Before running the experiment, I predicted that a shallow tree would underfit because it would be too simple. I expected performance to improve as the tree became deeper, but I also expected an unrestricted tree to become more prone to overfitting.

## Actual depth results

### Depth 1

The script did not print the individual depth results for depths 1, 2, 3, and 5 in the final output. Only the unlimited-depth result appeared in the displayed table.

### Depth 2

The individual result was not displayed in the final terminal output.

### Depth 3

The individual result was not displayed in the final terminal output.

### Depth 5

The individual result was not displayed in the final terminal output.

### Unlimited

**Train F1:** 1.000000
**Validation F1:** 0.594595
**Train ROC-AUC:** 1.000000
**Validation ROC-AUC:** 0.704108

The unlimited tree achieved perfect training performance but much lower validation performance, showing clear overfitting.

## Most obvious overfitting example

**Model:** Decision Tree with unlimited depth

**Train ROC-AUC:** 1.000000

**Validation ROC-AUC:** 0.704108

**Gap:** 0.295892

This was the clearest example of overfitting in my experiment.

## Random Forest

A Random Forest combines many Decision Trees instead of relying on one tree.

The trees are trained using randomness in the samples/features, and their predictions are combined. This generally makes the model more robust than a single Decision Tree.

My Random Forest had:

**Train ROC-AUC:** 1.000000
**Validation ROC-AUC:** 0.879332

Its ROC-AUC gap was **0.120668**, which was much smaller than the unlimited Decision Tree's gap of **0.295892**.

## Logistic Regression comparison

The **Random Forest performed better** on validation.

| Model                     | Validation F1 | Validation ROC-AUC |
| ------------------------- | ------------: | -----------------: |
| Logistic Regression       |      0.514286 |           0.779204 |
| Random Forest             |      0.702703 |           0.879332 |
| Decision Tree — Unlimited |      0.594595 |           0.704108 |

The Random Forest performed noticeably better than Logistic Regression.

The validation ROC-AUC improved from **0.779204** with Logistic Regression to **0.879332** with Random Forest.

## Feature importance

My Random Forest's top 5 features were:

1. **serum_creatinine** — 0.197086
2. **ejection_fraction** — 0.168322
3. **creatinine_phosphokinase** — 0.129188
4. **platelets** — 0.115957
5. **serum_sodium** — 0.113736

The importance values sum to **1.0**, confirming that the Random Forest's impurity-based feature importances were generated correctly.

## Why feature importance is not causality

Feature importance tells me which features were useful to the model when making predictions. It does not prove that those features cause the outcome.

For example, a feature can have high importance because it is associated with another variable or because it helps the model separate different groups. Therefore, feature importance should be interpreted as **predictive importance, not causal evidence**.

## Real error encountered

The real error I encountered was:

```text
TypeError: 'NoneType' object does not support item assignment
```

It occurred when I tried to run:

```python
result["max_depth"] = ...
```

## Root cause

The `evaluate_pipeline()` function was returning `None`.

Therefore:

```python
result = evaluate_pipeline(...)
```

made `result` equal to `None`.

When the code tried to add `"max_depth"` to `result`, Python could not assign a value to `None`.

## Fix

I added the missing `return` dictionary at the end of `evaluate_pipeline()`.

This returned the model name, training metrics, validation metrics, and fitting time.

I also removed the duplicate `train_probabilities` calculation.

After fixing the function, I ran the complete script successfully.

## Validation

The final script passed Python syntax checking:

```text
python -m py_compile exercises\day11_tree_forest_comparison.py
```

There was no error.

The expected Day 11 output files were also successfully created:

* `day11_depth_comparison.csv`
* `day11_feature_importance.csv`
* `day11_model_comparison.csv`
* `day11_model_comparison.png`

## Next smallest action

**Day 12:** Study confusion matrix, precision, recall, F1, ROC-AUC, and PR-AUC. Then compare the same classifier at multiple decision thresholds.