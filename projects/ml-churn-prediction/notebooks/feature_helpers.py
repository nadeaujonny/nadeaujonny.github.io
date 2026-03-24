"""
Shared feature engineering function.
Used by notebooks (training) and Streamlit app (prediction) to ensure identical transformations.
"""

def engineer_features(df):
    """
    Create engineered features from the cleaned telco churn dataset.
    
    Parameters:
        df: pandas DataFrame with cleaned columns
    
    Returns:
        df: DataFrame with new features added
    """
    df = df.copy()
    
    # 1. Service count: how many optional services does the customer have?
    service_cols = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                    'TechSupport', 'StreamingTV', 'StreamingMovies']
    df['ServiceCount'] = df[service_cols].apply(lambda row: (row == 'Yes').sum(), axis=1)
    
    # 2. Has internet service (binary)
    df['HasInternet'] = (df['InternetService'] != 'No').astype(int)
    
    # 3. Has phone service (binary) 
    df['HasPhone'] = (df['PhoneService'] == 'Yes').astype(int)
    
    # 4. Average monthly charge (TotalCharges / tenure), handle tenure=0
    df['AvgMonthlyCharge'] = df.apply(
        lambda row: row['TotalCharges'] / row['tenure'] if row['tenure'] > 0 
        else row['MonthlyCharges'], axis=1
    )
    
    # 5. Tenure group (numeric encoding for modeling)
    def tenure_bucket(t):
        if t <= 12: return 0
        elif t <= 24: return 1
        elif t <= 48: return 2
        else: return 3
    
    df['TenureGroup'] = df['tenure'].apply(tenure_bucket)
    
    return df