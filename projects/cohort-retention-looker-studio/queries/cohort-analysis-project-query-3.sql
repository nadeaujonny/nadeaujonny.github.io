WITH customer_cohorts AS (
  SELECT
    o.user_id,
    u.traffic_source,
    DATE(DATE_TRUNC(MIN(o.created_at), MONTH)) AS cohort_month
  FROM `bigquery-public-data.thelook_ecommerce.orders` o
  JOIN `bigquery-public-data.thelook_ecommerce.users` u
    ON o.user_id = u.id
  WHERE o.status = 'Complete'
    AND o.created_at < '2025-01-01'
  GROUP BY o.user_id, u.traffic_source
),

monthly_activity AS (
  SELECT DISTINCT
    user_id,
    DATE(DATE_TRUNC(created_at, MONTH)) AS activity_month
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
),

retention_data AS (
  SELECT
    c.traffic_source,
    DATE_DIFF(a.activity_month, c.cohort_month, MONTH) AS period_number,
    COUNT(DISTINCT c.user_id) AS active_users
  FROM customer_cohorts c
  JOIN monthly_activity a
    ON c.user_id = a.user_id
  GROUP BY c.traffic_source, period_number
),

channel_sizes AS (
  SELECT
    traffic_source,
    COUNT(DISTINCT user_id) AS channel_size
  FROM customer_cohorts
  GROUP BY traffic_source
)

SELECT
  r.traffic_source,
  r.period_number,
  r.active_users,
  s.channel_size,
  ROUND(r.active_users / s.channel_size * 100, 2) AS retention_pct
FROM retention_data r
JOIN channel_sizes s
  ON r.traffic_source = s.traffic_source
WHERE r.period_number >= 0
ORDER BY r.traffic_source, r.period_number