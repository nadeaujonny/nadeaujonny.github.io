WITH first_layer AS (
SELECT
  dc.id AS distribution_center_id,
  dc.name AS distribution_center_name,
  dc.latitude AS dc_latitude,
  dc.longitude AS dc_longitude,
  ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 END), 2) AS revenue,
  ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS profit,
  COUNT(*) AS unit_orders_placed,
  SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
  SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
  SUM(CASE WHEN oi.status = 'Cancelled' THEN 1 ELSE 0 END) AS units_cancelled,
  SUM(CASE WHEN oi.status IN ('Shipped', 'Processing') THEN 1 ELSE 0 END) AS units_en_route,
  ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
  ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit,
  COUNT(DISTINCT p.id) AS unique_products
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
JOIN `bigquery-public-data.thelook_ecommerce.distribution_centers` AS dc
ON p.distribution_center_id = dc.id
GROUP BY distribution_center_id, distribution_center_name, dc_latitude, dc_longitude
),
second_layer AS (
SELECT
  *,
  ROUND((profit / NULLIF(revenue, 0)), 4) AS profit_margin,
  ROUND(units_returned / NULLIF(units_completed + units_returned, 0), 4) AS return_rate,
  ROUND(units_completed / NULLIF(unit_orders_placed - units_cancelled, 0), 4) AS completion_rate,
  ROUND(units_cancelled / NULLIF(unit_orders_placed, 0), 4) AS cancellation_rate,
  ROUND(units_en_route / NULLIF(unit_orders_placed - (units_cancelled + units_returned), 0), 4) AS en_route_rate,
  ROUND(revenue / SUM(revenue) OVER(), 7) AS revenue_share,
  ROUND(profit / SUM(profit) OVER(), 7) AS profit_share,
  ROUND(unit_orders_placed / SUM(unit_orders_placed) OVER(), 7) AS unit_orders_placed_share
FROM first_layer
)
SELECT
  *,
  RANK() OVER(ORDER BY revenue DESC) AS revenue_rank,
  RANK() OVER(ORDER BY profit DESC) AS profit_rank,
  RANK() OVER(ORDER BY unit_orders_placed DESC) AS unit_orders_placed_rank,
  RANK() OVER(ORDER BY units_completed DESC) AS units_completed_rank,
  RANK() OVER(ORDER BY units_returned DESC) AS units_returned_rank,
  RANK() OVER(ORDER BY lost_revenue DESC) AS lost_revenue_rank,
  RANK() OVER(ORDER BY lost_profit DESC) AS lost_profit_rank,
  RANK() OVER(ORDER BY profit_margin DESC) AS profit_margin_rank,
  RANK() OVER(ORDER BY return_rate DESC) AS return_rate_rank,
  RANK() OVER(ORDER BY unique_products DESC) AS unique_products_rank
FROM second_layer
ORDER BY
  lost_revenue_rank ASC;