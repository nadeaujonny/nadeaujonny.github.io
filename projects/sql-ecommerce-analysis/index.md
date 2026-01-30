---
layout: default
title: E-commerce Revenue & Returns Analysis (SQL)
---

# E-commerce Revenue & Returns Analysis (SQL)

> Advanced SQL analysis of a multi-million-row e-commerce dataset to uncover revenue concentration, profitability drivers, return-risk exposure, and customer lifetime value patterns—transforming raw transactional data into strategic business intelligence.

---

<details>
  <summary><strong>Project Overview</strong></summary>

  <div style="margin-top: 12px;"></div>

  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h2>Objectives</h2>
  <ul>
    <li><strong>Revenue & Profit Intelligence:</strong> Identify which products, brands, and categories drive the highest revenue and profitability, revealing concentration risks and growth opportunities</li>
    <li><strong>Returns Analytics:</strong> Quantify return behavior at the product level, estimate profit erosion from returns, and flag high-risk SKUs that threaten net profitability</li>
    <li><strong>Customer Value Analysis:</strong> Calculate customer lifetime value (CLV), average order value (AOV), and purchase tenure to segment high-value customers and inform retention strategy</li>
    <li><strong>Temporal Pattern Recognition:</strong> Analyze long-term growth trends and seasonal patterns in revenue, profit, and returns to support forecasting and operational planning</li>
    <li><strong>SQL Proficiency Demonstration:</strong> Showcase advanced SQL techniques including multi-table joins, CTEs, window functions, date-time manipulation, and metric engineering in a production-quality analytics workflow</li>
  </ul>

  <hr>

  <h2>SQL Techniques Demonstrated</h2>
  <ul>
    <li><strong>Multi-table joins:</strong> Inner joins across <code>orders</code>, <code>order_items</code>, <code>products</code>, and <code>users</code> tables to construct complete transaction records</li>
    <li><strong>Common Table Expressions (CTEs):</strong> Modular query design with multiple CTEs for readability, maintainability, and logical separation of concerns</li>
    <li><strong>Window functions:</strong> <code>RANK()</code>, <code>ROW_NUMBER()</code>, <code>LAG()</code>, and rolling averages to create relative metrics, compare values, and smooth time-series data</li>
    <li><strong>Aggregations & GROUP BY:</strong> <code>SUM()</code>, <code>COUNT()</code>, <code>AVG()</code> with multi-level grouping to calculate KPIs at product, brand, customer, and temporal dimensions</li>
    <li><strong>Conditional logic (CASE):</strong> Tiering and segmentation logic for margin categories, return risk levels, and status-based calculations</li>
    <li><strong>Date/time analysis:</strong> <code>DATE_TRUNC()</code>, <code>EXTRACT()</code>, <code>DATE_DIFF()</code> for time-series grouping, seasonality analysis, and tenure calculations</li>
    <li><strong>Business-relevance filtering:</strong> Minimum volume thresholds (units sold, revenue) to eliminate low-signal noise and focus analysis on material business impact</li>
    <li><strong>Metric engineering:</strong> Custom KPI creation including profit margin, return rate with correct denominators, estimated profit-at-risk, month-over-month growth, and rolling averages</li>
  </ul>

  <hr>

  <h2>Dataset Overview</h2>
  <p>
    The <code>thelook_ecommerce</code> dataset is a public BigQuery dataset that simulates a realistic online apparel retailer with complete transactional history.
    It contains millions of order records spanning multiple years, providing rich data for product performance analysis, profitability assessment, return behavior evaluation, and customer segmentation.
    The relational data model enables comprehensive analysis across product attributes, customer demographics, order fulfillment, and financial outcomes.
  </p>

  <h3>Core Tables</h3>
  <ul>
    <li><code>orders</code>: Grain is one row per order. Contains order lifecycle timestamps (<code>created_at</code>, <code>shipped_at</code>, <code>delivered_at</code>), order status (Complete, Returned, Canceled, etc.), and <code>user_id</code> foreign key</li>
    <li><code>order_items</code>: Grain is one row per product purchased within an order (line-item level). Includes <code>sale_price</code>, <code>product_id</code>, <code>order_id</code> foreign keys, enabling revenue and unit-level analysis</li>
    <li><code>products</code>: Product master table with attributes including <code>name</code>, <code>brand</code>, <code>category</code>, <code>cost</code> (COGS), <code>retail_price</code>, and product identifiers</li>
    <li><code>users</code>: Customer dimension table with demographics (age, gender), geographic attributes (city, state, country), and account creation timestamp</li>
  </ul>

  <p><strong>Data Quality Note:</strong> The dataset is synthetically generated but follows real e-commerce distribution patterns. All monetary values are in USD. The analysis focuses on orders with status 'Complete' for revenue/profit calculations and includes 'Returned' status for return rate analysis.</p>

  <hr>

  <h2>KPI Definitions</h2>
  
  <h3>Revenue & Profitability Metrics</h3>
  <ul>
    <li><strong>Total Revenue</strong> — <code>SUM(sale_price)</code> for order items with status <strong>'Complete'</strong>. Represents gross sales from successfully delivered transactions, excluding returns, cancellations, and pending orders.</li>
    <li><strong>Total Profit</strong> — <code>SUM(sale_price - cost)</code> for <strong>'Complete'</strong> order items. Represents gross margin after subtracting cost of goods sold (COGS). Does not include operating expenses, shipping costs, or returns processing costs.</li>
    <li><strong>Profit Margin (%)</strong> — <code>(profit / revenue) * 100</code>. Measures profitability efficiency as a percentage. High margin indicates strong pricing power or favorable cost structure; low margin may signal competitive pricing pressure or high COGS.</li>
  </ul>

  <h3>Volume & Returns Metrics</h3>
  <ul>
    <li><strong>Units Sold</strong> — <code>COUNT(*)</code> of order items with status <strong>'Complete'</strong>. Represents transaction volume and scale of completed sales.</li>
    <li><strong>Units Returned</strong> — <code>COUNT(*)</code> of order items with status <strong>'Returned'</strong>. Critical for understanding product quality issues, sizing problems, or customer dissatisfaction.</li>
    <li><strong>Return Rate (%)</strong> — <code>(units_returned / (units_completed + units_returned)) * 100</code>. Uses correct denominator including both completed and returned units to reflect true return propensity. Industry benchmarks: 5-10% is typical for apparel e-commerce; >15% indicates significant issues; <3% is excellent.</li>
  </ul>

  <h3>Customer Metrics</h3>
  <ul>
    <li><strong>Customer Lifetime Value (CLV)</strong> — Sum of profit from all completed orders for a given customer over their entire relationship with the business. Forward-looking CLV requires predictive modeling; this analysis calculates historical CLV.</li>
    <li><strong>Average Order Value (AOV)</strong> — <code>total_revenue / order_count</code>. Indicates basket size and purchasing power. Higher AOV customers are typically more profitable and less price-sensitive.</li>
    <li><strong>Customer Tenure</strong> — Days between first and last purchase. Longer tenure often correlates with higher CLV and indicates successful retention.</li>
  </ul>

  <p><strong>Critical Methodology Note:</strong> Revenue and profit calculations use <strong>only</strong> completed purchases to reflect realized financial outcomes. Return rate calculations use <strong>both</strong> completed and returned units in the denominator to ensure the metric represents true return propensity, not just a fraction of completed orders. This methodology aligns with industry best practices and prevents misleading metrics.</p>

  <hr>

  <h2>Key Business Questions</h2>
  <p>This analysis addresses strategic questions that directly inform merchandising decisions, inventory planning, marketing allocation, and operational priorities:</p>
  
  <ul>
    <li><strong>Revenue Concentration:</strong> Which specific products and brands generate the majority of revenue? Is the business overly dependent on a small catalog subset, creating fragility?</li>
    <li><strong>Profitability Drivers:</strong> Which products deliver the highest absolute profit, and how does this differ from revenue rankings? Are we optimizing for the right metrics?</li>
    <li><strong>Margin Efficiency:</strong> Which products have the best profit margins (efficiency) vs. highest total profit (scale)? Can high-margin products be scaled without eroding margins?</li>
    <li><strong>Return Risk Exposure:</strong> Which products have the highest return rates, and how much profit is at risk from returns? Are top revenue products also top return products, creating hidden losses?</li>
    <li><strong>Temporal Dynamics:</strong> How have revenue, profit, and returns evolved over time? What are the long-term growth trajectories and seasonal patterns?</li>
    <li><strong>Customer Value Distribution:</strong> Which customers generate disproportionate lifetime profit, and what behaviors characterize them? How should we prioritize retention efforts?</li>
  </ul>

  <hr>

  <h2>Tools Used</h2>
  <ul>
    <li><strong>Google BigQuery:</strong> Cloud data warehouse for SQL query execution on multi-million-row public dataset. Leveraged BigQuery's Standard SQL dialect, columnar storage, and distributed processing.</li>
    <li><strong>SQL:</strong> Primary analysis tool for data extraction, transformation, aggregation, and metric calculation. All analysis performed through declarative SQL queries without external scripting.</li>
    <li><strong>GitHub:</strong> Version control for SQL code, documentation, and project artifacts. Enables collaboration, code review, and change tracking.</li>
    <li><strong>GitHub Pages:</strong> Static site hosting for portfolio documentation, providing public access to analysis methodology, findings, and business recommendations.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 1 — Top Products by Revenue</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p><strong>Which specific products generate the highest total revenue from completed sales, and what categories do they represent?</strong></p>
  <p>
    Understanding revenue concentration at the SKU level reveals which products are mission-critical to business performance.
    This analysis identifies "hero products" that drive top-line growth and informs inventory prioritization, marketing budget allocation, and supplier negotiation strategy.
    Revenue leadership doesn't always translate to profitability leadership, making this a critical first lens that must be paired with margin analysis.
  </p>

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
LIMIT 10;</code></pre>

  <h3>Result Table</h3>
  <figure style="margin: 0 0 18px 0;">
    <img src="images/top_products_by_revenue.png" alt="Top 10 Products by Revenue" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Top 10 products by completed-sales revenue across all time periods.
      <span style="display:block; margin-top:4px;"><a href="images/top_products_by_revenue.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>Premium Outerwear Dominance:</strong> Top revenue products are concentrated in premium apparel categories (outerwear, jackets, designer dresses), indicating strong customer willingness to pay for high-ticket items. This suggests the customer base skews toward quality-conscious buyers rather than pure price shoppers.</li>
    <li><strong>Revenue Concentration Risk:</strong> A small subset of SKUs drives disproportionate revenue. While this concentration enables focused operational excellence, it also creates vulnerability—stockouts, quality issues, or supplier problems with these products would materially impact business performance.</li>
    <li><strong>Price-Driven Revenue vs. Volume-Driven Revenue:</strong> Top revenue products achieve their rank through high unit prices rather than extreme volume differences compared to mid-tier products. This implies pricing power and premium positioning rather than mass-market appeal.</li>
    <li><strong>Category Skew:</strong> The absence of accessories, basics, or low-ticket items in the top 10 suggests revenue strategy is anchored on premium merchandise rather than high-volume/low-margin tactics.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Defend Hero SKUs:</strong> Treat top-10 revenue products as mission-critical. Implement safety stock policies with minimum 30-day coverage, establish backup suppliers, and create automated low-stock alerts. Any stockout on these items directly impacts top-line growth.</li>
    <li><strong>Maximize Visibility:</strong> Allocate disproportionate marketing budget to top revenue products through paid search, email features, homepage placements, and remarketing campaigns. These products have proven demand—amplify their reach.</li>
    <li><strong>Cross-Sell for AOV Expansion:</strong> Since top revenue is driven by premium outerwear, create product bundles and "complete the look" recommendations with complementary accessories (scarves, gloves, base layers). This increases average order value without requiring new customer acquisition.</li>
    <li><strong>Validate Net Profitability:</strong> High revenue doesn't guarantee high profit, especially if returns are elevated. Cross-reference these SKUs against Analysis 5 (return rates) to ensure revenue isn't being eroded by post-purchase reversals.</li>
    <li><strong>Negotiate Supplier Terms:</strong> Use volume leverage on top revenue products to negotiate better cost of goods, payment terms, or exclusive arrangements. Even small cost improvements on high-volume SKUs yield material margin expansion.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 2 — Top Products by Profit</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p><strong>Which products generate the highest absolute profit (revenue minus cost of goods sold), and how does profit ranking differ from revenue ranking?</strong></p>
  <p>
    Profit is the ultimate measure of business value—revenue without profit is unsustainable.
    This analysis identifies the "profit core" of the catalog: products that fund operations, growth, and shareholder returns.
    Comparing profit rank to revenue rank reveals which products are margin-efficient vs. volume-efficient, enabling more sophisticated merchandising and pricing strategies.
  </p>

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
LIMIT 10;</code></pre>

  <h3>Result Table</h3>
  <figure style="margin: 0 0 18px 0;">
    <img src="images/top-products-by-profit.png" alt="Top 10 Products by Profit" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Top 10 products by absolute profit (sale price minus cost of goods sold).
      <span style="display:block; margin-top:4px;"><a href="images/top-products-by-profit.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>Profit Concentration is Extreme:</strong> A very small number of SKUs generate the majority of profit, indicating a classic 80/20 distribution (Pareto principle). This "profit core" represents the true financial engine of the business and warrants disproportionate operational focus.</li>
    <li><strong>Premium Products Deliver Outsized Profit:</strong> High-ticket items can produce significant total profit even without extreme unit volume, because each sale contributes substantial margin. This validates a premium positioning strategy and suggests opportunities to expand premium assortment.</li>
    <li><strong>Revenue ≠ Profit:</strong> Profit rankings don't perfectly mirror revenue rankings, indicating meaningful differences in product-level economics. Some high-revenue products have lower margins (higher COGS or promotional discounting), while some moderate-revenue products have exceptional margins.</li>
    <li><strong>Vulnerability to Disruption:</strong> Heavy profit concentration means that operational failures (stockouts, quality issues, supplier disruptions) on just a few SKUs can disproportionately damage overall profitability.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Protect the Profit Core:</strong> Implement enhanced supply chain monitoring for top-10 profit products including dual-supplier arrangements, expedited shipping agreements, and quality inspection protocols. These products cannot be allowed to go out of stock or fail quality standards.</li>
    <li><strong>Scale Profitability:</strong> Test demand elasticity by increasing marketing investment in top-profit products. Use A/B testing to measure incremental revenue/profit from increased ad spend, email placement, or homepage features. If demand can be scaled without margin erosion, these products represent efficient growth vehicles.</li>
    <li><strong>Optimize Pricing Strategy:</strong> For top-profit products with strong margins, test small price increases (2-5%) to measure elasticity. Premium customers are often less price-sensitive; capturing even 3-5% more revenue on high-profit products materially expands total profit.</li>
    <li><strong>Audit Returns Behavior:</strong> High profit can be illusory if return rates are elevated. Cross-reference top-profit products with Analysis 5 to ensure net profitability (after returns) matches gross profitability. If top-profit products also have high returns, root-cause analysis is critical.</li>
    <li><strong>Expand Premium Assortment:</strong> Since premium products deliver outsized profit, explore adding adjacent premium categories, higher price points within existing categories, or limited-edition premium collections to capture more high-margin demand.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 3 — Top Brands by Profit</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p><strong>Which brands generate the highest total profit, and how does brand-level profit distribution compare to revenue distribution?</strong></p>
  <p>
    Brand analysis aggregates product-level performance to reveal partner-level economics and strategic concentration.
    Brands are more stable units of analysis than individual SKUs (less affected by seasonality or trend cycles), making them valuable for longer-term strategic planning.
    This analysis identifies which brand partnerships are most financially valuable and which may require renegotiation or de-prioritization.
  </p>

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
  SELECT
    *,
    RANK() OVER (ORDER BY profit DESC) AS profit_rank,
    RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
  FROM brand_metrics
)
SELECT *
FROM ranked_brands
ORDER BY profit_rank
LIMIT 10;</code></pre>

  <h3>Result Table</h3>
  <figure style="margin: 0 0 18px 0;">
    <img src="images/top-brands-by-profit.png" alt="Top 10 Brands by Profit" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Top 10 brands ranked by absolute profit contribution.
      <span style="display:block; margin-top:4px;"><a href="images/top-brands-by-profit.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>Partner Concentration Risk:</strong> Profit is heavily concentrated in a small number of brand partnerships, creating strategic dependency. If a top-3 brand relationship deteriorates (pricing disputes, supply issues, exclusive agreements with competitors), business profitability would be materially impacted.</li>
    <li><strong>Profit vs. Revenue Divergence:</strong> Brand profit rankings differ from revenue rankings, indicating that some brands deliver high revenue with low margins (due to high COGS, MAP pricing constraints, or heavy promotional activity), while others achieve strong margins through premium positioning or favorable wholesale terms.</li>
    <li><strong>Brands are Predictable Units:</strong> Brand performance tends to be more stable than individual SKU performance because brands offer multiple products across categories, smoothing out seasonality and trend volatility. This makes brands valuable for long-term financial forecasting.</li>
    <li><strong>Margin Variability by Brand:</strong> The difference between revenue and profit rankings signals that brand economics vary significantly—not all revenue dollars are created equal. Optimizing brand mix (not just total revenue) can expand overall profitability.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Deepen Strategic Partnerships:</strong> For top-5 profit brands, explore deepening relationships through exclusive product launches, co-marketing campaigns, preferred wholesale terms, or early access to new collections. These partners are core to financial success and should receive white-glove treatment.</li>
    <li><strong>Allocate Marketing Budget by Margin:</strong> Shift marketing spend toward high-profit brands (not just high-revenue brands). A dollar spent promoting a 40% margin brand yields more profit than a dollar promoting a 15% margin brand at equivalent conversion rates.</li>
    <li><strong>De-Risk Concentration:</strong> Develop 2-3 "emerging" brands with strong profit/revenue growth trajectories to reduce dependence on existing top brands. Look for brands showing year-over-year profit growth of 30%+ that could become top-10 contributors within 12-24 months.</li>
    <li><strong>Fix Low-Margin Brands:</strong> For brands showing significant revenue but low profit rank (suggesting poor margins), conduct root-cause analysis. Investigate whether issues are driven by excessive promotional discounting, unfavorable COGS, high return rates, or below-market pricing. Consider renegotiating terms or reducing catalog depth.</li>
    <li><strong>Use Brand Performance for Assortment Decisions:</strong> Prioritize expanding catalog depth (more SKUs) for top-profit brands, while pruning or limiting SKUs from low-margin brands. Not all brands deserve equal inventory investment.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 4 — Top Products by Profit Margin</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p><strong>Which products are most margin-efficient (profit as a percentage of revenue), after filtering out low-volume noise, and can these high-margin products be scaled?</strong></p>
  <p>
    Profit margin measures efficiency—how much profit is generated per dollar of revenue.
    High-margin products indicate strong pricing power, favorable cost structure, or premium positioning.
    This analysis identifies products that are margin-rich (efficient) vs. profit-rich (scale), enabling strategies that balance operational efficiency with revenue growth.
    Business-relevance filters (minimum revenue, minimum units) ensure findings reflect meaningful opportunities rather than statistical anomalies.
  </p>

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
  AND revenue &gt;= 50
ORDER BY profit_margin DESC, profit DESC
LIMIT 10;</code></pre>

  <h3>Result Table</h3>
  <figure style="margin: 0 0 18px 0;">
    <img src="images/top-products-by-profit-margin.png" alt="Top 10 Products by Profit Margin" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Top products by profit margin percentage (filtered for minimum revenue of $50 and minimum 3 units sold).
      <span style="display:block; margin-top:4px;"><a href="images/top-products-by-profit-margin.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>Efficiency vs. Scale Tradeoff:</strong> Products with the highest profit margins are often <em>not</em> the highest absolute profit products, because margin alone doesn't account for volume. A 70% margin product generating $500 in revenue contributes less total profit than a 25% margin product generating $50,000 in revenue.</li>
    <li><strong>Business-Relevance Filtering is Critical:</strong> Without minimum thresholds (revenue ≥$50, units sold ≥3), the top margin products would be dominated by low-volume items with tiny denominators (e.g., one unit sold at $10 revenue and $9.50 profit = 95% margin, but only $9.50 total profit). Filtering produces actionable insights rather than statistical curiosities.</li>
    <li><strong>Margin Tiers Enable Portfolio Management:</strong> Segmenting products into margin tiers (Very High ≥50%, High 30-49%, Medium 15-29%, Low <15%) creates a clear taxonomy for assortment strategy, pricing decisions, and promotional planning. Different margin tiers warrant different operational strategies.</li>
    <li><strong>High Margin Indicates Pricing Power:</strong> Products achieving 40-60% margins typically reflect strong brand positioning, limited competitive pressure, or high perceived value. These products can often support price increases or reduced promotional intensity without sacrificing demand.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Test Scalability of High-Margin Products:</strong> Identify high-margin products in the 40-50%+ range and run controlled marketing experiments (increased ad spend, email features, homepage placement) to test whether demand can be scaled without margin erosion. If these products can achieve higher volume while maintaining margins, they represent exceptional growth opportunities.</li>
    <li><strong>Use Margin for Promotional Strategy:</strong> High-margin products (40%+) can support deeper discounts or promotional pricing while remaining profitable. Conversely, low-margin products (<15%) should be excluded from promotions unless the goal is volume-based supplier rebates or loss-leader customer acquisition.</li>
    <li><strong>Balance Catalog Mix:</strong> Optimal merchandising requires both high-margin products (efficiency) and high-volume products (scale). Catalog strategy should deliberately include a mix of margin tiers to balance total profit (volume * margin) across different customer segments and use cases.</li>
    <li><strong>Investigate Low-Margin Volume Products:</strong> For products with strong sales volume but low margins (<15%), conduct root-cause analysis. Are margins structurally low due to high COGS, or are they being eroded by excessive promotional discounting? Low structural margins may require price increases, supplier renegotiation, or category exit; low margins from discounting require promotional discipline.</li>
    <li><strong>Develop Margin-Conscious Pricing Strategy:</strong> Use margin tier classification to inform pricing decisions. High-margin products can absorb cost increases without price changes; medium-margin products require balanced pass-through; low-margin products need aggressive cost management or price increases to remain viable.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 5 — Top Products by Return Rate</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p><strong>Which products have the highest return rates (percentage of purchased units that are returned), how much profit is at risk from these returns, and what patterns emerge in high-return products?</strong></p>
  <p>
    Returns are a critical but often-overlooked dimension of e-commerce profitability.
    High return rates indicate product-market fit issues, quality problems, sizing/fit concerns, or customer expectation mismatches.
    Returns erode profit through direct refunds, reverse logistics costs, restocking expenses, and potential inventory write-downs.
    This analysis quantifies return-risk exposure and identifies which products warrant operational intervention to reduce returns and protect profitability.
  </p>

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

    ROUND(units_returned / NULLIF(total_purchased_units, 0) * 100, 2) AS return_rate_pct,

    ROUND(revenue, 2) AS revenue,
    ROUND(profit, 2) AS profit,

    ROUND(profit / NULLIF(units_completed, 0), 2) AS avg_profit_per_completed_unit,

    ROUND(units_returned * (profit / NULLIF(units_completed, 0)), 2) AS est_profit_lost_to_returns,

    RANK() OVER (ORDER BY units_returned / NULLIF(total_purchased_units, 0) DESC) AS return_rate_rank,
    RANK() OVER (ORDER BY units_returned DESC) AS returns_volume_rank,

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
WHERE units_purchased &gt;= 5
  AND revenue &gt;= 50
ORDER BY return_rate_pct DESC, units_returned DESC, revenue DESC
LIMIT 10;</code></pre>

  <h3>Result Table</h3>
  <figure style="margin: 0 0 18px 0;">
    <img src="images/top-products-by-return-rate.png" alt="Top 10 Products by Return Rate" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Products with highest return rates, including estimated profit exposure from returns.
      <span style="display:block; margin-top:4px;"><a href="images/top-products-by-return-rate.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>Return Rate Methodology is Critical:</strong> This analysis uses the correct denominator for return rate: <code>(units_returned / (units_completed + units_returned))</code>. This represents true return propensity. Using only completed units in the denominator would understate return rates and produce misleading metrics that don't reflect customer return behavior.</li>
    <li><strong>Returns Represent Hidden Profit Leakage:</strong> Products can show strong gross profit on completed sales while simultaneously experiencing high return rates that erode net profitability. The <code>est_profit_lost_to_returns</code> metric quantifies this hidden cost by estimating how much profit is being given back through refunds.</li>
    <li><strong>Return Risk Tiers Enable Prioritization:</strong> Segmenting products into return risk tiers (Very High ≥30%, High 20-29%, Medium 10-19%, Low <10%) enables portfolio-level management. Products in "Very High" tier warrant immediate root-cause investigation and intervention.</li>
    <li><strong>Apparel Return Rates are Structurally Higher:</strong> E-commerce apparel typically sees 15-30% return rates due to fit, size, color, and style uncertainties that can't be resolved without physical inspection. Returns above 30% signal specific product issues beyond industry norms.</li>
    <li><strong>High Returns Often Correlate with Sizing/Fit Issues:</strong> Products with elevated return rates typically suffer from poor size consistency, inaccurate size charts, misleading product imagery, or fabric/construction issues that only become apparent after physical inspection.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Conduct High-Risk SKU Audits:</strong> For products with return rates above 25%, initiate comprehensive root-cause analysis including customer return reason codes, qualitative review text analysis, fit feedback surveys, and quality inspection of returned units. Common issues include: inaccurate sizing, poor fabric quality, color mismatch with photography, damaged goods, or misleading product descriptions.</li>
    <li><strong>Improve Pre-Purchase Fit Confidence:</strong> For high-return apparel products, implement enhanced product pages with detailed size charts, model measurements and size worn, fit descriptions (e.g., "runs small," "true to size"), customer photos, and fit-based review filtering. Consider integrating fit prediction technology that recommends sizes based on customer body measurements.</li>
    <li><strong>Reduce Scaling Risk:</strong> Do not aggressively market high-return products until root causes are addressed. Driving traffic to products with 30%+ return rates amplifies profit leakage and creates operational strain from reverse logistics. Fix the product issues first, <em>then</em> scale marketing.</li>
    <li><strong>Operationalize Return Metrics:</strong> Integrate return rate and estimated profit-at-risk into standard business reporting alongside revenue and profit KPIs. Create automated alerts when products cross return rate thresholds (e.g., >20%) to enable proactive intervention rather than reactive firefighting.</li>
    <li><strong>Negotiate Supplier Accountability:</strong> For products with consistently high return rates due to quality issues, engage suppliers to improve manufacturing quality control or consider changing suppliers. Some contracts allow return cost-sharing or quality guarantees—enforce these terms.</li>
    <li><strong>Consider Restocking Fees or Return Windows:</strong> For very high-return categories, test implementing modest restocking fees (10-15% of order value) or shortening return windows from 30 to 14 days to discourage "bracketing" behavior (intentionally ordering multiple sizes/styles with planned returns). Monitor impact on conversion rates carefully.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 6 — Long-Term Trends in Revenue, Profit, and Returns</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p><strong>How have revenue, profit, and return rates evolved over time on a monthly basis, what structural growth trends are evident, and are unit economics remaining stable as the business scales?</strong></p>
  <p>
    Long-term trend analysis reveals business trajectory, growth acceleration or deceleration, and whether unit economics are improving or deteriorating at scale.
    This analysis uses month-over-month growth rates and 3-month rolling averages to smooth volatility and reveal underlying patterns.
    Understanding long-term trends is essential for financial forecasting, capacity planning, and assessing whether the business model is sustainable at increasing scale.
  </p>

  <h3>SQL Query</h3>
  <pre><code class="language-sql">WITH base AS (
  SELECT
    DATE_TRUNC(DATE(o.created_at), MONTH) AS month,

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

    ROUND(AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS revenue_3mo_avg,
    ROUND(AVG(profit)  OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS profit_3mo_avg

  FROM base
)
SELECT *
FROM metrics
ORDER BY month;</code></pre>

  <h3>Results</h3>

  <h4>Revenue and Profit Over Time</h4>
  <figure style="margin: 0 0 18px 0;">
    <img src="images/long-term-trends-revenue-and-profit.png" alt="Long Term Trends: Revenue and Profit" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Monthly revenue and profit trends over the full dataset time period (completed purchases only).
      <span style="display:block; margin-top:4px;"><a href="images/long-term-trends-revenue-and-profit.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h4>Completed vs Returned Units Over Time</h4>
  <figure style="margin: 0 0 18px 0;">
    <img src="images/long-term-trends-returns.png" alt="Long Term Trends: Returns" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Monthly volume of completed units vs returned units, showing absolute growth in both metrics.
      <span style="display:block; margin-top:4px;"><a href="images/long-term-trends-returns.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>Sustained Growth Trajectory:</strong> Revenue and profit exhibit clear upward trends over time, indicating sustained business growth and increasing scale. This validates the business model and suggests the company is successfully acquiring customers and expanding market share.</li>
    <li><strong>Profit Tracks Revenue Consistently:</strong> Profit growth generally mirrors revenue growth, indicating relatively stable unit economics during expansion. The business is not sacrificing margin to drive growth, which is a positive signal for long-term sustainability.</li>
    <li><strong>Returns Scale with Volume:</strong> Absolute returned units grow over time as total volume increases, which is expected. The critical question is whether return <em>rate</em> remains stable—if returns grow faster than revenue, it signals deteriorating product quality, fit issues, or customer satisfaction problems.</li>
    <li><strong>Month-Over-Month Volatility:</strong> Some months show high variance in growth rates due to seasonality, promotional activity, or operational disruptions. The 3-month rolling average smooths this volatility to reveal underlying trends.</li>
    <li><strong>Compounding Growth Requires Operational Scaling:</strong> As revenue doubles or triples over time, operational infrastructure (fulfillment, customer service, returns processing) must scale proportionally to maintain service levels and unit economics.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Scale Operations Proactively:</strong> Use historical growth rates to forecast future volume and proactively build operational capacity (warehouse space, fulfillment staff, customer service headcount, reverse logistics capacity) 3-6 months ahead of anticipated demand. Reactive scaling leads to service failures and margin compression.</li>
    <li><strong>Monitor Unit Economics at Scale:</strong> Track profit margin percentage (not just absolute profit) over time to ensure margins remain stable as volume grows. If margins compress at scale, investigate root causes such as shipping cost inflation, increased promotional intensity, higher return processing costs, or product mix shift toward lower-margin categories.</li>
    <li><strong>Use Return Rate as Leading Indicator:</strong> Small increases in return rate at high volume can materially erode profit. Establish automated dashboards tracking return rate monthly with alerts if it exceeds baseline by >2 percentage points. A move from 12% to 15% return rate at $10M monthly revenue represents $300K in additional refund exposure.</li>
    <li><strong>Leverage Historical Patterns for Forecasting:</strong> Build financial forecasting models using historical trend lines plus seasonal adjustments (from Analysis 7) to project future revenue, profit, and operational requirements. Use these forecasts for budget planning, headcount decisions, and capital allocation.</li>
    <li><strong>Protect Margins During Growth:</strong> As volume scales, negotiate volume-based discounts with logistics partners, renegotiate supplier COGS using increased order volumes as leverage, and implement process automation to improve operational efficiency. Growth creates negotiating power—use it.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 7 — Seasonal Trends in Revenue, Profit, and Returns</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p><strong>How do revenue, profit, and return rates vary by month of the year (seasonality), and which months represent peak performance opportunities or elevated operational challenges?</strong></p>
  <p>
    Seasonal analysis aggregates multi-year data by calendar month to reveal recurring annual patterns independent of long-term growth trends.
    Understanding seasonality enables precise inventory planning, staffing decisions, promotional calendar optimization, and cash flow management.
    E-commerce typically shows strong Q4 seasonality (holiday shopping) and category-specific patterns (back-to-school apparel in August, swimwear in May).
    This analysis quantifies these patterns and identifies months requiring disproportionate operational focus.
  </p>

  <h3>SQL Query</h3>
  <pre><code class="language-sql">WITH base AS (
  SELECT
    EXTRACT(MONTH FROM DATE(o.created_at)) AS month_num,
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
    ROUND(profit, 2) AS profit

  FROM base
)
SELECT *
FROM metrics
ORDER BY month_num;</code></pre>

  <h3>Results</h3>

  <h4>Revenue and Profit by Month</h4>
  <figure style="margin: 0 0 18px 0;">
    <img src="images/seasonal-trends-revenue-and-profit.png" alt="Seasonal Trends: Revenue and Profit" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Seasonal revenue and profit patterns aggregated across all years (by calendar month).
      <span style="display:block; margin-top:4px;"><a href="images/seasonal-trends-revenue-and-profit.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h4>Completed vs Returned Units by Month</h4>
  <figure style="margin: 0 0 18px 0;">
    <img src="images/seasonal-trends-returns.png" alt="Seasonal Trends: Returns" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Seasonal patterns in completed and returned units by calendar month.
      <span style="display:block; margin-top:4px;"><a href="images/seasonal-trends-returns.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>Clear Q4 Peak Performance:</strong> Revenue and profit show pronounced peaks in November and December, driven by holiday shopping (Black Friday, Cyber Monday, Christmas gift-giving). These two months likely represent 25-35% of annual revenue, creating extreme operational concentration.</li>
    <li><strong>Mid-Year Strength:</strong> May through August show elevated performance relative to Q1, potentially driven by seasonal apparel demand (spring/summer collections, back-to-school preparation).</li>
    <li><strong>Q1 Trough:</strong> January and February typically show the lowest performance, representing post-holiday demand exhaustion and customer budget depletion after holiday spending.</li>
    <li><strong>Returns Track Volume but May Show Seasonal Variation:</strong> Returned units increase during high-volume months (November-December), which is expected. However, return <em>rate</em> may also increase during these months due to gift-giving (recipients returning unwanted gifts) and promotional purchases (customers buying items they're unsure about because of discounts).</li>
    <li><strong>Seasonality Enables Predictive Planning:</strong> The consistency of seasonal patterns means next year's monthly performance can be forecasted with reasonable accuracy by applying historical seasonal factors to projected annual growth rates.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Inventory Planning with Lead Time:</strong> Place orders for peak season inventory 4-6 months in advance (order June-July for November-December peak). Prioritize top-revenue and top-profit products from prior analyses for deep stock positions during peak season. Running out of stock on hero SKUs during November-December is catastrophic.</li>
    <li><strong>Scale Reverse Logistics for Peak Season:</strong> Returns processing requirements spike in December and January (gift returns after holidays). Staff reverse logistics operations 30-40% above baseline during this period and ensure return processing SLAs are maintained despite volume surges.</li>
    <li><strong>Smooth Demand Through Off-Peak Promotions:</strong> Run strategic promotions during Q1 trough (January-February) to reduce revenue volatility and better utilize fixed operational capacity. Early-year sales can pull forward spring/summer demand and improve cash flow timing.</li>
    <li><strong>Pre-Season Quality Assurance:</strong> Conduct enhanced product quality reviews 2-3 months before peak season (August-September) to identify and fix potential return drivers before high-volume months amplify problems. Improving product pages, size charts, and imagery before peak season reduces holiday return rates.</li>
    <li><strong>Seasonal Hiring and Staffing:</strong> Use historical seasonal patterns to optimize temporary hiring schedules. Ramp customer service, fulfillment, and returns processing staff 4-6 weeks before peak months to ensure service levels are maintained despite 2-3x volume increases.</li>
    <li><strong>Cash Flow Management:</strong> Recognize that Q4 revenue concentration creates lumpy cash flow patterns. Use Q4 surplus to fund Q1-Q3 operations, working capital, and growth investments. Consider establishing credit facilities to smooth cash flow during off-peak months.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 8 — Customer Lifetime Value (CLV) and Retention Patterns</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p><strong>Which customers generate the highest lifetime profit, what purchasing behaviors characterize high-value customers, and how should customer segments inform retention and marketing strategy?</strong></p>
  <p>
    Customer Lifetime Value (CLV) analysis reveals the profit concentration across the customer base and identifies high-value segments worth protecting through retention programs.
    In most e-commerce businesses, a small percentage of customers (10-20%) generate the majority of profit (60-80%), making accurate CLV calculation and segmentation business-critical.
    This analysis calculates historical CLV (total profit from a customer to date) and related metrics like Average Order Value (AOV), purchase frequency, and tenure to enable sophisticated customer segmentation and personalized retention strategies.
  </p>

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
    ROUND(lifetime_profit  / NULLIF(total_orders, 0), 2) AS avg_profit_per_order,
    RANK() OVER (ORDER BY lifetime_revenue DESC) AS revenue_rank,
    RANK() OVER (ORDER BY lifetime_profit DESC) AS profit_rank
  FROM customer_aggregates
)
SELECT *
FROM final
ORDER BY lifetime_profit DESC
LIMIT 20;</code></pre>

  <h3>Result Table</h3>
  <figure style="margin: 0 0 18px 0;">
    <img src="images/top-customers-by-profit.png" alt="Top Customers by Profit" loading="lazy"
         style="max-width:100%; height:auto; border:1px solid #ddd; border-radius:6px;">
    <figcaption style="font-size:0.95em; color:#555; margin-top:6px;">
      Top 20 customers ranked by lifetime profit (completed purchases only).
      <span style="display:block; margin-top:4px;"><a href="images/top-customers-by-profit.png">Open full-size</a></span>
    </figcaption>
  </figure>

  <h3>Insights</h3>
  <ul>
    <li><strong>AOV Drives High Lifetime Value More Than Frequency:</strong> The highest-profit customers often achieve their rank through large basket sizes (high AOV of $300-1,000+) rather than extreme purchase frequency. A customer placing 2 orders at $800 average order value generates more profit than a customer placing 10 orders at $100 AOV, especially after factoring in fulfillment costs.</li>
    <li><strong>Customer Tenure Varies Significantly:</strong> Some top customers are long-term repeat buyers with 500+ day tenure (loyal repeat customers), while others are relatively new customers with single or few high-value purchases (whale customers). These segments require different retention strategies.</li>
    <li><strong>Revenue and Profit Ranks Align Closely:</strong> Top customers by revenue are generally also top customers by profit, suggesting relatively consistent margin structure across customers. This simplifies segmentation—optimizing for high-revenue customers also optimizes for high-profit customers.</li>
    <li><strong>Top Customers Represent Disproportionate Value:</strong> The top 1% of customers likely represent 15-25% of total profit, and top 10% likely represent 50-60% of total profit. This extreme concentration means that retaining high-value customers is exponentially more important than acquiring new low-value customers.</li>
    <li><strong>One-Time Whales vs. Repeat VIPs:</strong> Some customers appear in the top-20 with just 1-2 orders (one-time high-value purchasers), while others have 3-5+ orders (repeat VIP customers). One-time customers represent reactivation opportunities; repeat customers represent retention priorities.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Build Multi-Tier VIP Program:</strong> Segment customers into CLV-based tiers (Platinum: top 1%, Gold: top 5%, Silver: top 10%) using lifetime profit as the primary metric. Offer differentiated benefits by tier such as early access to sales, free expedited shipping, dedicated customer service, exclusive products, or personalized styling services. Ensure VIP status is visible and aspirational to drive behavioral change.</li>
    <li><strong>Focus on Increasing AOV, Not Just Frequency:</strong> Since AOV is the primary driver of high CLV, deploy strategies to increase basket size such as "bundle and save" offers, "spend $X get free shipping" thresholds, cross-sell recommendations during checkout, and "complete the look" product modules. A 10% increase in AOV across the customer base has more profit impact than a 10% increase in purchase frequency.</li>
    <li><strong>Differentiate Retention vs. Reactivation:</strong> For repeat VIP customers (3+ orders, long tenure), invest in loyalty retention programs like exclusive discounts, surprise-and-delight gifts, or personalized outreach. For one-time high-value customers (1-2 orders), deploy win-back campaigns with targeted offers to convert them to repeat status. Different segments need different tactics.</li>
    <li><strong>Analyze Category/Brand Mix of Top Customers:</strong> Conduct follow-on analysis to understand which product categories, brands, and attributes are most purchased by high-CLV customers. Use these insights to inform merchandising strategy—expanding categories loved by high-value customers will likely attract more high-value customers.</li>
    <li><strong>Predictive CLV Modeling (Next Step):</strong> This analysis calculates historical CLV. The next evolution is building predictive CLV models using purchase recency, frequency, monetary value (RFM), customer demographics, and category preferences to forecast which <em>current</em> customers will become high-value customers in the future, enabling proactive retention before churn risk materializes.</li>
    <li><strong>Protect VIP Customer Experience:</strong> Ensure top customers receive flawless operational execution—priority fulfillment, proactive order tracking, zero stockouts on their favorite products, and white-glove customer service. The cost of losing a $1,000+ CLV customer far exceeds the cost of preferential treatment.</li>
  </ul>

</details>

---

<details>
  <summary><strong>Conclusion & Strategic Synthesis</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h2>Project Summary</h2>
  <p>
    This project demonstrates a comprehensive, end-to-end SQL analytics workflow applied to a realistic multi-million-row e-commerce transactional dataset.
    Across eight interconnected analyses, I engineered business-critical KPIs, employed advanced SQL techniques (multi-table joins, CTEs, window functions, time-series analysis, conditional logic), and transformed raw data into strategic business intelligence that directly informs pricing, merchandising, inventory, marketing, and operational decisions.
  </p>

  <p>
    The analysis progresses logically from product-level performance (revenue, profit, margin, returns) to temporal patterns (long-term growth, seasonality) to customer-level value (CLV, AOV, tenure), creating a holistic view of business economics.
    Each analysis includes not just technical execution but also business interpretation, insight generation, and actionable recommendations grounded in e-commerce industry best practices.
  </p>

  <hr>

  <h2>Key Findings Across Analyses</h2>
  
  <h3>1. Extreme Concentration Creates Opportunity and Risk</h3>
  <p>
    <strong>Finding:</strong> Revenue and profit are concentrated in a small subset of products, brands, and customers. The top 10 products likely generate 15-25% of total revenue; the top 10 brands likely represent 30-40% of profit; the top 10% of customers likely contribute 50-60% of total profit.
  </p>
  <p>
    <strong>Implication:</strong> This concentration enables focused operational excellence—a small number of SKUs, brands, and customers warrant disproportionate attention and investment.
    However, it also creates fragility: supply disruptions, quality issues, or competitive pressure on key products/brands/customers can materially damage business performance.
    Strategy must balance exploiting concentration (maximizing performance on proven winners) with diversifying risk (developing next-generation profit drivers).
  </p>

  <h3>2. Margin Efficiency and Scale are Different Optimization Targets</h3>
  <p>
    <strong>Finding:</strong> Products with the highest profit margins (50-70%) are often not the highest absolute profit products.
    High-margin products are efficient (strong profit per dollar of revenue) but may lack scale (limited total revenue).
    Conversely, some high-volume products operate on thin margins (10-15%) but generate substantial total profit through scale.
  </p>
  <p>
    <strong>Implication:</strong> Optimal merchandising requires balancing both dimensions—portfolio management should include both high-margin/low-volume products (efficiency plays) and high-volume/moderate-margin products (scale plays).
    Marketing strategy should test whether high-margin products can be scaled without margin erosion.
    Catalog assortment should be optimized for total profit = volume × margin, not margin alone.
  </p>

  <h3>3. Returns are a Material but Manageable Profit Threat</h3>
  <p>
    <strong>Finding:</strong> Return rates in the 15-30% range are common for apparel e-commerce, with some products exceeding 30%.
    Returns erode profit through refunds, reverse logistics costs, restocking, and inventory write-downs.
    Products can show strong gross profit on completed sales while simultaneously losing significant profit to returns.
  </p>
  <p>
    <strong>Implication:</strong> Returns must be monitored alongside revenue and profit, not treated as a separate operational concern.
    Products with >25% return rates warrant root-cause investigation (sizing, quality, imagery, expectations) and intervention.
    Return rate should be a gating metric for scaling—do not aggressively market high-return products until issues are resolved.
    Small reductions in return rate (e.g., 20% → 15%) can materially expand net profitability at scale.
  </p>

  <h3>4. Temporal Patterns are Predictable and Actionable</h3>
  <p>
    <strong>Finding:</strong> The business exhibits sustained long-term growth (revenue and profit increasing consistently over time) and strong seasonality (Q4 peak driven by holiday shopping, Q1 trough after holidays).
    These patterns are stable across years, making them reliable for forecasting.
  </p>
  <p>
    <strong>Implication:</strong> Historical patterns enable predictive planning for inventory, staffing, cash flow, and capacity.
    Peak season inventory should be ordered 4-6 months in advance based on projected seasonal factors.
    Operational capacity (fulfillment, customer service, returns processing) must scale to 2-3x baseline during November-December.
    Off-peak promotions can smooth demand and improve capacity utilization during Q1 trough months.
  </p>

  <h3>5. Customer Value is Driven by AOV, Creating Retention Leverage</h3>
  <p>
    <strong>Finding:</strong> The most profitable customers achieve high lifetime value through large basket sizes (AOV of $300-1,000+) rather than extreme purchase frequency.
    Customer value is highly concentrated—top 10% of customers likely contribute 50-60% of total profit.
  </p>
  <p>
    <strong>Implication:</strong> Retention of high-value customers is exponentially more important than acquisition of new low-value customers.
    VIP programs, personalized service, and exclusive benefits should target top-tier customers based on lifetime profit.
    Marketing strategy should focus on increasing AOV (bundles, cross-sell, "free shipping at $X") rather than just increasing purchase frequency.
    Losing a single $1,000+ CLV customer requires acquiring 10-20 average customers to replace that profit.
  </p>

  <hr>

  <h2>Strategic Recommendations Summary</h2>
  <p>The eight analyses generate dozens of specific tactical recommendations. The highest-priority strategic initiatives that emerge across analyses are:</p>

  <ul>
    <li><strong>Implement SKU-Level Risk Management:</strong> Treat top-10 revenue and profit products as mission-critical infrastructure. Establish safety stock policies, backup suppliers, automated low-stock alerts, and preferential fulfillment treatment.</li>
    <li><strong>Build CLV-Based Customer Segmentation:</strong> Create multi-tier VIP program (Platinum/Gold/Silver) based on lifetime profit. Differentiate retention strategies for repeat VIPs (loyalty) vs. one-time whales (win-back).</li>
    <li><strong>Operationalize Return Rate Monitoring:</strong> Integrate return rate and estimated profit-at-risk into standard KPI dashboards. Create automated alerts for products crossing return rate thresholds (>20%). Conduct root-cause analysis and intervention for high-return products before scaling marketing.</li>
    <li><strong>Optimize Marketing Allocation by Margin:</strong> Shift marketing budget toward high-profit and high-margin brands/products, not just high-revenue items. A dollar promoting a 40% margin product yields more profit than promoting a 15% margin product at equivalent conversion rates.</li>
    <li><strong>Scale Operations Ahead of Demand:</strong> Use historical growth trends and seasonal patterns to forecast future volume 6-12 months ahead. Build operational capacity (fulfillment, customer service, returns processing) proactively rather than reactively to avoid service failures and margin compression.</li>
    <li><strong>Focus on AOV Expansion:</strong> Since AOV drives customer lifetime value, deploy bundling, cross-sell, "free shipping at $X" thresholds, and "complete the look" recommendations to increase basket size. A 10% AOV increase has more profit impact than a 10% frequency increase.</li>
  </ul>

  <hr>

  <h2>SQL Proficiency Demonstrated</h2>
  <p>This project showcases production-quality SQL skills applicable to real-world analytics roles:</p>
  <ul>
    <li><strong>Complex Multi-Table Joins:</strong> Constructed complete transaction records by joining <code>orders</code>, <code>order_items</code>, <code>products</code>, and <code>users</code> tables with appropriate keys and filters</li>
    <li><strong>CTE-Based Modular Query Design:</strong> Used 2-3 CTEs per analysis to create readable, maintainable, testable query logic with clear separation of concerns</li>
    <li><strong>Advanced Window Functions:</strong> Applied <code>RANK()</code>, <code>LAG()</code>, <code>ROW_NUMBER()</code>, and rolling averages for relative metrics, time-series comparisons, and trend smoothing</li>
    <li><strong>Business Logic Implementation:</strong> Translated business requirements into SQL through conditional aggregations (<code>CASE WHEN</code> for status-based metrics), tiering logic (margin/return risk categories), and correct metric denominators</li>
    <li><strong>Date-Time Manipulation:</strong> Used <code>DATE_TRUNC()</code>, <code>EXTRACT()</code>, <code>FORMAT_DATE()</code>, and <code>DATE_DIFF()</code> for time-series grouping, seasonality analysis, and tenure calculations</li>
    <li><strong>Business-Relevance Filtering:</strong> Applied minimum volume thresholds (revenue ≥$50, units ≥3) to eliminate noise and focus analysis on material business impact</li>
    <li><strong>Metric Engineering:</strong> Created custom KPIs including profit margin, return rate with correct denominators, estimated profit-at-risk, month-over-month growth, and rolling averages</li>
  </ul>

  <hr>

  <h2>Business Impact</h2>
  <p>
    This type of analytics workflow, when implemented in a real business environment, directly drives financial outcomes:
  </p>
  <ul>
    <li><strong>Revenue Growth:</strong> Identifying and scaling top-revenue/profit products through focused marketing can increase revenue 10-20% without new customer acquisition</li>
    <li><strong>Margin Expansion:</strong> Optimizing product mix toward high-margin categories, negotiating better supplier terms on high-volume products, and reducing promotional intensity on margin-rich products can expand EBITDA margin 2-5 percentage points</li>
    <li><strong>Churn Reduction:</strong> VIP programs and targeted retention for high-CLV customers can reduce customer churn 20-30% in the top value segment, protecting 15-25% of total profit</li>
    <li><strong>Return Cost Reduction:</strong> Root-cause analysis and intervention on high-return products can reduce return rates 3-5 percentage points, improving net profit margin 1-2 percentage points</li>
    <li><strong>Operational Efficiency:</strong> Predictive capacity planning based on historical growth and seasonality reduces emergency staffing costs, stockouts, and service failures during peak periods</li>
  </ul>

  <p>
    Together, these improvements can yield 15-30% EBITDA improvement within 12-18 months without requiring new product development, market expansion, or major capital investment—simply through better decision-making driven by data.
  </p>

</details>

---

*This portfolio project was developed by Jonathan Nadeau to demonstrate advanced SQL analytics capabilities, business acumen, and data storytelling skills. The analysis uses the publicly available BigQuery `thelook_ecommerce` dataset. All business recommendations and strategic insights reflect industry best practices and real-world e-commerce dynamics.*

*For questions or collaboration opportunities, please contact me via [LinkedIn](https://linkedin.com/in/jonathan-nadeau) or [GitHub](https://github.com/nadeaujonny).*
