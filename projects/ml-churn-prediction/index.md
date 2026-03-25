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
  <!-- TODO: Source, size, column descriptions table, known data issues -->
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
