LOGISTICS DELAY PREDICTION Machine Learning for Operational Risk
Management

PROJECT OVERVIEW

This project develops a machine learning model to predict operational
delays in logistics processes and optimize critical alert thresholds.

The goal is not only to estimate delay in minutes, but to transform
predictions into actionable operational decisions.

This simulation replicates a real-world logistics environment where
predictive analytics can reduce risk, improve responsiveness, and
enhance resource allocation.



PROBLEM STATEMENT

In logistics operations, delays generate:

-   Operational congestion
-   Resource misallocation
-   Increased costs
-   Service-level deterioration

The challenge is twofold:

1.  Predict expected delay (regression problem)
2.  Detect critical delays early enough to trigger preventive action



METHODOLOGY

1)  Data Preparation

-   Synthetic dataset simulating 24-hour logistics activity
-   Temporal variables (hour of day)
-   Categorical variables (company, operation type, load type)
-   Target variable: delay in minutes

2)  Exploratory Data Analysis (EDA)

Key insights discovered:

-   Delay increases significantly after 18:00
-   Certain companies show structurally higher operational risk
-   Delay distribution is right-skewed with extreme outliers

These findings justified the use of non-linear models.

3)  Models Evaluated

-   Linear Regression
-   Random Forest
-   XGBoost (Selected Model)



MODEL PERFORMANCE

Best Model: XGBoost

MAE: approximately 11.6 minutes R2 : approximately 0.57

The model explains approximately 57 percent of delay variability and
predicts with an average error close to 12 minutes.



CRITICAL DELAY DETECTION

Beyond regression, a binary operational classification was implemented.

Default threshold: 30 minutes Optimized threshold: 27 minutes

Results:

-   Recall at 30 minutes: approximately 0.62
-   Recall at 27 minutes: approximately 0.70

Lowering the threshold improved early detection of critical delays while
maintaining acceptable precision.

This demonstrates how predictive modeling can directly support
operational policy decisions.



OPERATIONAL IMPACT METRIC

An additional impact indicator was developed:

Impact = Delay Frequency × Average Delay Severity

This allows prioritization of high-risk companies by combining:

-   How often delays occur
-   How severe those delays are

The result is a risk-based ranking for operational intervention.



TECH STACK

-   Python
-   Pandas
-   Scikit-learn
-   XGBoost
-   Matplotlib



PROJECT STRUCTURE

logistics-ml/

data/ -> Synthetic dataset Notebook/ -> Model development and evaluation
requirements.txt -> Dependencies README.txt



FUTURE IMPROVEMENTS

-   Hyperparameter tuning
-   Cross-validation refinement
-   SHAP for model interpretability
-   Real cost-based impact estimation
-   Deployment as interactive dashboard

------------------------------------------------------------------------

LICENSE

MIT License

Copyright (c) 2026 Paulo Baeza

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
