---
layout: default
title: "Machine Learning — Customer Churn Prediction"
description: "End-to-end ML pipeline: 5 classification models, hyperparameter tuning, SHAP explainability, and a Streamlit churn risk scoring app."
---

<a href="/projects/" class="back-to-projects btn" aria-label="Back to projects page">&larr; Back to Projects</a>

# Machine Learning &mdash; Customer Churn Prediction

> End-to-end ML pipeline that cleans, explores, and models 7,000 telecom customer records to predict churn &mdash; comparing 5 classification algorithms, explaining predictions with SHAP, and deploying an interactive Streamlit app for real-time risk scoring.

**Tools:** Python &middot; pandas &middot; NumPy &middot; scikit-learn &middot; XGBoost &middot; LightGBM &middot; SHAP &middot; matplotlib &middot; seaborn &middot; Streamlit &middot; Jupyter Notebook

**Live App:** <a href="https://nadeaujonnyappio-ba7xf6aknjidd9ppd5ww3t.streamlit.app" target="_blank">Launch Streamlit Churn Predictor &rarr;</a>

---

<details class="dropdown-section">
  <summary><strong>Project Overview</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Overview</h3>
  <p>
    This project builds an end-to-end machine learning pipeline that cleans, explores, and models 7,000 telecom
    customer records to predict churn &mdash; comparing five classification algorithms head-to-head, explaining
    predictions with SHAP values, and deploying an interactive Streamlit web app for real-time risk scoring.
    The pipeline spans six phases: data cleaning, exploratory data analysis, feature engineering &amp; preprocessing,
    model training &amp; comparison, hyperparameter tuning, and SHAP explainability &mdash; each implemented in
    dedicated Jupyter notebooks with all artifacts saved for downstream consumption.
  </p>
  <p>
    The final deployed model is a <strong>Logistic Regression classifier</strong> (class_weight='balanced') achieving
    <strong>0.83 AUC</strong> and <strong>79% recall</strong> on the held-out test set. The model is served through a
    four-page Streamlit application where users can input any customer profile and receive a churn probability score
    with a SHAP waterfall explanation showing exactly which features drove that prediction.
  </p>

  <h3>Business Context</h3>
  <p>
    Customer churn &mdash; when a customer cancels their service &mdash; is one of the most expensive problems in
    subscription businesses. Acquiring a new customer costs 5&ndash;7&times; more than retaining an existing one.
    Telecom companies, SaaS platforms, streaming services, and any company with recurring revenue build churn
    prediction models to identify at-risk customers before they leave, target retention offers to the right people,
    quantify the financial impact of churn reduction, and understand which factors drive customer attrition.
  </p>
  <p>
    This project simulates the role of a data analyst or data scientist tasked with building a churn prediction
    system for a telecom company's customer success team. The dataset comes from IBM's Telco Customer Churn sample
    on Kaggle &mdash; 7,043 customers with 21 attributes covering demographics, service subscriptions, account
    details, and churn status.
  </p>

  <h3>Why Recall Is the Priority Metric</h3>
  <p>
    In churn prediction, the costs of errors are asymmetric. A <strong>false negative</strong> (missed churner) means
    a lost customer and lost lifetime revenue. A <strong>false positive</strong> (flagging a loyal customer) means
    sending an unnecessary retention offer &mdash; a much cheaper mistake. This cost asymmetry means we optimize for
    <strong>recall</strong>: catching as many actual churners as possible, even if it means generating some false alarms.
    Every model in this project handles class imbalance explicitly (via <code>class_weight='balanced'</code> or
    <code>scale_pos_weight</code>), and model selection prioritizes recall alongside AUC.
  </p>

  <h3>Pipeline Architecture</h3>
  <p>
    The project follows a structured six-phase pipeline, each phase in its own Jupyter notebook with shared
    utilities in a dedicated Python module:
  </p>

  <table>
    <thead>
      <tr><th>Phase</th><th>Notebook</th><th>Purpose</th><th>Key Output</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>1 &mdash; Data Cleaning</td>
        <td><code>01_data_cleaning.ipynb</code></td>
        <td>Load, inspect, fix dtypes, handle NaNs, encode target</td>
        <td><code>telco_churn_cleaned.csv</code></td>
      </tr>
      <tr>
        <td>2 &mdash; EDA</td>
        <td><code>02_eda.ipynb</code></td>
        <td>7 visualizations, churn driver identification</td>
        <td>7 chart PNGs, documented findings</td>
      </tr>
      <tr>
        <td>3 &mdash; Feature Engineering</td>
        <td><code>03_feature_engineering.ipynb</code></td>
        <td>5 engineered features, preprocessing pipeline, train/test split</td>
        <td><code>preprocessor.pkl</code>, <code>feature_names.pkl</code></td>
      </tr>
      <tr>
        <td>4 &mdash; Model Training</td>
        <td><code>04_model_training.ipynb</code></td>
        <td>Train 5 models, cross-validate, compare on test set</td>
        <td><code>best_model.pkl</code>, <code>model_comparison.csv</code></td>
      </tr>
      <tr>
        <td>5 &mdash; Tuning</td>
        <td><code>05_tuning_evaluation.ipynb</code></td>
        <td>RandomizedSearchCV (50 iterations), default vs tuned comparison</td>
        <td>Decision: keep default balanced model</td>
      </tr>
      <tr>
        <td>6 &mdash; SHAP</td>
        <td><code>05_tuning_evaluation.ipynb</code></td>
        <td>Global importance, waterfall explanations, business translations</td>
        <td>3 SHAP chart PNGs</td>
      </tr>
    </tbody>
  </table>

  <h3>Key Code: Shared Feature Engineering Function</h3>
  <p>
    Feature engineering must be identical between training notebooks and the deployed Streamlit app. To guarantee
    consistency, all feature logic lives in a single shared function in <code>feature_helpers.py</code>, used by
    both the notebooks and the app:
  </p>

  <pre><code class="language-python">def engineer_features(df):
    """
    Apply all feature engineering transformations.
    Single source of truth — used by BOTH training notebooks and Streamlit app.
    """
    df = df.copy()
    service_cols = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                    'TechSupport', 'StreamingTV', 'StreamingMovies']
    df['ServiceCount'] = df[service_cols].apply(
        lambda row: (row == 'Yes').sum(), axis=1
    )
    df['HasInternet'] = (df['InternetService'] != 'No').astype(int)
    df['HasPhone'] = (df['PhoneService'] == 'Yes').astype(int)
    df['AvgMonthlyCharge'] = df.apply(
        lambda row: row['TotalCharges'] / row['tenure'] if row['tenure'] > 0
        else row['MonthlyCharges'], axis=1
    )
    def tenure_bucket(t):
        if t <= 12: return 0
        elif t <= 24: return 1
        elif t <= 48: return 2
        else: return 3
    df['TenureGroup'] = df['tenure'].apply(tenure_bucket)
    return df</code></pre>

  <h3>Key Code: Preprocessing Pipeline</h3>
  <p>
    The preprocessing pipeline uses scikit-learn's <code>ColumnTransformer</code> to apply <code>StandardScaler</code>
    to 9 numeric features and <code>OneHotEncoder</code> (with <code>drop='first'</code> to avoid the dummy variable
    trap) to 15 categorical features. The pipeline is fit on training data only, then applied to both train and test
    sets to prevent data leakage:
  </p>

  <pre><code class="language-python">from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

numeric_features = ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges',
                    'ServiceCount', 'HasInternet', 'HasPhone', 'AvgMonthlyCharge',
                    'TenureGroup']

categorical_features = ['gender', 'Partner', 'Dependents', 'PhoneService',
                        'MultipleLines', 'InternetService', 'OnlineSecurity',
                        'OnlineBackup', 'DeviceProtection', 'TechSupport',
                        'StreamingTV', 'StreamingMovies', 'Contract',
                        'PaperlessBilling', 'PaymentMethod']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(drop='first', sparse_output=False,
                              handle_unknown='ignore'), categorical_features)
    ]
)

# Fit on training data ONLY — transform both
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)</code></pre>

  <h3>Key Code: 5-Model Training &amp; Cross-Validation</h3>
  <p>
    Five classification algorithms &mdash; covering linear, ensemble, gradient boosting, and geometric model
    families &mdash; are trained and evaluated with 5-fold stratified cross-validation. All five models include
    explicit class imbalance handling:
  </p>

  <pre><code class="language-python">from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.svm import SVC

# Class weight ratio for gradient boosting models
pos_weight = y_train.value_counts()[0] / y_train.value_counts()[1]  # ≈ 2.76

models = {
    'Logistic Regression': LogisticRegression(
        class_weight='balanced', max_iter=1000, random_state=42
    ),
    'Random Forest': RandomForestClassifier(
        class_weight='balanced', n_estimators=100, random_state=42
    ),
    'XGBoost': XGBClassifier(
        scale_pos_weight=pos_weight, n_estimators=100,
        random_state=42, eval_metric='logloss'
    ),
    'LightGBM': LGBMClassifier(
        scale_pos_weight=pos_weight, n_estimators=100,
        random_state=42, verbose=-1
    ),
    'SVM': SVC(
        class_weight='balanced', probability=True, random_state=42
    ),
}

# 5-fold stratified cross-validation per model
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for name, model in models.items():
    cv_auc = cross_val_score(model, X_train_processed, y_train,
                              cv=cv, scoring='roc_auc')
    print(f"{name}: AUC={cv_auc.mean():.4f} (±{cv_auc.std():.4f})")</code></pre>

  <h3>Key Code: Hyperparameter Tuning (RandomizedSearchCV)</h3>
  <p>
    After Logistic Regression was identified as the best model, hyperparameter tuning was performed using
    <code>RandomizedSearchCV</code> with 50 random combinations across 5 CV folds, optimizing for AUC:
  </p>

  <pre><code class="language-python">from sklearn.model_selection import RandomizedSearchCV

param_dist = {
    'C': [0.001, 0.01, 0.1, 0.5, 1, 5, 10, 50, 100],
    'penalty': ['l1', 'l2'],
    'solver': ['liblinear', 'saga'],
    'class_weight': ['balanced', None],
    'max_iter': [1000]
}

search = RandomizedSearchCV(
    LogisticRegression(random_state=42),
    param_distributions=param_dist,
    n_iter=50, scoring='roc_auc',
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    random_state=42, n_jobs=-1
)
search.fit(X_train_processed, y_train)
# Best CV AUC: 0.8459</code></pre>

  <h3>Key Code: SHAP Explainability</h3>
  <p>
    SHAP (SHapley Additive exPlanations) values are computed for all 1,407 test set customers using
    <code>LinearExplainer</code>. The beeswarm summary plot shows global feature importance with direction
    of impact, and waterfall plots explain individual predictions feature-by-feature:
  </p>

  <pre><code class="language-python">import shap

# Create explainer for logistic regression
explainer = shap.LinearExplainer(model, X_train_processed,
                                  feature_names=all_feature_names)
shap_values = explainer.shap_values(X_test_processed)

# Global importance — beeswarm summary plot
shap.summary_plot(shap_values, X_test_processed,
                  feature_names=all_feature_names, show=False)
plt.savefig('outputs/figures/shap_summary.png', dpi=150, bbox_inches='tight')

# Individual explanation — waterfall for highest-risk customer
high_risk_idx = y_prob_final.argmax()
explanation = shap.Explanation(
    values=shap_values[high_risk_idx],
    base_values=explainer.expected_value,
    data=X_test_processed[high_risk_idx],
    feature_names=all_feature_names
)
shap.waterfall_plot(explanation, max_display=10, show=False)
plt.savefig('outputs/figures/shap_waterfall_example.png', dpi=150,
            bbox_inches='tight')</code></pre>

  <h3>Key Code: Streamlit Prediction Pipeline</h3>
  <p>
    The deployed Streamlit app loads the serialized model and preprocessor, accepts customer attribute inputs,
    engineers features using the same shared function, and produces a churn probability with a SHAP waterfall
    explanation:
  </p>

  <pre><code class="language-python"># Load serialized artifacts
model = joblib.load('best_model.pkl')
preprocessor = joblib.load('preprocessor.pkl')

# User submits customer attributes via Streamlit form...
# Build DataFrame from inputs, auto-compute TotalCharges
input_data['TotalCharges'] = input_data['MonthlyCharges'] * input_data['tenure']

# Apply shared feature engineering (identical to training)
input_engineered = engineer_features(input_data)
input_final = input_engineered[numeric_features + categorical_features]

# Preprocess and predict
input_processed = preprocessor.transform(input_final)
churn_prob = model.predict_proba(input_processed)[0][1]

# Generate per-prediction SHAP explanation
explainer = shap.LinearExplainer(model, input_processed,
                                  feature_names=all_names)
shap_values = explainer.shap_values(input_processed)

# Display: risk level (High/Medium/Low) + SHAP waterfall plot
if churn_prob >= 0.5:
    st.error(f"⚠️ HIGH RISK — Churn Probability: {churn_prob:.1%}")
elif churn_prob >= 0.3:
    st.warning(f"⚡ MEDIUM RISK — Churn Probability: {churn_prob:.1%}")
else:
    st.success(f"✅ LOW RISK — Churn Probability: {churn_prob:.1%}")</code></pre>

  <h3>Key Results at a Glance</h3>
  <table>
    <thead>
      <tr><th>Metric</th><th>Value</th></tr>
    </thead>
    <tbody>
      <tr><td>Best Model</td><td>Logistic Regression (class_weight='balanced')</td></tr>
      <tr><td>Test AUC</td><td>0.8344</td></tr>
      <tr><td>Test Recall</td><td>0.7888 (79% of churners caught)</td></tr>
      <tr><td>Test F1</td><td>0.6033</td></tr>
      <tr><td>Test Accuracy</td><td>0.7242</td></tr>
      <tr><td>Models Compared</td><td>5 (Logistic Regression, Random Forest, XGBoost, LightGBM, SVM)</td></tr>
      <tr><td>Tuning Decision</td><td>Kept default &mdash; tuned model lost 22pp recall for marginal AUC gain</td></tr>
      <tr><td>SHAP #1 Feature</td><td>tenure (low tenure strongly predicts churn)</td></tr>
      <tr><td>Deployed App</td><td>4-page Streamlit app with real-time predictions</td></tr>
    </tbody>
  </table>

  <h3>Skills Demonstrated</h3>
  <table>
    <thead>
      <tr><th>Skill Area</th><th>What This Project Shows</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>Data Cleaning</td>
        <td>dtype conversion, NaN handling decisions, target encoding, data quality validation</td>
      </tr>
      <tr>
        <td>Exploratory Data Analysis</td>
        <td>7 publication-quality visualizations, churn driver identification, statistical summaries</td>
      </tr>
      <tr>
        <td>Feature Engineering</td>
        <td>5 domain-informed features (ServiceCount, HasInternet, HasPhone, AvgMonthlyCharge, TenureGroup) with shared Python module for train/serve consistency</td>
      </tr>
      <tr>
        <td>Machine Learning</td>
        <td>5-model head-to-head comparison across 3 algorithmic families (linear, ensemble, geometric), stratified cross-validation, class imbalance handling</td>
      </tr>
      <tr>
        <td>Hyperparameter Tuning</td>
        <td>RandomizedSearchCV (50 iterations, 5 folds), principled decision to reject tuned model based on recall loss &mdash; demonstrates business-aware model selection</td>
      </tr>
      <tr>
        <td>Model Explainability</td>
        <td>SHAP LinearExplainer for global feature importance and per-customer waterfall explanations &mdash; translating predictions into business-readable insights</td>
      </tr>
      <tr>
        <td>Deployment</td>
        <td>4-page Streamlit app with real-time prediction, serialized model/preprocessor loading, SHAP waterfall generation on-the-fly</td>
      </tr>
      <tr>
        <td>Python Ecosystem</td>
        <td>pandas &middot; NumPy &middot; scikit-learn &middot; XGBoost &middot; LightGBM &middot; SHAP &middot; matplotlib &middot; seaborn &middot; Streamlit &middot; joblib</td>
      </tr>
      <tr>
        <td>Communication</td>
        <td>Business translations of SHAP findings, cost-asymmetry framing of metric selection, actionable retention recommendations</td>
      </tr>
    </tbody>
  </table>

  <h3>Live Application</h3>
  <p>
    <strong><a href="https://nadeaujonnyappio-ba7xf6aknjidd9ppd5ww3t.streamlit.app" target="_blank">Launch Streamlit Churn Predictor &rarr;</a></strong>
    &mdash; Input any customer profile and receive a churn risk score with a SHAP waterfall explanation.
  </p>

</details>

<details class="dropdown-section">
  <summary><strong>Dataset</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Source &amp; Overview</h3>
  <p>
    This project uses the <strong>Telco Customer Churn</strong> dataset &mdash; an IBM sample dataset hosted on
    Kaggle at
    <a href="https://www.kaggle.com/datasets/blastchar/telco-customer-churn" target="_blank">kaggle.com/datasets/blastchar/telco-customer-churn</a>.
    The dataset contains records for 7,043 customers of a fictional telecom company, with 21 columns capturing
    customer demographics, service subscriptions, account details, and whether the customer churned (cancelled
    their service) in the last month.
  </p>

  <table>
    <thead>
      <tr><th>Property</th><th>Value</th></tr>
    </thead>
    <tbody>
      <tr><td>File</td><td><code>WA_Fn-UseC_-Telco-Customer-Churn.csv</code></td></tr>
      <tr><td>File Size</td><td>~955 KB</td></tr>
      <tr><td>Raw Dimensions</td><td>7,043 rows &times; 21 columns</td></tr>
      <tr><td>Cleaned Dimensions</td><td>7,032 rows &times; 20 columns</td></tr>
      <tr><td>Target Variable</td><td><code>Churn</code> (Yes/No &rarr; 1/0, binary classification)</td></tr>
      <tr><td>Class Distribution</td><td>73.4% No Churn (5,163) / 26.6% Churn (1,869) &mdash; moderately imbalanced</td></tr>
    </tbody>
  </table>

  <h3>Key Code: Loading &amp; Initial Inspection</h3>
  <p>
    The raw dataset was loaded and inspected in <code>01_data_cleaning.ipynb</code>. The first inspection
    confirmed 7,043 rows, identified <code>TotalCharges</code> as an incorrectly typed object column, and
    verified zero explicit nulls and zero duplicates in the raw data:
  </p>

  <pre><code class="language-python">import pandas as pd
import numpy as np

# Load the raw dataset
df = pd.read_csv('../data/WA_Fn-UseC_-Telco-Customer-Churn.csv')

print(f"Shape: {df.shape}")
print(f"\nColumn dtypes:\n{df.dtypes}")
# Output: Shape: (7043, 21)
# TotalCharges shows as 'object' — should be numeric

# Confirm no explicit nulls and no duplicates
print(f"Missing values per column:\n{df.isnull().sum()}")
print(f"\nDuplicate rows: {df.duplicated().sum()}")
# Output: 0 missing values across all columns, 0 duplicates

# Check cardinality of each column
print(f"\nUnique values per column:\n{df.nunique()}")
# Output: customerID=7043 (unique), gender=2, SeniorCitizen=2,
# tenure=73, MonthlyCharges=1585, TotalCharges=6531, etc.</code></pre>

  <h3>Column Descriptions &mdash; Customer Demographics (5 columns)</h3>
  <table>
    <thead>
      <tr><th>Column</th><th>Type</th><th>Values</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr>
        <td><code>customerID</code></td>
        <td>string</td>
        <td>7,043 unique</td>
        <td>Unique customer identifier &mdash; dropped before modeling (not a predictive feature)</td>
      </tr>
      <tr>
        <td><code>gender</code></td>
        <td>categorical</td>
        <td>Male, Female</td>
        <td>Customer gender &mdash; EDA showed no meaningful difference in churn rates</td>
      </tr>
      <tr>
        <td><code>SeniorCitizen</code></td>
        <td>binary</td>
        <td>0, 1</td>
        <td>Whether customer is 65+ &mdash; already numeric (unlike other binary columns which use Yes/No), treated as a numeric feature during preprocessing</td>
      </tr>
      <tr>
        <td><code>Partner</code></td>
        <td>categorical</td>
        <td>Yes, No</td>
        <td>Whether customer has a partner</td>
      </tr>
      <tr>
        <td><code>Dependents</code></td>
        <td>categorical</td>
        <td>Yes, No</td>
        <td>Whether customer has dependents</td>
      </tr>
    </tbody>
  </table>

  <h3>Column Descriptions &mdash; Service Information (10 columns)</h3>
  <table>
    <thead>
      <tr><th>Column</th><th>Type</th><th>Values</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr>
        <td><code>tenure</code></td>
        <td>integer</td>
        <td>0&ndash;72 months</td>
        <td>Number of months the customer has been with the company &mdash; emerged as the single strongest SHAP feature</td>
      </tr>
      <tr>
        <td><code>PhoneService</code></td>
        <td>categorical</td>
        <td>Yes, No</td>
        <td>Whether customer has phone service</td>
      </tr>
      <tr>
        <td><code>MultipleLines</code></td>
        <td>categorical</td>
        <td>Yes, No, No phone service</td>
        <td>Whether customer has multiple phone lines &mdash; "No phone service" is a distinct category, not missing data</td>
      </tr>
      <tr>
        <td><code>InternetService</code></td>
        <td>categorical</td>
        <td>DSL, Fiber optic, No</td>
        <td>Type of internet service &mdash; fiber optic customers showed significantly higher churn rates despite paying more</td>
      </tr>
      <tr>
        <td><code>OnlineSecurity</code></td>
        <td>categorical</td>
        <td>Yes, No, No internet service</td>
        <td>Whether customer has online security add-on &mdash; absence correlates strongly with churn</td>
      </tr>
      <tr>
        <td><code>OnlineBackup</code></td>
        <td>categorical</td>
        <td>Yes, No, No internet service</td>
        <td>Whether customer has online backup add-on</td>
      </tr>
      <tr>
        <td><code>DeviceProtection</code></td>
        <td>categorical</td>
        <td>Yes, No, No internet service</td>
        <td>Whether customer has device protection add-on</td>
      </tr>
      <tr>
        <td><code>TechSupport</code></td>
        <td>categorical</td>
        <td>Yes, No, No internet service</td>
        <td>Whether customer has tech support add-on &mdash; absence correlates strongly with churn</td>
      </tr>
      <tr>
        <td><code>StreamingTV</code></td>
        <td>categorical</td>
        <td>Yes, No, No internet service</td>
        <td>Whether customer has streaming TV add-on</td>
      </tr>
      <tr>
        <td><code>StreamingMovies</code></td>
        <td>categorical</td>
        <td>Yes, No, No internet service</td>
        <td>Whether customer has streaming movies add-on</td>
      </tr>
    </tbody>
  </table>

  <h3>Column Descriptions &mdash; Account Information (5 columns)</h3>
  <table>
    <thead>
      <tr><th>Column</th><th>Type</th><th>Values</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr>
        <td><code>Contract</code></td>
        <td>categorical</td>
        <td>Month-to-month, One year, Two year</td>
        <td>Contract type &mdash; the single strongest churn predictor in EDA (42.7% churn for month-to-month vs. 2.8% for two-year)</td>
      </tr>
      <tr>
        <td><code>PaperlessBilling</code></td>
        <td>categorical</td>
        <td>Yes, No</td>
        <td>Whether customer uses paperless billing</td>
      </tr>
      <tr>
        <td><code>PaymentMethod</code></td>
        <td>categorical</td>
        <td>Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic)</td>
        <td>Payment method &mdash; electronic check showed noticeably higher churn than other methods</td>
      </tr>
      <tr>
        <td><code>MonthlyCharges</code></td>
        <td>float</td>
        <td>18.25&ndash;118.75</td>
        <td>Monthly charge amount in dollars &mdash; churners skew toward $70&ndash;$100/month plans</td>
      </tr>
      <tr>
        <td><code>TotalCharges</code></td>
        <td>string &rarr; float</td>
        <td>varies</td>
        <td>Total amount charged over customer lifetime &mdash; stored as string in raw data with whitespace entries for tenure=0 customers (see Known Data Issues below)</td>
      </tr>
    </tbody>
  </table>

  <h3>Column Descriptions &mdash; Target Variable (1 column)</h3>
  <table>
    <thead>
      <tr><th>Column</th><th>Type</th><th>Values</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr>
        <td><code>Churn</code></td>
        <td>categorical &rarr; binary</td>
        <td>Yes &rarr; 1, No &rarr; 0</td>
        <td>Whether the customer churned (cancelled service) in the last month &mdash; this is the prediction target</td>
      </tr>
    </tbody>
  </table>

  <h3>Class Distribution</h3>
  <p>
    The target variable is <strong>moderately imbalanced</strong>: 73.4% of customers did not churn (class 0) while
    26.6% did churn (class 1). This imbalance is not extreme enough to require synthetic oversampling (SMOTE), but it
    is significant enough that all five models in this project use explicit class imbalance handling &mdash;
    <code>class_weight='balanced'</code> for Logistic Regression, Random Forest, and SVM, and
    <code>scale_pos_weight</code> (ratio of negatives to positives &asymp; 2.76) for XGBoost and LightGBM. Evaluation
    also prioritizes recall and AUC over raw accuracy, since a naive "predict no churn for everyone" model would
    achieve 73.4% accuracy while catching zero churners.
  </p>

  <pre><code class="language-python"># Verify class distribution after encoding
print(df['Churn'].value_counts(normalize=True).round(4))
# Output:
# Churn
# 0    0.7342
# 1    0.2658

# Compute class weight ratio for gradient boosting models
pos_weight = y_train.value_counts()[0] / y_train.value_counts()[1]
# pos_weight ≈ 2.76</code></pre>

  <h3>Known Data Issues Handled</h3>
  <p>
    The dataset is relatively clean &mdash; no explicit missing values and no duplicate rows in the raw data.
    However, three data issues required attention during cleaning:
  </p>

  <h4>Issue 1: TotalCharges Stored as String</h4>
  <p>
    The <code>TotalCharges</code> column was loaded as <code>object</code> dtype instead of numeric. Investigation
    revealed that 11 rows contained whitespace strings instead of numeric values &mdash; all corresponding to
    customers with <code>tenure=0</code> (brand new customers with no billing history). Converting with
    <code>pd.to_numeric(errors='coerce')</code> turned these into NaN, and the 11 rows were dropped (0.16% of
    data &mdash; negligible impact on model training).
  </p>

  <pre><code class="language-python"># Fix TotalCharges: convert from string to numeric
# Whitespace entries (tenure=0 customers) will become NaN
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Check how many NaNs this created
print(f"TotalCharges NaNs after conversion: {df['TotalCharges'].isna().sum()}")
# Output: TotalCharges NaNs after conversion: 11

# Investigate: all NaN rows are tenure=0 customers
print(df[df['TotalCharges'].isna()][['customerID', 'tenure', 'MonthlyCharges', 'TotalCharges']])
# Output:
#       customerID  tenure  MonthlyCharges  TotalCharges
# 488   4472-LVYGI       0           52.55           NaN
# 753   3115-CZMZD       0           20.25           NaN
# 936   5709-LVOEQ       0           80.85           NaN
# 1082  4367-NUYAO       0           25.75           NaN
# 1340  1371-DWPAZ       0           56.05           NaN
# 3331  7644-OMVMY       0           19.85           NaN
# 3826  3213-VVOLG       0           25.35           NaN
# 4380  2520-SGTTA       0           20.00           NaN
# 5218  2923-ARZLG       0           19.70           NaN
# 6670  4075-WKNIU       0           73.35           NaN
# 6754  2775-SEFEE       0           61.90           NaN

# Drop the 11 rows — 0.16% of data, all tenure=0 with no billing history
df = df.dropna(subset=['TotalCharges'])</code></pre>

  <h4>Issue 2: SeniorCitizen Already Encoded as 0/1</h4>
  <p>
    Unlike every other binary column in the dataset (which uses Yes/No string values), <code>SeniorCitizen</code>
    is already encoded as 0/1 integers. This means it does not need one-hot encoding and is treated as a
    <strong>numeric feature</strong> during preprocessing. Applying <code>StandardScaler</code> to a 0/1 column
    is harmless and maintains pipeline consistency.
  </p>

  <h4>Issue 3: "No internet service" and "No phone service" Values</h4>
  <p>
    Six service columns (<code>OnlineSecurity</code>, <code>OnlineBackup</code>, <code>DeviceProtection</code>,
    <code>TechSupport</code>, <code>StreamingTV</code>, <code>StreamingMovies</code>) contain the value
    "No internet service" for customers who do not have internet at all, and <code>MultipleLines</code> contains
    "No phone service" for customers without phone service. These are <strong>informative categories, not missing
    data</strong> &mdash; they carry meaningful signal (a customer who doesn't have internet at all is different
    from a customer who has internet but opted out of a specific add-on). These values are preserved as distinct
    categories during one-hot encoding with <code>handle_unknown='ignore'</code>.
  </p>

  <h3>Key Code: Complete Cleaning Pipeline</h3>
  <p>
    The full cleaning pipeline runs in <code>01_data_cleaning.ipynb</code> and produces the cleaned CSV consumed
    by all downstream notebooks:
  </p>

  <pre><code class="language-python"># 1. Load raw data
df = pd.read_csv('../data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
# Shape: (7043, 21)

# 2. Fix TotalCharges dtype (string → float)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
# 11 whitespace entries become NaN

# 3. Drop 11 NaN rows (all tenure=0, no billing history, 0.16% of data)
df = df.dropna(subset=['TotalCharges'])

# 4. Drop customerID (not a predictive feature)
df = df.drop('customerID', axis=1)

# 5. Encode target variable: Yes=1, No=0
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# 6. Verify final state
print(f"Shape after cleaning: {df.shape}")
# Output: Shape after cleaning: (7032, 20)
print(f"\nTotalCharges dtype: {df['TotalCharges'].dtype}")
# Output: TotalCharges dtype: float64
print(f"\nChurn distribution:\n{df['Churn'].value_counts(normalize=True).round(4)}")
# Output: 0 = 0.7342, 1 = 0.2658

# 7. Save cleaned dataset for subsequent notebooks
df.to_csv('../data/telco_churn_cleaned.csv', index=False)
print(f"Cleaned dataset saved: {df.shape[0]} rows × {df.shape[1]} columns")
# Output: Cleaned dataset saved: 7032 rows × 20 columns
# Columns: ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
#   'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
#   'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
#   'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
#   'MonthlyCharges', 'TotalCharges', 'Churn']</code></pre>

  <h3>Feature Categorization Summary</h3>
  <p>
    After cleaning, the 20 remaining columns break down into three groups that determined preprocessing strategy
    in Phase 3:
  </p>

  <table>
    <thead>
      <tr><th>Category</th><th>Count</th><th>Columns</th><th>Preprocessing</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>Numeric (original)</td>
        <td>4</td>
        <td><code>SeniorCitizen</code>, <code>tenure</code>, <code>MonthlyCharges</code>, <code>TotalCharges</code></td>
        <td>StandardScaler</td>
      </tr>
      <tr>
        <td>Categorical (binary Yes/No)</td>
        <td>6</td>
        <td><code>gender</code>, <code>Partner</code>, <code>Dependents</code>, <code>PhoneService</code>, <code>PaperlessBilling</code>, <code>Churn</code> (target)</td>
        <td>OneHotEncoder (drop='first') for features; Churn mapped directly to 0/1</td>
      </tr>
      <tr>
        <td>Categorical (3&ndash;4 values)</td>
        <td>9</td>
        <td><code>MultipleLines</code>, <code>InternetService</code>, <code>OnlineSecurity</code>, <code>OnlineBackup</code>, <code>DeviceProtection</code>, <code>TechSupport</code>, <code>StreamingTV</code>, <code>StreamingMovies</code>, <code>Contract</code>, <code>PaymentMethod</code></td>
        <td>OneHotEncoder (drop='first', handle_unknown='ignore')</td>
      </tr>
    </tbody>
  </table>

  <p>
    After feature engineering in Phase 3 (adding <code>ServiceCount</code>, <code>HasInternet</code>,
    <code>HasPhone</code>, <code>AvgMonthlyCharge</code>, and <code>TenureGroup</code>), the final feature set
    grows to <strong>9 numeric + 15 categorical = 24 features before encoding</strong>, expanding to
    <strong>35 columns after one-hot encoding</strong> with <code>drop='first'</code>.
  </p>

</details>

<details class="dropdown-section">
  <summary><strong>Phase 1 &mdash; Data Cleaning</strong></summary>
  <div style="margin-top: 12px;"></div>
  <!-- TODO: Cleaning steps, code highlight, result -->
</details>

<details class="dropdown-section">
  <summary><strong>Phase 2 &mdash; Exploratory Data Analysis</strong></summary>
  <div style="margin-top: 12px;"></div>
  <!-- TODO: Key findings, all 7 charts with captions -->
</details>

<details class="dropdown-section">
  <summary><strong>Phase 3 &mdash; Feature Engineering &amp; Preprocessing</strong></summary>
  <div style="margin-top: 12px;"></div>
  <!-- TODO: Engineered features table, feature lists, pipeline code, train/test split -->
</details>

<details class="dropdown-section">
  <summary><strong>Phase 4 &mdash; Model Training &amp; Comparison</strong></summary>
  <div style="margin-top: 12px;"></div>
  <!-- TODO: 5 models, results table, charts, best model selection rationale -->
</details>

<details class="dropdown-section">
  <summary><strong>Phase 5 &mdash; Hyperparameter Tuning</strong></summary>
  <div style="margin-top: 12px;"></div>
  <!-- TODO: Tuning setup, default vs tuned comparison table, decision to keep default -->
</details>

<details class="dropdown-section">
  <summary><strong>Phase 6 &mdash; SHAP Explainability</strong></summary>
  <div style="margin-top: 12px;"></div>
  <!-- TODO: SHAP summary plot, bar plot, waterfall example, business translations -->
</details>

<details class="dropdown-section">
  <summary><strong>Streamlit App</strong></summary>
  <div style="margin-top: 12px;"></div>
  <!-- TODO: Link to live app, 4 pages described, screenshots, deployment info -->
</details>

<details class="dropdown-section">
  <summary><strong>Key Findings &amp; Business Recommendations</strong></summary>
  <div style="margin-top: 12px;"></div>
  <!-- TODO: Findings list, recommendations list -->
</details>

<details class="dropdown-section">
  <summary><strong>Technical Details</strong></summary>
  <div style="margin-top: 12px;"></div>
  <!-- TODO: Libraries table, final model specs, how to reproduce, project structure tree -->
</details>

<details class="dropdown-section">
  <summary><strong>Project Files &amp; Repository</strong></summary>
  <div style="margin-top: 12px;"></div>
  <!-- TODO: Links to repo, notebooks, app, shared module, models -->
</details>
