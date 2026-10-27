import pandas as pd
import numpy as np
import os

def generate_saas_data():
    os.makedirs('data', exist_ok=True)
    np.random.seed(42)
    
    n_samples = 100000
    
    customer_ids = [f"CUST-{10000 + i}" for i in range(n_samples)]
    company_names = [f"Enterprise Corp {i}" for i in range(n_samples)]
    
    tiers = ['Starter', 'Professional', 'Enterprise', 'Strategic']
    tier_weights = [0.4, 0.3, 0.2, 0.1]
    subscription_tier = np.random.choice(tiers, size=n_samples, p=tier_weights)
    
    mrr_map = {'Starter': 150, 'Professional': 600, 'Enterprise': 2500, 'Strategic': 8000}
    mrr = [mrr_map[t] * np.random.uniform(0.9, 1.2) for t in subscription_tier]
    
    tenure_months = np.random.randint(1, 72, size=n_samples)
    login_frequency = np.random.poisson(lam=15, size=n_samples)
    support_tickets = np.random.poisson(lam=3, size=n_samples)
    contract_type = np.random.choice(['Monthly', 'Annual'], size=n_samples, p=[0.6, 0.4])
    
    # Business logic for churn likelihood label (1 = Churned/At Risk, 0 = Active)
    churn_score = (
        (support_tickets * 0.2) - 
        (login_frequency * 0.05) - 
        (tenure_months * 0.02) + 
        (np.where(contract_type == 'Monthly', 0.5, -0.3)) +
        np.random.normal(0, 0.5, size=n_samples)
    )
    churn_label = np.where(churn_score > np.percentile(churn_score, 75), 1, 0)
    
    df = pd.DataFrame({
        'customer_id': customer_ids,
        'company_name': company_names,
        'subscription_tier': subscription_tier,
        'monthly_recurring_revenue': np.round(mrr, 2),
        'tenure_months': tenure_months,
        'login_frequency_weekly': login_frequency,
        'support_tickets_count': support_tickets,
        'contract_type': contract_type,
        'churned': churn_label
    })
    
    output_path = os.path.join('data', 'raw_saas_customers.csv')
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {n_samples:,} enterprise customer records at {output_path}")

if __name__ == "__main__":
    generate_saas_data()