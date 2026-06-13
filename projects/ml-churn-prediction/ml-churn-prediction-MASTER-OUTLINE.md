# Master Outline & Study Guide
## Machine Learning — Customer Churn Prediction (end-to-end ML pipeline + SHAP + Streamlit)

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.
>
> **One sentence to anchor everything:** This is a full ML pipeline — clean → explore →
> engineer features → train and compare 5 models → tune → explain with SHAP → deploy a
> Streamlit app — that predicts telecom customer churn, and the two ideas that run through
> *every* decision are **recall is the priority metric** and **the model must explain
> itself**.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Business Context)](#2-why-this-project-exists-business-context)
3. [Why Recall Is the Priority Metric](#3-why-recall-is-the-priority-metric)
4. [The Tech Stack](#4-the-tech-stack)
5. [The Dataset — Telco Customer Churn](#5-the-dataset--telco-customer-churn)
6. [The 6-Phase Pipeline (Architecture)](#6-the-6-phase-pipeline-architecture)
7. [Phase 1 — Data Cleaning](#7-phase-1--data-cleaning)
8. [Phase 2 — Exploratory Data Analysis](#8-phase-2--exploratory-data-analysis)
9. [Phase 3 — Feature Engineering & Preprocessing](#9-phase-3--feature-engineering--preprocessing)
10. [Phase 4 — Model Training & Comparison](#10-phase-4--model-training--comparison)
11. [Phase 5 — Hyperparameter Tuning](#11-phase-5--hyperparameter-tuning)
12. [Phase 6 — SHAP Explainability](#12-phase-6--shap-explainability)
13. [The Streamlit App](#13-the-streamlit-app)
14. [Key Results & Numbers](#14-key-results--numbers)
15. [Key Findings & Business Recommendations](#15-key-findings--business-recommendations)
16. [ML Concepts to Know Cold](#16-ml-concepts-to-know-cold)
17. [Limitations & Honest Caveats](#17-limitations--honest-caveats)
18. [Interview Q&A](#18-interview-qa)
19. [How to Walk Through This Project Live](#19-how-to-walk-through-this-project-live)
20. [Glossary](#20-glossary)

---

## 1. The 30-Second Pitch

This project is an **end-to-end machine-learning pipeline** that predicts **customer churn**
for a telecom company — built in Python across six phases, each in its own Jupyter
notebook, and finished with a deployed interactive web app.

It takes **7,000+ telecom customer records**, cleans them, explores them with seven
visualizations, engineers five new features, then **trains and compares five classification
algorithms head-to-head** — Logistic Regression, Random Forest, XGBoost, LightGBM, and SVM.
The winner is **Logistic Regression** with **0.83 AUC** and **79% recall** on the held-out
test set. Hyperparameter tuning was attempted and **deliberately rejected** — the tuned
model traded away 22 points of recall for a rounding-error AUC gain. Finally, **SHAP** is
used to explain *why* the model predicts what it predicts — both globally (which features
drive churn) and per-customer (a waterfall plot for any individual). The whole thing is
served through a **four-page Streamlit app** where anyone can score a customer profile and
get a churn probability with a live SHAP explanation.

Two themes make this more than a tutorial: **recall is the priority metric** (because a
missed churner costs far more than a false alarm), and **explainability is built in** (the
model doesn't just predict — it tells you why).

**One-line version:** "I built an end-to-end churn-prediction pipeline — five models
compared, business-aware model selection, SHAP explainability, and a deployed Streamlit
app — where every decision was driven by the cost asymmetry that makes recall the metric
that matters."

**Live app:** https://nadeaujonnyappio-ba7xf6aknjidd9ppd5ww3t.streamlit.app

---

## 2. Why This Project Exists (Business Context)

**The business problem.** Customer churn — when a customer cancels their service — is one
of the most expensive problems in any subscription business. The standard figure: acquiring
a new customer costs **5–7× more** than retaining an existing one. Telecom companies, SaaS
platforms, and streaming services all build churn-prediction models to **identify at-risk
customers *before* they leave**, so retention offers can be targeted at the right people.

**The simulated role.** The project plays a data analyst / data scientist building a churn
system for a telecom company's customer-success team. The output isn't just a model — it's
a *decision tool*: a deployed app the team can use, plus a ranked list of churn drivers
that translate directly into retention strategy.

**Why churn prediction is a classic ML portfolio project.** It exercises the entire
supervised-learning workflow on a real, messy, business-relevant problem: a binary
classification target, class imbalance, mixed data types (numeric + categorical), a clear
cost asymmetry that forces a thoughtful metric choice, and a genuine need for
explainability (a retention team won't act on a black-box score). It is the canonical
"prove you can do end-to-end ML" project — and this version does it thoroughly: six
documented phases, five models compared, a principled tuning decision, SHAP, and deployment.

**What lifts it above a tutorial — three things to emphasize in interviews:**
1. **Business-aware metric selection** — recall is chosen deliberately, with a cost
   argument behind it (§3).
2. **A principled "don't tune" decision** — tuning was run, evaluated, and *rejected*
   because it hurt the metric that matters (§11). Knowing when *not* to optimize is rarer
   than knowing how to optimize.
3. **Explainability as a first-class feature** — SHAP isn't a bonus chart; it's wired into
   the live app so every prediction comes with a reason (§12).

---

## 3. Why Recall Is the Priority Metric

**This is the single most important concept in the project. If you understand only one
thing, understand this — it justifies almost every downstream decision.**

In churn prediction, **the two kinds of error cost wildly different amounts:**

- A **false negative** = a **missed churner**. The model said "this customer will stay,"
  they actually left. Cost: a lost customer and all their future revenue — potentially
  hundreds or thousands of dollars in lifetime value.
- A **false positive** = a **false alarm**. The model said "this customer will churn,"
  they actually stayed. Cost: one unnecessary retention offer — maybe a $5–$10 discount.

The costs are **asymmetric by orders of magnitude.** Missing a churner is *far* more
expensive than a false alarm. So the model should be tuned to **catch as many real churners
as possible, even at the cost of more false alarms.**

That objective has a name: **recall** — of all the customers who *actually* churned, what
fraction did the model catch? Maximizing recall = minimizing missed churners.

**Every major decision in the project follows from this:**
- All five models use explicit **class-imbalance handling** so they don't ignore the
  minority (churn) class.
- Model selection ranks **recall first**, then AUC — not accuracy.
- Hyperparameter tuning was **rejected** specifically because it cost recall (§11).
- The project openly accepts **lower precision** (~49%) and even **lower accuracy than a
  do-nothing baseline** as the deliberate price of high recall.

**The cost math, made concrete** (from the project's own example): catching 83 extra
churners is worth far more than avoiding 187 unnecessary $10 retention offers — ~$41,500 of
saved lifetime value versus ~$1,870 of wasted offers. *That* is why recall wins.

---

## 4. The Tech Stack

| Tool | Role |
|---|---|
| **Python 3.13** | The language for the whole pipeline. |
| **Jupyter Notebook** | Each of the six phases lives in its own notebook — a clean, inspectable record. |
| **pandas / NumPy** | Data loading, cleaning, manipulation, feature engineering. |
| **scikit-learn** | Logistic Regression, Random Forest, SVM; the preprocessing pipeline (`ColumnTransformer`, `StandardScaler`, `OneHotEncoder`); `train_test_split`, stratified cross-validation, `RandomizedSearchCV`, all evaluation metrics. |
| **XGBoost** | `XGBClassifier` — gradient boosting (level-wise tree growth). |
| **LightGBM** | `LGBMClassifier` — gradient boosting (leaf-wise tree growth). |
| **SHAP** | Model explainability — `LinearExplainer` for global importance and per-customer waterfall plots. |
| **matplotlib / seaborn** | All charts — EDA, model comparison, ROC curves, confusion matrices, SHAP plots. |
| **Streamlit** | The four-page deployed web app for real-time scoring. |
| **joblib** | Serializing the model, preprocessor, and intermediate artifacts (`.pkl` files) to hand off between notebooks and the app. |
| **Streamlit Community Cloud** | Free hosting for the live app. |

**The mental model:** the notebooks are where the *building* happens (one per phase),
`joblib` `.pkl` files are the *handoff* between phases, and the Streamlit app is the
*delivery* — the trained model turned into a usable tool. Everything runs on CPU in
seconds; no GPU. `random_state=42` is set everywhere, so results are reproducible.

---

## 5. The Dataset — Telco Customer Churn

**What it is.** The **Telco Customer Churn** dataset — an **IBM sample dataset hosted on
Kaggle** (`blastchar/telco-customer-churn`). It describes **7,043 customers** of a
fictional telecom company, file `WA_Fn-UseC_-Telco-Customer-Churn.csv` (~955 KB), with **21
columns** and one row per customer.

| Property | Value |
|---|---|
| Raw dimensions | 7,043 rows × 21 columns |
| Cleaned dimensions | **7,032 rows × 20 columns** |
| Target | `Churn` (Yes/No → 1/0) — binary classification |
| Class distribution | **73.4% No churn (5,163) / 26.6% Churn (1,869)** — moderately imbalanced |

**The 21 columns group into four kinds:**
- **Demographics (5):** `customerID`, `gender`, `SeniorCitizen`, `Partner`, `Dependents`.
- **Services (10):** `tenure`, `PhoneService`, `MultipleLines`, `InternetService`,
  `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`,
  `StreamingMovies`.
- **Account (5):** `Contract`, `PaperlessBilling`, `PaymentMethod`, `MonthlyCharges`,
  `TotalCharges`.
- **Target (1):** `Churn`.

**Three dataset quirks you must know — interviewers probe these:**
1. **`TotalCharges` is stored as a string**, not a number, because 11 rows contain
   whitespace instead of a value. This is the central data-cleaning issue (§7).
2. **`SeniorCitizen` is already 0/1**, unlike every other binary column (which uses
   Yes/No strings). It gets routed to the *numeric* feature path.
3. **"No internet service" / "No phone service" are real categories, not missing data.**
   Six service columns and `MultipleLines` use them — they mean the customer doesn't have
   that base service. They were preserved as distinct categories, never dropped.

**Why the imbalance matters.** At 26.6% churn, a lazy "predict no churn for everyone" model
scores **73.4% accuracy** while catching **zero churners** — useless. This is *the* reason
accuracy is a misleading metric here and recall/AUC are used instead, and the reason every
model gets explicit class-imbalance handling.

---

## 6. The 6-Phase Pipeline (Architecture)

The project is a **structured six-phase pipeline**, each phase a notebook, each phase
producing serialized artifacts the next phase consumes.

```
  Raw CSV (7,043 × 21)
        │
        ▼
  PHASE 1 — Data Cleaning           01_data_cleaning.ipynb
  fix dtypes · drop 11 NaN rows · drop customerID · encode target
        │  → telco_churn_cleaned.csv  (7,032 × 20)
        ▼
  PHASE 2 — EDA                     02_eda.ipynb
  7 visualizations · identify churn drivers
        │  → 7 chart PNGs + documented findings
        ▼
  PHASE 3 — Feature Engineering     03_feature_engineering.ipynb
  +5 engineered features · 80/20 stratified split · preprocessing pipeline
        │  → preprocessor.pkl · feature_names.pkl · split + processed data
        ▼
  PHASE 4 — Model Training          04_model_training.ipynb
  train 5 models · 5-fold stratified CV · compare on test set
        │  → best_model.pkl (Logistic Regression) · model_comparison.csv
        ▼
  PHASE 5 — Hyperparameter Tuning   05_tuning_evaluation.ipynb
  RandomizedSearchCV (50 iter) · default-vs-tuned · DECISION: keep default
        │
        ▼
  PHASE 6 — SHAP Explainability     05_tuning_evaluation.ipynb (same notebook)
  global importance · per-customer waterfall · business translations
        │  → 3 SHAP chart PNGs
        ▼
  STREAMLIT APP                     app/app.py
  4 pages · real-time scoring · live SHAP waterfall
```

**The key architectural idea — phases hand off via serialized artifacts.** Each notebook
*saves* its outputs (cleaned CSV, fitted preprocessor, trained model, etc.) with `joblib`
or `to_csv`, and the next notebook *loads* them. Nothing is recomputed; nothing reaches
back to an earlier step's internal state. This makes each phase independently runnable and
debuggable, and it's what lets the Streamlit app load the exact same `preprocessor.pkl` and
`best_model.pkl` the notebooks produced — guaranteeing the app behaves identically to
training.

**Note on notebook count:** there are **5 notebooks for 6 phases** — Phases 5 (tuning) and
6 (SHAP) share `05_tuning_evaluation.ipynb`.

---

## 7. Phase 1 — Data Cleaning

**Notebook:** `01_data_cleaning.ipynb` · **Output:** `telco_churn_cleaned.csv` (7,032 × 20)

**Goal.** Load the raw CSV, find and fix data-quality issues, and save a clean dataset that
every downstream notebook loads (and never touches the raw file again).

**The steps:**
1. **Load and inspect** — `df.shape` (7,043 × 21) and `df.dtypes`. This immediately flagged
   the problem: `TotalCharges` had dtype `object` (string) when it should be numeric.
2. **Check nulls, duplicates, cardinality** — `isnull().sum()` reported **zero** missing
   values and zero duplicates. **This was misleading** — the real nulls in `TotalCharges`
   were whitespace strings, which `.isnull()` does not catch.
3. **Fix `TotalCharges`** — `pd.to_numeric(df['TotalCharges'], errors='coerce')` converts
   the column to float; the 11 whitespace entries become `NaN`. Investigation found a clear
   pattern: **all 11 NaN rows had `tenure = 0`** — brand-new customers with no billing
   history yet.
4. **Decide: drop vs. impute the 11 rows.** Two options: drop them, or impute
   `TotalCharges = 0`. **Drop was chosen** — 11 of 7,043 rows is **0.16%** of the data,
   negligible, and dropping avoids creating an artificial `tenure=0, TotalCharges=0` signal
   the model might latch onto.
5. **Drop `customerID`** — a unique identifier, not a predictive feature.
6. **Encode the target** — `Churn` mapped from `Yes`/`No` strings to `1`/`0` integers.
7. **Save** — `telco_churn_cleaned.csv`, 7,032 rows × 20 columns.

**The teachable point — "zero missing values" was a trap.** The whitespace-string issue is
the classic data-cleaning lesson: a `.isnull()` check passing doesn't mean the data is
clean. The dtype check (`object` where a number was expected) is what actually surfaced the
problem. Be ready to tell this story — it shows you inspect data critically, not
superficially.

---

## 8. Phase 2 — Exploratory Data Analysis

**Notebook:** `02_eda.ipynb` · **Output:** 7 chart PNGs + documented findings

**Goal.** Before any modeling, understand *which features drive churn* and which carry no
signal — and produce visualizations that document it.

**The 7 charts:** (1) overall churn distribution, (2) churn rate by contract type,
(3) tenure distribution by churn status, (4) monthly charges by churn status, (5) a 4×4
grid of churn rate across all 16 categorical features, (6) a correlation heatmap of numeric
features, (7) a tenure-vs-monthly-charges scatter colored by churn.

**The findings that mattered — these reappear all the way through to the SHAP results:**

1. **Contract type is the strongest single predictor** — and this is the chart to know
   cold: **month-to-month customers churn at 42.7%, one-year at 11.3%, two-year at just
   2.8%** — a **15× spread**.
2. **Churn is "front-loaded" by tenure** — churners cluster heavily in the **first 0–12
   months**; customers past 60 months almost never churn.
3. **Higher monthly charges correlate with churn** — churners skew toward $70–$100/month;
   retained customers cluster near $20.
4. **Fiber-optic internet customers churn more** — *despite paying more* — a hint of a
   service-quality problem, not a pricing one.
5. **Lack of support add-ons (OnlineSecurity, TechSupport) raises churn.**
6. **Electronic-check payment has higher churn** than the automatic methods.
7. **`gender` and `PhoneService` carry essentially no signal** — near-identical churn rates
   across categories.

**Correlation highlights:** `tenure` vs `Churn` = **−0.35** (strongest numeric predictor —
longer tenure, less churn); `TotalCharges` vs `tenure` = **0.83** (expected — charges
accumulate over time); `MonthlyCharges` vs `Churn` = **0.19**.

**The teachable point — EDA is a hypothesis generator.** Every one of these findings
directly shaped a later phase: front-loaded tenure → the `TenureGroup` engineered feature;
support add-ons → the `ServiceCount` feature; contract type → the top business
recommendation. EDA wasn't decoration — it set the agenda for feature engineering and was
later *independently confirmed* by SHAP (§15).

---

## 9. Phase 3 — Feature Engineering & Preprocessing

**Notebook:** `03_feature_engineering.ipynb` · **Outputs:** `preprocessor.pkl`,
`feature_names.pkl`, the train/test split, and processed data

This phase turns the clean dataset into a model-ready matrix. Three sub-steps: engineer
features, split the data, build the preprocessing pipeline.

### 9.1 The 5 engineered features

All created by a single function, `engineer_features()`, in a **shared module**
`feature_helpers.py` (see §9.4 — this is a key design decision):

| Feature | Logic | Motivated by |
|---|---|---|
| **`ServiceCount`** | Count of "Yes" across the 6 optional service columns (0–6) | More services = more switching cost = stickier customer |
| **`HasInternet`** | 1 if `InternetService` ≠ "No" | Internet/fiber customers churn more — consolidates the signal |
| **`HasPhone`** | 1 if `PhoneService` = "Yes" | Parallel base-service indicator |
| **`AvgMonthlyCharge`** | `TotalCharges / tenure` (uses `MonthlyCharges` if tenure = 0) | Captures the cost-to-loyalty ratio — churners cluster low-tenure/high-charge |
| **`TenureGroup`** | Buckets: 0–12→0, 13–24→1, 25–48→2, 49+→3 | Churn is front-loaded — bucketing captures the non-linear tenure effect |

Two features were **computed during EDA but deliberately excluded from the model**: a
string-binned `tenure_group` (redundant with raw `tenure`) and `TotalCharges/(tenure+1)`
(nearly identical to `MonthlyCharges` — would add multicollinearity). *Knowing what to
leave out is a feature-engineering skill too.*

### 9.2 The train/test split — done *before* preprocessing

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
```

→ **5,625 train / 1,407 test rows.** Two deliberate choices:
- **Split before preprocessing** — to prevent **data leakage** (§16). The scaler and
  encoder must learn *only* from training data.
- **`stratify=y`** — both train and test preserve the original 26.6% churn rate (confirmed:
  both came out to 0.2658). Critical on imbalanced data so the test set is representative.

### 9.3 The preprocessing pipeline

A scikit-learn **`ColumnTransformer`** applies two transformations in parallel:
- **`StandardScaler`** on the **9 numeric features** — rescales each to mean 0, std 1.
  Important for Logistic Regression and SVM, which are sensitive to feature scale.
- **`OneHotEncoder(drop='first', handle_unknown='ignore')`** on the **15 categorical
  features** — converts each category to binary columns.

Three design decisions worth being able to defend:
- **`drop='first'`** drops one category per feature to avoid the **dummy-variable trap**
  (perfect multicollinearity among the dummies) — and the dropped category becomes the
  interpretive **baseline** for that feature.
- **`handle_unknown='ignore'`** makes the pipeline robust in the app — an unseen category
  produces all-zeros instead of crashing.
- **Fit on train only, transform both** — `fit_transform` on train, `transform` on test —
  no test information leaks into the learned scaling/encoding.

**The shape math:** 24 features before encoding (9 numeric + 15 categorical) → **35 columns
after one-hot encoding** (9 numeric + 26 dummy columns).

### 9.4 The shared `feature_helpers.py` — train/serve consistency

`engineer_features()` lives in **one module**, and an **identical copy** sits in both
`notebooks/` and `app/`. This is the project's defense against the most common deployment
bug: the features being computed differently at training time versus serving time. One
function, one definition — change it once, it changes everywhere. (The two copies were
verified byte-identical.)

---

## 10. Phase 4 — Model Training & Comparison

**Notebook:** `04_model_training.ipynb` · **Outputs:** `best_model.pkl`, `model_comparison.csv`

**Goal.** Train **five** classification algorithms head-to-head and select a winner on
business-relevant criteria.

### 10.1 The five models — and why these five

The five span **three algorithmic families** — chosen to test whether complexity pays off:

| Model | Family | Why include it |
|---|---|---|
| **Logistic Regression** | Linear | The baseline — simple, fast, interpretable. Complex models must beat it to justify themselves. |
| **Random Forest** | Ensemble (bagging) | An ensemble of decision trees; handles non-linearity; the industry workhorse. |
| **XGBoost** | Gradient boosting | The Kaggle-winning tabular standard; level-wise tree growth. |
| **LightGBM** | Gradient boosting | Microsoft's framework; leaf-wise growth, often faster than XGBoost. |
| **SVM** | Geometric | A different mathematical approach (optimal separating hyperplane); breadth check. |

**Class-imbalance handling on every model:** `class_weight='balanced'` for Logistic
Regression, Random Forest, and SVM; **`scale_pos_weight ≈ 2.76`** (the ratio of
non-churners to churners) for XGBoost and LightGBM. These do the same job — make the model
penalize a missed minority-class (churn) case more heavily.

### 10.2 The evaluation method

Each model is run through **5-fold stratified cross-validation** on the training set
(scoring AUC), then trained on the full training set and scored on the **held-out test
set** across six metrics. Stratified folds preserve the 73/27 ratio in every fold.

### 10.3 The results — memorize this table

| Model | CV AUC | Accuracy | Precision | Recall | F1 | Test AUC |
|---|---|---|---|---|---|---|
| **Logistic Regression** | **0.8453** | 0.7242 | 0.4884 | **0.7888** | 0.6033 | **0.8344** |
| LightGBM | 0.8346 | 0.7548 | 0.5263 | 0.7754 | **0.6270** | 0.8292 |
| Random Forest | 0.8282 | **0.7861** | **0.6229** | 0.4947 | 0.5514 | 0.8170 |
| SVM | 0.8286 | 0.7257 | 0.4900 | **0.7888** | 0.6045 | 0.8151 |
| XGBoost | 0.8212 | 0.7456 | 0.5164 | 0.6738 | 0.5847 | 0.8095 |

### 10.4 The winner — Logistic Regression — and the surprise

**Logistic Regression won.** It had the **highest test AUC (0.8344)**, the **highest recall
(0.7888, tied with SVM)**, and the **highest cross-validated AUC (0.8453)** with low
variance. It tied SVM on recall but beat it on AUC — and is far more interpretable and
faster — so it was the clear choice.

**The surprise to talk about:** the project plan expected XGBoost or LightGBM to win.
Instead, **the simplest model beat the ensembles and gradient-boosters** on the two
priority metrics. The lesson: *model complexity doesn't always win.* On this dataset, with
well-engineered features, the feature→churn relationships are roughly linear — and a
well-configured logistic regression on good features is hard to beat, while being far
easier to explain and deploy.

**Why not Random Forest?** It had the *best accuracy* (0.7861) and *best precision*
(0.6229) — but the **worst recall (0.4947)**. It catches only 49% of churners — it would
let *more than half* of at-risk customers walk out undetected. High precision is worthless
if you're missing most of the churners. This is the cleanest illustration of why recall is
the metric (§3).

---

## 11. Phase 5 — Hyperparameter Tuning

**Notebook:** `05_tuning_evaluation.ipynb` (first half) · **Decision:** keep the default model

**Goal.** Try to improve the winning Logistic Regression — and, importantly, make a
*principled* decision about whether the improvement is worth taking.

**The method.** **`RandomizedSearchCV`** — 50 random parameter combinations, 5-fold
stratified CV, optimizing **AUC**. (RandomizedSearch samples random combinations rather
than exhaustively trying every one like GridSearch — far more efficient for a
multi-parameter space.) The search space covered `C` (regularization strength), `penalty`
(L1/L2), `solver`, and — critically — **`class_weight` (`balanced` vs `None`)**.

**What the tuner chose.** Best params: `C=1, penalty='l2', solver='liblinear'`, and
**`class_weight=None`** — i.e., the tuner decided to **turn off class balancing**.

**What that did — the default-vs-tuned comparison:**

| Metric | Default (balanced) | Tuned | Change |
|---|---|---|---|
| Accuracy | 0.7242 | 0.7982 | **+7.4 pp** |
| Precision | 0.4884 | 0.6347 | **+14.6 pp** |
| **Recall** | **0.7888** | 0.5668 | **−22.2 pp** |
| F1 | 0.6033 | 0.5989 | −0.4 pp |
| AUC | 0.8344 | 0.8346 | +0.0002 |

**The decision: reject the tuned model, keep the default.** The tuned model *looks* better
on accuracy and precision — the metrics people intuitively reach for — but it **lost 22
percentage points of recall** (79% → 57%) for an AUC gain of **0.0002** (a rounding error).
In churn terms, on the 374 actual churners in the test set:
- **Default model catches 295** churners (misses 79).
- **Tuned model catches only 212** (misses 162).

The tuned model generates fewer false alarms — but it **doubles the missed churners.** Per
the cost asymmetry of §3, that trade is unacceptable: avoiding ~187 needless $10 offers
(~$1,870) is not worth losing ~83 extra customers (~$41,500+ in lifetime value).

**The teachable point — this phase is the project's strongest "judgment" story.** It
demonstrates **knowing when *not* to optimize.** Blindly accepting the tuner's "best" model
(best by AUC, the thing it optimized) would have quietly wrecked the metric the business
actually cares about. The skill being shown isn't tuning — it's evaluating a tuning result
against the business objective and having the discipline to say no.

---

## 12. Phase 6 — SHAP Explainability

**Notebook:** `05_tuning_evaluation.ipynb` (second half) · **Outputs:** 3 SHAP chart PNGs

**Goal.** Make the model *explain itself* — both globally (what drives churn across all
customers) and locally (why *this one customer* got *this* score).

### 12.1 What SHAP is

**SHAP (SHapley Additive exPlanations)** comes from cooperative game theory (Shapley
values). For any single prediction, SHAP assigns **every feature an additive contribution**
showing how much it pushed the prediction away from the **base value** (the average
prediction across all customers). Positive SHAP value → pushes toward churn; negative →
pushes away. They're **additive**: base value + all SHAP values = the model's output for
that customer.

The project uses **`shap.LinearExplainer`** — the correct, exact explainer for a linear
model like Logistic Regression. SHAP values were computed for all 1,407 test customers,
giving a **(1407, 35)** matrix; the base value was **−1.0175** in log-odds space.

### 12.2 Global importance — the top SHAP features

The top features by **mean absolute SHAP value** (overall importance):

1. **`tenure`** — the #1 driver. Low tenure pushes strongly toward churn.
2. **`Contract_Two year`** — the #1 churn *reducer*. A two-year contract strongly pushes
   *away* from churn (baseline: month-to-month).
3. **`InternetService_Fiber optic`** — fiber pushes toward churn (the service-quality flag).
4. **`TotalCharges`** — higher total → away from churn (a loyalty proxy).
5. **`MonthlyCharges`** — higher monthly → toward churn.
6. **`Contract_One year`**, 7. `TenureGroup`, 8. `PaymentMethod_Electronic check`,
   9. `OnlineSecurity_Yes`, … down to `gender` which (as EDA predicted) is *not in the top
   15* at all.

Two SHAP chart types: the **beeswarm summary plot** (every customer is a dot — position
shows impact direction/magnitude, color shows whether the feature value was high or low)
and a simpler **bar plot** of mean absolute SHAP value.

### 12.3 Local explanations — the waterfall plot

The **waterfall plot** explains **one customer's prediction**, feature by feature. Starting
from the base value, each bar shows how one feature pushed that customer's score up (toward
churn, red) or down (away, blue). For the highest-risk test customer, the breakdown was:
very low `tenure` (+1.22), fiber optic (+0.59), not on a two-year contract (+0.36), in the
0–12-month `TenureGroup` (+0.30), electronic-check payment (+0.20) — partially offset by
relatively low `TotalCharges` (−0.54) and `MonthlyCharges` (−0.44).

### 12.4 Why this is the project's "crown jewel"

The waterfall plot is **generated live in the Streamlit app for every customer scored.**
The model doesn't just say "this customer is high risk" — it says *"high risk **because**
they have very low tenure, use fiber optic, aren't on a long-term contract, and pay by
electronic check."* That turns a black-box score into something a retention team can act
on — and translates directly into business recommendations (§15).

---

## 13. The Streamlit App

**File:** `app/app.py` (~240 lines) · **Deployed:** Streamlit Community Cloud (free tier)

The project ends in a **deployed, interactive four-page web app** — anyone can score a
customer and see a SHAP explanation without touching code. A live app is far more
compelling than a static notebook: it proves deployment skill and makes the work usable by
non-technical people.

### 13.1 How it loads the model

The app loads the serialized `best_model.pkl` and `preprocessor.pkl` once, wrapped in
**`@st.cache_resource`** so the load happens a single time and is reused across reruns and
sessions (Streamlit re-runs the whole script on every interaction — caching avoids
reloading the model each time). It imports the **same `feature_helpers.py`** the notebooks
used.

### 13.2 The four pages

| Page | Purpose |
|---|---|
| **1 — Predict Churn Risk** | The centerpiece. A 3-column input form (demographics / services / account) captures a customer profile, the app scores it, and shows a color-coded risk level **plus a live SHAP waterfall**. |
| **2 — Model Performance** | The 5-model comparison table (from `model_comparison.csv`), an info box explaining why Logistic Regression won, and the comparison / ROC / confusion-matrix charts. |
| **3 — Data Insights** | Key EDA charts (churn by contract, tenure histogram), the SHAP beeswarm summary, and the five business recommendations. |
| **4 — Sample Predictions** | A table of 15 test customers — actual vs. predicted vs. probability — with a red-yellow-green color gradient on the probability column. |

### 13.3 The Predict page flow (Page 1)

When the user clicks "Predict": the app builds a one-row DataFrame from the form inputs,
**auto-computes `TotalCharges` as `MonthlyCharges × tenure`**, applies the shared
`engineer_features()`, transforms with the fitted `preprocessor`, calls
`model.predict_proba()`, and renders the result:

- **≥ 50%** → **HIGH RISK** (red, `st.error`)
- **30–49%** → **MEDIUM RISK** (yellow, `st.warning`)
- **< 30%** → **LOW RISK** (green, `st.success`)

Then it builds a `shap.LinearExplainer` on the spot and renders a **waterfall plot for that
exact customer** — the same explanation type from Phase 6, generated in real time.

### 13.4 Train/serve consistency — the deployment story

The most common deployment bug is the model behaving differently in the app than in
training because features were transformed differently. The app prevents this five ways —
a strong interview talking point:

1. **`feature_helpers.py` is a shared module** — identical copy in `notebooks/` and `app/`,
   so feature engineering is byte-identical.
2. **The fitted `ColumnTransformer` is serialized** — the app reuses the *exact* scaler
   means/stds and encoder categories learned at training time.
3. **Feature column order is explicitly defined** in the same order as training.
4. **`handle_unknown='ignore'`** — an unseen category produces zeros, not a crash.
5. **`SeniorCitizen`** is converted from the Yes/No dropdown to 1/0 to match training.

### 13.5 One honest nuance

The app **derives `TotalCharges` as `MonthlyCharges × tenure`.** In the real dataset
`TotalCharges` is the *actual accumulated* total, which won't exactly equal that product
(monthly charges drift over time). It's a reasonable simplification — an app user can't be
expected to know a customer's lifetime billing total — but be ready to name it if asked:
it's a small, deliberate input approximation, not an oversight.

---

## 14. Key Results & Numbers

Memorize the headline figures.

| Metric | Value |
|---|---|
| Dataset | IBM Telco Customer Churn (Kaggle) — 7,043 → **7,032** cleaned rows |
| Class balance | 73.4% no churn / **26.6% churn** |
| Train / test split | 5,625 / 1,407 (80/20, stratified) |
| Features | 24 before encoding (9 numeric + 15 categorical) → **35 after one-hot** |
| Engineered features | 5 (ServiceCount, HasInternet, HasPhone, AvgMonthlyCharge, TenureGroup) |
| Models compared | **5** (Logistic Regression, Random Forest, XGBoost, LightGBM, SVM) |
| **Winning model** | **Logistic Regression** (`class_weight='balanced'`, `max_iter=1000`, `random_state=42`) |
| **Test AUC** | **0.8344** |
| **Test Recall** | **0.7888** — catches 79% of churners (295 of 374) |
| Test F1 | 0.6033 |
| Test Precision | 0.4884 |
| Test Accuracy | 0.7242 |
| CV AUC | 0.8453 ± 0.0187 |
| Tuning outcome | **Rejected** — tuned model lost 22 pp recall for +0.0002 AUC |
| #1 SHAP feature | `tenure` (low tenure → churn) |
| Deployment | 4-page Streamlit app on Streamlit Community Cloud |

**One number to be ready to defend: accuracy is 0.7242 — *lower* than the 73.4%
"predict-no-churn-for-everyone" baseline.** This is **not a failure** — it's the deliberate
trade. The baseline scores 73.4% accuracy with **0% recall** (catches no churners). This
model scores slightly lower accuracy but **79% recall**. For a churn problem, that is
unambiguously the better model. If an interviewer frames the accuracy as a weakness, the
answer is §3: accuracy is the wrong metric here.

---

## 15. Key Findings & Business Recommendations

**The findings** (each confirmed by *two independent methods* — raw EDA churn rates **and**
SHAP feature importance):

1. **Contract type is the strongest churn lever** — 42.7% (month-to-month) vs 2.8%
   (two-year); SHAP #2.
2. **Churn is front-loaded by tenure** — most churn in the first 12 months; SHAP #1.
3. **Fiber-optic customers churn more despite paying more** — SHAP #3; a quality/expectations gap.
4. **Support add-ons reduce churn** — OnlineSecurity (SHAP #9), TechSupport (#11).
5. **Electronic-check payment correlates with churn** — SHAP #8.
6. **The simplest model won** — Logistic Regression beat all four complex models.
7. **Tuning was rejected** — the default balanced model was kept.

**The EDA ↔ SHAP convergence is itself a finding.** EDA computed churn drivers from raw
churn rates with *no model involved*; SHAP derived them from the *trained model*. The two
independent methods produce the **same ranking** — contract, tenure, internet type,
charges, support add-ons, payment method — and both agree `gender` has no signal. That
convergence means the findings are robust, not artifacts of one method.

**The five business recommendations** (each tied to a SHAP finding):

1. **Incentivize annual contracts** — the highest-impact single lever (42.7% → 2.8% churn
   gap). Even a small discount on annual plans likely pays for itself.
2. **Focus retention on first-year customers** — onboarding, 30/60/90-day check-ins, early
   loyalty perks.
3. **Bundle OnlineSecurity and TechSupport** — they create perceived value and switching
   cost; offer them cheap or by default to at-risk segments.
4. **Investigate fiber-optic service quality** — higher churn at a higher price point is an
   experience problem, not a pricing one.
5. **Migrate electronic-check users to autopay** — automatic payment creates passive
   retention; a small incentive to switch costs less than losing the customer.

**The teachable point.** Every recommendation traces to evidence — a SHAP rank *and* an EDA
number — and each is framed as an action with an expected impact. This is the "so what"
layer that turns a model into business value.

---

## 16. ML Concepts to Know Cold

An ML interview will probe the fundamentals behind the project. Know these.

**Classification metrics — and which matters here:**
- **Accuracy** — fraction of all predictions correct. *Misleading on imbalanced data* — a
  do-nothing model scores 73.4% here.
- **Precision** — of customers *predicted* to churn, how many *actually* did. Low precision
  = many false alarms.
- **Recall (sensitivity)** — of customers who *actually* churned, how many were *caught*.
  **The priority metric** (§3). 0.7888 = 79% of churners caught.
- **F1** — the harmonic mean of precision and recall; a single balanced number.
- **ROC-AUC** — the area under the ROC curve; the probability the model ranks a random
  churner above a random non-churner. Threshold-independent overall quality. 0.5 = random,
  1.0 = perfect; this model = 0.834.
- **Confusion matrix** — the 2×2 grid of true/false positives/negatives that all the above
  are computed from.

**Class imbalance** — when one class is much rarer (26.6% churn). Handled here with
`class_weight='balanced'` (sklearn — re-weights the loss to penalize minority-class errors
more) and `scale_pos_weight` (the XGBoost/LightGBM equivalent). The project judged the
imbalance *moderate* — enough to require weighting, not extreme enough to need **SMOTE**
(synthetic oversampling).

**Data leakage** — when information from the test set (or the future) sneaks into training,
inflating results. Prevented here by **splitting before preprocessing** and **fitting the
scaler/encoder on training data only**.

**Cross-validation** — splitting training data into *k* folds, training on k−1 and
validating on the held-out fold, rotating through. **Stratified** k-fold preserves the
class ratio in each fold. Used here as **5-fold stratified CV** to estimate generalization
and stability (the ± on CV AUC).

**Train/test split & stratification** — 80/20 split; `stratify=y` keeps the churn rate
identical in both sets.

**Preprocessing** — **`StandardScaler`** (mean 0, std 1 — matters for LR and SVM);
**`OneHotEncoder`** (categories → binary columns); **`drop='first'`** avoids the
**dummy-variable trap** (perfect collinearity among dummies).

**The algorithm families** — **linear** (Logistic Regression — a weighted sum of features
through a sigmoid); **bagging ensemble** (Random Forest — many decorrelated trees, averaged);
**gradient boosting** (XGBoost, LightGBM — trees built sequentially, each correcting the
last); **geometric** (SVM — the maximum-margin separating hyperplane).

**Hyperparameter tuning** — searching for the best model settings. **`GridSearchCV`** tries
every combination; **`RandomizedSearchCV`** samples random combinations (more efficient).
Key Logistic Regression hyperparameters: **`C`** (inverse regularization strength — small C
= stronger regularization = simpler model), **`penalty`** (L1/Lasso can zero out
coefficients; L2/Ridge shrinks them).

**SHAP** — game-theory-based additive feature attributions; explains any single prediction
as base value + per-feature contributions (§12).

**Regularization** — penalizing large coefficients to prevent overfitting; controlled by
`C` and `penalty` in Logistic Regression.

---

## 17. Limitations & Honest Caveats

Volunteer these — they show ML maturity.

1. **Precision is ~49%** — about half of customers flagged as churners won't actually
   churn. This is the *deliberate* price of high recall (§3), but it is a real property: a
   retention campaign acting on the model's flags will spend roughly half its offers on
   customers who would have stayed. Acceptable only because offers are cheap relative to
   lost customers.
2. **Accuracy (0.7242) is below the naive baseline (0.734)** — by design (§14), but be
   ready to explain it rather than be caught out by it.
3. **It's a static, public sample dataset.** The IBM Telco set is a fixed snapshot of a
   *fictional* company — no concept drift, no real-world messiness beyond the one
   `TotalCharges` issue. Real churn data is harder.
4. **`Churn` is "in the last month"** — a specific, short prediction window. The model
   predicts *that*, not churn-ever or churn-next-year.
5. **The app approximates `TotalCharges`** as `MonthlyCharges × tenure` (§13.5).
6. **No threshold optimization shipped.** The app uses the default 0.5 decision threshold.
   Because recall matters, a *lower* threshold (flag more customers) could be justified —
   the project discusses threshold/precision-recall tradeoffs but ships the 0.5 default.
7. **No causal claims.** SHAP shows what the model *associates* with churn, not what
   *causes* it. "Fiber optic → churn" is a correlation flag for investigation, not proof
   fiber causes churn.
8. **Small dataset, simple problem.** 7K rows, 35 features — it trains in seconds. The
   pipeline and rigor are the transferable skills; the scale is modest.

---

## 18. Interview Q&A

Practice these out loud. Answers are written the way you'd actually speak.

**Q1. Walk me through this project end to end.**
"It's an end-to-end churn-prediction pipeline on a telecom dataset, in six phases. Phase
one cleans the raw 7,000-row data — the main issue was TotalCharges stored as a string.
Phase two is EDA — seven visualizations to find churn drivers. Phase three engineers five
new features and builds a preprocessing pipeline. Phase four trains and compares five
classification models. Phase five tunes the winner — and decides not to use the tuned
version. Phase six uses SHAP to explain the model. Then I deployed it as a four-page
Streamlit app. The winning model is Logistic Regression with 0.83 AUC and 79% recall."

**Q2. Why is recall your priority metric and not accuracy?**
"Because the errors cost wildly different amounts. A false negative — a missed churner — is
a lost customer and all their future revenue, maybe hundreds or thousands of dollars. A
false positive — flagging a loyal customer — just means one unnecessary retention offer,
maybe five or ten dollars. The costs are asymmetric by orders of magnitude, so I optimize
for catching churners, which is recall. Accuracy is actively misleading here — the data is
27% churn, so a model that predicts 'no churn' for everyone scores 73% accuracy and catches
zero churners. Useless."

**Q3. Your model's accuracy is 72%, below that 73% baseline. Isn't that bad?**
"It looks bad only if accuracy is your metric, and here it shouldn't be. That 73% baseline
catches zero churners — recall of zero. My model gives up about a point of accuracy and in
exchange catches 79% of churners. For a churn problem that's unambiguously the better
model. It's the deliberate trade-off, not a defect — and it's exactly why I report recall
and AUC, not accuracy."

**Q4. How did you handle the class imbalance?**
"The data is about 73/27, moderately imbalanced — enough to bias a model toward the
majority class, but not extreme enough to need synthetic oversampling like SMOTE. So every
model uses built-in class weighting: class_weight='balanced' for Logistic Regression,
Random Forest, and SVM, and scale_pos_weight set to the negative-to-positive ratio, about
2.76, for XGBoost and LightGBM. Both re-weight the loss so a missed churner is penalized
more heavily. And I evaluate on recall and AUC rather than accuracy."

**Q5. You compared five models — which won, and were you surprised?**
"Logistic Regression won — highest test AUC at 0.834, highest recall tied with SVM at 79%,
and the most stable cross-validated AUC. And yes, I was surprised — I expected XGBoost or
LightGBM, the usual winners on tabular data. The lesson is that complexity doesn't always
win: with well-engineered features the feature-to-churn relationships here are roughly
linear, and a properly configured logistic regression is hard to beat — plus it's far more
interpretable and faster to deploy. Random Forest actually had the best accuracy and
precision but the worst recall, under 50% — it misses more than half the churners, so it
was disqualified on the metric that matters."

**Q6. You tuned the model and then didn't use the tuned version. Why?**
"This is the part of the project I'd most want to talk about. I ran RandomizedSearchCV, 50
combinations, optimizing AUC. The tuner's 'best' model turned off class balancing — and the
result was higher accuracy and precision but recall collapsed from 79% to 57%, a 22-point
drop, for an AUC gain of 0.0002, basically nothing. In churn terms that's catching 212 of
374 churners instead of 295 — almost doubling the misses. The tuner optimized AUC, which is
what I told it to optimize, but it wrecked recall, which is what the business cares about.
So I rejected the tuned model and kept the default. The skill there isn't tuning — it's
knowing when not to."

**Q7. What is SHAP and why did you use it?**
"SHAP explains a model's predictions. It comes from game theory — for any prediction it
gives every feature an additive contribution showing how much it pushed the score toward or
away from churn, relative to the average prediction. I used it two ways. Globally, to rank
which features drive churn across all customers — tenure was number one. And locally, a
waterfall plot that explains one specific customer: this person is high-risk because of low
tenure, fiber optic, no long-term contract, electronic-check payment. That local
explanation runs live in the app, so the model doesn't just score a customer — it tells the
retention team why."

**Q8. How did you prevent data leakage?**
"Two things. I split the data into train and test before any preprocessing — so the test
set is genuinely held out. And the scaler and one-hot encoder are fit on the training data
only; the test set is just transformed with the parameters learned from training. If I'd
fit the scaler on the full dataset, test-set statistics would leak into training and inflate
my results."

**Q9. Walk me through your feature engineering.**
"I engineered five features from domain reasoning, each motivated by an EDA finding.
ServiceCount counts how many optional add-ons a customer has — more services means more
switching cost. HasInternet and HasPhone are binary base-service flags. AvgMonthlyCharge is
total charges over tenure — a cost-to-loyalty ratio. And TenureGroup buckets tenure into
four bins, because EDA showed churn is heavily front-loaded in the first year — bucketing
captures that non-linearity. Critically, the feature logic lives in one shared module,
feature_helpers.py, used by both the training notebooks and the app — so features are
computed identically at train time and serve time."

**Q10. How did you make sure the deployed app behaves like training?**
"Train/serve consistency was a deliberate focus. The feature engineering is one shared
module copied identically into the app. The preprocessing pipeline — the fitted
ColumnTransformer — is serialized with joblib, so the app reuses the exact scaler
statistics and encoder categories from training. Feature column order is explicitly defined
to match. And the encoder uses handle_unknown='ignore', so if an app user enters an
unusual category combination it produces zeros instead of crashing."

**Q11. Why one-hot encoding with drop='first'?**
"One-hot turns each categorical column into binary columns. drop='first' drops one category
per feature — that avoids the dummy-variable trap, where the dummy columns are perfectly
collinear because they always sum to one, which is a problem for linear models. The dropped
category just becomes the baseline you interpret the others against — for Contract, for
example, month-to-month is the baseline, so the SHAP value for Contract_Two year is the
effect relative to month-to-month."

**Q12. What does an AUC of 0.83 actually mean?**
"AUC is the area under the ROC curve. Concretely it's the probability that the model gives
a randomly chosen actual churner a higher risk score than a randomly chosen non-churner.
0.5 is random guessing, 1.0 is perfect. 0.83 means that 83% of the time the model correctly
ranks a churner above a non-churner — solid discriminative ability. And it's
threshold-independent, which is why I used it as the overall quality metric alongside
recall."

**Q13. How would you improve or extend this project?**
"A few directions. I'd tune the decision threshold — the app uses 0.5, but since recall
matters I could lower it to flag more customers, and I'd pick the threshold from a
precision-recall curve tied to the actual cost of an offer versus a lost customer. I'd add
calibration so the probabilities are trustworthy. With real data I'd retrain on a rolling
window to handle concept drift. And I'd close the loop — track whether customers the model
flagged actually churned, and whether retention offers worked."

**Q14. The dataset only had one real data-quality issue. Walk me through it.**
"TotalCharges came in as a string instead of a number. The trap was that a missing-value
check passed — zero nulls — because the bad entries were whitespace strings, which
isnull() doesn't catch. The dtype check is what flagged it: an object column where I
expected a number. Converting with pd.to_numeric and errors='coerce' turned the 11
whitespace entries into real NaNs, and all 11 turned out to be tenure-zero customers — brand
new, no billing history. I dropped them — 11 of 7,000 rows, 0.16%, negligible — rather than
impute, to avoid creating an artificial tenure-zero, charges-zero signal."

**Q15. What's the single most important takeaway from this project?**
"That the metric has to match the business problem, and you have to have the discipline to
hold that line. Recall — catching churners — is what matters here because of the cost
asymmetry. That one principle drove everything: class weighting on every model, ranking
models by recall, and most of all rejecting a tuned model that looked better on accuracy
but quietly halved how many churners it caught. A model that's technically 'optimized' but
optimized for the wrong thing is worse than a simpler one aimed at the right thing."

---

## 19. How to Walk Through This Project Live

If asked to screen-share, use this order:

1. **Open the live Streamlit app first.** Lead with the *outcome* — fill in a customer
   profile on the Predict page, show the color-coded risk score and the live SHAP
   waterfall. Let them see the model explain itself.
2. **State the thesis** — "recall is the priority metric because a missed churner costs far
   more than a false alarm" (§3). This frames everything else.
3. **Show the pipeline** — the six phases, each a notebook, each handing off serialized
   artifacts.
4. **Walk Phase 1's data-cleaning catch** — the TotalCharges string / hidden-whitespace-NaN
   story. Quick, but it shows you inspect data critically.
5. **Show the model comparison table** (Phase 4) — five models, and narrate *why Logistic
   Regression won on recall and AUC* and why Random Forest's 49% recall disqualified it.
6. **Tell the tuning story** (Phase 5) — this is the strongest judgment moment: ran the
   tuning, it cost 22 points of recall, rejected it. "Knowing when not to optimize."
7. **Show SHAP** (Phase 6) — global importance (tenure #1) and a waterfall, and note EDA
   and SHAP independently agree on the drivers.
8. **Close on business recommendations** — incentivize annual contracts, focus on
   first-year customers. End on the decision, not the code.

**Pacing tip:** spend the most time on the recall/cost-asymmetry argument (§3), the
model-comparison reasoning (§10), and the tuning-rejection decision (§11). Those three show
ML *judgment* — which is what separates this from a tutorial. The cleaning and EDA are
quick to cover.

---

## 20. Glossary

- **Churn** — a customer cancelling their service; the prediction target (here, "in the
  last month").
- **Binary classification** — predicting one of two classes (churn / no churn).
- **Class imbalance** — one class much rarer than the other (26.6% churn here).
- **`class_weight='balanced'`** — sklearn setting that re-weights the loss to penalize
  minority-class errors more.
- **`scale_pos_weight`** — the XGBoost/LightGBM equivalent; set to the negative-to-positive
  ratio (≈2.76).
- **SMOTE** — synthetic minority oversampling; *not* used here (imbalance judged moderate).
- **Recall (sensitivity)** — of actual churners, the fraction caught. **The priority metric.**
- **Precision** — of predicted churners, the fraction that actually churned.
- **F1** — harmonic mean of precision and recall.
- **Accuracy** — fraction of all predictions correct; misleading under class imbalance.
- **ROC-AUC** — area under the ROC curve; probability the model ranks a random churner
  above a random non-churner. 0.5 = random, 1.0 = perfect.
- **Confusion matrix** — the 2×2 grid of true/false positives and negatives.
- **False negative** — a missed churner (the expensive error here).
- **False positive** — a false alarm (the cheap error here).
- **Cost asymmetry** — the two error types costing very different amounts; the project's
  central justification for prioritizing recall.
- **Cross-validation** — rotating train/validate folds to estimate generalization; here
  **5-fold stratified**.
- **Stratified** — preserving the class ratio in each split/fold.
- **Data leakage** — test/future information contaminating training; prevented by splitting
  before preprocessing.
- **Feature engineering** — creating new predictive columns from existing data (here, 5).
- **`StandardScaler`** — rescales a numeric feature to mean 0, std 1.
- **`OneHotEncoder`** — converts a categorical column into binary indicator columns.
- **`drop='first'`** — drops one dummy per feature to avoid the dummy-variable trap.
- **Dummy-variable trap** — perfect multicollinearity among one-hot columns.
- **`ColumnTransformer`** — sklearn tool applying different preprocessing to different
  column groups.
- **Logistic Regression** — a linear classifier; weighted feature sum through a sigmoid.
- **Random Forest** — a bagging ensemble of decision trees.
- **XGBoost / LightGBM** — gradient-boosting frameworks; sequential trees that correct
  prior errors.
- **SVM** — Support Vector Machine; finds the maximum-margin separating hyperplane.
- **Hyperparameter tuning** — searching for the best model settings.
- **`RandomizedSearchCV`** — samples random hyperparameter combinations (vs. GridSearch's
  exhaustive grid).
- **`C` / `penalty`** — Logistic Regression hyperparameters: inverse regularization
  strength, and regularization type (L1/L2).
- **Regularization** — penalizing large coefficients to curb overfitting.
- **SHAP** — SHapley Additive exPlanations; game-theory-based per-feature attributions for
  any prediction.
- **Beeswarm / waterfall plot** — SHAP's global (all customers) and local (one customer)
  visualizations.
- **`joblib` / `.pkl`** — Python serialization; how the model, preprocessor, and artifacts
  are saved and handed between phases.
- **Train/serve consistency** — guaranteeing features are transformed identically at
  training and prediction time.
- **`@st.cache_resource`** — Streamlit decorator that loads the model once and reuses it.

---

*This study guide documents the project as built. The authoritative references are the five
notebooks in `notebooks/`, the shared `feature_helpers.py`, the Streamlit app `app/app.py`,
the serialized `best_model.pkl` / `preprocessor.pkl`, and the portfolio page `index.md`.
When this guide and the source disagree, the source wins.*