# Day 11 — Decision Trees and Random Forests

## Objective

Compare nonlinear tree-based classifiers against the Day 10 Logistic
Regression baseline while monitoring overfitting.

## Models

- Logistic Regression
- Decision Tree max_depth=1
- Decision Tree max_depth=2
- Decision Tree max_depth=3
- Decision Tree max_depth=5
- Decision Tree unrestricted
- Random Forest

## Experimental controls

All models use:

- The same dataset
- The same feature definition
- The same train/validation/test split
- The same random seed where applicable
- The same protected test-set policy

## Tree-depth result

Insert my actual results.

## Overfitting observation

Describe the relationship between training and validation performance as tree
depth increased.

## Random Forest result

Compare it with the individual trees.

## Logistic Regression comparison

State whether the nonlinear models improved validation performance enough to
justify their complexity.

## Feature importance

List the top five impurity-based Random Forest feature importances.

## Feature-importance limitation

Impurity-based importance is model-specific, can favor high-cardinality
features and does not establish causality.

## Test-set policy

The protected test set was not used to select a model on Day 11.

## Limitations

- Small historical dataset
- Single validation split
- No formal cross-validation yet
- No hyperparameter optimization yet
- Feature importance is not causal
- No external validation