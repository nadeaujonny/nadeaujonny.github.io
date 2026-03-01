WITH customer_activity AS (
  SELECT
    user_id,
    DATE(MIN(created_at)) AS first_order_date,
    DATE(MAX(created_at)) AS last_order_date,
    COUNT(DISTINCT order_id) AS total_orders,
    DATE_DIFF(
      DATE('2024-12-31'),
      DATE(MAX(created_at)),
      DAY
    ) AS days_since_last_order
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
  GROUP BY user_id
),

customer_segments AS (
  SELECT
    user_id,
    first_order_date,
    last_order_date,
    total_orders,
    days_since_last_order,
    CASE
      WHEN days_since_last_order <= 90 THEN 'Active'
      WHEN days_since_last_order <= 180 THEN 'At-Risk'
      ELSE 'Churned'
    END AS customer_status
  FROM customer_activity
),

-- Bonus: detect reactivations (customers who returned after a 90+ day gap)
order_gaps AS (
  SELECT
    user_id,
    DATE(created_at) AS order_date,
    LAG(DATE(created_at)) OVER (PARTITION BY user_id ORDER BY created_at) AS prev_order_date,
    DATE_DIFF(
      DATE(created_at),
      LAG(DATE(created_at)) OVER (PARTITION BY user_id ORDER BY created_at),
      DAY
    ) AS days_between_orders
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
),

reactivations AS (
  SELECT
    COUNT(DISTINCT user_id) AS reactivated_customers
  FROM order_gaps
  WHERE days_between_orders > 90
)

-- Main output: segment counts
SELECT
  customer_status,
  COUNT(*) AS customer_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_total,
  ROUND(AVG(total_orders), 2) AS avg_orders,
  ROUND(AVG(days_since_last_order), 0) AS avg_days_since_last_order
FROM customer_segments
GROUP BY customer_status
ORDER BY customer_count DESC