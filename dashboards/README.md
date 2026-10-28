# 📈 Power BI Executive Revenue Intelligence Dashboard

## 📊 Overview
The Power BI dashboard connects directly to the PostgreSQL Star Schema data warehouse (`saas_revenue_db`), providing executives with real-time visibility into customer retention, revenue at risk, and predictive churn risk scoring.

## 🛠️ Key Components & DAX Measures
- **Total MRR:** Aggregates active corporate subscription value.
- **Revenue at Risk:** Dynamically filters clients with a machine learning-derived churn probability > 75.
- **Avg Churn Risk & Churn Rate %:** Tracks overall portfolio stability and historical loss rate.
- **Relational Star Schema:** Joins `dim_customers` and `public_fact_customer_metrics` for high-speed analytical aggregatio.