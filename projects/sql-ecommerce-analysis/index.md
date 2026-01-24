---
layout: default
title: E-commerce Revenue & Returns Analysis (SQL)
---

<a href="/projects" class="back-btn">← Back to Projects</a>

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
- Which products generate the highest revenue?

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
![Top 10 Products by Revenue](images/top_products_by_revenue.png)

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

---

## Analysis 2 - Top Products by Profit

### Business Question
- Which products generate the highest profit?

### SQL Query
```sql
WITH product_profit AS (
  SELECT
    p.id AS product_id,
    p.name AS product_name,
    ROUND(SUM(oi.sale_price), 2) AS revenue,
    ROUND(SUM(oi.sale_price - p.cost), 2) AS profit,
    COUNT(*) AS units_sold
  FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` o
    ON oi.order_id = o.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` p
    ON oi.product_id = p.id
  WHERE o.status = 'Complete'
  GROUP BY p.id, p.name
)

SELECT *
FROM product_profit
ORDER BY profit DESC
LIMIT 10;
```

### Result Table
![Top 10 Products by Profit](images/top-products-by-profit.png)

### Insights
- Profit is highly concentrated among a small number of products, indicating that a limited subset of the catalog drives a disproportionate share of total profit.
- Most top-profit products are premium outerwear and apparel items (jackets, hoodies, ski pants), suggesting higher margins compared to lower-priced categories.
- Several products achieve high profit despite relatively low unit sales, indicating that per-unit margin is a more important driver of profitability than sales volume for these items.
- Well-known premium brands (e.g., Nike/Jordan, The North Face, Canada Goose) appear frequently in the top results, highlighting the impact of brand positioning and pricing power.
- Revenue and profit rankings are similar but not identical, reinforcing that revenue alone does not fully capture business performance.

### Business Recommendations
- Prioritize inventory availability for these high-profit products to avoid stockouts, especially during peak seasonal demand.
- Increase marketing visibility for these items through homepage placement, targeted email campaigns, and paid advertising to maximize profit contribution.
- Test modest price increases on top-profit products to evaluate demand sensitivity while potentially improving margins further.
- Create product bundles or cross-sell complementary items (e.g., accessories or base layers) to increase average order value without relying on heavy discounting.
- Closely monitor return rates for these products to ensure high profitability is not offset by reverse-logistics and refund costs.

---

## Analysis 3 - Top Brands by Profit

### Business Question
- Which brands generate the highest profit?

### SQL Query
```sql
WITH brand_metrics AS (
  SELECT
    p.brand,
    ROUND(SUM(oi.sale_price), 2) AS revenue,
    ROUND(SUM(oi.sale_price - p.cost), 2) AS profit,
    COUNT(*) AS units_sold
  FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` o
    ON oi.order_id = o.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` p
    ON oi.product_id = p.id
  WHERE o.status = 'Complete'
  GROUP BY p.brand
),

ranked_brands AS (
  SELECT *,
         RANK() OVER (ORDER BY profit DESC) AS profit_rank,
         RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
  FROM brand_metrics
)

SELECT *
FROM ranked_brands
ORDER BY profit_rank
LIMIT 10;
```

### Result Table
![Top 10 Brands by Profit](images/top-brands-by-profit.png)

### Insights
- Profit is highly concentrated among a small subset of brands, indicating that overall profitability depends heavily on a limited number of key partners.
- While high-profit brands also tend to generate strong revenue, the rankings differ, showing that margin structure varies significantly between brands.
- Some brands achieve high profitability with relatively fewer units sold, suggesting premium pricing power or more efficient cost structures.
- Brand-level performance is more stable and predictable than individual product performance, making it a stronger signal for long-term strategic planning.
- The presence of premium brands among the top performers highlights the importance of brand positioning in driving sustainable profit.

### Business Recommendations
- Strengthen relationships with top-performing brands through exclusive product lines, co-marketing campaigns, or preferred supplier agreements.
- Allocate a larger share of marketing budget to high-profit brands to maximize return on advertising spend.
- Expand the product assortment from the most profitable brands to capitalize on demonstrated customer demand.
- Review pricing and cost structures for lower-performing brands to identify opportunities for margin improvement or renegotiation.
- Reduce dependency risk by identifying and developing emerging mid-tier brands that show strong growth potential in profit or revenue.

---

## Analysis 4 - Top Products by Profit Margin

### Business Question
- Which products generate the highest profit margins? (profit margin being defined as profit/revenue)

### SQL Query
```sql
WITH product_totals AS (
  SELECT
    p.id AS product_id,
    p.name AS product_name,
    p.category AS product_category,
    SUM(oi.sale_price) AS revenue,
    SUM(oi.sale_price - p.cost) AS profit,
    COUNT(*) AS units_sold
  FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
    ON oi.order_id = o.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
    ON oi.product_id = p.id
  WHERE o.status = 'Complete'
  GROUP BY 1, 2, 3
),

metrics AS (
  SELECT
    product_id,
    product_name,
    product_category,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,
    units_sold,

    ROUND(profit / NULLIF(revenue, 0), 4) AS profit_margin,

    RANK() OVER (ORDER BY profit DESC) AS profit_rank,
    RANK() OVER (ORDER BY profit / NULLIF(revenue, 0) DESC) AS margin_rank,

    CASE
      WHEN revenue = 0 THEN 'Undefined'
      WHEN profit / revenue >= 0.50 THEN 'Very High (>= 50%)'
      WHEN profit / revenue >= 0.30 THEN 'High (30%–49.9%)'
      WHEN profit / revenue >= 0.15 THEN 'Medium (15%–29.9%)'
      WHEN profit / revenue > 0 THEN 'Low (0%–14.9%)'
      ELSE 'Negative (<= 0%)'
    END AS margin_tier
  FROM product_totals
)

SELECT *
FROM metrics
WHERE revenue > 0
  AND units_sold >= 3     
  AND revenue >= 50   --takes extremely low volume products out of the picture    
ORDER BY profit_margin DESC, profit DESC
LIMIT 10;
```

### Result Table
![Top 10 Products by Profit Margin](images/top-products-by-profit-margin.png)

### Insights
- The top profit-margin products are high-margin apparel items, with margins clustered around 65–67%, indicating strong pricing power relative to cost.
- All top-margin products fall within the “Blazers & Jackets” category, suggesting that this category benefits from either premium pricing, efficient sourcing, or both.
- These products generate moderate revenue but relatively small sales volumes (3–5 units each), which explains why they did not appear in the top products by total profit or revenue analyses.
- The large gap between profit margin rankings and profit rankings highlights that high margin does not necessarily translate to high total profit without sufficient sales volume.
- Applying minimum thresholds for units sold and revenue helps eliminate misleading results driven by extremely small denominators, producing a more business-relevant view of product efficiency.

### Business Recommendations
- Prioritize marketing tests for high-margin products. Increase visibility of these products through targeted promotions, homepage placement, or paid ads to determine whether demand can be scaled while maintaining strong margins.
- Evaluate supply chain scalability for high-margin categories. Investigate whether the cost structure that enables these margins (supplier contracts, materials, manufacturing) can be maintained at higher volumes.
- Use profit margin to guide discount strategy. High-margin products can tolerate deeper discounts while remaining profitable, making them ideal candidates for seasonal promotions or customer acquisition campaigns.
- Reassess low-margin, high-volume products. Products with strong sales but weak margins should be reviewed for potential price optimization, cost reduction, or bundling strategies.
- Incorporate margin metrics into assortment planning. Future product selection and inventory decisions should consider profit margin alongside revenue and volume to optimize long-term profitability.
