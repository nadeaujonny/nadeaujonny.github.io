WITH customer_cohorts AS (
  SELECT
    user_id,
    DATE(DATE_TRUNC(MIN(created_at), MONTH)) AS cohort_month
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
  GROUP BY user_id
),

cohort_sizes AS (
  SELECT
    cohort_month,
    COUNT(DISTINCT user_id) AS cohort_size
  FROM customer_cohorts
  GROUP BY cohort_month
),

monthly_revenue AS (
  SELECT
    c.cohort_month,
    DATE_DIFF(DATE(DATE_TRUNC(oi.created_at, MONTH)), c.cohort_month, MONTH) AS period_number,
    SUM(oi.sale_price) AS period_revenue
  FROM customer_cohorts c
  JOIN `bigquery-public-data.thelook_ecommerce.order_items` oi
    ON c.user_id = oi.user_id
  JOIN `bigquery-public-data.thelook_ecommerce.orders` o
    ON oi.order_id = o.order_id
  WHERE o.status = 'Complete'
    AND o.created_at < '2025-01-01'
  GROUP BY c.cohort_month, period_number
)

SELECT
  r.cohort_month,
  r.period_number,
  ROUND(r.period_revenue, 2) AS period_revenue,
  ROUND(
    SUM(r.period_revenue) OVER (
      PARTITION BY r.cohort_month
      ORDER BY r.period_number
    ), 2
  ) AS cumulative_revenue,
  s.cohort_size,
  ROUND(
    SUM(r.period_revenue) OVER (
      PARTITION BY r.cohort_month
      ORDER BY r.period_number
    ) / s.cohort_size, 2
  ) AS cumulative_revenue_per_customer
FROM monthly_revenue r
JOIN cohort_sizes s
  ON r.cohort_month = s.cohort_month
WHERE r.period_number >= 0
ORDER BY r.cohort_month, r.period_number