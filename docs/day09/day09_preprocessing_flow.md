		   Dataset
		      ↓
	     Separate X and y
		      ↓
	        Leakage audit
		      ↓
	  Train / Validation / Test
		      ↓
                  TRAIN ONLY
                      │
          ┌───────────┴───────────┐
          │                       │
       Numeric               Categorical
          │                       │
   Median Imputer        Most-Frequent Imputer
          │                       │
   StandardScaler          OneHotEncoder
          │                       │
          └───────────┬───────────┘
                      │
              ColumnTransformer
                      │
             FIT on TRAIN only
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
       Train       Validation     Test
   fit_transform    transform    transform


## Leakage rule

Validation and test data are never used to fit imputers, scalers or encoders.

The fitted preprocessing object learns statistics and categories from the
training subset only and applies those learned transformations unchanged to
validation and test data.