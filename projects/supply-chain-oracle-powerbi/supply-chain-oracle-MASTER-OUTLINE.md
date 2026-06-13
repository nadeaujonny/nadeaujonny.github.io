# Master Outline & Study Guide
## Supply Chain Analytics — Oracle SQL → Excel → Power BI (Demand Forecasting, Inventory Optimization & MRP)

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.
>
> **One sentence to anchor everything:** This is an **end-to-end, automated supply-chain
> analytics pipeline** — raw order data is loaded into an **Oracle** database, normalized
> and processed by **stored procedures and an MRP simulation**, transformed through **Excel
> Power Query**, modeled and forecast in **Excel**, and delivered as a **six-page Power BI
> dashboard** — designed as a **closed-loop system** where the dashboard's recommendations
> feed back into the database and the next refresh reflects them.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Context)](#2-why-this-project-exists-context)
3. [The Tech Stack — Three Layers](#3-the-tech-stack--three-layers)
4. [The Dataset — DataCo Smart Supply Chain](#4-the-dataset--dataco-smart-supply-chain)
5. [The Automation Architecture (the Closed Loop)](#5-the-automation-architecture-the-closed-loop)
6. [Phase 1–2 — Oracle SQL: Schema, Views, Stored Procedure & MRP](#6-phase-12--oracle-sql-schema-views-stored-procedure--mrp)
7. [Phase 3 — Power Query ETL & Custom M Functions](#7-phase-3--power-query-etl--custom-m-functions)
8. [Phase 4 — Excel: Forecasting, ABC/XYZ, EOQ, Write-Back](#8-phase-4--excel-forecasting-abcxyz-eoq-write-back)
9. [Phase 5 — The Power BI Dashboard (6 Pages)](#9-phase-5--the-power-bi-dashboard-6-pages)
10. [Key Findings](#10-key-findings)
11. [Supply Chain & Technical Concepts to Know Cold](#11-supply-chain--technical-concepts-to-know-cold)
12. [Limitations & Honest Caveats](#12-limitations--honest-caveats)
13. [Interview Q&A](#13-interview-qa)
14. [How to Walk Through This Project Live](#14-how-to-walk-through-this-project-live)
15. [Glossary](#15-glossary)

---

## 1. The 30-Second Pitch

This project is a **complete, automated supply-chain analytics pipeline** — it spans three
tools and the full workflow of a real supply-chain analyst. It uses the **DataCo Smart
Supply Chain dataset** (~180,000 order records) and moves it through five phases:

1. **Oracle SQL** — load the flat CSV, normalize it into a relational schema, write
   extraction queries and reporting views, and build a **stored procedure with an MRP
   simulation** scheduled to run nightly.
2. **Power Query ETL** — transform the data with **custom M functions** and parameters.
3. **Excel analysis** — **demand forecasting** (ETS, moving averages), **ABC/XYZ
   classification**, and **inventory optimization** (EOQ, safety stock via Solver).
4. **Forecast write-back** — push the Excel forecasts *back into* Oracle so the MRP
   procedure consumes them.
5. **Power BI** — a **six-page interactive dashboard** with a star-schema model, DAX
   measures, data alerts, and Row-Level Security.

What distinguishes it is the **automation and the closed loop**: every stage is built as a
*repeatable, refreshable system*, and the dashboard's recommendations feed back into Oracle
master data so the next refresh cycle reflects them automatically. It answers the core
questions of supply-chain management — *How much should we make? When do we reorder? Are we
delivering on time? Where are the bottlenecks?*

**One-line version:** "I built an end-to-end automated supply-chain analytics pipeline —
Oracle SQL with stored procedures and an MRP simulation, Power Query ETL with custom
functions, Excel demand forecasting and inventory optimization, and a six-page Power BI
dashboard — designed as a closed-loop system where insights feed back into the database."

---

## 2. Why This Project Exists (Context)

**The business problem.** A consumer-goods manufacturer running hundreds of SKUs across
multiple channels has to answer a recurring set of questions: *How much of each product
should we produce? When do we reorder? Are we delivering on time? Where are our
bottlenecks? Are planned values tracking against actuals?* Those are the daily questions of
**demand planning, inventory management, and supply planning** — and they require pulling
data from an ERP, modeling it, and reporting it.

**What makes this project distinctive — automation at every stage.** Most analytics
projects are one-time analyses. This one is built as a **production-style system**: Oracle
stored procedures automate data extraction and MRP calculation on a nightly schedule,
Power Query custom functions automate transformation logic across all categories, and
Power BI scheduled refresh is architected to push updated dashboards out without manual
work. The payoff is a **closed-loop system** — the dashboard's recommendations (revised
lead times, adjusted safety stock, new lot-sizing rules) map to **master-data updates in
Oracle** that take effect on the next automated cycle.

**Why it's a strong portfolio project.** It's the portfolio's broadest project — it touches
**three major tools** (Oracle SQL, Excel, Power BI) and demonstrates genuine **supply-chain
domain knowledge**: MRP net-requirements logic, EOQ lot sizing, ABC/XYZ segmentation,
safety-stock math, demand forecasting. It models the same tools and workflows used in real
production supply-chain environments (the kind found in Oracle Fusion Cloud ERP shops).

---

## 3. The Tech Stack — Three Layers

| Layer | Tool | Role |
|---|---|---|
| **Database / ERP** | **Oracle Autonomous Database** (19c, Always Free tier) | SQL extraction, joins, aggregation, views; stored procedures; `DBMS_SCHEDULER` for nightly automation; the MRP simulation tables/views |
| **ETL & Analysis** | **Excel** — Power Query, Power Pivot, Solver, Goal Seek, What-If Analysis, dynamic arrays | Transformation (Power Query M); demand forecasting (Forecast Sheet / ETS); inventory optimization (Solver) |
| **Dashboards** | **Power BI Desktop** | Six-page report, star-schema model, DAX measures, data alerts, Row-Level Security |

**The mental model — a three-stage relay.** Oracle is the **system of record** (where the
data lives, is normalized, and where the MRP runs). Excel is the **analysis bench** (where
forecasting and inventory modeling happen). Power BI is the **delivery surface** (where
stakeholders consume it). Crucially, it's not a one-way relay — Excel's forecasts are
**written back** into Oracle, and Power BI's insights map to Oracle master-data changes.
That two-way flow is what makes it a "closed loop" rather than a linear pipeline.

**The deliverables:** 7 Oracle SQL scripts (`sql/01`–`07`), an Excel workbook
(`SupplyChain_Analysis_V11.xlsx`), and a Power BI file (`SupplyChain_Dashboard_V1.pbix`).

---

## 4. The Dataset — DataCo Smart Supply Chain

**What it is.** The **DataCo Smart Supply Chain dataset** from Kaggle — **~180,000 order
records** covering the full order-to-delivery lifecycle, **January 2015 – January 2018**. It
arrives as a single **flat CSV with 53 columns**: product categories, customer segments,
order dates, shipping modes, **scheduled vs. actual delivery dates**, late-delivery flags,
geographic data, and financial metrics (sales, profit, discounts).

**The normalized Oracle schema — 8 tables.** The flat file is decomposed (in script 02)
from a staging table `STG_DATACO` (~180,500 rows) into a proper relational schema:

- **5 transactional tables:** `CUSTOMERS`, `PRODUCTS`, `ORDERS`, `ORDER_ITEMS`,
  `SHIPMENTS` — the order-to-delivery facts.
- **3 supply-planning tables:** `FORECAST_PLAN` (demand forecasts), `MRP_REQUIREMENTS`
  (the MRP net-requirements output), `INVENTORY_SNAPSHOT` (current inventory positions).

**Why normalize a flat file?** A 53-column flat CSV repeats customer and product
information on every order row — wasteful and error-prone. Splitting it into transactional
tables (one row per customer, per product, per order) removes that redundancy, enforces
relationships, and makes the data queryable the way an ERP actually stores it. The 3
planning tables are *new* — they don't exist in the raw data; they're built to hold the
forecasting and MRP outputs the project generates.

---

## 5. The Automation Architecture (the Closed Loop)

**This is the project's signature concept — know it cold.**

```
  Oracle DBMS_SCHEDULER  (nightly, 2:00 AM)
        │  runs the REFRESH_SUPPLY_CHAIN_DATA stored procedure:
        │  staging refresh → derived fields → read latest forecast →
        │  MRP net-requirements calculation → rebuild 6 reporting views → audit log
        ▼
  Power BI Service scheduled refresh  (5:00 AM)
        │  connects to the Oracle views; Power Query custom functions + parameters run
        ▼
  DAX measures recalculate · data alerts evaluate thresholds · notifications sent
        ▼
  Dashboard is current by morning
        │
        │  ◄────── CLOSED LOOP ──────────────────────────────────────┐
        ▼                                                             │
  Analyst reviews Page 6 recommendations → updates Oracle master data │
  (lead times, safety stock, lot sizing) ─────────────────────────────┘
        (the next nightly run reflects those changes automatically)
```

**The three automation pieces:**
- **Oracle:** `DBMS_SCHEDULER` runs the `REFRESH_SUPPLY_CHAIN_DATA` stored procedure
  nightly; 6 reporting views are defined once and rebuilt every cycle.
- **Power Query:** custom M functions and parameters re-execute automatically on refresh.
- **Power BI:** scheduled refresh, auto-recalculating DAX, and data alerts.

**The "closed loop" — the differentiator.** Page 6 of the dashboard maps each
recommendation to a specific **Oracle master-data update** (a revised lead time, an
adjusted safety-stock level, a new lot-sizing rule). When the analyst makes that change,
the next nightly `DBMS_SCHEDULER` run recalculates MRP with the new parameters, and the
next Power BI refresh surfaces the impact. The cycle is **analyze → recommend → execute →
measure** — which turns a reporting dashboard into a *continuous-improvement system*.

**The honest caveat — state this in interviews.** The DataCo dataset is a **static
historical snapshot** (no new transactions flow in). So the automation infrastructure is
**built, tested, and validated end-to-end** — the stored procedure runs correctly when
called, the `DBMS_SCHEDULER` job is configured, the forecast write-back round-trips with
zero variance, Power Query refreshes repeatably — but it is **not actively processing new
data nightly**, and the dashboard isn't published to Power BI Service with a live Oracle
gateway. The architecture is production-ready; the static dataset is what makes this a
*portfolio demonstration* rather than a live system. Saying that plainly is the mature
framing.

---

## 6. Phase 1–2 — Oracle SQL: Schema, Views, Stored Procedure & MRP

Seven SQL scripts (`sql/01`–`07`) build the entire database layer.

**Script 01 — Schema DDL.** `CREATE TABLE` statements for all 8 tables (5 transactional +
3 planning), with primary/foreign keys and constraints — the normalized relational schema.

**Script 02 — Data Normalization.** Splits the flat `STG_DATACO` staging table (~180,500
rows) into the 5 transactional tables (`CUSTOMERS`, `PRODUCTS`, `ORDERS`, `ORDER_ITEMS`,
`SHIPMENTS`) — `INSERT ... SELECT DISTINCT` to deduplicate customers and products, joins to
wire up foreign keys.

**Scripts 03 & 04 — Extraction & analysis queries.** Script 03 = demand/sales queries
(feed the forecasting page and ABC/XYZ inputs). Script 04 = inventory & fulfillment queries
— ABC classification by revenue (Pareto/80-20), the combined ABC-XYZ matrix with policy
recommendations, and delivery-performance analysis. These use **CTEs and window functions**
for multi-stage calculations (cumulative revenue for ABC, rolling demand variability,
gross-to-net for MRP).

**Script 05 — Reporting Views (6).** Six views package pre-calculated, analysis-ready data
as single virtual tables, so the extraction logic is **defined once and reused on every
refresh**: `VW_DEMAND_TIMESERIES`, `VW_FULFILLMENT_KPI`, `VW_PRODUCT_MASTER`,
`VW_PLANNED_VS_ACTUAL`, `VW_MRP_PLAN`, `VW_FORECAST_VS_ACTUAL`. Power BI and Power Query
connect directly to *these views* — not the raw tables — which decouples the dashboard from
schema details.

**Script 06 — Stored Procedure, MRP Logic & Scheduler.** The heart of the automation:
- The **`REFRESH_SUPPLY_CHAIN_DATA` stored procedure** wraps the full pipeline — refresh
  `INVENTORY_SNAPSHOT` with current positions, read demand forecasts from `FORECAST_PLAN`,
  run the **MRP net-requirements calculation**, write planned orders, rebuild the 6 views,
  and log to an audit table.
- The **MRP logic** — the simulation of Material Requirements Planning: take **gross
  requirements** (demand from the forecast), subtract **projected on-hand** inventory and
  scheduled receipts to get **net requirements**, then generate **planned order releases**
  applying **EOQ lot sizing** and **lead-time offsets**.
- The **`DBMS_SCHEDULER` job** runs the procedure nightly at 2:00 AM — the same mechanism
  used in production Oracle Fusion Cloud environments.

**Script 07 — Forecast Write-Back.** Loads the Excel-generated ETS forecasts into Oracle's
`FORECAST_PLAN` table (**42 rows = 7 A-class categories × 6 forecast months**) via explicit
`INSERT` statements, then runs a **cross-check query** — a `LEFT JOIN` of `FORECAST_PLAN`
to `MRP_REQUIREMENTS` comparing forecast quantity to MRP gross requirements; **the variance
should be zero**, proving the MRP procedure consumed the forecasts correctly. (A `LEFT JOIN`
is used deliberately, so a missing MRP row surfaces as a `NULL` rather than being silently
dropped — a missing row would signal a procedure failure.)

**The teachable point.** The Oracle layer isn't just "extract data." It's a *system*:
normalized schema, reusable views, an automated stored procedure, a scheduler, an MRP
simulation, and a validated write-back round-trip. That's database engineering, not just
querying.

---

## 7. Phase 3 — Power Query ETL & Custom M Functions

**Power Query** (in Excel) is the ETL layer between Oracle and the analysis.

**The signature technique — custom M functions.** Rather than copy-pasting transformation
logic, the project wrote **5 reusable custom functions in M** (Power Query's language) and
*invokes* them across every product category:
- **`fn_CalculateSafetyStock`** — safety-stock math from demand variability and service
  level.
- **`fn_ClassifyABC`** — ABC classification by cumulative revenue.
- **`fn_ClassifyXYZ`** — XYZ classification by demand variability.
- **`fn_CalculateReorderPoint`** — reorder-point calculation.
- **`fn_CalculateNetRequirements`** — MRP net-requirements logic.

**Why custom functions matter.** "Write once, invoke everywhere." Without them, the same
safety-stock or ABC logic would be duplicated for every category — and a fix would have to
be made in dozens of places. A function centralizes the logic; change it once, every
category updates.

**Parameters.** Four parameters make the ETL dynamic without editing queries: **Date**
(the analysis window), **Source** (which Oracle environment), **Service Level** (the
Z-score for safety stock — drives what-if analysis), and **Planning Horizon** (3/6/12
months).

**Query folding.** The project **documents which transformation steps "fold" to Oracle**
versus execute locally in Excel. *Query folding* is when Power Query translates a step into
native SQL and pushes it down to the database to run there — far faster than pulling all
the data into Excel and processing it locally. Knowing which steps fold (and keeping
foldable steps early in the query) is a real performance-optimization skill.

---

## 8. Phase 4 — Excel: Forecasting, ABC/XYZ, EOQ, Write-Back

Excel is the **analysis and modeling bench**. Four bodies of work:

### 8.1 Demand Forecasting & Method Comparison

Demand forecasts were built for the **top 9 product categories** using **four methods**,
all consolidated in one `Demand_Forecast` worksheet:
- **`FORECAST.ETS`** — Excel's Exponential Triple Smoothing (handles level, trend,
  seasonality automatically).
- **MA-3 / MA-6** — 3- and 6-month moving averages.
- **WMA-3** — 3-month weighted moving average.

**Confidence intervals** were generated with `FORECAST.ETS.CONFINT` (scoped to forecast
periods only). **A key data-quality catch:** October 2017 was a *partial month* in the
dataset, showing anomalously low units — **excluding it from the ETS training range
corrected the forecasts from unrealistic to credible**. (`SORTBY`/`FILTER` dynamic arrays
were used to extract and sort category data, avoiding a known numeric-sort bug.)

**The finding that drives a recommendation:** **WMA-3 outperformed ETS and MA-3 on MAPE
across all 7 A-class categories** — so WMA-3 was recommended as the production forecast
method. Forecast error ranged from **Fishing's MAPE ~5.3%** (most predictable) to **Cardio
Equipment's ~9.5%** (most volatile).

### 8.2 ABC/XYZ Classification

A two-dimensional inventory segmentation:
- **ABC** — by **cumulative revenue** (A = top 80%, B = next 15%, C = bottom 5%) — the
  Pareto 80/20 principle applied to the catalog.
- **XYZ** — by **coefficient of variation (CoV) of demand** (X = stable/predictable, Y =
  moderate, Z = erratic).

Classification was computed in Oracle for all 50 categories, then summarized in an
`ABC_XYZ_Matrix` worksheet with `COUNTIFS`/`SUMIFS` grids. **The key finding: all A-class
categories are also X-class (AX)** — the highest-revenue *and* most-predictable segment,
ideal for automated replenishment with tight planning.

### 8.3 Inventory Optimization (EOQ, Safety Stock, Solver)

For each A-class category: **EOQ** (Economic Order Quantity — the order size that minimizes
total ordering + holding cost), **safety stock** (the buffer for demand uncertainty), and
**reorder point** — computed via the custom M functions, with the **service-level Z-score**
driven from a `Parameters` sheet for what-if analysis. **Solver** and **Goal Seek**
optimize lot sizing. The What-If analysis showed **95% service level is the cost-optimized
target** — dropping to 90% saves ~$62K but raises stockout risk; 99% adds ~$70K for
diminishing reliability gains.

### 8.4 Forecast Write-Back — Closing the Loop

The Excel ETS forecasts are exported as a **42-row flat table** (`Forecast_Export` sheet)
and written into Oracle's `FORECAST_PLAN` table (script 07). This **closes the loop**: once
the forecasts are in the database, the nightly stored procedure reads them as MRP gross
requirements — no manual handoff. The cross-check query (variance = 0) confirms it worked.

---

## 9. Phase 5 — The Power BI Dashboard (6 Pages)

A **six-page interactive Power BI report**, built on a **star-schema data model** — fact
tables (demand, fulfillment, KPI) surrounded by dimension tables (date, category, region,
shipping mode).

| Page | Title | What it answers |
|---|---|---|
| **1** | Executive KPI Overview | "Is the supply chain healthy? Where do we focus?" — 6 KPI cards, revenue trend, top-10 categories, shipping-mode breakdown |
| **2** | Demand Analysis & Forecasting | "What does demand look like? Which forecast method is best?" — demand trends with ETS overlays, MAE/MAPE by category, method comparison |
| **3** | Inventory Optimization & ABC/XYZ | "Where is working capital tied up? What inventory policy per segment?" — ABC-XYZ heatmap, inventory-health table, EOQ/safety-stock params |
| **4** | Fulfillment & Logistics | "Which shipping modes/regions underperform? What's the revenue at risk?" — on-time trends, lead-time variance, regional revenue-at-risk |
| **5** | Supply Plan & MRP Analysis | "Is the supply plan covering demand? Any exceptions?" — time-phased MRP output, exception log, planned orders |
| **6** | Insights & Closed-Loop Actions | "What are this cycle's priorities, and how do they map to master-data changes?" — consolidated recommendations |

**Page 5 is the most technically distinctive** — it visualizes the MRP simulation output:
time-phased net requirements across the 6-month horizon (Oct 2017–Mar 2018), showing gross
requirements, scheduled receipts, projected on-hand, net requirements, and planned order
releases, plus an **MRP exception log**.

**Page 6 is the differentiator** — it's where the closed loop is made explicit:
recommendations map directly to Oracle master-data updates that take effect on the next
refresh.

**The technical features:**
- **DAX measures** — YoY Growth %, On-Time/Late Delivery Rate, forecast accuracy (MAE,
  MAPE, Forecast Bias), Inventory Turnover, Days of Supply, In-Stock Rate, MRP Coverage
  Ratio, Supply Plan Adherence — all auto-recalculating on refresh.
- **Data alerts** — threshold notifications on in-stock-rate drops, late-delivery spikes,
  projected stockouts, MRP exception counts, and forecast bias.
- **Row-Level Security (RLS)** — two roles: **Marketing** sees sell-through/demand data
  only; **Operations** sees production, fulfillment, MRP, and inventory. Same dashboard,
  filtered automatically by role.

---

## 10. Key Findings

Memorize the headline numbers.

1. **Revenue is Pareto-concentrated.** Total revenue ≈ **$35.2M**; the **7 A-class
   categories drive ~77% ($27.12M)** — confirming the 80/20 principle and validating the
   decision to focus forecasting and MRP on those 7.
2. **On-time delivery is critically low — 42.7%** (57.3% late). Persistent across all
   periods — a **structural** problem, not a seasonal blip.
3. **Premium shipping is the worst performer.** **First Class ≈ 95% late, Second Class ≈
   85% late** — the tiers that promise the *fastest* delivery are the *least reliable*.
   **Standard Class** handles ~60% of volume *and* has the best on-time rate (~55%).
4. **WMA-3 beats ETS and MA-3** on MAPE for all 7 A-class categories — the recommended
   production forecast method. Fishing is most predictable (MAPE ~5.3%), Cardio Equipment
   least (~9.5%).
5. **All A-class categories are "AX"** — high revenue *and* stable demand (CoV < 0.20) —
   ideal for tight, automated replenishment.
6. **~$597K of working capital is tied up in overstock** — three categories (Camping &
   Hiking, Fishing, Water Sports) sit at ~51 days of supply against a 30-day target.
7. **Safety stock ≈ 824 units ($167,826)** at the 95% service level — the What-If analysis
   found 95% is the cost-optimized sweet spot.
8. **The MRP run is clean** — zero exceptions across the full 6-month horizon for all 7
   A-class categories; gross requirements ≈ 48,600 units, fully covered by planned orders +
   opening on-hand. This validates the end-to-end planning pipeline.
9. **Top revenue drivers** — Fishing and Cleats, each exceeding $4M.

---

## 11. Supply Chain & Technical Concepts to Know Cold

A supply-chain-analytics interview will probe the domain concepts — this project is built
on them.

**MRP (Material Requirements Planning)** — the core supply-planning method. It answers
*how much to order and when*. The logic: **gross requirements** (demand) − **projected
on-hand inventory** − **scheduled receipts** = **net requirements**; then generate
**planned order releases** to cover the net, offset earlier by the **lead time**.

**Gross-to-net** — the MRP calculation of subtracting available inventory from demand to
find what genuinely needs to be ordered.

**Lead-time offset** — placing a planned order *earlier* than it's needed by the supplier's
lead time, so it arrives on time (this project uses ~3.5 days average).

**Lot sizing** — the rule for how big each order is. Options: **EOQ** (economic order
quantity), **Fixed Lot**, **Lot-for-Lot** (order exactly what's needed).

**EOQ (Economic Order Quantity)** — the order quantity that **minimizes total cost** of
ordering plus holding inventory. Order too small → too many orders (high ordering cost);
too large → too much sitting inventory (high holding cost). EOQ is the balance point.

**Safety stock** — a buffer of extra inventory held to absorb demand variability and avoid
stockouts; sized from demand standard deviation, lead time, and a service-level Z-score.

**Reorder point (ROP)** — the inventory level at which a replenishment order is triggered;
roughly (average demand over lead time) + safety stock.

**Service level** — the target probability of *not* stocking out (90% / 95% / 99%);
higher service level = more safety stock = more cost. A Z-score converts it to a buffer.

**ABC classification** — segmenting items by revenue contribution (Pareto): A = top 80%,
B = next 15%, C = bottom 5%. Focus management attention on A items.

**XYZ classification** — segmenting items by demand *variability* (coefficient of
variation): X = stable/predictable, Y = moderate, Z = erratic. Combined with ABC into an
**ABC-XYZ matrix** — an "AX" item (high revenue, stable) gets a very different inventory
policy than a "CZ" item (low revenue, erratic).

**Coefficient of variation (CoV)** — standard deviation ÷ mean of demand; the measure
behind XYZ. Low CoV = predictable.

**Demand forecasting methods** — **ETS** (Exponential Triple Smoothing — models level,
trend, seasonality; Excel's `FORECAST.ETS`), **moving average** (MA — mean of the last N
periods), **weighted moving average** (WMA — recent periods weighted more heavily).

**MAE / MAPE / Forecast Bias** — forecast-accuracy metrics. MAE = mean absolute error
(in units); **MAPE** = mean absolute *percentage* error (the headline accuracy metric);
bias = whether the forecast systematically over- or under-predicts.

**Days of supply** — how many days current inventory will last at the demand rate; compared
to a target to flag overstock or understock.

**Inventory turnover** — how many times inventory is sold and replaced in a period.

**Normalization (database)** — splitting a flat, redundant table into related tables to
remove duplication and enforce relationships.

**Stored procedure** — a saved, callable block of SQL; here, `REFRESH_SUPPLY_CHAIN_DATA`
wraps the whole nightly pipeline.

**`DBMS_SCHEDULER`** — Oracle's built-in job scheduler; runs the procedure nightly.

**Reporting view** — a saved query exposed as a virtual table; the 6 views Power BI
connects to.

**Power Query / M** — Excel's ETL tool and its language; custom **M functions** make
transformation logic reusable.

**Query folding** — Power Query translating steps into native SQL pushed down to the
database for speed.

**Star schema** — a central fact table surrounded by dimension tables; the Power BI model.

**DAX** — Power BI's measure/calculation language.

**Row-Level Security (RLS)** — filtering what data a user sees based on their role.

**Closed-loop system** — analysis → recommendation → master-data change → next cycle
reflects it; the project's organizing idea.

---

## 12. Limitations & Honest Caveats

Volunteer these — the project itself is candid about most.

1. **The dataset is a static historical snapshot** (DataCo, Jan 2015 – Jan 2018) — no new
   transactions flow in. So the automation is **built, tested, and validated** but **not
   actively running nightly**, and the dashboard isn't published to Power BI Service with a
   live Oracle gateway. The infrastructure is production-ready; the static data is what
   makes it a portfolio demonstration. **State this plainly — the project does.**
2. **The MRP and inventory tables are simulated.** `FORECAST_PLAN`, `MRP_REQUIREMENTS`, and
   `INVENTORY_SNAPSHOT` don't exist in the raw DataCo data — they're constructed to model
   the planning layer. The DataCo dataset has no real inventory positions, so opening
   on-hand balances are assumed/derived.
3. **Forecasting is at the category level**, not SKU level (the dataset's product detail is
   category-grained). Real demand planning often goes to the SKU.
4. **An October 2017 partial-month artifact** had to be excluded from forecast training —
   a reminder that the dataset's time coverage isn't perfectly clean.
5. **No formal time-series testing.** ETS auto-detected seasonality and found little; the
   project didn't run formal stationarity or decomposition diagnostics.
6. **Some steps depend on desktop tooling** (Excel Solver, the Power BI Desktop file) —
   it's a multi-tool project, so reproducing it end-to-end requires Oracle access, Excel,
   and Power BI Desktop.
7. **Findings are descriptive/correlational** — e.g., "premium shipping is unreliable"
   identifies the pattern but a carrier audit (not in scope) would establish the cause.

---

## 13. Interview Q&A

Practice these out loud.

**Q1. Give me the overview of this project.**
"It's an end-to-end automated supply-chain analytics pipeline across three tools. I loaded
the DataCo Smart Supply Chain dataset — about 180,000 orders — into an Oracle database,
normalized it into a relational schema, and wrote queries, reporting views, and a stored
procedure that runs an MRP simulation on a nightly schedule. Then Power Query handles ETL
with custom functions, Excel does the demand forecasting and inventory optimization, and
Power BI delivers a six-page dashboard. The distinguishing idea is the closed loop — the
dashboard's recommendations feed back into Oracle master data, so the next refresh reflects
them."

**Q2. What is MRP, and how did you simulate it?**
"MRP is Material Requirements Planning — it answers how much to order and when. The logic
is gross-to-net: start with gross requirements, which is the demand forecast, subtract
projected on-hand inventory and any scheduled receipts, and what's left is net
requirements. Then you generate planned orders to cover that net, offset earlier by the
supplier lead time so they arrive on time, and sized by a lot-sizing rule — I used EOQ. I
simulated this in Oracle with planning tables and a stored procedure: it reads the forecast
from the FORECAST_PLAN table, runs the net-requirements calculation, and writes planned
orders to MRP_REQUIREMENTS."

**Q3. What's the 'closed loop' and why does it matter?**
"Most dashboards are one-directional — data goes in, a report comes out, and that's it. The
closed loop makes it bidirectional. Page 6 of my dashboard maps each recommendation to a
specific Oracle master-data change — a revised lead time, an adjusted safety-stock level, a
new lot-sizing rule. When the analyst makes that change in Oracle, the next nightly stored
procedure run recalculates MRP with the new parameters and the next dashboard refresh shows
the impact. So the cycle is analyze, recommend, execute, measure — it turns a reporting
tool into a continuous-improvement system."

**Q4. Explain EOQ and safety stock.**
"EOQ, economic order quantity, is the order size that minimizes total cost — there's a
trade-off: order in small batches and you pay a lot of ordering and setup cost; order in
huge batches and you pay a lot of holding cost for inventory sitting in the warehouse. EOQ
is the mathematical balance point between those two. Safety stock is separate — it's a
buffer you hold on top of expected demand to absorb variability and avoid stockouts. You
size it from the demand standard deviation, the lead time, and a service-level Z-score. I
calculated both per category with custom Power Query functions, and used Solver for the lot-
sizing optimization."

**Q5. What's ABC/XYZ classification?**
"It's a two-dimensional way to segment inventory. ABC is by revenue — A items are the top
80% of revenue, B the next 15%, C the bottom 5% — it's Pareto, 80/20. XYZ is by demand
variability — X is stable and predictable, Z is erratic. You combine them into a matrix. An
AX item — high revenue, stable demand — should get tight, automated replenishment with low
safety stock. A CZ item — low revenue, erratic — needs a totally different policy. A key
finding in my project was that all seven A-class categories were also X-class, so the
highest-revenue categories were also the most predictable, which validated using tight MRP
planning on them."

**Q6. Why did you normalize the flat CSV into a relational schema?**
"The DataCo data comes as one flat 53-column CSV, which repeats every customer's and
product's details on every order line — that's wasteful and makes updates error-prone. I
split it into five transactional tables — customers, products, orders, order items,
shipments — so each entity is stored once, relationships are enforced with keys, and the
data is queryable the way a real ERP stores it. I also added three planning tables for the
forecast, MRP, and inventory layers, which don't exist in the raw data."

**Q7. What did you use custom M functions for, and why?**
"In Power Query I wrote five custom M functions — for safety stock, ABC classification, XYZ
classification, reorder point, and MRP net requirements. The reason is reusability — write
the logic once, invoke it across every product category. Without functions, the same
safety-stock formula would be duplicated dozens of times, and a fix would mean changing it
in every place. A function centralizes the logic so one change updates everything."

**Q8. Which forecast method did you recommend, and how did you decide?**
"I built four methods for the top categories — ETS, three- and six-month moving averages,
and a three-month weighted moving average — and compared them on MAPE, mean absolute
percentage error. The weighted moving average, WMA-3, beat ETS and the plain moving
averages on all seven A-class categories, so I recommended it as the production method,
with ETS kept as a secondary check for emerging seasonality. One thing I caught along the
way: October 2017 was a partial month in the data with artificially low units — I had to
exclude it from the ETS training range, which corrected the forecasts from unrealistic to
credible."

**Q9. Your dashboard showed 42.7% on-time delivery — what would you do about it?**
"First, I'd note it's structural — it's persistent across every period, not a seasonal
spike. The most striking detail is that the premium shipping tiers are the worst: First
Class is about 95% late, Second Class about 85%, while Standard Class, which handles 60% of
volume, has the best on-time rate. So my recommendation was a formal carrier performance
audit for First and Second Class — either the promised delivery windows are unrealistic, or
the carriers are underperforming. Short term, reset customer expectations by adjusting
quoted timelines; medium term, renegotiate carrier SLAs or issue RFPs for the two highest-
revenue-at-risk regions, Europe and Latin America."

**Q10. Is the automation actually running?**
"I'd be straight about this. The infrastructure is fully built and tested — the stored
procedure runs correctly end to end, the DBMS_SCHEDULER job is configured for a nightly 2
AM run, the forecast write-back round-trips with zero variance, and Power Query refreshes
repeatably. But the DataCo dataset is a static historical snapshot — no new transactions
flow in — so the pipeline isn't actively processing data nightly, and the dashboard isn't
published to Power BI Service with a live Oracle gateway. The architecture is production-
ready; the static dataset is what makes this a portfolio demonstration rather than a live
system. In a real environment with live data, it would run autonomously on the schedule."

**Q11. What does query folding mean and why did you document it?**
"Query folding is when Power Query translates a transformation step into native SQL and
pushes it down to the database to run there, instead of pulling all the data into Excel and
processing it locally. Folding is much faster because the database does the heavy lifting on
its own engine. I documented which steps fold and which don't, because the order of steps
matters — you want foldable operations early so as much work as possible happens on Oracle.
It's a real performance-optimization consideration."

**Q12. What's the most technically impressive part of this project?**
"The MRP simulation in Oracle and the closed loop around it. The MRP isn't just a query —
it's a stored procedure that does real gross-to-net netting, applies EOQ lot sizing and
lead-time offsets, and generates planned orders. And I validated it: I wrote the Excel
forecasts back into Oracle, the procedure consumed them, and a cross-check query confirmed
zero variance between the forecast and the MRP gross requirements. That round-trip — Excel
forecast to Oracle to MRP, validated — is the piece I'm proudest of."

---

## 14. How to Walk Through This Project Live

If asked to screen-share:

1. **State the three-layer structure first** — "Oracle is the system of record, Excel is
   the analysis bench, Power BI is the delivery surface — and it's a closed loop, not a
   one-way pipeline."
2. **Show the automation architecture diagram** — the nightly Oracle job → Power BI
   refresh → and the loop back to master data. This is the signature concept.
3. **Walk the Oracle layer** — the normalized 8-table schema, the 6 reporting views, and
   the **`REFRESH_SUPPLY_CHAIN_DATA` stored procedure with the MRP logic**. Spend time on
   the MRP gross-to-net calculation.
4. **Show the forecast write-back** — Excel ETS forecast → `FORECAST_PLAN` → the
   zero-variance cross-check. This is the validation moment.
5. **Show the Excel analysis** — the four-method forecast comparison, the ABC/XYZ matrix,
   and EOQ/safety-stock optimization with Solver.
6. **Walk the Power BI dashboard** — pages 1 through 6, ending on **Page 5 (the MRP
   output)** and **Page 6 (the closed-loop recommendations)**.
7. **Close on the honest framing** — the automation is built and validated; the static
   dataset is what makes it a demonstration. Then end on a finding-to-recommendation, like
   the premium-shipping carrier audit.

**Pacing tip:** spend the most time on the **MRP simulation** and the **closed-loop
automation** — those are the differentiated, domain-heavy parts that separate this from a
generic dashboard project. And be confident and upfront about the static-dataset caveat —
the project documents it, and owning it reads as maturity.

---

## 15. Glossary

- **DataCo Smart Supply Chain dataset** — the Kaggle dataset (~180,000 orders, 2015–2018)
  the project analyzes.
- **Oracle Autonomous Database** — the cloud database (Always Free tier) holding the data.
- **Normalization** — splitting a flat redundant table into related tables.
- **Transactional tables** — `CUSTOMERS`, `PRODUCTS`, `ORDERS`, `ORDER_ITEMS`, `SHIPMENTS`.
- **Planning tables** — `FORECAST_PLAN`, `MRP_REQUIREMENTS`, `INVENTORY_SNAPSHOT`
  (constructed for the planning layer).
- **Reporting view** — a saved query exposed as a virtual table; the 6 views Power BI reads.
- **Stored procedure** — a saved, callable block of SQL; `REFRESH_SUPPLY_CHAIN_DATA` here.
- **`DBMS_SCHEDULER`** — Oracle's job scheduler; runs the procedure nightly at 2 AM.
- **MRP (Material Requirements Planning)** — the supply-planning method computing what to
  order and when.
- **Gross requirements** — total demand to be met (from the forecast).
- **Net requirements** — gross requirements minus available inventory and scheduled
  receipts.
- **Planned order release** — an order MRP recommends placing, offset by lead time.
- **Lead-time offset** — placing an order early by the supplier's lead time.
- **Lot sizing** — the rule for order size (EOQ / Fixed Lot / Lot-for-Lot).
- **EOQ (Economic Order Quantity)** — the order size minimizing ordering + holding cost.
- **Safety stock** — a buffer of inventory against demand variability.
- **Reorder point (ROP)** — the inventory level that triggers a replenishment order.
- **Service level** — the target probability of not stocking out (90/95/99%).
- **ABC classification** — segmenting items by revenue (A = top 80%, etc.).
- **XYZ classification** — segmenting items by demand variability (X stable, Z erratic).
- **ABC-XYZ matrix** — the combined revenue × variability segmentation grid.
- **Coefficient of variation (CoV)** — std dev ÷ mean of demand; the XYZ metric.
- **ETS** — Exponential Triple Smoothing; Excel's `FORECAST.ETS` forecast method.
- **Moving average (MA) / weighted moving average (WMA)** — simpler forecast methods.
- **MAE / MAPE** — mean absolute error / mean absolute percentage error (forecast
  accuracy).
- **Forecast bias** — whether a forecast systematically over- or under-predicts.
- **Days of supply** — how long current inventory lasts at the demand rate.
- **Inventory turnover** — how often inventory is sold and replaced per period.
- **Power Query / M** — Excel's ETL tool and language.
- **Custom M function** — a reusable transformation function (e.g.,
  `fn_CalculateSafetyStock`).
- **Query folding** — Power Query pushing steps down to the database as native SQL.
- **Star schema** — a central fact table surrounded by dimension tables.
- **DAX** — Power BI's calculation/measure language.
- **Data alert** — a Power BI threshold notification.
- **Row-Level Security (RLS)** — role-based filtering of what data a user sees.
- **Closed-loop system** — analysis feeding back into master data so the next cycle
  reflects it.
- **Forecast write-back** — pushing Excel forecasts back into the Oracle database.

---

*This study guide documents the project as built. The authoritative references are the 7
SQL scripts in `sql/`, the Excel workbook `SupplyChain_Analysis_V11.xlsx`, the Power BI
file `SupplyChain_Dashboard_V1.pbix`, and the portfolio page `index.md`. The automation is
built and validated but not actively running on a live schedule (the dataset is static —
see §12). When this guide and the source files disagree, the source files win.*