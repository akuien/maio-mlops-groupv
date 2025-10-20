All notable changes to this project will be documented in this file.

[v0.2] - 2025-10-20
Changed
* Model: Switched from LinearRegression to Ridge regression to introduce regularization, which can help prevent overfitting and improve generalization on unseen data.

Metrics Comparison
| Metric | v0.1 (LinearRegression) | v0.2 (Ridge) | Change      |
| :----- | :---------------------- | :----------- | :---------- |
| RMSE | 53.85                   | 53.84 | -0.02% |

Rationale: The improvement in RMSE is marginal for this dataset, but Ridge provides a more robust model foundation against potential multicollinearity in features. It's a low-cost change that aligns with best practices for building stable models.

[v0.1] - 2025-10-08
* Metric (RMSE): 53.85

Added


* Initial release of the Diabetes Triage API.
* Model: Baseline model using StandardScaler + LinearRegression.
* API: Includes /health and /predict endpoints.
* CI/CD: Full pipeline for CI (lint, test, train) and Release (build, push, release).
