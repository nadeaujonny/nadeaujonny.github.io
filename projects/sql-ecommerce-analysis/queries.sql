/* =========================================================
   BUSINESS QUESTION:
   What are the top 10 products by total revenue?

   DATASET:
   bigquery-public-data.thelook_ecommerce

   METRICS:
   - total_revenue
   - total_profit
   - units_sold

   SQL FEATURES:
   - joins
   - filtering
   - grouping
   - ordering
   - SUM aggregations
========================================================= */

SELECT 
  p.name AS product_name,
  p.category AS product_category,
  ROUND(SUM(oi.sale_price), 2) AS total_revenue,
  ROUND(SUM(oi.sale_price - p.cost), 2) AS total_profit,
  COUNT(*) AS units_sold

FROM `bigquery-public-data.thelook_ecommerce.products` AS p
JOIN `bigquery-public-data.thelook_ecommerce.order_items` AS oi
  ON p.id = oi.product_id
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
  ON o.order_id = oi.order_id

WHERE o.status = 'Complete'

GROUP BY product_name, product_category

ORDER BY total_revenue DESC
LIMIT 10;

---

/* =========================================================
   BUSINESS QUESTION:
   What are the top 10 products by total profit?

   DATASET:
   bigquery-public-data.thelook_ecommerce

   METRICS:
   - total_revenue
   - total_profit
   - units_sold

   SQL FEATURES:
   - CTE
========================================================= */

WITH product_profit AS (
  SELECT
    p.id AS product_id,
    p.name AS product_name,
    ROUND(SUM(oi.sale_price), 2) AS revenue,
    ROUND(SUM(oi.sale_price - p.cost), 2) AS profit,
    COUNT(*) AS units_sold
  FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` o
    ON oi.order_id = o.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` p
    ON oi.product_id = p.id
  WHERE o.status = 'Complete'
  GROUP BY p.id, p.name
)

   
SELECT *
FROM product_profit
ORDER BY profit DESC
LIMIT 10;

---

/* =========================================================
   BUSINESS QUESTION:
   What are the top 10 brands by profit?

   DATASET:
   bigquery-public-data.thelook_ecommerce

   METRICS:
   - revenue
   - profit
   - units_sold

   SQL FEATURES:
   - CTEs
   - window functions
========================================================= */

WITH brand_metrics AS (
  SELECT
    p.brand,
    ROUND(SUM(oi.sale_price), 2) AS revenue,
    ROUND(SUM(oi.sale_price - p.cost), 2) AS profit,
    COUNT(*) AS units_sold
  FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` o
    ON oi.order_id = o.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` p
    ON oi.product_id = p.id
  WHERE o.status = 'Complete'
  GROUP BY p.brand
),

ranked_brands AS (
  SELECT *,
         RANK() OVER (ORDER BY profit DESC) AS profit_rank,
         RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
  FROM brand_metrics
)

SELECT *
FROM ranked_brands
ORDER BY profit_rank
LIMIT 10;
