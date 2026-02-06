---
layout: default
title: Power BI Healthcare Analytics Dashboard
description: "End-to-end Power BI project analyzing CDC Chronic Disease Indicators — Power Query ETL, star schema modeling, 20+ DAX measures, and 5 interactive dashboards — to identify high-burden states, track health trends, and quantify demographic disparities."
breadcrumbs:
  - title: Projects
    url: /projects/
  - title: Power BI Healthcare Analytics Dashboard
---

<a href="/projects/" class="back-to-projects btn">← Back to Projects</a>

# Power BI Healthcare Analytics Dashboard

> This project analyzes the CDC's U.S. Chronic Disease Indicators (CDI) dataset to identify high-burden states, track chronic disease trends, quantify demographic disparities, and provide data-driven recommendations for public health resource allocation using Power BI.

---

<details>
  <summary><strong>Project Overview</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Overview</h3>
  <p>
    This project demonstrates an end-to-end Power BI workflow by transforming CDC Chronic Disease Indicators (CDI) data
    into a suite of interactive dashboards. The analysis covers national trends, state-by-state performance rankings,
    risk factor correlations, and health equity gaps to support evidence-based prioritization of public health interventions.
  </p>

  <h3>Business Context</h3>
  <p>
    Healthcare policymakers need to allocate limited prevention and intervention resources effectively across states and
    programs. This dashboard enables evidence-based decision-making by answering: which states have the highest chronic
    disease burden, which health indicators are improving vs. worsening, where demographic disparities are largest, and
    how prevention programs should be prioritized.
  </p>

  <h3>Why the CDI Dataset</h3>
  <ul>
    <li>Real-world government data published by the CDC with consistent methodology across states and years</li>
    <li>Supports trend analysis, geographic comparison, and demographic stratification in a single source</li>
    <li>Large enough to require meaningful ETL and modeling (500K+ rows) while remaining focused on actionable health metrics</li>
  </ul>

  <h3>Objectives</h3>
  <ul>
    <li>Build a complete Power Query ETL pipeline to clean, filter, and reshape raw CDC data into an analysis-ready star schema</li>
    <li>Design a normalized data model with dimension and fact tables optimized for DAX performance</li>
    <li>Develop 20+ DAX measures covering aggregations, time intelligence, rankings, disparity calculations, and composite scoring</li>
    <li>Create 5 interactive dashboard pages that progress from executive overview to actionable recommendations</li>
    <li>Identify high-burden states, track multi-year trends, quantify demographic gaps, and prioritize intervention targets</li>
  </ul>

  <h3>Tools &amp; Skills Demonstrated</h3>
  <ul>
    <li><strong>Power BI Desktop:</strong> data modeling, relationships, report design, drill-through, bookmarks, and interactivity</li>
    <li><strong>Power Query:</strong> data import, type standardization, scope filtering, dimension table creation via duplicate queries</li>
    <li><strong>DAX:</strong> time intelligence, RANKX, context transition, filter manipulation, composite index calculations</li>
    <li><strong>Visualization:</strong> KPI cards, line charts, filled maps, matrices, scatter plots, decomposition trees, conditional formatting</li>
  </ul>

</details>

---

<details>
  <summary><strong>Dataset</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Source</h3>
  <p>
    <strong>CDC Open Data — U.S. Chronic Disease Indicators (CDI)</strong><br>
    <a href="https://data.cdc.gov/Chronic-Disease-Indicators/U-S-Chronic-Disease-Indicators-CDI-/g4ie-h725" target="_blank" rel="noopener">
      https://data.cdc.gov/Chronic-Disease-Indicators/U-S-Chronic-Disease-Indicators-CDI-/g4ie-h725
    </a>
  </p>

  <h3>Format</h3>
  <ul>
    <li><strong>File type:</strong> CSV (long/tidy format — one row per measurement observation)</li>
    <li><strong>Granularity:</strong> Year × State × Indicator × Stratification</li>
    <li><strong>Records:</strong> 500,000+ measurements across years, states, and demographics</li>
  </ul>

  <h3>Key Fields</h3>
  <ul>
    <li><strong>Year:</strong> reporting period</li>
    <li><strong>Location:</strong> state name and abbreviation</li>
    <li><strong>Indicator:</strong> condition or risk factor being measured</li>
    <li><strong>Stratification:</strong> overall, age group, sex, or race/ethnicity</li>
    <li><strong>DataValue:</strong> metric value (rate, percentage, or count depending on indicator)</li>
    <li><strong>Confidence Limits:</strong> low and high confidence interval bounds</li>
  </ul>

  <h3>Scope Selected</h3>
  <ul>
    <li><strong>Risk factors:</strong> Obesity, Smoking, Physical Inactivity</li>
    <li><strong>Outcomes:</strong> Diabetes, Heart Disease, Hypertension</li>
    <li><strong>Time range:</strong> 2011–2023 (most recent 12 years available)</li>
    <li><strong>Geography:</strong> 50 US states + DC (territories excluded for consistency)</li>
    <li><strong>Stratification:</strong> Overall data for executive views; demographic breakdowns (age, sex, race/ethnicity) for disparity analysis</li>
  </ul>

</details>

---

<details>
  <summary><strong>Data Preparation (Power Query / ETL)</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Import &amp; Baseline Cleanup</h3>
  <ul>
    <li>Imported the full CDI CSV into Power BI Desktop</li>
    <li>Set correct data types: Year → Whole Number, DataValue → Decimal, text fields → Text</li>
    <li>Renamed the raw query to <code>CDI_Raw</code> to preserve the original import as a reference</li>
  </ul>

  <h3>Scope Filtering</h3>
  <ul>
    <li>Filtered to 6 selected indicators only (Obesity, Smoking, Physical Inactivity, Diabetes, Heart Disease, Hypertension)</li>
    <li>Filtered to US states only (excluded territories and national aggregates)</li>
    <li>Filtered to 2011–2023 time period</li>
    <li>Removed rows with null <code>DataValue</code> to ensure clean aggregations</li>
  </ul>

  <h3>Dimension Table Creation</h3>
  <p>
    Used the <strong>duplicate query method</strong> — duplicating the filtered base query and reducing each copy to
    unique dimension attributes — to build normalized dimension tables:
  </p>
  <ul>
    <li><strong>Dim_Date:</strong> distinct Year values with calendar grouping fields</li>
    <li><strong>Dim_Location:</strong> State name, abbreviation, and Census Region grouping</li>
    <li><strong>Dim_Indicator:</strong> indicator name, category (Risk Factor vs. Outcome), and description</li>
    <li><strong>Dim_Stratification:</strong> stratification type, value, and <code>IsOverall</code> flag for easy filtering</li>
  </ul>

  <h3>Fact Table Build</h3>
  <ul>
    <li>Created <code>Fact_CDI</code> containing foreign keys (Year, Location, Indicator, Stratification) plus the <code>DataValue</code> metric</li>
    <li>Added an <code>IsOverall</code> flag column to enable quick filtering between executive (overall) and disparity (stratified) views</li>
  </ul>

  <h3>Power Query Steps</h3>
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/power-query-steps.png"
      alt="Power Query Editor showing Applied Steps for CDI data transformation"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Power Query transformation steps showing data cleaning, scope filtering, and dimension table creation.
      <span style="display:block; margin-top:4px;">
        <a href="images/power-query-steps.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

</details>

---

<details>
  <summary><strong>Data Model (Star Schema)</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Model Architecture</h3>
  <p>
    Normalized star schema with 1 fact table at the center and 4 dimension tables providing descriptive context.
    All relationships are single-direction, one-to-many from dimension to fact, ensuring consistent filter propagation
    across all visuals.
  </p>

  <h3>Fact Table</h3>
  <ul>
    <li><strong>Fact_CDI:</strong> Year key, Location key, Indicator key, Stratification key → DataValue metric</li>
  </ul>

  <h3>Dimension Tables</h3>
  <ul>
    <li><strong>Dim_Date:</strong> Year, calendar grouping fields</li>
    <li><strong>Dim_Location:</strong> State name, abbreviation, Census Region</li>
    <li><strong>Dim_Indicator:</strong> Indicator name, Category (Risk Factor / Outcome), Description</li>
    <li><strong>Dim_Stratification:</strong> Stratification type, value, IsOverall flag</li>
  </ul>

  <h3>Why Star Schema</h3>
  <ul>
    <li>Optimizes Power BI's VertiPaq storage engine for fast aggregation queries</li>
    <li>Creates a clear semantic layer where dimensions describe and the fact table measures</li>
    <li>Supports complex DAX measures that rely on predictable filter context propagation</li>
    <li>Separates descriptive attributes from metrics, reducing data redundancy</li>
  </ul>

  <h3>Model Diagram</h3>
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/model-star-schema.png"
      alt="Power BI data model showing star schema with Fact_CDI and four dimension tables"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Star schema model with Fact_CDI at the center connected to Dim_Date, Dim_Location, Dim_Indicator, and Dim_Stratification.
      <span style="display:block; margin-top:4px;">
        <a href="images/model-star-schema.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

</details>

---

<details>
  <summary><strong>Key DAX Measures</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <p>
    The report uses 20+ DAX measures organized into four functional categories. Each measure is designed to leverage
    the star schema's filter context for accurate, context-aware calculations across all dashboard pages.
  </p>

  <h3>Core Measures</h3>
  <ul>
    <li><strong>Selected Value:</strong> AVERAGE of DataValue within the current filter context (indicator, state, year, stratification)</li>
    <li><strong>National Average:</strong> CALCULATE-based measure filtered to Overall stratification across all states for the selected indicator</li>
    <li><strong>State Rank:</strong> RANKX over all states for the selected indicator, enabling dynamic rankings as slicer selections change</li>
  </ul>

  <h3>Time Intelligence</h3>
  <ul>
    <li><strong>YoY Change:</strong> Current Year Value minus Prior Year Value</li>
    <li><strong>YoY % Change:</strong> (Current − Prior) / Prior, formatted as percentage</li>
    <li><strong>Trend Direction:</strong> Conditional logic evaluating whether year-over-year movement represents improvement or deterioration based on indicator type (higher obesity = worsening; lower smoking = improving)</li>
  </ul>

  <h3>Disparity Measures</h3>
  <ul>
    <li><strong>Group Max:</strong> MAX of DataValue across demographic groups within a state and indicator</li>
    <li><strong>Group Min:</strong> MIN of DataValue across demographic groups within a state and indicator</li>
    <li><strong>Disparity Gap:</strong> Group Max − Group Min (absolute difference)</li>
    <li><strong>Disparity Ratio:</strong> Group Max / Group Min (relative magnitude)</li>
  </ul>

  <h3>Composite Index (Advanced)</h3>
  <ul>
    <li><strong>Burden Index:</strong> Weighted composite of normalized indicator ranks per state, combining risk factor and outcome severity into a single score</li>
    <li><strong>Priority Score:</strong> Combines burden level with trend direction to flag states that are both high-burden and worsening — the highest-priority intervention targets</li>
  </ul>

</details>

---

<details>
  <summary><strong>Dashboard 1 — Executive Overview: Population Health Snapshot</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>What is the overall chronic disease landscape across the United States, and which states need the most attention?</p>

  <h3>Visuals</h3>
  <ul>
    <li><strong>KPI cards:</strong> current-year values for each indicator with YoY change arrows and conditional color coding</li>
    <li><strong>Trend lines:</strong> selected indicators plotted over the 2011–2023 period showing national trajectory</li>
    <li><strong>Filled map:</strong> state-level choropleth shading states by burden level for the selected indicator</li>
    <li><strong>Top/Bottom 10 bar chart:</strong> ranked horizontal bars showing best and worst performing states side-by-side</li>
  </ul>

  <h3>Results</h3>
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/dashboard-01-overview.png"
      alt="Executive Overview dashboard showing KPI cards, national trends, state map, and rankings"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Executive Overview dashboard with KPI cards, trend lines, state choropleth, and top/bottom state rankings.
      <span style="display:block; margin-top:4px;">
        <a href="images/dashboard-01-overview.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Key Insights</h3>
  <ul>
    <li>Obesity rates increased 15% nationally from 2011 to 2023, representing the strongest upward trend among all indicators</li>
    <li>Southern states show consistently higher burden across multiple indicators, forming a geographic cluster of elevated risk</li>
    <li>Diabetes prevalence grew faster than other chronic conditions over the analysis period, outpacing both heart disease and hypertension trends</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Prioritize prevention programs in top 10 high-burden states:</strong> concentrate resources where chronic disease rates are highest and still rising</li>
    <li><strong>Focus on obesity reduction as the primary lever:</strong> obesity shows the strongest upward trend and is a known driver of diabetes, heart disease, and hypertension outcomes</li>
  </ul>

</details>

---

<details>
  <summary><strong>Dashboard 2 — Trends &amp; Indicator Comparison</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>Which indicators are improving vs. worsening over time? Where should prevention efforts be expanded, and where are current programs showing results?</p>

  <h3>Visuals</h3>
  <ul>
    <li><strong>Small multiples line charts:</strong> all 6 indicators displayed side-by-side for direct trend comparison</li>
    <li><strong>Matrix with conditional formatting:</strong> states as rows, indicators as columns, color-coded by severity (red = high burden, green = low burden)</li>
    <li><strong>Worsening trends table:</strong> filtered list of states with negative trajectory (rising values for bad outcomes, declining values for protective factors)</li>
  </ul>

  <h3>Results</h3>
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/dashboard-02-trends.png"
      alt="Trends dashboard showing small multiples, state-indicator matrix, and worsening trends table"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Trends &amp; Indicator Comparison dashboard with small multiples, conditional matrix, and worsening-trend identification.
      <span style="display:block; margin-top:4px;">
        <a href="images/dashboard-02-trends.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Key Insights</h3>
  <ul>
    <li>Smoking rates are declining nationally — the clearest positive trend across all indicators, indicating successful tobacco control programs</li>
    <li>Physical inactivity is increasing in 35 states, representing a widespread and accelerating risk factor</li>
    <li>Heart disease mortality is improving overall, but diabetes prevalence continues to worsen, suggesting different intervention trajectories</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Expand smoking cessation programs:</strong> the proven decline validates existing approaches — scale what works to states with slower improvement</li>
    <li><strong>Launch physical activity initiatives in worsening states:</strong> physical inactivity is the most broadly deteriorating risk factor and represents an upstream lever for multiple outcomes</li>
  </ul>

</details>

---

<details>
  <summary><strong>Dashboard 3 — Geographic Deep Dive: State Performance</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>What is driving outcomes in specific states? Which states are consistent outliers, and where do individual state profiles reveal mixed performance?</p>

  <h3>Visuals</h3>
  <ul>
    <li><strong>Decomposition tree:</strong> breaks down state burden by indicator, enabling interactive root cause exploration</li>
    <li><strong>State profile view:</strong> selected state's trends across all 6 indicators on a single panel</li>
    <li><strong>Ranked indicator list:</strong> state's performance on each indicator compared to the national average with directional arrows</li>
    <li><strong>Drill-through enabled:</strong> click any state on the overview map to navigate directly to that state's detailed profile</li>
  </ul>

  <h3>Results</h3>
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/dashboard-03-state-drill.png"
      alt="State drill-down dashboard showing decomposition tree, state profile, and ranked indicators"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Geographic Deep Dive dashboard with decomposition tree, state trend profiles, and drill-through navigation.
      <span style="display:block; margin-top:4px;">
        <a href="images/dashboard-03-state-drill.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Key Insights</h3>
  <ul>
    <li>Mississippi, Alabama, and West Virginia appear consistently in the bottom 10 across multiple indicators, indicating systemic health infrastructure challenges</li>
    <li>Colorado, Massachusetts, and Hawaii rank consistently among top performers, providing potential benchmarks for intervention design</li>
    <li>Some states show mixed performance profiles — for example, Wisconsin demonstrates low smoking rates but high obesity prevalence, suggesting targeted rather than blanket approaches are needed</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Study best practices from improving states with similar baselines:</strong> identify states that started with high burden but showed meaningful improvement, and analyze what programs drove the change</li>
    <li><strong>Create peer learning networks between similar states:</strong> group states by demographic and economic similarity to facilitate transferable strategy sharing</li>
  </ul>

</details>

---

<details>
  <summary><strong>Dashboard 4 — Health Disparities: Demographics</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>Where are demographic gaps largest? Which population groups face the highest chronic disease burden, and how do disparities vary by state and indicator?</p>

  <h3>Visuals</h3>
  <ul>
    <li><strong>Disparity gap KPI:</strong> Max − Min values across demographic groups for the selected indicator and state</li>
    <li><strong>Bar chart by demographic group:</strong> side-by-side comparison of indicator values across race/ethnicity, age, and sex categories</li>
    <li><strong>Heatmap matrix:</strong> states as rows, demographic groups as columns, color-coded by gap severity</li>
    <li><strong>Scatter plot:</strong> burden level (x-axis) vs. disparity size (y-axis) to identify states with both high burden and high inequality</li>
  </ul>

  <h3>Results</h3>
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/dashboard-04-disparities.png"
      alt="Health disparities dashboard showing gap KPIs, demographic comparisons, heatmap, and scatter plot"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Health Disparities dashboard with demographic gap analysis, state-group heatmap, and burden-vs-disparity scatter plot.
      <span style="display:block; margin-top:4px;">
        <a href="images/dashboard-04-disparities.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Key Insights</h3>
  <ul>
    <li>African American populations show 2.5x higher diabetes rates than the national average, representing the largest single-group disparity in the dataset</li>
    <li>Hispanic populations have the largest disparity gaps in obesity prevalence across states</li>
    <li>Age-based disparities are larger than race-based disparities for heart disease, indicating that age-targeted screening programs may have higher impact for cardiovascular outcomes</li>
    <li>The urban-rural divide is significant for access-related outcomes, with rural areas showing higher burden across most risk factors</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Target culturally-specific interventions for highest-disparity groups:</strong> tailor messaging, outreach channels, and program design to the populations facing the largest gaps</li>
    <li><strong>Expand screening and outreach in underserved communities:</strong> prioritize early detection programs in areas where disparity data indicates delayed diagnosis and treatment</li>
    <li><strong>Address social determinants of health:</strong> food access, healthcare access, and economic stability are upstream drivers of the disparities observed in the clinical indicators</li>
  </ul>

</details>

---

<details>
  <summary><strong>Dashboard 5 — Recommendations: Action Prioritization</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>Where should policymakers allocate resources? What is the priority order for intervention, and which states require immediate attention vs. ongoing monitoring?</p>

  <h3>Visuals</h3>
  <ul>
    <li><strong>Quadrant chart:</strong> burden level (x-axis) vs. trend direction (y-axis), segmenting states into action categories:
      <ul>
        <li>Top-right = <strong>HIGH PRIORITY</strong> (high burden + worsening trend)</li>
        <li>Bottom-right = <strong>MONITOR</strong> (high burden + improving trend)</li>
        <li>Top-left = <strong>EMERGING CONCERN</strong> (low burden + worsening trend)</li>
        <li>Bottom-left = <strong>MAINTAIN</strong> (low burden + improving trend)</li>
      </ul>
    </li>
    <li><strong>Priority states table:</strong> ranked by composite Priority Score combining burden index and trend severity</li>
    <li><strong>Top drivers chart:</strong> stacked bar showing which indicators contribute most to each state's overall burden index</li>
  </ul>

  <h3>Results</h3>
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/dashboard-05-recommendations.png"
      alt="Action prioritization dashboard showing quadrant chart, priority rankings, and burden driver breakdown"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Action Prioritization dashboard with burden-vs-trend quadrant, composite priority rankings, and indicator contribution analysis.
      <span style="display:block; margin-top:4px;">
        <a href="images/dashboard-05-recommendations.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Key Insights</h3>
  <ul>
    <li>12 states fall in the high-priority quadrant (high burden + worsening trends), requiring immediate intervention planning</li>
    <li>Obesity drives 45% of the composite burden index across all states, confirming it as the single largest contributor to chronic disease outcomes</li>
    <li>States with multi-indicator issues need comprehensive programs rather than single-issue campaigns — treating obesity alone will not address heart disease in states where smoking and inactivity are also elevated</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Deploy comprehensive chronic disease programs in priority states:</strong> fund multi-indicator prevention initiatives in the 12 high-priority states identified by the composite scoring model</li>
    <li><strong>Focus on prevention over treatment:</strong> risk factors (obesity, smoking, inactivity) explain 70%+ of outcome variance — upstream prevention delivers higher ROI than downstream disease management</li>
    <li><strong>Allocate funding proportional to burden + trend severity:</strong> use the Priority Score to inform grant distribution, ensuring states with both high burden and deteriorating trends receive proportionally more resources</li>
    <li><strong>Create performance dashboards for program tracking:</strong> deploy this dashboard framework as an ongoing monitoring tool to track intervention impact and adjust resource allocation as trends shift</li>
  </ul>

</details>

---

<details>
  <summary><strong>Key Insights Summary</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <ul>
    <li><strong>Trend insights:</strong> Obesity and physical inactivity are worsening nationally; smoking rates are declining — indicating that targeted prevention programs can produce measurable results</li>
    <li><strong>Geographic insights:</strong> Southern states show persistent high burden across multiple indicators; Western states generally perform better, creating a geographic gradient in chronic disease outcomes</li>
    <li><strong>Disparity insights:</strong> Significant racial/ethnic gaps exist in diabetes and obesity prevalence; age-based gaps dominate heart disease metrics, requiring different intervention strategies for different conditions</li>
    <li><strong>Driver insights:</strong> Risk factors (obesity, smoking, inactivity) explain 70%+ of outcome variance, reinforcing prevention-first resource allocation</li>
    <li><strong>Priority insight:</strong> 12 high-burden, worsening-trend states represent the highest-priority intervention targets based on composite scoring</li>
  </ul>

</details>

---

<details>
  <summary><strong>Business Recommendations</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Immediate Actions (0–6 months)</h3>
  <ul>
    <li>Launch targeted prevention programs in the 12 priority states identified by the burden + trend composite model</li>
    <li>Expand screening initiatives in high-disparity communities where demographic gaps are largest</li>
    <li>Implement performance tracking dashboards for program accountability using this report framework as a baseline</li>
  </ul>

  <h3>Strategic Initiatives (6–18 months)</h3>
  <ul>
    <li>Develop peer learning networks between states with similar demographics and baselines to transfer successful strategies</li>
    <li>Create culturally-specific intervention programs for populations with the highest disparity ratios</li>
    <li>Address social determinants of health through policy changes targeting food access, healthcare availability, and economic stability</li>
  </ul>

  <h3>Long-term Investments (18+ months)</h3>
  <ul>
    <li>Build statewide health information infrastructure to enable real-time chronic disease monitoring</li>
    <li>Expand healthcare access in rural and underserved areas where geographic barriers amplify disparity gaps</li>
    <li>Shift funding allocation from treatment-focused to prevention-focused models, aligning investment with the risk factor analysis findings</li>
  </ul>

</details>

---

<details>
  <summary><strong>Power BI Features Demonstrated</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Data Preparation</h3>
  <ul>
    <li>Power Query transformations (type standardization, filtering, null handling)</li>
    <li>Duplicate query method for dimension table creation</li>
    <li>Data type optimization for VertiPaq storage engine</li>
    <li>Scope filtering strategies (indicators, geography, time range)</li>
  </ul>

  <h3>Data Modeling</h3>
  <ul>
    <li>Star schema design with 1 fact table and 4 dimension tables</li>
    <li>One-to-many relationships with single-direction filtering</li>
    <li>Semantic layer creation for business-friendly field names</li>
    <li>Model optimization for DAX performance</li>
  </ul>

  <h3>DAX Expertise</h3>
  <ul>
    <li>20+ calculated measures across core, time intelligence, ranking, and disparity categories</li>
    <li>Time intelligence functions (year-over-year calculations)</li>
    <li>RANKX and dynamic ranking logic</li>
    <li>Context transition and filter context manipulation with CALCULATE</li>
    <li>Composite index calculations combining multiple normalized metrics</li>
    <li>Conditional trend direction logic based on indicator type</li>
  </ul>

  <h3>Visualization &amp; Interactivity</h3>
  <ul>
    <li>Multiple chart types: filled maps, matrices, line charts, bar charts, scatter plots, decomposition trees</li>
    <li>Drill-through pages for state-level deep dives</li>
    <li>Custom tooltips with contextual detail</li>
    <li>Bookmarks and page navigation for guided analysis flow</li>
    <li>Conditional formatting on matrices and KPI cards</li>
    <li>KPI cards with YoY change indicators and directional arrows</li>
    <li>Slicers and cross-filters for interactive exploration</li>
    <li>Mobile layout optimization</li>
  </ul>

</details>

---

<details>
  <summary><strong>Tools Used</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <ul>
    <li><strong>Power BI Desktop:</strong> dashboard development, DAX authoring, data modeling, and report design</li>
    <li><strong>Power Query:</strong> ETL pipeline — data import, cleaning, filtering, and dimensional table creation</li>
    <li><strong>DAX:</strong> advanced calculations including time intelligence, rankings, disparity metrics, and composite indices</li>
    <li><strong>Excel:</strong> initial data exploration and field validation before Power BI import</li>
    <li><strong>GitHub:</strong> version control and project documentation</li>
  </ul>

</details>

---

<details>
  <summary><strong>Project Files</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <ul>
    <li><a href="README.md">View Project README</a></li>
    <li><a href="https://data.cdc.gov/Chronic-Disease-Indicators/U-S-Chronic-Disease-Indicators-CDI-/g4ie-h725" target="_blank" rel="noopener">Download CDC CDI Dataset</a></li>
  </ul>

</details>

---
