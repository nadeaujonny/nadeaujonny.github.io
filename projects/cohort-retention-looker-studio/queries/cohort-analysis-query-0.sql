SELECT
  cohort_month,
  COUNT(DISTINCT user_id) AS new_customers
FROM (
  SELECT
    user_id,
    DATE(DATE_TRUNC(MIN(created_at), MONTH)) AS cohort_month
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
  GROUP BY user_id
)
GROUP BY cohort_month
ORDER BY cohort_month