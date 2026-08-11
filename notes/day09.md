# Day 9 Learning Log

## Purpose

Learn how to build leakage-safe preprocessing for mixed numeric and categorical features using scikit-learn `Pipeline` and `ColumnTransformer`.

## Numeric features

The numeric features used in the preprocessing pipeline are:

* `age`
* `creatinine_phosphokinase`
* `ejection_fraction`
* `platelets`
* `serum_creatinine`
* `serum_sodium`

These features are processed using median imputation followed by standard scaling.

## Categorical features

The categorical features used are:

* `anaemia`
* `diabetes`
* `high_blood_pressure`
* `sex`
* `smoking`

These features are processed using most-frequent imputation followed by one-hot encoding.

## Excluded features

### Target: `death_event`

**Reason:**
`death_event` is the target variable that the future model will predict. It must not be included inside the feature matrix `X`, because including the answer as an input would create target leakage.

### `time`

**Reason:**
`time` represents follow-up duration. Based on the prediction scenario defined earlier, it is excluded because it contains information related to what happens after the prediction point and could introduce future-information leakage.

## SimpleImputer

`SimpleImputer.fit()` learns the replacement value that should be used when missing values are encountered.

For example, the numeric imputer learns the median of each numeric training feature.

The categorical imputer learns the most frequent category of each categorical training feature.

These learned values must come only from the training dataset.

**Numeric strategy:** `median`

**Categorical strategy:** `most_frequent`

## StandardScaler

`StandardScaler` learns the mean and standard deviation of every numeric feature from the training data.

It then transforms values using those learned statistics so numerical features are placed on comparable scales.

The scaler is fitted only on `X_train`.

Validation and test data are transformed using the statistics already learned from the training data.

## OneHotEncoder

`OneHotEncoder` converts categorical variables into numerical binary columns.

For example:

`anaemia`

can become:

* `anaemia_0`
* `anaemia_1`

This prevents the model from treating categories as if they had an artificial numerical order.

## Unknown categories

I used:

`handle_unknown="ignore"`

This prevents the pipeline from crashing if validation, test, or future production data contains a category that was not observed when the encoder was fitted.

An unknown category can therefore be transformed without fitting the encoder again.

## Pipeline

A `Pipeline` keeps preprocessing operations in a fixed and reproducible order.

For the numeric features, the order is:

Missing values
→ Median imputation
→ Standard scaling

For categorical features:

Missing values
→ Most-frequent imputation
→ One-hot encoding

Using pipelines is safer than manually applying separate transformations because it reduces the risk of:

* forgetting a preprocessing step,
* applying transformations in the wrong order,
* fitting a transformer on validation or test data,
* using inconsistent preprocessing between datasets.

## ColumnTransformer

`ColumnTransformer` allows different groups of columns to use different preprocessing pipelines.

Numeric features require:

* median imputation,
* standard scaling.

Categorical features require:

* most-frequent imputation,
* one-hot encoding.

`ColumnTransformer` applies these transformations to their respective columns and combines the results into one processed feature matrix.

## Fit versus transform

### Train

`X_train` uses:

`fit_transform()`

The preprocessing pipeline learns statistics and categories from the training data and then transforms it.

### Validation

`X_val` uses:

`transform()`

It uses only the preprocessing rules already learned from `X_train`.

### Test

`X_test` uses:

`transform()`

The test dataset is never used to fit the imputer, scaler, or encoder.

The rule I learned is:

Train → `fit_transform()`

Validation → `transform()`

Test → `transform()`

## Leakage proof

I confirmed that the scaler learned its statistics from the training data by extracting the fitted `StandardScaler` from the numeric pipeline.

The scaler means were:

`[61.3091285, 635.670391, 37.1229050, 265028.561, 1.31201117, 136.877095]`

I independently calculated the means of the numeric features from `X_train`.

The values matched the scaler's learned means.

I also compared them with the means from the complete dataset and found that they were different.

This demonstrates that the scaler was fitted on the training subset rather than on the full dataset.

## Missing-value stress test

The original dataset was not modified.

Instead, I created a temporary copy containing three rows from the validation dataset:

`stress_test = X_val.head(3).copy()`

I deliberately introduced missing values into:

* `age`
* `serum_creatinine`
* `diabetes`

I then used:

`preprocessor.transform(stress_test)`

I did not use `fit_transform()`.

After transformation, the number of remaining missing values was:

`0`

This demonstrated that the imputers learned from the training data could handle missing values in new data without refitting the pipeline.

Using a disposable copy was important because I did not want to modify the original dataset or permanently alter the train, validation, or test splits.

## Actual transformed shape

### Raw shapes

Train: `(179, 11)`

Validation: `(60, 11)`

Test: `(60, 11)`

### Processed shapes

Train: `(179, 16)`

Validation: `(60, 16)`

Test: `(60, 16)`

The processed datasets all contain the same 16 features in the same order.

The number of features increased from 11 to 16 because the five binary categorical variables were converted into one-hot encoded columns.

## Real error encountered

The main error I encountered was:

`NameError: name 'X_train' is not defined`

I later also encountered:

`NameError: name 'build_preprocessor' is not defined`

## Root cause

For the first error, I had created the `split_dataset()` function but had not actually called it before trying to use `X_train`, `X_val`, and `X_test`.

Defining a function only tells Python how to perform an operation. It does not execute the function.

For the second error, `main()` attempted to call:

`build_preprocessor()`

but I had not correctly defined the function containing Steps 6–9.

There was also a structural problem where some processing code was outside `main()`, causing variables to be referenced before they were created in the correct scope.

## Fix

I fixed the first problem by calling:

`split_dataset(X, y)`

and unpacking its returned values into:

* `X_train`
* `X_val`
* `X_test`
* `y_train`
* `y_val`
* `y_test`

I fixed the preprocessing structure by creating a separate:

`build_preprocessor()`

function.

This function now:

1. Creates the numeric pipeline.
2. Creates the categorical pipeline.
3. Combines them using `ColumnTransformer`.
4. Requests pandas output.
5. Returns the unfitted preprocessor.

The actual fitting and transformation are performed inside `main()`.

I also corrected the project path to:

`Path(__file__).resolve().parent.parent`

so the script correctly finds the dataset inside the `ai-engineer-journey` repository.

## Next smallest action

Day 10: attach `LogisticRegression` to the preprocessing pipeline and establish a baseline classifier.
