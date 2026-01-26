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

  <h2>Overview</h2>
  <p>
    This project analyzes retail sales data using Microsoft Excel to uncover trends in revenue, profit, customer segments, and regional performance.
    The goal is to demonstrate real-world Excel analytics skills used in business environments.
  </p>

  <hr>

  <h2>Business Context</h2>
  <p>
    This analysis simulates a retail company evaluating sales performance, profitability, customer behavior, and operational efficiency
    to support data-driven decision making by executives and category managers.
  </p>

  <hr>

  <h2>Objectives</h2>
  <ul>
    <li>Build and calculate key business KPIs (revenue, profit, profit margin, units sold, return rate)</li>
    <li>Clean and transform raw data using Power Query</li>
    <li>Perform analysis using pivot tables and calculated fields</li>
    <li>Design an interactive executive-style dashboard</li>
  </ul>

  <hr>

  <h2>Dataset Overview</h2>
  <p>
    The Superstore dataset is a public retail transaction dataset commonly used for analytics and business intelligence practice.
    It represents order-level sales data for a fictional office supply retailer.
  </p>

  <p><strong>Key tables / structure:</strong></p>
  <ul>
    <li>Orders (order date, ship date, customer, segment, region, product, category, sales, profit, quantity)</li>
    <li>Returns (returned flag by order ID)</li>
  </ul>

  <p>
    <strong>Time range:</strong> 2014–2017<br>
    <strong>Granularity:</strong> One row per order line item<br>
    <strong>Records:</strong> ~10,000 rows
  </p>

  <p><strong>Key dimensions:</strong></p>
  <ul>
    <li>Customer segment</li>
    <li>Product category & sub-category</li>
    <li>Region, state, city</li>
    <li>Order & ship dates</li>
  </ul>

  <p><strong>Key measures:</strong></p>
  <ul>
    <li>Sales (revenue)</li>
    <li>Profit</li>
    <li>Quantity</li>
  </ul>

  <p><strong>Limitations:</strong></p>
  <ul>
    <li>Fictional data (not from a real company)</li>
    <li>No marketing or acquisition channel data</li>
    <li>Limited customer demographics</li>
    <li>Returns data may be incomplete depending on version</li>
  </ul>

  <hr>

  <h2>Tools & Skills Demonstrated</h2>

  <p><strong>Data Preparation</strong></p>
  <ul>
    <li>Power Query</li>
    <li>Data validation & normalization</li>
  </ul>

  <p><strong>Analysis</strong></p>
  <ul>
    <li>Pivot tables</li>
    <li>Calculated fields</li>
    <li>KPI modeling</li>
  </ul>

  <p><strong>Excel Functions</strong></p>
  <ul>
    <li>XLOOKUP</li>
    <li>SUMIFS / COUNTIFS</li>
    <li>IF / IFERROR</li>
    <li>Date & text functions</li>
  </ul>

  <p><strong>Visualization</strong></p>
  <ul>
    <li>Pivot charts</li>
    <li>Conditional formatting</li>
    <li>Slicers & timelines</li>
    <li>Dashboard layout design</li>
  </ul>

  <hr>

  <h2>KPI Definitions</h2>
  <ul>
    <li><strong>Revenue</strong> = SUM(Sales)</li>
    <li><strong>Profit</strong> = SUM(Profit)</li>
    <li><strong>Profit Margin</strong> = Profit / Revenue</li>
    <li><strong>Units Sold</strong> = SUM(Quantity)</li>
    <li><strong>Return Rate</strong> = # Returned Orders / # Total Orders</li>
  </ul>

  <hr>

  <h2>Data Preparation</h2>
  <ul>
    <li>Removed duplicates and invalid records</li>
    <li>Standardized date formats and categories</li>
    <li>Created calculated columns for profit margin and return flags</li>
    <li>Built a clean analysis table using Power Query</li>
  </ul>

</details>

---

<section id="data-preparation">
  <details>
    <summary><strong>Data Preparation</strong></summary>

    <p>
      Before building KPIs, pivot tables, and charts, I cleaned and standardized the Superstore Orders dataset using
      <strong>Excel Power Query</strong>. The goal was to create a reliable, refreshable table (<code>Clean_Orders</code>)
      that serves as the single source of truth for all downstream analysis and dashboarding.
    </p>

    <h3>Overview</h3>
    <ul>
      <li><strong>Input:</strong> Raw Superstore Orders data (<code>.xls</code>) preserved as <code>Raw_Orders</code> (no manual edits).</li>
      <li><strong>Tool:</strong> Excel Power Query (Get &amp; Transform).</li>
      <li><strong>Output:</strong> Cleaned dataset loaded into <code>Clean_Orders</code>.</li>
      <li><strong>Why Power Query:</strong> Transformations are documented, repeatable, and can be refreshed as the dataset changes.</li>
    </ul>

    <h3>Power Query Applied Steps (Evidence)</h3>
    <p>
      The screenshot below shows the Power Query Editor with the <em>Applied Steps</em> panel, documenting the full
      cleaning pipeline from raw input to cleaned output.
    </p>
    <figure style="margin: 0;">
      <img
        src="images/excel-data-prep-power-query.png"
        alt="Power Query Applied Steps for Superstore data preparation"
        style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
      >
      <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
        Power Query: applied transformations used to produce <code>Clean_Orders</code>.
      </figcaption>
    </figure>

    <h3>Cleaning &amp; Transformation Steps</h3>

    <h4>1) Import &amp; Preserve Raw Data</h4>
    <ul>
      <li>Imported the raw Orders dataset into Power Query Editor.</li>
      <li>Kept the original table (<code>Raw_Orders</code>) untouched to preserve a clean baseline and ensure traceability.</li>
    </ul>

    <h4>2) Standardize Column Data Types</h4>
    <ul>
      <li>Validated column types to prevent incorrect aggregations and grouping issues in pivot tables.</li>
      <li>Converted <code>Order Date</code> and <code>Ship Date</code> from DateTime to <strong>Date</strong> (date-only values) for consistent time-based analysis.</li>
      <li>Set <code>Postal Code</code> to <strong>Text</strong> to preserve leading zeros and avoid formatting issues.</li>
      <li>Ensured numeric fields (e.g., <code>Sales</code>, <code>Profit</code>, <code>Discount</code>, <code>Quantity</code>) were stored as appropriate numeric types.</li>
      <li>Ensured IDs and dimension fields (Order/Customer/Product IDs and categorical columns) were treated as text for stable filtering and grouping.</li>
    </ul>

    <h4>3) Clean Text Fields</h4>
    <ul>
      <li>Trimmed whitespace and removed non-printing characters across key text columns.</li>
      <li>Improved consistency for customer/product names and category/geographic fields to reduce duplicate-looking labels in pivots.</li>
    </ul>

    <h4>4) Remove Blank / Invalid Rows</h4>
    <ul>
      <li>Removed blank rows and incomplete records that could create noise or inaccuracies in summaries and visualizations.</li>
    </ul>

    <h4>5) Remove Duplicate Records</h4>
    <ul>
      <li>De-duplicated records using a composite key:</li>
      <ul>
        <li><code>Order ID + Product ID</code></li>
      </ul>
      <li>This ensured each row in <code>Clean_Orders</code> represents a unique product line within an order.</li>
    </ul>

    <h4>6) Create Derived Time Fields</h4>
    <ul>
      <li>Created additional time fields to support consistent monthly trending and pivot grouping:</li>
      <ul>
        <li><code>Order Year</code></li>
        <li><code>Order Month</code></li>
        <li><code>Order Year-Month</code> (formatted as <code>YYYY-MM</code>)</li>
      </ul>
    </ul>

    <h4>7) Load Clean Output to <code>Clean_Orders</code></h4>
    <ul>
      <li>Loaded the transformed dataset into the workbook as <code>Clean_Orders</code>.</li>
      <li>Used <code>Clean_Orders</code> as the source for all KPI calculations, pivot tables, charts, and the dashboard.</li>
    </ul>

  </details>
</section>

---

<details>
  <summary><strong>Analysis 1 — Sales &amp; Profit Trends Over Time</strong></summary>

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
  <summary><strong>Analysis 2 — Product &amp; Category Performance</strong></summary>

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
  <summary><strong>Analysis 3 — Regional Performance &amp; Market Efficiency</strong></summary>

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
