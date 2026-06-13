# Master Outline & Study Guide
## Power BI — CDC Chronic Disease Analytics (Power Query ETL · Star Schema · DAX · 5 Dashboards)

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.
>
> **One sentence to anchor everything:** This is an end-to-end **Power BI** project — raw
> CDC health data is shaped with **Power Query** into a **star-schema data model**, a set
> of **DAX measures** turns that model into metrics, and **five interactive dashboard
> pages** turn the metrics into decisions: the full Power BI development lifecycle, ETL →
> model → DAX → report.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Context)](#2-why-this-project-exists-context)
3. [The Tech Stack & Skills](#3-the-tech-stack--skills)
4. [The Dataset — CDC Chronic Disease Indicators](#4-the-dataset--cdc-chronic-disease-indicators)
5. [The Power Query ETL Pipeline](#5-the-power-query-etl-pipeline)
6. [The Star Schema Data Model](#6-the-star-schema-data-model)
7. [The DAX Measures (the core technical piece)](#7-the-dax-measures-the-core-technical-piece)
8. [Dashboard Page 1 — Executive Overview](#8-dashboard-page-1--executive-overview)
9. [Dashboard Page 2 — Trends & Indicator Comparison](#9-dashboard-page-2--trends--indicator-comparison)
10. [Dashboard Page 3 — State Performance](#10-dashboard-page-3--state-performance)
11. [Dashboard Page 4 — Health Disparities / Demographic Analysis](#11-dashboard-page-4--health-disparities--demographic-analysis)
12. [Dashboard Page 5 — Action Prioritization](#12-dashboard-page-5--action-prioritization)
13. [Key Findings](#13-key-findings)
14. [Power BI Concepts to Know Cold](#14-power-bi-concepts-to-know-cold)
15. [Limitations & Honest Caveats](#15-limitations--honest-caveats)
16. [Design Decisions & Trade-offs (the "Why")](#16-design-decisions--trade-offs-the-why)
17. [Interview Q&A](#17-interview-qa)
18. [How to Walk Through This Project Live](#18-how-to-walk-through-this-project-live)
19. [Glossary](#19-glossary)

---

## 1. The 30-Second Pitch

This is an **end-to-end Power BI project** analyzing the **CDC's U.S. Chronic Disease
Indicators (CDI)** dataset. It demonstrates the full Power BI development lifecycle: a
**Power Query ETL pipeline**, a **star-schema dimensional data model**, **DAX measure
development**, and **five interactive dashboard pages**.

The work: raw CDC health-surveillance data is imported, filtered, and reshaped in **Power
Query** from one wide CSV into a normalized **star schema** — one fact table (`Fact_CDI`,
999+ rows) and four dimension tables (Location, Indicator, Stratification, Date). Then
**10 DAX measures** — grouped into core aggregations, time intelligence, and disparity
analysis — turn that model into metrics. Finally, **five dashboard pages** answer five
escalating business questions: a national overview, trend tracking, state-by-state
performance, demographic disparities, and an action-prioritization triage matrix.

The analysis covers **9 chronic disease topics, 52 locations, and 7 years** of data, and
the dashboards surface concrete public-health findings — Diabetes improving, Alcohol and
Tobacco worsening, demographic disparity ratios near 6×, and a burden-vs-trend matrix that
flags which states need urgent intervention.

**One-line version:** "I built an end-to-end Power BI project on CDC chronic-disease data —
Power Query ETL into a star schema, 10 DAX measures, and five interactive dashboards — that
tracks health trends, benchmarks states, and quantifies demographic health inequities."

---

## 2. Why This Project Exists (Context)

**The premise.** Public-health agencies use chronic-disease surveillance data to decide
where to spend limited intervention budgets. But the CDC's CDI dataset arrives as one large,
flat CSV — it has to be *modeled* before it can be analyzed well. The project's job: turn
that raw file into a decision tool.

**What the project sets out to demonstrate** — and this is the honest framing — it is a
**skills-showcase project**. It exists to prove fluency in the four things a Power BI
analyst does every day: (1) build an ETL pipeline in Power Query, (2) design a proper
dimensional data model, (3) write DAX measures, and (4) design interactive reports. The CDC
dataset was chosen because it's real, public, and genuinely *needs* transformation before
analysis — so it exercises the whole toolchain rather than a clean toy dataset.

**The five business questions** — one per dashboard page, escalating in sophistication:
1. *Executive Overview* — what's the national picture, and how do states compare?
2. *Trends* — which conditions are improving vs. worsening over time?
3. *State Performance* — how does one state stack up against the national benchmark?
4. *Health Disparities* — are favorable averages hiding demographic inequities?
5. *Action Prioritization* — which states need intervention *first*?

**Why it's a strong portfolio project.** It is a complete, layered deliverable — each phase
builds on the last (ETL → model → DAX → report), and each dashboard adds analytical
sophistication, ending in a genuine decision framework (the burden-vs-trend matrix). It
reads like real BI-analyst work: not "I made a chart," but "I built a reporting product."

*(Cross-project note: this uses the same CDC CDI data family as the Julius AI project in
the portfolio — a useful contrast in interviews. Same data domain, completely different
tool and approach: rigorous Power BI dimensional modeling here vs. conversational AI EDA
there. It shows you pick the tool to fit the job.)*

---

## 3. The Tech Stack & Skills

Everything is **Microsoft Power BI** — but used as a full BI platform, across four distinct
skill layers.

| Layer | Tool / Language | What it does here |
|---|---|---|
| **ETL** | **Power Query (M language)** | Imports the raw CSV, filters scope, fixes data types, removes nulls, and builds the dimension and fact tables. |
| **Data model** | **Power BI modeling** (relationships, the model view) | The star schema — relationships, cardinality, filter direction. |
| **Calculations** | **DAX** (Data Analysis Expressions) | The 10 measures — aggregations, time intelligence, rankings, disparity math. |
| **Reporting** | **Power BI Desktop report canvas** | The five dashboard pages — KPI cards, maps, charts, slicers, interactivity. |

**The mental model — four sequential layers, each feeding the next:** Power Query is the
*prep kitchen* (raw data → clean tables), the data model is the *structure* (how the tables
relate), DAX is the *calculation engine* (tables → metrics), and the report is the
*presentation* (metrics → dashboards a stakeholder can use). A Power BI project is only as
good as its weakest layer — a beautiful report on a bad model produces wrong numbers.

**The skills, concretely:**
- **Power Query (M):** data import, type standardization, scope filtering, null removal,
  and the **duplicate-and-reduce method** for building dimension tables.
- **DAX:** `SUM`, `AVERAGE`, `CALCULATE` with `ALL` and `ALLEXCEPT`, `RANKX`, `DATEADD`
  time intelligence, `DIVIDE` for safe division, `VAR` for readable multi-step formulas.
- **Data modeling:** star schema, one-to-many relationships, single-direction filter
  propagation, a dedicated `_Measures` table.
- **Visualization:** KPI cards, line charts, filled maps, bar charts, matrix tables,
  scatter plots, decomposition trees, gauge charts, conditional formatting.

---

## 4. The Dataset — CDC Chronic Disease Indicators

**What it is.** The **U.S. Chronic Disease Indicators (CDI)** — a public dataset from the
**CDC** (`data.cdc.gov`, dataset `g4ie-h725`). It's the standardized national set of
chronic-disease surveillance measures.

**The format — and the key structural fact.** The raw CSV is in **tidy / "long" format**:
**one row per measurement observation.** Each row's grain is **Year × Location × Indicator
× Stratification** — one data point for a specific year, state, health indicator, and
demographic group. This long shape is *why* the project needs an ETL step: a long table has
to be split into a fact table and dimension tables before it models well.

**The scope decisions** (made during Power Query ETL — the full CDI dataset has hundreds of
thousands of rows):

| Dimension | Scope kept | Rationale |
|---|---|---|
| **Topics** | **9** — Alcohol, Arthritis, Asthma, Cancer, Cardiovascular Disease, Chronic Kidney Disease, Diabetes, Nutrition/Physical Activity/Weight Status, Tobacco | Major chronic-disease categories; a mix of **disease outcomes** (Cancer, CVD, Diabetes) and **behavioral risk factors** (Alcohol, Tobacco, Nutrition) — lets you analyze upstream causes *and* downstream impacts. |
| **Locations** | **52** — 50 states + DC + "United States" (national aggregate) | Territories excluded for consistent state-to-state comparison and clean national benchmarks. |
| **Years** | **7** — 2015, 2016, 2018, 2019, 2020, 2021, 2022 | **2017 is missing from the source data itself** — a data gap, not a filtering choice. (Know this — it's a likely interview question.) |

**The filtered result: 999+ rows** after removing territories, out-of-scope topics, and
rows with a null `DataValue`. The null-removal matters: a null `DataValue` would corrupt
the `SUM`/`AVERAGE` aggregations in DAX.

**Key raw columns to know:** `YearStart`/`YearEnd`, `LocationAbbr`/`LocationDesc`,
`Topic`/`Question` (the broad category and the specific measured question), `DataValueType`
and `DataValueUnit` (the *kind* of measure and its unit), `DataValue` (the number),
`Stratification1` (the demographic group), and `LowConfidenceLimit`/`HighConfidenceLimit`
(the statistical confidence interval around `DataValue`).

---

## 5. The Power Query ETL Pipeline

**This is the project's foundation — know the four steps.** All data shaping happens in
**Power Query** inside Power BI Desktop. The goal: turn one wide CSV into a normalized star
schema.

**Step 1 — Import & preserve the raw data.** The full CDI CSV is imported and kept as
`CDI_Raw` — an **unmodified reference copy**, no transformations. (Same discipline as
preserving raw data in any pipeline: it's the audit trail, and every other query is built
*from* a copy of it.)

**Step 2 — Filter & scope.** On a working copy of the data: filter to the **9 topics**,
filter to the **52 locations** (drop territories), **remove rows with a null `DataValue`**,
and **set correct data types** — `YearStart` → Whole Number, `DataValue` /
`LowConfidenceLimit` / `HighConfidenceLimit` → Decimal, text fields → Text. Correct types
matter because DAX aggregations and relationships behave wrongly on mistyped columns.

**Step 3 — Create the dimension tables (the "duplicate-and-reduce" method).** This is the
signature technique — be ready to explain it. For each dimension: **duplicate** the
filtered base query, **remove every column except that dimension's attributes**, then apply
**Remove Duplicates**. The result is a clean lookup table. Doing it this way (rather than
authoring dimension tables from scratch) **guarantees every value in a dimension has a
matching record in the fact table** — the dimension and fact tables can't drift apart
because they came from the same source.

The four dimensions built this way:
- **`Dim_Location`** — 52 rows (`LocationAbbr`, `LocationDesc`, `Geolocation`,
  `LocationID`).
- **`Dim_Indicator`** — 9 rows (`Topic`, `TopicID`, `Question`, `QuestionID`,
  `DataValueType`, `DataValueTypeID`, `DataValueUnit`).
- **`Dim_Stratification`** — 5 rows (`StratificationCategory1`, `Stratification1`,
  `StratificationCategoryID1`, `StratificationID1`).
- **`Dim_Date`** — 7 rows (`YearStart`, `YearEnd`).

**Step 4 — Build the fact table.** `Fact_CDI` is created from the filtered base query by
keeping **only the foreign-key columns and the metric columns** — descriptive text is
dropped because it now lives in the dimensions. Result: 999+ rows × 7 columns — four foreign
keys + three metrics.

**Why this ETL approach matters** (the four payoffs): **accuracy** (null/territory removal
prevents misleading aggregations), **performance** (narrow normalized tables compress well
in Power BI's storage engine), **maintainability** (duplicate-and-reduce keeps dimensions
aligned with the fact table), and **scalability** (adding a year or topic just means
editing a scope filter, not restructuring the model).

---

## 6. The Star Schema Data Model

**The star schema is the project's structural centerpiece. Know what it is and why it's
used — this is a guaranteed interview topic.**

### 6.1 What a star schema is

A **star schema** organizes data into a central **fact table** (the measurable numbers)
surrounded by **dimension tables** (the descriptive context — who, what, where, when). Drawn
out, the fact table is the center and the dimensions radiate from it like points of a star.
It is the **standard model shape for analytics in Power BI**.

### 6.2 This project's model

```
                ┌──────────────┐
                │  Dim_Date    │  7 rows
                │  (YearStart) │
                └──────┬───────┘
                       │ 1
                       │
        ┌──────────────▼──────────────┐
┌───────┴────────┐            ┌───────┴────────────┐
│ Dim_Location   │ 1        1 │ Dim_Indicator      │
│ 52 rows        ├───┐  ┌─────┤ 9 rows             │
│ (LocationID)   │   │  │     │ (QuestionID)       │
└────────────────┘   │  │     └────────────────────┘
                  ┌──▼──▼──────────────┐
                  │     Fact_CDI       │  999+ rows
                  │  4 foreign keys +  │
                  │  3 metric columns  │
                  └──────────▲─────────┘
                             │ 1
                  ┌──────────┴─────────┐
                  │ Dim_Stratification │  5 rows
                  │ (StratificationID1)│
                  └────────────────────┘
```

**The fact table — `Fact_CDI`** (999+ rows, 7 columns):
- **4 foreign keys:** `YearStart`, `LocationID`, `QuestionID`, `StratificationID1`.
- **3 metrics:** `DataValue`, `LowConfidenceLimit`, `HighConfidenceLimit`.

**The 4 dimension tables:** `Dim_Date` (7 rows, key `YearStart`), `Dim_Location` (52 rows,
key `LocationID`), `Dim_Indicator` (9 rows, key `QuestionID`), `Dim_Stratification` (5 rows,
key `StratificationID1`).

### 6.3 The relationships

Every relationship is the **same pattern: one-to-many, from the dimension (the "one" side)
to `Fact_CDI` (the "many" side), with single-direction filter propagation** flowing from
dimension → fact. That gives three guarantees:
- A slicer on any dimension (year, state, indicator, demographic group) correctly filters
  the fact table.
- DAX measures using `CALCULATE` with `ALL`/`ALLEXCEPT` can override the filter context
  *predictably*.
- There are no circular dependencies or ambiguous filter paths.

### 6.4 The `_Measures` table

All 10 DAX measures live in a dedicated, empty table called **`_Measures`** — a Power BI
best practice. It separates calculation logic from data tables, keeps measures easy to find
in the Fields pane, and prevents measure columns from being accidentally aggregated
alongside raw data.

### 6.5 Why the star schema improves things

- **Storage-engine optimization** — narrow, low-cardinality dimension tables compress
  efficiently in Power BI's in-memory **VertiPaq** engine.
- **DAX clarity** — measures pull *context* from dimensions and *numbers* from the fact
  table; that clean separation makes formulas easier to write and debug.
- **Predictable filter propagation** — one-to-many relationships make slicers and
  cross-filtering behave consistently across all five pages.
- **Reduced redundancy** — a state name or indicator description is stored *once* in a
  dimension, not repeated across 999+ fact rows.

---

## 7. The DAX Measures (the core technical piece)

**DAX (Data Analysis Expressions)** is Power BI's formula language. The project's **10
measures** all live in the `_Measures` table, in three functional groups. Know the *logic*
of each, the DAX function it showcases, and *why* it's written that way.

> **An accuracy note for interviews:** the project's two source documents (`index.md` and
> `README.md`) give slightly different DAX wordings for a couple of measures (`Group Max` /
> `Group Min`, and the exact form of `YoY % Change`), and the `.pbix`'s data model is a
> compressed backup, so the exact stored strings can't be machine-verified from the file.
> The **logic of every measure is consistent across both docs** — so in an interview,
> explain *what each measure computes and which DAX functions it uses*, and don't stake
> your answer on one exact string. The versions below are the documented ones.

### 7.1 Core Aggregations (the foundation for every visual)

**`Total Value`** — `SUM(Fact_CDI[DataValue])`. The aggregate sum of all data values in the
current filter context.

**`Average Value`** — `AVERAGE(Fact_CDI[DataValue])`. **The primary metric of the whole
project.** Most health indicators are *rates or percentages*, so an average is meaningful
where a sum is not. Almost every visual is built on this.

**`National Average`** —
```dax
National Average = CALCULATE([Average Value], ALL(Dim_Location))
```
Computes the all-states benchmark by **removing every location filter** with `ALL`. The
clever part: even when a slicer has a specific state selected, this measure *still* returns
the national figure — which is exactly what enables state-vs-national comparison on KPI
cards and reference lines. **This is the project's clearest demonstration of `CALCULATE` +
`ALL` overriding filter context.**

**`State Rank`** —
```dax
State Rank = RANKX(ALL(Dim_Location[LocationDesc]), [Average Value], , DESC)
```
Ranks states 1 = highest. `RANKX` iterates over **every** state (`ALL` ignores the current
filter) and ranks them by `[Average Value]`. Because it's a measure, the ranking
**recomputes dynamically** as the indicator or year slicer changes.

### 7.2 Time Intelligence (is it getting better or worse?)

**`YoY Change`** — the absolute year-over-year change, written with `VAR` for readability:
```dax
YoY Change =
VAR CurrentValue = [Average Value]
VAR PreviousValue = CALCULATE([Average Value], DATEADD(Dim_Date[YearStart], -1, YEAR))
RETURN CurrentValue - PreviousValue
```
`DATEADD(..., -1, YEAR)` shifts the date context back one year; the measure subtracts last
year from this year. Positive = the indicator rose; negative = it fell.

**`Previous Year Value`** *(a helper measure)* —
`CALCULATE([Average Value], PREVIOUSYEAR(Dim_Date[YearStart]))`. Returns the prior year's
average as a clean reference point. It's a behind-the-scenes helper used inside the percent
calculation — not placed on any visual.

**`YoY % Change`** — the percentage year-over-year change, using `DIVIDE` for **safe
division** (returns blank, not an error, when the prior year is zero or missing):
`DIVIDE([Average Value] - [Previous Year Value], [Previous Year Value])`. A result of 0.05
means the indicator rose 5% versus last year. *(The README writes this equivalently as
`DIVIDE([YoY Change], [Previous Year Value])` — same result.)*

*(On the count: the project describes "**10 DAX measures**." `Previous Year Value` is a
helper that supports `YoY % Change`; depending on whether you count the helper, the model
holds 10 or 11 measure definitions. Say "10 headline measures plus a helper" and you're
accurate.)*

### 7.3 Disparity Analysis (the project's most sophisticated DAX)

These four measures quantify the gap between the **best- and worst-off demographic groups**
for a given state, indicator, and year — the heart of the health-equity analysis.

**`Group Max`** / **`Group Min`** — find the **highest / lowest data value across all
demographic stratification groups**, while *holding location, indicator, and year fixed*.
The technique is the interesting part: the measure must scan across *stratifications* but
*not* collapse the location/indicator/year context. The documented DAX does this either via
`CALCULATE(MAX(Fact_CDI[DataValue]), ALLEXCEPT(Fact_CDI, Dim_Location, Dim_Indicator,
Dim_Date))` — `ALLEXCEPT` clears *every* filter **except** the listed dimensions, so the
stratification filter is removed and the others stay — or, equivalently, via
`MAXX(VALUES(Dim_Stratification[Stratification1]), [Average Value])`, which iterates the
stratification values explicitly. **Either way, the logic is: max/min over demographic
groups, holding the other three dimensions constant.**

**`Disparity Gap`** — `[Group Max] - [Group Min]`. The **absolute** difference between the
worst- and best-off groups. A gap of 10 means the hardest-hit group's rate is 10 units
higher.

**`Disparity Ratio`** — `DIVIDE([Group Max], [Group Min])`. The **relative** inequality. A
ratio of 2.0 means the highest-burden group's rate is 2× the lowest's. Why have both gap
*and* ratio: the gap is scale-dependent (10 points means different things for a percentage
vs. a rate-per-100,000); the ratio is scale-free, so it compares disparity severity *across*
indicators with different units.

### 7.4 Why these measures matter

The three tiers map to three analytical needs: **core aggregations** drive every KPI card,
trend line, and map; **time intelligence** answers "improving or worsening?"; and
**disparity measures** go beyond the population average to expose whether a good headline
number is hiding an inequity. That last tier is what lifts the project above a basic
dashboard.

---

## 8. Dashboard Page 1 — Executive Overview

**Purpose.** A high-level national snapshot — the at-a-glance page for quick assessment of
chronic-disease indicators across the U.S.

**Business questions:** Which indicators have the highest/lowest national values? How do
states compare for a selected topic? Are conditions improving or worsening over time?

**The visuals:**
- **4 KPI cards** — Total Value, Average Value, National Average, State Rank — immediate
  numeric context for the current filter selection.
- **Trend line chart** — Average Value over time (2015–2022), showing direction.
- **Top 10 bar chart** — states ranked by Average Value (the highest-burden states for the
  selected topic).
- **Filled map** — a color-shaded U.S. map of Average Value by state, revealing regional
  clusters.
- **3 slicers** — Topic, Year, Stratification — filter every visual on the page at once.

**Key insights:** state rankings **shift by topic** (a state worst for Tobacco isn't
necessarily worst for Cardiovascular Disease — burden isn't uniformly distributed); trend
patterns differ by indicator (some improve steadily, some plateau); and the filled map
shows **geographic clustering** — neighboring states with similar values, hinting at shared
environmental/economic/policy drivers.

**The teachable point.** This page is the "lead with the outcome" page — KPIs first, then
geography, then trend. It's deliberately the *simplest* of the five; each later page adds
analytical depth on top of it.

---

## 9. Dashboard Page 2 — Trends & Indicator Comparison

**Purpose.** Track how indicators evolve over time and compare all 9 topics in one view —
the difference between a *snapshot* and *direction & momentum*.

**Business questions:** Which indicators are improving vs. worsening? How do year-over-year
change rates compare across topics? Which states perform well (or badly) across *multiple*
indicators at once?

**The visuals:**
- **Multi-line trend chart** — Average Value by year and topic, all 9 topics on one
  timeline.
- **Indicator performance summary table** — a matrix of Topic, Average Value, and YoY %
  Change — a sortable scorecard of current state *and* momentum.
- **State-by-indicator matrix** — each state's Average Value broken out by topic — spot
  states that are consistently high or low across health domains.
- **YoY % Change bar chart** — horizontal bars **color-coded by direction** (red =
  worsening, green = improving).
- **4 slicers** — Topic, State, Stratification, Year.

**Key insights** (memorize the headline numbers): **Diabetes shows the strongest
improvement at −12.57% YoY**; **Alcohol (+4.03%) and Tobacco (+3.74%) are moving the wrong
way**; Asthma is improving (−4.38%); and **Cardiovascular Disease has the highest
magnitude — average value 68.44** — far above other topics even though it's slowly
improving (−1.34%).

**The teachable point.** The takeaway the project draws: chronic diseases **don't all move
in the same direction**, so blanket public-health strategies are insufficient —
**topic-specific intervention** is required. This page exists to surface *momentum*, which a
static overview can't show.

---

## 10. Dashboard Page 3 — State Performance

**Purpose.** A single-state deep dive — profile one state against the national benchmark
across every topic. (The page is titled "State Performance" in the report.)

**Business questions:** How does a chosen state's burden compare to the national average?
Which indicators contribute most to its overall value? Where does it rank nationally per
topic? How do demographic subgroups differ within the state? Are its indicators trending
up or down?

**The visuals:**
- **4 KPI cards** — Average Value, National Average, State Rank, YoY Change.
- **Decomposition tree** — starts at the state's overall Average Value and lets the user
  **drill down** interactively: first by Topic, then by Stratification group. This is the
  page's signature visual — it turns an aggregate number into an explorable hierarchy.
- **State rankings table** — Topic × Average Value × State Rank, a compact national-standing
  scorecard.
- **State-vs-national bar chart** — the selected state's Average Value beside the National
  Average for each topic — instantly shows which indicators beat or trail the benchmark.
- **Multi-line trend chart** — each topic's Average Value over recent years for that state.
- **3 slicers** — State, Year, Topic.

**Key insights (California, the worked example):** California's overall average (13.80) is
**well below the national 17.43** — a low-burden state. Even its *worst* topic (Arthritis,
20.84) still ranks 50th nationally (where higher rank = higher burden). Tobacco ranks 51st
(10.46) — consistent with California's aggressive tobacco-control history. And the
decomposition tree exposes within-state variation: for Arthritis, the Male (20.93) and
Hispanic (17.98) subgroups both exceed the Overall figure (16.58) — aggregate state numbers
*mask* demographic differences.

**The teachable point.** This page demonstrates **benchmarking** (`National Average` doing
its job) and **drill-down** (the decomposition tree). The "aggregate masks subgroups"
observation here is the bridge to Page 4.

---

## 11. Dashboard Page 4 — Health Disparities / Demographic Analysis

**Purpose.** Quantify and visualize **health inequities across demographic groups** within
a chosen state and topic. (The report tab is named "Demographic Analysis"; the project
write-up calls it "Health Disparities" — same page.)

**Business questions:** How large is the gap between the highest- and lowest-burden
demographic groups? Which groups carry the most/least burden? Is the disparity widening or
narrowing over time? Where does the state's overall average sit within the demographic
range?

**The visuals:**
- **4 KPI cards** — Disparity Gap, Disparity Ratio, Group Max, Group Min — the four
  disparity DAX measures, front and center.
- **Health burden by demographic group** — a horizontal bar of Average Value by
  Stratification1.
- **Disparity trend chart** — Group Max, Group Min, and Disparity Gap plotted across years —
  shows whether the gap is widening.
- **Demographic disparity matrix** — a Location × Stratification table with **conditional
  formatting** (red = higher burden, green = lower) for at-a-glance pattern spotting.
- **Gauge chart** — the state's overall Average Value positioned between Group Min and
  Group Max, so you can see where the average falls within the full demographic range.
- **3 slicers** — Topic, State, Year.

**Key insights (New York / Alcohol, the worked example):** the **Male group carries the
highest alcohol burden (≈20.0)**; the **Age ≥65 group is far lower (≈5.3)**; the
**Disparity Ratio is 5.69** — the worst-off group's rate is nearly **6× the best-off
group's** — and the **gap is widening**, from roughly 15 in 2019 to 23 by 2022. New York's
*overall* average (14.91) sits low in that range, **closer to Group Min than Group Max** —
meaning the population average is pulled down by lower-burden groups and *understates* the
burden on the most-affected groups.

**The teachable point.** This is the project's most important analytical idea:
**population-level averages can hide significant inequities.** A state can look fine on the
headline number while a specific demographic group bears disproportionate burden — and the
four disparity measures exist specifically to make that visible.

---

## 12. Dashboard Page 5 — Action Prioritization

**Purpose.** The decision page — synthesize everything into a **triage framework** that
flags which states need intervention first.

**Business questions:** Which states have *both* high burden *and* worsening trends? How do
states distribute across the burden-vs-trend space? Which topics contribute the most
burden? Where should limited public-health resources go?

**The signature visual — the State Priority Matrix (scatter plot):** a quadrant chart with
**YoY % Change on the x-axis** and **Average Value on the y-axis**, one bubble per state,
with dashed reference lines splitting it into **four priority zones**:
- **Upper-right = high burden + worsening → highest priority.**
- Upper-left = high burden + improving → monitor.
- Lower-right = low burden + worsening → watch.
- Lower-left = low burden + improving → lowest priority.

The whole point: ranking by burden *alone* misses **trend direction** — a moderate-burden
state deteriorating fast may need help sooner than a high-burden state that's stable.
Combining both dimensions into one visual is data-driven triage.

**The other visuals:** a **topic-burden ranking bar chart** (which topics drive the most
burden) and a **high-priority states table** (LocationDesc, Average Value, YoY % Change,
State Rank for the worst-quadrant states), plus 2 slicers (Topic, Year).

**Key insights (Alcohol/Diabetes/Nutrition/Tobacco, 2020):** **Diabetes dominates the topic
burden ranking** (≈4–5× the next topic); **Texas is a top-priority state** (Average Value
60.82, **+16.64% YoY**); **California (59.23, +37.54%) and Florida (38.09, +37.41%)** show
alarming trend acceleration; South Carolina and Georgia are *emerging* high-priority states
(moderate burden, but +33–38% YoY). *(Note: the "United States" national-aggregate bubble
appears as a dramatic outlier — it's a reference point, not a state, and isn't directly
comparable to individual states.)*

**The teachable point.** This page is the project's payoff — it converts five pages of
analysis into a **prioritized action list**, and it does it with a genuine 2-dimensional
framework (burden × trend), not just a sorted list.

---

## 13. Key Findings

The findings synthesized across all five pages — memorize the headline numbers:

1. **Uneven progress by topic.** Diabetes improved most (**−12.57% YoY**); Alcohol
   (**+4.03%**) and Tobacco (**+3.74%**) worsened. Blanket strategies don't work —
   topic-specific intervention is needed.
2. **Cardiovascular Disease dominates burden** — average value **68.44**, far above every
   other topic; heart disease and stroke remain the largest chronic-disease challenge.
3. **State performance varies by indicator** — California ranks 50th for Arthritis but 36th
   for Alcohol; outcomes are shaped by local policy and infrastructure, not uniform system
   quality.
4. **Demographic disparities are large and widening** — in New York, the Alcohol disparity
   ratio hit **5.69** (a nearly 6× gap), and the disparity gap grew from ~15 (2019) to ~23
   (2022). Population averages mask growing inequities.
5. **High-priority states identified** — **Texas** (60.82 avg, +16.64% YoY), **California**
   (59.23, +37.54%), and **Florida** (38.09, +37.41%) combine high burden with rapid
   deterioration — the highest-priority quadrant for intervention.

**The structural finding:** the five dashboards *compound*. The Overview finds national
burden patterns; Trends shows direction; State Performance enables benchmarked drill-down;
Health Disparities exposes hidden inequities; Action Prioritization turns it all into a
triage framework. Each page answers a distinct question, and together they walk a
stakeholder from "what's happening" to "what to do first."

---

## 14. Power BI Concepts to Know Cold

A Power BI / BI-analyst interview will probe these fundamentals.

**Power Query vs. DAX — the most important distinction.** **Power Query (M)** runs *once,
at data-refresh time* — it shapes and loads the data (ETL). **DAX** runs *continuously, at
report-interaction time* — it calculates metrics in response to filters and clicks. Rule of
thumb: **shape data in Power Query, calculate metrics in DAX.**

**Star schema** — a central fact table (numbers) + dimension tables (descriptive context),
related one-to-many. The standard analytical model shape (§6).

**Fact table vs. dimension table** — the fact table holds *measurements* and *foreign keys*
and has many rows; dimension tables hold *descriptive attributes* and have few rows.

**Cardinality** — the type of a relationship. This project uses **one-to-many** everywhere
(one dimension row → many fact rows).

**Filter direction / filter propagation** — which way filters flow across a relationship.
This project uses **single-direction** (dimension → fact): a slicer on a dimension filters
the fact table, not vice versa. Single-direction avoids ambiguous filter paths.

**Filter context** — the set of filters (from slicers, rows, columns, other visuals)
applying to a DAX calculation at a given moment. Almost all DAX behavior is about filter
context.

**`CALCULATE`** — the most important DAX function: it evaluates an expression under a
*modified* filter context. `CALCULATE([Average Value], ALL(Dim_Location))` = "compute the
average, but ignore location filters."

**`ALL` vs. `ALLEXCEPT`** — `ALL` removes *all* filters from a table/column; `ALLEXCEPT`
removes all filters *except* the ones you name. The project uses `ALL(Dim_Location)` for
the national benchmark and `ALLEXCEPT` to scan demographic groups while holding
location/indicator/year fixed.

**`RANKX`** — ranks rows by an expression; used for `State Rank`.

**Time intelligence** — DAX functions that shift the date context: `DATEADD` (shift by an
interval), `PREVIOUSYEAR` (the prior year). Require a proper date dimension.

**`DIVIDE`** — safe division: returns blank instead of an error on divide-by-zero. Used in
`YoY % Change` and `Disparity Ratio`.

**`VAR` / `RETURN`** — DAX variables for readable, multi-step formulas (used in `YoY
Change`).

**Measure vs. calculated column** — a **measure** is computed *on the fly* at query time,
responding to filter context (all 10 here are measures). A **calculated column** is
computed *once at refresh* and stored row-by-row. Measures for aggregations; columns for
row-level attributes.

**VertiPaq** — Power BI's in-memory, columnar storage/compression engine. Narrow,
low-cardinality dimension tables compress well in it — a reason star schemas perform well.

**`_Measures` table** — the convention of putting all measures in one dedicated empty table.

---

## 15. Limitations & Honest Caveats

Volunteer these — they show analytical maturity.

1. **`Average Value` averages across `DataValueType`s.** The CDI dataset mixes measure
   *types* — percentages, crude rates, rates per 100,000, counts. The project's primary
   metric is a plain `AVERAGE(DataValue)`, so a topic's "average value" can blend
   differently-scaled numbers. This is why some figures look large (CVD's 68.44, the
   national aggregate's 432.62) — they aren't all the same unit. It's the dataset's main
   analytical trap; a stricter version would filter to one `DataValueType` per comparison.
2. **The "United States" location is a national aggregate, not a state.** It's kept in the
   model as a benchmark row but isn't comparable to individual states — it shows up as an
   outlier on the Action Prioritization scatter, which the project flags.
3. **2017 is missing** from the source data — a real gap, so year-over-year math across
   2016→2018 spans two years, not one.
4. **Scoped to 999+ rows.** Nine topics, 52 locations, 7 years, and the demographic
   stratifications were deliberately narrowed (only 5 stratification groups) — a focused
   slice of a much larger dataset, chosen for a clean showcase, not a comprehensive study.
5. **Documentation drift on a couple of DAX measures.** The project's `index.md` and
   `README.md` give slightly different DAX wordings for `Group Max`/`Group Min` and
   `YoY % Change`, and the count is described as "10" while a `Previous Year Value` helper
   makes the model hold 11 measure definitions. The *logic* is consistent; cite logic, not
   one exact string (§7).
6. **Descriptive, not predictive.** The dashboards report what *is* and what *changed* —
   there's no forecasting or statistical modeling. The Action Prioritization matrix is a
   sensible heuristic, not a predictive model.
7. **No published Power BI Service version.** The deliverable is a `.pbix` file; a future
   step (in the project's own "future enhancements") is publishing to Power BI Service for
   web access.

---

## 16. Design Decisions & Trade-offs (the "Why")

Interviewers reward "why" answers. The deliberate choices and their rationale:

**Why a star schema instead of just using the flat CSV?**
A flat table forces descriptive text to repeat on every row, bloats the file, slows queries,
and makes DAX harder to write. A star schema stores each description once, compresses well
in VertiPaq, and gives clean, predictable filter propagation — it's the standard for a
reason.

**Why the duplicate-and-reduce method for dimensions?**
Because it *guarantees referential integrity by construction* — every dimension table is
literally a de-duplicated subset of the same filtered source the fact table came from, so a
dimension can't contain a value the fact table doesn't have, and vice versa. Authoring
dimensions separately would risk drift.

**Why one-to-many, single-direction relationships?**
Single-direction filtering (dimension → fact) is predictable and avoids ambiguous filter
paths and circular dependencies. Bidirectional filtering is occasionally needed but
introduces complexity and ambiguity — not warranted here.

**Why `Average Value` as the primary metric, not `Total Value`?**
Most health indicators are *rates and percentages*. Summing percentages across states is
meaningless; averaging them is interpretable. `Total Value` exists for the few genuine
count-style views, but `Average Value` drives almost everything.

**Why a dedicated `_Measures` table?**
It separates calculation logic from data, keeps measures findable, and prevents Power BI
from treating a measure like an aggregatable data column. Standard best practice.

**Why both a Disparity Gap and a Disparity Ratio?**
The gap (absolute) is intuitive but scale-dependent — 10 points means different things for
a percentage vs. a rate per 100,000. The ratio (relative) is scale-free, so it compares
disparity severity *across* indicators. Reporting both gives an absolute and a relative
read.

**Why five pages instead of one big dashboard?**
Each page answers one escalating question — overview → trend → state → disparity →
prioritize. Separating them keeps each page focused and lets the analysis build in
sophistication, ending in a genuine decision tool rather than a wall of charts.

**Why remove null `DataValue` rows in Power Query rather than handle them in DAX?**
Cleaning at the ETL stage means every downstream measure, on every page, is automatically
working with clean data — you fix it once, at the source, instead of defending against
nulls in every formula.

---

## 17. Interview Q&A

Practice these out loud. Answers are written the way you'd actually speak.

**Q1. Give me the overview of this project.**
"It's an end-to-end Power BI project on the CDC's Chronic Disease Indicators data. I used
Power Query to import a raw CSV and reshape it into a star schema — one fact table and four
dimension tables. Then I wrote ten DAX measures across three groups: core aggregations,
time intelligence, and disparity analysis. And I built five interactive dashboard pages
that escalate from a national overview to trend tracking, state benchmarking, demographic
disparities, and finally an action-prioritization matrix. It covers nine disease topics,
52 locations, and seven years of data."

**Q2. What is a star schema and why did you use one?**
"A star schema is a central fact table — the measurable numbers — surrounded by dimension
tables that hold descriptive context: who, what, where, when. Here the fact table is
Fact_CDI with the data values and foreign keys, and the four dimensions are Location,
Indicator, Stratification, and Date. I used it because it's the standard analytical model
shape — descriptive text is stored once instead of repeating across a thousand rows, the
narrow dimension tables compress efficiently in Power BI's VertiPaq engine, filter
propagation through one-to-many relationships is predictable, and DAX is much cleaner to
write when context comes from dimensions and numbers come from the fact table."

**Q3. Walk me through your Power Query ETL.**
"Four steps. First, import the raw CDI CSV and preserve it untouched as CDI_Raw — the
reference copy. Second, on a working copy, filter to my nine topics and 52 locations, remove
rows with a null DataValue, and set correct data types. Third, build the four dimension
tables with what I call the duplicate-and-reduce method — duplicate the filtered query, keep
only that dimension's columns, remove duplicates. Fourth, build the fact table by keeping
only the foreign keys and metric columns. The duplicate-and-reduce method matters because
it guarantees every dimension value has a matching fact record — they come from the same
source."

**Q4. What's the difference between Power Query and DAX?**
"Power Query is the ETL layer — it runs once, at data-refresh time, and shapes and loads the
data: filtering, type-setting, building tables. DAX runs continuously, at report-interaction
time — it calculates metrics in response to whatever filters and slicers are active. The
rule I follow is: shape the data in Power Query, calculate metrics in DAX. Cleaning the
null values, for example, belongs in Power Query so every downstream measure gets clean
data automatically."

**Q5. Explain your National Average measure.**
"National Average is CALCULATE of Average Value, with ALL applied to the Location
dimension. ALL removes every location filter, so even when a slicer has one state selected,
this measure still returns the all-states average. That's what makes state-versus-national
comparison possible — on a KPI card or a reference line, the state value moves with the
slicer but the national benchmark stays put. It's the clearest example in the project of
CALCULATE overriding filter context."

**Q6. How does your State Rank measure work?**
"State Rank uses RANKX over ALL of the location names, ranked by Average Value, descending.
The ALL is important — it makes RANKX evaluate every state regardless of the current filter,
so the ranking is computed against the full field. And because it's a measure, not a stored
column, the ranking recomputes dynamically: change the topic or year slicer and every
state's rank updates."

**Q7. What's the disparity analysis, and why does it matter?**
"It's the part of the project I'd most want to highlight. Population averages can look fine
while a specific demographic group bears far higher burden. So I built four measures: Group
Max and Group Min find the highest and lowest values across demographic groups while
holding location, indicator, and year fixed — I used ALLEXCEPT to clear just the
stratification filter and keep the others. Then Disparity Gap is the absolute difference and
Disparity Ratio is the relative one. In the data, New York's alcohol disparity ratio hit
5.69 — the worst-off group's rate was almost six times the best-off group's — and that gap
was widening year over year. The state's overall average completely hid that."

**Q8. Why do you have both a Disparity Gap and a Disparity Ratio?**
"Because they answer different questions. The gap is the absolute difference — intuitive,
but scale-dependent: a 10-point gap means something very different for an indicator measured
in percentages versus one measured as a rate per 100,000. The ratio is scale-free — a ratio
of 2 always means twice the burden — so it lets me compare disparity severity across
indicators with different units. Reporting both gives an absolute and a relative read."

**Q9. How did you handle time intelligence — year-over-year change?**
"YoY Change uses DATEADD on the date dimension to shift the context back one year, then
subtracts last year's average from this year's. I wrote it with VAR variables so it reads
as clear steps. YoY % Change converts that to a percentage using DIVIDE, which is safe
division — it returns blank instead of an error if the prior year is missing or zero. One
real wrinkle: 2017 is missing from the source data, so a year-over-year calculation across
that gap actually spans two years — worth knowing."

**Q10. What does the Action Prioritization page do, and why is it the most advanced page?**
"It's the decision page. The signature visual is a scatter-plot priority matrix — YoY %
Change on the x-axis, Average Value on the y-axis, one bubble per state, with reference
lines splitting it into four quadrants. The upper-right quadrant — high burden and
worsening — is the highest priority. The reason it's the most advanced page is that it
combines two dimensions: ranking by burden alone misses trend direction. A moderate-burden
state deteriorating fast can need help sooner than a stable high-burden state. It turns five
pages of analysis into a data-driven triage list."

**Q11. Why is Average Value your primary metric instead of Total Value?**
"Because most health indicators are rates and percentages, and summing percentages across
states is meaningless — averaging them is interpretable. Total Value exists for the genuine
count-style views, but Average Value drives almost every visual. I'd also be honest about a
limitation here: the CDI dataset mixes measure types — percentages, crude rates, rates per
100,000 — so a plain average can blend different scales. A stricter version would filter to
one DataValueType per comparison."

**Q12. What is a measure versus a calculated column?**
"A measure is calculated on the fly at query time and responds to the current filter
context — all ten of mine are measures, because aggregations like an average or a rank only
make sense relative to whatever's filtered. A calculated column is computed once at refresh
and stored row by row — you'd use that for a row-level attribute. Measures for
aggregations, columns for attributes."

**Q13. What would you improve or add next?**
"A few things. I'd add a composite Burden Index or Priority Score measure that combines
burden and trend into a single ranking, so the prioritization isn't just visual. I'd add
bookmarks for a guided flow between the overview and the drill-down pages. I'd build custom
tooltips so hovering a state on the map shows its full profile. And I'd publish to Power BI
Service so it's accessible on the web instead of as a desktop file."

**Q14. The CDC data is the same dataset family as another project in your portfolio — why
two?**
"Yes — my Julius AI project also uses CDC Chronic Disease Indicators data, and that's
deliberate. Same data domain, completely different approach. The Julius project explores it
conversationally with an AI tool — fast, exploratory. This Power BI project does rigorous
dimensional modeling — a star schema, DAX measures, a structured five-page report. Together
they show I pick the tool to fit the job: AI for quick exploration, Power BI for a
structured, repeatable reporting product."

---

## 18. How to Walk Through This Project Live

If asked to screen-share the .pbix, use this order:

1. **Open on the report pages first** — lead with the outcome. Show the Executive Overview,
   click a slicer, watch every visual refilter. Then flip through to the Action
   Prioritization scatter to show where it builds to.
2. **State the thesis** — "the project is the full Power BI lifecycle: Power Query ETL →
   star-schema model → DAX measures → five dashboards."
3. **Open Power Query** — walk the four ETL steps, and explain the **duplicate-and-reduce
   method** for the dimension tables. This is the foundation.
4. **Open the Model view** — show the **star schema**: Fact_CDI in the center, four
   dimensions, one-to-many single-direction relationships. Explain *why* it's shaped this
   way.
5. **Show the `_Measures` table and walk 2–3 DAX measures** — pick `National Average`
   (CALCULATE + ALL — filter-context override), `State Rank` (RANKX), and one disparity
   measure (`Group Max` — ALLEXCEPT). Explain the *logic*, not just the syntax.
6. **Walk the five pages in order** — narrate how each answers a distinct, escalating
   question: overview → trend → state → disparity → prioritize.
7. **Close on the disparity finding and the priority matrix** — the New York 5.69 ratio,
   and the burden-vs-trend triage. End on the decision, not the chart.

**Pacing tip:** spend the most time on the **star schema** and the **DAX measures** —
those are the differentiated technical skills. The report pages are the wow factor to open
and close with; the model and DAX are what an interviewer will dig into.

---

## 19. Glossary

- **Power BI Desktop** — Microsoft's BI authoring tool; where the whole project was built.
- **Power Query** — Power BI's ETL tool; shapes and loads data, written in the **M**
  language; runs at refresh time.
- **DAX (Data Analysis Expressions)** — Power BI's formula language for measures; runs at
  report-interaction time.
- **ETL** — Extract, Transform, Load — importing raw data, cleaning it, loading it into the
  model.
- **Star schema** — a central fact table surrounded by dimension tables; the standard
  analytical model.
- **Fact table** — the central table of measurements and foreign keys (`Fact_CDI`, 999+
  rows).
- **Dimension table** — a lookup table of descriptive attributes (Location, Indicator,
  Stratification, Date).
- **Duplicate-and-reduce method** — building a dimension by duplicating the base query,
  keeping only that dimension's columns, and removing duplicates.
- **Foreign key** — a column in the fact table that links to a dimension's key.
- **Relationship / cardinality** — the link between two tables; this project uses
  **one-to-many** (dimension → fact).
- **Filter direction / propagation** — the way a filter flows across a relationship; here,
  **single-direction**, dimension → fact.
- **Filter context** — the set of filters applying to a DAX calculation at a given moment.
- **Measure** — a DAX calculation evaluated on the fly at query time, responsive to filter
  context.
- **Calculated column** — a column computed once at refresh and stored per row.
- **`_Measures` table** — a dedicated empty table holding all measures; a best-practice
  convention.
- **`CALCULATE`** — the core DAX function; evaluates an expression under a modified filter
  context.
- **`ALL` / `ALLEXCEPT`** — DAX filter modifiers; `ALL` removes all filters from a
  table/column, `ALLEXCEPT` removes all *except* named ones.
- **`RANKX`** — a DAX function that ranks rows by an expression.
- **`DATEADD` / `PREVIOUSYEAR`** — time-intelligence functions that shift the date context.
- **`DIVIDE`** — safe division; returns blank instead of erroring on divide-by-zero.
- **`VAR` / `RETURN`** — DAX variables for readable multi-step formulas.
- **Time intelligence** — DAX calculations that compare across time periods (YoY, etc.).
- **VertiPaq** — Power BI's in-memory columnar compression/storage engine.
- **KPI card** — a visual showing a single headline number.
- **Filled map / choropleth** — a map with regions color-shaded by a metric.
- **Decomposition tree** — a Power BI visual for interactive hierarchical drill-down.
- **Conditional formatting** — color-coding table cells by value (red/green) for
  at-a-glance reading.
- **Gauge chart** — a visual showing a value within a min–max range.
- **Slicer** — an on-canvas filter control.
- **Star schema vs. flat table** — the modeled (normalized) vs. the raw (one wide table)
  shape of the data.
- **CDI** — CDC U.S. Chronic Disease Indicators; the source dataset.
- **Stratification** — a demographic breakdown of a measure (Overall, Sex, Race/Ethnicity,
  Age, Grade).
- **Disparity Gap / Ratio** — the absolute / relative difference between the highest- and
  lowest-burden demographic groups.

---

*This study guide documents the project as built. The authoritative references are the
Power BI workbook `Power_BI_Project_CDC_Healthcare_Data.pbix` (its Power Query queries,
data model, and DAX measures), the portfolio page `index.md`, and `README.md`. The `.pbix`
data model is a compressed backup, so exact M/DAX strings can't be machine-verified from
the file — where the two write-ups differ, this guide notes it and favors describing the
consistent underlying logic. When this guide and the workbook disagree, the workbook wins.*