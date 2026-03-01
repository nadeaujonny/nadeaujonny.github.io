WITH customer_cohorts AS (
  -- CTE 1: Get each customer's cohort month (first order month)
  SELECT
    user_id,
    DATE(DATE_TRUNC(MIN(created_at), MONTH)) AS cohort_month
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
  GROUP BY user_id
),

monthly_activity AS (
  -- CTE 2: Get every distinct month each customer placed an order
  SELECT DISTINCT
    user_id,
    DATE(DATE_TRUNC(created_at, MONTH)) AS activity_month
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
),

retention_data AS (
  -- CTE 3: Join cohorts to activity, calculate period number
  SELECT
    c.cohort_month,
    DATE_DIFF(DATE(a.activity_month), DATE(c.cohort_month), MONTH) AS period_number,
    COUNT(DISTINCT c.user_id) AS active_users
  FROM customer_cohorts c
  JOIN monthly_activity a
    ON c.user_id = a.user_id
  GROUP BY c.cohort_month, period_number
),

cohort_sizes AS (
  -- Get total customers per cohort for retention % calculation
  SELECT
    cohort_month,
    COUNT(DISTINCT user_id) AS cohort_size
  FROM customer_cohorts
  GROUP BY cohort_month
)

-- Final query: retention matrix
SELECT
  r.cohort_month,
  r.period_number,
  r.active_users,
  s.cohort_size,
  ROUND(r.active_users / s.cohort_size * 100, 2) AS retention_pct
FROM retention_data r
JOIN cohort_sizes s
  ON r.cohort_month = s.cohort_month
WHERE r.period_number >= 0
ORDER BY r.cohort_month, r.period_number