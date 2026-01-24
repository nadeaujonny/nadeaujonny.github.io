---
layout: default
title: E-commerce Revenue & Returns Analysis (SQL)
---

# E-commerce Revenue & Returns Analysis (SQL)

This project analyzes sales and returns data from the BigQuery **thelook_ecommerce** dataset to uncover revenue drivers, product performance, return patterns, and operational insights.

---

## Objectives

- Identify key revenue and profit drivers
- Analyze return behavior by product and category
- Evaluate customer purchasing patterns
- Demonstrate advanced SQL techniques (CTEs, joins, window functions, aggregations)

---

## SQL Techniques Demonstrated

- Multi-table joins
- Aggregations and GROUP BY
- Common Table Expressions (CTEs)
- Window functions (RANK, ROW_NUMBER)
- CASE statements
- Date/time analysis
- Subqueries
- Filtering and segmentation

---

## Dataset

Source: BigQuery Public Dataset – `thelook_ecommerce`

Tables used:
- orders
- order_items
- products
- users

---

## Key Metrics (KPIs)

- Total Revenue
- Total Profit
- Units Sold
- Return Rate
- Average Order Value (AOV)
- Customer Lifetime Value (CLV)
- Monthly Revenue Growth

---

## Key Business Questions

- Which products and categories generate the most revenue and profit?
- Which products are returned most frequently?
- How do returns affect overall profitability?
- Which customers generate the highest lifetime value?
- How does revenue trend over time?

---

## Tools Used

- Google BigQuery (SQL)
- GitHub Pages (documentation)
- GitHub (version control)

---

## Analysis 1 - Top Products by Revenue

### Business Question
- Which Products generate the highest revenue?
  - How much profit do they generate?
  - How many units of them are sold?

### SQL Query
```sql
SELECT 
  p.name AS product_name,
  p.category AS product_category,
  ROUND(SUM(oi.sale_price), 2) AS total_revenue,
  ROUND(SUM(oi.sale_price - p.cost), 2) AS total_profit,
  COUNT(*) AS units_sold
FROM `bigquery-public-data.thelook_ecommerce.products` p
JOIN `bigquery-public-data.thelook_ecommerce.order_items` oi
  ON p.id = oi.product_id
JOIN `bigquery-public-data.thelook_ecommerce.orders` o
  ON o.order_id = oi.order_id
WHERE o.status = 'Complete'
GROUP BY product_name, product_category
ORDER BY total_revenue DESC
LIMIT 10;
```

### Result Table
![Top products by revenue](images/top_products_by_revenue.png)

### Insights
- The highest-revenue products are dominated by premium outerwear brands (North Face, Canada Goose).
- Outerwear & Coats appears multiple times in the top 10, indicating category concentration.
- Top products generate both high revenue and strong profit margins, suggesting pricing power.
- Unit sales are relatively balanced among top products, implying revenue is driven more by price than volume.

### Business Recommendations
- Prioritize inventory and marketing spend on top-performing outerwear products.
- Bundle or cross-sell accessories with premium jackets to increase AOV.
- Analyze return rates for these top products to ensure high revenue is not offset by returns.
- Negotiate supplier costs for high-volume premium brands to improve margins further.
