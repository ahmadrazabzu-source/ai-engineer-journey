# Day 8 Learning Log

## Purpose

Learn how an ML project should be designed before training any model.

## Supervised learning

Learning from labeled examples where the model is given both the input clues ($X$) and the correct answers ($y$) so it can learn a mathematical function to predict answers for new, unseen inputs.

## Unsupervised learning

Finding hidden patterns, groupings, or structures in data ($X$) without being given any target labels ($y$) or explicit correct answers.

## Features

$X$ represents the matrix of input variables, attributes, or clues available to the model at prediction time.

## Label

$y$ represents the target column—the specific outcome or answer key we want the model to predict.

## Prediction-time definition

My hypothetical prediction time is:

Baseline (the moment a patient first presents at the clinic).

## Leakage example from today's dataset

The `time` variable represents follow-up duration. For my hypothetical baseline-prediction use case, this information would not yet exist at prediction time, so I excluded it.

## Train set

Used to fit model parameters and allow the algorithm to learn patterns from the data (60% of total data).

## Validation set

Used to compare models, tune hyperparameters, and make development decisions during training without peeking at the test set (20% of total data).

## Test set

Used strictly for the final, independent score after all model decisions are frozen. It must be protected to prevent data leakage and indirect overfitting.

## Split used

- Train: 60%
- Validation: 20%
- Test: 20%

## Class proportions

- Train positive rate: ~32.1% (`death_event = 1`)
- Validation positive rate: ~32.1%
- Test positive rate: ~32.1%

## Leakage categories I can identify

- Target leakage
- Future-information leakage
- Preprocessing leakage
- Duplicate/entity leakage
- Temporal leakage
- Test-set tuning leakage

## Most important rule I learned

The test set is not development data; all learned preprocessing, feature choices, and model fitting must rely exclusively on training data.

## Real confusion/error

1. Differentiating Leakage Type 1 (target directly inside $X$) from Leakage Type 2 (future variables like `time` that do not exist at baseline).
2. Encountering `no changes added to commit` in Git when trying to commit before staging files with `git add`.

## How I resolved it

1. Learned the 3-Question Shield: What are we predicting? When are we predicting it? What exists at that exact moment?
2. Used `git add .` to properly stage untracked files into the Git repository before running `git commit`.

## Next smallest action

Day 9: build leakage-safe preprocessing with Pipeline and ColumnTransformer.