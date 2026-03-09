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

  <!-- PLACEHOLDER: Add automation architecture diagram screenshot here -->
  <!--
  <figure style="margin: 20px 0;">
    <img
      src="images/automation-pipeline-diagram.png"
      alt="Automation pipeline diagram showing Oracle to Power Query to Power BI flow"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
      End-to-end automation pipeline: Oracle stored procedure → Power Query ETL → Power BI dashboard refresh.
    </figcaption>
  </figure>
  -->

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

  <!-- PLACEHOLDER: Fill in when Phase 1 is complete -->

  <h3>Schema Design</h3>
  <p>
    <!-- Describe the normalized relational schema: ORDERS, ORDER_ITEMS, PRODUCTS, CUSTOMERS, SHIPMENTS, FORECAST_PLAN, MRP_REQUIREMENTS, INVENTORY_SNAPSHOT -->
    <em>Section content will be added when Phase 1 is complete.</em>
  </p>

  <!-- PLACEHOLDER: Add ERD screenshot here -->
  <!--
  <figure style="margin: 20px 0;">
    <img
      src="images/schema-erd.png"
      alt="Entity-relationship diagram of the normalized supply chain schema"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
      Normalized relational schema with 8 tables and foreign key relationships.
    </figcaption>
  </figure>
  -->

  <!-- PLACEHOLDER: Add key DDL snippets or link to full SQL file -->

</details>

<details class="dropdown-section">
  <summary><strong>Phase 2 — Oracle SQL: Queries, Views &amp; Stored Procedures</strong></summary>

  <div style="margin-top: 12px;"></div>

  <!-- PLACEHOLDER: Fill in when Phase 2 is complete -->

  <h3>SQL Query Categories</h3>
  <ul>
    <li><strong>Demand &amp; Sales Extraction</strong> &mdash; Monthly/weekly aggregations, rolling averages, demand variability metrics</li>
    <li><strong>Inventory &amp; Product Analytics</strong> &mdash; ABC revenue concentration, demand rate, product master summary</li>
    <li><strong>Planned vs. Actual Analysis</strong> &mdash; Lead time variance, on-time delivery rate, late delivery root cause ranking</li>
    <li><strong>MRP &amp; Supply Planning</strong> &mdash; Gross requirements, projected on-hand, net requirements, planned order releases, exception flagging</li>
    <li><strong>Forecast Accuracy</strong> &mdash; Forecast vs. actual comparison, MAE, MAPE, bias detection</li>
  </ul>

  <h3>Reporting Views</h3>
  <p><em>Section content will be added when Phase 2 is complete.</em></p>
  <!-- PLACEHOLDER: Document each of the 6 views with purpose and key columns -->

  <h3>Stored Procedure: REFRESH_SUPPLY_CHAIN_DATA</h3>
  <p><em>Section content will be added when Phase 2 is complete.</em></p>
  <!-- PLACEHOLDER: Document the procedure steps and add code snippet -->

  <h3>Scheduled Job (DBMS_SCHEDULER)</h3>
  <p><em>Section content will be added when Phase 2 is complete.</em></p>
  <!-- PLACEHOLDER: Document the scheduler configuration -->

</details>

<details class="dropdown-section">
  <summary><strong>Phase 3 — Power Query ETL &amp; Custom Functions</strong></summary>

  <div style="margin-top: 12px;"></div>

  <!-- PLACEHOLDER: Fill in when Phase 3 is complete -->

  <h3>Core Transformation Steps</h3>
  <p><em>Section content will be added when Phase 3 is complete.</em></p>

  <h3>Custom M Functions</h3>
  <ul>
    <li><strong>fn_CalculateSafetyStock</strong> &mdash; Inputs: avg demand, demand std dev, lead time, service level Z-score</li>
    <li><strong>fn_ClassifyABC</strong> &mdash; Input: cumulative revenue %; Output: A/B/C classification</li>
    <li><strong>fn_ClassifyXYZ</strong> &mdash; Input: coefficient of variation; Output: X/Y/Z classification</li>
    <li><strong>fn_CalculateReorderPoint</strong> &mdash; Combines avg daily demand, lead time, and safety stock</li>
    <li><strong>fn_CalculateNetRequirements</strong> &mdash; Gross requirements minus projected on-hand minus scheduled receipts</li>
  </ul>

  <h3>Parameters &amp; Query Folding</h3>
  <p><em>Section content will be added when Phase 3 is complete.</em></p>

</details>

<details class="dropdown-section">
  <summary><strong>Phase 4 — Excel Analysis &amp; Optimization</strong></summary>

  <div style="margin-top: 12px;"></div>

  <!-- PLACEHOLDER: Fill in when Phase 4 is complete -->

  <h3>Demand Forecasting &amp; Method Comparison</h3>
  <p><em>Section content will be added when Phase 4 is complete.</em></p>
  <!-- PLACEHOLDER: Screenshots of forecast comparison, accuracy metrics -->

  <h3>ABC/XYZ Classification</h3>
  <p><em>Section content will be added when Phase 4 is complete.</em></p>
  <!-- PLACEHOLDER: ABC-XYZ matrix screenshot, policy recommendations -->

  <h3>Inventory Optimization (EOQ, Safety Stock, Solver)</h3>
  <p><em>Section content will be added when Phase 4 is complete.</em></p>
  <!-- PLACEHOLDER: Solver setup screenshot, optimization results -->

  <h3>MRP Scenario Analysis Workbook</h3>
  <p><em>Section content will be added when Phase 4 is complete.</em></p>
  <!-- PLACEHOLDER: What-if screenshots, large order impact modeling -->

</details>

<details class="dropdown-section">
  <summary><strong>Phase 5 — Power BI Dashboard</strong></summary>

  <div style="margin-top: 12px;"></div>

  <!-- PLACEHOLDER: Fill in when Phase 5 is complete -->

  <h3>Data Model</h3>
  <p><em>Section content will be added when Phase 5 is complete.</em></p>
  <!-- PLACEHOLDER: Star schema screenshot from Power BI model view -->

  <h3>Page 1: Executive KPI Overview</h3>
  <p><em>Section content will be added when Phase 5 is complete.</em></p>
  <!-- PLACEHOLDER: Dashboard screenshot + KPI descriptions -->

  <h3>Page 2: Demand Analysis &amp; Forecasting</h3>
  <p><em>Section content will be added when Phase 5 is complete.</em></p>

  <h3>Page 3: Inventory Optimization &amp; ABC/XYZ Analysis</h3>
  <p><em>Section content will be added when Phase 5 is complete.</em></p>

  <h3>Page 4: Fulfillment &amp; Logistics Performance</h3>
  <p><em>Section content will be added when Phase 5 is complete.</em></p>

  <h3>Page 5: Supply Plan &amp; MRP Analysis</h3>
  <p><em>Section content will be added when Phase 5 is complete.</em></p>

  <h3>Page 6: Insights, Recommendations &amp; Closed-Loop Actions</h3>
  <p><em>Section content will be added when Phase 5 is complete.</em></p>

  <h3>DAX Measures</h3>
  <p><em>Section content will be added when Phase 5 is complete.</em></p>
  <!-- PLACEHOLDER: Key DAX measure code snippets -->

  <h3>Data Alerts &amp; Row-Level Security</h3>
  <p><em>Section content will be added when Phase 5 is complete.</em></p>

</details>

<details class="dropdown-section">
  <summary><strong>Key Findings &amp; Business Recommendations</strong></summary>

  <div style="margin-top: 12px;"></div>

  <!-- PLACEHOLDER: Fill in when all phases are complete -->
  <p><em>Section content will be added when all project phases are complete.</em></p>

  <!--
  Expected sections:
  - Demand Forecast Highlights (trending categories, seasonality, accuracy)
  - Inventory Recommendations (reorder point adjustments, safety stock, ABC/XYZ policy)
  - Supply Plan Recommendations (MRP exceptions, lead time adjustments, lot sizing)
  - Fulfillment Improvements (shipping mode optimization, regional bottlenecks)
  - Master Data Update Recommendations (closed-loop process demonstration)
  -->

</details>

<details class="dropdown-section">
  <summary><strong>Project Files &amp; Repository</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Repository Structure</h3>
  <ul>
    <li><strong>sql/</strong> &mdash; All Oracle SQL scripts (DDL, queries, views, stored procedure, scheduler job)</li>
    <li><strong>images/</strong> &mdash; Dashboard screenshots, ERD diagram, analysis visuals</li>
    <li><strong>README.md</strong> &mdash; Full project documentation (in the standalone GitHub repo)</li>
  </ul>

  <p>
    <!-- PLACEHOLDER: Add link to standalone GitHub repo once created -->
    <strong>GitHub Repository:</strong> <em>Link will be added when the standalone repo is created.</em>
  </p>

</details>
