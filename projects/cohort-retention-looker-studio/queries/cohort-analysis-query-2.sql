WITH customer_cohorts AS (
  SELECT
    user_id,
    DATE(DATE_TRUNC(MIN(created_at), MONTH)) AS cohort_month
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
  GROUP BY user_id
),

monthly_revenue AS (
  SELECT
    oi.user_id,
    DATE(DATE_TRUNC(oi.created_at, MONTH)) AS activity_month,
    SUM(oi.sale_price) AS monthly_revenue
  FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` o
    ON oi.order_id = o.order_id
  WHERE o.status = 'Complete'
    AND o.created_at < '2025-01-01'
  GROUP BY oi.user_id, activity_month
),

revenue_by_period AS (
  SELECT
    c.cohort_month,
    DATE_DIFF(r.activity_month, c.cohort_month, MONTH) AS period_number,
    SUM(r.monthly_revenue) AS period_revenue
  FROM customer_cohorts c
  JOIN monthly_revenue r
    ON c.user_id = r.user_id
  GROUP BY c.cohort_month, period_number
),

period_zero_revenue AS (
  SELECT
    cohort_month,
    period_revenue AS baseline_revenue
  FROM revenue_by_period
  WHERE period_number = 0
)

SELECT
  r.cohort_month,
  r.period_number,
  ROUND(r.period_revenue, 2) AS period_revenue,
  ROUND(p.baseline_revenue, 2) AS baseline_revenue,
  ROUND(r.period_revenue / p.baseline_revenue * 100, 2) AS revenue_retention_pct
FROM revenue_by_period r
JOIN period_zero_revenue p
  ON r.cohort_month = p.cohort_month
WHERE r.period_number >= 0
ORDER BY r.cohort_month, r.period_number