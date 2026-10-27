-- 1. Executive Summary: Revenue at Risk by Subscription Tier
CREATE OR REPLACE VIEW vw_revenue_at_risk AS
SELECT 
    f.subscription_tier,
    COUNT(f.customer_id) AS total_customers,
    SUM(f.monthly_recurring_revenue) AS total_mrr,
    SUM(CASE WHEN f.churn_risk_probability > 75.0 THEN f.monthly_recurring_revenue ELSE 0 END) AS revenue_at_risk,
    ROUND(AVG(f.churn_risk_probability), 2) AS avg_churn_risk_score
FROM fact_customer_metrics f
GROUP BY f.subscription_tier
ORDER BY revenue_at_risk DESC;

-- 2. High-Risk Enterprise Accounts Targeting View
CREATE OR REPLACE VIEW vw_high_risk_accounts AS
SELECT 
    d.company_name,
    f.subscription_tier,
    f.monthly_recurring_revenue,
    f.tenure_months,
    f.login_frequency_weekly,
    f.support_tickets_count,
    f.churn_risk_probability
FROM fact_customer_metrics f
JOIN dim_customers d ON f.customer_id = d.customer_id
WHERE f.churn_risk_probability > 80.0
ORDER BY f.monthly_recurring_revenue DESC;