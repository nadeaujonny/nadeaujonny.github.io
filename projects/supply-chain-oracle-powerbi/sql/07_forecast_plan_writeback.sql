/*
================================================================================
  SUPPLY CHAIN ANALYTICS — FORECAST PLAN WRITE-BACK
  07_forecast_plan_writeback.sql
  
  Oracle Autonomous Database (19c)
  Author: Jonathan Nadeau
  
  Purpose: Loads demand forecast data from the Excel Forecast_Export sheet
  into the FORECAST_PLAN table, completing the demand planning round-trip:
  
    Excel ETS Forecast → Forecast_Export sheet → CSV/ODBC → FORECAST_PLAN
    → REFRESH_SUPPLY_CHAIN_DATA stored procedure → MRP recalculates
    → MRP_REQUIREMENTS updated with new planned orders
  
  This script:
    1. Drops and recreates FORECAST_PLAN with two additional columns
       (MAPE_PCT, NOTES) beyond the original 01_schema_ddl.sql definition
    2. Recreates the category/period index
    3. Inserts 42 forecast rows (7 A-class categories x 6 months)
    4. Provides validation queries and stored procedure execution
  
  Notes:
    - Uses individual INSERT statements (not INSERT ALL) because Oracle's
      INSERT ALL does not correctly generate unique IDENTITY values per row
    - Uses SET DEFINE OFF to prevent Oracle from interpreting '&' in
      'Camping & Hiking' as a substitution variable
    - Uses string concatenation ('Camping ' || '& Hiking') as additional
      protection against substitution variable parsing
    - Forecast method is ETS (Exponential Triple Smoothing) for all
      categories, selected by Excel Forecast Sheet with auto-seasonality
    - MAPE calculated on holdout validation periods (Jan-Sep 2017)
    - Planning horizon: Oct 2017 - Mar 2018 (6 months)
    - Qty values rounded to whole units from Excel ETS output
  
  Prerequisites:
    - All tables from 01_schema_ddl.sql exist
    - Data loaded via 02_data_normalization.sql
    - Views from 05_reporting_views.sql exist
    - Stored procedure from 06_stored_procedure_mrp.sql compiled
  
  Run: Paste entire script into a NEW clean worksheet, then Run Script (F5).
  
  After running:
    1. Verify 42 rows with validation query (Section 5)
    2. Run stored procedure (Section 6) to trigger MRP recalculation
    3. Run cross-check query (Section 7) to confirm variance = 0
================================================================================
*/


-- ============================================================================
-- 1. DISABLE SUBSTITUTION VARIABLES
-- ============================================================================
-- Prevents Oracle from treating '&' as a bind variable prompt
-- (required for 'Camping & Hiking' category name)

SET DEFINE OFF;


-- ============================================================================
-- 2. DROP AND RECREATE FORECAST_PLAN TABLE
-- ============================================================================
-- Recreates with two additional columns beyond 01_schema_ddl.sql:
--   MAPE_PCT  — forecast accuracy metric for the selected method
--   NOTES     — forecast generation metadata
--
-- Original columns preserved: FORECAST_ID, CATEGORY_NAME, FORECAST_PERIOD,
-- FORECASTED_QTY, FORECAST_METHOD, CONFIDENCE_LOWER, CONFIDENCE_UPPER,
-- CREATED_DATE

DROP TABLE FORECAST_PLAN CASCADE CONSTRAINTS;

CREATE TABLE FORECAST_PLAN (
    FORECAST_ID         NUMBER(10)      GENERATED ALWAYS AS IDENTITY NOT NULL,
    CATEGORY_NAME       VARCHAR2(150)   NOT NULL,
    FORECAST_PERIOD     DATE            NOT NULL,
    FORECASTED_QTY      NUMBER(12,2)    NOT NULL,
    FORECAST_METHOD     VARCHAR2(50),
    CONFIDENCE_LOWER    NUMBER(12,2),
    CONFIDENCE_UPPER    NUMBER(12,2),
    MAPE_PCT            NUMBER(6,2),
    NOTES               VARCHAR2(200),
    CREATED_DATE        TIMESTAMP       DEFAULT SYSTIMESTAMP,
    CONSTRAINT PK_FORECAST_PLAN PRIMARY KEY (FORECAST_ID)
);

COMMENT ON TABLE FORECAST_PLAN IS 'Demand forecast data — populated from Excel ETS model, consumed by REFRESH_SUPPLY_CHAIN_DATA stored procedure for MRP gross requirements';
COMMENT ON COLUMN FORECAST_PLAN.FORECAST_METHOD IS 'Algorithm used: ETS (Exponential Triple Smoothing), MOVING_AVG, or WEIGHTED_MA. Best method selected per category by lowest MAPE on holdout periods.';
COMMENT ON COLUMN FORECAST_PLAN.FORECAST_PERIOD IS 'First day of the forecast month';
COMMENT ON COLUMN FORECAST_PLAN.MAPE_PCT IS 'Mean Absolute Percentage Error of the selected forecast method on holdout validation periods (Jan-Sep 2017)';
COMMENT ON COLUMN FORECAST_PLAN.NOTES IS 'Forecast generation notes — method details, horizon, seasonality settings';


-- ============================================================================
-- 3. RECREATE INDEX
-- ============================================================================

CREATE INDEX IDX_FORECAST_CAT_PERIOD ON FORECAST_PLAN(CATEGORY_NAME, FORECAST_PERIOD);


-- ============================================================================
-- 4. INSERT FORECAST DATA
-- ============================================================================
-- Source: Forecast_Export sheet in SupplyChain_Analysis workbook
-- Method: ETS (Exponential Triple Smoothing) with auto-seasonality detection
-- Planning Horizon: Oct 2017 - Mar 2018 (6 months)
-- Categories: 7 A-class categories from ABC/XYZ classification
-- Qty values: Rounded to whole units from Excel ETS output
-- Confidence bounds: 95% prediction interval from ETS model
-- ============================================================================

-- Fishing (ETS MAPE: 5.78%)
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Fishing', DATE '2017-10-01', 505, 471.25, 537.65, 'ETS', 5.78, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Fishing', DATE '2017-11-01', 532, 497.94, 565.28, 'ETS', 5.78, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Fishing', DATE '2017-12-01', 536, 502.11, 569.52, 'ETS', 5.78, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Fishing', DATE '2018-01-01', 522, 490.77, 557.63, 'ETS', 5.78, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Fishing', DATE '2018-02-01', 469, 433.59, 501.82, 'ETS', 5.78, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Fishing', DATE '2018-03-01', 514, 481.97, 551.23, 'ETS', 5.78, 'Auto-seasonality; 6-month horizon');

-- Cleats (ETS MAPE: 5.70%)
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Cleats', DATE '2017-10-01', 2011, 1879.29, 2140.43, 'ETS', 5.70, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Cleats', DATE '2017-11-01', 2060, 1924.09, 2188.23, 'ETS', 5.70, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Cleats', DATE '2017-12-01', 2051, 1915.69, 2185.83, 'ETS', 5.70, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Cleats', DATE '2018-01-01', 2048, 1913.17, 2199.51, 'ETS', 5.70, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Cleats', DATE '2018-02-01', 1879, 1738.03, 2016.10, 'ETS', 5.70, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Cleats', DATE '2018-03-01', 2266, 2123.72, 2413.27, 'ETS', 5.70, 'Auto-seasonality; 6-month horizon');

-- Camping & Hiking (ETS MAPE: 6.28%)
-- Note: Uses string concatenation to avoid substitution variable parsing on '&'
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Camping ' || '& Hiking', DATE '2017-10-01', 420, 390.10, 449.28, 'ETS', 6.28, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Camping ' || '& Hiking', DATE '2017-11-01', 416, 387.16, 444.60, 'ETS', 6.28, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Camping ' || '& Hiking', DATE '2017-12-01', 385, 358.14, 411.22, 'ETS', 6.28, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Camping ' || '& Hiking', DATE '2018-01-01', 414, 385.00, 441.55, 'ETS', 6.28, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Camping ' || '& Hiking', DATE '2018-02-01', 394, 366.33, 421.28, 'ETS', 6.28, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Camping ' || '& Hiking', DATE '2018-03-01', 426, 396.28, 457.26, 'ETS', 6.28, 'Auto-seasonality; 6-month horizon');

-- Cardio Equipment (ETS MAPE: 10.01%)
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Cardio Equipment', DATE '2017-10-01', 1029, 869.99, 1180.28, 'ETS', 10.01, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Cardio Equipment', DATE '2017-11-01', 1127, 970.87, 1267.89, 'ETS', 10.01, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Cardio Equipment', DATE '2017-12-01', 1125, 955.18, 1280.91, 'ETS', 10.01, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Cardio Equipment', DATE '2018-01-01', 1181, 1017.61, 1337.88, 'ETS', 10.01, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Cardio Equipment', DATE '2018-02-01', 1155, 997.60, 1315.38, 'ETS', 10.01, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Cardio Equipment', DATE '2018-03-01', 1013, 853.92, 1179.89, 'ETS', 10.01, 'Auto-seasonality; 6-month horizon');

-- Women's Apparel (ETS MAPE: 6.66%)
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Women''s Apparel', DATE '2017-10-01', 1952, 1804.80, 2107.04, 'ETS', 6.66, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Women''s Apparel', DATE '2017-11-01', 1762, 1621.19, 1915.66, 'ETS', 6.66, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Women''s Apparel', DATE '2017-12-01', 1780, 1633.52, 1930.10, 'ETS', 6.66, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Women''s Apparel', DATE '2018-01-01', 1938, 1793.71, 2087.14, 'ETS', 6.66, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Women''s Apparel', DATE '2018-02-01', 1821, 1676.90, 1955.25, 'ETS', 6.66, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Women''s Apparel', DATE '2018-03-01', 1939, 1796.60, 2082.30, 'ETS', 6.66, 'Auto-seasonality; 6-month horizon');

-- Water Sports (ETS MAPE: 5.41%)
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Water Sports', DATE '2017-10-01', 487, 446.66, 526.75, 'ETS', 5.41, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Water Sports', DATE '2017-11-01', 468, 426.79, 509.68, 'ETS', 5.41, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Water Sports', DATE '2017-12-01', 482, 441.82, 520.43, 'ETS', 5.41, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Water Sports', DATE '2018-01-01', 459, 414.83, 498.18, 'ETS', 5.41, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Water Sports', DATE '2018-02-01', 444, 404.17, 484.97, 'ETS', 5.41, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Water Sports', DATE '2018-03-01', 487, 444.60, 529.45, 'ETS', 5.41, 'Auto-seasonality; 6-month horizon');

-- Indoor/Outdoor Games (ETS MAPE: 5.92%)
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Indoor/Outdoor Games', DATE '2017-10-01', 1889, 1745.76, 2034.07, 'ETS', 5.92, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Indoor/Outdoor Games', DATE '2017-11-01', 1697, 1553.76, 1835.73, 'ETS', 5.92, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Indoor/Outdoor Games', DATE '2017-12-01', 1812, 1683.60, 1959.18, 'ETS', 5.92, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Indoor/Outdoor Games', DATE '2018-01-01', 1697, 1552.68, 1839.22, 'ETS', 5.92, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Indoor/Outdoor Games', DATE '2018-02-01', 1690, 1551.22, 1816.51, 'ETS', 5.92, 'Auto-seasonality; 6-month horizon');
INSERT INTO FORECAST_PLAN (CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY, CONFIDENCE_LOWER, CONFIDENCE_UPPER, FORECAST_METHOD, MAPE_PCT, NOTES) VALUES ('Indoor/Outdoor Games', DATE '2018-03-01', 1642, 1513.55, 1778.79, 'ETS', 5.92, 'Auto-seasonality; 6-month horizon');

COMMIT;


-- ============================================================================
-- 5. VALIDATION: Verify 42 rows loaded correctly
-- ============================================================================

SELECT
    CATEGORY_NAME,
    FORECAST_PERIOD,
    FORECASTED_QTY,
    CONFIDENCE_LOWER,
    CONFIDENCE_UPPER,
    FORECAST_METHOD,
    MAPE_PCT,
    CREATED_DATE,
    NOTES
FROM FORECAST_PLAN
ORDER BY CATEGORY_NAME, FORECAST_PERIOD;

-- Row count check
SELECT COUNT(*) AS TOTAL_FORECAST_ROWS FROM FORECAST_PLAN;


-- ============================================================================
-- 6. RUN STORED PROCEDURE — triggers MRP recalculation against new forecast
-- ============================================================================
-- Uncomment and run after confirming 42 rows loaded successfully.
-- Use Run Script to see DBMS_OUTPUT messages.

-- SET SERVEROUTPUT ON;
-- BEGIN
--     REFRESH_SUPPLY_CHAIN_DATA;
-- END;
-- /


-- ============================================================================
-- 7. CROSS-CHECK: Forecast vs MRP Gross Requirements
-- ============================================================================
-- Run AFTER the stored procedure completes.
-- Verifies MRP consumed the forecast correctly.
-- Variance should be 0 for all 42 rows — proof the round-trip works.

SELECT
    fp.CATEGORY_NAME,
    fp.FORECAST_PERIOD,
    fp.FORECASTED_QTY         AS "Forecast Qty",
    mr.GROSS_REQUIREMENTS     AS "MRP Gross Req",
    fp.FORECASTED_QTY - mr.GROSS_REQUIREMENTS AS "Variance"
FROM FORECAST_PLAN fp
LEFT JOIN MRP_REQUIREMENTS mr
    ON fp.CATEGORY_NAME = mr.CATEGORY_NAME
    AND fp.FORECAST_PERIOD = mr.PLANNING_PERIOD
ORDER BY fp.CATEGORY_NAME, fp.FORECAST_PERIOD;


-- ============================================================================
-- 8. SUMMARY BY CATEGORY
-- ============================================================================
-- Quick overview of forecast load by category with accuracy metrics.

SELECT
    CATEGORY_NAME,
    COUNT(*)                        AS PERIODS,
    MIN(FORECAST_PERIOD)            AS FIRST_PERIOD,
    MAX(FORECAST_PERIOD)            AS LAST_PERIOD,
    ROUND(AVG(FORECASTED_QTY), 0)  AS AVG_FORECAST_QTY,
    ROUND(SUM(FORECASTED_QTY), 0)  AS TOTAL_FORECAST_QTY,
    MAX(MAPE_PCT)                   AS MAPE_PCT,
    MAX(FORECAST_METHOD)            AS METHOD
FROM FORECAST_PLAN
GROUP BY CATEGORY_NAME
ORDER BY TOTAL_FORECAST_QTY DESC;