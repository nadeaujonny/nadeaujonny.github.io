/*
================================================================================
  SUPPLY CHAIN ANALYTICS — DEMAND & SALES EXTRACTION QUERIES
  03_demand_queries.sql
  
  Oracle Autonomous Database (19c)
  Author: Jonathan Nadeau
  
  These queries extract and analyze demand patterns from the order data to
  feed the Demand Forecasting dashboard (Page 2) and provide inputs for
  ABC/XYZ classification and MRP planning.
  
  SQL techniques demonstrated:
    - CTEs (Common Table Expressions)
    - Window functions (AVG OVER, SUM OVER, LAG, RANK)
    - Date truncation and aggregation
    - Rolling averages and cumulative calculations
    - Coefficient of variation for demand variability
  
  Data range: Jan 2015 – Jan 2018 (~180K order items, 50 categories)
================================================================================
*/


-- ============================================================================
-- QUERY 1: Monthly Order Volume by Category
-- Purpose: Build the core time series for demand forecasting
-- Feeds: Page 2 demand trend line charts, Excel Forecast Sheet input
-- Techniques: CTE, TRUNC for month aggregation, GROUP BY
-- ============================================================================
SELECT
    TRUNC(o.ORDER_DATE, 'MM')       AS ORDER_MONTH,
    p.CATEGORY_NAME,
    COUNT(oi.ORDER_ITEM_ID)         AS ORDER_ITEM_COUNT,
    SUM(oi.QUANTITY)                 AS TOTAL_UNITS,
    ROUND(SUM(oi.SALES), 2)         AS TOTAL_REVENUE
FROM ORDER_ITEMS oi
JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
GROUP BY TRUNC(o.ORDER_DATE, 'MM'), p.CATEGORY_NAME
ORDER BY p.CATEGORY_NAME, ORDER_MONTH;


-- ============================================================================
-- QUERY 2: Monthly Demand with Rolling Averages
-- Purpose: Smooth demand trends and identify seasonality patterns
-- Feeds: Page 2 moving average overlay charts
-- Techniques: CTE, Window functions (AVG OVER ROWS BETWEEN)
-- ============================================================================
WITH monthly_demand AS (
    SELECT
        TRUNC(o.ORDER_DATE, 'MM')       AS ORDER_MONTH,
        p.CATEGORY_NAME,
        COUNT(oi.ORDER_ITEM_ID)         AS ITEM_COUNT,
        SUM(oi.QUANTITY)                 AS TOTAL_UNITS,
        ROUND(SUM(oi.SALES), 2)         AS REVENUE
    FROM ORDER_ITEMS oi
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
    GROUP BY TRUNC(o.ORDER_DATE, 'MM'), p.CATEGORY_NAME
)
SELECT
    ORDER_MONTH,
    CATEGORY_NAME,
    TOTAL_UNITS,
    REVENUE,
    ROUND(AVG(TOTAL_UNITS) OVER (
        PARTITION BY CATEGORY_NAME
        ORDER BY ORDER_MONTH
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS ROLLING_3M_AVG_UNITS,
    ROUND(AVG(TOTAL_UNITS) OVER (
        PARTITION BY CATEGORY_NAME
        ORDER BY ORDER_MONTH
        ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
    ), 2) AS ROLLING_6M_AVG_UNITS,
    ROUND(AVG(REVENUE) OVER (
        PARTITION BY CATEGORY_NAME
        ORDER BY ORDER_MONTH
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS ROLLING_3M_AVG_REVENUE
FROM monthly_demand
ORDER BY CATEGORY_NAME, ORDER_MONTH;


-- ============================================================================
-- QUERY 3: Period-over-Period Demand Comparison (YoY)
-- Purpose: Identify growth/decline trends per category
-- Feeds: Page 1 YoY comparison KPIs, Page 2 trend analysis
-- Techniques: CTE, LAG window function for prior period comparison
-- ============================================================================
WITH monthly_demand AS (
    SELECT
        TRUNC(o.ORDER_DATE, 'MM')       AS ORDER_MONTH,
        p.CATEGORY_NAME,
        SUM(oi.QUANTITY)                 AS TOTAL_UNITS,
        ROUND(SUM(oi.SALES), 2)         AS REVENUE
    FROM ORDER_ITEMS oi
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
    GROUP BY TRUNC(o.ORDER_DATE, 'MM'), p.CATEGORY_NAME
)
SELECT
    ORDER_MONTH,
    CATEGORY_NAME,
    TOTAL_UNITS,
    REVENUE,
    LAG(TOTAL_UNITS, 12) OVER (
        PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
    ) AS UNITS_PRIOR_YEAR,
    LAG(REVENUE, 12) OVER (
        PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
    ) AS REVENUE_PRIOR_YEAR,
    CASE
        WHEN LAG(TOTAL_UNITS, 12) OVER (
            PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
        ) > 0 THEN
            ROUND(
                (TOTAL_UNITS - LAG(TOTAL_UNITS, 12) OVER (
                    PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
                )) * 100.0 /
                LAG(TOTAL_UNITS, 12) OVER (
                    PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
                ), 2
            )
        ELSE NULL
    END AS YOY_UNITS_CHANGE_PCT,
    CASE
        WHEN LAG(REVENUE, 12) OVER (
            PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
        ) > 0 THEN
            ROUND(
                (REVENUE - LAG(REVENUE, 12) OVER (
                    PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
                )) * 100.0 /
                LAG(REVENUE, 12) OVER (
                    PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
                ), 2
            )
        ELSE NULL
    END AS YOY_REVENUE_CHANGE_PCT
FROM monthly_demand
ORDER BY CATEGORY_NAME, ORDER_MONTH;


-- ============================================================================
-- QUERY 4: Demand Variability by Category (for XYZ Classification)
-- Purpose: Calculate coefficient of variation per category to classify
--          demand stability (X = stable, Y = moderate, Z = volatile)
-- Feeds: Page 3 ABC/XYZ matrix, inventory policy recommendations
-- Techniques: CTE, STDDEV, AVG, CASE for classification
-- ============================================================================
WITH monthly_demand AS (
    SELECT
        p.CATEGORY_NAME,
        TRUNC(o.ORDER_DATE, 'MM')       AS ORDER_MONTH,
        SUM(oi.QUANTITY)                 AS MONTHLY_UNITS
    FROM ORDER_ITEMS oi
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
    GROUP BY p.CATEGORY_NAME, TRUNC(o.ORDER_DATE, 'MM')
),
variability AS (
    SELECT
        CATEGORY_NAME,
        ROUND(AVG(MONTHLY_UNITS), 2)        AS AVG_MONTHLY_DEMAND,
        ROUND(STDDEV(MONTHLY_UNITS), 2)     AS STDDEV_DEMAND,
        ROUND(
            STDDEV(MONTHLY_UNITS) / NULLIF(AVG(MONTHLY_UNITS), 0), 4
        )                                    AS COEFF_OF_VARIATION,
        MIN(MONTHLY_UNITS)                   AS MIN_MONTH,
        MAX(MONTHLY_UNITS)                   AS MAX_MONTH,
        COUNT(*)                             AS MONTHS_WITH_DEMAND
    FROM monthly_demand
    GROUP BY CATEGORY_NAME
)
SELECT
    CATEGORY_NAME,
    AVG_MONTHLY_DEMAND,
    STDDEV_DEMAND,
    COEFF_OF_VARIATION,
    MIN_MONTH,
    MAX_MONTH,
    MONTHS_WITH_DEMAND,
    CASE
        WHEN COEFF_OF_VARIATION <= 0.5  THEN 'X'   -- Stable demand
        WHEN COEFF_OF_VARIATION <= 1.0  THEN 'Y'   -- Moderate variability
        ELSE                                 'Z'    -- Highly volatile
    END AS XYZ_CLASS
FROM variability
ORDER BY COEFF_OF_VARIATION;


-- ============================================================================
-- QUERY 5: Sell-In History by Category and Market with Rolling Averages
-- Purpose: Analyze demand patterns across different markets
-- Feeds: Page 2 market-level demand analysis
-- Techniques: CTE, Window functions, multi-level GROUP BY
-- ============================================================================
WITH market_demand AS (
    SELECT
        TRUNC(o.ORDER_DATE, 'MM')       AS ORDER_MONTH,
        o.MARKET,
        p.CATEGORY_NAME,
        SUM(oi.QUANTITY)                 AS TOTAL_UNITS,
        ROUND(SUM(oi.SALES), 2)         AS REVENUE,
        COUNT(DISTINCT o.ORDER_ID)      AS ORDER_COUNT
    FROM ORDER_ITEMS oi
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
    GROUP BY TRUNC(o.ORDER_DATE, 'MM'), o.MARKET, p.CATEGORY_NAME
)
SELECT
    ORDER_MONTH,
    MARKET,
    CATEGORY_NAME,
    TOTAL_UNITS,
    REVENUE,
    ORDER_COUNT,
    ROUND(AVG(TOTAL_UNITS) OVER (
        PARTITION BY MARKET, CATEGORY_NAME
        ORDER BY ORDER_MONTH
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS ROLLING_3M_AVG
FROM market_demand
ORDER BY MARKET, CATEGORY_NAME, ORDER_MONTH;


-- ============================================================================
-- QUERY 6: Weekly Demand Granularity (for short-term forecasting)
-- Purpose: Provide weekly-level demand data for near-term planning
-- Feeds: Short-term demand planning, MRP near-horizon inputs
-- Techniques: TRUNC with 'IW' for ISO week, GROUP BY
-- ============================================================================
SELECT
    TRUNC(o.ORDER_DATE, 'IW')       AS ORDER_WEEK,
    p.CATEGORY_NAME,
    COUNT(oi.ORDER_ITEM_ID)         AS ITEM_COUNT,
    SUM(oi.QUANTITY)                 AS TOTAL_UNITS,
    ROUND(SUM(oi.SALES), 2)         AS REVENUE
FROM ORDER_ITEMS oi
JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
GROUP BY TRUNC(o.ORDER_DATE, 'IW'), p.CATEGORY_NAME
ORDER BY p.CATEGORY_NAME, ORDER_WEEK;


-- ============================================================================
-- QUERY 7: Top 10 Categories by Revenue (with Ranking)
-- Purpose: Identify highest-value categories for prioritization
-- Feeds: Page 1 revenue bar chart, ABC classification inputs
-- Techniques: CTE, RANK window function, revenue concentration
-- ============================================================================
WITH category_revenue AS (
    SELECT
        p.CATEGORY_NAME,
        ROUND(SUM(oi.SALES), 2)              AS TOTAL_REVENUE,
        SUM(oi.QUANTITY)                      AS TOTAL_UNITS,
        COUNT(DISTINCT o.ORDER_ID)            AS TOTAL_ORDERS,
        ROUND(AVG(oi.SALES), 2)              AS AVG_ORDER_VALUE
    FROM ORDER_ITEMS oi
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
    GROUP BY p.CATEGORY_NAME
)
SELECT
    CATEGORY_NAME,
    TOTAL_REVENUE,
    TOTAL_UNITS,
    TOTAL_ORDERS,
    AVG_ORDER_VALUE,
    RANK() OVER (ORDER BY TOTAL_REVENUE DESC) AS REVENUE_RANK,
    ROUND(
        TOTAL_REVENUE * 100.0 / SUM(TOTAL_REVENUE) OVER (), 2
    ) AS PCT_OF_TOTAL_REVENUE,
    ROUND(
        SUM(TOTAL_REVENUE) OVER (ORDER BY TOTAL_REVENUE DESC 
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) * 100.0 / SUM(TOTAL_REVENUE) OVER (), 2
    ) AS CUMULATIVE_REVENUE_PCT
FROM category_revenue
ORDER BY REVENUE_RANK
FETCH FIRST 10 ROWS ONLY;


-- ============================================================================
-- QUERY 8: Demand Summary Dashboard Metrics
-- Purpose: High-level KPIs for the executive overview
-- Feeds: Page 1 KPI cards
-- Techniques: Aggregation, CASE WHEN, date arithmetic
-- ============================================================================
SELECT
    COUNT(DISTINCT o.ORDER_ID)                           AS TOTAL_ORDERS,
    COUNT(oi.ORDER_ITEM_ID)                              AS TOTAL_LINE_ITEMS,
    ROUND(SUM(oi.SALES), 2)                              AS TOTAL_REVENUE,
    ROUND(AVG(oi.SALES), 2)                              AS AVG_ITEM_REVENUE,
    ROUND(SUM(oi.PROFIT_PER_ORDER), 2)                   AS TOTAL_PROFIT,
    ROUND(
        SUM(oi.PROFIT_PER_ORDER) * 100.0 / 
        NULLIF(SUM(oi.SALES), 0), 2
    )                                                     AS PROFIT_MARGIN_PCT,
    COUNT(DISTINCT p.CATEGORY_NAME)                       AS ACTIVE_CATEGORIES,
    COUNT(DISTINCT p.PRODUCT_CARD_ID)                     AS ACTIVE_PRODUCTS,
    COUNT(DISTINCT oi.CUSTOMER_ID)                        AS UNIQUE_CUSTOMERS,
    ROUND(
        MONTHS_BETWEEN(MAX(o.ORDER_DATE), MIN(o.ORDER_DATE)), 1
    )                                                     AS DATA_SPAN_MONTHS
FROM ORDER_ITEMS oi
JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD');