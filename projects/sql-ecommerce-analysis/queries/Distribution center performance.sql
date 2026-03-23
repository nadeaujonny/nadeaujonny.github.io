SELECT
  dc.name AS distribution_center,
  COUNT(oi.id) AS total_units,
  ROUND(SUM(oi.sale_price), 2) AS revenue,
  ROUND(SUM(oi.sale_price) - SUM(p.cost), 2) AS profit,
  ROUND(
    COUNTIF(oi.status = 'Processing') / COUNT(oi.id) * 100, 2
  ) AS processing_pct
FROM
  `bigquery-public-data.thelook_ecommerce.order_items` oi
JOIN
  `bigquery-public-data.thelook_ecommerce.products` p
  ON oi.product_id = p.id
JOIN
  `bigquery-public-data.thelook_ecommerce.distribution_centers` dc
  ON p.distribution_center_id = dc.id
GROUP BY
  dc.name
ORDER BY
  total_units DESC;