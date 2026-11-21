
-- Question 1: Overall churn percentage
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_percentage
FROM customers;


-- Question 2: Churn by contract type
SELECT
    contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_percentage
FROM customers
GROUP BY contract
ORDER BY churn_percentage DESC;


-- Question 3: Average charges by churn status
SELECT
    churn,
    COUNT(*) AS total_customers,
    ROUND(AVG(monthly_charges), 2) AS average_monthly_charges,
    ROUND(AVG(total_charges), 2) AS average_total_charges
FROM customers
GROUP BY churn;


-- Question 4: Churn by payment method
SELECT
    payment_method,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_percentage
FROM customers
GROUP BY payment_method
ORDER BY churn_percentage DESC;


-- Question 5: Average tenure by churn status
SELECT
    churn,
    COUNT(*) AS total_customers,
    ROUND(AVG(tenure), 2) AS average_tenure_months,
    MIN(tenure) AS minimum_tenure,
    MAX(tenure) AS maximum_tenure
FROM customers
GROUP BY churn;
