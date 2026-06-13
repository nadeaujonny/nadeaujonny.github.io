# Master Outline & Study Guide
## Cohort Retention Analysis — BigQuery SQL + Looker Studio Dashboard

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.
>
> **One sentence to anchor everything:** This project takes raw e-commerce transaction
> data, writes seven BigQuery SQL queries that turn it into six cohort-retention analyses,
> and surfaces the results through an interactive Looker Studio dashboard — the whole
> pipeline being *raw data → SQL → insight → dashboard*.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Business Context)](#2-why-this-project-exists-business-context)
3. [The Tech Stack at a Glance](#3-the-tech-stack-at-a-glance)
4. [End-to-End Workflow](#4-end-to-end-workflow)
5. [The Dataset: theLook eCommerce](#5-the-dataset-thelook-ecommerce)
6. [Core SQL Concepts & Techniques (Study This First)](#6-core-sql-concepts--techniques-study-this-first)
7. [Analysis 1 — Cohort Sizing](#7-analysis-1--cohort-sizing)
8. [Analysis 2 — Customer Retention Matrix](#8-analysis-2--customer-retention-matrix)
9. [Analysis 3 — Revenue Retention by Cohort](#9-analysis-3--revenue-retention-by-cohort)
10. [Analysis 4 — Retention by Acquisition Channel](#10-analysis-4--retention-by-acquisition-channel)
11. [Analysis 5 — Customer Lifecycle Segmentation](#11-analysis-5--customer-lifecycle-segmentation)
12. [Analysis 6 — Cumulative Revenue & Customer LTV](#12-analysis-6--cumulative-revenue--customer-ltv)
13. [The Looker Studio Dashboard](#13-the-looker-studio-dashboard)
14. [Key Results & Insights (Consolidated)](#14-key-results--insights-consolidated)
15. [KPI & Definitions Reference](#15-kpi--definitions-reference)
16. [Limitations & Honest Caveats](#16-limitations--honest-caveats)
17. [Design Decisions & Trade-offs (the "Why")](#17-design-decisions--trade-offs-the-why)
18. [Interview Q&A](#18-interview-qa)
19. [How to Walk Through This Project Live](#19-how-to-walk-through-this-project-live)
20. [Glossary](#20-glossary)

---

## 1. The 30-Second Pitch

This project is an **end-to-end cohort retention analysis** built on **Google BigQuery
SQL** and delivered through an **interactive Looker Studio dashboard**. It uses the public
`thelook_ecommerce` dataset — a simulated online retailer — and answers a single strategic
question from six angles: **once we acquire a customer, do they stay, and what are they
worth?**

The six analyses are: (1) **cohort sizing** — how many new customers we acquire each
month; (2) the **retention matrix** — what % of each cohort comes back month over month;
(3) **revenue retention** — how cohort *spending* evolves vs. its first month; (4)
**retention by acquisition channel** — which traffic sources produce durable customers;
(5) **lifecycle segmentation** — splitting customers into Active / At-Risk / Churned and
counting reactivations; and (6) **cumulative LTV** — running revenue per customer by cohort.

The headline finding: **retention is the business's biggest weakness** — Period-1 customer
retention sits below 2% across all 72 cohorts, 78% of the 14,997 customers are churned, and
lifetime value plateaus around $100–$110. The analysis turns that into concrete
recommendations about onboarding, win-back campaigns, and acquisition-cost ceilings.

**One-line version:** "I built a six-part cohort retention analysis in BigQuery SQL — using
CTEs, window functions, and date logic — and shipped it as a self-service Looker Studio
dashboard that turns raw transaction data into retention and LTV insights."

**Live dashboard:** https://lookerstudio.google.com/reporting/44cf727a-85c5-4eca-9ba2-b2553d5164ae

---

## 2. Why This Project Exists (Business Context)

**The business problem.** Acquiring a customer costs money — ad spend, sales effort,
discounts. That cost is only worth it if the customer *stays* and keeps buying. Retention,
not acquisition, is the lever that compounds: a business that retains well grows on a
smaller acquisition budget. So the question every growth/marketing team needs answered is:
**after we pay to acquire a customer, how long do they stay, when do they churn, and which
acquisition channels produce the most durable customers?**

**Why cohort analysis specifically.** A single blended "retention rate" hides everything
useful. Cohort analysis groups customers by *when they were acquired* (their "cohort") and
tracks each group separately over time. That lets you answer: are *newer* cohorts retaining
better than *older* ones (i.e., are our product/CX investments working)? Is a retention dip
a real trend or just one bad month? Cohorts make retention *comparable* and *diagnosable*.

**The simulated role.** The project frames the analyst as supporting the **growth and
marketing teams at an e-commerce company** — someone who must turn the raw orders table
into decisions about budget allocation, onboarding investment, and win-back campaigns.

**Why it's a strong portfolio project.** It demonstrates the full analyst loop end to end:
framing a business question, writing non-trivial SQL (CTEs, window functions, date math,
multi-table joins, segmentation logic), validating the output, interpreting it into
insight, and **delivering it as a self-service dashboard** a non-technical stakeholder can
actually use. It's not "I ran a query" — it's "I built a retention reporting product."

---

## 3. The Tech Stack at a Glance

| Tool | Role in the project | Why it was chosen |
|---|---|---|
| **Google BigQuery** | The SQL engine and data warehouse. All seven queries run here against the public `thelook_ecommerce` dataset. | Serverless, no setup, hosts the public dataset directly, handles the joins/window functions at scale. |
| **SQL (BigQuery Standard SQL / GoogleSQL)** | The analysis language — every cohort, retention %, and LTV figure is computed in SQL. | The right tool for set-based aggregation over transactional data. |
| **Google Looker Studio** | The dashboard / visualization layer. Connects to the query results and provides interactive filtering. | Free, integrates natively with BigQuery, produces an embeddable, shareable self-service report. |
| **GitHub** | Version control for the SQL files, result CSVs, and project documentation. | Standard source control; makes the work inspectable. |
| **GitHub Pages** | Publishes the portfolio write-up (`index.md`) with the embedded live dashboard. | Free static hosting for the project page. |
| **CSV exports** | The seven query results are saved as CSVs in `results/` — the frozen snapshot of each query's output. | A reproducible record; also a possible data source for Looker Studio. |

**The mental model:** BigQuery is where the *thinking* happens (SQL), Looker Studio is
where the *communication* happens (dashboard), GitHub/Pages is where the *evidence* lives
(queries + results + write-up).

---

## 4. End-to-End Workflow

```
  bigquery-public-data.thelook_ecommerce   (public simulated e-commerce dataset)
        │   tables used: orders, order_items, users
        ▼
  ┌───────────────────────────────────────────────────────────┐
  │ BIGQUERY — 7 SQL queries, one per analysis step            │
  │  query-0   → Analysis 1: cohort sizing                      │
  │  query-1   → Analysis 2: customer retention matrix          │
  │  query-2   → Analysis 3: revenue retention                  │
  │  query-3   → Analysis 4: retention by acquisition channel   │
  │  query-4a  → Analysis 5: lifecycle segmentation             │
  │  query-4b  → Analysis 5: reactivation count (bonus)         │
  │  query-5   → Analysis 6: cumulative revenue / LTV           │
  └───────────────────────────┬───────────────────────────────┘
                              │  results exported
                              ▼
  ┌───────────────────────────────────────────────────────────┐
  │ results/*.csv  — 7 frozen result snapshots                  │
  └───────────────────────────┬───────────────────────────────┘
                              │  connected as data
                              ▼
  ┌───────────────────────────────────────────────────────────┐
  │ LOOKER STUDIO — interactive dashboard                       │
  │  retention matrices · revenue retention · channel compare   │
  │  · lifecycle segments · LTV curves · filters & controls     │
  └───────────────────────────┬───────────────────────────────┘
                              │  embedded via iframe
                              ▼
  ┌───────────────────────────────────────────────────────────┐
  │ GITHUB PAGES — portfolio write-up (index.md)                │
  │  business questions · SQL · results tables · insights ·     │
  │  recommendations · the live embedded dashboard              │
  └───────────────────────────────────────────────────────────┘
```

**The repo layout** (`projects/cohort-retention-looker-studio/`):

- `index.md` — the portfolio page: every analysis with its business question, SQL, results
  table, insights, and recommendations, plus the embedded dashboard.
- `queries/` — the seven `.sql` files (the actual BigQuery queries).
- `results/` — the seven result CSVs (the exported output of each query).
- `looker-studio-files/` — the dashboard `embed-code` (iframe) and `project-link` (URL).

**A naming note worth knowing:** the SQL filenames don't line up 1:1 with the analysis
numbers — they're numbered by an internal query index, not by analysis. The mapping:

| Analysis | SQL file | Result CSV |
|---|---|---|
| 1 — Cohort sizing | `cohort-analysis-query-0.sql` | `cohort-analysis-query-0-results.csv` |
| 2 — Retention matrix | `cohort-retention-project-query-1.sql` | `cohort-analysis-query-1-results.csv` |
| 3 — Revenue retention | `cohort-analysis-query-2.sql` | `cohort-analysis-query-2-results.csv` |
| 4 — Retention by channel | `cohort-analysis-project-query-3.sql` | `cohort-analysis-query-3-results.csv` |
| 5 — Lifecycle segments | `cohort-analysis-query-4a.sql` | `cohort-analysis-query-4a-results.csv` |
| 5 — Reactivations (bonus) | `cohort-analysis-query-4b.sql` | `cohort-analysis-query-4b-results.csv` |
| 6 — Cumulative LTV | `cohort-analysis-query-5.sql` | `cohort-analysis-query-5-results.csv` |

---

## 5. The Dataset: theLook eCommerce

**What it is.** `bigquery-public-data.thelook_ecommerce` is a **public BigQuery dataset**
that simulates an online retail business. It's maintained by Google as a free sample
dataset — anyone with a BigQuery account can query it. It contains transactional order
data, line-item purchases, product attributes, and customer records.

**The three tables this project uses:**

| Table | Grain (what one row is) | Key columns used |
|---|---|---|
| `orders` | One row per **order** | `order_id`, `user_id`, `created_at`, `status` |
| `order_items` | One row per **item purchased** within an order | `order_id`, `user_id`, `product_id`, `sale_price`, `created_at` |
| `users` | One row per **customer** | `id`, `traffic_source`, demographic fields |

**Why two order tables?** `orders` is the order-header grain (one row per order); a single
order can contain several items. `order_items` is the line-item grain (one row per item) —
and it's where **`sale_price`** lives, so **all revenue figures come from `order_items`**.
Headcount/retention come from `orders`; revenue comes from `order_items`. Knowing which
table to pull from for which metric is a core competency the project demonstrates.

**The two filters applied to (almost) every query — know these cold:**

```sql
WHERE status = 'Complete'
  AND created_at < '2025-01-01'
```

- **`status = 'Complete'`** — only count orders that actually completed. The dataset also
  has Cancelled, Returned, Processing, and Shipped statuses; including them would inflate
  retention and revenue with orders that didn't really "count."
- **`created_at < '2025-01-01'`** — bound the analysis window. This gives a **clean,
  closed analysis period** (data through end of 2024) so partial-month-2025 data doesn't
  distort the most recent cohorts.

**The join key for revenue queries.** `order_items` joins back to `orders` on
`order_items.order_id = orders.order_id` so the `status = 'Complete'` filter (which lives
on `orders`) can be applied to line items. `users` joins on `orders.user_id = users.id`.

**Important caveat about this dataset — see §16.** theLook is a *synthetic, continuously
regenerated* dataset. Its rows shift over time, so queries run on different dates return
slightly different numbers. This explains small reconciliation gaps across the project's
own results (e.g., the December 2024 cohort showing 550 customers in one query and 556 in
another). Be ready to explain this in an interview — it's a sign of understanding, not a bug.

---

## 6. Core SQL Concepts & Techniques (Study This First)

Every query in this project is built from the same handful of techniques. Master these six
and you can explain any query in the project.

### 6.1 Common Table Expressions (CTEs) — `WITH ... AS (...)`

A CTE is a **named, temporary result set** defined with `WITH` that exists only for the
duration of the query. The project uses CTEs to break a complex analysis into **readable,
modular steps**, each one feeding the next. The retention matrix query, for example, is
four CTEs chained together: assign cohorts → capture activity → compute periods → compute
cohort sizes → final SELECT joins the last pieces.

**Why CTEs instead of subqueries:** readability and debuggability. Each CTE can be
SELECT-ed on its own to inspect its output, and the names (`customer_cohorts`,
`monthly_activity`) document intent. An interviewer asking "why CTEs?" wants exactly that
answer: *modularity, readability, and the ability to test each step in isolation.*

### 6.2 The cohort-assignment pattern (the project's foundational idiom)

This exact block appears in five of the seven queries — it is the heart of the project:

```sql
SELECT
  user_id,
  DATE(DATE_TRUNC(MIN(created_at), MONTH)) AS cohort_month
FROM `bigquery-public-data.thelook_ecommerce.orders`
WHERE status = 'Complete' AND created_at < '2025-01-01'
GROUP BY user_id
```

Read it as: for each customer (`GROUP BY user_id`), find their **earliest** completed
order (`MIN(created_at)`), truncate that timestamp to the **first day of its month**
(`DATE_TRUNC(..., MONTH)`), and call it that customer's **cohort month**. Every customer
belongs to exactly one cohort — the month of their first purchase.

### 6.3 `DATE_TRUNC` and `DATE_DIFF` — the date math

- **`DATE_TRUNC(timestamp, MONTH)`** — "snaps" a timestamp down to the start of its month.
  `2024-07-23` → `2024-07-01`. This is how customers get grouped into *monthly* cohorts
  rather than each having a unique day.
- **`DATE_DIFF(activity_month, cohort_month, MONTH)`** — counts the number of months
  between two dates. This produces the **`period_number`**: 0 = the cohort's first month,
  1 = the next month, etc. Period number is the x-axis of every retention curve.
- **`DATE(...)`** wraps the result to cast a `TIMESTAMP`/`DATETIME` down to a clean `DATE`,
  which keeps the grouping keys consistent and the joins clean.

### 6.4 Window functions — `LAG()` and `SUM() OVER (...)`

A window function computes a value across a set of rows *related to the current row*,
**without collapsing them into one row** (unlike `GROUP BY`). The project uses two:

- **`LAG(DATE(created_at)) OVER (PARTITION BY user_id ORDER BY created_at)`** — for each
  order, look at the **previous** order *by the same customer*. Subtract the two dates and
  you get the gap between consecutive orders — used to detect reactivations (Analysis 5).
- **`SUM(period_revenue) OVER (PARTITION BY cohort_month ORDER BY period_number)`** — a
  **running total**: for each cohort, accumulate revenue period by period. This is how
  cumulative revenue (and therefore LTV) is computed in Analysis 6.

The `PARTITION BY` clause restarts the window per group (per customer, per cohort); the
`ORDER BY` clause defines the sequence the function walks.

### 6.5 `CASE` statements — segmentation logic

`CASE WHEN ... THEN ... ELSE ... END` turns a continuous number into labeled buckets. In
Analysis 5 it converts `days_since_last_order` into `Active` / `At-Risk` / `Churned`. The
ordering of the `WHEN` clauses matters — the first match wins, so the thresholds cascade
(`<= 90` → Active, then `<= 180` → At-Risk, else Churned).

### 6.6 Multi-table joins & self-joins

- **Multi-table joins** — revenue queries join `order_items` → `orders` (to filter on
  status) and channel analysis joins `orders` → `users` (to bring in `traffic_source`).
- **Self-join pattern (baseline comparison)** — the revenue retention query computes each
  cohort's Period-0 revenue in its own CTE (`period_zero_revenue`) and joins it back to
  every period of the same cohort, so every row can be expressed as a % of its own
  baseline. It's a "join a table to a filtered version of itself" pattern.

### 6.7 The retention-rate formula — the metric every query orbits

```
retention_pct = active_users / cohort_size * 100
```

`ROUND(..., 2)` keeps it to two decimals. Revenue retention swaps in revenue figures;
cumulative LTV divides cumulative revenue by cohort size. Every headline number in the
project is one of these three ratios.

---

## 7. Analysis 1 — Cohort Sizing

**SQL file:** `cohort-analysis-query-0.sql` · **Result:** `cohort-analysis-query-0-results.csv` (72 rows)

**Business question.** How many new customers do we acquire each month, and how has
acquisition volume changed over time?

**Why it's first.** Every later analysis needs a *denominator* — you can't compute a
retention *percentage* without knowing how big each cohort was. This query establishes that
baseline.

**How the SQL works.** It's a two-level query (an inner subquery feeding an outer
aggregation):

1. **Inner subquery** — runs the cohort-assignment pattern: `GROUP BY user_id`,
   `MIN(created_at)`, `DATE_TRUNC(..., MONTH)` → one row per customer with their
   `cohort_month`.
2. **Outer query** — `GROUP BY cohort_month`, `COUNT(DISTINCT user_id)` → one row per
   month with `new_customers`, ordered chronologically.

**`COUNT(DISTINCT user_id)`** is used (rather than plain `COUNT`) as a safety measure — the
inner query already produces one row per user, but `DISTINCT` guarantees no double-count.

**Results.** 72 monthly cohorts, January 2019 → December 2024, totaling **14,997 unique
customers**. Cohort sizes grow steadily: 2 customers in Jan 2019 → 550 in Dec 2024.

**Insights.**
- Acquisition grew **~275×** over the window (2 → 550) — strong, sustained growth with no
  visible plateau.
- 2019 averaged ~26 new customers/month; 2024 averaged ~458 — clear year-over-year
  acceleration.
- **December is consistently the biggest cohort** each year (47 → 107 → 168 → 301 → 430 →
  550) — a recurring seasonal acquisition spike.

**Recommendations.** Track cohort size monthly to catch growth slowdowns early; overlay
acquisition *cost* per cohort to test whether the 275× volume growth is cost-efficient;
lean into the December seasonality with aligned campaigns.

**Interview angle.** Be ready for "why count distinct here?" and "what is a cohort, in your
own words?" — a cohort is a group of customers bucketed by a shared start event (here, the
month of first completed purchase).

---

## 8. Analysis 2 — Customer Retention Matrix

**SQL file:** `cohort-retention-project-query-1.sql` · **Result:** `cohort-analysis-query-1-results.csv` (936 rows)

**This is the core analysis of the project. Know its CTE chain cold.**

**Business question.** What percentage of each monthly cohort returns to make a purchase in
subsequent months?

**How the SQL works — four CTEs feeding a final SELECT:**

1. **`customer_cohorts`** — the cohort-assignment pattern: one row per customer with their
   `cohort_month`.
2. **`monthly_activity`** — `SELECT DISTINCT user_id, DATE_TRUNC(created_at, MONTH)` → every
   *distinct month* each customer placed a completed order. `DISTINCT` is essential here:
   if a customer ordered three times in March, we only want March counted once.
3. **`retention_data`** — joins cohorts to activity on `user_id`, computes
   `period_number = DATE_DIFF(activity_month, cohort_month, MONTH)`, and counts
   `active_users` per `(cohort_month, period_number)`. This is the matrix's body.
4. **`cohort_sizes`** — `COUNT(DISTINCT user_id)` per cohort → the denominator.

The **final SELECT** joins `retention_data` to `cohort_sizes` on `cohort_month` and
computes `retention_pct = active_users / cohort_size * 100`, filtered to
`period_number >= 0`, ordered by cohort then period.

**The output shape.** Each row is one **cohort-period pair**: "the January-2024 cohort, 3
months in, had N active users = X% retention." Pivot cohort_month against period_number and
you get the classic triangular **retention heatmap**.

**Why `period_number >= 0`.** It's a guard. A customer's activity should never predate
their cohort month (the cohort month *is* their first order), but the filter defends
against any edge case producing a negative period.

**Results.** **936 cohort-period pairs** across 72 cohorts. Period 0 is always 100% (by
definition — the whole cohort is active in its first month). The drop after Period 0 is
severe: the July 2024 cohort falls from 100% to ~1.3% at Period 1.

**Insights.**
- Retention collapses after Period 0 — **Period 1 retention is consistently below 2%**
  across every cohort. This is the project's single most important finding.
- The matrix is **sparse** — most customers buy once and don't return in consecutive
  months; when they do return it's often much later.
- The pattern holds for large recent cohorts too, so it's a **product-wide behavior**, not
  a cohort-specific fluke.

**Recommendations.** Invest in **Month-1 activation** (post-purchase emails, incentives,
reminders) — it's the highest-leverage fix; set per-period retention targets and flag
underperforming cohorts; watch whether newer cohorts retain better over time as a signal
that CX investments are working.

**Interview angle.** Expect "walk me through this query." Narrate the four CTEs in order
and say *what each produces*. Also expect "why is Period 0 always 100%?" — because the
cohort is *defined* by first purchase, so 100% of it is active in month 0.

---

## 9. Analysis 3 — Revenue Retention by Cohort

**SQL file:** `cohort-analysis-query-2.sql` · **Result:** `cohort-analysis-query-2-results.csv` (917 rows)

**Business question.** How does cohort *revenue* evolve over time relative to the first
month — are retained customers spending more or less?

**The key idea.** Analysis 2 counted *heads*; this counts *dollars*. It measures each
cohort-period's revenue as a percentage of that cohort's **Period-0 (baseline) revenue**.

**How the SQL works — four CTEs:**

1. **`customer_cohorts`** — the standard cohort-assignment pattern.
2. **`monthly_revenue`** — joins `order_items` to `orders` (so the `status='Complete'`
   filter applies), and computes `SUM(sale_price)` per `(user_id, activity_month)`.
   **Revenue comes from `order_items.sale_price`** — this is the table-grain point from §5.
3. **`revenue_by_period`** — joins cohorts to monthly revenue, computes `period_number` via
   `DATE_DIFF`, and sums revenue per `(cohort_month, period_number)`.
4. **`period_zero_revenue`** — filters `revenue_by_period` to `period_number = 0`,
   exposing each cohort's `baseline_revenue`. This is the **self-join baseline pattern**:
   one slice of a result set is joined back against all of it.

The **final SELECT** joins every period's revenue to its cohort's baseline and computes
`revenue_retention_pct = period_revenue / baseline_revenue * 100`.

**How to read it.** Revenue retention **above 100%** would mean retained customers spend
more in a later period than the *entire original cohort* spent in month 0. In this dataset
it's almost always far below 100% (because so few customers return).

**Results.** **917 cohort-period pairs.** Baseline revenue scales with cohort size — from
**$83 (Jan 2019) to $47,454 (Dec 2024)**.

**Insights.**
- Period-1 revenue retention runs **2–6%** — *higher* than customer retention (~1–2%). The
  implication: customers who *do* return place **moderately larger orders**.
- Occasional spikes in late periods (e.g., a Sept-2020 cohort showing 8.4% at Period 51)
  reflect rare large purchases by long-dormant customers.
- Baseline revenue growth (~$83 → ~$47K) reflects both bigger cohorts *and* rising average
  order value over time.

**Recommendations.** Track revenue retention *alongside* customer retention — the gap
proves retained customers are disproportionately valuable; invest in loyalty/personalized
recommendations; flag cohorts where revenue decays faster than headcount (a pricing or
engagement warning sign).

**Interview angle.** Be ready for "why does revenue retention beat customer retention?" —
because the few returners spend above the cohort's average order size, so each returning
*head* carries more than its proportional share of *dollars*. Also: "what does >100%
revenue retention mean, and why don't you see it here?"

---

## 10. Analysis 4 — Retention by Acquisition Channel

**SQL file:** `cohort-analysis-project-query-3.sql` · **Result:** `cohort-analysis-query-3-results.csv` (203 rows)

**Business question.** Which acquisition channels produce the most durable customers, and
how does retention vary by traffic source?

**The key structural change.** This query swaps the grouping dimension. Instead of grouping
retention by *cohort month*, it groups by **`traffic_source`** (the acquisition channel)
across all cohorts combined. It answers "which *channel* retains," not "which *month*
retains."

**How the SQL works — four CTEs:**

1. **`customer_cohorts`** — same cohort-assignment pattern, but now it **joins `users`** on
   `orders.user_id = users.id` to pull in `traffic_source`. Note the `GROUP BY` includes
   `traffic_source`.
2. **`monthly_activity`** — distinct active months per customer (same as Analysis 2).
3. **`retention_data`** — joins cohorts to activity, but groups by
   `(traffic_source, period_number)` — so retention is aggregated *per channel per period*.
4. **`channel_sizes`** — `COUNT(DISTINCT user_id)` per `traffic_source` — the per-channel
   denominator.

Final SELECT: `retention_pct = active_users / channel_size * 100`.

**Results.** **203 channel-period pairs** across **5 channels**. Channel sizes:

| Channel | Customers | Share |
|---|---|---|
| Search | 10,523 | ~70% |
| Organic | 2,258 | ~15% |
| Facebook | 860 | ~6% |
| Email | 751 | ~5% |
| Display | 605 | ~4% |

**Insights.**
- **Search dominates** acquisition — ~70% of all customers come from it.
- **Facebook shows the highest Period-1 retention (~0.70%)** despite far smaller volume —
  those customers may arrive more engaged.
- **No channel exceeds ~1% retention at Period 1.** Churn is a **product-wide** problem,
  not a channel-quality problem — no channel is meaningfully "saving" the business.

**Recommendations.** Factor retention-adjusted LTV into **CAC** (customer acquisition cost)
math — Facebook's better early retention may justify a higher CAC; improve onboarding
across *all* channels (since none clears 1%); set per-channel retention benchmarks.

**Interview angle.** Expect "what changed between this query and the retention matrix?" —
the answer: the grouping dimension moved from `cohort_month` to `traffic_source`, and a
join to `users` was added. Also be ready to explain why concluding "churn is product-wide"
is *more* useful than finding a single bad channel.

---

## 11. Analysis 5 — Customer Lifecycle Segmentation

**SQL files:** `cohort-analysis-query-4a.sql` (segments) + `cohort-analysis-query-4b.sql` (reactivations)
**Results:** `cohort-analysis-query-4a-results.csv` (3 rows) + `cohort-analysis-query-4b-results.csv` (1 row)

**Business question.** What proportion of customers are currently Active, At-Risk, or
Churned — and how many have reactivated after a long gap?

**The key idea — a snapshot, not a time series.** Analyses 1–4 track cohorts *over time*.
This one takes a **single point-in-time photo** of the whole customer base as of a fixed
"as-of" date (`2024-12-31`) and buckets every customer by **recency** (how long since their
last order).

### 11a — Lifecycle segments (`query-4a`)

**How the SQL works:**

1. **`customer_activity`** — per customer: first order date, last order date, total order
   count, and **`days_since_last_order = DATE_DIFF('2024-12-31', MAX(created_at), DAY)`**.
   The hardcoded as-of date is what makes this a snapshot.
2. **`customer_segments`** — a **`CASE`** statement turns `days_since_last_order` into a
   label: **`<= 90` → Active**, **`91–180` → At-Risk**, **`> 180` → Churned**.
3. **Final SELECT** — `GROUP BY customer_status` and reports: customer count, **percent of
   total** via the window function `COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()`, average
   orders, and average days since last order.

*(The `SUM(COUNT(*)) OVER ()` is a neat trick: an empty `OVER ()` window sums the grouped
counts across all rows, giving each segment's share of the grand total in one pass.)*

**Note on the bonus CTE.** Query 4a *also* contains `order_gaps` and `reactivations` CTEs,
but the final SELECT only outputs the segment counts — those extra CTEs are unused scaffolding
in 4a. The reactivation number is actually produced by the separate, cleaner query 4b.

### 11b — Reactivations (`query-4b`)

A focused query: for each order, use **`LAG()`** to find the customer's previous order
date, compute `days_between_orders` with `DATE_DIFF`, and **count distinct customers who
ever had a gap greater than 90 days** between consecutive orders. That's a "reactivation" —
a customer who went quiet for 90+ days and came back.

**Results.**

| Status | Customers | % of total | Avg orders | Avg days since last order |
|---|---|---|---|---|
| Churned | 11,697 | 78.00% | 1.08 | 755 |
| Active | 1,771 | 11.81% | 1.12 | 44 |
| At-Risk | 1,529 | 10.20% | 1.13 | 134 |

**Reactivated customers: 1,015** — roughly **6.8%** of the 14,997-customer base.

**Insights.**
- **78% of customers are Churned** — averaging 755 days since last order and only ~1.08
  orders ever. The majority simply never come back after the first purchase.
- Only **11.81% are Active** — the genuinely engaged base.
- **1,015 customers reactivated** after a 90+ day gap — churn is *not always permanent*, so
  win-back campaigns have a proven, real audience.

**Recommendations.** Prioritize the **1,529 At-Risk** customers (still recoverable at ~134
days out) before they tip into Churned; build structured **win-back flows** (1,015 already
returned *organically* — campaigns should beat that); track segment movement monthly as a
retention-health pulse.

**Interview angle.** Be ready for "why a fixed as-of date instead of CURRENT_DATE?" —
reproducibility: hardcoding `2024-12-31` means the snapshot is stable and matches the
analysis window, whereas `CURRENT_DATE` would give a different answer every run. Also
expect "what's a reactivation and how did you detect it?" — `LAG()` over each customer's
orders, then a gap > 90 days.

---

## 12. Analysis 6 — Cumulative Revenue & Customer LTV

**SQL file:** `cohort-analysis-query-5.sql` · **Result:** `cohort-analysis-query-5-results.csv` (917 rows)

**Business question.** How does cumulative revenue per customer grow over time by cohort,
and which cohorts generate the highest long-term value?

**The key technique — a running total via a window function.** Analysis 3 measured each
period's revenue *in isolation*; this one **accumulates** it. The result is a curve that
only ever goes up, approximating each cohort's **lifetime value (LTV)** trajectory.

**How the SQL works — three CTEs + a windowed final SELECT:**

1. **`customer_cohorts`** — standard cohort assignment.
2. **`cohort_sizes`** — `COUNT(DISTINCT user_id)` per cohort (the per-customer denominator).
3. **`monthly_revenue`** — joins cohorts to `order_items` and `orders`, computes
   `period_number`, and sums `sale_price` per `(cohort_month, period_number)`.
4. **Final SELECT** — the centerpiece is the window function:

   ```sql
   SUM(period_revenue) OVER (
     PARTITION BY cohort_month
     ORDER BY period_number
   ) AS cumulative_revenue
   ```

   `PARTITION BY cohort_month` restarts the running sum for each cohort; `ORDER BY
   period_number` makes it accumulate in period order. Dividing that by `cohort_size`
   yields **`cumulative_revenue_per_customer`** — the LTV proxy.

**Why a window function, not a self-join.** You *could* compute a running total by joining
the table to itself on `period <= current_period`, but that's O(n²) and ugly. `SUM() OVER`
does it in one clean pass — exactly what window functions exist for.

**Results.** **917 cohort-period pairs.** Cumulative revenue per customer starts around
**$77–$95** at Period 0 (most lifetime value is captured in the *first* purchase) and the
curve is **shallow** afterward — mature cohorts reach only ~$105 over ~30 periods.

**Insights.**
- **The first purchase is most of the LTV.** The Period-0 figure is already most of the
  eventual total — the curve barely rises after.
- **LTV plateaus around $100–$110** for mature cohorts — an effective lifetime-value
  ceiling for this business.
- Newer cohorts start *higher* at Period 0 ($80–$90 in 2024 vs. $40–$70 in 2019),
  reflecting rising average order value or product-mix shift.

**Recommendations.** **Set CAC ceilings from LTV** — with LTV near $100–$110, acquisition
cost must stay well below that for healthy unit economics; compare cohort trajectories
(newer tracking below older = a monetization problem); use the mature-cohort curve shape to
**forecast** revenue from recent large cohorts.

**Interview angle.** The guaranteed question: "how does the running total work?" Answer
with the `SUM() OVER (PARTITION BY cohort ORDER BY period)` mechanics. Also: "why is LTV a
*proxy* here?" — because it's cumulative revenue per *cohort member*, not margin, and the
window is bounded at end-2024 so young cohorts haven't finished maturing.

---

## 13. The Looker Studio Dashboard

**What it is.** An interactive **Google Looker Studio** report that surfaces all six
analyses in one place, so a non-technical stakeholder (a marketing or growth lead) can
explore retention without writing SQL. It is the project's **delivery layer** — the thing
that turns the analysis into a *product*.

**How it's wired.** The dashboard connects to the BigQuery query results and provides
**filters and controls** to drill into specific cohorts, time periods, and acquisition
channels. It presents the retention matrices, revenue retention, channel comparison,
lifecycle segments, and LTV curves as interactive visuals.

**How it's embedded in the portfolio.** The repo's `looker-studio-files/` folder holds two
artifacts: `project-link` (the report URL,
`lookerstudio.google.com/reporting/44cf727a-85c5-4eca-9ba2-b2553d5164ae`) and `embed-code`
(the `<iframe>` snippet). The portfolio page (`index.md`) embeds that iframe so the live,
interactive dashboard renders directly on the GitHub Pages site.

**Why a dashboard at all — the portfolio point.** A query result is a dead artifact; a
dashboard is a **self-service tool**. The project deliberately ends in Looker Studio to
demonstrate the *last mile* of analytics work: making insight usable by people who will
never open BigQuery. In an interview, frame it as "I didn't just answer the question once —
I built something the team can keep asking questions of."

**Interview angle.** Expect "why Looker Studio?" — it's free, connects natively to
BigQuery, and produces an embeddable self-service report. And "who is the dashboard for?" —
growth/marketing stakeholders who need retention answers without SQL.

---

## 14. Key Results & Insights (Consolidated)

The numbers every interviewer will want. Memorize the headline figures.

| Metric | Value |
|---|---|
| Analysis window | Jan 2019 – Dec 2024 (`created_at < '2025-01-01'`, completed orders only) |
| Monthly cohorts | **72** |
| Total unique customers | **14,997** |
| Acquisition growth | 2 customers (Jan 2019) → 550 (Dec 2024) — **~275×** |
| Period-1 customer retention | **< 2%** across all 72 cohorts |
| Period-1 revenue retention | **2–6%** (higher than headcount retention) |
| Acquisition channels | 5 — Search (10,523 ≈ 70%), Organic (2,258), Facebook (860), Email (751), Display (605) |
| Best early-retention channel | Facebook (~0.70% Period 1) — but no channel exceeds ~1% |
| Lifecycle split (as of 2024-12-31) | Churned **78.0%** (11,697) · Active **11.81%** (1,771) · At-Risk **10.20%** (1,529) |
| Reactivated customers | **1,015** (~6.8% of base) — returned after a 90+ day gap |
| LTV plateau | **~$100–$110** cumulative revenue per customer for mature cohorts |
| Result rows by query | sizing 72 · retention 936 · revenue 917 · channel 203 · segments 3 · reactivations 1 · LTV 917 |

**The five takeaways (the story the project tells):**

1. **Early churn is the biggest lever.** Period-1 retention below 2% everywhere — onboarding
   and first-repeat activation deserve the most investment.
2. **Revenue retention ≠ headcount retention.** Returning customers spend more, so customer
   retention alone *understates* the value of loyalty. Track both.
3. **Channel quality varies, but churn is universal.** Search drives 70% of acquisition, yet
   no channel clears 1% Period-1 retention — this is a product problem, not a channel problem.
4. **Lifecycle segmentation is actionable.** 78% churned, but 1,529 At-Risk customers and
   1,015 proven reactivations are a concrete win-back audience.
5. **LTV drives strategy.** The ~$100–$110 LTV ceiling gives a hard cap for acquisition-cost
   planning.

---

## 15. KPI & Definitions Reference

| Term | Definition |
|---|---|
| **Cohort month** | The month of a customer's **first completed order**. Every customer has exactly one. |
| **Period number** | Months elapsed since the cohort month. **0 = the first month.** Computed with `DATE_DIFF`. |
| **Cohort size** | Count of distinct customers in a cohort — the denominator for retention %. |
| **Retention %** | `active_users / cohort_size × 100` — share of a cohort active in a given period. |
| **Revenue retention %** | `period_revenue / baseline_revenue × 100` — a period's revenue vs. the cohort's Period-0 revenue. |
| **Baseline revenue** | A cohort's Period-0 (first-month) revenue — the comparison point for revenue retention. |
| **Customer status** | Active (≤ 90 days since last order), At-Risk (91–180), Churned (> 180), measured as of 2024-12-31. |
| **Reactivation** | A customer returning after a 90+ day gap between two consecutive orders. |
| **Cumulative revenue per customer** | Running total of cohort revenue ÷ cohort size — the project's LTV proxy. |
| **`traffic_source`** | The acquisition channel a customer came from (Search, Organic, Facebook, Email, Display). |
| **`status = 'Complete'`** | The order-status filter — only completed orders count toward any metric. |

---

## 16. Limitations & Honest Caveats

Volunteer these before being asked — knowing the weaknesses of your own analysis signals
maturity.

1. **theLook is a synthetic, non-static dataset.** `bigquery-public-data.thelook_ecommerce`
   is continuously regenerated by Google, so the *same query* run on different dates
   returns slightly different numbers. This is visible inside the project's own outputs —
   e.g., the December-2024 cohort shows **550** customers in the sizing query but **556** in
   the retention-matrix query, and the July-2024 cohort shows 464 vs. 445 across queries.
   The portfolio page's row counts (e.g., "937 pairs") are likewise one or two higher than
   the saved CSVs (936). **None of this is an error** — it's the dataset shifting between
   query runs. The fix for a production version would be to **snapshot the source tables
   into a static table first**, then run all analyses against the frozen copy.
2. **Synthetic data behaves unrealistically.** Real e-commerce Period-1 retention is
   typically 20–40%, not <2%. theLook's order timestamps are generated semi-randomly, so
   the *retention pattern itself is an artifact of the simulation*. The **SQL methodology is
   the transferable skill**; the specific retention numbers wouldn't generalize to a real
   business. Be honest about this in interviews.
3. **Recent cohorts are right-censored.** A cohort acquired in December 2024 has only one
   month of observable history before the `< 2025-01-01` cutoff. Comparing a young cohort's
   LTV to a mature cohort's is apples-to-oranges — the young one simply hasn't had time.
4. **Revenue uses `sale_price`, not margin.** "LTV" here is cumulative *revenue* per
   customer, not profit. True LTV would subtract COGS, returns, and acquisition cost.
5. **The lifecycle snapshot is a single fixed date.** Active/At-Risk/Churned is measured
   only as of 2024-12-31; the segments would look different on any other date.
6. **No statistical testing.** Channel-retention differences (e.g., Facebook's 0.70% vs.
   Email's 0.27% at Period 1) are descriptive — with small channels (605–860 customers) the
   gaps may not be statistically significant. The project reads them directionally.
7. **Unused scaffolding in query 4a.** Query 4a contains `order_gaps` / `reactivations`
   CTEs that its final SELECT never uses — the reactivation count is delivered by the
   separate query 4b. Worth knowing so it doesn't surprise you in a code walkthrough.

---

## 17. Design Decisions & Trade-offs (the "Why")

Interviewers reward "why" answers. Here are the deliberate choices and their rationale.

**Why cohort analysis instead of a single blended retention rate?**
A blended rate averages away the signal. Cohorts make retention *comparable over time* —
you can see whether newer cohorts retain better than older ones, which is the only way to
tell if product/CX investments are actually working.

**Why CTEs instead of nested subqueries?**
Readability and debuggability. Each CTE is a named, testable step — you can SELECT any one
of them in isolation to verify it. A four-CTE query reads like a paragraph; the same logic
as nested subqueries reads like a puzzle.

**Why filter to `status = 'Complete'`?**
Cancelled, returned, and in-progress orders don't represent real, retained revenue.
Including them would inflate every retention and revenue figure with transactions that
didn't actually count.

**Why the `created_at < '2025-01-01'` cutoff?**
To get a clean, closed analysis window. A hard date boundary means the most recent cohorts
aren't distorted by a partial month of 2025 data, and the whole analysis is reproducible.

**Why measure the lifecycle snapshot from a hardcoded `2024-12-31` instead of `CURRENT_DATE`?**
Reproducibility. A hardcoded as-of date gives the same answer every time the query runs and
matches the analysis window. `CURRENT_DATE` would silently change the segment counts on
every run.

**Why compute revenue from `order_items` but retention from `orders`?**
Table grain. `orders` is one row per order (right for counting customer activity);
`order_items` is one row per item and is where `sale_price` lives (right for summing
revenue). Using the correct grain for each metric is the core data-modeling decision.

**Why a window function for the running total instead of a self-join?**
`SUM() OVER (PARTITION BY ... ORDER BY ...)` computes the cumulative total in one pass. A
self-join on `period <= current_period` would be slower, harder to read, and error-prone.

**Why end in a Looker Studio dashboard at all?**
Because a query result is a one-time answer and a dashboard is a reusable tool. The
dashboard demonstrates the last mile of analytics — making insight self-service for people
who don't write SQL.

**Why six analyses rather than one big query?**
Each analysis answers one business question and is independently understandable and
verifiable. Separating them mirrors how real analytics work is scoped and reviewed.

---

## 18. Interview Q&A

Practice these out loud. Answers are written the way you'd actually speak.

**Q1. Give me the overview of this project.**
"It's an end-to-end cohort retention analysis. I used BigQuery SQL on the public theLook
e-commerce dataset to answer one question from six angles — how many customers we acquire,
how well each monthly cohort retains, how their revenue retains, which acquisition channels
produce durable customers, how the base splits into Active/At-Risk/Churned, and how
cumulative lifetime value builds by cohort. Then I delivered all of it as an interactive
Looker Studio dashboard so a marketing team could explore it without SQL."

**Q2. What is a cohort, and how did you assign customers to one?**
"A cohort is a group of customers bucketed by a shared starting event. Here it's the month
of a customer's first completed order. In SQL I grouped the orders table by user_id, took
the MIN of created_at to get their first order, and truncated that to the month with
DATE_TRUNC. Every customer ends up in exactly one monthly cohort."

**Q3. Walk me through the retention matrix query.**
"It's four CTEs. The first, customer_cohorts, assigns every customer their cohort month.
The second, monthly_activity, gets every distinct month each customer ordered — distinct is
important so multiple orders in one month count once. The third, retention_data, joins
cohorts to activity on user_id and uses DATE_DIFF to compute the period number — months
since the cohort month — then counts active users per cohort-period. The fourth,
cohort_sizes, counts each cohort's total customers. The final SELECT joins those last two
and computes retention as active_users over cohort_size times 100."

**Q4. Why is retention so low — under 2% at Period 1?**
"Two things. First, in the data, most customers genuinely make a single purchase and don't
come back in the next month. But second — and I'd be upfront about this — theLook is a
synthetic dataset, and its order timestamps are generated semi-randomly, so the retention
*pattern* is partly an artifact of the simulation. Real e-commerce Period-1 retention is
more like 20–40%. The transferable part of this project is the SQL methodology, not the
specific percentages."

**Q5. What's the difference between customer retention and revenue retention?**
"Customer retention counts heads — what share of the cohort came back. Revenue retention
counts dollars — a period's revenue as a percentage of the cohort's first-month revenue. In
this project revenue retention runs higher than customer retention, which tells you the few
customers who return spend more than the cohort's average order. So loyalty is worth more
than a headcount metric alone suggests."

**Q6. How did you calculate cumulative LTV?**
"In the LTV query I summed each cohort-period's revenue, then used a window function —
SUM(period_revenue) OVER, partitioned by cohort month and ordered by period number — to get
a running total. Dividing that running total by the cohort size gives cumulative revenue
per customer, which is my LTV proxy. It showed LTV plateauing around $100 to $110 for
mature cohorts."

**Q7. Why a window function instead of a self-join for the running total?**
"A window function does it in a single pass — SUM OVER with a PARTITION BY and ORDER BY
walks the rows in order and accumulates. A self-join joining each period to all earlier
periods of the same cohort would be slower and much harder to read. Running totals are
exactly what window functions are designed for."

**Q8. How did you detect reactivated customers?**
"I used LAG. For each order, LAG over PARTITION BY user_id ORDER BY created_at gives the
customer's previous order date. DATE_DIFF between the two gives the gap in days. Any gap
over 90 days means the customer went dormant and came back — a reactivation. I counted
distinct customers with at least one such gap, and got 1,015, about 6.8% of the base."

**Q9. Why did you split revenue from order_items but retention from orders?**
"It's about table grain. The orders table is one row per order — right for counting whether
a customer was active. The order_items table is one row per item purchased, and it's where
sale_price lives — so any revenue figure has to come from order_items. For the revenue
queries I join order_items back to orders so I can still apply the completed-order filter."

**Q10. Why did you filter to completed orders and a 2025 cutoff?**
"Completed orders only, because cancelled or returned orders aren't real retained revenue —
counting them would inflate everything. And created_at before 2025-01-01 to get a clean,
closed window, so a partial month of 2025 doesn't distort the newest cohorts and the whole
analysis is reproducible."

**Q11. Which acquisition channel should the business invest in?**
"Search drives about 70% of customers, so it's the volume engine. Facebook had the best
early retention — around 0.70% at Period 1 versus 0.17% for Display — so on a
retention-adjusted basis Facebook customers may justify a higher acquisition cost. But the
honest headline is that *no* channel clears 1% Period-1 retention, so the real takeaway is
that churn is a product-wide problem and onboarding is the fix, not channel reallocation."

**Q12. I noticed your December 2024 cohort is 550 in one query and 556 in another. Why?**
"Good catch — that's the theLook dataset being non-static. Google continuously regenerates
it, so a query run on a different day sees slightly different rows even with the same date
filter. In a production setting I'd snapshot the source tables into a static table first
and run every analysis against that frozen copy so all the numbers reconcile exactly."

**Q13. What would you do differently or add next?**
"Three things. First, snapshot the source data so results are fully reproducible. Second,
add cohort-over-cohort comparison — explicitly testing whether newer cohorts retain better
than older ones. Third, bring in cost data — acquisition cost per channel and product
margin — so I could compute true LTV and a real LTV-to-CAC ratio instead of a
revenue-based proxy."

**Q14. What does Period 0 mean and why is its retention always 100%?**
"Period 0 is the cohort's first month. Retention there is 100% by definition — the cohort
is *defined* as the customers who first purchased that month, so 100% of them are active in
month 0. The interesting part is always the drop from Period 0 to Period 1."

**Q15. What's the single most important finding?**
"Early churn. Period-1 retention is below 2% across all 72 cohorts and 78% of customers end
up churned. Acquisition is growing nicely — about 275× over the window — but the business
is pouring customers into a leaky bucket. The highest-leverage investment isn't more
acquisition, it's onboarding and first-repeat activation."

---

## 19. How to Walk Through This Project Live

If asked to screen-share and walk through the project, use this order:

1. **Open the Looker Studio dashboard first.** Lead with the *outcome* — show the
   interactive retention matrix, the channel comparison, the lifecycle segments. Let them
   see the deliverable before the plumbing.
2. **State the business question** — "after we acquire a customer, do they stay, and what
   are they worth?" — and the six-analysis structure.
3. **Show the dataset** — `thelook_ecommerce`, the three tables (`orders`, `order_items`,
   `users`), and the two universal filters (`status = 'Complete'`,
   `created_at < '2025-01-01'`).
4. **Walk the retention matrix query** (`cohort-retention-project-query-1.sql`) — this is
   the core. Narrate the four CTEs in order and what each produces.
5. **Show one window-function query** — the LTV query (`query-5`) for `SUM() OVER`, or the
   reactivation query (`query-4b`) for `LAG()`. Pick whichever you can explain most
   fluently.
6. **Show a results CSV** — point out the cohort-period grain and the retention curve.
7. **Close with insight + recommendation** — "Period-1 retention is under 2%, so the
   business should invest in onboarding over more acquisition." End on the *decision*, not
   the SQL.
8. **Volunteer a limitation** — the synthetic, non-static dataset (§16). It signals
   maturity and pre-empts the "your numbers don't reconcile" question.

**Pacing tip:** spend the most time on the retention matrix query and one window-function
query. Those two demonstrate the headline SQL skills; the other analyses are variations on
the same patterns.

---

## 20. Glossary

- **Cohort** — a group of customers bucketed by a shared start event; here, the month of
  first completed purchase.
- **Cohort analysis** — tracking each cohort separately over time so retention is
  comparable and diagnosable.
- **Cohort month** — the month of a customer's first completed order (their cohort label).
- **Period number** — months elapsed since the cohort month; 0 = first month.
- **Retention %** — `active_users / cohort_size × 100`.
- **Revenue retention %** — a period's revenue as a % of the cohort's Period-0 revenue.
- **Baseline revenue** — a cohort's Period-0 (first-month) revenue.
- **Retention matrix** — the cohort × period grid of retention percentages; pivots into a
  triangular heatmap.
- **Churn** — a customer ceasing to purchase; here, > 180 days since last order.
- **Reactivation** — a customer returning after a 90+ day gap between orders.
- **LTV (lifetime value)** — total value a customer generates; proxied here by cumulative
  revenue per customer.
- **CAC** — customer acquisition cost; the LTV ceiling sets the budget for it.
- **CTE (Common Table Expression)** — a named temporary result set defined with `WITH`,
  used to build a query in modular steps.
- **Window function** — a function (`LAG`, `SUM() OVER`) computing across related rows
  without collapsing them into one.
- **`PARTITION BY`** — the window-function clause that restarts the calculation per group.
- **`LAG()`** — a window function returning a value from a previous row (used for
  order-gap detection).
- **`DATE_TRUNC`** — snaps a timestamp to the start of a unit (here, the month).
- **`DATE_DIFF`** — counts the units (months, days) between two dates.
- **Self-join** — joining a table to a filtered version of itself; used for the Period-0
  baseline comparison.
- **Table grain** — what a single row represents (`orders` = one order; `order_items` =
  one item).
- **`traffic_source`** — the acquisition channel field on the `users` table.
- **theLook eCommerce** — Google's public, synthetic e-commerce sample dataset in BigQuery.
- **BigQuery** — Google Cloud's serverless data warehouse; the SQL engine for this project.
- **Looker Studio** — Google's free dashboard/BI tool; the project's delivery layer.
- **Right-censored** — data cut off by the analysis window; recent cohorts have less
  observable history.

---

*This study guide documents the project as built. The authoritative references in the
project folder are the SQL files in `queries/`, the result snapshots in `results/`, the
portfolio write-up `index.md`, and the dashboard in `looker-studio-files/`. When this guide
and those files disagree, the files win.*
