---
layout: default
title: Power BI — CDC Chronic Disease Analytics
description: "End-to-end Power BI project analyzing CDC Chronic Disease Indicators — Power Query ETL, star schema dimensional modeling, 10 DAX measures, and 5 interactive dashboards — tracking U.S. health trends, ranking states, and quantifying demographic disparities across 9 chronic disease topics."
breadcrumbs:
  - title: Projects
    url: /projects/
  - title: Power BI — CDC Chronic Disease Analytics
---

<a href="/projects/" class="back-to-projects btn">← Back to Projects</a>

# Power BI — CDC Chronic Disease Analytics

<div class="project-hero">
  <figure class="project-hero-img">
    <img
      src="images/powerbi-dashboard-1.png"
      alt="Executive Overview dashboard with KPI cards, trend line, top 10 bar chart, filled map, and slicers"
      loading="eager"
    >
  </figure>

  <div class="project-meta">
    <div class="meta-badges">
      <span class="badge badge-tool">Power BI</span>
      <span class="badge badge-tool">Power Query</span>
      <span class="badge badge-tool">DAX</span>
      <span class="badge badge-data">CDC Open Data</span>
    </div>
  </div>
</div>

> End-to-end Power BI analysis of the CDC's U.S. Chronic Disease Indicators dataset — from raw CSV through Power Query ETL, star schema modeling, and 10 DAX measures to 5 interactive dashboards tracking health trends, ranking states, and quantifying demographic disparities.

<div class="project-stats">
  <div class="stat-item">
    <span class="stat-number">9</span>
    <span class="stat-label">Disease Topics</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">52</span>
    <span class="stat-label">U.S. Locations</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">7</span>
    <span class="stat-label">Years of Data</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">10</span>
    <span class="stat-label">DAX Measures</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">5</span>
    <span class="stat-label">Dashboards</span>
  </div>
</div>

---

<details>
  <summary><strong>Project Overview</strong></summary>

<div class="details-content">

### The Problem

Chronic diseases account for the leading causes of death and disability in the United States, but surveillance data from the CDC arrives as a massive, flat CSV file — hundreds of thousands of rows spanning dozens of topics, all states and territories, and multiple demographic stratifications. Without transformation and modeling, this data is unusable for decision-making.

### The Approach

I built a complete Power BI analytics solution that transforms raw CDC data into an interactive reporting tool. The pipeline covers every stage of the BI development lifecycle:

1. **Power Query ETL** — import, filter, type-cast, and reshape raw data
2. **Star Schema Modeling** — one fact table + four dimension tables with proper relationships
3. **DAX Measure Development** — 10 measures across aggregations, time intelligence, and disparity analysis
4. **Interactive Dashboards** — 5 report pages answering distinct business questions

### Scope

- **9 topics:** Alcohol, Arthritis, Asthma, Cancer, Cardiovascular Disease, Chronic Kidney Disease, Diabetes, Nutrition/Physical Activity/Weight Status, Tobacco
- **52 locations:** 50 states + DC + national aggregate (territories excluded for consistency)
- **7 years:** 2015–2022 (2017 absent from source data)

### Tools & Skills

- **Power BI Desktop:** data modeling, relationships, DAX authoring, report design, interactivity
- **Power Query (M):** data import, type standardization, scope filtering, null removal, dimension table creation via duplicate-and-reduce
- **DAX:** SUM, AVERAGE, CALCULATE with ALL, RANKX, DATEADD, ALLEXCEPT, DIVIDE
- **Data Modeling:** star schema, one-to-many relationships, single-direction filter propagation, dedicated _Measures table
- **Visualization:** KPI cards, line charts, filled maps, bar charts, matrix tables, scatter plots, decomposition trees, gauge charts, conditional formatting

</div>
</details>

<details>
  <summary><strong>Dataset</strong></summary>

<div class="details-content">

### Source

**CDC Open Data — U.S. Chronic Disease Indicators (CDI)**
<a href="https://data.cdc.gov/Chronic-Disease-Indicators/U-S-Chronic-Disease-Indicators-CDI-/g4ie-h725" target="_blank" rel="noopener">data.cdc.gov/Chronic-Disease-Indicators</a>

### Format

- **File type:** CSV in tidy/long format — one row per measurement observation
- **Granularity:** Year × Location × Indicator × Stratification
- **Structure:** Each row represents a single data point for a specific year, state, health indicator, and demographic group

### Scope Decisions

The full CDI dataset contains hundreds of thousands of rows. To create a focused analysis, I made these filtering decisions during Power Query ETL:

**9 Topics Selected** — Alcohol, Arthritis, Asthma, Cancer, Cardiovascular Disease, Chronic Kidney Disease, Diabetes, Nutrition/Physical Activity/Weight Status, Tobacco. These cover both direct disease outcomes and behavioral risk factors.

**52 Locations** — 50 states + DC + national aggregate. Territories excluded for consistent state-to-state comparisons.

**7 Years** — 2015, 2016, 2018, 2019, 2020, 2021, 2022. Note: 2017 is missing from the source data.

**Filtered Result** — 999+ rows after removing territories, null data values, and out-of-scope topics. Null `DataValue` rows removed to ensure clean DAX aggregations.

</div>
</details>

<details>
  <summary><strong>Data Preparation (Power Query ETL)</strong></summary>

<div class="details-content">

The raw CDC CSV required significant transformation before analysis. I used Power Query to convert a single flat file into a normalized star schema with one fact table and four dimension tables.

### Step 1 — Import Raw Data

Imported the full CDI CSV into Power BI as `CDI_Raw` — an unmodified reference copy with no transformations applied.

<figure class="project-figure">
  <img
    src="images/powerbi-power-query-cdi-raw.png"
    alt="Power Query Editor showing the raw CDI dataset before transformation"
    loading="lazy"
  >
  <figcaption>
    <code>CDI_Raw</code> — original imported dataset preserved as-is before any transformations.
    <a href="images/powerbi-power-query-cdi-raw.png">View full size</a>
  </figcaption>
</figure>

### Step 2 — Filter & Scope

- Filtered to 9 selected disease topics
- Filtered to 52 locations (territories excluded)
- Removed rows with null `DataValue`
- Set correct data types: `YearStart` → Whole Number, `DataValue` → Decimal, confidence limits → Decimal, text fields → Text

### Step 3 — Create Dimension Tables

Used the **duplicate-and-reduce method**: duplicated the filtered query, removed all columns except dimension attributes, and applied *Remove Duplicates*. This ensures every dimension value has a corresponding fact record.

**Dim_Location** (52 rows, 4 columns)

<figure class="project-figure">
  <img
    src="images/powerbi-power-query-dim-location.png"
    alt="Dim_Location dimension table with 52 rows"
    loading="lazy"
  >
  <figcaption>
    <code>Dim_Location</code> — 52 unique locations with <code>LocationAbbr</code>, <code>LocationDesc</code>, <code>Geolocation</code>, and <code>LocationID</code>.
    <a href="images/powerbi-power-query-dim-location.png">View full size</a>
  </figcaption>
</figure>

**Dim_Indicator** (9 rows, 7 columns)

<figure class="project-figure">
  <img
    src="images/powerbi-power-query-dim-indicator.png"
    alt="Dim_Indicator dimension table with 9 rows"
    loading="lazy"
  >
  <figcaption>
    <code>Dim_Indicator</code> — 9 health indicators mapping topics to specific measurement questions (e.g., Cancer → Invasive cancer incidence, Diabetes → Diabetic ketoacidosis mortality).
    <a href="images/powerbi-power-query-dim-indicator.png">View full size</a>
  </figcaption>
</figure>

**Dim_Stratification** (5 rows, 4 columns)

<figure class="project-figure">
  <img
    src="images/powerbi-power-query-dim-stratification.png"
    alt="Dim_Stratification dimension table with 5 rows"
    loading="lazy"
  >
  <figcaption>
    <code>Dim_Stratification</code> — 5 demographic groups: Overall, Sex (Male), Race/Ethnicity (Hispanic), Age (≥65), Grade (10).
    <a href="images/powerbi-power-query-dim-stratification.png">View full size</a>
  </figcaption>
</figure>

**Dim_Date** (7 rows, 2 columns)

<figure class="project-figure">
  <img
    src="images/powerbi-power-query-dim-date.png"
    alt="Dim_Date dimension table with 7 rows"
    loading="lazy"
  >
  <figcaption>
    <code>Dim_Date</code> — 7 year records covering 2015–2022 (2017 absent from source).
    <a href="images/powerbi-power-query-dim-date.png">View full size</a>
  </figcaption>
</figure>

### Step 4 — Build Fact Table

Created `Fact_CDI` by selecting only foreign key and metric columns from the filtered query.

<figure class="project-figure">
  <img
    src="images/powerbi-power-query-fact-cdi.png"
    alt="Fact_CDI fact table with foreign keys and metric columns"
    loading="lazy"
  >
  <figcaption>
    <code>Fact_CDI</code> — 999+ rows with 7 columns: <code>YearStart</code>, <code>LocationID</code>, <code>QuestionID</code>, <code>StratificationID1</code>, <code>DataValue</code>, <code>LowConfidenceLimit</code>, <code>HighConfidenceLimit</code>.
    <a href="images/powerbi-power-query-fact-cdi.png">View full size</a>
  </figcaption>
</figure>

### Why This Approach

- **Accuracy:** removing nulls and territories prevents misleading aggregations
- **Performance:** normalized dimensions reduce redundancy and optimize VertiPaq compression
- **Maintainability:** duplicate-and-reduce ensures dimension-fact alignment
- **Scalability:** adding years or topics requires updating scope filters, not restructuring the model

</div>
</details>

<details>
  <summary><strong>Data Model (Star Schema)</strong></summary>

<div class="details-content">

### Architecture

A star schema organizes data into a central **fact table** (metrics) surrounded by **dimension tables** (descriptive context). This is the standard for Power BI because it optimizes query performance, simplifies DAX, and creates predictable filter propagation.

<figure class="project-figure">
  <img
    src="images/powerbi-data-connections.png"
    alt="Star schema with Fact_CDI connected to four dimension tables"
    loading="lazy"
  >
  <figcaption>
    Star schema: <code>Fact_CDI</code> at center, connected to <code>Dim_Date</code>, <code>Dim_Location</code>, <code>Dim_Indicator</code>, and <code>Dim_Stratification</code>.
    <a href="images/powerbi-data-connections.png">View full size</a>
  </figcaption>
</figure>

### Fact Table

**Fact_CDI** (999+ rows, 7 columns)
- **Foreign keys:** `YearStart`, `LocationID`, `QuestionID`, `StratificationID1`
- **Metrics:** `DataValue`, `LowConfidenceLimit`, `HighConfidenceLimit`

### Dimension Tables

| Table | Rows | Key | Purpose |
|---|---|---|---|
| **Dim_Location** | 52 | `LocationID` | Geographic filtering, maps, state comparisons |
| **Dim_Indicator** | 9 | `QuestionID` | Indicator metadata, topic-level analysis |
| **Dim_Stratification** | 5 | `StratificationID1` | Demographic group filtering, disparity analysis |
| **Dim_Date** | 7 | `YearStart` | Time-series trends, YoY calculations |

### Relationships

All relationships follow the same pattern: **one-to-many** from dimension to fact, with **single-direction** filter propagation. This ensures:

- Slicer selections correctly filter the fact table
- `CALCULATE` and `ALL` override filter context predictably
- No circular dependencies or ambiguous paths

### Why Star Schema

- **VertiPaq optimization:** low-cardinality dimensions compress efficiently in Power BI's in-memory engine
- **DAX clarity:** measures reference dimensions for context and facts for calculations
- **Filter propagation:** one-to-many ensures slicers and cross-filters work consistently
- **Reduced redundancy:** descriptive text stored once in dimensions, not repeated across 999+ fact rows

</div>
</details>

<details>
  <summary><strong>DAX Measures (10 Total)</strong></summary>

<div class="details-content">

All measures live in a dedicated `_Measures` table — separating calculation logic from data tables. The 10 measures fall into three categories.

### Core Aggregations

These drive all primary visualizations — KPI cards, trend lines, bar charts, and map shading.

**Total Value**
```
Total Value = SUM(Fact_CDI[DataValue])
```
Aggregate sum within current filter context. Used for total-volume views.

**Average Value**
```
Average Value = AVERAGE(Fact_CDI[DataValue])
```
The **primary metric** — most health indicators are rates or percentages where the mean is more meaningful than the sum.

**National Average**
```
National Average =
CALCULATE(
    [Average Value],
    ALL(Dim_Location)
)
```
Removes location filters to return the all-states benchmark. When a slicer selects a specific state, this still returns the national figure for comparison.

**State Rank**
```
State Rank =
RANKX(
    ALL(Dim_Location[LocationDesc]),
    [Average Value],
    ,
    DESC
)
```
Ranks states highest to lowest (1 = highest value). Updates dynamically as indicator and year selections change.

### Time Intelligence

Track how indicators change over time — whether conditions are improving or deteriorating.

**YoY Change**
```
YoY Change =
VAR CurrentValue = [Average Value]
VAR PreviousValue =
    CALCULATE(
        [Average Value],
        DATEADD(Dim_Date[YearStart], -1, YEAR)
    )
RETURN
    CurrentValue - PreviousValue
```
Absolute year-over-year difference. Positive = increased, negative = decreased.

**Previous Year Value**
```
Previous Year Value =
CALCULATE(
    [Average Value],
    PREVIOUSYEAR(Dim_Date[YearStart])
)
```
Helper measure returning the prior year's average for clean YoY calculations.

**YoY % Change**
```
YoY % Change =
DIVIDE(
    [Average Value] - [Previous Year Value],
    [Previous Year Value]
)
```
Percentage change using `DIVIDE` for safe division (returns blank when denominator is zero).

### Disparity Analysis

Quantify the gap between best- and worst-performing demographic groups. Critical for health equity — population averages can mask significant inequities.

**Group Max**
```
Group Max =
CALCULATE(
    MAX(Fact_CDI[DataValue]),
    ALLEXCEPT(Fact_CDI, Dim_Location, Dim_Indicator, Dim_Date)
)
```
Highest value across all demographic groups for a given location-indicator-year combination. `ALLEXCEPT` removes stratification filters while preserving other context.

**Group Min**
```
Group Min =
CALCULATE(
    MIN(Fact_CDI[DataValue]),
    ALLEXCEPT(Fact_CDI, Dim_Location, Dim_Indicator, Dim_Date)
)
```
Lowest value across demographic groups — the counterpart to Group Max.

**Disparity Gap**
```
Disparity Gap = [Group Max] - [Group Min]
```
Absolute difference between highest and lowest groups. A gap of 10 means a 10-point spread in outcomes.

**Disparity Ratio**
```
Disparity Ratio = DIVIDE([Group Max], [Group Min])
```
Relative inequality. A ratio of 2.0 means the highest-burden group's rate is 2x the lowest. Useful for comparing disparity severity across indicators with different scales.

</div>
</details>

<details>
  <summary><strong>Dashboard 1 — Executive Overview</strong></summary>

<div class="details-content">

A high-level population health snapshot for quick assessment of chronic disease indicators nationally.

### Questions Answered

- Which indicators have the highest or lowest values nationally?
- How do states compare for a selected health topic?
- Are conditions improving or worsening year over year?

### Visuals

- **4 KPI Cards:** Total Value, Average Value, National Average, State Rank
- **Trend Line:** Average Value by year (2015–2022)
- **Top 10 Bar Chart:** States ranked by Average Value
- **Filled Map:** Color-coded states by Average Value
- **3 Slicers:** Topic, Year, Stratification

<figure class="project-figure">
  <img
    src="images/powerbi-dashboard-1.png"
    alt="Executive Overview dashboard with KPI cards, trend line, top 10 bar chart, filled map, and slicers"
    loading="lazy"
  >
  <figcaption>
    Executive Overview — KPIs, geographic comparison, trend analysis, and interactive filtering.
    <a href="images/powerbi-dashboard-1.png">View full size</a>
  </figcaption>
</figure>

### Key Findings

- **State rankings shift by topic** — states ranking highest for Tobacco often differ from those ranking highest for Cardiovascular Disease, revealing non-uniform burden distribution
- **Trend patterns vary** — some topics show steady improvement while others plateau or worsen
- **Geographic clustering** — the filled map reveals regional patterns where neighboring states share similar values, suggesting shared environmental, economic, or policy drivers

</div>
</details>

<details>
  <summary><strong>Dashboard 2 — Trends & Indicator Comparison</strong></summary>

<div class="details-content">

Multi-indicator trend analysis tracking how chronic disease indicators evolve over time and comparing cross-topic performance.

### Questions Answered

- Which indicators are improving or worsening over the 2018–2022 period?
- How do YoY change rates compare across health topics?
- How do states perform across multiple indicators simultaneously?

### Visuals

- **Multi-Line Trend Chart:** Average Value by year and topic — all 9 topics on one timeline
- **Performance Summary Table:** Topic, Average Value, and YoY % Change (sortable)
- **State Performance Matrix:** Cross-tabulation of state × topic Average Values
- **YoY % Change Bar Chart:** Color-coded by direction (red = worsening, green = improving)
- **4 Slicers:** Topic, State, Stratification, Year

<figure class="project-figure">
  <img
    src="images/powerbi-dashboard-2.png"
    alt="Trends and Indicator Comparison dashboard with multi-line chart, summary table, state matrix, and YoY bars"
    loading="lazy"
  >
  <figcaption>
    Trends & Indicator Comparison — longitudinal tracking and cross-indicator performance (2018–2022).
    <a href="images/powerbi-dashboard-2.png">View full size</a>
  </figcaption>
</figure>

### Key Findings

- **Diabetes improved the most** — -12.57% YoY, suggesting public health interventions (screening, medication adherence, lifestyle modification) are producing measurable results
- **Alcohol and Tobacco are worsening** — +4.03% and +3.74% YoY respectively, signaling that risk factor mitigation efforts may be losing effectiveness
- **Cardiovascular Disease remains the highest-magnitude indicator** at 68.44 average — substantially higher than all other topics despite a modest -1.34% YoY improvement
- **Asthma is also improving** — -4.38% YoY, potentially linked to air quality improvements or better access to controller medications
- **State performance is heterogeneous** — a state ranking poorly for Alcohol may rank well for Diabetes, indicating that local policy environments create indicator-specific outcomes

</div>
</details>

<details>
  <summary><strong>Dashboard 3 — State Performance Analysis</strong></summary>

<div class="details-content">

State-level deep dive profiling individual state performance across all indicators, with national benchmarking, rankings, and demographic breakdowns.

### Questions Answered

- How does a selected state compare to the national average?
- Which topics contribute most to a state's overall burden?
- Where does a state rank nationally for each topic?
- How do demographic subgroups differ within a given indicator?

### Visuals

- **4 KPI Cards:** Average Value, National Average, State Rank, YoY Change
- **Decomposition Tree:** Average Value → Topic → Stratification (interactive drill-down)
- **Rankings Table:** Topic, Average Value, and State Rank
- **State vs. National Bar Chart:** Side-by-side comparison for each topic
- **Multi-Line Trend Chart:** Topic trends (2019–2022) for the selected state
- **3 Slicers:** State, Year, Topic

<figure class="project-figure">
  <img
    src="images/powerbi-dashboard-3.png"
    alt="State Performance Analysis dashboard with KPI cards, decomposition tree, rankings, bar chart, and trend lines (California selected)"
    loading="lazy"
  >
  <figcaption>
    State Performance Analysis — state profile with indicator breakdown, national benchmarking, and trend tracking (California selected).
    <a href="images/powerbi-dashboard-3.png">View full size</a>
  </figcaption>
</figure>

### Key Findings (California)

- **Overall average (13.80) is well below national average (17.43)** — positioning California among the lowest-burden states
- **Arthritis is California's highest-burden topic (20.84) but still ranks 50th nationally** — even its weakest indicator places it near the bottom of the rankings
- **Decomposition tree reveals demographic variation** — for Arthritis, Male (20.93) and Hispanic (17.98) both exceed the Overall population average (16.58)
- **Tobacco ranks 51st (10.46)** — consistent with California's aggressive tobacco control policies (high excise taxes, smoke-free workplace laws, sustained public education)
- **Alcohol ranks 36th** — California's highest/worst rank, making it the indicator with the most room for improvement

</div>
</details>

<details>
  <summary><strong>Dashboard 4 — Health Disparities</strong></summary>

<div class="details-content">

Demographic disparity analysis quantifying health inequities across population subgroups. Uses the Disparity Gap, Disparity Ratio, Group Max, and Group Min DAX measures to surface where aggregate averages mask significant between-group differences.

### Questions Answered

- How large is the gap between highest- and lowest-burden demographic groups?
- Which groups carry disproportionate disease burden?
- Are disparities widening, narrowing, or stable over time?
- Where does a state's overall average fall within its demographic range?

### Visuals

- **4 KPI Cards:** Disparity Gap, Disparity Ratio, Group Max, Group Min
- **Demographic Bar Chart:** Average Value by stratification group
- **Disparity Trend Chart:** Group Max, Group Min, and Disparity Gap over time (2019–2022)
- **Conditional Formatting Matrix:** State × Stratification with color-coded cells (red = higher burden, green = lower)
- **Gauge Chart:** Average Value positioned between Group Min and Group Max boundaries
- **3 Slicers:** Topic, State, Year

<figure class="project-figure">
  <img
    src="images/powerbi-dashboard-4.png"
    alt="Health Disparities dashboard with KPI cards, demographic bar chart, disparity trends, matrix, and gauge (New York, Alcohol)"
    loading="lazy"
  >
  <figcaption>
    Health Disparities — demographic gap quantification, trend tracking, and conditional formatting (New York, Alcohol selected).
    <a href="images/powerbi-dashboard-4.png">View full size</a>
  </figcaption>
</figure>

### Key Findings (New York — Alcohol)

- **Males carry the highest burden (20.0)** — consistent with national data showing higher rates of heavy and binge drinking among men
- **Age ≥65 shows dramatically lower burden (5.3)** — less than one-third of the Male group, reflecting lower consumption rates and survivorship effects
- **Disparity Ratio of 5.69** — the highest-burden group's rate is nearly 6x the lowest, indicating severe demographic inequality that population averages completely obscure
- **Disparity Gap is widening** — Group Max trended upward from 2019–2022 while Group Min stayed flat, driving the gap from ~15 to 23. Alcohol-related health inequities in New York are growing
- **Overall average (14.91) sits in the lower half of the demographic range** — closer to Group Min (4.90) than Group Max (27.90), meaning population-level statistics understate the burden on the most affected groups

</div>
</details>

<details>
  <summary><strong>Dashboard 5 — Action Prioritization</strong></summary>

<div class="details-content">

Action-oriented prioritization combining disease burden (Average Value) with trend direction (YoY % Change) to identify which states need the most urgent intervention. Uses a scatter plot priority matrix to classify states into quadrants.

### Questions Answered

- Which states have both high burden and worsening trends (highest priority)?
- How do states distribute across the burden-vs-trend matrix?
- Which topics contribute the most to overall chronic disease burden?
- Where should agencies focus limited resources for maximum impact?

### Visuals

- **Scatter Plot Priority Matrix:** YoY % Change (x) vs. Average Value (y) — states as color-coded bubbles, dashed reference lines creating four quadrants (upper-right = critical priority)
- **Topic Burden Bar Chart:** Topics ranked by Average Value
- **High-Priority States Table:** States in the high-burden + worsening quadrant with Average Value, YoY % Change, and State Rank
- **2 Slicers:** Topic (multi-select), Year (multi-select)

<figure class="project-figure">
  <img
    src="images/powerbi-dashboard-5.png"
    alt="Action Prioritization dashboard with scatter plot priority matrix, topic burden ranking, and high-priority states table"
    loading="lazy"
  >
  <figcaption>
    Action Prioritization — state triage using burden vs. trend quadrants, topic ranking, and priority identification (Alcohol, Diabetes, Nutrition/Physical Activity, Tobacco; 2020).
    <a href="images/powerbi-dashboard-5.png">View full size</a>
  </figcaption>
</figure>

### Key Findings

- **Most states cluster in low-burden + worsening** — absolute levels are moderate but trends are unfavorable, indicating conditions are deteriorating across the selected topics in 2020
- **Diabetes dominates overall burden** — Average Value roughly 4–5x higher than the next-highest topics, confirming it as the single largest contributor
- **Texas (60.82 avg, +16.64% YoY)** — high burden with double-digit worsening, firmly in the critical priority quadrant
- **California and Florida show alarming acceleration** — both exceed 37% YoY change, indicating rapid deterioration in these large-population states
- **South Carolina and Georgia are emerging priorities** — YoY rates above 33% with moderate burden suggest they could enter the high-burden zone within 1–2 years

</div>
</details>

<details>
  <summary><strong>Conclusion & Key Takeaways</strong></summary>

<div class="details-content">

### What the Data Revealed

Across five dashboards, the analysis surfaced distinct patterns at national, state, and demographic levels:

- **Uneven progress across topics** — Diabetes showed the strongest improvement (-12.57% YoY) while Alcohol (+4.03%) and Tobacco (+3.74%) moved in the wrong direction. Blanket public health strategies are insufficient; topic-specific interventions are required.
- **Cardiovascular Disease dominates burden** — at 68.44 average, it remains substantially higher than all other topics, reinforcing heart disease and stroke as the single largest chronic disease challenge nationally.
- **State performance varies by indicator** — California ranks 50th for Arthritis but 36th for Alcohol, showing that chronic disease outcomes are shaped by local policy environments rather than uniform system quality.
- **Demographic disparities are significant and widening** — in New York, the Alcohol disparity ratio reached 5.69 (highest-burden group nearly 6x the lowest), and the gap widened from ~15 to 23 between 2019–2022.
- **High-burden states with worsening trends need urgent attention** — Texas, California, and Florida combine high disease burden with rapid deterioration, placing them in the highest-priority quadrant.

### How the Dashboards Connect

Each page answers a distinct question, but findings compound together. The Executive Overview identified which topics carry the highest burden. Trends revealed whether those burdens are improving or worsening. State Performance enabled drill-down with national benchmarking. Health Disparities exposed that favorable averages can mask inequities. Action Prioritization synthesized burden and trend data into a two-dimensional triage framework.

### Skills Demonstrated

- **Power Query (M):** data import, type standardization, scope filtering, null handling, dimension table creation via duplicate-and-reduce
- **Data Modeling:** star schema with one fact table and four dimensions, one-to-many relationships, single-direction filter propagation, dedicated `_Measures` table
- **DAX:** SUM, AVERAGE, CALCULATE with ALL/ALLEXCEPT, RANKX, DATEADD, PREVIOUSYEAR, DIVIDE, MAX/MIN, VAR for multi-step formulas
- **Report Design:** 5 interactive pages with KPI cards, filled maps, scatter plot priority matrices, decomposition trees, conditional formatting, gauge charts, trend lines, and multi-select slicers

### Future Enhancements

- Composite Burden Index and Priority Score combining multiple indicators into a single state-level ranking
- Bookmarks for guided analysis flow between executive overview and detailed drill-downs
- Custom tooltips showing state profiles on map hover
- Publish to Power BI Service for web-based interactive access

</div>
</details>
