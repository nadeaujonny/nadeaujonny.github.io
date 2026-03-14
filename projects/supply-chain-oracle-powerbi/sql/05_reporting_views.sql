/*
================================================================================
  SUPPLY CHAIN ANALYTICS — REPORTING VIEWS
  05_reporting_views.sql
  
  Oracle Autonomous Database (19c)
  Author: Jonathan Nadeau
  
  Six reporting views that package pre-calculated, analysis-ready data as
  single virtual tables. Power BI and Power Query connect directly to these
  views, so the extraction logic is defined once and reused on every refresh.
  
  Views:
    1. VW_DEMAND_TIMESERIES     — Monthly demand by category with rolling avgs
    2. VW_FULFILLMENT_KPI       — Monthly delivery performance metrics
    3. VW_PRODUCT_MASTER        — Category-level summary with ABC/XYZ and planning params
    4. VW_PLANNED_VS_ACTUAL     — Lead time variance by category and shipping mode
    5. VW_MRP_PLAN              — MRP output (populated after stored procedure runs)
    6. VW_FORECAST_VS_ACTUAL    — Forecast accuracy (populated after Excel write-back)
  
  Note: Views 5 and 6 depend on FORECAST_PLAN and MRP_REQUIREMENTS tables
  which are populated in Phase 4 (Excel forecasting) and Phase 2 (stored
  procedure). They are created now as structures so the full pipeline is
  in place, and will return data once those tables are populated.
================================================================================
*/


-- ============================================================================
-- Drop existing views (safe re-run)
-- ============================================================================
BEGIN EXECUTE IMMEDIATE 'DROP VIEW VW_DEMAND_TIMESERIES'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP VIEW VW_FULFILLMENT_KPI'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP VIEW VW_PRODUCT_MASTER'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP VIEW VW_PLANNED_VS_ACTUAL'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP VIEW VW_MRP_PLAN'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP VIEW VW_FORECAST_VS_ACTUAL'; EXCEPTION WHEN OTHERS THEN NULL; END;
/


-- ============================================================================
-- VIEW 1: VW_DEMAND_TIMESERIES
-- Monthly demand by category with rolling averages and YoY comparison
-- Feeds: Page 2 (Demand Forecasting), Excel Forecast Sheet input
-- ============================================================================
CREATE OR REPLACE VIEW VW_DEMAND_TIMESERIES AS
WITH monthly_raw AS (
    SELECT
        TRUNC(o.ORDER_DATE, 'MM')       AS ORDER_MONTH,
        p.CATEGORY_NAME,
        COUNT(oi.ORDER_ITEM_ID)         AS ITEM_COUNT,
        SUM(oi.QUANTITY)                 AS TOTAL_UNITS,
        ROUND(SUM(oi.SALES), 2)         AS REVENUE,
        COUNT(DISTINCT o.ORDER_ID)      AS ORDER_COUNT
    FROM ORDER_ITEMS oi
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
    GROUP BY TRUNC(o.ORDER_DATE, 'MM'), p.CATEGORY_NAME
)
SELECT
    ORDER_MONTH,
    CATEGORY_NAME,
    ITEM_COUNT,
    TOTAL_UNITS,
    REVENUE,
    ORDER_COUNT,
    ROUND(AVG(TOTAL_UNITS) OVER (
        PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS ROLLING_3M_AVG_UNITS,
    ROUND(AVG(TOTAL_UNITS) OVER (
        PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
        ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
    ), 2) AS ROLLING_6M_AVG_UNITS,
    ROUND(AVG(REVENUE) OVER (
        PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS ROLLING_3M_AVG_REVENUE,
    LAG(TOTAL_UNITS, 12) OVER (
        PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
    ) AS UNITS_PRIOR_YEAR,
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
    END AS YOY_CHANGE_PCT
FROM monthly_raw;


-- ============================================================================
-- VIEW 2: VW_FULFILLMENT_KPI
-- Monthly delivery performance with on-time rates and lead time stats
-- Feeds: Page 1 (Executive KPI), Page 4 (Fulfillment & Logistics)
-- ============================================================================
CREATE OR REPLACE VIEW VW_FULFILLMENT_KPI AS
SELECT
    TRUNC(o.ORDER_DATE, 'MM') AS ORDER_MONTH,
    p.CATEGORY_NAME,
    s.SHIPPING_MODE,
    COUNT(s.SHIPMENT_ID) AS TOTAL_SHIPMENTS,
    SUM(CASE WHEN s.DELIVERY_STATUS = 'Shipping on time' THEN 1 ELSE 0 END) AS ON_TIME_COUNT,
    SUM(CASE WHEN s.DELIVERY_STATUS = 'Advance shipping' THEN 1 ELSE 0 END) AS EARLY_COUNT,
    SUM(CASE WHEN s.DELIVERY_STATUS = 'Late delivery' THEN 1 ELSE 0 END) AS LATE_COUNT,
    SUM(CASE WHEN s.DELIVERY_STATUS = 'Shipping canceled' THEN 1 ELSE 0 END) AS CANCELED_COUNT,
    ROUND(
        SUM(CASE WHEN s.DELIVERY_STATUS IN ('Shipping on time', 'Advance shipping') THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0), 2
    ) AS ON_TIME_PCT,
    ROUND(
        SUM(CASE WHEN s.DELIVERY_STATUS = 'Late delivery' THEN 1 ELSE 0 END)
        * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0), 2
    ) AS LATE_PCT,
    ROUND(AVG(s.DAYS_SHIPPING_REAL), 2) AS AVG_ACTUAL_DAYS,
    ROUND(AVG(s.DAYS_SHIPPING_SCHED), 2) AS AVG_PLANNED_DAYS,
    ROUND(AVG(s.DAYS_SHIPPING_REAL - s.DAYS_SHIPPING_SCHED), 2) AS AVG_LEAD_TIME_VARIANCE
FROM SHIPMENTS s
JOIN ORDER_ITEMS oi ON s.ORDER_ITEM_ID = oi.ORDER_ITEM_ID
JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
GROUP BY TRUNC(o.ORDER_DATE, 'MM'), p.CATEGORY_NAME, s.SHIPPING_MODE;


-- ============================================================================
-- VIEW 3: VW_PRODUCT_MASTER
-- Category-level summary with ABC/XYZ classification and planning parameters
-- Feeds: Page 3 (Inventory Optimization), MRP parameter reference
-- ============================================================================
CREATE OR REPLACE VIEW VW_PRODUCT_MASTER AS
WITH category_revenue AS (
    SELECT
        p.CATEGORY_NAME,
        ROUND(SUM(oi.SALES), 2) AS TOTAL_REVENUE,
        SUM(oi.QUANTITY) AS TOTAL_UNITS,
        COUNT(oi.ORDER_ITEM_ID) AS TOTAL_ITEMS,
        ROUND(AVG(oi.SALES), 2) AS AVG_ITEM_VALUE,
        COUNT(DISTINCT o.ORDER_ID) AS TOTAL_ORDERS
    FROM ORDER_ITEMS oi
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
    GROUP BY p.CATEGORY_NAME
),
abc AS (
    SELECT
        CATEGORY_NAME, TOTAL_REVENUE, TOTAL_UNITS, TOTAL_ITEMS,
        AVG_ITEM_VALUE, TOTAL_ORDERS,
        ROUND(
            SUM(TOTAL_REVENUE) OVER (ORDER BY TOTAL_REVENUE DESC
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) * 100.0 / SUM(TOTAL_REVENUE) OVER (), 2
        ) AS CUMULATIVE_PCT,
        CASE
            WHEN SUM(TOTAL_REVENUE) OVER (ORDER BY TOTAL_REVENUE DESC
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) * 100.0 / SUM(TOTAL_REVENUE) OVER () <= 80 THEN 'A'
            WHEN SUM(TOTAL_REVENUE) OVER (ORDER BY TOTAL_REVENUE DESC
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
        ROUND(AVG(MONTHLY_UNITS), 2) AS AVG_MONTHLY_DEMAND,
        ROUND(STDDEV(MONTHLY_UNITS), 2) AS STDDEV_DEMAND,
        ROUND(STDDEV(MONTHLY_UNITS) / NULLIF(AVG(MONTHLY_UNITS), 0), 4) AS CV,
        CASE
            WHEN STDDEV(MONTHLY_UNITS) / NULLIF(AVG(MONTHLY_UNITS), 0) <= 0.5 THEN 'X'
            WHEN STDDEV(MONTHLY_UNITS) / NULLIF(AVG(MONTHLY_UNITS), 0) <= 1.0 THEN 'Y'
            ELSE 'Z'
        END AS XYZ_CLASS
    FROM monthly_demand
    GROUP BY CATEGORY_NAME
),
ship_stats AS (
    SELECT
        p.CATEGORY_NAME,
        ROUND(AVG(s.DAYS_SHIPPING_REAL), 2) AS AVG_LEAD_TIME,
        ROUND(AVG(s.DAYS_SHIPPING_REAL - s.DAYS_SHIPPING_SCHED), 2) AS AVG_LT_VARIANCE
    FROM SHIPMENTS s
    JOIN ORDER_ITEMS oi ON s.ORDER_ITEM_ID = oi.ORDER_ITEM_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    GROUP BY p.CATEGORY_NAME
),
inv AS (
    SELECT CATEGORY_NAME, ON_HAND_QTY, IN_TRANSIT_QTY, ALLOCATED_QTY, AVAILABLE_QTY
    FROM INVENTORY_SNAPSHOT
)
SELECT
    a.CATEGORY_NAME,
    a.TOTAL_REVENUE,
    a.TOTAL_UNITS,
    a.TOTAL_ITEMS,
    a.AVG_ITEM_VALUE,
    a.TOTAL_ORDERS,
    a.CUMULATIVE_PCT,
    a.ABC_CLASS,
    x.XYZ_CLASS,
    a.ABC_CLASS || '-' || x.XYZ_CLASS AS MATRIX_CELL,
    x.AVG_MONTHLY_DEMAND,
    x.STDDEV_DEMAND,
    x.CV AS COEFF_OF_VARIATION,
    ss.AVG_LEAD_TIME,
    ss.AVG_LT_VARIANCE,
    i.ON_HAND_QTY,
    i.IN_TRANSIT_QTY,
    i.AVAILABLE_QTY,
    CASE
        WHEN x.AVG_MONTHLY_DEMAND > 0 THEN
            ROUND(i.AVAILABLE_QTY / (x.AVG_MONTHLY_DEMAND / 30), 1)
        ELSE NULL
    END AS DAYS_OF_SUPPLY,
    CASE
        WHEN a.ABC_CLASS = 'A' AND x.XYZ_CLASS = 'X' THEN 'JIT/Kanban — low safety stock, frequent small orders'
        WHEN a.ABC_CLASS = 'A' AND x.XYZ_CLASS = 'Y' THEN 'Moderate safety stock — demand-driven replenishment'
        WHEN a.ABC_CLASS = 'A' AND x.XYZ_CLASS = 'Z' THEN 'High safety stock — buffer against volatility'
        WHEN a.ABC_CLASS = 'B' AND x.XYZ_CLASS = 'X' THEN 'Standard replenishment — EOQ with periodic review'
        WHEN a.ABC_CLASS = 'B' AND x.XYZ_CLASS = 'Y' THEN 'Moderate safety stock — balanced ordering frequency'
        WHEN a.ABC_CLASS = 'B' AND x.XYZ_CLASS = 'Z' THEN 'Higher safety stock — consider make-to-order'
        WHEN a.ABC_CLASS = 'C' AND x.XYZ_CLASS = 'X' THEN 'Low priority — large infrequent orders'
        WHEN a.ABC_CLASS = 'C' AND x.XYZ_CLASS = 'Y' THEN 'Minimal stock — order on demand where possible'
        WHEN a.ABC_CLASS = 'C' AND x.XYZ_CLASS = 'Z' THEN 'Evaluate for discontinuation — high risk, low reward'
    END AS INVENTORY_POLICY
FROM abc a
JOIN xyz x ON a.CATEGORY_NAME = x.CATEGORY_NAME
LEFT JOIN ship_stats ss ON a.CATEGORY_NAME = ss.CATEGORY_NAME
LEFT JOIN inv i ON a.CATEGORY_NAME = i.CATEGORY_NAME;


-- ============================================================================
-- VIEW 4: VW_PLANNED_VS_ACTUAL
-- Lead time variance analysis for planned vs actual reporting
-- Feeds: Page 1 (KPIs), Page 4 (Fulfillment — planned vs actual charts)
-- ============================================================================
CREATE OR REPLACE VIEW VW_PLANNED_VS_ACTUAL AS
SELECT
    TRUNC(o.ORDER_DATE, 'MM') AS ORDER_MONTH,
    p.CATEGORY_NAME,
    s.SHIPPING_MODE,
    o.ORDER_REGION,
    COUNT(s.SHIPMENT_ID) AS SHIPMENT_COUNT,
    ROUND(AVG(s.DAYS_SHIPPING_SCHED), 2) AS AVG_PLANNED_DAYS,
    ROUND(AVG(s.DAYS_SHIPPING_REAL), 2) AS AVG_ACTUAL_DAYS,
    ROUND(AVG(s.DAYS_SHIPPING_REAL - s.DAYS_SHIPPING_SCHED), 2) AS AVG_VARIANCE,
    SUM(CASE WHEN s.DAYS_SHIPPING_REAL > s.DAYS_SHIPPING_SCHED THEN 1 ELSE 0 END) AS OVER_PLANNED_COUNT,
    SUM(CASE WHEN s.DAYS_SHIPPING_REAL <= s.DAYS_SHIPPING_SCHED THEN 1 ELSE 0 END) AS ON_OR_UNDER_COUNT,
    SUM(CASE WHEN s.LATE_DELIVERY_RISK = 1 THEN 1 ELSE 0 END) AS LATE_RISK_COUNT,
    ROUND(SUM(oi.SALES), 2) AS REVENUE_AT_RISK
FROM SHIPMENTS s
JOIN ORDER_ITEMS oi ON s.ORDER_ITEM_ID = oi.ORDER_ITEM_ID
JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
GROUP BY TRUNC(o.ORDER_DATE, 'MM'), p.CATEGORY_NAME, s.SHIPPING_MODE, o.ORDER_REGION;


-- ============================================================================
-- VIEW 5: VW_MRP_PLAN
-- MRP output — exposes planned orders, projected on-hand, and exceptions
-- Feeds: Page 5 (Supply Plan & MRP Analysis)
-- Note: Returns data once MRP_REQUIREMENTS is populated by stored procedure
-- ============================================================================
CREATE OR REPLACE VIEW VW_MRP_PLAN AS
SELECT
    m.MRP_ID,
    m.CATEGORY_NAME,
    m.PLANNING_PERIOD,
    m.GROSS_REQUIREMENTS,
    m.SCHEDULED_RECEIPTS,
    m.PROJECTED_ON_HAND,
    m.NET_REQUIREMENTS,
    m.PLANNED_ORDER_QTY,
    m.PLANNED_RELEASE_DATE,
    m.LOT_SIZING_METHOD,
    m.EXCEPTION_FLAG,
    m.EXCEPTION_MESSAGE,
    m.CREATED_DATE,
    i.ON_HAND_QTY AS CURRENT_ON_HAND,
    i.AVAILABLE_QTY AS CURRENT_AVAILABLE
FROM MRP_REQUIREMENTS m
LEFT JOIN INVENTORY_SNAPSHOT i ON m.CATEGORY_NAME = i.CATEGORY_NAME;


-- ============================================================================
-- VIEW 6: VW_FORECAST_VS_ACTUAL
-- Forecast accuracy — compares planned demand to actual with error metrics
-- Feeds: Page 2 (Demand Forecasting accuracy), Page 5 (forecast input to MRP)
-- Note: Returns data once FORECAST_PLAN is populated from Excel write-back
-- ============================================================================
CREATE OR REPLACE VIEW VW_FORECAST_VS_ACTUAL AS
SELECT
    f.FORECAST_ID,
    f.CATEGORY_NAME,
    f.FORECAST_PERIOD,
    f.FORECASTED_QTY,
    f.FORECAST_METHOD,
    f.CONFIDENCE_LOWER,
    f.CONFIDENCE_UPPER,
    d.ACTUAL_UNITS,
    d.ACTUAL_REVENUE,
    ROUND(f.FORECASTED_QTY - d.ACTUAL_UNITS, 2) AS FORECAST_ERROR,
    ROUND(ABS(f.FORECASTED_QTY - d.ACTUAL_UNITS), 2) AS ABS_ERROR,
    CASE
        WHEN d.ACTUAL_UNITS > 0 THEN
            ROUND(ABS(f.FORECASTED_QTY - d.ACTUAL_UNITS) * 100.0 / d.ACTUAL_UNITS, 2)
        ELSE NULL
    END AS APE,
    CASE
        WHEN f.FORECASTED_QTY > d.ACTUAL_UNITS THEN 'OVER'
        WHEN f.FORECASTED_QTY < d.ACTUAL_UNITS THEN 'UNDER'
        ELSE 'EXACT'
    END AS BIAS_DIRECTION,
    f.CREATED_DATE AS FORECAST_DATE
FROM FORECAST_PLAN f
LEFT JOIN (
    SELECT
        p.CATEGORY_NAME,
        TRUNC(o.ORDER_DATE, 'MM') AS ORDER_MONTH,
        SUM(oi.QUANTITY) AS ACTUAL_UNITS,
        ROUND(SUM(oi.SALES), 2) AS ACTUAL_REVENUE
    FROM ORDER_ITEMS oi
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
    GROUP BY p.CATEGORY_NAME, TRUNC(o.ORDER_DATE, 'MM')
) d ON f.CATEGORY_NAME = d.CATEGORY_NAME
    AND f.FORECAST_PERIOD = d.ORDER_MONTH;


-- ============================================================================
-- VERIFICATION: Confirm all views exist and are queryable
-- ============================================================================
SELECT 'VW_DEMAND_TIMESERIES' AS VIEW_NAME, COUNT(*) AS ROW_COUNT FROM VW_DEMAND_TIMESERIES
UNION ALL SELECT 'VW_FULFILLMENT_KPI', COUNT(*) FROM VW_FULFILLMENT_KPI
UNION ALL SELECT 'VW_PRODUCT_MASTER', COUNT(*) FROM VW_PRODUCT_MASTER
UNION ALL SELECT 'VW_PLANNED_VS_ACTUAL', COUNT(*) FROM VW_PLANNED_VS_ACTUAL
UNION ALL SELECT 'VW_MRP_PLAN', COUNT(*) FROM VW_MRP_PLAN
UNION ALL SELECT 'VW_FORECAST_VS_ACTUAL', COUNT(*) FROM VW_FORECAST_VS_ACTUAL;