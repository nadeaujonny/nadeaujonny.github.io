# Master Outline & Study Guide
## E-commerce Business Optimization Analysis (BigQuery SQL)

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.
>
> **One sentence to anchor everything:** This is a **10-dimension SQL deep-dive** of a
> large e-commerce dataset, built entirely in BigQuery — every analysis uses the same
> **layered-CTE architecture** (raw aggregation → derived ratios → ranking) to turn raw
> transactions into revenue, profit, return-risk, and operational insights, and every
> section ends in concrete business recommendations.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Context)](#2-why-this-project-exists-context)
3. [The Tech Stack & Dataset](#3-the-tech-stack--dataset)
4. [The Signature SQL Pattern — Layered CTEs](#4-the-signature-sql-pattern--layered-ctes)
5. [The Analytical Framework — 10 Dimensions](#5-the-analytical-framework--10-dimensions)
6. [The Key Metrics (Definitions)](#6-the-key-metrics-definitions)
7. [The SQL Techniques in Depth](#7-the-sql-techniques-in-depth)
8. [Key Findings](#8-key-findings)
9. [Highest-Impact Recommendations](#9-highest-impact-recommendations)
10. [SQL Concepts to Know Cold](#10-sql-concepts-to-know-cold)
11. [Limitations & Honest Caveats](#11-limitations--honest-caveats)
12. [Interview Q&A](#12-interview-qa)
13. [How to Walk Through This Project Live](#13-how-to-walk-through-this-project-live)
14. [Glossary](#14-glossary)

---

## 1. The 30-Second Pitch

This project is a **multi-dimensional SQL analysis** of a large e-commerce dataset —
Google's public **`thelook_ecommerce`** dataset in BigQuery (~181,000 order items, ~80,000
customers, ~29,000 products across ~2,700 brands and 26 categories). It's built entirely in
**BigQuery Standard SQL** — **92 queries**, no data ever exported to another tool.

The analysis is structured across **10 analytical dimensions** — Top and Bottom Products,
Brands, and Categories; Long-Term Trends; Seasonal Trends; Customers; and Distribution
Centers — and examines each entity from **6–8 metric angles at once** (revenue, profit,
margin, unit volume, return rate, lost revenue, and more). Every query uses the same
**layered-CTE pattern**: a first layer that does raw conditional aggregation, a second
layer that derives ratios and shares, and a final ranking layer.

The framing is deliberate: *"if I were hired as a data analyst at this company, what would
I investigate, what would I find, and what would I recommend?"* Every one of the 10
sections ends in a concrete, prioritized **business recommendation**. Headline findings:
revenue concentrates in premium categories, profit margin diverges sharply from revenue,
return rates are a **systemic ~28%** across all 26 categories, lost revenue rivals earned
revenue, and **80.7% of customers bought only 1–4 items** — a huge retention opportunity.

**One-line version:** "I built a 92-query, 10-dimension SQL analysis of a large e-commerce
dataset entirely in BigQuery — using a layered-CTE architecture with window functions and
conditional aggregation — to find where revenue, profit, and return risk actually come
from, and translated every finding into a business recommendation."

---

## 2. Why This Project Exists (Context)

**The premise.** E-commerce companies generate enormous transactional datasets but often
stop reporting at top-line revenue. This project goes deeper — it asks where *profit* is
actually generated (which is rarely the same place as revenue), which products and brands
are *net-negative* once returns and cancellations are counted, and what operational
patterns are quietly costing money.

**The framing.** The project explicitly simulates the job: *"if I were hired as a data
analyst at this company, what would I investigate first, what would I find, and what would
I recommend?"* That framing drives the central design choice — **every section ends with a
business recommendation**, because "data analysis is only valuable when it translates into
decisions."

**Why SQL is the right tool.** The questions all require joining multiple tables, filtering
on complex conditions, and computing **derived metrics that don't exist in the raw data** —
profit margins, return rates, revenue shares, cross-metric rankings. That is exactly the
daily workflow of a data analyst, and the project's thesis is that **SQL is a full
analytical engine**, not just a data-extraction language — the entire analysis (joining six
tables, ranking 29,000+ products) was done in SQL alone, with nothing exported.

**Why it's a strong portfolio project.** It demonstrates SQL depth at scale: layered CTEs,
window functions, conditional aggregation — and the *analytical thinking* around it: a
multi-dimensional framework, paired top/bottom analysis, and recommendations grounded in
specific numbers. It reads like real analyst work, not a query exercise.

*(Cross-project note: this uses the **same `thelook_ecommerce` dataset** as the cohort
retention project in the portfolio — a useful interview contrast. Cohort retention used it
for time-based retention math; this project uses it for cross-dimensional business
optimization. Same data, two different analytical lenses.)*

---

## 3. The Tech Stack & Dataset

| | |
|---|---|
| **Engine** | Google BigQuery (cloud data warehouse, Standard SQL / GoogleSQL) |
| **Dataset** | `bigquery-public-data.thelook_ecommerce` — a public, synthetic e-commerce dataset |
| **Deliverable** | 92 `.sql` query files + a 10-section analysis write-up |
| **External tools** | **None** — all analysis is SQL-native; nothing exported |

**The dataset — `thelook_ecommerce`.** A public BigQuery dataset simulating a mid-size
e-commerce retailer selling apparel, accessories, and outerwear.

| Scale | Value |
|---|---|
| Order items | ~181,000 |
| Unique customers | ~80,000 (79,963) |
| Unique products | ~29,000 |
| Brands | ~2,700 |
| Product categories | 26 |
| Time range | 2019 – early 2026 (synthetic data keeps regenerating) |

**The 6 tables used** (and how they relate):
- **`order_items`** — one row per item ordered; carries `status`, `sale_price`. The grain
  of the analysis.
- **`orders`** — one row per order; `created_at`, `order_id`.
- **`products`** — `name`, `brand`, `category`, `cost`.
- **`users`** — customer demographics, geography.
- **`distribution_centers`** — fulfillment facilities.
- **`inventory_items`** — stock-level records.

The core join chain is **`order_items` → `orders` → `products`** (on `order_id` and
`product_id`), extended to `users`, `distribution_centers`, and `inventory_items` where a
section needs them.

**The order-status field is the analytical key.** `order_items.status` takes values
**Complete, Returned, Cancelled, Shipped, Processing** — and almost every metric in the
project is computed by conditionally aggregating on this field (see §7).

**An honest dataset caveat:** it's synthetic, so some prices are anomalous (e.g., socks
listed at $903). Those are left in deliberately — the project's purpose is to demonstrate
*methodology*, not to clean one company's data.

---

## 4. The Signature SQL Pattern — Layered CTEs

**Every analytical query in this project is built the same way — a layered chain of CTEs.
Know this pattern cold; it is the project's technical signature.**

A **CTE (Common Table Expression)** is a named temporary result set defined with `WITH`.
The project chains them so each layer has one job:

**Layer 1 — `first_layer`: raw conditional aggregation.** Joins the tables, `GROUP BY`s the
entity (product / brand / category), and computes raw totals using **`CASE WHEN` inside
`SUM`/`COUNT`** — e.g., revenue = sum of `sale_price` *only where `status = 'Complete'`*,
units_returned = count *only where `status = 'Returned'`*.

**Layer 2 — `second_layer`: derived ratios and shares.** Takes the raw totals and computes
the metrics that *don't exist in the raw data*: profit margin (`profit / NULLIF(revenue,
0)`), return rate, completion rate, plus revenue/profit **shares** using
`SUM(...) OVER()` (each entity's slice of the whole-table total).

**Final layer — ranking.** A final `SELECT` adds **`RANK() OVER(ORDER BY <metric> DESC)`**
for *every* metric — so each product carries a `revenue_rank`, `profit_rank`,
`margin_rank`, `return_rate_rank`, and so on simultaneously. Then it orders by the relevant
rank and `LIMIT`s to the top/bottom 15. *(Some queries add an explicit `third_layer` CTE
with a `WHERE` clause to filter on a rank threshold; simpler trend queries use just one CTE
then a SELECT — the CTE depth flexes to the question.)*

**Why this architecture matters — the interview point.** Building complex metrics in one
giant nested query is unreadable and undebuggable. The layered pattern **separates concerns**:
Layer 1 is "aggregate the raw facts," Layer 2 is "derive the ratios," the final layer is
"rank and filter." Each layer can be run on its own to inspect it. The result is SQL that
is *readable, maintainable, and auditable* — another analyst could pick it up and extend it
without reverse-engineering. That separation-of-concerns discipline is the thing to
emphasize.

**The cross-metric ranking idea.** Because the final layer ranks the entity on *every*
metric at once, a single query answers "this product is #1 in revenue but #10 in unit
volume and #21 in margin." That multi-rank output is what powers the project's core
insight: **revenue, profit, margin, and volume tell different stories, and you have to see
all of them together.**

---

## 5. The Analytical Framework — 10 Dimensions

The analysis is structured across **10 dimensions**, deliberately paired:

| # | Dimension | What it examines |
|---|---|---|
| 1 | **Top Products** | The best products by revenue, profit, margin, volume, return rate, lost revenue |
| 2 | **Bottom Products** | Underperformers, zero-revenue products, high-return risks |
| 3 | **Top Brands** | Best-performing of the ~2,700 brands |
| 4 | **Bottom Brands** | Margin-compressing and high-loss brands |
| 5 | **Top Categories** | Best of the 26 categories |
| 6 | **Bottom Categories** | Weakest categories |
| 7 | **Long-Term Trends** | Revenue/profit, units sold, margin, return rate — month over month |
| 8 | **Seasonal Trends** | The same metrics by calendar month (`EXTRACT(MONTH ...)`) |
| 9 | **Customers** | Revenue, orders, lifetime, returns, cancellations, demographics, geography |
| 10 | **Distribution Centers** | Facility performance and inventory balance |

**Two deliberate design choices:**

1. **Multi-angle, not single-metric.** Each entity is examined from 6–8 metric
   perspectives at once. The reason: a product can look *excellent* on revenue and
   *terrible* on margin; a brand can lead on profit while *hemorrhaging returns*.
   Single-metric analysis leads to bad decisions; multi-dimensional analysis reveals the
   trade-offs.
2. **Paired Top *and* Bottom.** Analyzing only winners is half the picture. The "Bottom"
   sections surface where the business is *bleeding* — zero-revenue products,
   margin-compressing categories, serial-returning customers. **Knowing what to *stop*
   doing is as valuable as knowing what to double down on.**

Every section concludes with an **Analytical Insights & Business Recommendations** block.

---

## 6. The Key Metrics (Definitions)

These are computed and referenced throughout. Knowing the exact definitions is essential —
interviewers will ask "how did you define X?"

| Metric | Definition |
|---|---|
| **Revenue** | Sum of `sale_price` from **completed orders only** (`status = 'Complete'`) |
| **Profit** | Revenue minus product `cost`, for completed orders |
| **Profit Margin** | Profit / Revenue — share of each revenue dollar retained |
| **Return Rate** | Returned items / (Completed + Returned items) — post-delivery dissatisfaction |
| **Completion Rate** | Completed items / (Total items − Cancelled items) — fulfillment success |
| **Cancellation Rate** | Cancelled items / Total items ordered |
| **En Route Rate** | (Shipped + Processing) / (Total − Cancelled − Returned) — share of surviving orders still in transit |
| **Lost Revenue / Lost Profit** | Revenue / profit that *would have been* earned if returned & cancelled orders had completed — quantifies the cost of failed orders |
| **Revenue / Profit / Unit-Orders Share** | Each entity's contribution to the total — enables apples-to-apples comparison across scales |

**The most important definitional choice — "Revenue = completed only."** Revenue counts
*only* `status = 'Complete'` items. An order that was placed but returned or cancelled
contributes **zero** to revenue — and instead shows up in **Lost Revenue**. This split is
the analytical backbone: it's what lets the project show that, for many top products,
*lost* revenue rivals *earned* revenue.

**Why Return Rate's denominator excludes cancellations and in-transit items.** Return rate
= Returned / (Completed + Returned). A return only makes sense for an item that was
actually *delivered* — so the denominator is the delivered population (completed +
returned), not all orders. Cancelled and still-shipping items aren't eligible to be
returned, so including them would understate the true return rate.

---

## 7. The SQL Techniques in Depth

The six techniques used consistently across all 92 queries:

**1. Common Table Expressions (CTEs).** The layered `first_layer → second_layer →
[third_layer]` chain (§4) — building complex metrics incrementally in readable stages.

**2. Conditional aggregation (`CASE WHEN` inside `SUM`/`COUNT`).** The workhorse. Instead
of running separate queries for completed, returned, and cancelled metrics, a single pass
computes them all:
```sql
SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 END) AS revenue,
SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END)            AS units_returned,
SUM(CASE WHEN oi.status IN ('Returned','Cancelled') THEN oi.sale_price ELSE 0 END) AS lost_revenue
```
One scan of the data, every status-specific metric. This is *the* technique to be able to
explain.

**3. Window functions.** Two kinds: **`SUM(...) OVER()`** (an empty `OVER()` sums across
the *whole* result, used to compute each entity's share of the total — `revenue /
SUM(revenue) OVER()`), and **`RANK() OVER(ORDER BY metric DESC)`** (ranks every entity on
every metric, enabling cross-metric comparison in one query).

**4. Multi-table JOINs.** The `order_items → orders → products` chain, extended to `users`,
`distribution_centers`, `inventory_items` — building a unified analytical view from
normalized tables.

**5. `NULLIF` for safe division.** Every ratio wraps its denominator in `NULLIF(x, 0)` so a
zero denominator yields `NULL` instead of a divide-by-zero error — essential when ranking
thousands of products, some with zero completed orders.

**6. `DATE` functions.** `DATE_TRUNC(date, MONTH)` for monthly time-series buckets (the
long-term trends), `EXTRACT(MONTH FROM ...)` for seasonal (calendar-month) aggregation, and
`DATE_DIFF` for customer-lifetime calculations.

**The teachable point.** These queries "go well beyond basic `SELECT` statements" — they
**compute derived metrics that don't exist in the raw data** (margins, rates, shares,
ranks) entirely within a single query execution. That's the difference between using SQL to
*extract* data and using it to *analyze*.

---

## 8. Key Findings

Memorize these — they're the substance of the analysis.

1. **Revenue concentrates in premium categories.** **Outerwear & Coats is #1 in revenue
   ($339,222) but only #10 in unit volume (9,028 orders)** — premium categories drive
   disproportionate revenue *per unit*. The top 2 categories (Outerwear, Jeans) ≈ **24% of
   total revenue** — a quarter of the business on two product lines.
2. **Margin diverges sharply from revenue.** **Blazers & Jackets has the highest margin
   (62.1%) but ranks only #15 in revenue.** Conversely **Jeans is #2 in revenue but #21 in
   margin (46.5%)**. A revenue-optimized strategy looks fundamentally different from a
   profit-optimized one.
3. **Return rates are systemic, not category-specific.** All 26 categories fall in a tight
   **27–31% return-rate band** (~28% baseline). That uniformity means the cause is
   **platform-level** (return policy, photography, sizing tools) — *not* category-specific
   quality. This is critical: a platform-wide fix compounds across the whole catalog.
4. **Lost revenue rivals earned revenue.** For nearly every top product, brand, and
   category, lost revenue from returns/cancellations *approaches or exceeds* completed
   revenue. **Diesel leads all brands in lost revenue ($49,754) against $53,774 earned.**
5. **The customer base is overwhelmingly single-purchase.** **80.7% of customers (64,554 of
   79,963) ordered only 1–4 items total.** The top revenue customer generated $1,487 — from
   a *single* order. Retention is the biggest untapped growth lever.
6. **Distribution centers are systematically understocked.** Across all 10 facilities,
   **understocked products outnumber overstocked ~10:1** — Chicago alone has 3,595
   understocked vs. 311 overstocked. Revenue is being lost to stockouts at scale.
7. **Zero-revenue products consume resources.** Some products and brands generated **$0 in
   completed revenue** despite having orders — 100% returned/cancelled/in-transit — yet
   still occupy inventory and processing capacity.
8. **Geographic concentration.** Three countries — **China, US, Brazil** — dominate
   revenue; per-customer spend is fairly uniform ($122–$131 in the top 5 markets).

---

## 9. Highest-Impact Recommendations

Every recommendation ties to a specific finding with a specific number — the project orders
them by estimated impact:

1. **Invest in platform-wide return reduction** (better sizing tools, photography, virtual
   try-on). Because the ~28% return rate is *uniform across all 26 categories*, one
   platform fix compounds catalog-wide. A 2-point reduction recovers thousands of lost
   orders with zero new customer acquisition.
2. **Rebalance distribution-center inventory** — fix the 10:1 understock ratio, prioritizing
   high-revenue/high-margin categories so premium items don't stock out.
3. **Launch retention campaigns at single-purchase customers** — the 64,554 one-to-four-item
   customers; converting even 5% adds ~3,200 repeat buyers, far cheaper than new
   acquisition.
4. **Renegotiate supplier costs for high-volume, low-margin brands** (Diesel, Wrangler,
   denim broadly) — use volume leverage to lift compressed margins toward the catalog
   average.
5. **Delist zero-revenue products** — items with 3+ orders and $0 completed revenue consume
   warehouse and fulfillment capacity for no return.
6. **Prioritize marketing spend on high-margin categories** — a $1 of Blazers & Jackets
   demand yields $0.62 profit vs. $0.44 for Tops & Tees; same budget, more profit.
7. **Build seasonal inventory planning from the trend data** — front-load outerwear before
   fall/winter peak, staff fulfillment for high-volume months, time clearance to demand
   troughs.

**The teachable point.** Each recommendation is *specific and defensible* — "reduce the
platform-wide ~28% return rate that is uniform across all 26 categories, suggesting
platform-level UX as the root cause" beats a vague "reduce returns." Specificity is what
makes a data-driven recommendation credible.

---

## 10. SQL Concepts to Know Cold

**CTE (Common Table Expression)** — a named temporary result set defined with `WITH`; used
here in layered chains to build metrics in readable stages.

**Conditional aggregation** — `SUM(CASE WHEN condition THEN value ELSE 0 END)` (or `COUNT`)
— computing status-specific metrics in a single pass. The project's workhorse technique.

**Window function** — a function computed across a set of rows *related to the current
row*, without collapsing them. Uses here: `SUM(...) OVER()` (totals for shares) and
`RANK() OVER(ORDER BY ...)` (per-metric ranking).

**`OVER()` clause** — defines the window. Empty `OVER()` = the whole result set;
`OVER(ORDER BY x)` orders the window for ranking.

**`RANK()`** — assigns a rank by an ordering; ties get the same rank.

**Aggregate function vs. window function** — an aggregate (`SUM` with `GROUP BY`) collapses
rows into one; a window function (`SUM() OVER()`) keeps every row and adds the computed
value alongside.

**JOIN** — combining tables on a key; this project chains `order_items → orders →
products`.

**`GROUP BY`** — collapsing rows into one per group, for aggregation.

**`NULLIF(a, b)`** — returns `NULL` if `a = b`; wrapped around denominators (`NULLIF(x, 0)`)
to make division safe.

**`DATE_TRUNC` / `EXTRACT` / `DATE_DIFF`** — `DATE_TRUNC` snaps a date to a unit (month),
`EXTRACT(MONTH FROM ...)` pulls the calendar month, `DATE_DIFF` counts units between dates.

**`LIMIT`** — caps the row count (here, top/bottom 15).

**Derived metric** — a value computed in the query that isn't a raw column (margin, return
rate, share, rank).

**Standard SQL / GoogleSQL** — BigQuery's modern SQL dialect.

---

## 11. Limitations & Honest Caveats

Volunteer these — the project's own conclusion lists them, which itself shows maturity.

1. **Synthetic dataset.** `thelook_ecommerce` is Google's generated data, not a real
   company's. Pricing anomalies exist (socks at $903). The *methodology* is fully
   transferable; the specific dollar figures are illustrative.
2. **No cost-of-operations data.** Profit here is `sale_price − product cost` — it can't
   account for fulfillment costs, marketing spend, overhead, or return-processing costs.
   True net profitability would need those.
3. **No customer-journey data.** No clickstream, page views, cart abandonment, or marketing
   attribution — customer analysis is limited to *transactional* behavior, so the project
   can't explain *why* customers don't return.
4. **Trends not statistically tested.** The long-term and seasonal sections identify
   patterns *visually*; they don't apply formal time-series tests (stationarity,
   decomposition, forecasting) — those belong in Python or R.
5. **All findings are correlational.** "Improve sizing tools to reduce returns" is grounded
   in observed patterns but would need a controlled experiment (A/B test) to prove causal
   impact.
6. **The synthetic data regenerates.** Because BigQuery continuously generates new
   `thelook_ecommerce` rows, exact figures shift between query runs — the same dataset-drift
   nuance as any analysis on this public dataset.

**Natural future extensions** (named in the conclusion): customer cohort/retention
analysis, RFM segmentation, market-basket analysis, and predictive return-probability
modeling — each building on this SQL foundation but needing tools beyond SQL.

---

## 12. Interview Q&A

Practice these out loud.

**Q1. Give me the overview of this project.**
"It's a multi-dimensional SQL analysis of a large e-commerce dataset — Google's public
thelook_ecommerce in BigQuery, about 181,000 order items and 80,000 customers. I wrote 92
queries structured across 10 analytical dimensions — top and bottom products, brands, and
categories, plus trends, customers, and distribution centers. Every query examines an
entity from six to eight metric angles at once, and every section ends with a concrete
business recommendation. The whole thing is SQL-native — nothing was exported."

**Q2. Walk me through the structure of a typical query.**
"Every analytical query uses a layered-CTE pattern. The first layer joins the tables, groups
by the entity, and does raw conditional aggregation — sum of sale price where status is
Complete for revenue, count where status is Returned for returns, and so on. The second
layer takes those raw totals and derives the ratios that don't exist in the raw data —
profit margin, return rate, revenue share. Then the final layer ranks the entity on every
metric with RANK() OVER, orders by the relevant rank, and limits to the top 15. Each layer
has one job, so the SQL stays readable and auditable."

**Q3. What's conditional aggregation and why is it central here?**
"It's putting a CASE WHEN inside a SUM or COUNT. The order_items table has a status column —
Complete, Returned, Cancelled, Shipped, Processing — and almost every metric I need is
status-specific. Instead of running separate queries, I compute them all in one pass: sum
sale_price where status is Complete gives revenue, sum where status is Returned or
Cancelled gives lost revenue. One scan of the data, every metric. It's the workhorse
technique of the whole project."

**Q4. How did you define revenue, and why that way?**
"Revenue is the sum of sale_price for completed items only — status equals Complete. An
order that was placed but returned or cancelled contributes zero to revenue; instead it
goes into a separate metric, lost revenue. That split is the analytical backbone of the
project — it's what let me show that for many top products, the lost revenue from returns
and cancellations actually rivals the revenue they earned."

**Q5. What's the difference between a window function and a regular aggregate?**
"A regular aggregate with GROUP BY collapses rows — many rows become one. A window function
keeps every row and adds a computed value alongside it. I used two. SUM with an empty OVER
clause sums across the whole result, so I can divide each entity's revenue by the total to
get its revenue share without collapsing the table. And RANK OVER ORDER BY ranks every
entity on a metric — I rank on every metric at once, so one query tells me a product is
number one in revenue but number ten in volume."

**Q6. What was your single most important finding?**
"That return rates are systemic, not category-specific. All 26 categories had return rates
in a tight 27 to 31 percent band. That uniformity is the insight — if returns were a
product-quality problem, you'd see big variation between categories. The fact that it's
flat everywhere means the root cause is platform-level: the return policy, the product
photography, the sizing tools. And that changes the recommendation completely — a single
platform-wide fix compounds across the entire catalog, whereas chasing individual products
would barely move the needle."

**Q7. Why analyze 'bottom' performers, not just 'top'?**
"Because analyzing only winners gives you half the picture. The bottom sections are where
the business is bleeding — zero-revenue products that are 100% returned or cancelled,
categories with compressed margins, customers who serial-return. Knowing what to stop doing
is as valuable as knowing what to double down on. A company that only watches its best
sellers misses the products quietly eroding profitability."

**Q8. Revenue versus profit — why do you keep separating them?**
"Because they tell opposite stories. Outerwear and Coats is number one in revenue but only
number ten in volume. Blazers and Jackets has the best margin at 62 percent but ranks
fifteenth in revenue. Jeans is number two in revenue but number twenty-one in margin. A
strategy optimized for revenue looks fundamentally different from one optimized for profit —
and you only see that by ranking on both at once."

**Q9. How did you prevent divide-by-zero errors?**
"NULLIF on every denominator. Profit margin is profit divided by NULLIF of revenue and
zero. If revenue is zero, NULLIF turns it into NULL, and dividing by NULL gives NULL
instead of throwing an error. With thousands of products — some with zero completed orders
— that safety is essential, otherwise the whole query fails."

**Q10. What would you do to extend this project?**
"A few things, all named in my conclusion. Cohort and retention analysis to track repeat
purchasing over time. RFM segmentation — scoring customers on recency, frequency, and
monetary value. Market-basket analysis for which products sell together. And a predictive
return-probability model. Those go beyond SQL into Python or R, but they build naturally on
this foundation. I'd also be honest that all my current findings are correlational — a
recommendation like 'better sizing tools reduce returns' would need an A/B test to confirm
causally."

**Q11. Why do this entirely in SQL instead of exporting to Python?**
"To demonstrate that SQL is a full analytical engine, not just an extraction language. I
joined six tables, computed conditional aggregations, built multi-layer derived metrics,
and ranked across 29,000 products and 2,700 brands — all in BigQuery, nothing exported. For
this kind of cross-dimensional business analysis, SQL is the right and sufficient tool. I'd
reach for Python only for the things SQL genuinely can't do well — time-series modeling,
machine learning."

---

## 13. How to Walk Through This Project Live

If asked to screen-share:

1. **State the framework first** — "10 analytical dimensions, every entity examined from 6
   to 8 metric angles, every section ending in a recommendation, all in BigQuery SQL."
2. **Open one representative query** (e.g., "Top products by revenue") and **walk the
   layered CTEs** — first layer raw conditional aggregation, second layer derived ratios
   and shares, final layer the RANK() OVER cross-metric ranking. This is the technical
   core; spend time here.
3. **Explain conditional aggregation** with the revenue / lost-revenue example — one scan,
   status-specific metrics.
4. **Show the multi-rank payoff** — point at a product that's #1 revenue / #10 volume / #21
   margin and explain why seeing all ranks at once matters.
5. **Walk 2–3 headline findings** — the systemic ~28% return rate, lost revenue rivaling
   earned revenue, the 80.7% single-purchase customers.
6. **Close on recommendations** — platform-wide return reduction, inventory rebalancing,
   retention campaigns. End on the decisions, not the SQL.

**Pacing tip:** spend the most time on the **layered-CTE pattern** and **conditional
aggregation** — those are the differentiated SQL skills — and on the **return-rate
systemic finding**, which is the smartest analytical observation in the project.

---

## 14. Glossary

- **BigQuery** — Google Cloud's serverless data warehouse; the SQL engine for this project.
- **`thelook_ecommerce`** — Google's public synthetic e-commerce dataset.
- **Standard SQL / GoogleSQL** — BigQuery's SQL dialect.
- **CTE (Common Table Expression)** — a named temporary result set defined with `WITH`.
- **Layered CTEs** — chaining CTEs (`first_layer → second_layer → third_layer`) so each
  builds on the last.
- **Conditional aggregation** — `SUM`/`COUNT` with a `CASE WHEN` inside, for status-specific
  metrics.
- **Window function** — a function computed over related rows without collapsing them.
- **`OVER()`** — the clause defining a window function's window.
- **`RANK()`** — a window function assigning rank by an ordering.
- **`SUM(...) OVER()`** — a window sum over the whole result, used for share calculations.
- **JOIN** — combining tables on a key.
- **`GROUP BY`** — collapsing rows into groups for aggregation.
- **`NULLIF(a,b)`** — returns NULL if a equals b; used for safe division.
- **`DATE_TRUNC` / `EXTRACT` / `DATE_DIFF`** — date-bucketing, calendar-part extraction, and
  date-interval functions.
- **Revenue** — sum of sale price for completed items only.
- **Profit** — revenue minus product cost.
- **Profit margin** — profit / revenue.
- **Return rate** — returned / (completed + returned).
- **Completion / cancellation / en-route rate** — status-share metrics (see §6).
- **Lost revenue / lost profit** — revenue/profit forgone to returned and cancelled orders.
- **Revenue share** — an entity's fraction of total revenue.
- **Derived metric** — a value computed in-query that isn't a raw column.
- **Order status** — `order_items.status`: Complete, Returned, Cancelled, Shipped,
  Processing.
- **Paired top/bottom analysis** — analyzing best and worst performers together.

---

*This study guide documents the project as built. The authoritative references are the 92
SQL files in `queries/`, the result CSVs in `csv-return-tables/`, and the portfolio page
`index.md`. When this guide and the queries disagree, the queries win.*