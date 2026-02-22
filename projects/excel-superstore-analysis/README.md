# Sales Dashboard – Superstore Dataset (Excel)

> An end-to-end Excel analytics project demonstrating Power Query data cleaning, KPI development, pivot-table analysis, and executive dashboard design using the Superstore retail dataset.

**Tools:** Excel · Power Query · Pivot Tables · Pivot Charts · Slicers · XLOOKUP · SUMIFS/COUNTIFS

🔗 **[View Full Project Page](https://nadeaujonny.github.io/projects/excel-superstore-analysis/)**

---

## Dashboard Preview

![Excel Superstore Profit-Oriented Dashboard](projects/excel-superstore-analysis/images/excel-project-profit-oriented-dashboard.png)

*Final profit-oriented dashboard with fully connected slicers. Best viewed in Microsoft Excel (desktop) for full interactivity.*

---

## Project Overview

This project analyzes Superstore retail sales data in Microsoft Excel to uncover trends in revenue, profit, customer segments, regional performance, and return impact. The goal is to demonstrate practical Excel analytics skills used in business environments: Power Query (ETL), pivot-driven analysis, KPI modeling, and dashboard design.

### Business Context

This analysis simulates a retail company evaluating sales performance, profitability, customer behavior, and operational efficiency to support data-driven decision making by executives and category managers.

### Dataset

- **Source:** Superstore (public retail sample dataset)
- **Records:** 9,994 orders
- **Time Range:** 2014–2017
- **Granularity:** One row per order line item
- **Core Tables:** Orders, Returns
- **Total Sales:** $2.3M | **Total Profit:** $286K

---

## Objectives

- Define and calculate core KPIs: revenue, profit, profit margin, units sold, and return rate
- Clean and standardize raw orders using Power Query (data types, text cleanup, de-duplication, derived date fields)
- Analyze performance using pivot tables and calculated fields (time trends, product mix, regional efficiency, segments, returns)
- Build an executive-style dashboard with connected slicers for interactive exploration

---

## Tools & Skills Demonstrated

| Skill Area | Details |
|---|---|
| **Power Query** | ETL, data type enforcement, text cleanup, de-duplication, derived date fields |
| **Pivot Tables** | Grouping, sorting, filters, calculated fields |
| **KPI Modeling** | Profit margin, return rate, performance comparisons |
| **Excel Functions** | XLOOKUP, SUMIFS/COUNTIFS, IF/IFERROR, date & text functions |
| **Visualization** | Pivot charts, conditional formatting, slicers, dashboard layout |

---

## KPI Definitions

| KPI | Formula |
|---|---|
| Revenue | SUM(Sales) |
| Profit | SUM(Profit) |
| Profit Margin | Profit / Revenue |
| Units Sold | SUM(Quantity) |
| Return Rate | Returned Sales / Total Sales (sales-based) |

---

## Data Preparation (Power Query / ETL)

Before building KPIs, pivot tables, and charts, I cleaned and standardized the Superstore Orders dataset using Excel Power Query. The goal was to create a reliable, refreshable table (`Clean_Orders`) that serves as the single source of truth for all downstream analysis and dashboarding.

- **Input:** Raw Orders data (`.xls`) preserved as `Raw_Orders` (no manual edits)
- **Tool:** Excel Power Query (Get & Transform)
- **Output:** Cleaned dataset loaded to `Clean_Orders` (used by all pivots, charts, and KPIs)
- **Refreshable:** Can update via *Data → Refresh All* without redoing manual steps

![Power Query Applied Steps](projects/excel-superstore-analysis/images/excel-data-prep-power-query.png)

---

## Analyses

### Analysis 1 — Revenue & Profit Trends

**Business Question:** Are there trends, seasonality, or periods of volatility that could inform forecasting, inventory planning, and cost control?

**Key Insights:**
- Revenue grows consistently from 2014–2017 with predictable seasonal peaks
- Profit is volatile — significant month-to-month swings including several negative-profit periods
- Revenue increases don't always translate to proportional profit gains, suggesting cost or discount issues
- Recurring high-demand periods offer opportunities for better inventory and capacity planning

---

### Analysis 2 — Product & Category Performance

**Business Question:** Which categories and products contribute the most to revenue and profit? Where do profitability differences suggest pricing, discounting, inventory, or product strategy changes?

**Key Insights:**
- Technology and Office Supplies drive 93.6% of profit despite being only 67.7% of revenue
- Furniture generates 32.3% of revenue but only 6.4% of profit, with a 2.5% margin — 7x lower than top categories
- Profit is concentrated in few products — top 10 products contribute a disproportionate share
- The 7x margin difference between categories means uniform pricing and discount policies don't work

| Category | Revenue | Profit | Profit Margin |
|---|---|---|---|
| Technology | $835,760 | $145,386 | 17.4% |
| Office Supplies | $718,318 | $122,247 | 17.0% |
| Furniture | $741,400 | $18,381 | 2.5% |

---

### Analysis 3 — Regional Performance & Market Efficiency

**Business Question:** Which regions are driving the most profit and where are we seeing efficiency gaps? Which states and cities are the largest profit contributors — and which are consistently unprofitable?

**Key Insights:**
- California and New York alone generate ~52% of total profit, creating geographic risk
- West and East regions show higher efficiency than South and Central
- Bottom 10 states collectively represent $98K+ in losses, with Texas (-$25,729), Ohio (-$16,959), and Pennsylvania (-$15,560) as the biggest drags
- Top cities (NYC, LA, Seattle) demonstrate that dense markets support premium pricing and efficient delivery

---

### Analysis 4 — Customer Segment Analysis

**Business Question:** Which customer segments drive the most revenue and profit, and which segments are the most efficient?

**Key Insights:**
- Consumer dominates volume (50.6% of revenue) but has the lowest margin at 11.5%
- Home Office is most efficient at 14.0% margin, 220 basis points above average, despite being only 18.7% of revenue
- Corporate balances scale and efficiency — strong 13.0% margin with $705,602 revenue
- The 250 basis point margin spread means uniform discounting over-discounts high-margin segments

---

### Analysis 5 — Returns Analysis & Revenue Impact

**Business Question:** How much revenue and profit are impacted by returns? Which sub-categories have the highest return rates?

**Key Insights:**
- Returns erase one month of profit: $180,504 in returned sales (7.86%) and $23,232 in lost profit (8.12%)
- Return rates vary by category: Copiers (12.84%), Furnishings (10.48%), Appliances (9.42%) vs Binders (4.91%) — a 2.6x spread
- Returns hit high-margin products harder: returns destroy more profit (8.12%) than revenue (7.86%)
- Impact is concentrated: top 10 products drive disproportionate return impact, enabling targeted fixes

---

## Dashboard Features

- **Profit-oriented, single-screen layout** designed for clean portfolio screenshots
- **Connected slicers** for *Order Year* and *Order Month* that filter every chart simultaneously
- **Core visuals:** Monthly Profit Trend, Return Profit Impact, Top Profit Sub-Categories, Top Profit States, Segment Profit

---

## Workbook Structure

```
Superstore_Portfolio_Excel_Project.xlsx
├── Raw_Orders    — Original imported dataset (preserved; no manual edits)
├── Clean_Orders  — Power Query cleaned, analysis-ready table (single source of truth)
├── Returns       — Returned orders reference table
├── People        — Region/manager reference table
├── Pivots        — Pivot tables + pivot charts used for analysis and the dashboard
└── Dashboard     — Final profit-oriented, single-screen interactive dashboard
```

---

## Project Structure

```
excel-superstore-analysis/
├── index.md                                        # Project page (GitHub Pages)
├── README.md                                       # This file
├── data/
│   └── superstore_raw.xls                          # Raw dataset
├── workbook/
│   └── Superstore_Portfolio_Excel_Project.xlsx      # Final Excel workbook
└── images/                                         # Analysis charts & dashboard screenshots
    ├── excel-project-profit-oriented-dashboard.png
    ├── excel-data-prep-power-query.png
    ├── excel-analysis-1-kpi-summary.png
    ├── excel-analysis-1-monthly-sales.png
    ├── excel-analysis-1-monthly-profit.png
    ├── excel-analysis-2-*.png
    ├── excel-analysis-3-*.png
    ├── excel-analysis-4-*.png
    └── excel-analysis-5-*.png
```

---

## Downloads

- **Excel Workbook:** [`Superstore_Portfolio_Excel_Project.xlsx`](workbook/Superstore_Portfolio_Excel_Project.xlsx) — *Best viewed in Microsoft Excel (desktop) to use slicers and full interactivity.*
- **Raw Dataset:** [`superstore_raw.xls`](data/superstore_raw.xls)

---

## Conclusion

This project demonstrates an end-to-end Excel analytics workflow: importing raw retail data, transforming it with Power Query, building pivot-driven analysis, and delivering a polished, interactive dashboard optimized for stakeholder reporting. The final dashboard supports fast profit-based exploration by time and surfaces key profitability drivers (category mix, region performance, segment efficiency) along with the revenue/profit impact of returns.

---

## Author

**Jonathan Nadeau**

- 🌐 [Portfolio Website](https://nadeaujonny.github.io/)
- 💼 [LinkedIn](https://www.linkedin.com/in/nadeau-jonathan)
- 📧 [nadeau.jonny@gmail.com](mailto:nadeau.jonny@gmail.com)
