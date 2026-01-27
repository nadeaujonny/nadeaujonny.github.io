---
layout: default
title: Sales Dashboard – Superstore Dataset (Excel)
---

<a href="/projects" class="back-btn">← Back to Projects</a>

# Sales Dashboard – Superstore Dataset (Excel)

> An end-to-end Excel analytics project demonstrating Power Query data cleaning, KPI development, pivot-table analysis, and executive dashboard design using the Superstore retail dataset.

---

<details>
  <summary><strong>Project Overview</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Overview</h3>
  <p>
    This project analyzes Superstore retail sales data in Microsoft Excel to uncover trends in revenue, profit,
    customer segments, regional performance, and return impact. The goal is to demonstrate practical Excel analytics
    skills used in business environments: Power Query (ETL), pivot-driven analysis, KPI modeling, and dashboard design.
  </p>

  <h3>Business Context</h3>
  <p>
    This analysis simulates a retail company evaluating sales performance, profitability, customer behavior, and
    operational efficiency to support data-driven decision making by executives and category managers.
  </p>

  <h3>Objectives</h3>
  <ul>
    <li>Define and calculate core KPIs: revenue, profit, profit margin, units sold, and return rate</li>
    <li>Clean and standardize raw orders using Power Query (data types, text cleanup, de-duplication, derived date fields)</li>
    <li>Analyze performance using pivot tables and calculated fields (time trends, product mix, regional efficiency, segments, returns)</li>
    <li>Build an executive-style dashboard with connected slicers for interactive exploration</li>
  </ul>

  <h3>Dataset Overview</h3>
  <ul>
    <li><strong>Dataset:</strong> Superstore (public retail sample dataset)</li>
    <li><strong>Time range:</strong> 2014–2017</li>
    <li><strong>Granularity:</strong> One row per order line item</li>
    <li><strong>Core tables:</strong> Orders, Returns</li>
  </ul>

  <h3>Tools &amp; Skills Demonstrated</h3>
  <ul>
    <li><strong>Power Query:</strong> ETL, data types, text cleanup, de-duplication, derived date fields</li>
    <li><strong>Pivot Tables:</strong> grouping, sorting, filters, calculated fields</li>
    <li><strong>KPI Modeling:</strong> profit margin, return rate, performance comparisons</li>
    <li><strong>Excel Functions:</strong> XLOOKUP, SUMIFS/COUNTIFS, IF/IFERROR, date &amp; text functions</li>
    <li><strong>Visualization:</strong> pivot charts, conditional formatting, slicers, dashboard layout</li>
  </ul>

  <h3>KPI Definitions</h3>
  <ul>
    <li><strong>Revenue:</strong> SUM(Sales)</li>
    <li><strong>Profit:</strong> SUM(Profit)</li>
    <li><strong>Profit Margin:</strong> Profit / Revenue</li>
    <li><strong>Units Sold:</strong> SUM(Quantity)</li>
    <li><strong>Return Rate:</strong> Returned Sales / Total Sales (sales-based return rate)</li>
  </ul>

</details>

---

<details>
  <summary><strong>Data Preparation (Power Query / ETL)</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <p>
    Before building KPIs, pivot tables, and charts, I cleaned and standardized the Superstore Orders dataset using
    <strong>Excel Power Query</strong>. The goal was to create a reliable, refreshable table (<code>Clean_Orders</code>)
    that serves as the single source of truth for all downstream analysis and dashboarding.
  </p>

  <h3>ETL Summary</h3>
  <ul>
    <li><strong>Input:</strong> Raw Orders data (<code>.xls</code>) preserved as <code>Raw_Orders</code> (no manual edits)</li>
    <li><strong>Tool:</strong> Excel Power Query (Get &amp; Transform)</li>
    <li><strong>Output:</strong> Cleaned dataset loaded to <code>Clean_Orders</code> (used by all pivots, charts, and KPIs)</li>
    <li><strong>Refreshable:</strong> Can update via <em>Data → Refresh All</em> without redoing manual steps</li>
  </ul>

  <h3>Power Query Applied Steps (Evidence)</h3>
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/excel-data-prep-power-query.png"
      alt="Power Query Editor showing Applied Steps for Superstore data preparation"
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
      <strong>Import &amp; preserve raw data</strong>
      <ul>
        <li>Imported raw Superstore Orders and preserved the original table unchanged.</li>
      </ul>
    </li>
    <li>
      <strong>Standardize data types</strong>
      <ul>
        <li>Converted <code>Order Date</code> and <code>Ship Date</code> to Date-only values.</li>
        <li>Set <code>Postal Code</code> to Text to preserve leading zeros.</li>
        <li>Validated numeric fields (<code>Sales</code>, <code>Profit</code>, <code>Discount</code>, <code>Quantity</code>) as numeric types.</li>
      </ul>
    </li>
    <li>
      <strong>Clean text columns</strong>
      <ul>
        <li>Trimmed whitespace and removed non-printable characters across key text fields.</li>
        <li>Improved pivot grouping stability (e.g., prevents “duplicate labels” caused by trailing spaces).</li>
      </ul>
    </li>
    <li>
      <strong>Remove invalid / blank records</strong>
      <ul>
        <li>Removed blank rows and incomplete records that could distort totals and trends.</li>
      </ul>
    </li>
    <li>
      <strong>Remove duplicates</strong>
      <ul>
        <li>Removed duplicates using a composite key: <code>Order ID + Product ID</code>.</li>
        <li>Ensured each row represents a unique order line item (avoids double counting).</li>
      </ul>
    </li>
    <li>
      <strong>Create derived time fields</strong>
      <ul>
        <li>Created <code>Order Year</code>, <code>Order Month</code>, and <code>Order Year-Month</code> (YYYY-MM) for consistent time-series reporting.</li>
      </ul>
    </li>
    <li>
      <strong>Load to <code>Clean_Orders</code></strong>
      <ul>
        <li>Loaded the final cleaned table to Excel for analysis, pivots, and dashboarding.</li>
      </ul>
    </li>
  </ol>

  <h3>Why This Matters</h3>
  <ul>
    <li><strong>Accuracy:</strong> prevents inflated KPIs due to duplicates and invalid records</li>
    <li><strong>Consistency:</strong> stable grouping and filtering in pivots (clean types + clean text)</li>
    <li><strong>Repeatability:</strong> refreshable pipeline for maintainable analytics workflows</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 1 — Sales &amp; Profit Trends Over Time</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>
    How have sales and profitability evolved over time from 2014 to 2017? Are there trends, seasonality,
    or periods of volatility that could inform forecasting, inventory planning, and cost control?
  </p>

  <h3>Method</h3>
  <ul>
    <li>Used <code>Clean_Orders</code> as the data source.</li>
    <li>Built pivot tables grouped by <code>Order Year-Month</code>.</li>
    <li>Created line charts for monthly revenue and monthly profit.</li>
    <li>Reviewed overall KPIs to contextualize the trends.</li>
  </ul>

  <h3>Results</h3>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/excel-analysis-1-kpi-summary.png"
      alt="KPI summary for Superstore (revenue, profit, profit margin, orders, units sold, average order value)"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Overall KPI summary used to contextualize trend performance.
      <span style="display:block; margin-top:4px;">
        <a href="images/excel-analysis-1-kpi-summary.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/excel-analysis-1-monthly-sales.png"
      alt="Monthly sales (revenue) trend from 2014 to 2017"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Monthly revenue trend grouped by Year–Month.
      <span style="display:block; margin-top:4px;">
        <a href="images/excel-analysis-1-monthly-sales.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/excel-analysis-1-monthly-profit.png"
      alt="Monthly profit trend from 2014 to 2017"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Monthly profit trend highlighting volatility and negative-profit periods.
      <span style="display:block; margin-top:4px;">
        <a href="images/excel-analysis-1-monthly-profit.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>Revenue grows over time:</strong> sales show a clear upward trajectory across the 2014–2017 period.</li>
    <li><strong>Seasonality appears consistent:</strong> recurring peaks suggest predictable high-demand periods that can be planned for.</li>
    <li><strong>Profit is more volatile than revenue:</strong> there are sharper swings in profit, including negative months.</li>
    <li><strong>Margin pressure exists in specific periods:</strong> revenue growth does not always translate proportionally into profit growth.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Plan for seasonal demand:</strong> improve inventory coverage and fulfillment capacity ahead of predictable peaks.</li>
    <li><strong>Drill into negative-profit months:</strong> break down by Sub-Category, Discount band, and Ship Mode to identify the primary margin drivers.</li>
    <li><strong>Set discount guardrails:</strong> implement policies that prevent heavy discounting on low-margin items without approvals.</li>
    <li><strong>Monitor profit margin monthly:</strong> track margin alongside revenue so growth doesn’t hide profitability deterioration.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 2 — Product &amp; Category Performance</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>
    Which categories and products contribute the most to revenue and profit? Where do profitability differences
    suggest pricing, discounting, inventory, or product strategy changes?
  </p>

  <h3>Method</h3>
  <ul>
    <li>Used <code>Clean_Orders</code> as the data source.</li>
    <li>Built category pivots for Revenue, Profit, and Profit Margin (Profit / Sales).</li>
    <li>Built a product pivot sorted by Profit (descending) to identify top profit contributors.</li>
    <li>Created pivot charts with labels for fast comparison.</li>
  </ul>

  <h3>Category KPI Summary</h3>
  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin-bottom: 18px;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Category</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Revenue</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Profit</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Profit Margin</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Technology</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">$835,759.74</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">$145,386.13</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">17.4%</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Office Supplies</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">$718,317.79</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">$122,247.40</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">17.0%</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Furniture</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">$741,432.04</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">$18,380.28</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">2.5%</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; font-weight:700;">Total</td>
        <td style="padding: 8px 6px; text-align:right; font-weight:700;">$2,295,509.57</td>
        <td style="padding: 8px 6px; text-align:right; font-weight:700;">$286,013.82</td>
        <td style="padding: 8px 6px; text-align:right; font-weight:700;">12.5%</td>
      </tr>
    </tbody>
  </table>

  <h3>Results (Charts)</h3>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/excel-analysis-2-sales-revenue-by-category.png"
      alt="Sales revenue by category"
      loading="lazy"
      style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;"
    >
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Revenue by category.
      <span style="display:block; margin-top:4px;">
        <a href="images/excel-analysis-2-sales-revenue-by-category.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/excel-analysis-2-profit-by-category.png"
      alt="Profit by category"
      loading="lazy"
      style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;"
    >
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Profit by category (profit is concentrated in Technology and Office Supplies).
      <span style="display:block; margin-top:4px;">
        <a href="images/excel-analysis-2-profit-by-category.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/excel-analysis-2-profit-margin-by-category.png"
      alt="Profit margin by category"
      loading="lazy"
      style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;"
    >
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Profit margin by category (Furniture is a low-margin outlier).
      <span style="display:block; margin-top:4px;">
        <a href="images/excel-analysis-2-profit-margin-by-category.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/excel-analysis-2-top-10-products-by-profit.png"
      alt="Top 10 products by profit"
      loading="lazy"
      style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;"
    >
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Top 10 products by total profit.
      <span style="display:block; margin-top:4px;">
        <a href="images/excel-analysis-2-top-10-products-by-profit.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>Technology and Office Supplies drive most profit:</strong> both categories have strong margins (~17%) and dominate total profit contribution.</li>
    <li><strong>Furniture is the efficiency problem:</strong> high revenue but very low profit margin (~2.5%), suggesting discounting, shipping, or product mix issues.</li>
    <li><strong>Profit is concentrated:</strong> the business is dependent on a small set of high-profit products and categories—great for focus, but a concentration risk.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Scale and protect the profit core:</strong> prioritize in-stock rates and margin discipline in Technology and Office Supplies.</li>
    <li><strong>Fix Furniture with a drilldown:</strong> analyze Furniture by Sub-Category × Discount band × Ship Mode to identify margin killers.</li>
    <li><strong>Implement discount guardrails:</strong> tie discounting to expected margin thresholds, especially in low-margin categories.</li>
    <li><strong>Protect top-profit SKUs:</strong> monitor stockouts and lead times for the highest-profit products.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 3 — Regional Performance &amp; Market Efficiency</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>
    Which regions are driving the most profit and where are we seeing efficiency gaps (low profit margin)?
    Which states and cities are the largest profit contributors—and which locations are consistently unprofitable?
  </p>

  <h3>Method</h3>
  <ul>
    <li>Used <code>Clean_Orders</code> as the source for all pivots.</li>
    <li>Built region pivots for Revenue, Profit, and Profit Margin (Profit / Sales).</li>
    <li>Ranked Top 10 and Bottom 10 States and Cities by Profit.</li>
    <li>Visualized results using pivot charts with labels for readability.</li>
  </ul>

  <h3>Results (Charts)</h3>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-3-sales-by-region.png" alt="Sales revenue by region" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Revenue by region.
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-3-sales-by-region.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-3-profit-by-region.png" alt="Profit by region" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Profit by region.
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-3-profit-by-region.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-3-profit-margin-by-region.png" alt="Profit margin by region" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Profit margin (efficiency) by region.
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-3-profit-margin-by-region.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-3-top-10-states-by-profit.png" alt="Top 10 states by profit" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Top 10 states by profit.
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-3-top-10-states-by-profit.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-3-top-10-cities-by-profit.png" alt="Top 10 cities by profit" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Top 10 cities by profit.
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-3-top-10-cities-by-profit.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-3-bottom-10-states-by-profit.png" alt="Bottom 10 states by profit" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Bottom 10 states by profit (loss markets).
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-3-bottom-10-states-by-profit.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-3-bottom-10-cities-by-profit.png" alt="Bottom 10 cities by profit" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Bottom 10 cities by profit (loss pockets).
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-3-bottom-10-cities-by-profit.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>Profit and efficiency vary by region:</strong> some regions combine strong revenue with strong profitability, while others show margin pressure.</li>
    <li><strong>Profit concentration is real:</strong> a small number of states and cities account for a large share of profit.</li>
    <li><strong>Losses are localized but meaningful:</strong> bottom states/cities can offset gains if the drivers aren’t addressed.</li>
    <li><strong>Regional inefficiency is often fixable:</strong> discounting, shipping mode, and product mix are common controllable drivers.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Defend the profit core:</strong> prioritize service levels and margin discipline in top-profit states/cities to protect the biggest profit pools.</li>
    <li><strong>Run a margin root-cause drilldown in weaker regions:</strong> analyze by Category → Sub-Category → Ship Mode and add Discount bands to isolate margin killers.</li>
    <li><strong>Create a “loss-market watchlist”:</strong> for bottom locations, identify the top 3 loss drivers and apply targeted corrective actions (pricing, discount rules, shipping policy, assortment changes).</li>
    <li><strong>Operationalize location KPIs:</strong> add regional margin monitoring to the dashboard to prevent persistent losses from being overlooked.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 4 — Customer Segment Analysis</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>
    Which customer segments drive the most revenue and profit, and which segments are the most efficient (highest profit margin)?
    How should the business prioritize growth, pricing, and retention across Consumer, Corporate, and Home Office?
  </p>

  <h3>Method</h3>
  <ul>
    <li>Used <code>Clean_Orders</code> as the data source.</li>
    <li>Built a pivot grouped by <strong>Segment</strong> for Sales, Profit, and Profit Margin.</li>
    <li>Created charts for Sales, Profit, and Profit Margin to compare segment performance.</li>
  </ul>

  <h3>Results (Charts)</h3>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-4-segment-summary.png" alt="Segment summary table (Sales, Profit, Profit Margin)" loading="lazy"
         style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;">
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Segment summary KPI table.
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-4-segment-summary.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-4-sales-by-segment.png" alt="Sales revenue by customer segment" loading="lazy"
         style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;">
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Sales by segment.
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-4-sales-by-segment.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-4-profit-by-segment.png" alt="Profit by customer segment" loading="lazy"
         style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;">
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Profit by segment.
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-4-profit-by-segment.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-4-profit-margin-by-segment.png" alt="Profit margin by customer segment" loading="lazy"
         style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;">
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Profit margin (efficiency) by segment.
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-4-profit-margin-by-segment.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>Consumer drives scale:</strong> Sales <strong>$1,161,012.63</strong>, Profit <strong>$134,022.09</strong>, Margin <strong>11.5%</strong>.</li>
    <li><strong>Corporate is strong and efficient:</strong> Sales <strong>$705,601.99</strong>, Profit <strong>$91,821.26</strong>, Margin <strong>13.0%</strong>.</li>
    <li><strong>Home Office is most efficient:</strong> Sales <strong>$428,894.96</strong>, Profit <strong>$60,170.47</strong>, Margin <strong>14.0%</strong>.</li>
    <li><strong>Overall:</strong> Total Sales <strong>$2,295,509.57</strong>, Total Profit <strong>$286,013.82</strong>, Margin <strong>12.5%</strong>.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Improve Consumer margin without sacrificing volume:</strong> analyze Consumer by Discount band and Ship Mode to identify margin erosion and set guardrails.</li>
    <li><strong>Scale Home Office profitably:</strong> invest in targeted campaigns and bundles to grow the highest-margin segment.</li>
    <li><strong>Expand Corporate through repeatable programs:</strong> focus on retention and upsell with contract-style offers (bulk tiers, replenishment programs).</li>
    <li><strong>Monitor segment KPIs monthly:</strong> track Sales, Profit, and Margin by segment so efficiency doesn’t deteriorate unnoticed.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 5 — Returns Analysis &amp; Revenue Impact</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <ul>
    <li>How much revenue and profit are impacted by returns?</li>
    <li>Which sub-categories have the highest return rates (sales-based)?</li>
    <li>Which products drive the greatest return impact by sales and profit?</li>
  </ul>

  <h3>Method</h3>
  <ul>
    <li>Created a return flag by joining Orders to Returns using <strong>Order ID</strong>.</li>
    <li>Built pivots for Returned vs Not Returned (Sales, Profit, return %).</li>
    <li>Built return-rate pivots by Month and Sub-Category.</li>
    <li>Ranked products by Returned Sales and Returned Profit impact.</li>
  </ul>

  <h3>Results (Charts)</h3>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-5-returns-kpi-summary.png" alt="Returns KPI summary (returned vs non-returned sales and profit)" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Returns KPI summary (returned vs not returned).
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-5-returns-kpi-summary.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-5-returns-sales-rate-by-month-year.png" alt="Monthly return rate (sales %) over time" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Monthly return rate trend (sales-based).
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-5-returns-sales-rate-by-month-year.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-5-returns-sales-rate-by-sub-category.png" alt="Return rate (sales %) by sub-category" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Return rate by sub-category (sales-based).
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-5-returns-sales-rate-by-sub-category.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-5-top-10-products-by-return-sales.png" alt="Top 10 products by returned sales" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Top products by returned sales ($).
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-5-top-10-products-by-return-sales.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img src="images/excel-analysis-5-top-10-products-by-return-profit.png" alt="Top 10 products by returned profit impact" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Top products by returned profit impact ($).
      <span style="display:block; margin-top:4px;"><a href="images/excel-analysis-5-top-10-products-by-return-profit.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>Total Sales:</strong> $2,295,509.57 &nbsp;|&nbsp; <strong>Total Profit:</strong> $286,013.82</li>
    <li><strong>Returned Sales:</strong> $180,504.28 (<strong>7.86%</strong> of total sales)</li>
    <li><strong>Returned Profit impact:</strong> $23,232.36 (<strong>8.12%</strong> of total profit)</li>
    <li><strong>Net after excluding returns:</strong> $2,115,005.29 sales and $262,781.46 profit</li>
    <li><strong>Highest return-rate sub-categories (sales %):</strong> Copiers (12.84%), Furnishings (10.48%), Appliances (9.42%), Paper (9.11%), Phones (8.37%)</li>
    <li><strong>Lowest observed return rate:</strong> Binders (4.91%)</li>
    <li><strong>Return impact is concentrated:</strong> a small number of high-dollar products drive a large share of returned sales and returned profit impact.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Prioritize high-return sub-categories:</strong> start with Copiers and Furnishings—improve product guidance, QA, and packaging to reduce defects/damage.</li>
    <li><strong>Investigate spike months:</strong> filter high-return periods by Discount band, Ship Mode, Region, and Product to identify root causes.</li>
    <li><strong>Target high-impact SKUs:</strong> implement product-level actions (vendor review, listing clarity, fulfillment checks, exchange/repair options).</li>
    <li><strong>Tighten discounting where returns are high:</strong> if high discounts correlate with high returns or negative profitability, apply stricter approval thresholds.</li>
    <li><strong>Operationalize return KPIs:</strong> track Returned Sales, Returned Profit impact, and Return Rate in the dashboard with slicers for time and category.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Project Implementation &amp; Deliverables</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Workbook Structure</h3>
  <ul>
    <li><strong>Raw_Orders</strong> — Original imported dataset (preserved; no manual edits)</li>
    <li><strong>Clean_Orders</strong> — Power Query cleaned, analysis-ready table (single source of truth)</li>
    <li><strong>Returns</strong> — Returned orders reference table</li>
    <li><strong>People</strong> — Region/manager reference table</li>
    <li><strong>Pivots</strong> — Pivot tables + pivot charts used for analysis and the dashboard</li>
    <li><strong>Dashboard</strong> — Final profit-oriented, single-screen interactive dashboard</li>
  </ul>

  <hr>

  <h3>Dashboard Features</h3>
  <ul>
    <li><strong>Profit-oriented, single-screen layout</strong> designed for clean portfolio screenshots</li>
    <li><strong>Connected slicers</strong> for <em>Order Year</em> and <em>Order Month</em> that filter every chart</li>
    <li><strong>Core visuals:</strong> Monthly Profit Trend, Return Profit Impact, Top Profit Sub-Categories, Top Profit States, Segment Profit</li>
  </ul>

  <hr>

  <h3>Final Dashboard</h3>
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/excel-project-profit-oriented-dashboard.png"
      alt="Excel Superstore profit-oriented dashboard (single-screen layout with slicers)"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Final profit-oriented dashboard with fully connected slicers.
      <span style="display:block; margin-top:4px;">
        <a href="images/excel-project-profit-oriented-dashboard.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Downloads</h3>
  <ul>
    <li>
      <strong>Excel Workbook:</strong>
      <a href="workbook/Superstore_Portfolio_Excel_Project.xlsx" target="_blank" rel="noopener">
        Download Superstore_Portfolio_Excel_Project.xlsx
      </a>
      <br>
      <em>Best viewed in Microsoft Excel (desktop) to use slicers and full interactivity.</em>
    </li>
    <li>
      <strong>Raw Dataset:</strong>
      <a href="data/superstore_raw.xls" target="_blank" rel="noopener">
        Download superstore_raw.xls
      </a>
    </li>
  </ul>

  <hr>

  <h3>Conclusion</h3>
  <p>
    This project demonstrates an end-to-end Excel analytics workflow: importing raw retail data, transforming it with
    Power Query, building pivot-driven analysis, and delivering a polished, interactive dashboard optimized for
    stakeholder reporting. The final dashboard supports fast profit-based exploration by time and surfaces key
    profitability drivers (category mix, region performance, segment efficiency) along with the revenue/profit impact
    of returns.
  </p>

</details>
