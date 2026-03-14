/*
================================================================================
  SUPPLY CHAIN ANALYTICS — INVENTORY & FULFILLMENT QUERIES
  04_inventory_fulfillment_queries.sql
  
  Oracle Autonomous Database (19c)
  Author: Jonathan Nadeau
  
  Two query groups:
    A) Inventory & Product Analytics (feeds Page 3: Inventory Optimization)
       - ABC classification by revenue (Pareto/80-20)
       - Combined ABC-XYZ matrix with policy recommendations
       - Product master summary with planning parameters
       - Average daily demand and lead time inputs
  
    B) Fulfillment & Logistics Performance (feeds Page 4: Fulfillment)
       - On-time delivery rate by month
       - Lead time variance (planned vs actual)
       - Late delivery root cause analysis
       - Shipping mode performance comparison
       - Regional delivery performance
  
  SQL techniques demonstrated:
    - Cumulative SUM for Pareto analysis
    - CASE WHEN for classification logic
    - RANK / DENSE_RANK for root cause ranking
    - Multi-table JOINs across all 5 tables
    - Date arithmetic for lead time calculations
================================================================================
*/


-- ============================================================================
-- A. INVENTORY & PRODUCT ANALYTICS
-- ============================================================================


-- ============================================================================
-- QUERY 1: ABC Classification by Revenue (Pareto Analysis)
-- Purpose: Classify categories into A (top 80%), B (next 15%), C (bottom 5%)
-- Feeds: Page 3 ABC classification, inventory policy table
-- Techniques: CTE, cumulative SUM window function, CASE for classification
-- ============================================================================
WITH category_revenue AS (
    SELECT
        p.CATEGORY_NAME,
        ROUND(SUM(oi.SALES), 2)      AS TOTAL_REVENUE,
        SUM(oi.QUANTITY)              AS TOTAL_UNITS,
        COUNT(oi.ORDER_ITEM_ID)       AS TOTAL_ITEMS
    FROM ORDER_ITEMS oi
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
    GROUP BY p.CATEGORY_NAME
),
ranked AS (
    SELECT
        CATEGORY_NAME,
        TOTAL_REVENUE,
        TOTAL_UNITS,
        TOTAL_ITEMS,
        ROUND(
            TOTAL_REVENUE * 100.0 / SUM(TOTAL_REVENUE) OVER (), 2
        ) AS PCT_OF_REVENUE,
        ROUND(
            SUM(TOTAL_REVENUE) OVER (
                ORDER BY TOTAL_REVENUE DESC
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) * 100.0 / SUM(TOTAL_REVENUE) OVER (), 2
        ) AS CUMULATIVE_PCT,
        RANK() OVER (ORDER BY TOTAL_REVENUE DESC) AS REVENUE_RANK
    FROM category_revenue
)
SELECT
    CATEGORY_NAME,
    TOTAL_REVENUE,
    TOTAL_UNITS,
    PCT_OF_REVENUE,
    CUMULATIVE_PCT,
    REVENUE_RANK,
    CASE
        WHEN CUMULATIVE_PCT <= 80 THEN 'A'
        WHEN CUMULATIVE_PCT <= 95 THEN 'B'
        ELSE 'C'
    END AS ABC_CLASS
FROM ranked
ORDER BY REVENUE_RANK;


-- ============================================================================
-- QUERY 2: Combined ABC-XYZ Classification Matrix
-- Purpose: Cross-reference revenue importance (ABC) with demand stability (XYZ)
--          to produce inventory policy recommendations per category
-- Feeds: Page 3 ABC-XYZ heatmap, policy recommendation table
-- Techniques: Multiple CTEs, CASE for dual classification and policy logic
-- ============================================================================
WITH category_revenue AS (
    SELECT
        p.CATEGORY_NAME,
        ROUND(SUM(oi.SALES), 2) AS TOTAL_REVENUE
    FROM ORDER_ITEMS oi
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
    GROUP BY p.CATEGORY_NAME
),
abc AS (
    SELECT
        CATEGORY_NAME,
        TOTAL_REVENUE,
        CASE
            WHEN SUM(TOTAL_REVENUE) OVER (
                ORDER BY TOTAL_REVENUE DESC
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) * 100.0 / SUM(TOTAL_REVENUE) OVER () <= 80 THEN 'A'
            WHEN SUM(TOTAL_REVENUE) OVER (
                ORDER BY TOTAL_REVENUE DESC
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) * 100.0 / SUM(TOTAL_REVENUE) OVER () <= 95 THEN 'B'
            ELSE 'C'
        END AS ABC_CLASS
    FROM category_revenue
),
monthly_demand AS (
    SELECT
        p.CATEGORY_NAME,
        TRUNC(o.ORDER_DATE, 'MM') AS ORDER_MONTH,
        SUM(oi.QUANTITY) AS MONTHLY_UNITS
    FROM ORDER_ITEMS oi
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
    GROUP BY p.CATEGORY_NAME, TRUNC(o.ORDER_DATE, 'MM')
),
xyz AS (
    SELECT
        CATEGORY_NAME,
        ROUND(AVG(MONTHLY_UNITS), 2)    AS AVG_DEMAND,
        ROUND(STDDEV(MONTHLY_UNITS), 2) AS STDDEV_DEMAND,
        ROUND(STDDEV(MONTHLY_UNITS) / NULLIF(AVG(MONTHLY_UNITS), 0), 4) AS CV,
        CASE
            WHEN STDDEV(MONTHLY_UNITS) / NULLIF(AVG(MONTHLY_UNITS), 0) <= 0.5 THEN 'X'
            WHEN STDDEV(MONTHLY_UNITS) / NULLIF(AVG(MONTHLY_UNITS), 0) <= 1.0 THEN 'Y'
            ELSE 'Z'
        END AS XYZ_CLASS
    FROM monthly_demand
    GROUP BY CATEGORY_NAME
)
SELECT
    a.CATEGORY_NAME,
    a.ABC_CLASS,
    x.XYZ_CLASS,
    a.ABC_CLASS || '-' || x.XYZ_CLASS AS MATRIX_CELL,
    a.TOTAL_REVENUE,
    x.AVG_DEMAND,
    x.CV,
    CASE
        WHEN a.ABC_CLASS = 'A' AND x.XYZ_CLASS = 'X' THEN 'JIT/Kanban — low safety stock, frequent small orders'
        WHEN a.ABC_CLASS = 'A' AND x.XYZ_CLASS = 'Y' THEN 'Moderate safety stock — demand-driven replenishment'
        WHEN a.ABC_CLASS = 'A' AND x.XYZ_CLASS = 'Z' THEN 'High safety stock — buffer against volatility, close monitoring'
        WHEN a.ABC_CLASS = 'B' AND x.XYZ_CLASS = 'X' THEN 'Standard replenishment — EOQ with periodic review'
        WHEN a.ABC_CLASS = 'B' AND x.XYZ_CLASS = 'Y' THEN 'Moderate safety stock — balanced ordering frequency'
        WHEN a.ABC_CLASS = 'B' AND x.XYZ_CLASS = 'Z' THEN 'Higher safety stock — consider make-to-order for some items'
        WHEN a.ABC_CLASS = 'C' AND x.XYZ_CLASS = 'X' THEN 'Low priority — large infrequent orders to minimize cost'
        WHEN a.ABC_CLASS = 'C' AND x.XYZ_CLASS = 'Y' THEN 'Minimal stock — order on demand where possible'
        WHEN a.ABC_CLASS = 'C' AND x.XYZ_CLASS = 'Z' THEN 'Evaluate for discontinuation — high risk, low reward'
    END AS INVENTORY_POLICY
FROM abc a
JOIN xyz x ON a.CATEGORY_NAME = x.CATEGORY_NAME
ORDER BY a.ABC_CLASS, x.XYZ_CLASS, a.TOTAL_REVENUE DESC;


-- ============================================================================
-- QUERY 3: Product Master Summary with Planning Parameters
-- Purpose: Create a single reference table per category with all planning inputs
-- Feeds: Page 3 inventory health table, MRP parameter inputs
-- Techniques: Multi-table JOIN, aggregation, date arithmetic
-- ============================================================================
WITH demand_stats AS (
    SELECT
        p.CATEGORY_NAME,
        COUNT(oi.ORDER_ITEM_ID) AS TOTAL_LINE_ITEMS,
        SUM(oi.QUANTITY) AS TOTAL_UNITS,
        ROUND(SUM(oi.SALES), 2) AS TOTAL_REVENUE,
        ROUND(AVG(oi.SALES), 2) AS AVG_ITEM_VALUE,
        ROUND(
            SUM(oi.QUANTITY) /
            GREATEST(EXTRACT(DAY FROM (MAX(o.ORDER_DATE) - MIN(o.ORDER_DATE))), 1),
            4
        ) AS AVG_DAILY_DEMAND
    FROM ORDER_ITEMS oi
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
    GROUP BY p.CATEGORY_NAME
),
ship_stats AS (
    SELECT
        p.CATEGORY_NAME,
        ROUND(AVG(s.DAYS_SHIPPING_REAL), 2) AS AVG_ACTUAL_LEAD_TIME,
        ROUND(AVG(s.DAYS_SHIPPING_SCHED), 2) AS AVG_SCHED_LEAD_TIME,
        ROUND(AVG(s.DAYS_SHIPPING_REAL - s.DAYS_SHIPPING_SCHED), 2) AS AVG_LEAD_TIME_VARIANCE
    FROM SHIPMENTS s
    JOIN ORDER_ITEMS oi ON s.ORDER_ITEM_ID = oi.ORDER_ITEM_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    GROUP BY p.CATEGORY_NAME
),
inv AS (
    SELECT CATEGORY_NAME, ON_HAND_QTY, AVAILABLE_QTY
    FROM INVENTORY_SNAPSHOT
)
SELECT
    d.CATEGORY_NAME,
    d.TOTAL_UNITS,
    d.TOTAL_REVENUE,
    d.AVG_ITEM_VALUE,
    d.AVG_DAILY_DEMAND,
    ss.AVG_ACTUAL_LEAD_TIME,
    ss.AVG_SCHED_LEAD_TIME,
    ss.AVG_LEAD_TIME_VARIANCE,
    i.ON_HAND_QTY AS CURRENT_ON_HAND,
    i.AVAILABLE_QTY AS CURRENT_AVAILABLE,
    CASE
        WHEN d.AVG_DAILY_DEMAND > 0 THEN
            ROUND(i.AVAILABLE_QTY / d.AVG_DAILY_DEMAND, 1)
        ELSE NULL
    END AS DAYS_OF_SUPPLY,
    CASE
        WHEN d.AVG_DAILY_DEMAND > 0 AND i.AVAILABLE_QTY / d.AVG_DAILY_DEMAND < ss.AVG_ACTUAL_LEAD_TIME THEN 'CRITICAL'
        WHEN d.AVG_DAILY_DEMAND > 0 AND i.AVAILABLE_QTY / d.AVG_DAILY_DEMAND < ss.AVG_ACTUAL_LEAD_TIME * 2 THEN 'LOW'
        ELSE 'HEALTHY'
    END AS STOCK_STATUS
FROM demand_stats d
LEFT JOIN ship_stats ss ON d.CATEGORY_NAME = ss.CATEGORY_NAME
LEFT JOIN inv i ON d.CATEGORY_NAME = i.CATEGORY_NAME
ORDER BY d.TOTAL_REVENUE DESC;


-- ============================================================================
-- B. FULFILLMENT & LOGISTICS PERFORMANCE
-- ============================================================================


-- ============================================================================
-- QUERY 4: Monthly On-Time Delivery Rate
-- Purpose: Track delivery performance over time
-- Feeds: Page 1 KPI trend, Page 4 delivery trend chart
-- Techniques: CASE WHEN for conditional counting, date truncation
-- ============================================================================
SELECT
    TRUNC(o.ORDER_DATE, 'MM') AS ORDER_MONTH,
    COUNT(s.SHIPMENT_ID) AS TOTAL_SHIPMENTS,
    SUM(CASE WHEN s.DELIVERY_STATUS = 'Shipping on time' THEN 1 ELSE 0 END) AS ON_TIME,
    SUM(CASE WHEN s.DELIVERY_STATUS = 'Advance shipping' THEN 1 ELSE 0 END) AS EARLY,
    SUM(CASE WHEN s.DELIVERY_STATUS = 'Late delivery' THEN 1 ELSE 0 END) AS LATE,
    SUM(CASE WHEN s.DELIVERY_STATUS = 'Shipping canceled' THEN 1 ELSE 0 END) AS CANCELED,
    ROUND(
        SUM(CASE WHEN s.DELIVERY_STATUS IN ('Shipping on time', 'Advance shipping') THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0), 2
    ) AS ON_TIME_PCT,
    ROUND(
        SUM(CASE WHEN s.DELIVERY_STATUS = 'Late delivery' THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0), 2
    ) AS LATE_PCT
FROM SHIPMENTS s
JOIN ORDER_ITEMS oi ON s.ORDER_ITEM_ID = oi.ORDER_ITEM_ID
JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
GROUP BY TRUNC(o.ORDER_DATE, 'MM')
ORDER BY ORDER_MONTH;


-- ============================================================================
-- QUERY 5: Lead Time Variance Analysis (Planned vs Actual)
-- Purpose: Compare scheduled vs actual shipping days by category and mode
-- Feeds: Page 4 planned vs actual chart, lead time variance analysis
-- Techniques: AVG, GROUP BY multi-level, variance calculation
-- ============================================================================
SELECT
    p.CATEGORY_NAME,
    s.SHIPPING_MODE,
    COUNT(s.SHIPMENT_ID) AS SHIPMENT_COUNT,
    ROUND(AVG(s.DAYS_SHIPPING_SCHED), 2) AS AVG_PLANNED_DAYS,
    ROUND(AVG(s.DAYS_SHIPPING_REAL), 2) AS AVG_ACTUAL_DAYS,
    ROUND(AVG(s.DAYS_SHIPPING_REAL - s.DAYS_SHIPPING_SCHED), 2) AS AVG_VARIANCE,
    ROUND(STDDEV(s.DAYS_SHIPPING_REAL - s.DAYS_SHIPPING_SCHED), 2) AS STDDEV_VARIANCE,
    SUM(CASE WHEN s.DAYS_SHIPPING_REAL > s.DAYS_SHIPPING_SCHED THEN 1 ELSE 0 END) AS LATE_COUNT,
    ROUND(
        SUM(CASE WHEN s.DAYS_SHIPPING_REAL > s.DAYS_SHIPPING_SCHED THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0), 2
    ) AS LATE_PCT
FROM SHIPMENTS s
JOIN ORDER_ITEMS oi ON s.ORDER_ITEM_ID = oi.ORDER_ITEM_ID
JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
GROUP BY p.CATEGORY_NAME, s.SHIPPING_MODE
ORDER BY p.CATEGORY_NAME, s.SHIPPING_MODE;


-- ============================================================================
-- QUERY 6: Late Delivery Root Cause Analysis
-- Purpose: Identify which categories, regions, and shipping modes drive late deliveries
-- Feeds: Page 4 Key Influencers / Decomposition Tree visual
-- Techniques: RANK/DENSE_RANK, multi-dimension GROUP BY, percentage calculation
-- ============================================================================

-- 6a: Top categories by late delivery rate
SELECT
    p.CATEGORY_NAME,
    COUNT(s.SHIPMENT_ID) AS TOTAL_SHIPMENTS,
    SUM(CASE WHEN s.LATE_DELIVERY_RISK = 1 THEN 1 ELSE 0 END) AS LATE_DELIVERIES,
    ROUND(
        SUM(CASE WHEN s.LATE_DELIVERY_RISK = 1 THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0), 2
    ) AS LATE_DELIVERY_PCT,
    DENSE_RANK() OVER (
        ORDER BY SUM(CASE WHEN s.LATE_DELIVERY_RISK = 1 THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0) DESC
    ) AS LATE_RANK
FROM SHIPMENTS s
JOIN ORDER_ITEMS oi ON s.ORDER_ITEM_ID = oi.ORDER_ITEM_ID
JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
GROUP BY p.CATEGORY_NAME
ORDER BY LATE_DELIVERY_PCT DESC;

-- 6b: Top regions by late delivery rate
SELECT
    o.ORDER_REGION,
    COUNT(s.SHIPMENT_ID) AS TOTAL_SHIPMENTS,
    SUM(CASE WHEN s.LATE_DELIVERY_RISK = 1 THEN 1 ELSE 0 END) AS LATE_DELIVERIES,
    ROUND(
        SUM(CASE WHEN s.LATE_DELIVERY_RISK = 1 THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0), 2
    ) AS LATE_DELIVERY_PCT,
    DENSE_RANK() OVER (
        ORDER BY SUM(CASE WHEN s.LATE_DELIVERY_RISK = 1 THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0) DESC
    ) AS LATE_RANK
FROM SHIPMENTS s
JOIN ORDER_ITEMS oi ON s.ORDER_ITEM_ID = oi.ORDER_ITEM_ID
JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
GROUP BY o.ORDER_REGION
ORDER BY LATE_DELIVERY_PCT DESC;

-- 6c: Shipping mode performance comparison
SELECT
    s.SHIPPING_MODE,
    COUNT(s.SHIPMENT_ID) AS TOTAL_SHIPMENTS,
    ROUND(AVG(s.DAYS_SHIPPING_REAL), 2) AS AVG_ACTUAL_DAYS,
    ROUND(AVG(s.DAYS_SHIPPING_SCHED), 2) AS AVG_PLANNED_DAYS,
    SUM(CASE WHEN s.LATE_DELIVERY_RISK = 1 THEN 1 ELSE 0 END) AS LATE_DELIVERIES,
    ROUND(
        SUM(CASE WHEN s.LATE_DELIVERY_RISK = 1 THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0), 2
    ) AS LATE_PCT,
    SUM(CASE WHEN s.DELIVERY_STATUS = 'Advance shipping' THEN 1 ELSE 0 END) AS EARLY_DELIVERIES,
    ROUND(
        SUM(CASE WHEN s.DELIVERY_STATUS = 'Advance shipping' THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0), 2
    ) AS EARLY_PCT
FROM SHIPMENTS s
GROUP BY s.SHIPPING_MODE
ORDER BY LATE_PCT DESC;


-- ============================================================================
-- QUERY 7: Regional Delivery Performance Map Data
-- Purpose: Geographic breakdown of delivery performance for map visual
-- Feeds: Page 4 regional performance map
-- Techniques: Multi-level aggregation, percentage calculations
-- ============================================================================
SELECT
    o.ORDER_REGION,
    o.ORDER_COUNTRY,
    COUNT(s.SHIPMENT_ID) AS TOTAL_SHIPMENTS,
    ROUND(AVG(s.DAYS_SHIPPING_REAL), 2) AS AVG_DELIVERY_DAYS,
    ROUND(
        SUM(CASE WHEN s.DELIVERY_STATUS = 'Late delivery' THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0), 2
    ) AS LATE_PCT,
    ROUND(
        SUM(CASE WHEN s.DELIVERY_STATUS IN ('Shipping on time', 'Advance shipping') THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0), 2
    ) AS ON_TIME_PCT,
    ROUND(SUM(oi.SALES), 2) AS TOTAL_REVENUE
FROM SHIPMENTS s
JOIN ORDER_ITEMS oi ON s.ORDER_ITEM_ID = oi.ORDER_ITEM_ID
JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
GROUP BY o.ORDER_REGION, o.ORDER_COUNTRY
ORDER BY TOTAL_SHIPMENTS DESC;


-- ============================================================================
-- QUERY 8: Delivery Time Distribution (for Histogram)
-- Purpose: Show the distribution of actual delivery days
-- Feeds: Page 4 delivery time histogram
-- Techniques: CASE WHEN for bucketing, COUNT for distribution
-- ============================================================================
SELECT
    CASE
        WHEN s.DAYS_SHIPPING_REAL = 0 THEN '0 days (same day)'
        WHEN s.DAYS_SHIPPING_REAL = 1 THEN '1 day'
        WHEN s.DAYS_SHIPPING_REAL = 2 THEN '2 days'
        WHEN s.DAYS_SHIPPING_REAL = 3 THEN '3 days'
        WHEN s.DAYS_SHIPPING_REAL = 4 THEN '4 days'
        WHEN s.DAYS_SHIPPING_REAL = 5 THEN '5 days'
        WHEN s.DAYS_SHIPPING_REAL = 6 THEN '6 days'
        ELSE '7+ days'
    END AS DELIVERY_BUCKET,
    s.DAYS_SHIPPING_REAL,
    COUNT(*) AS SHIPMENT_COUNT,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS PCT_OF_TOTAL
FROM SHIPMENTS s
GROUP BY s.DAYS_SHIPPING_REAL,
    CASE
        WHEN s.DAYS_SHIPPING_REAL = 0 THEN '0 days (same day)'
        WHEN s.DAYS_SHIPPING_REAL = 1 THEN '1 day'
        WHEN s.DAYS_SHIPPING_REAL = 2 THEN '2 days'
        WHEN s.DAYS_SHIPPING_REAL = 3 THEN '3 days'
        WHEN s.DAYS_SHIPPING_REAL = 4 THEN '4 days'
        WHEN s.DAYS_SHIPPING_REAL = 5 THEN '5 days'
        WHEN s.DAYS_SHIPPING_REAL = 6 THEN '6 days'
        ELSE '7+ days'
    END
ORDER BY s.DAYS_SHIPPING_REAL;