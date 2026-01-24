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

---

/* =========================================================
   BUSINESS QUESTION:
   What are the top 10 products by profit margin?

   DATASET:
   bigquery-public-data.thelook_ecommerce

   METRICS:
   - revenue
   - profit
   - units_sold
   - profit margin

   SQL FEATURES:
   - CTEs
   - window functions
   - CASE Statements
========================================================= */

WITH product_totals AS (
  SELECT
    p.id AS product_id,
    p.name AS product_name,
    p.category AS product_category,
    SUM(oi.sale_price) AS revenue,
    SUM(oi.sale_price - p.cost) AS profit,
    COUNT(*) AS units_sold
  FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
    ON oi.order_id = o.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
    ON oi.product_id = p.id
  WHERE o.status = 'Complete'
  GROUP BY 1, 2, 3
),

metrics AS (
  SELECT
    product_id,
    product_name,
    product_category,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    units_sold,

    ROUND(profit / NULLIF(revenue, 0), 4) AS profit_margin,

    RANK() OVER (ORDER BY profit DESC) AS profit_rank,
    RANK() OVER (ORDER BY profit / NULLIF(revenue, 0) DESC) AS margin_rank,

    CASE
      WHEN revenue = 0 THEN 'Undefined'
      WHEN profit / revenue >= 0.50 THEN 'Very High (>= 50%)'
      WHEN profit / revenue >= 0.30 THEN 'High (30%–49.9%)'
      WHEN profit / revenue >= 0.15 THEN 'Medium (15%–29.9%)'
      WHEN profit / revenue > 0 THEN 'Low (0%–14.9%)'
      ELSE 'Negative (<= 0%)'
    END AS margin_tier
  FROM product_totals
)

SELECT *
FROM metrics
WHERE revenue > 0
  AND units_sold >= 3     
  AND revenue >= 50   --takes extremely low volume products out of the picture    
ORDER BY profit_margin DESC, profit DESC
LIMIT 10;
