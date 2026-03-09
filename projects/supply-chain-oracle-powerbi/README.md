# Supply Chain Demand Forecasting, Inventory Optimization & MRP Simulation Dashboard

End-to-end automated supply chain analytics solution using Oracle SQL, Excel Power Query, and Power BI.

**Author:** Jonathan Nadeau
**Portfolio:** [nadeaujonny.github.io](https://nadeaujonny.github.io)
**Full Project Writeup:** [Portfolio Project Page](https://nadeaujonny.github.io/projects/supply-chain-oracle-powerbi/)

---

## Project Overview

This project builds a complete, automated supply chain analytics pipeline — from Oracle database extraction through MRP simulation, demand forecasting, and inventory optimization to a six-page interactive Power BI dashboard — using the DataCo Smart Supply Chain dataset (~180,000 orders).

### What Makes This Different

Every stage is designed as a **repeatable, refreshable system** rather than a one-time analysis:

- **Oracle stored procedures** automate data extraction, MRP net requirements calculation, and forecast write-back
- **Power Query custom M functions** automate transformation logic across hundreds of SKUs
- **Power BI scheduled refresh** pushes updated dashboards to stakeholders without manual intervention
- The result is a **closed-loop system** where reporting findings feed back into master data updates and the next refresh cycle reflects those changes

---

## Technical Stack

| Layer | Tools & Approach |
|---|---|
| **Database / ERP** | Oracle Autonomous Database; SQL extraction, joins, aggregation, views; stored procedures; DBMS_SCHEDULER |
| **MRP Simulation** | Oracle SQL tables/views for gross-to-net netting, lot sizing, lead time offsets, planned order releases |
| **ETL** | Excel Power Query — custom M functions, parameters, query folding |
| **Analysis** | Excel — Power Pivot, Solver, Goal Seek, What-If Analysis, dynamic arrays |
| **Forecasting** | Excel Forecast Sheet (ETS), moving averages, forecast write-back to Oracle |
| **Dashboards** | Power BI — six-page report, DAX measures, data alerts, Row-Level Security, scheduled refresh |

---

## Dataset

**DataCo Smart Supply Chain Dataset** (Kaggle) — ~180,000 order records covering the full order-to-delivery lifecycle with product categories, customer segments, shipping modes, delivery performance, and financial metrics.

Loaded into Oracle Autonomous Database with a normalized schema:
`ORDERS` · `ORDER_ITEMS` · `PRODUCTS` · `CUSTOMERS` · `SHIPMENTS` · `FORECAST_PLAN` · `MRP_REQUIREMENTS` · `INVENTORY_SNAPSHOT`

---

## Automation Pipeline

```
Oracle DBMS_SCHEDULER (2:00 AM)
  → REFRESH_SUPPLY_CHAIN_DATA stored procedure
    → Staging refresh → Derived fields → MRP calculation → View rebuild
      → Power BI scheduled refresh (5:00 AM)
        → Power Query custom functions execute
          → DAX measures recalculate
            → Data alerts evaluate thresholds
              → Dashboard ready by morning
```

---

## Repository Structure

```
supply-chain-analytics/
├── README.md
├── sql/
│   ├── 01_schema_ddl.sql              # Table creation, PKs, FKs, indexes
│   ├── 02_data_loading.sql            # Data import scripts
│   ├── 03_demand_queries.sql          # Demand & sales extraction
│   ├── 04_inventory_queries.sql       # ABC classification, product analytics
│   ├── 05_fulfillment_queries.sql     # Planned vs actual, delivery performance
│   ├── 06_mrp_queries.sql             # MRP net requirements logic
│   ├── 07_forecast_queries.sql        # Forecast accuracy, bias detection
│   ├── 08_views.sql                   # All 6 reporting views
│   ├── 09_stored_procedure.sql        # REFRESH_SUPPLY_CHAIN_DATA
│   └── 10_scheduler_job.sql           # DBMS_SCHEDULER configuration
├── images/
│   └── (dashboard screenshots, ERD, analysis visuals)
└── docs/
    └── (methodology notes, query folding documentation)
```

---

## Dashboard Pages

| Page | Focus | Key Visuals |
|---|---|---|
| **1. Executive KPI Overview** | At-a-glance supply chain health | KPI cards, order volume trend, delivery breakdown, revenue by category |
| **2. Demand Analysis & Forecasting** | Historical demand + forecasts | Time series, seasonality overlays, forecast accuracy (MAE, MAPE), method comparison |
| **3. Inventory Optimization** | ABC/XYZ classification + stocking parameters | Classification matrix, inventory health table, EOQ sensitivity, stockout indicators |
| **4. Fulfillment & Logistics** | Delivery performance + bottlenecks | Planned vs actual, lead time variance, shipping mode analysis, regional map |
| **5. Supply Plan & MRP** | MRP output + supply plan | Time-phased plan, planned order Gantt, net requirements waterfall, exception log |
| **6. Insights & Actions** | Closed-loop recommendations | Key findings, master data update suggestions, methodology notes |

---

## Key Analyses

- **Demand Forecasting:** ETS, moving average, and weighted moving average with per-category method selection and accuracy evaluation
- **ABC/XYZ Classification:** Revenue-based ABC × demand-variability XYZ matrix with inventory policy recommendations per cell
- **Inventory Optimization:** EOQ, safety stock, reorder point calculations with Solver-optimized lot sizing
- **MRP Simulation:** Gross-to-net netting, lot sizing rules, lead time offsets, exception flagging (expedite, reschedule, split)
- **Planned vs. Actual:** Lead time variance, on-time delivery rate, forecast bias detection
- **Forecast Write-Back:** Demand planning round-trip — Excel forecasts written back to Oracle FORECAST_PLAN to feed MRP

---

## Skills Demonstrated

- SQL querying against Oracle (CTEs, window functions, stored procedures, scheduled jobs)
- MRP net requirements logic and supply planning concepts
- Demand forecasting and forecast accuracy measurement
- ABC/XYZ inventory classification and policy determination
- Excel Power Query ETL with custom M functions and parameters
- Power BI dashboard design with DAX, star schema, and Row-Level Security
- End-to-end automation architecture design
- Data modeling and relational schema design

---

## Status

🚧 **In Progress** — Building Phase 1 (Oracle schema design and data loading)

---

## Contact

**Jonathan Nadeau**
- Portfolio: [nadeaujonny.github.io](https://nadeaujonny.github.io)
- LinkedIn: [linkedin.com/in/nadeau-jonathan](https://linkedin.com/in/nadeau-jonathan)
- GitHub: [github.com/nadeaujonny](https://github.com/nadeaujonny)
- Email: nadeau.jonny@gmail.com
