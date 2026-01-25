---
layout: default
title: E-commerce Revenue & Returns Analysis (SQL)
---

<a href="/projects" class="back-btn">← Back to Projects</a>

# E-commerce Revenue & Returns Analysis (SQL)

> This project analyzes sales and returns data from the BigQuery **thelook_ecommerce** dataset to uncover revenue drivers, product performance, return patterns, and operational insights.

---

<details>
  <summary><strong>Project Overview</strong></summary>

  <h2>Objectives</h2>
  <ul>
    <li>Identify key revenue and profit drivers</li>
    <li>Analyze return behavior by product and category</li>
    <li>Evaluate customer purchasing patterns</li>
    <li>Demonstrate advanced SQL techniques (CTEs, joins, window functions, aggregations)</li>
  </ul>

  <hr>

  <h2>SQL Techniques Demonstrated</h2>
  <ul>
    <li>Multi-table joins</li>
    <li>Aggregations and GROUP BY</li>
    <li>Common Table Expressions (CTEs)</li>
    <li>Window functions (RANK, ROW_NUMBER)</li>
    <li>CASE statements</li>
    <li>Date/time analysis</li>
    <li>Subqueries</li>
    <li>Filtering and segmentation</li>
  </ul>

  <hr>

  <h2>Dataset Overview</h2>
  <p>
    The <code>thelook_ecommerce</code> dataset is a public BigQuery dataset that simulates the operations of an online retail company.
    It contains detailed transactional data covering customer orders, individual items within each order, product attributes, and user information.
  </p>

  <p>The data is structured in a relational format:</p>
  <ul>
    <li><code>orders</code> contains one row per order and includes timestamps, order status (e.g., Complete, Returned), and user identifiers.</li>
    <li><code>order_items</code> contains one row per product purchased within an order, allowing revenue, profit, and return behavior to be analyzed at the product level.</li>
    <li><code>products</code> provides product metadata such as category, brand, and cost, enabling profitability and margin calculations.</li>
    <li><code>users</code> contains customer-level demographic and geographic attributes.</li>
  </ul>

  <p>
    This structure supports analysis across multiple business dimensions including product performance, brand contribution,
    customer behavior, operational efficiency (returns), and time-based trends. The dataset is well-suited for demonstrating SQL techniques
    such as joins, aggregations, window functions, and time-series analysis in an e-commerce context.
  </p>

  <hr>

  <h2>Key Metrics (KPIs)</h2>
  <p>The following key performance indicators (KPIs) are used throughout this analysis:</p>
  <ul>
    <li><strong>Total Revenue</strong> – The total dollar value of completed sales.</li>
    <li><strong>Total Profit</strong> – Revenue minus product cost for completed orders.</li>
    <li><strong>Units Sold (Completed Purchases)</strong> – The number of items successfully purchased and not returned.</li>
    <li><strong>Units Returned</strong> – The number of items returned by customers.</li>
    <li><strong>Return Rate (%)</strong> – Returned units ÷ (completed units + returned units).</li>
    <li><strong>Profit Margin (%)</strong> – Profit ÷ revenue.</li>
  </ul>

  <p>
    These metrics collectively provide visibility into sales growth, profitability, product efficiency,
    and operational risk associated with customer returns.
  </p>

  <hr>

  <h2>Key Business Questions</h2>
  <ul>
    <li>Which products and categories generate the most revenue and profit?</li>
    <li>Which products are returned most frequently?</li>
    <li>How do returns affect overall profitability?</li>
    <li>Which customers generate the highest lifetime value?</li>
    <li>How does revenue trend over time?</li>
  </ul>

  <hr>

  <h2>Tools Used</h2>
  <ul>
    <li>Google BigQuery (SQL)</li>
    <li>GitHub Pages (documentation)</li>
    <li>GitHub (version control)</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 1 – Top Products by Revenue</strong></summary>

  <h3>Business Question</h3>
  <ul>
    <li>Which products generate the highest revenue?</li>
  </ul>

  <h3>SQL Query</h3>

  <pre><code class="language-sql">SELECT 
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
</code></pre>

  <h3>Result Table</h3>
  <img src="images/top_products_by_revenue.png" alt="Top 10 Products by Revenue" style="max-width:100%; height:auto;">

  <h3>Insights</h3>
  <ul>
    <li>The highest-revenue products are dominated by premium outerwear brands (North Face, Canada Goose).</li>
    <li>Outerwear &amp; Coats appears multiple times in the top 10, indicating category concentration.</li>
    <li>Top products generate both high revenue and strong profit margins, suggesting pricing power.</li>
    <li>Unit sales are relatively balanced among top products, implying revenue is driven more by price than volume.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>Prioritize inventory and marketing spend on top-performing outerwear products.</li>
    <li>Bundle or cross-sell accessories with premium jackets to increase AOV.</li>
    <li>Analyze return rates for these top products to ensure high revenue is not offset by returns.</li>
    <li>Negotiate supplier costs for high-volume premium brands to improve margins further.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 2 – Top Products by Profit</strong></summary>

  <h3>Business Question</h3>
  <ul>
    <li>Which products generate the highest profit?</li>
  </ul>

  <h3>SQL Query</h3>

  <pre><code class="language-sql">WITH product_profit AS (
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
</code></pre>

  <h3>Result Table</h3>
  <img src="images/top-products-by-profit.png" alt="Top 10 Products by Profit" style="max-width:100%; height:auto;">

  <h3>Insights</h3>
  <ul>
    <li>Profit is highly concentrated among a small number of products, indicating that a limited subset of the catalog drives a disproportionate share of total profit.</li>
    <li>Most top-profit products are premium outerwear and apparel items (jackets, hoodies, ski pants), suggesting higher margins compared to lower-priced categories.</li>
    <li>Several products achieve high profit despite relatively low unit sales, indicating that per-unit margin is a more important driver of profitability than sales volume for these items.</li>
    <li>Well-known premium brands (e.g., Nike/Jordan, The North Face, Canada Goose) appear frequently in the top results, highlighting the impact of brand positioning and pricing power.</li>
    <li>Revenue and profit rankings are similar but not identical, reinforcing that revenue alone does not fully capture business performance.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>Prioritize inventory availability for these high-profit products to avoid stockouts, especially during peak seasonal demand.</li>
    <li>Increase marketing visibility for these items through homepage placement, targeted email campaigns, and paid advertising to maximize profit contribution.</li>
    <li>Test modest price increases on top-profit products to evaluate demand sensitivity while potentially improving margins further.</li>
    <li>Create product bundles or cross-sell complementary items (e.g., accessories or base layers) to increase average order value without relying on heavy discounting.</li>
    <li>Closely monitor return rates for these products to ensure high profitability is not offset by reverse-logistics and refund costs.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 3 – Top Brands by Profit</strong></summary>

  <h3>Business Question</h3>
  <ul>
    <li>Which brands generate the highest profit?</li>
  </ul>

  <h3>SQL Query</h3>

  <pre><code class="language-sql">WITH brand_metrics AS (
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
</code></pre>

  <h3>Result Table</h3>
  <img src="images/top-brands-by-profit.png" alt="Top 10 Brands by Profit" style="max-width:100%; height:auto;">

  <h3>Insights</h3>
  <ul>
    <li>Profit is highly concentrated among a small subset of brands, indicating that overall profitability depends heavily on a limited number of key partners.</li>
    <li>While high-profit brands also tend to generate strong revenue, the rankings differ, showing that margin structure varies significantly between brands.</li>
    <li>Some brands achieve high profitability with relatively fewer units sold, suggesting premium pricing power or more efficient cost structures.</li>
    <li>Brand-level performance is more stable and predictable than individual product performance, making it a stronger signal for long-term strategic planning.</li>
    <li>The presence of premium brands among the top performers highlights the importance of brand positioning in driving sustainable profit.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>Strengthen relationships with top-performing brands through exclusive product lines, co-marketing campaigns, or preferred supplier agreements.</li>
    <li>Allocate a larger share of marketing budget to high-profit brands to maximize return on advertising spend.</li>
    <li>Expand the product assortment from the most profitable brands to capitalize on demonstrated customer demand.</li>
    <li>Review pricing and cost structures for lower-performing brands to identify opportunities for margin improvement or renegotiation.</li>
    <li>Reduce dependency risk by identifying and developing emerging mid-tier brands that show strong growth potential in profit or revenue.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 4 – Top Products by Profit Margin</strong></summary>

  <h3>Business Question</h3>
  <ul>
    <li>Which products generate the highest profit margins? (Profit margin is defined as profit ÷ revenue.)</li>
  </ul>

  <h3>SQL Query</h3>

  <pre><code class="language-sql">WITH product_totals AS (
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
      WHEN profit / revenue >= 0.50 THEN 'Very High (&gt;= 50%)'
      WHEN profit / revenue >= 0.30 THEN 'High (30%–49.9%)'
      WHEN profit / revenue >= 0.15 THEN 'Medium (15%–29.9%)'
      WHEN profit / revenue &gt; 0 THEN 'Low (0%–14.9%)'
      ELSE 'Negative (&lt;= 0%)'
    END AS margin_tier
  FROM product_totals
)

SELECT *
FROM metrics
WHERE revenue &gt; 0
  AND units_sold &gt;= 3
  AND revenue &gt;= 50   -- takes extremely low volume products out of the picture
ORDER BY profit_margin DESC, profit DESC
LIMIT 10;
</code></pre>

  <h3>Result Table</h3>
  <img src="images/top-products-by-profit-margin.png" alt="Top 10 Products by Profit Margin" style="max-width:100%; height:auto;">

  <h3>Insights</h3>
  <ul>
    <li>The top profit-margin products are high-margin apparel items, with margins clustered around 65–67%, indicating strong pricing power relative to cost.</li>
    <li>All top-margin products fall within the “Blazers &amp; Jackets” category, suggesting that this category benefits from either premium pricing, efficient sourcing, or both.</li>
    <li>These products generate moderate revenue but relatively small sales volumes (3–5 units each), which explains why they did not appear in the top products by total profit or revenue analyses.</li>
    <li>The large gap between profit margin rankings and profit rankings highlights that high margin does not necessarily translate to high total profit without sufficient sales volume.</li>
    <li>Applying minimum thresholds for units sold and revenue helps eliminate misleading results driven by extremely small denominators, producing a more business-relevant view of product efficiency.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>Prioritize marketing tests for high-margin products. Increase visibility through targeted promotions, homepage placement, or paid ads to determine whether demand can be scaled while maintaining strong margins.</li>
    <li>Evaluate supply chain scalability for high-margin categories. Investigate whether the cost structure enabling these margins can be maintained at higher volumes.</li>
    <li>Use profit margin to guide discount strategy. High-margin products can tolerate deeper discounts while remaining profitable, making them ideal candidates for seasonal promotions or customer acquisition campaigns.</li>
    <li>Reassess low-margin, high-volume products. Review for potential price optimization, cost reduction, or bundling strategies.</li>
    <li>Incorporate margin metrics into assortment planning. Consider profit margin alongside revenue and volume to optimize long-term profitability.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 5 – Top Products by Return Rate</strong></summary>

  <h3>Business Question</h3>
  <ul>
    <li>Which products have the highest return rates?</li>
  </ul>

  <h3>SQL Query</h3>

  <pre><code class="language-sql">WITH product_status_counts AS (
  SELECT
    p.id AS product_id,
    p.name AS product_name,
    p.category AS product_category,

    -- Denominator: all purchased units that are either Complete or Returned
    COUNT(*) AS total_purchased_units,

    -- Status-based unit counts
    SUM(CASE WHEN o.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
    SUM(CASE WHEN o.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,

    -- Sales metrics based on completed purchases only
    SUM(CASE WHEN o.status = 'Complete' THEN oi.sale_price ELSE 0 END) AS revenue,
    SUM(CASE WHEN o.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0 END) AS profit

  FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
    ON oi.order_id = o.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
    ON oi.product_id = p.id
  WHERE o.status IN ('Complete', 'Returned')
  GROUP BY 1, 2, 3
),

final AS (
  SELECT
    product_id,
    product_name,
    product_category,

    total_purchased_units AS units_purchased,
    units_completed,
    units_returned,

    -- Return rate as a percentage
    ROUND(units_returned / NULLIF(total_purchased_units, 0) * 100, 2) AS return_rate_pct,

    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,

    -- Average profit per completed unit (simple proxy used to estimate profit at risk from returns)
    ROUND(profit / NULLIF(units_completed, 0), 2) AS avg_profit_per_completed_unit,

    -- Estimated profit impacted by returns (simple proxy)
    ROUND(units_returned * (profit / NULLIF(units_completed, 0)), 2) AS est_profit_lost_to_returns,

    -- Ranks (portfolio-friendly context)
    RANK() OVER (ORDER BY units_returned / NULLIF(total_purchased_units, 0) DESC) AS return_rate_rank,
    RANK() OVER (ORDER BY units_returned DESC) AS returns_volume_rank,

    -- Risk tiers via CASE
    CASE
      WHEN total_purchased_units = 0 THEN 'Undefined'
      WHEN units_returned / NULLIF(total_purchased_units, 0) &gt;= 0.30 THEN 'Very High (&gt;= 30%)'
      WHEN units_returned / NULLIF(total_purchased_units, 0) &gt;= 0.20 THEN 'High (20%–29.9%)'
      WHEN units_returned / NULLIF(total_purchased_units, 0) &gt;= 0.10 THEN 'Medium (10%–19.9%)'
      WHEN units_returned &gt; 0 THEN 'Low (0%–9.9%)'
      ELSE 'None (0%)'
    END AS return_risk_tier

  FROM product_status_counts
)

SELECT
  product_id,
  product_name,
  product_category,
  units_purchased,
  units_completed,
  units_returned,
  return_rate_pct,
  revenue,
  profit,
  avg_profit_per_completed_unit,
  est_profit_lost_to_returns,
  return_risk_tier,
  return_rate_rank,
  returns_volume_rank
FROM final
-- Filters to reduce noise (tune as needed; these align with your earlier low-volume filtering approach)
WHERE units_purchased &gt;= 5
  AND revenue &gt;= 50
ORDER BY return_rate_pct DESC, units_returned DESC, revenue DESC
LIMIT 10;
</code></pre>

  <h3>Result Table</h3>
  <img src="images/top-products-by-return-rate.png" alt="Top 10 Products by Return Rate" style="max-width:100%; height:auto;">

  <h3>Insights</h3>
  <ul>
    <li>The top return-rate products exhibit extremely high return rates (80%–83%), meaning that only 1 out of every 5–6 purchases is ultimately kept by the customer.</li>
    <li>These high-return products span multiple apparel categories (leggings, shorts, jeans, outerwear, suits, skirts, swimwear) as well as accessories, indicating that the issue is not isolated to a single product type but is broader across fit- and style-sensitive items.</li>
    <li>Despite relatively low sales volumes, these products generate meaningful revenue and profit on completed purchases, but the estimated profit lost to returns is substantial relative to their realized profit, significantly reducing net contribution.</li>
    <li>Several products fall into the “Very High (≥ 30%)” return-risk tier by a wide margin, suggesting systematic problems such as sizing inconsistencies, misleading product images/descriptions, or quality issues.</li>
    <li>The presence of both high return rates and high estimated profit loss highlights returns as a critical operational risk, not just a customer-experience issue.</li>
    <li>Using total purchased units (completed + returned) as the denominator produces realistic return rates and avoids misleading values above 100%, strengthening the reliability of the analysis.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>Audit high-return products individually. Review product pages, size charts, material descriptions, and customer feedback for these SKUs to identify common reasons for dissatisfaction or mismatch with customer expectations.</li>
    <li>Improve sizing and fit guidance for apparel. Introduce enhanced sizing charts, customer fit reviews, model measurements, and fit-prediction tools to reduce uncertainty before purchase.</li>
    <li>Prioritize quality control for repeat offenders. Products with consistently high return rates should undergo supplier and manufacturing reviews to detect defects or inconsistencies.</li>
    <li>Adjust merchandising and promotion strategy. Avoid aggressively promoting high-return products until root causes are addressed, as scaling sales would likely amplify profit losses.</li>
    <li>Introduce targeted return-reduction experiments. Test changes such as improved product photography, clearer fabric descriptions, or virtual try-on tools on high-risk products to measure their impact on return rates.</li>
    <li>Incorporate return-rate thresholds into product lifecycle decisions. Consider redesigning, repricing, renegotiating supplier terms, or discontinuing products that remain in the “Very High” risk tier after remediation efforts.</li>
    <li>Track return rate alongside revenue and profit in performance reporting. Product success should be evaluated using a balanced scorecard of sales volume, profit margin, and return rate to avoid optimizing for revenue at the expense of profitability.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 6 – Long-Term Trends in Revenue, Profit, and Returns</strong></summary>

  <h3>Business Question</h3>
  <ul>
    <li>How have revenue, profit, and return rates evolved over the company’s lifetime, and what long-term trends or structural shifts are observable?</li>
  </ul>

  <h3>SQL Query</h3>

  <pre><code class="language-sql">WITH base AS (
  SELECT
    DATE_TRUNC(o.created_at, MONTH) AS month,

    COUNT(*) AS total_units,

    SUM(CASE WHEN o.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
    SUM(CASE WHEN o.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,

    SUM(CASE WHEN o.status = 'Complete' THEN oi.sale_price ELSE 0 END) AS revenue,
    SUM(CASE WHEN o.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0 END) AS profit

  FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` o
    ON oi.order_id = o.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` p
    ON oi.product_id = p.id

  WHERE o.status IN ('Complete', 'Returned')
  GROUP BY 1
),

metrics AS (
  SELECT
    month,
    total_units,
    units_completed,
    units_returned,

    ROUND(units_returned / NULLIF(total_units, 0) * 100, 2) AS return_rate_pct,
    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,

    -- Month-over-month growth
    ROUND(
      (revenue - LAG(revenue) OVER (ORDER BY month))
      / NULLIF(LAG(revenue) OVER (ORDER BY month), 0) * 100,
      2
    ) AS revenue_mom_growth_pct,

    ROUND(
      (profit - LAG(profit) OVER (ORDER BY month))
      / NULLIF(LAG(profit) OVER (ORDER BY month), 0) * 100,
      2
    ) AS profit_mom_growth_pct,

    -- Rolling 3-month averages (trend smoothing)
    ROUND(AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2)
      AS revenue_3mo_avg,

    ROUND(AVG(profit) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2)
      AS profit_3mo_avg

  FROM base
)

SELECT *
FROM metrics
ORDER BY month;
</code></pre>

  <h3>Result Tables</h3>

  <h4>Revenue and Profit</h4>
  <ul>
    <li>REVENUE is GREEN</li>
    <li>PROFIT is BLUE</li>
  </ul>
  <img src="images/long-term-trends-revenue-and-profit.png" alt="Long Term Trends: Revenue and Profit" style="max-width:100%; height:auto;">

  <h4>Returns</h4>
  <ul>
    <li>UNITS PURCHASED is BLUE</li>
    <li>UNITS COMPLETED is GREEN</li>
    <li>UNITS RETURNED is PURPLE</li>
  </ul>
  <img src="images/long-term-trends-returns.png" alt="Long Term Trends: Returns" style="max-width:100%; height:auto;">

  <h3>Insights</h3>
  <ul>
    <li>Revenue (green line) and profit (blue line) both show strong long-term upward growth, indicating sustained expansion of the business over time.</li>
    <li>Profit closely tracks revenue throughout the company’s lifetime, suggesting that operating costs and pricing strategy have remained relatively stable as sales volume increased.</li>
    <li>The gap between revenue and profit remains consistent, implying that margins have not materially deteriorated during periods of rapid growth.</li>
    <li>Units purchased (blue) and units completed (green) rise steadily over time, confirming that revenue growth is primarily driven by increased transaction volume rather than short-term pricing spikes.</li>
    <li>Units returned (purple) also increase as sales scale, but remain substantially lower than completed purchases, indicating that returns have not outpaced business growth.</li>
    <li>A noticeable acceleration in all metrics occurs in the later periods, signaling either increased customer acquisition, expanded product offerings, or improved marketing effectiveness.</li>
    <li>The early years exhibit lower and more volatile performance, consistent with a typical early-stage growth phase before reaching operational maturity.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>Continue investing in scalable operations. The rapid growth in order volume suggests that fulfillment, logistics, and customer support infrastructure should be continuously expanded to avoid bottlenecks and service degradation.</li>
    <li>Protect profit margins during expansion. As revenue grows, closely monitor unit economics to ensure rising costs (shipping, returns, marketing, suppliers) do not erode profitability.</li>
    <li>Track return rate as a leading risk indicator. Although returns remain proportionally smaller than completed orders, their absolute growth means even small increases in return rate could significantly impact future profit.</li>
    <li>Use historical growth patterns for forecasting. The consistent upward trajectory can be leveraged to build more accurate revenue, staffing, and inventory forecasts for upcoming quarters.</li>
    <li>Identify drivers behind recent acceleration. Analyze marketing campaigns, product launches, or channel expansion that coincided with the latest growth phase to replicate successful strategies.</li>
    <li>Introduce capacity planning for peak growth periods. The steep upward trend in recent months suggests upcoming demand surges should be anticipated with proactive inventory purchasing and supplier coordination.</li>
    <li>Pair volume growth with customer experience optimization. As scale increases, improving product descriptions, sizing accuracy, and post-purchase support can prevent returns from becoming a larger drag on profitability.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 7 – Seasonal Trends in Revenue, Profit, and Returns</strong></summary>

  <h3>Business Question</h3>
  <ul>
    <li>How do revenue, profit, and return rates vary by month of the year, and which seasons represent peak performance or elevated return risk?</li>
  </ul>

  <h3>SQL Query</h3>

  <pre><code class="language-sql">WITH base AS (
  SELECT
    EXTRACT(MONTH FROM o.created_at) AS month_num,
    FORMAT_DATE('%B', DATE(o.created_at)) AS month_name,

    COUNT(*) AS total_units,

    SUM(CASE WHEN o.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
    SUM(CASE WHEN o.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,

    SUM(CASE WHEN o.status = 'Complete' THEN oi.sale_price ELSE 0 END) AS revenue,
    SUM(CASE WHEN o.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0 END) AS profit

  FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` o
    ON oi.order_id = o.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` p
    ON oi.product_id = p.id

  WHERE o.status IN ('Complete', 'Returned')
  GROUP BY 1, 2
),

metrics AS (
  SELECT
    month_num,
    month_name,

    total_units AS units_purchased,
    units_completed,
    units_returned,

    ROUND(units_returned / NULLIF(total_units, 0) * 100, 2) AS return_rate_pct,

    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,

    ROUND(profit / NULLIF(units_completed, 0), 2) AS avg_profit_per_completed_unit

  FROM base
)

SELECT *
FROM metrics
ORDER BY month_num;
</code></pre>

  <h3>Result Tables</h3>

  <h4>Revenue and Profit</h4>
  <ul>
    <li>REVENUE is GREEN</li>
    <li>PROFIT is BLUE</li>
  </ul>
  <img src="images/seasonal-trends-revenue-and-profit.png" alt="Seasonal Trends: Revenue and Profit" style="max-width:100%; height:auto;">

  <h4>Returns</h4>
  <ul>
    <li>UNITS PURCHASED is GREEN</li>
    <li>UNITS COMPLETED is BLUE</li>
    <li>UNITS RETURNED is PURPLE</li>
  </ul>
  <img src="images/seasonal-trends-returns.png" alt="Seasonal Trends: Returns" style="max-width:100%; height:auto;">

  <h3>Insights</h3>
  <ul>
    <li>Revenue (green) and profit (blue) both exhibit clear seasonality, with performance weakest early in the year and steadily increasing toward year-end, peaking in late Q4.</li>
    <li>The consistent gap between revenue and profit across months suggests that profit margins remain relatively stable throughout the year, even during high-volume periods.</li>
    <li>Units purchased and units completed follow the same seasonal pattern as revenue, confirming that sales volume — not price fluctuations — is the primary driver of seasonal performance.</li>
    <li>Units returned (purple) also increase toward the end of the year, indicating that higher sales volumes are accompanied by higher absolute return volumes during peak seasons.</li>
    <li>Despite higher return volumes in late months, completed purchases remain substantially higher than returns, suggesting that peak-season growth remains net-positive for profitability.</li>
    <li>The sharp drop in performance from January to February followed by gradual growth throughout the year highlights a post-holiday slowdown and a steady build-up toward holiday demand.</li>
    <li>Seasonal alignment across revenue, profit, and operational volume indicates predictable consumer behavior patterns that can be leveraged for planning and forecasting.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>Increase inventory levels ahead of peak months. Stock critical and high-demand products earlier in Q3 and Q4 to avoid stockouts during the highest-revenue periods.</li>
    <li>Scale fulfillment and customer support capacity seasonally. Prepare warehouses, shipping partners, and support teams for higher order and return volumes in late-year months to prevent operational bottlenecks.</li>
    <li>Launch targeted promotions during low-demand months. Use discounts, bundles, or loyalty incentives in early-year months to smooth demand and reduce seasonal revenue volatility.</li>
    <li>Proactively manage returns during peak season. Improve product descriptions, sizing guidance, and quality checks ahead of Q4 to limit the financial and operational impact of increased returns.</li>
    <li>Align marketing spend with seasonal ROI. Concentrate advertising budgets in months with historically higher conversion and profitability to maximize return on marketing investment.</li>
    <li>Incorporate seasonality into financial forecasting. Budgeting, staffing, and procurement plans should explicitly account for cyclical demand patterns to avoid over- or under-resourcing.</li>
    <li>Monitor seasonal return rates as a profitability safeguard. Tracking return rates alongside revenue ensures that peak sales periods do not mask rising hidden costs from excessive returns.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 8 – Customer Lifetime Value (CLV) and Retention Patterns</strong></summary>

  <h3>Business Question</h3>
  <ul>
    <li>Which customers generate the highest lifetime revenue and profit, and what purchasing patterns distinguish high-value customers from the rest?</li>
  </ul>

  <h3>SQL Query</h3>

  <pre><code class="language-sql">WITH completed_orders AS (
  SELECT
    o.user_id AS customer_id,
    o.order_id,
    o.created_at,
    oi.sale_price,
    p.cost
  FROM `bigquery-public-data.thelook_ecommerce.orders` o
  JOIN `bigquery-public-data.thelook_ecommerce.order_items` oi
    ON o.order_id = oi.order_id
  JOIN `bigquery-public-data.thelook_ecommerce.products` p
    ON oi.product_id = p.id
  WHERE o.status = 'Complete'
),

customer_aggregates AS (
  SELECT
    customer_id,

    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(*) AS total_items,

    ROUND(SUM(sale_price), 2) AS lifetime_revenue,
    ROUND(SUM(sale_price - cost), 2) AS lifetime_profit,

    MIN(created_at) AS first_purchase_date,
    MAX(created_at) AS last_purchase_date,

    DATE_DIFF(DATE(MAX(created_at)), DATE(MIN(created_at)), DAY) AS customer_tenure_days
  FROM completed_orders
  GROUP BY customer_id
),

final AS (
  SELECT
    *,

    ROUND(lifetime_revenue / NULLIF(total_orders, 0), 2) AS avg_order_value,
    ROUND(lifetime_profit / NULLIF(total_orders, 0), 2) AS avg_profit_per_order,

    RANK() OVER (ORDER BY lifetime_revenue DESC) AS revenue_rank,
    RANK() OVER (ORDER BY lifetime_profit DESC) AS profit_rank
  FROM customer_aggregates
)

SELECT *
FROM final
ORDER BY lifetime_profit DESC
LIMIT 20;
</code></pre>

  <h3>Result Table</h3>
  <img src="images/top-customers-by-profit.png" alt="Top Customers By Profit" style="max-width:100%; height:auto;">

  <h3>Insights</h3>
  <ul>
    <li>High lifetime value is driven more by high order value than by high purchase frequency. Several top-profit customers placed only 1–3 orders but generated over $600 in lifetime profit due to very large basket sizes.</li>
    <li>Customer tenure varies widely among top contributors. Some high-value customers have been active for 2–5 years, while others generated substantial profit in a single day, indicating both long-term loyal customers and high-impact one-time buyers.</li>
    <li>Average profit per order is consistently high among top customers (often $300–$600+), suggesting that premium-priced products or bundled purchases are a major driver of customer profitability.</li>
    <li>Revenue rank and profit rank are closely aligned, indicating that cost structures are relatively stable across customers and that higher spending customers also tend to be more profitable customers.</li>
    <li>Repeat customers do contribute meaningfully to lifetime value, but frequency alone does not guarantee high profitability—order size is a stronger determinant of customer value in this dataset.</li>
    <li>A small number of customers contribute disproportionately to total profit, reinforcing the presence of a classic “high-value minority” segment.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li>Identify and segment high-value customers based on lifetime profit and average order value, and prioritize them for retention efforts such as loyalty programs, early access to new products, or personalized promotions.</li>
    <li>Develop targeted marketing campaigns focused on increasing basket size (cross-selling and bundling), since order value appears to drive profitability more strongly than purchase frequency.</li>
    <li>Create a “VIP customer” tier using thresholds for lifetime profit or average profit per order to encourage repeat purchases from already high-margin customers.</li>
    <li>Analyze the product categories and brands most frequently purchased by top-value customers to guide inventory planning, merchandising, and premium product expansion.</li>
    <li>Use customer tenure metrics to distinguish between long-term loyal customers and high-value one-time buyers, and apply different engagement strategies to each group (retention vs. reactivation vs. acquisition lookalikes).</li>
    <li>Allocate customer acquisition budget toward channels that historically attract high-order-value customers rather than optimizing solely for customer volume.</li>
    <li>Track CLV alongside revenue and profit in executive reporting to ensure marketing and product decisions focus on long-term profitability rather than short-term sales growth.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Conclusion</strong></summary>

  <p>
    This project provided a comprehensive SQL-driven analysis of transactional e-commerce data using the
    <code>thelook_ecommerce</code> BigQuery public dataset. Across eight structured analyses, I explored key business
    performance metrics including revenue, profit, units sold, units returned, return rate, and profit margin.
    I also examined long-term growth trends, seasonal patterns, and customer lifetime value (CLV) to generate
    actionable business insights.
  </p>

  <p><strong>The analysis demonstrated that:</strong></p>
  <ul>
    <li>Revenue and profit have grown steadily over time, driven largely by increased sales volume.</li>
    <li>Profitability is concentrated among specific high-margin products and brands, though the highest revenue items do not always align with the most efficient ones.</li>
    <li>Return behavior represents meaningful operational risk that varies across products, requiring strategy beyond simple revenue optimization.</li>
    <li>Seasonal patterns indicate predictable cycles in customer demand and returns, which can inform inventory planning and marketing cadence.</li>
    <li>Customer lifetime value is distributed across a broad base of moderate-value customers rather than a small group of “whales,” highlighting the importance of scalable acquisition and retention strategies.</li>
  </ul>

  <p>
    Together, these results show how SQL can be used to extract business-relevant insight from raw transactional data,
    informing decisions in pricing, inventory, product mix, marketing, and customer experience. The analyses illustrate
    a complete analytical workflow — from data modeling and metric engineering to business interpretation and strategic
    recommendation — and demonstrate how strong data foundations support measurable commercial impact.
  </p>

</details>
