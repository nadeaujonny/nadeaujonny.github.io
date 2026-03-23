---
layout: default
title: E-commerce Sales Analysis (SQL)
description: "Analyzing 1M+ e-commerce orders in BigQuery using advanced SQL — CTEs, window functions, and time-series logic — to examine products, brands, categories, trends, and customers."
---

<a href="/projects/" class="back-to-projects btn">← Back to Projects</a>

# E-commerce Sales Analysis (SQL)

> This project analyzes the BigQuery **thelook_ecommerce** dataset to identify ways to optimize the company using advanced SQL.

---

<details>
  <summary><strong>Introduction</strong></summary>

  <div style="margin-top: 12px;"></div>

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

<h3>Top products by Profit</h3>

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
  profit_rank ASC
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
    <tr><td>Bergama Natural Raccoon Hooded Stroller - - Multicolor</td><td>Bergama</td><td>Outerwear & Coats</td><td>749.99</td><td>306.75</td><td>2999.96</td><td>1772.98</td><td>10</td><td>4</td><td>1</td><td>0</td><td>5</td><td>749.99</td><td>443.24</td><td>0.591</td><td>0.2</td><td>0.4</td><td>0.0</td><td>0.5556</td><td>0.0011113</td><td>0.0012671</td><td>5.52e-05</td><td>40</td><td>43</td><td>4</td><td>3</td><td>1962</td><td>776</td><td>3978</td><td>17458</td><td>3026</td><td>267</td><td>224</td><td>3279</td><td>12637</td><td>7482</td><td>17458</td><td>19270</td></tr>
    <tr><td>Spyder Women's Jesst In Time Jacket</td><td>Spyder</td><td>Outerwear & Coats</td><td>650.0</td><td>295.75</td><td>3250.0</td><td>1771.25</td><td>10</td><td>5</td><td>4</td><td>0</td><td>1</td><td>2600.0</td><td>1417.0</td><td>0.545</td><td>0.4444</td><td>0.5</td><td>0.0</td><td>0.1667</td><td>0.0012039</td><td>0.0012659</td><td>5.52e-05</td><td>52</td><td>50</td><td>3</td><td>4</td><td>1962</td><td>251</td><td>30</td><td>17458</td><td>23197</td><td>7</td><td>7</td><td>8121</td><td>8264</td><td>3269</td><td>17458</td><td>27059</td></tr>
    <tr><td>Joseph Abboud Men's Two-button Side Vent Sport Coat</td><td>Joseph Abboud</td><td>Suits & Sport Coats</td><td>264.0</td><td>101.9</td><td>2904.0</td><td>1759.82</td><td>30</td><td>11</td><td>2</td><td>2</td><td>15</td><td>1056.0</td><td>656.57</td><td>0.606</td><td>0.1538</td><td>0.3929</td><td>0.0667</td><td>0.5769</td><td>0.0010758</td><td>0.0012577</td><td>0.0001655</td><td>430</td><td>734</td><td>6</td><td>5</td><td>7</td><td>3</td><td>844</td><td>2100</td><td>11</td><td>112</td><td>91</td><td>2144</td><td>13388</td><td>9081</td><td>17408</td><td>18610</td></tr>
    <tr><td>Woolrich Arctic Parka DF</td><td>Woolrich</td><td>Outerwear & Coats</td><td>990.0</td><td>478.17</td><td>2970.0</td><td>1535.49</td><td>12</td><td>3</td><td>2</td><td>1</td><td>6</td><td>2970.0</td><td>1535.49</td><td>0.517</td><td>0.4</td><td>0.2727</td><td>0.0833</td><td>0.6667</td><td>0.0011002</td><td>0.0010974</td><td>6.62e-05</td><td>3</td><td>6</td><td>5</td><td>6</td><td>694</td><td>2358</td><td>844</td><td>7029</td><td>1398</td><td>4</td><td>4</td><td>10735</td><td>8312</td><td>14284</td><td>17144</td><td>12990</td></tr>
    <tr><td>The North Face Denali Down Mens Jacket 2013</td><td>The North Face</td><td>Outerwear & Coats</td><td>903.0</td><td>436.15</td><td>2709.0</td><td>1400.55</td><td>13</td><td>3</td><td>2</td><td>2</td><td>6</td><td>3612.0</td><td>1867.4</td><td>0.517</td><td>0.4</td><td>0.2727</td><td>0.1538</td><td>0.6667</td><td>0.0010035</td><td>0.001001</td><td>7.17e-05</td><td>5</td><td>10</td><td>7</td><td>7</td><td>423</td><td>2358</td><td>844</td><td>2100</td><td>1398</td><td>2</td><td>3</td><td>10735</td><td>8312</td><td>14284</td><td>12634</td><td>12990</td></tr>
    <tr><td>Michael Kors Men's Marlow Wool-Blend Single-Breasted Fitted Top Coat</td><td>Michael Kors</td><td>Outerwear & Coats</td><td>255.0</td><td>102.26</td><td>2295.0</td><td>1374.7</td><td>15</td><td>9</td><td>1</td><td>2</td><td>3</td><td>765.0</td><td>458.23</td><td>0.599</td><td>0.1</td><td>0.6923</td><td>0.1333</td><td>0.25</td><td>0.0008502</td><td>0.0009825</td><td>8.27e-05</td><td>469</td><td>728</td><td>13</td><td>8</td><td>187</td><td>5</td><td>3978</td><td>2100</td><td>10869</td><td>252</td><td>208</td><td>2612</td><td>13461</td><td>1184</td><td>14317</td><td>26348</td></tr>
    <tr><td>AIR JORDAN DOMINATE SHORTS MENS 465071-100</td><td>Jordan</td><td>Shorts</td><td>903.0</td><td>454.21</td><td>2709.0</td><td>1346.37</td><td>5</td><td>3</td><td>0</td><td>0</td><td>2</td><td>0.0</td><td>0.0</td><td>0.497</td><td>0.0</td><td>0.6</td><td>0.0</td><td>0.4</td><td>0.0010035</td><td>0.0009622</td><td>2.76e-05</td><td>5</td><td>8</td><td>7</td><td>9</td><td>16887</td><td>2358</td><td>13463</td><td>17458</td><td>17069</td><td>22642</td><td>22642</td><td>12874</td><td>13463</td><td>2189</td><td>17458</td><td>23875</td></tr>
    <tr><td>Diesel Men's Lagnum Leather Jacket</td><td>Diesel</td><td>Outerwear & Coats</td><td>598.0</td><td>267.9</td><td>2392.0</td><td>1320.38</td><td>7</td><td>4</td><td>1</td><td>1</td><td>1</td><td>1196.0</td><td>660.19</td><td>0.552</td><td>0.2</td><td>0.6667</td><td>0.1429</td><td>0.2</td><td>0.0008861</td><td>0.0009437</td><td>3.86e-05</td><td>57</td><td>56</td><td>9</td><td>10</td><td>8625</td><td>776</td><td>3978</td><td>7029</td><td>23197</td><td>92</td><td>89</td><td>7373</td><td>12637</td><td>1185</td><td>12706</td><td>26859</td></tr>
    <tr><td>Men's Classic Sheepskin B-3 Bomber Jacket</td><td>Overland Sheepskin Co</td><td>Outerwear & Coats</td><td>595.0</td><td>270.73</td><td>2380.0</td><td>1297.1</td><td>13</td><td>4</td><td>0</td><td>2</td><td>7</td><td>1190.0</td><td>648.55</td><td>0.545</td><td>0.0</td><td>0.3636</td><td>0.1538</td><td>0.6364</td><td>0.0008816</td><td>0.000927</td><td>7.17e-05</td><td>60</td><td>55</td><td>12</td><td>11</td><td>423</td><td>776</td><td>13463</td><td>2100</td><td>623</td><td>95</td><td>94</td><td>8121</td><td>13463</td><td>9638</td><td>12634</td><td>16487</td></tr>
    <tr><td>Nobis Merideth Parka</td><td>Nobis</td><td>Outerwear & Coats</td><td>795.0</td><td>382.39</td><td>2385.0</td><td>1237.82</td><td>7</td><td>3</td><td>1</td><td>1</td><td>2</td><td>1590.0</td><td>825.21</td><td>0.519</td><td>0.25</td><td>0.5</td><td>0.1429</td><td>0.4</td><td>0.0008835</td><td>0.0008847</td><td>3.86e-05</td><td>33</td><td>23</td><td>10</td><td>12</td><td>8625</td><td>2358</td><td>3978</td><td>7029</td><td>17069</td><td>37</td><td>45</td><td>10485</td><td>11344</td><td>3269</td><td>12706</td><td>23875</td></tr>
    <tr><td>Canada Goose Women's Expedition Parka</td><td>Canada Goose</td><td>Outerwear & Coats</td><td>795.0</td><td>395.91</td><td>2385.0</td><td>1197.27</td><td>4</td><td>3</td><td>0</td><td>1</td><td>0</td><td>795.0</td><td>399.09</td><td>0.502</td><td>0.0</td><td>1.0</td><td>0.25</td><td>0.0</td><td>0.0008835</td><td>0.0008557</td><td>2.21e-05</td><td>33</td><td>19</td><td>10</td><td>13</td><td>21053</td><td>2358</td><td>13463</td><td>7029</td><td>27145</td><td>230</td><td>277</td><td>12357</td><td>13463</td><td>1</td><td>5542</td><td>27145</td></tr>
    <tr><td>Canada Goose Women's Solaris</td><td>Canada Goose</td><td>Outerwear & Coats</td><td>695.0</td><td>296.76</td><td>2085.0</td><td>1194.71</td><td>6</td><td>3</td><td>0</td><td>2</td><td>1</td><td>1390.0</td><td>796.47</td><td>0.573</td><td>0.0</td><td>0.75</td><td>0.3333</td><td>0.25</td><td>0.0007724</td><td>0.0008538</td><td>3.31e-05</td><td>46</td><td>48</td><td>17</td><td>14</td><td>12532</td><td>2358</td><td>13463</td><td>2100</td><td>23197</td><td>67</td><td>52</td><td>5041</td><td>13463</td><td>746</td><td>2619</td><td>26348</td></tr>
    <tr><td>Darla</td><td>Alpha Industries</td><td>Outerwear & Coats</td><td>999.0</td><td>404.6</td><td>1998.0</td><td>1188.81</td><td>7</td><td>2</td><td>2</td><td>0</td><td>3</td><td>1998.0</td><td>1188.81</td><td>0.595</td><td>0.5</td><td>0.2857</td><td>0.0</td><td>0.6</td><td>0.0007401</td><td>0.0008496</td><td>3.86e-05</td><td>1</td><td>16</td><td>18</td><td>15</td><td>8625</td><td>6114</td><td>844</td><td>17458</td><td>10869</td><td>14</td><td>14</td><td>2925</td><td>4275</td><td>13238</td><td>17458</td><td>16953</td></tr>
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

<h3>Top products by Unit Orders</h3>

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
  unit_orders_placed_rank ASC
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
    <tr><td>Wrangler Men's Premium Performance Cowboy Cut Jean</td><td>Wrangler</td><td>Jeans</td><td>47.45</td><td>25.88</td><td>570.83</td><td>264.22</td><td>58</td><td>12</td><td>2</td><td>7</td><td>37</td><td>417.81</td><td>189.65</td><td>0.4629</td><td>0.1429</td><td>0.2353</td><td>0.1207</td><td>0.7551</td><td>0.0002115</td><td>0.0001888</td><td>0.00032</td><td>12004</td><td>10508</td><td>470</td><td>662</td><td>1</td><td>2</td><td>844</td><td>2</td><td>1</td><td>905</td><td>1224</td><td>16149</td><td>13389</td><td>17092</td><td>15548</td><td>9486</td></tr>
    <tr><td>7 For All Mankind Men's Standard Classic Straight Leg Jean</td><td>7 For All Mankind</td><td>Jeans</td><td>157.45</td><td>80.97</td><td>1435.0</td><td>696.01</td><td>42</td><td>9</td><td>5</td><td>5</td><td>23</td><td>1673.0</td><td>844.04</td><td>0.485</td><td>0.3571</td><td>0.2432</td><td>0.119</td><td>0.7188</td><td>0.0005316</td><td>0.0004974</td><td>0.0002317</td><td>1798</td><td>1488</td><td>46</td><td>60</td><td>2</td><td>5</td><td>5</td><td>24</td><td>2</td><td>32</td><td>41</td><td>14028</td><td>8749</td><td>17091</td><td>15552</td><td>12034</td></tr>
    <tr><td>Wrangler Men's Rugged Wear Classic Fit Jean</td><td>Wrangler</td><td>Jeans</td><td>40.87</td><td>22.23</td><td>367.56</td><td>169.24</td><td>38</td><td>9</td><td>5</td><td>9</td><td>15</td><td>596.43</td><td>273.96</td><td>0.4604</td><td>0.3571</td><td>0.3103</td><td>0.2368</td><td>0.625</td><td>0.0001362</td><td>0.000121</td><td>0.0002096</td><td>13688</td><td>12514</td><td>1205</td><td>1552</td><td>3</td><td>5</td><td>5</td><td>1</td><td>11</td><td>440</td><td>628</td><td>16340</td><td>8749</td><td>13014</td><td>7776</td><td>16547</td></tr>
    <tr><td>True Religion Men's Ricky Straight Jean</td><td>True Religion</td><td>Jeans</td><td>246.88</td><td>129.05</td><td>1366.0</td><td>666.07</td><td>34</td><td>5</td><td>4</td><td>3</td><td>22</td><td>1400.0</td><td>654.5</td><td>0.4876</td><td>0.4444</td><td>0.1613</td><td>0.0882</td><td>0.8148</td><td>0.000506</td><td>0.000476</td><td>0.0001876</td><td>534</td><td>354</td><td>56</td><td>65</td><td>4</td><td>251</td><td>30</td><td>526</td><td>3</td><td>63</td><td>92</td><td>13792</td><td>8264</td><td>20804</td><td>17143</td><td>7595</td></tr>
    <tr><td>Kenneth Cole REACTION Men's Passcase Wallet</td><td>Kenneth Cole REACTION</td><td>Accessories</td><td>18.91</td><td>7.72</td><td>152.71</td><td>89.4</td><td>34</td><td>8</td><td>4</td><td>4</td><td>18</td><td>150.85</td><td>90.57</td><td>0.5854</td><td>0.3333</td><td>0.2667</td><td>0.1176</td><td>0.6923</td><td>5.66e-05</td><td>6.39e-05</td><td>0.0001876</td><td>23389</td><td>24481</td><td>4958</td><td>4188</td><td>4</td><td>16</td><td>30</td><td>126</td><td>4</td><td>5015</td><td>4078</td><td>3806</td><td>8752</td><td>14395</td><td>15553</td><td>12966</td></tr>
    <tr><td>HUGO BOSS Men's Long Pant</td><td>HUGO BOSS</td><td>Sleep & Lounge</td><td>74.72</td><td>28.3</td><td>1033.11</td><td>648.16</td><td>33</td><td>14</td><td>0</td><td>3</td><td>16</td><td>233.01</td><td>138.21</td><td>0.6274</td><td>0.0</td><td>0.4667</td><td>0.0909</td><td>0.5333</td><td>0.0003827</td><td>0.0004632</td><td>0.000182</td><td>6501</td><td>9383</td><td>113</td><td>75</td><td>6</td><td>1</td><td>13463</td><td>526</td><td>7</td><td>2702</td><td>2165</td><td>933</td><td>13463</td><td>6418</td><td>16872</td><td>19494</td></tr>
    <tr><td>Joseph Abboud Men's Two-button Side Vent Sport Coat</td><td>Joseph Abboud</td><td>Suits & Sport Coats</td><td>264.0</td><td>101.9</td><td>2904.0</td><td>1759.82</td><td>30</td><td>11</td><td>2</td><td>2</td><td>15</td><td>1056.0</td><td>656.57</td><td>0.606</td><td>0.1538</td><td>0.3929</td><td>0.0667</td><td>0.5769</td><td>0.0010758</td><td>0.0012577</td><td>0.0001655</td><td>430</td><td>734</td><td>6</td><td>5</td><td>7</td><td>3</td><td>844</td><td>2100</td><td>11</td><td>112</td><td>91</td><td>2144</td><td>13388</td><td>9081</td><td>17408</td><td>18610</td></tr>
    <tr><td>Wrangler Men's Genuine Tampa Cargo Short</td><td>Wrangler</td><td>Shorts</td><td>31.37</td><td>15.61</td><td>229.94</td><td>116.44</td><td>29</td><td>7</td><td>1</td><td>5</td><td>16</td><td>179.94</td><td>90.54</td><td>0.5064</td><td>0.125</td><td>0.2917</td><td>0.1724</td><td>0.6957</td><td>8.52e-05</td><td>8.32e-05</td><td>0.00016</td><td>17403</td><td>17266</td><td>2818</td><td>2869</td><td>8</td><td>33</td><td>3978</td><td>24</td><td>7</td><td>3935</td><td>4081</td><td>11924</td><td>13444</td><td>13236</td><td>10730</td><td>12964</td></tr>
    <tr><td>Hanes Men's 4 Pack Boxer Brief</td><td>Hanes</td><td>Underwear</td><td>25.0</td><td>11.52</td><td>250.0</td><td>133.47</td><td>28</td><td>10</td><td>2</td><td>5</td><td>11</td><td>175.0</td><td>92.77</td><td>0.5339</td><td>0.1667</td><td>0.4348</td><td>0.1786</td><td>0.5238</td><td>9.26e-05</td><td>9.54e-05</td><td>0.0001545</td><td>19651</td><td>20997</td><td>2432</td><td>2340</td><td>9</td><td>4</td><td>844</td><td>24</td><td>43</td><td>4152</td><td>3935</td><td>9232</td><td>13196</td><td>6738</td><td>10715</td><td>19500</td></tr>
    <tr><td>Chaps Big and Tall Solid V-Neck Vest</td><td>Chaps</td><td>Sweaters</td><td>39.88</td><td>20.32</td><td>279.16</td><td>134.91</td><td>28</td><td>7</td><td>4</td><td>1</td><td>16</td><td>199.4</td><td>99.06</td><td>0.4833</td><td>0.3636</td><td>0.2593</td><td>0.0357</td><td>0.6957</td><td>0.0001034</td><td>9.64e-05</td><td>0.0001545</td><td>14437</td><td>13747</td><td>2029</td><td>2288</td><td>9</td><td>33</td><td>30</td><td>7029</td><td>7</td><td>3354</td><td>3543</td><td>14237</td><td>8748</td><td>14407</td><td>17457</td><td>12964</td></tr>
    <tr><td>True Religion Men's Ricky Straight Leg Jean</td><td>True Religion</td><td>Jeans</td><td>227.86</td><td>123.14</td><td>1452.0</td><td>661.01</td><td>28</td><td>7</td><td>1</td><td>5</td><td>15</td><td>1430.0</td><td>645.85</td><td>0.4552</td><td>0.125</td><td>0.3043</td><td>0.1786</td><td>0.6818</td><td>0.0005379</td><td>0.0004724</td><td>0.0001545</td><td>646</td><td>406</td><td>45</td><td>69</td><td>9</td><td>33</td><td>3978</td><td>24</td><td>11</td><td>57</td><td>95</td><td>16801</td><td>13444</td><td>13032</td><td>10715</td><td>12986</td></tr>
    <tr><td>Joe's Jeans Men's Slim Fit Straight Leg Brixton</td><td>Joe's Jeans</td><td>Jeans</td><td>194.26</td><td>102.07</td><td>1353.0</td><td>647.44</td><td>27</td><td>7</td><td>3</td><td>2</td><td>15</td><td>976.0</td><td>458.49</td><td>0.4785</td><td>0.3</td><td>0.28</td><td>0.0741</td><td>0.6818</td><td>0.0005012</td><td>0.0004627</td><td>0.0001489</td><td>992</td><td>729</td><td>58</td><td>76</td><td>12</td><td>33</td><td>151</td><td>2100</td><td>11</td><td>133</td><td>207</td><td>14773</td><td>11276</td><td>14282</td><td>17370</td><td>12986</td></tr>
    <tr><td>Dockers Men's Suit Separate Coat</td><td>Dockers</td><td>Suits & Sport Coats</td><td>88.36</td><td>33.97</td><td>231.12</td><td>140.98</td><td>27</td><td>3</td><td>4</td><td>2</td><td>18</td><td>542.11</td><td>337.6</td><td>0.61</td><td>0.5714</td><td>0.12</td><td>0.0741</td><td>0.8571</td><td>8.56e-05</td><td>0.0001008</td><td>0.0001489</td><td>5094</td><td>7229</td><td>2783</td><td>2122</td><td>12</td><td>2358</td><td>30</td><td>2100</td><td>4</td><td>542</td><td>391</td><td>1873</td><td>4252</td><td>22129</td><td>17370</td><td>6057</td></tr>
    <tr><td>Volcom Men's Kinkade Jean</td><td>Volcom</td><td>Jeans</td><td>66.67</td><td>35.17</td><td>269.9</td><td>125.86</td><td>27</td><td>4</td><td>3</td><td>5</td><td>15</td><td>538.25</td><td>254.63</td><td>0.4663</td><td>0.4286</td><td>0.1818</td><td>0.1852</td><td>0.7895</td><td>0.0001</td><td>9e-05</td><td>0.0001489</td><td>7633</td><td>6807</td><td>2158</td><td>2560</td><td>12</td><td>776</td><td>151</td><td>24</td><td>11</td><td>562</td><td>723</td><td>15806</td><td>8270</td><td>19358</td><td>10467</td><td>9273</td></tr>
    <tr><td>Wrangler Men's Wrancher Dress Jean</td><td>Wrangler</td><td>Jeans</td><td>40.4</td><td>20.2</td><td>242.4</td><td>118.65</td><td>27</td><td>6</td><td>2</td><td>3</td><td>16</td><td>202.0</td><td>102.05</td><td>0.4895</td><td>0.25</td><td>0.25</td><td>0.1111</td><td>0.7273</td><td>8.98e-05</td><td>8.48e-05</td><td>0.0001489</td><td>13728</td><td>13816</td><td>2533</td><td>2788</td><td>12</td><td>84</td><td>844</td><td>526</td><td>7</td><td>3236</td><td>3382</td><td>13585</td><td>11344</td><td>14408</td><td>15570</td><td>11980</td></tr>
  </tbody>
</table>

</div>

<h3>Top products by Return Rate</h3>

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
WHERE lost_profit_rank &lt;= 15
ORDER BY
  return_rate_rank ASC
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
    <tr><td>IGIGI by Yuliya Raquel Plus Size Kandinsky Gown</td><td>IGIGI by Yuliya Raquel</td><td>Dresses</td><td>325.0</td><td>136.17</td><td>0.0</td><td>0.0</td><td>13</td><td>0</td><td>3</td><td>5</td><td>5</td><td>2600.0</td><td>1510.6</td><td></td><td>1.0</td><td>0.0</td><td>0.3846</td><td>1.0</td><td>0.0</td><td>0.0</td><td>7.17e-05</td><td>236</td><td>300</td><td>22532</td><td>22532</td><td>423</td><td>22532</td><td>151</td><td>24</td><td>3026</td><td>7</td><td>5</td><td>22532</td><td>1</td><td>22532</td><td>2333</td><td>1</td></tr>
    <tr><td>MiH Jeans Women's Aztec Jacket</td><td>MiH Jeans</td><td>Blazers & Jackets</td><td>495.0</td><td>169.79</td><td>0.0</td><td>0.0</td><td>6</td><td>0</td><td>2</td><td>2</td><td>2</td><td>1980.0</td><td>1300.86</td><td></td><td>1.0</td><td>0.0</td><td>0.3333</td><td>1.0</td><td>0.0</td><td>0.0</td><td>3.31e-05</td><td>74</td><td>157</td><td>22532</td><td>22532</td><td>12532</td><td>22532</td><td>844</td><td>2100</td><td>17069</td><td>16</td><td>11</td><td>22532</td><td>1</td><td>22532</td><td>2619</td><td>1</td></tr>
    <tr><td>Canada Goose Men's The Chateau Jacket</td><td>Canada Goose</td><td>Active</td><td>815.0</td><td>337.41</td><td>0.0</td><td>0.0</td><td>6</td><td>0</td><td>1</td><td>4</td><td>1</td><td>4075.0</td><td>2387.95</td><td></td><td>1.0</td><td>0.0</td><td>0.6667</td><td>1.0</td><td>0.0</td><td>0.0</td><td>3.31e-05</td><td>31</td><td>39</td><td>22532</td><td>22532</td><td>12532</td><td>22532</td><td>3978</td><td>126</td><td>23197</td><td>1</td><td>1</td><td>22532</td><td>1</td><td>22532</td><td>154</td><td>1</td></tr>
    <tr><td>Canada Goose Women's Chilliwack Bomber</td><td>Canada Goose</td><td>Outerwear & Coats</td><td>695.0</td><td>287.73</td><td>695.0</td><td>407.27</td><td>8</td><td>1</td><td>3</td><td>2</td><td>2</td><td>3475.0</td><td>2036.35</td><td>0.586</td><td>0.75</td><td>0.1667</td><td>0.25</td><td>0.6667</td><td>0.0002575</td><td>0.0002911</td><td>4.41e-05</td><td>46</td><td>52</td><td>294</td><td>240</td><td>5507</td><td>13264</td><td>151</td><td>2100</td><td>17069</td><td>3</td><td>2</td><td>3719</td><td>2834</td><td>19436</td><td>5542</td><td>12990</td></tr>
    <tr><td>Mens Nike AirJordan Varsity Hoodie Jacket Grey / Black 451582-066</td><td>Jordan</td><td>Outerwear & Coats</td><td>903.0</td><td>409.06</td><td>903.0</td><td>493.94</td><td>8</td><td>1</td><td>2</td><td>1</td><td>4</td><td>2709.0</td><td>1481.82</td><td>0.547</td><td>0.6667</td><td>0.1429</td><td>0.125</td><td>0.8</td><td>0.0003345</td><td>0.000353</td><td>4.41e-05</td><td>5</td><td>14</td><td>149</td><td>153</td><td>5507</td><td>13264</td><td>844</td><td>7029</td><td>6105</td><td>5</td><td>6</td><td>7915</td><td>3055</td><td>20815</td><td>14338</td><td>7598</td></tr>
    <tr><td>Joseph Abboud Men's Super 120's Two Button Side Vent Single Pleat Pant Tuxedo With Grosgrain Notch Lapel</td><td>Joseph Abboud</td><td>Suits & Sport Coats</td><td>405.26</td><td>145.08</td><td>405.26</td><td>260.18</td><td>11</td><td>1</td><td>2</td><td>3</td><td>5</td><td>2026.3</td><td>1300.88</td><td>0.642</td><td>0.6667</td><td>0.125</td><td>0.2727</td><td>0.8333</td><td>0.0001501</td><td>0.0001859</td><td>6.07e-05</td><td>108</td><td>256</td><td>961</td><td>686</td><td>1161</td><td>13264</td><td>844</td><td>526</td><td>3026</td><td>13</td><td>10</td><td>361</td><td>3055</td><td>21675</td><td>5408</td><td>6580</td></tr>
    <tr><td>Canada Goose Women's Mystique</td><td>Canada Goose</td><td>Outerwear & Coats</td><td>750.0</td><td>353.25</td><td>1500.0</td><td>793.5</td><td>6</td><td>2</td><td>3</td><td>0</td><td>1</td><td>2250.0</td><td>1190.25</td><td>0.529</td><td>0.6</td><td>0.3333</td><td>0.0</td><td>0.3333</td><td>0.0005557</td><td>0.0005671</td><td>3.31e-05</td><td>37</td><td>35</td><td>41</td><td>44</td><td>12532</td><td>6114</td><td>151</td><td>17458</td><td>23197</td><td>9</td><td>13</td><td>9645</td><td>4103</td><td>9747</td><td>17458</td><td>24854</td></tr>
    <tr><td>DOLCE & GABBANA DG4167 501/8G BLACK GRAY GRADIENT 5917</td><td>Dolce & Gabbana</td><td>Accessories</td><td>243.0</td><td>94.67</td><td>486.0</td><td>294.03</td><td>14</td><td>2</td><td>3</td><td>5</td><td>4</td><td>1944.0</td><td>1194.59</td><td>0.605</td><td>0.6</td><td>0.2222</td><td>0.3571</td><td>0.6667</td><td>0.00018</td><td>0.0002101</td><td>7.72e-05</td><td>541</td><td>948</td><td>707</td><td>527</td><td>268</td><td>6114</td><td>151</td><td>24</td><td>6105</td><td>18</td><td>12</td><td>2194</td><td>4103</td><td>17122</td><td>2614</td><td>12990</td></tr>
    <tr><td>Darla</td><td>Alpha Industries</td><td>Outerwear & Coats</td><td>999.0</td><td>404.6</td><td>1998.0</td><td>1188.81</td><td>7</td><td>2</td><td>2</td><td>0</td><td>3</td><td>1998.0</td><td>1188.81</td><td>0.595</td><td>0.5</td><td>0.2857</td><td>0.0</td><td>0.6</td><td>0.0007401</td><td>0.0008496</td><td>3.86e-05</td><td>1</td><td>16</td><td>18</td><td>15</td><td>8625</td><td>6114</td><td>844</td><td>17458</td><td>10869</td><td>14</td><td>14</td><td>2925</td><td>4275</td><td>13238</td><td>17458</td><td>16953</td></tr>
    <tr><td>Magaschoni Women's Shimmer Jacket</td><td>Magaschoni</td><td>Blazers & Jackets</td><td>698.0</td><td>258.96</td><td>698.0</td><td>439.04</td><td>6</td><td>1</td><td>1</td><td>2</td><td>2</td><td>2094.0</td><td>1317.13</td><td>0.629</td><td>0.5</td><td>0.25</td><td>0.3333</td><td>0.6667</td><td>0.0002586</td><td>0.0003138</td><td>3.31e-05</td><td>43</td><td>58</td><td>288</td><td>201</td><td>12532</td><td>13264</td><td>3978</td><td>2100</td><td>17069</td><td>12</td><td>9</td><td>839</td><td>4275</td><td>14408</td><td>2619</td><td>12990</td></tr>
    <tr><td>Canada Goose Women's Mystique</td><td>Canada Goose</td><td>Active</td><td>750.0</td><td>280.5</td><td>750.0</td><td>469.5</td><td>9</td><td>1</td><td>1</td><td>2</td><td>5</td><td>2250.0</td><td>1408.5</td><td>0.626</td><td>0.5</td><td>0.1429</td><td>0.2222</td><td>0.8333</td><td>0.0002778</td><td>0.0003355</td><td>4.96e-05</td><td>37</td><td>53</td><td>230</td><td>170</td><td>3355</td><td>13264</td><td>3978</td><td>2100</td><td>3026</td><td>9</td><td>8</td><td>984</td><td>4275</td><td>20815</td><td>7837</td><td>6580</td></tr>
    <tr><td>Spyder Women's Jesst In Time Jacket</td><td>Spyder</td><td>Outerwear & Coats</td><td>650.0</td><td>295.75</td><td>3250.0</td><td>1771.25</td><td>10</td><td>5</td><td>4</td><td>0</td><td>1</td><td>2600.0</td><td>1417.0</td><td>0.545</td><td>0.4444</td><td>0.5</td><td>0.0</td><td>0.1667</td><td>0.0012039</td><td>0.0012659</td><td>5.52e-05</td><td>52</td><td>50</td><td>3</td><td>4</td><td>1962</td><td>251</td><td>30</td><td>17458</td><td>23197</td><td>7</td><td>7</td><td>8121</td><td>8264</td><td>3269</td><td>17458</td><td>27059</td></tr>
    <tr><td>Woolrich Arctic Parka DF</td><td>Woolrich</td><td>Outerwear & Coats</td><td>990.0</td><td>478.17</td><td>2970.0</td><td>1535.49</td><td>12</td><td>3</td><td>2</td><td>1</td><td>6</td><td>2970.0</td><td>1535.49</td><td>0.517</td><td>0.4</td><td>0.2727</td><td>0.0833</td><td>0.6667</td><td>0.0011002</td><td>0.0010974</td><td>6.62e-05</td><td>3</td><td>6</td><td>5</td><td>6</td><td>694</td><td>2358</td><td>844</td><td>7029</td><td>1398</td><td>4</td><td>4</td><td>10735</td><td>8312</td><td>14284</td><td>17144</td><td>12990</td></tr>
    <tr><td>The North Face Denali Down Mens Jacket 2013</td><td>The North Face</td><td>Outerwear & Coats</td><td>903.0</td><td>436.15</td><td>2709.0</td><td>1400.55</td><td>13</td><td>3</td><td>2</td><td>2</td><td>6</td><td>3612.0</td><td>1867.4</td><td>0.517</td><td>0.4</td><td>0.2727</td><td>0.1538</td><td>0.6667</td><td>0.0010035</td><td>0.001001</td><td>7.17e-05</td><td>5</td><td>10</td><td>7</td><td>7</td><td>423</td><td>2358</td><td>844</td><td>2100</td><td>1398</td><td>2</td><td>3</td><td>10735</td><td>8312</td><td>14284</td><td>12634</td><td>12990</td></tr>
    <tr><td>NIKE WOMEN'S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort*</td><td>Nike</td><td>Intimates</td><td>903.0</td><td>512.0</td><td>0.0</td><td>0.0</td><td>4</td><td>0</td><td>0</td><td>3</td><td>1</td><td>2709.0</td><td>1173.0</td><td></td><td></td><td>0.0</td><td>0.75</td><td>1.0</td><td>0.0</td><td>0.0</td><td>2.21e-05</td><td>5</td><td>4</td><td>22532</td><td>22532</td><td>21053</td><td>22532</td><td>13463</td><td>526</td><td>23197</td><td>5</td><td>15</td><td>22532</td><td>25326</td><td>22532</td><td>109</td><td>1</td></tr>
  </tbody>
</table>

</div>

<h3>Top products by Units Returned</h3>

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
  units_returned_rank ASC
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
    <tr><td>Kenneth Cole Men's Straight Leg Jean</td><td>Kenneth Cole</td><td>Jeans</td><td>54.25</td><td>27.11</td><td>54.99</td><td>26.89</td><td>24</td><td>1</td><td>7</td><td>4</td><td>12</td><td>632.25</td><td>318.8</td><td>0.489</td><td>0.875</td><td>0.05</td><td>0.1667</td><td>0.9231</td><td>2.04e-05</td><td>1.92e-05</td><td>0.0001324</td><td>10100</td><td>9920</td><td>13356</td><td>13628</td><td>30</td><td>13264</td><td>1</td><td>126</td><td>37</td><td>380</td><td>462</td><td>13602</td><td>2795</td><td>22531</td><td>10731</td><td>5642</td></tr>
    <tr><td>Alex Stevens Men's Chevron Cuff Cardigan</td><td>Alex Stevens</td><td>Sweaters</td><td>26.0</td><td>11.78</td><td>26.0</td><td>14.22</td><td>14</td><td>1</td><td>7</td><td>0</td><td>6</td><td>182.0</td><td>99.55</td><td>0.5469</td><td>0.875</td><td>0.0714</td><td>0.0</td><td>0.8571</td><td>9.6e-06</td><td>1.02e-05</td><td>7.72e-05</td><td>19363</td><td>20777</td><td>18768</td><td>18407</td><td>268</td><td>13264</td><td>1</td><td>17458</td><td>1398</td><td>3788</td><td>3516</td><td>7983</td><td>2795</td><td>22525</td><td>17458</td><td>6057</td></tr>
    <tr><td>Womenâ€™s UA Baseâ„¢ 4.0 Leggings Bottoms by Under Armour</td><td>Under Armour</td><td>Active</td><td>63.99</td><td>23.93</td><td>127.98</td><td>80.12</td><td>12</td><td>2</td><td>6</td><td>2</td><td>2</td><td>511.92</td><td>320.46</td><td>0.626</td><td>0.75</td><td>0.2</td><td>0.1667</td><td>0.5</td><td>4.74e-05</td><td>5.73e-05</td><td>6.62e-05</td><td>8152</td><td>11520</td><td>6273</td><td>4860</td><td>694</td><td>6114</td><td>3</td><td>2100</td><td>17069</td><td>616</td><td>453</td><td>984</td><td>2834</td><td>17510</td><td>10731</td><td>19501</td></tr>
    <tr><td>G by GUESS Cosmos Slit-Front Top</td><td>G by GUESS</td><td>Tops & Tees</td><td>29.5</td><td>16.87</td><td>88.5</td><td>37.88</td><td>13</td><td>3</td><td>6</td><td>1</td><td>3</td><td>206.5</td><td>88.38</td><td>0.428</td><td>0.6667</td><td>0.25</td><td>0.0769</td><td>0.5</td><td>3.28e-05</td><td>2.71e-05</td><td>7.17e-05</td><td>18349</td><td>16195</td><td>9301</td><td>10674</td><td>423</td><td>2358</td><td>3</td><td>7029</td><td>10869</td><td>3172</td><td>4221</td><td>19180</td><td>3055</td><td>14408</td><td>17286</td><td>19501</td></tr>
    <tr><td>G-Star Men's Attacc Straight Vintage Jean</td><td>G-Star</td><td>Jeans</td><td>210.0</td><td>102.9</td><td>210.0</td><td>107.1</td><td>7</td><td>1</td><td>5</td><td>0</td><td>1</td><td>1050.0</td><td>535.5</td><td>0.51</td><td>0.8333</td><td>0.1429</td><td>0.0</td><td>0.5</td><td>7.78e-05</td><td>7.65e-05</td><td>3.86e-05</td><td>737</td><td>713</td><td>3106</td><td>3251</td><td>8625</td><td>13264</td><td>5</td><td>17458</td><td>23197</td><td>113</td><td>132</td><td>11510</td><td>2797</td><td>20815</td><td>17458</td><td>19501</td></tr>
    <tr><td>Quiksilver Waterman Men's Cabo 3 Walkshort</td><td>Quiksilver</td><td>Shorts</td><td>35.98</td><td>18.39</td><td>35.98</td><td>17.59</td><td>10</td><td>1</td><td>5</td><td>1</td><td>3</td><td>215.88</td><td>105.57</td><td>0.4889</td><td>0.8333</td><td>0.1111</td><td>0.1</td><td>0.75</td><td>1.33e-05</td><td>1.26e-05</td><td>5.52e-05</td><td>15686</td><td>15023</td><td>16878</td><td>17002</td><td>1962</td><td>13264</td><td>5</td><td>7029</td><td>10869</td><td>2994</td><td>3212</td><td>13683</td><td>2797</td><td>22130</td><td>16366</td><td>9487</td></tr>
    <tr><td>Icebreaker Men's Kodiak Zip Jacket</td><td>Icebreaker</td><td>Outerwear & Coats</td><td>250.0</td><td>122.5</td><td>250.0</td><td>127.5</td><td>13</td><td>1</td><td>5</td><td>1</td><td>6</td><td>1500.0</td><td>765.0</td><td>0.51</td><td>0.8333</td><td>0.0833</td><td>0.0769</td><td>0.8571</td><td>9.26e-05</td><td>9.11e-05</td><td>7.17e-05</td><td>480</td><td>413</td><td>2432</td><td>2507</td><td>423</td><td>13264</td><td>5</td><td>7029</td><td>1398</td><td>43</td><td>60</td><td>11510</td><td>2797</td><td>22497</td><td>17286</td><td>6057</td></tr>
    <tr><td>Levi's Women's Demi Curve Slim Fit Jean</td><td>Levi's</td><td>Jeans</td><td>44.99</td><td>25.36</td><td>359.92</td><td>158.59</td><td>22</td><td>8</td><td>5</td><td>3</td><td>6</td><td>359.92</td><td>157.29</td><td>0.4406</td><td>0.3846</td><td>0.4211</td><td>0.1364</td><td>0.4286</td><td>0.0001333</td><td>0.0001133</td><td>0.0001214</td><td>12553</td><td>10773</td><td>1272</td><td>1757</td><td>43</td><td>16</td><td>5</td><td>526</td><td>1398</td><td>1228</td><td>1730</td><td>18170</td><td>8724</td><td>7452</td><td>14315</td><td>23541</td></tr>
    <tr><td>Ames Walker Style 166 Men's Microfiber Firm Support Travel Socks 15-20 - Available in Various Sizes and Colors</td><td>Ames</td><td>Socks</td><td>12.99</td><td>8.07</td><td>12.99</td><td>4.92</td><td>11</td><td>1</td><td>5</td><td>2</td><td>3</td><td>90.93</td><td>34.46</td><td>0.3788</td><td>0.8333</td><td>0.1111</td><td>0.1818</td><td>0.75</td><td>4.8e-06</td><td>3.5e-06</td><td>6.07e-05</td><td>25756</td><td>24123</td><td>21580</td><td>22067</td><td>1161</td><td>13264</td><td>5</td><td>2100</td><td>10869</td><td>8965</td><td>11517</td><td>21711</td><td>2797</td><td>22130</td><td>10468</td><td>9487</td></tr>
    <tr><td>Under Armour Igniter Pro Sport Sunglasses</td><td>Under Armour</td><td>Accessories</td><td>94.99</td><td>41.47</td><td>284.97</td><td>162.72</td><td>17</td><td>3</td><td>5</td><td>3</td><td>6</td><td>759.92</td><td>424.04</td><td>0.571</td><td>0.625</td><td>0.2143</td><td>0.1765</td><td>0.6667</td><td>0.0001056</td><td>0.0001163</td><td>9.38e-05</td><td>4573</td><td>5187</td><td>1952</td><td>1668</td><td>103</td><td>2358</td><td>5</td><td>526</td><td>1398</td><td>255</td><td>249</td><td>5261</td><td>4099</td><td>17490</td><td>10717</td><td>12990</td></tr>
    <tr><td>Men's Superior 150s Single Breasted Two Button Black Pinstripe Dress Suit European Cut</td><td>Giorgio Cerruti</td><td>Suits & Sport Coats</td><td>69.95</td><td>27.98</td><td>209.85</td><td>125.91</td><td>16</td><td>3</td><td>5</td><td>0</td><td>8</td><td>349.75</td><td>209.85</td><td>0.6</td><td>0.625</td><td>0.1875</td><td>0.0</td><td>0.7273</td><td>7.77e-05</td><td>9e-05</td><td>8.83e-05</td><td>6978</td><td>9517</td><td>3144</td><td>2557</td><td>150</td><td>2358</td><td>5</td><td>17458</td><td>295</td><td>1333</td><td>1043</td><td>2533</td><td>4099</td><td>19354</td><td>17458</td><td>11980</td></tr>
    <tr><td>Wrangler Men's Rugged Wear Classic Fit Jean</td><td>Wrangler</td><td>Jeans</td><td>40.87</td><td>22.23</td><td>367.56</td><td>169.24</td><td>38</td><td>9</td><td>5</td><td>9</td><td>15</td><td>596.43</td><td>273.96</td><td>0.4604</td><td>0.3571</td><td>0.3103</td><td>0.2368</td><td>0.625</td><td>0.0001362</td><td>0.000121</td><td>0.0002096</td><td>13688</td><td>12514</td><td>1205</td><td>1552</td><td>3</td><td>5</td><td>5</td><td>1</td><td>11</td><td>440</td><td>628</td><td>16340</td><td>8749</td><td>13014</td><td>7776</td><td>16547</td></tr>
    <tr><td>Wrangler Men's Original Cowboy Cut Relaxed Fit Jean</td><td>Wrangler</td><td>Jeans</td><td>42.99</td><td>22.67</td><td>228.46</td><td>108.63</td><td>25</td><td>5</td><td>5</td><td>7</td><td>8</td><td>493.18</td><td>228.73</td><td>0.4755</td><td>0.5</td><td>0.2778</td><td>0.28</td><td>0.6154</td><td>8.46e-05</td><td>7.76e-05</td><td>0.0001379</td><td>13180</td><td>12269</td><td>2826</td><td>3184</td><td>21</td><td>251</td><td>5</td><td>2</td><td>295</td><td>687</td><td>895</td><td>15040</td><td>4275</td><td>14283</td><td>5404</td><td>16940</td></tr>
    <tr><td>Robert Graham Men's Cheshire</td><td>Robert Graham</td><td>Tops & Tees</td><td>179.99</td><td>92.69</td><td>179.99</td><td>87.3</td><td>11</td><td>1</td><td>5</td><td>1</td><td>4</td><td>1079.94</td><td>523.77</td><td>0.485</td><td>0.8333</td><td>0.1</td><td>0.0909</td><td>0.8</td><td>6.67e-05</td><td>6.24e-05</td><td>6.07e-05</td><td>1179</td><td>1014</td><td>3947</td><td>4329</td><td>1161</td><td>13264</td><td>5</td><td>7029</td><td>6105</td><td>110</td><td>145</td><td>14028</td><td>2797</td><td>22369</td><td>16872</td><td>7598</td></tr>
    <tr><td>Tolani Women's Daphne Top</td><td>Tolani</td><td>Tops & Tees</td><td>194.0</td><td>104.95</td><td>388.0</td><td>178.09</td><td>12</td><td>2</td><td>5</td><td>1</td><td>4</td><td>1164.0</td><td>534.28</td><td>0.459</td><td>0.7143</td><td>0.1818</td><td>0.0833</td><td>0.6667</td><td>0.0001437</td><td>0.0001273</td><td>6.62e-05</td><td>993</td><td>654</td><td>1103</td><td>1402</td><td>694</td><td>6114</td><td>5</td><td>7029</td><td>6105</td><td>103</td><td>134</td><td>16449</td><td>3052</td><td>19358</td><td>17144</td><td>12990</td></tr>
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

<h3>Top products by Lost Profit</h3>

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
  lost_profit_rank ASC
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
    <tr><td>Canada Goose Women's Chilliwack Bomber</td><td>Canada Goose</td><td>Outerwear & Coats</td><td>695.0</td><td>287.73</td><td>695.0</td><td>407.27</td><td>8</td><td>1</td><td>3</td><td>2</td><td>2</td><td>3475.0</td><td>2036.35</td><td>0.586</td><td>0.75</td><td>0.1667</td><td>0.25</td><td>0.6667</td><td>0.0002575</td><td>0.0002911</td><td>4.41e-05</td><td>46</td><td>52</td><td>294</td><td>240</td><td>5507</td><td>13264</td><td>151</td><td>2100</td><td>17069</td><td>3</td><td>2</td><td>3719</td><td>2834</td><td>19436</td><td>5542</td><td>12990</td></tr>
    <tr><td>The North Face Denali Down Mens Jacket 2013</td><td>The North Face</td><td>Outerwear & Coats</td><td>903.0</td><td>436.15</td><td>2709.0</td><td>1400.55</td><td>13</td><td>3</td><td>2</td><td>2</td><td>6</td><td>3612.0</td><td>1867.4</td><td>0.517</td><td>0.4</td><td>0.2727</td><td>0.1538</td><td>0.6667</td><td>0.0010035</td><td>0.001001</td><td>7.17e-05</td><td>5</td><td>10</td><td>7</td><td>7</td><td>423</td><td>2358</td><td>844</td><td>2100</td><td>1398</td><td>2</td><td>3</td><td>10735</td><td>8312</td><td>14284</td><td>12634</td><td>12990</td></tr>
    <tr><td>Woolrich Arctic Parka DF</td><td>Woolrich</td><td>Outerwear & Coats</td><td>990.0</td><td>478.17</td><td>2970.0</td><td>1535.49</td><td>12</td><td>3</td><td>2</td><td>1</td><td>6</td><td>2970.0</td><td>1535.49</td><td>0.517</td><td>0.4</td><td>0.2727</td><td>0.0833</td><td>0.6667</td><td>0.0011002</td><td>0.0010974</td><td>6.62e-05</td><td>3</td><td>6</td><td>5</td><td>6</td><td>694</td><td>2358</td><td>844</td><td>7029</td><td>1398</td><td>4</td><td>4</td><td>10735</td><td>8312</td><td>14284</td><td>17144</td><td>12990</td></tr>
    <tr><td>IGIGI by Yuliya Raquel Plus Size Kandinsky Gown</td><td>IGIGI by Yuliya Raquel</td><td>Dresses</td><td>325.0</td><td>136.17</td><td>0.0</td><td>0.0</td><td>13</td><td>0</td><td>3</td><td>5</td><td>5</td><td>2600.0</td><td>1510.6</td><td></td><td>1.0</td><td>0.0</td><td>0.3846</td><td>1.0</td><td>0.0</td><td>0.0</td><td>7.17e-05</td><td>236</td><td>300</td><td>22532</td><td>22532</td><td>423</td><td>22532</td><td>151</td><td>24</td><td>3026</td><td>7</td><td>5</td><td>22532</td><td>1</td><td>22532</td><td>2333</td><td>1</td></tr>
    <tr><td>Mens Nike AirJordan Varsity Hoodie Jacket Grey / Black 451582-066</td><td>Jordan</td><td>Outerwear & Coats</td><td>903.0</td><td>409.06</td><td>903.0</td><td>493.94</td><td>8</td><td>1</td><td>2</td><td>1</td><td>4</td><td>2709.0</td><td>1481.82</td><td>0.547</td><td>0.6667</td><td>0.1429</td><td>0.125</td><td>0.8</td><td>0.0003345</td><td>0.000353</td><td>4.41e-05</td><td>5</td><td>14</td><td>149</td><td>153</td><td>5507</td><td>13264</td><td>844</td><td>7029</td><td>6105</td><td>5</td><td>6</td><td>7915</td><td>3055</td><td>20815</td><td>14338</td><td>7598</td></tr>
    <tr><td>Spyder Women's Jesst In Time Jacket</td><td>Spyder</td><td>Outerwear & Coats</td><td>650.0</td><td>295.75</td><td>3250.0</td><td>1771.25</td><td>10</td><td>5</td><td>4</td><td>0</td><td>1</td><td>2600.0</td><td>1417.0</td><td>0.545</td><td>0.4444</td><td>0.5</td><td>0.0</td><td>0.1667</td><td>0.0012039</td><td>0.0012659</td><td>5.52e-05</td><td>52</td><td>50</td><td>3</td><td>4</td><td>1962</td><td>251</td><td>30</td><td>17458</td><td>23197</td><td>7</td><td>7</td><td>8121</td><td>8264</td><td>3269</td><td>17458</td><td>27059</td></tr>
    <tr><td>Canada Goose Women's Mystique</td><td>Canada Goose</td><td>Active</td><td>750.0</td><td>280.5</td><td>750.0</td><td>469.5</td><td>9</td><td>1</td><td>1</td><td>2</td><td>5</td><td>2250.0</td><td>1408.5</td><td>0.626</td><td>0.5</td><td>0.1429</td><td>0.2222</td><td>0.8333</td><td>0.0002778</td><td>0.0003355</td><td>4.96e-05</td><td>37</td><td>53</td><td>230</td><td>170</td><td>3355</td><td>13264</td><td>3978</td><td>2100</td><td>3026</td><td>9</td><td>8</td><td>984</td><td>4275</td><td>20815</td><td>7837</td><td>6580</td></tr>
    <tr><td>Magaschoni Women's Shimmer Jacket</td><td>Magaschoni</td><td>Blazers & Jackets</td><td>698.0</td><td>258.96</td><td>698.0</td><td>439.04</td><td>6</td><td>1</td><td>1</td><td>2</td><td>2</td><td>2094.0</td><td>1317.13</td><td>0.629</td><td>0.5</td><td>0.25</td><td>0.3333</td><td>0.6667</td><td>0.0002586</td><td>0.0003138</td><td>3.31e-05</td><td>43</td><td>58</td><td>288</td><td>201</td><td>12532</td><td>13264</td><td>3978</td><td>2100</td><td>17069</td><td>12</td><td>9</td><td>839</td><td>4275</td><td>14408</td><td>2619</td><td>12990</td></tr>
    <tr><td>Joseph Abboud Men's Super 120's Two Button Side Vent Single Pleat Pant Tuxedo With Grosgrain Notch Lapel</td><td>Joseph Abboud</td><td>Suits & Sport Coats</td><td>405.26</td><td>145.08</td><td>405.26</td><td>260.18</td><td>11</td><td>1</td><td>2</td><td>3</td><td>5</td><td>2026.3</td><td>1300.88</td><td>0.642</td><td>0.6667</td><td>0.125</td><td>0.2727</td><td>0.8333</td><td>0.0001501</td><td>0.0001859</td><td>6.07e-05</td><td>108</td><td>256</td><td>961</td><td>686</td><td>1161</td><td>13264</td><td>844</td><td>526</td><td>3026</td><td>13</td><td>10</td><td>361</td><td>3055</td><td>21675</td><td>5408</td><td>6580</td></tr>
    <tr><td>MiH Jeans Women's Aztec Jacket</td><td>MiH Jeans</td><td>Blazers & Jackets</td><td>495.0</td><td>169.79</td><td>0.0</td><td>0.0</td><td>6</td><td>0</td><td>2</td><td>2</td><td>2</td><td>1980.0</td><td>1300.86</td><td></td><td>1.0</td><td>0.0</td><td>0.3333</td><td>1.0</td><td>0.0</td><td>0.0</td><td>3.31e-05</td><td>74</td><td>157</td><td>22532</td><td>22532</td><td>12532</td><td>22532</td><td>844</td><td>2100</td><td>17069</td><td>16</td><td>11</td><td>22532</td><td>1</td><td>22532</td><td>2619</td><td>1</td></tr>
    <tr><td>DOLCE & GABBANA DG4167 501/8G BLACK GRAY GRADIENT 5917</td><td>Dolce & Gabbana</td><td>Accessories</td><td>243.0</td><td>94.67</td><td>486.0</td><td>294.03</td><td>14</td><td>2</td><td>3</td><td>5</td><td>4</td><td>1944.0</td><td>1194.59</td><td>0.605</td><td>0.6</td><td>0.2222</td><td>0.3571</td><td>0.6667</td><td>0.00018</td><td>0.0002101</td><td>7.72e-05</td><td>541</td><td>948</td><td>707</td><td>527</td><td>268</td><td>6114</td><td>151</td><td>24</td><td>6105</td><td>18</td><td>12</td><td>2194</td><td>4103</td><td>17122</td><td>2614</td><td>12990</td></tr>
    <tr><td>Canada Goose Women's Mystique</td><td>Canada Goose</td><td>Outerwear & Coats</td><td>750.0</td><td>353.25</td><td>1500.0</td><td>793.5</td><td>6</td><td>2</td><td>3</td><td>0</td><td>1</td><td>2250.0</td><td>1190.25</td><td>0.529</td><td>0.6</td><td>0.3333</td><td>0.0</td><td>0.3333</td><td>0.0005557</td><td>0.0005671</td><td>3.31e-05</td><td>37</td><td>35</td><td>41</td><td>44</td><td>12532</td><td>6114</td><td>151</td><td>17458</td><td>23197</td><td>9</td><td>13</td><td>9645</td><td>4103</td><td>9747</td><td>17458</td><td>24854</td></tr>
    <tr><td>Darla</td><td>Alpha Industries</td><td>Outerwear & Coats</td><td>999.0</td><td>404.6</td><td>1998.0</td><td>1188.81</td><td>7</td><td>2</td><td>2</td><td>0</td><td>3</td><td>1998.0</td><td>1188.81</td><td>0.595</td><td>0.5</td><td>0.2857</td><td>0.0</td><td>0.6</td><td>0.0007401</td><td>0.0008496</td><td>3.86e-05</td><td>1</td><td>16</td><td>18</td><td>15</td><td>8625</td><td>6114</td><td>844</td><td>17458</td><td>10869</td><td>14</td><td>14</td><td>2925</td><td>4275</td><td>13238</td><td>17458</td><td>16953</td></tr>
    <tr><td>NIKE WOMEN'S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort*</td><td>Nike</td><td>Intimates</td><td>903.0</td><td>512.0</td><td>0.0</td><td>0.0</td><td>4</td><td>0</td><td>0</td><td>3</td><td>1</td><td>2709.0</td><td>1173.0</td><td></td><td></td><td>0.0</td><td>0.75</td><td>1.0</td><td>0.0</td><td>0.0</td><td>2.21e-05</td><td>5</td><td>4</td><td>22532</td><td>22532</td><td>21053</td><td>22532</td><td>13463</td><td>526</td><td>23197</td><td>5</td><td>15</td><td>22532</td><td>25326</td><td>22532</td><td>109</td><td>1</td></tr>
  </tbody>
</table>

</div>

<h3>Analytical Insights & Business Recommendations</h3>
<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p>The top 15 products by revenue are overwhelmingly dominated by Outerwear & Coats (11 of 15), with premium brands like The North Face, Canada Goose, Woolrich, Spyder, and Arc'teryx. This category commands the highest average sale prices ($595–$999) and generates the most revenue per unit sold. The top revenue product, ASICS Cushion Low Socks, is anomalous — priced at $903 (likely a data entry error or premium bundle) but sitting in the Active category. It ranks #1 in both revenue and profit with $3,612 and $2,116.63 respectively. Joseph Abboud Men's Sport Coat stands out as a high-volume high-revenue outlier with 30 unit orders placed (rank #7 across all products) while also ranking #5 in profit. This combination of volume and margin makes it the strongest candidate for promotional investment among top products.</p>

<p>The highest profit margin products (~66.9%) are exclusively Blazers & Jackets from mid-range brands (Fashion Love, Ulla Popken, Ted Baker, Eddie Bauer, DKNYC). These have low costs relative to sale prices but individually small revenue contributions. Since these high-margin blazer products have small individual revenue footprints, promote them in cohorts — bundle or cross-sell multiple blazer/jacket items together to amplify the margin advantage across a group rather than relying on individual unit sales. For top revenue products that already have strong demand (like the Joseph Abboud Sport Coat at 60.6% margin), consider strategic price testing. With 30 orders placed and strong brand recognition, there may be room to incrementally increase price by 3–5% without meaningfully reducing demand, yielding significant net profit gains given the volume.</p>

<p>The highest-volume products (Wrangler, 7 For All Mankind, True Religion jeans) rank in the top 15 by unit orders but have notably lower profit margins (45–49%) compared to outerwear. These jeans brands drive order volume but contribute disproportionately less to profit. For these high-volume, lower-margin jeans products, focus on cost reduction strategies — negotiate better supplier pricing on Wrangler and 7 For All Mankind given the volume leverage. Even a small per-unit cost reduction on 40–58 unit orders compounds meaningfully. Consider bundling high-volume jeans with higher-margin accessories (belts, socks) to increase average order value and overall basket margin.</p>

<p>Several top products have alarming return/cancellation profiles. The Canada Goose Men's Chateau Jacket has $0 in completed revenue — 100% of its orders were returned or cancelled, yet it ranks #1 in lost revenue ($4,075) and lost profit ($2,387.95). This product is generating no value while consuming inventory space, shipping bandwidth, and processing resources. IGIGI Kandinsky Gown similarly has a 100% return rate with $0 revenue and $2,600 in lost revenue. Both products warrant immediate quality inspection and supplier communication. The Spyder Women's Jesst In Time Jacket has a 44.4% return rate but still ranks #3 in revenue ($3,250) and #4 in profit ($1,771.25), meaning the returns are masking what could be even stronger performance. Investigate root causes of returns — sizing issues, product description mismatches, or quality defects. Products with high return rates among the top earners (Woolrich Arctic Parka at 40%, North Face Denali Down at 40%) should be flagged for quality inspection. Their return-related losses ($2,970 and $3,612 respectively) nearly equal their actual revenue, meaning nearly half of all potential profit is evaporating.</p>

<p>Many top products show 60–80% of their non-cancelled/returned orders still in transit (en route). This is a significant operational signal — high en-route rates on premium outerwear suggest either very recent order surges or systemic delays in shipping and fulfillment for high-value items. Investigate shipping and processing timelines specifically for premium outerwear ($500+ items). If transit times are longer due to heavier packaging or insurance requirements, explore dedicated fulfillment lanes for high-value products to reduce lost-revenue risk from cancellations during extended shipping windows.</p>

<p>Products like AIR JORDAN DOMINATE SHORTS (0% return rate, $2,709 revenue) and Canada Goose Women's Expedition Parka (0% return rate, 100% completion rate, $2,385 revenue) demonstrate that high revenue and zero returns are achievable simultaneously. Examine what makes these zero-return products successful — supplier quality, accurate product descriptions, proper sizing information — and replicate those practices across the product catalog, especially for high-return items in the same categories.</p>

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

<h3>Bottom products by Profit</h3>

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
WHERE unit_orders_placed_rank &lt;= 50
ORDER BY
  profit_rank DESC
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
    <tr><td>HUGO BOSS Men's Bright Argyle Crew Sock</td><td>HUGO BOSS</td><td>Socks</td><td>9.75</td><td>5.68</td><td>39.0</td><td>15.65</td><td>22</td><td>4</td><td>4</td><td>4</td><td>10</td><td>78.0</td><td>32.25</td><td>0.4013</td><td>0.5</td><td>0.2222</td><td>0.1818</td><td>0.7143</td><td>1.44e-05</td><td>1.12e-05</td><td>0.0001214</td><td>27342</td><td>26355</td><td>16327</td><td>17765</td><td>43</td><td>776</td><td>30</td><td>126</td><td>77</td><td>10368</td><td>12068</td><td>20837</td><td>4275</td><td>17122</td><td>10468</td><td>12035</td></tr>
    <tr><td>New Men's Sexy Center Patch Bikini Swimsuit 3G by Gregg Homme</td><td>Gregg Homme</td><td>Swim</td><td>13.22</td><td>7.85</td><td>54.6</td><td>20.64</td><td>25</td><td>4</td><td>2</td><td>5</td><td>14</td><td>90.3</td><td>38.29</td><td>0.378</td><td>0.3333</td><td>0.2</td><td>0.2</td><td>0.7778</td><td>2.02e-05</td><td>1.48e-05</td><td>0.0001379</td><td>25672</td><td>24345</td><td>13422</td><td>15782</td><td>21</td><td>776</td><td>844</td><td>24</td><td>22</td><td>8973</td><td>10649</td><td>21721</td><td>8752</td><td>17510</td><td>8435</td><td>9281</td></tr>
    <tr><td>Kenneth Cole Men's Straight Leg Jean</td><td>Kenneth Cole</td><td>Jeans</td><td>54.25</td><td>27.11</td><td>54.99</td><td>26.89</td><td>24</td><td>1</td><td>7</td><td>4</td><td>12</td><td>632.25</td><td>318.8</td><td>0.489</td><td>0.875</td><td>0.05</td><td>0.1667</td><td>0.9231</td><td>2.04e-05</td><td>1.92e-05</td><td>0.0001324</td><td>10100</td><td>9920</td><td>13356</td><td>13628</td><td>30</td><td>13264</td><td>1</td><td>126</td><td>37</td><td>380</td><td>462</td><td>13602</td><td>2795</td><td>22531</td><td>10731</td><td>5642</td></tr>
    <tr><td>Tommy Hilfiger Men Classic Fit T-shirt</td><td>Tommy Hilfiger</td><td>Tops & Tees</td><td>21.99</td><td>12.22</td><td>65.97</td><td>28.41</td><td>25</td><td>3</td><td>2</td><td>5</td><td>15</td><td>153.93</td><td>70.63</td><td>0.4307</td><td>0.4</td><td>0.15</td><td>0.2</td><td>0.8333</td><td>2.44e-05</td><td>2.03e-05</td><td>0.0001379</td><td>22049</td><td>20333</td><td>11887</td><td>13165</td><td>21</td><td>2358</td><td>844</td><td>24</td><td>11</td><td>4954</td><td>5704</td><td>18998</td><td>8312</td><td>20814</td><td>8435</td><td>6580</td></tr>
    <tr><td>Volcom Juniors Pocket Blocket Long Sleeve Tee</td><td>Volcom</td><td>Tops & Tees</td><td>27.0</td><td>15.34</td><td>81.0</td><td>33.86</td><td>21</td><td>3</td><td>4</td><td>5</td><td>9</td><td>243.0</td><td>107.41</td><td>0.418</td><td>0.5714</td><td>0.1875</td><td>0.2381</td><td>0.75</td><td>3e-05</td><td>2.42e-05</td><td>0.0001158</td><td>19072</td><td>17500</td><td>9846</td><td>11622</td><td>50</td><td>2358</td><td>30</td><td>24</td><td>140</td><td>2456</td><td>3131</td><td>20016</td><td>4252</td><td>19354</td><td>7773</td><td>9487</td></tr>
    <tr><td>Puma Men's Socks</td><td>PUMA</td><td>Socks</td><td>13.0</td><td>7.78</td><td>90.0</td><td>35.98</td><td>24</td><td>7</td><td>1</td><td>5</td><td>11</td><td>78.0</td><td>31.36</td><td>0.3998</td><td>0.125</td><td>0.3684</td><td>0.2083</td><td>0.6111</td><td>3.33e-05</td><td>2.57e-05</td><td>0.0001324</td><td>25705</td><td>24414</td><td>8929</td><td>11107</td><td>30</td><td>33</td><td>3978</td><td>24</td><td>43</td><td>10368</td><td>12295</td><td>20955</td><td>13444</td><td>9637</td><td>8433</td><td>16951</td></tr>
    <tr><td>HUGO BOSS Men's Striped Crew Sock</td><td>HUGO BOSS</td><td>Socks</td><td>13.0</td><td>8.14</td><td>104.0</td><td>40.17</td><td>24</td><td>8</td><td>3</td><td>4</td><td>9</td><td>91.0</td><td>33.33</td><td>0.3863</td><td>0.2727</td><td>0.4</td><td>0.1667</td><td>0.5294</td><td>3.85e-05</td><td>2.87e-05</td><td>0.0001324</td><td>25705</td><td>24062</td><td>7764</td><td>10157</td><td>30</td><td>16</td><td>151</td><td>126</td><td>140</td><td>8958</td><td>11794</td><td>21483</td><td>11342</td><td>7482</td><td>10731</td><td>19498</td></tr>
    <tr><td>Lilly Pulitzer Women's Callahan Short</td><td>Lilly Pulitzer</td><td>Shorts</td><td>48.24</td><td>24.35</td><td>106.11</td><td>53.14</td><td>24</td><td>2</td><td>4</td><td>5</td><td>13</td><td>420.02</td><td>207.44</td><td>0.5008</td><td>0.6667</td><td>0.1053</td><td>0.2083</td><td>0.8667</td><td>3.93e-05</td><td>3.8e-05</td><td>0.0001324</td><td>11747</td><td>11307</td><td>7626</td><td>7813</td><td>30</td><td>6114</td><td>30</td><td>24</td><td>31</td><td>883</td><td>1063</td><td>12538</td><td>3055</td><td>22368</td><td>8433</td><td>6056</td></tr>
    <tr><td>Lee Men's Relaxed Fit Slightly Tapered Leg Jean</td><td>Lee</td><td>Jeans</td><td>30.99</td><td>16.89</td><td>122.96</td><td>55.54</td><td>21</td><td>4</td><td>5</td><td>3</td><td>9</td><td>248.92</td><td>113.31</td><td>0.4517</td><td>0.5556</td><td>0.2222</td><td>0.1429</td><td>0.6923</td><td>4.55e-05</td><td>3.97e-05</td><td>0.0001158</td><td>17446</td><td>16178</td><td>6481</td><td>7447</td><td>50</td><td>776</td><td>5</td><td>526</td><td>140</td><td>2405</td><td>2891</td><td>17150</td><td>4274</td><td>17122</td><td>12706</td><td>12966</td></tr>
    <tr><td>Bottoms Out Men's Plaid Sleep Pant</td><td>Bottoms Out</td><td>Sleep & Lounge</td><td>13.49</td><td>5.05</td><td>94.43</td><td>59.4</td><td>25</td><td>7</td><td>2</td><td>4</td><td>12</td><td>80.94</td><td>50.64</td><td>0.629</td><td>0.2222</td><td>0.3333</td><td>0.16</td><td>0.6316</td><td>3.5e-05</td><td>4.25e-05</td><td>0.0001379</td><td>25625</td><td>26913</td><td>8758</td><td>6904</td><td>21</td><td>33</td><td>844</td><td>126</td><td>37</td><td>9890</td><td>8299</td><td>839</td><td>12628</td><td>9747</td><td>12630</td><td>16546</td></tr>
    <tr><td>RSQ London Mens Skinny Jeans</td><td>RSQ</td><td>Jeans</td><td>44.99</td><td>24.2</td><td>134.97</td><td>63.21</td><td>21</td><td>3</td><td>5</td><td>3</td><td>10</td><td>359.92</td><td>163.94</td><td>0.4683</td><td>0.625</td><td>0.1667</td><td>0.1429</td><td>0.7692</td><td>5e-05</td><td>4.52e-05</td><td>0.0001158</td><td>12553</td><td>11383</td><td>5908</td><td>6477</td><td>50</td><td>2358</td><td>5</td><td>526</td><td>77</td><td>1228</td><td>1608</td><td>15636</td><td>4099</td><td>19436</td><td>12706</td><td>9471</td></tr>
    <tr><td>Diesel Men's Blade Underpant</td><td>Diesel</td><td>Underwear</td><td>22.14</td><td>9.75</td><td>122.0</td><td>66.53</td><td>22</td><td>6</td><td>0</td><td>2</td><td>14</td><td>43.0</td><td>23.83</td><td>0.5453</td><td>0.0</td><td>0.3</td><td>0.0909</td><td>0.7</td><td>4.52e-05</td><td>4.75e-05</td><td>0.0001214</td><td>21886</td><td>22702</td><td>6504</td><td>6114</td><td>43</td><td>84</td><td>13463</td><td>2100</td><td>22</td><td>15676</td><td>14732</td><td>8115</td><td>13463</td><td>13033</td><td>16872</td><td>12849</td></tr>
    <tr><td>Michael Kors Men's 3 Pack Brief</td><td>Michael Kors</td><td>Underwear</td><td>25.99</td><td>12.48</td><td>130.46</td><td>67.73</td><td>24</td><td>5</td><td>5</td><td>4</td><td>10</td><td>232.38</td><td>120.98</td><td>0.5192</td><td>0.5</td><td>0.25</td><td>0.1667</td><td>0.6667</td><td>4.83e-05</td><td>4.84e-05</td><td>0.0001324</td><td>19456</td><td>20053</td><td>6070</td><td>5979</td><td>30</td><td>251</td><td>5</td><td>126</td><td>77</td><td>2705</td><td>2646</td><td>10469</td><td>4275</td><td>14408</td><td>10731</td><td>12990</td></tr>
    <tr><td>RUDE Dark Vintage Skinny Jeans</td><td>Hot Topic</td><td>Jeans</td><td>36.5</td><td>19.33</td><td>146.0</td><td>68.99</td><td>24</td><td>4</td><td>4</td><td>3</td><td>13</td><td>255.5</td><td>123.41</td><td>0.4725</td><td>0.5</td><td>0.1905</td><td>0.125</td><td>0.7647</td><td>5.41e-05</td><td>4.93e-05</td><td>0.0001324</td><td>15396</td><td>14389</td><td>5357</td><td>5845</td><td>30</td><td>776</td><td>30</td><td>526</td><td>31</td><td>2306</td><td>2570</td><td>15319</td><td>4275</td><td>19353</td><td>14338</td><td>9484</td></tr>
    <tr><td>Bottoms Out Men's Plaid Sleep Jam</td><td>Bottoms Out</td><td>Sleep & Lounge</td><td>25.0</td><td>9.3</td><td>125.0</td><td>78.03</td><td>24</td><td>5</td><td>2</td><td>2</td><td>15</td><td>100.0</td><td>63.2</td><td>0.6242</td><td>0.2857</td><td>0.2273</td><td>0.0833</td><td>0.75</td><td>4.63e-05</td><td>5.58e-05</td><td>0.0001324</td><td>19651</td><td>23078</td><td>6364</td><td>5026</td><td>30</td><td>251</td><td>844</td><td>2100</td><td>11</td><td>7972</td><td>6500</td><td>1088</td><td>11280</td><td>17121</td><td>17144</td><td>9487</td></tr>
  </tbody>
</table>

</div>

<h3>Bottom products by Profit Margin</h3>

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
    <tr><td>The North Face Apex Bionic Soft Shell Jacket - Men's</td><td>The North Face</td><td>Fashion Hoodies & Sweatshirts</td><td>903.0</td><td>524.64</td><td>1806.0</td><td>756.71</td><td>6</td><td>2</td><td>0</td><td>0</td><td>4</td><td>0.0</td><td>0.0</td><td>0.419</td><td>0.0</td><td>0.3333</td><td>0.0</td><td>0.6667</td><td>0.000669</td><td>0.0005408</td><td>3.31e-05</td><td>5</td><td>3</td><td>21</td><td>55</td><td>12532</td><td>6114</td><td>13463</td><td>17458</td><td>6105</td><td>22642</td><td>22642</td><td>19960</td><td>13463</td><td>9747</td><td>17458</td><td>12990</td></tr>
    <tr><td>PAIGE Women's Skyline Skinny Jean</td><td>PAIGE</td><td>Jeans</td><td>158.0</td><td>90.19</td><td>1422.0</td><td>608.93</td><td>19</td><td>9</td><td>0</td><td>2</td><td>8</td><td>316.0</td><td>135.88</td><td>0.4282</td><td>0.0</td><td>0.5294</td><td>0.1053</td><td>0.4706</td><td>0.0005268</td><td>0.0004352</td><td>0.0001048</td><td>1714</td><td>1108</td><td>48</td><td>90</td><td>72</td><td>5</td><td>13463</td><td>2100</td><td>295</td><td>1575</td><td>2230</td><td>19172</td><td>13463</td><td>3268</td><td>16363</td><td>23444</td></tr>
    <tr><td>7 For All Mankind Men's Austyn Relaxed Straight Jean</td><td>7 For All Mankind</td><td>Jeans</td><td>197.94</td><td>111.63</td><td>1399.0</td><td>608.64</td><td>17</td><td>7</td><td>0</td><td>1</td><td>9</td><td>189.0</td><td>83.35</td><td>0.4351</td><td>0.0</td><td>0.4375</td><td>0.0588</td><td>0.5625</td><td>0.0005182</td><td>0.000435</td><td>9.38e-05</td><td>942</td><td>526</td><td>50</td><td>91</td><td>103</td><td>33</td><td>13463</td><td>7029</td><td>140</td><td>3671</td><td>4605</td><td>18597</td><td>13463</td><td>6734</td><td>17433</td><td>19266</td></tr>
    <tr><td>Catherine Malandrino Women's Stretch Leather Pant</td><td>Catherine Malandrino</td><td>Leggings</td><td>528.81</td><td>291.37</td><td>1586.43</td><td>712.31</td><td>5</td><td>3</td><td>1</td><td>0</td><td>1</td><td>528.81</td><td>237.44</td><td>0.449</td><td>0.25</td><td>0.6</td><td>0.0</td><td>0.25</td><td>0.0005877</td><td>0.0005091</td><td>2.76e-05</td><td>68</td><td>51</td><td>38</td><td>59</td><td>16887</td><td>2358</td><td>3978</td><td>17458</td><td>23197</td><td>584</td><td>835</td><td>17380</td><td>11344</td><td>2189</td><td>17458</td><td>26348</td></tr>
    <tr><td>True Religion Men's Ricky Straight Leg Jean</td><td>True Religion</td><td>Jeans</td><td>227.86</td><td>123.14</td><td>1452.0</td><td>661.01</td><td>28</td><td>7</td><td>1</td><td>5</td><td>15</td><td>1430.0</td><td>645.85</td><td>0.4552</td><td>0.125</td><td>0.3043</td><td>0.1786</td><td>0.6818</td><td>0.0005379</td><td>0.0004724</td><td>0.0001545</td><td>646</td><td>406</td><td>45</td><td>69</td><td>9</td><td>33</td><td>3978</td><td>24</td><td>11</td><td>57</td><td>95</td><td>16801</td><td>13444</td><td>13032</td><td>10715</td><td>12986</td></tr>
    <tr><td>Diesel Men's Shioner Skinny Straight Leg Jean</td><td>Diesel</td><td>Jeans</td><td>295.98</td><td>157.9</td><td>1695.85</td><td>779.71</td><td>25</td><td>6</td><td>2</td><td>3</td><td>14</td><td>1431.9</td><td>657.85</td><td>0.4598</td><td>0.25</td><td>0.2727</td><td>0.12</td><td>0.7</td><td>0.0006282</td><td>0.0005572</td><td>0.0001379</td><td>318</td><td>201</td><td>33</td><td>50</td><td>21</td><td>84</td><td>844</td><td>526</td><td>22</td><td>56</td><td>90</td><td>16428</td><td>11344</td><td>14284</td><td>15549</td><td>12849</td></tr>
    <tr><td>True Religion Women's Julie Super T Jean</td><td>True Religion</td><td>Jeans</td><td>326.0</td><td>172.13</td><td>1956.0</td><td>923.23</td><td>8</td><td>6</td><td>0</td><td>1</td><td>1</td><td>326.0</td><td>153.87</td><td>0.472</td><td>0.0</td><td>0.8571</td><td>0.125</td><td>0.1429</td><td>0.0007246</td><td>0.0006598</td><td>4.41e-05</td><td>233</td><td>145</td><td>19</td><td>31</td><td>5507</td><td>84</td><td>13463</td><td>7029</td><td>23197</td><td>1487</td><td>1788</td><td>15335</td><td>13463</td><td>546</td><td>14338</td><td>27121</td></tr>
    <tr><td>Quiksilver Men's Rockefeller Walkshort</td><td>Quiksilver</td><td>Shorts</td><td>903.0</td><td>472.27</td><td>1806.0</td><td>861.46</td><td>6</td><td>2</td><td>0</td><td>0</td><td>4</td><td>0.0</td><td>0.0</td><td>0.477</td><td>0.0</td><td>0.3333</td><td>0.0</td><td>0.6667</td><td>0.000669</td><td>0.0006157</td><td>3.31e-05</td><td>5</td><td>7</td><td>21</td><td>34</td><td>12532</td><td>6114</td><td>13463</td><td>17458</td><td>6105</td><td>22642</td><td>22642</td><td>14881</td><td>13463</td><td>9747</td><td>17458</td><td>12990</td></tr>
    <tr><td>7 For All Mankind Men's Standard Classic Straight Leg Jean</td><td>7 For All Mankind</td><td>Jeans</td><td>157.45</td><td>80.97</td><td>1435.0</td><td>696.01</td><td>42</td><td>9</td><td>5</td><td>5</td><td>23</td><td>1673.0</td><td>844.04</td><td>0.485</td><td>0.3571</td><td>0.2432</td><td>0.119</td><td>0.7188</td><td>0.0005316</td><td>0.0004974</td><td>0.0002317</td><td>1798</td><td>1488</td><td>46</td><td>60</td><td>2</td><td>5</td><td>5</td><td>24</td><td>2</td><td>32</td><td>41</td><td>14028</td><td>8749</td><td>17091</td><td>15552</td><td>12034</td></tr>
    <tr><td>AIR JORDAN DOMINATE SHORTS MENS 465071-100</td><td>Jordan</td><td>Shorts</td><td>903.0</td><td>454.21</td><td>2709.0</td><td>1346.37</td><td>5</td><td>3</td><td>0</td><td>0</td><td>2</td><td>0.0</td><td>0.0</td><td>0.497</td><td>0.0</td><td>0.6</td><td>0.0</td><td>0.4</td><td>0.0010035</td><td>0.0009622</td><td>2.76e-05</td><td>5</td><td>8</td><td>7</td><td>9</td><td>16887</td><td>2358</td><td>13463</td><td>17458</td><td>17069</td><td>22642</td><td>22642</td><td>12874</td><td>13463</td><td>2189</td><td>17458</td><td>23875</td></tr>
    <tr><td>Canada Goose Women's Expedition Parka</td><td>Canada Goose</td><td>Outerwear & Coats</td><td>795.0</td><td>395.91</td><td>2385.0</td><td>1197.27</td><td>4</td><td>3</td><td>0</td><td>1</td><td>0</td><td>795.0</td><td>399.09</td><td>0.502</td><td>0.0</td><td>1.0</td><td>0.25</td><td>0.0</td><td>0.0008835</td><td>0.0008557</td><td>2.21e-05</td><td>33</td><td>19</td><td>10</td><td>13</td><td>21053</td><td>2358</td><td>13463</td><td>7029</td><td>27145</td><td>230</td><td>277</td><td>12357</td><td>13463</td><td>1</td><td>5542</td><td>27145</td></tr>
    <tr><td>Arc'teryx Moray Jacket - Women's</td><td>Arc'teryx</td><td>Outerwear & Coats</td><td>699.0</td><td>343.91</td><td>2097.0</td><td>1065.28</td><td>9</td><td>3</td><td>0</td><td>3</td><td>3</td><td>2097.0</td><td>1065.28</td><td>0.508</td><td>0.0</td><td>0.5</td><td>0.3333</td><td>0.5</td><td>0.0007768</td><td>0.0007613</td><td>4.96e-05</td><td>41</td><td>36</td><td>15</td><td>20</td><td>3355</td><td>2358</td><td>13463</td><td>526</td><td>10869</td><td>11</td><td>22</td><td>11720</td><td>13463</td><td>3269</td><td>2619</td><td>19501</td></tr>
    <tr><td>Barbour Sapper Jacket</td><td>Barbour</td><td>Outerwear & Coats</td><td>429.0</td><td>210.21</td><td>2145.0</td><td>1093.95</td><td>10</td><td>5</td><td>1</td><td>1</td><td>3</td><td>858.0</td><td>437.58</td><td>0.51</td><td>0.1667</td><td>0.5556</td><td>0.1</td><td>0.375</td><td>0.0007946</td><td>0.0007818</td><td>5.52e-05</td><td>94</td><td>81</td><td>14</td><td>18</td><td>1962</td><td>251</td><td>3978</td><td>7029</td><td>10869</td><td>185</td><td>233</td><td>11510</td><td>13196</td><td>3151</td><td>16366</td><td>24717</td></tr>
    <tr><td>Women's Knee Length Overcoat in Pure Cashmere</td><td>Cashmere Boutique</td><td>Outerwear & Coats</td><td>399.0</td><td>193.12</td><td>1596.0</td><td>814.76</td><td>9</td><td>4</td><td>0</td><td>0</td><td>5</td><td>0.0</td><td>0.0</td><td>0.5105</td><td>0.0</td><td>0.4444</td><td>0.0</td><td>0.5556</td><td>0.0005912</td><td>0.0005823</td><td>4.96e-05</td><td>115</td><td>100</td><td>35</td><td>40</td><td>3355</td><td>776</td><td>13463</td><td>17458</td><td>3026</td><td>22642</td><td>22642</td><td>11502</td><td>13463</td><td>6492</td><td>17458</td><td>19270</td></tr>
    <tr><td>Barbour Classic Beaufort Jacket / Beaufort Jacket</td><td>Barbour</td><td>Outerwear & Coats</td><td>399.0</td><td>193.91</td><td>1596.0</td><td>820.34</td><td>10</td><td>4</td><td>0</td><td>1</td><td>5</td><td>399.0</td><td>205.09</td><td>0.514</td><td>0.0</td><td>0.4444</td><td>0.1</td><td>0.5556</td><td>0.0005912</td><td>0.0005863</td><td>5.52e-05</td><td>115</td><td>98</td><td>35</td><td>38</td><td>1962</td><td>776</td><td>13463</td><td>7029</td><td>3026</td><td>985</td><td>1084</td><td>11041</td><td>13463</td><td>6492</td><td>16366</td><td>19270</td></tr>
  </tbody>
</table>

</div>

<h3>Bottom products by Unit Orders</h3>

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
  unit_orders_placed_rank DESC
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
    <tr><td>Ulla Popken Plus Size Sequined Swing Jacket</td><td>Ulla Popken</td><td>Blazers & Jackets</td><td>169.0</td><td>62.7</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>169.0</td><td>106.3</td><td></td><td></td><td></td><td>1.0</td><td></td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>1446</td><td>2577</td><td>22532</td><td>22532</td><td>27983</td><td>22532</td><td>13463</td><td>7029</td><td>27145</td><td>4331</td><td>3178</td><td>22532</td><td>25326</td><td>28303</td><td>1</td><td>28172</td></tr>
    <tr><td>Carhartt Women's Wylie Flannel Hoodie</td><td>Carhartt</td><td>Fashion Hoodies & Sweatshirts</td><td>59.95</td><td>27.76</td><td>59.95</td><td>32.19</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0.0</td><td>0.0</td><td>0.5369</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>2.22e-05</td><td>2.3e-05</td><td>5.5e-06</td><td>8808</td><td>9607</td><td>12711</td><td>12060</td><td>27983</td><td>13264</td><td>13463</td><td>17458</td><td>27145</td><td>22642</td><td>22642</td><td>8960</td><td>13463</td><td>1</td><td>17458</td><td>27145</td></tr>
    <tr><td>Lucky Brand Mens 361 Vintage Straight Leg Jean</td><td>Lucky Brand</td><td>Jeans</td><td>61.99</td><td>35.27</td><td>61.99</td><td>26.72</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0.0</td><td>0.0</td><td>0.431</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>2.3e-05</td><td>1.91e-05</td><td>5.5e-06</td><td>8368</td><td>6768</td><td>12308</td><td>13690</td><td>27983</td><td>13264</td><td>13463</td><td>17458</td><td>27145</td><td>22642</td><td>22642</td><td>18935</td><td>13463</td><td>1</td><td>17458</td><td>27145</td></tr>
    <tr><td>Solid Series Silk Scarves</td><td>Wolfmark</td><td>Accessories</td><td>18.0</td><td>7.56</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>23512</td><td>24629</td><td>22532</td><td>22532</td><td>27983</td><td>22532</td><td>13463</td><td>17458</td><td>23197</td><td>22642</td><td>22642</td><td>22532</td><td>25326</td><td>22532</td><td>17458</td><td>1</td></tr>
    <tr><td>Bottoms Out - Mens Microfleece Lounge Pant Burgundy 23439</td><td>Bottoms Out</td><td>Sleep & Lounge</td><td>13.75</td><td>5.71</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>25545</td><td>26326</td><td>22532</td><td>22532</td><td>27983</td><td>22532</td><td>13463</td><td>17458</td><td>23197</td><td>22642</td><td>22642</td><td>22532</td><td>25326</td><td>22532</td><td>17458</td><td>1</td></tr>
    <tr><td>Acid Wash Jean Dark Leggings</td><td>Yelete</td><td>Leggings</td><td>15.99</td><td>9.35</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>15.99</td><td>6.64</td><td></td><td>1.0</td><td>0.0</td><td>0.0</td><td></td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>24393</td><td>23040</td><td>22532</td><td>22532</td><td>27983</td><td>22532</td><td>3978</td><td>17458</td><td>27145</td><td>21199</td><td>21673</td><td>22532</td><td>1</td><td>22532</td><td>17458</td><td>28172</td></tr>
    <tr><td>Corset-story WT-066 waist training corset</td><td>Corset-story</td><td>Intimates</td><td>100.0</td><td>54.1</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>3867</td><td>3383</td><td>22532</td><td>22532</td><td>27983</td><td>22532</td><td>13463</td><td>17458</td><td>23197</td><td>22642</td><td>22642</td><td>22532</td><td>25326</td><td>22532</td><td>17458</td><td>1</td></tr>
    <tr><td>prAna Women's Diva Vest</td><td>prAna</td><td>Active</td><td>119.0</td><td>51.53</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>3169</td><td>3649</td><td>22532</td><td>22532</td><td>27983</td><td>22532</td><td>13463</td><td>17458</td><td>23197</td><td>22642</td><td>22642</td><td>22532</td><td>25326</td><td>22532</td><td>17458</td><td>1</td></tr>
    <tr><td>adidas Women's Pursuit Pant</td><td>adidas</td><td>Active</td><td>50.0</td><td>18.65</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>50.0</td><td>31.35</td><td></td><td></td><td></td><td>1.0</td><td></td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>10696</td><td>14839</td><td>22532</td><td>22532</td><td>27983</td><td>22532</td><td>13463</td><td>7029</td><td>27145</td><td>14018</td><td>12300</td><td>22532</td><td>25326</td><td>28303</td><td>1</td><td>28172</td></tr>
    <tr><td>Volcom Juniors Frochickie 2 1/2 Inch Plain Front Short</td><td>Volcom</td><td>Shorts</td><td>39.5</td><td>21.17</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>14466</td><td>13153</td><td>22532</td><td>22532</td><td>27983</td><td>22532</td><td>13463</td><td>17458</td><td>23197</td><td>22642</td><td>22642</td><td>22532</td><td>25326</td><td>22532</td><td>17458</td><td>1</td></tr>
    <tr><td>Nautica Mens 3 Pack Performance Casual Crew Track Socks</td><td>Nautica</td><td>Socks</td><td>14.4</td><td>8.12</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>25223</td><td>24070</td><td>22532</td><td>22532</td><td>27983</td><td>22532</td><td>13463</td><td>17458</td><td>23197</td><td>22642</td><td>22642</td><td>22532</td><td>25326</td><td>22532</td><td>17458</td><td>1</td></tr>
    <tr><td>TAUPE PALAZZO PANT SPLIT SKIRT GAUCHO - FITS (ONE SIZE) - L XL 1X 2X - U652S - LOTUSTRADERS</td><td>LOTUSTRADERS</td><td>Pants & Capris</td><td>42.99</td><td>21.92</td><td>42.99</td><td>21.07</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0.0</td><td>0.0</td><td>0.4901</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>1.59e-05</td><td>1.51e-05</td><td>5.5e-06</td><td>13180</td><td>12697</td><td>15536</td><td>15631</td><td>27983</td><td>13264</td><td>13463</td><td>17458</td><td>27145</td><td>22642</td><td>22642</td><td>13507</td><td>13463</td><td>1</td><td>17458</td><td>27145</td></tr>
    <tr><td>Arena Men's Satamis Race Xtra Life Lycra Solid Brief Swimsuit</td><td>Arena</td><td>Swim</td><td>24.95</td><td>15.17</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td></td><td></td><td>0.0</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>21005</td><td>17618</td><td>22532</td><td>22532</td><td>27983</td><td>22532</td><td>13463</td><td>17458</td><td>23197</td><td>22642</td><td>22642</td><td>22532</td><td>25326</td><td>22532</td><td>17458</td><td>1</td></tr>
    <tr><td>Le Suit Safari Nights Jacket Dress</td><td>Le Suit</td><td>Suits</td><td>141.62</td><td>83.84</td><td>0.0</td><td>0.0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>141.62</td><td>57.78</td><td></td><td></td><td></td><td>1.0</td><td></td><td>0.0</td><td>0.0</td><td>5.5e-06</td><td>2207</td><td>1356</td><td>22532</td><td>22532</td><td>27983</td><td>22532</td><td>13463</td><td>7029</td><td>27145</td><td>5534</td><td>7190</td><td>22532</td><td>25326</td><td>28303</td><td>1</td><td>28172</td></tr>
    <tr><td>Trina Turk Women's Pasha Pant</td><td>Trina Turk</td><td>Pants & Capris</td><td>288.0</td><td>162.72</td><td>288.0</td><td>125.28</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0.0</td><td>0.0</td><td>0.435</td><td>0.0</td><td>1.0</td><td>0.0</td><td>0.0</td><td>0.0001067</td><td>8.95e-05</td><td>5.5e-06</td><td>338</td><td>178</td><td>1925</td><td>2574</td><td>27983</td><td>13264</td><td>13463</td><td>17458</td><td>27145</td><td>22642</td><td>22642</td><td>18613</td><td>13463</td><td>1</td><td>17458</td><td>27145</td></tr>
  </tbody>
</table>

</div>

<h3>Bottom products by Return Rate</h3>

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
WHERE revenue_rank &lt;= 20
ORDER BY
  return_rate_rank DESC
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
    <tr><td>AIR JORDAN DOMINATE SHORTS MENS 465071-100</td><td>Jordan</td><td>Shorts</td><td>903.0</td><td>454.21</td><td>2709.0</td><td>1346.37</td><td>5</td><td>3</td><td>0</td><td>0</td><td>2</td><td>0.0</td><td>0.0</td><td>0.497</td><td>0.0</td><td>0.6</td><td>0.0</td><td>0.4</td><td>0.0010035</td><td>0.0009622</td><td>2.76e-05</td><td>5</td><td>8</td><td>7</td><td>9</td><td>16887</td><td>2358</td><td>13463</td><td>17458</td><td>17069</td><td>22642</td><td>22642</td><td>12874</td><td>13463</td><td>2189</td><td>17458</td><td>23875</td></tr>
    <tr><td>Canada Goose Women's Expedition Parka</td><td>Canada Goose</td><td>Outerwear & Coats</td><td>795.0</td><td>395.91</td><td>2385.0</td><td>1197.27</td><td>4</td><td>3</td><td>0</td><td>1</td><td>0</td><td>795.0</td><td>399.09</td><td>0.502</td><td>0.0</td><td>1.0</td><td>0.25</td><td>0.0</td><td>0.0008835</td><td>0.0008557</td><td>2.21e-05</td><td>33</td><td>19</td><td>10</td><td>13</td><td>21053</td><td>2358</td><td>13463</td><td>7029</td><td>27145</td><td>230</td><td>277</td><td>12357</td><td>13463</td><td>1</td><td>5542</td><td>27145</td></tr>
    <tr><td>True Religion Women's Julie Super T Jean</td><td>True Religion</td><td>Jeans</td><td>326.0</td><td>172.13</td><td>1956.0</td><td>923.23</td><td>8</td><td>6</td><td>0</td><td>1</td><td>1</td><td>326.0</td><td>153.87</td><td>0.472</td><td>0.0</td><td>0.8571</td><td>0.125</td><td>0.1429</td><td>0.0007246</td><td>0.0006598</td><td>4.41e-05</td><td>233</td><td>145</td><td>19</td><td>31</td><td>5507</td><td>84</td><td>13463</td><td>7029</td><td>23197</td><td>1487</td><td>1788</td><td>15335</td><td>13463</td><td>546</td><td>14338</td><td>27121</td></tr>
    <tr><td>Mountain Hardwear Women's Chillwave Down Jacket</td><td>Mountain Hardwear</td><td>Outerwear & Coats</td><td>375.0</td><td>179.25</td><td>1875.0</td><td>978.75</td><td>6</td><td>5</td><td>0</td><td>1</td><td>0</td><td>375.0</td><td>195.75</td><td>0.522</td><td>0.0</td><td>1.0</td><td>0.1667</td><td>0.0</td><td>0.0006946</td><td>0.0006995</td><td>3.31e-05</td><td>155</td><td>128</td><td>20</td><td>29</td><td>12532</td><td>251</td><td>13463</td><td>7029</td><td>27145</td><td>1150</td><td>1161</td><td>10227</td><td>13463</td><td>1</td><td>10731</td><td>27145</td></tr>
    <tr><td>Canada Goose Women's Solaris</td><td>Canada Goose</td><td>Outerwear & Coats</td><td>695.0</td><td>296.76</td><td>2085.0</td><td>1194.71</td><td>6</td><td>3</td><td>0</td><td>2</td><td>1</td><td>1390.0</td><td>796.47</td><td>0.573</td><td>0.0</td><td>0.75</td><td>0.3333</td><td>0.25</td><td>0.0007724</td><td>0.0008538</td><td>3.31e-05</td><td>46</td><td>48</td><td>17</td><td>14</td><td>12532</td><td>2358</td><td>13463</td><td>2100</td><td>23197</td><td>67</td><td>52</td><td>5041</td><td>13463</td><td>746</td><td>2619</td><td>26348</td></tr>
    <tr><td>ASCIS Cushion Low Socks (Pack of 3)</td><td>ASICS</td><td>Active</td><td>903.0</td><td>373.84</td><td>3612.0</td><td>2116.63</td><td>11</td><td>4</td><td>0</td><td>1</td><td>6</td><td>903.0</td><td>529.16</td><td>0.586</td><td>0.0</td><td>0.4</td><td>0.0909</td><td>0.6</td><td>0.001338</td><td>0.0015127</td><td>6.07e-05</td><td>5</td><td>28</td><td>1</td><td>1</td><td>1161</td><td>776</td><td>13463</td><td>7029</td><td>1398</td><td>155</td><td>142</td><td>3719</td><td>13463</td><td>7482</td><td>16872</td><td>16953</td></tr>
    <tr><td>Arc'teryx Moray Jacket - Women's</td><td>Arc'teryx</td><td>Outerwear & Coats</td><td>699.0</td><td>343.91</td><td>2097.0</td><td>1065.28</td><td>9</td><td>3</td><td>0</td><td>3</td><td>3</td><td>2097.0</td><td>1065.28</td><td>0.508</td><td>0.0</td><td>0.5</td><td>0.3333</td><td>0.5</td><td>0.0007768</td><td>0.0007613</td><td>4.96e-05</td><td>41</td><td>36</td><td>15</td><td>20</td><td>3355</td><td>2358</td><td>13463</td><td>526</td><td>10869</td><td>11</td><td>22</td><td>11720</td><td>13463</td><td>3269</td><td>2619</td><td>19501</td></tr>
    <tr><td>Men's Classic Sheepskin B-3 Bomber Jacket</td><td>Overland Sheepskin Co</td><td>Outerwear & Coats</td><td>595.0</td><td>270.73</td><td>2380.0</td><td>1297.1</td><td>13</td><td>4</td><td>0</td><td>2</td><td>7</td><td>1190.0</td><td>648.55</td><td>0.545</td><td>0.0</td><td>0.3636</td><td>0.1538</td><td>0.6364</td><td>0.0008816</td><td>0.000927</td><td>7.17e-05</td><td>60</td><td>55</td><td>12</td><td>11</td><td>423</td><td>776</td><td>13463</td><td>2100</td><td>623</td><td>95</td><td>94</td><td>8121</td><td>13463</td><td>9638</td><td>12634</td><td>16487</td></tr>
    <tr><td>Michael Kors Men's Marlow Wool-Blend Single-Breasted Fitted Top Coat</td><td>Michael Kors</td><td>Outerwear & Coats</td><td>255.0</td><td>102.26</td><td>2295.0</td><td>1374.7</td><td>15</td><td>9</td><td>1</td><td>2</td><td>3</td><td>765.0</td><td>458.23</td><td>0.599</td><td>0.1</td><td>0.6923</td><td>0.1333</td><td>0.25</td><td>0.0008502</td><td>0.0009825</td><td>8.27e-05</td><td>469</td><td>728</td><td>13</td><td>8</td><td>187</td><td>5</td><td>3978</td><td>2100</td><td>10869</td><td>252</td><td>208</td><td>2612</td><td>13461</td><td>1184</td><td>14317</td><td>26348</td></tr>
    <tr><td>Joseph Abboud Men's Two-button Side Vent Sport Coat</td><td>Joseph Abboud</td><td>Suits & Sport Coats</td><td>264.0</td><td>101.9</td><td>2904.0</td><td>1759.82</td><td>30</td><td>11</td><td>2</td><td>2</td><td>15</td><td>1056.0</td><td>656.57</td><td>0.606</td><td>0.1538</td><td>0.3929</td><td>0.0667</td><td>0.5769</td><td>0.0010758</td><td>0.0012577</td><td>0.0001655</td><td>430</td><td>734</td><td>6</td><td>5</td><td>7</td><td>3</td><td>844</td><td>2100</td><td>11</td><td>112</td><td>91</td><td>2144</td><td>13388</td><td>9081</td><td>17408</td><td>18610</td></tr>
    <tr><td>Barbour Sapper Jacket</td><td>Barbour</td><td>Outerwear & Coats</td><td>429.0</td><td>210.21</td><td>2145.0</td><td>1093.95</td><td>10</td><td>5</td><td>1</td><td>1</td><td>3</td><td>858.0</td><td>437.58</td><td>0.51</td><td>0.1667</td><td>0.5556</td><td>0.1</td><td>0.375</td><td>0.0007946</td><td>0.0007818</td><td>5.52e-05</td><td>94</td><td>81</td><td>14</td><td>18</td><td>1962</td><td>251</td><td>3978</td><td>7029</td><td>10869</td><td>185</td><td>233</td><td>11510</td><td>13196</td><td>3151</td><td>16366</td><td>24717</td></tr>
    <tr><td>Diesel Men's Lagnum Leather Jacket</td><td>Diesel</td><td>Outerwear & Coats</td><td>598.0</td><td>267.9</td><td>2392.0</td><td>1320.38</td><td>7</td><td>4</td><td>1</td><td>1</td><td>1</td><td>1196.0</td><td>660.19</td><td>0.552</td><td>0.2</td><td>0.6667</td><td>0.1429</td><td>0.2</td><td>0.0008861</td><td>0.0009437</td><td>3.86e-05</td><td>57</td><td>56</td><td>9</td><td>10</td><td>8625</td><td>776</td><td>3978</td><td>7029</td><td>23197</td><td>92</td><td>89</td><td>7373</td><td>12637</td><td>1185</td><td>12706</td><td>26859</td></tr>
    <tr><td>The North Face Women's S-XL Oso Jacket</td><td>The North Face</td><td>Outerwear & Coats</td><td>903.0</td><td>378.36</td><td>3612.0</td><td>2098.57</td><td>10</td><td>4</td><td>1</td><td>1</td><td>4</td><td>1806.0</td><td>1049.29</td><td>0.581</td><td>0.2</td><td>0.4444</td><td>0.1</td><td>0.5</td><td>0.001338</td><td>0.0014998</td><td>5.52e-05</td><td>5</td><td>25</td><td>1</td><td>2</td><td>1962</td><td>776</td><td>3978</td><td>7029</td><td>6105</td><td>22</td><td>24</td><td>4209</td><td>12637</td><td>6492</td><td>16366</td><td>19501</td></tr>
    <tr><td>Bergama Natural Raccoon Hooded Stroller - - Multicolor</td><td>Bergama</td><td>Outerwear & Coats</td><td>749.99</td><td>306.75</td><td>2999.96</td><td>1772.98</td><td>10</td><td>4</td><td>1</td><td>0</td><td>5</td><td>749.99</td><td>443.24</td><td>0.591</td><td>0.2</td><td>0.4</td><td>0.0</td><td>0.5556</td><td>0.0011113</td><td>0.0012671</td><td>5.52e-05</td><td>40</td><td>43</td><td>4</td><td>3</td><td>1962</td><td>776</td><td>3978</td><td>17458</td><td>3026</td><td>267</td><td>224</td><td>3279</td><td>12637</td><td>7482</td><td>17458</td><td>19270</td></tr>
    <tr><td>Diesel Men's Jimeneo Jacket</td><td>Diesel</td><td>Suits & Sport Coats</td><td>698.0</td><td>304.33</td><td>2094.0</td><td>1181.02</td><td>13</td><td>3</td><td>1</td><td>1</td><td>8</td><td>1396.0</td><td>787.34</td><td>0.564</td><td>0.25</td><td>0.25</td><td>0.0769</td><td>0.7273</td><td>0.0007757</td><td>0.0008441</td><td>7.17e-05</td><td>43</td><td>46</td><td>16</td><td>16</td><td>423</td><td>2358</td><td>3978</td><td>7029</td><td>295</td><td>65</td><td>54</td><td>6066</td><td>11344</td><td>14408</td><td>17286</td><td>11980</td></tr>
  </tbody>
</table>

</div>

<h3>Bottom products by Units Returned</h3>

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
WHERE unit_orders_placed_rank &lt;= 50
ORDER BY
  units_returned_rank DESC
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
    <tr><td>TapouT Men's Lock Up Hoodie</td><td>TapouT</td><td>Fashion Hoodies & Sweatshirts</td><td>36.61</td><td>20.6</td><td>229.12</td><td>103.62</td><td>23</td><td>7</td><td>0</td><td>1</td><td>15</td><td>39.6</td><td>16.16</td><td>0.4523</td><td>0.0</td><td>0.3182</td><td>0.0435</td><td>0.6818</td><td>8.49e-05</td><td>7.41e-05</td><td>0.0001269</td><td>15388</td><td>13556</td><td>2822</td><td>3414</td><td>41</td><td>33</td><td>13463</td><td>7029</td><td>11</td><td>16416</td><td>17785</td><td>17057</td><td>13463</td><td>13008</td><td>17454</td><td>12986</td></tr>
    <tr><td>HUGO BOSS Men's Long Pant</td><td>HUGO BOSS</td><td>Sleep & Lounge</td><td>74.72</td><td>28.3</td><td>1033.11</td><td>648.16</td><td>33</td><td>14</td><td>0</td><td>3</td><td>16</td><td>233.01</td><td>138.21</td><td>0.6274</td><td>0.0</td><td>0.4667</td><td>0.0909</td><td>0.5333</td><td>0.0003827</td><td>0.0004632</td><td>0.000182</td><td>6501</td><td>9383</td><td>113</td><td>75</td><td>6</td><td>1</td><td>13463</td><td>526</td><td>7</td><td>2702</td><td>2165</td><td>933</td><td>13463</td><td>6418</td><td>16872</td><td>19494</td></tr>
    <tr><td>Joe's Jeans Men's Rebel Relaxed Fit Jean</td><td>Joe's Jeans</td><td>Jeans</td><td>139.29</td><td>76.13</td><td>1296.69</td><td>583.03</td><td>26</td><td>9</td><td>0</td><td>3</td><td>14</td><td>339.69</td><td>166.11</td><td>0.4496</td><td>0.0</td><td>0.3913</td><td>0.1154</td><td>0.6087</td><td>0.0004803</td><td>0.0004167</td><td>0.0001434</td><td>2334</td><td>1721</td><td>68</td><td>102</td><td>17</td><td>5</td><td>13463</td><td>526</td><td>22</td><td>1403</td><td>1558</td><td>17357</td><td>13463</td><td>9082</td><td>15567</td><td>16952</td></tr>
    <tr><td>Diesel Men's Blade Underpant</td><td>Diesel</td><td>Underwear</td><td>22.14</td><td>9.75</td><td>122.0</td><td>66.53</td><td>22</td><td>6</td><td>0</td><td>2</td><td>14</td><td>43.0</td><td>23.83</td><td>0.5453</td><td>0.0</td><td>0.3</td><td>0.0909</td><td>0.7</td><td>4.52e-05</td><td>4.75e-05</td><td>0.0001214</td><td>21886</td><td>22702</td><td>6504</td><td>6114</td><td>43</td><td>84</td><td>13463</td><td>2100</td><td>22</td><td>15676</td><td>14732</td><td>8115</td><td>13463</td><td>13033</td><td>16872</td><td>12849</td></tr>
    <tr><td>Ray-Ban Women's 4101 Jackie Ohh Sunglasses</td><td>Ray-Ban</td><td>Accessories</td><td>97.5</td><td>41.94</td><td>486.16</td><td>280.13</td><td>22</td><td>5</td><td>1</td><td>5</td><td>11</td><td>586.32</td><td>330.97</td><td>0.5762</td><td>0.1667</td><td>0.2941</td><td>0.2273</td><td>0.6875</td><td>0.0001801</td><td>0.0002002</td><td>0.0001214</td><td>4451</td><td>5084</td><td>706</td><td>587</td><td>43</td><td>251</td><td>3978</td><td>24</td><td>43</td><td>472</td><td>408</td><td>4708</td><td>13196</td><td>13232</td><td>7836</td><td>12983</td></tr>
    <tr><td>Wrangler Men's 20X No. 33 Relaxed Straight Leg Jean</td><td>Wrangler</td><td>Jeans</td><td>55.0</td><td>29.66</td><td>220.0</td><td>100.87</td><td>24</td><td>4</td><td>1</td><td>2</td><td>17</td><td>165.0</td><td>74.2</td><td>0.4585</td><td>0.2</td><td>0.1818</td><td>0.0833</td><td>0.8095</td><td>8.15e-05</td><td>7.21e-05</td><td>0.0001324</td><td>9673</td><td>8784</td><td>2941</td><td>3526</td><td>30</td><td>776</td><td>3978</td><td>2100</td><td>6</td><td>4449</td><td>5375</td><td>16533</td><td>12637</td><td>19358</td><td>17144</td><td>7597</td></tr>
    <tr><td>Wrangler Men's Sarasota Agility Short</td><td>Wrangler</td><td>Shorts</td><td>33.03</td><td>16.36</td><td>198.95</td><td>101.37</td><td>25</td><td>6</td><td>1</td><td>3</td><td>15</td><td>138.97</td><td>68.68</td><td>0.5095</td><td>0.1429</td><td>0.2727</td><td>0.12</td><td>0.7143</td><td>7.37e-05</td><td>7.24e-05</td><td>0.0001379</td><td>16765</td><td>16618</td><td>3447</td><td>3505</td><td>21</td><td>84</td><td>3978</td><td>526</td><td>11</td><td>5758</td><td>5901</td><td>11606</td><td>13389</td><td>14284</td><td>15549</td><td>12035</td></tr>
    <tr><td>True Religion Men's Ricky Straight Leg Jean</td><td>True Religion</td><td>Jeans</td><td>227.86</td><td>123.14</td><td>1452.0</td><td>661.01</td><td>28</td><td>7</td><td>1</td><td>5</td><td>15</td><td>1430.0</td><td>645.85</td><td>0.4552</td><td>0.125</td><td>0.3043</td><td>0.1786</td><td>0.6818</td><td>0.0005379</td><td>0.0004724</td><td>0.0001545</td><td>646</td><td>406</td><td>45</td><td>69</td><td>9</td><td>33</td><td>3978</td><td>24</td><td>11</td><td>57</td><td>95</td><td>16801</td><td>13444</td><td>13032</td><td>10715</td><td>12986</td></tr>
    <tr><td>Fred Perry Men's Crew Neck Sweater</td><td>Fred Perry</td><td>Sweaters</td><td>104.69</td><td>54.65</td><td>815.72</td><td>392.52</td><td>24</td><td>8</td><td>1</td><td>1</td><td>14</td><td>214.74</td><td>106.77</td><td>0.4812</td><td>0.1111</td><td>0.3478</td><td>0.0417</td><td>0.6364</td><td>0.0003022</td><td>0.0002805</td><td>0.0001324</td><td>3741</td><td>3335</td><td>188</td><td>264</td><td>30</td><td>16</td><td>3978</td><td>7029</td><td>22</td><td>3010</td><td>3162</td><td>14461</td><td>13456</td><td>9743</td><td>17456</td><td>16487</td></tr>
    <tr><td>Volcom Men's Vorta Slim Straight Leg Fit Jean</td><td>Volcom</td><td>Jeans</td><td>73.57</td><td>41.13</td><td>574.85</td><td>249.86</td><td>27</td><td>8</td><td>1</td><td>4</td><td>14</td><td>387.8</td><td>166.89</td><td>0.4347</td><td>0.1111</td><td>0.3478</td><td>0.1481</td><td>0.6364</td><td>0.0002129</td><td>0.0001786</td><td>0.0001489</td><td>6603</td><td>5251</td><td>467</td><td>746</td><td>12</td><td>16</td><td>3978</td><td>126</td><td>22</td><td>1091</td><td>1537</td><td>18678</td><td>13456</td><td>9743</td><td>12705</td><td>16487</td></tr>
    <tr><td>Puma Men's Socks</td><td>PUMA</td><td>Socks</td><td>13.0</td><td>7.78</td><td>90.0</td><td>35.98</td><td>24</td><td>7</td><td>1</td><td>5</td><td>11</td><td>78.0</td><td>31.36</td><td>0.3998</td><td>0.125</td><td>0.3684</td><td>0.2083</td><td>0.6111</td><td>3.33e-05</td><td>2.57e-05</td><td>0.0001324</td><td>25705</td><td>24414</td><td>8929</td><td>11107</td><td>30</td><td>33</td><td>3978</td><td>24</td><td>43</td><td>10368</td><td>12295</td><td>20955</td><td>13444</td><td>9637</td><td>8433</td><td>16951</td></tr>
    <tr><td>Wrangler Men's Genuine Tampa Cargo Short</td><td>Wrangler</td><td>Shorts</td><td>31.37</td><td>15.61</td><td>229.94</td><td>116.44</td><td>29</td><td>7</td><td>1</td><td>5</td><td>16</td><td>179.94</td><td>90.54</td><td>0.5064</td><td>0.125</td><td>0.2917</td><td>0.1724</td><td>0.6957</td><td>8.52e-05</td><td>8.32e-05</td><td>0.00016</td><td>17403</td><td>17266</td><td>2818</td><td>2869</td><td>8</td><td>33</td><td>3978</td><td>24</td><td>7</td><td>3935</td><td>4081</td><td>11924</td><td>13444</td><td>13236</td><td>10730</td><td>12964</td></tr>
    <tr><td>Bottoms Out Men's Plaid Sleep Pant</td><td>Bottoms Out</td><td>Sleep & Lounge</td><td>13.49</td><td>5.05</td><td>94.43</td><td>59.4</td><td>25</td><td>7</td><td>2</td><td>4</td><td>12</td><td>80.94</td><td>50.64</td><td>0.629</td><td>0.2222</td><td>0.3333</td><td>0.16</td><td>0.6316</td><td>3.5e-05</td><td>4.25e-05</td><td>0.0001379</td><td>25625</td><td>26913</td><td>8758</td><td>6904</td><td>21</td><td>33</td><td>844</td><td>126</td><td>37</td><td>9890</td><td>8299</td><td>839</td><td>12628</td><td>9747</td><td>12630</td><td>16546</td></tr>
    <tr><td>JiMarti JM01 Sunglasses for Golf Fishing Cycling-Unbreakable-... Frame</td><td>JiMarti</td><td>Accessories</td><td>29.95</td><td>11.92</td><td>269.55</td><td>161.1</td><td>22</td><td>9</td><td>2</td><td>2</td><td>9</td><td>119.8</td><td>72.12</td><td>0.5977</td><td>0.1818</td><td>0.45</td><td>0.0909</td><td>0.5</td><td>9.99e-05</td><td>0.0001151</td><td>0.0001214</td><td>18166</td><td>20613</td><td>2175</td><td>1707</td><td>43</td><td>5</td><td>844</td><td>2100</td><td>140</td><td>6868</td><td>5540</td><td>2758</td><td>13193</td><td>6490</td><td>16872</td><td>19501</td></tr>
    <tr><td>Wrangler Men's Premium Performance Cowboy Cut Jean</td><td>Wrangler</td><td>Jeans</td><td>47.45</td><td>25.88</td><td>570.83</td><td>264.22</td><td>58</td><td>12</td><td>2</td><td>7</td><td>37</td><td>417.81</td><td>189.65</td><td>0.4629</td><td>0.1429</td><td>0.2353</td><td>0.1207</td><td>0.7551</td><td>0.0002115</td><td>0.0001888</td><td>0.00032</td><td>12004</td><td>10508</td><td>470</td><td>662</td><td>1</td><td>2</td><td>844</td><td>2</td><td>1</td><td>905</td><td>1224</td><td>16149</td><td>13389</td><td>17092</td><td>15548</td><td>9486</td></tr>
  </tbody>
</table>

</div>

<h3>Bottom products by Lost Revenue</h3>

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
  lost_revenue_rank DESC
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
    <tr><td>Steinbock Tyrolean Sport Coat</td><td>Orvis</td><td>Suits & Sport Coats</td><td>350.0</td><td>154.0</td><td>1400.0</td><td>784.0</td><td>11</td><td>4</td><td>0</td><td>0</td><td>7</td><td>0.0</td><td>0.0</td><td>0.56</td><td>0.0</td><td>0.3636</td><td>0.0</td><td>0.6364</td><td>0.0005186</td><td>0.0005603</td><td>6.07e-05</td><td>180</td><td>217</td><td>49</td><td>48</td><td>1161</td><td>776</td><td>13463</td><td>17458</td><td>623</td><td>22642</td><td>22642</td><td>6489</td><td>13463</td><td>9638</td><td>17458</td><td>16487</td></tr>
    <tr><td>The North Face Apex Bionic Soft Shell Jacket - Men's</td><td>The North Face</td><td>Fashion Hoodies & Sweatshirts</td><td>903.0</td><td>524.64</td><td>1806.0</td><td>756.71</td><td>6</td><td>2</td><td>0</td><td>0</td><td>4</td><td>0.0</td><td>0.0</td><td>0.419</td><td>0.0</td><td>0.3333</td><td>0.0</td><td>0.6667</td><td>0.000669</td><td>0.0005408</td><td>3.31e-05</td><td>5</td><td>3</td><td>21</td><td>55</td><td>12532</td><td>6114</td><td>13463</td><td>17458</td><td>6105</td><td>22642</td><td>22642</td><td>19960</td><td>13463</td><td>9747</td><td>17458</td><td>12990</td></tr>
    <tr><td>Women's Knee Length Overcoat in Pure Cashmere</td><td>Cashmere Boutique</td><td>Outerwear & Coats</td><td>399.0</td><td>193.12</td><td>1596.0</td><td>814.76</td><td>9</td><td>4</td><td>0</td><td>0</td><td>5</td><td>0.0</td><td>0.0</td><td>0.5105</td><td>0.0</td><td>0.4444</td><td>0.0</td><td>0.5556</td><td>0.0005912</td><td>0.0005823</td><td>4.96e-05</td><td>115</td><td>100</td><td>35</td><td>40</td><td>3355</td><td>776</td><td>13463</td><td>17458</td><td>3026</td><td>22642</td><td>22642</td><td>11502</td><td>13463</td><td>6492</td><td>17458</td><td>19270</td></tr>
    <tr><td>Mountain Hardwear Men's Chillwave Down Parka</td><td>Mountain Hardwear</td><td>Outerwear & Coats</td><td>375.0</td><td>176.63</td><td>1500.0</td><td>793.5</td><td>5</td><td>4</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td>0.529</td><td>0.0</td><td>0.8</td><td>0.0</td><td>0.2</td><td>0.0005557</td><td>0.0005671</td><td>2.76e-05</td><td>155</td><td>135</td><td>41</td><td>44</td><td>16887</td><td>776</td><td>13463</td><td>17458</td><td>23197</td><td>22642</td><td>22642</td><td>9645</td><td>13463</td><td>607</td><td>17458</td><td>26859</td></tr>
    <tr><td>AIR JORDAN DOMINATE SHORTS MENS 465071-100</td><td>Jordan</td><td>Shorts</td><td>903.0</td><td>454.21</td><td>2709.0</td><td>1346.37</td><td>5</td><td>3</td><td>0</td><td>0</td><td>2</td><td>0.0</td><td>0.0</td><td>0.497</td><td>0.0</td><td>0.6</td><td>0.0</td><td>0.4</td><td>0.0010035</td><td>0.0009622</td><td>2.76e-05</td><td>5</td><td>8</td><td>7</td><td>9</td><td>16887</td><td>2358</td><td>13463</td><td>17458</td><td>17069</td><td>22642</td><td>22642</td><td>12874</td><td>13463</td><td>2189</td><td>17458</td><td>23875</td></tr>
    <tr><td>Quiksilver Men's Rockefeller Walkshort</td><td>Quiksilver</td><td>Shorts</td><td>903.0</td><td>472.27</td><td>1806.0</td><td>861.46</td><td>6</td><td>2</td><td>0</td><td>0</td><td>4</td><td>0.0</td><td>0.0</td><td>0.477</td><td>0.0</td><td>0.3333</td><td>0.0</td><td>0.6667</td><td>0.000669</td><td>0.0006157</td><td>3.31e-05</td><td>5</td><td>7</td><td>21</td><td>34</td><td>12532</td><td>6114</td><td>13463</td><td>17458</td><td>6105</td><td>22642</td><td>22642</td><td>14881</td><td>13463</td><td>9747</td><td>17458</td><td>12990</td></tr>
    <tr><td>The North Face Nuptse 2 Jacket - Noah Green/TNF Black</td><td>The North Face</td><td>Outerwear & Coats</td><td>903.0</td><td>370.23</td><td>1806.0</td><td>1065.54</td><td>8</td><td>2</td><td>0</td><td>0</td><td>6</td><td>0.0</td><td>0.0</td><td>0.59</td><td>0.0</td><td>0.25</td><td>0.0</td><td>0.75</td><td>0.000669</td><td>0.0007615</td><td>4.41e-05</td><td>5</td><td>29</td><td>21</td><td>19</td><td>5507</td><td>6114</td><td>13463</td><td>17458</td><td>1398</td><td>22642</td><td>22642</td><td>3353</td><td>13463</td><td>14408</td><td>17458</td><td>9487</td></tr>
    <tr><td>The North Face Denali Down Womens Jacket 2013</td><td>The North Face</td><td>Active</td><td>903.0</td><td>395.51</td><td>1806.0</td><td>1014.97</td><td>8</td><td>2</td><td>0</td><td>0</td><td>6</td><td>0.0</td><td>0.0</td><td>0.562</td><td>0.0</td><td>0.25</td><td>0.0</td><td>0.75</td><td>0.000669</td><td>0.0007254</td><td>4.41e-05</td><td>5</td><td>20</td><td>21</td><td>25</td><td>5507</td><td>6114</td><td>13463</td><td>17458</td><td>1398</td><td>22642</td><td>22642</td><td>6272</td><td>13463</td><td>14408</td><td>17458</td><td>9487</td></tr>
    <tr><td>HALSTON HERITAGE Women's Sleeveless Ponte Pleated Dress</td><td>Halston Heritage</td><td>Dresses</td><td>357.0</td><td>161.36</td><td>1428.0</td><td>782.54</td><td>9</td><td>4</td><td>0</td><td>0</td><td>5</td><td>0.0</td><td>0.0</td><td>0.548</td><td>0.0</td><td>0.4444</td><td>0.0</td><td>0.5556</td><td>0.000529</td><td>0.0005593</td><td>4.96e-05</td><td>172</td><td>181</td><td>47</td><td>49</td><td>3355</td><td>776</td><td>13463</td><td>17458</td><td>3026</td><td>22642</td><td>22642</td><td>7812</td><td>13463</td><td>6492</td><td>17458</td><td>19270</td></tr>
    <tr><td>7 For All Mankind Men's Austyn Relaxed Straight Jean</td><td>7 For All Mankind</td><td>Jeans</td><td>197.94</td><td>111.63</td><td>1399.0</td><td>608.64</td><td>17</td><td>7</td><td>0</td><td>1</td><td>9</td><td>189.0</td><td>83.35</td><td>0.4351</td><td>0.0</td><td>0.4375</td><td>0.0588</td><td>0.5625</td><td>0.0005182</td><td>0.000435</td><td>9.38e-05</td><td>942</td><td>526</td><td>50</td><td>91</td><td>103</td><td>33</td><td>13463</td><td>7029</td><td>140</td><td>3671</td><td>4605</td><td>18597</td><td>13463</td><td>6734</td><td>17433</td><td>19266</td></tr>
    <tr><td>PAIGE Women's Skyline Skinny Jean</td><td>PAIGE</td><td>Jeans</td><td>158.0</td><td>90.19</td><td>1422.0</td><td>608.93</td><td>19</td><td>9</td><td>0</td><td>2</td><td>8</td><td>316.0</td><td>135.88</td><td>0.4282</td><td>0.0</td><td>0.5294</td><td>0.1053</td><td>0.4706</td><td>0.0005268</td><td>0.0004352</td><td>0.0001048</td><td>1714</td><td>1108</td><td>48</td><td>90</td><td>72</td><td>5</td><td>13463</td><td>2100</td><td>295</td><td>1575</td><td>2230</td><td>19172</td><td>13463</td><td>3268</td><td>16363</td><td>23444</td></tr>
    <tr><td>True Religion Women's Julie Super T Jean</td><td>True Religion</td><td>Jeans</td><td>326.0</td><td>172.13</td><td>1956.0</td><td>923.23</td><td>8</td><td>6</td><td>0</td><td>1</td><td>1</td><td>326.0</td><td>153.87</td><td>0.472</td><td>0.0</td><td>0.8571</td><td>0.125</td><td>0.1429</td><td>0.0007246</td><td>0.0006598</td><td>4.41e-05</td><td>233</td><td>145</td><td>19</td><td>31</td><td>5507</td><td>84</td><td>13463</td><td>7029</td><td>23197</td><td>1487</td><td>1788</td><td>15335</td><td>13463</td><td>546</td><td>14338</td><td>27121</td></tr>
    <tr><td>Mountain Hardwear Women's Chillwave Down Jacket</td><td>Mountain Hardwear</td><td>Outerwear & Coats</td><td>375.0</td><td>179.25</td><td>1875.0</td><td>978.75</td><td>6</td><td>5</td><td>0</td><td>1</td><td>0</td><td>375.0</td><td>195.75</td><td>0.522</td><td>0.0</td><td>1.0</td><td>0.1667</td><td>0.0</td><td>0.0006946</td><td>0.0006995</td><td>3.31e-05</td><td>155</td><td>128</td><td>20</td><td>29</td><td>12532</td><td>251</td><td>13463</td><td>7029</td><td>27145</td><td>1150</td><td>1161</td><td>10227</td><td>13463</td><td>1</td><td>10731</td><td>27145</td></tr>
    <tr><td>Barbour Bedale Jacket / Bedale Jacket</td><td>Barbour</td><td>Outerwear & Coats</td><td>379.0</td><td>173.96</td><td>1516.0</td><td>820.16</td><td>8</td><td>4</td><td>0</td><td>1</td><td>3</td><td>379.0</td><td>205.04</td><td>0.541</td><td>0.0</td><td>0.5714</td><td>0.125</td><td>0.4286</td><td>0.0005616</td><td>0.0005862</td><td>4.41e-05</td><td>147</td><td>142</td><td>39</td><td>39</td><td>5507</td><td>776</td><td>13463</td><td>7029</td><td>10869</td><td>1133</td><td>1085</td><td>8491</td><td>13463</td><td>2847</td><td>14338</td><td>23541</td></tr>
    <tr><td>Barbour Classic Beaufort Jacket / Beaufort Jacket</td><td>Barbour</td><td>Outerwear & Coats</td><td>399.0</td><td>193.91</td><td>1596.0</td><td>820.34</td><td>10</td><td>4</td><td>0</td><td>1</td><td>5</td><td>399.0</td><td>205.09</td><td>0.514</td><td>0.0</td><td>0.4444</td><td>0.1</td><td>0.5556</td><td>0.0005912</td><td>0.0005863</td><td>5.52e-05</td><td>115</td><td>98</td><td>35</td><td>38</td><td>1962</td><td>776</td><td>13463</td><td>7029</td><td>3026</td><td>985</td><td>1084</td><td>11041</td><td>13463</td><td>6492</td><td>16366</td><td>19270</td></tr>
  </tbody>
</table>

</div>

<h3>Bottom products by Lost Profit</h3>

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
WHERE profit_rank &lt;= 50
ORDER BY
  lost_profit_rank DESC
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
    <tr><td>The North Face Denali Down Womens Jacket 2013</td><td>The North Face</td><td>Active</td><td>903.0</td><td>395.51</td><td>1806.0</td><td>1014.97</td><td>8</td><td>2</td><td>0</td><td>0</td><td>6</td><td>0.0</td><td>0.0</td><td>0.562</td><td>0.0</td><td>0.25</td><td>0.0</td><td>0.75</td><td>0.000669</td><td>0.0007254</td><td>4.41e-05</td><td>5</td><td>20</td><td>21</td><td>25</td><td>5507</td><td>6114</td><td>13463</td><td>17458</td><td>1398</td><td>22642</td><td>22642</td><td>6272</td><td>13463</td><td>14408</td><td>17458</td><td>9487</td></tr>
    <tr><td>Women's Knee Length Overcoat in Pure Cashmere</td><td>Cashmere Boutique</td><td>Outerwear & Coats</td><td>399.0</td><td>193.12</td><td>1596.0</td><td>814.76</td><td>9</td><td>4</td><td>0</td><td>0</td><td>5</td><td>0.0</td><td>0.0</td><td>0.5105</td><td>0.0</td><td>0.4444</td><td>0.0</td><td>0.5556</td><td>0.0005912</td><td>0.0005823</td><td>4.96e-05</td><td>115</td><td>100</td><td>35</td><td>40</td><td>3355</td><td>776</td><td>13463</td><td>17458</td><td>3026</td><td>22642</td><td>22642</td><td>11502</td><td>13463</td><td>6492</td><td>17458</td><td>19270</td></tr>
    <tr><td>AIR JORDAN DOMINATE SHORTS MENS 465071-100</td><td>Jordan</td><td>Shorts</td><td>903.0</td><td>454.21</td><td>2709.0</td><td>1346.37</td><td>5</td><td>3</td><td>0</td><td>0</td><td>2</td><td>0.0</td><td>0.0</td><td>0.497</td><td>0.0</td><td>0.6</td><td>0.0</td><td>0.4</td><td>0.0010035</td><td>0.0009622</td><td>2.76e-05</td><td>5</td><td>8</td><td>7</td><td>9</td><td>16887</td><td>2358</td><td>13463</td><td>17458</td><td>17069</td><td>22642</td><td>22642</td><td>12874</td><td>13463</td><td>2189</td><td>17458</td><td>23875</td></tr>
    <tr><td>Steinbock Tyrolean Sport Coat</td><td>Orvis</td><td>Suits & Sport Coats</td><td>350.0</td><td>154.0</td><td>1400.0</td><td>784.0</td><td>11</td><td>4</td><td>0</td><td>0</td><td>7</td><td>0.0</td><td>0.0</td><td>0.56</td><td>0.0</td><td>0.3636</td><td>0.0</td><td>0.6364</td><td>0.0005186</td><td>0.0005603</td><td>6.07e-05</td><td>180</td><td>217</td><td>49</td><td>48</td><td>1161</td><td>776</td><td>13463</td><td>17458</td><td>623</td><td>22642</td><td>22642</td><td>6489</td><td>13463</td><td>9638</td><td>17458</td><td>16487</td></tr>
    <tr><td>Mountain Hardwear Men's Chillwave Down Parka</td><td>Mountain Hardwear</td><td>Outerwear & Coats</td><td>375.0</td><td>176.63</td><td>1500.0</td><td>793.5</td><td>5</td><td>4</td><td>0</td><td>0</td><td>1</td><td>0.0</td><td>0.0</td><td>0.529</td><td>0.0</td><td>0.8</td><td>0.0</td><td>0.2</td><td>0.0005557</td><td>0.0005671</td><td>2.76e-05</td><td>155</td><td>135</td><td>41</td><td>44</td><td>16887</td><td>776</td><td>13463</td><td>17458</td><td>23197</td><td>22642</td><td>22642</td><td>9645</td><td>13463</td><td>607</td><td>17458</td><td>26859</td></tr>
    <tr><td>The North Face Nuptse 2 Jacket - Noah Green/TNF Black</td><td>The North Face</td><td>Outerwear & Coats</td><td>903.0</td><td>370.23</td><td>1806.0</td><td>1065.54</td><td>8</td><td>2</td><td>0</td><td>0</td><td>6</td><td>0.0</td><td>0.0</td><td>0.59</td><td>0.0</td><td>0.25</td><td>0.0</td><td>0.75</td><td>0.000669</td><td>0.0007615</td><td>4.41e-05</td><td>5</td><td>29</td><td>21</td><td>19</td><td>5507</td><td>6114</td><td>13463</td><td>17458</td><td>1398</td><td>22642</td><td>22642</td><td>3353</td><td>13463</td><td>14408</td><td>17458</td><td>9487</td></tr>
    <tr><td>HALSTON HERITAGE Women's Sleeveless Ponte Pleated Dress</td><td>Halston Heritage</td><td>Dresses</td><td>357.0</td><td>161.36</td><td>1428.0</td><td>782.54</td><td>9</td><td>4</td><td>0</td><td>0</td><td>5</td><td>0.0</td><td>0.0</td><td>0.548</td><td>0.0</td><td>0.4444</td><td>0.0</td><td>0.5556</td><td>0.000529</td><td>0.0005593</td><td>4.96e-05</td><td>172</td><td>181</td><td>47</td><td>49</td><td>3355</td><td>776</td><td>13463</td><td>17458</td><td>3026</td><td>22642</td><td>22642</td><td>7812</td><td>13463</td><td>6492</td><td>17458</td><td>19270</td></tr>
    <tr><td>Quiksilver Men's Rockefeller Walkshort</td><td>Quiksilver</td><td>Shorts</td><td>903.0</td><td>472.27</td><td>1806.0</td><td>861.46</td><td>6</td><td>2</td><td>0</td><td>0</td><td>4</td><td>0.0</td><td>0.0</td><td>0.477</td><td>0.0</td><td>0.3333</td><td>0.0</td><td>0.6667</td><td>0.000669</td><td>0.0006157</td><td>3.31e-05</td><td>5</td><td>7</td><td>21</td><td>34</td><td>12532</td><td>6114</td><td>13463</td><td>17458</td><td>6105</td><td>22642</td><td>22642</td><td>14881</td><td>13463</td><td>9747</td><td>17458</td><td>12990</td></tr>
    <tr><td>True Religion Women's Julie Super T Jean</td><td>True Religion</td><td>Jeans</td><td>326.0</td><td>172.13</td><td>1956.0</td><td>923.23</td><td>8</td><td>6</td><td>0</td><td>1</td><td>1</td><td>326.0</td><td>153.87</td><td>0.472</td><td>0.0</td><td>0.8571</td><td>0.125</td><td>0.1429</td><td>0.0007246</td><td>0.0006598</td><td>4.41e-05</td><td>233</td><td>145</td><td>19</td><td>31</td><td>5507</td><td>84</td><td>13463</td><td>7029</td><td>23197</td><td>1487</td><td>1788</td><td>15335</td><td>13463</td><td>546</td><td>14338</td><td>27121</td></tr>
    <tr><td>Mountain Hardwear Women's Chillwave Down Jacket</td><td>Mountain Hardwear</td><td>Outerwear & Coats</td><td>375.0</td><td>179.25</td><td>1875.0</td><td>978.75</td><td>6</td><td>5</td><td>0</td><td>1</td><td>0</td><td>375.0</td><td>195.75</td><td>0.522</td><td>0.0</td><td>1.0</td><td>0.1667</td><td>0.0</td><td>0.0006946</td><td>0.0006995</td><td>3.31e-05</td><td>155</td><td>128</td><td>20</td><td>29</td><td>12532</td><td>251</td><td>13463</td><td>7029</td><td>27145</td><td>1150</td><td>1161</td><td>10227</td><td>13463</td><td>1</td><td>10731</td><td>27145</td></tr>
    <tr><td>Barbour Bedale Jacket / Bedale Jacket</td><td>Barbour</td><td>Outerwear & Coats</td><td>379.0</td><td>173.96</td><td>1516.0</td><td>820.16</td><td>8</td><td>4</td><td>0</td><td>1</td><td>3</td><td>379.0</td><td>205.04</td><td>0.541</td><td>0.0</td><td>0.5714</td><td>0.125</td><td>0.4286</td><td>0.0005616</td><td>0.0005862</td><td>4.41e-05</td><td>147</td><td>142</td><td>39</td><td>39</td><td>5507</td><td>776</td><td>13463</td><td>7029</td><td>10869</td><td>1133</td><td>1085</td><td>8491</td><td>13463</td><td>2847</td><td>14338</td><td>23541</td></tr>
    <tr><td>Barbour Classic Beaufort Jacket / Beaufort Jacket</td><td>Barbour</td><td>Outerwear & Coats</td><td>399.0</td><td>193.91</td><td>1596.0</td><td>820.34</td><td>10</td><td>4</td><td>0</td><td>1</td><td>5</td><td>399.0</td><td>205.09</td><td>0.514</td><td>0.0</td><td>0.4444</td><td>0.1</td><td>0.5556</td><td>0.0005912</td><td>0.0005863</td><td>5.52e-05</td><td>115</td><td>98</td><td>35</td><td>38</td><td>1962</td><td>776</td><td>13463</td><td>7029</td><td>3026</td><td>985</td><td>1084</td><td>11041</td><td>13463</td><td>6492</td><td>16366</td><td>19270</td></tr>
    <tr><td>Carhartt Men's Canvas Shirt Jacket</td><td>Carhartt</td><td>Outerwear & Coats</td><td>448.99</td><td>181.39</td><td>1346.97</td><td>802.79</td><td>5</td><td>3</td><td>0</td><td>1</td><td>1</td><td>448.99</td><td>267.6</td><td>0.596</td><td>0.0</td><td>0.75</td><td>0.2</td><td>0.25</td><td>0.000499</td><td>0.0005737</td><td>2.76e-05</td><td>92</td><td>120</td><td>61</td><td>42</td><td>16887</td><td>2358</td><td>13463</td><td>7029</td><td>23197</td><td>828</td><td>658</td><td>2857</td><td>13463</td><td>746</td><td>8435</td><td>26348</td></tr>
    <tr><td>Jones New York Women's Hidden Snap Notch Collar Coat</td><td>Jones New York</td><td>Outerwear & Coats</td><td>599.0</td><td>253.38</td><td>1797.0</td><td>1036.87</td><td>5</td><td>3</td><td>0</td><td>1</td><td>1</td><td>599.0</td><td>345.62</td><td>0.577</td><td>0.0</td><td>0.75</td><td>0.2</td><td>0.25</td><td>0.0006657</td><td>0.000741</td><td>2.76e-05</td><td>56</td><td>61</td><td>28</td><td>24</td><td>16887</td><td>2358</td><td>13463</td><td>7029</td><td>23197</td><td>428</td><td>368</td><td>4613</td><td>13463</td><td>746</td><td>8435</td><td>26348</td></tr>
    <tr><td>Rebecca Minkoff Women's Leather Luciana Skirt</td><td>Rebecca Minkoff</td><td>Skirts</td><td>598.0</td><td>249.96</td><td>1794.0</td><td>1044.11</td><td>7</td><td>3</td><td>1</td><td>0</td><td>3</td><td>598.0</td><td>348.04</td><td>0.582</td><td>0.25</td><td>0.4286</td><td>0.0</td><td>0.5</td><td>0.0006646</td><td>0.0007462</td><td>3.86e-05</td><td>57</td><td>62</td><td>30</td><td>22</td><td>8625</td><td>2358</td><td>3978</td><td>17458</td><td>10869</td><td>430</td><td>358</td><td>4095</td><td>11344</td><td>6739</td><td>17458</td><td>19501</td></tr>
  </tbody>
</table>

</div>

<h3>Analytical Insights & Business Recommendations</h3>
<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p>The bottom 15 products by revenue all show $0 in completed revenue — every order for these items was either cancelled, returned, or is still in transit with no completions. Products like Marc Ecko Cut & Sew Pinstripe Vest (10 orders, $0 revenue), Diesel Women's Louvboot Slim Flare Jean (4 orders, $0 revenue), and Allegra K Dotted Dress (5 orders, $0 revenue) are occupying warehouse space and shipping bandwidth without generating any return. Many of these zero-revenue products still have units en route (shown by en_route_rate of 1.0), meaning they are actively consuming fulfillment resources. Others have high cancellation rates, suggesting customers are abandoning these purchases during checkout or processing.</p>

<p>Recommendation: These zero-revenue products should be evaluated for delisting. If a product has generated multiple orders but zero completions, the pattern indicates either a systemic quality issue, misleading product listings, or severe delivery problems. Flag all products with 3+ orders and $0 revenue for an immediate review, and consider removing them from active listings if the pattern persists, as they are wasting inventory space and shipping bandwidth that could serve profitable items.</p>

<p>Among the top 50 products by order volume, the lowest-profit items are dominated by low-price-point basics: HUGO BOSS Argyle Crew Socks ($9.75 avg sale, $15.65 profit on 22 orders), Gregg Homme Bikini Swimsuit ($13.22 avg sale, $20.64 profit on 25 orders), and Puma Men's Socks ($13.00 avg sale, $35.98 profit on 24 orders). These high-volume, low-profit products have thin individual margins and contribute minimally to overall profitability despite generating consistent order activity. Their high volume creates operational costs (picking, packing, shipping) that may approach or exceed their profit contribution.</p>

<p>Recommendation: For low-profit basics that still move volume, consider two strategies: (1) bundle them with higher-margin items to improve basket profitability — e.g., include socks or underwear as add-on suggestions when customers are purchasing outerwear or jeans; (2) streamline their fulfillment by packaging commonly co-ordered basics together to reduce per-unit handling costs.</p>

<p>The lowest profit margins among top-50 revenue products include The North Face Apex Bionic ($903 sale, 41.9% margin), PAIGE Skyline Skinny Jean (42.8% margin), and 7 For All Mankind Austyn Relaxed Straight (43.5% margin). These are high-cost items where the gap between sale price and product cost is compressed.</p>

<p>Recommendation: For premium products with low margins, negotiate better supplier pricing. The North Face Apex Bionic has a $524.64 average cost on a $903 sale price — the margin is below 42% while comparable outerwear in the top products section achieves 54–59%. Either the supplier cost is disproportionately high or the retail price is undervaluing the brand. Explore whether cost renegotiation or a modest price increase (given the premium brand positioning) can bring margins in line with category peers.</p>

<p>Several bottom products by return rate (filtered to top-20 revenue items) actually show the lowest return rates in the dataset. Products like AIR JORDAN DOMINATE SHORTS (0% return rate), Canada Goose Women's Expedition Parka (0% return rate, 100% completion rate), and True Religion Women's Julie Super T Jean (0% return rate) demonstrate strong product quality and customer satisfaction.</p>

<p>Recommendation: These low-return, high-revenue products represent quality benchmarks. Investigate their suppliers, product descriptions, sizing accuracy, and packaging to identify what practices keep returns at zero. Apply those practices (better product photography, more accurate sizing guides, quality packaging) to high-return items in the same categories to reduce return-driven revenue leakage.</p>

<p>The bottom products by lost revenue (filtered to top-50 revenue items) include several products with $0 in lost revenue — Steinbock Tyrolean Sport Coat, The North Face Apex Bionic, Women's Cashmere Overcoat, Mountain Hardwear Chillwave Parka, and AIR JORDAN DOMINATE SHORTS all have zero cancellations and zero returns among their completed orders. These products represent the ideal state: customers order them, the orders complete, and no revenue is lost to returns or cancellations. The common thread is premium outerwear/coats and specialty items where purchase intent is presumably more deliberate.</p>

<p>Recommendation: Prioritize internal inventory space and marketing resources for these zero-loss products. They are the most operationally efficient items in the catalog — every unit shipped generates full revenue with no return-processing costs or refund overhead. Ensure these items never experience stockouts, as the demand-to-completion pipeline is clean.</p>

<p>The bottom 15 products by unit orders all have just 1 order placed, with most generating $0 revenue. Products like Ulla Popken Sequined Swing Jacket (1 order, cancelled), Acid Wash Jean Dark Leggings (1 order, returned), and multiple others across various brands represent the extreme long tail of the product catalog. With over 27,000+ products ranked at the bottom for order volume, a significant portion of the catalog may be dead weight — occupying listing space, complicating inventory management, and diluting search/browse results for customers.</p>

<p>Recommendation: Consider dropping products with fewer than 3 lifetime orders and $0 revenue from active listings. This catalog pruning would reduce operational complexity without meaningfully impacting revenue, and it would improve the browsing and search experience for customers by surfacing higher-performing items. These low-performing products may also indicate brands that are not resonating with the customer base.</p>

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

<h3>Top brands by Profit</h3>

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
  profit_rank ASC
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
    <tr><td>Calvin Klein</td><td>62.49</td><td>29.31</td><td>53041.76</td><td>28267.04</td><td>3180</td><td>820</td><td>322</td><td>471</td><td>1567</td><td>48698.1</td><td>25795.42</td><td>0.5329</td><td>0.282</td><td>0.3027</td><td>0.1481</td><td>0.6565</td><td>0.0196488</td><td>0.0202021</td><td>0.0175425</td><td>805</td><td>836</td><td>2</td><td>1</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>1</td><td>1128</td><td>1282</td><td>1212</td><td>1270</td><td>1568</td></tr>
    <tr><td>Diesel</td><td>138.24</td><td>68.92</td><td>53774.81</td><td>27000.8</td><td>1466</td><td>378</td><td>143</td><td>213</td><td>732</td><td>49754.6</td><td>24735.41</td><td>0.5021</td><td>0.2745</td><td>0.3017</td><td>0.1453</td><td>0.6595</td><td>0.0199204</td><td>0.0192971</td><td>0.0080872</td><td>205</td><td>184</td><td>1</td><td>2</td><td>13</td><td>10</td><td>12</td><td>13</td><td>13</td><td>1</td><td>2</td><td>1502</td><td>1319</td><td>1221</td><td>1318</td><td>1552</td></tr>
    <tr><td>Carhartt</td><td>68.41</td><td>32.02</td><td>44947.96</td><td>23945.23</td><td>2509</td><td>663</td><td>251</td><td>366</td><td>1229</td><td>41134.22</td><td>22022.28</td><td>0.5327</td><td>0.2746</td><td>0.3094</td><td>0.1459</td><td>0.6496</td><td>0.0166506</td><td>0.0171134</td><td>0.0138409</td><td>703</td><td>724</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>5</td><td>3</td><td>1132</td><td>1317</td><td>1155</td><td>1311</td><td>1623</td></tr>
    <tr><td>True Religion</td><td>196.17</td><td>101.7</td><td>43598.78</td><td>21127.8</td><td>879</td><td>225</td><td>84</td><td>146</td><td>424</td><td>43136.54</td><td>20619.76</td><td>0.4846</td><td>0.2718</td><td>0.307</td><td>0.1661</td><td>0.6533</td><td>0.0161508</td><td>0.0150998</td><td>0.004849</td><td>91</td><td>64</td><td>4</td><td>4</td><td>27</td><td>28</td><td>33</td><td>25</td><td>29</td><td>4</td><td>5</td><td>1705</td><td>1347</td><td>1186</td><td>1064</td><td>1592</td></tr>
    <tr><td>7 For All Mankind</td><td>155.67</td><td>81.33</td><td>39429.55</td><td>18708.21</td><td>1086</td><td>254</td><td>108</td><td>179</td><td>545</td><td>44113.73</td><td>21179.32</td><td>0.4745</td><td>0.2983</td><td>0.28</td><td>0.1648</td><td>0.6821</td><td>0.0146063</td><td>0.0133705</td><td>0.0059909</td><td>156</td><td>123</td><td>5</td><td>5</td><td>20</td><td>24</td><td>19</td><td>19</td><td>20</td><td>3</td><td>4</td><td>1826</td><td>1168</td><td>1503</td><td>1067</td><td>1192</td></tr>
    <tr><td>Columbia</td><td>69.37</td><td>31.72</td><td>26587.28</td><td>14439.48</td><td>1529</td><td>374</td><td>135</td><td>252</td><td>768</td><td>26842.48</td><td>14585.03</td><td>0.5431</td><td>0.2652</td><td>0.2929</td><td>0.1648</td><td>0.6725</td><td>0.009849</td><td>0.0103197</td><td>0.0084347</td><td>687</td><td>737</td><td>8</td><td>6</td><td>11</td><td>11</td><td>13</td><td>9</td><td>11</td><td>8</td><td>7</td><td>987</td><td>1379</td><td>1340</td><td>1067</td><td>1270</td></tr>
    <tr><td>Tommy Hilfiger</td><td>71.62</td><td>32.46</td><td>26074.49</td><td>14100.38</td><td>1615</td><td>404</td><td>162</td><td>254</td><td>795</td><td>29731.26</td><td>16179.42</td><td>0.5408</td><td>0.2862</td><td>0.2968</td><td>0.1573</td><td>0.6631</td><td>0.0096591</td><td>0.0100774</td><td>0.0089092</td><td>649</td><td>706</td><td>9</td><td>7</td><td>8</td><td>8</td><td>10</td><td>8</td><td>9</td><td>6</td><td>6</td><td>1021</td><td>1218</td><td>1294</td><td>1152</td><td>1525</td></tr>
    <tr><td>Volcom</td><td>58.67</td><td>29.91</td><td>28804.39</td><td>14059.0</td><td>1893</td><td>482</td><td>182</td><td>294</td><td>935</td><td>26458.99</td><td>12887.05</td><td>0.4881</td><td>0.2741</td><td>0.3014</td><td>0.1553</td><td>0.6598</td><td>0.0106703</td><td>0.0100478</td><td>0.0104428</td><td>877</td><td>805</td><td>6</td><td>8</td><td>5</td><td>4</td><td>7</td><td>5</td><td>5</td><td>9</td><td>10</td><td>1663</td><td>1320</td><td>1223</td><td>1174</td><td>1547</td></tr>
    <tr><td>Ray-Ban</td><td>118.89</td><td>50.08</td><td>23852.78</td><td>13833.41</td><td>798</td><td>206</td><td>78</td><td>131</td><td>383</td><td>25134.08</td><td>14434.77</td><td>0.5799</td><td>0.2746</td><td>0.3088</td><td>0.1642</td><td>0.6503</td><td>0.008836</td><td>0.0098866</td><td>0.0044022</td><td>278</td><td>346</td><td>15</td><td>9</td><td>34</td><td>32</td><td>35</td><td>30</td><td>37</td><td>11</td><td>8</td><td>437</td><td>1317</td><td>1160</td><td>1073</td><td>1612</td></tr>
    <tr><td>The North Face</td><td>440.81</td><td>197.82</td><td>25174.88</td><td>13719.13</td><td>233</td><td>61</td><td>20</td><td>36</td><td>116</td><td>21048.75</td><td>11669.08</td><td>0.545</td><td>0.2469</td><td>0.3096</td><td>0.1545</td><td>0.6554</td><td>0.0093258</td><td>0.0098049</td><td>0.0012853</td><td>9</td><td>9</td><td>11</td><td>10</td><td>153</td><td>152</td><td>182</td><td>151</td><td>153</td><td>16</td><td>16</td><td>962</td><td>1608</td><td>1153</td><td>1181</td><td>1574</td></tr>
    <tr><td>Jones New York</td><td>100.52</td><td>45.47</td><td>24723.78</td><td>13604.24</td><td>846</td><td>230</td><td>96</td><td>114</td><td>406</td><td>20262.41</td><td>10960.83</td><td>0.5502</td><td>0.2945</td><td>0.3142</td><td>0.1348</td><td>0.6384</td><td>0.0091587</td><td>0.0097228</td><td>0.004667</td><td>361</td><td>403</td><td>13</td><td>11</td><td>32</td><td>27</td><td>27</td><td>34</td><td>33</td><td>18</td><td>18</td><td>876</td><td>1178</td><td>1106</td><td>1532</td><td>1701</td></tr>
    <tr><td>Orvis</td><td>128.92</td><td>60.07</td><td>25260.0</td><td>13494.35</td><td>721</td><td>186</td><td>65</td><td>102</td><td>368</td><td>21012.0</td><td>11275.59</td><td>0.5342</td><td>0.259</td><td>0.3005</td><td>0.1415</td><td>0.6643</td><td>0.0093573</td><td>0.0096442</td><td>0.0039774</td><td>239</td><td>245</td><td>10</td><td>12</td><td>39</td><td>39</td><td>47</td><td>44</td><td>38</td><td>17</td><td>17</td><td>1110</td><td>1416</td><td>1228</td><td>1453</td><td>1519</td></tr>
    <tr><td>Oakley</td><td>110.41</td><td>49.26</td><td>24423.2</td><td>13410.52</td><td>866</td><td>225</td><td>90</td><td>118</td><td>433</td><td>23073.48</td><td>12801.68</td><td>0.5491</td><td>0.2857</td><td>0.3008</td><td>0.1363</td><td>0.6581</td><td>0.0090474</td><td>0.0095843</td><td>0.0047773</td><td>316</td><td>355</td><td>14</td><td>13</td><td>29</td><td>28</td><td>30</td><td>33</td><td>27</td><td>12</td><td>12</td><td>896</td><td>1219</td><td>1227</td><td>1522</td><td>1556</td></tr>
    <tr><td>Quiksilver</td><td>57.01</td><td>30.91</td><td>27609.19</td><td>12579.68</td><td>1873</td><td>471</td><td>202</td><td>297</td><td>903</td><td>26410.17</td><td>12067.7</td><td>0.4556</td><td>0.3001</td><td>0.2989</td><td>0.1586</td><td>0.6572</td><td>0.0102276</td><td>0.0089905</td><td>0.0103324</td><td>903</td><td>764</td><td>7</td><td>14</td><td>6</td><td>6</td><td>5</td><td>4</td><td>7</td><td>10</td><td>14</td><td>2066</td><td>1129</td><td>1275</td><td>1126</td><td>1563</td></tr>
    <tr><td>Joe&#x27;s Jeans</td><td>152.81</td><td>80.23</td><td>25134.81</td><td>11891.96</td><td>697</td><td>169</td><td>76</td><td>99</td><td>353</td><td>27326.02</td><td>13164.83</td><td>0.4731</td><td>0.3102</td><td>0.2826</td><td>0.142</td><td>0.6762</td><td>0.009311</td><td>0.008499</td><td>0.003845</td><td>163</td><td>133</td><td>12</td><td>15</td><td>41</td><td>42</td><td>38</td><td>47</td><td>41</td><td>7</td><td>9</td><td>1850</td><td>1094</td><td>1486</td><td>1448</td><td>1239</td></tr>
  </tbody>
</table>

</div>

<h3>Top brands by Profit Margin</h3>

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
WHERE revenue_rank &lt;= 30
ORDER BY
  profit_margin_rank ASC
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
    <tr><td>Ray-Ban</td><td>118.89</td><td>50.08</td><td>23852.78</td><td>13833.41</td><td>798</td><td>206</td><td>78</td><td>131</td><td>383</td><td>25134.08</td><td>14434.77</td><td>0.5799</td><td>0.2746</td><td>0.3088</td><td>0.1642</td><td>0.6503</td><td>0.008836</td><td>0.0098866</td><td>0.0044022</td><td>278</td><td>346</td><td>15</td><td>9</td><td>34</td><td>32</td><td>35</td><td>30</td><td>37</td><td>11</td><td>8</td><td>437</td><td>1317</td><td>1160</td><td>1073</td><td>1612</td></tr>
    <tr><td>Paul Fredrick</td><td>150.52</td><td>65.49</td><td>17954.0</td><td>10251.08</td><td>445</td><td>112</td><td>42</td><td>56</td><td>235</td><td>15161.0</td><td>8567.86</td><td>0.571</td><td>0.2727</td><td>0.2879</td><td>0.1258</td><td>0.6772</td><td>0.0066509</td><td>0.0073263</td><td>0.0024548</td><td>171</td><td>209</td><td>24</td><td>18</td><td>68</td><td>70</td><td>84</td><td>91</td><td>65</td><td>28</td><td>26</td><td>538</td><td>1322</td><td>1379</td><td>1628</td><td>1232</td></tr>
    <tr><td>Jones New York</td><td>100.52</td><td>45.47</td><td>24723.78</td><td>13604.24</td><td>846</td><td>230</td><td>96</td><td>114</td><td>406</td><td>20262.41</td><td>10960.83</td><td>0.5502</td><td>0.2945</td><td>0.3142</td><td>0.1348</td><td>0.6384</td><td>0.0091587</td><td>0.0097228</td><td>0.004667</td><td>361</td><td>403</td><td>13</td><td>11</td><td>32</td><td>27</td><td>27</td><td>34</td><td>33</td><td>18</td><td>18</td><td>876</td><td>1178</td><td>1106</td><td>1532</td><td>1701</td></tr>
    <tr><td>Oakley</td><td>110.41</td><td>49.26</td><td>24423.2</td><td>13410.52</td><td>866</td><td>225</td><td>90</td><td>118</td><td>433</td><td>23073.48</td><td>12801.68</td><td>0.5491</td><td>0.2857</td><td>0.3008</td><td>0.1363</td><td>0.6581</td><td>0.0090474</td><td>0.0095843</td><td>0.0047773</td><td>316</td><td>355</td><td>14</td><td>13</td><td>29</td><td>28</td><td>30</td><td>33</td><td>27</td><td>12</td><td>12</td><td>896</td><td>1219</td><td>1227</td><td>1522</td><td>1556</td></tr>
    <tr><td>Mountain Hardwear</td><td>170.78</td><td>76.25</td><td>19859.63</td><td>10859.12</td><td>425</td><td>116</td><td>34</td><td>64</td><td>211</td><td>16634.22</td><td>9313.3</td><td>0.5468</td><td>0.2267</td><td>0.3213</td><td>0.1506</td><td>0.6453</td><td>0.0073568</td><td>0.0077609</td><td>0.0023445</td><td>131</td><td>154</td><td>17</td><td>17</td><td>77</td><td>66</td><td>106</td><td>76</td><td>72</td><td>24</td><td>22</td><td>934</td><td>1666</td><td>1047</td><td>1241</td><td>1651</td></tr>
    <tr><td>Arc&#x27;teryx</td><td>323.7</td><td>146.18</td><td>18141.7</td><td>9908.14</td><td>271</td><td>56</td><td>22</td><td>41</td><td>152</td><td>22880.85</td><td>12500.89</td><td>0.5462</td><td>0.2821</td><td>0.2435</td><td>0.1513</td><td>0.7308</td><td>0.0067204</td><td>0.0070812</td><td>0.001495</td><td>22</td><td>20</td><td>22</td><td>19</td><td>132</td><td>169</td><td>161</td><td>132</td><td>118</td><td>13</td><td>13</td><td>943</td><td>1281</td><td>1928</td><td>1234</td><td>808</td></tr>
    <tr><td>The North Face</td><td>440.81</td><td>197.82</td><td>25174.88</td><td>13719.13</td><td>233</td><td>61</td><td>20</td><td>36</td><td>116</td><td>21048.75</td><td>11669.08</td><td>0.545</td><td>0.2469</td><td>0.3096</td><td>0.1545</td><td>0.6554</td><td>0.0093258</td><td>0.0098049</td><td>0.0012853</td><td>9</td><td>9</td><td>11</td><td>10</td><td>153</td><td>152</td><td>182</td><td>151</td><td>153</td><td>16</td><td>16</td><td>962</td><td>1608</td><td>1153</td><td>1181</td><td>1574</td></tr>
    <tr><td>Columbia</td><td>69.37</td><td>31.72</td><td>26587.28</td><td>14439.48</td><td>1529</td><td>374</td><td>135</td><td>252</td><td>768</td><td>26842.48</td><td>14585.03</td><td>0.5431</td><td>0.2652</td><td>0.2929</td><td>0.1648</td><td>0.6725</td><td>0.009849</td><td>0.0103197</td><td>0.0084347</td><td>687</td><td>737</td><td>8</td><td>6</td><td>11</td><td>11</td><td>13</td><td>9</td><td>11</td><td>8</td><td>7</td><td>987</td><td>1379</td><td>1340</td><td>1067</td><td>1270</td></tr>
    <tr><td>Tommy Hilfiger</td><td>71.62</td><td>32.46</td><td>26074.49</td><td>14100.38</td><td>1615</td><td>404</td><td>162</td><td>254</td><td>795</td><td>29731.26</td><td>16179.42</td><td>0.5408</td><td>0.2862</td><td>0.2968</td><td>0.1573</td><td>0.6631</td><td>0.0096591</td><td>0.0100774</td><td>0.0089092</td><td>649</td><td>706</td><td>9</td><td>7</td><td>8</td><td>8</td><td>10</td><td>8</td><td>9</td><td>6</td><td>6</td><td>1021</td><td>1218</td><td>1294</td><td>1152</td><td>1525</td></tr>
    <tr><td>Kenneth Cole</td><td>84.27</td><td>39.03</td><td>15734.23</td><td>8442.44</td><td>775</td><td>189</td><td>79</td><td>111</td><td>396</td><td>15627.95</td><td>8304.84</td><td>0.5366</td><td>0.2948</td><td>0.2846</td><td>0.1432</td><td>0.6769</td><td>0.0058286</td><td>0.0060337</td><td>0.0042753</td><td>499</td><td>528</td><td>27</td><td>26</td><td>36</td><td>36</td><td>34</td><td>35</td><td>35</td><td>27</td><td>27</td><td>1079</td><td>1177</td><td>1464</td><td>1333</td><td>1235</td></tr>
    <tr><td>Orvis</td><td>128.92</td><td>60.07</td><td>25260.0</td><td>13494.35</td><td>721</td><td>186</td><td>65</td><td>102</td><td>368</td><td>21012.0</td><td>11275.59</td><td>0.5342</td><td>0.259</td><td>0.3005</td><td>0.1415</td><td>0.6643</td><td>0.0093573</td><td>0.0096442</td><td>0.0039774</td><td>239</td><td>245</td><td>10</td><td>12</td><td>39</td><td>39</td><td>47</td><td>44</td><td>38</td><td>17</td><td>17</td><td>1110</td><td>1416</td><td>1228</td><td>1453</td><td>1519</td></tr>
    <tr><td>Calvin Klein</td><td>62.49</td><td>29.31</td><td>53041.76</td><td>28267.04</td><td>3180</td><td>820</td><td>322</td><td>471</td><td>1567</td><td>48698.1</td><td>25795.42</td><td>0.5329</td><td>0.282</td><td>0.3027</td><td>0.1481</td><td>0.6565</td><td>0.0196488</td><td>0.0202021</td><td>0.0175425</td><td>805</td><td>836</td><td>2</td><td>1</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>1</td><td>1128</td><td>1282</td><td>1212</td><td>1270</td><td>1568</td></tr>
    <tr><td>Carhartt</td><td>68.41</td><td>32.02</td><td>44947.96</td><td>23945.23</td><td>2509</td><td>663</td><td>251</td><td>366</td><td>1229</td><td>41134.22</td><td>22022.28</td><td>0.5327</td><td>0.2746</td><td>0.3094</td><td>0.1459</td><td>0.6496</td><td>0.0166506</td><td>0.0171134</td><td>0.0138409</td><td>703</td><td>724</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>5</td><td>3</td><td>1132</td><td>1317</td><td>1155</td><td>1311</td><td>1623</td></tr>
    <tr><td>Ralph Lauren</td><td>86.37</td><td>40.49</td><td>16195.65</td><td>8604.78</td><td>760</td><td>188</td><td>67</td><td>107</td><td>398</td><td>15089.08</td><td>8150.14</td><td>0.5313</td><td>0.2627</td><td>0.2879</td><td>0.1408</td><td>0.6792</td><td>0.0059995</td><td>0.0061497</td><td>0.0041925</td><td>487</td><td>491</td><td>26</td><td>24</td><td>37</td><td>37</td><td>44</td><td>38</td><td>34</td><td>29</td><td>29</td><td>1150</td><td>1396</td><td>1379</td><td>1459</td><td>1221</td></tr>
    <tr><td>Allegra K</td><td>14.35</td><td>6.76</td><td>20908.12</td><td>11061.0</td><td>6057</td><td>1467</td><td>610</td><td>943</td><td>3037</td><td>22396.3</td><td>11874.9</td><td>0.529</td><td>0.2937</td><td>0.2869</td><td>0.1557</td><td>0.6743</td><td>0.0077452</td><td>0.0079052</td><td>0.0334135</td><td>2442</td><td>2434</td><td>16</td><td>16</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>15</td><td>15</td><td>1172</td><td>1190</td><td>1384</td><td>1170</td><td>1255</td></tr>
  </tbody>
</table>

</div>

<h3>Top brands by Unit Orders</h3>

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
  unit_orders_placed_rank ASC
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
    <tr><td>Allegra K</td><td>14.35</td><td>6.76</td><td>20908.12</td><td>11061.0</td><td>6057</td><td>1467</td><td>610</td><td>943</td><td>3037</td><td>22396.3</td><td>11874.9</td><td>0.529</td><td>0.2937</td><td>0.2869</td><td>0.1557</td><td>0.6743</td><td>0.0077452</td><td>0.0079052</td><td>0.0334135</td><td>2442</td><td>2434</td><td>16</td><td>16</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>15</td><td>15</td><td>1172</td><td>1190</td><td>1384</td><td>1170</td><td>1255</td></tr>
    <tr><td>Calvin Klein</td><td>62.49</td><td>29.31</td><td>53041.76</td><td>28267.04</td><td>3180</td><td>820</td><td>322</td><td>471</td><td>1567</td><td>48698.1</td><td>25795.42</td><td>0.5329</td><td>0.282</td><td>0.3027</td><td>0.1481</td><td>0.6565</td><td>0.0196488</td><td>0.0202021</td><td>0.0175425</td><td>805</td><td>836</td><td>2</td><td>1</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>1</td><td>1128</td><td>1282</td><td>1212</td><td>1270</td><td>1568</td></tr>
    <tr><td>Carhartt</td><td>68.41</td><td>32.02</td><td>44947.96</td><td>23945.23</td><td>2509</td><td>663</td><td>251</td><td>366</td><td>1229</td><td>41134.22</td><td>22022.28</td><td>0.5327</td><td>0.2746</td><td>0.3094</td><td>0.1459</td><td>0.6496</td><td>0.0166506</td><td>0.0171134</td><td>0.0138409</td><td>703</td><td>724</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>5</td><td>3</td><td>1132</td><td>1317</td><td>1155</td><td>1311</td><td>1623</td></tr>
    <tr><td>Hanes</td><td>20.0</td><td>9.63</td><td>9350.02</td><td>4878.18</td><td>1966</td><td>473</td><td>225</td><td>275</td><td>993</td><td>10001.01</td><td>5127.51</td><td>0.5217</td><td>0.3223</td><td>0.2797</td><td>0.1399</td><td>0.6774</td><td>0.0034636</td><td>0.0034864</td><td>0.0108455</td><td>2145</td><td>2182</td><td>59</td><td>58</td><td>4</td><td>5</td><td>4</td><td>6</td><td>4</td><td>54</td><td>56</td><td>1270</td><td>1053</td><td>1511</td><td>1469</td><td>1230</td></tr>
    <tr><td>Volcom</td><td>58.67</td><td>29.91</td><td>28804.39</td><td>14059.0</td><td>1893</td><td>482</td><td>182</td><td>294</td><td>935</td><td>26458.99</td><td>12887.05</td><td>0.4881</td><td>0.2741</td><td>0.3014</td><td>0.1553</td><td>0.6598</td><td>0.0106703</td><td>0.0100478</td><td>0.0104428</td><td>877</td><td>805</td><td>6</td><td>8</td><td>5</td><td>4</td><td>7</td><td>5</td><td>5</td><td>9</td><td>10</td><td>1663</td><td>1320</td><td>1223</td><td>1174</td><td>1547</td></tr>
    <tr><td>Quiksilver</td><td>57.01</td><td>30.91</td><td>27609.19</td><td>12579.68</td><td>1873</td><td>471</td><td>202</td><td>297</td><td>903</td><td>26410.17</td><td>12067.7</td><td>0.4556</td><td>0.3001</td><td>0.2989</td><td>0.1586</td><td>0.6572</td><td>0.0102276</td><td>0.0089905</td><td>0.0103324</td><td>903</td><td>764</td><td>7</td><td>14</td><td>6</td><td>6</td><td>5</td><td>4</td><td>7</td><td>10</td><td>14</td><td>2066</td><td>1129</td><td>1275</td><td>1126</td><td>1563</td></tr>
    <tr><td>Nautica</td><td>41.7</td><td>20.24</td><td>18412.72</td><td>9492.15</td><td>1827</td><td>451</td><td>185</td><td>266</td><td>925</td><td>18833.69</td><td>9728.4</td><td>0.5155</td><td>0.2909</td><td>0.2889</td><td>0.1456</td><td>0.6722</td><td>0.0068208</td><td>0.0067839</td><td>0.0100787</td><td>1306</td><td>1314</td><td>19</td><td>20</td><td>7</td><td>7</td><td>6</td><td>7</td><td>6</td><td>22</td><td>19</td><td>1351</td><td>1204</td><td>1371</td><td>1315</td><td>1272</td></tr>
    <tr><td>Tommy Hilfiger</td><td>71.62</td><td>32.46</td><td>26074.49</td><td>14100.38</td><td>1615</td><td>404</td><td>162</td><td>254</td><td>795</td><td>29731.26</td><td>16179.42</td><td>0.5408</td><td>0.2862</td><td>0.2968</td><td>0.1573</td><td>0.6631</td><td>0.0096591</td><td>0.0100774</td><td>0.0089092</td><td>649</td><td>706</td><td>9</td><td>7</td><td>8</td><td>8</td><td>10</td><td>8</td><td>9</td><td>6</td><td>6</td><td>1021</td><td>1218</td><td>1294</td><td>1152</td><td>1525</td></tr>
    <tr><td>Levi&#x27;s</td><td>49.38</td><td>25.11</td><td>18282.06</td><td>8881.53</td><td>1555</td><td>380</td><td>170</td><td>226</td><td>779</td><td>19255.96</td><td>9460.87</td><td>0.4858</td><td>0.3091</td><td>0.2859</td><td>0.1453</td><td>0.6721</td><td>0.0067724</td><td>0.0063475</td><td>0.0085782</td><td>1107</td><td>1028</td><td>20</td><td>23</td><td>9</td><td>9</td><td>8</td><td>11</td><td>10</td><td>20</td><td>21</td><td>1691</td><td>1097</td><td>1390</td><td>1318</td><td>1273</td></tr>
    <tr><td>Hurley</td><td>50.65</td><td>26.84</td><td>18145.13</td><td>8556.32</td><td>1546</td><td>361</td><td>149</td><td>223</td><td>813</td><td>19565.08</td><td>9135.89</td><td>0.4715</td><td>0.2922</td><td>0.2729</td><td>0.1442</td><td>0.6925</td><td>0.0067217</td><td>0.0061151</td><td>0.0085285</td><td>1044</td><td>932</td><td>21</td><td>25</td><td>10</td><td>12</td><td>11</td><td>12</td><td>8</td><td>19</td><td>23</td><td>1875</td><td>1197</td><td>1555</td><td>1327</td><td>1091</td></tr>
    <tr><td>Columbia</td><td>69.37</td><td>31.72</td><td>26587.28</td><td>14439.48</td><td>1529</td><td>374</td><td>135</td><td>252</td><td>768</td><td>26842.48</td><td>14585.03</td><td>0.5431</td><td>0.2652</td><td>0.2929</td><td>0.1648</td><td>0.6725</td><td>0.009849</td><td>0.0103197</td><td>0.0084347</td><td>687</td><td>737</td><td>8</td><td>6</td><td>11</td><td>11</td><td>13</td><td>9</td><td>11</td><td>8</td><td>7</td><td>987</td><td>1379</td><td>1340</td><td>1067</td><td>1270</td></tr>
    <tr><td>Dockers</td><td>41.44</td><td>19.27</td><td>14602.39</td><td>7836.27</td><td>1499</td><td>358</td><td>164</td><td>234</td><td>743</td><td>16357.14</td><td>8732.29</td><td>0.5366</td><td>0.3142</td><td>0.283</td><td>0.1561</td><td>0.6748</td><td>0.0054093</td><td>0.0056005</td><td>0.0082692</td><td>1312</td><td>1369</td><td>31</td><td>29</td><td>12</td><td>13</td><td>9</td><td>10</td><td>12</td><td>25</td><td>25</td><td>1079</td><td>1077</td><td>1480</td><td>1167</td><td>1254</td></tr>
    <tr><td>Diesel</td><td>138.24</td><td>68.92</td><td>53774.81</td><td>27000.8</td><td>1466</td><td>378</td><td>143</td><td>213</td><td>732</td><td>49754.6</td><td>24735.41</td><td>0.5021</td><td>0.2745</td><td>0.3017</td><td>0.1453</td><td>0.6595</td><td>0.0199204</td><td>0.0192971</td><td>0.0080872</td><td>205</td><td>184</td><td>1</td><td>2</td><td>13</td><td>10</td><td>12</td><td>13</td><td>13</td><td>1</td><td>2</td><td>1502</td><td>1319</td><td>1221</td><td>1318</td><td>1552</td></tr>
    <tr><td>Wrangler</td><td>42.55</td><td>22.53</td><td>12679.57</td><td>5981.86</td><td>1287</td><td>301</td><td>128</td><td>191</td><td>667</td><td>13499.91</td><td>6413.97</td><td>0.4718</td><td>0.2984</td><td>0.2746</td><td>0.1484</td><td>0.689</td><td>0.004697</td><td>0.0042752</td><td>0.0070997</td><td>1285</td><td>1187</td><td>37</td><td>41</td><td>14</td><td>15</td><td>15</td><td>15</td><td>14</td><td>35</td><td>39</td><td>1871</td><td>1167</td><td>1548</td><td>1267</td><td>1132</td></tr>
    <tr><td>American Apparel</td><td>37.49</td><td>18.04</td><td>10780.0</td><td>5628.61</td><td>1204</td><td>290</td><td>120</td><td>191</td><td>603</td><td>11807.99</td><td>6094.43</td><td>0.5221</td><td>0.2927</td><td>0.2863</td><td>0.1586</td><td>0.6753</td><td>0.0039934</td><td>0.0040227</td><td>0.0066419</td><td>1437</td><td>1442</td><td>47</td><td>46</td><td>15</td><td>16</td><td>16</td><td>15</td><td>15</td><td>46</td><td>43</td><td>1265</td><td>1194</td><td>1389</td><td>1126</td><td>1247</td></tr>
  </tbody>
</table>

</div>

<h3>Top brands by Return Rate</h3>

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
WHERE unit_orders_placed_rank &lt;= 30
ORDER BY
  return_rate_rank ASC
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
    <tr><td>Hanes</td><td>20.0</td><td>9.63</td><td>9350.02</td><td>4878.18</td><td>1966</td><td>473</td><td>225</td><td>275</td><td>993</td><td>10001.01</td><td>5127.51</td><td>0.5217</td><td>0.3223</td><td>0.2797</td><td>0.1399</td><td>0.6774</td><td>0.0034636</td><td>0.0034864</td><td>0.0108455</td><td>2145</td><td>2182</td><td>59</td><td>58</td><td>4</td><td>5</td><td>4</td><td>6</td><td>4</td><td>54</td><td>56</td><td>1270</td><td>1053</td><td>1511</td><td>1469</td><td>1230</td></tr>
    <tr><td>Dockers</td><td>41.44</td><td>19.27</td><td>14602.39</td><td>7836.27</td><td>1499</td><td>358</td><td>164</td><td>234</td><td>743</td><td>16357.14</td><td>8732.29</td><td>0.5366</td><td>0.3142</td><td>0.283</td><td>0.1561</td><td>0.6748</td><td>0.0054093</td><td>0.0056005</td><td>0.0082692</td><td>1312</td><td>1369</td><td>31</td><td>29</td><td>12</td><td>13</td><td>9</td><td>10</td><td>12</td><td>25</td><td>25</td><td>1079</td><td>1077</td><td>1480</td><td>1167</td><td>1254</td></tr>
    <tr><td>Fruit of the Loom</td><td>17.8</td><td>8.71</td><td>3598.46</td><td>1822.47</td><td>858</td><td>204</td><td>93</td><td>137</td><td>424</td><td>4113.8</td><td>2115.63</td><td>0.5065</td><td>0.3131</td><td>0.2829</td><td>0.1597</td><td>0.6752</td><td>0.001333</td><td>0.0013025</td><td>0.0047332</td><td>2284</td><td>2262</td><td>145</td><td>152</td><td>30</td><td>33</td><td>29</td><td>28</td><td>29</td><td>127</td><td>132</td><td>1465</td><td>1078</td><td>1482</td><td>1116</td><td>1249</td></tr>
    <tr><td>Levi&#x27;s</td><td>49.38</td><td>25.11</td><td>18282.06</td><td>8881.53</td><td>1555</td><td>380</td><td>170</td><td>226</td><td>779</td><td>19255.96</td><td>9460.87</td><td>0.4858</td><td>0.3091</td><td>0.2859</td><td>0.1453</td><td>0.6721</td><td>0.0067724</td><td>0.0063475</td><td>0.0085782</td><td>1107</td><td>1028</td><td>20</td><td>23</td><td>9</td><td>9</td><td>8</td><td>11</td><td>10</td><td>20</td><td>21</td><td>1691</td><td>1097</td><td>1390</td><td>1318</td><td>1273</td></tr>
    <tr><td>Speedo</td><td>51.0</td><td>24.98</td><td>15357.4</td><td>7698.19</td><td>1176</td><td>302</td><td>135</td><td>174</td><td>565</td><td>15950.94</td><td>8214.56</td><td>0.5013</td><td>0.3089</td><td>0.3014</td><td>0.148</td><td>0.6517</td><td>0.005689</td><td>0.0055018</td><td>0.0064874</td><td>1034</td><td>1038</td><td>28</td><td>31</td><td>16</td><td>14</td><td>13</td><td>20</td><td>17</td><td>26</td><td>28</td><td>1514</td><td>1099</td><td>1223</td><td>1287</td><td>1606</td></tr>
    <tr><td>HUGO BOSS</td><td>41.95</td><td>18.49</td><td>9749.08</td><td>5443.79</td><td>928</td><td>235</td><td>102</td><td>130</td><td>461</td><td>10857.69</td><td>6091.93</td><td>0.5584</td><td>0.3027</td><td>0.2945</td><td>0.1401</td><td>0.6624</td><td>0.0036115</td><td>0.0038906</td><td>0.0051193</td><td>1300</td><td>1413</td><td>54</td><td>53</td><td>26</td><td>26</td><td>22</td><td>31</td><td>25</td><td>48</td><td>44</td><td>723</td><td>1124</td><td>1313</td><td>1468</td><td>1530</td></tr>
    <tr><td>Quiksilver</td><td>57.01</td><td>30.91</td><td>27609.19</td><td>12579.68</td><td>1873</td><td>471</td><td>202</td><td>297</td><td>903</td><td>26410.17</td><td>12067.7</td><td>0.4556</td><td>0.3001</td><td>0.2989</td><td>0.1586</td><td>0.6572</td><td>0.0102276</td><td>0.0089905</td><td>0.0103324</td><td>903</td><td>764</td><td>7</td><td>14</td><td>6</td><td>6</td><td>5</td><td>4</td><td>7</td><td>10</td><td>14</td><td>2066</td><td>1129</td><td>1275</td><td>1126</td><td>1563</td></tr>
    <tr><td>Dickies</td><td>40.19</td><td>19.51</td><td>11280.31</td><td>5811.09</td><td>1139</td><td>276</td><td>118</td><td>187</td><td>558</td><td>11942.83</td><td>6160.0</td><td>0.5152</td><td>0.2995</td><td>0.2899</td><td>0.1642</td><td>0.6691</td><td>0.0041787</td><td>0.0041531</td><td>0.0062833</td><td>1331</td><td>1360</td><td>44</td><td>42</td><td>17</td><td>18</td><td>17</td><td>17</td><td>18</td><td>45</td><td>42</td><td>1355</td><td>1163</td><td>1362</td><td>1073</td><td>1284</td></tr>
    <tr><td>Wrangler</td><td>42.55</td><td>22.53</td><td>12679.57</td><td>5981.86</td><td>1287</td><td>301</td><td>128</td><td>191</td><td>667</td><td>13499.91</td><td>6413.97</td><td>0.4718</td><td>0.2984</td><td>0.2746</td><td>0.1484</td><td>0.689</td><td>0.004697</td><td>0.0042752</td><td>0.0070997</td><td>1285</td><td>1187</td><td>37</td><td>41</td><td>14</td><td>15</td><td>15</td><td>15</td><td>14</td><td>35</td><td>39</td><td>1871</td><td>1167</td><td>1548</td><td>1267</td><td>1132</td></tr>
    <tr><td>7 For All Mankind</td><td>155.67</td><td>81.33</td><td>39429.55</td><td>18708.21</td><td>1086</td><td>254</td><td>108</td><td>179</td><td>545</td><td>44113.73</td><td>21179.32</td><td>0.4745</td><td>0.2983</td><td>0.28</td><td>0.1648</td><td>0.6821</td><td>0.0146063</td><td>0.0133705</td><td>0.0059909</td><td>156</td><td>123</td><td>5</td><td>5</td><td>20</td><td>24</td><td>19</td><td>19</td><td>20</td><td>3</td><td>4</td><td>1826</td><td>1168</td><td>1503</td><td>1067</td><td>1192</td></tr>
    <tr><td>Allegra K</td><td>14.35</td><td>6.76</td><td>20908.12</td><td>11061.0</td><td>6057</td><td>1467</td><td>610</td><td>943</td><td>3037</td><td>22396.3</td><td>11874.9</td><td>0.529</td><td>0.2937</td><td>0.2869</td><td>0.1557</td><td>0.6743</td><td>0.0077452</td><td>0.0079052</td><td>0.0334135</td><td>2442</td><td>2434</td><td>16</td><td>16</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>15</td><td>15</td><td>1172</td><td>1190</td><td>1384</td><td>1170</td><td>1255</td></tr>
    <tr><td>FineBrandShop</td><td>21.28</td><td>9.66</td><td>5198.85</td><td>2814.5</td><td>990</td><td>255</td><td>106</td><td>156</td><td>473</td><td>5944.2</td><td>3265.8</td><td>0.5414</td><td>0.2936</td><td>0.3058</td><td>0.1576</td><td>0.6497</td><td>0.0019259</td><td>0.0020115</td><td>0.0054613</td><td>2119</td><td>2178</td><td>101</td><td>97</td><td>24</td><td>23</td><td>20</td><td>23</td><td>23</td><td>87</td><td>81</td><td>1007</td><td>1191</td><td>1191</td><td>1148</td><td>1622</td></tr>
    <tr><td>American Apparel</td><td>37.49</td><td>18.04</td><td>10780.0</td><td>5628.61</td><td>1204</td><td>290</td><td>120</td><td>191</td><td>603</td><td>11807.99</td><td>6094.43</td><td>0.5221</td><td>0.2927</td><td>0.2863</td><td>0.1586</td><td>0.6753</td><td>0.0039934</td><td>0.0040227</td><td>0.0066419</td><td>1437</td><td>1442</td><td>47</td><td>46</td><td>15</td><td>16</td><td>16</td><td>15</td><td>15</td><td>46</td><td>43</td><td>1265</td><td>1194</td><td>1389</td><td>1126</td><td>1247</td></tr>
    <tr><td>Hurley</td><td>50.65</td><td>26.84</td><td>18145.13</td><td>8556.32</td><td>1546</td><td>361</td><td>149</td><td>223</td><td>813</td><td>19565.08</td><td>9135.89</td><td>0.4715</td><td>0.2922</td><td>0.2729</td><td>0.1442</td><td>0.6925</td><td>0.0067217</td><td>0.0061151</td><td>0.0085285</td><td>1044</td><td>932</td><td>21</td><td>25</td><td>10</td><td>12</td><td>11</td><td>12</td><td>8</td><td>19</td><td>23</td><td>1875</td><td>1197</td><td>1555</td><td>1327</td><td>1091</td></tr>
    <tr><td>Nautica</td><td>41.7</td><td>20.24</td><td>18412.72</td><td>9492.15</td><td>1827</td><td>451</td><td>185</td><td>266</td><td>925</td><td>18833.69</td><td>9728.4</td><td>0.5155</td><td>0.2909</td><td>0.2889</td><td>0.1456</td><td>0.6722</td><td>0.0068208</td><td>0.0067839</td><td>0.0100787</td><td>1306</td><td>1314</td><td>19</td><td>20</td><td>7</td><td>7</td><td>6</td><td>7</td><td>6</td><td>22</td><td>19</td><td>1351</td><td>1204</td><td>1371</td><td>1315</td><td>1272</td></tr>
  </tbody>
</table>

</div>

<h3>Top brands by Units Returned</h3>

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
  units_returned_rank ASC
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
    <tr><td>Allegra K</td><td>14.35</td><td>6.76</td><td>20908.12</td><td>11061.0</td><td>6057</td><td>1467</td><td>610</td><td>943</td><td>3037</td><td>22396.3</td><td>11874.9</td><td>0.529</td><td>0.2937</td><td>0.2869</td><td>0.1557</td><td>0.6743</td><td>0.0077452</td><td>0.0079052</td><td>0.0334135</td><td>2442</td><td>2434</td><td>16</td><td>16</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>15</td><td>15</td><td>1172</td><td>1190</td><td>1384</td><td>1170</td><td>1255</td></tr>
    <tr><td>Calvin Klein</td><td>62.49</td><td>29.31</td><td>53041.76</td><td>28267.04</td><td>3180</td><td>820</td><td>322</td><td>471</td><td>1567</td><td>48698.1</td><td>25795.42</td><td>0.5329</td><td>0.282</td><td>0.3027</td><td>0.1481</td><td>0.6565</td><td>0.0196488</td><td>0.0202021</td><td>0.0175425</td><td>805</td><td>836</td><td>2</td><td>1</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>1</td><td>1128</td><td>1282</td><td>1212</td><td>1270</td><td>1568</td></tr>
    <tr><td>Carhartt</td><td>68.41</td><td>32.02</td><td>44947.96</td><td>23945.23</td><td>2509</td><td>663</td><td>251</td><td>366</td><td>1229</td><td>41134.22</td><td>22022.28</td><td>0.5327</td><td>0.2746</td><td>0.3094</td><td>0.1459</td><td>0.6496</td><td>0.0166506</td><td>0.0171134</td><td>0.0138409</td><td>703</td><td>724</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>5</td><td>3</td><td>1132</td><td>1317</td><td>1155</td><td>1311</td><td>1623</td></tr>
    <tr><td>Hanes</td><td>20.0</td><td>9.63</td><td>9350.02</td><td>4878.18</td><td>1966</td><td>473</td><td>225</td><td>275</td><td>993</td><td>10001.01</td><td>5127.51</td><td>0.5217</td><td>0.3223</td><td>0.2797</td><td>0.1399</td><td>0.6774</td><td>0.0034636</td><td>0.0034864</td><td>0.0108455</td><td>2145</td><td>2182</td><td>59</td><td>58</td><td>4</td><td>5</td><td>4</td><td>6</td><td>4</td><td>54</td><td>56</td><td>1270</td><td>1053</td><td>1511</td><td>1469</td><td>1230</td></tr>
    <tr><td>Quiksilver</td><td>57.01</td><td>30.91</td><td>27609.19</td><td>12579.68</td><td>1873</td><td>471</td><td>202</td><td>297</td><td>903</td><td>26410.17</td><td>12067.7</td><td>0.4556</td><td>0.3001</td><td>0.2989</td><td>0.1586</td><td>0.6572</td><td>0.0102276</td><td>0.0089905</td><td>0.0103324</td><td>903</td><td>764</td><td>7</td><td>14</td><td>6</td><td>6</td><td>5</td><td>4</td><td>7</td><td>10</td><td>14</td><td>2066</td><td>1129</td><td>1275</td><td>1126</td><td>1563</td></tr>
    <tr><td>Nautica</td><td>41.7</td><td>20.24</td><td>18412.72</td><td>9492.15</td><td>1827</td><td>451</td><td>185</td><td>266</td><td>925</td><td>18833.69</td><td>9728.4</td><td>0.5155</td><td>0.2909</td><td>0.2889</td><td>0.1456</td><td>0.6722</td><td>0.0068208</td><td>0.0067839</td><td>0.0100787</td><td>1306</td><td>1314</td><td>19</td><td>20</td><td>7</td><td>7</td><td>6</td><td>7</td><td>6</td><td>22</td><td>19</td><td>1351</td><td>1204</td><td>1371</td><td>1315</td><td>1272</td></tr>
    <tr><td>Volcom</td><td>58.67</td><td>29.91</td><td>28804.39</td><td>14059.0</td><td>1893</td><td>482</td><td>182</td><td>294</td><td>935</td><td>26458.99</td><td>12887.05</td><td>0.4881</td><td>0.2741</td><td>0.3014</td><td>0.1553</td><td>0.6598</td><td>0.0106703</td><td>0.0100478</td><td>0.0104428</td><td>877</td><td>805</td><td>6</td><td>8</td><td>5</td><td>4</td><td>7</td><td>5</td><td>5</td><td>9</td><td>10</td><td>1663</td><td>1320</td><td>1223</td><td>1174</td><td>1547</td></tr>
    <tr><td>Levi&#x27;s</td><td>49.38</td><td>25.11</td><td>18282.06</td><td>8881.53</td><td>1555</td><td>380</td><td>170</td><td>226</td><td>779</td><td>19255.96</td><td>9460.87</td><td>0.4858</td><td>0.3091</td><td>0.2859</td><td>0.1453</td><td>0.6721</td><td>0.0067724</td><td>0.0063475</td><td>0.0085782</td><td>1107</td><td>1028</td><td>20</td><td>23</td><td>9</td><td>9</td><td>8</td><td>11</td><td>10</td><td>20</td><td>21</td><td>1691</td><td>1097</td><td>1390</td><td>1318</td><td>1273</td></tr>
    <tr><td>Dockers</td><td>41.44</td><td>19.27</td><td>14602.39</td><td>7836.27</td><td>1499</td><td>358</td><td>164</td><td>234</td><td>743</td><td>16357.14</td><td>8732.29</td><td>0.5366</td><td>0.3142</td><td>0.283</td><td>0.1561</td><td>0.6748</td><td>0.0054093</td><td>0.0056005</td><td>0.0082692</td><td>1312</td><td>1369</td><td>31</td><td>29</td><td>12</td><td>13</td><td>9</td><td>10</td><td>12</td><td>25</td><td>25</td><td>1079</td><td>1077</td><td>1480</td><td>1167</td><td>1254</td></tr>
    <tr><td>Tommy Hilfiger</td><td>71.62</td><td>32.46</td><td>26074.49</td><td>14100.38</td><td>1615</td><td>404</td><td>162</td><td>254</td><td>795</td><td>29731.26</td><td>16179.42</td><td>0.5408</td><td>0.2862</td><td>0.2968</td><td>0.1573</td><td>0.6631</td><td>0.0096591</td><td>0.0100774</td><td>0.0089092</td><td>649</td><td>706</td><td>9</td><td>7</td><td>8</td><td>8</td><td>10</td><td>8</td><td>9</td><td>6</td><td>6</td><td>1021</td><td>1218</td><td>1294</td><td>1152</td><td>1525</td></tr>
    <tr><td>Hurley</td><td>50.65</td><td>26.84</td><td>18145.13</td><td>8556.32</td><td>1546</td><td>361</td><td>149</td><td>223</td><td>813</td><td>19565.08</td><td>9135.89</td><td>0.4715</td><td>0.2922</td><td>0.2729</td><td>0.1442</td><td>0.6925</td><td>0.0067217</td><td>0.0061151</td><td>0.0085285</td><td>1044</td><td>932</td><td>21</td><td>25</td><td>10</td><td>12</td><td>11</td><td>12</td><td>8</td><td>19</td><td>23</td><td>1875</td><td>1197</td><td>1555</td><td>1327</td><td>1091</td></tr>
    <tr><td>Diesel</td><td>138.24</td><td>68.92</td><td>53774.81</td><td>27000.8</td><td>1466</td><td>378</td><td>143</td><td>213</td><td>732</td><td>49754.6</td><td>24735.41</td><td>0.5021</td><td>0.2745</td><td>0.3017</td><td>0.1453</td><td>0.6595</td><td>0.0199204</td><td>0.0192971</td><td>0.0080872</td><td>205</td><td>184</td><td>1</td><td>2</td><td>13</td><td>10</td><td>12</td><td>13</td><td>13</td><td>1</td><td>2</td><td>1502</td><td>1319</td><td>1221</td><td>1318</td><td>1552</td></tr>
    <tr><td>Columbia</td><td>69.37</td><td>31.72</td><td>26587.28</td><td>14439.48</td><td>1529</td><td>374</td><td>135</td><td>252</td><td>768</td><td>26842.48</td><td>14585.03</td><td>0.5431</td><td>0.2652</td><td>0.2929</td><td>0.1648</td><td>0.6725</td><td>0.009849</td><td>0.0103197</td><td>0.0084347</td><td>687</td><td>737</td><td>8</td><td>6</td><td>11</td><td>11</td><td>13</td><td>9</td><td>11</td><td>8</td><td>7</td><td>987</td><td>1379</td><td>1340</td><td>1067</td><td>1270</td></tr>
    <tr><td>Speedo</td><td>51.0</td><td>24.98</td><td>15357.4</td><td>7698.19</td><td>1176</td><td>302</td><td>135</td><td>174</td><td>565</td><td>15950.94</td><td>8214.56</td><td>0.5013</td><td>0.3089</td><td>0.3014</td><td>0.148</td><td>0.6517</td><td>0.005689</td><td>0.0055018</td><td>0.0064874</td><td>1034</td><td>1038</td><td>28</td><td>31</td><td>16</td><td>14</td><td>13</td><td>20</td><td>17</td><td>26</td><td>28</td><td>1514</td><td>1099</td><td>1223</td><td>1287</td><td>1606</td></tr>
    <tr><td>Wrangler</td><td>42.55</td><td>22.53</td><td>12679.57</td><td>5981.86</td><td>1287</td><td>301</td><td>128</td><td>191</td><td>667</td><td>13499.91</td><td>6413.97</td><td>0.4718</td><td>0.2984</td><td>0.2746</td><td>0.1484</td><td>0.689</td><td>0.004697</td><td>0.0042752</td><td>0.0070997</td><td>1285</td><td>1187</td><td>37</td><td>41</td><td>14</td><td>15</td><td>15</td><td>15</td><td>14</td><td>35</td><td>39</td><td>1871</td><td>1167</td><td>1548</td><td>1267</td><td>1132</td></tr>
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

<h3>Top brands by Lost Profit</h3>

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
  lost_profit_rank ASC
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
    <tr><td>Calvin Klein</td><td>62.49</td><td>29.31</td><td>53041.76</td><td>28267.04</td><td>3180</td><td>820</td><td>322</td><td>471</td><td>1567</td><td>48698.1</td><td>25795.42</td><td>0.5329</td><td>0.282</td><td>0.3027</td><td>0.1481</td><td>0.6565</td><td>0.0196488</td><td>0.0202021</td><td>0.0175425</td><td>805</td><td>836</td><td>2</td><td>1</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>1</td><td>1128</td><td>1282</td><td>1212</td><td>1270</td><td>1568</td></tr>
    <tr><td>Diesel</td><td>138.24</td><td>68.92</td><td>53774.81</td><td>27000.8</td><td>1466</td><td>378</td><td>143</td><td>213</td><td>732</td><td>49754.6</td><td>24735.41</td><td>0.5021</td><td>0.2745</td><td>0.3017</td><td>0.1453</td><td>0.6595</td><td>0.0199204</td><td>0.0192971</td><td>0.0080872</td><td>205</td><td>184</td><td>1</td><td>2</td><td>13</td><td>10</td><td>12</td><td>13</td><td>13</td><td>1</td><td>2</td><td>1502</td><td>1319</td><td>1221</td><td>1318</td><td>1552</td></tr>
    <tr><td>Carhartt</td><td>68.41</td><td>32.02</td><td>44947.96</td><td>23945.23</td><td>2509</td><td>663</td><td>251</td><td>366</td><td>1229</td><td>41134.22</td><td>22022.28</td><td>0.5327</td><td>0.2746</td><td>0.3094</td><td>0.1459</td><td>0.6496</td><td>0.0166506</td><td>0.0171134</td><td>0.0138409</td><td>703</td><td>724</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>5</td><td>3</td><td>1132</td><td>1317</td><td>1155</td><td>1311</td><td>1623</td></tr>
    <tr><td>7 For All Mankind</td><td>155.67</td><td>81.33</td><td>39429.55</td><td>18708.21</td><td>1086</td><td>254</td><td>108</td><td>179</td><td>545</td><td>44113.73</td><td>21179.32</td><td>0.4745</td><td>0.2983</td><td>0.28</td><td>0.1648</td><td>0.6821</td><td>0.0146063</td><td>0.0133705</td><td>0.0059909</td><td>156</td><td>123</td><td>5</td><td>5</td><td>20</td><td>24</td><td>19</td><td>19</td><td>20</td><td>3</td><td>4</td><td>1826</td><td>1168</td><td>1503</td><td>1067</td><td>1192</td></tr>
    <tr><td>True Religion</td><td>196.17</td><td>101.7</td><td>43598.78</td><td>21127.8</td><td>879</td><td>225</td><td>84</td><td>146</td><td>424</td><td>43136.54</td><td>20619.76</td><td>0.4846</td><td>0.2718</td><td>0.307</td><td>0.1661</td><td>0.6533</td><td>0.0161508</td><td>0.0150998</td><td>0.004849</td><td>91</td><td>64</td><td>4</td><td>4</td><td>27</td><td>28</td><td>33</td><td>25</td><td>29</td><td>4</td><td>5</td><td>1705</td><td>1347</td><td>1186</td><td>1064</td><td>1592</td></tr>
    <tr><td>Tommy Hilfiger</td><td>71.62</td><td>32.46</td><td>26074.49</td><td>14100.38</td><td>1615</td><td>404</td><td>162</td><td>254</td><td>795</td><td>29731.26</td><td>16179.42</td><td>0.5408</td><td>0.2862</td><td>0.2968</td><td>0.1573</td><td>0.6631</td><td>0.0096591</td><td>0.0100774</td><td>0.0089092</td><td>649</td><td>706</td><td>9</td><td>7</td><td>8</td><td>8</td><td>10</td><td>8</td><td>9</td><td>6</td><td>6</td><td>1021</td><td>1218</td><td>1294</td><td>1152</td><td>1525</td></tr>
    <tr><td>Columbia</td><td>69.37</td><td>31.72</td><td>26587.28</td><td>14439.48</td><td>1529</td><td>374</td><td>135</td><td>252</td><td>768</td><td>26842.48</td><td>14585.03</td><td>0.5431</td><td>0.2652</td><td>0.2929</td><td>0.1648</td><td>0.6725</td><td>0.009849</td><td>0.0103197</td><td>0.0084347</td><td>687</td><td>737</td><td>8</td><td>6</td><td>11</td><td>11</td><td>13</td><td>9</td><td>11</td><td>8</td><td>7</td><td>987</td><td>1379</td><td>1340</td><td>1067</td><td>1270</td></tr>
    <tr><td>Ray-Ban</td><td>118.89</td><td>50.08</td><td>23852.78</td><td>13833.41</td><td>798</td><td>206</td><td>78</td><td>131</td><td>383</td><td>25134.08</td><td>14434.77</td><td>0.5799</td><td>0.2746</td><td>0.3088</td><td>0.1642</td><td>0.6503</td><td>0.008836</td><td>0.0098866</td><td>0.0044022</td><td>278</td><td>346</td><td>15</td><td>9</td><td>34</td><td>32</td><td>35</td><td>30</td><td>37</td><td>11</td><td>8</td><td>437</td><td>1317</td><td>1160</td><td>1073</td><td>1612</td></tr>
    <tr><td>Joe&#x27;s Jeans</td><td>152.81</td><td>80.23</td><td>25134.81</td><td>11891.96</td><td>697</td><td>169</td><td>76</td><td>99</td><td>353</td><td>27326.02</td><td>13164.83</td><td>0.4731</td><td>0.3102</td><td>0.2826</td><td>0.142</td><td>0.6762</td><td>0.009311</td><td>0.008499</td><td>0.003845</td><td>163</td><td>133</td><td>12</td><td>15</td><td>41</td><td>42</td><td>38</td><td>47</td><td>41</td><td>7</td><td>9</td><td>1850</td><td>1094</td><td>1486</td><td>1448</td><td>1239</td></tr>
    <tr><td>Volcom</td><td>58.67</td><td>29.91</td><td>28804.39</td><td>14059.0</td><td>1893</td><td>482</td><td>182</td><td>294</td><td>935</td><td>26458.99</td><td>12887.05</td><td>0.4881</td><td>0.2741</td><td>0.3014</td><td>0.1553</td><td>0.6598</td><td>0.0106703</td><td>0.0100478</td><td>0.0104428</td><td>877</td><td>805</td><td>6</td><td>8</td><td>5</td><td>4</td><td>7</td><td>5</td><td>5</td><td>9</td><td>10</td><td>1663</td><td>1320</td><td>1223</td><td>1174</td><td>1547</td></tr>
    <tr><td>Canada Goose</td><td>577.82</td><td>249.06</td><td>12909.93</td><td>7257.7</td><td>115</td><td>22</td><td>15</td><td>21</td><td>57</td><td>22479.93</td><td>12816.81</td><td>0.5622</td><td>0.4054</td><td>0.234</td><td>0.1826</td><td>0.7215</td><td>0.0047824</td><td>0.005187</td><td>0.0006344</td><td>4</td><td>5</td><td>36</td><td>34</td><td>337</td><td>412</td><td>261</td><td>265</td><td>329</td><td>14</td><td>11</td><td>672</td><td>572</td><td>1980</td><td>814</td><td>871</td></tr>
    <tr><td>Oakley</td><td>110.41</td><td>49.26</td><td>24423.2</td><td>13410.52</td><td>866</td><td>225</td><td>90</td><td>118</td><td>433</td><td>23073.48</td><td>12801.68</td><td>0.5491</td><td>0.2857</td><td>0.3008</td><td>0.1363</td><td>0.6581</td><td>0.0090474</td><td>0.0095843</td><td>0.0047773</td><td>316</td><td>355</td><td>14</td><td>13</td><td>29</td><td>28</td><td>30</td><td>33</td><td>27</td><td>12</td><td>12</td><td>896</td><td>1219</td><td>1227</td><td>1522</td><td>1556</td></tr>
    <tr><td>Arc&#x27;teryx</td><td>323.7</td><td>146.18</td><td>18141.7</td><td>9908.14</td><td>271</td><td>56</td><td>22</td><td>41</td><td>152</td><td>22880.85</td><td>12500.89</td><td>0.5462</td><td>0.2821</td><td>0.2435</td><td>0.1513</td><td>0.7308</td><td>0.0067204</td><td>0.0070812</td><td>0.001495</td><td>22</td><td>20</td><td>22</td><td>19</td><td>132</td><td>169</td><td>161</td><td>132</td><td>118</td><td>13</td><td>13</td><td>943</td><td>1281</td><td>1928</td><td>1234</td><td>808</td></tr>
    <tr><td>Quiksilver</td><td>57.01</td><td>30.91</td><td>27609.19</td><td>12579.68</td><td>1873</td><td>471</td><td>202</td><td>297</td><td>903</td><td>26410.17</td><td>12067.7</td><td>0.4556</td><td>0.3001</td><td>0.2989</td><td>0.1586</td><td>0.6572</td><td>0.0102276</td><td>0.0089905</td><td>0.0103324</td><td>903</td><td>764</td><td>7</td><td>14</td><td>6</td><td>6</td><td>5</td><td>4</td><td>7</td><td>10</td><td>14</td><td>2066</td><td>1129</td><td>1275</td><td>1126</td><td>1563</td></tr>
    <tr><td>Allegra K</td><td>14.35</td><td>6.76</td><td>20908.12</td><td>11061.0</td><td>6057</td><td>1467</td><td>610</td><td>943</td><td>3037</td><td>22396.3</td><td>11874.9</td><td>0.529</td><td>0.2937</td><td>0.2869</td><td>0.1557</td><td>0.6743</td><td>0.0077452</td><td>0.0079052</td><td>0.0334135</td><td>2442</td><td>2434</td><td>16</td><td>16</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>15</td><td>15</td><td>1172</td><td>1190</td><td>1384</td><td>1170</td><td>1255</td></tr>
  </tbody>
</table>

</div>

<h3>Analytical Insights & Business Recommendations</h3>

<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p><strong>Revenue vs. Profit Leadership Diverges:</strong> Diesel leads all brands in revenue ($53,774.81) but drops to #2 in profit ($27,000.80) due to a relatively low profit margin of 50.2%. Calvin Klein overtakes Diesel in profit ($28,267.04) despite ranking #2 in revenue, thanks to a stronger 53.3% margin. This divergence reveals that Diesel's higher average sale price ($138.24) comes with proportionally higher product costs ($68.92), compressing margins.</p>

<p>Recommendation: For high-revenue, lower-margin brands like Diesel, negotiate better supplier pricing given the volume leverage — 1,466 units ordered gives significant bargaining power. Even a 2–3% cost reduction on Diesel products would yield substantial additional profit given the revenue scale. Alternatively, since Diesel already commands premium pricing, explore whether modest price increases on best-selling Diesel items would be absorbed by demand without significant volume loss.</p>

<p><strong>The North Face: Premium Pricing Power:</strong> The North Face ranks #11 in revenue ($25,174.88) but achieves this with only 233 unit orders — the fewest among the top 15 brands. Its average sale price of $440.81 is the highest by a wide margin (the next highest is True Religion at $196.17). This means The North Face extracts over 2x more revenue per unit than any comparable brand.</p>

<p>With a 54.5% profit margin and only 20 returns out of 81 completed/returned units (24.7% return rate — the lowest among top brands), The North Face represents the most efficient revenue-to-order ratio in the dataset.</p>

<p>Recommendation: Allocate increased internal inventory space and priority fulfillment to The North Face products. Their per-unit contribution is unmatched, and with the lowest return rate among top brands, each sale is highly likely to convert to retained revenue. Ensure stockouts never occur on The North Face items — lost sales on $440+ average items represent outsized opportunity cost.</p>

<p><strong>Volume-Driven Brands Need Margin Attention:</strong> Allegra K dominates unit orders (6,057 — nearly 2x the next brand) but ranks only #16 in revenue ($20,908.12) and has the lowest average sale price ($14.35) among any significant brand. Its profit margin of 52.9% is decent, but the absolute profit per unit is tiny due to the low price point.</p>

<p>Similarly, Hanes (1,966 orders, $20 avg price) and Nautica (1,827 orders, $41.70 avg price) move high volumes but contribute modestly to total profit.</p>

<p>Recommendation: For mass-market brands like Allegra K and Hanes, the sheer volume makes them candidates for package deals and bulk purchasing incentives. Sell packs of 3–5 items at a slight per-unit discount to streamline delivery and processing costs while incentivizing larger basket sizes. A customer buying 5 Allegra K items in one shipment is more profitable than 5 separate single-item orders due to reduced per-order fulfillment costs.</p>

<p><strong>Return Rate Patterns by Brand:</strong> Return rates among the top 30 brands by volume are tightly clustered (27–32%), suggesting returns are somewhat systematic across the business rather than brand-specific. Hanes has the highest return rate at 32.2%, followed by Dockers (31.4%) and Fruit of the Loom (31.3%). These are all mass-market, lower-price basics where sizing uncertainty and low switching costs likely drive returns.</p>

<p>At the other end, Carhartt (27.5%), The North Face (24.7%), and Columbia (26.5%) have the lowest return rates among volume brands, suggesting that outdoor/workwear brands may benefit from more deliberate purchase intent or better product-description accuracy.</p>

<p>Recommendation: Focus return-reduction efforts on the high-return basics brands (Hanes, Dockers, Fruit of the Loom) through better sizing guides and product imagery. Even a 2-point reduction in return rate across Hanes' 1,966 orders would recover approximately 39 additional completed sales.</p>

<p><strong>Lost Revenue Leaders Mirror Revenue Leaders:</strong> The top brands by lost revenue are the same as the top brands by revenue — Diesel ($49,754.60 lost), Calvin Klein ($48,698.10), Carhartt ($41,134.22). This is expected since lost revenue scales with order volume and average price. However, the ratio of lost revenue to actual revenue is striking: Diesel loses $49K vs. earning $53K, meaning nearly half of all potential Diesel revenue evaporates through returns and cancellations.</p>

<p>Recommendation: For brands where lost revenue approaches or exceeds earned revenue, the cost of returns processing, reverse shipping, and restocking is a significant hidden expense. Investigate whether specific Diesel or Calvin Klein product lines disproportionately drive the returns, and target those SKUs for quality review or enhanced product descriptions rather than applying broad brand-level interventions.</p>

<p><strong>Canada Goose: High Value, High Risk:</strong> Canada Goose stands out in the lost revenue/profit tables despite ranking #36 in revenue and #337 in unit orders. With only 115 orders placed, it generates $12,909.93 in revenue but $22,479.93 in lost revenue — nearly 2x what it actually earns. Its 40.5% return rate is the highest among brands appearing in the top 15 by lost profit.</p>

<p>Recommendation: Given Canada Goose's extremely high price point ($577.82 avg) and disproportionate loss ratio, this brand warrants a targeted investigation. With only 22 completed sales out of 115 orders, something systemic is driving cancellations and returns — possibly shipping delays on premium items, customer sticker shock after purchase, or quality/authenticity concerns. Consider whether the brand partnership is net-positive after accounting for return-processing costs on $500+ items.</p>

<p><strong>High-Margin Brand Leaders:</strong> Among the top 30 revenue brands, Ray-Ban leads in profit margin at 58.0%, followed by Paul Fredrick (57.1%), Jones New York (55.0%), and Oakley (54.9%). These brands share a common profile: moderately high average prices ($100–$150) with well-controlled product costs.</p>

<p>Recommendation: Increase advertising and promotional spend for high-margin brands like Ray-Ban and Oakley, especially targeting their best-selling products. A $1 increase in demand for a Ray-Ban item yields $0.58 in profit vs. $0.47 for a Quiksilver item. Strategically advertising Ray-Ban and Oakley — particularly to customer segments in regions where accessory demand is high — would disproportionately grow profit relative to spend.</p>

</div>

</details>
<details>
  <summary><strong>Bottom Brands</strong></summary>

  <div style="margin-top: 12px;"></div>

<h3>Bottom brands by Lost Revenue</h3>

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
  lost_revenue_rank DESC
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
    <tr><td>Nike</td><td>80.59</td><td>40.35</td><td>16424.08</td><td>8174.99</td><td>520</td><td>125</td><td>44</td><td>76</td><td>275</td><td>7304.66</td><td>3876.47</td><td>0.4977</td><td>0.2604</td><td>0.2815</td><td>0.1462</td><td>0.6875</td><td>0.0061025</td><td>0.0058633</td><td>0.0028694</td><td>531</td><td>487</td><td>25</td><td>28</td><td>55</td><td>56</td><td>73</td><td>63</td><td>50</td><td>76</td><td>73</td><td>1534</td><td>1384</td><td>1460</td><td>1321</td><td>1169</td></tr>
    <tr><td>Alpha Industries</td><td>204.86</td><td>92.63</td><td>13163.17</td><td>7202.15</td><td>188</td><td>58</td><td>12</td><td>31</td><td>87</td><td>8183.49</td><td>4536.63</td><td>0.5471</td><td>0.1714</td><td>0.3694</td><td>0.1649</td><td>0.6</td><td>0.0048909</td><td>0.0051655</td><td>0.0010374</td><td>80</td><td>85</td><td>38</td><td>34</td><td>200</td><td>157</td><td>314</td><td>174</td><td>216</td><td>66</td><td>62</td><td>869</td><td>1853</td><td>603</td><td>1076</td><td>1994</td></tr>
    <tr><td>Champion</td><td>35.82</td><td>16.19</td><td>10673.83</td><td>5891.72</td><td>1124</td><td>304</td><td>111</td><td>152</td><td>557</td><td>9239.17</td><td>5060.81</td><td>0.552</td><td>0.2675</td><td>0.3128</td><td>0.1352</td><td>0.6469</td><td>0.0039659</td><td>0.0042257</td><td>0.0062023</td><td>1481</td><td>1583</td><td>50</td><td>47</td><td>18</td><td>14</td><td>18</td><td>23</td><td>19</td><td>59</td><td>56</td><td>805</td><td>1350</td><td>1091</td><td>1520</td><td>1693</td></tr>
    <tr><td>Hudson</td><td>175.32</td><td>92.88</td><td>10759.54</td><td>5042.67</td><td>238</td><td>59</td><td>22</td><td>36</td><td>121</td><td>9975.18</td><td>4637.96</td><td>0.4687</td><td>0.2716</td><td>0.2921</td><td>0.1513</td><td>0.6722</td><td>0.0039978</td><td>0.0036167</td><td>0.0013133</td><td>124</td><td>81</td><td>49</td><td>57</td><td>147</td><td>155</td><td>163</td><td>147</td><td>147</td><td>53</td><td>61</td><td>1890</td><td>1334</td><td>1311</td><td>1241</td><td>1291</td></tr>
    <tr><td>Sutton Studio</td><td>100.0</td><td>44.04</td><td>11113.33</td><td>6103.95</td><td>428</td><td>115</td><td>54</td><td>56</td><td>203</td><td>10428.99</td><td>5790.5</td><td>0.5492</td><td>0.3195</td><td>0.3091</td><td>0.1308</td><td>0.6384</td><td>0.0041292</td><td>0.0043779</td><td>0.0023617</td><td>355</td><td>419</td><td>48</td><td>46</td><td>74</td><td>67</td><td>56</td><td>91</td><td>77</td><td>49</td><td>46</td><td>849</td><td>1051</td><td>1126</td><td>1591</td><td>1758</td></tr>
    <tr><td>Haggar</td><td>51.76</td><td>23.14</td><td>12529.07</td><td>6973.15</td><td>868</td><td>228</td><td>85</td><td>115</td><td>440</td><td>10540.29</td><td>5879.88</td><td>0.5566</td><td>0.2716</td><td>0.3028</td><td>0.1325</td><td>0.6587</td><td>0.0046553</td><td>0.0050013</td><td>0.0047897</td><td>1016</td><td>1147</td><td>42</td><td>36</td><td>29</td><td>28</td><td>34</td><td>36</td><td>28</td><td>48</td><td>42</td><td>741</td><td>1334</td><td>1191</td><td>1575</td><td>1605</td></tr>
    <tr><td>Icebreaker</td><td>107.7</td><td>49.13</td><td>13391.97</td><td>7282.95</td><td>446</td><td>118</td><td>52</td><td>50</td><td>226</td><td>10889.89</td><td>5958.82</td><td>0.5438</td><td>0.3059</td><td>0.298</td><td>0.1121</td><td>0.657</td><td>0.0049759</td><td>0.0052235</td><td>0.0024611</td><td>325</td><td>348</td><td>36</td><td>33</td><td>69</td><td>64</td><td>60</td><td>106</td><td>68</td><td>47</td><td>41</td><td>929</td><td>1117</td><td>1262</td><td>1824</td><td>1615</td></tr>
    <tr><td>Dickies</td><td>41.86</td><td>20.18</td><td>12172.74</td><td>6307.66</td><td>1144</td><td>276</td><td>107</td><td>175</td><td>586</td><td>11380.62</td><td>5875.24</td><td>0.5182</td><td>0.2794</td><td>0.2848</td><td>0.153</td><td>0.6798</td><td>0.0045229</td><td>0.004524</td><td>0.0063127</td><td>1293</td><td>1309</td><td>45</td><td>44</td><td>17</td><td>17</td><td>19</td><td>17</td><td>17</td><td>45</td><td>43</td><td>1259</td><td>1291</td><td>1434</td><td>1223</td><td>1237</td></tr>
    <tr><td>Jordan</td><td>712.87</td><td>364.11</td><td>13002.76</td><td>6657.31</td><td>57</td><td>19</td><td>10</td><td>4</td><td>24</td><td>11798.99</td><td>5837.86</td><td>0.512</td><td>0.3448</td><td>0.3585</td><td>0.0702</td><td>0.5581</td><td>0.0048313</td><td>0.0047748</td><td>0.0003145</td><td>3</td><td>2</td><td>39</td><td>42</td><td>577</td><td>467</td><td>370</td><td>943</td><td>669</td><td>44</td><td>44</td><td>1342</td><td>802</td><td>668</td><td>2163</td><td>2248</td></tr>
    <tr><td>Woolrich</td><td>92.27</td><td>43.53</td><td>11626.08</td><td>6134.65</td><td>496</td><td>124</td><td>47</td><td>82</td><td>243</td><td>12054.34</td><td>6338.46</td><td>0.5277</td><td>0.2749</td><td>0.2995</td><td>0.1653</td><td>0.6621</td><td>0.0043198</td><td>0.0043999</td><td>0.002737</td><td>428</td><td>424</td><td>47</td><td>45</td><td>61</td><td>57</td><td>67</td><td>59</td><td>64</td><td>42</td><td>38</td><td>1149</td><td>1307</td><td>1250</td><td>1073</td><td>1583</td></tr>
    <tr><td>AG Adriano Goldschmied</td><td>158.52</td><td>81.45</td><td>15325.0</td><td>7390.13</td><td>353</td><td>96</td><td>35</td><td>43</td><td>179</td><td>12419.86</td><td>6058.66</td><td>0.4822</td><td>0.2672</td><td>0.3097</td><td>0.1218</td><td>0.6509</td><td>0.0056941</td><td>0.0053003</td><td>0.0019479</td><td>149</td><td>121</td><td>30</td><td>30</td><td>100</td><td>84</td><td>102</td><td>126</td><td>93</td><td>40</td><td>40</td><td>1713</td><td>1351</td><td>1123</td><td>1739</td><td>1660</td></tr>
    <tr><td>DC</td><td>50.94</td><td>25.91</td><td>14076.31</td><td>6883.92</td><td>966</td><td>263</td><td>101</td><td>148</td><td>454</td><td>12578.25</td><td>6213.14</td><td>0.489</td><td>0.2775</td><td>0.3215</td><td>0.1532</td><td>0.6332</td><td>0.0052302</td><td>0.0049373</td><td>0.0053304</td><td>1036</td><td>990</td><td>32</td><td>37</td><td>25</td><td>22</td><td>22</td><td>24</td><td>26</td><td>39</td><td>39</td><td>1628</td><td>1299</td><td>1027</td><td>1219</td><td>1811</td></tr>
    <tr><td>Not Your Daughter&#x27;s Jeans</td><td>100.85</td><td>54.77</td><td>16067.86</td><td>7332.91</td><td>527</td><td>157</td><td>62</td><td>61</td><td>247</td><td>12591.86</td><td>5739.96</td><td>0.4564</td><td>0.2831</td><td>0.3369</td><td>0.1157</td><td>0.6114</td><td>0.0059701</td><td>0.0052593</td><td>0.002908</td><td>351</td><td>296</td><td>26</td><td>32</td><td>54</td><td>46</td><td>49</td><td>82</td><td>61</td><td>38</td><td>48</td><td>2039</td><td>1273</td><td>768</td><td>1797</td><td>1957</td></tr>
    <tr><td>Joseph Abboud</td><td>173.3</td><td>71.4</td><td>11656.07</td><td>6870.25</td><td>298</td><td>70</td><td>34</td><td>37</td><td>157</td><td>12746.72</td><td>7531.64</td><td>0.5894</td><td>0.3269</td><td>0.2682</td><td>0.1242</td><td>0.6916</td><td>0.0043309</td><td>0.0049275</td><td>0.0016444</td><td>128</td><td>170</td><td>46</td><td>38</td><td>117</td><td>124</td><td>107</td><td>144</td><td>108</td><td>37</td><td>32</td><td>315</td><td>1027</td><td>1588</td><td>1726</td><td>1140</td></tr>
    <tr><td>O&#x27;Neill</td><td>48.36</td><td>26.32</td><td>12853.97</td><td>5838.83</td><td>1056</td><td>266</td><td>105</td><td>166</td><td>519</td><td>12805.89</td><td>5826.98</td><td>0.4542</td><td>0.283</td><td>0.2989</td><td>0.1572</td><td>0.6611</td><td>0.004776</td><td>0.0041877</td><td>0.0058271</td><td>1121</td><td>966</td><td>40</td><td>49</td><td>21</td><td>20</td><td>20</td><td>19</td><td>21</td><td>36</td><td>45</td><td>2064</td><td>1275</td><td>1256</td><td>1152</td><td>1592</td></tr>
  </tbody>
</table>

</div>

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

<h3>Bottom brands by Units Returned</h3>

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
WHERE units_returned = 0
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
    <tr><td>Moncler</td><td>550.0</td><td>238.15</td><td>1650.0</td><td>935.55</td><td>9</td><td>3</td><td>0</td><td>1</td><td>5</td><td>550.0</td><td>311.85</td><td>0.567</td><td>0.0</td><td>0.375</td><td>0.1111</td><td>0.625</td><td>0.0006131</td><td>0.000671</td><td>4.97e-05</td><td>6</td><td>6</td><td>338</td><td>313</td><td>1790</td><td>1481</td><td>2066</td><td>1744</td><td>1686</td><td>744</td><td>703</td><td>598</td><td>2066</td><td>548</td><td>1827</td><td>1843</td></tr>
    <tr><td>Oxfords Cashmere</td><td>260.25</td><td>121.29</td><td>1544.0</td><td>823.21</td><td>16</td><td>6</td><td>0</td><td>3</td><td>7</td><td>667.0</td><td>355.4</td><td>0.5332</td><td>0.0</td><td>0.4615</td><td>0.1875</td><td>0.5385</td><td>0.0005737</td><td>0.0005904</td><td>8.83e-05</td><td>39</td><td>37</td><td>354</td><td>344</td><td>1326</td><td>1030</td><td>2066</td><td>1126</td><td>1418</td><td>658</td><td>644</td><td>1073</td><td>2066</td><td>281</td><td>766</td><td>2301</td></tr>
    <tr><td>Skins</td><td>96.28</td><td>41.5</td><td>1249.34</td><td>701.49</td><td>43</td><td>14</td><td>0</td><td>11</td><td>18</td><td>996.89</td><td>562.31</td><td>0.5615</td><td>0.0</td><td>0.4375</td><td>0.2558</td><td>0.5625</td><td>0.0004642</td><td>0.0005031</td><td>0.0002373</td><td>393</td><td>463</td><td>419</td><td>395</td><td>722</td><td>586</td><td>2066</td><td>472</td><td>830</td><td>503</td><td>463</td><td>671</td><td>2066</td><td>314</td><td>295</td><td>2239</td></tr>
    <tr><td>NAU</td><td>414.95</td><td>146.89</td><td>829.9</td><td>536.12</td><td>6</td><td>2</td><td>0</td><td>0</td><td>4</td><td>0.0</td><td>0.0</td><td>0.646</td><td>0.0</td><td>0.3333</td><td>0.0</td><td>0.6667</td><td>0.0003084</td><td>0.0003845</td><td>3.31e-05</td><td>9</td><td>20</td><td>560</td><td>482</td><td>2174</td><td>1758</td><td>2066</td><td>2284</td><td>1860</td><td>2499</td><td>2499</td><td>17</td><td>2066</td><td>773</td><td>2284</td><td>1312</td></tr>
    <tr><td>Klymit</td><td>204.95</td><td>104.11</td><td>819.8</td><td>403.34</td><td>6</td><td>4</td><td>0</td><td>0</td><td>2</td><td>0.0</td><td>0.0</td><td>0.492</td><td>0.0</td><td>0.6667</td><td>0.0</td><td>0.3333</td><td>0.0003046</td><td>0.0002893</td><td>3.31e-05</td><td>79</td><td>55</td><td>570</td><td>590</td><td>2174</td><td>1309</td><td>2066</td><td>2284</td><td>2334</td><td>2499</td><td>2499</td><td>1597</td><td>2066</td><td>40</td><td>2284</td><td>2625</td></tr>
    <tr><td>VIPARO</td><td>189.95</td><td>85.79</td><td>759.8</td><td>414.09</td><td>12</td><td>4</td><td>0</td><td>4</td><td>4</td><td>759.8</td><td>414.09</td><td>0.545</td><td>0.0</td><td>0.5</td><td>0.3333</td><td>0.5</td><td>0.0002823</td><td>0.000297</td><td>6.62e-05</td><td>104</td><td>110</td><td>600</td><td>580</td><td>1567</td><td>1309</td><td>2066</td><td>943</td><td>1860</td><td>596</td><td>582</td><td>908</td><td>2066</td><td>143</td><td>121</td><td>2349</td></tr>
    <tr><td>Scully</td><td>149.0</td><td>57.81</td><td>745.0</td><td>455.94</td><td>12</td><td>5</td><td>0</td><td>0</td><td>7</td><td>0.0</td><td>0.0</td><td>0.612</td><td>0.0</td><td>0.4167</td><td>0.0</td><td>0.5833</td><td>0.0002768</td><td>0.000327</td><td>6.62e-05</td><td>170</td><td>264</td><td>611</td><td>548</td><td>1567</td><td>1160</td><td>2066</td><td>2284</td><td>1418</td><td>2499</td><td>2499</td><td>126</td><td>2066</td><td>384</td><td>2284</td><td>2122</td></tr>
    <tr><td>66 North</td><td>146.39</td><td>64.5</td><td>697.98</td><td>379.04</td><td>10</td><td>5</td><td>0</td><td>0</td><td>5</td><td>0.0</td><td>0.0</td><td>0.5431</td><td>0.0</td><td>0.5</td><td>0.0</td><td>0.5</td><td>0.0002593</td><td>0.0002719</td><td>5.52e-05</td><td>181</td><td>213</td><td>639</td><td>611</td><td>1712</td><td>1160</td><td>2066</td><td>2284</td><td>1686</td><td>2499</td><td>2499</td><td>938</td><td>2066</td><td>143</td><td>2284</td><td>2349</td></tr>
    <tr><td>Krazy</td><td>70.61</td><td>35.46</td><td>689.97</td><td>323.15</td><td>29</td><td>7</td><td>0</td><td>6</td><td>16</td><td>378.95</td><td>183.56</td><td>0.4684</td><td>0.0</td><td>0.3043</td><td>0.2069</td><td>0.6957</td><td>0.0002564</td><td>0.0002318</td><td>0.00016</td><td>660</td><td>621</td><td>644</td><td>682</td><td>963</td><td>932</td><td>2066</td><td>741</td><td>904</td><td>909</td><td>945</td><td>1894</td><td>2066</td><td>1178</td><td>569</td><td>1104</td></tr>
    <tr><td>PEZ Candy</td><td>83.18</td><td>37.96</td><td>662.86</td><td>363.31</td><td>22</td><td>7</td><td>0</td><td>3</td><td>12</td><td>232.86</td><td>128.84</td><td>0.5481</td><td>0.0</td><td>0.3684</td><td>0.1364</td><td>0.6316</td><td>0.0002463</td><td>0.0002606</td><td>0.0001214</td><td>508</td><td>546</td><td>666</td><td>636</td><td>1122</td><td>932</td><td>2066</td><td>1126</td><td>1062</td><td>1166</td><td>1125</td><td>857</td><td>2066</td><td>604</td><td>1505</td><td>1819</td></tr>
    <tr><td>Burk&#x27;s Bay</td><td>149.97</td><td>65.39</td><td>599.88</td><td>338.33</td><td>10</td><td>4</td><td>0</td><td>3</td><td>3</td><td>449.91</td><td>253.75</td><td>0.564</td><td>0.0</td><td>0.5714</td><td>0.3</td><td>0.4286</td><td>0.0002229</td><td>0.0002427</td><td>5.52e-05</td><td>169</td><td>212</td><td>703</td><td>662</td><td>1712</td><td>1309</td><td>2066</td><td>1126</td><td>2082</td><td>839</td><td>789</td><td>631</td><td>2066</td><td>113</td><td>200</td><td>2559</td></tr>
    <tr><td>Fisherman</td><td>149.0</td><td>70.63</td><td>596.0</td><td>313.5</td><td>9</td><td>4</td><td>0</td><td>1</td><td>4</td><td>149.0</td><td>78.37</td><td>0.526</td><td>0.0</td><td>0.5</td><td>0.1111</td><td>0.5</td><td>0.0002214</td><td>0.0002248</td><td>4.97e-05</td><td>170</td><td>175</td><td>705</td><td>694</td><td>1790</td><td>1309</td><td>2066</td><td>1744</td><td>1860</td><td>1439</td><td>1426</td><td>1168</td><td>2066</td><td>143</td><td>1827</td><td>2349</td></tr>
    <tr><td>Enro</td><td>71.92</td><td>33.49</td><td>583.5</td><td>312.51</td><td>25</td><td>8</td><td>0</td><td>4</td><td>13</td><td>278.0</td><td>139.83</td><td>0.5356</td><td>0.0</td><td>0.381</td><td>0.16</td><td>0.619</td><td>0.0002168</td><td>0.0002241</td><td>0.000138</td><td>645</td><td>680</td><td>715</td><td>696</td><td>1035</td><td>858</td><td>2066</td><td>943</td><td>1022</td><td>1071</td><td>1083</td><td>1047</td><td>2066</td><td>537</td><td>1115</td><td>1910</td></tr>
    <tr><td>Knoles &amp; Carter</td><td>144.54</td><td>66.58</td><td>579.96</td><td>314.82</td><td>11</td><td>4</td><td>0</td><td>1</td><td>6</td><td>149.99</td><td>86.99</td><td>0.5428</td><td>0.0</td><td>0.4</td><td>0.0909</td><td>0.6</td><td>0.0002155</td><td>0.0002258</td><td>6.07e-05</td><td>186</td><td>196</td><td>717</td><td>691</td><td>1626</td><td>1309</td><td>2066</td><td>1744</td><td>1551</td><td>1425</td><td>1355</td><td>946</td><td>2066</td><td>418</td><td>2012</td><td>1994</td></tr>
    <tr><td>Patterson J. Kincaid</td><td>128.18</td><td>65.74</td><td>546.91</td><td>255.35</td><td>14</td><td>4</td><td>0</td><td>2</td><td>8</td><td>161.84</td><td>84.8</td><td>0.4669</td><td>0.0</td><td>0.3333</td><td>0.1429</td><td>0.6667</td><td>0.0002032</td><td>0.0001831</td><td>7.73e-05</td><td>235</td><td>208</td><td>739</td><td>781</td><td>1441</td><td>1309</td><td>2066</td><td>1353</td><td>1310</td><td>1383</td><td>1377</td><td>1914</td><td>2066</td><td>773</td><td>1347</td><td>1312</td></tr>
  </tbody>
</table>

</div>

<h3>Analytical Insights & Business Recommendations</h3>
<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p>Among the top 50 brands by revenue, the ones with the lowest lost revenue include Nike ($7,304.66 lost on $16,424.08 revenue), Alpha Industries ($8,183.49 lost on $13,163.17 revenue), and Champion ($9,239.17 lost on $10,673.83 revenue). These brands have more favorable lost-revenue-to-earned-revenue ratios compared to leaders like Diesel and Calvin Klein where losses nearly match earnings. Nike's lost revenue is under half its earned revenue, which is notably better than the dataset average. However, Nike only places #25 in revenue despite strong brand recognition — suggesting either limited product catalog representation or underinvestment in Nike product promotion. Nike, Champion, and Alpha Industries present an opportunity — they have relatively clean loss profiles, meaning promotional spend on these brands is more likely to translate into retained revenue. Increasing marketing for these brands could grow revenue without proportionally increasing return-related losses.</p>

<p>The lowest profit margins among top-50 revenue brands are O'Neill (45.4%), Not Your Daughter's Jeans (45.6%), Quiksilver (45.6%), and Hurley (46.4%). These are overwhelmingly surf/action sports and denim brands where product costs consume a larger share of the sale price. The denim brands specifically (True Religion at 47.5%, 7 For All Mankind at 47.5%, Joe's Jeans at 47.1%, Hudson at 46.9%) all cluster in the 46–48% margin range, suggesting that denim as a product type carries higher input costs industry-wide. Given that denim margins are structurally lower, cost reduction is the primary lever. With brands like Wrangler (1,284 orders), Levi's (1,555 orders), and 7 For All Mankind (1,086 orders) driving substantial volume, negotiate volume-based supplier discounts. The order quantities provide real leverage — present suppliers with the choice of better unit pricing or reduced shelf allocation in favor of higher-margin categories.</p>

<p>The bottom 15 brands by unit orders all have just 1 order placed (Versace, Hermanny, Danshuz, Soft-Fit, TAIGA, NCIS, EuroBrand, FREEGUN, etc.). Most generated $0 in revenue — their only orders were returned or cancelled. These brands collectively represent dead inventory and wasted catalog space. Several of these brands (Versace with $128.50 avg price, TAIGA at $80.95, Steel Paisley at $120.00) carry higher price points, meaning each failed order ties up more capital in unsold inventory. Brands with fewer than 5 lifetime orders and $0 completed revenue should be evaluated for removal. Maintaining supplier relationships, inventory allocations, and product listings for brands that generate no revenue is a net drain on operational resources. Consider stopping deals with these underperforming brands to free up bandwidth and inventory space for proven performers. These brands may also be negatively affecting the company's reputation if customers encounter low-quality products from unknown suppliers.</p>

<p>Several brands have achieved zero returns while generating meaningful revenue: Moncler ($1,650 revenue, 9 orders, 0 returns), Scully ($745 revenue, 12 orders, 0 returns), 66 North ($697.98 revenue, 10 orders, 0 returns), and Krazy ($689.97 revenue, 29 orders, 0 returns). Notably, Krazy stands out with 29 orders and zero returns despite a moderate price point ($70.61 avg) — a strong signal of consistent product quality and accurate customer expectations. Investigate what makes zero-return brands successful. Examine their product descriptions, sizing accuracy, packaging quality, and supplier relationships. Replicate those practices across brands with high return rates in similar categories. Zero-return brands also represent reliable supplier partnerships worth deepening — negotiate expanded product lines or better terms with suppliers like Moncler, Scully, and 66 North whose products consistently meet customer expectations.</p>

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

<h3>Top categories by Profit</h3>

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
  profit_rank ASC
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
    <tr><td>Suits &amp; Sport Coats</td><td>124.74</td><td>50.03</td><td>153543.45</td><td>92034.55</td><td>5176</td><td>1255</td><td>486</td><td>790</td><td>2645</td><td>160577.15</td><td>96066.37</td><td>0.5994</td><td>0.2791</td><td>0.2861</td><td>0.1526</td><td>0.6782</td><td>0.0570503</td><td>0.066009</td><td>0.0285615</td><td>2</td><td>5</td><td>6</td><td>4</td><td>16</td><td>16</td><td>17</td><td>16</td><td>16</td><td>4</td><td>4</td><td>2</td><td>22</td><td>23</td><td>5</td><td>2</td></tr>
    <tr><td>Swim</td><td>57.2</td><td>28.98</td><td>156523.7</td><td>76716.71</td><td>11246</td><td>2772</td><td>1143</td><td>1660</td><td>5671</td><td>159217.24</td><td>78510.83</td><td>0.4901</td><td>0.292</td><td>0.2892</td><td>0.1476</td><td>0.6717</td><td>0.0581577</td><td>0.0550227</td><td>0.0620561</td><td>10</td><td>10</td><td>4</td><td>5</td><td>5</td><td>7</td><td>5</td><td>7</td><td>5</td><td>6</td><td>5</td><td>16</td><td>7</td><td>17</td><td>22</td><td>10</td></tr>
    <tr><td>Fashion Hoodies &amp; Sweatshirts</td><td>54.02</td><td>28.09</td><td>155933.0</td><td>74918.07</td><td>11737</td><td>2951</td><td>1191</td><td>1714</td><td>5881</td><td>159794.53</td><td>76980.63</td><td>0.4805</td><td>0.2875</td><td>0.2944</td><td>0.146</td><td>0.6659</td><td>0.0579382</td><td>0.0537327</td><td>0.0647655</td><td>12</td><td>11</td><td>5</td><td>6</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td><td>5</td><td>6</td><td>17</td><td>14</td><td>12</td><td>23</td><td>14</td></tr>
    <tr><td>Active</td><td>50.94</td><td>21.35</td><td>117645.45</td><td>68332.26</td><td>8932</td><td>2180</td><td>938</td><td>1362</td><td>4452</td><td>113272.89</td><td>66015.46</td><td>0.5808</td><td>0.3008</td><td>0.288</td><td>0.1525</td><td>0.6713</td><td>0.0437121</td><td>0.0490092</td><td>0.0492873</td><td>15</td><td>18</td><td>11</td><td>7</td><td>11</td><td>11</td><td>10</td><td>10</td><td>11</td><td>10</td><td>9</td><td>6</td><td>4</td><td>21</td><td>7</td><td>11</td></tr>
    <tr><td>Sleep &amp; Lounge</td><td>48.79</td><td>23.64</td><td>132101.2</td><td>68241.52</td><td>11071</td><td>2737</td><td>1128</td><td>1645</td><td>5561</td><td>134573.41</td><td>68950.32</td><td>0.5166</td><td>0.2918</td><td>0.2904</td><td>0.1486</td><td>0.6702</td><td>0.0490833</td><td>0.0489441</td><td>0.0610905</td><td>16</td><td>15</td><td>8</td><td>8</td><td>8</td><td>8</td><td>7</td><td>8</td><td>6</td><td>8</td><td>7</td><td>13</td><td>8</td><td>15</td><td>15</td><td>12</td></tr>
    <tr><td>Shorts</td><td>47.29</td><td>23.69</td><td>136510.82</td><td>68155.43</td><td>11176</td><td>2819</td><td>1130</td><td>1690</td><td>5537</td><td>134644.7</td><td>67078.36</td><td>0.4993</td><td>0.2861</td><td>0.2972</td><td>0.1512</td><td>0.6626</td><td>0.0507217</td><td>0.0488824</td><td>0.0616699</td><td>17</td><td>14</td><td>7</td><td>9</td><td>6</td><td>5</td><td>6</td><td>5</td><td>7</td><td>7</td><td>8</td><td>14</td><td>15</td><td>7</td><td>10</td><td>21</td></tr>
    <tr><td>Dresses</td><td>84.24</td><td>37.9</td><td>112895.24</td><td>62082.56</td><td>5358</td><td>1316</td><td>549</td><td>792</td><td>2701</td><td>113022.02</td><td>62283.44</td><td>0.5499</td><td>0.2944</td><td>0.2882</td><td>0.1478</td><td>0.6724</td><td>0.0419471</td><td>0.0445268</td><td>0.0295658</td><td>7</td><td>6</td><td>12</td><td>10</td><td>15</td><td>15</td><td>15</td><td>15</td><td>15</td><td>11</td><td>10</td><td>9</td><td>6</td><td>20</td><td>21</td><td>9</td></tr>
    <tr><td>Accessories</td><td>42.05</td><td>16.85</td><td>99096.96</td><td>59262.83</td><td>9813</td><td>2384</td><td>967</td><td>1497</td><td>4965</td><td>103385.5</td><td>62000.28</td><td>0.598</td><td>0.2886</td><td>0.2867</td><td>0.1526</td><td>0.6756</td><td>0.0368203</td><td>0.0425044</td><td>0.0541488</td><td>19</td><td>22</td><td>14</td><td>11</td><td>9</td><td>9</td><td>9</td><td>9</td><td>9</td><td>14</td><td>11</td><td>5</td><td>12</td><td>22</td><td>5</td><td>5</td></tr>
    <tr><td>Pants</td><td>59.65</td><td>27.35</td><td>106719.7</td><td>57634.8</td><td>7239</td><td>1823</td><td>713</td><td>1076</td><td>3627</td><td>106167.82</td><td>57611.26</td><td>0.5401</td><td>0.2812</td><td>0.2958</td><td>0.1486</td><td>0.6655</td><td>0.0396526</td><td>0.0413368</td><td>0.0399453</td><td>9</td><td>12</td><td>13</td><td>12</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>12</td><td>10</td><td>21</td><td>10</td><td>15</td><td>16</td></tr>
    <tr><td>Intimates</td><td>33.75</td><td>17.96</td><td>118381.2</td><td>55321.28</td><td>13423</td><td>3393</td><td>1329</td><td>2044</td><td>6657</td><td>112421.97</td><td>52618.74</td><td>0.4673</td><td>0.2814</td><td>0.2982</td><td>0.1523</td><td>0.6624</td><td>0.0439855</td><td>0.0396775</td><td>0.074069</td><td>22</td><td>21</td><td>10</td><td>13</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>12</td><td>14</td><td>20</td><td>19</td><td>5</td><td>9</td><td>23</td></tr>
    <tr><td>Tops &amp; Tees</td><td>40.97</td><td>22.93</td><td>121151.89</td><td>53364.7</td><td>12000</td><td>2960</td><td>1292</td><td>1783</td><td>5965</td><td>123378.82</td><td>54313.77</td><td>0.4405</td><td>0.3039</td><td>0.2897</td><td>0.1486</td><td>0.6683</td><td>0.045015</td><td>0.0382742</td><td>0.0662168</td><td>20</td><td>16</td><td>9</td><td>14</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>9</td><td>13</td><td>22</td><td>2</td><td>16</td><td>15</td><td>13</td></tr>
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

<h3>Top categories by Unit Orders</h3>

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
  unit_orders_placed_rank ASC
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
    <tr><td>Intimates</td><td>33.75</td><td>17.96</td><td>118381.2</td><td>55321.28</td><td>13423</td><td>3393</td><td>1329</td><td>2044</td><td>6657</td><td>112421.97</td><td>52618.74</td><td>0.4673</td><td>0.2814</td><td>0.2982</td><td>0.1523</td><td>0.6624</td><td>0.0439855</td><td>0.0396775</td><td>0.074069</td><td>22</td><td>21</td><td>10</td><td>13</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>12</td><td>14</td><td>20</td><td>19</td><td>5</td><td>9</td><td>23</td></tr>
    <tr><td>Jeans</td><td>97.76</td><td>52.34</td><td>308764.08</td><td>143520.48</td><td>12655</td><td>3169</td><td>1303</td><td>1955</td><td>6228</td><td>319052.52</td><td>148299.49</td><td>0.4648</td><td>0.2914</td><td>0.2962</td><td>0.1545</td><td>0.6628</td><td>0.1147238</td><td>0.1029357</td><td>0.0698311</td><td>4</td><td>4</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>21</td><td>9</td><td>9</td><td>3</td><td>20</td></tr>
    <tr><td>Tops &amp; Tees</td><td>40.97</td><td>22.93</td><td>121151.89</td><td>53364.7</td><td>12000</td><td>2960</td><td>1292</td><td>1783</td><td>5965</td><td>123378.82</td><td>54313.77</td><td>0.4405</td><td>0.3039</td><td>0.2897</td><td>0.1486</td><td>0.6683</td><td>0.045015</td><td>0.0382742</td><td>0.0662168</td><td>20</td><td>16</td><td>9</td><td>14</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>9</td><td>13</td><td>22</td><td>2</td><td>16</td><td>15</td><td>13</td></tr>
    <tr><td>Fashion Hoodies &amp; Sweatshirts</td><td>54.02</td><td>28.09</td><td>155933.0</td><td>74918.07</td><td>11737</td><td>2951</td><td>1191</td><td>1714</td><td>5881</td><td>159794.53</td><td>76980.63</td><td>0.4805</td><td>0.2875</td><td>0.2944</td><td>0.146</td><td>0.6659</td><td>0.0579382</td><td>0.0537327</td><td>0.0647655</td><td>12</td><td>11</td><td>5</td><td>6</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td><td>5</td><td>6</td><td>17</td><td>14</td><td>12</td><td>23</td><td>14</td></tr>
    <tr><td>Swim</td><td>57.2</td><td>28.98</td><td>156523.7</td><td>76716.71</td><td>11246</td><td>2772</td><td>1143</td><td>1660</td><td>5671</td><td>159217.24</td><td>78510.83</td><td>0.4901</td><td>0.292</td><td>0.2892</td><td>0.1476</td><td>0.6717</td><td>0.0581577</td><td>0.0550227</td><td>0.0620561</td><td>10</td><td>10</td><td>4</td><td>5</td><td>5</td><td>7</td><td>5</td><td>7</td><td>5</td><td>6</td><td>5</td><td>16</td><td>7</td><td>17</td><td>22</td><td>10</td></tr>
    <tr><td>Shorts</td><td>47.29</td><td>23.69</td><td>136510.82</td><td>68155.43</td><td>11176</td><td>2819</td><td>1130</td><td>1690</td><td>5537</td><td>134644.7</td><td>67078.36</td><td>0.4993</td><td>0.2861</td><td>0.2972</td><td>0.1512</td><td>0.6626</td><td>0.0507217</td><td>0.0488824</td><td>0.0616699</td><td>17</td><td>14</td><td>7</td><td>9</td><td>6</td><td>5</td><td>6</td><td>5</td><td>7</td><td>7</td><td>8</td><td>14</td><td>15</td><td>7</td><td>10</td><td>21</td></tr>
    <tr><td>Sweaters</td><td>75.46</td><td>36.32</td><td>213600.63</td><td>110714.83</td><td>11078</td><td>2792</td><td>1081</td><td>1688</td><td>5517</td><td>208115.59</td><td>107697.32</td><td>0.5183</td><td>0.2791</td><td>0.2973</td><td>0.1524</td><td>0.664</td><td>0.0793651</td><td>0.0794068</td><td>0.0611291</td><td>8</td><td>7</td><td>3</td><td>3</td><td>7</td><td>6</td><td>8</td><td>6</td><td>8</td><td>3</td><td>3</td><td>12</td><td>22</td><td>6</td><td>8</td><td>18</td></tr>
    <tr><td>Sleep &amp; Lounge</td><td>48.79</td><td>23.64</td><td>132101.2</td><td>68241.52</td><td>11071</td><td>2737</td><td>1128</td><td>1645</td><td>5561</td><td>134573.41</td><td>68950.32</td><td>0.5166</td><td>0.2918</td><td>0.2904</td><td>0.1486</td><td>0.6702</td><td>0.0490833</td><td>0.0489441</td><td>0.0610905</td><td>16</td><td>15</td><td>8</td><td>8</td><td>8</td><td>8</td><td>7</td><td>8</td><td>6</td><td>8</td><td>7</td><td>13</td><td>8</td><td>15</td><td>15</td><td>12</td></tr>
    <tr><td>Accessories</td><td>42.05</td><td>16.85</td><td>99096.96</td><td>59262.83</td><td>9813</td><td>2384</td><td>967</td><td>1497</td><td>4965</td><td>103385.5</td><td>62000.28</td><td>0.598</td><td>0.2886</td><td>0.2867</td><td>0.1526</td><td>0.6756</td><td>0.0368203</td><td>0.0425044</td><td>0.0541488</td><td>19</td><td>22</td><td>14</td><td>11</td><td>9</td><td>9</td><td>9</td><td>9</td><td>9</td><td>14</td><td>11</td><td>5</td><td>12</td><td>22</td><td>5</td><td>5</td></tr>
    <tr><td>Outerwear &amp; Coats</td><td>146.29</td><td>65.02</td><td>339222.29</td><td>188050.56</td><td>9028</td><td>2308</td><td>862</td><td>1318</td><td>4540</td><td>322743.18</td><td>179542.92</td><td>0.5544</td><td>0.2719</td><td>0.2994</td><td>0.146</td><td>0.663</td><td>0.1260408</td><td>0.1348735</td><td>0.0498171</td><td>1</td><td>2</td><td>1</td><td>1</td><td>10</td><td>10</td><td>11</td><td>11</td><td>10</td><td>1</td><td>1</td><td>8</td><td>26</td><td>4</td><td>23</td><td>19</td></tr>
    <tr><td>Active</td><td>50.94</td><td>21.35</td><td>117645.45</td><td>68332.26</td><td>8932</td><td>2180</td><td>938</td><td>1362</td><td>4452</td><td>113272.89</td><td>66015.46</td><td>0.5808</td><td>0.3008</td><td>0.288</td><td>0.1525</td><td>0.6713</td><td>0.0437121</td><td>0.0490092</td><td>0.0492873</td><td>15</td><td>18</td><td>11</td><td>7</td><td>11</td><td>11</td><td>10</td><td>10</td><td>11</td><td>10</td><td>9</td><td>6</td><td>4</td><td>21</td><td>7</td><td>11</td></tr>
    <tr><td>Underwear</td><td>27.21</td><td>12.79</td><td>50614.6</td><td>26861.36</td><td>7505</td><td>1886</td><td>738</td><td>1122</td><td>3759</td><td>51345.06</td><td>27197.18</td><td>0.5307</td><td>0.2813</td><td>0.2955</td><td>0.1495</td><td>0.6659</td><td>0.0188063</td><td>0.0192655</td><td>0.0414131</td><td>23</td><td>24</td><td>17</td><td>17</td><td>12</td><td>12</td><td>12</td><td>12</td><td>12</td><td>17</td><td>17</td><td>11</td><td>20</td><td>11</td><td>13</td><td>14</td></tr>
    <tr><td>Pants</td><td>59.65</td><td>27.35</td><td>106719.7</td><td>57634.8</td><td>7239</td><td>1823</td><td>713</td><td>1076</td><td>3627</td><td>106167.82</td><td>57611.26</td><td>0.5401</td><td>0.2812</td><td>0.2958</td><td>0.1486</td><td>0.6655</td><td>0.0396526</td><td>0.0413368</td><td>0.0399453</td><td>9</td><td>12</td><td>13</td><td>12</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>12</td><td>10</td><td>21</td><td>10</td><td>15</td><td>16</td></tr>
    <tr><td>Socks</td><td>21.13</td><td>12.76</td><td>31572.07</td><td>12517.44</td><td>6329</td><td>1557</td><td>636</td><td>939</td><td>3197</td><td>32927.59</td><td>13032.11</td><td>0.3965</td><td>0.29</td><td>0.2889</td><td>0.1484</td><td>0.6725</td><td>0.0117309</td><td>0.0089777</td><td>0.0349238</td><td>25</td><td>25</td><td>21</td><td>22</td><td>14</td><td>14</td><td>14</td><td>14</td><td>14</td><td>20</td><td>21</td><td>24</td><td>10</td><td>18</td><td>18</td><td>8</td></tr>
    <tr><td>Dresses</td><td>84.24</td><td>37.9</td><td>112895.24</td><td>62082.56</td><td>5358</td><td>1316</td><td>549</td><td>792</td><td>2701</td><td>113022.02</td><td>62283.44</td><td>0.5499</td><td>0.2944</td><td>0.2882</td><td>0.1478</td><td>0.6724</td><td>0.0419471</td><td>0.0445268</td><td>0.0295658</td><td>7</td><td>6</td><td>12</td><td>10</td><td>15</td><td>15</td><td>15</td><td>15</td><td>15</td><td>11</td><td>10</td><td>9</td><td>6</td><td>20</td><td>21</td><td>9</td></tr>
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

<h3>Top categories by Units Returned</h3>

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
  units_returned_rank ASC
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
    <tr><td>Intimates</td><td>33.75</td><td>17.96</td><td>118381.2</td><td>55321.28</td><td>13423</td><td>3393</td><td>1329</td><td>2044</td><td>6657</td><td>112421.97</td><td>52618.74</td><td>0.4673</td><td>0.2814</td><td>0.2982</td><td>0.1523</td><td>0.6624</td><td>0.0439855</td><td>0.0396775</td><td>0.074069</td><td>22</td><td>21</td><td>10</td><td>13</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>12</td><td>14</td><td>20</td><td>19</td><td>5</td><td>9</td><td>23</td></tr>
    <tr><td>Jeans</td><td>97.76</td><td>52.34</td><td>308764.08</td><td>143520.48</td><td>12655</td><td>3169</td><td>1303</td><td>1955</td><td>6228</td><td>319052.52</td><td>148299.49</td><td>0.4648</td><td>0.2914</td><td>0.2962</td><td>0.1545</td><td>0.6628</td><td>0.1147238</td><td>0.1029357</td><td>0.0698311</td><td>4</td><td>4</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>21</td><td>9</td><td>9</td><td>3</td><td>20</td></tr>
    <tr><td>Tops &amp; Tees</td><td>40.97</td><td>22.93</td><td>121151.89</td><td>53364.7</td><td>12000</td><td>2960</td><td>1292</td><td>1783</td><td>5965</td><td>123378.82</td><td>54313.77</td><td>0.4405</td><td>0.3039</td><td>0.2897</td><td>0.1486</td><td>0.6683</td><td>0.045015</td><td>0.0382742</td><td>0.0662168</td><td>20</td><td>16</td><td>9</td><td>14</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>9</td><td>13</td><td>22</td><td>2</td><td>16</td><td>15</td><td>13</td></tr>
    <tr><td>Fashion Hoodies &amp; Sweatshirts</td><td>54.02</td><td>28.09</td><td>155933.0</td><td>74918.07</td><td>11737</td><td>2951</td><td>1191</td><td>1714</td><td>5881</td><td>159794.53</td><td>76980.63</td><td>0.4805</td><td>0.2875</td><td>0.2944</td><td>0.146</td><td>0.6659</td><td>0.0579382</td><td>0.0537327</td><td>0.0647655</td><td>12</td><td>11</td><td>5</td><td>6</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td><td>5</td><td>6</td><td>17</td><td>14</td><td>12</td><td>23</td><td>14</td></tr>
    <tr><td>Swim</td><td>57.2</td><td>28.98</td><td>156523.7</td><td>76716.71</td><td>11246</td><td>2772</td><td>1143</td><td>1660</td><td>5671</td><td>159217.24</td><td>78510.83</td><td>0.4901</td><td>0.292</td><td>0.2892</td><td>0.1476</td><td>0.6717</td><td>0.0581577</td><td>0.0550227</td><td>0.0620561</td><td>10</td><td>10</td><td>4</td><td>5</td><td>5</td><td>7</td><td>5</td><td>7</td><td>5</td><td>6</td><td>5</td><td>16</td><td>7</td><td>17</td><td>22</td><td>10</td></tr>
    <tr><td>Shorts</td><td>47.29</td><td>23.69</td><td>136510.82</td><td>68155.43</td><td>11176</td><td>2819</td><td>1130</td><td>1690</td><td>5537</td><td>134644.7</td><td>67078.36</td><td>0.4993</td><td>0.2861</td><td>0.2972</td><td>0.1512</td><td>0.6626</td><td>0.0507217</td><td>0.0488824</td><td>0.0616699</td><td>17</td><td>14</td><td>7</td><td>9</td><td>6</td><td>5</td><td>6</td><td>5</td><td>7</td><td>7</td><td>8</td><td>14</td><td>15</td><td>7</td><td>10</td><td>21</td></tr>
    <tr><td>Sleep &amp; Lounge</td><td>48.79</td><td>23.64</td><td>132101.2</td><td>68241.52</td><td>11071</td><td>2737</td><td>1128</td><td>1645</td><td>5561</td><td>134573.41</td><td>68950.32</td><td>0.5166</td><td>0.2918</td><td>0.2904</td><td>0.1486</td><td>0.6702</td><td>0.0490833</td><td>0.0489441</td><td>0.0610905</td><td>16</td><td>15</td><td>8</td><td>8</td><td>8</td><td>8</td><td>7</td><td>8</td><td>6</td><td>8</td><td>7</td><td>13</td><td>8</td><td>15</td><td>15</td><td>12</td></tr>
    <tr><td>Sweaters</td><td>75.46</td><td>36.32</td><td>213600.63</td><td>110714.83</td><td>11078</td><td>2792</td><td>1081</td><td>1688</td><td>5517</td><td>208115.59</td><td>107697.32</td><td>0.5183</td><td>0.2791</td><td>0.2973</td><td>0.1524</td><td>0.664</td><td>0.0793651</td><td>0.0794068</td><td>0.0611291</td><td>8</td><td>7</td><td>3</td><td>3</td><td>7</td><td>6</td><td>8</td><td>6</td><td>8</td><td>3</td><td>3</td><td>12</td><td>22</td><td>6</td><td>8</td><td>18</td></tr>
    <tr><td>Accessories</td><td>42.05</td><td>16.85</td><td>99096.96</td><td>59262.83</td><td>9813</td><td>2384</td><td>967</td><td>1497</td><td>4965</td><td>103385.5</td><td>62000.28</td><td>0.598</td><td>0.2886</td><td>0.2867</td><td>0.1526</td><td>0.6756</td><td>0.0368203</td><td>0.0425044</td><td>0.0541488</td><td>19</td><td>22</td><td>14</td><td>11</td><td>9</td><td>9</td><td>9</td><td>9</td><td>9</td><td>14</td><td>11</td><td>5</td><td>12</td><td>22</td><td>5</td><td>5</td></tr>
    <tr><td>Active</td><td>50.94</td><td>21.35</td><td>117645.45</td><td>68332.26</td><td>8932</td><td>2180</td><td>938</td><td>1362</td><td>4452</td><td>113272.89</td><td>66015.46</td><td>0.5808</td><td>0.3008</td><td>0.288</td><td>0.1525</td><td>0.6713</td><td>0.0437121</td><td>0.0490092</td><td>0.0492873</td><td>15</td><td>18</td><td>11</td><td>7</td><td>11</td><td>11</td><td>10</td><td>10</td><td>11</td><td>10</td><td>9</td><td>6</td><td>4</td><td>21</td><td>7</td><td>11</td></tr>
    <tr><td>Outerwear &amp; Coats</td><td>146.29</td><td>65.02</td><td>339222.29</td><td>188050.56</td><td>9028</td><td>2308</td><td>862</td><td>1318</td><td>4540</td><td>322743.18</td><td>179542.92</td><td>0.5544</td><td>0.2719</td><td>0.2994</td><td>0.146</td><td>0.663</td><td>0.1260408</td><td>0.1348735</td><td>0.0498171</td><td>1</td><td>2</td><td>1</td><td>1</td><td>10</td><td>10</td><td>11</td><td>11</td><td>10</td><td>1</td><td>1</td><td>8</td><td>26</td><td>4</td><td>23</td><td>19</td></tr>
    <tr><td>Underwear</td><td>27.21</td><td>12.79</td><td>50614.6</td><td>26861.36</td><td>7505</td><td>1886</td><td>738</td><td>1122</td><td>3759</td><td>51345.06</td><td>27197.18</td><td>0.5307</td><td>0.2813</td><td>0.2955</td><td>0.1495</td><td>0.6659</td><td>0.0188063</td><td>0.0192655</td><td>0.0414131</td><td>23</td><td>24</td><td>17</td><td>17</td><td>12</td><td>12</td><td>12</td><td>12</td><td>12</td><td>17</td><td>17</td><td>11</td><td>20</td><td>11</td><td>13</td><td>14</td></tr>
    <tr><td>Pants</td><td>59.65</td><td>27.35</td><td>106719.7</td><td>57634.8</td><td>7239</td><td>1823</td><td>713</td><td>1076</td><td>3627</td><td>106167.82</td><td>57611.26</td><td>0.5401</td><td>0.2812</td><td>0.2958</td><td>0.1486</td><td>0.6655</td><td>0.0396526</td><td>0.0413368</td><td>0.0399453</td><td>9</td><td>12</td><td>13</td><td>12</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>12</td><td>10</td><td>21</td><td>10</td><td>15</td><td>16</td></tr>
    <tr><td>Socks</td><td>21.13</td><td>12.76</td><td>31572.07</td><td>12517.44</td><td>6329</td><td>1557</td><td>636</td><td>939</td><td>3197</td><td>32927.59</td><td>13032.11</td><td>0.3965</td><td>0.29</td><td>0.2889</td><td>0.1484</td><td>0.6725</td><td>0.0117309</td><td>0.0089777</td><td>0.0349238</td><td>25</td><td>25</td><td>21</td><td>22</td><td>14</td><td>14</td><td>14</td><td>14</td><td>14</td><td>20</td><td>21</td><td>24</td><td>10</td><td>18</td><td>18</td><td>8</td></tr>
    <tr><td>Dresses</td><td>84.24</td><td>37.9</td><td>112895.24</td><td>62082.56</td><td>5358</td><td>1316</td><td>549</td><td>792</td><td>2701</td><td>113022.02</td><td>62283.44</td><td>0.5499</td><td>0.2944</td><td>0.2882</td><td>0.1478</td><td>0.6724</td><td>0.0419471</td><td>0.0445268</td><td>0.0295658</td><td>7</td><td>6</td><td>12</td><td>10</td><td>15</td><td>15</td><td>15</td><td>15</td><td>15</td><td>11</td><td>10</td><td>9</td><td>6</td><td>20</td><td>21</td><td>9</td></tr>
  </tbody>
</table>

</div>

<h3>Top categories by Lost Revenue</h3>

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
  lost_revenue_rank ASC
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
    <tr><td>Suits &amp; Sport Coats</td><td>124.74</td><td>50.03</td><td>153543.45</td><td>92034.55</td><td>5176</td><td>1255</td><td>486</td><td>790</td><td>2645</td><td>160577.15</td><td>96066.37</td><td>0.5994</td><td>0.2791</td><td>0.2861</td><td>0.1526</td><td>0.6782</td><td>0.0570503</td><td>0.066009</td><td>0.0285615</td><td>2</td><td>5</td><td>6</td><td>4</td><td>16</td><td>16</td><td>17</td><td>16</td><td>16</td><td>4</td><td>4</td><td>2</td><td>22</td><td>23</td><td>5</td><td>2</td></tr>
    <tr><td>Fashion Hoodies &amp; Sweatshirts</td><td>54.02</td><td>28.09</td><td>155933.0</td><td>74918.07</td><td>11737</td><td>2951</td><td>1191</td><td>1714</td><td>5881</td><td>159794.53</td><td>76980.63</td><td>0.4805</td><td>0.2875</td><td>0.2944</td><td>0.146</td><td>0.6659</td><td>0.0579382</td><td>0.0537327</td><td>0.0647655</td><td>12</td><td>11</td><td>5</td><td>6</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td><td>5</td><td>6</td><td>17</td><td>14</td><td>12</td><td>23</td><td>14</td></tr>
    <tr><td>Swim</td><td>57.2</td><td>28.98</td><td>156523.7</td><td>76716.71</td><td>11246</td><td>2772</td><td>1143</td><td>1660</td><td>5671</td><td>159217.24</td><td>78510.83</td><td>0.4901</td><td>0.292</td><td>0.2892</td><td>0.1476</td><td>0.6717</td><td>0.0581577</td><td>0.0550227</td><td>0.0620561</td><td>10</td><td>10</td><td>4</td><td>5</td><td>5</td><td>7</td><td>5</td><td>7</td><td>5</td><td>6</td><td>5</td><td>16</td><td>7</td><td>17</td><td>22</td><td>10</td></tr>
    <tr><td>Shorts</td><td>47.29</td><td>23.69</td><td>136510.82</td><td>68155.43</td><td>11176</td><td>2819</td><td>1130</td><td>1690</td><td>5537</td><td>134644.7</td><td>67078.36</td><td>0.4993</td><td>0.2861</td><td>0.2972</td><td>0.1512</td><td>0.6626</td><td>0.0507217</td><td>0.0488824</td><td>0.0616699</td><td>17</td><td>14</td><td>7</td><td>9</td><td>6</td><td>5</td><td>6</td><td>5</td><td>7</td><td>7</td><td>8</td><td>14</td><td>15</td><td>7</td><td>10</td><td>21</td></tr>
    <tr><td>Sleep &amp; Lounge</td><td>48.79</td><td>23.64</td><td>132101.2</td><td>68241.52</td><td>11071</td><td>2737</td><td>1128</td><td>1645</td><td>5561</td><td>134573.41</td><td>68950.32</td><td>0.5166</td><td>0.2918</td><td>0.2904</td><td>0.1486</td><td>0.6702</td><td>0.0490833</td><td>0.0489441</td><td>0.0610905</td><td>16</td><td>15</td><td>8</td><td>8</td><td>8</td><td>8</td><td>7</td><td>8</td><td>6</td><td>8</td><td>7</td><td>13</td><td>8</td><td>15</td><td>15</td><td>12</td></tr>
    <tr><td>Tops &amp; Tees</td><td>40.97</td><td>22.93</td><td>121151.89</td><td>53364.7</td><td>12000</td><td>2960</td><td>1292</td><td>1783</td><td>5965</td><td>123378.82</td><td>54313.77</td><td>0.4405</td><td>0.3039</td><td>0.2897</td><td>0.1486</td><td>0.6683</td><td>0.045015</td><td>0.0382742</td><td>0.0662168</td><td>20</td><td>16</td><td>9</td><td>14</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>9</td><td>13</td><td>22</td><td>2</td><td>16</td><td>15</td><td>13</td></tr>
    <tr><td>Active</td><td>50.94</td><td>21.35</td><td>117645.45</td><td>68332.26</td><td>8932</td><td>2180</td><td>938</td><td>1362</td><td>4452</td><td>113272.89</td><td>66015.46</td><td>0.5808</td><td>0.3008</td><td>0.288</td><td>0.1525</td><td>0.6713</td><td>0.0437121</td><td>0.0490092</td><td>0.0492873</td><td>15</td><td>18</td><td>11</td><td>7</td><td>11</td><td>11</td><td>10</td><td>10</td><td>11</td><td>10</td><td>9</td><td>6</td><td>4</td><td>21</td><td>7</td><td>11</td></tr>
    <tr><td>Dresses</td><td>84.24</td><td>37.9</td><td>112895.24</td><td>62082.56</td><td>5358</td><td>1316</td><td>549</td><td>792</td><td>2701</td><td>113022.02</td><td>62283.44</td><td>0.5499</td><td>0.2944</td><td>0.2882</td><td>0.1478</td><td>0.6724</td><td>0.0419471</td><td>0.0445268</td><td>0.0295658</td><td>7</td><td>6</td><td>12</td><td>10</td><td>15</td><td>15</td><td>15</td><td>15</td><td>15</td><td>11</td><td>10</td><td>9</td><td>6</td><td>20</td><td>21</td><td>9</td></tr>
    <tr><td>Intimates</td><td>33.75</td><td>17.96</td><td>118381.2</td><td>55321.28</td><td>13423</td><td>3393</td><td>1329</td><td>2044</td><td>6657</td><td>112421.97</td><td>52618.74</td><td>0.4673</td><td>0.2814</td><td>0.2982</td><td>0.1523</td><td>0.6624</td><td>0.0439855</td><td>0.0396775</td><td>0.074069</td><td>22</td><td>21</td><td>10</td><td>13</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>12</td><td>14</td><td>20</td><td>19</td><td>5</td><td>9</td><td>23</td></tr>
    <tr><td>Pants</td><td>59.65</td><td>27.35</td><td>106719.7</td><td>57634.8</td><td>7239</td><td>1823</td><td>713</td><td>1076</td><td>3627</td><td>106167.82</td><td>57611.26</td><td>0.5401</td><td>0.2812</td><td>0.2958</td><td>0.1486</td><td>0.6655</td><td>0.0396526</td><td>0.0413368</td><td>0.0399453</td><td>9</td><td>12</td><td>13</td><td>12</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>12</td><td>10</td><td>21</td><td>10</td><td>15</td><td>16</td></tr>
    <tr><td>Accessories</td><td>42.05</td><td>16.85</td><td>99096.96</td><td>59262.83</td><td>9813</td><td>2384</td><td>967</td><td>1497</td><td>4965</td><td>103385.5</td><td>62000.28</td><td>0.598</td><td>0.2886</td><td>0.2867</td><td>0.1526</td><td>0.6756</td><td>0.0368203</td><td>0.0425044</td><td>0.0541488</td><td>19</td><td>22</td><td>14</td><td>11</td><td>9</td><td>9</td><td>9</td><td>9</td><td>9</td><td>14</td><td>11</td><td>5</td><td>12</td><td>22</td><td>5</td><td>5</td></tr>
    <tr><td>Blazers &amp; Jackets</td><td>90.68</td><td>34.35</td><td>65986.31</td><td>40954.92</td><td>3194</td><td>745</td><td>334</td><td>506</td><td>1609</td><td>76039.51</td><td>47305.1</td><td>0.6207</td><td>0.3095</td><td>0.2772</td><td>0.1584</td><td>0.6835</td><td>0.0245178</td><td>0.0293737</td><td>0.0176247</td><td>5</td><td>8</td><td>15</td><td>15</td><td>22</td><td>22</td><td>22</td><td>20</td><td>21</td><td>15</td><td>15</td><td>1</td><td>1</td><td>26</td><td>1</td><td>1</td></tr>
  </tbody>
</table>

</div>

<h3>Top categories by Lost Profit</h3>

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
  lost_profit_rank ASC
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
    <tr><td>Suits &amp; Sport Coats</td><td>124.74</td><td>50.03</td><td>153543.45</td><td>92034.55</td><td>5176</td><td>1255</td><td>486</td><td>790</td><td>2645</td><td>160577.15</td><td>96066.37</td><td>0.5994</td><td>0.2791</td><td>0.2861</td><td>0.1526</td><td>0.6782</td><td>0.0570503</td><td>0.066009</td><td>0.0285615</td><td>2</td><td>5</td><td>6</td><td>4</td><td>16</td><td>16</td><td>17</td><td>16</td><td>16</td><td>4</td><td>4</td><td>2</td><td>22</td><td>23</td><td>5</td><td>2</td></tr>
    <tr><td>Swim</td><td>57.2</td><td>28.98</td><td>156523.7</td><td>76716.71</td><td>11246</td><td>2772</td><td>1143</td><td>1660</td><td>5671</td><td>159217.24</td><td>78510.83</td><td>0.4901</td><td>0.292</td><td>0.2892</td><td>0.1476</td><td>0.6717</td><td>0.0581577</td><td>0.0550227</td><td>0.0620561</td><td>10</td><td>10</td><td>4</td><td>5</td><td>5</td><td>7</td><td>5</td><td>7</td><td>5</td><td>6</td><td>5</td><td>16</td><td>7</td><td>17</td><td>22</td><td>10</td></tr>
    <tr><td>Fashion Hoodies &amp; Sweatshirts</td><td>54.02</td><td>28.09</td><td>155933.0</td><td>74918.07</td><td>11737</td><td>2951</td><td>1191</td><td>1714</td><td>5881</td><td>159794.53</td><td>76980.63</td><td>0.4805</td><td>0.2875</td><td>0.2944</td><td>0.146</td><td>0.6659</td><td>0.0579382</td><td>0.0537327</td><td>0.0647655</td><td>12</td><td>11</td><td>5</td><td>6</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td><td>5</td><td>6</td><td>17</td><td>14</td><td>12</td><td>23</td><td>14</td></tr>
    <tr><td>Sleep &amp; Lounge</td><td>48.79</td><td>23.64</td><td>132101.2</td><td>68241.52</td><td>11071</td><td>2737</td><td>1128</td><td>1645</td><td>5561</td><td>134573.41</td><td>68950.32</td><td>0.5166</td><td>0.2918</td><td>0.2904</td><td>0.1486</td><td>0.6702</td><td>0.0490833</td><td>0.0489441</td><td>0.0610905</td><td>16</td><td>15</td><td>8</td><td>8</td><td>8</td><td>8</td><td>7</td><td>8</td><td>6</td><td>8</td><td>7</td><td>13</td><td>8</td><td>15</td><td>15</td><td>12</td></tr>
    <tr><td>Shorts</td><td>47.29</td><td>23.69</td><td>136510.82</td><td>68155.43</td><td>11176</td><td>2819</td><td>1130</td><td>1690</td><td>5537</td><td>134644.7</td><td>67078.36</td><td>0.4993</td><td>0.2861</td><td>0.2972</td><td>0.1512</td><td>0.6626</td><td>0.0507217</td><td>0.0488824</td><td>0.0616699</td><td>17</td><td>14</td><td>7</td><td>9</td><td>6</td><td>5</td><td>6</td><td>5</td><td>7</td><td>7</td><td>8</td><td>14</td><td>15</td><td>7</td><td>10</td><td>21</td></tr>
    <tr><td>Active</td><td>50.94</td><td>21.35</td><td>117645.45</td><td>68332.26</td><td>8932</td><td>2180</td><td>938</td><td>1362</td><td>4452</td><td>113272.89</td><td>66015.46</td><td>0.5808</td><td>0.3008</td><td>0.288</td><td>0.1525</td><td>0.6713</td><td>0.0437121</td><td>0.0490092</td><td>0.0492873</td><td>15</td><td>18</td><td>11</td><td>7</td><td>11</td><td>11</td><td>10</td><td>10</td><td>11</td><td>10</td><td>9</td><td>6</td><td>4</td><td>21</td><td>7</td><td>11</td></tr>
    <tr><td>Dresses</td><td>84.24</td><td>37.9</td><td>112895.24</td><td>62082.56</td><td>5358</td><td>1316</td><td>549</td><td>792</td><td>2701</td><td>113022.02</td><td>62283.44</td><td>0.5499</td><td>0.2944</td><td>0.2882</td><td>0.1478</td><td>0.6724</td><td>0.0419471</td><td>0.0445268</td><td>0.0295658</td><td>7</td><td>6</td><td>12</td><td>10</td><td>15</td><td>15</td><td>15</td><td>15</td><td>15</td><td>11</td><td>10</td><td>9</td><td>6</td><td>20</td><td>21</td><td>9</td></tr>
    <tr><td>Accessories</td><td>42.05</td><td>16.85</td><td>99096.96</td><td>59262.83</td><td>9813</td><td>2384</td><td>967</td><td>1497</td><td>4965</td><td>103385.5</td><td>62000.28</td><td>0.598</td><td>0.2886</td><td>0.2867</td><td>0.1526</td><td>0.6756</td><td>0.0368203</td><td>0.0425044</td><td>0.0541488</td><td>19</td><td>22</td><td>14</td><td>11</td><td>9</td><td>9</td><td>9</td><td>9</td><td>9</td><td>14</td><td>11</td><td>5</td><td>12</td><td>22</td><td>5</td><td>5</td></tr>
    <tr><td>Pants</td><td>59.65</td><td>27.35</td><td>106719.7</td><td>57634.8</td><td>7239</td><td>1823</td><td>713</td><td>1076</td><td>3627</td><td>106167.82</td><td>57611.26</td><td>0.5401</td><td>0.2812</td><td>0.2958</td><td>0.1486</td><td>0.6655</td><td>0.0396526</td><td>0.0413368</td><td>0.0399453</td><td>9</td><td>12</td><td>13</td><td>12</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>12</td><td>10</td><td>21</td><td>10</td><td>15</td><td>16</td></tr>
    <tr><td>Tops &amp; Tees</td><td>40.97</td><td>22.93</td><td>121151.89</td><td>53364.7</td><td>12000</td><td>2960</td><td>1292</td><td>1783</td><td>5965</td><td>123378.82</td><td>54313.77</td><td>0.4405</td><td>0.3039</td><td>0.2897</td><td>0.1486</td><td>0.6683</td><td>0.045015</td><td>0.0382742</td><td>0.0662168</td><td>20</td><td>16</td><td>9</td><td>14</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>9</td><td>13</td><td>22</td><td>2</td><td>16</td><td>15</td><td>13</td></tr>
    <tr><td>Intimates</td><td>33.75</td><td>17.96</td><td>118381.2</td><td>55321.28</td><td>13423</td><td>3393</td><td>1329</td><td>2044</td><td>6657</td><td>112421.97</td><td>52618.74</td><td>0.4673</td><td>0.2814</td><td>0.2982</td><td>0.1523</td><td>0.6624</td><td>0.0439855</td><td>0.0396775</td><td>0.074069</td><td>22</td><td>21</td><td>10</td><td>13</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>12</td><td>14</td><td>20</td><td>19</td><td>5</td><td>9</td><td>23</td></tr>
    <tr><td>Blazers &amp; Jackets</td><td>90.68</td><td>34.35</td><td>65986.31</td><td>40954.92</td><td>3194</td><td>745</td><td>334</td><td>506</td><td>1609</td><td>76039.51</td><td>47305.1</td><td>0.6207</td><td>0.3095</td><td>0.2772</td><td>0.1584</td><td>0.6835</td><td>0.0245178</td><td>0.0293737</td><td>0.0176247</td><td>5</td><td>8</td><td>15</td><td>15</td><td>22</td><td>22</td><td>22</td><td>20</td><td>21</td><td>15</td><td>15</td><td>1</td><td>1</td><td>26</td><td>1</td><td>1</td></tr>
  </tbody>
</table>

</div>

<h3>Analytical Insights & Business Recommendations</h3>
<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p>Outerwear & Coats is the clear category leader with $339,222.29 in revenue and $188,050.56 in profit — both #1 overall. However, it achieves this with only 9,028 unit orders (rank #10), meaning it generates far more revenue per unit than any other category thanks to its $146.29 average sale price, the highest across all 26 categories. With a 55.4% profit margin, Outerwear & Coats also ranks above the median for margin efficiency. Its return rate of 27.2% is actually the lowest among all categories, suggesting that customers purchasing outerwear are more deliberate and satisfied with their purchases. Outerwear is the profit engine of the business. Increase internal inventory allocation, marketing spend, and priority fulfillment resources for this category. Ensure stockouts are prevented — each lost outerwear sale costs an average of $146.29 in revenue and $81.30 in profit, far exceeding the cost of overstocking. Additionally, this category's demand likely peaks seasonally before and during winter months, so inventory orders should be front-loaded accordingly.</p>

<p>Intimates leads all categories in unit orders (13,423) but ranks #10 in revenue ($118,381.20) due to its low average sale price of $33.75. Conversely, Suits & Sport Coats ranks #16 in unit orders (5,176) but #4 in profit ($92,034.55) thanks to its $124.74 average sale price and 59.9% profit margin. This pattern — high-volume/low-revenue vs. low-volume/high-revenue — is consistent across the category landscape. Tops & Tees, Intimates, and Fashion Hoodies move the most units but contribute less to profit per order. For high-volume, low-revenue categories (Intimates, Tops & Tees, Shorts), operational efficiency is paramount. Streamline fulfillment for these items — batch picking, simplified packaging, automated label generation — since the margin per unit is thin and any fulfillment inefficiency eats into profit. For low-volume, high-revenue categories (Suits & Sport Coats, Outerwear), invest in premium fulfillment and quality packaging to protect the customer experience on high-value purchases.</p>

<p>Blazers & Jackets commands the highest profit margin (62.1%) across all categories, despite ranking only #15 in revenue and #22 in unit orders. This means every dollar of blazer revenue retains $0.62 in profit — nearly 50% more efficient than bottom-margin categories like Socks (39.7%) or Clothing Sets (38.5%). Accessories (59.8% margin), Socks & Hosiery (59.9%), and Suits & Sport Coats (59.9%) form a tier of high-margin categories. Notably, Socks & Hosiery achieves a top-3 margin despite the lowest average sale price ($16.81) — meaning the cost-to-price ratio is extremely favorable even at low price points. Strategically promote high-margin categories through targeted advertising. A $1 increase in Blazers & Jackets demand yields $0.62 in profit vs. $0.44 for Tops & Tees. Cross-sell blazers and accessories when customers are browsing jeans or outerwear. For Socks & Hosiery, the near-60% margin on a $16 product suggests significant untapped potential if volume can be increased — consider featuring them as add-on recommendations at checkout.</p>

<p>Category return rates are remarkably tight, ranging from 27.2% (Outerwear & Coats) to 31.0% (Blazers & Jackets). The ~4 percentage point spread across all 26 categories suggests that returns are driven more by systemic business factors (e.g., return policy leniency, shipping delays, overall site UX) than by category-specific product quality. Blazers & Jackets has both the highest margin (62.1%) and the highest return rate (31.0%), which may seem contradictory but reflects the category's nature — fit-dependent items where customers may order multiple sizes. Since return rates are uniformly high across all categories (all above 27%), invest in platform-wide return reduction strategies rather than category-specific ones: improved sizing tools, better product photography, clearer product descriptions, and potentially a try-before-you-buy or virtual fitting room feature. A 2-point reduction in the business-wide return rate would compound into significant recovered revenue across all categories.</p>

<p>Categories with the highest revenue also have the highest lost revenue — Outerwear ($322,743.18 lost), Jeans ($319,052.52), Sweaters ($208,115.59). In every case, lost revenue roughly equals or exceeds actual completed revenue, indicating that for every dollar earned, approximately one dollar is lost to returns and cancellations. The near 1:1 ratio of lost revenue to earned revenue across top categories is a critical business health metric. Investigate the split between returns and cancellations — if cancellations dominate, the issue may be upstream (checkout friction, payment processing, stock availability). If returns dominate, the issue is downstream (product quality, sizing, delivery condition). Each root cause requires a different intervention, and the category-level data suggests this is a business-wide issue rather than a category-specific one.</p>

<p>Categories with the most returns (Intimates: 1,329; Jeans: 1,303; Tops & Tees: 1,292) are also the highest-volume categories. The return rate per unit is similar across these categories (~28–30%), meaning the absolute return count is primarily a function of order volume rather than disproportionate quality issues. Rather than flagging high-return categories for quality intervention, track return rates as a percentage and focus on categories where the rate significantly exceeds the business average. Currently, the most productive return-reduction investment would target Blazers & Jackets (31.0%), Tops & Tees (30.4%), and Active (30.1%) — the categories with rates above 30%.</p>

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

<h3>Bottom categories by Profit</h3>

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
  profit_rank DESC
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
    <tr><td>Leggings</td><td>26.79</td><td>16.07</td><td>22032.86</td><td>8796.32</td><td>3246</td><td>804</td><td>345</td><td>500</td><td>1597</td><td>22344.1</td><td>8926.78</td><td>0.3992</td><td>0.3003</td><td>0.2928</td><td>0.154</td><td>0.6651</td><td>0.0081865</td><td>0.0063089</td><td>0.0179116</td><td>24</td><td>23</td><td>23</td><td>24</td><td>21</td><td>21</td><td>21</td><td>21</td><td>22</td><td>23</td><td>24</td><td>23</td><td>5</td><td>13</td><td>4</td><td>17</td></tr>
    <tr><td>Socks &amp; Hosiery</td><td>16.81</td><td>6.75</td><td>15695.27</td><td>9398.63</td><td>3821</td><td>929</td><td>372</td><td>566</td><td>1954</td><td>15784.16</td><td>9453.9</td><td>0.5988</td><td>0.2859</td><td>0.2854</td><td>0.1481</td><td>0.6778</td><td>0.0058317</td><td>0.0067409</td><td>0.0210845</td><td>26</td><td>26</td><td>24</td><td>23</td><td>19</td><td>19</td><td>19</td><td>19</td><td>19</td><td>24</td><td>23</td><td>3</td><td>16</td><td>24</td><td>20</td><td>3</td></tr>
    <tr><td>Socks</td><td>21.13</td><td>12.76</td><td>31572.07</td><td>12517.44</td><td>6329</td><td>1557</td><td>636</td><td>939</td><td>3197</td><td>32927.59</td><td>13032.11</td><td>0.3965</td><td>0.29</td><td>0.2889</td><td>0.1484</td><td>0.6725</td><td>0.0117309</td><td>0.0089777</td><td>0.0349238</td><td>25</td><td>25</td><td>21</td><td>22</td><td>14</td><td>14</td><td>14</td><td>14</td><td>14</td><td>20</td><td>21</td><td>24</td><td>10</td><td>18</td><td>18</td><td>8</td></tr>
    <tr><td>Suits</td><td>117.3</td><td>70.96</td><td>32903.24</td><td>13000.36</td><td>1123</td><td>287</td><td>113</td><td>167</td><td>556</td><td>32368.47</td><td>12778.14</td><td>0.3951</td><td>0.2825</td><td>0.3002</td><td>0.1487</td><td>0.6595</td><td>0.0122255</td><td>0.0093241</td><td>0.0061968</td><td>3</td><td>1</td><td>20</td><td>21</td><td>24</td><td>24</td><td>24</td><td>24</td><td>24</td><td>21</td><td>22</td><td>25</td><td>18</td><td>3</td><td>14</td><td>24</td></tr>
    <tr><td>Skirts</td><td>52.13</td><td>20.8</td><td>26843.42</td><td>16061.8</td><td>2087</td><td>539</td><td>208</td><td>314</td><td>1026</td><td>27751.21</td><td>16709.53</td><td>0.5984</td><td>0.2784</td><td>0.304</td><td>0.1505</td><td>0.6556</td><td>0.0099739</td><td>0.0115198</td><td>0.0115162</td><td>13</td><td>19</td><td>22</td><td>20</td><td>23</td><td>23</td><td>23</td><td>23</td><td>23</td><td>22</td><td>20</td><td>4</td><td>24</td><td>2</td><td>11</td><td>25</td></tr>
    <tr><td>Plus</td><td>39.47</td><td>19.84</td><td>44807.01</td><td>22316.68</td><td>4358</td><td>1070</td><td>436</td><td>646</td><td>2206</td><td>42048.64</td><td>21041.57</td><td>0.4981</td><td>0.2895</td><td>0.2883</td><td>0.1482</td><td>0.6734</td><td>0.0166484</td><td>0.016006</td><td>0.0240477</td><td>21</td><td>20</td><td>19</td><td>19</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>15</td><td>11</td><td>19</td><td>19</td><td>6</td></tr>
    <tr><td>Pants &amp; Capris</td><td>55.37</td><td>29.2</td><td>49331.52</td><td>23421.93</td><td>3392</td><td>864</td><td>350</td><td>481</td><td>1697</td><td>41999.86</td><td>19777.56</td><td>0.4748</td><td>0.2883</td><td>0.2968</td><td>0.1418</td><td>0.6626</td><td>0.0183295</td><td>0.0167987</td><td>0.0187173</td><td>11</td><td>9</td><td>18</td><td>18</td><td>20</td><td>20</td><td>20</td><td>22</td><td>20</td><td>19</td><td>19</td><td>18</td><td>13</td><td>8</td><td>26</td><td>21</td></tr>
    <tr><td>Underwear</td><td>27.21</td><td>12.79</td><td>50614.6</td><td>26861.36</td><td>7505</td><td>1886</td><td>738</td><td>1122</td><td>3759</td><td>51345.06</td><td>27197.18</td><td>0.5307</td><td>0.2813</td><td>0.2955</td><td>0.1495</td><td>0.6659</td><td>0.0188063</td><td>0.0192655</td><td>0.0414131</td><td>23</td><td>24</td><td>17</td><td>17</td><td>12</td><td>12</td><td>12</td><td>12</td><td>12</td><td>17</td><td>17</td><td>11</td><td>20</td><td>11</td><td>13</td><td>14</td></tr>
    <tr><td>Maternity</td><td>51.5</td><td>22.73</td><td>63613.6</td><td>35563.76</td><td>5086</td><td>1232</td><td>531</td><td>741</td><td>2582</td><td>61413.18</td><td>34274.78</td><td>0.5591</td><td>0.3012</td><td>0.2835</td><td>0.1457</td><td>0.677</td><td>0.0236362</td><td>0.025507</td><td>0.0280649</td><td>14</td><td>17</td><td>16</td><td>16</td><td>17</td><td>17</td><td>16</td><td>17</td><td>17</td><td>16</td><td>16</td><td>7</td><td>3</td><td>25</td><td>25</td><td>4</td></tr>
    <tr><td>Blazers &amp; Jackets</td><td>90.68</td><td>34.35</td><td>65986.31</td><td>40954.92</td><td>3194</td><td>745</td><td>334</td><td>506</td><td>1609</td><td>76039.51</td><td>47305.1</td><td>0.6207</td><td>0.3095</td><td>0.2772</td><td>0.1584</td><td>0.6835</td><td>0.0245178</td><td>0.0293737</td><td>0.0176247</td><td>5</td><td>8</td><td>15</td><td>15</td><td>22</td><td>22</td><td>22</td><td>20</td><td>21</td><td>15</td><td>15</td><td>1</td><td>1</td><td>26</td><td>1</td><td>1</td></tr>
    <tr><td>Tops &amp; Tees</td><td>40.97</td><td>22.93</td><td>121151.89</td><td>53364.7</td><td>12000</td><td>2960</td><td>1292</td><td>1783</td><td>5965</td><td>123378.82</td><td>54313.77</td><td>0.4405</td><td>0.3039</td><td>0.2897</td><td>0.1486</td><td>0.6683</td><td>0.045015</td><td>0.0382742</td><td>0.0662168</td><td>20</td><td>16</td><td>9</td><td>14</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>9</td><td>13</td><td>22</td><td>2</td><td>16</td><td>15</td><td>13</td></tr>
    <tr><td>Intimates</td><td>33.75</td><td>17.96</td><td>118381.2</td><td>55321.28</td><td>13423</td><td>3393</td><td>1329</td><td>2044</td><td>6657</td><td>112421.97</td><td>52618.74</td><td>0.4673</td><td>0.2814</td><td>0.2982</td><td>0.1523</td><td>0.6624</td><td>0.0439855</td><td>0.0396775</td><td>0.074069</td><td>22</td><td>21</td><td>10</td><td>13</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>12</td><td>14</td><td>20</td><td>19</td><td>5</td><td>9</td><td>23</td></tr>
    <tr><td>Pants</td><td>59.65</td><td>27.35</td><td>106719.7</td><td>57634.8</td><td>7239</td><td>1823</td><td>713</td><td>1076</td><td>3627</td><td>106167.82</td><td>57611.26</td><td>0.5401</td><td>0.2812</td><td>0.2958</td><td>0.1486</td><td>0.6655</td><td>0.0396526</td><td>0.0413368</td><td>0.0399453</td><td>9</td><td>12</td><td>13</td><td>12</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>12</td><td>10</td><td>21</td><td>10</td><td>15</td><td>16</td></tr>
  </tbody>
</table>

</div>

<h3>Bottom categories by Profit Margin</h3>

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
  profit_margin_rank DESC
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
    <tr><td>Suits</td><td>117.3</td><td>70.96</td><td>32903.24</td><td>13000.36</td><td>1123</td><td>287</td><td>113</td><td>167</td><td>556</td><td>32368.47</td><td>12778.14</td><td>0.3951</td><td>0.2825</td><td>0.3002</td><td>0.1487</td><td>0.6595</td><td>0.0122255</td><td>0.0093241</td><td>0.0061968</td><td>3</td><td>1</td><td>20</td><td>21</td><td>24</td><td>24</td><td>24</td><td>24</td><td>24</td><td>21</td><td>22</td><td>25</td><td>18</td><td>3</td><td>14</td><td>24</td></tr>
    <tr><td>Socks</td><td>21.13</td><td>12.76</td><td>31572.07</td><td>12517.44</td><td>6329</td><td>1557</td><td>636</td><td>939</td><td>3197</td><td>32927.59</td><td>13032.11</td><td>0.3965</td><td>0.29</td><td>0.2889</td><td>0.1484</td><td>0.6725</td><td>0.0117309</td><td>0.0089777</td><td>0.0349238</td><td>25</td><td>25</td><td>21</td><td>22</td><td>14</td><td>14</td><td>14</td><td>14</td><td>14</td><td>20</td><td>21</td><td>24</td><td>10</td><td>18</td><td>18</td><td>8</td></tr>
    <tr><td>Leggings</td><td>26.79</td><td>16.07</td><td>22032.86</td><td>8796.32</td><td>3246</td><td>804</td><td>345</td><td>500</td><td>1597</td><td>22344.1</td><td>8926.78</td><td>0.3992</td><td>0.3003</td><td>0.2928</td><td>0.154</td><td>0.6651</td><td>0.0081865</td><td>0.0063089</td><td>0.0179116</td><td>24</td><td>23</td><td>23</td><td>24</td><td>21</td><td>21</td><td>21</td><td>21</td><td>22</td><td>23</td><td>24</td><td>23</td><td>5</td><td>13</td><td>4</td><td>17</td></tr>
    <tr><td>Tops &amp; Tees</td><td>40.97</td><td>22.93</td><td>121151.89</td><td>53364.7</td><td>12000</td><td>2960</td><td>1292</td><td>1783</td><td>5965</td><td>123378.82</td><td>54313.77</td><td>0.4405</td><td>0.3039</td><td>0.2897</td><td>0.1486</td><td>0.6683</td><td>0.045015</td><td>0.0382742</td><td>0.0662168</td><td>20</td><td>16</td><td>9</td><td>14</td><td>3</td><td>3</td><td>3</td><td>3</td><td>3</td><td>9</td><td>13</td><td>22</td><td>2</td><td>16</td><td>15</td><td>13</td></tr>
    <tr><td>Jeans</td><td>97.76</td><td>52.34</td><td>308764.08</td><td>143520.48</td><td>12655</td><td>3169</td><td>1303</td><td>1955</td><td>6228</td><td>319052.52</td><td>148299.49</td><td>0.4648</td><td>0.2914</td><td>0.2962</td><td>0.1545</td><td>0.6628</td><td>0.1147238</td><td>0.1029357</td><td>0.0698311</td><td>4</td><td>4</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>2</td><td>21</td><td>9</td><td>9</td><td>3</td><td>20</td></tr>
    <tr><td>Intimates</td><td>33.75</td><td>17.96</td><td>118381.2</td><td>55321.28</td><td>13423</td><td>3393</td><td>1329</td><td>2044</td><td>6657</td><td>112421.97</td><td>52618.74</td><td>0.4673</td><td>0.2814</td><td>0.2982</td><td>0.1523</td><td>0.6624</td><td>0.0439855</td><td>0.0396775</td><td>0.074069</td><td>22</td><td>21</td><td>10</td><td>13</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>12</td><td>14</td><td>20</td><td>19</td><td>5</td><td>9</td><td>23</td></tr>
    <tr><td>Jumpsuits &amp; Rompers</td><td>46.79</td><td>24.83</td><td>10339.76</td><td>4897.93</td><td>929</td><td>230</td><td>86</td><td>139</td><td>474</td><td>9496.98</td><td>4463.25</td><td>0.4737</td><td>0.2722</td><td>0.2911</td><td>0.1496</td><td>0.6733</td><td>0.0038418</td><td>0.0035129</td><td>0.0051263</td><td>18</td><td>13</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>19</td><td>25</td><td>14</td><td>12</td><td>7</td></tr>
    <tr><td>Pants &amp; Capris</td><td>55.37</td><td>29.2</td><td>49331.52</td><td>23421.93</td><td>3392</td><td>864</td><td>350</td><td>481</td><td>1697</td><td>41999.86</td><td>19777.56</td><td>0.4748</td><td>0.2883</td><td>0.2968</td><td>0.1418</td><td>0.6626</td><td>0.0183295</td><td>0.0167987</td><td>0.0187173</td><td>11</td><td>9</td><td>18</td><td>18</td><td>20</td><td>20</td><td>20</td><td>22</td><td>20</td><td>19</td><td>19</td><td>18</td><td>13</td><td>8</td><td>26</td><td>21</td></tr>
    <tr><td>Fashion Hoodies &amp; Sweatshirts</td><td>54.02</td><td>28.09</td><td>155933.0</td><td>74918.07</td><td>11737</td><td>2951</td><td>1191</td><td>1714</td><td>5881</td><td>159794.53</td><td>76980.63</td><td>0.4805</td><td>0.2875</td><td>0.2944</td><td>0.146</td><td>0.6659</td><td>0.0579382</td><td>0.0537327</td><td>0.0647655</td><td>12</td><td>11</td><td>5</td><td>6</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td><td>5</td><td>6</td><td>17</td><td>14</td><td>12</td><td>23</td><td>14</td></tr>
    <tr><td>Swim</td><td>57.2</td><td>28.98</td><td>156523.7</td><td>76716.71</td><td>11246</td><td>2772</td><td>1143</td><td>1660</td><td>5671</td><td>159217.24</td><td>78510.83</td><td>0.4901</td><td>0.292</td><td>0.2892</td><td>0.1476</td><td>0.6717</td><td>0.0581577</td><td>0.0550227</td><td>0.0620561</td><td>10</td><td>10</td><td>4</td><td>5</td><td>5</td><td>7</td><td>5</td><td>7</td><td>5</td><td>6</td><td>5</td><td>16</td><td>7</td><td>17</td><td>22</td><td>10</td></tr>
    <tr><td>Plus</td><td>39.47</td><td>19.84</td><td>44807.01</td><td>22316.68</td><td>4358</td><td>1070</td><td>436</td><td>646</td><td>2206</td><td>42048.64</td><td>21041.57</td><td>0.4981</td><td>0.2895</td><td>0.2883</td><td>0.1482</td><td>0.6734</td><td>0.0166484</td><td>0.016006</td><td>0.0240477</td><td>21</td><td>20</td><td>19</td><td>19</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>15</td><td>11</td><td>19</td><td>19</td><td>6</td></tr>
    <tr><td>Shorts</td><td>47.29</td><td>23.69</td><td>136510.82</td><td>68155.43</td><td>11176</td><td>2819</td><td>1130</td><td>1690</td><td>5537</td><td>134644.7</td><td>67078.36</td><td>0.4993</td><td>0.2861</td><td>0.2972</td><td>0.1512</td><td>0.6626</td><td>0.0507217</td><td>0.0488824</td><td>0.0616699</td><td>17</td><td>14</td><td>7</td><td>9</td><td>6</td><td>5</td><td>6</td><td>5</td><td>7</td><td>7</td><td>8</td><td>14</td><td>15</td><td>7</td><td>10</td><td>21</td></tr>
    <tr><td>Sleep &amp; Lounge</td><td>48.79</td><td>23.64</td><td>132101.2</td><td>68241.52</td><td>11071</td><td>2737</td><td>1128</td><td>1645</td><td>5561</td><td>134573.41</td><td>68950.32</td><td>0.5166</td><td>0.2918</td><td>0.2904</td><td>0.1486</td><td>0.6702</td><td>0.0490833</td><td>0.0489441</td><td>0.0610905</td><td>16</td><td>15</td><td>8</td><td>8</td><td>8</td><td>8</td><td>7</td><td>8</td><td>6</td><td>8</td><td>7</td><td>13</td><td>8</td><td>15</td><td>15</td><td>12</td></tr>
    <tr><td>Sweaters</td><td>75.46</td><td>36.32</td><td>213600.63</td><td>110714.83</td><td>11078</td><td>2792</td><td>1081</td><td>1688</td><td>5517</td><td>208115.59</td><td>107697.32</td><td>0.5183</td><td>0.2791</td><td>0.2973</td><td>0.1524</td><td>0.664</td><td>0.0793651</td><td>0.0794068</td><td>0.0611291</td><td>8</td><td>7</td><td>3</td><td>3</td><td>7</td><td>6</td><td>8</td><td>6</td><td>8</td><td>3</td><td>3</td><td>12</td><td>22</td><td>6</td><td>8</td><td>18</td></tr>
  </tbody>
</table>

</div>

<h3>Bottom categories by Unit Orders</h3>

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
  unit_orders_placed_rank DESC
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
    <tr><td>Suits</td><td>117.3</td><td>70.96</td><td>32903.24</td><td>13000.36</td><td>1123</td><td>287</td><td>113</td><td>167</td><td>556</td><td>32368.47</td><td>12778.14</td><td>0.3951</td><td>0.2825</td><td>0.3002</td><td>0.1487</td><td>0.6595</td><td>0.0122255</td><td>0.0093241</td><td>0.0061968</td><td>3</td><td>1</td><td>20</td><td>21</td><td>24</td><td>24</td><td>24</td><td>24</td><td>24</td><td>21</td><td>22</td><td>25</td><td>18</td><td>3</td><td>14</td><td>24</td></tr>
    <tr><td>Skirts</td><td>52.13</td><td>20.8</td><td>26843.42</td><td>16061.8</td><td>2087</td><td>539</td><td>208</td><td>314</td><td>1026</td><td>27751.21</td><td>16709.53</td><td>0.5984</td><td>0.2784</td><td>0.304</td><td>0.1505</td><td>0.6556</td><td>0.0099739</td><td>0.0115198</td><td>0.0115162</td><td>13</td><td>19</td><td>22</td><td>20</td><td>23</td><td>23</td><td>23</td><td>23</td><td>23</td><td>22</td><td>20</td><td>4</td><td>24</td><td>2</td><td>11</td><td>25</td></tr>
    <tr><td>Blazers &amp; Jackets</td><td>90.68</td><td>34.35</td><td>65986.31</td><td>40954.92</td><td>3194</td><td>745</td><td>334</td><td>506</td><td>1609</td><td>76039.51</td><td>47305.1</td><td>0.6207</td><td>0.3095</td><td>0.2772</td><td>0.1584</td><td>0.6835</td><td>0.0245178</td><td>0.0293737</td><td>0.0176247</td><td>5</td><td>8</td><td>15</td><td>15</td><td>22</td><td>22</td><td>22</td><td>20</td><td>21</td><td>15</td><td>15</td><td>1</td><td>1</td><td>26</td><td>1</td><td>1</td></tr>
    <tr><td>Leggings</td><td>26.79</td><td>16.07</td><td>22032.86</td><td>8796.32</td><td>3246</td><td>804</td><td>345</td><td>500</td><td>1597</td><td>22344.1</td><td>8926.78</td><td>0.3992</td><td>0.3003</td><td>0.2928</td><td>0.154</td><td>0.6651</td><td>0.0081865</td><td>0.0063089</td><td>0.0179116</td><td>24</td><td>23</td><td>23</td><td>24</td><td>21</td><td>21</td><td>21</td><td>21</td><td>22</td><td>23</td><td>24</td><td>23</td><td>5</td><td>13</td><td>4</td><td>17</td></tr>
    <tr><td>Pants &amp; Capris</td><td>55.37</td><td>29.2</td><td>49331.52</td><td>23421.93</td><td>3392</td><td>864</td><td>350</td><td>481</td><td>1697</td><td>41999.86</td><td>19777.56</td><td>0.4748</td><td>0.2883</td><td>0.2968</td><td>0.1418</td><td>0.6626</td><td>0.0183295</td><td>0.0167987</td><td>0.0187173</td><td>11</td><td>9</td><td>18</td><td>18</td><td>20</td><td>20</td><td>20</td><td>22</td><td>20</td><td>19</td><td>19</td><td>18</td><td>13</td><td>8</td><td>26</td><td>21</td></tr>
    <tr><td>Socks &amp; Hosiery</td><td>16.81</td><td>6.75</td><td>15695.27</td><td>9398.63</td><td>3821</td><td>929</td><td>372</td><td>566</td><td>1954</td><td>15784.16</td><td>9453.9</td><td>0.5988</td><td>0.2859</td><td>0.2854</td><td>0.1481</td><td>0.6778</td><td>0.0058317</td><td>0.0067409</td><td>0.0210845</td><td>26</td><td>26</td><td>24</td><td>23</td><td>19</td><td>19</td><td>19</td><td>19</td><td>19</td><td>24</td><td>23</td><td>3</td><td>16</td><td>24</td><td>20</td><td>3</td></tr>
    <tr><td>Plus</td><td>39.47</td><td>19.84</td><td>44807.01</td><td>22316.68</td><td>4358</td><td>1070</td><td>436</td><td>646</td><td>2206</td><td>42048.64</td><td>21041.57</td><td>0.4981</td><td>0.2895</td><td>0.2883</td><td>0.1482</td><td>0.6734</td><td>0.0166484</td><td>0.016006</td><td>0.0240477</td><td>21</td><td>20</td><td>19</td><td>19</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>15</td><td>11</td><td>19</td><td>19</td><td>6</td></tr>
    <tr><td>Maternity</td><td>51.5</td><td>22.73</td><td>63613.6</td><td>35563.76</td><td>5086</td><td>1232</td><td>531</td><td>741</td><td>2582</td><td>61413.18</td><td>34274.78</td><td>0.5591</td><td>0.3012</td><td>0.2835</td><td>0.1457</td><td>0.677</td><td>0.0236362</td><td>0.025507</td><td>0.0280649</td><td>14</td><td>17</td><td>16</td><td>16</td><td>17</td><td>17</td><td>16</td><td>17</td><td>17</td><td>16</td><td>16</td><td>7</td><td>3</td><td>25</td><td>25</td><td>4</td></tr>
    <tr><td>Suits &amp; Sport Coats</td><td>124.74</td><td>50.03</td><td>153543.45</td><td>92034.55</td><td>5176</td><td>1255</td><td>486</td><td>790</td><td>2645</td><td>160577.15</td><td>96066.37</td><td>0.5994</td><td>0.2791</td><td>0.2861</td><td>0.1526</td><td>0.6782</td><td>0.0570503</td><td>0.066009</td><td>0.0285615</td><td>2</td><td>5</td><td>6</td><td>4</td><td>16</td><td>16</td><td>17</td><td>16</td><td>16</td><td>4</td><td>4</td><td>2</td><td>22</td><td>23</td><td>5</td><td>2</td></tr>
    <tr><td>Dresses</td><td>84.24</td><td>37.9</td><td>112895.24</td><td>62082.56</td><td>5358</td><td>1316</td><td>549</td><td>792</td><td>2701</td><td>113022.02</td><td>62283.44</td><td>0.5499</td><td>0.2944</td><td>0.2882</td><td>0.1478</td><td>0.6724</td><td>0.0419471</td><td>0.0445268</td><td>0.0295658</td><td>7</td><td>6</td><td>12</td><td>10</td><td>15</td><td>15</td><td>15</td><td>15</td><td>15</td><td>11</td><td>10</td><td>9</td><td>6</td><td>20</td><td>21</td><td>9</td></tr>
    <tr><td>Socks</td><td>21.13</td><td>12.76</td><td>31572.07</td><td>12517.44</td><td>6329</td><td>1557</td><td>636</td><td>939</td><td>3197</td><td>32927.59</td><td>13032.11</td><td>0.3965</td><td>0.29</td><td>0.2889</td><td>0.1484</td><td>0.6725</td><td>0.0117309</td><td>0.0089777</td><td>0.0349238</td><td>25</td><td>25</td><td>21</td><td>22</td><td>14</td><td>14</td><td>14</td><td>14</td><td>14</td><td>20</td><td>21</td><td>24</td><td>10</td><td>18</td><td>18</td><td>8</td></tr>
    <tr><td>Pants</td><td>59.65</td><td>27.35</td><td>106719.7</td><td>57634.8</td><td>7239</td><td>1823</td><td>713</td><td>1076</td><td>3627</td><td>106167.82</td><td>57611.26</td><td>0.5401</td><td>0.2812</td><td>0.2958</td><td>0.1486</td><td>0.6655</td><td>0.0396526</td><td>0.0413368</td><td>0.0399453</td><td>9</td><td>12</td><td>13</td><td>12</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>12</td><td>10</td><td>21</td><td>10</td><td>15</td><td>16</td></tr>
    <tr><td>Underwear</td><td>27.21</td><td>12.79</td><td>50614.6</td><td>26861.36</td><td>7505</td><td>1886</td><td>738</td><td>1122</td><td>3759</td><td>51345.06</td><td>27197.18</td><td>0.5307</td><td>0.2813</td><td>0.2955</td><td>0.1495</td><td>0.6659</td><td>0.0188063</td><td>0.0192655</td><td>0.0414131</td><td>23</td><td>24</td><td>17</td><td>17</td><td>12</td><td>12</td><td>12</td><td>12</td><td>12</td><td>17</td><td>17</td><td>11</td><td>20</td><td>11</td><td>13</td><td>14</td></tr>
  </tbody>
</table>

</div>

<h3>Bottom categories by Return Rate</h3>

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
  return_rate_rank DESC
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
    <tr><td>Jumpsuits &amp; Rompers</td><td>46.79</td><td>24.83</td><td>10339.76</td><td>4897.93</td><td>929</td><td>230</td><td>86</td><td>139</td><td>474</td><td>9496.98</td><td>4463.25</td><td>0.4737</td><td>0.2722</td><td>0.2911</td><td>0.1496</td><td>0.6733</td><td>0.0038418</td><td>0.0035129</td><td>0.0051263</td><td>18</td><td>13</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>25</td><td>19</td><td>25</td><td>14</td><td>12</td><td>7</td></tr>
    <tr><td>Skirts</td><td>52.13</td><td>20.8</td><td>26843.42</td><td>16061.8</td><td>2087</td><td>539</td><td>208</td><td>314</td><td>1026</td><td>27751.21</td><td>16709.53</td><td>0.5984</td><td>0.2784</td><td>0.304</td><td>0.1505</td><td>0.6556</td><td>0.0099739</td><td>0.0115198</td><td>0.0115162</td><td>13</td><td>19</td><td>22</td><td>20</td><td>23</td><td>23</td><td>23</td><td>23</td><td>23</td><td>22</td><td>20</td><td>4</td><td>24</td><td>2</td><td>11</td><td>25</td></tr>
    <tr><td>Suits &amp; Sport Coats</td><td>124.74</td><td>50.03</td><td>153543.45</td><td>92034.55</td><td>5176</td><td>1255</td><td>486</td><td>790</td><td>2645</td><td>160577.15</td><td>96066.37</td><td>0.5994</td><td>0.2791</td><td>0.2861</td><td>0.1526</td><td>0.6782</td><td>0.0570503</td><td>0.066009</td><td>0.0285615</td><td>2</td><td>5</td><td>6</td><td>4</td><td>16</td><td>16</td><td>17</td><td>16</td><td>16</td><td>4</td><td>4</td><td>2</td><td>22</td><td>23</td><td>5</td><td>2</td></tr>
    <tr><td>Sweaters</td><td>75.46</td><td>36.32</td><td>213600.63</td><td>110714.83</td><td>11078</td><td>2792</td><td>1081</td><td>1688</td><td>5517</td><td>208115.59</td><td>107697.32</td><td>0.5183</td><td>0.2791</td><td>0.2973</td><td>0.1524</td><td>0.664</td><td>0.0793651</td><td>0.0794068</td><td>0.0611291</td><td>8</td><td>7</td><td>3</td><td>3</td><td>7</td><td>6</td><td>8</td><td>6</td><td>8</td><td>3</td><td>3</td><td>12</td><td>22</td><td>6</td><td>8</td><td>18</td></tr>
    <tr><td>Pants</td><td>59.65</td><td>27.35</td><td>106719.7</td><td>57634.8</td><td>7239</td><td>1823</td><td>713</td><td>1076</td><td>3627</td><td>106167.82</td><td>57611.26</td><td>0.5401</td><td>0.2812</td><td>0.2958</td><td>0.1486</td><td>0.6655</td><td>0.0396526</td><td>0.0413368</td><td>0.0399453</td><td>9</td><td>12</td><td>13</td><td>12</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>12</td><td>10</td><td>21</td><td>10</td><td>15</td><td>16</td></tr>
    <tr><td>Underwear</td><td>27.21</td><td>12.79</td><td>50614.6</td><td>26861.36</td><td>7505</td><td>1886</td><td>738</td><td>1122</td><td>3759</td><td>51345.06</td><td>27197.18</td><td>0.5307</td><td>0.2813</td><td>0.2955</td><td>0.1495</td><td>0.6659</td><td>0.0188063</td><td>0.0192655</td><td>0.0414131</td><td>23</td><td>24</td><td>17</td><td>17</td><td>12</td><td>12</td><td>12</td><td>12</td><td>12</td><td>17</td><td>17</td><td>11</td><td>20</td><td>11</td><td>13</td><td>14</td></tr>
    <tr><td>Intimates</td><td>33.75</td><td>17.96</td><td>118381.2</td><td>55321.28</td><td>13423</td><td>3393</td><td>1329</td><td>2044</td><td>6657</td><td>112421.97</td><td>52618.74</td><td>0.4673</td><td>0.2814</td><td>0.2982</td><td>0.1523</td><td>0.6624</td><td>0.0439855</td><td>0.0396775</td><td>0.074069</td><td>22</td><td>21</td><td>10</td><td>13</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>12</td><td>14</td><td>20</td><td>19</td><td>5</td><td>9</td><td>23</td></tr>
    <tr><td>Suits</td><td>117.3</td><td>70.96</td><td>32903.24</td><td>13000.36</td><td>1123</td><td>287</td><td>113</td><td>167</td><td>556</td><td>32368.47</td><td>12778.14</td><td>0.3951</td><td>0.2825</td><td>0.3002</td><td>0.1487</td><td>0.6595</td><td>0.0122255</td><td>0.0093241</td><td>0.0061968</td><td>3</td><td>1</td><td>20</td><td>21</td><td>24</td><td>24</td><td>24</td><td>24</td><td>24</td><td>21</td><td>22</td><td>25</td><td>18</td><td>3</td><td>14</td><td>24</td></tr>
    <tr><td>Clothing Sets</td><td>85.82</td><td>52.9</td><td>5539.46</td><td>2131.98</td><td>221</td><td>60</td><td>24</td><td>35</td><td>102</td><td>4604.36</td><td>1726.01</td><td>0.3849</td><td>0.2857</td><td>0.3226</td><td>0.1584</td><td>0.6296</td><td>0.0020582</td><td>0.0015291</td><td>0.0012195</td><td>6</td><td>3</td><td>26</td><td>26</td><td>26</td><td>26</td><td>26</td><td>26</td><td>26</td><td>26</td><td>26</td><td>26</td><td>17</td><td>1</td><td>1</td><td>26</td></tr>
    <tr><td>Socks &amp; Hosiery</td><td>16.81</td><td>6.75</td><td>15695.27</td><td>9398.63</td><td>3821</td><td>929</td><td>372</td><td>566</td><td>1954</td><td>15784.16</td><td>9453.9</td><td>0.5988</td><td>0.2859</td><td>0.2854</td><td>0.1481</td><td>0.6778</td><td>0.0058317</td><td>0.0067409</td><td>0.0210845</td><td>26</td><td>26</td><td>24</td><td>23</td><td>19</td><td>19</td><td>19</td><td>19</td><td>19</td><td>24</td><td>23</td><td>3</td><td>16</td><td>24</td><td>20</td><td>3</td></tr>
    <tr><td>Shorts</td><td>47.29</td><td>23.69</td><td>136510.82</td><td>68155.43</td><td>11176</td><td>2819</td><td>1130</td><td>1690</td><td>5537</td><td>134644.7</td><td>67078.36</td><td>0.4993</td><td>0.2861</td><td>0.2972</td><td>0.1512</td><td>0.6626</td><td>0.0507217</td><td>0.0488824</td><td>0.0616699</td><td>17</td><td>14</td><td>7</td><td>9</td><td>6</td><td>5</td><td>6</td><td>5</td><td>7</td><td>7</td><td>8</td><td>14</td><td>15</td><td>7</td><td>10</td><td>21</td></tr>
    <tr><td>Fashion Hoodies &amp; Sweatshirts</td><td>54.02</td><td>28.09</td><td>155933.0</td><td>74918.07</td><td>11737</td><td>2951</td><td>1191</td><td>1714</td><td>5881</td><td>159794.53</td><td>76980.63</td><td>0.4805</td><td>0.2875</td><td>0.2944</td><td>0.146</td><td>0.6659</td><td>0.0579382</td><td>0.0537327</td><td>0.0647655</td><td>12</td><td>11</td><td>5</td><td>6</td><td>4</td><td>4</td><td>4</td><td>4</td><td>4</td><td>5</td><td>6</td><td>17</td><td>14</td><td>12</td><td>23</td><td>14</td></tr>
    <tr><td>Pants &amp; Capris</td><td>55.37</td><td>29.2</td><td>49331.52</td><td>23421.93</td><td>3392</td><td>864</td><td>350</td><td>481</td><td>1697</td><td>41999.86</td><td>19777.56</td><td>0.4748</td><td>0.2883</td><td>0.2968</td><td>0.1418</td><td>0.6626</td><td>0.0183295</td><td>0.0167987</td><td>0.0187173</td><td>11</td><td>9</td><td>18</td><td>18</td><td>20</td><td>20</td><td>20</td><td>22</td><td>20</td><td>19</td><td>19</td><td>18</td><td>13</td><td>8</td><td>26</td><td>21</td></tr>
    <tr><td>Accessories</td><td>42.05</td><td>16.85</td><td>99096.96</td><td>59262.83</td><td>9813</td><td>2384</td><td>967</td><td>1497</td><td>4965</td><td>103385.5</td><td>62000.28</td><td>0.598</td><td>0.2886</td><td>0.2867</td><td>0.1526</td><td>0.6756</td><td>0.0368203</td><td>0.0425044</td><td>0.0541488</td><td>19</td><td>22</td><td>14</td><td>11</td><td>9</td><td>9</td><td>9</td><td>9</td><td>9</td><td>14</td><td>11</td><td>5</td><td>12</td><td>22</td><td>5</td><td>5</td></tr>
  </tbody>
</table>

</div>

<h3>Bottom categories by Units Returned</h3>

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
  units_returned_rank DESC
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
    <tr><td>Suits</td><td>117.3</td><td>70.96</td><td>32903.24</td><td>13000.36</td><td>1123</td><td>287</td><td>113</td><td>167</td><td>556</td><td>32368.47</td><td>12778.14</td><td>0.3951</td><td>0.2825</td><td>0.3002</td><td>0.1487</td><td>0.6595</td><td>0.0122255</td><td>0.0093241</td><td>0.0061968</td><td>3</td><td>1</td><td>20</td><td>21</td><td>24</td><td>24</td><td>24</td><td>24</td><td>24</td><td>21</td><td>22</td><td>25</td><td>18</td><td>3</td><td>14</td><td>24</td></tr>
    <tr><td>Skirts</td><td>52.13</td><td>20.8</td><td>26843.42</td><td>16061.8</td><td>2087</td><td>539</td><td>208</td><td>314</td><td>1026</td><td>27751.21</td><td>16709.53</td><td>0.5984</td><td>0.2784</td><td>0.304</td><td>0.1505</td><td>0.6556</td><td>0.0099739</td><td>0.0115198</td><td>0.0115162</td><td>13</td><td>19</td><td>22</td><td>20</td><td>23</td><td>23</td><td>23</td><td>23</td><td>23</td><td>22</td><td>20</td><td>4</td><td>24</td><td>2</td><td>11</td><td>25</td></tr>
    <tr><td>Blazers &amp; Jackets</td><td>90.68</td><td>34.35</td><td>65986.31</td><td>40954.92</td><td>3194</td><td>745</td><td>334</td><td>506</td><td>1609</td><td>76039.51</td><td>47305.1</td><td>0.6207</td><td>0.3095</td><td>0.2772</td><td>0.1584</td><td>0.6835</td><td>0.0245178</td><td>0.0293737</td><td>0.0176247</td><td>5</td><td>8</td><td>15</td><td>15</td><td>22</td><td>22</td><td>22</td><td>20</td><td>21</td><td>15</td><td>15</td><td>1</td><td>1</td><td>26</td><td>1</td><td>1</td></tr>
    <tr><td>Leggings</td><td>26.79</td><td>16.07</td><td>22032.86</td><td>8796.32</td><td>3246</td><td>804</td><td>345</td><td>500</td><td>1597</td><td>22344.1</td><td>8926.78</td><td>0.3992</td><td>0.3003</td><td>0.2928</td><td>0.154</td><td>0.6651</td><td>0.0081865</td><td>0.0063089</td><td>0.0179116</td><td>24</td><td>23</td><td>23</td><td>24</td><td>21</td><td>21</td><td>21</td><td>21</td><td>22</td><td>23</td><td>24</td><td>23</td><td>5</td><td>13</td><td>4</td><td>17</td></tr>
    <tr><td>Pants &amp; Capris</td><td>55.37</td><td>29.2</td><td>49331.52</td><td>23421.93</td><td>3392</td><td>864</td><td>350</td><td>481</td><td>1697</td><td>41999.86</td><td>19777.56</td><td>0.4748</td><td>0.2883</td><td>0.2968</td><td>0.1418</td><td>0.6626</td><td>0.0183295</td><td>0.0167987</td><td>0.0187173</td><td>11</td><td>9</td><td>18</td><td>18</td><td>20</td><td>20</td><td>20</td><td>22</td><td>20</td><td>19</td><td>19</td><td>18</td><td>13</td><td>8</td><td>26</td><td>21</td></tr>
    <tr><td>Socks &amp; Hosiery</td><td>16.81</td><td>6.75</td><td>15695.27</td><td>9398.63</td><td>3821</td><td>929</td><td>372</td><td>566</td><td>1954</td><td>15784.16</td><td>9453.9</td><td>0.5988</td><td>0.2859</td><td>0.2854</td><td>0.1481</td><td>0.6778</td><td>0.0058317</td><td>0.0067409</td><td>0.0210845</td><td>26</td><td>26</td><td>24</td><td>23</td><td>19</td><td>19</td><td>19</td><td>19</td><td>19</td><td>24</td><td>23</td><td>3</td><td>16</td><td>24</td><td>20</td><td>3</td></tr>
    <tr><td>Plus</td><td>39.47</td><td>19.84</td><td>44807.01</td><td>22316.68</td><td>4358</td><td>1070</td><td>436</td><td>646</td><td>2206</td><td>42048.64</td><td>21041.57</td><td>0.4981</td><td>0.2895</td><td>0.2883</td><td>0.1482</td><td>0.6734</td><td>0.0166484</td><td>0.016006</td><td>0.0240477</td><td>21</td><td>20</td><td>19</td><td>19</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>18</td><td>15</td><td>11</td><td>19</td><td>19</td><td>6</td></tr>
    <tr><td>Suits &amp; Sport Coats</td><td>124.74</td><td>50.03</td><td>153543.45</td><td>92034.55</td><td>5176</td><td>1255</td><td>486</td><td>790</td><td>2645</td><td>160577.15</td><td>96066.37</td><td>0.5994</td><td>0.2791</td><td>0.2861</td><td>0.1526</td><td>0.6782</td><td>0.0570503</td><td>0.066009</td><td>0.0285615</td><td>2</td><td>5</td><td>6</td><td>4</td><td>16</td><td>16</td><td>17</td><td>16</td><td>16</td><td>4</td><td>4</td><td>2</td><td>22</td><td>23</td><td>5</td><td>2</td></tr>
    <tr><td>Maternity</td><td>51.5</td><td>22.73</td><td>63613.6</td><td>35563.76</td><td>5086</td><td>1232</td><td>531</td><td>741</td><td>2582</td><td>61413.18</td><td>34274.78</td><td>0.5591</td><td>0.3012</td><td>0.2835</td><td>0.1457</td><td>0.677</td><td>0.0236362</td><td>0.025507</td><td>0.0280649</td><td>14</td><td>17</td><td>16</td><td>16</td><td>17</td><td>17</td><td>16</td><td>17</td><td>17</td><td>16</td><td>16</td><td>7</td><td>3</td><td>25</td><td>25</td><td>4</td></tr>
    <tr><td>Dresses</td><td>84.24</td><td>37.9</td><td>112895.24</td><td>62082.56</td><td>5358</td><td>1316</td><td>549</td><td>792</td><td>2701</td><td>113022.02</td><td>62283.44</td><td>0.5499</td><td>0.2944</td><td>0.2882</td><td>0.1478</td><td>0.6724</td><td>0.0419471</td><td>0.0445268</td><td>0.0295658</td><td>7</td><td>6</td><td>12</td><td>10</td><td>15</td><td>15</td><td>15</td><td>15</td><td>15</td><td>11</td><td>10</td><td>9</td><td>6</td><td>20</td><td>21</td><td>9</td></tr>
    <tr><td>Socks</td><td>21.13</td><td>12.76</td><td>31572.07</td><td>12517.44</td><td>6329</td><td>1557</td><td>636</td><td>939</td><td>3197</td><td>32927.59</td><td>13032.11</td><td>0.3965</td><td>0.29</td><td>0.2889</td><td>0.1484</td><td>0.6725</td><td>0.0117309</td><td>0.0089777</td><td>0.0349238</td><td>25</td><td>25</td><td>21</td><td>22</td><td>14</td><td>14</td><td>14</td><td>14</td><td>14</td><td>20</td><td>21</td><td>24</td><td>10</td><td>18</td><td>18</td><td>8</td></tr>
    <tr><td>Pants</td><td>59.65</td><td>27.35</td><td>106719.7</td><td>57634.8</td><td>7239</td><td>1823</td><td>713</td><td>1076</td><td>3627</td><td>106167.82</td><td>57611.26</td><td>0.5401</td><td>0.2812</td><td>0.2958</td><td>0.1486</td><td>0.6655</td><td>0.0396526</td><td>0.0413368</td><td>0.0399453</td><td>9</td><td>12</td><td>13</td><td>12</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>13</td><td>12</td><td>10</td><td>21</td><td>10</td><td>15</td><td>16</td></tr>
    <tr><td>Underwear</td><td>27.21</td><td>12.79</td><td>50614.6</td><td>26861.36</td><td>7505</td><td>1886</td><td>738</td><td>1122</td><td>3759</td><td>51345.06</td><td>27197.18</td><td>0.5307</td><td>0.2813</td><td>0.2955</td><td>0.1495</td><td>0.6659</td><td>0.0188063</td><td>0.0192655</td><td>0.0414131</td><td>23</td><td>24</td><td>17</td><td>17</td><td>12</td><td>12</td><td>12</td><td>12</td><td>12</td><td>17</td><td>17</td><td>11</td><td>20</td><td>11</td><td>13</td><td>14</td></tr>
  </tbody>
</table>

</div>

<h3>Analytical Insights & Business Recommendations</h3>
<div style="margin-top: 12px; padding: 16px; background: #f8f9fa; border-left: 4px solid #2E75B6; border-radius: 4px;">

<p>Clothing Sets is the worst-performing category across nearly every metric: #26 in revenue ($5,539.46), #26 in profit ($2,131.98), #26 in unit orders (221), and notably has the highest cancellation rate (15.8%) and highest completion rate (32.3% — meaning orders that survive cancellation tend to complete). The combination of an $85.82 average sale price with a $52.90 cost leaves a margin of only 38.5%, the lowest of all 26 categories.</p>

<p>Clothing Sets should be considered for discontinuation or dramatic restructuring. With the lowest profit margin, fewest orders, and highest cancellation rate in the business, this category consumes disproportionate operational resources relative to its contribution. If the category is retained, its product cost structure ($52.90 avg cost on an $85.82 price) needs renegotiation — the cost-to-price ratio is over 61%, far above the business average.</p>

<p>Suits rank #24 in unit orders (1,123) and #21 in profit ($13,000.36) despite having the highest average product cost ($70.96) and third-highest average sale price ($117.30). The resulting profit margin of 39.5% is second-lowest, meaning the premium pricing doesn't translate to premium profitability. This is a category where high input costs (likely driven by fabric quality and construction complexity) compress margins despite strong retail pricing. The 28.3% return rate is moderate, so the margin issue is cost-driven rather than return-driven.</p>

<p>Investigate supplier cost structures for the Suits category. At $70.96 average cost, Suits products consume nearly 60.5% of revenue in input costs — compared to 44.5% for Outerwear & Coats, which has an even higher average sale price. Consider whether a shift to suppliers offering better cost-to-quality ratios could preserve the product's market positioning while improving margins toward the 50%+ range.</p>

<p>Socks (6,329 orders, 39.7% margin) and Leggings (3,246 orders, 39.9% margin) represent high-volume categories that contribute minimally to profit due to structurally low margins. Socks generate $31,572.07 in revenue but only $12,517.44 in profit, while Leggings generate $22,032.86 revenue with $8,796.32 profit. Both categories have average costs that consume ~60% of sale price ($12.76/$21.13 for Socks; $16.07/$26.79 for Leggings), leaving thin absolute profit per unit.</p>

<p>Rather than dropping these categories (they drive significant order volume which may increase basket size through cross-selling), optimize their fulfillment costs. Socks and leggings are lightweight, compact items ideal for low-cost shipping. Consider offering multi-pack deals — a 3-pack of socks at a slight per-unit discount still generates more total profit than a single pair while reducing per-order shipping costs.</p>

<p>The five lowest-margin categories are Clothing Sets (38.5%), Suits (39.5%), Socks (39.7%), Leggings (39.9%), and Tops & Tees (44.1%). These span a range of price points ($16.81–$117.30), indicating that low margins aren't purely a function of low prices — Suits have the highest avg cost in the dataset but still achieve poor margins. By contrast, the top margin categories (Blazers & Jackets at 62.1%, Socks & Hosiery at 59.9%, Suits & Sport Coats at 59.9%) demonstrate that similar product types can achieve very different margin profiles depending on cost structure and pricing strategy.</p>

<p>The juxtaposition of Socks (39.7% margin) vs. Socks & Hosiery (59.9% margin) is particularly striking — two closely related categories with a 20-point margin spread. Analyze whether the Socks category can migrate its supplier mix or pricing approach closer to the Socks & Hosiery model. The same logic applies to Suits (39.5%) vs. Suits & Sport Coats (59.9%) — the combined category architecture may benefit from consolidation or realignment.</p>

<p>Even the bottom categories show return rates in the 27–29% range, consistent with the business-wide pattern. Outerwear & Coats has the lowest return rate (27.2%), and Jumpsuits & Rompers has the second-lowest (27.2%), while Skirts (27.8%) and Suits (28.3%) round out the bottom. The consistency reinforces the finding from the Top Categories section: returns appear driven by platform-level factors rather than category-specific issues. No category deviates more than ~4 points from the mean return rate.</p>

<p>This uniformity strengthens the case for business-wide return reduction investment (better sizing tools, enhanced product photography, virtual try-on) rather than category-specific quality interventions. A platform-level improvement that reduces the baseline return rate by even 1–2 percentage points would compound across all 26 categories.</p>

<p>The smallest categories by order volume — Clothing Sets (221), Jumpsuits & Rompers (929), Suits (1,123) — generate relatively few transactions while requiring full catalog management, supplier relationships, and inventory allocation. Evaluate whether the smallest categories justify their operational overhead. Clothing Sets' 221 orders represent just 0.12% of total order volume. If maintaining supplier relationships, inventory space, and marketing for this category costs more than the $2,131.98 in profit it generates, the category should be wound down or consolidated into a broader category (e.g., merged into Active or Outerwear depending on product types).</p>

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

<h3>Top customers by generated Profit</h3>

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
ORDER BY profit_rank ASC
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
    <tr><td>6721</td><td>1303.55</td><td>708.33</td><td>6</td><td>3</td><td>0</td><td>5</td><td>0</td><td>2</td><td>2025-06-17 16:41:11.000000 UTC</td><td>2026-02-18 00:34:38.000000 UTC</td><td>651.77</td><td>2.0</td><td>0.0</td><td>246</td><td>4</td><td>2</td><td>2025</td><td>5093</td><td>12023</td><td>144</td><td>17392</td><td>299</td><td>23890</td><td>8652</td><td>100</td><td>8103</td><td>12023</td><td>18441</td></tr>
    <tr><td>9608</td><td>1348.98</td><td>703.94</td><td>9</td><td>4</td><td>0</td><td>4</td><td>4</td><td>2</td><td>2022-06-02 13:50:09.000000 UTC</td><td>2025-04-28 20:40:37.000000 UTC</td><td>674.49</td><td>2.25</td><td>0.0</td><td>1061</td><td>2</td><td>3</td><td>148</td><td>1</td><td>12023</td><td>435</td><td>164</td><td>299</td><td>65844</td><td>37422</td><td>96</td><td>7921</td><td>12023</td><td>4750</td></tr>
    <tr><td>58672</td><td>1327.33</td><td>688.92</td><td>6</td><td>2</td><td>0</td><td>4</td><td>0</td><td>1</td><td>2021-12-10 12:12:04.000000 UTC</td><td>2025-09-11 22:33:43.000000 UTC</td><td>1327.33</td><td>3.0</td><td>0.0</td><td>1371</td><td>3</td><td>4</td><td>2025</td><td>10016</td><td>12023</td><td>435</td><td>17392</td><td>3350</td><td>69626</td><td>27098</td><td>2</td><td>2670</td><td>12023</td><td>2338</td></tr>
    <tr><td>41139</td><td>1170.01</td><td>645.44</td><td>4</td><td>1</td><td>0</td><td>4</td><td>0</td><td>1</td><td>2025-08-23 10:04:29.000000 UTC</td><td>2025-08-23 10:04:29.000000 UTC</td><td>1170.01</td><td>4.0</td><td>0.0</td><td>0</td><td>5</td><td>5</td><td>8057</td><td>30074</td><td>12023</td><td>435</td><td>17392</td><td>3350</td><td>19645</td><td>28833</td><td>3</td><td>1</td><td>12023</td><td>29774</td></tr>
    <tr><td>31261</td><td>1079.88</td><td>634.52</td><td>4</td><td>1</td><td>0</td><td>4</td><td>0</td><td>1</td><td>2025-11-10 19:44:29.000000 UTC</td><td>2025-11-10 19:44:29.000000 UTC</td><td>1079.88</td><td>4.0</td><td>0.0</td><td>0</td><td>11</td><td>6</td><td>8057</td><td>30074</td><td>12023</td><td>435</td><td>17392</td><td>3350</td><td>14129</td><td>21355</td><td>8</td><td>1</td><td>12023</td><td>29774</td></tr>
    <tr><td>90530</td><td>1039.66</td><td>618.49</td><td>7</td><td>4</td><td>0</td><td>4</td><td>1</td><td>1</td><td>2025-01-12 02:14:23.000000 UTC</td><td>2025-11-14 14:49:28.000000 UTC</td><td>1039.66</td><td>1.75</td><td>0.0</td><td>306</td><td>15</td><td>7</td><td>887</td><td>1</td><td>12023</td><td>435</td><td>6078</td><td>3350</td><td>32497</td><td>20944</td><td>11</td><td>21174</td><td>12023</td><td>16753</td></tr>
    <tr><td>96233</td><td>1142.38</td><td>614.03</td><td>7</td><td>3</td><td>0</td><td>4</td><td>0</td><td>1</td><td>2025-09-02 02:54:09.000000 UTC</td><td>2025-10-28 15:36:32.000000 UTC</td><td>1142.38</td><td>2.33</td><td>0.0</td><td>56</td><td>6</td><td>8</td><td>887</td><td>5093</td><td>12023</td><td>435</td><td>17392</td><td>3350</td><td>19003</td><td>22776</td><td>4</td><td>7675</td><td>12023</td><td>25645</td></tr>
    <tr><td>99402</td><td>1095.49</td><td>605.27</td><td>4</td><td>2</td><td>0</td><td>3</td><td>0</td><td>1</td><td>2024-06-22 08:20:14.000000 UTC</td><td>2025-07-10 07:07:30.000000 UTC</td><td>1095.49</td><td>2.0</td><td>0.0</td><td>383</td><td>9</td><td>9</td><td>8057</td><td>10016</td><td>12023</td><td>2050</td><td>17392</td><td>3350</td><td>41884</td><td>32315</td><td>6</td><td>8103</td><td>12023</td><td>14818</td></tr>
    <tr><td>84673</td><td>1025.41</td><td>599.53</td><td>4</td><td>1</td><td>0</td><td>4</td><td>0</td><td>1</td><td>2025-08-04 04:24:13.000000 UTC</td><td>2025-08-04 04:24:13.000000 UTC</td><td>1025.41</td><td>4.0</td><td>0.0</td><td>0</td><td>21</td><td>10</td><td>8057</td><td>30074</td><td>12023</td><td>435</td><td>17392</td><td>3350</td><td>20891</td><td>30370</td><td>16</td><td>1</td><td>12023</td><td>29774</td></tr>
    <tr><td>3450</td><td>999.0</td><td>594.4</td><td>1</td><td>1</td><td>0</td><td>1</td><td>0</td><td>1</td><td>2026-03-15 16:39:41.000000 UTC</td><td>2026-03-15 16:39:41.000000 UTC</td><td>999.0</td><td>1.0</td><td>0.0</td><td>0</td><td>26</td><td>11</td><td>44959</td><td>30074</td><td>12023</td><td>10609</td><td>17392</td><td>3350</td><td>2807</td><td>3594</td><td>21</td><td>32299</td><td>12023</td><td>29774</td></tr>
    <tr><td>95653</td><td>999.0</td><td>594.4</td><td>5</td><td>4</td><td>0</td><td>1</td><td>0</td><td>1</td><td>2026-03-06 10:36:13.000000 UTC</td><td>2026-03-19 12:12:08.000000 UTC</td><td>999.0</td><td>1.25</td><td>0.0</td><td>13</td><td>26</td><td>11</td><td>4060</td><td>1</td><td>12023</td><td>10609</td><td>17392</td><td>3350</td><td>3948</td><td>1914</td><td>21</td><td>30873</td><td>12023</td><td>28153</td></tr>
    <tr><td>83506</td><td>981.99</td><td>577.49</td><td>3</td><td>1</td><td>0</td><td>3</td><td>0</td><td>1</td><td>2026-03-10 22:20:15.000000 UTC</td><td>2026-03-10 22:20:15.000000 UTC</td><td>981.99</td><td>3.0</td><td>0.0</td><td>0</td><td>33</td><td>13</td><td>15410</td><td>30074</td><td>12023</td><td>2050</td><td>17392</td><td>3350</td><td>3422</td><td>4690</td><td>27</td><td>2670</td><td>12023</td><td>29774</td></tr>
    <tr><td>89840</td><td>1103.0</td><td>576.93</td><td>4</td><td>2</td><td>0</td><td>3</td><td>0</td><td>1</td><td>2024-12-07 22:57:33.000000 UTC</td><td>2026-02-12 19:45:20.000000 UTC</td><td>1103.0</td><td>2.0</td><td>0.0</td><td>432</td><td>8</td><td>14</td><td>8057</td><td>10016</td><td>12023</td><td>2050</td><td>17392</td><td>3350</td><td>34223</td><td>9545</td><td>5</td><td>8103</td><td>12023</td><td>13731</td></tr>
    <tr><td>31643</td><td>1001.52</td><td>572.46</td><td>4</td><td>1</td><td>0</td><td>4</td><td>0</td><td>1</td><td>2025-10-07 02:30:03.000000 UTC</td><td>2025-10-07 02:30:03.000000 UTC</td><td>1001.52</td><td>4.0</td><td>0.0</td><td>0</td><td>25</td><td>15</td><td>8057</td><td>30074</td><td>12023</td><td>435</td><td>17392</td><td>3350</td><td>16629</td><td>24783</td><td>20</td><td>1</td><td>12023</td><td>29774</td></tr>
  </tbody>
</table>

</div>

<h3>Top customers by number of Orders</h3>

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
ORDER BY num_orders_rank ASC
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
    <tr><td>82006</td><td>41.57</td><td>19.76</td><td>7</td><td>4</td><td>4</td><td>2</td><td>1</td><td>2</td><td>2019-12-22 03:50:49.000000 UTC</td><td>2023-11-25 09:42:04.000000 UTC</td><td>20.79</td><td>1.75</td><td>0.6667</td><td>1434</td><td>18224</td><td>18704</td><td>887</td><td>1</td><td>77</td><td>4241</td><td>6078</td><td>299</td><td>78818</td><td>60612</td><td>23868</td><td>21174</td><td>9573</td><td>2016</td></tr>
    <tr><td>5570</td><td>127.5</td><td>70.16</td><td>8</td><td>4</td><td>0</td><td>2</td><td>4</td><td>1</td><td>2020-09-24 16:25:48.000000 UTC</td><td>2025-09-29 08:49:48.000000 UTC</td><td>127.5</td><td>2.0</td><td>0.0</td><td>1831</td><td>6924</td><td>6273</td><td>364</td><td>1</td><td>12023</td><td>4241</td><td>164</td><td>3350</td><td>76388</td><td>25511</td><td>5631</td><td>8103</td><td>12023</td><td>618</td></tr>
    <tr><td>81271</td><td>184.49</td><td>100.8</td><td>5</td><td>4</td><td>0</td><td>2</td><td>0</td><td>2</td><td>2020-09-29 15:33:54.000000 UTC</td><td>2024-06-11 15:18:03.000000 UTC</td><td>92.25</td><td>1.25</td><td>0.0</td><td>1351</td><td>3875</td><td>3473</td><td>4060</td><td>1</td><td>12023</td><td>4241</td><td>17392</td><td>299</td><td>76326</td><td>53853</td><td>8564</td><td>30873</td><td>12023</td><td>2453</td></tr>
    <tr><td>24922</td><td>79.95</td><td>51.25</td><td>4</td><td>4</td><td>1</td><td>1</td><td>1</td><td>1</td><td>2021-11-19 18:54:38.000000 UTC</td><td>2026-03-04 07:51:19.000000 UTC</td><td>79.95</td><td>1.0</td><td>0.5</td><td>1566</td><td>11314</td><td>9090</td><td>8057</td><td>1</td><td>4008</td><td>10609</td><td>6078</td><td>3350</td><td>70031</td><td>6028</td><td>10026</td><td>32299</td><td>10028</td><td>1415</td></tr>
    <tr><td>1284</td><td>29.5</td><td>14.63</td><td>4</td><td>4</td><td>0</td><td>1</td><td>0</td><td>1</td><td>2021-01-29 14:45:09.000000 UTC</td><td>2025-11-30 15:17:14.000000 UTC</td><td>29.5</td><td>1.0</td><td>0.0</td><td>1766</td><td>21440</td><td>21450</td><td>8057</td><td>1</td><td>12023</td><td>10609</td><td>17392</td><td>3350</td><td>74863</td><td>19192</td><td>21079</td><td>32299</td><td>12023</td><td>774</td></tr>
    <tr><td>45906</td><td>116.63</td><td>58.69</td><td>5</td><td>4</td><td>1</td><td>2</td><td>0</td><td>1</td><td>2021-04-09 07:04:02.000000 UTC</td><td>2025-03-19 13:36:35.000000 UTC</td><td>116.63</td><td>1.25</td><td>0.3333</td><td>1440</td><td>7725</td><td>7846</td><td>4060</td><td>1</td><td>4008</td><td>4241</td><td>17392</td><td>3350</td><td>73869</td><td>39969</td><td>6426</td><td>30873</td><td>11257</td><td>1988</td></tr>
    <tr><td>33893</td><td>129.7</td><td>70.76</td><td>6</td><td>4</td><td>0</td><td>3</td><td>1</td><td>1</td><td>2022-02-17 10:57:23.000000 UTC</td><td>2024-11-25 03:46:52.000000 UTC</td><td>129.7</td><td>1.5</td><td>0.0</td><td>1012</td><td>6740</td><td>6200</td><td>2025</td><td>1</td><td>12023</td><td>2050</td><td>6078</td><td>3350</td><td>68156</td><td>46375</td><td>5457</td><td>22716</td><td>12023</td><td>5193</td></tr>
    <tr><td>1199</td><td>0.0</td><td>0.0</td><td>5</td><td>4</td><td>2</td><td>0</td><td>0</td><td>0</td><td>2023-02-19 09:15:41.000000 UTC</td><td>2025-12-06 06:12:55.000000 UTC</td><td></td><td>1.25</td><td>1.0</td><td>1021</td><td>27532</td><td>27532</td><td>4060</td><td>1</td><td>1439</td><td>27532</td><td>17392</td><td>27532</td><td>59011</td><td>18552</td><td>27532</td><td>30873</td><td>1</td><td>5110</td></tr>
    <tr><td>30389</td><td>0.0</td><td>0.0</td><td>4</td><td>4</td><td>1</td><td>0</td><td>1</td><td>0</td><td>2021-10-27 07:13:37.000000 UTC</td><td>2024-10-12 17:03:14.000000 UTC</td><td></td><td>1.0</td><td>1.0</td><td>1081</td><td>27532</td><td>27532</td><td>8057</td><td>1</td><td>4008</td><td>27532</td><td>6078</td><td>27532</td><td>70474</td><td>48470</td><td>27532</td><td>32299</td><td>1</td><td>4566</td></tr>
    <tr><td>24237</td><td>0.0</td><td>0.0</td><td>6</td><td>4</td><td>1</td><td>0</td><td>0</td><td>0</td><td>2020-02-04 20:12:52.000000 UTC</td><td>2024-09-19 22:46:09.000000 UTC</td><td></td><td>1.5</td><td>1.0</td><td>1689</td><td>27532</td><td>27532</td><td>2025</td><td>1</td><td>4008</td><td>27532</td><td>17392</td><td>27532</td><td>78551</td><td>49576</td><td>27532</td><td>22716</td><td>1</td><td>988</td></tr>
    <tr><td>43298</td><td>0.0</td><td>0.0</td><td>7</td><td>4</td><td>1</td><td>0</td><td>0</td><td>0</td><td>2021-10-22 16:09:02.000000 UTC</td><td>2026-01-14 12:24:02.000000 UTC</td><td></td><td>1.75</td><td>1.0</td><td>1545</td><td>27532</td><td>27532</td><td>887</td><td>1</td><td>4008</td><td>27532</td><td>17392</td><td>27532</td><td>70578</td><td>13821</td><td>27532</td><td>21174</td><td>1</td><td>1512</td></tr>
    <tr><td>95470</td><td>222.43</td><td>129.79</td><td>7</td><td>4</td><td>0</td><td>5</td><td>0</td><td>2</td><td>2022-12-12 18:47:31.000000 UTC</td><td>2025-10-19 12:15:13.000000 UTC</td><td>111.22</td><td>1.75</td><td>0.0</td><td>1042</td><td>2602</td><td>2039</td><td>887</td><td>1</td><td>12023</td><td>144</td><td>17392</td><td>299</td><td>60971</td><td>23635</td><td>6746</td><td>21174</td><td>12023</td><td>4931</td></tr>
    <tr><td>18930</td><td>41.99</td><td>21.79</td><td>5</td><td>4</td><td>1</td><td>1</td><td>0</td><td>1</td><td>2019-12-27 22:41:54.000000 UTC</td><td>2025-10-23 08:27:54.000000 UTC</td><td>41.99</td><td>1.25</td><td>0.5</td><td>2127</td><td>18130</td><td>17718</td><td>4060</td><td>1</td><td>4008</td><td>10609</td><td>17392</td><td>3350</td><td>78792</td><td>23269</td><td>17443</td><td>30873</td><td>10028</td><td>162</td></tr>
    <tr><td>40252</td><td>53.45</td><td>25.85</td><td>4</td><td>4</td><td>0</td><td>2</td><td>0</td><td>2</td><td>2020-01-27 14:41:04.000000 UTC</td><td>2025-08-20 18:07:50.000000 UTC</td><td>26.73</td><td>1.0</td><td>0.0</td><td>2032</td><td>15634</td><td>15962</td><td>8057</td><td>1</td><td>12023</td><td>4241</td><td>17392</td><td>299</td><td>78608</td><td>29053</td><td>21737</td><td>32299</td><td>12023</td><td>259</td></tr>
    <tr><td>43911</td><td>0.0</td><td>0.0</td><td>5</td><td>4</td><td>0</td><td>0</td><td>1</td><td>0</td><td>2020-11-19 03:44:57.000000 UTC</td><td>2024-12-06 15:26:31.000000 UTC</td><td></td><td>1.25</td><td></td><td>1478</td><td>27532</td><td>27532</td><td>4060</td><td>1</td><td>12023</td><td>27532</td><td>6078</td><td>27532</td><td>75771</td><td>45798</td><td>27532</td><td>30873</td><td>36927</td><td>1821</td></tr>
  </tbody>
</table>

</div>

<h3>Top customers by number of ordered Items</h3>

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
ORDER BY num_items_ordered_rank ASC
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
    <tr><td>50358</td><td>0.0</td><td>0.0</td><td>13</td><td>4</td><td>0</td><td>0</td><td>4</td><td>0</td><td>2020-04-06 11:47:15.000000 UTC</td><td>2024-06-20 12:43:58.000000 UTC</td><td></td><td>3.25</td><td></td><td>1536</td><td>27532</td><td>27532</td><td>1</td><td>1</td><td>12023</td><td>27532</td><td>164</td><td>27532</td><td>78071</td><td>53463</td><td>27532</td><td>2669</td><td>36927</td><td>1564</td></tr>
    <tr><td>26807</td><td>289.42</td><td>151.0</td><td>12</td><td>4</td><td>0</td><td>8</td><td>2</td><td>2</td><td>2025-07-01 22:52:38.000000 UTC</td><td>2026-02-28 04:27:15.000000 UTC</td><td>144.71</td><td>3.0</td><td>0.0</td><td>242</td><td>1351</td><td>1411</td><td>2</td><td>1</td><td>12023</td><td>3</td><td>2345</td><td>299</td><td>23029</td><td>6821</td><td>4585</td><td>2670</td><td>12023</td><td>18572</td></tr>
    <tr><td>49539</td><td>142.97</td><td>69.84</td><td>12</td><td>4</td><td>0</td><td>4</td><td>5</td><td>1</td><td>2022-12-29 08:39:56.000000 UTC</td><td>2025-12-30 08:46:59.000000 UTC</td><td>142.97</td><td>3.0</td><td>0.0</td><td>1097</td><td>5871</td><td>6315</td><td>2</td><td>1</td><td>12023</td><td>435</td><td>47</td><td>3350</td><td>60512</td><td>15764</td><td>4653</td><td>2670</td><td>12023</td><td>4394</td></tr>
    <tr><td>19412</td><td>15.0</td><td>7.44</td><td>12</td><td>4</td><td>4</td><td>1</td><td>0</td><td>1</td><td>2024-01-14 18:04:56.000000 UTC</td><td>2025-12-19 17:16:33.000000 UTC</td><td>15.0</td><td>3.0</td><td>0.8</td><td>705</td><td>25366</td><td>25547</td><td>2</td><td>1</td><td>77</td><td>10609</td><td>17392</td><td>3350</td><td>48138</td><td>16998</td><td>25322</td><td>2670</td><td>9402</td><td>8870</td></tr>
    <tr><td>26964</td><td>219.97</td><td>120.47</td><td>12</td><td>4</td><td>3</td><td>5</td><td>0</td><td>2</td><td>2022-12-08 23:26:00.000000 UTC</td><td>2025-03-01 03:22:51.000000 UTC</td><td>109.98</td><td>3.0</td><td>0.375</td><td>814</td><td>2665</td><td>2410</td><td>2</td><td>1</td><td>715</td><td>144</td><td>17392</td><td>299</td><td>61069</td><td>41119</td><td>6911</td><td>2670</td><td>11253</td><td>7453</td></tr>
    <tr><td>30487</td><td>360.62</td><td>190.94</td><td>12</td><td>4</td><td>0</td><td>4</td><td>0</td><td>1</td><td>2025-02-04 18:25:16.000000 UTC</td><td>2025-11-24 14:33:51.000000 UTC</td><td>360.62</td><td>3.0</td><td>0.0</td><td>293</td><td>711</td><td>716</td><td>2</td><td>1</td><td>12023</td><td>435</td><td>17392</td><td>3350</td><td>31267</td><td>19903</td><td>477</td><td>2670</td><td>12023</td><td>17110</td></tr>
    <tr><td>7251</td><td>61.99</td><td>33.46</td><td>12</td><td>4</td><td>2</td><td>2</td><td>0</td><td>1</td><td>2022-03-19 18:28:23.000000 UTC</td><td>2024-12-27 03:48:57.000000 UTC</td><td>61.99</td><td>3.0</td><td>0.5</td><td>1014</td><td>13977</td><td>13246</td><td>2</td><td>1</td><td>1439</td><td>4241</td><td>17392</td><td>3350</td><td>67511</td><td>44691</td><td>12889</td><td>2670</td><td>10028</td><td>5176</td></tr>
    <tr><td>50553</td><td>0.0</td><td>0.0</td><td>11</td><td>4</td><td>0</td><td>0</td><td>4</td><td>0</td><td>2023-11-27 05:07:46.000000 UTC</td><td>2024-08-27 08:33:03.000000 UTC</td><td></td><td>2.75</td><td></td><td>274</td><td>27532</td><td>27532</td><td>8</td><td>1</td><td>12023</td><td>27532</td><td>164</td><td>27532</td><td>49889</td><td>50633</td><td>27532</td><td>5658</td><td>36927</td><td>17606</td></tr>
    <tr><td>35024</td><td>155.66</td><td>67.13</td><td>11</td><td>4</td><td>0</td><td>4</td><td>4</td><td>1</td><td>2023-05-02 16:38:49.000000 UTC</td><td>2026-03-18 23:40:22.000000 UTC</td><td>155.66</td><td>2.75</td><td>0.0</td><td>1051</td><td>5158</td><td>6641</td><td>8</td><td>1</td><td>12023</td><td>435</td><td>164</td><td>3350</td><td>56901</td><td>2269</td><td>4013</td><td>5658</td><td>12023</td><td>4847</td></tr>
    <tr><td>19105</td><td>249.55</td><td>136.38</td><td>11</td><td>4</td><td>0</td><td>6</td><td>0</td><td>2</td><td>2022-03-31 16:31:39.000000 UTC</td><td>2025-03-11 16:32:39.000000 UTC</td><td>124.78</td><td>2.75</td><td>0.0</td><td>1076</td><td>1994</td><td>1811</td><td>8</td><td>1</td><td>12023</td><td>41</td><td>17392</td><td>299</td><td>67257</td><td>40472</td><td>5842</td><td>5658</td><td>12023</td><td>4611</td></tr>
    <tr><td>89231</td><td>69.0</td><td>39.74</td><td>11</td><td>4</td><td>4</td><td>1</td><td>2</td><td>1</td><td>2025-10-11 18:13:51.000000 UTC</td><td>2026-03-12 16:56:11.000000 UTC</td><td>69.0</td><td>2.75</td><td>0.8</td><td>152</td><td>12837</td><td>11643</td><td>8</td><td>1</td><td>77</td><td>10609</td><td>2345</td><td>3350</td><td>16298</td><td>4296</td><td>11659</td><td>5658</td><td>9402</td><td>21589</td></tr>
    <tr><td>24294</td><td>0.0</td><td>0.0</td><td>11</td><td>4</td><td>4</td><td>0</td><td>3</td><td>0</td><td>2019-07-28 10:26:40.000000 UTC</td><td>2025-02-13 09:42:17.000000 UTC</td><td></td><td>2.75</td><td>1.0</td><td>2027</td><td>27532</td><td>27532</td><td>8</td><td>1</td><td>77</td><td>27532</td><td>1133</td><td>27532</td><td>79546</td><td>42048</td><td>27532</td><td>5658</td><td>1</td><td>266</td></tr>
    <tr><td>75994</td><td>365.25</td><td>187.72</td><td>11</td><td>4</td><td>0</td><td>5</td><td>4</td><td>2</td><td>2024-11-09 13:54:59.000000 UTC</td><td>2026-01-05 02:12:35.000000 UTC</td><td>182.63</td><td>2.75</td><td>0.0</td><td>422</td><td>687</td><td>753</td><td>8</td><td>1</td><td>12023</td><td>144</td><td>164</td><td>299</td><td>35549</td><td>15065</td><td>2937</td><td>5658</td><td>12023</td><td>13948</td></tr>
    <tr><td>56718</td><td>167.3</td><td>84.9</td><td>11</td><td>3</td><td>4</td><td>4</td><td>0</td><td>1</td><td>2021-12-01 03:13:24.000000 UTC</td><td>2024-06-19 08:28:19.000000 UTC</td><td>167.3</td><td>3.67</td><td>0.5</td><td>931</td><td>4638</td><td>4690</td><td>8</td><td>5093</td><td>77</td><td>435</td><td>17392</td><td>3350</td><td>69815</td><td>53509</td><td>3560</td><td>2543</td><td>10028</td><td>6027</td></tr>
    <tr><td>39235</td><td>0.0</td><td>0.0</td><td>11</td><td>4</td><td>0</td><td>0</td><td>4</td><td>0</td><td>2025-08-16 22:48:53.000000 UTC</td><td>2026-03-06 04:49:00.000000 UTC</td><td></td><td>2.75</td><td></td><td>202</td><td>27532</td><td>27532</td><td>8</td><td>1</td><td>12023</td><td>27532</td><td>164</td><td>27532</td><td>20052</td><td>5679</td><td>27532</td><td>5658</td><td>36927</td><td>19846</td></tr>
  </tbody>
</table>

</div>

<h3>Top customers by Lifetime Days</h3>

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
ORDER BY lifetime_days_rank ASC
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
    <tr><td>21593</td><td>21.75</td><td>11.01</td><td>6</td><td>4</td><td>1</td><td>1</td><td>3</td><td>1</td><td>2019-02-09 09:42:27.000000 UTC</td><td>2025-12-31 05:35:38.000000 UTC</td><td>21.75</td><td>1.5</td><td>0.5</td><td>2517</td><td>23873</td><td>23588</td><td>2025</td><td>1</td><td>4008</td><td>10609</td><td>1133</td><td>3350</td><td>79950</td><td>15640</td><td>23719</td><td>22716</td><td>10028</td><td>1</td></tr>
    <tr><td>2629</td><td>7.0</td><td>4.14</td><td>2</td><td>2</td><td>0</td><td>1</td><td>1</td><td>1</td><td>2019-03-29 20:39:47.000000 UTC</td><td>2026-02-08 04:40:28.000000 UTC</td><td>7.0</td><td>1.0</td><td>0.0</td><td>2508</td><td>27297</td><td>27115</td><td>25303</td><td>10016</td><td>12023</td><td>10609</td><td>6078</td><td>3350</td><td>79881</td><td>10316</td><td>27297</td><td>32299</td><td>12023</td><td>2</td></tr>
    <tr><td>56521</td><td>59.5</td><td>27.25</td><td>2</td><td>2</td><td>0</td><td>1</td><td>0</td><td>1</td><td>2019-05-09 07:19:27.000000 UTC</td><td>2026-03-17 14:13:55.000000 UTC</td><td>59.5</td><td>1.0</td><td>0.0</td><td>2504</td><td>14449</td><td>15408</td><td>25303</td><td>10016</td><td>12023</td><td>10609</td><td>17392</td><td>3350</td><td>79788</td><td>2974</td><td>13387</td><td>32299</td><td>12023</td><td>3</td></tr>
    <tr><td>85000</td><td>12.0</td><td>4.38</td><td>2</td><td>2</td><td>0</td><td>1</td><td>0</td><td>1</td><td>2019-03-31 14:19:41.000000 UTC</td><td>2026-02-01 14:48:34.000000 UTC</td><td>12.0</td><td>1.0</td><td>0.0</td><td>2499</td><td>26255</td><td>27038</td><td>25303</td><td>10016</td><td>12023</td><td>10609</td><td>17392</td><td>3350</td><td>79877</td><td>11253</td><td>26238</td><td>32299</td><td>12023</td><td>4</td></tr>
    <tr><td>13335</td><td>141.68</td><td>77.89</td><td>5</td><td>4</td><td>0</td><td>2</td><td>1</td><td>1</td><td>2019-04-22 16:08:39.000000 UTC</td><td>2026-02-19 18:18:55.000000 UTC</td><td>141.68</td><td>1.25</td><td>0.0</td><td>2495</td><td>5933</td><td>5418</td><td>4060</td><td>1</td><td>12023</td><td>4241</td><td>6078</td><td>3350</td><td>79838</td><td>8366</td><td>4718</td><td>30873</td><td>12023</td><td>5</td></tr>
    <tr><td>40414</td><td>18.96</td><td>8.93</td><td>2</td><td>2</td><td>0</td><td>1</td><td>0</td><td>1</td><td>2019-04-28 01:01:56.000000 UTC</td><td>2026-02-23 07:48:50.000000 UTC</td><td>18.96</td><td>1.0</td><td>0.0</td><td>2493</td><td>24568</td><td>24785</td><td>25303</td><td>10016</td><td>12023</td><td>10609</td><td>17392</td><td>3350</td><td>79817</td><td>7756</td><td>24470</td><td>32299</td><td>12023</td><td>6</td></tr>
    <tr><td>10484</td><td>0.0</td><td>0.0</td><td>5</td><td>4</td><td>1</td><td>0</td><td>1</td><td>0</td><td>2019-04-17 06:55:59.000000 UTC</td><td>2026-02-07 23:25:44.000000 UTC</td><td></td><td>1.25</td><td>1.0</td><td>2488</td><td>27532</td><td>27532</td><td>4060</td><td>1</td><td>4008</td><td>27532</td><td>6078</td><td>27532</td><td>79846</td><td>10346</td><td>27532</td><td>30873</td><td>1</td><td>7</td></tr>
    <tr><td>5544</td><td>257.5</td><td>122.04</td><td>5</td><td>4</td><td>0</td><td>2</td><td>1</td><td>1</td><td>2019-04-30 06:07:29.000000 UTC</td><td>2026-02-20 08:31:48.000000 UTC</td><td>257.5</td><td>1.25</td><td>0.0</td><td>2488</td><td>1832</td><td>2330</td><td>4060</td><td>1</td><td>12023</td><td>4241</td><td>6078</td><td>3350</td><td>79811</td><td>8261</td><td>1273</td><td>30873</td><td>12023</td><td>7</td></tr>
    <tr><td>85692</td><td>243.9</td><td>103.99</td><td>6</td><td>4</td><td>0</td><td>3</td><td>0</td><td>2</td><td>2019-05-20 18:07:33.000000 UTC</td><td>2026-03-11 06:42:46.000000 UTC</td><td>121.95</td><td>1.5</td><td>0.0</td><td>2487</td><td>2105</td><td>3263</td><td>2025</td><td>1</td><td>12023</td><td>2050</td><td>17392</td><td>299</td><td>79774</td><td>4610</td><td>5997</td><td>22716</td><td>12023</td><td>9</td></tr>
    <tr><td>76311</td><td>0.0</td><td>0.0</td><td>7</td><td>4</td><td>0</td><td>0</td><td>2</td><td>0</td><td>2019-05-30 16:34:10.000000 UTC</td><td>2026-03-19 17:50:58.000000 UTC</td><td></td><td>1.75</td><td></td><td>2485</td><td>27532</td><td>27532</td><td>887</td><td>1</td><td>12023</td><td>27532</td><td>2345</td><td>27532</td><td>79734</td><td>1713</td><td>27532</td><td>21174</td><td>36927</td><td>10</td></tr>
    <tr><td>9842</td><td>50.0</td><td>29.0</td><td>7</td><td>4</td><td>0</td><td>1</td><td>4</td><td>1</td><td>2019-05-28 14:07:40.000000 UTC</td><td>2026-03-12 17:50:30.000000 UTC</td><td>50.0</td><td>1.75</td><td>0.0</td><td>2480</td><td>16021</td><td>14730</td><td>887</td><td>1</td><td>12023</td><td>10609</td><td>164</td><td>3350</td><td>79741</td><td>4287</td><td>15152</td><td>21174</td><td>12023</td><td>11</td></tr>
    <tr><td>1380</td><td>0.0</td><td>0.0</td><td>5</td><td>3</td><td>1</td><td>0</td><td>4</td><td>0</td><td>2019-06-13 06:04:10.000000 UTC</td><td>2026-03-17 23:02:23.000000 UTC</td><td></td><td>1.67</td><td>1.0</td><td>2469</td><td>27532</td><td>27532</td><td>4060</td><td>5093</td><td>4008</td><td>27532</td><td>164</td><td>27532</td><td>79699</td><td>2816</td><td>27532</td><td>21954</td><td>1</td><td>12</td></tr>
    <tr><td>23520</td><td>0.0</td><td>0.0</td><td>8</td><td>4</td><td>2</td><td>0</td><td>5</td><td>0</td><td>2019-03-14 17:25:45.000000 UTC</td><td>2025-12-15 19:07:17.000000 UTC</td><td></td><td>2.0</td><td>1.0</td><td>2468</td><td>27532</td><td>27532</td><td>364</td><td>1</td><td>1439</td><td>27532</td><td>47</td><td>27532</td><td>79916</td><td>17464</td><td>27532</td><td>8103</td><td>1</td><td>13</td></tr>
    <tr><td>98794</td><td>0.0</td><td>0.0</td><td>6</td><td>4</td><td>0</td><td>0</td><td>2</td><td>0</td><td>2019-07-02 17:21:36.000000 UTC</td><td>2026-03-19 04:33:52.000000 UTC</td><td></td><td>1.5</td><td></td><td>2452</td><td>27532</td><td>27532</td><td>2025</td><td>1</td><td>12023</td><td>27532</td><td>2345</td><td>27532</td><td>79639</td><td>2156</td><td>27532</td><td>22716</td><td>36927</td><td>14</td></tr>
    <tr><td>7650</td><td>0.0</td><td>0.0</td><td>2</td><td>2</td><td>0</td><td>0</td><td>1</td><td>0</td><td>2019-03-21 00:28:49.000000 UTC</td><td>2025-11-27 19:11:31.000000 UTC</td><td></td><td>1.0</td><td></td><td>2443</td><td>27532</td><td>27532</td><td>25303</td><td>10016</td><td>12023</td><td>27532</td><td>6078</td><td>27532</td><td>79903</td><td>19528</td><td>27532</td><td>32299</td><td>36927</td><td>15</td></tr>
  </tbody>
</table>

</div>

<h3>Top customers by number of returned Items</h3>

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
ORDER BY num_returned_items_rank ASC
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
    <tr><td>60297</td><td>0.0</td><td>0.0</td><td>10</td><td>4</td><td>9</td><td>0</td><td>0</td><td>0</td><td>2025-08-28 17:11:07.000000 UTC</td><td>2026-02-12 16:17:59.000000 UTC</td><td></td><td>2.5</td><td>1.0</td><td>168</td><td>27532</td><td>27532</td><td>49</td><td>1</td><td>1</td><td>27532</td><td>17392</td><td>27532</td><td>19285</td><td>9566</td><td>27532</td><td>5779</td><td>1</td><td>21006</td></tr>
    <tr><td>46813</td><td>79.99</td><td>35.84</td><td>9</td><td>4</td><td>8</td><td>1</td><td>0</td><td>1</td><td>2022-07-24 19:23:52.000000 UTC</td><td>2025-11-07 02:23:59.000000 UTC</td><td>79.99</td><td>2.25</td><td>0.8889</td><td>1202</td><td>11217</td><td>12592</td><td>148</td><td>1</td><td>2</td><td>10609</td><td>17392</td><td>3350</td><td>64638</td><td>21752</td><td>9931</td><td>7921</td><td>9396</td><td>3508</td></tr>
    <tr><td>39503</td><td>0.0</td><td>0.0</td><td>7</td><td>2</td><td>7</td><td>0</td><td>0</td><td>0</td><td>2025-08-17 14:33:03.000000 UTC</td><td>2025-11-29 10:13:11.000000 UTC</td><td></td><td>3.5</td><td>1.0</td><td>104</td><td>27532</td><td>27532</td><td>887</td><td>10016</td><td>3</td><td>27532</td><td>17392</td><td>27532</td><td>20014</td><td>19331</td><td>27532</td><td>2545</td><td>1</td><td>23415</td></tr>
    <tr><td>11354</td><td>0.0</td><td>0.0</td><td>7</td><td>2</td><td>7</td><td>0</td><td>0</td><td>0</td><td>2024-08-21 15:42:09.000000 UTC</td><td>2025-02-19 20:37:16.000000 UTC</td><td></td><td>3.5</td><td>1.0</td><td>182</td><td>27532</td><td>27532</td><td>887</td><td>10016</td><td>3</td><td>27532</td><td>17392</td><td>27532</td><td>39264</td><td>41703</td><td>27532</td><td>2545</td><td>1</td><td>20515</td></tr>
    <tr><td>59640</td><td>0.0</td><td>0.0</td><td>7</td><td>2</td><td>7</td><td>0</td><td>0</td><td>0</td><td>2025-09-07 15:46:55.000000 UTC</td><td>2025-11-24 02:27:39.000000 UTC</td><td></td><td>3.5</td><td>1.0</td><td>78</td><td>27532</td><td>27532</td><td>887</td><td>10016</td><td>3</td><td>27532</td><td>17392</td><td>27532</td><td>18632</td><td>19949</td><td>27532</td><td>2545</td><td>1</td><td>24594</td></tr>
    <tr><td>60349</td><td>0.0</td><td>0.0</td><td>7</td><td>2</td><td>7</td><td>0</td><td>0</td><td>0</td><td>2021-11-13 11:06:48.000000 UTC</td><td>2023-12-12 18:26:45.000000 UTC</td><td></td><td>3.5</td><td>1.0</td><td>759</td><td>27532</td><td>27532</td><td>887</td><td>10016</td><td>3</td><td>27532</td><td>17392</td><td>27532</td><td>70167</td><td>60101</td><td>27532</td><td>2545</td><td>1</td><td>8144</td></tr>
    <tr><td>87895</td><td>0.0</td><td>0.0</td><td>9</td><td>4</td><td>6</td><td>0</td><td>0</td><td>0</td><td>2023-06-22 14:54:45.000000 UTC</td><td>2026-02-07 09:40:03.000000 UTC</td><td></td><td>2.25</td><td>1.0</td><td>961</td><td>27532</td><td>27532</td><td>148</td><td>1</td><td>7</td><td>27532</td><td>17392</td><td>27532</td><td>55359</td><td>10438</td><td>27532</td><td>7921</td><td>1</td><td>5677</td></tr>
    <tr><td>18146</td><td>0.0</td><td>0.0</td><td>6</td><td>3</td><td>6</td><td>0</td><td>0</td><td>0</td><td>2026-02-12 09:30:34.000000 UTC</td><td>2026-03-14 14:52:21.000000 UTC</td><td></td><td>2.0</td><td>1.0</td><td>30</td><td>27532</td><td>27532</td><td>2025</td><td>5093</td><td>7</td><td>27532</td><td>17392</td><td>27532</td><td>6345</td><td>3842</td><td>27532</td><td>8103</td><td>1</td><td>27027</td></tr>
    <tr><td>27201</td><td>42.16</td><td>19.31</td><td>8</td><td>4</td><td>6</td><td>1</td><td>1</td><td>1</td><td>2021-09-25 19:13:29.000000 UTC</td><td>2026-01-30 16:52:20.000000 UTC</td><td>42.16</td><td>2.0</td><td>0.8571</td><td>1588</td><td>18016</td><td>18948</td><td>364</td><td>1</td><td>7</td><td>10609</td><td>6078</td><td>3350</td><td>71073</td><td>11557</td><td>17326</td><td>8103</td><td>9397</td><td>1335</td></tr>
    <tr><td>89971</td><td>0.0</td><td>0.0</td><td>6</td><td>2</td><td>6</td><td>0</td><td>0</td><td>0</td><td>2024-07-22 10:51:16.000000 UTC</td><td>2025-04-03 13:12:55.000000 UTC</td><td></td><td>3.0</td><td>1.0</td><td>255</td><td>27532</td><td>27532</td><td>2025</td><td>10016</td><td>7</td><td>27532</td><td>17392</td><td>27532</td><td>40553</td><td>39024</td><td>27532</td><td>2670</td><td>1</td><td>18195</td></tr>
    <tr><td>39197</td><td>0.0</td><td>0.0</td><td>6</td><td>2</td><td>6</td><td>0</td><td>0</td><td>0</td><td>2025-06-13 09:18:02.000000 UTC</td><td>2026-03-03 06:26:24.000000 UTC</td><td></td><td>3.0</td><td>1.0</td><td>263</td><td>27532</td><td>27532</td><td>2025</td><td>10016</td><td>7</td><td>27532</td><td>17392</td><td>27532</td><td>24144</td><td>6230</td><td>27532</td><td>2670</td><td>1</td><td>17965</td></tr>
    <tr><td>29308</td><td>0.0</td><td>0.0</td><td>6</td><td>2</td><td>6</td><td>0</td><td>0</td><td>0</td><td>2026-03-19 11:15:45.276157 UTC</td><td>2026-03-19 12:01:06.276157 UTC</td><td></td><td>3.0</td><td>1.0</td><td>0</td><td>27532</td><td>27532</td><td>2025</td><td>10016</td><td>7</td><td>27532</td><td>17392</td><td>27532</td><td>1361</td><td>1921</td><td>27532</td><td>2670</td><td>1</td><td>29774</td></tr>
    <tr><td>15921</td><td>0.0</td><td>0.0</td><td>6</td><td>3</td><td>6</td><td>0</td><td>0</td><td>0</td><td>2023-10-07 02:25:11.000000 UTC</td><td>2025-07-06 23:31:11.000000 UTC</td><td></td><td>2.0</td><td>1.0</td><td>638</td><td>27532</td><td>27532</td><td>2025</td><td>5093</td><td>7</td><td>27532</td><td>17392</td><td>27532</td><td>51754</td><td>32558</td><td>27532</td><td>8103</td><td>1</td><td>9887</td></tr>
    <tr><td>99384</td><td>0.0</td><td>0.0</td><td>7</td><td>4</td><td>6</td><td>0</td><td>0</td><td>0</td><td>2023-06-13 07:11:13.000000 UTC</td><td>2025-09-14 09:21:52.000000 UTC</td><td></td><td>1.75</td><td>1.0</td><td>824</td><td>27532</td><td>27532</td><td>887</td><td>1</td><td>7</td><td>27532</td><td>17392</td><td>27532</td><td>55640</td><td>26886</td><td>27532</td><td>21174</td><td>1</td><td>7337</td></tr>
    <tr><td>50833</td><td>0.0</td><td>0.0</td><td>6</td><td>2</td><td>6</td><td>0</td><td>0</td><td>0</td><td>2020-06-11 20:41:30.000000 UTC</td><td>2024-11-29 01:34:57.000000 UTC</td><td></td><td>3.0</td><td>1.0</td><td>1632</td><td>27532</td><td>27532</td><td>2025</td><td>10016</td><td>7</td><td>27532</td><td>17392</td><td>27532</td><td>77512</td><td>46165</td><td>27532</td><td>2670</td><td>1</td><td>1171</td></tr>
  </tbody>
</table>

</div>

<h3>Top customers by number of cancelled Items</h3>

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
ORDER BY num_cancelled_items_rank ASC
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
    <tr><td>52450</td><td>0.0</td><td>0.0</td><td>10</td><td>4</td><td>2</td><td>0</td><td>8</td><td>0</td><td>2022-03-11 13:56:16.000000 UTC</td><td>2024-02-04 12:21:46.000000 UTC</td><td></td><td>2.5</td><td>1.0</td><td>695</td><td>27532</td><td>27532</td><td>49</td><td>1</td><td>1439</td><td>27532</td><td>1</td><td>27532</td><td>67677</td><td>58458</td><td>27532</td><td>5779</td><td>1</td><td>9009</td></tr>
    <tr><td>888</td><td>0.0</td><td>0.0</td><td>8</td><td>3</td><td>0</td><td>0</td><td>8</td><td>0</td><td>2024-06-16 06:47:35.000000 UTC</td><td>2026-03-07 11:36:20.000000 UTC</td><td></td><td>2.67</td><td></td><td>629</td><td>27532</td><td>27532</td><td>364</td><td>5093</td><td>12023</td><td>27532</td><td>1</td><td>27532</td><td>42169</td><td>5387</td><td>27532</td><td>5697</td><td>36927</td><td>10055</td></tr>
    <tr><td>66118</td><td>0.0</td><td>0.0</td><td>8</td><td>2</td><td>0</td><td>0</td><td>8</td><td>0</td><td>2021-01-07 00:01:40.000000 UTC</td><td>2025-04-19 10:09:06.000000 UTC</td><td></td><td>4.0</td><td></td><td>1563</td><td>27532</td><td>27532</td><td>364</td><td>10016</td><td>12023</td><td>27532</td><td>1</td><td>27532</td><td>75145</td><td>38045</td><td>27532</td><td>1</td><td>36927</td><td>1430</td></tr>
    <tr><td>56460</td><td>0.0</td><td>0.0</td><td>8</td><td>2</td><td>0</td><td>0</td><td>8</td><td>0</td><td>2023-12-21 22:29:09.000000 UTC</td><td>2025-10-05 22:53:44.000000 UTC</td><td></td><td>4.0</td><td></td><td>654</td><td>27532</td><td>27532</td><td>364</td><td>10016</td><td>12023</td><td>27532</td><td>1</td><td>27532</td><td>49020</td><td>24914</td><td>27532</td><td>1</td><td>36927</td><td>9616</td></tr>
    <tr><td>88430</td><td>16.0</td><td>8.67</td><td>8</td><td>4</td><td>0</td><td>1</td><td>7</td><td>1</td><td>2025-01-31 20:12:54.000000 UTC</td><td>2026-02-09 12:48:47.000000 UTC</td><td>16.0</td><td>2.0</td><td>0.0</td><td>374</td><td>25144</td><td>24938</td><td>364</td><td>1</td><td>12023</td><td>10609</td><td>5</td><td>3350</td><td>31481</td><td>10094</td><td>25091</td><td>8103</td><td>12023</td><td>15040</td></tr>
    <tr><td>76677</td><td>0.0</td><td>0.0</td><td>7</td><td>2</td><td>0</td><td>0</td><td>7</td><td>0</td><td>2019-03-21 01:21:25.000000 UTC</td><td>2020-11-24 22:01:33.000000 UTC</td><td></td><td>3.5</td><td></td><td>614</td><td>27532</td><td>27532</td><td>887</td><td>10016</td><td>12023</td><td>27532</td><td>5</td><td>27532</td><td>79902</td><td>77969</td><td>27532</td><td>2545</td><td>36927</td><td>10299</td></tr>
    <tr><td>35419</td><td>12.95</td><td>6.29</td><td>9</td><td>4</td><td>0</td><td>1</td><td>7</td><td>1</td><td>2022-07-02 09:04:30.000000 UTC</td><td>2025-05-10 12:07:44.000000 UTC</td><td>12.95</td><td>2.25</td><td>0.0</td><td>1043</td><td>26101</td><td>26081</td><td>148</td><td>1</td><td>12023</td><td>10609</td><td>5</td><td>3350</td><td>65171</td><td>36648</td><td>26077</td><td>7921</td><td>12023</td><td>4923</td></tr>
    <tr><td>50844</td><td>0.0</td><td>0.0</td><td>9</td><td>4</td><td>0</td><td>0</td><td>7</td><td>0</td><td>2022-09-13 18:27:12.000000 UTC</td><td>2025-05-23 12:09:09.000000 UTC</td><td></td><td>2.25</td><td></td><td>983</td><td>27532</td><td>27532</td><td>148</td><td>1</td><td>12023</td><td>27532</td><td>5</td><td>27532</td><td>63329</td><td>35759</td><td>27532</td><td>7921</td><td>36927</td><td>5453</td></tr>
    <tr><td>6014</td><td>147.97</td><td>88.15</td><td>10</td><td>4</td><td>0</td><td>2</td><td>7</td><td>1</td><td>2024-09-30 18:03:34.000000 UTC</td><td>2026-03-02 09:47:36.000000 UTC</td><td>147.97</td><td>2.5</td><td>0.0</td><td>518</td><td>5625</td><td>4405</td><td>49</td><td>1</td><td>12023</td><td>4241</td><td>5</td><td>3350</td><td>37438</td><td>6389</td><td>4439</td><td>5779</td><td>12023</td><td>11983</td></tr>
    <tr><td>20234</td><td>0.0</td><td>0.0</td><td>7</td><td>2</td><td>0</td><td>0</td><td>7</td><td>0</td><td>2024-11-03 06:08:40.000000 UTC</td><td>2025-09-13 09:32:50.000000 UTC</td><td></td><td>3.5</td><td></td><td>314</td><td>27532</td><td>27532</td><td>887</td><td>10016</td><td>12023</td><td>27532</td><td>5</td><td>27532</td><td>35827</td><td>26962</td><td>27532</td><td>2545</td><td>36927</td><td>16548</td></tr>
    <tr><td>51664</td><td>0.0</td><td>0.0</td><td>8</td><td>4</td><td>1</td><td>0</td><td>7</td><td>0</td><td>2019-12-14 08:09:34.000000 UTC</td><td>2025-03-09 18:05:06.000000 UTC</td><td></td><td>2.0</td><td>1.0</td><td>1912</td><td>27532</td><td>27532</td><td>364</td><td>1</td><td>4008</td><td>27532</td><td>5</td><td>27532</td><td>78884</td><td>40590</td><td>27532</td><td>8103</td><td>1</td><td>433</td></tr>
    <tr><td>61360</td><td>0.0</td><td>0.0</td><td>8</td><td>4</td><td>0</td><td>0</td><td>7</td><td>0</td><td>2023-03-30 09:36:45.000000 UTC</td><td>2025-04-21 01:54:53.000000 UTC</td><td></td><td>2.0</td><td></td><td>753</td><td>27532</td><td>27532</td><td>364</td><td>1</td><td>12023</td><td>27532</td><td>5</td><td>27532</td><td>57877</td><td>37937</td><td>27532</td><td>8103</td><td>36927</td><td>8228</td></tr>
    <tr><td>89403</td><td>0.0</td><td>0.0</td><td>7</td><td>4</td><td>0</td><td>0</td><td>7</td><td>0</td><td>2024-01-08 04:53:32.000000 UTC</td><td>2025-03-18 04:13:22.000000 UTC</td><td></td><td>1.75</td><td></td><td>435</td><td>27532</td><td>27532</td><td>887</td><td>1</td><td>12023</td><td>27532</td><td>5</td><td>27532</td><td>48359</td><td>40060</td><td>27532</td><td>21174</td><td>36927</td><td>13677</td></tr>
    <tr><td>4384</td><td>0.0</td><td>0.0</td><td>7</td><td>3</td><td>0</td><td>0</td><td>6</td><td>0</td><td>2021-11-10 18:10:24.000000 UTC</td><td>2023-09-13 17:23:58.000000 UTC</td><td></td><td>2.33</td><td></td><td>672</td><td>27532</td><td>27532</td><td>887</td><td>5093</td><td>12023</td><td>27532</td><td>14</td><td>27532</td><td>70211</td><td>62732</td><td>27532</td><td>7675</td><td>36927</td><td>9363</td></tr>
    <tr><td>89847</td><td>286.0</td><td>155.13</td><td>9</td><td>4</td><td>0</td><td>2</td><td>6</td><td>1</td><td>2022-10-25 12:13:38.000000 UTC</td><td>2026-01-14 13:40:30.000000 UTC</td><td>286.0</td><td>2.25</td><td>0.0</td><td>1177</td><td>1398</td><td>1324</td><td>148</td><td>1</td><td>12023</td><td>4241</td><td>14</td><td>3350</td><td>62260</td><td>13811</td><td>957</td><td>7921</td><td>12023</td><td>3692</td></tr>
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

<h3>Customer Ages</h3>

<pre><code class="language-sql">SELECT
  CONCAT(CAST(FLOOR(u.age / 10) * 10 AS STRING), '-', CAST(FLOOR(u.age / 10) * 10 + 9 AS STRING)) AS age_segment,
  MIN(u.age) AS min_age,
  MAX(u.age) AS max_age,
  COUNT(DISTINCT u.id) AS num_customers,
  COUNT(oi.id) AS units_sold,
  ROUND(SUM(oi.sale_price), 2) AS revenue,
  ROUND(SUM(oi.sale_price) - SUM(p.cost), 2) AS profit
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
  age_segment
ORDER BY
  age_segment;</code></pre>

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

<table>
  <thead>
    <tr>
      <th>age_segment</th>
      <th>min_age</th>
      <th>max_age</th>
      <th>num_customers</th>
      <th>units_sold</th>
      <th>revenue</th>
      <th>profit</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>10-19</td><td>12</td><td>19</td><td>8928</td><td>18359</td><td>1098311.66</td><td>570248.54</td></tr>
    <tr><td>20-29</td><td>20</td><td>29</td><td>11058</td><td>22694</td><td>1353558.57</td><td>702335.54</td></tr>
    <tr><td>30-39</td><td>30</td><td>39</td><td>11110</td><td>22874</td><td>1368064.11</td><td>709341.37</td></tr>
    <tr><td>40-49</td><td>40</td><td>49</td><td>11213</td><td>23025</td><td>1374079.88</td><td>712808.13</td></tr>
    <tr><td>50-59</td><td>50</td><td>59</td><td>11381</td><td>23401</td><td>1382324.6</td><td>716881.16</td></tr>
    <tr><td>60-69</td><td>60</td><td>69</td><td>11250</td><td>23322</td><td>1389785.0</td><td>720863.76</td></tr>
    <tr><td>70-79</td><td>70</td><td>70</td><td>1109</td><td>2156</td><td>127107.71</td><td>65796.11</td></tr>
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

</details>
<details>
  <summary><strong>Conclusion</strong></summary>

  <div style="margin-top: 12px;"></div>

</details>
