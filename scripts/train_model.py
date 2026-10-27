import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

def train_churn_model():
    raw_path = os.path.join('data', 'raw_saas_customers.csv')
    if not os.path.exists(raw_path):
        print("❌ Error: Raw dataset not found. Run scripts/generate_data.py first.")
        return

    print("Loading raw enterprise dataset...")
    df = pd.read_csv(raw_path)
    
    # Feature Engineering: One-hot encoding categorical variables
    df_encoded = pd.get_dummies(df, columns=['subscription_tier', 'contract_type'], drop_first=True)
    
    X = df_encoded.drop(columns=['customer_id', 'company_name', 'churned'])
    y = df_encoded['churned']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Churn Risk Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict Churn Risk Probabilities for entire dataset
    probabilities = model.predict_proba(X)[:, 1]
    df['churn_risk_probability'] = np.round(probabilities * 100, 2)
    
    # Save model and scored dataset
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/churn_model.pkl')
    
    processed_path = os.path.join('data', 'processed_saas_customers.csv')
    df.to_csv(processed_path, index=False)
    print(f"✅ Model trained! Scored dataset saved to {processed_path}")

if __name__ == "__main__":
    train_churn_model()