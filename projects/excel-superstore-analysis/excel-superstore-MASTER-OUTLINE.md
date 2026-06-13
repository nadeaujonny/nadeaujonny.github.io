# Master Outline & Study Guide
## Sales Dashboard — Superstore Dataset (Excel · Power Query · Pivot Tables · Dashboard)

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.
>
> **One sentence to anchor everything:** This is an end-to-end *Excel* analytics project —
> raw retail data is cleaned with **Power Query** into one refreshable "single source of
> truth" table, analyzed through **46 pivot tables** across five business questions, and
> delivered as an **interactive, slicer-driven dashboard**.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Business Context)](#2-why-this-project-exists-business-context)
3. [The Tech Stack & Skills](#3-the-tech-stack--skills)
4. [The Dataset — Superstore](#4-the-dataset--superstore)
5. [The Workbook Architecture](#5-the-workbook-architecture)
6. [The Power Query ETL Pipeline (the core technical piece)](#6-the-power-query-etl-pipeline-the-core-technical-piece)
7. [KPI Modeling](#7-kpi-modeling)
8. [Analysis 1 — Sales & Profit Trends Over Time](#8-analysis-1--sales--profit-trends-over-time)
9. [Analysis 2 — Product & Category Performance](#9-analysis-2--product--category-performance)
10. [Analysis 3 — Regional Performance & Market Efficiency](#10-analysis-3--regional-performance--market-efficiency)
11. [Analysis 4 — Customer Segment Analysis](#11-analysis-4--customer-segment-analysis)
12. [Analysis 5 — Returns Analysis & Revenue Impact](#12-analysis-5--returns-analysis--revenue-impact)
13. [The Dashboard](#13-the-dashboard)
14. [Excel Techniques Demonstrated](#14-excel-techniques-demonstrated)
15. [Key Results & Numbers](#15-key-results--numbers)
16. [Limitations & Honest Caveats](#16-limitations--honest-caveats)
17. [Design Decisions & Trade-offs (the "Why")](#17-design-decisions--trade-offs-the-why)
18. [Interview Q&A](#18-interview-qa)
19. [How to Walk Through This Project Live](#19-how-to-walk-through-this-project-live)
20. [Glossary](#20-glossary)

---

## 1. The 30-Second Pitch

This is an **end-to-end Excel analytics project** on the Superstore retail dataset. It
demonstrates the four skills a business analyst actually uses in Excel every day:
**Power Query (ETL)**, **pivot-table analysis**, **KPI modeling**, and **dashboard design**.

The workflow is a clean pipeline: raw `.xls` order data is imported and **preserved
untouched**, then cleaned and reshaped with **Power Query** into a refreshable table called
`Clean_Orders` — the single source of truth. From that one table, **46 pivot tables** drive
**five analyses**: sales & profit trends over time, product & category performance,
regional performance, customer-segment performance, and a returns-impact analysis. The
whole thing ends in a **profit-oriented, single-screen dashboard** with **connected slicers**
(Order Year, Order Month) that filter every chart at once.

The headline finding: **revenue grows steadily 2014–2017 but profit is volatile and
concentrated** — Technology and Office Supplies generate 93.6% of profit while Furniture
posts a 2.5% margin; two states (California, New York) produce ~52% of all profit; and
returns quietly erase roughly a full month of earnings.

**One-line version:** "I built an end-to-end Excel project — Power Query ETL into one
refreshable clean table, 46 pivot tables across five business analyses, and an interactive
slicer-driven dashboard — on the Superstore retail dataset."

**Deliverable:** `workbook/Superstore_Portfolio_Excel_Project.xlsx`

---

## 2. Why This Project Exists (Business Context)

**The simulated scenario.** The project plays the role of an analyst at a retail company
whose executives and category managers need to understand sales performance, profitability,
customer behavior, and operational efficiency — and want it in **Excel**, the tool every
business stakeholder already has open.

**The business questions it answers.** Five, one per analysis: (1) How are sales and profit
trending over time — is there seasonality or volatility? (2) Which categories and products
actually make money? (3) Which regions, states, and cities are profitable — and which lose
money? (4) Which customer segments are most valuable and most efficient? (5) How much do
returns cost us, and which products drive them?

**Why it's a strong portfolio project.** It is deliberately *not* a Python or SQL project —
it proves fluency in the tool most analyst roles still run on day-to-day. It shows the full
Excel analytics lifecycle: a real **ETL pipeline** (not manual copy-paste cleaning), a
**refreshable, maintainable** workflow, **pivot-driven analysis** with calculated fields,
defensible **KPI definitions**, and a **stakeholder-ready dashboard**. Each analysis ends in
concrete, costed **business recommendations** — it reads like analyst work, not a tutorial.

**The core principle behind the whole build:** *one clean source of truth.* The raw data is
never edited by hand; all cleaning lives in Power Query; every pivot, chart, and KPI reads
from the single `Clean_Orders` table. That is what makes the workbook **accurate**
(no double-counting), **consistent** (stable grouping), and **repeatable** (refreshable
with one click).

---

## 3. The Tech Stack & Skills

Everything is **Microsoft Excel** — but Excel used like a real analytics platform, not a
spreadsheet. The skills, and where each shows up:

| Skill area | What it covers | Where in the project |
|---|---|---|
| **Power Query (Get & Transform)** | The ETL layer — import, type enforcement, text cleanup, de-duplication, derived columns, merging (joining) tables | The 3 queries that produce `Clean_Orders` |
| **Pivot Tables** | Grouping, sorting, filtering, calculated fields | 46 pivot tables across 6 sheets |
| **Pivot Charts** | Visualizing pivot output | 49 charts |
| **Calculated Fields** | Metrics computed inside the pivot cache | "Profit Margin" and "Returns Sales Percentages" |
| **Worksheet formulas** | KPI summary cells | `SUM`, `COUNTA`, `SUMIF`, ratio formulas |
| **Slicers** | Interactive cross-chart filtering | Order Year + Order Month slicers on the Dashboard |
| **Date grouping** | Rolling time periods up to months/quarters/years | The pivot date-group fields |
| **Dashboard design** | Single-screen executive layout | The `Dashboard` sheet |

**The mental model:** Power Query is the *kitchen* (where the raw ingredients get prepped),
the pivot tables are the *cooking* (turning the clean table into answers), and the dashboard
is the *plating* (presenting it to executives). Each stage feeds the next, and the whole
chain is refreshable.

**Why "refreshable" is the recurring theme.** A spreadsheet where cleaning was done by hand
is a dead artifact — if the data updates, you redo everything. This project's pipeline can
take new raw data and regenerate every clean row, KPI, pivot, and chart via a single
**Data → Refresh All**. That repeatability is the difference between a one-off and a
*tool*.

---

## 4. The Dataset — Superstore

**What it is.** The **Superstore** dataset — a well-known public retail sample dataset
(it ships with Tableau and is widely used for analytics practice). It simulates a U.S.
office-supplies/furniture/technology retailer.

**The raw file** (`data/superstore_raw.xls`) has **three sheets**:

| Sheet | Rows | What it is |
|---|---|---|
| **Orders** | 9,994 order-line rows × 21 columns | One row per **order line item** (a product within an order) |
| **Returns** | 296 rows × 2 columns | `Returned` flag + `Order ID` — which orders were returned |
| **People** | 4 rows × 2 columns | `Person` + `Region` — the regional manager for each of the 4 regions |

**The Orders columns (the 21 raw fields):** Row ID, Order ID, Order Date, Ship Date, Ship
Mode, Customer ID, Customer Name, Segment, Country, City, State, Postal Code, Region,
Product ID, Category, Sub-Category, Product Name, Sales, Quantity, Discount, Profit.

**Grain to know cold:** one row = **one product line within one order**. A single Order ID
can span several rows (one per product). This is *why* de-duplication uses the composite
key **Order ID + Product ID** — that pair is what makes a row unique.

**Time range:** 2014–2017. **Three categories:** Technology, Office Supplies, Furniture.
**Three customer segments:** Consumer, Corporate, Home Office. **Four regions:** West, East,
Central, South.

**The People sheet** (Anna Andreadi → West, Chuck Magee → East, Kelly Williams → Central,
Cassandra Brandow → South) is carried into the workbook as a reference table but isn't a
driver of the five analyses — it's there for completeness.

---

## 5. The Workbook Architecture

The deliverable `Superstore_Portfolio_Excel_Project.xlsx` has **12 sheets**. Knowing the
sheet roles is knowing the project's structure.

| Sheet | Role |
|---|---|
| **Raw_Orders** | The original imported Orders data — **preserved, never hand-edited** (9,994 rows × 21 cols) |
| **Clean_Orders** | The Power Query output — the **single source of truth** (9,986 rows × 27 cols) |
| **Returns** | The returned-orders reference table (296 rows) |
| **People** | The region/manager reference table (4 rows) |
| **Analysis_1_KPIs** | Overall KPI summary block + trend pivots |
| **Analysis_2_Product_and_Category** | Category & product pivots |
| **Analysis_3_Regional_Performance** | Region / state / city pivots |
| **Analysis_4_Customer_Segment** | Segment pivots |
| **Analysis_5_Returns** | Returns pivots + return-rate formulas |
| **Pivots** | A working sheet holding many of the pivot tables that feed charts |
| **Dashboard** | The final single-screen interactive dashboard |
| **Clean_Orders_OLD** | An earlier version of the clean table (24 cols, pre-returns) — see §16 |

**The data flow through the sheets:** `Raw_Orders` → (Power Query) → `Clean_Orders` →
(46 pivot tables on the Analysis_* and Pivots sheets) → (49 pivot charts) → `Dashboard`.

**Two pivot caches power everything** — both holding **9,986 records**:
- Cache built on `Clean_Orders` — 31 fields, including the calculated field **"Returns
  Sales Percentages"** and the date-group fields **Months / Quarters / Years (Order
  Year-Month)**.
- A second cache built on the older `Clean_Orders_OLD` — includes the calculated field
  **"Profit Margin"**.

A pivot **cache** is the in-memory snapshot of the source data that pivots read from —
multiple pivot tables sharing one cache stay consistent and keep the file smaller.

**Honest note for interviews (see §16):** the workbook contains both `Clean_Orders` and a
leftover `Clean_Orders_OLD`, and the KPI summary block still references the old one. It's
harmless legacy from the build but worth knowing so it doesn't surprise you in a
walkthrough.

---

## 6. The Power Query ETL Pipeline (the core technical piece)

**This is the most technical part of the project — know it cold.** All data cleaning lives
in **Power Query** (Excel's "Get & Transform"), written in the **M language**. There are
**three chained queries**.

### 6.1 Why Power Query at all

Hand-cleaning data in cells is unrepeatable and error-prone. Power Query records every
transformation as an ordered list of **Applied Steps**. The benefits, stated the way the
project frames them: **accuracy** (de-duplication and type enforcement prevent inflated
KPIs), **consistency** (clean text + clean types mean pivots group correctly), and
**repeatability** (new raw data → *Data → Refresh All* → everything regenerates, no manual
rework).

### 6.2 Query 1 — `tbl_raw_orders` (clean the orders)

Source: the raw Orders table. Its Applied Steps, in order:

1. **Changed Type** — set every column to its correct data type: `Order Date` / `Ship
   Date` → date, `Postal Code` → **text** (to preserve leading zeros), `Sales` / `Profit` /
   `Discount` → number, `Quantity` / `Row ID` → integer, the rest → text.
2. **Trimmed Text** — `Text.Trim` on all 13 text columns to strip leading/trailing
   whitespace.
3. **Cleaned Text** — `Text.Clean` on the same columns to remove non-printable characters.
   *(Trim + Clean together are why pivots don't show "duplicate" labels caused by stray
   spaces or hidden characters.)*
4. **Removed Blank Rows** — drops fully-blank/incomplete rows that would distort totals.
5. **Removed Duplicates** — `Table.Distinct` on the **composite key `{Order ID, Product
   ID}`** so each row is a genuinely unique order line item (prevents double-counting).
6. **Added Custom — Order Year** — `Date.Year([Order Date])`.
7. **Added Custom1 — Order Month** — `Date.MonthName([Order Date])`.
8. **Added Custom2 — Order Year-Month** — `Date.ToText([Order Date], "yyyy-MM")` — the
   `YYYY-MM` string used for clean chronological time-series grouping.

### 6.3 Query 2 — `Returns` (clean the returns table)

Source: the raw Returns table (`Returned`, `Order ID`). Steps: **Changed Type** (both to
text), then **Removed Duplicates** on `Order ID` so each order appears at most once. This
matters — if an Order ID appeared twice in Returns, the upcoming join would fan out and
duplicate order rows.

### 6.4 Query 3 — `Clean_Orders` (join returns onto orders — the key step)

This is the query that produces the final 27-column source of truth. Its steps:

1. **Changed Type** — re-assert types on the cleaned orders table.
2. **Merged Queries** — `Table.NestedJoin` joins the cleaned orders to the `Returns` query
   on `Order ID`, **`JoinKind.LeftOuter`** — keep *every* order, attach return info where
   it exists.
3. **Expanded Returns** — pull the `Returned` column out of the nested join result.
4. **Added Custom — `Returned Flag`** — `if [Returns.Returned] = null then "No" else
   "Yes"`. The left-outer join leaves `null` for non-returned orders; this converts that
   to a clean **Yes/No** flag.
5. **Added Custom1 — `Returned Sales`** — `if [Returned Flag] = "Yes" then [Sales] else 0`.
6. **Added Custom2 — `Returned Profit`** — `if [Returned Flag] = "Yes" then [Profit] else
   0`. *(These two pre-computed columns make returns analysis a simple `SUM` later instead
   of a conditional aggregation.)*
7. **Removed Columns** — drop the now-redundant raw `Returns.Returned` column.

**The interview-critical point:** the orders↔returns link is done as a **Power Query merge
(a join)**, *not* an XLOOKUP in worksheet cells. That's deliberately better practice — the
join is part of the refreshable pipeline, it can't break when rows are sorted or inserted,
and it doesn't leave thousands of volatile formulas in the sheet. If an interviewer asks
"how did you connect orders to returns," the answer is: a **left-outer merge on Order ID in
Power Query**.

### 6.5 The output

`Clean_Orders`: **9,986 rows × 27 columns** — the 21 original fields, plus the 3 derived
date fields (`Order Year`, `Order Month`, `Order Year-Month`), plus the 3 returns fields
(`Returned Flag`, `Returned Sales`, `Returned Profit`). The raw Orders had **9,994** rows;
**8 duplicate order-line rows were removed** by the composite-key de-duplication.

---

## 7. KPI Modeling

Five core KPIs are defined once, explicitly, and used consistently everywhere. Defining a
KPI *precisely* (and being able to defend the definition) is itself an analyst skill.

| KPI | Definition / Formula | Notes |
|---|---|---|
| **Revenue** | `SUM(Sales)` | Total top-line sales |
| **Profit** | `SUM(Profit)` | Total bottom-line profit |
| **Profit Margin** | `Profit / Revenue` | Efficiency, not size — the key "is this *good* business" metric |
| **Units Sold** | `SUM(Quantity)` | Volume |
| **Return Rate** | `Returned Sales / Total Sales` | **Sales-based**, not count-based (see below) |

Supporting KPIs in the summary block: **Orders** = `COUNTA(Order ID)`, **Average Order
Value** = `Revenue / Orders`.

**How they're built in the workbook:**
- The **KPI summary block** (`Analysis_1_KPIs` sheet) uses plain worksheet formulas —
  `SUM(...[Sales])`, `SUM(...[Profit])`, `B3/B2` for margin, `COUNTA(...[Order ID])`,
  `SUM(...[Quantity])`.
- **Return rate** uses `SUMIF`: `SUMIF(Clean_Orders[Returned Flag],"=Yes",Clean_Orders[Sales]) / SUM(Clean_Orders[Sales])`.
- **Profit Margin** also exists as a **pivot calculated field** so it can be shown per
  category, region, or segment inside any pivot.

**The one KPI choice you must be able to defend — sales-based return rate.** Return Rate is
**returned *sales* ÷ total *sales***, not returned *order count* ÷ total *order count*. Why:
a count-based rate treats a returned $5 binder the same as a returned $5,000 copier. A
sales-based rate measures the **financial impact** of returns — which is what a business
actually cares about. The project states this explicitly, and it's a strong "I thought
about the metric, not just computed one" talking point.

---

## 8. Analysis 1 — Sales & Profit Trends Over Time

**Business question.** How have sales and profitability evolved 2014–2017? Is there a
trend, seasonality, or volatility that should inform forecasting, inventory, and cost
control?

**Method.** Pivot tables on `Clean_Orders` grouped by `Order Year-Month`; line charts for
monthly revenue and monthly profit; an overall KPI summary block for context.

**Key insights.**
- **Revenue grows steadily** from 2014 to 2017, with predictable seasonal peaks.
- **Profit is volatile** — large month-to-month swings, including **several negative-profit
  months**, even while revenue rises.
- **Margin pressure during growth** — revenue gains don't translate proportionally into
  profit, pointing at cost or discount problems.
- **Seasonality is predictable** — recurring high-demand periods are a planning opportunity.

**The "so what" — the recommendations.** Plan inventory 60–90 days ahead of seasonal peaks;
drill into the negative-profit months by category, discount level, and shipping method;
require manager approval for discounts above 20% (especially on low-margin Furniture); and
**put profit margin on the executive dashboard next to revenue** so hidden profit erosion
is visible.

**The teachable point.** "Revenue up, profit flat-or-down" is the single most important
pattern in the whole project — it reframes the business problem from *growth* to
*profitability*, and every later analysis is a hunt for where the profit leaks.

---

## 9. Analysis 2 — Product & Category Performance

**Business question.** Which categories and products drive revenue and profit — and where do
margin gaps signal a pricing, discounting, or product-mix problem?

**Method.** Category pivots for Revenue, Profit, and Profit Margin (`Profit / Sales`); a
product pivot sorted by Profit descending for a top-10; labeled pivot charts.

**The category numbers — memorize this table:**

| Category | Revenue | Profit | Profit Margin |
|---|---|---|---|
| Technology | $835,760 | $145,386 | 17.4% |
| Office Supplies | $718,318 | $122,247 | 17.0% |
| Furniture | $741,432 | $18,380 | 2.5% |
| **Total** | **$2,295,510** | **$286,014** | **12.5%** |

**Key insights.**
- **Technology + Office Supplies generate 93.6% of profit** ($267,633 of $286,014) on only
  **67.7% of revenue** — profit is concentrated in two categories.
- **Furniture is the margin problem** — 32.3% of revenue but only **6.4% of profit**, at a
  **2.5% margin ≈ 7× lower** than the top categories.
- **Profit is concentrated in a few products** — the top 10 products carry a
  disproportionate share.
- **One pricing policy can't fit all** — a 7× margin spread means uniform discounting is
  wrong by construction.

**Recommendations.** Protect the profit core (98%+ in-stock on Technology / Office
Supplies); fix Furniture by drilling into sub-category, discount, and shipping to find the
margin killers; set **category-specific discount caps** (Tech/Office 25%, Furniture 15%);
review and cut the bottom 20% of SKUs by profit.

**The teachable point.** This is the classic **revenue ≠ profit** lesson. Furniture *looks*
like a third of the business by revenue and is almost worthless by profit — a category
manager paid on revenue would never see it.

---

## 10. Analysis 3 — Regional Performance & Market Efficiency

**Business question.** Which regions, states, and cities drive profit — and which are
consistently *unprofitable*? Where are the efficiency (margin) gaps?

**Method.** Region pivots for Revenue, Profit, and Profit Margin; **Top 10 and Bottom 10**
States and Cities ranked by Profit; labeled pivot charts. The Top/Bottom-10 pattern is done
by sorting a pivot by Profit and using a value filter.

**Key insights.**
- **Profit is geographically concentrated** — **California and New York alone ≈ 52% of
  total profit**, which is a real geographic-risk concentration.
- **Regional margins vary** — West and East are more *efficient* (higher margin) than South
  and Central, hinting at operational differences worth copying.
- **Loss markets are concentrated** — the bottom 10 states are **$98K+ in collective
  losses**, led by **Texas (−$25,729), Ohio (−$16,959), Pennsylvania (−$15,560)**.
- **Dense urban markets perform best** — NYC, LA, Seattle top the city ranking.

**Recommendations.** Defend the California/New York profit base with service and inventory
priority; fix Texas/Ohio/Pennsylvania by drilling into category, discount, and shipping,
with 15% discount caps and small price increases; document and replicate West/East regional
practices in South/Central; add state- and city-level dashboards with monthly review.

**The teachable point.** Distinguish **size** (revenue/profit totals) from **efficiency**
(profit margin). A region can be large and inefficient, or small and efficient — and the
fix is different for each. And a few **negative-profit markets** can quietly drag down the
whole P&L.

---

## 11. Analysis 4 — Customer Segment Analysis

**Business question.** Which of the three customer segments (Consumer, Corporate, Home
Office) drive the most revenue and profit, and which are the most *efficient*? How should
growth, pricing, and retention be prioritized across them?

**Method.** A pivot grouped by `Segment` for Sales, Profit, and Profit Margin; comparison
charts for each.

**Key insights.**
- **Consumer — big but thin.** ~**50.6% of revenue** ($1,161,013) but the **lowest margin
  at 11.5%**. Because it's so large, every 1 margin point ≈ **$11,600** of profit — small
  fixes here are worth a lot.
- **Home Office — small but efficient.** The **highest margin at 14.0%** (~220 basis points
  above the 12.5% average) on only 18.7% of revenue.
- **Corporate — the balanced sweet spot.** A solid **13.0% margin** on substantial
  ($705,602) revenue — scalable profit.
- **Segments need different playbooks** — a ~250-basis-point margin spread means uniform
  discounting over-discounts the efficient segments and under-fixes Consumer.

**Recommendations.** Improve Consumer margin (discipline discounts, test 2–3% price
increases on commodities); grow the high-margin Home Office segment 25–30% with targeted
campaigns and bundles; scale Corporate with tiered volume contracts; track per-segment
margin targets monthly and tie incentives to **profitability, not revenue**.

**The teachable point.** "Biggest" and "best" are different questions. Consumer is the
biggest segment and the *worst* on efficiency — and because it's biggest, it's also where a
margin fix pays off most. A **basis point** = 0.01% — analysts use it to talk about margin
changes precisely.

---

## 12. Analysis 5 — Returns Analysis & Revenue Impact

**Business question.** How much revenue and profit do returns destroy? Which sub-categories
have the highest return rates? Which products drive the most return impact?

**Method.** This analysis depends entirely on the **Power Query merge** from §6.4 — the
`Returned Flag`, `Returned Sales`, and `Returned Profit` columns. Pivots compare Returned
vs. Not Returned for Sales and Profit; return-rate pivots by Month and by Sub-Category;
products ranked by Returned Sales and Returned Profit. The return-rate cells use `SUMIF` on
`Returned Flag = "Yes"`.

**Key insights.**
- **Returns erase roughly a month of profit** — **$180,504 in returned sales (7.86%)** and
  **$23,232 in lost profit (8.12%)**.
- **Return rate varies sharply by sub-category** — **Copiers 12.84%, Furnishings 10.48%,
  Appliances 9.42%** vs. **Binders 4.91%** — a **~2.6× spread**, which says the cause is
  product-specific, not company-wide.
- **Returns hit high-margin items harder** — profit impact (8.12%) **exceeds** revenue
  impact (7.86%), so returned items skew toward higher-margin products.
- **Impact is concentrated** — the top 10 products drive a disproportionate share, so
  targeted fixes beat broad policy changes.

**Recommendations.** Fix the worst sub-categories first (Copiers, Furnishings) with better
product descriptions, packaging, and vendor quality audits; target the top-10 return
products for quality and listing-accuracy issues; investigate return-spike months by
discount/shipping/region; and **track return rate as a standing KPI** with tiered targets
(complex products ≤ 8%, standard ≤ 6%, commodities ≤ 4%).

**The teachable point.** The fact that **profit impact > revenue impact** is a subtle,
strong insight — it means returns aren't random; they concentrate in the products you can
least afford to lose. That's the kind of observation that separates "I made a chart" from
"I read the data."

---

## 13. The Dashboard

The project ends in a **single-screen, profit-oriented dashboard** — the executive
deliverable.

**Design choices.**
- **Profit-oriented** — the dashboard leads with *profit*, not revenue, because the
  project's whole story is that revenue grows but profit is the real problem.
- **Single-screen** — everything fits one view, no scrolling, so it reads at a glance and
  screenshots cleanly for a portfolio.
- **Connected slicers** — two slicers, **Order Year** and **Order Month**, are wired to
  **every** chart on the dashboard at once. Pick a year and the entire dashboard refilters
  in sync.

**The core visuals:** Monthly Profit Trend, Return Profit Impact, Top Profit Sub-Categories,
Top Profit States, and Segment Profit — a one-screen synthesis of Analyses 1–5.

**How the slicers work technically.** A **slicer** is a visual filter control. When one
slicer is connected to multiple pivot tables that **share a pivot cache**, clicking it
filters all of them simultaneously — that "Report Connections" wiring is what makes the
dashboard feel interactive. The two slicers here filter on `Order Year` and `Order Month`.

**Why a dashboard at all.** Pivot tables answer questions for an analyst; a dashboard
answers them for an executive who will never build a pivot. The dashboard is the project's
**last mile** — turning analysis into a tool a stakeholder can self-serve.

---

## 14. Excel Techniques Demonstrated

A consolidated checklist of the actual Excel skills in the workbook — useful for "what did
you use?" questions.

**Power Query / M language**
- `Table.TransformColumnTypes` — data-type enforcement.
- `Text.Trim` + `Text.Clean` — whitespace and non-printable-character cleanup.
- `Table.SelectRows` — removing blank/invalid rows.
- `Table.Distinct` — de-duplication on a composite key.
- `Table.AddColumn` with `Date.Year` / `Date.MonthName` / `Date.ToText` — derived columns.
- `Table.NestedJoin` + `Table.ExpandTableColumn` — a left-outer **merge** (join).
- Conditional columns with `if … then … else` — the Yes/No flag and the returned-value
  columns.

**Pivot tables**
- Row grouping by date, category, region, state, city, sub-category, segment, product.
- Sorting + value filters → Top 10 / Bottom 10 rankings.
- **Calculated fields** — "Profit Margin" and "Returns Sales Percentages" computed inside
  the pivot cache.
- Date grouping into Months / Quarters / Years.
- Shared pivot caches for consistency and smaller file size.

**Worksheet formulas**
- `SUM`, `COUNTA` — KPI aggregation.
- `SUMIF` — conditional aggregation for the return rate.
- Structured table references (`Clean_Orders[Sales]`) rather than fragile cell ranges.
- Ratio formulas for margin and average order value.

**Visualization & presentation**
- 49 pivot charts with data labels.
- Slicers with multi-pivot report connections.
- A single-screen executive dashboard layout.

*(Accuracy note for interviews — see §16: the README lists "XLOOKUP" and "SUMIFS/COUNTIFS"
among the skills. The committed workbook actually uses a **Power Query merge** for the
orders↔returns lookup and **`SUMIF` / `COUNTA`** for the KPIs. The Power Query merge is the
*better* engineering choice than an XLOOKUP — frame it that way rather than treating it as a
gap.)*

---

## 15. Key Results & Numbers

Memorize the headline figures — interviewers will want concrete numbers.

| Metric | Value |
|---|---|
| Raw order-line rows | **9,994** |
| Clean rows after de-duplication | **9,986** (8 duplicates removed on Order ID + Product ID) |
| Time range | 2014–2017 |
| Total Revenue | **$2,295,510** (~$2.3M) |
| Total Profit | **$286,014** (~$286K) |
| Overall Profit Margin | **12.5%** |
| Returns reference rows | 296 returned orders |
| Pivot tables | 46 |
| Pivot charts | 49 |
| Slicers | 2 (Order Year, Order Month) |
| Workbook sheets | 12 |
| **Category profit concentration** | Technology + Office Supplies = **93.6% of profit** on 67.7% of revenue |
| **Furniture margin** | **2.5%** (vs. ~17% for the other two — a 7× gap) |
| **Geographic concentration** | California + New York ≈ **52% of total profit** |
| **Worst loss states** | Texas −$25,729 · Ohio −$16,959 · Pennsylvania −$15,560 |
| **Segment margins** | Home Office 14.0% · Corporate 13.0% · Consumer 11.5% |
| **Returns impact** | $180,504 returned sales (**7.86%**) · $23,232 lost profit (**8.12%**) |
| **Worst return sub-categories** | Copiers 12.84% · Furnishings 10.48% · Appliances 9.42% |

**The five takeaways (the story the project tells):**

1. **Revenue grows, profit doesn't.** Steady 2014–2017 revenue growth, but volatile profit
   with negative-profit months — the business problem is profitability, not growth.
2. **Profit is concentrated.** Two categories make 93.6% of profit; two states make ~52%.
   Concentration is both a strength to protect and a risk to manage.
3. **Furniture is the margin drag.** A third of revenue, 2.5% margin — uniform pricing
   hides it.
4. **Segments differ on efficiency.** Consumer is biggest and thinnest; Home Office is
   smallest and best. One discount policy can't serve all three.
5. **Returns quietly cost a month of profit.** ~8% of sales and profit, concentrated in a
   few products and sub-categories — and biased toward high-margin items.

---

## 16. Limitations & Honest Caveats

Volunteer these — knowing your project's limits signals maturity.

1. **The dataset is a public sample, not a real company.** Superstore is a synthetic
   practice dataset. The *methodology* (ETL, pivots, KPIs, dashboard) is the transferable
   skill; the specific numbers describe a fictional retailer.
2. **It's a static 2014–2017 snapshot.** No live feed. The pipeline is *refreshable* in
   principle — drop in new raw data and **Refresh All** — but the data itself doesn't update.
3. **Leftover `Clean_Orders_OLD` sheet.** The workbook still contains an earlier 24-column
   version of the clean table, and the **KPI summary block on `Analysis_1_KPIs` still
   references `Clean_Orders_OLD`** while the returns analysis references the current
   `Clean_Orders`. The two tables hold the same 9,986 rows so the KPI numbers are correct,
   but in a production workbook the old sheet would be deleted and all references pointed at
   one table. Know this so a code-walkthrough doesn't catch you off guard — and the honest
   framing is "build-time legacy I'd clean up before shipping to a stakeholder."
4. **Skill-list vs. workbook mismatch.** The README/portfolio page list "XLOOKUP" and
   "SUMIFS/COUNTIFS." The workbook actually uses a **Power Query merge** for the
   orders↔returns join and **`SUMIF`/`COUNTA`** for KPIs. Cite what's actually there — and
   note the Power Query merge is the stronger, more refreshable choice than an XLOOKUP.
5. **No statistical analysis.** This is descriptive analytics — totals, ratios, rankings,
   trends. There's no forecasting, regression, or significance testing; the recommendations
   are directional business judgment, not modeled predictions.
6. **Profit/Sales come pre-computed in the source.** The dataset already contains a `Profit`
   column; the project doesn't derive profit from cost — it aggregates what's given. Real
   margin analysis would start from cost and price components.
7. **The dashboard is desktop-Excel-dependent.** Slicer interactivity needs Excel desktop;
   the portfolio page shows static screenshots for everyone else.

---

## 17. Design Decisions & Trade-offs (the "Why")

Interviewers reward "why" answers. The deliberate choices and their rationale:

**Why preserve the raw data untouched?**
`Raw_Orders` is never hand-edited. It's the audit trail — you can always prove what the
source said and re-run cleaning from scratch. Editing raw data in place destroys
reproducibility.

**Why Power Query instead of cleaning in cells?**
Repeatability. Cell-by-cell cleaning is a one-time manual act; Power Query records every
step and re-applies them on refresh. New data → one click → fully regenerated clean table.
It also makes the cleaning *inspectable* — the Applied Steps list documents exactly what
was done.

**Why de-duplicate on Order ID + Product ID (a composite key)?**
Because the grain is one product line per order. `Order ID` alone isn't unique (an order
has many products); `Product ID` alone isn't unique (a product sells in many orders). The
*pair* is the true unique key — dedup on it and you remove genuine duplicates without
deleting legitimate rows.

**Why join returns in Power Query rather than XLOOKUP?**
A Power Query merge is part of the refreshable pipeline, survives row sorting/insertion, and
doesn't litter the sheet with thousands of volatile lookup formulas. A `LeftOuter` join also
*keeps every order* and simply attaches return info where it exists — exactly the right
semantics.

**Why a sales-based return rate, not count-based?**
A count-based rate weights a $5 return and a $5,000 return equally. Sales-based return rate
measures *financial* impact, which is the decision-relevant quantity.

**Why one `Clean_Orders` table feeding everything?**
A single source of truth means every pivot, chart, and KPI is computed from the same
9,986 rows. If analyses each cleaned their own copy, two charts could disagree. One table →
guaranteed consistency.

**Why pre-compute `Returned Sales` / `Returned Profit` as columns?**
Doing the `if Returned then Sales else 0` once in Power Query means returns analysis is a
plain `SUM` afterward — simpler pivots, and the logic lives in one auditable place.

**Why a profit-oriented, single-screen dashboard?**
The project's core finding is that profit — not revenue — is the problem. The dashboard
leads with profit to match the story, and single-screen so an executive absorbs it at a
glance.

---

## 18. Interview Q&A

Practice these out loud. Answers are written the way you'd actually speak.

**Q1. Give me the overview of this project.**
"It's an end-to-end Excel analytics project on the Superstore retail dataset. I imported
the raw order data, cleaned it with Power Query into one refreshable table called
Clean_Orders, then built about 46 pivot tables across five analyses — sales and profit
trends, product and category performance, regional performance, customer segments, and
returns. It ends in a single-screen, profit-oriented dashboard with slicers that filter
every chart at once. The point was to show the full Excel analyst workflow: ETL, pivot
analysis, KPI modeling, and dashboard design."

**Q2. Walk me through your data cleaning.**
"All of it is in Power Query, as three chained queries. The first takes the raw orders and
applies typed columns — dates as dates, postal code as text to keep leading zeros — then
trims and cleans the text columns, removes blank rows, removes duplicates on the composite
key Order ID plus Product ID, and adds three derived date fields: Order Year, Order Month,
and a YYYY-MM Year-Month. The second query cleans the Returns table and dedupes it on Order
ID. The third query merges returns onto orders with a left-outer join and adds a Yes/No
returned flag plus pre-computed returned-sales and returned-profit columns. The output is
Clean_Orders — 9,986 rows, the single source of truth."

**Q3. Why de-duplicate on two columns instead of one?**
"Because of the data's grain — one row is one product line within an order. An Order ID
isn't unique on its own; a single order has multiple product rows. A Product ID isn't
unique either; a product sells across many orders. The unique key is the pair — Order ID
plus Product ID. Dedup on the pair and you catch true duplicate line items without deleting
legitimate rows. It removed 8 rows, taking 9,994 down to 9,986."

**Q4. How did you connect the Returns data to the Orders data?**
"A merge in Power Query — a left-outer join on Order ID. Left-outer so every order is kept
and return information is attached only where it exists. After the join, non-returned
orders have a null, which I convert to a clean Yes/No returned flag. I did it in Power
Query rather than an XLOOKUP on purpose — the join is part of the refreshable pipeline, it
can't break when rows are sorted or inserted, and it doesn't leave thousands of volatile
formulas in the sheet."

**Q5. Why is Power Query better than just cleaning the data by hand?**
"Repeatability and auditability. Hand-cleaning is a one-time manual act — if the data
updates you redo everything, and there's no record of what you did. Power Query records
every transformation as an ordered list of Applied Steps. New data drops in, you hit
Refresh All, and the whole clean table, every pivot, and every chart regenerate. And anyone
can open the query and see exactly how the data was cleaned."

**Q6. What's your single most important finding?**
"Revenue grows steadily from 2014 to 2017, but profit is volatile and even goes negative
some months. The business problem isn't growth — it's profitability. And the profit that
does exist is concentrated: Technology and Office Supplies make 93.6% of profit on about
two-thirds of revenue, while Furniture is a third of revenue at a 2.5% margin. So my
headline recommendation was to manage the business on margin, not just revenue, and to fix
Furniture specifically."

**Q7. How did you define return rate, and why that way?**
"As returned sales divided by total sales — a sales-based rate, not a count-based one. A
count-based rate would treat a returned five-dollar binder the same as a returned
five-thousand-dollar copier. The sales-based version measures the actual financial impact
of returns, which is what the business cares about. It came out to 7.86% of sales, and
notably 8.12% of profit — returns destroy proportionally more profit than revenue, which
tells me returned items skew toward higher-margin products."

**Q8. What's a pivot calculated field, and where did you use one?**
"It's a metric computed inside the pivot cache from other fields, so it's available in any
pivot regardless of how you group. I used one for Profit Margin — Profit divided by Sales —
so I could show margin per category, region, or segment, and one for a returns sales
percentage. The alternative, computing margin in worksheet cells next to each pivot, breaks
when the pivot resizes; a calculated field travels with the pivot."

**Q9. How does the dashboard interactivity work?**
"Two slicers — Order Year and Order Month. A slicer is a visual filter, and when it's
connected to multiple pivot tables that share a pivot cache, clicking it filters all of
them at once. I connected both slicers to every pivot behind the dashboard charts, so
picking a year refilters the entire dashboard in sync. That shared-cache plus
report-connections wiring is what makes it feel like an app rather than static charts."

**Q10. Revenue versus profit — why do you keep separating them?**
"Because they tell opposite stories here. Furniture is a third of revenue and almost
nothing in profit. The Consumer segment is the biggest by revenue and the worst by margin.
Revenue measures size; profit margin measures whether the business is actually *good*. A
manager paid on revenue would never see the Furniture problem. Splitting the two is how you
find where money is leaking."

**Q11. What's a basis point, and why use it?**
"A basis point is one-hundredth of a percent — 0.01%. I used it for segment margins because
the differences are small but meaningful: Home Office at 14.0% is about 220 basis points
above the 12.5% average. Saying '220 basis points' is more precise than 'a bit higher' and
it's the standard way analysts talk about margin and rate changes."

**Q12. If you kept building this, what would you improve?**
"A few things. I'd delete the leftover Clean_Orders_OLD sheet and point the KPI block at
the single current table — that's build-time legacy I'd tidy before shipping. I'd add a
proper date-table for cleaner time intelligence. And if I had cost and price components
rather than a pre-computed Profit column, I'd build real margin-bridge analysis. Longer
term, this analysis is descriptive — a forecasting layer on the seasonal revenue pattern
would make it predictive."

**Q13. Why Excel and not Python or SQL for this?**
"Deliberate. Most analyst and business roles still run day-to-day reporting in Excel, and
stakeholders want deliverables they can open and click themselves. This project proves I
can use Excel as a real analytics platform — a recorded ETL pipeline, not manual cleaning;
pivot-driven analysis; an interactive dashboard. It's a different skill demonstration than
my SQL or Python projects, on purpose."

**Q14. How do you know your numbers are correct?**
"Three safeguards. The raw data is preserved untouched so I can always re-verify against
it. De-duplication on the composite key prevents double-counting, which is the most common
way Excel totals get inflated. And everything reads from one Clean_Orders table through
shared pivot caches, so every chart and KPI is computed from the same 9,986 rows — they
can't silently disagree."

---

## 19. How to Walk Through This Project Live

If asked to screen-share the workbook, use this order:

1. **Open the Dashboard first.** Lead with the outcome — show the profit-oriented
   single-screen layout, click the Year and Month slicers, watch every chart refilter.
2. **State the thesis** — "revenue grows but profit is volatile and concentrated; the
   dashboard is built around profit for that reason."
3. **Show `Raw_Orders`** — point out it's preserved, never edited; the audit trail.
4. **Open Power Query** (Data → Queries) — walk the three queries and the Applied Steps of
   `tbl_raw_orders`: typing, trim/clean, remove blanks, **dedup on Order ID + Product ID**,
   the three derived date columns. Then show the `Clean_Orders` query's **merge** with
   Returns and the Yes/No flag. This is the technical core — spend time here.
5. **Show `Clean_Orders`** — the 27-column single source of truth.
6. **Walk one analysis end to end** — Analysis 2 (Product & Category) is the strongest:
   the pivot, the calculated Profit Margin field, the 2.5%-margin Furniture finding.
7. **Show the returns analysis** — explain that the `Returned Flag` it relies on came from
   the Power Query merge, and the sales-based return-rate `SUMIF`.
8. **Close on a recommendation** — "manage on margin, fix Furniture, cap discounts by
   category." End on the business decision, not the spreadsheet.

**Pacing tip:** spend the most time in Power Query and on one full analysis. The Power
Query pipeline is the differentiated technical skill; the dashboard is the wow factor to
open and close with.

---

## 20. Glossary

- **Power Query (Get & Transform)** — Excel's built-in ETL tool; records data
  transformations as repeatable, refreshable Applied Steps.
- **M** — the language Power Query queries are written in.
- **Applied Steps** — the ordered list of transformations that make up a Power Query query;
  each step transforms the result of the previous one.
- **ETL** — Extract, Transform, Load; here, importing raw data, cleaning it, and loading
  the result into `Clean_Orders`.
- **Merge / join** — combining two tables on a shared key; this project does a
  **left-outer** merge of Orders to Returns on `Order ID`.
- **Left-outer join** — keeps every row from the left table (all orders) and attaches
  matching rows from the right table (returns) where they exist.
- **Composite key** — a unique identifier made of more than one column; here `Order ID +
  Product ID`.
- **Grain** — what one row of a table represents; here, one product line within one order.
- **De-duplication** — removing repeated rows; done on the composite key via
  `Table.Distinct`.
- **`Clean_Orders`** — the Power Query output table; the project's single source of truth.
- **Pivot table** — Excel's interactive aggregation tool; summarizes a table by grouping
  and aggregating fields.
- **Pivot cache** — the in-memory snapshot of source data that pivot tables read from;
  shared caches keep multiple pivots consistent.
- **Calculated field** — a metric computed inside the pivot cache (e.g., Profit Margin),
  usable in any pivot.
- **Slicer** — a visual filter control; connected to multiple pivots, it filters them all
  at once.
- **KPI** — Key Performance Indicator; the five core metrics (Revenue, Profit, Profit
  Margin, Units Sold, Return Rate).
- **Profit margin** — Profit ÷ Revenue; an efficiency metric, distinct from profit size.
- **Return rate (sales-based)** — Returned Sales ÷ Total Sales; measures the financial
  impact of returns.
- **Basis point** — one-hundredth of a percent (0.01%); used to describe small margin
  differences precisely.
- **Average Order Value (AOV)** — Revenue ÷ number of orders.
- **`SUMIF`** — a worksheet function that sums values meeting one condition; used for the
  return rate.
- **Structured table reference** — referring to a table column by name (`Clean_Orders[Sales]`)
  instead of a fixed cell range; robust to inserted rows.
- **Superstore** — the public sample retail dataset the project analyzes.

---

*This study guide documents the project as built. The authoritative references are the
workbook `Superstore_Portfolio_Excel_Project.xlsx` (its Power Query queries, pivot tables,
and Dashboard), the raw `superstore_raw.xls`, and the portfolio page `index.md`. When this
guide and the workbook disagree, the workbook wins.*