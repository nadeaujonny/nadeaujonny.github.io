# SQL E-commerce Revenue & Profit Analysis

This project analyzes sales, profitability, and return behavior for a fictional e-commerce company using the public **BigQuery `thelook_ecommerce` dataset**.

The goal is to demonstrate practical, business-focused SQL analysis using real-world data modeling patterns and advanced querying techniques.

---

## Project Objectives

- Identify top-performing products and brands by revenue and profit
- Analyze how returns impact overall profitability
- Explore sales trends across time and geography
- Demonstrate advanced SQL skills (CTEs, window functions, joins, aggregations)

---

## Dataset

Source:  
`bigquery-public-data.thelook_ecommerce`

Key tables used:

- `orders`
- `order_items`
- `products`
- `users`

Only **completed orders** are included in revenue and profit calculations to avoid inflating sales metrics.

---

## Key Metrics

- Revenue
- Profit
- Units Sold
- Return Rate
- Average Order Value (AOV)
- Customer Lifetime Value (CLV)

---

## SQL Techniques Demonstrated

- Common Table Expressions (CTEs)
- Multi-table joins
- Window functions (RANK, LAG, etc.)
- Conditional aggregation (CASE)
- Time-based analysis
- Business metric engineering

---

## Repository Structure

```text
sql-ecommerce-analysis/
├── index.md        # Project page for GitHub Pages site
├── queries.sql     # All SQL queries used in the analysis
├── images/         # Screenshots of query results from BigQuery
└── README.md       # This file
