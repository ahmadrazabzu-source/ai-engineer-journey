# Machine Learning Leakage Checklist

## 1. Problem definition

- [ ] Is the exact prediction target defined?
- [ ] Is the prediction time defined?
- [ ] Is the intended user/use case defined?
- [ ] Do I know which information exists at prediction time?

## 2. Target separation

- [ ] Is the target excluded from X?
- [ ] Are there features that directly encode the target?
- [ ] Are there proxy variables that effectively reveal the target?

## 3. Future information

- [ ] Was every feature available at prediction time?
- [ ] Does any feature contain post-outcome information?
- [ ] Does any variable summarize events occurring after prediction time?

## 4. Dataset splitting

- [ ] Was the data split before learned preprocessing?
- [ ] Are train, validation and test sets mutually separated?
- [ ] Is the split reproducible?
- [ ] For classification, did I consider stratification?

## 5. Entity leakage

- [ ] Could the same patient/user/entity occur in multiple splits?
- [ ] Could duplicate records occur across splits?
- [ ] Should I use group-based splitting instead of row-level splitting?

## 6. Temporal leakage

- [ ] Does time order matter?
- [ ] Could training data contain information from after evaluation examples?
- [ ] Should the split be chronological?

## 7. Preprocessing leakage

- [ ] Are imputers fitted only on training data?
- [ ] Are scalers fitted only on training data?
- [ ] Are encoders fitted only on training data?
- [ ] Is feature selection performed only from training data?
- [ ] Is dimensionality reduction fitted only on training data?

## 8. Evaluation leakage

- [ ] Is validation used for development decisions?
- [ ] Is the test set protected from model selection?
- [ ] Have I avoided repeatedly tuning after looking at test performance?
- [ ] Are final metrics calculated only after decisions are frozen?

## Decision

- [ ] I can explain why every model feature would be available during real inference.

This checklist is grounded in the core leakage rule from scikit-learn: keep train/test separated and never learn transformations from test data.