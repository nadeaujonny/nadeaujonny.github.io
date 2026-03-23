SELECT
  u.country,
  COUNT(DISTINCT u.id) AS num_customers,
  COUNT(oi.id) AS units_sold,
  ROUND(SUM(oi.sale_price), 2) AS revenue,
  ROUND(SUM(oi.sale_price - p.cost), 2) AS profit
FROM
  `bigquery-public-data.thelook_ecommerce.order_items` oi
JOIN
  `bigquery-public-data.thelook_ecommerce.users` u
  ON oi.user_id = u.id
JOIN
  `bigquery-public-data.thelook_ecommerce.products` p
  ON oi.product_id = p.id
WHERE
  oi.status NOT IN ('Cancelled', 'Returned')
GROUP BY
  u.country
ORDER BY
  revenue DESC;