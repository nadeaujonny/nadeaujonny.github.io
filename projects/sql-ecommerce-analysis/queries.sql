/* =========================================================
   ANALYSIS 1: Top Products by Revenue
   
   BUSINESS QUESTION:
   Which products generate the highest completed-sales revenue?
   
   DATASET:
   bigquery-public-data.thelook_ecommerce
   
   SQL FEATURES:
   - Multi-table joins
   - Aggregation (SUM, COUNT)
   - Filtering (WHERE)
   - Grouping and ordering
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
   ANALYSIS 2: Top Products by Profit
   
   BUSINESS QUESTION:
   Which products generate the highest total profit from 
   completed purchases?
   
   SQL FEATURES:
   - CTE (Common Table Expression)
   - Multi-table joins
   - Aggregation
========================================================= */

WITH product_profit AS (
  SELECT
    p.id AS product_id,
    p.name AS product_name,
    ROUND(SUM(oi.sale_price), 2) AS revenue,
    ROUND(SUM(oi.sale_price - p.cost), 2) AS profit,
    COUNT(*) AS units_sold
  FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
    ON oi.order_id = o.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
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
   ANALYSIS 3: Top Brands by Profit
   
   BUSINESS QUESTION:
   Which brands generate the highest total profit from 
   completed purchases?
   
   SQL FEATURES:
   - Multiple CTEs
   - Window functions (RANK)
   - Aggregation
========================================================= */

WITH brand_metrics AS (
  SELECT
    p.brand,
    ROUND(SUM(oi.sale_price), 2) AS revenue,
    ROUND(SUM(oi.sale_price - p.cost), 2) AS profit,
    COUNT(*) AS units_sold
  FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
    ON oi.order_id = o.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
    ON oi.product_id = p.id
  WHERE o.status = 'Complete'
  GROUP BY p.brand
),
ranked_brands AS (
  SELECT
    *,
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
   ANALYSIS 4: Top Products by Profit Margin
   
   BUSINESS QUESTION:
   Which products are most margin-efficient (profit ÷ revenue),
   after filtering out low-volume noise?
   
   SQL FEATURES:
   - Multiple CTEs
   - Window functions (RANK)
   - CASE statements for tiering
   - NULLIF for safe division
   - Business-relevant filtering
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
  AND revenue >= 50
ORDER BY profit_margin DESC, profit DESC
LIMIT 10;

---

/* =========================================================
   ANALYSIS 5: Top Products by Return Rate
   
   BUSINESS QUESTION:
   Which products have the highest return rates, and what 
   profit is at risk from those returns?
   
   SQL FEATURES:
   - Multiple CTEs
   - CASE statements for conditional aggregation
   - Window functions (RANK)
   - CASE statements for risk tiering
   - Complex metric engineering
========================================================= */

WITH product_status_counts AS (
  SELECT
    p.id AS product_id,
    p.name AS product_name,
    p.category AS product_category,
    COUNT(*) AS total_purchased_units,
    SUM(CASE WHEN o.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
    SUM(CASE WHEN o.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
    SUM(CASE WHEN o.status = 'Complete' THEN oi.sale_price ELSE 0 END) AS revenue,
    SUM(CASE WHEN o.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0 END) AS profit
  FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
    ON oi.order_id = o.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
    ON oi.product_id = p.id
  WHERE o.status IN ('Complete', 'Returned')
  GROUP BY 1, 2, 3
),
final AS (
  SELECT
    product_id,
    product_name,
    product_category,
    total_purchased_units AS units_purchased,
    units_completed,
    units_returned,
    ROUND(units_returned / NULLIF(total_purchased_units, 0) * 100, 2) AS return_rate_pct,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    ROUND(profit / NULLIF(units_completed, 0), 2) AS avg_profit_per_completed_unit,
    ROUND(units_returned * (profit / NULLIF(units_completed, 0)), 2) AS est_profit_lost_to_returns,
    RANK() OVER (ORDER BY units_returned / NULLIF(total_purchased_units, 0) DESC) AS return_rate_rank,
    RANK() OVER (ORDER BY units_returned DESC) AS returns_volume_rank,
    CASE
      WHEN total_purchased_units = 0 THEN 'Undefined'
      WHEN units_returned / NULLIF(total_purchased_units, 0) >= 0.30 THEN 'Very High (>= 30%)'
      WHEN units_returned / NULLIF(total_purchased_units, 0) >= 0.20 THEN 'High (20%–29.9%)'
      WHEN units_returned / NULLIF(total_purchased_units, 0) >= 0.10 THEN 'Medium (10%–19.9%)'
      WHEN units_returned > 0 THEN 'Low (0%–9.9%)'
      ELSE 'None (0%)'
    END AS return_risk_tier
  FROM product_status_counts
)
SELECT
  product_id,
  product_name,
  product_category,
  units_purchased,
  units_completed,
  units_returned,
  return_rate_pct,
  revenue,
  profit,
  avg_profit_per_completed_unit,
  est_profit_lost_to_returns,
  return_risk_tier,
  return_rate_rank,
  returns_volume_rank
FROM final
WHERE units_purchased >= 5
  AND revenue >= 50
ORDER BY return_rate_pct DESC, units_returned DESC, revenue DESC
LIMIT 10;

---

/* =========================================================
   ANALYSIS 6: Long-Term Trends in Revenue, Profit, and Returns
   
   BUSINESS QUESTION:
   How have revenue, profit, and return rates evolved over time,
   and what structural trends are visible?
   
   SQL FEATURES:
   - DATE_TRUNC for time grouping
   - Window functions (LAG, AVG with ROWS BETWEEN)
   - Month-over-month growth calculations
   - Rolling averages
========================================================= */

WITH base AS (
  SELECT
    DATE_TRUNC(DATE(o.created_at), MONTH) AS month,
    COUNT(*) AS total_units,
    SUM(CASE WHEN o.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
    SUM(CASE WHEN o.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
    SUM(CASE WHEN o.status = 'Complete' THEN oi.sale_price ELSE 0 END) AS revenue,
    SUM(CASE WHEN o.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0 END) AS profit
  FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
    ON oi.order_id = o.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
    ON oi.product_id = p.id
  WHERE o.status IN ('Complete', 'Returned')
  GROUP BY 1
),
metrics AS (
  SELECT
    month,
    total_units,
    units_completed,
    units_returned,
    ROUND(units_returned / NULLIF(total_units, 0) * 100, 2) AS return_rate_pct,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    ROUND(
      (revenue - LAG(revenue) OVER (ORDER BY month))
      / NULLIF(LAG(revenue) OVER (ORDER BY month), 0) * 100,
      2
    ) AS revenue_mom_growth_pct,
    ROUND(
      (profit - LAG(profit) OVER (ORDER BY month))
      / NULLIF(LAG(profit) OVER (ORDER BY month), 0) * 100,
      2
    ) AS profit_mom_growth_pct,
    ROUND(AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS revenue_3mo_avg,
    ROUND(AVG(profit) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS profit_3mo_avg
  FROM base
)
SELECT *
FROM metrics
ORDER BY month;

---

/* =========================================================
   ANALYSIS 7: Seasonal Trends in Revenue, Profit, and Returns
   
   BUSINESS QUESTION:
   How do revenue, profit, and return rates vary by month of 
   the year, and which seasons represent peak performance or 
   elevated return risk?
   
   SQL FEATURES:
   - EXTRACT for month number
   - FORMAT_DATE for month name
   - Aggregation by calendar month
========================================================= */

WITH base AS (
  SELECT
    EXTRACT(MONTH FROM DATE(o.created_at)) AS month_num,
    FORMAT_DATE('%B', DATE(o.created_at)) AS month_name,
    COUNT(*) AS total_units,
    SUM(CASE WHEN o.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
    SUM(CASE WHEN o.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
    SUM(CASE WHEN o.status = 'Complete' THEN oi.sale_price ELSE 0 END) AS revenue,
    SUM(CASE WHEN o.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0 END) AS profit
  FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
    ON oi.order_id = o.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
    ON oi.product_id = p.id
  WHERE o.status IN ('Complete', 'Returned')
  GROUP BY 1, 2
),
metrics AS (
  SELECT
    month_num,
    month_name,
    total_units AS units_purchased,
    units_completed,
    units_returned,
    ROUND(units_returned / NULLIF(total_units, 0) * 100, 2) AS return_rate_pct,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit
  FROM base
)
SELECT *
FROM metrics
ORDER BY month_num;

---

/* =========================================================
   ANALYSIS 8: Customer Lifetime Value (CLV) and Retention Patterns
   
   BUSINESS QUESTION:
   Which customers generate the highest lifetime profit, and 
   what purchasing patterns define high-value customers?
   
   SQL FEATURES:
   - Multiple CTEs
   - Aggregation at customer level
   - DATE_DIFF for tenure calculation
   - Window functions (RANK)
   - CLV metrics (AOV, lifetime profit)
========================================================= */

WITH completed_orders AS (
  SELECT
    o.user_id AS customer_id,
    o.order_id,
    o.created_at,
    oi.sale_price,
    p.cost
  FROM `bigquery-public-data.thelook_ecommerce.orders` AS o
  JOIN `bigquery-public-data.thelook_ecommerce.order_items` AS oi
    ON o.order_id = oi.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
    ON oi.product_id = p.id
  WHERE o.status = 'Complete'
),
customer_aggregates AS (
  SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items,
    ROUND(SUM(sale_price), 2) AS lifetime_revenue,
    ROUND(SUM(sale_price - cost), 2) AS lifetime_profit,
    MIN(created_at) AS first_purchase_date,
    MAX(created_at) AS last_purchase_date,
    DATE_DIFF(DATE(MAX(created_at)), DATE(MIN(created_at)), DAY) AS customer_tenure_days
  FROM completed_orders
  GROUP BY customer_id
),
final AS (
  SELECT
    *,
    ROUND(lifetime_revenue / NULLIF(total_orders, 0), 2) AS avg_order_value,
    ROUND(lifetime_profit / NULLIF(total_orders, 0), 2) AS avg_profit_per_order,
    RANK() OVER (ORDER BY lifetime_revenue DESC) AS revenue_rank,
    RANK() OVER (ORDER BY lifetime_profit DESC) AS profit_rank
  FROM customer_aggregates
)
SELECT *
FROM final
ORDER BY lifetime_profit DESC
LIMIT 20;
