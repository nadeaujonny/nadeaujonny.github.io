# Master Outline & Study Guide
## Tableau — Olist E-commerce Operations & Customer Experience Analysis

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.
>
> **One sentence to anchor everything:** This project is a **five-dashboard Tableau
> analysis** of the Olist Brazilian e-commerce marketplace (99,441 orders) — built on an
> 8-table relationship model — examining order fulfillment, revenue, customer reviews, and
> marketplace dynamics, and synthesizing all of it into an interactive executive summary
> with LOD expressions, parameters, and forecasting.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Context)](#2-why-this-project-exists-context)
3. [The Tech Stack](#3-the-tech-stack)
4. [The Dataset — Olist Brazilian E-commerce](#4-the-dataset--olist-brazilian-e-commerce)
5. [The Data Model — 8 Tables via Relationships](#5-the-data-model--8-tables-via-relationships)
6. [Calculated Fields & Advanced Tableau Techniques](#6-calculated-fields--advanced-tableau-techniques)
7. [Dashboard 1 — Order Fulfillment Performance](#7-dashboard-1--order-fulfillment-performance)
8. [Dashboard 2 — Revenue & Sales Performance](#8-dashboard-2--revenue--sales-performance)
9. [Dashboard 3 — Customer Experience & Review Quality](#9-dashboard-3--customer-experience--review-quality)
10. [Dashboard 4 — Marketplace Ecosystem (Products & Sellers)](#10-dashboard-4--marketplace-ecosystem-products--sellers)
11. [Dashboard 5 — Executive Summary](#11-dashboard-5--executive-summary)
12. [Key Findings (Consolidated)](#12-key-findings-consolidated)
13. [Tableau Concepts to Know Cold](#13-tableau-concepts-to-know-cold)
14. [Limitations & Honest Caveats](#14-limitations--honest-caveats)
15. [Interview Q&A](#15-interview-qa)
16. [How to Walk Through This Project Live](#16-how-to-walk-through-this-project-live)
17. [Glossary](#17-glossary)

---

## 1. The 30-Second Pitch

This project is a **comprehensive Tableau analysis** of the **Olist Brazilian e-commerce
marketplace** — **99,441 orders** spanning **September 2016 to August 2018**. It's built as
**five interconnected dashboards** that examine the marketplace from four perspectives —
**operational performance, financial health, customer satisfaction, and ecosystem
dynamics** — plus an executive summary that ties them together.

The whole analysis runs on an **8-table data model** connected through Tableau's
**relationship model** (not joins), with **calculated fields** for delivery time and late-
delivery flags, **LOD (Level of Detail) expressions** for month-over-month comparisons,
**parameters** for interactive filtering, and **Tableau's native forecasting** for a
3-month revenue projection.

The headline story: Olist's **core operations are strong** — a 97% completion rate,
delivery times that improved from 50+ days to 12.5, $15.8M revenue, 21% YoY growth — but
there are clear **pressure points**: a 6.8% late-delivery rate above the 5% target, a
strong link between delivery delays and falling review scores, and heavy revenue
concentration in São Paulo. Every dashboard ends in business recommendations.

**One-line version:** "I built a five-dashboard Tableau analysis of 99,000 Olist e-commerce
orders — on an 8-table relationship model with LOD expressions, parameters, and forecasting
— covering fulfillment, revenue, customer experience, and marketplace health, all
synthesized into an interactive executive summary."

---

## 2. Why This Project Exists (Context)

**The business problem.** E-commerce marketplaces live or die on **reliable fulfillment and
customer satisfaction** — late deliveries erode reviews, bad reviews erode repeat
purchases, and the whole flywheel slows. Operations, finance, and customer-experience teams
need *visibility* into delivery times, revenue trends, review-score drivers, and seller
health to make decisions. This project builds exactly that visibility.

**The four lenses.** The project deliberately examines the marketplace from four
interlocking perspectives, one dashboard each, plus a fifth that synthesizes them:
operational performance (fulfillment), financial health (revenue), customer satisfaction
(reviews), and ecosystem dynamics (products & sellers). The stated goal is to **move beyond
surface metrics and uncover the *relationships between* them** — where delivery performance
drives satisfaction, where geographic concentration is both a strength and a risk.

**Why it's a strong portfolio project.** It's the portfolio's flagship **Tableau** project,
and it demonstrates the tool's full depth — not just charts, but a proper relationship data
model, calculated fields, **LOD expressions**, parameter-driven interactivity, Top N sets,
native forecasting, and dashboard actions. It also demonstrates **analytical synthesis**:
five dashboards that each answer one question but *compound* when read together, ending in
an executive monitoring surface. It's published live on **Tableau Public**.

---

## 3. The Tech Stack

| | |
|---|---|
| **Tool** | **Tableau Desktop** (workbook published to Tableau Public) |
| **Deliverable** | `tableau_olist_ops_cx_v1_raw_load.twbx` — a packaged Tableau workbook |
| **Dataset** | Olist Brazilian E-commerce Public Dataset (Kaggle) |
| **Techniques** | Relationship data model · calculated fields · LOD expressions · parameters · Top N sets · native forecasting · dashboard actions |

**The mental model.** Tableau is doing three jobs here: it's the **data modeling layer**
(connecting 8 tables via relationships), the **calculation layer** (calculated fields and
LOD expressions that derive metrics not in the raw data), and the **visualization/delivery
layer** (5 dashboards). A `.twbx` is a "packaged workbook" — it bundles the workbook *and*
its data into one file, so it's fully portable.

**One connection detail worth knowing:** the data uses a **live connection** (rather than a
static extract), which the project notes was chosen for real-time filtering and
exploration during development.

---

## 4. The Dataset — Olist Brazilian E-commerce

**What it is.** The **Olist Brazilian E-commerce Public Dataset** from Kaggle — real
(anonymized) order data from **Olist**, a Brazilian marketplace that connects small sellers
to large e-commerce platforms.

| Attribute | Value |
|---|---|
| Total orders | **99,441** |
| Time range | September 2016 – August 2018 |
| Granularity | Order-level, with customer, seller, product, payment, and review detail |
| Total revenue | **$15.8M** |
| Average Order Value (AOV) | **$159.33** |
| Average review score | **4.09 / 5** |
| YoY revenue growth | **~21%** (2017 → 2018) |

**The 8 tables:**
- **Orders** — the central fact table; one row per order, with the timestamps that drive
  delivery analysis (purchase, delivered-to-customer, estimated delivery) and `order_status`.
- **Order Items** — one row per item in an order; carries `price` and `freight`.
- **Customers**, **Sellers** — the two sides of the marketplace.
- **Products** + **Product Category Translation** — product detail; the translation table
  maps Portuguese category names to English.
- **Order Payments** — payment method and value (credit card, boleto, etc.).
- **Order Reviews** — the 1–5 star review scores.

**A Brazil-specific detail to know:** **boleto** is a Brazilian bank-slip payment method —
~18% of revenue here — it matters because it serves *underbanked* customers who don't have
credit cards. The other ~80% of revenue is credit card (Brazilians lean heavily on
installment payments). Knowing what boleto is signals you understood the market context.

---

## 5. The Data Model — 8 Tables via Relationships

**A deliberate, defensible technical choice — know why it was made.**

The 8 tables are connected using **Tableau's relationship model**, *not* traditional joins.
The relationships:
- **`olist_orders_dataset`** is the **central fact table** (`order_id` primary key).
- Customers link via `customer_id`; Order Items link via `order_id` (many-to-one with
  orders); Products link via `product_id`; the Category Translation links via
  `product_category_name`; Sellers via `seller_id`; Payments and Reviews via `order_id`.

**Relationships vs. joins — the interview point.** A traditional **join** physically merges
tables into one flat result *at one fixed granularity* — which causes **double-counting**
when you mix tables of different grain (e.g., joining order-level data to item-level data
multiplies the order rows). Tableau's **relationship model** is "smarter": it keeps the
tables separate and **lets Tableau choose the right join and granularity per visualization
at query time.** So a chart counting *orders* aggregates at order grain, and a chart
summing *item revenue* aggregates at item grain — from the *same* model, with no
double-counting. That flexibility "across different levels of analysis" is exactly why
relationships were chosen over joins.

**Data preparation:** calculated fields were built for delivery-time analysis, the
late-delivery flag was built by comparing actual to estimated delivery date, and
delivery/completion metrics were filtered to `"delivered"` orders.

---

## 6. Calculated Fields & Advanced Tableau Techniques

**The metrics that drive the dashboards don't exist in the raw data — they're built with
calculated fields. Know these.**

### 6.1 Core calculated fields

- **`Delivery Days`** = `DATEDIFF('day', [Order Purchase Timestamp], [Order Delivered
  Customer Date])` — the number of days from order to delivery.
- **`Late Delivery Flag`** = `IF [Order Delivered Customer Date] > [Order Estimated
  Delivery Date] THEN 1 ELSE 0 END` — 1 if the order arrived after its estimate.
- **`Is Delivered`** = `IF [Order Status] = "delivered" THEN 1 ELSE 0 END`.
- **`Order Completion Rate`** = `SUM([Is Delivered]) / COUNT([Order Id])`.
- **`Late Delivery Rate`** = `SUM([Late Delivery Flag]) / COUNT([Order Id])` (for delivered
  orders).

### 6.2 LOD expressions — the advanced technique

**LOD (Level of Detail) expressions** let a calculation run at a *different granularity*
than the visualization it sits in. The project uses **8 `FIXED` LOD calculations** to
compute **prior-month values** — `Previous Month Revenue`, `Previous Month Orders`,
`Previous Month Avg Review`, `Previous Month Delivery Time` — each pinned to a fixed level
so it can be compared against the current month regardless of how the view is filtered.

**Why LOD matters — the interview point.** A normal aggregate in Tableau is computed at the
granularity of the chart. But a **month-over-month comparison** needs *two* values at once
— this month *and* last month — at a fixed level. A `FIXED` LOD expression computes a value
at a granularity you specify, independent of the view, which is exactly what makes the
prior-month and **MoM % change** calculations possible. LOD expressions are the single most
"advanced Tableau" thing in the project.

### 6.3 The rest of the advanced toolkit

- **17 additional calculated fields** — the MoM % change percentages, display-text helpers
  with conditional **▲/▼ arrows**, trend indicators (Improving/Declining/Stable), and
  color-coding helpers for conditional formatting on KPI cards.
- **Parameters** — a **Date Range parameter** (5 preset time options driving global date
  filtering) and a **Selected Metric parameter** (4 options driving a dynamic "Key Insight"
  box). Parameters are user-facing controls that change what the dashboard shows.
- **Native forecasting** — Tableau's built-in forecasting engine produces a **3-month
  revenue forecast** with automatic seasonal adjustment and a **95% confidence interval**,
  plus a linear trend line.
- **Top N sets** and **dashboard actions** for interactive drill-down.

---

## 7. Dashboard 1 — Order Fulfillment Performance

**Business question:** How is the marketplace performing operationally — order volume,
delivery speed, late deliveries, order status?

**The visuals:** 4 KPI cards (Total Orders, Avg Delivery Time, Order Completion Rate, Late
Delivery Rate), a monthly order-volume line chart, an average-delivery-time trend, a
late-delivery-rate trend, a delivery-time distribution histogram, and an order-status
breakdown.

**Key findings:**
- **97% order completion rate** — reliable fulfillment.
- **Dramatic growth** — monthly order volume rose from ~400 (late 2016) to a peak of
  ~7,500 (early 2018).
- **Delivery speed improved enormously** — average delivery time fell from **50+ days** in
  early operations to **stabilizing around 12.5 days** by 2017–2018.
- **6.8% late-delivery rate** overall, with periodic spikes of 10–20%.
- **Early-operations stress** — Aug–Nov 2016 showed *100% late delivery* (the launch/
  scaling phase); operations stabilized to a ~10% baseline by early 2017.

**The teachable point.** This dashboard establishes the operational baseline — and surfaces
the project's central tension: operations are *strong overall* (97% completion, big speed
improvement) but the *6.8% late rate exceeds the 5% target*, and the long tail of 45+ day
deliveries is the thread the customer-experience analysis (Dashboard 3) later picks up.

---

## 8. Dashboard 2 — Revenue & Sales Performance

**Business question:** How is revenue growing, and where does it come from — by category,
payment method, and geography?

**The visuals:** KPI cards (Total Revenue, AOV, Items Sold, Growth Rate), a monthly revenue
trend, revenue by product category, revenue by payment method, and revenue by state.

**Key findings:**
- **21.01% YoY revenue growth** (2017 → 2018) — healthy expansion. Monthly revenue grew
  from near-zero (late 2016) to **exceeding $1.2M** by early 2018.
- **Diversified category mix** — top 10 categories are relatively balanced; **Health &
  Beauty leads but is only ~9% of revenue** (no single category dominates).
- **Credit card dominates payment** — **~80% of revenue** via credit card (Brazilian
  installment-payment culture); **~18% via boleto** (serving underbanked customers).
- **Heavy geographic concentration** — **São Paulo alone = 37% of total revenue**; the
  Southeast region (SP, RJ, MG) drives **60%+** of sales.
- **Healthy AOV of $159.33** — customers make meaningful, not trivial, purchases.

**The teachable point.** Revenue is growing well and is *category*-diversified — but it is
*geographically* concentrated. São Paulo at 37% is both Olist's strength and its biggest
strategic risk; the recommendation is geographic expansion into underserved northern and
central-western states.

---

## 9. Dashboard 3 — Customer Experience & Review Quality

**Business question:** How satisfied are customers, and what drives their review scores?

**The visuals:** KPI cards (Total Reviews, Avg Review Score, 5-Star Rate, 1-Star Rate), a
review-score distribution, a review-score trend, **review score by delivery status**, a
**review score vs. delivery-days** chart, and top/bottom-10 categories by review score plus
a category-performance scatterplot.

**Key findings:**
- **Average review score 4.086**, with a strong **58.25% 5-star rate** — high overall
  satisfaction.
- But a **meaningful 11.61% 1-star rate** — a sizable poor-experience segment.
- **Delivery speed drives satisfaction** — the project found a **strong negative
  correlation (−0.65)** between delivery time and review score: faster delivery → higher
  ratings; long delivery → lower ratings. On-time orders average significantly higher
  satisfaction than late ones.
- **Category gaps are real** — bottom categories trail the average by ~0.2–0.5 points.
- Sentiment **stabilized** around 4.0–4.3 after early-2016 volatility, though the recent
  trend is gently declining.

**The teachable point — the most actionable finding in the whole project.** This dashboard
is what *connects* Dashboard 1's delivery problem to a business consequence: the −0.65
delivery-time/review-score correlation means **late deliveries directly cost customer
satisfaction**, and with an 11.6% 1-star rate, fixing logistics is the single highest-
leverage lever. (Be ready to note it's a *correlation*, not proven causation — §14.)

---

## 10. Dashboard 4 — Marketplace Ecosystem (Products & Sellers)

**Business question:** How healthy is the marketplace itself — product mix, seller
distribution, concentration, and category-seller dynamics?

**The visuals** (three sections — products, sellers, integrated): product performance,
seller distribution and growth, a **seller quadrant** (revenue vs. review score), and a
**category-state heatmap** for white-space analysis.

**Key findings:**
- **Healthy, democratized marketplace structure** — **2,970 sellers**, and the **top 10
  sellers account for just 12.93% of revenue** (low concentration — competitive, not an
  oligopoly).
- **Quality and scale coexist** — the seller quadrant shows **most sellers maintain 4.0+
  review scores regardless of revenue level** — platform quality standards are working.
- **Category diversification** — the top 5 categories are **39.25% of revenue**; the other
  60%+ spreads across **66 other categories**.
- **E-commerce-optimized product mix** — the platform favors lightweight, affordable
  products (good shipping economics).
- **Single-item shopping behavior** — only **1.142 items per order** — customers buy
  targeted, not baskets → a cross-sell opportunity.
- Steady seller onboarding (100–200 new sellers/month), and clear **white-space
  opportunities** in underserved category-state combinations.

**The teachable point.** This dashboard checks the *structural health* of the marketplace —
and the verdict is positive (low concentration, broad seller base, quality maintained at
scale). The category-state heatmap turns that into an action: target seller recruitment at
specific empty category-state cells.

---

## 11. Dashboard 5 — Executive Summary

**Business question:** Can leadership see the whole marketplace's health on one screen and
drill down when needed?

This is the **synthesis dashboard** — and the most technically advanced. It consolidates
Dashboards 1–4 into a single monitoring surface:
- **KPI cards** with **MoM % change** indicators (powered by the 8 LOD expressions) —
  conditional **▲/▼ arrows** and Improving/Declining/Stable trend labels.
- A **revenue trend with Tableau's native 3-month forecast** (95% confidence band) and a
  linear trend line.
- **Geographic drill-downs** and a **revenue density map**.
- **Parameter-driven interactivity** — the Date Range parameter refilters everything; the
  Selected Metric parameter drives a dynamic "Key Insight" box.

**Key findings surfaced on this page:**
- **Delivery alert** — the 6.8% late rate exceeds the 5% target (tied to the −0.65 review
  correlation).
- **Orders/revenue divergence** — orders grew **+3.5% MoM** while revenue fell **−5.2%
  MoM** → **AOV compression** (customers ordering more but spending less per order).
- The 3-month **forecast predicts recovery** with an upward trend line — suggesting the
  −5.2% dip is **seasonal**, not a systemic downturn.
- Despite that, **declining review-score trend** needs proactive intervention.

**The teachable point.** Dashboard 5 demonstrates the *synthesis* skill — five separate
analyses distilled into one executive surface — and it's where the advanced Tableau
(LOD-driven MoM cards, parameters, forecasting) all comes together. It's designed for a
**weekly executive review cadence**, drilling into Dashboards 1–4 when a KPI breaches its
threshold.

---

## 12. Key Findings (Consolidated)

Memorize the headline numbers.

| Theme | Finding |
|---|---|
| Scale | 99,441 orders · **$15.8M revenue** · AOV **$159.33** · **21% YoY** growth |
| Operations | **97% completion rate**; delivery time improved **50+ days → 12.5 days** |
| The problem | **6.8% late-delivery rate** vs. a 5% target — structural, not seasonal |
| The link | **−0.65 correlation** between delivery time and review score |
| Satisfaction | Avg review **4.09**; **58.25% 5-star**, but **11.61% 1-star** |
| Geography | **São Paulo = 37%** of revenue; Southeast = 60%+ |
| Payments | ~80% credit card · ~18% boleto |
| Marketplace | **2,970 sellers**; top 10 = only **12.93%** of revenue (healthy, democratized) |
| Behavior | **1.142 items/order** — single-item shopping; cross-sell opportunity |
| Recent signal | Orders **+3.5% MoM** but revenue **−5.2% MoM** → AOV compression |

**The five-part story:** (1) Olist's **core operations are genuinely strong** and scaled
well; (2) but the **6.8% late-delivery rate** is the one clear operational failure; (3) and
it *matters* because late deliveries are strongly correlated with lower reviews; (4)
revenue is healthy but **geographically over-concentrated** in São Paulo; (5) the
marketplace structure is **healthy and competitive** (low seller concentration), with clear
white-space for expansion. **Logistics is the highest-leverage fix.**

---

## 13. Tableau Concepts to Know Cold

**Calculated field** — a new field you define with a formula (e.g., `Delivery Days`,
`Late Delivery Flag`); the metrics not present in the raw data.

**Relationships vs. joins** — a **join** physically merges tables at one fixed granularity
(and risks double-counting across grains); a **relationship** keeps tables separate and
lets Tableau pick the correct join and grain *per visualization*. This project uses
relationships for exactly that flexibility.

**Fact table / dimension** — the central transactional table (Orders) vs. the descriptive
tables linked to it (Customers, Products, Sellers).

**Granularity / grain** — the level of detail one row represents (order-level vs.
item-level); mismatched grain is what causes double-counting in joins.

**LOD (Level of Detail) expression** — a calculation that runs at a granularity *different*
from the view. **`FIXED`** computes at a level you specify, ignoring the view's filters;
used here for all the prior-month values. (`INCLUDE` and `EXCLUDE` are the other two LOD
keywords.)

**`DATEDIFF`** — a Tableau function returning the number of date units between two dates;
used for `Delivery Days`.

**Aggregate functions** — `SUM`, `COUNT`, `COUNTD` (count distinct), `AVG`.

**Parameter** — a user-facing control (dropdown, slider) that feeds a value into
calculations; here, the Date Range and Selected Metric parameters.

**Set (Top N set)** — a dynamic subset of dimension members (e.g., the top 10 categories).

**Forecasting** — Tableau's built-in projection of future values with seasonal adjustment
and confidence intervals; here a 3-month revenue forecast.

**Trend line** — a fitted line (e.g., linear) overlaid on data to show direction.

**Dashboard action** — interactivity that links sheets (filter, highlight, drill on click).

**KPI card** — a visual showing one headline number, often with a MoM indicator.

**MoM (Month over Month)** — comparing a metric to the prior month; the % change.

**Live connection vs. extract** — a *live* connection queries the source in real time; an
*extract* is a static snapshot. This project used a live connection for exploration.

**`.twbx`** — a packaged Tableau workbook bundling the workbook and its data into one
portable file.

**Tableau Public** — Tableau's free hosting platform for sharing interactive dashboards.

---

## 14. Limitations & Honest Caveats

Volunteer these — the project itself lists them.

1. **Truncated boundary periods.** August 2018 shows a sharp order-volume drop consistent
   with **incomplete data collection**, and Aug–Nov 2016 has too few orders for reliable
   trends. Insights from those boundary months are **directional, not definitive**.
2. **No logistics provenance data.** The dataset has no carrier identity, warehouse
   locations, or external context (holidays, promotions, weather) — so delivery-performance
   variation **can't be attributed to specific operational causes**.
3. **Geographic granularity ceiling.** Locations are city/state level only — no postal-code
   coordinates — so **delivery *distance* can't be measured**, even though it's a likely
   confound in delivery-time patterns.
4. **The review–delivery link is correlational.** The −0.65 relationship is strong, but the
   data can't isolate delivery experience from product quality or seller communication.
   **It's a strong correlation, not proven causation** — be precise about this.
5. **Single marketplace, single country, single era.** All findings are specific to Olist's
   Brazilian marketplace in 2016–2018 — the payment mix (boleto), logistics realities, and
   consumer behavior are particular to that market and time.
6. **The recent MoM dip is one data point.** The −5.2% revenue MoM is interpreted as
   seasonal (and the forecast supports recovery), but it's a single month near a
   data-truncated boundary.

---

## 15. Interview Q&A

Practice these out loud.

**Q1. Give me the overview of this project.**
"It's a five-dashboard Tableau analysis of the Olist Brazilian e-commerce marketplace —
about 99,000 orders from 2016 to 2018. The five dashboards cover order fulfillment, revenue
and sales, customer experience and reviews, the marketplace ecosystem of products and
sellers, and an executive summary that ties it all together. It's built on an eight-table
data model connected through Tableau relationships, with calculated fields, LOD
expressions, parameters, and native forecasting. The big theme is that Olist's operations
are strong but late deliveries are hurting customer satisfaction."

**Q2. Why did you use Tableau relationships instead of joins?**
"Because the eight tables sit at different granularities — orders are order-level, order
items are item-level, payments and reviews are their own grains. If I did traditional
joins, mixing those grains would double-count — joining order-level data to item-level data
multiplies the order rows. Tableau's relationship model keeps the tables separate and lets
Tableau choose the right join and the right granularity for each individual visualization
at query time. So a chart counting orders aggregates at order level, and a chart summing
item revenue aggregates at item level, from the same model, with no double-counting."

**Q3. What's an LOD expression and where did you use one?**
"An LOD — Level of Detail — expression lets a calculation run at a different granularity
than the chart it's in. A normal Tableau aggregate is computed at the view's level of
detail. But for a month-over-month KPI card, I need this month's value and last month's
value at the same time, at a fixed level. So I used FIXED LOD expressions — I built eight
of them, for previous-month revenue, orders, average review, and delivery time. FIXED
computes the value at a granularity I specify, independent of the view's filters, which is
what makes the MoM percentage-change calculations possible."

**Q4. What were your key calculated fields?**
"The core ones drove the delivery analysis. Delivery Days is a DATEDIFF between the purchase
timestamp and the delivered date. Late Delivery Flag is an IF — one if the actual delivery
date is later than the estimated delivery date, otherwise zero. Is Delivered checks the
order status. And then Order Completion Rate and Late Delivery Rate are ratios built on
those. None of those metrics exist in the raw data — they're all derived in Tableau."

**Q5. What's the single most important finding?**
"The link between delivery performance and customer satisfaction. The fulfillment dashboard
showed a 6.8% late-delivery rate, above the 5% target. The customer-experience dashboard
then showed a strong negative correlation, about −0.65, between delivery time and review
score — late orders get meaningfully lower ratings. With an 11.6% one-star rate, that makes
logistics the highest-leverage fix in the whole analysis: improving delivery directly
protects reviews, and reviews drive repeat purchases. I'd add that it's a strong
correlation, not proven causation — the data can't fully separate delivery from product
quality."

**Q6. You found revenue down 5% but orders up — what does that mean?**
"That's average order value compression — customers are placing more orders but spending
less per order. Orders grew about 3.5% month over month while revenue fell about 5.2%. It's
a warning sign worth investigating — it could be discounting, a product-mix shift, or
seasonality. My executive dashboard's three-month forecast actually predicted recovery with
an upward trend, which suggests the dip is seasonal rather than systemic — but I'd still
recommend looking into cross-selling and bundle strategies to stabilize AOV."

**Q7. How did you handle the geographic concentration finding?**
"São Paulo alone is 37% of revenue and the Southeast region is over 60%. That's both
Olist's strength and its biggest strategic risk — heavy dependence on one region. My
recommendation was geographic expansion: invest in marketing and seller recruitment in
underserved northern and central-western states, using the category-state heatmap from the
marketplace dashboard to find specific white-space — category-state combinations with no
seller presence."

**Q8. What does the executive summary dashboard add over the other four?**
"Synthesis. The other four dashboards each answer one question in depth. The executive
summary distills all of them into one monitoring surface — KPI cards with month-over-month
arrows powered by the LOD expressions, a revenue forecast, a geographic map, and parameter-
driven filters. It's designed for a weekly executive review: you scan the KPIs, and if one
breaches its threshold, you drill into the detailed dashboard behind it. It's also where
the advanced Tableau — the LOD-driven cards, the parameters, the native forecasting — all
comes together."

**Q9. What's boleto and why does it matter to this analysis?**
"Boleto is a Brazilian bank-slip payment method — about 18% of Olist's revenue. It matters
because it serves underbanked customers who don't have credit cards. The other 80% is
credit card, reflecting Brazil's installment-payment culture. It's a good example of why
market context matters — a US e-commerce analysis wouldn't have a boleto segment at all,
and recognizing it shapes the recommendation to expand payment accessibility to capture
more of the underbanked market."

**Q10. What are the limitations of this analysis?**
"A few I'd flag. The boundary periods are truncated — August 2018 has incomplete data and
late 2016 is too sparse for reliable trends. There's no logistics provenance — no carrier
identity, no warehouse locations — so I can't attribute delivery problems to specific
causes. Locations are only city and state level, so I can't measure delivery distance,
which is probably a confound. And the delivery-to-review relationship is correlational, not
causal — it's strong, but the data can't isolate delivery from product quality or seller
communication. All findings are also specific to one marketplace, one country, one era."

**Q11. How would you extend this project?**
"If I had carrier and warehouse data, I'd attribute the late deliveries to specific
logistics causes rather than just observing the rate. With postal-code coordinates I'd add
delivery distance as a variable, which is likely driving a lot of the delivery-time
variation. And I'd love to test the delivery-to-review link more rigorously — ideally
isolating delivery experience from product quality — to move from correlation toward causal
attribution before committing major logistics investment."

---

## 16. How to Walk Through This Project Live

If asked to screen-share the Tableau workbook:

1. **Open on the Executive Summary (Dashboard 5)** — lead with the synthesis: KPI cards,
   the forecast, the map, the parameters. Then say "let me show you the four analyses
   behind it."
2. **State the structure** — "five dashboards, four lenses — operations, revenue, customer
   experience, marketplace — plus the executive synthesis."
3. **Show the data model** — the 8 tables, and explain **why relationships, not joins**
   (the granularity / double-counting point). This is a strong technical talking point.
4. **Show the calculated fields** — `Delivery Days`, `Late Delivery Flag` — and the **LOD
   expressions** for the MoM cards. Spend time on LOD; it's the most advanced technique.
5. **Walk Dashboard 1 → 3 as a story** — Dashboard 1 finds the 6.8% late rate; Dashboard 3
   shows the −0.65 delivery/review correlation. That's the project's core narrative.
6. **Show Dashboard 4** — the healthy marketplace structure and the category-state heatmap.
7. **Return to Dashboard 5** — show the forecast and the parameter interactivity, and frame
   it as a weekly executive monitoring surface.
8. **Close on the recommendation** — logistics is the highest-leverage fix; and volunteer
   the correlational caveat.

**Pacing tip:** spend the most time on (a) the relationships-vs-joins decision, (b) the LOD
expressions, and (c) the Dashboard 1 → Dashboard 3 delivery-to-reviews story. Those are the
differentiated technical skill, the advanced Tableau, and the smartest analytical insight,
respectively.

---

## 17. Glossary

- **Olist** — a Brazilian e-commerce marketplace connecting small sellers to large
  platforms; the dataset's source.
- **`.twbx`** — a packaged Tableau workbook bundling the workbook and its data.
- **Tableau Public** — Tableau's free platform for publishing interactive dashboards.
- **Relationship (Tableau)** — a flexible link between tables that lets Tableau pick the
  join and grain per visualization (vs. a fixed join).
- **Join** — physically merging tables at one fixed granularity.
- **Granularity / grain** — the level of detail one row represents.
- **Fact table** — the central transactional table (Orders here).
- **Calculated field** — a user-defined field built with a formula.
- **`DATEDIFF`** — Tableau function for the number of units between two dates.
- **LOD (Level of Detail) expression** — a calculation at a granularity different from the
  view; `FIXED`, `INCLUDE`, `EXCLUDE`.
- **`FIXED` LOD** — computes a value at a specified level, independent of view filters.
- **`COUNTD`** — count distinct.
- **Parameter** — a user-facing control feeding a value into calculations.
- **Set / Top N set** — a dynamic subset of dimension members.
- **Forecasting (Tableau)** — built-in future-value projection with confidence intervals.
- **Trend line** — a fitted line showing data direction.
- **Dashboard action** — click-driven interactivity linking sheets.
- **KPI card** — a single-number visual, often with a MoM indicator.
- **MoM (Month over Month)** — comparison of a metric to the prior month.
- **AOV (Average Order Value)** — total revenue ÷ number of orders ($159.33 here).
- **Completion rate** — share of orders with status "delivered".
- **Late delivery rate** — share of orders delivered after their estimated date.
- **Review score** — the 1–5 star customer rating.
- **boleto** — a Brazilian bank-slip payment method serving underbanked customers.
- **Seller concentration** — the revenue share held by the top sellers (low = healthy).
- **White-space analysis** — finding unserved category-state combinations for expansion.
- **Live connection vs. extract** — real-time source query vs. a static data snapshot.

---

*This study guide documents the project as built. The authoritative references are the
Tableau workbook `tableau_olist_ops_cx_v1_raw_load.twbx`, the portfolio page `index.md`,
and the live Tableau Public dashboard. When this guide and the workbook disagree, the
workbook wins.*