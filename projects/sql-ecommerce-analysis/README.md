# E-commerce Business Optimization Analysis (BigQuery SQL)

Multi-dimensional SQL analysis of the BigQuery `thelook_ecommerce` dataset (~181K order items, ~80K customers, ~29K products) examining revenue, profitability, return risk, and operational efficiency across 10 analytical dimensions.

## Analysis Dimensions

- Top & Bottom Products (by revenue, profit, margin, returns, lost revenue)
- Top & Bottom Brands
- Top & Bottom Categories
- Long-Term Trends (revenue, units, margin, return rate)
- Seasonal Trends
- Customers (revenue, orders, lifetime, returns, cancellations, demographics, geography)
- Distribution Centers (performance, inventory balance)

## SQL Techniques

- Multi-layered CTEs (first_layer → second_layer → third_layer)
- Window functions (RANK, SUM OVER, revenue/profit share calculations)
- Conditional aggregation (CASE WHEN for status-specific metrics)
- Multi-table JOINs (order_items → orders → products → users → distribution_centers)
- NULLIF for safe division, DATE_TRUNC/EXTRACT for time-series aggregation

## Key Findings

- Outerwear & Coats generates #1 revenue ($339K) with only #10 unit volume — highest revenue per unit
- Blazers & Jackets has the highest profit margin (62.1%) but ranks #15 in revenue
- Return rates cluster tightly at 27–31% across all 26 categories — systemic, not category-specific
- Lost revenue approaches or exceeds earned revenue for most top products and brands
- 80.7% of customers ordered only 1–4 items total — massive retention opportunity
- Distribution centers are understocked 10:1 vs. overstocked across all facilities

## Tools

- Google BigQuery (Standard SQL)
- Dataset: `bigquery-public-data.thelook_ecommerce`

## Live Project Page

[nadeaujonny.github.io/projects/sql-ecommerce-analysis](https://nadeaujonny.github.io/projects/sql-ecommerce-analysis/)
