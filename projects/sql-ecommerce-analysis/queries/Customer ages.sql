SELECT
  CONCAT(CAST(FLOOR(u.age / 10) * 10 AS STRING), '-', CAST(FLOOR(u.age / 10) * 10 + 9 AS STRING)) AS age_segment,
  MIN(u.age) AS min_age,
  MAX(u.age) AS max_age,
  COUNT(oi.id) AS units_sold,
  ROUND(SUM(oi.sale_price), 2) AS revenue,
  ROUND(SUM(oi.sale_price) - SUM(p.cost), 2) AS profit
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
  age_segment
ORDER BY
  Age_segment;