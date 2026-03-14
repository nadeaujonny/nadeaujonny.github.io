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
  <ul>
    <li><strong>Demand &amp; Sales Extraction</strong> &mdash; Monthly/weekly aggregations, rolling averages, demand variability metrics (<a href="sql/03_demand_queries.sql">03_demand_queries.sql</a>)</li>
    <li><strong>Inventory &amp; Product Analytics</strong> &mdash; ABC revenue concentration, fulfillment KPIs, lead time variance, demand rate, product master summary (<a href="sql/04_inventory_fulfillment_queries.sql">04_inventory_fulfillment_queries.sql</a>)</li>
    <li><strong>Planned vs. Actual Analysis</strong> &mdash; Lead time variance, on-time delivery rate, late delivery root cause ranking</li>
    <li><strong>MRP &amp; Supply Planning</strong> &mdash; Gross requirements, projected on-hand, net requirements, planned order releases, exception flagging</li>
    <li><strong>Forecast Accuracy</strong> &mdash; Forecast vs. actual comparison, MAE, MAPE, bias detection</li>
  </ul>

  <h3>Reporting Views</h3>
  <p>
    Six reporting views pre-aggregate data for downstream consumption by Power Query and Power BI, eliminating
    repeated complex joins at the dashboard layer.
  </p>
  <ul>
    <li><strong>VW_DEMAND_TIMESERIES</strong> &mdash; Pre-aggregated monthly demand by category, ready for Excel forecast sheet ingestion</li>
    <li><strong>VW_FULFILLMENT_KPI</strong> &mdash; Monthly on-time rate, average lead time, late delivery rate, lead time variance by category and shipping mode</li>
    <li><strong>VW_PRODUCT_MASTER</strong> &mdash; SKU-level summary with total revenue, total units, average demand rate, demand CV, ABC/XYZ classification inputs, and planning parameters</li>
    <li><strong>VW_PLANNED_VS_ACTUAL</strong> &mdash; Planned vs. actual lead times and delivery dates for variance reporting</li>
    <li><strong>VW_MRP_PLAN</strong> &mdash; Complete MRP output by category and period: gross requirements, scheduled receipts, projected on-hand, net requirements, planned orders, exception flags</li>
    <li><strong>VW_FORECAST_VS_ACTUAL</strong> &mdash; Forecast accuracy: planned vs. actual demand by category/period with MAE, MAPE, and bias pre-calculated</li>
  </ul>
  <p>
    <strong>SQL Script:</strong> <a href="sql/05_reporting_views.sql">05_reporting_views.sql</a>
  </p>

  <h3>Stored Procedure: REFRESH_SUPPLY_CHAIN_DATA</h3>
  <p>
    The <code>REFRESH_SUPPLY_CHAIN_DATA</code> procedure packages the full data refresh and MRP calculation pipeline
    into a single callable command, executed as part of the nightly automation cycle:
  </p>
  <ol>
    <li>Truncates staging/temp tables to clear stale data</li>
    <li>Reloads fresh transactional data from source tables</li>
    <li>Recalculates derived fields (lead time variances, demand aggregations, ABC classification inputs)</li>
    <li>Reads the latest demand forecast from FORECAST_PLAN</li>
    <li>Runs MRP net requirements calculation (gross-to-net netting, lot sizing, lead time offsetting, exception flagging)</li>
    <li>Writes planned order releases to MRP_REQUIREMENTS</li>
    <li>Refreshes all six reporting views</li>
    <li>Logs refresh timestamp and row counts for audit trail</li>
  </ol>
  <p>
    <strong>SQL Script:</strong> <a href="sql/06_stored_procedure_mrp.sql">06_stored_procedure_mrp.sql</a>
  </p>

  <h3>Scheduled Job (DBMS_SCHEDULER)</h3>
  <p>
    DBMS_SCHEDULER is configured to run the stored procedure nightly at 2:00 AM &mdash; the same scheduling mechanism
    used in production Oracle Fusion Cloud environments. This eliminates manual SQL execution from the routine workflow,
    ensuring that reporting views and MRP outputs are always current when downstream consumers (Power BI, analysts)
    access the data each morning.
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

</details>

<details class="dropdown-section">
  <summary><strong>Phase 4 — Excel Analysis &amp; Optimization</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Demand Forecasting &amp; Method Comparison</h3>
  <p>
    Demand forecasts were built for the top 9 product categories (by ABC classification) using Excel's FORECAST.ETS
    function (exponential triple smoothing), 3-month moving average (MA_3), 6-month moving average (MA_6), and
    3-month weighted moving average (WMA_3). All categories and methods are consolidated in a single structured
    Demand_Forecast worksheet within
    <a href="excel/SupplyChain_Analysis_V11.xlsx">SupplyChain_Analysis_V11.xlsx</a>.
    SORTBY/FILTER was used to extract and sort category data by date, avoiding the
    numeric-sort bug that arises from separate SORT/FILTER formulas.
  </p>
  <p>
    Confidence intervals (ETS_LOWER, ETS_UPPER) were generated using FORECAST.ETS.CONFINT scoped to forecast periods
    only. A key learning: October 2017 showed anomalously low units due to being a partial month in the dataset &mdash;
    excluding it from ETS historical ranges corrected forecasts from unrealistic to credible values. Forecast outputs
    were formatted for write-back to Oracle's FORECAST_PLAN table
    (see <a href="sql/07_forecast_plan_writeback.sql">07_forecast_plan_writeback.sql</a>).
  </p>

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

</details>

<details class="dropdown-section">
  <summary><strong>Phase 5 — Power BI Dashboard</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Data Model</h3>
  <p>
    A star schema was built in Power BI with fact and dimension tables, enabling efficient slicing and cross-filtering
    across all six dashboard pages. The full report is available for download:
    <a href="powerbi/SupplyChain_Dashboard_V1.pbix">SupplyChain_Dashboard_V1.pbix</a>.
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
    <li><strong>sql/</strong> &mdash; All Oracle SQL scripts:
      <a href="sql/01_schema_ddl.sql">01_schema_ddl</a>,
      <a href="sql/02_data_normalization.sql">02_data_normalization</a>,
      <a href="sql/03_demand_queries.sql">03_demand_queries</a>,
      <a href="sql/04_inventory_fulfillment_queries.sql">04_inventory_fulfillment_queries</a>,
      <a href="sql/05_reporting_views.sql">05_reporting_views</a>,
      <a href="sql/06_stored_procedure_mrp.sql">06_stored_procedure_mrp</a>,
      <a href="sql/07_forecast_plan_writeback.sql">07_forecast_plan_writeback</a>
    </li>
    <li><strong>excel/</strong> &mdash; <a href="excel/SupplyChain_Analysis_V11.xlsx">SupplyChain_Analysis_V11.xlsx</a> &mdash; Excel workbook with Power Query, Power Pivot, forecasting, and optimization</li>
    <li><strong>powerbi/</strong> &mdash; <a href="powerbi/SupplyChain_Dashboard_V1.pbix">SupplyChain_Dashboard_V1.pbix</a> &mdash; Six-page Power BI dashboard with DAX measures, star schema, and RLS</li>
    <li><strong>images/</strong> &mdash; Dashboard screenshots, star schema, ABC/XYZ matrix</li>
  </ul>

  <p>
    <strong>GitHub Repository:</strong>
    <a href="https://github.com/nadeaujonny/nadeaujonny.github.io/tree/main/projects/supply-chain-oracle-powerbi">
      nadeaujonny/nadeaujonny.github.io/projects/supply-chain-oracle-powerbi
    </a>
  </p>

</details>
