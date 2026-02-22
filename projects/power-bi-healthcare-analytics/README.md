# Power BI — CDC Chronic Disease Analytics

> An end-to-end Power BI project analyzing the CDC's U.S. Chronic Disease Indicators dataset to track health trends across 9 topics, rank state performance, and quantify demographic disparities — demonstrating Power Query ETL, star schema modeling, and DAX measure development.

**Tools:** Power BI Desktop · Power Query (M) · DAX · Star Schema Modeling

🔗 **[View Full Project Page](https://nadeaujonny.github.io/projects/power-bi-healthcare-analytics/)**

---

## Dashboard Previews

### Executive Overview
![Executive Overview Dashboard](projects/power-bi-healthcare-analytics/images/powerbi-dashboard-1.png)
*National KPI snapshot with geographic comparison, trend analysis, and interactive filtering.*

### Action Prioritization
![Action Prioritization Dashboard](projects/power-bi-healthcare-analytics/images/powerbi-dashboard-5.png)
*State-level triage using burden vs. trend priority matrix, topic burden ranking, and high-priority state identification.*

---

## Project Overview

This project analyzes the CDC's U.S. Chronic Disease Indicators (CDI) dataset using Power BI to track chronic disease trends across the United States, compare state-level performance against national benchmarks, and quantify health disparities across demographic groups. The analysis covers 9 chronic disease topics, 52 locations, and 7 years of surveillance data.

### Business Context

This project was designed to showcase practical Power BI skills used in analytics roles: building a complete ETL pipeline in Power Query, designing a normalized star schema data model, writing DAX measures for aggregations, time intelligence, rankings, and disparity calculations, and creating interactive report pages. The CDC dataset provides a real-world context that requires meaningful data transformation before analysis can begin.

---

## Project Goals

- Build a complete Power Query ETL pipeline to import, filter, and reshape raw CDC data into an analysis-ready star schema
- Design a normalized data model with one fact table and four dimension tables optimized for DAX performance
- Develop 10 DAX measures covering core aggregations, time intelligence, state rankings, and demographic disparity calculations
- Create interactive dashboard pages that track health trends, compare states, and surface demographic inequities
- Demonstrate end-to-end Power BI proficiency from raw data ingestion through polished report delivery

---

## Tools & Skills Demonstrated

| Skill Area | Details |
|---|---|
| **Power BI Desktop** | Data modeling, relationships, DAX authoring, report design, and interactivity |
| **Power Query (M)** | Data import, type standardization, scope filtering, null removal, dimension table creation via duplicate-and-reduce method |
| **DAX** | SUM, AVERAGE, CALCULATE with ALL/ALLEXCEPT, RANKX, DATEADD time intelligence, DIVIDE for safe division, VAR for readable multi-step formulas |
| **Data Modeling** | Star schema design with one-to-many relationships, single-direction filter propagation, separate `_Measures` table |
| **Visualization** | KPI cards, line charts, filled maps, bar charts, scatter plots, decomposition trees, matrix tables, gauge charts, conditional formatting |

---

## Dataset

- **Source:** [CDC Open Data — U.S. Chronic Disease Indicators (CDI)](https://data.cdc.gov/Chronic-Disease-Indicators/U-S-Chronic-Disease-Indicators-CDI-/g4ie-h725)
- **Format:** CSV in tidy/long format — one row per measurement observation
- **Granularity:** Year × Location × Indicator × Stratification
- **Topics (9):** Alcohol, Arthritis, Asthma, Cancer, Cardiovascular Disease, Chronic Kidney Disease, Diabetes, Nutrition/Physical Activity/Weight Status, Tobacco
- **Locations (52):** 50 U.S. states + DC + national aggregate (territories excluded)
- **Years (7):** 2015, 2016, 2018, 2019, 2020, 2021, 2022 (2017 absent from source data)

---

## Data Preparation (Power Query / ETL)

Transformed the raw CDC dataset using Power Query in Power BI Desktop. The goal was to convert a single wide CSV file into a normalized star schema with one fact table and four dimension tables.

1. **Import Raw Data** — preserved as `CDI_Raw` (unmodified reference copy)
2. **Filter & Scope** — filtered to 9 topics, 52 locations; removed null `DataValue` rows; set correct data types
3. **Create Dimension Tables** — used the duplicate-and-reduce method to produce clean lookup tables
4. **Build Fact Table** — selected only foreign key and metric columns from the filtered base query

![Power Query Applied Steps](projects/power-bi-healthcare-analytics/images/powerbi-power-query-cdi-raw.png)

---

## Data Model (Star Schema)

The star schema organizes data into a central fact table containing measurable values surrounded by dimension tables that provide descriptive context.

![Star Schema Data Model](projects/power-bi-healthcare-analytics/images/powerbi-data-connections.png)

### Fact Table

**Fact_CDI** (999+ rows, 7 columns) — one row per observation with foreign keys (`YearStart`, `LocationID`, `QuestionID`, `StratificationID1`) and metrics (`DataValue`, `LowConfidenceLimit`, `HighConfidenceLimit`).

### Dimension Tables

| Table | Rows | Key | Purpose |
|---|---|---|---|
| **Dim_Location** | 52 | `LocationID` | Geographic filtering, maps, state comparisons |
| **Dim_Indicator** | 9 | `QuestionID` | Indicator metadata — topic, question, data value type, unit |
| **Dim_Stratification** | 5 | `StratificationID1` | Overall population vs. demographic group breakdowns |
| **Dim_Date** | 7 | `YearStart` | Time-series trend analysis, YoY DAX calculations |

All relationships: **one-to-many** from dimension → `Fact_CDI`, single-direction filter propagation.

---

## Key DAX Measures

All 10 measures are organized in a dedicated `_Measures` table, grouped into three functional categories.

### Core Aggregations

```dax
Total Value = SUM(Fact_CDI[DataValue])

Average Value = AVERAGE(Fact_CDI[DataValue])

National Average =
CALCULATE(
    [Average Value],
    ALL(Dim_Location)
)

State Rank =
RANKX(
    ALL(Dim_Location[LocationDesc]),
    [Average Value], , DESC
)
```

### Time Intelligence

```dax
YoY Change =
VAR CurrentValue = [Average Value]
VAR PreviousValue =
    CALCULATE(
        [Average Value],
        DATEADD(Dim_Date[YearStart], -1, YEAR)
    )
RETURN
    CurrentValue - PreviousValue

YoY % Change = DIVIDE([YoY Change], [Previous Year Value])
```

### Disparity Analysis

```dax
Group Max = CALCULATE(MAXX(VALUES(Dim_Stratification[Stratification1]), [Average Value]))

Group Min = CALCULATE(MINX(VALUES(Dim_Stratification[Stratification1]), [Average Value]))

Disparity Gap = [Group Max] - [Group Min]

Disparity Ratio = DIVIDE([Group Max], [Group Min])
```

---

## Dashboard Pages (5)

### Page 1 — Executive Overview
At-a-glance KPIs, geographic comparisons, and trend context. Includes KPI cards, trend line chart, top 10 states bar chart, filled map, and slicers for Topic, Year, and Stratification.

### Page 2 — Trends & Indicator Comparison
Longitudinal view tracking year-over-year changes across all 9 topics. Includes multi-line trend chart, indicator performance summary table, state-by-indicator matrix, and YoY % change bar chart.

### Page 3 — State Performance Analysis
State-level profile with national benchmarking. Includes decomposition tree (Topic → Stratification drill-down), state rankings table, state vs. national average bar chart, and multi-line trend chart.

### Page 4 — Health Disparities
Demographic disparity analysis quantifying health inequities across population subgroups. Includes Disparity Gap/Ratio KPI cards, group burden bar chart, disparity trend line, conditional formatting matrix, and gauge chart.

### Page 5 — Action Prioritization
Two-dimensional triage framework combining burden level with trend direction. Includes scatter plot priority matrix (high burden + worsening = highest priority quadrant), topic burden ranking, and high-priority states table.

---

## Key Findings

- **Uneven progress across topics:** Diabetes showed the strongest improvement (-12.57% YoY), while Alcohol (+4.03%) and Tobacco (+3.74%) moved in the wrong direction
- **Cardiovascular Disease dominates burden:** average value of 68.44, substantially higher than all other topics
- **State performance varies by indicator:** California ranks 50th for Arthritis but 36th for Alcohol — outcomes are shaped by local policy environments
- **Demographic disparities are widening:** in New York, the Alcohol-related disparity ratio reached 5.69 (nearly 6x gap), and the disparity gap widened from ~15 in 2019 to 23 by 2022
- **High-priority states identified:** Texas (60.82 avg, +16.64% YoY), California (59.23 avg, +37.54% YoY), and Florida (38.09 avg, +37.41% YoY) combine high burden with rapid deterioration

---

## Project Structure

```
power-bi-healthcare-analytics/
├── index.md                                       # Project page (GitHub Pages)
├── README.md                                      # This file
├── data/
│   └── cdi_raw.csv                                # Raw CDC dataset
├── report/
│   └── CDC_Chronic_Disease_Analytics.pbix          # Power BI report file
└── images/                                        # Dashboard screenshots & model diagrams
    ├── powerbi-dashboard-1.png                     # Executive Overview
    ├── powerbi-dashboard-2.png                     # Trends & Indicator Comparison
    ├── powerbi-dashboard-3.png                     # State Performance Analysis
    ├── powerbi-dashboard-4.png                     # Health Disparities
    ├── powerbi-dashboard-5.png                     # Action Prioritization
    ├── powerbi-data-connections.png                # Star schema diagram
    ├── powerbi-power-query-cdi-raw.png             # Power Query raw import
    ├── powerbi-power-query-dim-location.png        # Dim_Location
    ├── powerbi-power-query-dim-indicator.png       # Dim_Indicator
    ├── powerbi-power-query-dim-stratification.png  # Dim_Stratification
    ├── powerbi-power-query-dim-date.png            # Dim_Date
    └── powerbi-power-query-fact-cdi.png            # Fact_CDI
```

---

## Future Enhancements

- Add composite Burden Index and Priority Score measures combining multiple indicators into a single state-level ranking
- Implement bookmarks for guided analysis flow between executive overview and detailed drill-downs
- Create custom tooltips showing state profiles on map hover
- Publish to Power BI Service for web-based interactive access

---

## Conclusion

This project demonstrates an end-to-end Power BI analytics workflow using real-world CDC chronic disease surveillance data. From raw CSV import through polished interactive dashboards, the analysis covers the full Power BI development lifecycle: Power Query ETL, star schema data modeling, DAX measure authoring, and multi-page report design — applied to a dataset spanning 9 chronic disease topics, 52 locations, and 7 years of public health surveillance.

Each dashboard was designed to answer a distinct set of business questions, but the findings compound when viewed together: the Executive Overview identifies national burden patterns, the Trends dashboard reveals improvement or deterioration, State Performance enables drill-down benchmarking, Health Disparities exposes hidden inequities, and Action Prioritization synthesizes everything into a triage framework for resource allocation.

---

## Author

**Jonathan Nadeau**

- 🌐 [Portfolio Website](https://nadeaujonny.github.io/)
- 💼 [LinkedIn](https://www.linkedin.com/in/nadeau-jonathan)
- 📧 [nadeau.jonny@gmail.com](mailto:nadeau.jonny@gmail.com)
