SELECT
  COUNT(DISTINCT user_id) AS reactivated_customers
FROM (
  SELECT
    user_id,
    DATE_DIFF(
      DATE(created_at),
      LAG(DATE(created_at)) OVER (PARTITION BY user_id ORDER BY created_at),
      DAY
    ) AS days_between_orders
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
)
WHERE days_between_orders > 90