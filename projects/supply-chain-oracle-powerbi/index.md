---
layout: default
title: "Supply Chain Demand Forecasting, Inventory Optimization & MRP Simulation"
description: "End-to-end automated supply chain analytics solution using Oracle SQL, Excel Power Query, and Power BI — featuring demand forecasting, ABC/XYZ classification, MRP net requirements simulation, and a six-page interactive dashboard with scheduled refresh."
---

<a href="/projects/" class="back-to-projects btn">&larr; Back to Projects</a>

# Supply Chain Demand Forecasting, Inventory Optimization &amp; MRP Simulation

> An end-to-end, automated supply chain analytics solution demonstrating demand forecasting, inventory optimization, MRP simulation, and fulfillment performance analysis &mdash; built with Oracle SQL, Excel Power Query, and Power BI using the DataCo Smart Supply Chain dataset (~180,000 orders).

**Tools:** Oracle SQL &middot; Excel (Power Query, Power Pivot, Solver) &middot; Power BI (DAX, Star Schema) &middot; Git/GitHub

---

<details class="dropdown-section">
  <summary><strong>Project Overview</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Overview</h3>
  <p>
    This project builds an end-to-end, automated supply chain analytics solution focused on demand forecasting,
    inventory optimization, MRP simulation, and fulfillment performance for a consumer goods product catalog. The
    analysis uses the DataCo Smart Supply Chain dataset (~180,000 order records) loaded into an Oracle Autonomous
    Database, processed through Excel Power Query, and visualized in a six-page Power BI dashboard.
  </p>
  <p>
    What distinguishes this project is the <strong>automation layer</strong> built into every stage: Oracle stored procedures
    automate data extraction and MRP calculation on a nightly schedule, Power Query custom functions automate
    transformation logic across hundreds of SKUs, and Power BI scheduled refresh pushes updated dashboards to
    stakeholders without manual intervention. The result is a closed-loop system where reporting findings feed back
    into master data updates and the next refresh cycle automatically reflects those changes.
  </p>

  <h3>Business Context</h3>
  <p>
    Consumer goods manufacturers managing hundreds of SKUs across multiple channels need to answer: How much of
    each product should we produce? When do we reorder? Are we delivering on time? Where are our bottlenecks?
    Are planned values tracking against actuals? This project directly models those questions using the same tools
    and workflows used in production supply chain environments &mdash; SQL against Oracle for data extraction,
    Excel for analysis and modeling, and Power BI for dashboards and reporting.
  </p>

  <h3>Technical Stack</h3>
  <ul>
    <li><strong>Database / ERP Layer:</strong> Oracle Autonomous Database (Always Free tier) &mdash; SQL for extraction, joins, aggregation, view creation; stored procedures for automated refresh and MRP calculation; DBMS_SCHEDULER for nightly execution</li>
    <li><strong>MRP / Supply Planning Simulation:</strong> Oracle SQL tables and views simulating MRP net requirements logic &mdash; gross requirements, projected on-hand, net requirements, planned order releases with lead time offsets and lot sizing rules</li>
    <li><strong>Data Processing &amp; ETL:</strong> Excel Power Query with custom M functions, parameters for dynamic switching, and query folding documentation</li>
    <li><strong>Analysis &amp; Modeling:</strong> Excel formulas, pivot tables, Power Pivot data model, Goal Seek, Solver for lot sizing optimization, What-If analysis</li>
    <li><strong>Forecasting &amp; Demand Planning:</strong> Excel Forecast Sheet (ETS algorithm), moving averages, forecast write-back to Oracle</li>
    <li><strong>Dashboards &amp; Reporting:</strong> Power BI Desktop (six-page report with DAX measures, slicers, drilldowns, data alerts, Row-Level Security)</li>
  </ul>

  <h3>Dataset</h3>
  <p>
    <strong>DataCo Smart Supply Chain Dataset (Kaggle)</strong> &mdash; ~180,000 order records with product categories,
    customer segments, order dates, shipping modes, scheduled vs. actual delivery dates, late delivery flags,
    geographic data, and financial metrics (sales, profit, discounts). Loaded into Oracle Autonomous Database
    with a normalized relational schema (ORDERS, ORDER_ITEMS, PRODUCTS, CUSTOMERS, SHIPMENTS, FORECAST_PLAN,
    MRP_REQUIREMENTS, INVENTORY_SNAPSHOT).
  </p>

</details>

<details class="dropdown-section">
  <summary><strong>Automation Architecture</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>The Full Automated Pipeline: Oracle &rarr; Power Query &rarr; Power BI</h3>
  <ol>
    <li><strong>Oracle DBMS_SCHEDULER</strong> executes the <code>REFRESH_SUPPLY_CHAIN_DATA</code> stored procedure at 2:00 AM &mdash; pulls fresh data, recalculates derived fields, reads the latest demand forecast, runs MRP net requirements calculation, writes planned orders, and updates all six reporting views.</li>
    <li><strong>Power BI Service scheduled refresh</strong> triggers at 5:00 AM &mdash; connects to Oracle views, Power Query custom functions and parameters execute automatically against updated data.</li>
    <li><strong>DAX measures</strong> recalculate all KPIs, forecasts, MRP coverage metrics, and classifications. Data alerts evaluate thresholds and send notifications if critical metrics breach targets.</li>
    <li><strong>By morning</strong>, the dashboard reflects last night's actuals, MRP recommendations are current, and supply plan alerts have been sent for any issues.</li>
  </ol>

  <h3>Oracle SQL Automation</h3>
  <ul>
    <li><strong>Reporting Views:</strong> Six pre-calculated views (VW_DEMAND_TIMESERIES, VW_FULFILLMENT_KPI, VW_PRODUCT_MASTER, VW_PLANNED_VS_ACTUAL, VW_MRP_PLAN, VW_FORECAST_VS_ACTUAL) defined once, reused on every refresh</li>
    <li><strong>Stored Procedure:</strong> <code>REFRESH_SUPPLY_CHAIN_DATA</code> wraps the full pipeline &mdash; staging table refresh, derived field calculation, MRP net requirements execution, view rebuild, and audit logging</li>
    <li><strong>Scheduled Job:</strong> DBMS_SCHEDULER runs the procedure nightly at 2:00 AM, same mechanism as production Oracle Fusion Cloud</li>
    <li><strong>CTEs &amp; Window Functions:</strong> Multi-stage calculations (cumulative revenue for ABC, rolling demand variability, MRP gross-to-net) structured as readable, modular CTEs</li>
  </ul>

  <h3>Power Query Automation</h3>
  <ul>
    <li><strong>Custom M Functions:</strong> fn_CalculateSafetyStock, fn_ClassifyABC, fn_ClassifyXYZ, fn_CalculateReorderPoint, fn_CalculateNetRequirements &mdash; write once, invoke across all categories</li>
    <li><strong>Parameters:</strong> Date (analysis window), Source (Oracle environment), Service Level (Z-score), Planning Horizon (3/6/12 months)</li>
    <li><strong>Query Folding:</strong> Documented which steps fold to Oracle vs. execute locally for performance optimization</li>
  </ul>

  <h3>Power BI Automation</h3>
  <ul>
    <li><strong>Scheduled Refresh:</strong> Aligned to Oracle job schedule via Power BI Service</li>
    <li><strong>DAX Measures:</strong> Auto-calculating KPIs &mdash; YoY growth, on-time rate, forecast accuracy (MAE, MAPE), inventory turnover, MRP coverage ratio, supply plan adherence</li>
    <li><strong>Data Alerts:</strong> Threshold notifications for in-stock rate drops, late delivery spikes, MRP stockout projections, forecast bias</li>
    <li><strong>Row-Level Security:</strong> Marketing sees sell-through data; Operations sees production, fulfillment, MRP, and inventory</li>
  </ul>

</details>

<details class="dropdown-section">
  <summary><strong>Phase 1 — Oracle SQL: Schema Design &amp; Data Loading</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Schema Design</h3>
  <p>
    The flat DataCo CSV (~180,000 rows, 53 columns) was decomposed into a normalized relational schema consisting of
    5 transactional tables and 3 supply planning tables. A staging table (<strong>STG_DATACO</strong>) mirrors the flat CSV
    structure for initial data load via Oracle Database Actions import tool, after which INSERT/SELECT statements
    normalize the data into the production tables.
  </p>
  <ul>
    <li><strong>ORDERS</strong> &mdash; Order header: order ID, order date, customer ID, status, market, region</li>
    <li><strong>ORDER_ITEMS</strong> &mdash; Line-item detail: quantity, unit price, discount, profit, sales</li>
    <li><strong>PRODUCTS</strong> &mdash; Product master: category, department, price, plus planning parameters (lead time days, lot sizing method, minimum order quantity, EOQ, safety stock, reorder point)</li>
    <li><strong>CUSTOMERS</strong> &mdash; Customer master: segment, city, state, country, zip code</li>
    <li><strong>SHIPMENTS</strong> &mdash; Fulfillment: shipping mode, shipping date, scheduled vs. actual days, delivery status, late delivery risk flag</li>
    <li><strong>FORECAST_PLAN</strong> &mdash; Demand forecast output: category, forecast period, forecasted quantity, method, confidence bounds</li>
    <li><strong>MRP_REQUIREMENTS</strong> &mdash; MRP output: gross requirements, scheduled receipts, projected on-hand, net requirements, planned order quantity/release date, lot sizing method, exception flags</li>
    <li><strong>INVENTORY_SNAPSHOT</strong> &mdash; Simulated current inventory positions derived from order/shipment data</li>
  </ul>
  <p>
    Primary keys, foreign keys, and indexes were defined across all tables. Planning parameter columns were added to
    PRODUCTS to enable MRP simulation directly within the Oracle layer.
  </p>

  <h4>PRODUCTS Table with Planning Parameters</h4>
  <pre><code class="language-sql">CREATE TABLE PRODUCTS (
    PRODUCT_CARD_ID     NUMBER(10)      NOT NULL,
    PRODUCT_NAME        VARCHAR2(300)   NOT NULL,
    CATEGORY_ID         NUMBER(10)      NOT NULL,
    CATEGORY_NAME       VARCHAR2(150)   NOT NULL,
    DEPARTMENT_ID       NUMBER(10)      NOT NULL,
    DEPARTMENT_NAME     VARCHAR2(100)   NOT NULL,
    PRODUCT_PRICE       NUMBER(12,2)    NOT NULL,
    PRODUCT_STATUS      NUMBER(1)       DEFAULT 0,
    -- Planning parameters (populated during inventory optimization phase)
    LEAD_TIME_DAYS      NUMBER(5)       DEFAULT 7,
    LOT_SIZING_METHOD   VARCHAR2(20)    DEFAULT 'EOQ',
    MIN_ORDER_QTY       NUMBER(10)      DEFAULT 1,
    EOQ                 NUMBER(12,2),
    SAFETY_STOCK        NUMBER(12,2),
    REORDER_POINT       NUMBER(12,2),
    CONSTRAINT PK_PRODUCTS PRIMARY KEY (PRODUCT_CARD_ID)
);</code></pre>

  <h4>MRP Requirements Table</h4>
  <pre><code class="language-sql">CREATE TABLE MRP_REQUIREMENTS (
    MRP_ID              NUMBER(10)      GENERATED ALWAYS AS IDENTITY NOT NULL,
    CATEGORY_NAME       VARCHAR2(150)   NOT NULL,
    PLANNING_PERIOD     DATE            NOT NULL,
    GROSS_REQUIREMENTS  NUMBER(12,2)    DEFAULT 0,
    SCHEDULED_RECEIPTS  NUMBER(12,2)    DEFAULT 0,
    PROJECTED_ON_HAND   NUMBER(12,2)    DEFAULT 0,
    NET_REQUIREMENTS    NUMBER(12,2)    DEFAULT 0,
    PLANNED_ORDER_QTY   NUMBER(12,2)    DEFAULT 0,
    PLANNED_RELEASE_DATE DATE,
    LOT_SIZING_METHOD   VARCHAR2(20),
    EXCEPTION_FLAG      VARCHAR2(50),
    EXCEPTION_MESSAGE   VARCHAR2(500),
    CONSTRAINT PK_MRP_REQUIREMENTS PRIMARY KEY (MRP_ID)
);</code></pre>

  <h4>Data Normalization &mdash; ROW_NUMBER Deduplication</h4>
  <pre><code class="language-sql">-- Deduplicate customers from staging (one row per order item → one row per customer)
INSERT INTO CUSTOMERS (
    CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL, SEGMENT,
    CITY, STATE, COUNTRY, STREET, ZIPCODE, LATITUDE, LONGITUDE
)
SELECT
    CUSTOMER_ID, NVL(CUSTOMER_FNAME, 'Unknown'), NVL(CUSTOMER_LNAME, 'Unknown'),
    CUSTOMER_EMAIL, NVL(CUSTOMER_SEGMENT, 'Unknown'),
    CUSTOMER_CITY, CUSTOMER_STATE, CUSTOMER_COUNTRY,
    CUSTOMER_STREET, CUSTOMER_ZIPCODE, LATITUDE, LONGITUDE
FROM (
    SELECT s.*,
        ROW_NUMBER() OVER (PARTITION BY s.CUSTOMER_ID ORDER BY s.ORDER_DATE DESC) AS rn
    FROM STG_DATACO s
)
WHERE rn = 1;</code></pre>

  <p>
    <strong>SQL Scripts:</strong>
    <a href="sql/01_schema_ddl.sql">01_schema_ddl.sql</a> &mdash; Schema DDL (8 normalized tables + staging table) |
    <a href="sql/02_data_normalization.sql">02_data_normalization.sql</a> &mdash; INSERT/SELECT normalization from staging to production tables
  </p>

</details>

<details class="dropdown-section">
  <summary><strong>Phase 2 — Oracle SQL: Queries, Views &amp; Stored Procedures</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>SQL Query Categories</h3>

  <p>
    Five query groups extract, transform, and classify supply chain data across ~180K order items and 50 product categories.
    SQL techniques include CTEs, window functions (AVG OVER, SUM OVER, LAG, RANK, DENSE_RANK), date arithmetic, and cumulative calculations.
  </p>
  <ul>
    <li><strong>Demand &amp; Sales Extraction</strong> (<a href="sql/03_demand_queries.sql">03_demand_queries.sql</a>) &mdash; Monthly/weekly order volume by category, rolling 3- and 6-month averages, MoM growth via LAG, cumulative revenue for Pareto analysis, and coefficient of variation for XYZ classification</li>
    <li><strong>Inventory &amp; Fulfillment Analytics</strong> (<a href="sql/04_inventory_fulfillment_queries.sql">04_inventory_fulfillment_queries.sql</a>) &mdash; ABC classification via cumulative revenue percentage, ABC-XYZ policy matrix, product master with planning parameters, on-time delivery rates, lead time variance, and late delivery root cause ranking</li>
    <li><strong>Planned vs. Actual Analysis</strong> &mdash; Lead time variance, on-time delivery rate, late delivery root cause ranking</li>
    <li><strong>MRP &amp; Supply Planning</strong> &mdash; Gross requirements, projected on-hand, net requirements, planned order releases, exception flagging</li>
    <li><strong>Forecast Accuracy</strong> &mdash; Forecast vs. actual comparison, MAE, MAPE, bias detection</li>
  </ul>

  <h4>Rolling Averages &amp; Demand Variability (XYZ Classification)</h4>
  <pre><code class="language-sql">-- Rolling 3-month and 6-month demand averages using window functions
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
    ORDER_MONTH, CATEGORY_NAME, TOTAL_UNITS, REVENUE,
    ROUND(AVG(TOTAL_UNITS) OVER (
        PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS ROLLING_3M_AVG_UNITS,
    ROUND(AVG(TOTAL_UNITS) OVER (
        PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
        ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
    ), 2) AS ROLLING_6M_AVG_UNITS
FROM monthly_demand
ORDER BY CATEGORY_NAME, ORDER_MONTH;</code></pre>

  <pre><code class="language-sql">-- Demand variability for XYZ classification (coefficient of variation)
WITH monthly_demand AS ( ... ),
variability AS (
    SELECT
        CATEGORY_NAME,
        ROUND(AVG(MONTHLY_UNITS), 2)    AS AVG_MONTHLY_DEMAND,
        ROUND(STDDEV(MONTHLY_UNITS), 2) AS STDDEV_DEMAND,
        ROUND(STDDEV(MONTHLY_UNITS) / NULLIF(AVG(MONTHLY_UNITS), 0), 4)
                                         AS COEFF_OF_VARIATION
    FROM monthly_demand
    GROUP BY CATEGORY_NAME
)
SELECT CATEGORY_NAME, AVG_MONTHLY_DEMAND, COEFF_OF_VARIATION,
    CASE
        WHEN COEFF_OF_VARIATION &lt;= 0.5 THEN 'X'   -- Stable demand
        WHEN COEFF_OF_VARIATION &lt;= 1.0 THEN 'Y'   -- Moderate variability
        ELSE                                 'Z'    -- Highly volatile
    END AS XYZ_CLASS
FROM variability
ORDER BY COEFF_OF_VARIATION;</code></pre>

  <h4>ABC Classification (Pareto Analysis) &amp; ABC-XYZ Policy Matrix</h4>
  <pre><code class="language-sql">-- ABC Classification by cumulative revenue percentage
WITH category_revenue AS (
    SELECT p.CATEGORY_NAME, ROUND(SUM(oi.SALES), 2) AS TOTAL_REVENUE,
           SUM(oi.QUANTITY) AS TOTAL_UNITS
    FROM ORDER_ITEMS oi
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
    GROUP BY p.CATEGORY_NAME
),
ranked AS (
    SELECT CATEGORY_NAME, TOTAL_REVENUE, TOTAL_UNITS,
        ROUND(SUM(TOTAL_REVENUE) OVER (
            ORDER BY TOTAL_REVENUE DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) * 100.0 / SUM(TOTAL_REVENUE) OVER (), 2) AS CUMULATIVE_PCT
    FROM category_revenue
)
SELECT CATEGORY_NAME, TOTAL_REVENUE, CUMULATIVE_PCT,
    CASE
        WHEN CUMULATIVE_PCT &lt;= 80 THEN 'A'
        WHEN CUMULATIVE_PCT &lt;= 95 THEN 'B'
        ELSE 'C'
    END AS ABC_CLASS
FROM ranked
ORDER BY TOTAL_REVENUE DESC;</code></pre>

  <pre><code class="language-sql">-- ABC-XYZ matrix with automated inventory policy recommendations
SELECT a.CATEGORY_NAME, a.ABC_CLASS, x.XYZ_CLASS,
    a.ABC_CLASS || '-' || x.XYZ_CLASS AS MATRIX_CELL,
    CASE
        WHEN a.ABC_CLASS = 'A' AND x.XYZ_CLASS = 'X'
            THEN 'JIT/Kanban — low safety stock, frequent small orders'
        WHEN a.ABC_CLASS = 'A' AND x.XYZ_CLASS = 'Y'
            THEN 'Moderate safety stock — demand-driven replenishment'
        WHEN a.ABC_CLASS = 'B' AND x.XYZ_CLASS = 'X'
            THEN 'Standard replenishment — EOQ with periodic review'
        WHEN a.ABC_CLASS = 'C' AND x.XYZ_CLASS = 'Z'
            THEN 'Evaluate for discontinuation — high risk, low reward'
        ...
    END AS INVENTORY_POLICY
FROM abc a
JOIN xyz x ON a.CATEGORY_NAME = x.CATEGORY_NAME
ORDER BY a.ABC_CLASS, x.XYZ_CLASS;</code></pre>

  <h4>On-Time Delivery Rate &amp; Late Delivery Root Cause Ranking</h4>
  <pre><code class="language-sql">-- Monthly on-time delivery rate
SELECT
    TRUNC(o.ORDER_DATE, 'MM') AS ORDER_MONTH,
    COUNT(s.SHIPMENT_ID) AS TOTAL_SHIPMENTS,
    ROUND(
        SUM(CASE WHEN s.DELIVERY_STATUS IN ('Shipping on time', 'Advance shipping')
            THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0), 2
    ) AS ON_TIME_PCT,
    ROUND(
        SUM(CASE WHEN s.DELIVERY_STATUS = 'Late delivery'
            THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(s.SHIPMENT_ID), 0), 2
    ) AS LATE_PCT
FROM SHIPMENTS s
JOIN ORDER_ITEMS oi ON s.ORDER_ITEM_ID = oi.ORDER_ITEM_ID
JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
GROUP BY TRUNC(o.ORDER_DATE, 'MM')
ORDER BY ORDER_MONTH;</code></pre>

  <pre><code class="language-sql">-- Late delivery root cause ranking by category using DENSE_RANK
SELECT p.CATEGORY_NAME,
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
ORDER BY LATE_DELIVERY_PCT DESC;</code></pre>

  <h3>Reporting Views</h3>
  <p>
    Six views pre-aggregate data for Power Query and Power BI, eliminating repeated complex joins at the dashboard layer:
    <strong>VW_DEMAND_TIMESERIES</strong> (monthly demand with rolling averages),
    <strong>VW_FULFILLMENT_KPI</strong> (on-time rate, lead time, late delivery by category/mode),
    <strong>VW_PRODUCT_MASTER</strong> (SKU-level revenue, demand CV, ABC/XYZ inputs, planning parameters),
    <strong>VW_PLANNED_VS_ACTUAL</strong> (lead time and delivery date variances),
    <strong>VW_MRP_PLAN</strong> (gross/net requirements, projected on-hand, planned orders, exceptions),
    <strong>VW_FORECAST_VS_ACTUAL</strong> (forecast accuracy with MAE, MAPE, bias).
  </p>

  <h4>VW_DEMAND_TIMESERIES &mdash; Monthly Demand with Rolling Averages &amp; YoY Comparison</h4>
  <pre><code class="language-sql">CREATE OR REPLACE VIEW VW_DEMAND_TIMESERIES AS
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
SELECT ORDER_MONTH, CATEGORY_NAME, TOTAL_UNITS, REVENUE,
    ROUND(AVG(TOTAL_UNITS) OVER (
        PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS ROLLING_3M_AVG_UNITS,
    ROUND(AVG(TOTAL_UNITS) OVER (
        PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
        ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
    ), 2) AS ROLLING_6M_AVG_UNITS,
    LAG(TOTAL_UNITS, 12) OVER (
        PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
    ) AS UNITS_PRIOR_YEAR,
    CASE
        WHEN LAG(TOTAL_UNITS, 12) OVER (
            PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH) > 0 THEN
            ROUND((TOTAL_UNITS - LAG(TOTAL_UNITS, 12) OVER (
                PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH
            )) * 100.0 / LAG(TOTAL_UNITS, 12) OVER (
                PARTITION BY CATEGORY_NAME ORDER BY ORDER_MONTH), 2)
        ELSE NULL
    END AS YOY_CHANGE_PCT
FROM monthly_raw;</code></pre>

  <h4>VW_FORECAST_VS_ACTUAL &mdash; Forecast Accuracy with Error Metrics</h4>
  <pre><code class="language-sql">CREATE OR REPLACE VIEW VW_FORECAST_VS_ACTUAL AS
SELECT
    f.CATEGORY_NAME, f.FORECAST_PERIOD, f.FORECASTED_QTY,
    f.FORECAST_METHOD, f.CONFIDENCE_LOWER, f.CONFIDENCE_UPPER,
    d.ACTUAL_UNITS, d.ACTUAL_REVENUE,
    ROUND(f.FORECASTED_QTY - d.ACTUAL_UNITS, 2)            AS FORECAST_ERROR,
    ROUND(ABS(f.FORECASTED_QTY - d.ACTUAL_UNITS), 2)       AS ABS_ERROR,
    CASE WHEN d.ACTUAL_UNITS > 0 THEN
        ROUND(ABS(f.FORECASTED_QTY - d.ACTUAL_UNITS) * 100.0
              / d.ACTUAL_UNITS, 2)
    ELSE NULL END                                           AS APE,
    CASE
        WHEN f.FORECASTED_QTY > d.ACTUAL_UNITS THEN 'OVER'
        WHEN f.FORECASTED_QTY &lt; d.ACTUAL_UNITS THEN 'UNDER'
        ELSE 'EXACT'
    END AS BIAS_DIRECTION
FROM FORECAST_PLAN f
LEFT JOIN (
    SELECT p.CATEGORY_NAME, TRUNC(o.ORDER_DATE, 'MM') AS ORDER_MONTH,
           SUM(oi.QUANTITY) AS ACTUAL_UNITS,
           ROUND(SUM(oi.SALES), 2) AS ACTUAL_REVENUE
    FROM ORDER_ITEMS oi
    JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
    JOIN PRODUCTS p ON oi.PRODUCT_CARD_ID = p.PRODUCT_CARD_ID
    WHERE o.ORDER_STATUS NOT IN ('CANCELED', 'SUSPECTED_FRAUD')
    GROUP BY p.CATEGORY_NAME, TRUNC(o.ORDER_DATE, 'MM')
) d ON f.CATEGORY_NAME = d.CATEGORY_NAME
    AND f.FORECAST_PERIOD = d.ORDER_MONTH;</code></pre>

  <p>
    <strong>SQL Scripts:</strong>
    <a href="sql/03_demand_queries.sql">03_demand_queries.sql</a> |
    <a href="sql/04_inventory_fulfillment_queries.sql">04_inventory_fulfillment_queries.sql</a> |
    <a href="sql/05_reporting_views.sql">05_reporting_views.sql</a>
  </p>

  <h3>Stored Procedure &amp; Scheduling</h3>
  <p>
    The <code>REFRESH_SUPPLY_CHAIN_DATA</code> procedure packages the full data refresh and MRP calculation into a single callable command:
    truncate staging tables, reload transactional data, recalculate derived fields, run MRP net requirements (gross-to-net netting, lot sizing, lead time offsetting, exception flagging),
    write planned orders to MRP_REQUIREMENTS, refresh all six reporting views, and log audit timestamps. DBMS_SCHEDULER runs this nightly at 2:00 AM.
  </p>

  <h4>MRP Net Requirements Calculation &mdash; Core Loop</h4>
  <pre><code class="language-sql">-- For each category with forecast data, loop through planning periods
FOR period_rec IN (
    SELECT FORECAST_PERIOD, FORECASTED_QTY
    FROM FORECAST_PLAN
    WHERE CATEGORY_NAME = v_category
    ORDER BY FORECAST_PERIOD
) LOOP
    v_gross_req    := period_rec.FORECASTED_QTY;
    v_sched_rcpt   := 0;

    -- Projected On-Hand = prior on-hand - gross + scheduled receipts
    v_proj_on_hand := v_prior_on_hand - v_gross_req + v_sched_rcpt;

    -- Net Requirements = MAX(0, gross - prior on-hand - sched receipts)
    v_net_req := GREATEST(0, v_gross_req - v_prior_on_hand - v_sched_rcpt);

    -- Planned Order Qty (apply lot sizing: EOQ, FIXED_LOT, or LOT_FOR_LOT)
    IF v_net_req > 0 THEN
        CASE v_lot_method
            WHEN 'EOQ' THEN
                v_planned_qty := CEIL(v_net_req / GREATEST(v_lot_size, 1))
                                 * GREATEST(v_lot_size, 1);
            WHEN 'LOT_FOR_LOT' THEN
                v_planned_qty := v_net_req;
            ...
        END CASE;
        v_proj_on_hand := v_proj_on_hand + v_planned_qty;
    END IF;

    -- Exception Flagging
    IF v_proj_on_hand &lt; v_safety_stock THEN
        v_exception := 'EXPEDITE';
    END IF;
    IF v_release_date &lt; TRUNC(SYSDATE) THEN
        v_exception := 'RESCHEDULE';
    END IF;

    INSERT INTO MRP_REQUIREMENTS (...) VALUES (...);
    v_prior_on_hand := v_proj_on_hand;  -- carry forward
END LOOP;</code></pre>

  <h4>DBMS_SCHEDULER Job Creation</h4>
  <pre><code class="language-sql">BEGIN
    DBMS_SCHEDULER.CREATE_JOB(
        job_name        => 'JOB_REFRESH_SUPPLY_CHAIN',
        job_type        => 'STORED_PROCEDURE',
        job_action      => 'REFRESH_SUPPLY_CHAIN_DATA',
        start_date      => TRUNC(SYSDATE + 1) + INTERVAL '2' HOUR,  -- Next day 2:00 AM
        repeat_interval => 'FREQ=DAILY; BYHOUR=2; BYMINUTE=0; BYSECOND=0',
        enabled         => TRUE,
        auto_drop       => FALSE,
        comments        => 'Nightly refresh: inventory snapshot recalculation, '
                        || 'MRP net requirements calculation, and reporting view '
                        || 'data update. Runs at 2:00 AM daily.'
    );
END;</code></pre>

  <p>
    <strong>SQL Script:</strong> <a href="sql/06_stored_procedure_mrp.sql">06_stored_procedure_mrp.sql</a>
  </p>

</details>

<details class="dropdown-section">
  <summary><strong>Phase 3 — Power Query ETL &amp; Custom Functions</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Core Transformation Steps</h3>
  <p>
    Four Oracle view CSV exports were imported into Excel as structured tables. Transformations applied include
    datetime type fixes (set datetime type first, then Date Only as a separate step to avoid DataFormat.Error),
    null handling, text standardization, and proper data type assignment. Derived time features were created
    for downstream analysis: month, quarter, day of week, and fiscal period.
  </p>

  <h3>Custom M Functions</h3>
  <ul>
    <li><strong>fn_CalculateSafetyStock</strong> &mdash; Inputs: avg demand, demand std dev, lead time, service level Z-score</li>
    <li><strong>fn_ClassifyABC</strong> &mdash; Input: cumulative revenue %; Output: A/B/C classification</li>
    <li><strong>fn_ClassifyXYZ</strong> &mdash; Input: coefficient of variation; Output: X/Y/Z classification</li>
    <li><strong>fn_CalculateReorderPoint</strong> &mdash; Combines avg daily demand, lead time, and safety stock</li>
    <li><strong>fn_CalculateNetRequirements</strong> &mdash; Gross requirements minus projected on-hand minus scheduled receipts</li>
  </ul>

  <h3>Parameters &amp; Query Folding</h3>
  <p>
    A Parameters sheet was created with named ranges &mdash; ServiceLevel, ZScore, PlanningHorizon, AnalysisStart,
    and AnalysisEnd &mdash; enabling dynamic switching between analysis windows, Oracle environments, and planning
    horizons (3/6/12 months) without modifying query logic. Query folding was documented for each transformation step,
    identifying which steps fold to Oracle (execute server-side) vs. execute locally in the Power Query engine.
  </p>

  <p>
    <strong>Excel Workbook:</strong>
    <a href="excel/SupplyChain_Analysis_V11.xlsx">SupplyChain_Analysis_V11.xlsx</a> &mdash; Complete Excel workbook containing all Power Query ETL logic with custom M functions, the Power Pivot data model, demand forecasting worksheets (ETS, MA_3, MA_6, WMA_3), ABC/XYZ classification matrix, inventory optimization calculations (EOQ, safety stock, reorder points), MRP simulation and what-if analysis via Goal Seek and Solver, dynamic array lookup tools (FILTER, XLOOKUP, SORT), and the parameter sheet for dynamic analysis switching.
  </p>

</details>

<details class="dropdown-section">
  <summary><strong>Phase 4 — Excel Analysis &amp; Optimization</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Demand Forecasting &amp; Method Comparison</h3>
  <p>
    Demand forecasts were built for the top 9 product categories (by ABC classification) using Excel's FORECAST.ETS
    function (exponential triple smoothing), 3-month moving average (MA_3), 6-month moving average (MA_6), and
    3-month weighted moving average (WMA_3). All categories and methods are consolidated in a single structured
    Demand_Forecast worksheet. SORTBY/FILTER was used to extract and sort category data by date, avoiding the
    numeric-sort bug that arises from separate SORT/FILTER formulas.
  </p>
  <p>
    Confidence intervals (ETS_LOWER, ETS_UPPER) were generated using FORECAST.ETS.CONFINT scoped to forecast periods
    only. A key learning: October 2017 showed anomalously low units due to being a partial month in the dataset &mdash;
    excluding it from ETS historical ranges corrected forecasts from unrealistic to credible values. Forecast outputs
    were formatted for write-back to Oracle's FORECAST_PLAN table
    (see <a href="sql/07_forecast_plan_writeback.sql">07_forecast_plan_writeback.sql</a>).
  </p>

  <details style="margin-top: 8px;">
    <summary><em>Forecast Write-Back &amp; MRP Cross-Check</em></summary>
    <pre><code class="language-sql">-- Insert ETS forecast data into Oracle (7 A-class categories x 6 months = 42 rows)
INSERT INTO FORECAST_PLAN (
    CATEGORY_NAME, FORECAST_PERIOD, FORECASTED_QTY,
    CONFIDENCE_LOWER, CONFIDENCE_UPPER,
    FORECAST_METHOD, MAPE_PCT, NOTES
) VALUES (
    'Fishing', DATE '2017-10-01', 505,
    471.25, 537.65,
    'ETS', 5.78, 'Auto-seasonality; 6-month horizon'
);
-- ... 41 additional INSERT statements for remaining categories/periods

-- Cross-check: Forecast vs MRP Gross Requirements (variance should be 0)
SELECT
    fp.CATEGORY_NAME, fp.FORECAST_PERIOD,
    fp.FORECASTED_QTY                          AS "Forecast Qty",
    mr.GROSS_REQUIREMENTS                      AS "MRP Gross Req",
    fp.FORECASTED_QTY - mr.GROSS_REQUIREMENTS  AS "Variance"
FROM FORECAST_PLAN fp
LEFT JOIN MRP_REQUIREMENTS mr
    ON fp.CATEGORY_NAME = mr.CATEGORY_NAME
    AND fp.FORECAST_PERIOD = mr.PLANNING_PERIOD
ORDER BY fp.CATEGORY_NAME, fp.FORECAST_PERIOD;</code></pre>
  </details>

  <h3>ABC/XYZ Classification</h3>
  <p>
    ABC classification was based on cumulative revenue percentage (A = top 80%, B = next 15%, C = bottom 5%).
    XYZ classification was based on coefficient of variation of demand (X = stable/predictable, Y = moderate
    variability, Z = erratic). Classification was computed at the Oracle layer for all 50 product categories,
    then summarized in the ABC_XYZ_Matrix worksheet using COUNTIFS/SUMIFS grids. A key finding: all A-class
    categories are X-class (stable demand), representing the highest-revenue, most-predictable segment &mdash;
    ideal candidates for automated replenishment.
  </p>

  <figure style="margin: 20px 0;">
    <img
      src="images/supply-chain-matrix.png"
      alt="ABC/XYZ classification matrix showing category counts and revenue distribution"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
      ABC/XYZ classification matrix &mdash; all A-class categories fall into the X (stable demand) column.
    </figcaption>
  </figure>

  <h3>Inventory Optimization (EOQ, Safety Stock, Solver)</h3>
  <p>
    EOQ (Economic Order Quantity), safety stock, and reorder points were calculated per category using custom
    Power Query M functions (fn_CalculateSafetyStock, fn_CalculateReorderPoint). The service level parameter
    (Z-score) is driven from the Parameters sheet for dynamic what-if analysis. The Inventory_Optimization
    worksheet consolidates all metrics per category into a single actionable view.
  </p>

  <h3>MRP Scenario Analysis Workbook</h3>
  <p>
    The MRP_Simulation worksheet performs net requirements calculation (gross requirements minus projected on-hand
    minus scheduled receipts) using fn_CalculateNetRequirements. The What_If_Analysis worksheet provides sensitivity
    analysis on service levels and planning horizons using Goal Seek and Solver. An Inventory_Tools worksheet offers
    dynamic array-based lookup tools (FILTER, XLOOKUP, SORT) for the Operations team to query inventory status
    by category.
  </p>

  <p>
    <strong>Excel Workbook:</strong>
    <a href="excel/SupplyChain_Analysis_V11.xlsx">SupplyChain_Analysis_V11.xlsx</a> &mdash; Contains all worksheets referenced above: Demand_Forecast (all categories and methods), ABC_XYZ_Matrix (COUNTIFS/SUMIFS classification grids), Inventory_Optimization (EOQ, safety stock, reorder points per category), MRP_Simulation (net requirements calculation), What_If_Analysis (sensitivity analysis via Goal Seek and Solver), Inventory_Tools (dynamic array lookup tools), and the Parameters sheet for dynamic switching.
  </p>

</details>

<details class="dropdown-section">
  <summary><strong>Phase 5 — Power BI Dashboard</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Data Model</h3>
  <p>
    A star schema was built in Power BI with fact and dimension tables, enabling efficient slicing and cross-filtering
    across all six dashboard pages.
  </p>

  <figure style="margin: 20px 0;">
    <img
      src="images/supply-chain-star-schema.png"
      alt="Power BI star schema data model showing fact and dimension table relationships"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
      Star schema data model in Power BI with fact tables (demand, fulfillment, KPI) and dimension tables (date, category, region, shipping mode).
    </figcaption>
  </figure>

  <h3>Page 1: Executive KPI Overview</h3>
  <p>
    High-level summary of supply chain health with KPI cards, trend lines, and performance indicators. Provides
    at-a-glance metrics including total orders, revenue, on-time delivery rate, and YoY growth. Serves as the
    landing page for executives who need a quick pulse check.
  </p>

  <figure style="margin: 20px 0;">
    <img
      src="images/supply-chain-page-1-dashboard.png"
      alt="Executive KPI Overview dashboard with KPI cards, trend lines, and performance indicators"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
      Page 1: Executive KPI Overview &mdash; at-a-glance supply chain health metrics.
    </figcaption>
  </figure>

  <h3>Page 2: Demand Analysis &amp; Forecasting</h3>
  <p>
    Monthly demand trends by product category with ETS forecast overlays, confidence intervals, and forecast
    accuracy metrics (MAE, MAPE). Enables demand planners to compare forecast methods, identify seasonal patterns,
    and assess which categories are trending up or down.
  </p>

  <figure style="margin: 20px 0;">
    <img
      src="images/supply-chain-page-2-dashboard.png"
      alt="Demand Analysis and Forecasting dashboard with trend lines and forecast overlays"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
      Page 2: Demand Analysis &amp; Forecasting &mdash; category-level demand trends with ETS forecast overlays.
    </figcaption>
  </figure>

  <h3>Page 3: Inventory Optimization &amp; ABC/XYZ Analysis</h3>
  <p>
    ABC/XYZ classification matrix, inventory health metrics, safety stock levels, and reorder point analysis.
    Highlights which categories need inventory policy adjustments and where stockout risk is highest.
  </p>

  <figure style="margin: 20px 0;">
    <img
      src="images/supply-chain-page-3-dashboard.png"
      alt="Inventory Optimization and ABC/XYZ Analysis dashboard"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
      Page 3: Inventory Optimization &amp; ABC/XYZ Analysis &mdash; classification matrix and inventory health metrics.
    </figcaption>
  </figure>

  <h3>Page 4: Fulfillment &amp; Logistics Performance</h3>
  <p>
    On-time delivery rates, lead time variance analysis, shipping mode performance comparison, and late delivery
    root cause ranking by category, region, and shipping mode. Helps operations teams pinpoint fulfillment bottlenecks.
  </p>

  <figure style="margin: 20px 0;">
    <img
      src="images/supply-chain-page-4-dashboard.png"
      alt="Fulfillment and Logistics Performance dashboard with delivery metrics"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
      Page 4: Fulfillment &amp; Logistics Performance &mdash; on-time rates, lead time variance, and shipping mode comparison.
    </figcaption>
  </figure>

  <h3>Page 5: Supply Plan &amp; MRP Analysis</h3>
  <p>
    Time-phased MRP output showing gross requirements, scheduled receipts, projected on-hand inventory, net
    requirements, and planned order releases. Includes MRP exception log and planned order timeline for supply planners.
  </p>

  <figure style="margin: 20px 0;">
    <img
      src="images/supply-chain-page-5-dashboard.png"
      alt="Supply Plan and MRP Analysis dashboard with time-phased requirements"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
      Page 5: Supply Plan &amp; MRP Analysis &mdash; time-phased MRP output with exception log.
    </figcaption>
  </figure>

  <h3>Page 6: Insights, Recommendations &amp; Closed-Loop Actions</h3>
  <p>
    Consolidated findings and actionable business recommendations. Demonstrates the closed-loop process: analysis
    findings feed back into master data updates (lead times, safety stock levels, lot sizing rules) that take effect
    in the next automated refresh cycle.
  </p>

  <figure style="margin: 20px 0;">
    <img
      src="images/supply-chain-page-6-dashboard.png"
      alt="Insights, Recommendations and Closed-Loop Actions dashboard"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
      Page 6: Insights, Recommendations &amp; Closed-Loop Actions &mdash; findings feed back into master data updates.
    </figcaption>
  </figure>

  <h3>DAX Measures</h3>
  <p>Key DAX measures created for the dashboard:</p>
  <ul>
    <li><strong>Growth &amp; Revenue:</strong> YoY Growth %, Total Revenue, Total Orders</li>
    <li><strong>Fulfillment:</strong> On-Time Delivery Rate, Late Delivery Rate</li>
    <li><strong>Forecast Accuracy:</strong> MAE, MAPE, Forecast Bias</li>
    <li><strong>Inventory:</strong> Inventory Turnover, Days of Supply, In-Stock Rate</li>
    <li><strong>Supply Planning:</strong> MRP Coverage Ratio, Supply Plan Adherence</li>
  </ul>
  <p>All DAX measures auto-recalculate on every scheduled refresh cycle.</p>

  <h3>Data Alerts &amp; Row-Level Security</h3>
  <p>
    Data alerts were configured on critical thresholds: in-stock rate drops, late delivery spikes, projected stockouts,
    MRP exception counts, and forecast bias. Row-Level Security (RLS) was implemented with two roles &mdash; the
    Marketing team sees sell-through and demand data only, while the Operations team sees production, fulfillment,
    MRP, and inventory data. Both roles use the same dashboard; Power BI filters automatically based on role assignment.
  </p>

  <p>
    <strong>Power BI File:</strong>
    <a href="powerbi/SupplyChain_Dashboard_V1.pbix">SupplyChain_Dashboard_V1.pbix</a> &mdash; Complete Power BI Desktop file containing the six-page interactive dashboard, star schema data model with fact and dimension tables, all DAX measures (YoY growth, on-time rate, MAE, MAPE, inventory turnover, MRP coverage ratio, supply plan adherence), configured data alerts for critical threshold monitoring, and Row-Level Security roles for Marketing and Operations teams. Designed for scheduled refresh integration with Oracle views via the Power BI Service.
  </p>

</details>

<details class="dropdown-section">
  <summary><strong>Key Findings &amp; Business Recommendations</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Demand Forecast Highlights</h3>
  <p>
    All A-class categories exhibit stable (X-class) demand patterns, making them strong candidates for automated ETS
    forecasting. Seasonal patterns were identified in several categories. Partial-month data artifacts (e.g., October
    2017) must be excluded from ETS historical ranges to avoid corrupting forecast accuracy.
  </p>

  <h3>Inventory Recommendations</h3>
  <p>
    A-X categories (highest revenue, most predictable) should use automated reorder point replenishment with tight
    safety stock. B-Y and C-Z categories need higher safety stock buffers or periodic manual review. EOQ-based lot
    sizing reduces ordering costs for high-volume categories.
  </p>

  <h3>Supply Plan Recommendations</h3>
  <p>
    The MRP exception log identifies categories where projected on-hand drops below safety stock (expedite action),
    planned orders exceed capacity (split action), or scheduled receipts are past due (reschedule action). Lead time
    adjustments are recommended for categories with consistently high variance.
  </p>

  <h3>Fulfillment Improvements</h3>
  <p>
    Late delivery patterns are concentrated in specific regions and shipping modes. Shipping mode optimization
    opportunities were identified where standard shipping consistently underperforms relative to other modes.
  </p>

  <h3>Closed-Loop Process</h3>
  <p>
    Analysis findings feed back into master data updates: revised lead times, adjusted safety stock levels, updated
    lot sizing rules, and forecast method selections that improve the next MRP cycle &mdash; demonstrating the
    continuous improvement loop built into the automation architecture.
  </p>

</details>

<details class="dropdown-section">
  <summary><strong>Project Files &amp; Repository</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Repository Structure</h3>
  <ul>
    <li><strong>sql/</strong> &mdash; Oracle SQL scripts:
      <ul>
        <li><a href="sql/01_schema_ddl.sql">01_schema_ddl.sql</a> &mdash; Schema DDL (8 normalized tables + staging table)</li>
        <li><a href="sql/02_data_normalization.sql">02_data_normalization.sql</a> &mdash; INSERT/SELECT normalization from staging to production tables</li>
        <li><a href="sql/03_demand_queries.sql">03_demand_queries.sql</a> &mdash; Demand &amp; sales extraction queries (monthly/weekly aggregations, rolling averages, demand variability)</li>
        <li><a href="sql/04_inventory_fulfillment_queries.sql">04_inventory_fulfillment_queries.sql</a> &mdash; Inventory analytics (ABC/XYZ classification, product master) &amp; fulfillment performance (on-time rates, lead time variance, root cause ranking)</li>
        <li><a href="sql/05_reporting_views.sql">05_reporting_views.sql</a> &mdash; Six pre-calculated reporting views for Power BI consumption</li>
        <li><a href="sql/06_stored_procedure_mrp.sql">06_stored_procedure_mrp.sql</a> &mdash; REFRESH_SUPPLY_CHAIN_DATA stored procedure &amp; DBMS_SCHEDULER job</li>
        <li><a href="sql/07_forecast_plan_writeback.sql">07_forecast_plan_writeback.sql</a> &mdash; Forecast write-back logic from Excel to Oracle</li>
      </ul>
    </li>
    <li><strong>excel/</strong> &mdash; <a href="excel/SupplyChain_Analysis_V11.xlsx">SupplyChain_Analysis_V11.xlsx</a> &mdash; Excel workbook with Power Query ETL, Power Pivot data model, demand forecasting, ABC/XYZ classification, inventory optimization, MRP simulation, and what-if analysis</li>
    <li><strong>powerbi/</strong> &mdash; <a href="powerbi/SupplyChain_Dashboard_V1.pbix">SupplyChain_Dashboard_V1.pbix</a> &mdash; Six-page interactive Power BI dashboard with star schema, DAX measures, data alerts, and Row-Level Security</li>
    <li><strong>images/</strong> &mdash; Dashboard screenshots, star schema diagram, ABC/XYZ matrix visualization</li>
  </ul>

  <p>
    <strong>GitHub Repository:</strong>
    <a href="https://github.com/nadeaujonny/nadeaujonny.github.io/tree/main/projects/supply-chain-oracle-powerbi">
      nadeaujonny/nadeaujonny.github.io/projects/supply-chain-oracle-powerbi
    </a>
  </p>

</details>
