---
layout: default
title: Sales Dashboard – Superstore Dataset (Excel)
---

<a href="/projects" class="back-btn">← Back to Projects</a>

# Sales Dashboard – Superstore Dataset (Excel)

> An end-to-end Excel analytics project demonstrating data cleaning, KPI development, pivot-table analysis, and executive dashboard design using a widely used public retail sample dataset.

---

<details>
  <summary><strong>Project Overview</strong></summary>

  <h3>Overview</h3>
  <p>
    This project analyzes Superstore retail sales data in Microsoft Excel to uncover trends in revenue, profit,
    customer segments, and regional performance. The goal is to demonstrate practical Excel analytics skills
    used in business environments—data cleaning (Power Query), pivot-based analysis, KPI modeling, and dashboard design.
  </p>

  <h3>Business Context</h3>
  <p>
    This analysis simulates a retail company evaluating sales performance, profitability, customer behavior,
    and operational efficiency to support data-driven decision making by executives and category managers.
  </p>

  <h3>Objectives</h3>
  <ul>
    <li>Define and calculate core KPIs: revenue, profit, profit margin, units sold, and return rate</li>
    <li>Clean and standardize raw orders using Power Query (types, trimming/cleaning text fields, deduping)</li>
    <li>Analyze performance using pivot tables and calculated fields (time trends, product mix, regional efficiency)</li>
    <li>Build an executive-style dashboard with slicers/timelines for interactive exploration</li>
  </ul>

  <h3>Dataset Overview</h3>
  <p>
    The Superstore dataset is a public retail transaction dataset commonly used for analytics and BI practice.
    It contains order-level sales data for a fictional office supply retailer.
  </p>

  <p><strong>At a glance</strong></p>
  <ul>
    <li><strong>Time range:</strong> 2014–2017</li>
    <li><strong>Granularity:</strong> one row per order line item</li>
    <li><strong>Size:</strong> ~10,000 rows</li>
    <li><strong>Core tables:</strong> Orders, Returns</li>
  </ul>

  <p><strong>Key fields</strong></p>
  <ul>
    <li><strong>Dimensions:</strong> segment, category/sub-category, region/state/city, order/ship dates</li>
    <li><strong>Measures:</strong> sales (revenue), profit, quantity</li>
  </ul>

  <p><strong>Limitations</strong></p>
  <ul>
    <li>Fictional data (not from a real company)</li>
    <li>No marketing/acquisition channel data</li>
    <li>Limited customer demographics</li>
    <li>Returns coverage depends on dataset version</li>
  </ul>

  <h3>Tools &amp; Skills Demonstrated</h3>
  <ul>
    <li><strong>Power Query:</strong> ETL, data types, text cleanup, de-duplication, derived date fields</li>
    <li><strong>Pivot Tables:</strong> grouping, sorting, filters, calculated fields</li>
    <li><strong>KPI Modeling:</strong> profit margin, return rate, performance comparisons</li>
    <li><strong>Excel Functions:</strong> XLOOKUP, SUMIFS/COUNTIFS, IF/IFERROR, date &amp; text functions</li>
    <li><strong>Visualization:</strong> pivot charts, conditional formatting, slicers/timelines, dashboard layout</li>
  </ul>

  <h3>KPI Definitions</h3>
  <ul>
    <li><strong>Revenue:</strong> SUM(Sales)</li>
    <li><strong>Profit:</strong> SUM(Profit)</li>
    <li><strong>Profit Margin:</strong> Profit / Revenue</li>
    <li><strong>Units Sold:</strong> SUM(Quantity)</li>
    <li><strong>Return Rate:</strong> # Returned Orders / # Total Orders</li>
  </ul>

  <h3>Data Preparation</h3>
  <ul>
    <li>Removed duplicates and invalid records</li>
    <li>Standardized date formats and category/location text fields</li>
    <li>Created derived columns (e.g., Year, Month, Year-Month; optional Profit Margin)</li>
    <li>Loaded a clean analysis table for pivots and dashboarding</li>
  </ul>

</details>

---

<details>
  <summary><strong>Data Preparation</strong></summary>

  <p>
    Before building KPIs, pivot tables, and charts, I cleaned and standardized the Superstore Orders dataset using
    <strong>Excel Power Query</strong>. The goal was to create a reliable, refreshable table (<code>Clean_Orders</code>)
    that serves as the single source of truth for all downstream analysis and dashboarding.
  </p>

  <h3>ETL Overview (At a Glance)</h3>
  <ul>
    <li><strong>Input:</strong> Raw Superstore Orders data (<code>.xls</code>) preserved as <code>Raw_Orders</code> (no manual edits).</li>
    <li><strong>Tool:</strong> Excel Power Query (Get &amp; Transform).</li>
    <li><strong>Query:</strong> Power Query pipeline documented in the Applied Steps panel (repeatable transformations).</li>
    <li><strong>Output:</strong> Cleaned dataset loaded into <code>Clean_Orders</code> (used by all pivots, charts, and KPIs).</li>
    <li><strong>Refreshability:</strong> Updates can be applied via <em>Data → Refresh All</em> without redoing manual steps.</li>
  </ul>

  <h3>Power Query Applied Steps (Evidence)</h3>
  <p>
    The screenshot below shows the Power Query Editor with the <em>Applied Steps</em> panel, documenting the cleaning pipeline
    (e.g., Source → Changed Type → Trim/Clean Text → Remove blanks/duplicates → Add derived columns). This provides traceable
    evidence of the transformation workflow.
  </p>

  <figure style="margin: 0;">
    <img
      src="images/excel-data-prep-power-query.png"
      alt="Power Query Applied Steps for Superstore data preparation"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Power Query Editor showing Applied Steps used to produce <code>Clean_Orders</code>.
      <span style="display:block; margin-top:4px;">
        <a href="images/excel-data-prep-power-query.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Cleaning &amp; Transformation Steps</h3>
  <ol>
    <li>
      <strong>Import &amp; Preserve Raw Data (Source)</strong>
      <ul>
        <li>Imported the dataset into Power Query and preserved the original <code>Raw_Orders</code> table unchanged.</li>
      </ul>
    </li>

    <li>
      <strong>Standardize Data Types (Changed Type)</strong>
      <ul>
        <li>Converted <code>Order Date</code> and <code>Ship Date</code> from DateTime to Date-only values for consistent time grouping.</li>
        <li>Set <code>Postal Code</code> to Text to preserve leading zeros.</li>
        <li>Validated numeric fields (<code>Sales</code>, <code>Profit</code>, <code>Discount</code>, <code>Quantity</code>) as numeric types.</li>
        <li>Ensured IDs and categorical fields were treated as text for stable grouping/filtering in pivots.</li>
      </ul>
    </li>

    <li>
      <strong>Clean Text Columns (Trimmed Text / Cleaned Text)</strong>
      <ul>
        <li>Trimmed whitespace and removed non-printable characters across key text columns.</li>
        <li>Standardized customer/product and category/geographic fields to prevent “duplicate label” issues in pivots.</li>
      </ul>
    </li>

    <li>
      <strong>Remove Blank / Invalid Records (Removed Blank Rows)</strong>
      <ul>
        <li>Removed blank rows and incomplete records that could distort KPI totals and chart trends.</li>
      </ul>
    </li>

    <li>
      <strong>Remove Duplicate Records (Removed Duplicates)</strong>
      <ul>
        <li>Removed duplicates using a composite key: <code>Order ID + Product ID</code>.</li>
        <li>Ensured each row represents a unique product line within an order (avoids double-counting revenue/profit).</li>
      </ul>
    </li>

    <li>
      <strong>Create Derived Time Fields (Added Custom Columns)</strong>
      <ul>
        <li>Created <code>Order Year</code>, <code>Order Month</code>, and <code>Order Year-Month</code> (YYYY-MM) for time-series analysis.</li>
        <li>These fields support consistent monthly trend pivots and timeline/slicer-friendly reporting.</li>
      </ul>
    </li>

    <li>
      <strong>Load Output to <code>Clean_Orders</code></strong>
      <ul>
        <li>Loaded the transformed result into <code>Clean_Orders</code>, which serves as the source for all pivots, charts, and KPIs.</li>
      </ul>
    </li>
  </ol>

  <h3>Data Quality Checks (Validation)</h3>
  <ul>
    <li>Verified key fields required for analysis (dates, location, category, sales, profit) were populated and correctly typed.</li>
    <li>Confirmed Postal Codes remain stable as text (prevents grouping errors from dropped leading zeros).</li>
    <li>Reviewed that duplicates were removed to prevent inflated revenue/profit totals.</li>
  </ul>

  <h3>Why This Matters</h3>
  <ul>
    <li><strong>Accuracy:</strong> Removing duplicates and invalid rows prevents inflated KPIs and misleading rankings.</li>
    <li><strong>Consistency:</strong> Cleaned text + standardized types eliminate pivot inconsistencies (e.g., “NY” vs “NY ”).</li>
    <li><strong>Repeatability:</strong> Power Query steps are documented and refreshable, enabling a maintainable analytics workflow.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 1 – Sales & Profit Trends Over Time</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>
    How have sales and profitability evolved over time from 2014 to 2017? Are there observable trends, seasonality,
    or periods of financial volatility that could inform forecasting, inventory planning, and cost control strategies?
  </p>

  <h3>Method</h3>
  <ul>
    <li>Used the cleaned <code>Clean_Orders</code> table as the data source.</li>
    <li>Built pivot tables grouped by <code>Order Year-Month</code>.</li>
    <li>Created line charts to visualize monthly revenue and monthly profit.</li>
    <li>Calculated key performance indicators (KPIs) to contextualize trends.</li>
  </ul>

  <h3>Key Performance Indicators (Overall)</h3>
  <figure style="margin: 0 0 16px 0;">
    <img
      src="images/excel-analysis-1-kpi-summary.png"
      alt="Superstore KPI summary"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Overall revenue, profit, profit margin, total orders, units sold, and average order value.
    </figcaption>
  </figure>

  <h3>Monthly Sales Trend</h3>
  <figure style="margin: 0 0 16px 0;">
    <img
      src="images/excel-analysis-1-monthly-sales.png"
      alt="Monthly sales trend from 2014 to 2017"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Monthly revenue trend grouped by year and month.
    </figcaption>
  </figure>

  <h3>Monthly Profit Trend</h3>
  <figure style="margin: 0 0 16px 0;">
    <img
      src="images/excel-analysis-1-monthly-profit.png"
      alt="Monthly profit trend from 2014 to 2017"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Monthly profit trend highlighting volatility and negative-profit periods.
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li>Revenue shows a clear upward long-term trend, indicating overall business growth.</li>
    <li>Sales exhibit strong seasonality, with recurring spikes toward the end of each year.</li>
    <li>Profit is significantly more volatile than revenue, with several months operating at a loss.</li>
    <li>Early years show more frequent negative-profit periods, while later years appear more stable.</li>
    <li>Revenue growth does not always translate proportionally to profit growth, suggesting cost or discount pressure.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>Increase inventory and staffing ahead of Q4 to capitalize on predictable seasonal demand.</li>
    <li>Investigate negative-profit months to identify unprofitable products, excessive discounting, or high shipping costs.</li>
    <li>Introduce profit-based performance monitoring in addition to revenue targets.</li>
    <li>Develop short-term sales and profit forecasts using historical seasonality patterns.</li>
    <li>Evaluate pricing and logistics strategies to stabilize margins during high-growth periods.</li>
  </ul>

</details>

---

<details>
<summary><strong>Analysis 2 – Product & Category Performance</strong></summary>

<br>

<h3>Business Question</h3>

<p>
Which product categories and individual products contribute the most to revenue and profit? 
Are there meaningful differences in profitability across categories that could inform pricing, 
inventory, and product strategy?
</p>

<hr>

<h3>Method</h3>

<ul>
  <li>Used the cleaned <code>Clean_Orders</code> table as the data source.</li>
  <li>Built pivot tables grouped by <strong>Category</strong> to calculate:
    <ul>
      <li>Total Sales (Revenue)</li>
      <li>Total Profit</li>
      <li>Profit Margin (calculated field = Profit / Sales)</li>
    </ul>
  </li>
  <li>Built a pivot table grouped by <strong>Product Name</strong> and sorted by <strong>Sum of Profit (descending)</strong> to identify the top 10 most profitable products.</li>
  <li>Created column and bar charts to visualize category-level and product-level performance.</li>
</ul>

<hr>

<h3>Sales Revenue by Category</h3>

<img src="images/excel-analysis-2-sales-revenue-by-category.png" alt="Sales Revenue by Category" style="max-width:100%;">

<hr>

<h3>Profit by Category</h3>

<img src="images/excel-analysis-2-profit-by-category.png" alt="Profit by Category" style="max-width:100%;">

<hr>

<h3>Profit Margin by Category</h3>

<img src="images/excel-analysis-2-profit-margin-by-category.png" alt="Profit Margin by Category" style="max-width:100%;">

<hr>

<h3>Top 10 Products by Total Profit</h3>

<img src="images/excel-analysis-2-top-10-products-by-profit.png" alt="Top 10 Products by Profit" style="max-width:100%;">

<hr>

<h3>Insights</h3>

<ul>
  <li><strong>Technology</strong> generates the highest revenue and profit among all categories, making it the strongest overall performer.</li>
  <li><strong>Office Supplies</strong> generates substantial revenue and maintains a strong profit margin comparable to Technology.</li>
  <li><strong>Furniture</strong> produces high revenue but significantly lower profit and profit margin, indicating weaker efficiency.</li>
  <li>Profit margins vary substantially by category:
    <ul>
      <li>Technology and Office Supplies operate near ~17% margins.</li>
      <li>Furniture operates near ~2–3%, signaling potential pricing or cost issues.</li>
    </ul>
  </li>
  <li>A small number of products account for a disproportionately large share of total profit, indicating a strong long-tail distribution of product performance.</li>
</ul>

<hr>

<h3>Business Recommendations</h3>

<ul>
  <li>Prioritize inventory availability and marketing investment for <strong>Technology</strong> and <strong>Office Supplies</strong>, as they deliver both high revenue and strong margins.</li>
  <li>Conduct a pricing, discounting, and cost analysis for <strong>Furniture</strong> to improve profitability or reconsider product assortment.</li>
  <li>Protect and monitor the <strong>top-profit products</strong> closely to avoid stockouts or supplier disruptions.</li>
  <li>Use product-level profit rankings to guide:
    <ul>
      <li>Promotional strategy</li>
      <li>Product bundling</li>
      <li>Discontinuation of consistently low-margin items</li>
    </ul>
  </li>
  <li>Introduce margin-based KPIs alongside revenue targets to avoid growth that erodes profitability.</li>
</ul>

</details>

---

<details>
  <summary><strong>Analysis 3 — Regional Performance &amp; Market Efficiency</strong></summary>

  <h3>Business Question</h3>
  <p>
    Which regions are driving the most revenue and profit, and where are we seeing efficiency gaps (low profit margin)?
    Which states and cities are the biggest profit contributors—and which locations are consistently unprofitable and may require corrective action?
  </p>

  <h3>Method</h3>
  <ul>
    <li>Used the cleaned <code>Clean_Orders</code> table as the source for all pivots.</li>
    <li>Built region-level pivots for <strong>Total Sales</strong>, <strong>Total Profit</strong>, and <strong>Profit Margin</strong> (calculated field = Profit / Sales).</li>
    <li>Created ranked pivots for <strong>Top 10</strong> and <strong>Bottom 10</strong> <strong>States</strong> and <strong>Cities</strong> by <strong>Sum of Profit</strong>.</li>
    <li>Visualized results with column and horizontal bar charts and added data labels for readability.</li>
  </ul>

  <h3>Sales Revenue by Region</h3>
  <p>
    <img src="/projects/excel-superstore-analysis/images/excel-analysis-3-sales-by-region.png"
         alt="Sales Revenue by Region"
         style="max-width:100%; height:auto; margin: 0 0 18px 0;">
  </p>

  <h3>Profit by Region</h3>
  <p>
    <img src="/projects/excel-superstore-analysis/images/excel-analysis-3-profit-by-region.png"
         alt="Profit by Region"
         style="max-width:100%; height:auto; margin: 0 0 18px 0;">
  </p>

  <h3>Profit Margin by Region</h3>
  <p>
    <img src="/projects/excel-superstore-analysis/images/excel-analysis-3-profit-margin-by-region.png"
         alt="Profit Margin by Region"
         style="max-width:100%; height:auto; margin: 0 0 18px 0;">
  </p>

  <h3>Top 10 States by Profit</h3>
  <p>
    <img src="/projects/excel-superstore-analysis/images/excel-analysis-3-top-10-states-by-profit.png"
         alt="Top 10 States by Profit"
         style="max-width:100%; height:auto; margin: 0 0 18px 0;">
  </p>

  <h3>Top 10 Cities by Profit</h3>
  <p>
    <img src="/projects/excel-superstore-analysis/images/excel-analysis-3-top-10-cities-by-profit.png"
         alt="Top 10 Cities by Profit"
         style="max-width:100%; height:auto; margin: 0 0 18px 0;">
  </p>

  <h3>Bottom 10 States by Profit</h3>
  <p>
    <img src="/projects/excel-superstore-analysis/images/excel-analysis-3-bottom-10-states-by-profit.png"
         alt="Bottom 10 States by Profit"
         style="max-width:100%; height:auto; margin: 0 0 18px 0;">
  </p>

  <h3>Bottom 10 Cities by Profit</h3>
  <p>
    <img src="/projects/excel-superstore-analysis/images/excel-analysis-3-bottom-10-cities-by-profit.png"
         alt="Bottom 10 Cities by Profit"
         style="max-width:100%; height:auto; margin: 0 0 18px 0;">
  </p>

  <h3>Insights</h3>
  <ul>
    <li>
      <strong>West and East are the growth engines.</strong> West leads both revenue (~$725K) and profit (~$108K), with East close behind (~$678K revenue; ~$91K profit). :contentReference[oaicite:1]{index=1}
    </li>
    <li>
      <strong>Efficiency gap: Central is the margin problem.</strong> Central’s profit margin is ~<strong>7.9%</strong>, roughly half of West’s ~<strong>14.9%</strong>, despite Central producing meaningful revenue (~$501K). This is a classic sign of discount/shipping/product-mix pressure. :contentReference[oaicite:2]{index=2}
    </li>
    <li>
      <strong>Profit is highly concentrated in a few states.</strong> California (~$76K) and New York (~$74K) together generate about <strong>$150K</strong> profit—roughly <strong>half of total profit</strong> in this dataset (~$286K). This makes these markets “must-protect” from stockouts, service issues, or margin erosion. :contentReference[oaicite:3]{index=3}
    </li>
    <li>
      <strong>A few cities drive outsized profitability.</strong> New York City alone contributes ~<strong>$62K</strong> profit (about <strong>one-fifth</strong> of total profit), with Los Angeles and Seattle also major contributors. These metros are strong candidates for targeted campaigns and assortment expansion. :contentReference[oaicite:4]{index=4}
    </li>
    <li>
      <strong>Losses are localized—but material.</strong> The bottom 10 states total ~<strong>-$98K</strong> profit (Texas is the biggest drag at ~<strong>-$26K</strong>). These losses partially offset gains from the top-performing states. :contentReference[oaicite:5]{index=5}
    </li>
    <li>
      <strong>City-level loss pockets point to fixable operational issues.</strong> Philadelphia (~-$14K), Houston (~-$10K), and San Antonio (~-$7K) suggest recurring patterns such as heavy discounting, high freight costs, or a low-margin category mix in specific markets. :contentReference[oaicite:6]{index=6}
    </li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>
      <strong>Defend and scale the profit core (West/East + top metros).</strong> Prioritize in-stock rates, faster fulfillment, and targeted promotions in top-profit states/cities (CA, NY; NYC, LA, Seattle) to protect the largest profit pools. :contentReference[oaicite:7]{index=7}
    </li>
    <li>
      <strong>Fix Central margin with a structured root-cause drilldown.</strong> For Central, build pivots by <em>Category → Sub-Category → Ship Mode</em> and add <em>Discount bands</em> (e.g., 0%, 1–10%, 11–20%, 21%+). Identify which combinations collapse margin and adjust pricing/discount rules accordingly. :contentReference[oaicite:8]{index=8}
    </li>
    <li>
      <strong>Implement discount guardrails tied to margin.</strong> Replace blanket discounting with rules like: “No discounts above X% on low-margin sub-categories” and “Require manager approval if projected line margin falls below a threshold.” This directly targets the gap between high revenue and low profitability. :contentReference[oaicite:9]{index=9}
    </li>
    <li>
      <strong>Create a “loss-market watchlist” and intervene systematically.</strong> Start with Texas, Ohio, Pennsylvania, Illinois, and the bottom-profit cities. For each, isolate the top 3 drivers of loss (sub-category, ship mode, discount band) and define a corrective action (pricing update, assortment change, shipping policy change). :contentReference[oaicite:10]{index=10}
    </li>
    <li>
      <strong>Reduce freight-driven losses with shipping policy tests.</strong> Test changes like: raising free-shipping thresholds, incentivizing lower-cost ship modes, or bundling orders to reduce per-order shipping cost—especially in chronic loss cities/states. :contentReference[oaicite:11]{index=11}
    </li>
    <li>
      <strong>Operationalize this into the dashboard.</strong> Add regional KPI cards (Revenue, Profit, Margin) plus a “Bottom Locations” table that updates with slicers. Track month-over-month movement so losses don’t persist unnoticed. :contentReference[oaicite:12]{index=12}
    </li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 4 — Customer Segment Analysis</strong></summary>

<p><strong>Business Question:</strong></p>
  <p>(write your question here)</p>

  <p><strong>Data &amp; Method:</strong></p>
  <p>(describe what you built in Excel: pivots, KPIs, calculated fields, slicers, charts)</p>

  <p><strong>Key Findings:</strong></p>
  <ul>
    <li>(finding 1)</li>
    <li>(finding 2)</li>
    <li>(finding 3)</li>
  </ul>

  <p><strong>Business Recommendations:</strong></p>
  <ul>
    <li>(recommendation 1)</li>
    <li>(recommendation 2)</li>
    <li>(recommendation 3)</li>
  </ul>
</details>

---

<details>
  <summary><strong>Analysis 5 — Returns Analysis &amp; Revenue Impact</strong></summary>

<p><strong>Business Question:</strong></p>
  <p>(write your question here)</p>

  <p><strong>Data &amp; Method:</strong></p>
  <p>(describe what you built in Excel: pivots, KPIs, calculated fields, slicers, charts)</p>

  <p><strong>Key Findings:</strong></p>
  <ul>
    <li>(finding 1)</li>
    <li>(finding 2)</li>
    <li>(finding 3)</li>
  </ul>

  <p><strong>Business Recommendations:</strong></p>
  <ul>
    <li>(recommendation 1)</li>
    <li>(recommendation 2)</li>
    <li>(recommendation 3)</li>
  </ul>
</details>

---

<details>
  <summary><strong>Project Implementation &amp; Deliverables</strong></summary>

  <h2>Workbook Structure</h2>
  <ul>
    <li>Raw Data (original import)</li>
    <li>Power Query (cleaning steps)</li>
    <li>Analysis Table (final cleaned table)</li>
    <li>Pivot Tables (model + calculations)</li>
    <li>Dashboard (final presentation)</li>
  </ul>

  <hr>

  <h2>Dashboard Features</h2>
  <ul>
    <li>Interactive slicers for region, category, and time</li>
    <li>KPI summary cards</li>
    <li>Trend visualizations</li>
    <li>Top / bottom product rankings</li>
    <li>Dynamic filtering across all charts</li>
  </ul>

  <hr>

  <h2>Final Dashboard</h2>
  <p>(Screenshot will be added here)</p>

  <hr>

  <h2>Project Deliverables</h2>
  <ul>
    <li>Fully interactive Excel dashboard workbook</li>
    <li>Cleaned analysis-ready dataset</li>
    <li>SQL-style business question documentation</li>
  </ul>

  <hr>

  <h2>Files</h2>
  <ul>
    <li>Raw dataset</li>
    <li>Cleaned dataset</li>
    <li>Excel workbook</li>
  </ul>

  <hr>

  <h2>Conclusion</h2>
  <p>(Concluding statements)</p>

</details>
