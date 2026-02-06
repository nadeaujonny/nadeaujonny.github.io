---
layout: default
title: Healthcare Analytics Dashboard (Power BI)
description: "A comprehensive Power BI healthcare analytics dashboard showcasing advanced DAX, Power Query, data modeling, and executive-level insights."
breadcrumbs:
  - title: Projects
    url: /projects/
  - title: Healthcare Analytics Dashboard (Power BI)
---

<a href="/projects/" class="back-to-projects btn">← Back to Projects</a>

# Healthcare Analytics Dashboard (Power BI)

> A Power BI portfolio project analyzing CDC chronic disease indicators to surface trends, geographic hotspots, and demographic disparities that inform healthcare resource planning.

---

<details>
  <summary><strong>Project Overview</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Overview</h3>
  <p>
    This project showcases end-to-end Power BI workflow by transforming CDC Chronic Disease Indicators (CDI) data into a
    stakeholder-ready healthcare analytics dashboard. The report focuses on national trends, state-by-state performance,
    and health equity gaps to support evidence-based prioritization.
  </p>

  <h3>Business Context</h3>
  <p>
    Public health teams need clear visibility into which chronic conditions are worsening, which states face the highest
    burden, and where disparities are most pronounced. This dashboard simulates a public health analytics engagement
    supporting program funding, outreach planning, and policy targeting.
  </p>

  <h3>Objectives</h3>
  <ul>
    <li>Deliver an executive overview of chronic disease trends and burden drivers</li>
    <li>Rank states by outcome severity and highlight geographic clusters</li>
    <li>Quantify disparities across age, sex, and race/ethnicity groups</li>
    <li>Demonstrate Power BI skills: Power Query, data modeling, DAX, and report design</li>
  </ul>

  <h3>Tools &amp; Skills Demonstrated</h3>
  <ul>
    <li><strong>Power BI Desktop:</strong> data modeling, relationships, report design, and interactivity</li>
    <li><strong>Power Query:</strong> data cleaning, filtering, and dimensional table creation</li>
    <li><strong>DAX:</strong> time intelligence, rankings, variance calculations, and KPI definitions</li>
    <li><strong>Visualization:</strong> KPI cards, line charts, maps, matrices, and drill-through views</li>
  </ul>
</details>

---

<details>
  <summary><strong>Data</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Dataset Overview</h3>
  <ul>
    <li><strong>Source:</strong> CDC Open Data – U.S. Chronic Disease Indicators (CDI)</li>
    <li><strong>Format:</strong> CSV extract (long/tidy format, one row per metric observation)</li>
    <li><strong>Granularity:</strong> Year × State × Indicator × Stratification</li>
    <li><strong>Metric:</strong> DataValue (rate, percentage, or count depending on indicator)</li>
  </ul>

  <h3>Scope</h3>
  <ul>
    <li><strong>Time range:</strong> Most recent 8–12 years available for selected indicators</li>
    <li><strong>Indicators:</strong> Core outcomes (e.g., diabetes, heart disease) + risk factors (e.g., obesity, smoking)</li>
    <li><strong>Geography:</strong> U.S. states and D.C. (territories excluded for consistency)</li>
  </ul>

  <h3>Key Fields Used</h3>
  <ul>
    <li><strong>Year:</strong> reporting period</li>
    <li><strong>Location:</strong> state name and abbreviation</li>
    <li><strong>Indicator:</strong> condition or risk factor being measured</li>
    <li><strong>Stratification:</strong> overall, age group, sex, or race/ethnicity</li>
    <li><strong>DataValue:</strong> metric value used in KPIs and comparisons</li>
  </ul>
</details>

---

<details>
  <summary><strong>Methodology</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Power Query (ETL)</h3>
  <ul>
    <li>Imported the raw CDI CSV and standardized data types (Year, DataValue).</li>
    <li>Filtered to selected indicators, years, and U.S. states only.</li>
    <li>Created dimension tables for Location, Indicator, Stratification, and Date.</li>
    <li>Built a clean fact table (Fact_CDI) with keys + metric fields only.</li>
  </ul>

  <h3>Data Model</h3>
  <ul>
    <li>Star schema with Fact_CDI at the center.</li>
    <li>Dimensions: Dim_Date, Dim_Location, Dim_Indicator, Dim_Stratification.</li>
    <li>Single-direction relationships for consistent filter context across visuals.</li>
  </ul>

  <h3>DAX Measures (Examples)</h3>
  <ul>
    <li><strong>Selected Value:</strong> AVG of DataValue for current filter context.</li>
    <li><strong>YoY Change:</strong> Current Value – Prior Year Value.</li>
    <li><strong>YoY % Change:</strong> (Current – Prior) / Prior.</li>
    <li><strong>State Rank:</strong> RANKX over states for the selected indicator.</li>
    <li><strong>Disparity Gap:</strong> MAX group value – MIN group value within a state.</li>
  </ul>

  <h3>Report Design</h3>
  <ul>
    <li><strong>Executive Overview:</strong> KPI cards, national trend line, and top/bottom states.</li>
    <li><strong>Trends &amp; Drivers:</strong> indicator comparisons and YoY variance.</li>
    <li><strong>Geographic Deep Dive:</strong> state profiles with ranked indicators.</li>
    <li><strong>Equity Focus:</strong> disparity metrics by demographic stratification.</li>
  </ul>
</details>

---

<details>
  <summary><strong>Analysis 1 — National Trends &amp; KPI Overview</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>Which chronic disease indicators are improving or worsening at the national level?</p>

  <h3>Method</h3>
  <ul>
    <li>Filtered to overall (non-stratified) rows for clean national comparisons.</li>
    <li>Built KPI cards for current-year values and YoY change.</li>
    <li>Used line charts to show multi-year trends per indicator.</li>
  </ul>

  <h3>Insights</h3>
  <ul>
    <li>Risk factors with sustained upward trends signal future care demand pressure.</li>
    <li>Indicators with steady declines highlight successful prevention programs.</li>
    <li>Volatile indicators suggest data quality checks or policy changes affecting reporting.</li>
  </ul>
</details>

---

<details>
  <summary><strong>Analysis 2 — Geographic Performance (State Rankings)</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>Which states show the highest burden for priority conditions and risk factors?</p>

  <h3>Method</h3>
  <ul>
    <li>Ranked states by selected indicator values using RANKX.</li>
    <li>Visualized results with a filled map and ranked bar chart.</li>
    <li>Highlighted top/bottom performers for rapid executive scanning.</li>
  </ul>

  <h3>Insights</h3>
  <ul>
    <li>Geographic clusters of high burden help target regional intervention strategies.</li>
    <li>Outlier states warrant deeper investigation into policy or socioeconomic drivers.</li>
    <li>Consistent top performers provide benchmarks for best-practice analysis.</li>
  </ul>
</details>

---

<details>
  <summary><strong>Analysis 3 — Risk Factors vs. Outcomes</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>How do behavioral risk factors align with chronic disease outcomes?</p>

  <h3>Method</h3>
  <ul>
    <li>Built a scatterplot comparing a risk factor (e.g., obesity) to an outcome (e.g., diabetes).</li>
    <li>Added quadrant lines for above/below national average segmentation.</li>
    <li>Enabled state-level drill-through to view detailed profiles.</li>
  </ul>

  <h3>Insights</h3>
  <ul>
    <li>States in the high-risk/high-outcome quadrant represent priority targets.</li>
    <li>High-risk but lower-outcome states may indicate early intervention success.</li>
    <li>Low-risk/high-outcome outliers suggest non-behavioral drivers worth investigating.</li>
  </ul>
</details>

---

<details>
  <summary><strong>Analysis 4 — Equity &amp; Disparities</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>Where are the largest demographic disparities within each state?</p>

  <h3>Method</h3>
  <ul>
    <li>Filtered to stratified rows and calculated disparity gaps by group.</li>
    <li>Used matrix heatmaps to compare disparities across indicators.</li>
    <li>Added slicers for race/ethnicity, sex, and age groups.</li>
  </ul>

  <h3>Insights</h3>
  <ul>
    <li>Disparity gaps highlight where equity-focused interventions are most urgent.</li>
    <li>Indicators with consistently large gaps merit targeted outreach and funding.</li>
    <li>States with narrowing gaps can inform best-practice transfer.</li>
  </ul>
</details>

---

<details>
  <summary><strong>Conclusions &amp; Recommendations</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Key Takeaways</h3>
  <ul>
    <li>Trend analysis surfaces both improving and worsening chronic disease indicators.</li>
    <li>State rankings expose geographic hotspots that require targeted resources.</li>
    <li>Equity metrics reveal where disparities are most persistent and actionable.</li>
  </ul>

  <h3>Recommended Actions</h3>
  <ul>
    <li>Prioritize funding in high-burden states with worsening trends.</li>
    <li>Expand prevention initiatives in high-risk quadrants (obesity, smoking, inactivity).</li>
    <li>Set equity KPIs to track gap reductions across demographic groups.</li>
    <li>Use top-performing states as benchmarks for scalable interventions.</li>
  </ul>
</details>
