import pandas as pd
import os
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_star_schema():
    processed_path = os.path.join('data', 'processed_saas_customers.csv')
    if not os.path.exists(processed_path):
        logging.error("Processed dataset missing. Run scripts/train_model.py first.")
        return

    logging.info("Loading processed SaaS dataset...")
    df = pd.read_csv(processed_path)
    
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    connection_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(connection_url)
    
    logging.info("Building Star Schema (Dimension & Fact Tables)...")
    
    # 1. Dimension Table: Customers
    dim_customers = df[['customer_id', 'company_name', 'contract_type']].drop_duplicates(subset=['customer_id'])
    
    # 2. Fact Table: Customer Metrics & Churn Risk
    fact_metrics = df[[
        'customer_id', 'subscription_tier', 'monthly_recurring_revenue', 
        'tenure_months', 'login_frequency_weekly', 'support_tickets_count', 
        'churned', 'churn_risk_probability'
    ]].copy()
    
    with engine.begin() as connection:
        logging.info("Ingesting dim_customers into PostgreSQL...")
        dim_customers.to_sql('dim_customers', connection, if_exists='replace', index=False)
        
        logging.info("Ingesting fact_customer_metrics into PostgreSQL...")
        fact_metrics.to_sql('fact_customer_metrics', connection, if_exists='replace', index=False)
        
        logging.info("Creating high-performance indexes...")
        connection.execute(text("CREATE INDEX IF NOT EXISTS idx_fact_customer_id ON fact_customer_metrics (customer_id);"))
        connection.execute(text("CREATE INDEX IF NOT EXISTS idx_fact_tier ON fact_customer_metrics (subscription_tier);"))
        connection.execute(text("CREATE INDEX IF NOT EXISTS idx_fact_risk ON fact_customer_metrics (churn_risk_probability);"))
        
    logging.info("✅ Star Schema data warehouse loaded and indexed successfully!")

if __name__ == "__main__":
    load_star_schema()