import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
import os
import sys

# Get the directory where app.py lives (works on both local and Streamlit Cloud)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)

from feature_helpers import engineer_features

# Page config
st.set_page_config(page_title="Customer Churn Predictor", page_icon="📊", layout="wide")

# Load model and preprocessor
@st.cache_resource
def load_model():
    model = joblib.load(os.path.join(APP_DIR, 'best_model.pkl'))
    preprocessor = joblib.load(os.path.join(APP_DIR, 'preprocessor.pkl'))
    return model, preprocessor

model, preprocessor = load_model()

# Sidebar navigation
st.sidebar.title("📊 Churn Predictor")
page = st.sidebar.radio("Navigate", ["Predict Churn Risk", "Model Performance", 
                                       "Data Insights", "Sample Predictions"])

# ============================================================
# PAGE 1: Predict Churn Risk
# ============================================================
if page == "Predict Churn Risk":
    st.title("🔮 Predict Customer Churn Risk")
    st.write("Enter customer attributes below to get a churn risk score with an explanation.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Demographics")
        gender = st.selectbox("Gender", ["Male", "Female"])
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
    
    with col2:
        st.subheader("Services")
        tenure = st.slider("Tenure (months)", 0, 72, 12)
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
        online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
        device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
        streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
        streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
    
    with col3:
        st.subheader("Account")
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment_method = st.selectbox("Payment Method", 
                                       ["Electronic check", "Mailed check", 
                                        "Bank transfer (automatic)", "Credit card (automatic)"])
        monthly_charges = st.slider("Monthly Charges ($)", 18.0, 120.0, 70.0, 0.05)
    
    # Compute TotalCharges from tenure * MonthlyCharges
    total_charges = tenure * monthly_charges if tenure > 0 else monthly_charges
    st.write(f"**Estimated Total Charges:** ${total_charges:,.2f}")
    
    # Convert SeniorCitizen to 0/1
    senior_citizen_val = 1 if senior_citizen == "Yes" else 0
    
    if st.button("🔍 Predict Churn Risk", type="primary"):
        # Build input DataFrame
        input_data = pd.DataFrame([{
            'gender': gender,
            'SeniorCitizen': senior_citizen_val,
            'Partner': partner,
            'Dependents': dependents,
            'tenure': tenure,
            'PhoneService': phone_service,
            'MultipleLines': multiple_lines,
            'InternetService': internet_service,
            'OnlineSecurity': online_security,
            'OnlineBackup': online_backup,
            'DeviceProtection': device_protection,
            'TechSupport': tech_support,
            'StreamingTV': streaming_tv,
            'StreamingMovies': streaming_movies,
            'Contract': contract,
            'PaperlessBilling': paperless_billing,
            'PaymentMethod': payment_method,
            'MonthlyCharges': monthly_charges,
            'TotalCharges': total_charges
        }])
        
        # Apply feature engineering (same function used in training)
        input_engineered = engineer_features(input_data)
        
        # Define feature order (must match training)
        numeric_features = ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges',
                            'ServiceCount', 'HasInternet', 'HasPhone', 'AvgMonthlyCharge', 'TenureGroup']
        categorical_features = ['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
                                'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                                'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
                                'PaperlessBilling', 'PaymentMethod']
        
        input_final = input_engineered[numeric_features + categorical_features]
        
        # Preprocess and predict
        input_processed = preprocessor.transform(input_final)
        churn_prob = model.predict_proba(input_processed)[0][1]
        churn_pred = model.predict(input_processed)[0]
        
        # Display result
        st.markdown("---")
        col_result1, col_result2 = st.columns(2)
        
        with col_result1:
            if churn_prob >= 0.5:
                st.error(f"⚠️ **HIGH RISK** — Churn Probability: {churn_prob:.1%}")
            elif churn_prob >= 0.3:
                st.warning(f"⚡ **MEDIUM RISK** — Churn Probability: {churn_prob:.1%}")
            else:
                st.success(f"✅ **LOW RISK** — Churn Probability: {churn_prob:.1%}")
        
        with col_result2:
            # SHAP explanation for this prediction
            st.subheader("Why this prediction?")
            
            # Get feature names
            cat_names = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features).tolist()
            all_names = numeric_features + cat_names
            
            explainer = shap.LinearExplainer(model, input_processed, feature_names=all_names)
            shap_values = explainer.shap_values(input_processed)
            
            explanation = shap.Explanation(
                values=shap_values[0],
                base_values=explainer.expected_value,
                data=input_processed[0],
                feature_names=all_names
            )
            
            fig, ax = plt.subplots(figsize=(8, 5))
            shap.waterfall_plot(explanation, max_display=10, show=False)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

# ============================================================
# PAGE 2: Model Performance
# ============================================================
elif page == "Model Performance":
    st.title("📈 Model Performance")
    st.write("Comparison of 5 classification models trained on the Telco Customer Churn dataset.")
    
    # Model comparison table
    st.subheader("Model Comparison")
    comparison_df = pd.read_csv(os.path.join(APP_DIR, 'model_comparison.csv'))
    st.dataframe(comparison_df, use_container_width=True)
    
    st.info("**Best Model: Logistic Regression** — Highest AUC (0.834) and Recall (0.789). "
            "Recall is our priority metric: it's cheaper to send a retention offer to a loyal customer "
            "than to miss a churner.")
    
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Model Comparison")
        st.image(os.path.join(APP_DIR, 'figures/model_comparison.png'), use_container_width=True)
    with col2:
        st.subheader("ROC Curves")
        st.image(os.path.join(APP_DIR, 'figures/roc_curves.png'), use_container_width=True)
    
    st.subheader("Confusion Matrices")
    st.image(os.path.join(APP_DIR, 'figures/confusion_matrix.png'), use_container_width=True)

# ============================================================
# PAGE 3: Data Insights
# ============================================================
elif page == "Data Insights":
    st.title("🔍 Data Insights & SHAP Explainability")
    
    st.subheader("Key EDA Findings")
    col1, col2 = st.columns(2)
    with col1:
        st.image(os.path.join(APP_DIR, 'figures/churn_by_contract.png'), 
                 caption='Churn Rate by Contract Type', use_container_width=True)
    with col2:
        st.image(os.path.join(APP_DIR, 'figures/tenure_by_churn.png'), 
                 caption='Tenure Distribution by Churn Status', use_container_width=True)
    
    st.markdown("---")
    st.subheader("SHAP Feature Importance")
    st.write("SHAP values show how each feature contributes to the model's churn predictions.")
    st.image(os.path.join(APP_DIR, 'figures/shap_summary.png'), 
             caption='SHAP Summary — Top 15 Features Driving Churn', use_container_width=True)
    
    st.subheader("Business Recommendations")
    st.markdown("""
    1. **Incentivize annual contracts** — Month-to-month customers churn at 42.7% vs 2.8% for two-year contracts
    2. **Focus retention on new customers** — Most churn happens in the first few months
    3. **Bundle support add-ons** — Customers with OnlineSecurity and TechSupport churn significantly less
    4. **Address fiber optic experience** — Fiber customers churn more despite paying more (potential service quality issue)
    5. **Migrate electronic check users** — This payment method correlates with higher churn
    """)

# ============================================================
# PAGE 4: Sample Predictions
# ============================================================
elif page == "Sample Predictions":
    st.title("📋 Sample Predictions")
    st.write("Predictions on 15 test set customers showing actual vs predicted churn with probability scores.")
    
    try:
        sample_df = pd.read_csv(os.path.join(APP_DIR, '..', 'outputs', 'metrics', 'sample_predictions.csv'))
    except FileNotFoundError:
        sample_df = pd.DataFrame({
            'Actual': [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            'Predicted': [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0],
            'Churn_Probability': [0.0497, 0.7920, 0.0141, 0.3977, 0.2398, 0.7201, 0.0712, 0.3605, 0.8375, 0.0529, 0.8672, 0.3457, 0.8268, 0.1601, 0.4274]
        })
    
    # Color code the probabilities
    st.dataframe(
        sample_df.style.background_gradient(subset=['Churn_Probability'], cmap='RdYlGn_r'),
        use_container_width=True
    )
    
    st.markdown("---")
    st.write("**How to read this table:**")
    st.markdown("""
    - **Actual**: Whether the customer actually churned (1) or stayed (0)
    - **Predicted**: The model's binary prediction at the 0.5 threshold
    - **Churn_Probability**: The model's confidence score (0 = definitely staying, 1 = definitely churning)
    """)