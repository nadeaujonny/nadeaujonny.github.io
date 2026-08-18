---
layout: default
title: E-commerce Business Optimization Analysis (BigQuery SQL)
description: "Multi-dimensional e-commerce analysis in BigQuery using CTEs, window functions, conditional aggregation, and cross-metric ranking to evaluate revenue, profitability, return risk, and operational efficiency across 10 analytical dimensions."
---

<a href="/projects/" class="back-to-projects btn">← Back to Projects</a>

# E-commerce Business Optimization Analysis (SQL)

> A 10-section analytical deep dive into the BigQuery **thelook_ecommerce** dataset – examining products, brands, categories, long-term trends, seasonal patterns, customers, and distribution centers across revenue, profit, margin, return rate, and lost revenue metrics to produce actionable business recommendations.

---

<details>
  <summary><strong>Introduction</strong></summary>

  <div style="margin-top: 12px;"></div>

<h3>Project Objective</h3>

<p>This project analyzes a large-scale e-commerce dataset to identify revenue drivers, profit optimization opportunities, return risk patterns, and operational inefficiencies – the same kinds of questions a data analyst would be asked to investigate at a real retail or e-commerce company. The framing is straightforward: if I were hired as a data analyst at this company, what would I investigate first, what would I find, and what would I recommend? Every analysis section ends with concrete, actionable business recommendations – not just charts and tables. The goal is to demonstrate that data analysis is only valuable when it translates into decisions.</p>

<h3>Dataset Overview</h3>

<p>The dataset used is <strong>thelook_ecommerce</strong>, a public dataset hosted in Google BigQuery (<code>bigquery-public-data.thelook_ecommerce</code>). It simulates a mid-size e-commerce retailer selling apparel, accessories, and outerwear – structurally analogous to real retail datasets with order statuses (Complete, Returned, Cancelled, Shipped, Processing), product costs, sale prices, customer demographics, and distribution center assignments.</p>

<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">
<p><strong>Dataset at a glance:</strong></p>
<ul>
<li><strong>Scale:</strong> ~181,000 order items, ~80,000 unique customers, ~29,000 unique products across ~2,700 brands and 26 product categories</li>
<li><strong>Tables used:</strong> order_items, orders, products, users, distribution_centers, inventory_items</li>
<li><strong>Time range:</strong> 2019 through early 2026 (BigQuery continuously generates synthetic data for this dataset, so the date range extends beyond the original creation date)</li>
<li><strong>Domain:</strong> Simulated e-commerce retailer – apparel, accessories, and outerwear</li>
</ul>
<p><strong>Note:</strong> Because this is a synthetic/simulated dataset, some product prices contain anomalies (e.g., socks listed at $903) that would not exist in production data. These anomalies are left in the analysis as-is since the purpose is to demonstrate analytical methodology rather than clean a specific company's data.</p>
</div>

<h3>SQL Techniques Demonstrated</h3>

<p>The queries in this project go well beyond basic SELECT statements. Each analysis builds complex, multi-layered queries designed to extract derived metrics that do not exist in the raw data – profit margins, return rates, revenue shares, and cross-metric rankings all computed within a single query execution. The following techniques are used consistently throughout:</p>

<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">
<ul>
<li><strong>Common Table Expressions (CTEs):</strong> Multi-layered CTEs (first_layer, second_layer, third_layer) used throughout to build complex metrics incrementally – separating raw aggregation, derived ratio calculations, and ranking into clean logical stages</li>
<li><strong>Window Functions:</strong> RANK(), SUM() OVER(), ROUND() with window clauses for calculating revenue shares, profit shares, and cross-metric rankings within a single query</li>
<li><strong>Conditional Aggregation:</strong> Extensive use of CASE WHEN inside SUM() and COUNT() to calculate status-specific metrics (revenue from completed orders only, return counts, cancellation counts, en-route counts) from a single pass through the data</li>
<li><strong>Multi-table JOINs:</strong> Consistently joining order_items → orders → products (and users, distribution_centers, inventory_items where relevant) to build unified analytical views</li>
<li><strong>NULLIF for safe division:</strong> Used throughout to prevent division-by-zero errors in ratio calculations (profit margin, return rate, completion rate, etc.)</li>
<li><strong>DATE functions:</strong> DATE_TRUNC, EXTRACT(MONTH FROM ...), DATE_DIFF for time-series aggregation and customer lifetime calculations</li>
<li><strong>Subquery filtering:</strong> Third-layer CTEs with WHERE clauses filtering on rank thresholds (e.g., WHERE revenue_rank <= 50) to create contextually meaningful "bottom" analyses rather than simply reversing sort order</li>
</ul>
<p>Every query is written to be readable and self-documenting – clear aliasing, logical CTE naming, and consistent formatting throughout.</p>
</div>

<h3>Analysis Structure</h3>

<p>The analysis is structured across ten analytical dimensions: Top Products, Bottom Products, Top Brands, Bottom Brands, Top Categories, Bottom Categories, Long Term Trends, Seasonal Trends, Customers, and Distribution Centers. Each section examines performance from multiple angles – revenue, profit, profit margin, unit volume, return rate, units returned, lost revenue, and lost profit – providing a 360-degree view rather than a single-metric snapshot.</p>

<p>"Top" and "Bottom" analyses are paired intentionally. Understanding what performs well is only half the picture – identifying underperformers, high-risk products, and margin-compressing segments is equally valuable for business optimization. A company that only monitors its best sellers will miss the products, brands, and categories that are quietly eroding profitability through returns, cancellations, and thin margins.</p>

<p>Every section concludes with an <strong>Analytical Insights &amp; Business Recommendations</strong> block that translates data findings into specific, prioritized actions a business could take.</p>

<h3>Business Context</h3>

<p>E-commerce businesses generate massive transactional datasets but often lack the analytical infrastructure to extract cross-dimensional insights – most reporting stops at top-line revenue. This project goes deeper: it examines where profit is actually generated vs. where revenue is highest (they often diverge), which products and brands are net-negative after accounting for returns and cancellations, and what operational patterns (distribution center inventory imbalances, seasonal demand shifts) are costing the business money.</p>

<p>SQL is the foundational tool for this kind of work because the questions require joining multiple tables, filtering on complex conditions, and computing derived metrics that don't exist in raw data – exactly the workflow a data analyst performs daily. The retail and e-commerce industry context is important here: return rates of 20–30% are common in online apparel retail. The ~28% average return rate observed in this dataset is realistic and aligns with industry benchmarks, which validates the analytical approach.</p>

<h3>Key Metrics Tracked</h3>

<p>The following metrics are computed and referenced throughout every section of the analysis. Understanding these definitions is essential for interpreting the tables and recommendations.</p>

<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">
<ul>
<li><strong>Revenue:</strong> Sum of sale prices from completed orders only</li>
<li><strong>Profit:</strong> Revenue minus product cost for completed orders</li>
<li><strong>Profit Margin:</strong> Profit / Revenue – measures how much of each revenue dollar is retained</li>
<li><strong>Return Rate:</strong> Returned items / (Completed + Returned items) – measures post-delivery dissatisfaction</li>
<li><strong>Completion Rate:</strong> Completed items / (Total items − Cancelled items) – measures fulfillment success</li>
<li><strong>Cancellation Rate:</strong> Cancelled items / Total items ordered</li>
<li><strong>En Route Rate:</strong> Shipped + Processing items / (Total − Cancelled − Returned) – measures what share of surviving orders are still in transit</li>
<li><strong>Lost Revenue / Lost Profit:</strong> Revenue and profit that would have been earned if returned and cancelled orders had completed – quantifies the business cost of failed orders</li>
<li><strong>Revenue Share / Profit Share / Unit Orders Share:</strong> Each entity's contribution to total business volume – enables apples-to-apples comparison across different scales</li>
</ul>
</div>

</details>
<details>
  <summary><strong>Top Products</strong></summary>

  <div style="margin-top: 12px;"></div>

<h3>Top products by Revenue</h3>

<pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = 'Cancelled' THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN ('Shipped', 'Processing') THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
GROUP BY product_name, product_brand, product_category
),
second_layer AS (
SELECT
  *,
  ROUND((profit / NULLIF(revenue, 0)), 4) AS profit_margin,
  ROUND(units_returned / NULLIF(units_completed + units_returned, 0), 4) AS return_rate,
  ROUND(units_completed / NULLIF(unit_orders_placed - units_cancelled, 0), 4) AS completion_rate,
  ROUND(units_cancelled / NULLIF(unit_orders_placed, 0), 4) AS cancellation_rate,
  ROUND(units_en_route / NULLIF(unit_orders_placed - (units_cancelled + units_returned), 0), 4) AS en_route_rate,
  ROUND(revenue / SUM(revenue) OVER(), 7) AS revenue_share,
  ROUND(profit / SUM(profit) OVER(), 7) AS profit_share,
  ROUND(unit_orders_placed / SUM(unit_orders_placed) OVER(), 7) AS unit_orders_placed_share
FROM first_layer
)
SELECT
  *,
  RANK() OVER(ORDER BY avg_product_sale_price DESC) AS avg_product_sale_price_rank,
  RANK() OVER(ORDER BY avg_product_cost DESC) AS avg_product_cost_rank,
  RANK() OVER(ORDER BY revenue DESC) AS revenue_rank,
  RANK() OVER(ORDER BY profit DESC) AS profit_rank,
  RANK() OVER(ORDER BY unit_orders_placed DESC) AS unit_orders_placed_rank,
  RANK() OVER(ORDER BY units_completed DESC) AS units_completed_rank,
  RANK() OVER(ORDER BY units_returned DESC) AS units_returned_rank,
  RANK() OVER(ORDER BY units_cancelled DESC) AS units_cancelled_rank,
  RANK() OVER(ORDER BY units_en_route DESC) AS units_en_route_rank,
  RANK() OVER(ORDER BY lost_revenue DESC) AS lost_revenue_rank,
  RANK() OVER(ORDER BY lost_profit DESC) AS lost_profit_rank,
  RANK() OVER(ORDER BY profit_margin DESC) AS profit_margin_rank,
  RANK() OVER(ORDER BY return_rate DESC) AS return_rate_rank,
  RANK() OVER(ORDER BY completion_rate DESC) AS completion_rate_rank,
  RANK() OVER(ORDER BY cancellation_rate DESC) AS cancellation_rate_rank,
  RANK() OVER(ORDER BY en_route_rate DESC) AS en_route_rate_rank
FROM second_layer
ORDER BY
  revenue_rank ASC
LIMIT 15;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>product_name</th>
      <th>product_brand</th>
      <th>product_category</th>
      <th>avg_product_sale_price</th>
      <th>avg_product_cost</th>
      <th>revenue</th>
      <th>profit</th>
      <th>unit_orders_placed</th>
      <th>units_completed</th>
      <th>units_returned</th>
      <th>units_cancelled</th>
      <th>units_en_route</th>
      <th>lost_revenue</th>
      <th>lost_profit</th>
      <th>profit_margin</th>
      <th>return_rate</th>
      <th>completion_rate</th>
      <th>cancellation_rate</th>
      <th>en_route_rate</th>
      <th>revenue_share</th>
      <th>profit_share</th>
      <th>unit_orders_placed_share</th>
      <th>avg_product_sale_price_rank</th>
      <th>avg_product_cost_rank</th>
      <th>revenue_rank</th>
      <th>profit_rank</th>
      <th>unit_orders_placed_rank</th>
      <th>units_completed_rank</th>
      <th>units_returned_rank</th>
      <th>units_cancelled_rank</th>
      <th>units_en_route_rank</th>
      <th>lost_revenue_rank</th>
      <th>lost_profit_rank</th>
      <th>profit_margin_rank</th>
      <th>return_rate_rank</th>
      <th>completion_rate_rank</th>
      <th>cancellation_rate_rank</th>
      <th>en_route_rate_rank</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>ASCIS Cushion Low Socks (Pack of 3)</td><td>ASICS</td><td>Active</td><td>903.0</td><td>373.84</td><td>3612.0</td><td>2116.63</td><td>11</td><td>4</td><td>0</td><td>1</td><td>6</td><td>903.0</td><td>529.16</td><td>0.586</td><td>0.0</td><td>0.4</td><td>0.0909</td><td>0.6</td><td>0.001338</td><td>0.0015127</td><td>6.07e-05</td><td>5</td><td>28</td><td>1</td><td>1</td><td>1161</td><td>776</td><td>13463</td><td>7029</td><td>1398</td><td>155</td><td>142</td><td>3719</td><td>13463</td><td>7482</td><td>16872</td><td>16953</td></tr>
    <tr><td>The North Face Women's S-XL Oso Jacket</td><td>The North Face</td><td>Outerwear & Coats</td><td>903.0</td><td>378.36</td><td>3612.0</td><td>2098.57</td><td>10</td><td>4</td><td>1</td><td>1</td><td>4</td><td>1806.0</td><td>1049.29</td><td>0.581</td><td>0.2</td><td>0.4444</td><td>0.1</td><td>0.5</td><td>0.001338</td><td>0.0014998</td><td>5.52e-05</td><td>5</td><td>25</td><td>1</td><td>2</td><td>1962</td><td>776</td><td>3978</td><td>7029</td><td>6105</td><td>22</td><td>24</td><td>4209</td><td>12637</td><td>6492</td><td>16366</td><td>19501</td></tr>
    <tr><td>Spyder Women's Jesst In Time Jacket</td><td>Spyder</td><td>Outerwear & Coats</td><td>650.0</td><td>295.75</td><td>3250.0</td><td>1771.25</td><td>10</td><td>5</td><td>4</td><td>0</td><td>1</td><td>2600.0</td><td>1417.0</td><td>0.545</td><td>0.4444</td><td>0.5</td><td>0.0</td><td>0.1667</td><td>0.0012039</td><td>0.0012659</td><td>5.52e-05</td><td>52</td><td>50</td><td>3</td><td>4</td><td>1962</td><td>251</td><td>30</td><td>17458</td><td>23197</td><td>7</td><td>7</td><td>8121</td><td>8264</td><td>3269</td><td>17458</td><td>27059</td></tr>
    <tr><td>Bergama Natural Raccoon Hooded Stroller - - Multicolor</td><td>Bergama</td><td>Outerwear & Coats</td><td>749.99</td><td>306.75</td><td>2999.96</td><td>1772.98</td><td>10</td><td>4</td><td>1</td><td>0</td><td>5</td><td>749.99</td><td>443.24</td><td>0.591</td><td>0.2</td><td>0.4</td><td>0.0</td><td>0.5556</td><td>0.0011113</td><td>0.0012671</td><td>5.52e-05</td><td>40</td><td>43</td><td>4</td><td>3</td><td>1962</td><td>776</td><td>3978</td><td>17458</td><td>3026</td><td>267</td><td>224</td><td>3279</td><td>12637</td><td>7482</td><td>17458</td><td>19270</td></tr>
    <tr><td>Woolrich Arctic Parka DF</td><td>Woolrich</td><td>Outerwear & Coats</td><td>990.0</td><td>478.17</td><td>2970.0</td><td>1535.49</td><td>12</td><td>3</td><td>2</td><td>1</td><td>6</td><td>2970.0</td><td>1535.49</td><td>0.517</td><td>0.4</td><td>0.2727</td><td>0.0833</td><td>0.6667</td><td>0.0011002</td><td>0.0010974</td><td>6.62e-05</td><td>3</td><td>6</td><td>5</td><td>6</td><td>694</td><td>2358</td><td>844</td><td>7029</td><td>1398</td><td>4</td><td>4</td><td>10735</td><td>8312</td><td>14284</td><td>17144</td><td>12990</td></tr>
    <tr><td>Joseph Abboud Men's Two-button Side Vent Sport Coat</td><td>Joseph Abboud</td><td>Suits & Sport Coats</td><td>264.0</td><td>101.9</td><td>2904.0</td><td>1759.82</td><td>30</td><td>11</td><td>2</td><td>2</td><td>15</td><td>1056.0</td><td>656.57</td><td>0.606</td><td>0.1538</td><td>0.3929</td><td>0.0667</td><td>0.5769</td><td>0.0010758</td><td>0.0012577</td><td>0.0001655</td><td>430</td><td>734</td><td>6</td><td>5</td><td>7</td><td>3</td><td>844</td><td>2100</td><td>11</td><td>112</td><td>91</td><td>2144</td><td>13388</td><td>9081</td><td>17408</td><td>18610</td></tr>
    <tr><td>AIR JORDAN DOMINATE SHORTS MENS 465071-100</td><td>Jordan</td><td>Shorts</td><td>903.0</td><td>454.21</td><td>2709.0</td><td>1346.37</td><td>5</td><td>3</td><td>0</td><td>0</td><td>2</td><td>0.0</td><td>0.0</td><td>0.497</td><td>0.0</td><td>0.6</td><td>0.0</td><td>0.4</td><td>0.0010035</td><td>0.0009622</td><td>2.76e-05</td><td>5</td><td>8</td><td>7</td><td>9</td><td>16887</td><td>2358</td><td>13463</td><td>17458</td><td>17069</td><td>22642</td><td>22642</td><td>12874</td><td>13463</td><td>2189</td><td>17458</td><td>23875</td></tr>
    <tr><td>The North Face Denali Down Mens Jacket 2013</td><td>The North Face</td><td>Outerwear & Coats</td><td>903.0</td><td>436.15</td><td>2709.0</td><td>1400.55</td><td>13</td><td>3</td><td>2</td><td>2</td><td>6</td><td>3612.0</td><td>1867.4</td><td>0.517</td><td>0.4</td><td>0.2727</td><td>0.1538</td><td>0.6667</td><td>0.0010035</td><td>0.001001</td><td>7.17e-05</td><td>5</td><td>10</td><td>7</td><td>7</td><td>423</td><td>2358</td><td>844</td><td>2100</td><td>1398</td><td>2</td><td>3</td><td>10735</td><td>8312</td><td>14284</td><td>12634</td><td>12990</td></tr>
    <tr><td>Diesel Men's Lagnum Leather Jacket</td><td>Diesel</td><td>Outerwear & Coats</td><td>598.0</td><td>267.9</td><td>2392.0</td><td>1320.38</td><td>7</td><td>4</td><td>1</td><td>1</td><td>1</td><td>1196.0</td><td>660.19</td><td>0.552</td><td>0.2</td><td>0.6667</td><td>0.1429</td><td>0.2</td><td>0.0008861</td><td>0.0009437</td><td>3.86e-05</td><td>57</td><td>56</td><td>9</td><td>10</td><td>8625</td><td>776</td><td>3978</td><td>7029</td><td>23197</td><td>92</td><td>89</td><td>7373</td><td>12637</td><td>1185</td><td>12706</td><td>26859</td></tr>
    <tr><td>Nobis Merideth Parka</td><td>Nobis</td><td>Outerwear & Coats</td><td>795.0</td><td>382.39</td><td>2385.0</td><td>1237.82</td><td>7</td><td>3</td><td>1</td><td>1</td><td>2</td><td>1590.0</td><td>825.21</td><td>0.519</td><td>0.25</td><td>0.5</td><td>0.1429</td><td>0.4</td><td>0.0008835</td><td>0.0008847</td><td>3.86e-05</td><td>33</td><td>23</td><td>10</td><td>12</td><td>8625</td><td>2358</td><td>3978</td><td>7029</td><td>17069</td><td>37</td><td>45</td><td>10485</td><td>11344</td><td>3269</td><td>12706</td><td>23875</td></tr>
    <tr><td>Canada Goose Women's Expedition Parka</td><td>Canada Goose</td><td>Outerwear & Coats</td><td>795.0</td><td>395.91</td><td>2385.0</td><td>1197.27</td><td>4</td><td>3</td><td>0</td><td>1</td><td>0</td><td>795.0</td><td>399.09</td><td>0.502</td><td>0.0</td><td>1.0</td><td>0.25</td><td>0.0</td><td>0.0008835</td><td>0.0008557</td><td>2.21e-05</td><td>33</td><td>19</td><td>10</td><td>13</td><td>21053</td><td>2358</td><td>13463</td><td>7029</td><td>27145</td><td>230</td><td>277</td><td>12357</td><td>13463</td><td>1</td><td>5542</td><td>27145</td></tr>
    <tr><td>Men's Classic Sheepskin B-3 Bomber Jacket</td><td>Overland Sheepskin Co</td><td>Outerwear & Coats</td><td>595.0</td><td>270.73</td><td>2380.0</td><td>1297.1</td><td>13</td><td>4</td><td>0</td><td>2</td><td>7</td><td>1190.0</td><td>648.55</td><td>0.545</td><td>0.0</td><td>0.3636</td><td>0.1538</td><td>0.6364</td><td>0.0008816</td><td>0.000927</td><td>7.17e-05</td><td>60</td><td>55</td><td>12</td><td>11</td><td>423</td><td>776</td><td>13463</td><td>2100</td><td>623</td><td>95</td><td>94</td><td>8121</td><td>13463</td><td>9638</td><td>12634</td><td>16487</td></tr>
    <tr><td>Michael Kors Men's Marlow Wool-Blend Single-Breasted Fitted Top Coat</td><td>Michael Kors</td><td>Outerwear & Coats</td><td>255.0</td><td>102.26</td><td>2295.0</td><td>1374.7</td><td>15</td><td>9</td><td>1</td><td>2</td><td>3</td><td>765.0</td><td>458.23</td><td>0.599</td><td>0.1</td><td>0.6923</td><td>0.1333</td><td>0.25</td><td>0.0008502</td><td>0.0009825</td><td>8.27e-05</td><td>469</td><td>728</td><td>13</td><td>8</td><td>187</td><td>5</td><td>3978</td><td>2100</td><td>10869</td><td>252</td><td>208</td><td>2612</td><td>13461</td><td>1184</td><td>14317</td><td>26348</td></tr>
    <tr><td>Barbour Sapper Jacket</td><td>Barbour</td><td>Outerwear & Coats</td><td>429.0</td><td>210.21</td><td>2145.0</td><td>1093.95</td><td>10</td><td>5</td><td>1</td><td>1</td><td>3</td><td>858.0</td><td>437.58</td><td>0.51</td><td>0.1667</td><td>0.5556</td><td>0.1</td><td>0.375</td><td>0.0007946</td><td>0.0007818</td><td>5.52e-05</td><td>94</td><td>81</td><td>14</td><td>18</td><td>1962</td><td>251</td><td>3978</td><td>7029</td><td>10869</td><td>185</td><td>233</td><td>11510</td><td>13196</td><td>3151</td><td>16366</td><td>24717</td></tr>
    <tr><td>Arc'teryx Moray Jacket - Women's</td><td>Arc'teryx</td><td>Outerwear & Coats</td><td>699.0</td><td>343.91</td><td>2097.0</td><td>1065.28</td><td>9</td><td>3</td><td>0</td><td>3</td><td>3</td><td>2097.0</td><td>1065.28</td><td>0.508</td><td>0.0</td><td>0.5</td><td>0.3333</td><td>0.5</td><td>0.0007768</td><td>0.0007613</td><td>4.96e-05</td><td>41</td><td>36</td><td>15</td><td>20</td><td>3355</td><td>2358</td><td>13463</td><td>526</td><td>10869</td><td>11</td><td>22</td><td>11720</td><td>13463</td><td>3269</td><td>2619</td><td>19501</td></tr>
  </tbody>
</table>

</div>

<h3>Top products by Profit Margin</h3>

<pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = 'Cancelled' THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN ('Shipped', 'Processing') THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
GROUP BY product_name, product_brand, product_category
),
second_layer AS (
SELECT
  *,
  ROUND((profit / NULLIF(revenue, 0)), 4) AS profit_margin,
  ROUND(units_returned / NULLIF(units_completed + units_returned, 0), 4) AS return_rate,
  ROUND(units_completed / NULLIF(unit_orders_placed - units_cancelled, 0), 4) AS completion_rate,
  ROUND(units_cancelled / NULLIF(unit_orders_placed, 0), 4) AS cancellation_rate,
  ROUND(units_en_route / NULLIF(unit_orders_placed - (units_cancelled + units_returned), 0), 4) AS en_route_rate,
  ROUND(revenue / SUM(revenue) OVER(), 7) AS revenue_share,
  ROUND(profit / SUM(profit) OVER(), 7) AS profit_share,
  ROUND(unit_orders_placed / SUM(unit_orders_placed) OVER(), 7) AS unit_orders_placed_share
FROM first_layer
)
SELECT
  *,
  RANK() OVER(ORDER BY avg_product_sale_price DESC) AS avg_product_sale_price_rank,
  RANK() OVER(ORDER BY avg_product_cost DESC) AS avg_product_cost_rank,
  RANK() OVER(ORDER BY revenue DESC) AS revenue_rank,
  RANK() OVER(ORDER BY profit DESC) AS profit_rank,
  RANK() OVER(ORDER BY unit_orders_placed DESC) AS unit_orders_placed_rank,
  RANK() OVER(ORDER BY units_completed DESC) AS units_completed_rank,
  RANK() OVER(ORDER BY units_returned DESC) AS units_returned_rank,
  RANK() OVER(ORDER BY units_cancelled DESC) AS units_cancelled_rank,
  RANK() OVER(ORDER BY units_en_route DESC) AS units_en_route_rank,
  RANK() OVER(ORDER BY lost_revenue DESC) AS lost_revenue_rank,
  RANK() OVER(ORDER BY lost_profit DESC) AS lost_profit_rank,
  RANK() OVER(ORDER BY profit_margin DESC) AS profit_margin_rank,
  RANK() OVER(ORDER BY return_rate DESC) AS return_rate_rank,
  RANK() OVER(ORDER BY completion_rate DESC) AS completion_rate_rank,
  RANK() OVER(ORDER BY cancellation_rate DESC) AS cancellation_rate_rank,
  RANK() OVER(ORDER BY en_route_rate DESC) AS en_route_rate_rank
FROM second_layer
ORDER BY
  profit_margin_rank ASC
LIMIT 15;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>product_name</th>
      <th>product_brand</th>
      <th>product_category</th>
      <th>avg_product_sale_price</th>
      <th>avg_product_cost</th>
      <th>revenue</th>
      <th>profit</th>
      <th>unit_orders_placed</th>
      <th>units_completed</th>
      <th>units_returned</th>
      <th>units_cancelled</th>
      <th>units_en_route</th>
      <th>lost_revenue</th>
      <th>lost_profit</th>
      <th>profit_margin</th>
      <th>return_rate</th>
      <th>completion_rate</th>
      <th>cancellation_rate</th>
      <th>en_route_rate</th>
      <th>revenue_share</th>
      <th>profit_share</th>
      <th>unit_orders_placed_share</th>
      <th>avg_product_sale_price_rank</th>
      <th>avg_product_cost_rank</th>
      <th>revenue_rank</th>
      <th>profit_rank</th>
      <th>unit_orders_placed_rank</th>
      <th>units_completed_rank</th>
      <th>units_returned_rank</th>
      <th>units_cancelled_rank</th>
      <th>units_en_route_rank</th>
      <th>lost_revenue_rank</th>
      <th>lost_profit_rank</th>
      <th>profit_margin_rank</th>
      <th>return_rate_rank</th>
      <th>completion_rate_rank</th>
      <th>cancellation_rate_rank</th>
      <th>en_route_rate_rank</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Plus Size Black Jazzy Jacket</td><td>Fashion Love</td><td>Blazers & Jackets</td><td>34.99</td><td>11.58</td><td>104.97</td><td>70.22</td><td>5</td><td>3</td><td>0</td><td>1</td><td>1</td><td>34.99</td><td>23.41</td><td>0.669</td><td>0.0</td><td>0.75</td><td>0.2</td><td>0.25</td><td>3.89e-05</td><td>5.02e-05</td><td>2.76e-05</td><td>15963</td><td>20949</td><td>7698</td><td>5726</td><td>16887</td><td>2358</td><td>13463</td><td>7029</td><td>23197</td><td>17236</td><td>14884</td><td>1</td><td>13463</td><td>746</td><td>8435</td><td>26348</td></tr>
    <tr><td>Ulla Popken Plus Size Soutache Embroidered Jacket</td><td>Ulla Popken</td><td>Blazers & Jackets</td><td>89.0</td><td>29.46</td><td>178.0</td><td>119.08</td><td>7</td><td>2</td><td>1</td><td>0</td><td>4</td><td>89.0</td><td>59.54</td><td>0.669</td><td>0.3333</td><td>0.2857</td><td>0.0</td><td>0.6667</td><td>6.59e-05</td><td>8.51e-05</td><td>3.86e-05</td><td>4994</td><td>8857</td><td>4102</td><td>2773</td><td>8625</td><td>6114</td><td>3978</td><td>17458</td><td>6105</td><td>9306</td><td>6919</td><td>1</td><td>8752</td><td>13238</td><td>17458</td><td>12990</td></tr>
    <tr><td>Ted Baker Women's Mowna</td><td>Ted Baker</td><td>Blazers & Jackets</td><td>206.96</td><td>68.5</td><td>206.96</td><td>138.46</td><td>7</td><td>1</td><td>1</td><td>1</td><td>4</td><td>413.92</td><td>276.91</td><td>0.669</td><td>0.5</td><td>0.1667</td><td>0.1429</td><td>0.8</td><td>7.67e-05</td><td>9.9e-05</td><td>3.86e-05</td><td>771</td><td>2149</td><td>3223</td><td>2200</td><td>8625</td><td>13264</td><td>3978</td><td>7029</td><td>6105</td><td>925</td><td>621</td><td>1</td><td>4275</td><td>19436</td><td>12706</td><td>7598</td></tr>
    <tr><td>Eddie Bauer Signature Stretch Blazer</td><td>Eddie Bauer</td><td>Blazers & Jackets</td><td>149.95</td><td>49.63</td><td>299.9</td><td>200.63</td><td>9</td><td>2</td><td>0</td><td>2</td><td>5</td><td>299.9</td><td>200.63</td><td>0.669</td><td>0.0</td><td>0.2857</td><td>0.2222</td><td>0.7143</td><td>0.0001111</td><td>0.0001434</td><td>4.96e-05</td><td>1956</td><td>3876</td><td>1775</td><td>1137</td><td>3355</td><td>6114</td><td>13463</td><td>2100</td><td>3026</td><td>1734</td><td>1126</td><td>1</td><td>13463</td><td>13238</td><td>7837</td><td>12035</td></tr>
    <tr><td>DKNYC Women's 2 Button Blazer</td><td>DKNYC</td><td>Blazers & Jackets</td><td>99.09</td><td>32.8</td><td>198.18</td><td>132.58</td><td>6</td><td>2</td><td>2</td><td>0</td><td>2</td><td>198.18</td><td>132.58</td><td>0.669</td><td>0.5</td><td>0.3333</td><td>0.0</td><td>0.5</td><td>7.34e-05</td><td>9.48e-05</td><td>3.31e-05</td><td>4110</td><td>7591</td><td>3450</td><td>2363</td><td>12532</td><td>6114</td><td>844</td><td>17458</td><td>17069</td><td>3375</td><td>2320</td><td>1</td><td>4275</td><td>9747</td><td>17458</td><td>19501</td></tr>
    <tr><td>Allegra K Front Opening Long Sleeve Womenwear Form-fitting Blazer Off White XS</td><td>Allegra K</td><td>Blazers & Jackets</td><td>18.68</td><td>6.18</td><td>37.36</td><td>24.99</td><td>6</td><td>2</td><td>0</td><td>1</td><td>3</td><td>18.68</td><td>12.5</td><td>0.6689</td><td>0.0</td><td>0.4</td><td>0.1667</td><td>0.6</td><td>1.38e-05</td><td>1.79e-05</td><td>3.31e-05</td><td>23425</td><td>25885</td><td>16627</td><td>14250</td><td>12532</td><td>6114</td><td>13463</td><td>7029</td><td>10869</td><td>20771</td><td>19355</td><td>6</td><td>13463</td><td>7482</td><td>10731</td><td>16953</td></tr>
    <tr><td>Allegra K Women Horizontal Stripes Bubble Sleeve Spring Coat Black XS</td><td>Allegra K</td><td>Blazers & Jackets</td><td>11.67</td><td>3.86</td><td>23.34</td><td>15.61</td><td>10</td><td>2</td><td>1</td><td>0</td><td>7</td><td>11.67</td><td>7.81</td><td>0.6688</td><td>0.3333</td><td>0.2</td><td>0.0</td><td>0.7778</td><td>8.6e-06</td><td>1.12e-05</td><td>5.52e-05</td><td>26523</td><td>27736</td><td>19737</td><td>17784</td><td>1962</td><td>6114</td><td>3978</td><td>17458</td><td>623</td><td>21976</td><td>21271</td><td>7</td><td>8752</td><td>17510</td><td>17458</td><td>9281</td></tr>
    <tr><td>BB Dakota Yellow Marigold Naples Boxy Cropped Blazer Button up Front and Double Pockets</td><td>BB Dakota</td><td>Blazers & Jackets</td><td>77.0</td><td>25.56</td><td>77.0</td><td>51.44</td><td>6</td><td>1</td><td>0</td><td>2</td><td>3</td><td>154.0</td><td>102.87</td><td>0.6681</td><td>0.0</td><td>0.25</td><td>0.3333</td><td>0.75</td><td>2.85e-05</td><td>3.68e-05</td><td>3.31e-05</td><td>6222</td><td>10673</td><td>10392</td><td>8077</td><td>12532</td><td>13264</td><td>13463</td><td>2100</td><td>10869</td><td>4944</td><td>3344</td><td>8</td><td>13463</td><td>14408</td><td>2619</td><td>9487</td></tr>
    <tr><td>Mango Women's Suit Cropped Blazer - Chipi</td><td>MANGO</td><td>Blazers & Jackets</td><td>49.99</td><td>16.6</td><td>99.98</td><td>66.79</td><td>4</td><td>2</td><td>1</td><td>0</td><td>1</td><td>49.99</td><td>33.39</td><td>0.668</td><td>0.3333</td><td>0.5</td><td>0.0</td><td>0.3333</td><td>3.7e-05</td><td>4.77e-05</td><td>2.21e-05</td><td>10894</td><td>16411</td><td>8109</td><td>6088</td><td>21053</td><td>6114</td><td>3978</td><td>17458</td><td>23197</td><td>14347</td><td>11779</td><td>9</td><td>8752</td><td>3269</td><td>17458</td><td>24854</td></tr>
    <tr><td>Calvin Klein Jeans Women's Moto Jacket</td><td>Calvin Klein Jeans</td><td>Blazers & Jackets</td><td>56.39</td><td>18.72</td><td>56.39</td><td>37.67</td><td>5</td><td>1</td><td>1</td><td>0</td><td>3</td><td>56.39</td><td>37.67</td><td>0.668</td><td>0.5</td><td>0.2</td><td>0.0</td><td>0.75</td><td>2.09e-05</td><td>2.69e-05</td><td>2.76e-05</td><td>9503</td><td>14790</td><td>13133</td><td>10707</td><td>16887</td><td>13264</td><td>3978</td><td>17458</td><td>10869</td><td>13238</td><td>10778</td><td>9</td><td>4275</td><td>17510</td><td>17458</td><td>9487</td></tr>
    <tr><td>Allegra K Women Double Breasted Long Sleeve Autumn Blazer Coat Army Green XS</td><td>Allegra K</td><td>Blazers & Jackets</td><td>16.05</td><td>5.33</td><td>32.1</td><td>21.44</td><td>4</td><td>2</td><td>0</td><td>1</td><td>1</td><td>16.05</td><td>10.72</td><td>0.6679</td><td>0.0</td><td>0.6667</td><td>0.25</td><td>0.3333</td><td>1.19e-05</td><td>1.53e-05</td><td>2.21e-05</td><td>24296</td><td>26673</td><td>17542</td><td>15499</td><td>21053</td><td>6114</td><td>13463</td><td>7029</td><td>23197</td><td>21164</td><td>20129</td><td>11</td><td>13463</td><td>1185</td><td>5542</td><td>24854</td></tr>
    <tr><td>Pendleton Women's Trimmed Herringbone Blazer</td><td>Pendleton</td><td>Blazers & Jackets</td><td>258.0</td><td>85.91</td><td>516.0</td><td>344.17</td><td>6</td><td>2</td><td>1</td><td>2</td><td>1</td><td>774.0</td><td>516.26</td><td>0.667</td><td>0.3333</td><td>0.5</td><td>0.3333</td><td>0.3333</td><td>0.0001911</td><td>0.000246</td><td>3.31e-05</td><td>462</td><td>1282</td><td>594</td><td>364</td><td>12532</td><td>6114</td><td>3978</td><td>2100</td><td>23197</td><td>251</td><td>153</td><td>12</td><td>8752</td><td>3269</td><td>2619</td><td>24854</td></tr>
    <tr><td>Corey Lynn Calter Women's Jessica Jacket</td><td>CoreyLynnCalter</td><td>Blazers & Jackets</td><td>79.0</td><td>26.31</td><td>79.0</td><td>52.69</td><td>3</td><td>1</td><td>0</td><td>1</td><td>1</td><td>79.0</td><td>52.69</td><td>0.667</td><td>0.0</td><td>0.5</td><td>0.3333</td><td>0.5</td><td>2.93e-05</td><td>3.77e-05</td><td>1.65e-05</td><td>5951</td><td>10284</td><td>10194</td><td>7889</td><td>24645</td><td>13264</td><td>13463</td><td>7029</td><td>23197</td><td>10287</td><td>7953</td><td>12</td><td>13463</td><td>3269</td><td>2619</td><td>19501</td></tr>
    <tr><td>Only Hearts Women's Double Knit 2 Button Jacket</td><td>Only Hearts</td><td>Blazers & Jackets</td><td>185.0</td><td>61.61</td><td>1110.0</td><td>740.37</td><td>11</td><td>6</td><td>0</td><td>0</td><td>5</td><td>0.0</td><td>0.0</td><td>0.667</td><td>0.0</td><td>0.5455</td><td>0.0</td><td>0.4545</td><td>0.0004112</td><td>0.0005291</td><td>6.07e-05</td><td>1114</td><td>2672</td><td>94</td><td>56</td><td>1161</td><td>84</td><td>13463</td><td>17458</td><td>3026</td><td>22642</td><td>22642</td><td>12</td><td>13463</td><td>3246</td><td>17458</td><td>23452</td></tr>
    <tr><td>Plus Size White Night Sky Top</td><td>Alex Evenings</td><td>Blazers & Jackets</td><td>124.99</td><td>41.62</td><td>124.99</td><td>83.37</td><td>4</td><td>1</td><td>2</td><td>0</td><td>1</td><td>249.98</td><td>166.74</td><td>0.667</td><td>0.6667</td><td>0.25</td><td>0.0</td><td>0.5</td><td>4.63e-05</td><td>5.96e-05</td><td>2.21e-05</td><td>2939</td><td>5153</td><td>6403</td><td>4593</td><td>21053</td><td>13264</td><td>844</td><td>17458</td><td>23197</td><td>2385</td><td>1545</td><td>12</td><td>3055</td><td>14408</td><td>17458</td><td>19501</td></tr>
  </tbody>
</table>

</div>

<h3>Top products by Lost Revenue</h3>

<pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = 'Cancelled' THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN ('Shipped', 'Processing') THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
GROUP BY product_name, product_brand, product_category
),
second_layer AS (
SELECT
  *,
  ROUND((profit / NULLIF(revenue, 0)), 4) AS profit_margin,
  ROUND(units_returned / NULLIF(units_completed + units_returned, 0), 4) AS return_rate,
  ROUND(units_completed / NULLIF(unit_orders_placed - units_cancelled, 0), 4) AS completion_rate,
  ROUND(units_cancelled / NULLIF(unit_orders_placed, 0), 4) AS cancellation_rate,
  ROUND(units_en_route / NULLIF(unit_orders_placed - (units_cancelled + units_returned), 0), 4) AS en_route_rate,
  ROUND(revenue / SUM(revenue) OVER(), 7) AS revenue_share,
  ROUND(profit / SUM(profit) OVER(), 7) AS profit_share,
  ROUND(unit_orders_placed / SUM(unit_orders_placed) OVER(), 7) AS unit_orders_placed_share
FROM first_layer
)
SELECT
  *,
  RANK() OVER(ORDER BY avg_product_sale_price DESC) AS avg_product_sale_price_rank,
  RANK() OVER(ORDER BY avg_product_cost DESC) AS avg_product_cost_rank,
  RANK() OVER(ORDER BY revenue DESC) AS revenue_rank,
  RANK() OVER(ORDER BY profit DESC) AS profit_rank,
  RANK() OVER(ORDER BY unit_orders_placed DESC) AS unit_orders_placed_rank,
  RANK() OVER(ORDER BY units_completed DESC) AS units_completed_rank,
  RANK() OVER(ORDER BY units_returned DESC) AS units_returned_rank,
  RANK() OVER(ORDER BY units_cancelled DESC) AS units_cancelled_rank,
  RANK() OVER(ORDER BY units_en_route DESC) AS units_en_route_rank,
  RANK() OVER(ORDER BY lost_revenue DESC) AS lost_revenue_rank,
  RANK() OVER(ORDER BY lost_profit DESC) AS lost_profit_rank,
  RANK() OVER(ORDER BY profit_margin DESC) AS profit_margin_rank,
  RANK() OVER(ORDER BY return_rate DESC) AS return_rate_rank,
  RANK() OVER(ORDER BY completion_rate DESC) AS completion_rate_rank,
  RANK() OVER(ORDER BY cancellation_rate DESC) AS cancellation_rate_rank,
  RANK() OVER(ORDER BY en_route_rate DESC) AS en_route_rate_rank
FROM second_layer
ORDER BY
  lost_revenue_rank ASC
LIMIT 15;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>product_name</th>
      <th>product_brand</th>
      <th>product_category</th>
      <th>avg_product_sale_price</th>
      <th>avg_product_cost</th>
      <th>revenue</th>
      <th>profit</th>
      <th>unit_orders_placed</th>
      <th>units_completed</th>
      <th>units_returned</th>
      <th>units_cancelled</th>
      <th>units_en_route</th>
      <th>lost_revenue</th>
      <th>lost_profit</th>
      <th>profit_margin</th>
      <th>return_rate</th>
      <th>completion_rate</th>
      <th>cancellation_rate</th>
      <th>en_route_rate</th>
      <th>revenue_share</th>
      <th>profit_share</th>
      <th>unit_orders_placed_share</th>
      <th>avg_product_sale_price_rank</th>
      <th>avg_product_cost_rank</th>
      <th>revenue_rank</th>
      <th>profit_rank</th>
      <th>unit_orders_placed_rank</th>
      <th>units_completed_rank</th>
      <th>units_returned_rank</th>
      <th>units_cancelled_rank</th>
      <th>units_en_route_rank</th>
      <th>lost_revenue_rank</th>
      <th>lost_profit_rank</th>
      <th>profit_margin_rank</th>
      <th>return_rate_rank</th>
      <th>completion_rate_rank</th>
      <th>cancellation_rate_rank</th>
      <th>en_route_rate_rank</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Canada Goose Men's The Chateau Jacket</td><td>Canada Goose</td><td>Active</td><td>815.0</td><td>337.41</td><td>0.0</td><td>0.0</td><td>6</td><td>0</td><td>1</td><td>4</td><td>1</td><td>4075.0</td><td>2387.95</td><td></td><td>1.0</td><td>0.0</td><td>0.6667</td><td>1.0</td><td>0.0</td><td>0.0</td><td>3.31e-05</td><td>31</td><td>39</td><td>22532</td><td>22532</td><td>12532</td><td>22532</td><td>3978</td><td>126</td><td>23197</td><td>1</td><td>1</td><td>22532</td><td>1</td><td>22532</td><td>154</td><td>1</td></tr>
    <tr><td>The North Face Denali Down Mens Jacket 2013</td><td>The North Face</td><td>Outerwear & Coats</td><td>903.0</td><td>436.15</td><td>2709.0</td><td>1400.55</td><td>13</td><td>3</td><td>2</td><td>2</td><td>6</td><td>3612.0</td><td>1867.4</td><td>0.517</td><td>0.4</td><td>0.2727</td><td>0.1538</td><td>0.6667</td><td>0.0010035</td><td>0.001001</td><td>7.17e-05</td><td>5</td><td>10</td><td>7</td><td>7</td><td>423</td><td>2358</td><td>844</td><td>2100</td><td>1398</td><td>2</td><td>3</td><td>10735</td><td>8312</td><td>14284</td><td>12634</td><td>12990</td></tr>
    <tr><td>Canada Goose Women's Chilliwack Bomber</td><td>Canada Goose</td><td>Outerwear & Coats</td><td>695.0</td><td>287.73</td><td>695.0</td><td>407.27</td><td>8</td><td>1</td><td>3</td><td>2</td><td>2</td><td>3475.0</td><td>2036.35</td><td>0.586</td><td>0.75</td><td>0.1667</td><td>0.25</td><td>0.6667</td><td>0.0002575</td><td>0.0002911</td><td>4.41e-05</td><td>46</td><td>52</td><td>294</td><td>240</td><td>5507</td><td>13264</td><td>151</td><td>2100</td><td>17069</td><td>3</td><td>2</td><td>3719</td><td>2834</td><td>19436</td><td>5542</td><td>12990</td></tr>
    <tr><td>Woolrich Arctic Parka DF</td><td>Woolrich</td><td>Outerwear & Coats</td><td>990.0</td><td>478.17</td><td>2970.0</td><td>1535.49</td><td>12</td><td>3</td><td>2</td><td>1</td><td>6</td><td>2970.0</td><td>1535.49</td><td>0.517</td><td>0.4</td><td>0.2727</td><td>0.0833</td><td>0.6667</td><td>0.0011002</td><td>0.0010974</td><td>6.62e-05</td><td>3</td><td>6</td><td>5</td><td>6</td><td>694</td><td>2358</td><td>844</td><td>7029</td><td>1398</td><td>4</td><td>4</td><td>10735</td><td>8312</td><td>14284</td><td>17144</td><td>12990</td></tr>
    <tr><td>Mens Nike AirJordan Varsity Hoodie Jacket Grey / Black 451582-066</td><td>Jordan</td><td>Outerwear & Coats</td><td>903.0</td><td>409.06</td><td>903.0</td><td>493.94</td><td>8</td><td>1</td><td>2</td><td>1</td><td>4</td><td>2709.0</td><td>1481.82</td><td>0.547</td><td>0.6667</td><td>0.1429</td><td>0.125</td><td>0.8</td><td>0.0003345</td><td>0.000353</td><td>4.41e-05</td><td>5</td><td>14</td><td>149</td><td>153</td><td>5507</td><td>13264</td><td>844</td><td>7029</td><td>6105</td><td>5</td><td>6</td><td>7915</td><td>3055</td><td>20815</td><td>14338</td><td>7598</td></tr>
    <tr><td>NIKE WOMEN'S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort*</td><td>Nike</td><td>Intimates</td><td>903.0</td><td>512.0</td><td>0.0</td><td>0.0</td><td>4</td><td>0</td><td>0</td><td>3</td><td>1</td><td>2709.0</td><td>1173.0</td><td></td><td></td><td>0.0</td><td>0.75</td><td>1.0</td><td>0.0</td><td>0.0</td><td>2.21e-05</td><td>5</td><td>4</td><td>22532</td><td>22532</td><td>21053</td><td>22532</td><td>13463</td><td>526</td><td>23197</td><td>5</td><td>15</td><td>22532</td><td>25326</td><td>22532</td><td>109</td><td>1</td></tr>
    <tr><td>Spyder Women's Jesst In Time Jacket</td><td>Spyder</td><td>Outerwear & Coats</td><td>650.0</td><td>295.75</td><td>3250.0</td><td>1771.25</td><td>10</td><td>5</td><td>4</td><td>0</td><td>1</td><td>2600.0</td><td>1417.0</td><td>0.545</td><td>0.4444</td><td>0.5</td><td>0.0</td><td>0.1667</td><td>0.0012039</td><td>0.0012659</td><td>5.52e-05</td><td>52</td><td>50</td><td>3</td><td>4</td><td>1962</td><td>251</td><td>30</td><td>17458</td><td>23197</td><td>7</td><td>7</td><td>8121</td><td>8264</td><td>3269</td><td>17458</td><td>27059</td></tr>
    <tr><td>IGIGI by Yuliya Raquel Plus Size Kandinsky Gown</td><td>IGIGI by Yuliya Raquel</td><td>Dresses</td><td>325.0</td><td>136.17</td><td>0.0</td><td>0.0</td><td>13</td><td>0</td><td>3</td><td>5</td><td>5</td><td>2600.0</td><td>1510.6</td><td></td><td>1.0</td><td>0.0</td><td>0.3846</td><td>1.0</td><td>0.0</td><td>0.0</td><td>7.17e-05</td><td>236</td><td>300</td><td>22532</td><td>22532</td><td>423</td><td>22532</td><td>151</td><td>24</td><td>3026</td><td>7</td><td>5</td><td>22532</td><td>1</td><td>22532</td><td>2333</td><td>1</td></tr>
    <tr><td>Canada Goose Women's Mystique</td><td>Canada Goose</td><td>Active</td><td>750.0</td><td>280.5</td><td>750.0</td><td>469.5</td><td>9</td><td>1</td><td>1</td><td>2</td><td>5</td><td>2250.0</td><td>1408.5</td><td>0.626</td><td>0.5</td><td>0.1429</td><td>0.2222</td><td>0.8333</td><td>0.0002778</td><td>0.0003355</td><td>4.96e-05</td><td>37</td><td>53</td><td>230</td><td>170</td><td>3355</td><td>13264</td><td>3978</td><td>2100</td><td>3026</td><td>9</td><td>8</td><td>984</td><td>4275</td><td>20815</td><td>7837</td><td>6580</td></tr>
    <tr><td>Canada Goose Women's Mystique</td><td>Canada Goose</td><td>Outerwear & Coats</td><td>750.0</td><td>353.25</td><td>1500.0</td><td>793.5</td><td>6</td><td>2</td><td>3</td><td>0</td><td>1</td><td>2250.0</td><td>1190.25</td><td>0.529</td><td>0.6</td><td>0.3333</td><td>0.0</td><td>0.3333</td><td>0.0005557</td><td>0.0005671</td><td>3.31e-05</td><td>37</td><td>35</td><td>41</td><td>44</td><td>12532</td><td>6114</td><td>151</td><td>17458</td><td>23197</td><td>9</td><td>13</td><td>9645</td><td>4103</td><td>9747</td><td>17458</td><td>24854</td></tr>
    <tr><td>Arc'teryx Moray Jacket - Women's</td><td>Arc'teryx</td><td>Outerwear & Coats</td><td>699.0</td><td>343.91</td><td>2097.0</td><td>1065.28</td><td>9</td><td>3</td><td>0</td><td>3</td><td>3</td><td>2097.0</td><td>1065.28</td><td>0.508</td><td>0.0</td><td>0.5</td><td>0.3333</td><td>0.5</td><td>0.0007768</td><td>0.0007613</td><td>4.96e-05</td><td>41</td><td>36</td><td>15</td><td>20</td><td>3355</td><td>2358</td><td>13463</td><td>526</td><td>10869</td><td>11</td><td>22</td><td>11720</td><td>13463</td><td>3269</td><td>2619</td><td>19501</td></tr>
    <tr><td>Magaschoni Women's Shimmer Jacket</td><td>Magaschoni</td><td>Blazers & Jackets</td><td>698.0</td><td>258.96</td><td>698.0</td><td>439.04</td><td>6</td><td>1</td><td>1</td><td>2</td><td>2</td><td>2094.0</td><td>1317.13</td><td>0.629</td><td>0.5</td><td>0.25</td><td>0.3333</td><td>0.6667</td><td>0.0002586</td><td>0.0003138</td><td>3.31e-05</td><td>43</td><td>58</td><td>288</td><td>201</td><td>12532</td><td>13264</td><td>3978</td><td>2100</td><td>17069</td><td>12</td><td>9</td><td>839</td><td>4275</td><td>14408</td><td>2619</td><td>12990</td></tr>
    <tr><td>Joseph Abboud Men's Super 120's Two Button Side Vent Single Pleat Pant Tuxedo With Grosgrain Notch Lapel</td><td>Joseph Abboud</td><td>Suits & Sport Coats</td><td>405.26</td><td>145.08</td><td>405.26</td><td>260.18</td><td>11</td><td>1</td><td>2</td><td>3</td><td>5</td><td>2026.3</td><td>1300.88</td><td>0.642</td><td>0.6667</td><td>0.125</td><td>0.2727</td><td>0.8333</td><td>0.0001501</td><td>0.0001859</td><td>6.07e-05</td><td>108</td><td>256</td><td>961</td><td>686</td><td>1161</td><td>13264</td><td>844</td><td>526</td><td>3026</td><td>13</td><td>10</td><td>361</td><td>3055</td><td>21675</td><td>5408</td><td>6580</td></tr>
    <tr><td>Darla</td><td>Alpha Industries</td><td>Outerwear & Coats</td><td>999.0</td><td>404.6</td><td>1998.0</td><td>1188.81</td><td>7</td><td>2</td><td>2</td><td>0</td><td>3</td><td>1998.0</td><td>1188.81</td><td>0.595</td><td>0.5</td><td>0.2857</td><td>0.0</td><td>0.6</td><td>0.0007401</td><td>0.0008496</td><td>3.86e-05</td><td>1</td><td>16</td><td>18</td><td>15</td><td>8625</td><td>6114</td><td>844</td><td>17458</td><td>10869</td><td>14</td><td>14</td><td>2925</td><td>4275</td><td>13238</td><td>17458</td><td>16953</td></tr>
    <tr><td>Alpha Industries Rip Stop Short</td><td>Alpha Industries</td><td>Shorts</td><td>999.0</td><td>482.52</td><td>999.0</td><td>516.48</td><td>8</td><td>1</td><td>1</td><td>1</td><td>5</td><td>1998.0</td><td>1032.97</td><td>0.517</td><td>0.5</td><td>0.1429</td><td>0.125</td><td>0.8333</td><td>0.0003701</td><td>0.0003691</td><td>4.41e-05</td><td>1</td><td>5</td><td>120</td><td>134</td><td>5507</td><td>13264</td><td>3978</td><td>7029</td><td>3026</td><td>14</td><td>25</td><td>10735</td><td>4275</td><td>20815</td><td>14338</td><td>6580</td></tr>
  </tbody>
</table>

</div>

<h3>Analytical Insights & Business Recommendations</h3>
<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p>The top 15 products by revenue are overwhelmingly dominated by Outerwear & Coats (11 of 15), with premium brands like The North Face, Canada Goose, Woolrich, Spyder, and Arc'teryx. This category commands the highest average sale prices ($595–$999) and generates the most revenue per unit sold. The top revenue product, ASICS Cushion Low Socks, is anomalous – priced at $903 (likely a data entry error or premium bundle) but sitting in the Active category. It ranks #1 in both revenue and profit with $3,612 and $2,116.63 respectively. Joseph Abboud Men's Sport Coat stands out as a high-volume high-revenue outlier with 30 unit orders placed (rank #7 across all products) while also ranking #5 in profit. This combination of volume and margin makes it the strongest candidate for promotional investment among top products.</p>

<p>The highest profit margin products (~66.9%) are exclusively Blazers & Jackets from mid-range brands (Fashion Love, Ulla Popken, Ted Baker, Eddie Bauer, DKNYC). These have low costs relative to sale prices but individually small revenue contributions. Since these high-margin blazer products have small individual revenue footprints, promote them in cohorts – bundle or cross-sell multiple blazer/jacket items together to amplify the margin advantage across a group rather than relying on individual unit sales. For top revenue products that already have strong demand (like the Joseph Abboud Sport Coat at 60.6% margin), consider strategic price testing. With 30 orders placed and strong brand recognition, there may be room to incrementally increase price by 3–5% without meaningfully reducing demand, yielding significant net profit gains given the volume.</p>


<p>Several top products have alarming return/cancellation profiles. The Canada Goose Men's Chateau Jacket has $0 in completed revenue – 100% of its orders were returned or cancelled, yet it ranks #1 in lost revenue ($4,075) and lost profit ($2,387.95). This product is generating no value while consuming inventory space, shipping bandwidth, and processing resources. IGIGI Kandinsky Gown similarly has a 100% return rate with $0 revenue and $2,600 in lost revenue. Both products warrant immediate quality inspection and supplier communication. The Spyder Women's Jesst In Time Jacket has a 44.4% return rate but still ranks #3 in revenue ($3,250) and #4 in profit ($1,771.25), meaning the returns are masking what could be even stronger performance. Investigate root causes of returns – sizing issues, product description mismatches, or quality defects. Products with high return rates among the top earners (Woolrich Arctic Parka at 40%, North Face Denali Down at 40%) should be flagged for quality inspection. Their return-related losses ($2,970 and $3,612 respectively) nearly equal their actual revenue, meaning nearly half of all potential profit is evaporating.</p>



</div>

</details>
<details>
  <summary><strong>Bottom Products</strong></summary>

  <div style="margin-top: 12px;"></div>

<h3>Bottom products by Revenue</h3>

<pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = 'Cancelled' THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN ('Shipped', 'Processing') THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
GROUP BY product_name, product_brand, product_category
),
second_layer AS (
SELECT
  *,
  ROUND((profit / NULLIF(revenue, 0)), 4) AS profit_margin,
  ROUND(units_returned / NULLIF(units_completed + units_returned, 0), 4) AS return_rate,
  ROUND(units_completed / NULLIF(unit_orders_placed - units_cancelled, 0), 4) AS completion_rate,
  ROUND(units_cancelled / NULLIF(unit_orders_placed, 0), 4) AS cancellation_rate,
  ROUND(units_en_route / NULLIF(unit_orders_placed - (units_cancelled + units_returned), 0), 4) AS en_route_rate,
  ROUND(revenue / SUM(revenue) OVER(), 7) AS revenue_share,
  ROUND(profit / SUM(profit) OVER(), 7) AS profit_share,
  ROUND(unit_orders_placed / SUM(unit_orders_placed) OVER(), 7) AS unit_orders_placed_share
FROM first_layer
)
SELECT
  *,
  RANK() OVER(ORDER BY avg_product_sale_price DESC) AS avg_product_sale_price_rank,
  RANK() OVER(ORDER BY avg_product_cost DESC) AS avg_product_cost_rank,
  RANK() OVER(ORDER BY revenue DESC) AS revenue_rank,
  RANK() OVER(ORDER BY profit DESC) AS profit_rank,
  RANK() OVER(ORDER BY unit_orders_placed DESC) AS unit_orders_placed_rank,
  RANK() OVER(ORDER BY units_completed DESC) AS units_completed_rank,
  RANK() OVER(ORDER BY units_returned DESC) AS units_returned_rank,
  RANK() OVER(ORDER BY units_cancelled DESC) AS units_cancelled_rank,
  RANK() OVER(ORDER BY units_en_route DESC) AS units_en_route_rank,
  RANK() OVER(ORDER BY lost_revenue DESC) AS lost_revenue_rank,
  RANK() OVER(ORDER BY lost_profit DESC) AS lost_profit_rank,
  RANK() OVER(ORDER BY profit_margin DESC) AS profit_margin_rank,
  RANK() OVER(ORDER BY return_rate DESC) AS return_rate_rank,
  RANK() OVER(ORDER BY completion_rate DESC) AS completion_rate_rank,
  RANK() OVER(ORDER BY cancellation_rate DESC) AS cancellation_rate_rank,
  RANK() OVER(ORDER BY en_route_rate DESC) AS en_route_rate_rank
FROM second_layer
ORDER BY
  revenue_rank DESC
LIMIT 15;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>product_name</th>
      <th>product_brand</th>
      <th>product_category</th>
      <th>avg_product_sale_price</th>
      <th>avg_product_cost</th>
      <th>revenue</th>
      <th>profit</th>
      <th>unit_orders_placed</th>
      <th>units_completed</th>
      <th>units_returned</th>
      <th>units_cancelled</th>
      <th>units_en_route</th>
      <th>lost_revenue</th>
      <th>lost_profit</th>
      <th>profit_margin</th>
      <th>return_rate</th>
      <th>completion_rate</th>
      <th>cancellation_rate</th>
      <th>en_route_rate</th>
      <th>revenue_share</th>
      <th>profit_share</th>
      <th>unit_orders_placed_share</th>
      <th>avg_product_sale_price_rank</th>
      <th>avg_product_cost_rank</th>
      <th>revenue_rank</th>
      <th>profit_rank</th>
      <th>unit_orders_placed_rank</th>
      <th>units_completed_rank</th>
      <th>units_returned_rank</th>
      <th>units_cancelled_rank</th>
      <th>units_en_route_rank</th>
      <th>lost_revenue_rank</th>
      <th>lost_profit_rank</th>
      <th>profit_margin_rank</th>
      <th>return_rate_rank</th>
      <th>completion_rate_rank</th>
      <th>cancellation_rate_rank</th>
      <th>en_route_rate_rank</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Marc Ecko Cut & Sew Men's Pinstripe and Plaid Pieced Vest</td><td>Marc Ecko Cut & Sew</td><td>Suits & Sport Coats</td><td>47.43</td><td>17.83</td><td>0.0</td><td>0.0</td><td>10</td><td>0</td><td>0</td><td>3</td><td>7</td><td>142.29</td><td>88.79</td><td></td><td></td><td>0.0</td><td>0.3</td><td>1.0</td><td>0.0</td><td>0.0</td><td>5.52e-05</td><td>12005</td><td>15475</td><td>22532</td><td>22532</td><td>1962</td><td>22532</td><td>13463</td><td>526</td><td>623</td><td>5528</td><td>4189</td><td>22532</td><td>25326</td><td>22532</td><td>4443</td><td>1</td></tr>
    <tr><td>Dexter's Wings - Dexter T-shirt</td><td>Dexter</td><td>Tops & Tees</td><td>19.95</td><td>11.11</td><td>0.0</td><td>0.0</td><td>5</td><td>0</td><td>1</td><td>1</td><td>3</td><td>39.9</td><td>17.68</td><td></td><td>1.0</td><td>0.0</td><td>0.2</td><td>1.0</td><td>0.0</td><td>0.0</td><td>2.76e-05</td><td>23040</td><td>21439</td><td>22532</td><td>22532</td><td>16887</td><td>22532</td><td>3978</td><td>7029</td><td>10869</td><td>16370</td><td>17124</td><td>22532</td><td>1</td><td>22532</td><td>8435</td><td>1</td></tr>
    <tr><td>RSQ Miami Womens Jeggings</td><td>RSQ</td><td>Pants & Capris</td><td>39.99</td><td>22.07</td><td>0.0</td><td>0.0</td><td>4</td><td>0</td><td>1</td><td>1</td><td>2</td><td>79.98</td><td>35.83</td><td></td><td>1.0</td><td>0.0</td><td>0.25</td><td>1.0</td><td>0.0</td><td>0.0</td><td>2.21e-05</td><td>13925</td><td>12599</td><td>22532</td><td>22532</td><td>21053</td><td>22532</td><td>3978</td><td>7029</td><td>17069</td><td>10039</td><td>11208</td><td>22532</td><td>1</td><td>22532</td><td>5542</td><td>1</td></tr>
    <tr><td>Medela Sleep Bra Nude Large</td><td>Medela</td><td>Maternity</td><td>15.99</td><td>6.88</td><td>0.0</td><td>0.0</td><td>7</td><td>0</td><td>3</td><td>1</td><td>3</td><td>63.96</td><td>36.46</td><td></td><td>1.0</td><td>0.0</td><td>0.1429</td><td>1.0</td><td>0.0</td><td>0.0</td><td>3.86e-05</td><td>24393</td><td>25240</td><td>22532</td><td>22532</td><td>8625</td><td>22532</td><td>151</td><td>7029</td><td>10869</td><td>12226</td><td>11055</td><td>22532</td><td>1</td><td>22532</td><td>12706</td><td>1</td></tr>
    <tr><td>Diesel Women's Louvboot Slim Flare Jean</td><td>Diesel</td><td>Jeans</td><td>198.0</td><td>97.61</td><td>0.0</td><td>0.0</td><td>4</td><td>0</td><td>0</td><td>2</td><td>2</td><td>396.0</td><td>200.77</td><td></td><td></td><td>0.0</td><td>0.5</td><td>1.0</td><td>0.0</td><td>0.0</td><td>2.21e-05</td><td>875</td><td>836</td><td>22532</td><td>22532</td><td>21053</td><td>22532</td><td>13463</td><td>2100</td><td>17069</td><td>1005</td><td>1124</td><td>22532</td><td>25326</td><td>22532</td><td>477</td><td>1</td></tr>
    <tr><td>SockGuy Men's Wooligan Socks</td><td>SockGuy</td><td>Socks</td><td>12.95</td><td>7.33</td><td>0.0</td><td>0.0</td><td>4</td><td>0</td><td>0</td><td>2</td><td>2</td><td>25.9</td><td>11.24</td><td></td><td></td><td>0.0</td><td>0.5</td><td>1.0</td><td>0.0</td><td>0.0</td><td>2.21e-05</td><td>25924</td><td>24844</td><td>22532</td><td>22532</td><td>21053</td><td>22532</td><td>13463</td><td>2100</td><td>17069</td><td>19080</td><td>19933</td><td>22532</td><td>25326</td><td>22532</td><td>477</td><td>1</td></tr>
    <tr><td>Allegra K Mens Casual Vertical Stripes Pattern Decor NEW Stylish Short Trousers Deep Beige W31</td><td>Allegra K</td><td>Shorts</td><td>15.95</td><td>7.99</td><td>0.0</td><td>0.0</td><td>6</td><td>0</td><td>1</td><td>0</td><td>5</td><td>15.95</td><td>7.96</td><td></td><td>1.0</td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>3.31e-05</td><td>24488</td><td>24197</td><td>22532</td><td>22532</td><td>12532</td><td>22532</td><td>3978</td><td>17458</td><td>3026</td><td>21250</td><td>21221</td><td>22532</td><td>1</td><td>22532</td><td>17458</td><td>1</td></tr>
    <tr><td>Southpole Men's Angled Cross With Shadowed Background Print Fashion T-Shirt</td><td>Southpole</td><td>Tops & Tees</td><td>25.0</td><td>13.52</td><td>0.0</td><td>0.0</td><td>6</td><td>0</td><td>0</td><td>1</td><td>5</td><td>25.0</td><td>11.48</td><td></td><td></td><td>0.0</td><td>0.1667</td><td>1.0</td><td>0.0</td><td>0.0</td><td>3.31e-05</td><td>19651</td><td>19040</td><td>22532</td><td>22532</td><td>12532</td><td>22532</td><td>13463</td><td>7029</td><td>3026</td><td>19164</td><td>19837</td><td>22532</td><td>25326</td><td>22532</td><td>10731</td><td>1</td></tr>
    <tr><td>Brushed-Back Satin Pajamas - Women's Sizes</td><td>Carol Wright Gifts</td><td>Sleep & Lounge</td><td>24.99</td><td>15.07</td><td>0.0</td><td>0.0</td><td>3</td><td>0</td><td>1</td><td>0</td><td>2</td><td>24.99</td><td>9.92</td><td></td><td>1.0</td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>1.65e-05</td><td>20698</td><td>17708</td><td>22532</td><td>22532</td><td>24645</td><td>22532</td><td>3978</td><td>17458</td><td>17069</td><td>19500</td><td>20477</td><td>22532</td><td>1</td><td>22532</td><td>17458</td><td>1</td></tr>
    <tr><td>Tommy Hilfiger Men's Tommy Tartan Boxer</td><td>Tommy Hilfiger</td><td>Underwear</td><td>18.0</td><td>8.69</td><td>0.0</td><td>0.0</td><td>5</td><td>0</td><td>1</td><td>1</td><td>3</td><td>36.0</td><td>18.61</td><td></td><td>1.0</td><td>0.0</td><td>0.2</td><td>1.0</td><td>0.0</td><td>0.0</td><td>2.76e-05</td><td>23512</td><td>23579</td><td>22532</td><td>22532</td><td>16887</td><td>22532</td><td>3978</td><td>7029</td><td>10869</td><td>16903</td><td>16747</td><td>22532</td><td>1</td><td>22532</td><td>8435</td><td>1</td></tr>
    <tr><td>One Pair MarcolianiMen's Italian Cashmere and Silk Over-the-Calf Fancy Argyle Socks</td><td>Marcoliani Milano</td><td>Socks</td><td>89.5</td><td>49.58</td><td>0.0</td><td>0.0</td><td>2</td><td>0</td><td>1</td><td>0</td><td>1</td><td>89.5</td><td>39.92</td><td></td><td>1.0</td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>1.1e-05</td><td>4936</td><td>3880</td><td>22532</td><td>22532</td><td>26863</td><td>22532</td><td>3978</td><td>17458</td><td>23197</td><td>9283</td><td>10290</td><td>22532</td><td>1</td><td>22532</td><td>17458</td><td>1</td></tr>
    <tr><td>Allegra K Ladies Dotted Double V Neck Banded Dress Pink White M</td><td>Allegra K</td><td>Dresses</td><td>10.15</td><td>4.83</td><td>0.0</td><td>0.0</td><td>5</td><td>0</td><td>0</td><td>0</td><td>5</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>2.76e-05</td><td>26937</td><td>27097</td><td>22532</td><td>22532</td><td>16887</td><td>22532</td><td>13463</td><td>17458</td><td>3026</td><td>22642</td><td>22642</td><td>22532</td><td>25326</td><td>22532</td><td>17458</td><td>1</td></tr>
    <tr><td>7 For All Mankind Women's Relaxed Mid Roll Up Short Authentic Nakita</td><td>7 For All Mankind</td><td>Shorts</td><td>178.0</td><td>82.95</td><td>0.0</td><td>0.0</td><td>6</td><td>0</td><td>2</td><td>1</td><td>3</td><td>534.0</td><td>285.16</td><td></td><td>1.0</td><td>0.0</td><td>0.1667</td><td>1.0</td><td>0.0</td><td>0.0</td><td>3.31e-05</td><td>1246</td><td>1403</td><td>22532</td><td>22532</td><td>12532</td><td>22532</td><td>844</td><td>7029</td><td>10869</td><td>570</td><td>582</td><td>22532</td><td>1</td><td>22532</td><td>10731</td><td>1</td></tr>
    <tr><td>Fox Men's Essex Short</td><td>Fox</td><td>Shorts</td><td>42.5</td><td>19.51</td><td>0.0</td><td>0.0</td><td>3</td><td>0</td><td>0</td><td>1</td><td>2</td><td>42.5</td><td>22.99</td><td></td><td></td><td>0.0</td><td>0.3333</td><td>1.0</td><td>0.0</td><td>0.0</td><td>1.65e-05</td><td>13301</td><td>14268</td><td>22532</td><td>22532</td><td>24645</td><td>22532</td><td>13463</td><td>7029</td><td>17069</td><td>15731</td><td>15034</td><td>22532</td><td>25326</td><td>22532</td><td>2619</td><td>1</td></tr>
    <tr><td>Motherhood Maternity: Plus Size Secret Fit Belly(r) Boot Cut Maternity Jeans</td><td>Motherhood Maternity</td><td>Maternity</td><td>34.98</td><td>15.74</td><td>0.0</td><td>0.0</td><td>3</td><td>0</td><td>0</td><td>0</td><td>3</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>1.65e-05</td><td>16197</td><td>17160</td><td>22532</td><td>22532</td><td>24645</td><td>22532</td><td>13463</td><td>17458</td><td>10869</td><td>22642</td><td>22642</td><td>22532</td><td>25326</td><td>22532</td><td>17458</td><td>1</td></tr>
  </tbody>
</table>

</div>

<h3>Analytical Insights & Business Recommendations</h3>
<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p>The bottom 15 products by revenue all show $0 in completed revenue – every order for these items was either cancelled, returned, or is still in transit with no completions. Products like Marc Ecko Cut & Sew Pinstripe Vest (10 orders, $0 revenue), Diesel Women's Louvboot Slim Flare Jean (4 orders, $0 revenue), and Allegra K Dotted Dress (5 orders, $0 revenue) are occupying warehouse space and shipping bandwidth without generating any return. Many of these zero-revenue products still have units en route (shown by en_route_rate of 1.0), meaning they are actively consuming fulfillment resources. Others have high cancellation rates, suggesting customers are abandoning these purchases during checkout or processing.</p>

<p>Recommendation: These zero-revenue products should be evaluated for delisting. If a product has generated multiple orders but zero completions, the pattern indicates either a systemic quality issue, misleading product listings, or severe delivery problems. Flag all products with 3+ orders and $0 revenue for an immediate review, and consider removing them from active listings if the pattern persists, as they are wasting inventory space and shipping bandwidth that could serve profitable items.</p>











</div>

</details>
<details>
  <summary><strong>Top Brands</strong></summary>

  <div style="margin-top: 12px;"></div>

<h3>Top brands by Revenue</h3>

<pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.brand AS product_brand,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = 'Cancelled' THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN ('Shipped', 'Processing') THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
GROUP BY product_brand
),
second_layer AS (
SELECT
  *,
  ROUND((profit / NULLIF(revenue, 0)), 4) AS profit_margin,
  ROUND(units_returned / NULLIF(units_completed + units_returned, 0), 4) AS return_rate,
  ROUND(units_completed / NULLIF(unit_orders_placed - units_cancelled, 0), 4) AS completion_rate,
  ROUND(units_cancelled / NULLIF(unit_orders_placed, 0), 4) AS cancellation_rate,
  ROUND(units_en_route / NULLIF(unit_orders_placed - (units_cancelled + units_returned), 0), 4) AS en_route_rate,
  ROUND(revenue / SUM(revenue) OVER(), 7) AS revenue_share,
  ROUND(profit / SUM(profit) OVER(), 7) AS profit_share,
  ROUND(unit_orders_placed / SUM(unit_orders_placed) OVER(), 7) AS unit_orders_placed_share
FROM first_layer
)
SELECT
  *,
  RANK() OVER(ORDER BY avg_product_sale_price DESC) AS avg_product_sale_price_rank,
  RANK() OVER(ORDER BY avg_product_cost DESC) AS avg_product_cost_rank,
  RANK() OVER(ORDER BY revenue DESC) AS revenue_rank,
  RANK() OVER(ORDER BY profit DESC) AS profit_rank,
  RANK() OVER(ORDER BY unit_orders_placed DESC) AS unit_orders_placed_rank,
  RANK() OVER(ORDER BY units_completed DESC) AS units_completed_rank,
  RANK() OVER(ORDER BY units_returned DESC) AS units_returned_rank,
  RANK() OVER(ORDER BY units_cancelled DESC) AS units_cancelled_rank,
  RANK() OVER(ORDER BY units_en_route DESC) AS units_en_route_rank,
  RANK() OVER(ORDER BY lost_revenue DESC) AS lost_revenue_rank,
  RANK() OVER(ORDER BY lost_profit DESC) AS lost_profit_rank,
  RANK() OVER(ORDER BY profit_margin DESC) AS profit_margin_rank,
  RANK() OVER(ORDER BY return_rate DESC) AS return_rate_rank,
  RANK() OVER(ORDER BY completion_rate DESC) AS completion_rate_rank,
  RANK() OVER(ORDER BY cancellation_rate DESC) AS cancellation_rate_rank,
  RANK() OVER(ORDER BY en_route_rate DESC) AS en_route_rate_rank
FROM second_layer
ORDER BY
  revenue_rank ASC
LIMIT 15;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>product_brand</th>
      <th>avg_product_sale_price</th>
      <th>avg_product_cost</th>
      <th>revenue</th>
      <th>profit</th>
      <th>unit_orders_placed</th>
      <th>units_completed</th>
      <th>units_returned</th>
      <th>units_cancelled</th>
      <th>units_en_route</th>
      <th>lost_revenue</th>
      <th>lost_profit</th>
      <th>profit_margin</th>
      <th>return_rate</th>
      <th>completion_rate</th>
      <th>cancellation_rate</th>
      <th>en_route_rate</th>
      <th>revenue_share</th>
      <th>profit_share</th>
      <th>unit_orders_placed_share</th>
      <th>avg_product_sale_price_rank</th>
      <th>avg_product_cost_rank</th>
      <th>revenue_rank</th>
      <th>profit_rank</th>
      <th>unit_orders_placed_rank</th>
      <th>units_completed_rank</th>
      <th>units_returned_rank</th>
      <th>units_cancelled_rank</th>
      <th>units_en_route_rank</th>
      <th>lost_revenue_rank</th>
      <th>lost_profit_rank</th>
      <th>profit_margin_rank</th>
      <th>return_rate_rank</th>
      <th>completion_rate_rank</th>
      <th>cancellation_rate_rank</th>
      <th>en_route_rate_rank</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Diesel</td><td>138.24</td><td>68.92</td><td>53774.81</td><td>27000.8</td><td>1466</td><td>378</td><td>143</td><td>213</td><td>732</td><td>49754.6</td><td>24735.41</td><td>0.5021</td><td>0.2745</td><td>0.3017</td><td>0.1453</td><td>0.6595</td><td>0.0199204</td><td>0.0192971</td><td>0.0080872</td><td>205</td><td>184</td><td>1</td><td>2</td><td>13</td><td>10</td><td>12</td><td>13</td><td>13</td><td>1</td><td>2</td><td>1502</td><td>1319</td><td>1221</td><td>1318</td><td>1552</td></tr>
    <tr><td>Calvin Klein</td><td>62.49</td><td>29.31</td><td>53041.76</td><td>28267.04</td><td>3180</td><td>820</td><td>322</td><td>471</td><td>1567</td><td>48698.1</td><td>25795.42</td><td>0.5329</td><td>0.282</td><td>0.3027</td><td>0.1481</td><td>0.6565</td><td>0.0196488</td><td>0.0202021</td><td>0.0175425</td><td>805</td><td>836</td><td>2</td><td>1</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>1</td><td>1128</td><td>1282</td><td>1212</td><td>1270</td><td>1568</td></tr>
    <tr><td>Carhartt</td><td>68.41</td><td>32.02</td><td>44947.96</td><td>23945.23</td><td>2509</td><td>663</td><td>251</td><td>366</td><td>1229</td><td>41134.22</td><td>22022.28</td><td>0.5327</td><td>0.2746</td><td>0.3094</td><td>0.1459</td><td>0.6496</td><td>0.0166506</td><td>0.0171134</td><td>0.0138409</td><td>703</td><td>724</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>5</td><td>3</td><td>1132</td><td>1317</td><td>1155</td><td>1311</td><td>1623</td></tr>
    <tr><td>True Religion</td><td>196.17</td><td>101.7</td><td>43598.78</td><td>21127.8</td><td>879</td><td>225</td><td>84</td><td>146</td><td>424</td><td>43136.54</td><td>20619.76</td><td>0.4846</td><td>0.2718</td><td>0.307</td><td>0.1661</td><td>0.6533</td><td>0.0161508</td><td>0.0150998</td><td>0.004849</td><td>91</td><td>64</td><td>4</td><td>4</td><td>27</td><td>28</td><td>33</td><td>25</td><td>29</td><td>4</td><td>5</td><td>1705</td><td>1347</td><td>1186</td><td>1064</td><td>1592</td></tr>
    <tr><td>7 For All Mankind</td><td>155.67</td><td>81.33</td><td>39429.55</td><td>18708.21</td><td>1086</td><td>254</td><td>108</td><td>179</td><td>545</td><td>44113.73</td><td>21179.32</td><td>0.4745</td><td>0.2983</td><td>0.28</td><td>0.1648</td><td>0.6821</td><td>0.0146063</td><td>0.0133705</td><td>0.0059909</td><td>156</td><td>123</td><td>5</td><td>5</td><td>20</td><td>24</td><td>19</td><td>19</td><td>20</td><td>3</td><td>4</td><td>1826</td><td>1168</td><td>1503</td><td>1067</td><td>1192</td></tr>
    <tr><td>Volcom</td><td>58.67</td><td>29.91</td><td>28804.39</td><td>14059.0</td><td>1893</td><td>482</td><td>182</td><td>294</td><td>935</td><td>26458.99</td><td>12887.05</td><td>0.4881</td><td>0.2741</td><td>0.3014</td><td>0.1553</td><td>0.6598</td><td>0.0106703</td><td>0.0100478</td><td>0.0104428</td><td>877</td><td>805</td><td>6</td><td>8</td><td>5</td><td>4</td><td>7</td><td>5</td><td>5</td><td>9</td><td>10</td><td>1663</td><td>1320</td><td>1223</td><td>1174</td><td>1547</td></tr>
    <tr><td>Quiksilver</td><td>57.01</td><td>30.91</td><td>27609.19</td><td>12579.68</td><td>1873</td><td>471</td><td>202</td><td>297</td><td>903</td><td>26410.17</td><td>12067.7</td><td>0.4556</td><td>0.3001</td><td>0.2989</td><td>0.1586</td><td>0.6572</td><td>0.0102276</td><td>0.0089905</td><td>0.0103324</td><td>903</td><td>764</td><td>7</td><td>14</td><td>6</td><td>6</td><td>5</td><td>4</td><td>7</td><td>10</td><td>14</td><td>2066</td><td>1129</td><td>1275</td><td>1126</td><td>1563</td></tr>
    <tr><td>Columbia</td><td>69.37</td><td>31.72</td><td>26587.28</td><td>14439.48</td><td>1529</td><td>374</td><td>135</td><td>252</td><td>768</td><td>26842.48</td><td>14585.03</td><td>0.5431</td><td>0.2652</td><td>0.2929</td><td>0.1648</td><td>0.6725</td><td>0.009849</td><td>0.0103197</td><td>0.0084347</td><td>687</td><td>737</td><td>8</td><td>6</td><td>11</td><td>11</td><td>13</td><td>9</td><td>11</td><td>8</td><td>7</td><td>987</td><td>1379</td><td>1340</td><td>1067</td><td>1270</td></tr>
    <tr><td>Tommy Hilfiger</td><td>71.62</td><td>32.46</td><td>26074.49</td><td>14100.38</td><td>1615</td><td>404</td><td>162</td><td>254</td><td>795</td><td>29731.26</td><td>16179.42</td><td>0.5408</td><td>0.2862</td><td>0.2968</td><td>0.1573</td><td>0.6631</td><td>0.0096591</td><td>0.0100774</td><td>0.0089092</td><td>649</td><td>706</td><td>9</td><td>7</td><td>8</td><td>8</td><td>10</td><td>8</td><td>9</td><td>6</td><td>6</td><td>1021</td><td>1218</td><td>1294</td><td>1152</td><td>1525</td></tr>
    <tr><td>Orvis</td><td>128.92</td><td>60.07</td><td>25260.0</td><td>13494.35</td><td>721</td><td>186</td><td>65</td><td>102</td><td>368</td><td>21012.0</td><td>11275.59</td><td>0.5342</td><td>0.259</td><td>0.3005</td><td>0.1415</td><td>0.6643</td><td>0.0093573</td><td>0.0096442</td><td>0.0039774</td><td>239</td><td>245</td><td>10</td><td>12</td><td>39</td><td>39</td><td>47</td><td>44</td><td>38</td><td>17</td><td>17</td><td>1110</td><td>1416</td><td>1228</td><td>1453</td><td>1519</td></tr>
    <tr><td>The North Face</td><td>440.81</td><td>197.82</td><td>25174.88</td><td>13719.13</td><td>233</td><td>61</td><td>20</td><td>36</td><td>116</td><td>21048.75</td><td>11669.08</td><td>0.545</td><td>0.2469</td><td>0.3096</td><td>0.1545</td><td>0.6554</td><td>0.0093258</td><td>0.0098049</td><td>0.0012853</td><td>9</td><td>9</td><td>11</td><td>10</td><td>153</td><td>152</td><td>182</td><td>151</td><td>153</td><td>16</td><td>16</td><td>962</td><td>1608</td><td>1153</td><td>1181</td><td>1574</td></tr>
    <tr><td>Joe&#x27;s Jeans</td><td>152.81</td><td>80.23</td><td>25134.81</td><td>11891.96</td><td>697</td><td>169</td><td>76</td><td>99</td><td>353</td><td>27326.02</td><td>13164.83</td><td>0.4731</td><td>0.3102</td><td>0.2826</td><td>0.142</td><td>0.6762</td><td>0.009311</td><td>0.008499</td><td>0.003845</td><td>163</td><td>133</td><td>12</td><td>15</td><td>41</td><td>42</td><td>38</td><td>47</td><td>41</td><td>7</td><td>9</td><td>1850</td><td>1094</td><td>1486</td><td>1448</td><td>1239</td></tr>
    <tr><td>Jones New York</td><td>100.52</td><td>45.47</td><td>24723.78</td><td>13604.24</td><td>846</td><td>230</td><td>96</td><td>114</td><td>406</td><td>20262.41</td><td>10960.83</td><td>0.5502</td><td>0.2945</td><td>0.3142</td><td>0.1348</td><td>0.6384</td><td>0.0091587</td><td>0.0097228</td><td>0.004667</td><td>361</td><td>403</td><td>13</td><td>11</td><td>32</td><td>27</td><td>27</td><td>34</td><td>33</td><td>18</td><td>18</td><td>876</td><td>1178</td><td>1106</td><td>1532</td><td>1701</td></tr>
    <tr><td>Oakley</td><td>110.41</td><td>49.26</td><td>24423.2</td><td>13410.52</td><td>866</td><td>225</td><td>90</td><td>118</td><td>433</td><td>23073.48</td><td>12801.68</td><td>0.5491</td><td>0.2857</td><td>0.3008</td><td>0.1363</td><td>0.6581</td><td>0.0090474</td><td>0.0095843</td><td>0.0047773</td><td>316</td><td>355</td><td>14</td><td>13</td><td>29</td><td>28</td><td>30</td><td>33</td><td>27</td><td>12</td><td>12</td><td>896</td><td>1219</td><td>1227</td><td>1522</td><td>1556</td></tr>
    <tr><td>Ray-Ban</td><td>118.89</td><td>50.08</td><td>23852.78</td><td>13833.41</td><td>798</td><td>206</td><td>78</td><td>131</td><td>383</td><td>25134.08</td><td>14434.77</td><td>0.5799</td><td>0.2746</td><td>0.3088</td><td>0.1642</td><td>0.6503</td><td>0.008836</td><td>0.0098866</td><td>0.0044022</td><td>278</td><td>346</td><td>15</td><td>9</td><td>34</td><td>32</td><td>35</td><td>30</td><td>37</td><td>11</td><td>8</td><td>437</td><td>1317</td><td>1160</td><td>1073</td><td>1612</td></tr>
  </tbody>
</table>

</div>

<h3>Top brands by Lost Revenue</h3>

<pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.brand AS product_brand,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = 'Cancelled' THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN ('Shipped', 'Processing') THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
GROUP BY product_brand
),
second_layer AS (
SELECT
  *,
  ROUND((profit / NULLIF(revenue, 0)), 4) AS profit_margin,
  ROUND(units_returned / NULLIF(units_completed + units_returned, 0), 4) AS return_rate,
  ROUND(units_completed / NULLIF(unit_orders_placed - units_cancelled, 0), 4) AS completion_rate,
  ROUND(units_cancelled / NULLIF(unit_orders_placed, 0), 4) AS cancellation_rate,
  ROUND(units_en_route / NULLIF(unit_orders_placed - (units_cancelled + units_returned), 0), 4) AS en_route_rate,
  ROUND(revenue / SUM(revenue) OVER(), 7) AS revenue_share,
  ROUND(profit / SUM(profit) OVER(), 7) AS profit_share,
  ROUND(unit_orders_placed / SUM(unit_orders_placed) OVER(), 7) AS unit_orders_placed_share
FROM first_layer
)
SELECT
  *,
  RANK() OVER(ORDER BY avg_product_sale_price DESC) AS avg_product_sale_price_rank,
  RANK() OVER(ORDER BY avg_product_cost DESC) AS avg_product_cost_rank,
  RANK() OVER(ORDER BY revenue DESC) AS revenue_rank,
  RANK() OVER(ORDER BY profit DESC) AS profit_rank,
  RANK() OVER(ORDER BY unit_orders_placed DESC) AS unit_orders_placed_rank,
  RANK() OVER(ORDER BY units_completed DESC) AS units_completed_rank,
  RANK() OVER(ORDER BY units_returned DESC) AS units_returned_rank,
  RANK() OVER(ORDER BY units_cancelled DESC) AS units_cancelled_rank,
  RANK() OVER(ORDER BY units_en_route DESC) AS units_en_route_rank,
  RANK() OVER(ORDER BY lost_revenue DESC) AS lost_revenue_rank,
  RANK() OVER(ORDER BY lost_profit DESC) AS lost_profit_rank,
  RANK() OVER(ORDER BY profit_margin DESC) AS profit_margin_rank,
  RANK() OVER(ORDER BY return_rate DESC) AS return_rate_rank,
  RANK() OVER(ORDER BY completion_rate DESC) AS completion_rate_rank,
  RANK() OVER(ORDER BY cancellation_rate DESC) AS cancellation_rate_rank,
  RANK() OVER(ORDER BY en_route_rate DESC) AS en_route_rate_rank
FROM second_layer
ORDER BY
  lost_revenue_rank ASC
LIMIT 15;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>product_brand</th>
      <th>avg_product_sale_price</th>
      <th>avg_product_cost</th>
      <th>revenue</th>
      <th>profit</th>
      <th>unit_orders_placed</th>
      <th>units_completed</th>
      <th>units_returned</th>
      <th>units_cancelled</th>
      <th>units_en_route</th>
      <th>lost_revenue</th>
      <th>lost_profit</th>
      <th>profit_margin</th>
      <th>return_rate</th>
      <th>completion_rate</th>
      <th>cancellation_rate</th>
      <th>en_route_rate</th>
      <th>revenue_share</th>
      <th>profit_share</th>
      <th>unit_orders_placed_share</th>
      <th>avg_product_sale_price_rank</th>
      <th>avg_product_cost_rank</th>
      <th>revenue_rank</th>
      <th>profit_rank</th>
      <th>unit_orders_placed_rank</th>
      <th>units_completed_rank</th>
      <th>units_returned_rank</th>
      <th>units_cancelled_rank</th>
      <th>units_en_route_rank</th>
      <th>lost_revenue_rank</th>
      <th>lost_profit_rank</th>
      <th>profit_margin_rank</th>
      <th>return_rate_rank</th>
      <th>completion_rate_rank</th>
      <th>cancellation_rate_rank</th>
      <th>en_route_rate_rank</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Diesel</td><td>138.24</td><td>68.92</td><td>53774.81</td><td>27000.8</td><td>1466</td><td>378</td><td>143</td><td>213</td><td>732</td><td>49754.6</td><td>24735.41</td><td>0.5021</td><td>0.2745</td><td>0.3017</td><td>0.1453</td><td>0.6595</td><td>0.0199204</td><td>0.0192971</td><td>0.0080872</td><td>205</td><td>184</td><td>1</td><td>2</td><td>13</td><td>10</td><td>12</td><td>13</td><td>13</td><td>1</td><td>2</td><td>1502</td><td>1319</td><td>1221</td><td>1318</td><td>1552</td></tr>
    <tr><td>Calvin Klein</td><td>62.49</td><td>29.31</td><td>53041.76</td><td>28267.04</td><td>3180</td><td>820</td><td>322</td><td>471</td><td>1567</td><td>48698.1</td><td>25795.42</td><td>0.5329</td><td>0.282</td><td>0.3027</td><td>0.1481</td><td>0.6565</td><td>0.0196488</td><td>0.0202021</td><td>0.0175425</td><td>805</td><td>836</td><td>2</td><td>1</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>1</td><td>1128</td><td>1282</td><td>1212</td><td>1270</td><td>1568</td></tr>
    <tr><td>7 For All Mankind</td><td>155.67</td><td>81.33</td><td>39429.55</td><td>18708.21</td><td>1086</td><td>254</td><td>108</td><td>179</td><td>545</td><td>44113.73</td><td>21179.32</td><td>0.4745</td><td>0.2983</td><td>0.28</td><td>0.1648</td><td>0.6821</td><td>0.0146063</td><td>0.0133705</td><td>0.0059909</td><td>156</td><td>123</td><td>5</td><td>5</td><td>20</td><td>24</td><td>19</td><td>19</td><td>20</td><td>3</td><td>4</td><td>1826</td><td>1168</td><td>1503</td><td>1067</td><td>1192</td></tr>
    <tr><td>True Religion</td><td>196.17</td><td>101.7</td><td>43598.78</td><td>21127.8</td><td>879</td><td>225</td><td>84</td><td>146</td><td>424</td><td>43136.54</td><td>20619.76</td><td>0.4846</td><td>0.2718</td><td>0.307</td><td>0.1661</td><td>0.6533</td><td>0.0161508</td><td>0.0150998</td><td>0.004849</td><td>91</td><td>64</td><td>4</td><td>4</td><td>27</td><td>28</td><td>33</td><td>25</td><td>29</td><td>4</td><td>5</td><td>1705</td><td>1347</td><td>1186</td><td>1064</td><td>1592</td></tr>
    <tr><td>Carhartt</td><td>68.41</td><td>32.02</td><td>44947.96</td><td>23945.23</td><td>2509</td><td>663</td><td>251</td><td>366</td><td>1229</td><td>41134.22</td><td>22022.28</td><td>0.5327</td><td>0.2746</td><td>0.3094</td><td>0.1459</td><td>0.6496</td><td>0.0166506</td><td>0.0171134</td><td>0.0138409</td><td>703</td><td>724</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>5</td><td>3</td><td>1132</td><td>1317</td><td>1155</td><td>1311</td><td>1623</td></tr>
    <tr><td>Tommy Hilfiger</td><td>71.62</td><td>32.46</td><td>26074.49</td><td>14100.38</td><td>1615</td><td>404</td><td>162</td><td>254</td><td>795</td><td>29731.26</td><td>16179.42</td><td>0.5408</td><td>0.2862</td><td>0.2968</td><td>0.1573</td><td>0.6631</td><td>0.0096591</td><td>0.0100774</td><td>0.0089092</td><td>649</td><td>706</td><td>9</td><td>7</td><td>8</td><td>8</td><td>10</td><td>8</td><td>9</td><td>6</td><td>6</td><td>1021</td><td>1218</td><td>1294</td><td>1152</td><td>1525</td></tr>
    <tr><td>Joe&#x27;s Jeans</td><td>152.81</td><td>80.23</td><td>25134.81</td><td>11891.96</td><td>697</td><td>169</td><td>76</td><td>99</td><td>353</td><td>27326.02</td><td>13164.83</td><td>0.4731</td><td>0.3102</td><td>0.2826</td><td>0.142</td><td>0.6762</td><td>0.009311</td><td>0.008499</td><td>0.003845</td><td>163</td><td>133</td><td>12</td><td>15</td><td>41</td><td>42</td><td>38</td><td>47</td><td>41</td><td>7</td><td>9</td><td>1850</td><td>1094</td><td>1486</td><td>1448</td><td>1239</td></tr>
    <tr><td>Columbia</td><td>69.37</td><td>31.72</td><td>26587.28</td><td>14439.48</td><td>1529</td><td>374</td><td>135</td><td>252</td><td>768</td><td>26842.48</td><td>14585.03</td><td>0.5431</td><td>0.2652</td><td>0.2929</td><td>0.1648</td><td>0.6725</td><td>0.009849</td><td>0.0103197</td><td>0.0084347</td><td>687</td><td>737</td><td>8</td><td>6</td><td>11</td><td>11</td><td>13</td><td>9</td><td>11</td><td>8</td><td>7</td><td>987</td><td>1379</td><td>1340</td><td>1067</td><td>1270</td></tr>
    <tr><td>Volcom</td><td>58.67</td><td>29.91</td><td>28804.39</td><td>14059.0</td><td>1893</td><td>482</td><td>182</td><td>294</td><td>935</td><td>26458.99</td><td>12887.05</td><td>0.4881</td><td>0.2741</td><td>0.3014</td><td>0.1553</td><td>0.6598</td><td>0.0106703</td><td>0.0100478</td><td>0.0104428</td><td>877</td><td>805</td><td>6</td><td>8</td><td>5</td><td>4</td><td>7</td><td>5</td><td>5</td><td>9</td><td>10</td><td>1663</td><td>1320</td><td>1223</td><td>1174</td><td>1547</td></tr>
    <tr><td>Quiksilver</td><td>57.01</td><td>30.91</td><td>27609.19</td><td>12579.68</td><td>1873</td><td>471</td><td>202</td><td>297</td><td>903</td><td>26410.17</td><td>12067.7</td><td>0.4556</td><td>0.3001</td><td>0.2989</td><td>0.1586</td><td>0.6572</td><td>0.0102276</td><td>0.0089905</td><td>0.0103324</td><td>903</td><td>764</td><td>7</td><td>14</td><td>6</td><td>6</td><td>5</td><td>4</td><td>7</td><td>10</td><td>14</td><td>2066</td><td>1129</td><td>1275</td><td>1126</td><td>1563</td></tr>
    <tr><td>Ray-Ban</td><td>118.89</td><td>50.08</td><td>23852.78</td><td>13833.41</td><td>798</td><td>206</td><td>78</td><td>131</td><td>383</td><td>25134.08</td><td>14434.77</td><td>0.5799</td><td>0.2746</td><td>0.3088</td><td>0.1642</td><td>0.6503</td><td>0.008836</td><td>0.0098866</td><td>0.0044022</td><td>278</td><td>346</td><td>15</td><td>9</td><td>34</td><td>32</td><td>35</td><td>30</td><td>37</td><td>11</td><td>8</td><td>437</td><td>1317</td><td>1160</td><td>1073</td><td>1612</td></tr>
    <tr><td>Oakley</td><td>110.41</td><td>49.26</td><td>24423.2</td><td>13410.52</td><td>866</td><td>225</td><td>90</td><td>118</td><td>433</td><td>23073.48</td><td>12801.68</td><td>0.5491</td><td>0.2857</td><td>0.3008</td><td>0.1363</td><td>0.6581</td><td>0.0090474</td><td>0.0095843</td><td>0.0047773</td><td>316</td><td>355</td><td>14</td><td>13</td><td>29</td><td>28</td><td>30</td><td>33</td><td>27</td><td>12</td><td>12</td><td>896</td><td>1219</td><td>1227</td><td>1522</td><td>1556</td></tr>
    <tr><td>Arc&#x27;teryx</td><td>323.7</td><td>146.18</td><td>18141.7</td><td>9908.14</td><td>271</td><td>56</td><td>22</td><td>41</td><td>152</td><td>22880.85</td><td>12500.89</td><td>0.5462</td><td>0.2821</td><td>0.2435</td><td>0.1513</td><td>0.7308</td><td>0.0067204</td><td>0.0070812</td><td>0.001495</td><td>22</td><td>20</td><td>22</td><td>19</td><td>132</td><td>169</td><td>161</td><td>132</td><td>118</td><td>13</td><td>13</td><td>943</td><td>1281</td><td>1928</td><td>1234</td><td>808</td></tr>
    <tr><td>Canada Goose</td><td>577.82</td><td>249.06</td><td>12909.93</td><td>7257.7</td><td>115</td><td>22</td><td>15</td><td>21</td><td>57</td><td>22479.93</td><td>12816.81</td><td>0.5622</td><td>0.4054</td><td>0.234</td><td>0.1826</td><td>0.7215</td><td>0.0047824</td><td>0.005187</td><td>0.0006344</td><td>4</td><td>5</td><td>36</td><td>34</td><td>337</td><td>412</td><td>261</td><td>265</td><td>329</td><td>14</td><td>11</td><td>672</td><td>572</td><td>1980</td><td>814</td><td>871</td></tr>
    <tr><td>Allegra K</td><td>14.35</td><td>6.76</td><td>20908.12</td><td>11061.0</td><td>6057</td><td>1467</td><td>610</td><td>943</td><td>3037</td><td>22396.3</td><td>11874.9</td><td>0.529</td><td>0.2937</td><td>0.2869</td><td>0.1557</td><td>0.6743</td><td>0.0077452</td><td>0.0079052</td><td>0.0334135</td><td>2442</td><td>2434</td><td>16</td><td>16</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>15</td><td>15</td><td>1172</td><td>1190</td><td>1384</td><td>1170</td><td>1255</td></tr>
  </tbody>
</table>

</div>

<h3>Analytical Insights & Business Recommendations</h3>

<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p><strong>Revenue vs. Profit Leadership Diverges:</strong> Diesel leads all brands in revenue ($53,774.81) but drops to #2 in profit ($27,000.80) due to a relatively low profit margin of 50.2%. Calvin Klein overtakes Diesel in profit ($28,267.04) despite ranking #2 in revenue, thanks to a stronger 53.3% margin. This divergence reveals that Diesel's higher average sale price ($138.24) comes with proportionally higher product costs ($68.92), compressing margins.</p>

<p>Recommendation: For high-revenue, lower-margin brands like Diesel, negotiate better supplier pricing given the volume leverage – 1,466 units ordered gives significant bargaining power. Even a 2–3% cost reduction on Diesel products would yield substantial additional profit given the revenue scale. Alternatively, since Diesel already commands premium pricing, explore whether modest price increases on best-selling Diesel items would be absorbed by demand without significant volume loss.</p>

<p><strong>The North Face: Premium Pricing Power:</strong> The North Face ranks #11 in revenue ($25,174.88) but achieves this with only 233 unit orders – the fewest among the top 15 brands. Its average sale price of $440.81 is the highest by a wide margin (the next highest is True Religion at $196.17). This means The North Face extracts over 2x more revenue per unit than any comparable brand.</p>

<p>With a 54.5% profit margin and only 20 returns out of 81 completed/returned units (24.7% return rate – the lowest among top brands), The North Face represents the most efficient revenue-to-order ratio in the dataset.</p>

<p>Recommendation: Allocate increased internal inventory space and priority fulfillment to The North Face products. Their per-unit contribution is unmatched, and with the lowest return rate among top brands, each sale is highly likely to convert to retained revenue. Ensure stockouts never occur on The North Face items – lost sales on $440+ average items represent outsized opportunity cost.</p>







<p><strong>Lost Revenue Leaders Mirror Revenue Leaders:</strong> The top brands by lost revenue are the same as the top brands by revenue – Diesel ($49,754.60 lost), Calvin Klein ($48,698.10), Carhartt ($41,134.22). This is expected since lost revenue scales with order volume and average price. However, the ratio of lost revenue to actual revenue is striking: Diesel loses $49K vs. earning $53K, meaning nearly half of all potential Diesel revenue evaporates through returns and cancellations.</p>

<p>Recommendation: For brands where lost revenue approaches or exceeds earned revenue, the cost of returns processing, reverse shipping, and restocking is a significant hidden expense. Investigate whether specific Diesel or Calvin Klein product lines disproportionately drive the returns, and target those SKUs for quality review or enhanced product descriptions rather than applying broad brand-level interventions.</p>

<p><strong>Canada Goose: High Value, High Risk:</strong> Canada Goose stands out in the lost revenue table despite ranking #36 in revenue and #337 in unit orders. With only 115 orders placed, it generates $12,909.93 in revenue but $22,479.93 in lost revenue – nearly 2x what it actually earns. Its 40.5% return rate is the highest among brands appearing in the top 15 by lost profit.</p>

<p>Recommendation: Given Canada Goose's extremely high price point ($577.82 avg) and disproportionate loss ratio, this brand warrants a targeted investigation. With only 22 completed sales out of 115 orders, something systemic is driving cancellations and returns – possibly shipping delays on premium items, customer sticker shock after purchase, or quality/authenticity concerns. Consider whether the brand partnership is net-positive after accounting for return-processing costs on $500+ items.</p>



</div>

</details>
<details>
  <summary><strong>Bottom Brands</strong></summary>

  <div style="margin-top: 12px;"></div>

<h3>Bottom brands by Profit Margin</h3>

<pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.brand AS product_brand,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = 'Cancelled' THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN ('Shipped', 'Processing') THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
GROUP BY product_brand
),
second_layer AS (
SELECT
  *,
  ROUND((profit / NULLIF(revenue, 0)), 4) AS profit_margin,
  ROUND(units_returned / NULLIF(units_completed + units_returned, 0), 4) AS return_rate,
  ROUND(units_completed / NULLIF(unit_orders_placed - units_cancelled, 0), 4) AS completion_rate,
  ROUND(units_cancelled / NULLIF(unit_orders_placed, 0), 4) AS cancellation_rate,
  ROUND(units_en_route / NULLIF(unit_orders_placed - (units_cancelled + units_returned), 0), 4) AS en_route_rate,
  ROUND(revenue / SUM(revenue) OVER(), 7) AS revenue_share,
  ROUND(profit / SUM(profit) OVER(), 7) AS profit_share,
  ROUND(unit_orders_placed / SUM(unit_orders_placed) OVER(), 7) AS unit_orders_placed_share
FROM first_layer
)
, third_layer AS (
SELECT
  *,
  RANK() OVER(ORDER BY avg_product_sale_price DESC) AS avg_product_sale_price_rank,
  RANK() OVER(ORDER BY avg_product_cost DESC) AS avg_product_cost_rank,
  RANK() OVER(ORDER BY revenue DESC) AS revenue_rank,
  RANK() OVER(ORDER BY profit DESC) AS profit_rank,
  RANK() OVER(ORDER BY unit_orders_placed DESC) AS unit_orders_placed_rank,
  RANK() OVER(ORDER BY units_completed DESC) AS units_completed_rank,
  RANK() OVER(ORDER BY units_returned DESC) AS units_returned_rank,
  RANK() OVER(ORDER BY units_cancelled DESC) AS units_cancelled_rank,
  RANK() OVER(ORDER BY units_en_route DESC) AS units_en_route_rank,
  RANK() OVER(ORDER BY lost_revenue DESC) AS lost_revenue_rank,
  RANK() OVER(ORDER BY lost_profit DESC) AS lost_profit_rank,
  RANK() OVER(ORDER BY profit_margin DESC) AS profit_margin_rank,
  RANK() OVER(ORDER BY return_rate DESC) AS return_rate_rank,
  RANK() OVER(ORDER BY completion_rate DESC) AS completion_rate_rank,
  RANK() OVER(ORDER BY cancellation_rate DESC) AS cancellation_rate_rank,
  RANK() OVER(ORDER BY en_route_rate DESC) AS en_route_rate_rank
FROM second_layer
)
SELECT
	*
FROM third_layer
WHERE revenue_rank &lt;= 50
ORDER BY
  profit_margin_rank DESC
LIMIT 15;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>product_brand</th>
      <th>avg_product_sale_price</th>
      <th>avg_product_cost</th>
      <th>revenue</th>
      <th>profit</th>
      <th>unit_orders_placed</th>
      <th>units_completed</th>
      <th>units_returned</th>
      <th>units_cancelled</th>
      <th>units_en_route</th>
      <th>lost_revenue</th>
      <th>lost_profit</th>
      <th>profit_margin</th>
      <th>return_rate</th>
      <th>completion_rate</th>
      <th>cancellation_rate</th>
      <th>en_route_rate</th>
      <th>revenue_share</th>
      <th>profit_share</th>
      <th>unit_orders_placed_share</th>
      <th>avg_product_sale_price_rank</th>
      <th>avg_product_cost_rank</th>
      <th>revenue_rank</th>
      <th>profit_rank</th>
      <th>unit_orders_placed_rank</th>
      <th>units_completed_rank</th>
      <th>units_returned_rank</th>
      <th>units_cancelled_rank</th>
      <th>units_en_route_rank</th>
      <th>lost_revenue_rank</th>
      <th>lost_profit_rank</th>
      <th>profit_margin_rank</th>
      <th>return_rate_rank</th>
      <th>completion_rate_rank</th>
      <th>cancellation_rate_rank</th>
      <th>en_route_rate_rank</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>O&#x27;Neill</td><td>48.36</td><td>26.32</td><td>12853.97</td><td>5838.83</td><td>1056</td><td>266</td><td>105</td><td>166</td><td>519</td><td>12805.89</td><td>5826.98</td><td>0.4542</td><td>0.283</td><td>0.2989</td><td>0.1572</td><td>0.6611</td><td>0.004776</td><td>0.0041877</td><td>0.0058271</td><td>1121</td><td>966</td><td>40</td><td>49</td><td>21</td><td>20</td><td>20</td><td>19</td><td>21</td><td>36</td><td>45</td><td>2064</td><td>1275</td><td>1256</td><td>1152</td><td>1592</td></tr>
    <tr><td>Not Your Daughter&#x27;s Jeans</td><td>100.85</td><td>54.77</td><td>16067.86</td><td>7332.91</td><td>527</td><td>157</td><td>62</td><td>61</td><td>247</td><td>12591.86</td><td>5739.96</td><td>0.4564</td><td>0.2831</td><td>0.3369</td><td>0.1157</td><td>0.6114</td><td>0.0059701</td><td>0.0052593</td><td>0.002908</td><td>351</td><td>296</td><td>26</td><td>32</td><td>54</td><td>46</td><td>49</td><td>82</td><td>61</td><td>38</td><td>48</td><td>2039</td><td>1273</td><td>768</td><td>1797</td><td>1957</td></tr>
    <tr><td>Quiksilver</td><td>61.96</td><td>33.3</td><td>27116.76</td><td>12559.81</td><td>1714</td><td>449</td><td>185</td><td>258</td><td>822</td><td>28245.96</td><td>13081.14</td><td>0.4632</td><td>0.2918</td><td>0.3084</td><td>0.1505</td><td>0.6467</td><td>0.0100755</td><td>0.0090081</td><td>0.009458</td><td>807</td><td>686</td><td>8</td><td>11</td><td>6</td><td>6</td><td>6</td><td>6</td><td>7</td><td>7</td><td>11</td><td>1969</td><td>1191</td><td>1129</td><td>1253</td><td>1694</td></tr>
    <tr><td>Hurley</td><td>51.36</td><td>27.48</td><td>21510.02</td><td>9986.41</td><td>1580</td><td>417</td><td>163</td><td>218</td><td>782</td><td>19406.52</td><td>9038.59</td><td>0.4643</td><td>0.281</td><td>0.3062</td><td>0.138</td><td>0.6522</td><td>0.0079922</td><td>0.0071624</td><td>0.0087185</td><td>1028</td><td>911</td><td>15</td><td>19</td><td>10</td><td>8</td><td>8</td><td>13</td><td>9</td><td>19</td><td>23</td><td>1950</td><td>1282</td><td>1168</td><td>1482</td><td>1647</td></tr>
    <tr><td>Hudson</td><td>175.32</td><td>92.88</td><td>10759.54</td><td>5042.67</td><td>238</td><td>59</td><td>22</td><td>36</td><td>121</td><td>9975.18</td><td>4637.96</td><td>0.4687</td><td>0.2716</td><td>0.2921</td><td>0.1513</td><td>0.6722</td><td>0.0039978</td><td>0.0036167</td><td>0.0013133</td><td>124</td><td>81</td><td>49</td><td>57</td><td>147</td><td>155</td><td>163</td><td>147</td><td>147</td><td>53</td><td>61</td><td>1890</td><td>1334</td><td>1311</td><td>1241</td><td>1291</td></tr>
    <tr><td>Wrangler</td><td>42.74</td><td>22.6</td><td>12444.43</td><td>5840.02</td><td>1284</td><td>293</td><td>128</td><td>220</td><td>643</td><td>14851.87</td><td>6983.23</td><td>0.4693</td><td>0.304</td><td>0.2754</td><td>0.1713</td><td>0.687</td><td>0.0046238</td><td>0.0041886</td><td>0.0070852</td><td>1272</td><td>1178</td><td>43</td><td>48</td><td>14</td><td>15</td><td>14</td><td>12</td><td>14</td><td>32</td><td>34</td><td>1880</td><td>1126</td><td>1522</td><td>929</td><td>1182</td></tr>
    <tr><td>Joe&#x27;s Jeans</td><td>152.57</td><td>80.56</td><td>24447.28</td><td>11502.21</td><td>680</td><td>161</td><td>61</td><td>112</td><td>346</td><td>26495.04</td><td>12836.04</td><td>0.4705</td><td>0.2748</td><td>0.2835</td><td>0.1647</td><td>0.6824</td><td>0.0090836</td><td>0.0082496</td><td>0.0037523</td><td>163</td><td>127</td><td>10</td><td>14</td><td>42</td><td>43</td><td>52</td><td>38</td><td>40</td><td>9</td><td>13</td><td>1861</td><td>1308</td><td>1444</td><td>1079</td><td>1212</td></tr>
    <tr><td>True Religion</td><td>202.86</td><td>106.23</td><td>41113.02</td><td>19519.17</td><td>849</td><td>195</td><td>93</td><td>126</td><td>435</td><td>45038.92</td><td>21465.47</td><td>0.4748</td><td>0.3229</td><td>0.2697</td><td>0.1484</td><td>0.6905</td><td>0.0152759</td><td>0.0139995</td><td>0.0046848</td><td>83</td><td>51</td><td>5</td><td>5</td><td>32</td><td>34</td><td>30</td><td>32</td><td>30</td><td>3</td><td>4</td><td>1810</td><td>1044</td><td>1573</td><td>1285</td><td>1144</td></tr>
    <tr><td>7 For All Mankind</td><td>157.7</td><td>82.42</td><td>43657.56</td><td>20989.88</td><td>1108</td><td>271</td><td>99</td><td>168</td><td>570</td><td>41942.75</td><td>19952.86</td><td>0.4808</td><td>0.2676</td><td>0.2883</td><td>0.1516</td><td>0.6778</td><td>0.0162213</td><td>0.0150543</td><td>0.006114</td><td>151</td><td>118</td><td>3</td><td>4</td><td>19</td><td>18</td><td>24</td><td>18</td><td>18</td><td>5</td><td>5</td><td>1730</td><td>1349</td><td>1336</td><td>1234</td><td>1251</td></tr>
    <tr><td>Lucky Brand</td><td>72.72</td><td>37.91</td><td>20488.7</td><td>9871.63</td><td>1073</td><td>289</td><td>92</td><td>157</td><td>535</td><td>18560.05</td><td>8803.71</td><td>0.4818</td><td>0.2415</td><td>0.3155</td><td>0.1463</td><td>0.6493</td><td>0.0076127</td><td>0.0070801</td><td>0.0059209</td><td>631</td><td>548</td><td>17</td><td>21</td><td>20</td><td>16</td><td>31</td><td>21</td><td>20</td><td>21</td><td>25</td><td>1719</td><td>1590</td><td>1077</td><td>1319</td><td>1673</td></tr>
    <tr><td>AG Adriano Goldschmied</td><td>158.52</td><td>81.45</td><td>15325.0</td><td>7390.13</td><td>353</td><td>96</td><td>35</td><td>43</td><td>179</td><td>12419.86</td><td>6058.66</td><td>0.4822</td><td>0.2672</td><td>0.3097</td><td>0.1218</td><td>0.6509</td><td>0.0056941</td><td>0.0053003</td><td>0.0019479</td><td>149</td><td>121</td><td>30</td><td>30</td><td>100</td><td>84</td><td>102</td><td>126</td><td>93</td><td>40</td><td>40</td><td>1713</td><td>1351</td><td>1123</td><td>1739</td><td>1660</td></tr>
    <tr><td>DC</td><td>50.94</td><td>25.91</td><td>14076.31</td><td>6883.92</td><td>966</td><td>263</td><td>101</td><td>148</td><td>454</td><td>12578.25</td><td>6213.14</td><td>0.489</td><td>0.2775</td><td>0.3215</td><td>0.1532</td><td>0.6332</td><td>0.0052302</td><td>0.0049373</td><td>0.0053304</td><td>1036</td><td>990</td><td>32</td><td>37</td><td>25</td><td>22</td><td>22</td><td>24</td><td>26</td><td>39</td><td>39</td><td>1628</td><td>1299</td><td>1027</td><td>1219</td><td>1811</td></tr>
    <tr><td>Volcom</td><td>59.28</td><td>29.98</td><td>31207.34</td><td>15349.94</td><td>1914</td><td>521</td><td>192</td><td>271</td><td>930</td><td>28218.2</td><td>13987.51</td><td>0.4919</td><td>0.2693</td><td>0.3171</td><td>0.1416</td><td>0.6409</td><td>0.0115953</td><td>0.0110093</td><td>0.0105616</td><td>868</td><td>801</td><td>6</td><td>7</td><td>5</td><td>4</td><td>5</td><td>5</td><td>5</td><td>8</td><td>8</td><td>1601</td><td>1341</td><td>1058</td><td>1448</td><td>1747</td></tr>
    <tr><td>Nike</td><td>80.59</td><td>40.35</td><td>16424.08</td><td>8174.99</td><td>520</td><td>125</td><td>44</td><td>76</td><td>275</td><td>7304.66</td><td>3876.47</td><td>0.4977</td><td>0.2604</td><td>0.2815</td><td>0.1462</td><td>0.6875</td><td>0.0061025</td><td>0.0058633</td><td>0.0028694</td><td>531</td><td>487</td><td>25</td><td>28</td><td>55</td><td>56</td><td>73</td><td>63</td><td>50</td><td>76</td><td>73</td><td>1534</td><td>1384</td><td>1460</td><td>1321</td><td>1169</td></tr>
    <tr><td>Levi&#x27;s</td><td>50.16</td><td>25.28</td><td>21140.97</td><td>10560.39</td><td>1583</td><td>418</td><td>172</td><td>238</td><td>755</td><td>20050.17</td><td>9823.1</td><td>0.4995</td><td>0.2915</td><td>0.3108</td><td>0.1503</td><td>0.6436</td><td>0.0078551</td><td>0.0075741</td><td>0.0087351</td><td>1053</td><td>1019</td><td>16</td><td>16</td><td>9</td><td>7</td><td>7</td><td>9</td><td>11</td><td>18</td><td>19</td><td>1502</td><td>1195</td><td>1112</td><td>1255</td><td>1713</td></tr>
  </tbody>
</table>

</div>

<h3>Bottom brands by Unit Orders</h3>

<pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.brand AS product_brand,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = 'Cancelled' THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN ('Shipped', 'Processing') THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
GROUP BY product_brand
),
second_layer AS (
SELECT
  *,
  ROUND((profit / NULLIF(revenue, 0)), 4) AS profit_margin,
  ROUND(units_returned / NULLIF(units_completed + units_returned, 0), 4) AS return_rate,
  ROUND(units_completed / NULLIF(unit_orders_placed - units_cancelled, 0), 4) AS completion_rate,
  ROUND(units_cancelled / NULLIF(unit_orders_placed, 0), 4) AS cancellation_rate,
  ROUND(units_en_route / NULLIF(unit_orders_placed - (units_cancelled + units_returned), 0), 4) AS en_route_rate,
  ROUND(revenue / SUM(revenue) OVER(), 7) AS revenue_share,
  ROUND(profit / SUM(profit) OVER(), 7) AS profit_share,
  ROUND(unit_orders_placed / SUM(unit_orders_placed) OVER(), 7) AS unit_orders_placed_share
FROM first_layer
)
SELECT
  *,
  RANK() OVER(ORDER BY avg_product_sale_price DESC) AS avg_product_sale_price_rank,
  RANK() OVER(ORDER BY avg_product_cost DESC) AS avg_product_cost_rank,
  RANK() OVER(ORDER BY revenue DESC) AS revenue_rank,
  RANK() OVER(ORDER BY profit DESC) AS profit_rank,
  RANK() OVER(ORDER BY unit_orders_placed DESC) AS unit_orders_placed_rank,
  RANK() OVER(ORDER BY units_completed DESC) AS units_completed_rank,
  RANK() OVER(ORDER BY units_returned DESC) AS units_returned_rank,
  RANK() OVER(ORDER BY units_cancelled DESC) AS units_cancelled_rank,
  RANK() OVER(ORDER BY units_en_route DESC) AS units_en_route_rank,
  RANK() OVER(ORDER BY lost_revenue DESC) AS lost_revenue_rank,
  RANK() OVER(ORDER BY lost_profit DESC) AS lost_profit_rank,
  RANK() OVER(ORDER BY profit_margin DESC) AS profit_margin_rank,
  RANK() OVER(ORDER BY return_rate DESC) AS return_rate_rank,
  RANK() OVER(ORDER BY completion_rate DESC) AS completion_rate_rank,
  RANK() OVER(ORDER BY cancellation_rate DESC) AS cancellation_rate_rank,
  RANK() OVER(ORDER BY en_route_rate DESC) AS en_route_rate_rank
FROM second_layer
ORDER BY
  unit_orders_placed_rank DESC
LIMIT 15;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>product_brand</th>
      <th>avg_product_sale_price</th>
      <th>avg_product_cost</th>
      <th>revenue</th>
      <th>profit</th>
      <th>unit_orders_placed</th>
      <th>units_completed</th>
      <th>units_returned</th>
      <th>units_cancelled</th>
      <th>units_en_route</th>
      <th>lost_revenue</th>
      <th>lost_profit</th>
      <th>profit_margin</th>
      <th>return_rate</th>
      <th>completion_rate</th>
      <th>cancellation_rate</th>
      <th>en_route_rate</th>
      <th>revenue_share</th>
      <th>profit_share</th>
      <th>unit_orders_placed_share</th>
      <th>avg_product_sale_price_rank</th>
      <th>avg_product_cost_rank</th>
      <th>revenue_rank</th>
      <th>profit_rank</th>
      <th>unit_orders_placed_rank</th>
      <th>units_completed_rank</th>
      <th>units_returned_rank</th>
      <th>units_cancelled_rank</th>
      <th>units_en_route_rank</th>
      <th>lost_revenue_rank</th>
      <th>lost_profit_rank</th>
      <th>profit_margin_rank</th>
      <th>return_rate_rank</th>
      <th>completion_rate_rank</th>
      <th>cancellation_rate_rank</th>
      <th>en_route_rate_rank</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Versace</td><td>128.5</td><td>57.7</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>128.5</td><td>70.8</td><td></td><td>1.0</td><td>0.0</td><td>0.0</td><td></td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>234</td><td>265</td><td>2518</td><td>2518</td><td>2742</td><td>2518</td><td>1457</td><td>2284</td><td>2713</td><td>1528</td><td>1482</td><td>2518</td><td>1</td><td>2518</td><td>2284</td><td>2743</td></tr>
    <tr><td>Hermanny</td><td>62.99</td><td>25.13</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>62.99</td><td>37.86</td><td></td><td>1.0</td><td>0.0</td><td>0.0</td><td></td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>796</td><td>1030</td><td>2518</td><td>2518</td><td>2742</td><td>2518</td><td>1457</td><td>2284</td><td>2713</td><td>1945</td><td>1840</td><td>2518</td><td>1</td><td>2518</td><td>2284</td><td>2743</td></tr>
    <tr><td>Danshuz</td><td>12.0</td><td>5.23</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>12.0</td><td>6.77</td><td></td><td></td><td></td><td>1.0</td><td></td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>2529</td><td>2569</td><td>2518</td><td>2518</td><td>2742</td><td>2518</td><td>2066</td><td>1744</td><td>2713</td><td>2439</td><td>2427</td><td>2518</td><td>2624</td><td>2752</td><td>1</td><td>2743</td></tr>
    <tr><td>Soft-Fit</td><td>19.99</td><td>12.99</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>19.99</td><td>7.0</td><td></td><td></td><td></td><td>1.0</td><td></td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>2156</td><td>1841</td><td>2518</td><td>2518</td><td>2742</td><td>2518</td><td>2066</td><td>1744</td><td>2713</td><td>2356</td><td>2423</td><td>2518</td><td>2624</td><td>2752</td><td>1</td><td>2743</td></tr>
    <tr><td>Trenway Textiles</td><td>5.2</td><td>3.28</td><td>5.2</td><td>1.92</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0.0</td><td>0.0</td><td>0.3692</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>1.9e-06</td><td>1.4e-06</td><td>5.5e-06</td><td>2719</td><td>2683</td><td>2508</td><td>2511</td><td>2742</td><td>2114</td><td>2066</td><td>2284</td><td>2713</td><td>2499</td><td>2499</td><td>2495</td><td>2066</td><td>1</td><td>2284</td><td>2713</td></tr>
    <tr><td>TAIGA</td><td>80.95</td><td>35.21</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>80.95</td><td>45.74</td><td></td><td></td><td></td><td>1.0</td><td></td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>530</td><td>626</td><td>2518</td><td>2518</td><td>2742</td><td>2518</td><td>2066</td><td>1744</td><td>2713</td><td>1773</td><td>1726</td><td>2518</td><td>2624</td><td>2752</td><td>1</td><td>2743</td></tr>
    <tr><td>NCIS</td><td>18.95</td><td>7.88</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>2238</td><td>2335</td><td>2518</td><td>2518</td><td>2742</td><td>2518</td><td>2066</td><td>2284</td><td>2575</td><td>2499</td><td>2499</td><td>2518</td><td>2624</td><td>2518</td><td>2284</td><td>1</td></tr>
    <tr><td>Steel Paisley</td><td>120.0</td><td>48.72</td><td>120.0</td><td>71.28</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0.0</td><td>0.0</td><td>0.594</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>4.46e-05</td><td>5.11e-05</td><td>5.5e-06</td><td>264</td><td>351</td><td>1535</td><td>1448</td><td>2742</td><td>2114</td><td>2066</td><td>2284</td><td>2713</td><td>2499</td><td>2499</td><td>269</td><td>2066</td><td>1</td><td>2284</td><td>2713</td></tr>
    <tr><td>marshal</td><td>0.02</td><td>0.01</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>2755</td><td>2755</td><td>2518</td><td>2518</td><td>2742</td><td>2518</td><td>2066</td><td>2284</td><td>2575</td><td>2499</td><td>2499</td><td>2518</td><td>2624</td><td>2518</td><td>2284</td><td>1</td></tr>
    <tr><td>EuroBrand</td><td>14.99</td><td>7.32</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>14.99</td><td>7.67</td><td></td><td>1.0</td><td>0.0</td><td>0.0</td><td></td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>2395</td><td>2393</td><td>2518</td><td>2518</td><td>2742</td><td>2518</td><td>1457</td><td>2284</td><td>2713</td><td>2410</td><td>2411</td><td>2518</td><td>1</td><td>2518</td><td>2284</td><td>2743</td></tr>
    <tr><td>FREEGUN</td><td>12.95</td><td>6.27</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>2503</td><td>2478</td><td>2518</td><td>2518</td><td>2742</td><td>2518</td><td>2066</td><td>2284</td><td>2575</td><td>2499</td><td>2499</td><td>2518</td><td>2624</td><td>2518</td><td>2284</td><td>1</td></tr>
    <tr><td>Easy Expression</td><td>29.99</td><td>12.39</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>1683</td><td>1919</td><td>2518</td><td>2518</td><td>2742</td><td>2518</td><td>2066</td><td>2284</td><td>2575</td><td>2499</td><td>2499</td><td>2518</td><td>2624</td><td>2518</td><td>2284</td><td>1</td></tr>
    <tr><td>VIP FASHION</td><td>15.99</td><td>6.54</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>2343</td><td>2452</td><td>2518</td><td>2518</td><td>2742</td><td>2518</td><td>2066</td><td>2284</td><td>2575</td><td>2499</td><td>2499</td><td>2518</td><td>2624</td><td>2518</td><td>2284</td><td>1</td></tr>
    <tr><td>Xscape</td><td>46.46</td><td>17.19</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>1163</td><td>1490</td><td>2518</td><td>2518</td><td>2742</td><td>2518</td><td>2066</td><td>2284</td><td>2575</td><td>2499</td><td>2499</td><td>2518</td><td>2624</td><td>2518</td><td>2284</td><td>1</td></tr>
    <tr><td>C &amp; C California</td><td>44.0</td><td>26.58</td><td>0.0</td><td>0.0</td><td>2</td><td>0</td><td>0</td><td>1</td><td>1</td><td>44.0</td><td>17.42</td><td></td><td></td><td>0.0</td><td>0.5</td><td>1.0</td><td>0.0</td><td>0.0</td><td>1.1e-05</td><td>1226</td><td>955</td><td>2518</td><td>2518</td><td>2686</td><td>2518</td><td>2066</td><td>1744</td><td>2575</td><td>2127</td><td>2219</td><td>2518</td><td>2624</td><td>2518</td><td>19</td><td>1</td></tr>
  </tbody>
</table>

</div>

<h3>Analytical Insights & Business Recommendations</h3>
<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">


<p>The lowest profit margins among top-50 revenue brands are O'Neill (45.4%), Not Your Daughter's Jeans (45.6%), Quiksilver (45.6%), and Hurley (46.4%). These are overwhelmingly surf/action sports and denim brands where product costs consume a larger share of the sale price. The denim brands specifically (True Religion at 47.5%, 7 For All Mankind at 47.5%, Joe's Jeans at 47.1%, Hudson at 46.9%) all cluster in the 46–48% margin range, suggesting that denim as a product type carries higher input costs industry-wide. Given that denim margins are structurally lower, cost reduction is the primary lever. With brands like Wrangler (1,284 orders), Levi's (1,555 orders), and 7 For All Mankind (1,086 orders) driving substantial volume, negotiate volume-based supplier discounts. The order quantities provide real leverage – present suppliers with the choice of better unit pricing or reduced shelf allocation in favor of higher-margin categories.</p>

<p>The bottom 15 brands by unit orders all have just 1 order placed (Versace, Hermanny, Danshuz, Soft-Fit, TAIGA, NCIS, EuroBrand, FREEGUN, etc.). Most generated $0 in revenue – their only orders were returned or cancelled. These brands collectively represent dead inventory and wasted catalog space. Several of these brands (Versace with $128.50 avg price, TAIGA at $80.95, Steel Paisley at $120.00) carry higher price points, meaning each failed order ties up more capital in unsold inventory. Brands with fewer than 5 lifetime orders and $0 completed revenue should be evaluated for removal. Maintaining supplier relationships, inventory allocations, and product listings for brands that generate no revenue is a net drain on operational resources. Consider stopping deals with these underperforming brands to free up bandwidth and inventory space for proven performers. These brands may also be negatively affecting the company's reputation if customers encounter low-quality products from unknown suppliers.</p>


<p>Some bottom-volume brands show strong margins and clean loss profiles when they do complete sales. VIPARO (12 orders, $759.80 revenue, 54.5% margin, 0 returns) and Fisherman (9 orders, $596 revenue, 52.6% margin, 0 returns) demonstrate that small brands can perform well when their products connect with buyers. Rather than dropping all low-volume brands indiscriminately, identify the ones with strong margins, zero returns, and reasonable completion rates. These brands may be underperforming due to lack of visibility rather than product quality issues. Targeted promotion through category-specific advertising or "featured new brand" placements could surface these hidden gems to a wider audience and test whether increased exposure drives proportional sales growth.</p>

</div>

</details>
<details>
  <summary><strong>Top Categories</strong></summary>

  <div style="margin-top: 12px;"></div>

<h3>Top categories by Revenue</h3>

<pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = 'Cancelled' THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN ('Shipped', 'Processing') THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
GROUP BY product_category
),
second_layer AS (
SELECT
  *,
  ROUND((profit / NULLIF(revenue, 0)), 4) AS profit_margin,
  ROUND(units_returned / NULLIF(units_completed + units_returned, 0), 4) AS return_rate,
  ROUND(units_completed / NULLIF(unit_orders_placed - units_cancelled, 0), 4) AS completion_rate,
  ROUND(units_cancelled / NULLIF(unit_orders_placed, 0), 4) AS cancellation_rate,
  ROUND(units_en_route / NULLIF(unit_orders_placed - (units_cancelled + units_returned), 0), 4) AS en_route_rate,
  ROUND(revenue / SUM(revenue) OVER(), 7) AS revenue_share,
  ROUND(profit / SUM(profit) OVER(), 7) AS profit_share,
  ROUND(unit_orders_placed / SUM(unit_orders_placed) OVER(), 7) AS unit_orders_placed_share
FROM first_layer
)
SELECT
  *,
  RANK() OVER(ORDER BY avg_product_sale_price DESC) AS avg_product_sale_price_rank,
  RANK() OVER(ORDER BY avg_product_cost DESC) AS avg_product_cost_rank,
  RANK() OVER(ORDER BY revenue DESC) AS revenue_rank,
  RANK() OVER(ORDER BY profit DESC) AS profit_rank,
  RANK() OVER(ORDER BY unit_orders_placed DESC) AS unit_orders_placed_rank,
  RANK() OVER(ORDER BY units_completed DESC) AS units_completed_rank,
  RANK() OVER(ORDER BY units_returned DESC) AS units_returned_rank,
  RANK() OVER(ORDER BY units_cancelled DESC) AS units_cancelled_rank,
  RANK() OVER(ORDER BY units_en_route DESC) AS units_en_route_rank,
  RANK() OVER(ORDER BY lost_revenue DESC) AS lost_revenue_rank,
  RANK() OVER(ORDER BY lost_profit DESC) AS lost_profit_rank,
  RANK() OVER(ORDER BY profit_margin DESC) AS profit_margin_rank,
  RANK() OVER(ORDER BY return_rate DESC) AS return_rate_rank,
  RANK() OVER(ORDER BY completion_rate DESC) AS completion_rate_rank,
  RANK() OVER(ORDER BY cancellation_rate DESC) AS cancellation_rate_rank,
  RANK() OVER(ORDER BY en_route_rate DESC) AS en_route_rate_rank
FROM second_layer
ORDER BY
  revenue_rank ASC
LIMIT 15;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>product_category</th>
      <th>avg_product_sale_price</th>
      <th>avg_product_cost</th>
      <th>revenue</th>
      <th>profit</th>
      <th>unit_orders_placed</th>
      <th>units_completed</th>
      <th>units_returned</th>
      <th>units_cancelled</th>
      <th>units_en_route</th>
      <th>lost_revenue</th>
      <th>lost_profit</th>
      <th>profit_margin</th>
      <th>return_rate</th>
      <th>completion_rate</th>
      <th>cancellation_rate</th>
      <th>en_route_rate</th>
      <th>revenue_share</th>
      <th>profit_share</th>
      <th>unit_orders_placed_share</th>
      <th>avg_product_sale_price_rank</th>
      <th>avg_product_cost_rank</th>
      <th>revenue_rank</th>
      <th>profit_rank</th>
      <th>unit_orders_placed_rank</th>
      <th>units_completed_rank</th>
      <th>units_returned_rank</th>
      <th>units_cancelled_rank</th>
      <th>units_en_route_rank</th>
      <th>lost_revenue_rank</th>
      <th>lost_profit_rank</th>
      <th>profit_margin_rank</th>
      <th>return_rate_rank</th>
      <th>completion_rate_rank</th>
      <th>cancellation_rate_rank</th>
      <th>en_route_rate_rank</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Outerwear &amp; Coats</td><td>146.29</td><td>65.02</td><td>339222.29</td><td>188050.56</td><td>9028</td><td>2308</td><td>862</td><td>1318</td><td>4540</td><td>322743.18</td><td>179542.92</td><td>0.5544</td><td>0.2719</td><td>0.2994</td><td>0.146</td><td>0.663</td><td>0.1260408</td><td>0.1348735</td><td>0.0498171</td><td>1</td><td>2</td><td>1</td><td>1</td><td>10</td><td>10</td><td>11</td><td>11</td><td>10</td><td>1</td><td>1</td><td>8</td><td>26</td><td>4</td><td>23</td><td>19</td></tr>
    <tr><td>Jeans</td><td>97.76</td><td>52.34</td><td>308764.08</td><td>143520.48</td><td>12655</td><td>3169</td><td>1303</td><td>1955</td><td>6228</td><td>319052.52</td><td>148299.49</td><td>0.4648</td><td>0.2914</td><td>0.2962</td><td>0.1545</td><td>0.6628</td><td>0.1147238</td><td>0.1029357</td><td>0.0698311</td><td>4</td><td>4</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>21</td><td>9</td><td>9</td><td>3</td><td>20</td></tr>
    <tr><td>Sweaters</td><td>75.46</td><td>36.32</td><td>213600.63</td><td>110714.83</td><td>11078</td><td>2792</td><td>1081</td><td>1688</td><td>5517</td><td>208115.59</td><td>107697.32</td><td>0.5183</td><td>0.2791</td><td>0.2973</td><td>0.1524</td><td>0.664</td><td>0.0793651</td><td>0.0794068</td><td>0.0611291</td><td>8</td><td>7</td><td>3</td><td>3</td><td>7</td><td>6</td><td>8</td><td>6</td><td>8</td><td>3</td><td>3</td><td>12</td><td>22</td><td>6</td><td>8</td><td>18</td></tr>
    <tr><td>Swim</td><td>57.2</td><td>28.98</td><td>156523.7</td><td>76716.71</td><td>11246</td><td>2772</td><td>1143</td><td>1660</td><td>5671</td><td>159217.24</td><td>78510.83</td><td>0.4901</td><td>0.292</td><td>0.2892</td><td>0.1476</td><td>0.6717</td><td>0.0581577</td><td>0.0550227</td><td>0.0620561</td><td>10</td><td>10</td><td>4</td><td>5</td><td>5</td><td>7</td><td>5</td><td>7</td><td>5</td><td>6</td><td>5</td><td>16</td><td>7</td><td>17</td><td>22</td><td>10</td></tr>
    <tr><td>Fashion Hoodies &amp; Sweatshirts</td><td>54.02</td><td>28.09</td><td>155933.0</td><td>74918.07</td><td>11737</td><td>2951</td><td>1191</td><td>1714</td><td>5881</td><td>159794.53</td><td>76980.63</td><td>0.4805</td><td>0.2875</td><td>0.2944</td><td>0.146</td><td>0.6659</td><td>0.0579382</td><td>0.0537327</td><td>0.0647655</td><td>12</td><td>11</td><td>5</td><td>6</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td><td>5</td><td>6</td><td>17</td><td>14</td><td>12</td><td>23</td><td>14</td></tr>
    <tr><td>Suits &amp; Sport Coats</td><td>124.74</td><td>50.03</td><td>153543.45</td><td>92034.55</td><td>5176</td><td>1255</td><td>486</td><td>790</td><td>2645</td><td>160577.15</td><td>96066.37</td><td>0.5994</td><td>0.2791</td><td>0.2861</td><td>0.1526</td><td>0.6782</td><td>0.0570503</td><td>0.066009</td><td>0.0285615</td><td>2</td><td>5</td><td>6</td><td>4</td><td>16</td><td>16</td><td>17</td><td>16</td><td>16</td><td>4</td><td>4</td><td>2</td><td>22</td><td>23</td><td>5</td><td>2</td></tr>
    <tr><td>Shorts</td><td>47.29</td><td>23.69</td><td>136510.82</td><td>68155.43</td><td>11176</td><td>2819</td><td>1130</td><td>1690</td><td>5537</td><td>134644.7</td><td>67078.36</td><td>0.4993</td><td>0.2861</td><td>0.2972</td><td>0.1512</td><td>0.6626</td><td>0.0507217</td><td>0.0488824</td><td>0.0616699</td><td>17</td><td>14</td><td>7</td><td>9</td><td>6</td><td>5</td><td>6</td><td>5</td><td>7</td><td>7</td><td>8</td><td>14</td><td>15</td><td>7</td><td>10</td><td>21</td></tr>
    <tr><td>Sleep &amp; Lounge</td><td>48.79</td><td>23.64</td><td>132101.2</td><td>68241.52</td><td>11071</td><td>2737</td><td>1128</td><td>1645</td><td>5561</td><td>134573.41</td><td>68950.32</td><td>0.5166</td><td>0.2918</td><td>0.2904</td><td>0.1486</td><td>0.6702</td><td>0.0490833</td><td>0.0489441</td><td>0.0610905</td><td>16</td><td>15</td><td>8</td><td>8</td><td>8</td><td>8</td><td>7</td><td>8</td><td>6</td><td>8</td><td>7</td><td>13</td><td>8</td><td>15</td><td>15</td><td>12</td></tr>
    <tr><td>Tops &amp; Tees</td><td>40.97</td><td>22.93</td><td>121151.89</td><td>53364.7</td><td>12000</td><td>2960</td><td>1292</td><td>1783</td><td>5965</td><td>123378.82</td><td>54313.77</td><td>0.4405</td><td>0.3039</td><td>0.2897</td><td>0.1486</td><td>0.6683</td><td>0.045015</td><td>0.0382742</td><td>0.0662168</td><td>20</td><td>16</td><td>9</td><td>14</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>9</td><td>13</td><td>22</td><td>2</td><td>16</td><td>15</td><td>13</td></tr>
    <tr><td>Intimates</td><td>33.75</td><td>17.96</td><td>118381.2</td><td>55321.28</td><td>13423</td><td>3393</td><td>1329</td><td>2044</td><td>6657</td><td>112421.97</td><td>52618.74</td><td>0.4673</td><td>0.2814</td><td>0.2982</td><td>0.1523</td><td>0.6624</td><td>0.0439855</td><td>0.0396775</td><td>0.074069</td><td>22</td><td>21</td><td>10</td><td>13</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>12</td><td>14</td><td>20</td><td>19</td><td>5</td><td>9</td><td>23</td></tr>
    <tr><td>Active</td><td>50.94</td><td>21.35</td><td>117645.45</td><td>68332.26</td><td>8932</td><td>2180</td><td>938</td><td>1362</td><td>4452</td><td>113272.89</td><td>66015.46</td><td>0.5808</td><td>0.3008</td><td>0.288</td><td>0.1525</td><td>0.6713</td><td>0.0437121</td><td>0.0490092</td><td>0.0492873</td><td>15</td><td>18</td><td>11</td><td>7</td><td>11</td><td>11</td><td>10</td><td>10</td><td>11</td><td>10</td><td>9</td><td>6</td><td>4</td><td>21</td><td>7</td><td>11</td></tr>
    <tr><td>Dresses</td><td>84.24</td><td>37.9</td><td>112895.24</td><td>62082.56</td><td>5358</td><td>1316</td><td>549</td><td>792</td><td>2701</td><td>113022.02</td><td>62283.44</td><td>0.5499</td><td>0.2944</td><td>0.2882</td><td>0.1478</td><td>0.6724</td><td>0.0419471</td><td>0.0445268</td><td>0.0295658</td><td>7</td><td>6</td><td>12</td><td>10</td><td>15</td><td>15</td><td>15</td><td>15</td><td>15</td><td>11</td><td>10</td><td>9</td><td>6</td><td>20</td><td>21</td><td>9</td></tr>
    <tr><td>Pants</td><td>59.65</td><td>27.35</td><td>106719.7</td><td>57634.8</td><td>7239</td><td>1823</td><td>713</td><td>1076</td><td>3627</td><td>106167.82</td><td>57611.26</td><td>0.5401</td><td>0.2812</td><td>0.2958</td><td>0.1486</td><td>0.6655</td><td>0.0396526</td><td>0.0413368</td><td>0.0399453</td><td>9</td><td>12</td><td>13</td><td>12</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>12</td><td>10</td><td>21</td><td>10</td><td>15</td><td>16</td></tr>
    <tr><td>Accessories</td><td>42.05</td><td>16.85</td><td>99096.96</td><td>59262.83</td><td>9813</td><td>2384</td><td>967</td><td>1497</td><td>4965</td><td>103385.5</td><td>62000.28</td><td>0.598</td><td>0.2886</td><td>0.2867</td><td>0.1526</td><td>0.6756</td><td>0.0368203</td><td>0.0425044</td><td>0.0541488</td><td>19</td><td>22</td><td>14</td><td>11</td><td>9</td><td>9</td><td>9</td><td>9</td><td>9</td><td>14</td><td>11</td><td>5</td><td>12</td><td>22</td><td>5</td><td>5</td></tr>
    <tr><td>Blazers &amp; Jackets</td><td>90.68</td><td>34.35</td><td>65986.31</td><td>40954.92</td><td>3194</td><td>745</td><td>334</td><td>506</td><td>1609</td><td>76039.51</td><td>47305.1</td><td>0.6207</td><td>0.3095</td><td>0.2772</td><td>0.1584</td><td>0.6835</td><td>0.0245178</td><td>0.0293737</td><td>0.0176247</td><td>5</td><td>8</td><td>15</td><td>15</td><td>22</td><td>22</td><td>22</td><td>20</td><td>21</td><td>15</td><td>15</td><td>1</td><td>1</td><td>26</td><td>1</td><td>1</td></tr>
  </tbody>
</table>

</div>

<h3>Top categories by Profit Margin</h3>

<pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = 'Cancelled' THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN ('Shipped', 'Processing') THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
GROUP BY product_category
),
second_layer AS (
SELECT
  *,
  ROUND((profit / NULLIF(revenue, 0)), 4) AS profit_margin,
  ROUND(units_returned / NULLIF(units_completed + units_returned, 0), 4) AS return_rate,
  ROUND(units_completed / NULLIF(unit_orders_placed - units_cancelled, 0), 4) AS completion_rate,
  ROUND(units_cancelled / NULLIF(unit_orders_placed, 0), 4) AS cancellation_rate,
  ROUND(units_en_route / NULLIF(unit_orders_placed - (units_cancelled + units_returned), 0), 4) AS en_route_rate,
  ROUND(revenue / SUM(revenue) OVER(), 7) AS revenue_share,
  ROUND(profit / SUM(profit) OVER(), 7) AS profit_share,
  ROUND(unit_orders_placed / SUM(unit_orders_placed) OVER(), 7) AS unit_orders_placed_share
FROM first_layer
)
SELECT
  *,
  RANK() OVER(ORDER BY avg_product_sale_price DESC) AS avg_product_sale_price_rank,
  RANK() OVER(ORDER BY avg_product_cost DESC) AS avg_product_cost_rank,
  RANK() OVER(ORDER BY revenue DESC) AS revenue_rank,
  RANK() OVER(ORDER BY profit DESC) AS profit_rank,
  RANK() OVER(ORDER BY unit_orders_placed DESC) AS unit_orders_placed_rank,
  RANK() OVER(ORDER BY units_completed DESC) AS units_completed_rank,
  RANK() OVER(ORDER BY units_returned DESC) AS units_returned_rank,
  RANK() OVER(ORDER BY units_cancelled DESC) AS units_cancelled_rank,
  RANK() OVER(ORDER BY units_en_route DESC) AS units_en_route_rank,
  RANK() OVER(ORDER BY lost_revenue DESC) AS lost_revenue_rank,
  RANK() OVER(ORDER BY lost_profit DESC) AS lost_profit_rank,
  RANK() OVER(ORDER BY profit_margin DESC) AS profit_margin_rank,
  RANK() OVER(ORDER BY return_rate DESC) AS return_rate_rank,
  RANK() OVER(ORDER BY completion_rate DESC) AS completion_rate_rank,
  RANK() OVER(ORDER BY cancellation_rate DESC) AS cancellation_rate_rank,
  RANK() OVER(ORDER BY en_route_rate DESC) AS en_route_rate_rank
FROM second_layer
ORDER BY
  profit_margin_rank ASC
LIMIT 15;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>product_category</th>
      <th>avg_product_sale_price</th>
      <th>avg_product_cost</th>
      <th>revenue</th>
      <th>profit</th>
      <th>unit_orders_placed</th>
      <th>units_completed</th>
      <th>units_returned</th>
      <th>units_cancelled</th>
      <th>units_en_route</th>
      <th>lost_revenue</th>
      <th>lost_profit</th>
      <th>profit_margin</th>
      <th>return_rate</th>
      <th>completion_rate</th>
      <th>cancellation_rate</th>
      <th>en_route_rate</th>
      <th>revenue_share</th>
      <th>profit_share</th>
      <th>unit_orders_placed_share</th>
      <th>avg_product_sale_price_rank</th>
      <th>avg_product_cost_rank</th>
      <th>revenue_rank</th>
      <th>profit_rank</th>
      <th>unit_orders_placed_rank</th>
      <th>units_completed_rank</th>
      <th>units_returned_rank</th>
      <th>units_cancelled_rank</th>
      <th>units_en_route_rank</th>
      <th>lost_revenue_rank</th>
      <th>lost_profit_rank</th>
      <th>profit_margin_rank</th>
      <th>return_rate_rank</th>
      <th>completion_rate_rank</th>
      <th>cancellation_rate_rank</th>
      <th>en_route_rate_rank</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Blazers &amp; Jackets</td><td>90.68</td><td>34.35</td><td>65986.31</td><td>40954.92</td><td>3194</td><td>745</td><td>334</td><td>506</td><td>1609</td><td>76039.51</td><td>47305.1</td><td>0.6207</td><td>0.3095</td><td>0.2772</td><td>0.1584</td><td>0.6835</td><td>0.0245178</td><td>0.0293737</td><td>0.0176247</td><td>5</td><td>8</td><td>15</td><td>15</td><td>22</td><td>22</td><td>22</td><td>20</td><td>21</td><td>15</td><td>15</td><td>1</td><td>1</td><td>26</td><td>1</td><td>1</td></tr>
    <tr><td>Suits &amp; Sport Coats</td><td>124.74</td><td>50.03</td><td>153543.45</td><td>92034.55</td><td>5176</td><td>1255</td><td>486</td><td>790</td><td>2645</td><td>160577.15</td><td>96066.37</td><td>0.5994</td><td>0.2791</td><td>0.2861</td><td>0.1526</td><td>0.6782</td><td>0.0570503</td><td>0.066009</td><td>0.0285615</td><td>2</td><td>5</td><td>6</td><td>4</td><td>16</td><td>16</td><td>17</td><td>16</td><td>16</td><td>4</td><td>4</td><td>2</td><td>22</td><td>23</td><td>5</td><td>2</td></tr>
    <tr><td>Socks &amp; Hosiery</td><td>16.81</td><td>6.75</td><td>15695.27</td><td>9398.63</td><td>3821</td><td>929</td><td>372</td><td>566</td><td>1954</td><td>15784.16</td><td>9453.9</td><td>0.5988</td><td>0.2859</td><td>0.2854</td><td>0.1481</td><td>0.6778</td><td>0.0058317</td><td>0.0067409</td><td>0.0210845</td><td>26</td><td>26</td><td>24</td><td>23</td><td>19</td><td>19</td><td>19</td><td>19</td><td>19</td><td>24</td><td>23</td><td>3</td><td>16</td><td>24</td><td>20</td><td>3</td></tr>
    <tr><td>Skirts</td><td>52.13</td><td>20.8</td><td>26843.42</td><td>16061.8</td><td>2087</td><td>539</td><td>208</td><td>314</td><td>1026</td><td>27751.21</td><td>16709.53</td><td>0.5984</td><td>0.2784</td><td>0.304</td><td>0.1505</td><td>0.6556</td><td>0.0099739</td><td>0.0115198</td><td>0.0115162</td><td>13</td><td>19</td><td>22</td><td>20</td><td>23</td><td>23</td><td>23</td><td>23</td><td>23</td><td>22</td><td>20</td><td>4</td><td>24</td><td>2</td><td>11</td><td>25</td></tr>
    <tr><td>Accessories</td><td>42.05</td><td>16.85</td><td>99096.96</td><td>59262.83</td><td>9813</td><td>2384</td><td>967</td><td>1497</td><td>4965</td><td>103385.5</td><td>62000.28</td><td>0.598</td><td>0.2886</td><td>0.2867</td><td>0.1526</td><td>0.6756</td><td>0.0368203</td><td>0.0425044</td><td>0.0541488</td><td>19</td><td>22</td><td>14</td><td>11</td><td>9</td><td>9</td><td>9</td><td>9</td><td>9</td><td>14</td><td>11</td><td>5</td><td>12</td><td>22</td><td>5</td><td>5</td></tr>
    <tr><td>Active</td><td>50.94</td><td>21.35</td><td>117645.45</td><td>68332.26</td><td>8932</td><td>2180</td><td>938</td><td>1362</td><td>4452</td><td>113272.89</td><td>66015.46</td><td>0.5808</td><td>0.3008</td><td>0.288</td><td>0.1525</td><td>0.6713</td><td>0.0437121</td><td>0.0490092</td><td>0.0492873</td><td>15</td><td>18</td><td>11</td><td>7</td><td>11</td><td>11</td><td>10</td><td>10</td><td>11</td><td>10</td><td>9</td><td>6</td><td>4</td><td>21</td><td>7</td><td>11</td></tr>
    <tr><td>Maternity</td><td>51.5</td><td>22.73</td><td>63613.6</td><td>35563.76</td><td>5086</td><td>1232</td><td>531</td><td>741</td><td>2582</td><td>61413.18</td><td>34274.78</td><td>0.5591</td><td>0.3012</td><td>0.2835</td><td>0.1457</td><td>0.677</td><td>0.0236362</td><td>0.025507</td><td>0.0280649</td><td>14</td><td>17</td><td>16</td><td>16</td><td>17</td><td>17</td><td>16</td><td>17</td><td>17</td><td>16</td><td>16</td><td>7</td><td>3</td><td>25</td><td>25</td><td>4</td></tr>
    <tr><td>Outerwear &amp; Coats</td><td>146.29</td><td>65.02</td><td>339222.29</td><td>188050.56</td><td>9028</td><td>2308</td><td>862</td><td>1318</td><td>4540</td><td>322743.18</td><td>179542.92</td><td>0.5544</td><td>0.2719</td><td>0.2994</td><td>0.146</td><td>0.663</td><td>0.1260408</td><td>0.1348735</td><td>0.0498171</td><td>1</td><td>2</td><td>1</td><td>1</td><td>10</td><td>10</td><td>11</td><td>11</td><td>10</td><td>1</td><td>1</td><td>8</td><td>26</td><td>4</td><td>23</td><td>19</td></tr>
    <tr><td>Dresses</td><td>84.24</td><td>37.9</td><td>112895.24</td><td>62082.56</td><td>5358</td><td>1316</td><td>549</td><td>792</td><td>2701</td><td>113022.02</td><td>62283.44</td><td>0.5499</td><td>0.2944</td><td>0.2882</td><td>0.1478</td><td>0.6724</td><td>0.0419471</td><td>0.0445268</td><td>0.0295658</td><td>7</td><td>6</td><td>12</td><td>10</td><td>15</td><td>15</td><td>15</td><td>15</td><td>15</td><td>11</td><td>10</td><td>9</td><td>6</td><td>20</td><td>21</td><td>9</td></tr>
    <tr><td>Pants</td><td>59.65</td><td>27.35</td><td>106719.7</td><td>57634.8</td><td>7239</td><td>1823</td><td>713</td><td>1076</td><td>3627</td><td>106167.82</td><td>57611.26</td><td>0.5401</td><td>0.2812</td><td>0.2958</td><td>0.1486</td><td>0.6655</td><td>0.0396526</td><td>0.0413368</td><td>0.0399453</td><td>9</td><td>12</td><td>13</td><td>12</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>12</td><td>10</td><td>21</td><td>10</td><td>15</td><td>16</td></tr>
    <tr><td>Underwear</td><td>27.21</td><td>12.79</td><td>50614.6</td><td>26861.36</td><td>7505</td><td>1886</td><td>738</td><td>1122</td><td>3759</td><td>51345.06</td><td>27197.18</td><td>0.5307</td><td>0.2813</td><td>0.2955</td><td>0.1495</td><td>0.6659</td><td>0.0188063</td><td>0.0192655</td><td>0.0414131</td><td>23</td><td>24</td><td>17</td><td>17</td><td>12</td><td>12</td><td>12</td><td>12</td><td>12</td><td>17</td><td>17</td><td>11</td><td>20</td><td>11</td><td>13</td><td>14</td></tr>
    <tr><td>Sweaters</td><td>75.46</td><td>36.32</td><td>213600.63</td><td>110714.83</td><td>11078</td><td>2792</td><td>1081</td><td>1688</td><td>5517</td><td>208115.59</td><td>107697.32</td><td>0.5183</td><td>0.2791</td><td>0.2973</td><td>0.1524</td><td>0.664</td><td>0.0793651</td><td>0.0794068</td><td>0.0611291</td><td>8</td><td>7</td><td>3</td><td>3</td><td>7</td><td>6</td><td>8</td><td>6</td><td>8</td><td>3</td><td>3</td><td>12</td><td>22</td><td>6</td><td>8</td><td>18</td></tr>
    <tr><td>Sleep &amp; Lounge</td><td>48.79</td><td>23.64</td><td>132101.2</td><td>68241.52</td><td>11071</td><td>2737</td><td>1128</td><td>1645</td><td>5561</td><td>134573.41</td><td>68950.32</td><td>0.5166</td><td>0.2918</td><td>0.2904</td><td>0.1486</td><td>0.6702</td><td>0.0490833</td><td>0.0489441</td><td>0.0610905</td><td>16</td><td>15</td><td>8</td><td>8</td><td>8</td><td>8</td><td>7</td><td>8</td><td>6</td><td>8</td><td>7</td><td>13</td><td>8</td><td>15</td><td>15</td><td>12</td></tr>
    <tr><td>Shorts</td><td>47.29</td><td>23.69</td><td>136510.82</td><td>68155.43</td><td>11176</td><td>2819</td><td>1130</td><td>1690</td><td>5537</td><td>134644.7</td><td>67078.36</td><td>0.4993</td><td>0.2861</td><td>0.2972</td><td>0.1512</td><td>0.6626</td><td>0.0507217</td><td>0.0488824</td><td>0.0616699</td><td>17</td><td>14</td><td>7</td><td>9</td><td>6</td><td>5</td><td>6</td><td>5</td><td>7</td><td>7</td><td>8</td><td>14</td><td>15</td><td>7</td><td>10</td><td>21</td></tr>
    <tr><td>Plus</td><td>39.47</td><td>19.84</td><td>44807.01</td><td>22316.68</td><td>4358</td><td>1070</td><td>436</td><td>646</td><td>2206</td><td>42048.64</td><td>21041.57</td><td>0.4981</td><td>0.2895</td><td>0.2883</td><td>0.1482</td><td>0.6734</td><td>0.0166484</td><td>0.016006</td><td>0.0240477</td><td>21</td><td>20</td><td>19</td><td>19</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>15</td><td>11</td><td>19</td><td>19</td><td>6</td></tr>
  </tbody>
</table>

</div>

<h3>Top categories by Return Rate</h3>

<pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = 'Cancelled' THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN ('Shipped', 'Processing') THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
GROUP BY product_category
),
second_layer AS (
SELECT
  *,
  ROUND((profit / NULLIF(revenue, 0)), 4) AS profit_margin,
  ROUND(units_returned / NULLIF(units_completed + units_returned, 0), 4) AS return_rate,
  ROUND(units_completed / NULLIF(unit_orders_placed - units_cancelled, 0), 4) AS completion_rate,
  ROUND(units_cancelled / NULLIF(unit_orders_placed, 0), 4) AS cancellation_rate,
  ROUND(units_en_route / NULLIF(unit_orders_placed - (units_cancelled + units_returned), 0), 4) AS en_route_rate,
  ROUND(revenue / SUM(revenue) OVER(), 7) AS revenue_share,
  ROUND(profit / SUM(profit) OVER(), 7) AS profit_share,
  ROUND(unit_orders_placed / SUM(unit_orders_placed) OVER(), 7) AS unit_orders_placed_share
FROM first_layer
)
SELECT
  *,
  RANK() OVER(ORDER BY avg_product_sale_price DESC) AS avg_product_sale_price_rank,
  RANK() OVER(ORDER BY avg_product_cost DESC) AS avg_product_cost_rank,
  RANK() OVER(ORDER BY revenue DESC) AS revenue_rank,
  RANK() OVER(ORDER BY profit DESC) AS profit_rank,
  RANK() OVER(ORDER BY unit_orders_placed DESC) AS unit_orders_placed_rank,
  RANK() OVER(ORDER BY units_completed DESC) AS units_completed_rank,
  RANK() OVER(ORDER BY units_returned DESC) AS units_returned_rank,
  RANK() OVER(ORDER BY units_cancelled DESC) AS units_cancelled_rank,
  RANK() OVER(ORDER BY units_en_route DESC) AS units_en_route_rank,
  RANK() OVER(ORDER BY lost_revenue DESC) AS lost_revenue_rank,
  RANK() OVER(ORDER BY lost_profit DESC) AS lost_profit_rank,
  RANK() OVER(ORDER BY profit_margin DESC) AS profit_margin_rank,
  RANK() OVER(ORDER BY return_rate DESC) AS return_rate_rank,
  RANK() OVER(ORDER BY completion_rate DESC) AS completion_rate_rank,
  RANK() OVER(ORDER BY cancellation_rate DESC) AS cancellation_rate_rank,
  RANK() OVER(ORDER BY en_route_rate DESC) AS en_route_rate_rank
FROM second_layer
ORDER BY
  return_rate_rank ASC
LIMIT 15;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>product_category</th>
      <th>avg_product_sale_price</th>
      <th>avg_product_cost</th>
      <th>revenue</th>
      <th>profit</th>
      <th>unit_orders_placed</th>
      <th>units_completed</th>
      <th>units_returned</th>
      <th>units_cancelled</th>
      <th>units_en_route</th>
      <th>lost_revenue</th>
      <th>lost_profit</th>
      <th>profit_margin</th>
      <th>return_rate</th>
      <th>completion_rate</th>
      <th>cancellation_rate</th>
      <th>en_route_rate</th>
      <th>revenue_share</th>
      <th>profit_share</th>
      <th>unit_orders_placed_share</th>
      <th>avg_product_sale_price_rank</th>
      <th>avg_product_cost_rank</th>
      <th>revenue_rank</th>
      <th>profit_rank</th>
      <th>unit_orders_placed_rank</th>
      <th>units_completed_rank</th>
      <th>units_returned_rank</th>
      <th>units_cancelled_rank</th>
      <th>units_en_route_rank</th>
      <th>lost_revenue_rank</th>
      <th>lost_profit_rank</th>
      <th>profit_margin_rank</th>
      <th>return_rate_rank</th>
      <th>completion_rate_rank</th>
      <th>cancellation_rate_rank</th>
      <th>en_route_rate_rank</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Blazers &amp; Jackets</td><td>90.68</td><td>34.35</td><td>65986.31</td><td>40954.92</td><td>3194</td><td>745</td><td>334</td><td>506</td><td>1609</td><td>76039.51</td><td>47305.1</td><td>0.6207</td><td>0.3095</td><td>0.2772</td><td>0.1584</td><td>0.6835</td><td>0.0245178</td><td>0.0293737</td><td>0.0176247</td><td>5</td><td>8</td><td>15</td><td>15</td><td>22</td><td>22</td><td>22</td><td>20</td><td>21</td><td>15</td><td>15</td><td>1</td><td>1</td><td>26</td><td>1</td><td>1</td></tr>
    <tr><td>Tops &amp; Tees</td><td>40.97</td><td>22.93</td><td>121151.89</td><td>53364.7</td><td>12000</td><td>2960</td><td>1292</td><td>1783</td><td>5965</td><td>123378.82</td><td>54313.77</td><td>0.4405</td><td>0.3039</td><td>0.2897</td><td>0.1486</td><td>0.6683</td><td>0.045015</td><td>0.0382742</td><td>0.0662168</td><td>20</td><td>16</td><td>9</td><td>14</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>9</td><td>13</td><td>22</td><td>2</td><td>16</td><td>15</td><td>13</td></tr>
    <tr><td>Maternity</td><td>51.5</td><td>22.73</td><td>63613.6</td><td>35563.76</td><td>5086</td><td>1232</td><td>531</td><td>741</td><td>2582</td><td>61413.18</td><td>34274.78</td><td>0.5591</td><td>0.3012</td><td>0.2835</td><td>0.1457</td><td>0.677</td><td>0.0236362</td><td>0.025507</td><td>0.0280649</td><td>14</td><td>17</td><td>16</td><td>16</td><td>17</td><td>17</td><td>16</td><td>17</td><td>17</td><td>16</td><td>16</td><td>7</td><td>3</td><td>25</td><td>25</td><td>4</td></tr>
    <tr><td>Active</td><td>50.94</td><td>21.35</td><td>117645.45</td><td>68332.26</td><td>8932</td><td>2180</td><td>938</td><td>1362</td><td>4452</td><td>113272.89</td><td>66015.46</td><td>0.5808</td><td>0.3008</td><td>0.288</td><td>0.1525</td><td>0.6713</td><td>0.0437121</td><td>0.0490092</td><td>0.0492873</td><td>15</td><td>18</td><td>11</td><td>7</td><td>11</td><td>11</td><td>10</td><td>10</td><td>11</td><td>10</td><td>9</td><td>6</td><td>4</td><td>21</td><td>7</td><td>11</td></tr>
    <tr><td>Leggings</td><td>26.79</td><td>16.07</td><td>22032.86</td><td>8796.32</td><td>3246</td><td>804</td><td>345</td><td>500</td><td>1597</td><td>22344.1</td><td>8926.78</td><td>0.3992</td><td>0.3003</td><td>0.2928</td><td>0.154</td><td>0.6651</td><td>0.0081865</td><td>0.0063089</td><td>0.0179116</td><td>24</td><td>23</td><td>23</td><td>24</td><td>21</td><td>21</td><td>21</td><td>21</td><td>22</td><td>23</td><td>24</td><td>23</td><td>5</td><td>13</td><td>4</td><td>17</td></tr>
    <tr><td>Dresses</td><td>84.24</td><td>37.9</td><td>112895.24</td><td>62082.56</td><td>5358</td><td>1316</td><td>549</td><td>792</td><td>2701</td><td>113022.02</td><td>62283.44</td><td>0.5499</td><td>0.2944</td><td>0.2882</td><td>0.1478</td><td>0.6724</td><td>0.0419471</td><td>0.0445268</td><td>0.0295658</td><td>7</td><td>6</td><td>12</td><td>10</td><td>15</td><td>15</td><td>15</td><td>15</td><td>15</td><td>11</td><td>10</td><td>9</td><td>6</td><td>20</td><td>21</td><td>9</td></tr>
    <tr><td>Swim</td><td>57.2</td><td>28.98</td><td>156523.7</td><td>76716.71</td><td>11246</td><td>2772</td><td>1143</td><td>1660</td><td>5671</td><td>159217.24</td><td>78510.83</td><td>0.4901</td><td>0.292</td><td>0.2892</td><td>0.1476</td><td>0.6717</td><td>0.0581577</td><td>0.0550227</td><td>0.0620561</td><td>10</td><td>10</td><td>4</td><td>5</td><td>5</td><td>7</td><td>5</td><td>7</td><td>5</td><td>6</td><td>5</td><td>16</td><td>7</td><td>17</td><td>22</td><td>10</td></tr>
    <tr><td>Sleep &amp; Lounge</td><td>48.79</td><td>23.64</td><td>132101.2</td><td>68241.52</td><td>11071</td><td>2737</td><td>1128</td><td>1645</td><td>5561</td><td>134573.41</td><td>68950.32</td><td>0.5166</td><td>0.2918</td><td>0.2904</td><td>0.1486</td><td>0.6702</td><td>0.0490833</td><td>0.0489441</td><td>0.0610905</td><td>16</td><td>15</td><td>8</td><td>8</td><td>8</td><td>8</td><td>7</td><td>8</td><td>6</td><td>8</td><td>7</td><td>13</td><td>8</td><td>15</td><td>15</td><td>12</td></tr>
    <tr><td>Jeans</td><td>97.76</td><td>52.34</td><td>308764.08</td><td>143520.48</td><td>12655</td><td>3169</td><td>1303</td><td>1955</td><td>6228</td><td>319052.52</td><td>148299.49</td><td>0.4648</td><td>0.2914</td><td>0.2962</td><td>0.1545</td><td>0.6628</td><td>0.1147238</td><td>0.1029357</td><td>0.0698311</td><td>4</td><td>4</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>21</td><td>9</td><td>9</td><td>3</td><td>20</td></tr>
    <tr><td>Socks</td><td>21.13</td><td>12.76</td><td>31572.07</td><td>12517.44</td><td>6329</td><td>1557</td><td>636</td><td>939</td><td>3197</td><td>32927.59</td><td>13032.11</td><td>0.3965</td><td>0.29</td><td>0.2889</td><td>0.1484</td><td>0.6725</td><td>0.0117309</td><td>0.0089777</td><td>0.0349238</td><td>25</td><td>25</td><td>21</td><td>22</td><td>14</td><td>14</td><td>14</td><td>14</td><td>14</td><td>20</td><td>21</td><td>24</td><td>10</td><td>18</td><td>18</td><td>8</td></tr>
    <tr><td>Plus</td><td>39.47</td><td>19.84</td><td>44807.01</td><td>22316.68</td><td>4358</td><td>1070</td><td>436</td><td>646</td><td>2206</td><td>42048.64</td><td>21041.57</td><td>0.4981</td><td>0.2895</td><td>0.2883</td><td>0.1482</td><td>0.6734</td><td>0.0166484</td><td>0.016006</td><td>0.0240477</td><td>21</td><td>20</td><td>19</td><td>19</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>15</td><td>11</td><td>19</td><td>19</td><td>6</td></tr>
    <tr><td>Accessories</td><td>42.05</td><td>16.85</td><td>99096.96</td><td>59262.83</td><td>9813</td><td>2384</td><td>967</td><td>1497</td><td>4965</td><td>103385.5</td><td>62000.28</td><td>0.598</td><td>0.2886</td><td>0.2867</td><td>0.1526</td><td>0.6756</td><td>0.0368203</td><td>0.0425044</td><td>0.0541488</td><td>19</td><td>22</td><td>14</td><td>11</td><td>9</td><td>9</td><td>9</td><td>9</td><td>9</td><td>14</td><td>11</td><td>5</td><td>12</td><td>22</td><td>5</td><td>5</td></tr>
    <tr><td>Pants &amp; Capris</td><td>55.37</td><td>29.2</td><td>49331.52</td><td>23421.93</td><td>3392</td><td>864</td><td>350</td><td>481</td><td>1697</td><td>41999.86</td><td>19777.56</td><td>0.4748</td><td>0.2883</td><td>0.2968</td><td>0.1418</td><td>0.6626</td><td>0.0183295</td><td>0.0167987</td><td>0.0187173</td><td>11</td><td>9</td><td>18</td><td>18</td><td>20</td><td>20</td><td>20</td><td>22</td><td>20</td><td>19</td><td>19</td><td>18</td><td>13</td><td>8</td><td>26</td><td>21</td></tr>
    <tr><td>Fashion Hoodies &amp; Sweatshirts</td><td>54.02</td><td>28.09</td><td>155933.0</td><td>74918.07</td><td>11737</td><td>2951</td><td>1191</td><td>1714</td><td>5881</td><td>159794.53</td><td>76980.63</td><td>0.4805</td><td>0.2875</td><td>0.2944</td><td>0.146</td><td>0.6659</td><td>0.0579382</td><td>0.0537327</td><td>0.0647655</td><td>12</td><td>11</td><td>5</td><td>6</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td><td>5</td><td>6</td><td>17</td><td>14</td><td>12</td><td>23</td><td>14</td></tr>
    <tr><td>Shorts</td><td>47.29</td><td>23.69</td><td>136510.82</td><td>68155.43</td><td>11176</td><td>2819</td><td>1130</td><td>1690</td><td>5537</td><td>134644.7</td><td>67078.36</td><td>0.4993</td><td>0.2861</td><td>0.2972</td><td>0.1512</td><td>0.6626</td><td>0.0507217</td><td>0.0488824</td><td>0.0616699</td><td>17</td><td>14</td><td>7</td><td>9</td><td>6</td><td>5</td><td>6</td><td>5</td><td>7</td><td>7</td><td>8</td><td>14</td><td>15</td><td>7</td><td>10</td><td>21</td></tr>
  </tbody>
</table>

</div>

<h3>Analytical Insights & Business Recommendations</h3>
<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p>Outerwear & Coats is the clear category leader with $339,222.29 in revenue and $188,050.56 in profit – both #1 overall. However, it achieves this with only 9,028 unit orders (rank #10), meaning it generates far more revenue per unit than any other category thanks to its $146.29 average sale price, the highest across all 26 categories. With a 55.4% profit margin, Outerwear & Coats also ranks above the median for margin efficiency. Its return rate of 27.2% is actually the lowest among all categories, suggesting that customers purchasing outerwear are more deliberate and satisfied with their purchases. Outerwear is the profit engine of the business. Increase internal inventory allocation, marketing spend, and priority fulfillment resources for this category. Ensure stockouts are prevented – each lost outerwear sale costs an average of $146.29 in revenue and $81.30 in profit, far exceeding the cost of overstocking. Additionally, this category's demand likely peaks seasonally before and during winter months, so inventory orders should be front-loaded accordingly.</p>

<p>Intimates leads all categories in unit orders (13,423) but ranks #10 in revenue ($118,381.20) due to its low average sale price of $33.75. Conversely, Suits & Sport Coats ranks #16 in unit orders (5,176) but #4 in profit ($92,034.55) thanks to its $124.74 average sale price and 59.9% profit margin. This pattern – high-volume/low-revenue vs. low-volume/high-revenue – is consistent across the category landscape. Tops & Tees, Intimates, and Fashion Hoodies move the most units but contribute less to profit per order. For high-volume, low-revenue categories (Intimates, Tops & Tees, Shorts), operational efficiency is paramount. Streamline fulfillment for these items – batch picking, simplified packaging, automated label generation – since the margin per unit is thin and any fulfillment inefficiency eats into profit. For low-volume, high-revenue categories (Suits & Sport Coats, Outerwear), invest in premium fulfillment and quality packaging to protect the customer experience on high-value purchases.</p>

<p>Blazers & Jackets commands the highest profit margin (62.1%) across all categories, despite ranking only #15 in revenue and #22 in unit orders. This means every dollar of blazer revenue retains $0.62 in profit – nearly 50% more efficient than bottom-margin categories like Socks (39.7%) or Clothing Sets (38.5%). Accessories (59.8% margin), Socks & Hosiery (59.9%), and Suits & Sport Coats (59.9%) form a tier of high-margin categories. Notably, Socks & Hosiery achieves a top-3 margin despite the lowest average sale price ($16.81) – meaning the cost-to-price ratio is extremely favorable even at low price points. Strategically promote high-margin categories through targeted advertising. A $1 increase in Blazers & Jackets demand yields $0.62 in profit vs. $0.44 for Tops & Tees. Cross-sell blazers and accessories when customers are browsing jeans or outerwear. For Socks & Hosiery, the near-60% margin on a $16 product suggests significant untapped potential if volume can be increased – consider featuring them as add-on recommendations at checkout.</p>

<p>Category return rates are remarkably tight, ranging from 27.2% (Outerwear & Coats) to 31.0% (Blazers & Jackets). The ~4 percentage point spread across all 26 categories suggests that returns are driven more by systemic business factors (e.g., return policy leniency, shipping delays, overall site UX) than by category-specific product quality. Blazers & Jackets has both the highest margin (62.1%) and the highest return rate (31.0%), which may seem contradictory but reflects the category's nature – fit-dependent items where customers may order multiple sizes. Since return rates are uniformly high across all categories (all above 27%), invest in platform-wide return reduction strategies rather than category-specific ones: improved sizing tools, better product photography, clearer product descriptions, and potentially a try-before-you-buy or virtual fitting room feature. A 2-point reduction in the business-wide return rate would compound into significant recovered revenue across all categories.</p>



</div>

</details>
<details>
  <summary><strong>Bottom Categories</strong></summary>

  <div style="margin-top: 12px;"></div>

<h3>Bottom categories by Revenue</h3>

<pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = 'Cancelled' THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN ('Shipped', 'Processing') THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN ('Returned', 'Cancelled') THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
GROUP BY product_category
),
second_layer AS (
SELECT
  *,
  ROUND((profit / NULLIF(revenue, 0)), 4) AS profit_margin,
  ROUND(units_returned / NULLIF(units_completed + units_returned, 0), 4) AS return_rate,
  ROUND(units_completed / NULLIF(unit_orders_placed - units_cancelled, 0), 4) AS completion_rate,
  ROUND(units_cancelled / NULLIF(unit_orders_placed, 0), 4) AS cancellation_rate,
  ROUND(units_en_route / NULLIF(unit_orders_placed - (units_cancelled + units_returned), 0), 4) AS en_route_rate,
  ROUND(revenue / SUM(revenue) OVER(), 7) AS revenue_share,
  ROUND(profit / SUM(profit) OVER(), 7) AS profit_share,
  ROUND(unit_orders_placed / SUM(unit_orders_placed) OVER(), 7) AS unit_orders_placed_share
FROM first_layer
)
SELECT
  *,
  RANK() OVER(ORDER BY avg_product_sale_price DESC) AS avg_product_sale_price_rank,
  RANK() OVER(ORDER BY avg_product_cost DESC) AS avg_product_cost_rank,
  RANK() OVER(ORDER BY revenue DESC) AS revenue_rank,
  RANK() OVER(ORDER BY profit DESC) AS profit_rank,
  RANK() OVER(ORDER BY unit_orders_placed DESC) AS unit_orders_placed_rank,
  RANK() OVER(ORDER BY units_completed DESC) AS units_completed_rank,
  RANK() OVER(ORDER BY units_returned DESC) AS units_returned_rank,
  RANK() OVER(ORDER BY units_cancelled DESC) AS units_cancelled_rank,
  RANK() OVER(ORDER BY units_en_route DESC) AS units_en_route_rank,
  RANK() OVER(ORDER BY lost_revenue DESC) AS lost_revenue_rank,
  RANK() OVER(ORDER BY lost_profit DESC) AS lost_profit_rank,
  RANK() OVER(ORDER BY profit_margin DESC) AS profit_margin_rank,
  RANK() OVER(ORDER BY return_rate DESC) AS return_rate_rank,
  RANK() OVER(ORDER BY completion_rate DESC) AS completion_rate_rank,
  RANK() OVER(ORDER BY cancellation_rate DESC) AS cancellation_rate_rank,
  RANK() OVER(ORDER BY en_route_rate DESC) AS en_route_rate_rank
FROM second_layer
ORDER BY
  revenue_rank DESC
LIMIT 15;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>product_category</th>
      <th>avg_product_sale_price</th>
      <th>avg_product_cost</th>
      <th>revenue</th>
      <th>profit</th>
      <th>unit_orders_placed</th>
      <th>units_completed</th>
      <th>units_returned</th>
      <th>units_cancelled</th>
      <th>units_en_route</th>
      <th>lost_revenue</th>
      <th>lost_profit</th>
      <th>profit_margin</th>
      <th>return_rate</th>
      <th>completion_rate</th>
      <th>cancellation_rate</th>
      <th>en_route_rate</th>
      <th>revenue_share</th>
      <th>profit_share</th>
      <th>unit_orders_placed_share</th>
      <th>avg_product_sale_price_rank</th>
      <th>avg_product_cost_rank</th>
      <th>revenue_rank</th>
      <th>profit_rank</th>
      <th>unit_orders_placed_rank</th>
      <th>units_completed_rank</th>
      <th>units_returned_rank</th>
      <th>units_cancelled_rank</th>
      <th>units_en_route_rank</th>
      <th>lost_revenue_rank</th>
      <th>lost_profit_rank</th>
      <th>profit_margin_rank</th>
      <th>return_rate_rank</th>
      <th>completion_rate_rank</th>
      <th>cancellation_rate_rank</th>
      <th>en_route_rate_rank</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Clothing Sets</td><td>85.82</td><td>52.9</td><td>5539.46</td><td>2131.98</td><td>221</td><td>60</td><td>24</td><td>35</td><td>102</td><td>4604.36</td><td>1726.01</td><td>0.3849</td><td>0.2857</td><td>0.3226</td><td>0.1584</td><td>0.6296</td><td>0.0020582</td><td>0.0015291</td><td>0.0012195</td><td>6</td><td>3</td><td>26</td><td>26</td><td>26</td><td>26</td><td>26</td><td>26</td><td>26</td><td>26</td><td>26</td><td>26</td><td>17</td><td>1</td><td>1</td><td>26</td></tr>
    <tr><td>Jumpsuits &amp; Rompers</td><td>46.79</td><td>24.83</td><td>10339.76</td><td>4897.93</td><td>929</td><td>230</td><td>86</td><td>139</td><td>474</td><td>9496.98</td><td>4463.25</td><td>0.4737</td><td>0.2722</td><td>0.2911</td><td>0.1496</td><td>0.6733</td><td>0.0038418</td><td>0.0035129</td><td>0.0051263</td><td>18</td><td>13</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>19</td><td>25</td><td>14</td><td>12</td><td>7</td></tr>
    <tr><td>Socks &amp; Hosiery</td><td>16.81</td><td>6.75</td><td>15695.27</td><td>9398.63</td><td>3821</td><td>929</td><td>372</td><td>566</td><td>1954</td><td>15784.16</td><td>9453.9</td><td>0.5988</td><td>0.2859</td><td>0.2854</td><td>0.1481</td><td>0.6778</td><td>0.0058317</td><td>0.0067409</td><td>0.0210845</td><td>26</td><td>26</td><td>24</td><td>23</td><td>19</td><td>19</td><td>19</td><td>19</td><td>19</td><td>24</td><td>23</td><td>3</td><td>16</td><td>24</td><td>20</td><td>3</td></tr>
    <tr><td>Leggings</td><td>26.79</td><td>16.07</td><td>22032.86</td><td>8796.32</td><td>3246</td><td>804</td><td>345</td><td>500</td><td>1597</td><td>22344.1</td><td>8926.78</td><td>0.3992</td><td>0.3003</td><td>0.2928</td><td>0.154</td><td>0.6651</td><td>0.0081865</td><td>0.0063089</td><td>0.0179116</td><td>24</td><td>23</td><td>23</td><td>24</td><td>21</td><td>21</td><td>21</td><td>21</td><td>22</td><td>23</td><td>24</td><td>23</td><td>5</td><td>13</td><td>4</td><td>17</td></tr>
    <tr><td>Skirts</td><td>52.13</td><td>20.8</td><td>26843.42</td><td>16061.8</td><td>2087</td><td>539</td><td>208</td><td>314</td><td>1026</td><td>27751.21</td><td>16709.53</td><td>0.5984</td><td>0.2784</td><td>0.304</td><td>0.1505</td><td>0.6556</td><td>0.0099739</td><td>0.0115198</td><td>0.0115162</td><td>13</td><td>19</td><td>22</td><td>20</td><td>23</td><td>23</td><td>23</td><td>23</td><td>23</td><td>22</td><td>20</td><td>4</td><td>24</td><td>2</td><td>11</td><td>25</td></tr>
    <tr><td>Socks</td><td>21.13</td><td>12.76</td><td>31572.07</td><td>12517.44</td><td>6329</td><td>1557</td><td>636</td><td>939</td><td>3197</td><td>32927.59</td><td>13032.11</td><td>0.3965</td><td>0.29</td><td>0.2889</td><td>0.1484</td><td>0.6725</td><td>0.0117309</td><td>0.0089777</td><td>0.0349238</td><td>25</td><td>25</td><td>21</td><td>22</td><td>14</td><td>14</td><td>14</td><td>14</td><td>14</td><td>20</td><td>21</td><td>24</td><td>10</td><td>18</td><td>18</td><td>8</td></tr>
    <tr><td>Suits</td><td>117.3</td><td>70.96</td><td>32903.24</td><td>13000.36</td><td>1123</td><td>287</td><td>113</td><td>167</td><td>556</td><td>32368.47</td><td>12778.14</td><td>0.3951</td><td>0.2825</td><td>0.3002</td><td>0.1487</td><td>0.6595</td><td>0.0122255</td><td>0.0093241</td><td>0.0061968</td><td>3</td><td>1</td><td>20</td><td>21</td><td>24</td><td>24</td><td>24</td><td>24</td><td>24</td><td>21</td><td>22</td><td>25</td><td>18</td><td>3</td><td>14</td><td>24</td></tr>
    <tr><td>Plus</td><td>39.47</td><td>19.84</td><td>44807.01</td><td>22316.68</td><td>4358</td><td>1070</td><td>436</td><td>646</td><td>2206</td><td>42048.64</td><td>21041.57</td><td>0.4981</td><td>0.2895</td><td>0.2883</td><td>0.1482</td><td>0.6734</td><td>0.0166484</td><td>0.016006</td><td>0.0240477</td><td>21</td><td>20</td><td>19</td><td>19</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>15</td><td>11</td><td>19</td><td>19</td><td>6</td></tr>
    <tr><td>Pants &amp; Capris</td><td>55.37</td><td>29.2</td><td>49331.52</td><td>23421.93</td><td>3392</td><td>864</td><td>350</td><td>481</td><td>1697</td><td>41999.86</td><td>19777.56</td><td>0.4748</td><td>0.2883</td><td>0.2968</td><td>0.1418</td><td>0.6626</td><td>0.0183295</td><td>0.0167987</td><td>0.0187173</td><td>11</td><td>9</td><td>18</td><td>18</td><td>20</td><td>20</td><td>20</td><td>22</td><td>20</td><td>19</td><td>19</td><td>18</td><td>13</td><td>8</td><td>26</td><td>21</td></tr>
    <tr><td>Underwear</td><td>27.21</td><td>12.79</td><td>50614.6</td><td>26861.36</td><td>7505</td><td>1886</td><td>738</td><td>1122</td><td>3759</td><td>51345.06</td><td>27197.18</td><td>0.5307</td><td>0.2813</td><td>0.2955</td><td>0.1495</td><td>0.6659</td><td>0.0188063</td><td>0.0192655</td><td>0.0414131</td><td>23</td><td>24</td><td>17</td><td>17</td><td>12</td><td>12</td><td>12</td><td>12</td><td>12</td><td>17</td><td>17</td><td>11</td><td>20</td><td>11</td><td>13</td><td>14</td></tr>
    <tr><td>Maternity</td><td>51.5</td><td>22.73</td><td>63613.6</td><td>35563.76</td><td>5086</td><td>1232</td><td>531</td><td>741</td><td>2582</td><td>61413.18</td><td>34274.78</td><td>0.5591</td><td>0.3012</td><td>0.2835</td><td>0.1457</td><td>0.677</td><td>0.0236362</td><td>0.025507</td><td>0.0280649</td><td>14</td><td>17</td><td>16</td><td>16</td><td>17</td><td>17</td><td>16</td><td>17</td><td>17</td><td>16</td><td>16</td><td>7</td><td>3</td><td>25</td><td>25</td><td>4</td></tr>
    <tr><td>Blazers &amp; Jackets</td><td>90.68</td><td>34.35</td><td>65986.31</td><td>40954.92</td><td>3194</td><td>745</td><td>334</td><td>506</td><td>1609</td><td>76039.51</td><td>47305.1</td><td>0.6207</td><td>0.3095</td><td>0.2772</td><td>0.1584</td><td>0.6835</td><td>0.0245178</td><td>0.0293737</td><td>0.0176247</td><td>5</td><td>8</td><td>15</td><td>15</td><td>22</td><td>22</td><td>22</td><td>20</td><td>21</td><td>15</td><td>15</td><td>1</td><td>1</td><td>26</td><td>1</td><td>1</td></tr>
    <tr><td>Accessories</td><td>42.05</td><td>16.85</td><td>99096.96</td><td>59262.83</td><td>9813</td><td>2384</td><td>967</td><td>1497</td><td>4965</td><td>103385.5</td><td>62000.28</td><td>0.598</td><td>0.2886</td><td>0.2867</td><td>0.1526</td><td>0.6756</td><td>0.0368203</td><td>0.0425044</td><td>0.0541488</td><td>19</td><td>22</td><td>14</td><td>11</td><td>9</td><td>9</td><td>9</td><td>9</td><td>9</td><td>14</td><td>11</td><td>5</td><td>12</td><td>22</td><td>5</td><td>5</td></tr>
    <tr><td>Pants</td><td>59.65</td><td>27.35</td><td>106719.7</td><td>57634.8</td><td>7239</td><td>1823</td><td>713</td><td>1076</td><td>3627</td><td>106167.82</td><td>57611.26</td><td>0.5401</td><td>0.2812</td><td>0.2958</td><td>0.1486</td><td>0.6655</td><td>0.0396526</td><td>0.0413368</td><td>0.0399453</td><td>9</td><td>12</td><td>13</td><td>12</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>12</td><td>10</td><td>21</td><td>10</td><td>15</td><td>16</td></tr>
    <tr><td>Dresses</td><td>84.24</td><td>37.9</td><td>112895.24</td><td>62082.56</td><td>5358</td><td>1316</td><td>549</td><td>792</td><td>2701</td><td>113022.02</td><td>62283.44</td><td>0.5499</td><td>0.2944</td><td>0.2882</td><td>0.1478</td><td>0.6724</td><td>0.0419471</td><td>0.0445268</td><td>0.0295658</td><td>7</td><td>6</td><td>12</td><td>10</td><td>15</td><td>15</td><td>15</td><td>15</td><td>15</td><td>11</td><td>10</td><td>9</td><td>6</td><td>20</td><td>21</td><td>9</td></tr>
  </tbody>
</table>

</div>

<h3>Analytical Insights & Business Recommendations</h3>
<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p>Clothing Sets is the worst-performing category across nearly every metric: #26 in revenue ($5,539.46), #26 in profit ($2,131.98), #26 in unit orders (221), and notably has the highest cancellation rate (15.8%) and highest completion rate (32.3% – meaning orders that survive cancellation tend to complete). The combination of an $85.82 average sale price with a $52.90 cost leaves a margin of only 38.5%, the lowest of all 26 categories.</p>

<p>Clothing Sets should be considered for discontinuation or dramatic restructuring. With the lowest profit margin, fewest orders, and highest cancellation rate in the business, this category consumes disproportionate operational resources relative to its contribution. If the category is retained, its product cost structure ($52.90 avg cost on an $85.82 price) needs renegotiation – the cost-to-price ratio is over 61%, far above the business average.</p>

<p>Suits rank #24 in unit orders (1,123) and #21 in profit ($13,000.36) despite having the highest average product cost ($70.96) and third-highest average sale price ($117.30). The resulting profit margin of 39.5% is second-lowest, meaning the premium pricing doesn't translate to premium profitability. This is a category where high input costs (likely driven by fabric quality and construction complexity) compress margins despite strong retail pricing. The 28.3% return rate is moderate, so the margin issue is cost-driven rather than return-driven.</p>

<p>Investigate supplier cost structures for the Suits category. At $70.96 average cost, Suits products consume nearly 60.5% of revenue in input costs – compared to 44.5% for Outerwear & Coats, which has an even higher average sale price. Consider whether a shift to suppliers offering better cost-to-quality ratios could preserve the product's market positioning while improving margins toward the 50%+ range.</p>

<p>Socks (6,329 orders, 39.7% margin) and Leggings (3,246 orders, 39.9% margin) represent high-volume categories that contribute minimally to profit due to structurally low margins. Socks generate $31,572.07 in revenue but only $12,517.44 in profit, while Leggings generate $22,032.86 revenue with $8,796.32 profit. Both categories have average costs that consume ~60% of sale price ($12.76/$21.13 for Socks; $16.07/$26.79 for Leggings), leaving thin absolute profit per unit.</p>

<p>Rather than dropping these categories (they drive significant order volume which may increase basket size through cross-selling), optimize their fulfillment costs. Socks and leggings are lightweight, compact items ideal for low-cost shipping. Consider offering multi-pack deals – a 3-pack of socks at a slight per-unit discount still generates more total profit than a single pair while reducing per-order shipping costs.</p>





<p>The smallest categories by order volume – Clothing Sets (221), Jumpsuits & Rompers (929), Suits (1,123) – generate relatively few transactions while requiring full catalog management, supplier relationships, and inventory allocation. Evaluate whether the smallest categories justify their operational overhead. Clothing Sets' 221 orders represent just 0.12% of total order volume. If maintaining supplier relationships, inventory space, and marketing for this category costs more than the $2,131.98 in profit it generates, the category should be wound down or consolidated into a broader category (e.g., merged into Active or Outerwear depending on product types).</p>

</div>

</details>
<details>
  <summary><strong>Long Term Trends</strong></summary>

  <div style="margin-top: 12px;"></div>

<h3>Long Term Trend: Total Revenue and Profit</h3>

<pre><code class="language-sql">SELECT
	DATE_TRUNC(DATE(o.created_at), MONTH) AS month,
	SUM(oi.sale_price) AS revenue,
	SUM(oi.sale_price - p.cost) AS profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
WHERE oi.status = 'Complete'
GROUP BY month
ORDER BY month;</code></pre>

<figure style="margin: 20px 0;">
  <img
    src="csv-return-tables/Long term trend for total revenue and profit.png"
    alt="Long term trend chart showing monthly total revenue and profit over time"
    loading="lazy"
    style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
  >
  <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
    Monthly total revenue and profit over the full date range.
    <span style="display:block; margin-top:4px;">
      <a href="csv-return-tables/Long term trend for total revenue and profit.png">Open full-size</a>
    </span>
  </figcaption>
</figure>

<h3>Long Term Trend: Units Sold</h3>

<pre><code class="language-sql">SELECT
	DATE_TRUNC(DATE(o.created_at), MONTH) AS month,
	COUNT(*) AS units_sold
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
WHERE oi.status = 'Complete'
GROUP BY month
ORDER BY month;</code></pre>

<figure style="margin: 20px 0;">
  <img
    src="csv-return-tables/Long term trend for units sold.png"
    alt="Long term trend chart showing monthly units sold over time"
    loading="lazy"
    style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
  >
  <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
    Monthly units sold over the full date range.
    <span style="display:block; margin-top:4px;">
      <a href="csv-return-tables/Long term trend for units sold.png">Open full-size</a>
    </span>
  </figcaption>
</figure>

<h3>Long Term Trend: Profit Margin</h3>

<pre><code class="language-sql">WITH metrics AS (
	SELECT
		DATE_TRUNC(DATE(o.created_at), MONTH) AS month,
		SUM(oi.sale_price - p.cost) AS profit,
		SUM(oi.sale_price) AS revenue
	FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
WHERE oi.status = 'Complete'
GROUP BY month
)
SELECT
	month,
	ROUND(profit/NULLIF(revenue, 0), 4) AS profit_margin
FROM
	metrics
ORDER BY
	month;</code></pre>

<figure style="margin: 20px 0;">
  <img
    src="csv-return-tables/Long term trend for profit margin.png"
    alt="Long term trend chart showing monthly profit margin over time"
    loading="lazy"
    style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
  >
  <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
    Monthly profit margin over the full date range.
    <span style="display:block; margin-top:4px;">
      <a href="csv-return-tables/Long term trend for profit margin.png">Open full-size</a>
    </span>
  </figcaption>
</figure>

<h3>Long Term Trend: Return Rate</h3>

<pre><code class="language-sql">WITH metrics AS (
SELECT
	DATE_TRUNC(DATE(o.created_at), MONTH) AS month,
	SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS complete_item_count,
	SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS returned_item_count
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
GROUP BY month
)
SELECT
	month,
	ROUND(returned_item_count / NULLIF((complete_item_count + returned_item_count),
0), 4) AS return_rate
FROM metrics
ORDER BY month;</code></pre>

<figure style="margin: 20px 0;">
  <img
    src="csv-return-tables/Long term trend for return rate.png"
    alt="Long term trend chart showing monthly return rate over time"
    loading="lazy"
    style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
  >
  <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
    Monthly return rate over the full date range.
    <span style="display:block; margin-top:4px;">
      <a href="csv-return-tables/Long term trend for return rate.png">Open full-size</a>
    </span>
  </figcaption>
</figure>

<h3>Analytical Insights & Business Recommendations</h3>
<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p>The long-term trend queries aggregate monthly revenue and profit from completed orders across the full date range of the dataset. For a growing e-commerce business, we expect to see an upward trajectory in both metrics, with revenue growth outpacing or tracking profit growth depending on margin stability. It is important to track whether profit growth is keeping pace with revenue growth. If revenue is growing faster than profit over time, it indicates either margin compression (rising product costs, increased discounting) or a shift in product mix toward lower-margin categories. Use demand forecasting and predictive modeling on the historical sales data to anticipate future revenue trends, plan inventory orders, and set staffing levels for peak periods.</p>

<p>Monthly units sold provides the clearest signal of demand growth independent of pricing changes. While revenue can increase due to price hikes, units sold directly reflects whether more customers are buying more products. Overlaying the units sold trend with marketing spend or promotional calendar data (if available) can measure campaign effectiveness. If units spike in specific months, identifying what drove those surges – new product launches, seasonal campaigns, or organic growth – and replicating successful patterns is key. Units sold is also the foundation for inventory planning: use the monthly trend to establish baseline demand, then adjust for seasonal patterns identified in the Seasonal Trends section.</p>

<p>Monthly profit margin trend reveals whether the business is becoming more or less efficient at converting revenue to profit over time. A stable or rising margin indicates good cost management and pricing discipline, while a declining margin signals potential issues: rising supplier costs, increased discounting, or a shift toward lower-margin products. If the profit margin trend shows compression over time, investigate root causes at the category and brand level. Cross-reference the margin trend with the category and brand analyses from earlier sections to identify whether specific segments are dragging overall margins down. Proactive supplier cost negotiations (particularly with high-volume brands like Diesel, Calvin Klein, and Carhartt identified in the brand analysis) should be timed to coincide with contract renewal periods.</p>

<p>Tracking return rate over time reveals whether the business is improving or deteriorating in customer satisfaction and product quality. A stable return rate (~28–30% as seen in the category analysis) suggests systemic factors. A rising trend would indicate worsening product quality or increasingly misaligned customer expectations, while a declining trend would validate that quality or UX improvements are working. The return rate trend is a lagging indicator – it reflects problems that already occurred. Complement it with leading indicators like product page bounce rates, customer review sentiment, and repeat purchase rates. If the return rate trend is flat (consistent with the uniformly ~28% rates seen across categories), it reinforces that a platform-wide intervention (better sizing tools, enhanced product photography, improved checkout UX) would be more effective than targeted product-level fixes.</p>

<p>The combination of these four long-term metrics – revenue, units sold, margin, and return rate – creates a business health dashboard. Revenue growth with stable margins indicates healthy scaling, while revenue growth with declining margins suggests unsustainable growth. Increasing units with declining revenue per unit suggests a product mix shift toward lower-price items. Establishing a monthly business review cadence using these four trend metrics is recommended. Set threshold alerts: if profit margin drops below 50% in any month, trigger a cost review; if return rate exceeds 30% in any month, trigger a quality review; if units sold declines month-over-month for two consecutive months, trigger a demand analysis. These trends enable proactive management rather than reactive problem-solving.</p>

</div>

</details>
<details>
  <summary><strong>Seasonal Trends</strong></summary>

  <div style="margin-top: 12px;"></div>

<h3>Seasonal Trend: Revenue and Profit</h3>

<pre><code class="language-sql">SELECT
	EXTRACT(MONTH FROM o.created_at) AS month,
	SUM(oi.sale_price) AS revenue,
	SUM(oi.sale_price - p.cost) AS profit
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
WHERE oi.status = 'Complete'
GROUP BY month
ORDER BY month;</code></pre>

<figure style="margin: 20px 0;">
  <img
    src="csv-return-tables/Seasonal trend for revenue and profit.png"
    alt="Seasonal trend chart showing revenue and profit by month of year"
    loading="lazy"
    style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
  >
  <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
    Revenue and profit aggregated by month of year to reveal seasonal patterns.
    <span style="display:block; margin-top:4px;">
      <a href="csv-return-tables/Seasonal trend for revenue and profit.png">Open full-size</a>
    </span>
  </figcaption>
</figure>

<h3>Seasonal Trend: Units Sold</h3>

<pre><code class="language-sql">SELECT
	EXTRACT(MONTH FROM o.created_at) AS month,
	COUNT(*) AS units_sold
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
WHERE oi.status = 'Complete'
GROUP BY month
ORDER BY month;</code></pre>

<figure style="margin: 20px 0;">
  <img
    src="csv-return-tables/Seasonal trend for units sold.png"
    alt="Seasonal trend chart showing units sold by month of year"
    loading="lazy"
    style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
  >
  <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
    Units sold aggregated by month of year to reveal seasonal patterns.
    <span style="display:block; margin-top:4px;">
      <a href="csv-return-tables/Seasonal trend for units sold.png">Open full-size</a>
    </span>
  </figcaption>
</figure>

<h3>Seasonal Trend: Profit Margin</h3>

<pre><code class="language-sql">WITH metrics AS (
	SELECT
		EXTRACT(MONTH FROM o.created_at) AS month,
		SUM(oi.sale_price - p.cost) AS profit,
		SUM(oi.sale_price) AS revenue
	FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id
WHERE oi.status = 'Complete'
GROUP BY month
)
SELECT
	month,
	ROUND(profit/NULLIF(revenue, 0), 4) AS profit_margin
FROM metrics
ORDER BY month;</code></pre>

<figure style="margin: 20px 0;">
  <img
    src="csv-return-tables/Seasonal trend for profit margin.png"
    alt="Seasonal trend chart showing profit margin by month of year"
    loading="lazy"
    style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
  >
  <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
    Profit margin aggregated by month of year to reveal seasonal patterns.
    <span style="display:block; margin-top:4px;">
      <a href="csv-return-tables/Seasonal trend for profit margin.png">Open full-size</a>
    </span>
  </figcaption>
</figure>

<h3>Seasonal Trend: Return Rate</h3>

<pre><code class="language-sql">WITH metrics AS (
SELECT
	EXTRACT(MONTH FROM o.created_at) AS month,
	SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS complete_item_count,
	SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS returned_item_count
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
GROUP BY month
)
SELECT
	month,
	ROUND(returned_item_count / NULLIF((complete_item_count + returned_item_count),
0), 4) AS return_rate
FROM metrics
ORDER BY month;</code></pre>

<figure style="margin: 20px 0;">
  <img
    src="csv-return-tables/Seasonal trend for return rate.png"
    alt="Seasonal trend chart showing return rate by month of year"
    loading="lazy"
    style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
  >
  <figcaption style="font-size: 0.95em; color: #555; margin-top: 8px;">
    Return rate aggregated by month of year to reveal seasonal patterns.
    <span style="display:block; margin-top:4px;">
      <a href="csv-return-tables/Seasonal trend for return rate.png">Open full-size</a>
    </span>
  </figcaption>
</figure>

<h3>Analytical Insights & Business Recommendations</h3>
<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p>Seasonal aggregation reveals which months consistently generate higher or lower revenue and profit, independent of the long-term growth trend. For an e-commerce retailer selling apparel and accessories, we would expect demand peaks around fall/winter (September–December) driven by back-to-school, holiday gift-giving, and cold-weather outerwear purchases – aligning directly with the finding that Outerwear & Coats is the #1 revenue category. To capitalize on this, inventory orders should be timed to arrive 4–6 weeks before identified peak months. Since Outerwear & Coats dominates revenue with a $146.29 average sale price, ensuring adequate stock of premium jackets and coats before October is critical. Stockouts during peak demand months represent the highest opportunity cost in the business. The historical seasonal pattern can be used to build a demand forecasting model – even a simple moving average of monthly revenue by category would enable more precise purchase orders.</p>

<p>Different categories likely peak at different times: Outerwear & Coats and Sweaters before winter, Swim and Shorts before summer, Active wear potentially showing dual peaks (New Year's resolutions in January, pre-summer fitness in April/May). A category-specific promotional calendar should be built based on these seasonal patterns. Outerwear, Sweaters, and Blazers & Jackets (the top 3 margin categories) should be promoted during September–November when demand naturally peaks, while Swim, Shorts, and Active wear should be promoted during March–May as customers prepare for warm weather. Off-peak months for specific categories can be used for clearance sales and inventory reduction, particularly for seasonal items that would otherwise become dead stock.</p>

<p>The monthly units sold aggregation shows the rhythm of customer purchasing behavior across the year. Peak months for unit volume may differ from peak revenue months – a high-volume month dominated by lower-priced items (Intimates, Socks, Tops & Tees) would show high units sold but moderate revenue, while a month dominated by outerwear and jeans would show lower units but higher revenue per transaction. Seasonal units sold patterns should be used to staff fulfillment operations. If November and December show 30–50% more unit volume than average months, temporary fulfillment staff or extended shipping hours should be pre-arranged. The en-route rate data from the product and category analyses showed that 60–70% of orders are processing or shipping at any given time – during peak months, this backlog would grow unless fulfillment capacity scales proportionally.</p>

<p>If profit margins dip during specific months (e.g., post-holiday January, mid-summer July), it may indicate seasonal clearance discounting or markdown activity that compresses margins. Conversely, margin peaks likely coincide with periods when full-price purchases dominate (e.g., early fall when new inventory arrives). If seasonal margin analysis reveals consistent dips, the discounting strategy should be evaluated on a net basis. A 20% discount that drives a 40% increase in volume is net-positive, but a 20% discount that only drives a 15% volume increase destroys margin without recovering it through volume. The seasonal margin data can be used to set discount ceilings – never discount below the point where the volume increase fails to offset the margin compression.</p>

<p>Return rates may fluctuate seasonally for predictable reasons: holiday gift returns in January, sizing issues on cold-weather clothing purchased online, or impulse-buy returns during sale events. Understanding when returns spike helps plan reverse logistics capacity and refund budgets. If holiday months (November–December) show elevated return rates in January–February, reverse logistics and refund processing capacity should be scaled accordingly. Tightening the return window for sale/clearance items (which are already discounted and thus lower-margin) can reduce the return burden from impulse purchases. For seasonal categories like Outerwear where returns cost the most per unit ($146 avg sale price), investing in better product descriptions, fit guides, and user reviews specifically targeting the pre-peak season months is worthwhile.</p>

<p>The four seasonal metrics together – revenue, units, margin, and returns – create a predictive framework for the business year. Each metric informs a different operational lever: revenue patterns drive marketing budgets, unit patterns drive fulfillment staffing, margin patterns drive pricing strategy, and return patterns drive reverse logistics planning. A unified seasonal planning document should be built that maps each month to its expected demand profile and prescribes operational actions. For example: September → increase outerwear inventory and marketing spend; January → scale return processing and plan clearance events; March → begin summer category promotions. This transforms reactive operations into proactive, data-driven planning.</p>

</div>

</details>
<details>
  <summary><strong>Customers</strong></summary>

  <div style="margin-top: 12px;"></div>

<h3>Top customers by generated Revenue</h3>

<pre><code class="language-sql">WITH first_layer AS (
	SELECT
		o.user_id AS customer_id,
		ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN oi.sale_price ELSE 0 
END), 2) AS generated_revenue,
		ROUND(SUM(CASE WHEN oi.status = 'Complete' THEN (oi.sale_price - p.cost) 
ELSE 0 END), 2) AS generated_profit,
		COUNT(*) AS num_items_ordered,
		COUNT(DISTINCT o.order_id) AS num_orders,
		SUM(CASE WHEN oi.status = 'Returned' THEN 1 ELSE 0 END) AS 
num_returned_items,
		SUM(CASE WHEN oi.status = 'Complete' THEN 1 ELSE 0 END) AS 
num_completed_items,
SUM(CASE WHEN oi.status = 'Cancelled' THEN 1 ELSE 0 END) AS 
num_cancelled_items,
COUNT(DISTINCT CASE WHEN o.status = 'Complete' THEN o.order_id END) AS 
num_completed_orders,
MIN(o.created_at) AS first_order, 
MAX(o.created_at) AS last_order
	FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
ON oi.product_id = p.id 
GROUP BY customer_id
)
, second_layer AS (
	SELECT 
		*,
		ROUND((generated_revenue / NULLIF(num_completed_orders, 0)), 2) AS 
avg_order_value,
		ROUND((num_items_ordered / NULLIF(num_orders, 0)), 2) AS avg_order_size,
		ROUND((num_returned_items / NULLIF((num_completed_items + 
num_returned_items), 0)), 4) AS return_rate,
		DATE_DIFF(DATE(last_order), DATE(first_order), DAY) AS lifetime_days
	FROM first_layer
)
SELECT
	*,
	RANK() OVER(ORDER BY generated_revenue DESC) AS revenue_rank,
	RANK() OVER(ORDER BY generated_profit DESC) AS profit_rank,
	RANK() OVER(ORDER BY num_items_ordered DESC) AS num_items_ordered_rank,
	RANK() OVER(ORDER BY num_orders DESC) AS num_orders_rank,
	RANK() OVER(ORDER BY num_returned_items DESC) AS num_returned_items_rank,
	RANK() OVER(ORDER BY num_completed_items DESC) AS num_completed_items_rank,
	RANK() OVER(ORDER BY num_cancelled_items DESC) AS num_cancelled_items_rank,
	RANK() OVER(ORDER BY num_completed_orders DESC) AS 
num_completed_orders_rank,
	RANK() OVER(ORDER BY first_order DESC) AS first_order_rank,
	RANK() OVER(ORDER BY last_order DESC) AS last_order_rank,
	RANK() OVER(ORDER BY avg_order_value DESC) AS avg_order_value_rank,
	RANK() OVER(ORDER BY avg_order_size DESC) AS avg_order_size_rank,
	RANK() OVER(ORDER BY return_rate DESC) AS return_rate_rank,
	RANK() OVER(ORDER BY lifetime_days DESC) AS lifetime_days_rank
FROM second_layer
ORDER BY revenue_rank ASC
LIMIT 15;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>customer_id</th>
      <th>generated_revenue</th>
      <th>generated_profit</th>
      <th>num_items_ordered</th>
      <th>num_orders</th>
      <th>num_returned_items</th>
      <th>num_completed_items</th>
      <th>num_cancelled_items</th>
      <th>num_completed_orders</th>
      <th>first_order</th>
      <th>last_order</th>
      <th>avg_order_value</th>
      <th>avg_order_size</th>
      <th>return_rate</th>
      <th>lifetime_days</th>
      <th>revenue_rank</th>
      <th>profit_rank</th>
      <th>num_items_ordered_rank</th>
      <th>num_orders_rank</th>
      <th>num_returned_items_rank</th>
      <th>num_completed_items_rank</th>
      <th>num_cancelled_items_rank</th>
      <th>num_completed_orders_rank</th>
      <th>first_order_rank</th>
      <th>last_order_rank</th>
      <th>avg_order_value_rank</th>
      <th>avg_order_size_rank</th>
      <th>return_rate_rank</th>
      <th>lifetime_days_rank</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>41791</td><td>1487.0</td><td>884.96</td><td>3</td><td>1</td><td>0</td><td>3</td><td>0</td><td>1</td><td>2022-09-28 04:15:35.000000 UTC</td><td>2022-09-28 04:15:35.000000 UTC</td><td>1487.0</td><td>3.0</td><td>0.0</td><td>0</td><td>1</td><td>1</td><td>15410</td><td>30074</td><td>12023</td><td>2050</td><td>17392</td><td>3350</td><td>62938</td><td>70428</td><td>1</td><td>2670</td><td>12023</td><td>29774</td></tr>
    <tr><td>9608</td><td>1348.98</td><td>703.94</td><td>9</td><td>4</td><td>0</td><td>4</td><td>4</td><td>2</td><td>2022-06-02 13:50:09.000000 UTC</td><td>2025-04-28 20:40:37.000000 UTC</td><td>674.49</td><td>2.25</td><td>0.0</td><td>1061</td><td>2</td><td>3</td><td>148</td><td>1</td><td>12023</td><td>435</td><td>164</td><td>299</td><td>65844</td><td>37422</td><td>96</td><td>7921</td><td>12023</td><td>4750</td></tr>
    <tr><td>58672</td><td>1327.33</td><td>688.92</td><td>6</td><td>2</td><td>0</td><td>4</td><td>0</td><td>1</td><td>2021-12-10 12:12:04.000000 UTC</td><td>2025-09-11 22:33:43.000000 UTC</td><td>1327.33</td><td>3.0</td><td>0.0</td><td>1371</td><td>3</td><td>4</td><td>2025</td><td>10016</td><td>12023</td><td>435</td><td>17392</td><td>3350</td><td>69626</td><td>27098</td><td>2</td><td>2670</td><td>12023</td><td>2338</td></tr>
    <tr><td>6721</td><td>1303.55</td><td>708.33</td><td>6</td><td>3</td><td>0</td><td>5</td><td>0</td><td>2</td><td>2025-06-17 16:41:11.000000 UTC</td><td>2026-02-18 00:34:38.000000 UTC</td><td>651.77</td><td>2.0</td><td>0.0</td><td>246</td><td>4</td><td>2</td><td>2025</td><td>5093</td><td>12023</td><td>144</td><td>17392</td><td>299</td><td>23890</td><td>8652</td><td>100</td><td>8103</td><td>12023</td><td>18441</td></tr>
    <tr><td>41139</td><td>1170.01</td><td>645.44</td><td>4</td><td>1</td><td>0</td><td>4</td><td>0</td><td>1</td><td>2025-08-23 10:04:29.000000 UTC</td><td>2025-08-23 10:04:29.000000 UTC</td><td>1170.01</td><td>4.0</td><td>0.0</td><td>0</td><td>5</td><td>5</td><td>8057</td><td>30074</td><td>12023</td><td>435</td><td>17392</td><td>3350</td><td>19645</td><td>28833</td><td>3</td><td>1</td><td>12023</td><td>29774</td></tr>
    <tr><td>96233</td><td>1142.38</td><td>614.03</td><td>7</td><td>3</td><td>0</td><td>4</td><td>0</td><td>1</td><td>2025-09-02 02:54:09.000000 UTC</td><td>2025-10-28 15:36:32.000000 UTC</td><td>1142.38</td><td>2.33</td><td>0.0</td><td>56</td><td>6</td><td>8</td><td>887</td><td>5093</td><td>12023</td><td>435</td><td>17392</td><td>3350</td><td>19003</td><td>22776</td><td>4</td><td>7675</td><td>12023</td><td>25645</td></tr>
    <tr><td>10218</td><td>1120.4</td><td>468.69</td><td>6</td><td>3</td><td>1</td><td>5</td><td>0</td><td>2</td><td>2026-02-22 01:11:21.000000 UTC</td><td>2026-03-16 03:41:47.000000 UTC</td><td>560.2</td><td>2.0</td><td>0.1667</td><td>22</td><td>7</td><td>67</td><td>2025</td><td>5093</td><td>4008</td><td>144</td><td>17392</td><td>299</td><td>5328</td><td>3464</td><td>128</td><td>8103</td><td>11983</td><td>27583</td></tr>
    <tr><td>89840</td><td>1103.0</td><td>576.93</td><td>4</td><td>2</td><td>0</td><td>3</td><td>0</td><td>1</td><td>2024-12-07 22:57:33.000000 UTC</td><td>2026-02-12 19:45:20.000000 UTC</td><td>1103.0</td><td>2.0</td><td>0.0</td><td>432</td><td>8</td><td>14</td><td>8057</td><td>10016</td><td>12023</td><td>2050</td><td>17392</td><td>3350</td><td>34223</td><td>9545</td><td>5</td><td>8103</td><td>12023</td><td>13731</td></tr>
    <tr><td>99402</td><td>1095.49</td><td>605.27</td><td>4</td><td>2</td><td>0</td><td>3</td><td>0</td><td>1</td><td>2024-06-22 08:20:14.000000 UTC</td><td>2025-07-10 07:07:30.000000 UTC</td><td>1095.49</td><td>2.0</td><td>0.0</td><td>383</td><td>9</td><td>9</td><td>8057</td><td>10016</td><td>12023</td><td>2050</td><td>17392</td><td>3350</td><td>41884</td><td>32315</td><td>6</td><td>8103</td><td>12023</td><td>14818</td></tr>
    <tr><td>72421</td><td>1090.96</td><td>566.27</td><td>5</td><td>2</td><td>0</td><td>4</td><td>1</td><td>1</td><td>2023-09-13 12:47:43.000000 UTC</td><td>2025-10-01 00:04:09.000000 UTC</td><td>1090.96</td><td>2.5</td><td>0.0</td><td>749</td><td>10</td><td>16</td><td>4060</td><td>10016</td><td>12023</td><td>435</td><td>6078</td><td>3350</td><td>52560</td><td>25388</td><td>7</td><td>5779</td><td>12023</td><td>8282</td></tr>
    <tr><td>31261</td><td>1079.88</td><td>634.52</td><td>4</td><td>1</td><td>0</td><td>4</td><td>0</td><td>1</td><td>2025-11-10 19:44:29.000000 UTC</td><td>2025-11-10 19:44:29.000000 UTC</td><td>1079.88</td><td>4.0</td><td>0.0</td><td>0</td><td>11</td><td>6</td><td>8057</td><td>30074</td><td>12023</td><td>435</td><td>17392</td><td>3350</td><td>14129</td><td>21355</td><td>8</td><td>1</td><td>12023</td><td>29774</td></tr>
    <tr><td>92743</td><td>1072.99</td><td>563.61</td><td>2</td><td>1</td><td>0</td><td>2</td><td>0</td><td>1</td><td>2019-05-26 14:46:36.000000 UTC</td><td>2019-05-26 14:46:36.000000 UTC</td><td>1072.99</td><td>2.0</td><td>0.0</td><td>0</td><td>12</td><td>17</td><td>25303</td><td>30074</td><td>12023</td><td>4241</td><td>17392</td><td>3350</td><td>79749</td><td>79862</td><td>9</td><td>8103</td><td>12023</td><td>29774</td></tr>
    <tr><td>58269</td><td>1061.94</td><td>515.49</td><td>5</td><td>3</td><td>0</td><td>4</td><td>1</td><td>2</td><td>2023-10-25 12:15:17.000000 UTC</td><td>2025-10-24 12:12:28.000000 UTC</td><td>530.97</td><td>1.67</td><td>0.0</td><td>730</td><td>13</td><td>42</td><td>4060</td><td>5093</td><td>12023</td><td>435</td><td>6078</td><td>299</td><td>51108</td><td>23151</td><td>143</td><td>21954</td><td>12023</td><td>8531</td></tr>
    <tr><td>31221</td><td>1046.99</td><td>467.51</td><td>5</td><td>2</td><td>0</td><td>4</td><td>0</td><td>1</td><td>2023-09-22 16:05:02.000000 UTC</td><td>2024-09-30 17:07:31.000000 UTC</td><td>1046.99</td><td>2.5</td><td>0.0</td><td>374</td><td>14</td><td>68</td><td>4060</td><td>10016</td><td>12023</td><td>435</td><td>17392</td><td>3350</td><td>52246</td><td>49093</td><td>10</td><td>5779</td><td>12023</td><td>15040</td></tr>
    <tr><td>90530</td><td>1039.66</td><td>618.49</td><td>7</td><td>4</td><td>0</td><td>4</td><td>1</td><td>1</td><td>2025-01-12 02:14:23.000000 UTC</td><td>2025-11-14 14:49:28.000000 UTC</td><td>1039.66</td><td>1.75</td><td>0.0</td><td>306</td><td>15</td><td>7</td><td>887</td><td>1</td><td>12023</td><td>435</td><td>6078</td><td>3350</td><td>32497</td><td>20944</td><td>11</td><td>21174</td><td>12023</td><td>16753</td></tr>
  </tbody>
</table>

</div>

<h3>Customer segment Counts</h3>

<pre><code class="language-sql">WITH customer_order_counts AS (
  SELECT
    user_id,
    SUM(num_of_item) AS total_items
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  GROUP BY user_id
),
bounds AS (
  SELECT
    MIN(total_items) AS min_items,
    MAX(total_items) AS max_items
  FROM customer_order_counts
),
segments AS (
  SELECT
    c.total_items,
    b.min_items,
    b.max_items,
    LEAST(
      FLOOR((c.total_items - b.min_items) / ((b.max_items - b.min_items) / 4.0)) + 1,
      4
    ) AS segment
  FROM customer_order_counts c
  CROSS JOIN bounds b
)
SELECT
  min_items,
  max_items,
  segment,
  ROUND(min_items + (segment - 1) * (max_items - min_items) / 4.0, 2) AS segment_start,
  ROUND(min_items + segment * (max_items - min_items) / 4.0, 2) AS segment_end,
  COUNT(*) AS num_customers
FROM segments
GROUP BY segment, min_items, max_items
ORDER BY segment;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>min_items</th>
      <th>max_items</th>
      <th>segment</th>
      <th>segment_start</th>
      <th>segment_end</th>
      <th>num_customers</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>13</td><td>1.0</td><td>1.0</td><td>4.0</td><td>64554</td></tr>
    <tr><td>1</td><td>13</td><td>2.0</td><td>4.0</td><td>7.0</td><td>13385</td></tr>
    <tr><td>1</td><td>13</td><td>3.0</td><td>7.0</td><td>10.0</td><td>1877</td></tr>
    <tr><td>1</td><td>13</td><td>4.0</td><td>10.0</td><td>13.0</td><td>147</td></tr>
  </tbody>
</table>

</div>

<h3>Customer Geographics</h3>

<pre><code class="language-sql">SELECT
  u.country,
  COUNT(DISTINCT u.id) AS num_customers,
  COUNT(oi.id) AS units_sold,
  ROUND(SUM(oi.sale_price), 2) AS revenue,
  ROUND(SUM(oi.sale_price - p.cost), 2) AS profit
FROM
  `bigquery-public-data.thelook_ecommerce.order_items` oi
JOIN
  `bigquery-public-data.thelook_ecommerce.users` u
  ON oi.user_id = u.id
JOIN
  `bigquery-public-data.thelook_ecommerce.products` p
  ON oi.product_id = p.id
WHERE
  oi.status NOT IN ('Cancelled', 'Returned')
GROUP BY
  u.country
ORDER BY
  revenue DESC;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>country</th>
      <th>num_customers</th>
      <th>units_sold</th>
      <th>revenue</th>
      <th>profit</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>China</td><td>22412</td><td>46162</td><td>2748111.08</td><td>1425885.25</td></tr>
    <tr><td>United States</td><td>14926</td><td>30626</td><td>1824282.8</td><td>944656.58</td></tr>
    <tr><td>Brasil</td><td>9618</td><td>19902</td><td>1186881.13</td><td>616746.55</td></tr>
    <tr><td>South Korea</td><td>3433</td><td>7038</td><td>412219.82</td><td>213576.53</td></tr>
    <tr><td>France</td><td>3137</td><td>6402</td><td>382581.48</td><td>198723.99</td></tr>
    <tr><td>United Kingdom</td><td>3038</td><td>6343</td><td>376944.04</td><td>195623.13</td></tr>
    <tr><td>Germany</td><td>2807</td><td>5713</td><td>348155.95</td><td>180505.4</td></tr>
    <tr><td>Spain</td><td>2745</td><td>5541</td><td>334100.88</td><td>173307.63</td></tr>
    <tr><td>Japan</td><td>1552</td><td>3153</td><td>188862.22</td><td>97987.7</td></tr>
    <tr><td>Australia</td><td>1450</td><td>2967</td><td>177458.55</td><td>92306.6</td></tr>
    <tr><td>Belgium</td><td>767</td><td>1666</td><td>96644.64</td><td>50128.32</td></tr>
    <tr><td>Poland</td><td>155</td><td>301</td><td>16104.04</td><td>8341.83</td></tr>
    <tr><td>Colombia</td><td>7</td><td>14</td><td>843.29</td><td>462.26</td></tr>
    <tr><td>Austria</td><td>1</td><td>2</td><td>21.63</td><td>12.09</td></tr>
    <tr><td>España</td><td>1</td><td>1</td><td>19.98</td><td>10.75</td></tr>
  </tbody>
</table>

</div>

<h3>Analytical Insights & Business Recommendations</h3>
<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p>The customer segment count data reveals an extremely skewed distribution: 64,554 customers (80.7%) fall in Segment 1 (1–4 items ordered), 13,385 (16.7%) in Segment 2 (4–7 items), 1,877 (2.3%) in Segment 3 (7–10 items), and only 147 (0.2%) in Segment 4 (10–13 items). The overwhelming majority of customers are low-frequency, low-volume purchasers. This distribution is typical of e-commerce businesses but highlights a critical retention challenge: most customers are essentially one-time or two-time buyers. The top customer by revenue (customer #41791) generated $1,487 from a single order of 3 items – showing that high revenue comes from high-value items, not repeat purchasing. Implementing customer retention strategies targeting the Segment 1 customers (1–4 items) could yield significant results. Even moving 5% of these 64,554 customers into Segment 2 (by encouraging one additional order) would add ~3,228 returning customers. Tactics include post-purchase email campaigns with personalized product recommendations, loyalty discounts on second purchases, and targeted ads for complementary items based on initial purchase categories. The cost of retaining an existing customer is significantly lower than acquiring a new one.</p>

<p>The top 15 customers by revenue almost all share a profile: 1–4 orders, 3–7 items, and very high average order values ($500–$1,487). Most of these customers achieved top-15 status through a single large purchase of premium items rather than through repeat buying behavior. Customer #41791's $1,487 came from one order; customer #41139's $1,170 from one order of 4 items. Only customers #9608 and #6721 show multiple orders (4 and 3 respectively) with meaningful lifetime spans (1,061 and 246 days), suggesting they may be the closest to genuinely loyal, repeat customers among the top earners. The high-value, single-order customers represent both an opportunity and a risk. They contribute outsized revenue but are fragile – if they don't return, their lifetime value is capped at one transaction. Targeting these customers with VIP-style retention – exclusive early access to new premium products, personalized thank-you communications, and loyalty incentives calibrated to their demonstrated willingness to spend ($500+) – could be highly effective. Even converting 20% of them into two-order customers would significantly impact revenue.</p>




<p>China dominates customer geography with 22,412 customers generating $2,748,111.08 in revenue – more than the next two countries combined. The United States follows with 14,926 customers and $1,824,282.80, then Brazil with 9,618 customers and $1,186,881.13. These three countries account for the vast majority of the customer base. The per-customer revenue is relatively consistent across major markets ($122–$131 per customer for the top 5 countries), suggesting that spending behavior doesn't vary dramatically by geography – the differences in total revenue are driven by customer count, not average spending. Identifying the top-demand products for each customer country and advertising accordingly is recommended. Chinese customers, representing the largest market, should see product recommendations optimized for their browsing and purchasing patterns. Logistics and shipping optimization should prioritize the China, US, and Brazil shipping corridors since they represent the overwhelming majority of order volume. For smaller but growing markets (South Korea, France, UK, Germany, Spain), investing in localized product pages and regional marketing to grow customer counts toward critical mass would be beneficial.</p>


</div>

</details>
<details>
  <summary><strong>Distribution Centers</strong></summary>

  <div style="margin-top: 12px;"></div>

<h3>Distribution center performance</h3>

<pre><code class="language-sql">SELECT
  dc.name AS distribution_center,
  COUNT(oi.id) AS total_units,
  ROUND(SUM(oi.sale_price), 2) AS revenue,
  ROUND(SUM(oi.sale_price) - SUM(p.cost), 2) AS profit,
  ROUND(
    COUNTIF(oi.status = 'Processing') / COUNT(oi.id) * 100, 2
  ) AS processing_pct
FROM
  `bigquery-public-data.thelook_ecommerce.order_items` oi
JOIN
  `bigquery-public-data.thelook_ecommerce.products` p
  ON oi.product_id = p.id
JOIN
  `bigquery-public-data.thelook_ecommerce.distribution_centers` dc
  ON p.distribution_center_id = dc.id
GROUP BY
  dc.name
ORDER BY
  total_units DESC;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>distribution_center</th>
      <th>total_units</th>
      <th>revenue</th>
      <th>profit</th>
      <th>processing_pct</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Memphis TN</td><td>24282</td><td>1417936.76</td><td>742425.78</td><td>20.27</td></tr>
    <tr><td>Chicago IL</td><td>23835</td><td>1321943.15</td><td>692110.99</td><td>19.83</td></tr>
    <tr><td>Houston TX</td><td>22829</td><td>1600413.73</td><td>853992.03</td><td>19.59</td></tr>
    <tr><td>Mobile AL</td><td>18515</td><td>1242396.82</td><td>634302.9</td><td>20.18</td></tr>
    <tr><td>Los Angeles CA</td><td>17274</td><td>949866.99</td><td>489442.35</td><td>19.71</td></tr>
    <tr><td>Charleston SC</td><td>16636</td><td>662246.68</td><td>334984.25</td><td>19.85</td></tr>
    <tr><td>Philadelphia PA</td><td>16568</td><td>1065642.92</td><td>542109.66</td><td>19.58</td></tr>
    <tr><td>Port Authority of New York/New Jersey NY/NJ</td><td>16388</td><td>933800.14</td><td>483299.71</td><td>20.23</td></tr>
    <tr><td>New Orleans LA</td><td>12816</td><td>786466.54</td><td>414082.5</td><td>19.47</td></tr>
    <tr><td>Savannah GA</td><td>11954</td><td>799532.26</td><td>405281.54</td><td>20.25</td></tr>
  </tbody>
</table>

</div>

<h3>Distribution center inventory</h3>

<pre><code class="language-sql">WITH product_sales AS (
  SELECT
    p.id AS product_id,
    p.distribution_center_id,
    COUNT(oi.id) / GREATEST(DATE_DIFF(CURRENT_DATE(), MIN(DATE(oi.created_at)), DAY), 1) AS daily_sales_rate
  FROM
    `bigquery-public-data.thelook_ecommerce.products` p
  LEFT JOIN
    `bigquery-public-data.thelook_ecommerce.order_items` oi
    ON p.id = oi.product_id
  GROUP BY
    p.id, p.distribution_center_id
),


inventory AS (
  SELECT
    id AS product_id,
    product_distribution_center_id,
    COUNT(*) AS stock_on_hand
  FROM
    `bigquery-public-data.thelook_ecommerce.inventory_items`
  WHERE
    sold_at IS NULL
  GROUP BY
    id, product_distribution_center_id
),


product_status AS (
  SELECT
    ps.distribution_center_id,
    CASE
      WHEN SAFE_DIVIDE(COALESCE(i.stock_on_hand, 0), ps.daily_sales_rate) > 90 THEN 'Overstocked'
      WHEN SAFE_DIVIDE(COALESCE(i.stock_on_hand, 0), ps.daily_sales_rate) < 14 THEN 'Understocked'
    END AS stock_status
  FROM
    product_sales ps
  LEFT JOIN
    inventory i
    ON ps.product_id = i.product_id
    AND ps.distribution_center_id = i.product_distribution_center_id
)


SELECT
  dc.name AS distribution_center,
  COUNTIF(stock_status = 'Overstocked') AS overstocked_products,
  COUNTIF(stock_status = 'Understocked') AS understocked_products,
  COUNTIF(stock_status IS NOT NULL) AS total_flagged_products
FROM
  product_status ps
JOIN
  `bigquery-public-data.thelook_ecommerce.distribution_centers` dc
  ON ps.distribution_center_id = dc.id
GROUP BY
  dc.name
ORDER BY
  total_flagged_products DESC;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>distribution_center</th>
      <th>overstocked_products</th>
      <th>understocked_products</th>
      <th>total_flagged_products</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Chicago IL</td><td>311</td><td>3595</td><td>3906</td></tr>
    <tr><td>Memphis TN</td><td>298</td><td>3576</td><td>3874</td></tr>
    <tr><td>Houston TX</td><td>294</td><td>3356</td><td>3650</td></tr>
    <tr><td>Mobile AL</td><td>188</td><td>2719</td><td>2907</td></tr>
    <tr><td>Los Angeles CA</td><td>162</td><td>2588</td><td>2750</td></tr>
    <tr><td>Charleston SC</td><td>160</td><td>2545</td><td>2705</td></tr>
    <tr><td>Philadelphia PA</td><td>155</td><td>2501</td><td>2656</td></tr>
    <tr><td>Port Authority of New York/New Jersey NY/NJ</td><td>151</td><td>2414</td><td>2565</td></tr>
    <tr><td>New Orleans LA</td><td>92</td><td>2014</td><td>2106</td></tr>
    <tr><td>Savannah GA</td><td>70</td><td>1805</td><td>1875</td></tr>
  </tbody>
</table>

</div>

<h3>Analytical Insights & Business Recommendations</h3>
<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p>Houston TX generates the most revenue ($1,600,413.73) and profit ($853,992.03) across all distribution centers, despite ranking only #3 in total units shipped (22,829). This means Houston is processing higher-value products – likely premium outerwear, jeans, and suits that dominate the top-revenue categories. By comparison, Memphis TN ships the most units (24,282) but generates $182K less revenue than Houston, indicating Memphis handles more lower-price-point items.</p>

<p>Recommendation: Given Houston's revenue leadership, ensure this facility has priority access to premium inventory (Outerwear & Coats, Suits & Sport Coats, Blazers & Jackets – the three highest-margin categories). Operational disruptions at Houston would disproportionately impact the business's bottom line. Consider allocating additional quality control resources to Houston since its higher-value shipments have greater per-unit revenue risk if damaged or delayed.</p>

<p>Processing percentages across all 10 distribution centers fall in a tight band of 19.47%–20.27%, suggesting that order processing capacity and speed are consistent across the network. No single facility is significantly bottlenecked or outperforming others in throughput.</p>

<p>Recommendation: The uniform ~20% processing rate raises a question: is this the optimal throughput, or is every facility equally constrained by the same bottleneck (e.g., a shared technology platform, standardized staffing model, or common shipping carrier limitations)? Investigate whether shipping routes and processing practices across the network can be optimized – even a 1 percentage point improvement in processing speed across all 10 facilities, moving more orders from processing to shipped faster, would reduce the window for customer cancellations (which were identified as a significant source of lost revenue in the product and brand analyses).</p>

<p>The inventory analysis reveals a dramatic imbalance: across all distribution centers, understocked products outnumber overstocked products by roughly 10:1. Chicago IL has 3,595 understocked products vs. 311 overstocked; Memphis TN has 3,576 understocked vs. 298 overstocked. This pattern is consistent across every facility.</p>

<p>Understocking means products with active demand don't have enough inventory to meet expected sales velocity, leading to potential stockouts, lost revenue, and disappointed customers. Given that the product-level analysis showed high-value items like The North Face, Canada Goose, and Diesel driving outsized revenue per unit, a stockout on these items has far greater revenue impact than on low-price basics.</p>

<p>Recommendation: The widespread understocking is the most actionable finding in the distribution center analysis. Prioritize replenishment for the highest-revenue and highest-margin products first – ensure Outerwear & Coats, Suits & Sport Coats, and Blazers & Jackets (the top 3 margin categories) are fully stocked before allocating capital to lower-margin items. Demand can be tracked and forecasted using the historical sales data and seasonal patterns identified in the trends sections to build more accurate reorder points and safety stock levels.</p>

<p>While understocking dominates, each facility does carry 70–311 overstocked products. These are items where inventory exceeds 90 days of projected sales at current velocity – capital tied up in slow-moving merchandise that could be allocated to higher-demand items.</p>

<p>Recommendation: Identify the specific overstocked products at each facility and cross-reference with the bottom products and bottom brands analyses. Products that are overstocked AND appear in the zero-revenue or low-demand lists should be candidates for clearance pricing or return to supplier. Products that are overstocked but have decent margins may simply need promotional support to accelerate their sell-through rate – targeted advertising or bundle deals could move excess inventory before it becomes obsolete.</p>

<p>With 10 distribution centers across the southeastern and eastern US (Memphis, Chicago, Houston, Mobile, LA, Charleston, Philadelphia, NY/NJ, New Orleans, Savannah), the network is heavily weighted toward the eastern half of the country. Given that the customer geography data shows China and Brazil as the #1 and #3 customer countries, the domestic distribution network may be serving international shipping corridors differently than domestic ones.</p>

<p>Recommendation: Evaluate whether the current distribution center footprint optimally serves the geographic customer mix. If the majority of US orders originate from certain regions, ensure inventory is positioned at the nearest facility rather than evenly distributed. For international shipments (especially to China, the largest market), identify which port-adjacent facilities (LA, Houston, NY/NJ) are most efficient for international fulfillment and consider concentrating international-bound inventory at those locations to reduce domestic transit time before international shipping.</p>

<p>The distribution center network as a whole has room for shipping and transit cost optimization. With high en-route rates (60–70% of non-cancelled, non-returned orders) observed across products and categories, a meaningful portion of the business's inventory is constantly in transit between facilities and customers.</p>

<p>Recommendation: Investigate whether shipping routes between facilities and major customer hubs can be consolidated or optimized. For high-volume brands (Calvin Klein with 3,180 orders, Allegra K with 6,057 orders, Carhartt with 2,509 orders), it may be more efficient to position their inventory at specific facilities closest to their customer demand centers rather than spreading it across all 10 locations. This reduces inter-facility transfers and shortens last-mile delivery times, improving both cost efficiency and customer satisfaction.</p>

</div>

</details>
<details>
  <summary><strong>Conclusion</strong></summary>

  <div style="margin-top: 12px;"></div>

<h3>Key Findings</h3>

<p>Across ten analytical dimensions – products, brands, categories, trends, customers, and distribution centers – several findings emerged that would be critical for any business stakeholder evaluating this retailer's performance.</p>

<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">
<p><strong>Revenue concentration in premium categories:</strong> Outerwear & Coats generates $339,222 in revenue – ranking #1 – with only 9,028 unit orders, which ranks #10 by volume. This proves that premium categories drive disproportionate revenue per unit. The top 2 categories (Outerwear & Jeans) account for approximately 24% of total revenue, meaning a quarter of the business depends on just two product lines.</p>

<p><strong>Margin diverges sharply from revenue:</strong> Blazers & Jackets has the highest profit margin at 62.1% but ranks only #15 in revenue – the most profitable category per dollar sold is one of the lower-volume ones. Conversely, Jeans ranks #2 in revenue but #21 in margin at 46.5%. A strategy optimized for revenue looks fundamentally different from one optimized for profitability.</p>

<p><strong>Return rates are systemic, not category-specific:</strong> Return rates across all 26 categories fall within a tight 27–31% band, suggesting the approximately 28% baseline is driven by platform-level factors – return policy, product photography, sizing tools – rather than category-specific quality issues. This is a critical finding because it means platform-wide UX improvements would compound across the entire catalog, whereas targeted product-level fixes would have limited impact.</p>

<p><strong>Lost revenue rivals earned revenue:</strong> For nearly every top product, brand, and category, lost revenue from returns and cancellations approaches or exceeds actual completed revenue. Diesel leads all brands in lost revenue ($49,754) against earned revenue of $53,774. Reducing the return and cancellation rate by even 2 percentage points would meaningfully increase net revenue across the business.</p>

<p><strong>The customer base is overwhelmingly single-purchase:</strong> 80.7% of customers (64,554 of 79,963) ordered only 1–4 items total. The top revenue customer generated $1,487 from a single order. Retention and repeat purchasing represent the largest untapped growth lever – the business is acquiring customers effectively but not converting them into repeat buyers.</p>

<p><strong>Distribution centers are systematically understocked:</strong> Across all 10 facilities, understocked products outnumber overstocked products by approximately 10:1. Chicago alone has 3,595 understocked items versus 311 overstocked – meaning potential revenue is being lost to stockouts at scale. This is an operational problem with a direct revenue impact.</p>

<p><strong>Zero-revenue products consume resources:</strong> Multiple products and brands generated $0 in completed revenue despite having orders placed – 100% of their orders were returned, cancelled, or remain in transit. These items occupy inventory space and processing bandwidth without contributing any revenue.</p>

<p><strong>Geographic concentration:</strong> Three countries (China, United States, Brazil) account for the vast majority of revenue, with per-customer spending relatively uniform across geographies at $122–$131 per customer in the top 5 markets. This suggests that demand patterns are consistent internationally but that revenue growth is constrained to a small number of markets.</p>
</div>

<h3>Highest-Impact Recommendations</h3>

<p>Synthesizing the findings across all ten analytical sections, the following actions would generate the greatest business value if implemented. These are ordered by estimated impact – the first recommendation alone would affect every category, brand, and product in the catalog.</p>

<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">
<p><strong>1. Invest in platform-wide return reduction.</strong> Implement improved sizing tools, enhanced product photography, and virtual try-on capabilities. The uniform ~28% return rate across all 26 categories means a single platform improvement compounds across the entire catalog. A 2-point reduction in return rate would recover thousands of currently-lost orders and directly increase net revenue without requiring any new customer acquisition.</p>

<p><strong>2. Rebalance distribution center inventory.</strong> Address the 10:1 understocking-to-overstocking ratio immediately, prioritizing the highest-revenue and highest-margin categories – Outerwear & Coats, Suits & Sport Coats, and Blazers & Jackets – to prevent stockouts on items with $100–$150 average revenue per unit. Every stockout on a premium item is a high-value sale lost.</p>

<p><strong>3. Implement customer retention campaigns targeting single-purchase customers.</strong> The 64,554 customers who purchased only 1–4 items represent a massive re-engagement opportunity. Even converting 5% into repeat buyers adds approximately 3,200 returning customers – significantly cheaper than equivalent new customer acquisition and with higher expected lifetime value.</p>

<p><strong>4. Negotiate supplier costs for high-volume, low-margin brands.</strong> Diesel (1,466 orders, 50.2% margin), Wrangler (1,287 orders, 47.2% margin), and the denim category broadly exhibit structural margin compression. The volume leverage with these suppliers is significant and should be used to renegotiate cost-of-goods to bring margins closer to the catalog average.</p>

<p><strong>5. Delist zero-revenue products and brands.</strong> Products with 3 or more orders and $0 in completed revenue are consuming inventory space, warehouse capacity, and fulfillment bandwidth for no return. Catalog pruning would simplify operations, reduce carrying costs, and improve the customer browsing experience by removing items that consistently fail to convert.</p>

<p><strong>6. Prioritize marketing spend on high-margin categories.</strong> A $1 increase in Blazers & Jackets demand yields $0.62 in profit versus $0.44 for Tops & Tees. Advertising ROI is structurally higher for high-margin categories, meaning the same marketing budget generates more profit when directed toward these product lines.</p>

<p><strong>7. Build seasonal inventory planning using trend data.</strong> Front-load outerwear and sweater inventory before fall/winter peak demand, scale fulfillment staffing for identified high-volume months, and time clearance events to align with the demand troughs visible in the seasonal analysis. Proactive inventory planning based on these patterns would reduce both stockouts and overstock carrying costs.</p>
</div>

<h3>Analytical Approach & What This Demonstrates</h3>

<p>This project was designed to demonstrate the kind of analysis a data analyst performs in practice – not isolated queries answering single questions, but a systematic, multi-dimensional examination of an entire business from the data layer up.</p>

<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">
<p><strong>Multi-dimensional analysis:</strong> Every entity – product, brand, category – was examined from 6–8 metric perspectives simultaneously (revenue, profit, margin, volume, return rate, lost revenue, and more) rather than just one. This mirrors real analyst work where a product can look excellent on revenue but terrible on margin, or a brand can lead in profit but hemorrhage returns. Single-metric analysis leads to bad decisions; multi-dimensional analysis reveals trade-offs.</p>

<p><strong>Paired top/bottom analysis:</strong> Analyzing only top performers gives an incomplete picture. The "Bottom" sections reveal where the business is bleeding – zero-revenue products, margin-compressing categories, and dead-weight brands. Identifying what to <em>stop</em> doing is as valuable as identifying what to double down on, and this paired structure ensures both sides are examined.</p>

<p><strong>Layered CTE architecture:</strong> The consistent <code>first_layer → second_layer → third_layer</code> CTE pattern demonstrates a real-world query design approach where complex metrics are built incrementally. Each layer has a clear purpose: aggregate raw data, derive ratios and calculated metrics, then rank and filter. This produces readable, maintainable, and auditable SQL that another analyst can pick up and extend without reverse-engineering the logic.</p>

<p><strong>Recommendations grounded in data:</strong> Every recommendation in this project ties directly to a specific finding with a specific number. "Reduce return rates" is vague; "reduce the platform-wide ~28% return rate that is uniformly distributed across all 26 categories, suggesting platform-level UX as the root cause" is actionable and defensible. Data-driven recommendations require this level of specificity to be credible.</p>

<p><strong>SQL as the right tool for the job:</strong> This entire analysis – joining six tables, computing conditional aggregations, building multi-layer derived metrics, ranking across 29,000+ products and 2,700+ brands – was accomplished purely in SQL. No data was exported for processing in another tool. This demonstrates that SQL is not just a "data extraction" language but a full analytical engine capable of end-to-end business analysis when used with intention and structure.</p>
</div>

<h3>Limitations & Future Work</h3>

<p>Analytical maturity includes knowing the boundaries of your own work. The following limitations are important context for interpreting the findings above.</p>

<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">
<p><strong>Synthetic dataset:</strong> <code>thelook_ecommerce</code> is Google's synthetic dataset, not real company data. Some pricing anomalies exist – for example, socks listed at $903, which are presumably data generation artifacts. The analytical methodology is sound and fully transferable to real datasets, but the specific dollar figures are illustrative rather than representative of a real retailer.</p>

<p><strong>No cost-of-operations data:</strong> The analysis calculates product-level profit (sale price minus product cost) but cannot account for fulfillment costs, marketing spend, overhead, or return processing costs. A real-world version of this analysis would incorporate these to produce true net profitability figures and more accurate ROI calculations for the recommendations.</p>

<p><strong>No customer journey data:</strong> The dataset lacks clickstream, page-view, cart-abandonment, or marketing attribution data. Customer analysis is limited to transactional behavior (orders, returns, cancellations) rather than full funnel analysis. Understanding <em>why</em> customers don't return would require data this dataset does not contain.</p>

<p><strong>Time-series stationarity not tested:</strong> The long-term and seasonal trend analyses identify patterns visually but do not apply statistical tests for trend significance or seasonality decomposition. A more rigorous approach would use time-series methods – moving averages, decomposition, or forecasting models – which is beyond SQL's native capabilities and better suited to Python or R.</p>

<p><strong>No A/B testing or causal inference:</strong> All findings are correlational. Recommendations like "improve sizing tools to reduce returns" are grounded in observed patterns but would need controlled experiments to validate causal impact before committing significant resources.</p>

<p><strong>Potential future extensions:</strong> This analysis could be extended with customer cohort and retention analysis (tracking repeat purchase behavior over time), RFM segmentation (Recency, Frequency, Monetary value scoring), market basket analysis (which products are frequently purchased together), or predictive modeling for return probability – each of which would require tools beyond SQL and would build naturally on the foundation established here.</p>
</div>

<h3>Tools Used</h3>

<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">
<ul>
<li><strong>Google BigQuery</strong> – cloud data warehouse, Standard SQL dialect</li>
<li><strong>BigQuery public dataset:</strong> <code>bigquery-public-data.thelook_ecommerce</code></li>
<li><strong>No external tools:</strong> All analysis performed entirely within SQL – no data export, no spreadsheet processing, no visualization libraries. Charts in the Long Term Trends and Seasonal Trends sections were produced separately from query result exports, but all underlying analysis is SQL-native.</li>
</ul>
</div>

</details>
