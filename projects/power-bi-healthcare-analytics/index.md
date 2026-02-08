---
layout: default
title: Power BI — CDC Chronic Disease Analytics
description: "End-to-end Power BI project analyzing CDC Chronic Disease Indicators — Power Query ETL, star schema dimensional modeling, 10 DAX measures, and interactive dashboards — to track U.S. health trends, rank states, and quantify demographic disparities across 9 chronic disease topics."
breadcrumbs:
  - title: Projects
    url: /projects/
  - title: Power BI — CDC Chronic Disease Analytics
---

<a href="/projects/" class="back-to-projects btn">← Back to Projects</a>

# Power BI — CDC Chronic Disease Analytics

> An end-to-end Power BI project analyzing the CDC's U.S. Chronic Disease Indicators dataset to track health trends across 9 topics, rank state performance, and quantify demographic disparities — demonstrating Power Query ETL, star schema modeling, and DAX measure development.

---

<details>
  <summary><strong>Project Overview</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Overview</h3>
  <p>
    This project analyzes the CDC's U.S. Chronic Disease Indicators (CDI) dataset using Power BI to track chronic disease
    trends across the United States, compare state-level performance against national benchmarks, and quantify health
    disparities across demographic groups. The analysis covers 9 chronic disease topics, 52 locations, and 7 years of
    surveillance data.
  </p>

  <h3>Why Power BI</h3>
  <p>
    This project was designed to showcase practical Power BI skills used in analytics roles: building a complete ETL pipeline
    in Power Query, designing a normalized star schema data model, writing DAX measures for aggregations, time intelligence,
    rankings, and disparity calculations, and creating interactive report pages. The CDC dataset provides a real-world context
    that requires meaningful data transformation before analysis can begin.
  </p>

  <h3>Project Goals</h3>
  <ul>
    <li>Build a complete Power Query ETL pipeline to import, filter, and reshape raw CDC data into an analysis-ready star schema</li>
    <li>Design a normalized data model with one fact table and four dimension tables optimized for DAX performance</li>
    <li>Develop 10 DAX measures covering core aggregations, time intelligence, state rankings, and demographic disparity calculations</li>
    <li>Create interactive dashboard pages that track health trends, compare states, and surface demographic inequities</li>
    <li>Demonstrate end-to-end Power BI proficiency from raw data ingestion through polished report delivery</li>
  </ul>

  <h3>Tools &amp; Skills Demonstrated</h3>
  <ul>
    <li><strong>Power BI Desktop:</strong> data modeling, relationships, DAX authoring, report design, and interactivity</li>
    <li><strong>Power Query (M):</strong> data import, type standardization, scope filtering, null removal, dimension table creation via duplicate-and-reduce method</li>
    <li><strong>DAX:</strong> SUM, AVERAGE, CALCULATE with ALL, RANKX, DATEADD time intelligence, ALLEXCEPT for group-level analysis, DIVIDE for safe division</li>
    <li><strong>Data Modeling:</strong> star schema design with one-to-many relationships, single-direction filter propagation, separate _Measures table</li>
    <li><strong>Visualization:</strong> KPI cards, line charts, filled maps, bar charts, matrix tables, conditional formatting</li>
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
    <li><strong>File type:</strong> CSV in tidy/long format — one row per measurement observation</li>
    <li><strong>Granularity:</strong> Year × Location × Indicator × Stratification</li>
    <li><strong>Structure:</strong> Each row represents a single data point for a specific year, state, health indicator, and demographic group</li>
  </ul>

  <h3>Scope Decisions</h3>
  <p>
    The full CDI dataset contains hundreds of thousands of rows spanning dozens of topics, all U.S. states and territories,
    and multiple stratification categories. To create a focused and meaningful analysis, I made the following scope decisions
    during the Power Query ETL phase:
  </p>

  <h4>9 Topics Selected</h4>
  <ul>
    <li><strong>Alcohol</strong></li>
    <li><strong>Arthritis</strong></li>
    <li><strong>Asthma</strong></li>
    <li><strong>Cancer</strong></li>
    <li><strong>Cardiovascular Disease</strong></li>
    <li><strong>Chronic Kidney Disease</strong></li>
    <li><strong>Diabetes</strong></li>
    <li><strong>Nutrition, Physical Activity, and Weight Status</strong></li>
    <li><strong>Tobacco</strong></li>
  </ul>
  <p>
    These 9 topics represent major chronic disease categories that collectively account for the leading causes of death
    and disability in the United States. They include both direct disease outcomes (Cancer, Cardiovascular Disease, Diabetes)
    and behavioral risk factors (Alcohol, Tobacco, Nutrition/Physical Activity) — enabling analysis of both upstream causes
    and downstream health impacts.
  </p>

  <h4>52 Locations</h4>
  <ul>
    <li>50 U.S. states + District of Columbia + United States (national aggregate)</li>
    <li>Territories excluded to maintain consistency in state-to-state comparisons and national benchmark calculations</li>
  </ul>

  <h4>7 Years</h4>
  <ul>
    <li>2015, 2016, 2018, 2019, 2020, 2021, 2022</li>
    <li><strong>Note:</strong> 2017 is missing from the dataset — this is a gap in the source data, not a filtering decision</li>
  </ul>

  <h4>Filtered Result</h4>
  <ul>
    <li><strong>999+ rows</strong> after removing territories, null data values, and out-of-scope topics</li>
    <li>Rows with null <code>DataValue</code> were removed to ensure clean aggregations in DAX measures</li>
  </ul>

</details>

---

<details>
  <summary><strong>Data Preparation (Power Query / ETL)</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <p>
    Before building the data model and DAX measures, I transformed the raw CDC dataset using <strong>Power Query</strong>
    in Power BI Desktop. The goal was to convert a single wide CSV file into a normalized star schema with one fact table
    and four dimension tables — each optimized for downstream analysis.
  </p>

  <h3>Step 1 — Import Raw Data</h3>
  <p>
    Imported the full CDI CSV file into Power BI and preserved it as <code>CDI_Raw</code>. This query serves as the
    unmodified reference copy of the original data — no manual edits or transformations applied.
  </p>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/powerbi-power-query-cdi-raw.png"
      alt="Power Query Editor showing the raw CDI dataset before transformation"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      <code>CDI_Raw</code> — original imported dataset preserved as-is before any transformations.
      <span style="display:block; margin-top:4px;">
        <a href="images/powerbi-power-query-cdi-raw.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Step 2 — Filter &amp; Scope</h3>
  <ul>
    <li>Filtered to 9 selected topics (Alcohol, Arthritis, Asthma, Cancer, Cardiovascular Disease, Chronic Kidney Disease, Diabetes, Nutrition/Physical Activity/Weight Status, Tobacco)</li>
    <li>Filtered to 52 locations (50 states + DC + national aggregate; territories excluded)</li>
    <li>Removed rows with null <code>DataValue</code> to prevent aggregation errors downstream</li>
    <li>Set correct data types: <code>YearStart</code> → Whole Number, <code>DataValue</code> → Decimal, <code>LowConfidenceLimit</code> → Decimal, <code>HighConfidenceLimit</code> → Decimal, text fields → Text</li>
  </ul>

  <h3>Step 3 — Create Dimension Tables</h3>
  <p>
    Used the <strong>duplicate-and-reduce method</strong>: duplicated the filtered base query, then removed all columns
    except the dimension attributes, and applied <em>Remove Duplicates</em> to produce clean lookup tables. This approach
    ensures every value in each dimension table has a corresponding record in the fact table.
  </p>

  <h4>Dim_Location (52 rows, 4 columns)</h4>
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/powerbi-power-query-dim-location.png"
      alt="Power Query showing Dim_Location dimension table with 52 rows"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      <code>Dim_Location</code> — 52 unique locations with <code>LocationAbbr</code>, <code>LocationDesc</code>, <code>Geolocation</code>, and <code>LocationID</code>.
      <span style="display:block; margin-top:4px;">
        <a href="images/powerbi-power-query-dim-location.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h4>Dim_Indicator (9 rows, 7 columns)</h4>
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/powerbi-power-query-dim-indicator.png"
      alt="Power Query showing Dim_Indicator dimension table with 9 rows"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      <code>Dim_Indicator</code> — 9 unique health indicators with <code>Topic</code>, <code>TopicID</code>, <code>Question</code>, <code>QuestionID</code>, <code>DataValueType</code>, <code>DataValueTypeID</code>, and <code>DataValueUnit</code>.
      <span style="display:block; margin-top:4px;">
        <a href="images/powerbi-power-query-dim-indicator.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <p>
    Each indicator maps a broad topic to a specific measurement question. For example:
  </p>
  <ul>
    <li><strong>Cancer</strong> → Invasive cancer incidence</li>
    <li><strong>Diabetes</strong> → Diabetic ketoacidosis mortality</li>
    <li><strong>Tobacco</strong> → Current cigarette smoking among adults</li>
  </ul>

  <h4>Dim_Stratification (5 rows, 4 columns)</h4>
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/powerbi-power-query-dim-stratification.png"
      alt="Power Query showing Dim_Stratification dimension table with 5 rows"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      <code>Dim_Stratification</code> — 5 unique demographic groups with <code>StratificationCategory1</code>, <code>Stratification1</code>, <code>StratificationCategoryID1</code>, and <code>StratificationID1</code>.
      <span style="display:block; margin-top:4px;">
        <a href="images/powerbi-power-query-dim-stratification.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <p>
    The stratification dimension enables both executive-level views (Overall) and demographic disparity analysis:
  </p>
  <ul>
    <li><strong>Overall</strong> — aggregate population values</li>
    <li><strong>Sex (Male)</strong></li>
    <li><strong>Race/Ethnicity (Hispanic)</strong></li>
    <li><strong>Age (Age >=65)</strong></li>
    <li><strong>Grade (Grade 10)</strong></li>
  </ul>

  <h4>Dim_Date (7 rows, 2 columns)</h4>
  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/powerbi-power-query-dim-date.png"
      alt="Power Query showing Dim_Date dimension table with 7 rows"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      <code>Dim_Date</code> — 7 unique year records with <code>YearStart</code> and <code>YearEnd</code> covering 2015–2022 (2017 absent from source data).
      <span style="display:block; margin-top:4px;">
        <a href="images/powerbi-power-query-dim-date.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Step 4 — Build Fact Table</h3>
  <p>
    Created <code>Fact_CDI</code> by selecting only the foreign key columns and metric columns from the filtered base
    query. This table contains the measurement data that connects to all four dimension tables through key relationships.
  </p>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/powerbi-power-query-fact-cdi.png"
      alt="Power Query showing Fact_CDI fact table with foreign keys and metric columns"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      <code>Fact_CDI</code> — 999+ rows with 7 columns: <code>YearStart</code>, <code>LocationID</code>, <code>QuestionID</code>, <code>StratificationID1</code>, <code>DataValue</code>, <code>LowConfidenceLimit</code>, <code>HighConfidenceLimit</code>.
      <span style="display:block; margin-top:4px;">
        <a href="images/powerbi-power-query-fact-cdi.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Why This ETL Approach Matters</h3>
  <ul>
    <li><strong>Accuracy:</strong> removing null values and territories prevents inflated or misleading aggregations in DAX measures</li>
    <li><strong>Performance:</strong> normalized dimension tables reduce data redundancy and optimize Power BI's VertiPaq storage engine</li>
    <li><strong>Maintainability:</strong> the duplicate-and-reduce method ensures dimension values always align with fact table records</li>
    <li><strong>Scalability:</strong> adding new years or topics requires updating scope filters rather than restructuring the model</li>
  </ul>

</details>

---

<details>
  <summary><strong>Data Model (Star Schema)</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>What Is a Star Schema</h3>
  <p>
    A star schema organizes data into a central <strong>fact table</strong> containing measurable values (metrics) surrounded
    by <strong>dimension tables</strong> that provide descriptive context (who, what, where, when). This structure is the
    standard for analytical data models in Power BI because it optimizes query performance, simplifies DAX measure writing,
    and creates predictable filter propagation across report visuals.
  </p>

  <h3>Model Architecture</h3>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/powerbi-data-connections.png"
      alt="Power BI data model diagram showing star schema with Fact_CDI connected to four dimension tables"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Star schema data model with <code>Fact_CDI</code> at the center connected to <code>Dim_Date</code>, <code>Dim_Location</code>, <code>Dim_Indicator</code>, and <code>Dim_Stratification</code>.
      <span style="display:block; margin-top:4px;">
        <a href="images/powerbi-data-connections.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Fact Table</h3>
  <p>
    <strong>Fact_CDI</strong> (999+ rows, 7 columns) — the central measurement table containing one row per observation.
  </p>
  <ul>
    <li><strong>Foreign keys:</strong> <code>YearStart</code>, <code>LocationID</code>, <code>QuestionID</code>, <code>StratificationID1</code></li>
    <li><strong>Metrics:</strong> <code>DataValue</code>, <code>LowConfidenceLimit</code>, <code>HighConfidenceLimit</code></li>
  </ul>

  <h3>Dimension Tables</h3>

  <h4>Dim_Location (52 rows, 4 columns)</h4>
  <ul>
    <li><strong>Key:</strong> <code>LocationID</code></li>
    <li><strong>Attributes:</strong> <code>LocationAbbr</code> (state abbreviation), <code>LocationDesc</code> (full state name), <code>Geolocation</code> (coordinates)</li>
    <li><strong>Purpose:</strong> enables geographic filtering, map visualizations, and state-level comparisons</li>
  </ul>

  <h4>Dim_Indicator (9 rows, 7 columns)</h4>
  <ul>
    <li><strong>Key:</strong> <code>QuestionID</code></li>
    <li><strong>Attributes:</strong> <code>Topic</code>, <code>TopicID</code>, <code>Question</code>, <code>DataValueType</code>, <code>DataValueTypeID</code>, <code>DataValueUnit</code></li>
    <li><strong>Purpose:</strong> provides indicator metadata including the specific measurement question, data value type, and unit of measurement for each topic</li>
  </ul>

  <h4>Dim_Stratification (5 rows, 4 columns)</h4>
  <ul>
    <li><strong>Key:</strong> <code>StratificationID1</code></li>
    <li><strong>Attributes:</strong> <code>StratificationCategory1</code>, <code>Stratification1</code>, <code>StratificationCategoryID1</code></li>
    <li><strong>Purpose:</strong> enables filtering between overall population values and specific demographic group breakdowns for disparity analysis</li>
  </ul>

  <h4>Dim_Date (7 rows, 2 columns)</h4>
  <ul>
    <li><strong>Key:</strong> <code>YearStart</code></li>
    <li><strong>Attributes:</strong> <code>YearEnd</code></li>
    <li><strong>Purpose:</strong> supports time-series trend analysis and year-over-year DAX calculations using DATEADD</li>
  </ul>

  <h3>Relationships</h3>
  <p>
    All relationships follow the same pattern: <strong>one-to-many</strong> from each dimension table to <code>Fact_CDI</code>,
    with <strong>single-direction</strong> filter propagation flowing from dimension to fact. This ensures:
  </p>
  <ul>
    <li>Slicer selections on any dimension (year, state, indicator, demographic group) correctly filter the fact table</li>
    <li>DAX measures using <code>CALCULATE</code> and <code>ALL</code> can override filter context predictably</li>
    <li>No circular dependencies or ambiguous filter paths exist in the model</li>
  </ul>

  <h3>Why This Structure Improves Performance and Analysis</h3>
  <ul>
    <li><strong>VertiPaq optimization:</strong> narrow dimension tables with low cardinality compress efficiently in Power BI's in-memory engine</li>
    <li><strong>DAX clarity:</strong> measures reference dimension attributes for context and fact columns for calculations — the separation makes formulas easier to write and debug</li>
    <li><strong>Filter propagation:</strong> one-to-many relationships ensure that slicers and cross-filters work consistently across all report pages</li>
    <li><strong>Reduced redundancy:</strong> descriptive text (state names, indicator descriptions) is stored once in dimensions rather than repeated across 999+ fact rows</li>
  </ul>

</details>

---

<details>
  <summary><strong>Key DAX Measures</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Measures Table</h3>
  <p>
    All DAX measures are organized in a dedicated <code>_Measures</code> table — a best practice in Power BI that
    separates calculation logic from data tables. This keeps the model clean, makes measures easy to find in the
    Fields pane, and prevents accidental aggregation of measure columns alongside raw data.
  </p>

  <p>
    The 10 measures below are grouped into three functional categories: <strong>Core Aggregations</strong>,
    <strong>Time Intelligence</strong>, and <strong>Disparity Analysis</strong>. Each measure is designed to
    leverage the star schema's filter context for accurate, context-aware calculations.
  </p>

  <h3>Core Aggregations</h3>
  <p>
    These foundational measures drive all primary visualizations — KPI cards, trend lines, bar charts, and map shading.
  </p>

  <h4>Total Value</h4>
  <pre><code class="language-dax">Total Value = SUM(Fact_CDI[DataValue])</code></pre>
  <p>Aggregate sum of all data values within the current filter context. Used for total-volume views where the sum across locations or indicators is meaningful.</p>

  <h4>Average Value</h4>
  <pre><code class="language-dax">Average Value = AVERAGE(Fact_CDI[DataValue])</code></pre>
  <p>Mean data value within the current filter context. This is the <strong>primary metric for analysis</strong> — most health indicators are rates or percentages where the average is more meaningful than the sum.</p>

  <h4>National Average</h4>
  <pre><code class="language-dax">National Average =
CALCULATE(
    [Average Value],
    ALL(Dim_Location)
)</code></pre>
  <p>
    Calculates the national benchmark by removing all location filters from the <code>[Average Value]</code> calculation.
    When a slicer selects a specific state, this measure still returns the all-states average — enabling state-vs-national
    comparison in KPI cards and reference lines.
  </p>

  <h4>State Rank</h4>
  <pre><code class="language-dax">State Rank =
RANKX(
    ALL(Dim_Location[LocationDesc]),
    [Average Value],
    ,
    DESC
)</code></pre>
  <p>
    Ranks states from highest to lowest average value (1 = highest value). Uses <code>ALL(Dim_Location[LocationDesc])</code>
    to evaluate every state regardless of the current filter context, then ranks them by <code>[Average Value]</code>.
    This enables dynamic state rankings that update as indicator and year selections change.
  </p>

  <h3>Time Intelligence</h3>
  <p>
    These measures track how health indicators change over time, supporting trend analysis and identifying whether
    conditions are improving or deteriorating year over year.
  </p>

  <h4>YoY Change</h4>
  <pre><code class="language-dax">YoY Change =
VAR CurrentValue = [Average Value]
VAR PreviousValue =
    CALCULATE(
        [Average Value],
        DATEADD(Dim_Date[YearStart], -1, YEAR)
    )
RETURN
    CurrentValue - PreviousValue</code></pre>
  <p>Calculates the absolute year-over-year change in average value. A positive result means the value increased from the prior year; a negative result means it decreased.</p>

  <h4>YoY % Change</h4>
  <pre><code class="language-dax">YoY % Change =
VAR CurrentValue = [Average Value]
VAR PreviousValue =
    CALCULATE(
        [Average Value],
        DATEADD(Dim_Date[YearStart], -1, YEAR)
    )
RETURN
    DIVIDE(CurrentValue - PreviousValue, PreviousValue)</code></pre>
  <p>
    Calculates the percentage year-over-year change using <code>DIVIDE</code> for safe division (returns blank instead of
    error when the prior year value is zero or missing). For example, a result of 0.05 means the indicator increased 5%
    compared to the previous year.
  </p>

  <h3>Disparity Analysis</h3>
  <p>
    These measures quantify the gap between the best-performing and worst-performing demographic groups within a given
    state, indicator, and year. Disparity analysis is critical in public health analytics because it reveals whether
    improvements in population-level averages are shared equitably across demographic groups or are masking widening
    inequities.
  </p>

  <h4>Group Max</h4>
  <pre><code class="language-dax">Group Max =
CALCULATE(
    MAX(Fact_CDI[DataValue]),
    ALLEXCEPT(Fact_CDI, Dim_Location, Dim_Indicator, Dim_Date)
)</code></pre>
  <p>
    Finds the highest data value among all demographic groups for a given location, indicator, and year combination.
    <code>ALLEXCEPT</code> removes the stratification filter while preserving location, indicator, and date context —
    so the measure scans across all demographic groups within the current state and indicator.
  </p>

  <h4>Group Min</h4>
  <pre><code class="language-dax">Group Min =
CALCULATE(
    MIN(Fact_CDI[DataValue]),
    ALLEXCEPT(Fact_CDI, Dim_Location, Dim_Indicator, Dim_Date)
)</code></pre>
  <p>
    Finds the lowest data value among all demographic groups for a given location, indicator, and year combination.
    The counterpart to <code>[Group Max]</code>, enabling the calculation of disparity measures below.
  </p>

  <h4>Disparity Gap</h4>
  <pre><code class="language-dax">Disparity Gap = [Group Max] - [Group Min]</code></pre>
  <p>
    The absolute difference between the highest and lowest performing demographic groups. A gap of 10 means the worst-performing
    group's rate is 10 percentage points (or units) higher than the best-performing group. Larger gaps indicate greater health inequity.
  </p>

  <h4>Disparity Ratio</h4>
  <pre><code class="language-dax">Disparity Ratio = DIVIDE([Group Max], [Group Min])</code></pre>
  <p>
    The relative inequality between demographic groups. A ratio of 2.0 means the highest-burden group's rate is 2x
    the lowest-burden group's rate. This measure is especially useful for comparing disparity severity across indicators
    with different scales — a 5-point gap means something different for an indicator measured in percentages versus one
    measured in rates per 100,000.
  </p>

  <h3>Why These Measures Matter for Health Analytics</h3>
  <ul>
    <li><strong>Core aggregations</strong> provide the foundation for every visualization — KPI cards, trend lines, maps, and ranking tables all depend on <code>[Average Value]</code>, <code>[National Average]</code>, and <code>[State Rank]</code></li>
    <li><strong>Time intelligence</strong> enables trend detection — policymakers need to know not just current values but whether conditions are improving or deteriorating, and at what rate</li>
    <li><strong>Disparity measures</strong> go beyond population averages to surface inequities — a state's overall rate may look acceptable while specific demographic groups face significantly higher burden, requiring targeted interventions</li>
  </ul>

</details>

---

<details>
  <summary><strong>Dashboard Page 1 — Executive Overview</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <p>
    A high-level population health snapshot designed for quick assessment of chronic disease indicators across the
    United States. This page provides at-a-glance KPIs, geographic comparisons, and trend context — enabling
    analysts and decision-makers to identify which indicators are most pressing and where to focus deeper analysis.
  </p>

  <h4>Business Questions Answered</h4>
  <ul>
    <li>Which chronic disease indicators have the highest or lowest average values nationally?</li>
    <li>How do states compare against each other for a selected health topic?</li>
    <li>What are the trends over time — are conditions improving or worsening year over year?</li>
  </ul>

  <h4>Visuals on This Page</h4>
  <ul>
    <li><strong>4 KPI Cards:</strong> Total Value, Average Value, National Average, and State Rank — providing immediate numeric context for the selected filters</li>
    <li><strong>Trend Line Chart:</strong> Average Value over time by year, showing directional movement across the 2015–2022 period</li>
    <li><strong>Top 10 Bar Chart:</strong> states ranked by Average Value, highlighting the highest-burden locations for the selected topic</li>
    <li><strong>Filled Map:</strong> geographic view with color-coded states based on Average Value, revealing regional patterns and clusters</li>
    <li><strong>3 Interactive Slicers:</strong> Topic, Year, and Stratification — enabling dynamic filtering across all visuals on the page</li>
  </ul>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/powerbi-dashboard-1.png"
      alt="Power BI Executive Overview dashboard showing KPI cards, trend line, top 10 bar chart, filled map, and slicers"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Executive Overview — national KPI snapshot with geographic comparison, trend analysis, and interactive filtering.
      <span style="display:block; margin-top:4px;">
        <a href="images/powerbi-dashboard-1.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h4>Key Insights</h4>
  <ul>
    <li><strong>State rankings shift by topic:</strong> states that rank highest for one health indicator (e.g., Tobacco use) often differ from those ranking highest for another (e.g., Cardiovascular Disease), revealing that chronic disease burden is not uniformly distributed</li>
    <li><strong>Trend patterns vary across indicators:</strong> some topics show steady year-over-year improvement while others plateau or worsen — the trend line makes it easy to distinguish improving conditions from stagnating ones</li>
    <li><strong>Geographic clustering is visible:</strong> the filled map reveals regional patterns where neighboring states share similar indicator values, suggesting that shared environmental, economic, or policy factors may drive health outcomes in those areas</li>
  </ul>

</details>

---

<details>
  <summary><strong>Dashboard Page 2 — Trend Analysis</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <p><em>Coming soon</em> — multi-year indicator comparisons identifying improving vs. worsening conditions.</p>

</details>

---

<details>
  <summary><strong>Dashboard Page 3 — State Performance</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <p><em>Coming soon</em> — geographic deep dive with rankings, drill-through, and state-vs-national benchmarks.</p>

</details>

---

<details>
  <summary><strong>Dashboard Page 4 — Health Disparities</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <p><em>Coming soon</em> — demographic gap analysis using Group Max/Min, Disparity Gap, and Disparity Ratio measures.</p>

</details>

---

<details>
  <summary><strong>Dashboard Page 5 — Action Prioritization</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <p><em>Coming soon</em> — composite scoring to identify highest-priority states for intervention.</p>

</details>

---

<details>
  <summary><strong>Conclusion &amp; Next Steps</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Work Completed</h3>
  <p>
    This project demonstrates the foundational stages of an end-to-end Power BI analytics workflow using real-world CDC
    chronic disease surveillance data. The work completed so far includes:
  </p>
  <ul>
    <li><strong>Power Query ETL pipeline:</strong> imported raw CDC data, applied scope filtering (9 topics, 52 locations, 7 years), removed null values, and built 4 normalized dimension tables using the duplicate-and-reduce method</li>
    <li><strong>Star schema data model:</strong> designed a fact table (<code>Fact_CDI</code>) connected to <code>Dim_Date</code>, <code>Dim_Location</code>, <code>Dim_Indicator</code>, and <code>Dim_Stratification</code> through one-to-many relationships with single-direction filtering</li>
    <li><strong>10 DAX measures:</strong> developed core aggregations (Total Value, Average Value, National Average, State Rank), time intelligence (YoY Change, YoY % Change), and disparity analysis (Group Max, Group Min, Disparity Gap, Disparity Ratio) in a dedicated <code>_Measures</code> table</li>
  </ul>

  <h3>Dashboard Development</h3>
  <p>
    The next phase of this project is building 5 interactive report pages that apply the data model and DAX measures
    to answer specific public health questions:
  </p>
  <ul>
    <li><strong>Executive Overview:</strong> national KPI snapshot with trend lines and state-level map shading</li>
    <li><strong>Trend Analysis:</strong> multi-year indicator comparisons identifying improving vs. worsening conditions</li>
    <li><strong>State Performance:</strong> geographic deep dive with rankings, drill-through, and state-vs-national benchmarks</li>
    <li><strong>Health Disparities:</strong> demographic gap analysis using Group Max/Min, Disparity Gap, and Disparity Ratio measures</li>
    <li><strong>Action Prioritization:</strong> composite scoring to identify highest-priority states for intervention</li>
  </ul>

  <h3>Skills Demonstrated</h3>
  <ul>
    <li><strong>Power Query:</strong> data import, type standardization, scope filtering, null handling, dimension table creation via duplicate-and-reduce method</li>
    <li><strong>Data Modeling:</strong> star schema design, one-to-many relationships, single-direction filter propagation, separate _Measures table</li>
    <li><strong>DAX:</strong> SUM, AVERAGE, CALCULATE with ALL/ALLEXCEPT, RANKX, DATEADD time intelligence, DIVIDE for safe division, VAR for readable multi-step formulas</li>
    <li><strong>Analytical Thinking:</strong> scoping decisions that balance breadth with focus, choosing metrics that enable both aggregate and demographic-level analysis</li>
  </ul>

  <h3>Future Enhancements</h3>
  <ul>
    <li>Build all 5 dashboard pages with interactive slicers, drill-through navigation, and conditional formatting</li>
    <li>Add composite Burden Index and Priority Score measures combining multiple indicators into a single state-level ranking</li>
    <li>Implement bookmarks for guided analysis flow between executive overview and detailed drill-downs</li>
    <li>Create custom tooltips showing state profiles on map hover</li>
    <li>Publish to Power BI Service for web-based interactive access</li>
  </ul>

</details>
