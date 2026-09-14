# Capstone Project 1 — Data Analytics & Machine Learning Dashboard

**Days 269–270.** A complete analytics + machine-learning product on the Olist Brazilian e-commerce dataset:
SQL → pandas → statistics → EDA → feature engineering → the full model zoo → business dashboard → executive story.

## Business question

> Which customers will not order again in the next 90 days, and what is the revenue impact of contacting them?

This is deliberately a **decision**, not a topic. Everything below exists to support that decision.

## Deliverable checklist

| # | Artefact | Where | Days that build it |
|---|---|---|---|
| 1 | Problem statement with owner, population, baseline, target, horizon | `docs/problem_statement.md` | 3 |
| 2 | Data dictionary (tables, columns, types, missingness, definitions) | `docs/data_dictionary.md` | 3, 51 |
| 3 | SQL layer: staging views + analytical queries | `sql/*.sql` | 135–150 |
| 4 | Cleaning + validation with quarantine report | `src/clean.py` | 56–61, 146 |
| 5 | EDA notebook: distributions, cohorts, correlations | `notebooks/01_eda.ipynb` | 52–70, 71–88 |
| 6 | Feature engineering table (RFM, tenure, frequency trends, delivery experience) | `src/features.py` | 69–70 |
| 7 | Leak-free preprocessing + training pipeline | `src/train.py` | 167–169, 195 |
| 8 | Model comparison across the canonical collections | `reports/model_comparison.md` | 165–196 |
| 9 | Chosen model + threshold justification with error costs | `reports/model_card.md` | 193–196 |
| 10 | Dashboard (Power BI **or** Tableau **or** Streamlit) | `dashboard/` | 155–164, 259 |
| 11 | Executive summary (one page, decision-first) | `reports/executive_summary.md` | 79, 270 |
| 12 | README a recruiter can skim in 60 seconds | this file | 273 |

## Data

The Olist dataset ships as nine relational tables (orders, order items, customers, payments, reviews, products,
sellers, geolocation, category translation). Load it into SQLite/Postgres and **do the joins in SQL first** —
that is exactly the skill Days 135–150 build, and it is what interviewers probe.

If the raw files are unavailable in your environment, `resources/datasets_for_practice/Sample_Superstore.xlsx`
(superstore orders) is an acceptable substitute for the dashboard half of the project, and
`resources/datasets_for_practice/titanic.csv` / `diamonds.csv` for the modelling half. Document the substitution.

## Architecture

```
raw CSVs ──► SQL staging views ──► clean/validate ──► features (RFM + delivery) ──► train/eval ──► model + card
                                        │                                              │
                                        └──────► BI extracts (CSV/Parquet) ──► dashboard ──► executive summary
```

## Model zoo to run (from the curriculum)

Regression (delivery time / revenue): Linear, Ridge, Lasso, Elastic Net, Polynomial, SVR, Decision Tree,
Random Forest, Gradient Boosting, AdaBoost, XGBoost, LightGBM, CatBoost, Bayesian, Poisson.
Classification (repeat purchase): Logistic, KNN, Naive Bayes, Decision Tree, Random Forest, SVM, Gradient
Boosting, AdaBoost, XGBoost, LightGBM, CatBoost.
Unsupervised (customer segments): K-Means, Hierarchical, DBSCAN, OPTICS, GMM, PCA, SVD, t-SNE, UMAP.

Report **all** of them in one cross-validated table with confidence intervals — the point is disciplined
comparison, not chasing a leaderboard.

## Non-negotiables

1. **No leakage**: fit every scaler/encoder inside a pipeline on training folds only.
2. **Time-aware validation**: split by order date, never randomly, for anything temporal.
3. **Cost-aware threshold**: choose the operating point from false-positive vs false-negative costs.
4. **Reproducibility**: fixed seed, pinned environment, one command to regenerate every artefact.
5. **Interpretability**: permutation importance plus SHAP for the final model, with the top drivers explained in business language.
6. **Honest reporting**: state what the model cannot do (no causal claims from observational data).

## Run it

```bash
python -m pip install -r ../.../requirements.txt      # pandas, scikit-learn, xgboost, lightgbm, catboost, shap
python src/clean.py --input data/raw --output data/processed
python src/features.py --input data/processed --output data/features.parquet
python src/train.py --features data/features.parquet --models all --report reports/
```

## Grading rubric (100 points)

| Criterion | Points |
|---|---|
| Problem framing with baseline and decision owner | 10 |
| SQL layer quality (joins, CTEs, window functions, correctness) | 15 |
| Cleaning + validation with documented quarantine counts | 10 |
| EDA that changes a decision (not decoration) | 10 |
| Feature engineering justified by domain reasoning | 10 |
| Model comparison breadth + correct CV methodology | 15 |
| Threshold/metric choice tied to error costs | 10 |
| Dashboard clarity and interactivity | 10 |
| Executive summary + repo presentation | 10 |
