WITH product_sales AS (
  SELECT
    p.id AS product_id,
    p.distribution_center_id,
    COUNT(oi.id) / GREATEST(DATE_DIFF(CURRENT_DATE(), MIN(DATE(oi.created_at)), DAY), 1) AS daily_sales_rate
  FROM
    `bigquery-public-data.thelook_ecommerce.products` p
  LEFT JOIN
    `bigquery-public-data.thelook_ecommerce.order_items` oi
    ON p.id = oi.product_id
  GROUP BY
    p.id, p.distribution_center_id
),


inventory AS (
  SELECT
    id AS product_id,
    product_distribution_center_id,
    COUNT(*) AS stock_on_hand
  FROM
    `bigquery-public-data.thelook_ecommerce.inventory_items`
  WHERE
    sold_at IS NULL
  GROUP BY
    id, product_distribution_center_id
),


product_status AS (
  SELECT
    ps.distribution_center_id,
    CASE
      WHEN SAFE_DIVIDE(COALESCE(i.stock_on_hand, 0), ps.daily_sales_rate) > 90 THEN 'Overstocked'
      WHEN SAFE_DIVIDE(COALESCE(i.stock_on_hand, 0), ps.daily_sales_rate) < 14 THEN 'Understocked'
    END AS stock_status
  FROM
    product_sales ps
  LEFT JOIN
    inventory i
    ON ps.product_id = i.product_id
    AND ps.distribution_center_id = i.product_distribution_center_id
)


SELECT
  dc.name AS distribution_center,
  COUNTIF(stock_status = 'Overstocked') AS overstocked_products,
  COUNTIF(stock_status = 'Understocked') AS understocked_products,
  COUNTIF(stock_status IS NOT NULL) AS total_flagged_products
FROM
  product_status ps
JOIN
  `bigquery-public-data.thelook_ecommerce.distribution_centers` dc
  ON ps.distribution_center_id = dc.id
GROUP BY
  dc.name
ORDER BY
  total_flagged_products DESC;