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

> This project demonstrates advanced Power BI proficiency through comprehensive analysis of public health data, focusing on healthcare outcomes, population health trends, and resource allocation insights.

---

<details>
  <summary><strong>Project Summary</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <p>
    This project uses the CDC’s U.S. Chronic Disease Indicators (CDI) dataset to analyze chronic disease outcomes and
    risk factors across time (year), geography (state), and demographic stratifications (age/sex/race, etc.). The goal is
    to build a professional Power BI report that demonstrates end-to-end BI workflow: data ingestion, Power Query
    transformation, dimensional modeling (star schema), advanced DAX measures, and stakeholder-ready dashboards with
    actionable insights and recommendations.
  </p>

  <p><strong>Key stakeholder questions addressed:</strong></p>
  <ul>
    <li>Which chronic conditions and risk factors are improving or worsening over time?</li>
    <li>Which states consistently show the highest burden?</li>
    <li>Where do disparities across demographic groups appear largest?</li>
    <li>Which metrics should policymakers prioritize for targeted interventions?</li>
  </ul>
</details>

---

<details>
  <summary><strong>Dataset</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <p><strong>Dataset:</strong> CDC Open Data – U.S. Chronic Disease Indicators (CDI)</p>
  <p><strong>Format:</strong> CSV download (raw) + optional API endpoint (future enhancement)</p>

  <h3>Key Characteristics</h3>
  <ul>
    <li>Long / “tidy” fact table structure: one row per measurement</li>
    <li>Includes Year, Location, Indicator, Stratification, and Value (rate/percent/count)</li>
    <li>Optional fields: confidence limits, footnotes, data source details</li>
  </ul>

  <h3>Why CDI Works Well for a Portfolio</h3>
  <ul>
    <li>Real-world, government-published, non-synthetic data</li>
    <li>Supports trend analysis, mapping, ranking, segmentation, and disparity analysis</li>
    <li>Large enough to be realistic but manageable in Power BI</li>
  </ul>
</details>

---

<details>
  <summary><strong>Project Goals</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Technical Goals (Power BI Skill Showcase)</h3>
  <ul>
    <li>Power Query ETL: clean raw CDC data, standardize types and values, filter to relevant scope.</li>
    <li>Dimensional modeling (star schema) with clean relationships and semantic layer.</li>
    <li>Advanced DAX measures: time intelligence, rankings, and disparity calculations.</li>
    <li>Interactive BI report with drill-through, tooltips, and optional bookmarks/navigation.</li>
  </ul>

  <h3>Analytical Goals (Business/Healthcare Outcomes)</h3>
  <ul>
    <li>Identify high-burden states and persistent regional clusters.</li>
    <li>Highlight worsening vs improving indicators over time.</li>
    <li>Quantify demographic disparities by condition and location.</li>
    <li>Provide actionable recommendations for resource allocation and prevention programs.</li>
  </ul>
</details>

---

<details>
  <summary><strong>Scope Definition</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <p>
    To keep the report stakeholder-friendly (and avoid “dashboard soup”), the project will focus on a curated set of
    6–12 indicators and a defined date range.
  </p>

  <h3>Recommended Scope (Balanced)</h3>
  <ul>
    <li><strong>Risk factors:</strong> obesity, smoking, physical inactivity</li>
    <li><strong>Outcomes:</strong> diabetes, heart disease (or hypertension), mortality-related metric (if available)</li>
    <li><strong>Time range:</strong> last ~8–12 years available (e.g., 2012–2023, depending on coverage)</li>
  </ul>

  <h3>Stratification Strategy</h3>
  <ul>
    <li>Executive/overview pages use Overall rows only for clean comparisons.</li>
    <li>Disparities pages use stratified rows (race/sex/age) with clear slicers.</li>
  </ul>
</details>

---

<details>
  <summary><strong>Data Model Design (Star Schema)</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <p>
    Even though the dataset is one CSV, the Power BI model will be normalized into a star schema by creating
    dimension tables in Power Query.
  </p>

  <h3>Fact Table</h3>
  <ul>
    <li><strong>Fact_CDI:</strong> core measurement table</li>
    <li><strong>Keys:</strong> Year, Location, Indicator, Stratification</li>
    <li><strong>Metrics:</strong> DataValue (+ optional confidence limits)</li>
  </ul>

  <h3>Dimension Tables</h3>
  <ul>
    <li><strong>Dim_Date:</strong> Year (plus fiscal/period fields if needed)</li>
    <li><strong>Dim_Location:</strong> State name, abbreviation, optional region grouping</li>
    <li><strong>Dim_Indicator:</strong> Indicator name, category/topic, description</li>
    <li><strong>Dim_Stratification:</strong> Overall vs stratification types and values</li>
  </ul>

  <h3>Relationships</h3>
  <ul>
    <li>Fact_CDI[Year] → Dim_Date[Year]</li>
    <li>Fact_CDI[LocationKey] → Dim_Location[LocationKey]</li>
    <li>Fact_CDI[IndicatorKey] → Dim_Indicator[IndicatorKey]</li>
    <li>Fact_CDI[StratKey] → Dim_Stratification[StratKey]</li>
  </ul>

  <p><strong>Why this matters:</strong> relationships replace joins from SQL by enforcing consistent context in every visual.</p>
</details>

---

<details>
  <summary><strong>Power Query (ETL) Plan</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Step A — Import and baseline cleanup</h3>
  <ul>
    <li>Import CSV into Power BI (Transform Data).</li>
    <li>Rename raw query to <code>CDI_Raw</code>.</li>
    <li>Set correct data types (Year → Whole Number, DataValue → Decimal, text fields → Text).</li>
  </ul>

  <h3>Step B — Reduce noise and focus scope</h3>
  <ul>
    <li>Filter out rows where DataValue is blank (or handle in measures).</li>
    <li>Filter territories if using US states only.</li>
    <li>Filter to selected years and indicators.</li>
  </ul>

  <h3>Step C — Create dimensions (duplicate query method)</h3>
  <ul>
    <li>Dim_Location: select location fields → remove duplicates.</li>
    <li>Dim_Indicator: select indicator fields → remove duplicates.</li>
    <li>Dim_Stratification: select stratification fields → remove duplicates.</li>
    <li>Dim_Date: create from Year values or build a proper date table.</li>
  </ul>

  <h3>Step D — Build Fact_CDI</h3>
  <ul>
    <li>Reference <code>CDI_Raw</code> and keep only keys + metric fields.</li>
    <li>Add an <code>IsOverall</code> flag (true/false) if helpful for filtering.</li>
    <li>Standardize numeric fields if values sometimes store as text.</li>
  </ul>
</details>

---

<details>
  <summary><strong>DAX Measures (Core Measure Set)</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Core Measures</h3>
  <ul>
    <li>Selected Value: average/median of DataValue (avg typically fits pre-aggregated rows).</li>
    <li>National Avg (overall filtered appropriately).</li>
    <li>State Rank (RANKX by state).</li>
  </ul>

  <h3>Time Intelligence</h3>
  <ul>
    <li>YoY Change = Value – Value prior year.</li>
    <li>YoY % Change = (Value – Prior) / Prior.</li>
    <li>Trend Direction = improving/worsening (based on sign and metric meaning).</li>
  </ul>

  <h3>Disparity Measures</h3>
  <ul>
    <li>Group Max vs Group Min (within state/indicator/year).</li>
    <li>Disparity Gap = Max – Min.</li>
    <li>Disparity Ratio = Max / Min.</li>
  </ul>

  <h3>Composite Index (Advanced)</h3>
  <ul>
    <li>Normalize selected indicators per state (percentile rank).</li>
    <li>Build a Burden Index to rank states across multiple metrics.</li>
  </ul>
</details>

---

<details>
  <summary><strong>Dashboard Pages (Purpose &amp; Features)</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Page 1 — Executive Overview (Population Health Snapshot)</h3>
  <ul>
    <li><strong>Purpose:</strong> high-level summary of health trends and best/worst states.</li>
    <li><strong>Visuals:</strong> KPI cards, trend lines, state map, Top/Bottom 10 chart.</li>
    <li><strong>Skills shown:</strong> time intelligence, mapping, clean layout, slicers.</li>
  </ul>

  <h3>Page 2 — Trends &amp; Indicator Comparison</h3>
  <ul>
    <li><strong>Purpose:</strong> compare indicators and identify worsening areas.</li>
    <li><strong>Visuals:</strong> small multiples or dynamic selector, conditional matrix, “worsening list.”</li>
    <li><strong>Skills shown:</strong> measure-driven visuals, formatting, dynamic filtering.</li>
  </ul>

  <h3>Page 3 — Geographic Deep Dive (State Performance)</h3>
  <ul>
    <li><strong>Purpose:</strong> drill into a state and see what drives outcomes.</li>
    <li><strong>Visuals:</strong> decomposition tree, state profile trends, ranked indicator list.</li>
    <li><strong>Skills shown:</strong> drill-through, tooltips, decomposition tree.</li>
  </ul>

  <h3>Page 4 — Health Disparities (Demographics)</h3>
  <ul>
    <li><strong>Purpose:</strong> quantify demographic gaps and identify inequities.</li>
    <li><strong>Visuals:</strong> disparity KPI, demographic bars, heatmap/matrix.</li>
    <li><strong>Skills shown:</strong> segmentation, disparity calculations, storytelling.</li>
  </ul>

  <h3>Page 5 — Recommendations / Action Prioritization</h3>
  <ul>
    <li><strong>Purpose:</strong> translate analysis into interventions.</li>
    <li><strong>Visuals:</strong> burden vs trend quadrant, priority states table, top drivers chart.</li>
    <li><strong>Skills shown:</strong> decision framing, prioritization logic, executive communication.</li>
  </ul>
</details>

---

<details>
  <summary><strong>Insight Themes &amp; Recommendations</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Insight Themes</h3>
  <ul>
    <li>Trend insight: which indicators are improving/worsening nationally.</li>
    <li>Geographic insight: states that cluster high/low and persistent outliers.</li>
    <li>Disparity insight: where gaps are largest and which groups are most affected.</li>
    <li>Driver insight: indicators that contribute most to a state’s burden.</li>
  </ul>

  <h3>Recommendation Examples</h3>
  <ul>
    <li>Prioritize prevention programs in “high burden + worsening trend” states.</li>
    <li>Expand screening/outreach where disparities are consistently large.</li>
    <li>Replicate strategies from improving states with similar baselines.</li>
    <li>Target risk-factor interventions where they dominate the burden index.</li>
  </ul>
</details>

---

<details>
  <summary><strong>Deliverables</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Power BI Artifacts</h3>
  <ul>
    <li>.pbix report file with star schema model and documented measures</li>
    <li>4–5 polished report pages with drill-through and tooltips</li>
  </ul>

  <h3>Documentation Artifacts</h3>
  <ul>
    <li>Data dictionary (key fields used)</li>
    <li>DAX measure catalog (names + definitions)</li>
    <li>Power Query steps summary</li>
  </ul>

  <h3>Portfolio Webpage Assets</h3>
  <ul>
    <li>Screenshots of data model view and Power Query steps</li>
    <li>Screenshots of each report page (overview, trends, deep dive, disparities, recommendations)</li>
    <li>Short narrative for each page (question → method → insight → recommendation)</li>
  </ul>
</details>

---

<details>
  <summary><strong>Suggested GitHub Project Folder Structure</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <pre>
projects/powerbi-healthcare-cdi/
│── index.md
│── README.md
│── data/
│   └── cdi_raw.csv  (or link if too large)
│── pbix/
│   └── healthcare_cdi_dashboard.pbix
│── images/
│   ├── model-star-schema.png
│   ├── power-query-steps.png
│   ├── dashboard-01-overview.png
│   ├── dashboard-02-trends.png
│   ├── dashboard-03-state-drill.png
│   ├── dashboard-04-disparities.png
│   ├── dashboard-05-recommendations.png
└── docs/
    ├── dax-measures.md
    └── data-dictionary.md
  </pre>
</details>

---

<details>
  <summary><strong>Webpage Structure Outline</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <ul>
    <li><strong>Overview:</strong> problem context, why CDI, why Power BI.</li>
    <li><strong>Dataset:</strong> source link, content summary, scope decisions.</li>
    <li><strong>Data Preparation:</strong> Power Query steps with screenshots.</li>
    <li><strong>Data Model:</strong> star schema explanation and relationships screenshot.</li>
    <li><strong>Key DAX Measures:</strong> short list with purpose and examples.</li>
    <li><strong>Dashboard Pages:</strong> overview, trends, state drill, disparities, prioritization.</li>
    <li><strong>Conclusion:</strong> summary of findings and next steps.</li>
  </ul>
</details>

---

<details>
  <summary><strong>Future Enhancements</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <ul>
    <li>Connect via API endpoint instead of static CSV (refreshable).</li>
    <li>Add a second dataset (e.g., CMS readmissions) as a second fact table.</li>
    <li>Add a policy simulation “what-if” parameter page.</li>
    <li>Document performance optimization (hide columns, reduce cardinality).</li>
  </ul>
</details>
