
# 📈 Enterprise SaaS Revenue Intelligence Platform

An end-to-end predictive churn analytics and revenue intelligence platform for B2B SaaS enterprises. This project integrates a Machine Learning risk-scoring engine, a PostgreSQL Star Schema data warehouse, and an interactive executive Power BI dashboard to deliver real-time visibility into Monthly Recurring Revenue (MRR) and churn risk.

---

## 📌 Executive Summary

For B2B SaaS companies, customer churn represents one of the largest threats to sustainable growth. Traditional analytics tools are reactive—reporting cancellations *after* they occur. 

This platform bridges the gap between **predictive data science** and **executive decision-making**:
1. Predicts customer churn probabilities across **100,000 enterprise accounts** using Machine Learning.
2. Ingests telemetry metrics and client demographics into an optimized **PostgreSQL Star Schema**.
3. Dynamically calculates critical financial metrics—such as **Revenue at Risk**—in an interactive **Power BI Executive Dashboard**.

---

## 🏗️ System Architecture

```text
[ Synthetic Data & ML Pipeline ] ──> [ PostgreSQL Star Schema Warehouse ] ──> [ Power BI Executive Dashboard ]
    • Synthetic B2B Telemetry            • saas_revenue_db                       • Real-Time DAX Measures
    • Scikit-Learn / XGBoost Risk Model   • dim_customers & fact_customer_metrics  • KPI Cards & Risk Tables
```

---

## 🛠️ Tech Stack & Key Components

| Layer | Technologies | Primary Purpose |
| :--- | :--- | :--- |
| **Data & ML Engine** | Python, Pandas, Scikit-Learn, XGBoost | Synthetic enterprise data generation, feature engineering, and churn risk scoring. |
| **Data Warehousing** | PostgreSQL, SQL, SQLAlchemy | Relational Star Schema modeling (`saas_revenue_db`) for fast analytical processing. |
| **Business Intelligence** | Power BI, DAX | Executive KPI monitoring, revenue risk modeling, and interactive visualization. |
| **Version Control** | Git, GitHub | Code management, versioning, and project documentation. |

---

## 🗄️ Database Architecture (Star Schema)

The analytical data warehouse is built in PostgreSQL (`saas_revenue_db`) using a Star Schema layout:

* **`public_dim_customers` (Dimension Table):**
  * `customer_id` (Primary Key)
  * `company_name`
  * `contract_type` (Monthly vs. Annual)
* **`public_fact_customer_metrics` (Fact Table):**
  * `customer_id` (Foreign Key)
  * `monthly_recurring_revenue` (MRR)
  * `support_tickets_count`
  * `login_frequency_weekly`
  * `tenure_months`
  * `churned` (Historical churn flag)
  * `churn_risk_probability` (ML-derived risk score: $0.0 - 100.0\%$)

---

## 📊 Business Intelligence & DAX Measures

The Power BI dashboard connects directly to the PostgreSQL warehouse and utilizes custom DAX measures for executive reporting:

* **Total MRR:**
  ```dax
  Total MRR = SUM('public_fact_customer_metrics'[monthly_recurring_revenue])
  ```
* **Revenue at Risk (Accounts with $> 75\%$ churn risk):**
  ```dax
  Revenue at Risk = 
  CALCULATE(
      SUM('public_fact_customer_metrics'[monthly_recurring_revenue]),
      'public_fact_customer_metrics'[churn_risk_probability] > 75.0
  )
  ```
* **Average Churn Risk:**
  ```dax
  Avg Churn Risk = AVERAGE('public_fact_customer_metrics'[churn_risk_probability])
  ```
* **Churn Rate %:**
  ```dax
  Churn Rate % = DIVIDE(
      CALCULATE(COUNT('public_fact_customer_metrics'[customer_id]), 'public_fact_customer_metrics'[churned] = 1),
      COUNT('public_fact_customer_metrics'[customer_id]),
      0
  ) * 100
  ```

---

## 🚀 How to Run the Pipeline

### 1. Prerequisites
* Python 3.10+ installed
* PostgreSQL database server running locally (`localhost:5432`)
* Power BI Desktop

### 2. Machine Learning & Data Pipeline
Run the Python ML script to generate the synthetic telemetry and fit the churn prediction model:
```powershell
python scripts/train_churn_model.py
```

### 3. Load Database Data Warehouse
Populate the PostgreSQL Star Schema warehouse:
```powershell
python scripts/load_star_schema.py
```

### 4. Power BI Dashboard Setup
1. Open Power BI Desktop and load `dashboards/saas_revenue_intelligence.pbix`.
2. Ensure the PostgreSQL source connection is set to `localhost:5432` / `saas_revenue_db`.
3. Click **Refresh** to load the latest analytical data.

---

## 📂 Repository Structure

```text
saas-churn-revenue-intelligence/
├── data/                         # CSV datasets (dim_customers, fact_customer_metrics)
├── dashboards/                   # Power BI report files and dashboard documentation
│   └── saas_revenue_intelligence.pbix
├── models/                       # Machine learning model artifacts (.pkl)
├── scripts/                      # ETL pipeline & ML modeling scripts
│   ├── load_star_schema.py
│   └── train_churn_model.py
├── sql/                          # DDL scripts for Star Schema table creation
├── .gitignore
└── README.md                     # Main GitHub repository documentation
```
