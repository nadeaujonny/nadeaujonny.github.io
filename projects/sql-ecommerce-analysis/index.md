---
layout: default
title: E-commerce Revenue & Returns Analysis (SQL)
description: "Analyzing 1M+ e-commerce orders in BigQuery using advanced SQL — CTEs, window functions, and time-series logic — to identify revenue drivers, return risk, and profit opportunities."
---

<a href="/projects/" class="back-to-projects btn">← Back to Projects</a>

# E-commerce Revenue & Returns Analysis (SQL)

> This project analyzes sales and returns activity from the BigQuery **thelook_ecommerce** dataset to identify revenue drivers, profit concentration, return-risk patterns, and actionable operational insights using advanced SQL.

---

<details>
  <summary><strong>Introduction</strong></summary>

  <div style="margin-top: 12px;"></div>

</details>
<details>
  <summary><strong>Top Products</strong></summary>

  <div style="margin-top: 12px;"></div>

  <p><strong>Top products by Revenue</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>ASCIS Cushion Low Socks (Pack of 3)</td>
          <td>ASICS</td>
          <td>Active</td>
          <td>903.0</td>
          <td>373.84</td>
          <td>3612.0</td>
          <td>2116.63</td>
          <td>11</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>6</td>
          <td>903.0</td>
          <td>529.16</td>
          <td>0.586</td>
          <td>0.0</td>
          <td>0.4</td>
          <td>0.0909</td>
          <td>0.6</td>
          <td>0.001338</td>
          <td>0.0015127</td>
          <td>6.07e-05</td>
          <td>5</td>
          <td>28</td>
          <td>1</td>
          <td>1</td>
          <td>1161</td>
          <td>776</td>
          <td>13463</td>
          <td>7029</td>
          <td>1398</td>
          <td>155</td>
          <td>142</td>
          <td>3719</td>
          <td>13463</td>
          <td>7482</td>
          <td>16872</td>
          <td>16953</td>
        </tr>
        <tr>
          <td>The North Face Women&#x27;s S-XL Oso Jacket</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>378.36</td>
          <td>3612.0</td>
          <td>2098.57</td>
          <td>10</td>
          <td>4</td>
          <td>1</td>
          <td>1</td>
          <td>4</td>
          <td>1806.0</td>
          <td>1049.29</td>
          <td>0.581</td>
          <td>0.2</td>
          <td>0.4444</td>
          <td>0.1</td>
          <td>0.5</td>
          <td>0.001338</td>
          <td>0.0014998</td>
          <td>5.52e-05</td>
          <td>5</td>
          <td>25</td>
          <td>1</td>
          <td>2</td>
          <td>1962</td>
          <td>776</td>
          <td>3978</td>
          <td>7029</td>
          <td>6105</td>
          <td>22</td>
          <td>24</td>
          <td>4209</td>
          <td>12637</td>
          <td>6492</td>
          <td>16366</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>Spyder Women&#x27;s Jesst In Time Jacket</td>
          <td>Spyder</td>
          <td>Outerwear &amp; Coats</td>
          <td>650.0</td>
          <td>295.75</td>
          <td>3250.0</td>
          <td>1771.25</td>
          <td>10</td>
          <td>5</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>2600.0</td>
          <td>1417.0</td>
          <td>0.545</td>
          <td>0.4444</td>
          <td>0.5</td>
          <td>0.0</td>
          <td>0.1667</td>
          <td>0.0012039</td>
          <td>0.0012659</td>
          <td>5.52e-05</td>
          <td>52</td>
          <td>50</td>
          <td>3</td>
          <td>4</td>
          <td>1962</td>
          <td>251</td>
          <td>30</td>
          <td>17458</td>
          <td>23197</td>
          <td>7</td>
          <td>7</td>
          <td>8121</td>
          <td>8264</td>
          <td>3269</td>
          <td>17458</td>
          <td>27059</td>
        </tr>
        <tr>
          <td>Bergama Natural Raccoon Hooded Stroller - - Multicolor</td>
          <td>Bergama</td>
          <td>Outerwear &amp; Coats</td>
          <td>749.99</td>
          <td>306.75</td>
          <td>2999.96</td>
          <td>1772.98</td>
          <td>10</td>
          <td>4</td>
          <td>1</td>
          <td>0</td>
          <td>5</td>
          <td>749.99</td>
          <td>443.24</td>
          <td>0.591</td>
          <td>0.2</td>
          <td>0.4</td>
          <td>0.0</td>
          <td>0.5556</td>
          <td>0.0011113</td>
          <td>0.0012671</td>
          <td>5.52e-05</td>
          <td>40</td>
          <td>43</td>
          <td>4</td>
          <td>3</td>
          <td>1962</td>
          <td>776</td>
          <td>3978</td>
          <td>17458</td>
          <td>3026</td>
          <td>267</td>
          <td>224</td>
          <td>3279</td>
          <td>12637</td>
          <td>7482</td>
          <td>17458</td>
          <td>19270</td>
        </tr>
        <tr>
          <td>Woolrich Arctic Parka DF</td>
          <td>Woolrich</td>
          <td>Outerwear &amp; Coats</td>
          <td>990.0</td>
          <td>478.17</td>
          <td>2970.0</td>
          <td>1535.49</td>
          <td>12</td>
          <td>3</td>
          <td>2</td>
          <td>1</td>
          <td>6</td>
          <td>2970.0</td>
          <td>1535.49</td>
          <td>0.517</td>
          <td>0.4</td>
          <td>0.2727</td>
          <td>0.0833</td>
          <td>0.6667</td>
          <td>0.0011002</td>
          <td>0.0010974</td>
          <td>6.62e-05</td>
          <td>3</td>
          <td>6</td>
          <td>5</td>
          <td>6</td>
          <td>694</td>
          <td>2358</td>
          <td>844</td>
          <td>7029</td>
          <td>1398</td>
          <td>4</td>
          <td>4</td>
          <td>10735</td>
          <td>8312</td>
          <td>14284</td>
          <td>17144</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Joseph Abboud Men&#x27;s Two-button Side Vent Sport Coat</td>
          <td>Joseph Abboud</td>
          <td>Suits &amp; Sport Coats</td>
          <td>264.0</td>
          <td>101.9</td>
          <td>2904.0</td>
          <td>1759.82</td>
          <td>30</td>
          <td>11</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>1056.0</td>
          <td>656.57</td>
          <td>0.606</td>
          <td>0.1538</td>
          <td>0.3929</td>
          <td>0.0667</td>
          <td>0.5769</td>
          <td>0.0010758</td>
          <td>0.0012577</td>
          <td>0.0001655</td>
          <td>430</td>
          <td>734</td>
          <td>6</td>
          <td>5</td>
          <td>7</td>
          <td>3</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>112</td>
          <td>91</td>
          <td>2144</td>
          <td>13388</td>
          <td>9081</td>
          <td>17408</td>
          <td>18610</td>
        </tr>
        <tr>
          <td>AIR JORDAN DOMINATE SHORTS MENS 465071-100</td>
          <td>Jordan</td>
          <td>Shorts</td>
          <td>903.0</td>
          <td>454.21</td>
          <td>2709.0</td>
          <td>1346.37</td>
          <td>5</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>2</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.497</td>
          <td>0.0</td>
          <td>0.6</td>
          <td>0.0</td>
          <td>0.4</td>
          <td>0.0010035</td>
          <td>0.0009622</td>
          <td>2.76e-05</td>
          <td>5</td>
          <td>8</td>
          <td>7</td>
          <td>9</td>
          <td>16887</td>
          <td>2358</td>
          <td>13463</td>
          <td>17458</td>
          <td>17069</td>
          <td>22642</td>
          <td>22642</td>
          <td>12874</td>
          <td>13463</td>
          <td>2189</td>
          <td>17458</td>
          <td>23875</td>
        </tr>
        <tr>
          <td>The North Face Denali Down Mens Jacket 2013</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>436.15</td>
          <td>2709.0</td>
          <td>1400.55</td>
          <td>13</td>
          <td>3</td>
          <td>2</td>
          <td>2</td>
          <td>6</td>
          <td>3612.0</td>
          <td>1867.4</td>
          <td>0.517</td>
          <td>0.4</td>
          <td>0.2727</td>
          <td>0.1538</td>
          <td>0.6667</td>
          <td>0.0010035</td>
          <td>0.001001</td>
          <td>7.17e-05</td>
          <td>5</td>
          <td>10</td>
          <td>7</td>
          <td>7</td>
          <td>423</td>
          <td>2358</td>
          <td>844</td>
          <td>2100</td>
          <td>1398</td>
          <td>2</td>
          <td>3</td>
          <td>10735</td>
          <td>8312</td>
          <td>14284</td>
          <td>12634</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Diesel Men&#x27;s Lagnum Leather Jacket</td>
          <td>Diesel</td>
          <td>Outerwear &amp; Coats</td>
          <td>598.0</td>
          <td>267.9</td>
          <td>2392.0</td>
          <td>1320.38</td>
          <td>7</td>
          <td>4</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>1196.0</td>
          <td>660.19</td>
          <td>0.552</td>
          <td>0.2</td>
          <td>0.6667</td>
          <td>0.1429</td>
          <td>0.2</td>
          <td>0.0008861</td>
          <td>0.0009437</td>
          <td>3.86e-05</td>
          <td>57</td>
          <td>56</td>
          <td>9</td>
          <td>10</td>
          <td>8625</td>
          <td>776</td>
          <td>3978</td>
          <td>7029</td>
          <td>23197</td>
          <td>92</td>
          <td>89</td>
          <td>7373</td>
          <td>12637</td>
          <td>1185</td>
          <td>12706</td>
          <td>26859</td>
        </tr>
        <tr>
          <td>Nobis Merideth Parka</td>
          <td>Nobis</td>
          <td>Outerwear &amp; Coats</td>
          <td>795.0</td>
          <td>382.39</td>
          <td>2385.0</td>
          <td>1237.82</td>
          <td>7</td>
          <td>3</td>
          <td>1</td>
          <td>1</td>
          <td>2</td>
          <td>1590.0</td>
          <td>825.21</td>
          <td>0.519</td>
          <td>0.25</td>
          <td>0.5</td>
          <td>0.1429</td>
          <td>0.4</td>
          <td>0.0008835</td>
          <td>0.0008847</td>
          <td>3.86e-05</td>
          <td>33</td>
          <td>23</td>
          <td>10</td>
          <td>12</td>
          <td>8625</td>
          <td>2358</td>
          <td>3978</td>
          <td>7029</td>
          <td>17069</td>
          <td>37</td>
          <td>45</td>
          <td>10485</td>
          <td>11344</td>
          <td>3269</td>
          <td>12706</td>
          <td>23875</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Expedition Parka</td>
          <td>Canada Goose</td>
          <td>Outerwear &amp; Coats</td>
          <td>795.0</td>
          <td>395.91</td>
          <td>2385.0</td>
          <td>1197.27</td>
          <td>4</td>
          <td>3</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>795.0</td>
          <td>399.09</td>
          <td>0.502</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.25</td>
          <td>0.0</td>
          <td>0.0008835</td>
          <td>0.0008557</td>
          <td>2.21e-05</td>
          <td>33</td>
          <td>19</td>
          <td>10</td>
          <td>13</td>
          <td>21053</td>
          <td>2358</td>
          <td>13463</td>
          <td>7029</td>
          <td>27145</td>
          <td>230</td>
          <td>277</td>
          <td>12357</td>
          <td>13463</td>
          <td>1</td>
          <td>5542</td>
          <td>27145</td>
        </tr>
        <tr>
          <td>Men&#x27;s Classic Sheepskin B-3 Bomber Jacket</td>
          <td>Overland Sheepskin Co</td>
          <td>Outerwear &amp; Coats</td>
          <td>595.0</td>
          <td>270.73</td>
          <td>2380.0</td>
          <td>1297.1</td>
          <td>13</td>
          <td>4</td>
          <td>0</td>
          <td>2</td>
          <td>7</td>
          <td>1190.0</td>
          <td>648.55</td>
          <td>0.545</td>
          <td>0.0</td>
          <td>0.3636</td>
          <td>0.1538</td>
          <td>0.6364</td>
          <td>0.0008816</td>
          <td>0.000927</td>
          <td>7.17e-05</td>
          <td>60</td>
          <td>55</td>
          <td>12</td>
          <td>11</td>
          <td>423</td>
          <td>776</td>
          <td>13463</td>
          <td>2100</td>
          <td>623</td>
          <td>95</td>
          <td>94</td>
          <td>8121</td>
          <td>13463</td>
          <td>9638</td>
          <td>12634</td>
          <td>16487</td>
        </tr>
        <tr>
          <td>Michael Kors Men&#x27;s Marlow Wool-Blend Single-Breasted Fitted Top Coat</td>
          <td>Michael Kors</td>
          <td>Outerwear &amp; Coats</td>
          <td>255.0</td>
          <td>102.26</td>
          <td>2295.0</td>
          <td>1374.7</td>
          <td>15</td>
          <td>9</td>
          <td>1</td>
          <td>2</td>
          <td>3</td>
          <td>765.0</td>
          <td>458.23</td>
          <td>0.599</td>
          <td>0.1</td>
          <td>0.6923</td>
          <td>0.1333</td>
          <td>0.25</td>
          <td>0.0008502</td>
          <td>0.0009825</td>
          <td>8.27e-05</td>
          <td>469</td>
          <td>728</td>
          <td>13</td>
          <td>8</td>
          <td>187</td>
          <td>5</td>
          <td>3978</td>
          <td>2100</td>
          <td>10869</td>
          <td>252</td>
          <td>208</td>
          <td>2612</td>
          <td>13461</td>
          <td>1184</td>
          <td>14317</td>
          <td>26348</td>
        </tr>
        <tr>
          <td>Barbour Sapper Jacket</td>
          <td>Barbour</td>
          <td>Outerwear &amp; Coats</td>
          <td>429.0</td>
          <td>210.21</td>
          <td>2145.0</td>
          <td>1093.95</td>
          <td>10</td>
          <td>5</td>
          <td>1</td>
          <td>1</td>
          <td>3</td>
          <td>858.0</td>
          <td>437.58</td>
          <td>0.51</td>
          <td>0.1667</td>
          <td>0.5556</td>
          <td>0.1</td>
          <td>0.375</td>
          <td>0.0007946</td>
          <td>0.0007818</td>
          <td>5.52e-05</td>
          <td>94</td>
          <td>81</td>
          <td>14</td>
          <td>18</td>
          <td>1962</td>
          <td>251</td>
          <td>3978</td>
          <td>7029</td>
          <td>10869</td>
          <td>185</td>
          <td>233</td>
          <td>11510</td>
          <td>13196</td>
          <td>3151</td>
          <td>16366</td>
          <td>24717</td>
        </tr>
        <tr>
          <td>Arc&#x27;teryx Moray Jacket - Women&#x27;s</td>
          <td>Arc&#x27;teryx</td>
          <td>Outerwear &amp; Coats</td>
          <td>699.0</td>
          <td>343.91</td>
          <td>2097.0</td>
          <td>1065.28</td>
          <td>9</td>
          <td>3</td>
          <td>0</td>
          <td>3</td>
          <td>3</td>
          <td>2097.0</td>
          <td>1065.28</td>
          <td>0.508</td>
          <td>0.0</td>
          <td>0.5</td>
          <td>0.3333</td>
          <td>0.5</td>
          <td>0.0007768</td>
          <td>0.0007613</td>
          <td>4.96e-05</td>
          <td>41</td>
          <td>36</td>
          <td>15</td>
          <td>20</td>
          <td>3355</td>
          <td>2358</td>
          <td>13463</td>
          <td>526</td>
          <td>10869</td>
          <td>11</td>
          <td>22</td>
          <td>11720</td>
          <td>13463</td>
          <td>3269</td>
          <td>2619</td>
          <td>19501</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by Profit</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>ASCIS Cushion Low Socks (Pack of 3)</td>
          <td>ASICS</td>
          <td>Active</td>
          <td>903.0</td>
          <td>373.84</td>
          <td>3612.0</td>
          <td>2116.63</td>
          <td>11</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>6</td>
          <td>903.0</td>
          <td>529.16</td>
          <td>0.586</td>
          <td>0.0</td>
          <td>0.4</td>
          <td>0.0909</td>
          <td>0.6</td>
          <td>0.001338</td>
          <td>0.0015127</td>
          <td>6.07e-05</td>
          <td>5</td>
          <td>28</td>
          <td>1</td>
          <td>1</td>
          <td>1161</td>
          <td>776</td>
          <td>13463</td>
          <td>7029</td>
          <td>1398</td>
          <td>155</td>
          <td>142</td>
          <td>3719</td>
          <td>13463</td>
          <td>7482</td>
          <td>16872</td>
          <td>16953</td>
        </tr>
        <tr>
          <td>The North Face Women&#x27;s S-XL Oso Jacket</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>378.36</td>
          <td>3612.0</td>
          <td>2098.57</td>
          <td>10</td>
          <td>4</td>
          <td>1</td>
          <td>1</td>
          <td>4</td>
          <td>1806.0</td>
          <td>1049.29</td>
          <td>0.581</td>
          <td>0.2</td>
          <td>0.4444</td>
          <td>0.1</td>
          <td>0.5</td>
          <td>0.001338</td>
          <td>0.0014998</td>
          <td>5.52e-05</td>
          <td>5</td>
          <td>25</td>
          <td>1</td>
          <td>2</td>
          <td>1962</td>
          <td>776</td>
          <td>3978</td>
          <td>7029</td>
          <td>6105</td>
          <td>22</td>
          <td>24</td>
          <td>4209</td>
          <td>12637</td>
          <td>6492</td>
          <td>16366</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>Bergama Natural Raccoon Hooded Stroller - - Multicolor</td>
          <td>Bergama</td>
          <td>Outerwear &amp; Coats</td>
          <td>749.99</td>
          <td>306.75</td>
          <td>2999.96</td>
          <td>1772.98</td>
          <td>10</td>
          <td>4</td>
          <td>1</td>
          <td>0</td>
          <td>5</td>
          <td>749.99</td>
          <td>443.24</td>
          <td>0.591</td>
          <td>0.2</td>
          <td>0.4</td>
          <td>0.0</td>
          <td>0.5556</td>
          <td>0.0011113</td>
          <td>0.0012671</td>
          <td>5.52e-05</td>
          <td>40</td>
          <td>43</td>
          <td>4</td>
          <td>3</td>
          <td>1962</td>
          <td>776</td>
          <td>3978</td>
          <td>17458</td>
          <td>3026</td>
          <td>267</td>
          <td>224</td>
          <td>3279</td>
          <td>12637</td>
          <td>7482</td>
          <td>17458</td>
          <td>19270</td>
        </tr>
        <tr>
          <td>Spyder Women&#x27;s Jesst In Time Jacket</td>
          <td>Spyder</td>
          <td>Outerwear &amp; Coats</td>
          <td>650.0</td>
          <td>295.75</td>
          <td>3250.0</td>
          <td>1771.25</td>
          <td>10</td>
          <td>5</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>2600.0</td>
          <td>1417.0</td>
          <td>0.545</td>
          <td>0.4444</td>
          <td>0.5</td>
          <td>0.0</td>
          <td>0.1667</td>
          <td>0.0012039</td>
          <td>0.0012659</td>
          <td>5.52e-05</td>
          <td>52</td>
          <td>50</td>
          <td>3</td>
          <td>4</td>
          <td>1962</td>
          <td>251</td>
          <td>30</td>
          <td>17458</td>
          <td>23197</td>
          <td>7</td>
          <td>7</td>
          <td>8121</td>
          <td>8264</td>
          <td>3269</td>
          <td>17458</td>
          <td>27059</td>
        </tr>
        <tr>
          <td>Joseph Abboud Men&#x27;s Two-button Side Vent Sport Coat</td>
          <td>Joseph Abboud</td>
          <td>Suits &amp; Sport Coats</td>
          <td>264.0</td>
          <td>101.9</td>
          <td>2904.0</td>
          <td>1759.82</td>
          <td>30</td>
          <td>11</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>1056.0</td>
          <td>656.57</td>
          <td>0.606</td>
          <td>0.1538</td>
          <td>0.3929</td>
          <td>0.0667</td>
          <td>0.5769</td>
          <td>0.0010758</td>
          <td>0.0012577</td>
          <td>0.0001655</td>
          <td>430</td>
          <td>734</td>
          <td>6</td>
          <td>5</td>
          <td>7</td>
          <td>3</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>112</td>
          <td>91</td>
          <td>2144</td>
          <td>13388</td>
          <td>9081</td>
          <td>17408</td>
          <td>18610</td>
        </tr>
        <tr>
          <td>Woolrich Arctic Parka DF</td>
          <td>Woolrich</td>
          <td>Outerwear &amp; Coats</td>
          <td>990.0</td>
          <td>478.17</td>
          <td>2970.0</td>
          <td>1535.49</td>
          <td>12</td>
          <td>3</td>
          <td>2</td>
          <td>1</td>
          <td>6</td>
          <td>2970.0</td>
          <td>1535.49</td>
          <td>0.517</td>
          <td>0.4</td>
          <td>0.2727</td>
          <td>0.0833</td>
          <td>0.6667</td>
          <td>0.0011002</td>
          <td>0.0010974</td>
          <td>6.62e-05</td>
          <td>3</td>
          <td>6</td>
          <td>5</td>
          <td>6</td>
          <td>694</td>
          <td>2358</td>
          <td>844</td>
          <td>7029</td>
          <td>1398</td>
          <td>4</td>
          <td>4</td>
          <td>10735</td>
          <td>8312</td>
          <td>14284</td>
          <td>17144</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>The North Face Denali Down Mens Jacket 2013</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>436.15</td>
          <td>2709.0</td>
          <td>1400.55</td>
          <td>13</td>
          <td>3</td>
          <td>2</td>
          <td>2</td>
          <td>6</td>
          <td>3612.0</td>
          <td>1867.4</td>
          <td>0.517</td>
          <td>0.4</td>
          <td>0.2727</td>
          <td>0.1538</td>
          <td>0.6667</td>
          <td>0.0010035</td>
          <td>0.001001</td>
          <td>7.17e-05</td>
          <td>5</td>
          <td>10</td>
          <td>7</td>
          <td>7</td>
          <td>423</td>
          <td>2358</td>
          <td>844</td>
          <td>2100</td>
          <td>1398</td>
          <td>2</td>
          <td>3</td>
          <td>10735</td>
          <td>8312</td>
          <td>14284</td>
          <td>12634</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Michael Kors Men&#x27;s Marlow Wool-Blend Single-Breasted Fitted Top Coat</td>
          <td>Michael Kors</td>
          <td>Outerwear &amp; Coats</td>
          <td>255.0</td>
          <td>102.26</td>
          <td>2295.0</td>
          <td>1374.7</td>
          <td>15</td>
          <td>9</td>
          <td>1</td>
          <td>2</td>
          <td>3</td>
          <td>765.0</td>
          <td>458.23</td>
          <td>0.599</td>
          <td>0.1</td>
          <td>0.6923</td>
          <td>0.1333</td>
          <td>0.25</td>
          <td>0.0008502</td>
          <td>0.0009825</td>
          <td>8.27e-05</td>
          <td>469</td>
          <td>728</td>
          <td>13</td>
          <td>8</td>
          <td>187</td>
          <td>5</td>
          <td>3978</td>
          <td>2100</td>
          <td>10869</td>
          <td>252</td>
          <td>208</td>
          <td>2612</td>
          <td>13461</td>
          <td>1184</td>
          <td>14317</td>
          <td>26348</td>
        </tr>
        <tr>
          <td>AIR JORDAN DOMINATE SHORTS MENS 465071-100</td>
          <td>Jordan</td>
          <td>Shorts</td>
          <td>903.0</td>
          <td>454.21</td>
          <td>2709.0</td>
          <td>1346.37</td>
          <td>5</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>2</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.497</td>
          <td>0.0</td>
          <td>0.6</td>
          <td>0.0</td>
          <td>0.4</td>
          <td>0.0010035</td>
          <td>0.0009622</td>
          <td>2.76e-05</td>
          <td>5</td>
          <td>8</td>
          <td>7</td>
          <td>9</td>
          <td>16887</td>
          <td>2358</td>
          <td>13463</td>
          <td>17458</td>
          <td>17069</td>
          <td>22642</td>
          <td>22642</td>
          <td>12874</td>
          <td>13463</td>
          <td>2189</td>
          <td>17458</td>
          <td>23875</td>
        </tr>
        <tr>
          <td>Diesel Men&#x27;s Lagnum Leather Jacket</td>
          <td>Diesel</td>
          <td>Outerwear &amp; Coats</td>
          <td>598.0</td>
          <td>267.9</td>
          <td>2392.0</td>
          <td>1320.38</td>
          <td>7</td>
          <td>4</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>1196.0</td>
          <td>660.19</td>
          <td>0.552</td>
          <td>0.2</td>
          <td>0.6667</td>
          <td>0.1429</td>
          <td>0.2</td>
          <td>0.0008861</td>
          <td>0.0009437</td>
          <td>3.86e-05</td>
          <td>57</td>
          <td>56</td>
          <td>9</td>
          <td>10</td>
          <td>8625</td>
          <td>776</td>
          <td>3978</td>
          <td>7029</td>
          <td>23197</td>
          <td>92</td>
          <td>89</td>
          <td>7373</td>
          <td>12637</td>
          <td>1185</td>
          <td>12706</td>
          <td>26859</td>
        </tr>
        <tr>
          <td>Men&#x27;s Classic Sheepskin B-3 Bomber Jacket</td>
          <td>Overland Sheepskin Co</td>
          <td>Outerwear &amp; Coats</td>
          <td>595.0</td>
          <td>270.73</td>
          <td>2380.0</td>
          <td>1297.1</td>
          <td>13</td>
          <td>4</td>
          <td>0</td>
          <td>2</td>
          <td>7</td>
          <td>1190.0</td>
          <td>648.55</td>
          <td>0.545</td>
          <td>0.0</td>
          <td>0.3636</td>
          <td>0.1538</td>
          <td>0.6364</td>
          <td>0.0008816</td>
          <td>0.000927</td>
          <td>7.17e-05</td>
          <td>60</td>
          <td>55</td>
          <td>12</td>
          <td>11</td>
          <td>423</td>
          <td>776</td>
          <td>13463</td>
          <td>2100</td>
          <td>623</td>
          <td>95</td>
          <td>94</td>
          <td>8121</td>
          <td>13463</td>
          <td>9638</td>
          <td>12634</td>
          <td>16487</td>
        </tr>
        <tr>
          <td>Nobis Merideth Parka</td>
          <td>Nobis</td>
          <td>Outerwear &amp; Coats</td>
          <td>795.0</td>
          <td>382.39</td>
          <td>2385.0</td>
          <td>1237.82</td>
          <td>7</td>
          <td>3</td>
          <td>1</td>
          <td>1</td>
          <td>2</td>
          <td>1590.0</td>
          <td>825.21</td>
          <td>0.519</td>
          <td>0.25</td>
          <td>0.5</td>
          <td>0.1429</td>
          <td>0.4</td>
          <td>0.0008835</td>
          <td>0.0008847</td>
          <td>3.86e-05</td>
          <td>33</td>
          <td>23</td>
          <td>10</td>
          <td>12</td>
          <td>8625</td>
          <td>2358</td>
          <td>3978</td>
          <td>7029</td>
          <td>17069</td>
          <td>37</td>
          <td>45</td>
          <td>10485</td>
          <td>11344</td>
          <td>3269</td>
          <td>12706</td>
          <td>23875</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Expedition Parka</td>
          <td>Canada Goose</td>
          <td>Outerwear &amp; Coats</td>
          <td>795.0</td>
          <td>395.91</td>
          <td>2385.0</td>
          <td>1197.27</td>
          <td>4</td>
          <td>3</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>795.0</td>
          <td>399.09</td>
          <td>0.502</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.25</td>
          <td>0.0</td>
          <td>0.0008835</td>
          <td>0.0008557</td>
          <td>2.21e-05</td>
          <td>33</td>
          <td>19</td>
          <td>10</td>
          <td>13</td>
          <td>21053</td>
          <td>2358</td>
          <td>13463</td>
          <td>7029</td>
          <td>27145</td>
          <td>230</td>
          <td>277</td>
          <td>12357</td>
          <td>13463</td>
          <td>1</td>
          <td>5542</td>
          <td>27145</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Solaris</td>
          <td>Canada Goose</td>
          <td>Outerwear &amp; Coats</td>
          <td>695.0</td>
          <td>296.76</td>
          <td>2085.0</td>
          <td>1194.71</td>
          <td>6</td>
          <td>3</td>
          <td>0</td>
          <td>2</td>
          <td>1</td>
          <td>1390.0</td>
          <td>796.47</td>
          <td>0.573</td>
          <td>0.0</td>
          <td>0.75</td>
          <td>0.3333</td>
          <td>0.25</td>
          <td>0.0007724</td>
          <td>0.0008538</td>
          <td>3.31e-05</td>
          <td>46</td>
          <td>48</td>
          <td>17</td>
          <td>14</td>
          <td>12532</td>
          <td>2358</td>
          <td>13463</td>
          <td>2100</td>
          <td>23197</td>
          <td>67</td>
          <td>52</td>
          <td>5041</td>
          <td>13463</td>
          <td>746</td>
          <td>2619</td>
          <td>26348</td>
        </tr>
        <tr>
          <td>Darla</td>
          <td>Alpha Industries</td>
          <td>Outerwear &amp; Coats</td>
          <td>999.0</td>
          <td>404.6</td>
          <td>1998.0</td>
          <td>1188.81</td>
          <td>7</td>
          <td>2</td>
          <td>2</td>
          <td>0</td>
          <td>3</td>
          <td>1998.0</td>
          <td>1188.81</td>
          <td>0.595</td>
          <td>0.5</td>
          <td>0.2857</td>
          <td>0.0</td>
          <td>0.6</td>
          <td>0.0007401</td>
          <td>0.0008496</td>
          <td>3.86e-05</td>
          <td>1</td>
          <td>16</td>
          <td>18</td>
          <td>15</td>
          <td>8625</td>
          <td>6114</td>
          <td>844</td>
          <td>17458</td>
          <td>10869</td>
          <td>14</td>
          <td>14</td>
          <td>2925</td>
          <td>4275</td>
          <td>13238</td>
          <td>17458</td>
          <td>16953</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by Profit Margin</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Plus Size Black Jazzy Jacket</td>
          <td>Fashion Love</td>
          <td>Blazers &amp; Jackets</td>
          <td>34.99</td>
          <td>11.58</td>
          <td>104.97</td>
          <td>70.22</td>
          <td>5</td>
          <td>3</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>34.99</td>
          <td>23.41</td>
          <td>0.669</td>
          <td>0.0</td>
          <td>0.75</td>
          <td>0.2</td>
          <td>0.25</td>
          <td>3.89e-05</td>
          <td>5.02e-05</td>
          <td>2.76e-05</td>
          <td>15963</td>
          <td>20949</td>
          <td>7698</td>
          <td>5726</td>
          <td>16887</td>
          <td>2358</td>
          <td>13463</td>
          <td>7029</td>
          <td>23197</td>
          <td>17236</td>
          <td>14884</td>
          <td>1</td>
          <td>13463</td>
          <td>746</td>
          <td>8435</td>
          <td>26348</td>
        </tr>
        <tr>
          <td>Ulla Popken Plus Size Soutache Embroidered Jacket</td>
          <td>Ulla Popken</td>
          <td>Blazers &amp; Jackets</td>
          <td>89.0</td>
          <td>29.46</td>
          <td>178.0</td>
          <td>119.08</td>
          <td>7</td>
          <td>2</td>
          <td>1</td>
          <td>0</td>
          <td>4</td>
          <td>89.0</td>
          <td>59.54</td>
          <td>0.669</td>
          <td>0.3333</td>
          <td>0.2857</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>6.59e-05</td>
          <td>8.51e-05</td>
          <td>3.86e-05</td>
          <td>4994</td>
          <td>8857</td>
          <td>4102</td>
          <td>2773</td>
          <td>8625</td>
          <td>6114</td>
          <td>3978</td>
          <td>17458</td>
          <td>6105</td>
          <td>9306</td>
          <td>6919</td>
          <td>1</td>
          <td>8752</td>
          <td>13238</td>
          <td>17458</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Ted Baker Women&#x27;s Mowna</td>
          <td>Ted Baker</td>
          <td>Blazers &amp; Jackets</td>
          <td>206.96</td>
          <td>68.5</td>
          <td>206.96</td>
          <td>138.46</td>
          <td>7</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>4</td>
          <td>413.92</td>
          <td>276.91</td>
          <td>0.669</td>
          <td>0.5</td>
          <td>0.1667</td>
          <td>0.1429</td>
          <td>0.8</td>
          <td>7.67e-05</td>
          <td>9.9e-05</td>
          <td>3.86e-05</td>
          <td>771</td>
          <td>2149</td>
          <td>3223</td>
          <td>2200</td>
          <td>8625</td>
          <td>13264</td>
          <td>3978</td>
          <td>7029</td>
          <td>6105</td>
          <td>925</td>
          <td>621</td>
          <td>1</td>
          <td>4275</td>
          <td>19436</td>
          <td>12706</td>
          <td>7598</td>
        </tr>
        <tr>
          <td>Eddie Bauer Signature Stretch Blazer</td>
          <td>Eddie Bauer</td>
          <td>Blazers &amp; Jackets</td>
          <td>149.95</td>
          <td>49.63</td>
          <td>299.9</td>
          <td>200.63</td>
          <td>9</td>
          <td>2</td>
          <td>0</td>
          <td>2</td>
          <td>5</td>
          <td>299.9</td>
          <td>200.63</td>
          <td>0.669</td>
          <td>0.0</td>
          <td>0.2857</td>
          <td>0.2222</td>
          <td>0.7143</td>
          <td>0.0001111</td>
          <td>0.0001434</td>
          <td>4.96e-05</td>
          <td>1956</td>
          <td>3876</td>
          <td>1775</td>
          <td>1137</td>
          <td>3355</td>
          <td>6114</td>
          <td>13463</td>
          <td>2100</td>
          <td>3026</td>
          <td>1734</td>
          <td>1126</td>
          <td>1</td>
          <td>13463</td>
          <td>13238</td>
          <td>7837</td>
          <td>12035</td>
        </tr>
        <tr>
          <td>DKNYC Women&#x27;s 2 Button Blazer</td>
          <td>DKNYC</td>
          <td>Blazers &amp; Jackets</td>
          <td>99.09</td>
          <td>32.8</td>
          <td>198.18</td>
          <td>132.58</td>
          <td>6</td>
          <td>2</td>
          <td>2</td>
          <td>0</td>
          <td>2</td>
          <td>198.18</td>
          <td>132.58</td>
          <td>0.669</td>
          <td>0.5</td>
          <td>0.3333</td>
          <td>0.0</td>
          <td>0.5</td>
          <td>7.34e-05</td>
          <td>9.48e-05</td>
          <td>3.31e-05</td>
          <td>4110</td>
          <td>7591</td>
          <td>3450</td>
          <td>2363</td>
          <td>12532</td>
          <td>6114</td>
          <td>844</td>
          <td>17458</td>
          <td>17069</td>
          <td>3375</td>
          <td>2320</td>
          <td>1</td>
          <td>4275</td>
          <td>9747</td>
          <td>17458</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>Allegra K Front Opening Long Sleeve Womenwear Form-fitting Blazer Off White XS</td>
          <td>Allegra K</td>
          <td>Blazers &amp; Jackets</td>
          <td>18.68</td>
          <td>6.18</td>
          <td>37.36</td>
          <td>24.99</td>
          <td>6</td>
          <td>2</td>
          <td>0</td>
          <td>1</td>
          <td>3</td>
          <td>18.68</td>
          <td>12.5</td>
          <td>0.6689</td>
          <td>0.0</td>
          <td>0.4</td>
          <td>0.1667</td>
          <td>0.6</td>
          <td>1.38e-05</td>
          <td>1.79e-05</td>
          <td>3.31e-05</td>
          <td>23425</td>
          <td>25885</td>
          <td>16627</td>
          <td>14250</td>
          <td>12532</td>
          <td>6114</td>
          <td>13463</td>
          <td>7029</td>
          <td>10869</td>
          <td>20771</td>
          <td>19355</td>
          <td>6</td>
          <td>13463</td>
          <td>7482</td>
          <td>10731</td>
          <td>16953</td>
        </tr>
        <tr>
          <td>Allegra K Women Horizontal Stripes Bubble Sleeve Spring Coat Black XS</td>
          <td>Allegra K</td>
          <td>Blazers &amp; Jackets</td>
          <td>11.67</td>
          <td>3.86</td>
          <td>23.34</td>
          <td>15.61</td>
          <td>10</td>
          <td>2</td>
          <td>1</td>
          <td>0</td>
          <td>7</td>
          <td>11.67</td>
          <td>7.81</td>
          <td>0.6688</td>
          <td>0.3333</td>
          <td>0.2</td>
          <td>0.0</td>
          <td>0.7778</td>
          <td>8.6e-06</td>
          <td>1.12e-05</td>
          <td>5.52e-05</td>
          <td>26523</td>
          <td>27736</td>
          <td>19737</td>
          <td>17784</td>
          <td>1962</td>
          <td>6114</td>
          <td>3978</td>
          <td>17458</td>
          <td>623</td>
          <td>21976</td>
          <td>21271</td>
          <td>7</td>
          <td>8752</td>
          <td>17510</td>
          <td>17458</td>
          <td>9281</td>
        </tr>
        <tr>
          <td>BB Dakota Yellow Marigold Naples Boxy Cropped Blazer Button up Front and Double Pockets</td>
          <td>BB Dakota</td>
          <td>Blazers &amp; Jackets</td>
          <td>77.0</td>
          <td>25.56</td>
          <td>77.0</td>
          <td>51.44</td>
          <td>6</td>
          <td>1</td>
          <td>0</td>
          <td>2</td>
          <td>3</td>
          <td>154.0</td>
          <td>102.87</td>
          <td>0.6681</td>
          <td>0.0</td>
          <td>0.25</td>
          <td>0.3333</td>
          <td>0.75</td>
          <td>2.85e-05</td>
          <td>3.68e-05</td>
          <td>3.31e-05</td>
          <td>6222</td>
          <td>10673</td>
          <td>10392</td>
          <td>8077</td>
          <td>12532</td>
          <td>13264</td>
          <td>13463</td>
          <td>2100</td>
          <td>10869</td>
          <td>4944</td>
          <td>3344</td>
          <td>8</td>
          <td>13463</td>
          <td>14408</td>
          <td>2619</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>Mango Women&#x27;s Suit Cropped Blazer - Chipi</td>
          <td>MANGO</td>
          <td>Blazers &amp; Jackets</td>
          <td>49.99</td>
          <td>16.6</td>
          <td>99.98</td>
          <td>66.79</td>
          <td>4</td>
          <td>2</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>49.99</td>
          <td>33.39</td>
          <td>0.668</td>
          <td>0.3333</td>
          <td>0.5</td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>3.7e-05</td>
          <td>4.77e-05</td>
          <td>2.21e-05</td>
          <td>10894</td>
          <td>16411</td>
          <td>8109</td>
          <td>6088</td>
          <td>21053</td>
          <td>6114</td>
          <td>3978</td>
          <td>17458</td>
          <td>23197</td>
          <td>14347</td>
          <td>11779</td>
          <td>9</td>
          <td>8752</td>
          <td>3269</td>
          <td>17458</td>
          <td>24854</td>
        </tr>
        <tr>
          <td>Calvin Klein Jeans Women&#x27;s Moto Jacket</td>
          <td>Calvin Klein Jeans</td>
          <td>Blazers &amp; Jackets</td>
          <td>56.39</td>
          <td>18.72</td>
          <td>56.39</td>
          <td>37.67</td>
          <td>5</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>3</td>
          <td>56.39</td>
          <td>37.67</td>
          <td>0.668</td>
          <td>0.5</td>
          <td>0.2</td>
          <td>0.0</td>
          <td>0.75</td>
          <td>2.09e-05</td>
          <td>2.69e-05</td>
          <td>2.76e-05</td>
          <td>9503</td>
          <td>14790</td>
          <td>13133</td>
          <td>10707</td>
          <td>16887</td>
          <td>13264</td>
          <td>3978</td>
          <td>17458</td>
          <td>10869</td>
          <td>13238</td>
          <td>10778</td>
          <td>9</td>
          <td>4275</td>
          <td>17510</td>
          <td>17458</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>Allegra K Women Double Breasted Long Sleeve Autumn Blazer Coat Army Green XS</td>
          <td>Allegra K</td>
          <td>Blazers &amp; Jackets</td>
          <td>16.05</td>
          <td>5.33</td>
          <td>32.1</td>
          <td>21.44</td>
          <td>4</td>
          <td>2</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>16.05</td>
          <td>10.72</td>
          <td>0.6679</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>0.25</td>
          <td>0.3333</td>
          <td>1.19e-05</td>
          <td>1.53e-05</td>
          <td>2.21e-05</td>
          <td>24296</td>
          <td>26673</td>
          <td>17542</td>
          <td>15499</td>
          <td>21053</td>
          <td>6114</td>
          <td>13463</td>
          <td>7029</td>
          <td>23197</td>
          <td>21164</td>
          <td>20129</td>
          <td>11</td>
          <td>13463</td>
          <td>1185</td>
          <td>5542</td>
          <td>24854</td>
        </tr>
        <tr>
          <td>Pendleton Women&#x27;s Trimmed Herringbone Blazer</td>
          <td>Pendleton</td>
          <td>Blazers &amp; Jackets</td>
          <td>258.0</td>
          <td>85.91</td>
          <td>516.0</td>
          <td>344.17</td>
          <td>6</td>
          <td>2</td>
          <td>1</td>
          <td>2</td>
          <td>1</td>
          <td>774.0</td>
          <td>516.26</td>
          <td>0.667</td>
          <td>0.3333</td>
          <td>0.5</td>
          <td>0.3333</td>
          <td>0.3333</td>
          <td>0.0001911</td>
          <td>0.000246</td>
          <td>3.31e-05</td>
          <td>462</td>
          <td>1282</td>
          <td>594</td>
          <td>364</td>
          <td>12532</td>
          <td>6114</td>
          <td>3978</td>
          <td>2100</td>
          <td>23197</td>
          <td>251</td>
          <td>153</td>
          <td>12</td>
          <td>8752</td>
          <td>3269</td>
          <td>2619</td>
          <td>24854</td>
        </tr>
        <tr>
          <td>Corey Lynn Calter Women&#x27;s Jessica Jacket</td>
          <td>CoreyLynnCalter</td>
          <td>Blazers &amp; Jackets</td>
          <td>79.0</td>
          <td>26.31</td>
          <td>79.0</td>
          <td>52.69</td>
          <td>3</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>79.0</td>
          <td>52.69</td>
          <td>0.667</td>
          <td>0.0</td>
          <td>0.5</td>
          <td>0.3333</td>
          <td>0.5</td>
          <td>2.93e-05</td>
          <td>3.77e-05</td>
          <td>1.65e-05</td>
          <td>5951</td>
          <td>10284</td>
          <td>10194</td>
          <td>7889</td>
          <td>24645</td>
          <td>13264</td>
          <td>13463</td>
          <td>7029</td>
          <td>23197</td>
          <td>10287</td>
          <td>7953</td>
          <td>12</td>
          <td>13463</td>
          <td>3269</td>
          <td>2619</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>Only Hearts Women&#x27;s Double Knit 2 Button Jacket</td>
          <td>Only Hearts</td>
          <td>Blazers &amp; Jackets</td>
          <td>185.0</td>
          <td>61.61</td>
          <td>1110.0</td>
          <td>740.37</td>
          <td>11</td>
          <td>6</td>
          <td>0</td>
          <td>0</td>
          <td>5</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.667</td>
          <td>0.0</td>
          <td>0.5455</td>
          <td>0.0</td>
          <td>0.4545</td>
          <td>0.0004112</td>
          <td>0.0005291</td>
          <td>6.07e-05</td>
          <td>1114</td>
          <td>2672</td>
          <td>94</td>
          <td>56</td>
          <td>1161</td>
          <td>84</td>
          <td>13463</td>
          <td>17458</td>
          <td>3026</td>
          <td>22642</td>
          <td>22642</td>
          <td>12</td>
          <td>13463</td>
          <td>3246</td>
          <td>17458</td>
          <td>23452</td>
        </tr>
        <tr>
          <td>Plus Size White Night Sky Top</td>
          <td>Alex Evenings</td>
          <td>Blazers &amp; Jackets</td>
          <td>124.99</td>
          <td>41.62</td>
          <td>124.99</td>
          <td>83.37</td>
          <td>4</td>
          <td>1</td>
          <td>2</td>
          <td>0</td>
          <td>1</td>
          <td>249.98</td>
          <td>166.74</td>
          <td>0.667</td>
          <td>0.6667</td>
          <td>0.25</td>
          <td>0.0</td>
          <td>0.5</td>
          <td>4.63e-05</td>
          <td>5.96e-05</td>
          <td>2.21e-05</td>
          <td>2939</td>
          <td>5153</td>
          <td>6403</td>
          <td>4593</td>
          <td>21053</td>
          <td>13264</td>
          <td>844</td>
          <td>17458</td>
          <td>23197</td>
          <td>2385</td>
          <td>1545</td>
          <td>12</td>
          <td>3055</td>
          <td>14408</td>
          <td>17458</td>
          <td>19501</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by Unit Orders</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Wrangler Men&#x27;s Premium Performance Cowboy Cut Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>47.45</td>
          <td>25.88</td>
          <td>570.83</td>
          <td>264.22</td>
          <td>58</td>
          <td>12</td>
          <td>2</td>
          <td>7</td>
          <td>37</td>
          <td>417.81</td>
          <td>189.65</td>
          <td>0.4629</td>
          <td>0.1429</td>
          <td>0.2353</td>
          <td>0.1207</td>
          <td>0.7551</td>
          <td>0.0002115</td>
          <td>0.0001888</td>
          <td>0.00032</td>
          <td>12004</td>
          <td>10508</td>
          <td>470</td>
          <td>662</td>
          <td>1</td>
          <td>2</td>
          <td>844</td>
          <td>2</td>
          <td>1</td>
          <td>905</td>
          <td>1224</td>
          <td>16149</td>
          <td>13389</td>
          <td>17092</td>
          <td>15548</td>
          <td>9486</td>
        </tr>
        <tr>
          <td>7 For All Mankind Men&#x27;s Standard Classic Straight Leg Jean</td>
          <td>7 For All Mankind</td>
          <td>Jeans</td>
          <td>157.45</td>
          <td>80.97</td>
          <td>1435.0</td>
          <td>696.01</td>
          <td>42</td>
          <td>9</td>
          <td>5</td>
          <td>5</td>
          <td>23</td>
          <td>1673.0</td>
          <td>844.04</td>
          <td>0.485</td>
          <td>0.3571</td>
          <td>0.2432</td>
          <td>0.119</td>
          <td>0.7188</td>
          <td>0.0005316</td>
          <td>0.0004974</td>
          <td>0.0002317</td>
          <td>1798</td>
          <td>1488</td>
          <td>46</td>
          <td>60</td>
          <td>2</td>
          <td>5</td>
          <td>5</td>
          <td>24</td>
          <td>2</td>
          <td>32</td>
          <td>41</td>
          <td>14028</td>
          <td>8749</td>
          <td>17091</td>
          <td>15552</td>
          <td>12034</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Rugged Wear Classic Fit Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.87</td>
          <td>22.23</td>
          <td>367.56</td>
          <td>169.24</td>
          <td>38</td>
          <td>9</td>
          <td>5</td>
          <td>9</td>
          <td>15</td>
          <td>596.43</td>
          <td>273.96</td>
          <td>0.4604</td>
          <td>0.3571</td>
          <td>0.3103</td>
          <td>0.2368</td>
          <td>0.625</td>
          <td>0.0001362</td>
          <td>0.000121</td>
          <td>0.0002096</td>
          <td>13688</td>
          <td>12514</td>
          <td>1205</td>
          <td>1552</td>
          <td>3</td>
          <td>5</td>
          <td>5</td>
          <td>1</td>
          <td>11</td>
          <td>440</td>
          <td>628</td>
          <td>16340</td>
          <td>8749</td>
          <td>13014</td>
          <td>7776</td>
          <td>16547</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>246.88</td>
          <td>129.05</td>
          <td>1366.0</td>
          <td>666.07</td>
          <td>34</td>
          <td>5</td>
          <td>4</td>
          <td>3</td>
          <td>22</td>
          <td>1400.0</td>
          <td>654.5</td>
          <td>0.4876</td>
          <td>0.4444</td>
          <td>0.1613</td>
          <td>0.0882</td>
          <td>0.8148</td>
          <td>0.000506</td>
          <td>0.000476</td>
          <td>0.0001876</td>
          <td>534</td>
          <td>354</td>
          <td>56</td>
          <td>65</td>
          <td>4</td>
          <td>251</td>
          <td>30</td>
          <td>526</td>
          <td>3</td>
          <td>63</td>
          <td>92</td>
          <td>13792</td>
          <td>8264</td>
          <td>20804</td>
          <td>17143</td>
          <td>7595</td>
        </tr>
        <tr>
          <td>Kenneth Cole REACTION Men&#x27;s Passcase Wallet</td>
          <td>Kenneth Cole REACTION</td>
          <td>Accessories</td>
          <td>18.91</td>
          <td>7.72</td>
          <td>152.71</td>
          <td>89.4</td>
          <td>34</td>
          <td>8</td>
          <td>4</td>
          <td>4</td>
          <td>18</td>
          <td>150.85</td>
          <td>90.57</td>
          <td>0.5854</td>
          <td>0.3333</td>
          <td>0.2667</td>
          <td>0.1176</td>
          <td>0.6923</td>
          <td>5.66e-05</td>
          <td>6.39e-05</td>
          <td>0.0001876</td>
          <td>23389</td>
          <td>24481</td>
          <td>4958</td>
          <td>4188</td>
          <td>4</td>
          <td>16</td>
          <td>30</td>
          <td>126</td>
          <td>4</td>
          <td>5015</td>
          <td>4078</td>
          <td>3806</td>
          <td>8752</td>
          <td>14395</td>
          <td>15553</td>
          <td>12966</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Long Pant</td>
          <td>HUGO BOSS</td>
          <td>Sleep &amp; Lounge</td>
          <td>74.72</td>
          <td>28.3</td>
          <td>1033.11</td>
          <td>648.16</td>
          <td>33</td>
          <td>14</td>
          <td>0</td>
          <td>3</td>
          <td>16</td>
          <td>233.01</td>
          <td>138.21</td>
          <td>0.6274</td>
          <td>0.0</td>
          <td>0.4667</td>
          <td>0.0909</td>
          <td>0.5333</td>
          <td>0.0003827</td>
          <td>0.0004632</td>
          <td>0.000182</td>
          <td>6501</td>
          <td>9383</td>
          <td>113</td>
          <td>75</td>
          <td>6</td>
          <td>1</td>
          <td>13463</td>
          <td>526</td>
          <td>7</td>
          <td>2702</td>
          <td>2165</td>
          <td>933</td>
          <td>13463</td>
          <td>6418</td>
          <td>16872</td>
          <td>19494</td>
        </tr>
        <tr>
          <td>Joseph Abboud Men&#x27;s Two-button Side Vent Sport Coat</td>
          <td>Joseph Abboud</td>
          <td>Suits &amp; Sport Coats</td>
          <td>264.0</td>
          <td>101.9</td>
          <td>2904.0</td>
          <td>1759.82</td>
          <td>30</td>
          <td>11</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>1056.0</td>
          <td>656.57</td>
          <td>0.606</td>
          <td>0.1538</td>
          <td>0.3929</td>
          <td>0.0667</td>
          <td>0.5769</td>
          <td>0.0010758</td>
          <td>0.0012577</td>
          <td>0.0001655</td>
          <td>430</td>
          <td>734</td>
          <td>6</td>
          <td>5</td>
          <td>7</td>
          <td>3</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>112</td>
          <td>91</td>
          <td>2144</td>
          <td>13388</td>
          <td>9081</td>
          <td>17408</td>
          <td>18610</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Genuine Tampa Cargo Short</td>
          <td>Wrangler</td>
          <td>Shorts</td>
          <td>31.37</td>
          <td>15.61</td>
          <td>229.94</td>
          <td>116.44</td>
          <td>29</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>16</td>
          <td>179.94</td>
          <td>90.54</td>
          <td>0.5064</td>
          <td>0.125</td>
          <td>0.2917</td>
          <td>0.1724</td>
          <td>0.6957</td>
          <td>8.52e-05</td>
          <td>8.32e-05</td>
          <td>0.00016</td>
          <td>17403</td>
          <td>17266</td>
          <td>2818</td>
          <td>2869</td>
          <td>8</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>7</td>
          <td>3935</td>
          <td>4081</td>
          <td>11924</td>
          <td>13444</td>
          <td>13236</td>
          <td>10730</td>
          <td>12964</td>
        </tr>
        <tr>
          <td>Hanes Men&#x27;s 4 Pack Boxer Brief</td>
          <td>Hanes</td>
          <td>Underwear</td>
          <td>25.0</td>
          <td>11.52</td>
          <td>250.0</td>
          <td>133.47</td>
          <td>28</td>
          <td>10</td>
          <td>2</td>
          <td>5</td>
          <td>11</td>
          <td>175.0</td>
          <td>92.77</td>
          <td>0.5339</td>
          <td>0.1667</td>
          <td>0.4348</td>
          <td>0.1786</td>
          <td>0.5238</td>
          <td>9.26e-05</td>
          <td>9.54e-05</td>
          <td>0.0001545</td>
          <td>19651</td>
          <td>20997</td>
          <td>2432</td>
          <td>2340</td>
          <td>9</td>
          <td>4</td>
          <td>844</td>
          <td>24</td>
          <td>43</td>
          <td>4152</td>
          <td>3935</td>
          <td>9232</td>
          <td>13196</td>
          <td>6738</td>
          <td>10715</td>
          <td>19500</td>
        </tr>
        <tr>
          <td>Chaps Big and Tall Solid V-Neck Vest</td>
          <td>Chaps</td>
          <td>Sweaters</td>
          <td>39.88</td>
          <td>20.32</td>
          <td>279.16</td>
          <td>134.91</td>
          <td>28</td>
          <td>7</td>
          <td>4</td>
          <td>1</td>
          <td>16</td>
          <td>199.4</td>
          <td>99.06</td>
          <td>0.4833</td>
          <td>0.3636</td>
          <td>0.2593</td>
          <td>0.0357</td>
          <td>0.6957</td>
          <td>0.0001034</td>
          <td>9.64e-05</td>
          <td>0.0001545</td>
          <td>14437</td>
          <td>13747</td>
          <td>2029</td>
          <td>2288</td>
          <td>9</td>
          <td>33</td>
          <td>30</td>
          <td>7029</td>
          <td>7</td>
          <td>3354</td>
          <td>3543</td>
          <td>14237</td>
          <td>8748</td>
          <td>14407</td>
          <td>17457</td>
          <td>12964</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Leg Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>227.86</td>
          <td>123.14</td>
          <td>1452.0</td>
          <td>661.01</td>
          <td>28</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>15</td>
          <td>1430.0</td>
          <td>645.85</td>
          <td>0.4552</td>
          <td>0.125</td>
          <td>0.3043</td>
          <td>0.1786</td>
          <td>0.6818</td>
          <td>0.0005379</td>
          <td>0.0004724</td>
          <td>0.0001545</td>
          <td>646</td>
          <td>406</td>
          <td>45</td>
          <td>69</td>
          <td>9</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>11</td>
          <td>57</td>
          <td>95</td>
          <td>16801</td>
          <td>13444</td>
          <td>13032</td>
          <td>10715</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Joe&#x27;s Jeans Men&#x27;s Slim Fit Straight Leg Brixton</td>
          <td>Joe&#x27;s Jeans</td>
          <td>Jeans</td>
          <td>194.26</td>
          <td>102.07</td>
          <td>1353.0</td>
          <td>647.44</td>
          <td>27</td>
          <td>7</td>
          <td>3</td>
          <td>2</td>
          <td>15</td>
          <td>976.0</td>
          <td>458.49</td>
          <td>0.4785</td>
          <td>0.3</td>
          <td>0.28</td>
          <td>0.0741</td>
          <td>0.6818</td>
          <td>0.0005012</td>
          <td>0.0004627</td>
          <td>0.0001489</td>
          <td>992</td>
          <td>729</td>
          <td>58</td>
          <td>76</td>
          <td>12</td>
          <td>33</td>
          <td>151</td>
          <td>2100</td>
          <td>11</td>
          <td>133</td>
          <td>207</td>
          <td>14773</td>
          <td>11276</td>
          <td>14282</td>
          <td>17370</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Dockers Men&#x27;s Suit Separate Coat</td>
          <td>Dockers</td>
          <td>Suits &amp; Sport Coats</td>
          <td>88.36</td>
          <td>33.97</td>
          <td>231.12</td>
          <td>140.98</td>
          <td>27</td>
          <td>3</td>
          <td>4</td>
          <td>2</td>
          <td>18</td>
          <td>542.11</td>
          <td>337.6</td>
          <td>0.61</td>
          <td>0.5714</td>
          <td>0.12</td>
          <td>0.0741</td>
          <td>0.8571</td>
          <td>8.56e-05</td>
          <td>0.0001008</td>
          <td>0.0001489</td>
          <td>5094</td>
          <td>7229</td>
          <td>2783</td>
          <td>2122</td>
          <td>12</td>
          <td>2358</td>
          <td>30</td>
          <td>2100</td>
          <td>4</td>
          <td>542</td>
          <td>391</td>
          <td>1873</td>
          <td>4252</td>
          <td>22129</td>
          <td>17370</td>
          <td>6057</td>
        </tr>
        <tr>
          <td>Volcom Men&#x27;s Kinkade Jean</td>
          <td>Volcom</td>
          <td>Jeans</td>
          <td>66.67</td>
          <td>35.17</td>
          <td>269.9</td>
          <td>125.86</td>
          <td>27</td>
          <td>4</td>
          <td>3</td>
          <td>5</td>
          <td>15</td>
          <td>538.25</td>
          <td>254.63</td>
          <td>0.4663</td>
          <td>0.4286</td>
          <td>0.1818</td>
          <td>0.1852</td>
          <td>0.7895</td>
          <td>0.0001</td>
          <td>9e-05</td>
          <td>0.0001489</td>
          <td>7633</td>
          <td>6807</td>
          <td>2158</td>
          <td>2560</td>
          <td>12</td>
          <td>776</td>
          <td>151</td>
          <td>24</td>
          <td>11</td>
          <td>562</td>
          <td>723</td>
          <td>15806</td>
          <td>8270</td>
          <td>19358</td>
          <td>10467</td>
          <td>9273</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Wrancher Dress Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.4</td>
          <td>20.2</td>
          <td>242.4</td>
          <td>118.65</td>
          <td>27</td>
          <td>6</td>
          <td>2</td>
          <td>3</td>
          <td>16</td>
          <td>202.0</td>
          <td>102.05</td>
          <td>0.4895</td>
          <td>0.25</td>
          <td>0.25</td>
          <td>0.1111</td>
          <td>0.7273</td>
          <td>8.98e-05</td>
          <td>8.48e-05</td>
          <td>0.0001489</td>
          <td>13728</td>
          <td>13816</td>
          <td>2533</td>
          <td>2788</td>
          <td>12</td>
          <td>84</td>
          <td>844</td>
          <td>526</td>
          <td>7</td>
          <td>3236</td>
          <td>3382</td>
          <td>13585</td>
          <td>11344</td>
          <td>14408</td>
          <td>15570</td>
          <td>11980</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by Average Sale Price</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
  avg_product_sale_price_rank ASC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Alpha Industries Rip Stop Short</td>
          <td>Alpha Industries</td>
          <td>Shorts</td>
          <td>999.0</td>
          <td>482.52</td>
          <td>999.0</td>
          <td>516.48</td>
          <td>8</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>5</td>
          <td>1998.0</td>
          <td>1032.97</td>
          <td>0.517</td>
          <td>0.5</td>
          <td>0.1429</td>
          <td>0.125</td>
          <td>0.8333</td>
          <td>0.0003701</td>
          <td>0.0003691</td>
          <td>4.41e-05</td>
          <td>1</td>
          <td>5</td>
          <td>120</td>
          <td>134</td>
          <td>5507</td>
          <td>13264</td>
          <td>3978</td>
          <td>7029</td>
          <td>3026</td>
          <td>14</td>
          <td>25</td>
          <td>10735</td>
          <td>4275</td>
          <td>20815</td>
          <td>14338</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>Darla</td>
          <td>Alpha Industries</td>
          <td>Outerwear &amp; Coats</td>
          <td>999.0</td>
          <td>404.6</td>
          <td>1998.0</td>
          <td>1188.81</td>
          <td>7</td>
          <td>2</td>
          <td>2</td>
          <td>0</td>
          <td>3</td>
          <td>1998.0</td>
          <td>1188.81</td>
          <td>0.595</td>
          <td>0.5</td>
          <td>0.2857</td>
          <td>0.0</td>
          <td>0.6</td>
          <td>0.0007401</td>
          <td>0.0008496</td>
          <td>3.86e-05</td>
          <td>1</td>
          <td>16</td>
          <td>18</td>
          <td>15</td>
          <td>8625</td>
          <td>6114</td>
          <td>844</td>
          <td>17458</td>
          <td>10869</td>
          <td>14</td>
          <td>14</td>
          <td>2925</td>
          <td>4275</td>
          <td>13238</td>
          <td>17458</td>
          <td>16953</td>
        </tr>
        <tr>
          <td>Woolrich Arctic Parka DF</td>
          <td>Woolrich</td>
          <td>Outerwear &amp; Coats</td>
          <td>990.0</td>
          <td>478.17</td>
          <td>2970.0</td>
          <td>1535.49</td>
          <td>12</td>
          <td>3</td>
          <td>2</td>
          <td>1</td>
          <td>6</td>
          <td>2970.0</td>
          <td>1535.49</td>
          <td>0.517</td>
          <td>0.4</td>
          <td>0.2727</td>
          <td>0.0833</td>
          <td>0.6667</td>
          <td>0.0011002</td>
          <td>0.0010974</td>
          <td>6.62e-05</td>
          <td>3</td>
          <td>6</td>
          <td>5</td>
          <td>6</td>
          <td>694</td>
          <td>2358</td>
          <td>844</td>
          <td>7029</td>
          <td>1398</td>
          <td>4</td>
          <td>4</td>
          <td>10735</td>
          <td>8312</td>
          <td>14284</td>
          <td>17144</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Nobis Yatesy Parka</td>
          <td>Nobis</td>
          <td>Outerwear &amp; Coats</td>
          <td>950.0</td>
          <td>381.9</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>7</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>6</td>
          <td>950.0</td>
          <td>568.1</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.1429</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.86e-05</td>
          <td>4</td>
          <td>24</td>
          <td>22532</td>
          <td>22532</td>
          <td>8625</td>
          <td>22532</td>
          <td>13463</td>
          <td>7029</td>
          <td>1398</td>
          <td>141</td>
          <td>114</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>12706</td>
          <td>1</td>
        </tr>
        <tr>
          <td>The North Face Denali Down Womens Jacket 2013</td>
          <td>The North Face</td>
          <td>Active</td>
          <td>903.0</td>
          <td>395.51</td>
          <td>1806.0</td>
          <td>1014.97</td>
          <td>8</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>6</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.562</td>
          <td>0.0</td>
          <td>0.25</td>
          <td>0.0</td>
          <td>0.75</td>
          <td>0.000669</td>
          <td>0.0007254</td>
          <td>4.41e-05</td>
          <td>5</td>
          <td>20</td>
          <td>21</td>
          <td>25</td>
          <td>5507</td>
          <td>6114</td>
          <td>13463</td>
          <td>17458</td>
          <td>1398</td>
          <td>22642</td>
          <td>22642</td>
          <td>6272</td>
          <td>13463</td>
          <td>14408</td>
          <td>17458</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>The North Face Freedom Mens Ski Pants 2013</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>369.33</td>
          <td>903.0</td>
          <td>533.67</td>
          <td>5</td>
          <td>1</td>
          <td>0</td>
          <td>2</td>
          <td>2</td>
          <td>1806.0</td>
          <td>1067.35</td>
          <td>0.591</td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>0.4</td>
          <td>0.6667</td>
          <td>0.0003345</td>
          <td>0.0003814</td>
          <td>2.76e-05</td>
          <td>5</td>
          <td>31</td>
          <td>149</td>
          <td>122</td>
          <td>16887</td>
          <td>13264</td>
          <td>13463</td>
          <td>2100</td>
          <td>17069</td>
          <td>22</td>
          <td>21</td>
          <td>3279</td>
          <td>13463</td>
          <td>9747</td>
          <td>1689</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>The North Face Women&#x27;s S-XL Oso Jacket</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>378.36</td>
          <td>3612.0</td>
          <td>2098.57</td>
          <td>10</td>
          <td>4</td>
          <td>1</td>
          <td>1</td>
          <td>4</td>
          <td>1806.0</td>
          <td>1049.29</td>
          <td>0.581</td>
          <td>0.2</td>
          <td>0.4444</td>
          <td>0.1</td>
          <td>0.5</td>
          <td>0.001338</td>
          <td>0.0014998</td>
          <td>5.52e-05</td>
          <td>5</td>
          <td>25</td>
          <td>1</td>
          <td>2</td>
          <td>1962</td>
          <td>776</td>
          <td>3978</td>
          <td>7029</td>
          <td>6105</td>
          <td>22</td>
          <td>24</td>
          <td>4209</td>
          <td>12637</td>
          <td>6492</td>
          <td>16366</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>JORDAN DURASHEEN SHORT MENS 404309-109</td>
          <td>Jordan</td>
          <td>Active</td>
          <td>903.0</td>
          <td>370.23</td>
          <td>903.0</td>
          <td>532.77</td>
          <td>4</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>2</td>
          <td>903.0</td>
          <td>532.77</td>
          <td>0.59</td>
          <td>0.5</td>
          <td>0.25</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>0.0003345</td>
          <td>0.0003808</td>
          <td>2.21e-05</td>
          <td>5</td>
          <td>29</td>
          <td>149</td>
          <td>123</td>
          <td>21053</td>
          <td>13264</td>
          <td>3978</td>
          <td>17458</td>
          <td>17069</td>
          <td>155</td>
          <td>138</td>
          <td>3353</td>
          <td>4275</td>
          <td>14408</td>
          <td>17458</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Nike Jordan Retro 11 Bred Bootie Socks</td>
          <td>Jordan</td>
          <td>Socks</td>
          <td>903.0</td>
          <td>557.15</td>
          <td>903.0</td>
          <td>345.85</td>
          <td>7</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>5</td>
          <td>903.0</td>
          <td>345.85</td>
          <td>0.383</td>
          <td>0.0</td>
          <td>0.1667</td>
          <td>0.1429</td>
          <td>0.8333</td>
          <td>0.0003345</td>
          <td>0.0002472</td>
          <td>3.86e-05</td>
          <td>5</td>
          <td>1</td>
          <td>149</td>
          <td>356</td>
          <td>8625</td>
          <td>13264</td>
          <td>13463</td>
          <td>7029</td>
          <td>3026</td>
          <td>155</td>
          <td>367</td>
          <td>21586</td>
          <td>13463</td>
          <td>19436</td>
          <td>12706</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>The North Face Apex Bionic Soft Shell Jacket - Men&#x27;s</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>363.01</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>3</td>
          <td>903.0</td>
          <td>539.99</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.21e-05</td>
          <td>5</td>
          <td>34</td>
          <td>22532</td>
          <td>22532</td>
          <td>21053</td>
          <td>22532</td>
          <td>3978</td>
          <td>17458</td>
          <td>10869</td>
          <td>155</td>
          <td>126</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
        <tr>
          <td>NIKE WOMEN&#x27;S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort*</td>
          <td>Nike</td>
          <td>Plus</td>
          <td>903.0</td>
          <td>420.8</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>4</td>
          <td>903.0</td>
          <td>482.2</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.76e-05</td>
          <td>5</td>
          <td>12</td>
          <td>22532</td>
          <td>22532</td>
          <td>16887</td>
          <td>22532</td>
          <td>3978</td>
          <td>17458</td>
          <td>6105</td>
          <td>155</td>
          <td>177</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
        <tr>
          <td>The North Face Nuptse 2 Jacket - Noah Green/TNF Black</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>370.23</td>
          <td>1806.0</td>
          <td>1065.54</td>
          <td>8</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>6</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.59</td>
          <td>0.0</td>
          <td>0.25</td>
          <td>0.0</td>
          <td>0.75</td>
          <td>0.000669</td>
          <td>0.0007615</td>
          <td>4.41e-05</td>
          <td>5</td>
          <td>29</td>
          <td>21</td>
          <td>19</td>
          <td>5507</td>
          <td>6114</td>
          <td>13463</td>
          <td>17458</td>
          <td>1398</td>
          <td>22642</td>
          <td>22642</td>
          <td>3353</td>
          <td>13463</td>
          <td>14408</td>
          <td>17458</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>NIKE WOMEN&#x27;S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort*</td>
          <td>Nike</td>
          <td>Active</td>
          <td>903.0</td>
          <td>403.64</td>
          <td>903.0</td>
          <td>499.36</td>
          <td>5</td>
          <td>1</td>
          <td>2</td>
          <td>0</td>
          <td>2</td>
          <td>1806.0</td>
          <td>998.72</td>
          <td>0.553</td>
          <td>0.6667</td>
          <td>0.2</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>0.0003345</td>
          <td>0.0003569</td>
          <td>2.76e-05</td>
          <td>5</td>
          <td>17</td>
          <td>149</td>
          <td>146</td>
          <td>16887</td>
          <td>13264</td>
          <td>844</td>
          <td>17458</td>
          <td>17069</td>
          <td>22</td>
          <td>28</td>
          <td>7266</td>
          <td>3055</td>
          <td>17510</td>
          <td>17458</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>NIKE WOMEN&#x27;S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort*</td>
          <td>Nike</td>
          <td>Intimates</td>
          <td>903.0</td>
          <td>512.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>1</td>
          <td>2709.0</td>
          <td>1173.0</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.75</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.21e-05</td>
          <td>5</td>
          <td>4</td>
          <td>22532</td>
          <td>22532</td>
          <td>21053</td>
          <td>22532</td>
          <td>13463</td>
          <td>526</td>
          <td>23197</td>
          <td>5</td>
          <td>15</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>109</td>
          <td>1</td>
        </tr>
        <tr>
          <td>The North Face Denali Down Mens Jacket 2013</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>436.15</td>
          <td>2709.0</td>
          <td>1400.55</td>
          <td>13</td>
          <td>3</td>
          <td>2</td>
          <td>2</td>
          <td>6</td>
          <td>3612.0</td>
          <td>1867.4</td>
          <td>0.517</td>
          <td>0.4</td>
          <td>0.2727</td>
          <td>0.1538</td>
          <td>0.6667</td>
          <td>0.0010035</td>
          <td>0.001001</td>
          <td>7.17e-05</td>
          <td>5</td>
          <td>10</td>
          <td>7</td>
          <td>7</td>
          <td>423</td>
          <td>2358</td>
          <td>844</td>
          <td>2100</td>
          <td>1398</td>
          <td>2</td>
          <td>3</td>
          <td>10735</td>
          <td>8312</td>
          <td>14284</td>
          <td>12634</td>
          <td>12990</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by Average Cost</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
  avg_product_cost_rank ASC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Nike Jordan Retro 11 Bred Bootie Socks</td>
          <td>Jordan</td>
          <td>Socks</td>
          <td>903.0</td>
          <td>557.15</td>
          <td>903.0</td>
          <td>345.85</td>
          <td>7</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>5</td>
          <td>903.0</td>
          <td>345.85</td>
          <td>0.383</td>
          <td>0.0</td>
          <td>0.1667</td>
          <td>0.1429</td>
          <td>0.8333</td>
          <td>0.0003345</td>
          <td>0.0002472</td>
          <td>3.86e-05</td>
          <td>5</td>
          <td>1</td>
          <td>149</td>
          <td>356</td>
          <td>8625</td>
          <td>13264</td>
          <td>13463</td>
          <td>7029</td>
          <td>3026</td>
          <td>155</td>
          <td>367</td>
          <td>21586</td>
          <td>13463</td>
          <td>19436</td>
          <td>12706</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>Jordan Low Quarter Sock Style # 427411</td>
          <td>Nike</td>
          <td>Socks</td>
          <td>903.0</td>
          <td>537.29</td>
          <td>903.0</td>
          <td>365.71</td>
          <td>7</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>5</td>
          <td>903.0</td>
          <td>365.71</td>
          <td>0.405</td>
          <td>0.0</td>
          <td>0.1667</td>
          <td>0.1429</td>
          <td>0.8333</td>
          <td>0.0003345</td>
          <td>0.0002614</td>
          <td>3.86e-05</td>
          <td>5</td>
          <td>2</td>
          <td>149</td>
          <td>311</td>
          <td>8625</td>
          <td>13264</td>
          <td>13463</td>
          <td>7029</td>
          <td>3026</td>
          <td>155</td>
          <td>323</td>
          <td>20649</td>
          <td>13463</td>
          <td>19436</td>
          <td>12706</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>The North Face Apex Bionic Soft Shell Jacket - Men&#x27;s</td>
          <td>The North Face</td>
          <td>Fashion Hoodies &amp; Sweatshirts</td>
          <td>903.0</td>
          <td>524.64</td>
          <td>1806.0</td>
          <td>756.71</td>
          <td>6</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>4</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.419</td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>0.000669</td>
          <td>0.0005408</td>
          <td>3.31e-05</td>
          <td>5</td>
          <td>3</td>
          <td>21</td>
          <td>55</td>
          <td>12532</td>
          <td>6114</td>
          <td>13463</td>
          <td>17458</td>
          <td>6105</td>
          <td>22642</td>
          <td>22642</td>
          <td>19960</td>
          <td>13463</td>
          <td>9747</td>
          <td>17458</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>NIKE WOMEN&#x27;S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort*</td>
          <td>Nike</td>
          <td>Intimates</td>
          <td>903.0</td>
          <td>512.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>1</td>
          <td>2709.0</td>
          <td>1173.0</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.75</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.21e-05</td>
          <td>5</td>
          <td>4</td>
          <td>22532</td>
          <td>22532</td>
          <td>21053</td>
          <td>22532</td>
          <td>13463</td>
          <td>526</td>
          <td>23197</td>
          <td>5</td>
          <td>15</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>109</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Alpha Industries Rip Stop Short</td>
          <td>Alpha Industries</td>
          <td>Shorts</td>
          <td>999.0</td>
          <td>482.52</td>
          <td>999.0</td>
          <td>516.48</td>
          <td>8</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>5</td>
          <td>1998.0</td>
          <td>1032.97</td>
          <td>0.517</td>
          <td>0.5</td>
          <td>0.1429</td>
          <td>0.125</td>
          <td>0.8333</td>
          <td>0.0003701</td>
          <td>0.0003691</td>
          <td>4.41e-05</td>
          <td>1</td>
          <td>5</td>
          <td>120</td>
          <td>134</td>
          <td>5507</td>
          <td>13264</td>
          <td>3978</td>
          <td>7029</td>
          <td>3026</td>
          <td>14</td>
          <td>25</td>
          <td>10735</td>
          <td>4275</td>
          <td>20815</td>
          <td>14338</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>Woolrich Arctic Parka DF</td>
          <td>Woolrich</td>
          <td>Outerwear &amp; Coats</td>
          <td>990.0</td>
          <td>478.17</td>
          <td>2970.0</td>
          <td>1535.49</td>
          <td>12</td>
          <td>3</td>
          <td>2</td>
          <td>1</td>
          <td>6</td>
          <td>2970.0</td>
          <td>1535.49</td>
          <td>0.517</td>
          <td>0.4</td>
          <td>0.2727</td>
          <td>0.0833</td>
          <td>0.6667</td>
          <td>0.0011002</td>
          <td>0.0010974</td>
          <td>6.62e-05</td>
          <td>3</td>
          <td>6</td>
          <td>5</td>
          <td>6</td>
          <td>694</td>
          <td>2358</td>
          <td>844</td>
          <td>7029</td>
          <td>1398</td>
          <td>4</td>
          <td>4</td>
          <td>10735</td>
          <td>8312</td>
          <td>14284</td>
          <td>17144</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Quiksilver Men&#x27;s Rockefeller Walkshort</td>
          <td>Quiksilver</td>
          <td>Shorts</td>
          <td>903.0</td>
          <td>472.27</td>
          <td>1806.0</td>
          <td>861.46</td>
          <td>6</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>4</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.477</td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>0.000669</td>
          <td>0.0006157</td>
          <td>3.31e-05</td>
          <td>5</td>
          <td>7</td>
          <td>21</td>
          <td>34</td>
          <td>12532</td>
          <td>6114</td>
          <td>13463</td>
          <td>17458</td>
          <td>6105</td>
          <td>22642</td>
          <td>22642</td>
          <td>14881</td>
          <td>13463</td>
          <td>9747</td>
          <td>17458</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>AIR JORDAN DOMINATE SHORTS MENS 465071-100</td>
          <td>Jordan</td>
          <td>Shorts</td>
          <td>903.0</td>
          <td>454.21</td>
          <td>2709.0</td>
          <td>1346.37</td>
          <td>5</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>2</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.497</td>
          <td>0.0</td>
          <td>0.6</td>
          <td>0.0</td>
          <td>0.4</td>
          <td>0.0010035</td>
          <td>0.0009622</td>
          <td>2.76e-05</td>
          <td>5</td>
          <td>8</td>
          <td>7</td>
          <td>9</td>
          <td>16887</td>
          <td>2358</td>
          <td>13463</td>
          <td>17458</td>
          <td>17069</td>
          <td>22642</td>
          <td>22642</td>
          <td>12874</td>
          <td>13463</td>
          <td>2189</td>
          <td>17458</td>
          <td>23875</td>
        </tr>
        <tr>
          <td>The North Face Denali Down Womens Jacket 2013</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>437.05</td>
          <td>903.0</td>
          <td>465.95</td>
          <td>5</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>3</td>
          <td>903.0</td>
          <td>465.95</td>
          <td>0.516</td>
          <td>0.0</td>
          <td>0.25</td>
          <td>0.2</td>
          <td>0.75</td>
          <td>0.0003345</td>
          <td>0.000333</td>
          <td>2.76e-05</td>
          <td>5</td>
          <td>9</td>
          <td>149</td>
          <td>173</td>
          <td>16887</td>
          <td>13264</td>
          <td>13463</td>
          <td>7029</td>
          <td>10869</td>
          <td>155</td>
          <td>198</td>
          <td>10830</td>
          <td>13463</td>
          <td>14408</td>
          <td>8435</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>The North Face Denali Down Mens Jacket 2013</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>436.15</td>
          <td>2709.0</td>
          <td>1400.55</td>
          <td>13</td>
          <td>3</td>
          <td>2</td>
          <td>2</td>
          <td>6</td>
          <td>3612.0</td>
          <td>1867.4</td>
          <td>0.517</td>
          <td>0.4</td>
          <td>0.2727</td>
          <td>0.1538</td>
          <td>0.6667</td>
          <td>0.0010035</td>
          <td>0.001001</td>
          <td>7.17e-05</td>
          <td>5</td>
          <td>10</td>
          <td>7</td>
          <td>7</td>
          <td>423</td>
          <td>2358</td>
          <td>844</td>
          <td>2100</td>
          <td>1398</td>
          <td>2</td>
          <td>3</td>
          <td>10735</td>
          <td>8312</td>
          <td>14284</td>
          <td>12634</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Catherine Malandrino Women&#x27;s Skinny Stretch Leather Pant</td>
          <td>Catherine Malandrino</td>
          <td>Pants &amp; Capris</td>
          <td>895.0</td>
          <td>434.07</td>
          <td>895.0</td>
          <td>460.93</td>
          <td>7</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>4</td>
          <td>1790.0</td>
          <td>921.85</td>
          <td>0.515</td>
          <td>0.5</td>
          <td>0.1667</td>
          <td>0.1429</td>
          <td>0.8</td>
          <td>0.0003315</td>
          <td>0.0003294</td>
          <td>3.86e-05</td>
          <td>29</td>
          <td>11</td>
          <td>162</td>
          <td>180</td>
          <td>8625</td>
          <td>13264</td>
          <td>3978</td>
          <td>7029</td>
          <td>6105</td>
          <td>29</td>
          <td>33</td>
          <td>10918</td>
          <td>4275</td>
          <td>19436</td>
          <td>12706</td>
          <td>7598</td>
        </tr>
        <tr>
          <td>NIKE WOMEN&#x27;S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort*</td>
          <td>Nike</td>
          <td>Plus</td>
          <td>903.0</td>
          <td>420.8</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>4</td>
          <td>903.0</td>
          <td>482.2</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.76e-05</td>
          <td>5</td>
          <td>12</td>
          <td>22532</td>
          <td>22532</td>
          <td>16887</td>
          <td>22532</td>
          <td>3978</td>
          <td>17458</td>
          <td>6105</td>
          <td>155</td>
          <td>177</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
        <tr>
          <td>The North Face Apex Bionic Mens Soft Shell Ski Jacket 2013</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>419.9</td>
          <td>1806.0</td>
          <td>966.21</td>
          <td>7</td>
          <td>2</td>
          <td>1</td>
          <td>1</td>
          <td>3</td>
          <td>1806.0</td>
          <td>966.21</td>
          <td>0.535</td>
          <td>0.3333</td>
          <td>0.3333</td>
          <td>0.1429</td>
          <td>0.6</td>
          <td>0.000669</td>
          <td>0.0006905</td>
          <td>3.86e-05</td>
          <td>5</td>
          <td>13</td>
          <td>21</td>
          <td>30</td>
          <td>8625</td>
          <td>6114</td>
          <td>3978</td>
          <td>7029</td>
          <td>10869</td>
          <td>22</td>
          <td>30</td>
          <td>9071</td>
          <td>8752</td>
          <td>9747</td>
          <td>12706</td>
          <td>16953</td>
        </tr>
        <tr>
          <td>Mens Nike AirJordan Varsity Hoodie Jacket Grey / Black 451582-066</td>
          <td>Jordan</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>409.06</td>
          <td>903.0</td>
          <td>493.94</td>
          <td>8</td>
          <td>1</td>
          <td>2</td>
          <td>1</td>
          <td>4</td>
          <td>2709.0</td>
          <td>1481.82</td>
          <td>0.547</td>
          <td>0.6667</td>
          <td>0.1429</td>
          <td>0.125</td>
          <td>0.8</td>
          <td>0.0003345</td>
          <td>0.000353</td>
          <td>4.41e-05</td>
          <td>5</td>
          <td>14</td>
          <td>149</td>
          <td>153</td>
          <td>5507</td>
          <td>13264</td>
          <td>844</td>
          <td>7029</td>
          <td>6105</td>
          <td>5</td>
          <td>6</td>
          <td>7915</td>
          <td>3055</td>
          <td>20815</td>
          <td>14338</td>
          <td>7598</td>
        </tr>
        <tr>
          <td>Diesel Men&#x27;s Lophophora Leather Jacket</td>
          <td>Diesel</td>
          <td>Outerwear &amp; Coats</td>
          <td>898.0</td>
          <td>408.59</td>
          <td>1796.0</td>
          <td>978.82</td>
          <td>5</td>
          <td>2</td>
          <td>0</td>
          <td>2</td>
          <td>1</td>
          <td>1796.0</td>
          <td>978.82</td>
          <td>0.545</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>0.4</td>
          <td>0.3333</td>
          <td>0.0006653</td>
          <td>0.0006996</td>
          <td>2.76e-05</td>
          <td>28</td>
          <td>15</td>
          <td>29</td>
          <td>28</td>
          <td>16887</td>
          <td>6114</td>
          <td>13463</td>
          <td>2100</td>
          <td>23197</td>
          <td>28</td>
          <td>29</td>
          <td>8121</td>
          <td>13463</td>
          <td>1185</td>
          <td>1689</td>
          <td>24854</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by Completion Rate</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
WHERE unit_orders_placed_rank &lt;= 15
ORDER BY
  completion_rate_rank ASC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>HUGO BOSS Men&#x27;s Long Pant</td>
          <td>HUGO BOSS</td>
          <td>Sleep &amp; Lounge</td>
          <td>74.72</td>
          <td>28.3</td>
          <td>1033.11</td>
          <td>648.16</td>
          <td>33</td>
          <td>14</td>
          <td>0</td>
          <td>3</td>
          <td>16</td>
          <td>233.01</td>
          <td>138.21</td>
          <td>0.6274</td>
          <td>0.0</td>
          <td>0.4667</td>
          <td>0.0909</td>
          <td>0.5333</td>
          <td>0.0003827</td>
          <td>0.0004632</td>
          <td>0.000182</td>
          <td>6501</td>
          <td>9383</td>
          <td>113</td>
          <td>75</td>
          <td>6</td>
          <td>1</td>
          <td>13463</td>
          <td>526</td>
          <td>7</td>
          <td>2702</td>
          <td>2165</td>
          <td>933</td>
          <td>13463</td>
          <td>6418</td>
          <td>16872</td>
          <td>19494</td>
        </tr>
        <tr>
          <td>Hanes Men&#x27;s 4 Pack Boxer Brief</td>
          <td>Hanes</td>
          <td>Underwear</td>
          <td>25.0</td>
          <td>11.52</td>
          <td>250.0</td>
          <td>133.47</td>
          <td>28</td>
          <td>10</td>
          <td>2</td>
          <td>5</td>
          <td>11</td>
          <td>175.0</td>
          <td>92.77</td>
          <td>0.5339</td>
          <td>0.1667</td>
          <td>0.4348</td>
          <td>0.1786</td>
          <td>0.5238</td>
          <td>9.26e-05</td>
          <td>9.54e-05</td>
          <td>0.0001545</td>
          <td>19651</td>
          <td>20997</td>
          <td>2432</td>
          <td>2340</td>
          <td>9</td>
          <td>4</td>
          <td>844</td>
          <td>24</td>
          <td>43</td>
          <td>4152</td>
          <td>3935</td>
          <td>9232</td>
          <td>13196</td>
          <td>6738</td>
          <td>10715</td>
          <td>19500</td>
        </tr>
        <tr>
          <td>Joseph Abboud Men&#x27;s Two-button Side Vent Sport Coat</td>
          <td>Joseph Abboud</td>
          <td>Suits &amp; Sport Coats</td>
          <td>264.0</td>
          <td>101.9</td>
          <td>2904.0</td>
          <td>1759.82</td>
          <td>30</td>
          <td>11</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>1056.0</td>
          <td>656.57</td>
          <td>0.606</td>
          <td>0.1538</td>
          <td>0.3929</td>
          <td>0.0667</td>
          <td>0.5769</td>
          <td>0.0010758</td>
          <td>0.0012577</td>
          <td>0.0001655</td>
          <td>430</td>
          <td>734</td>
          <td>6</td>
          <td>5</td>
          <td>7</td>
          <td>3</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>112</td>
          <td>91</td>
          <td>2144</td>
          <td>13388</td>
          <td>9081</td>
          <td>17408</td>
          <td>18610</td>
        </tr>
        <tr>
          <td>Volcom Men&#x27;s Vorta Slim Straight Leg Fit Jean</td>
          <td>Volcom</td>
          <td>Jeans</td>
          <td>73.57</td>
          <td>41.13</td>
          <td>574.85</td>
          <td>249.86</td>
          <td>27</td>
          <td>8</td>
          <td>1</td>
          <td>4</td>
          <td>14</td>
          <td>387.8</td>
          <td>166.89</td>
          <td>0.4347</td>
          <td>0.1111</td>
          <td>0.3478</td>
          <td>0.1481</td>
          <td>0.6364</td>
          <td>0.0002129</td>
          <td>0.0001786</td>
          <td>0.0001489</td>
          <td>6603</td>
          <td>5251</td>
          <td>467</td>
          <td>746</td>
          <td>12</td>
          <td>16</td>
          <td>3978</td>
          <td>126</td>
          <td>22</td>
          <td>1091</td>
          <td>1537</td>
          <td>18678</td>
          <td>13456</td>
          <td>9743</td>
          <td>12705</td>
          <td>16487</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Rugged Wear Classic Fit Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.87</td>
          <td>22.23</td>
          <td>367.56</td>
          <td>169.24</td>
          <td>38</td>
          <td>9</td>
          <td>5</td>
          <td>9</td>
          <td>15</td>
          <td>596.43</td>
          <td>273.96</td>
          <td>0.4604</td>
          <td>0.3571</td>
          <td>0.3103</td>
          <td>0.2368</td>
          <td>0.625</td>
          <td>0.0001362</td>
          <td>0.000121</td>
          <td>0.0002096</td>
          <td>13688</td>
          <td>12514</td>
          <td>1205</td>
          <td>1552</td>
          <td>3</td>
          <td>5</td>
          <td>5</td>
          <td>1</td>
          <td>11</td>
          <td>440</td>
          <td>628</td>
          <td>16340</td>
          <td>8749</td>
          <td>13014</td>
          <td>7776</td>
          <td>16547</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Leg Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>227.86</td>
          <td>123.14</td>
          <td>1452.0</td>
          <td>661.01</td>
          <td>28</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>15</td>
          <td>1430.0</td>
          <td>645.85</td>
          <td>0.4552</td>
          <td>0.125</td>
          <td>0.3043</td>
          <td>0.1786</td>
          <td>0.6818</td>
          <td>0.0005379</td>
          <td>0.0004724</td>
          <td>0.0001545</td>
          <td>646</td>
          <td>406</td>
          <td>45</td>
          <td>69</td>
          <td>9</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>11</td>
          <td>57</td>
          <td>95</td>
          <td>16801</td>
          <td>13444</td>
          <td>13032</td>
          <td>10715</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Genuine Tampa Cargo Short</td>
          <td>Wrangler</td>
          <td>Shorts</td>
          <td>31.37</td>
          <td>15.61</td>
          <td>229.94</td>
          <td>116.44</td>
          <td>29</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>16</td>
          <td>179.94</td>
          <td>90.54</td>
          <td>0.5064</td>
          <td>0.125</td>
          <td>0.2917</td>
          <td>0.1724</td>
          <td>0.6957</td>
          <td>8.52e-05</td>
          <td>8.32e-05</td>
          <td>0.00016</td>
          <td>17403</td>
          <td>17266</td>
          <td>2818</td>
          <td>2869</td>
          <td>8</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>7</td>
          <td>3935</td>
          <td>4081</td>
          <td>11924</td>
          <td>13444</td>
          <td>13236</td>
          <td>10730</td>
          <td>12964</td>
        </tr>
        <tr>
          <td>Joe&#x27;s Jeans Men&#x27;s Slim Fit Straight Leg Brixton</td>
          <td>Joe&#x27;s Jeans</td>
          <td>Jeans</td>
          <td>194.26</td>
          <td>102.07</td>
          <td>1353.0</td>
          <td>647.44</td>
          <td>27</td>
          <td>7</td>
          <td>3</td>
          <td>2</td>
          <td>15</td>
          <td>976.0</td>
          <td>458.49</td>
          <td>0.4785</td>
          <td>0.3</td>
          <td>0.28</td>
          <td>0.0741</td>
          <td>0.6818</td>
          <td>0.0005012</td>
          <td>0.0004627</td>
          <td>0.0001489</td>
          <td>992</td>
          <td>729</td>
          <td>58</td>
          <td>76</td>
          <td>12</td>
          <td>33</td>
          <td>151</td>
          <td>2100</td>
          <td>11</td>
          <td>133</td>
          <td>207</td>
          <td>14773</td>
          <td>11276</td>
          <td>14282</td>
          <td>17370</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Kenneth Cole REACTION Men&#x27;s Passcase Wallet</td>
          <td>Kenneth Cole REACTION</td>
          <td>Accessories</td>
          <td>18.91</td>
          <td>7.72</td>
          <td>152.71</td>
          <td>89.4</td>
          <td>34</td>
          <td>8</td>
          <td>4</td>
          <td>4</td>
          <td>18</td>
          <td>150.85</td>
          <td>90.57</td>
          <td>0.5854</td>
          <td>0.3333</td>
          <td>0.2667</td>
          <td>0.1176</td>
          <td>0.6923</td>
          <td>5.66e-05</td>
          <td>6.39e-05</td>
          <td>0.0001876</td>
          <td>23389</td>
          <td>24481</td>
          <td>4958</td>
          <td>4188</td>
          <td>4</td>
          <td>16</td>
          <td>30</td>
          <td>126</td>
          <td>4</td>
          <td>5015</td>
          <td>4078</td>
          <td>3806</td>
          <td>8752</td>
          <td>14395</td>
          <td>15553</td>
          <td>12966</td>
        </tr>
        <tr>
          <td>Chaps Big and Tall Solid V-Neck Vest</td>
          <td>Chaps</td>
          <td>Sweaters</td>
          <td>39.88</td>
          <td>20.32</td>
          <td>279.16</td>
          <td>134.91</td>
          <td>28</td>
          <td>7</td>
          <td>4</td>
          <td>1</td>
          <td>16</td>
          <td>199.4</td>
          <td>99.06</td>
          <td>0.4833</td>
          <td>0.3636</td>
          <td>0.2593</td>
          <td>0.0357</td>
          <td>0.6957</td>
          <td>0.0001034</td>
          <td>9.64e-05</td>
          <td>0.0001545</td>
          <td>14437</td>
          <td>13747</td>
          <td>2029</td>
          <td>2288</td>
          <td>9</td>
          <td>33</td>
          <td>30</td>
          <td>7029</td>
          <td>7</td>
          <td>3354</td>
          <td>3543</td>
          <td>14237</td>
          <td>8748</td>
          <td>14407</td>
          <td>17457</td>
          <td>12964</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Wrancher Dress Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.4</td>
          <td>20.2</td>
          <td>242.4</td>
          <td>118.65</td>
          <td>27</td>
          <td>6</td>
          <td>2</td>
          <td>3</td>
          <td>16</td>
          <td>202.0</td>
          <td>102.05</td>
          <td>0.4895</td>
          <td>0.25</td>
          <td>0.25</td>
          <td>0.1111</td>
          <td>0.7273</td>
          <td>8.98e-05</td>
          <td>8.48e-05</td>
          <td>0.0001489</td>
          <td>13728</td>
          <td>13816</td>
          <td>2533</td>
          <td>2788</td>
          <td>12</td>
          <td>84</td>
          <td>844</td>
          <td>526</td>
          <td>7</td>
          <td>3236</td>
          <td>3382</td>
          <td>13585</td>
          <td>11344</td>
          <td>14408</td>
          <td>15570</td>
          <td>11980</td>
        </tr>
        <tr>
          <td>7 For All Mankind Men&#x27;s Standard Classic Straight Leg Jean</td>
          <td>7 For All Mankind</td>
          <td>Jeans</td>
          <td>157.45</td>
          <td>80.97</td>
          <td>1435.0</td>
          <td>696.01</td>
          <td>42</td>
          <td>9</td>
          <td>5</td>
          <td>5</td>
          <td>23</td>
          <td>1673.0</td>
          <td>844.04</td>
          <td>0.485</td>
          <td>0.3571</td>
          <td>0.2432</td>
          <td>0.119</td>
          <td>0.7188</td>
          <td>0.0005316</td>
          <td>0.0004974</td>
          <td>0.0002317</td>
          <td>1798</td>
          <td>1488</td>
          <td>46</td>
          <td>60</td>
          <td>2</td>
          <td>5</td>
          <td>5</td>
          <td>24</td>
          <td>2</td>
          <td>32</td>
          <td>41</td>
          <td>14028</td>
          <td>8749</td>
          <td>17091</td>
          <td>15552</td>
          <td>12034</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Premium Performance Cowboy Cut Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>47.45</td>
          <td>25.88</td>
          <td>570.83</td>
          <td>264.22</td>
          <td>58</td>
          <td>12</td>
          <td>2</td>
          <td>7</td>
          <td>37</td>
          <td>417.81</td>
          <td>189.65</td>
          <td>0.4629</td>
          <td>0.1429</td>
          <td>0.2353</td>
          <td>0.1207</td>
          <td>0.7551</td>
          <td>0.0002115</td>
          <td>0.0001888</td>
          <td>0.00032</td>
          <td>12004</td>
          <td>10508</td>
          <td>470</td>
          <td>662</td>
          <td>1</td>
          <td>2</td>
          <td>844</td>
          <td>2</td>
          <td>1</td>
          <td>905</td>
          <td>1224</td>
          <td>16149</td>
          <td>13389</td>
          <td>17092</td>
          <td>15548</td>
          <td>9486</td>
        </tr>
        <tr>
          <td>Volcom Men&#x27;s Kinkade Jean</td>
          <td>Volcom</td>
          <td>Jeans</td>
          <td>66.67</td>
          <td>35.17</td>
          <td>269.9</td>
          <td>125.86</td>
          <td>27</td>
          <td>4</td>
          <td>3</td>
          <td>5</td>
          <td>15</td>
          <td>538.25</td>
          <td>254.63</td>
          <td>0.4663</td>
          <td>0.4286</td>
          <td>0.1818</td>
          <td>0.1852</td>
          <td>0.7895</td>
          <td>0.0001</td>
          <td>9e-05</td>
          <td>0.0001489</td>
          <td>7633</td>
          <td>6807</td>
          <td>2158</td>
          <td>2560</td>
          <td>12</td>
          <td>776</td>
          <td>151</td>
          <td>24</td>
          <td>11</td>
          <td>562</td>
          <td>723</td>
          <td>15806</td>
          <td>8270</td>
          <td>19358</td>
          <td>10467</td>
          <td>9273</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>246.88</td>
          <td>129.05</td>
          <td>1366.0</td>
          <td>666.07</td>
          <td>34</td>
          <td>5</td>
          <td>4</td>
          <td>3</td>
          <td>22</td>
          <td>1400.0</td>
          <td>654.5</td>
          <td>0.4876</td>
          <td>0.4444</td>
          <td>0.1613</td>
          <td>0.0882</td>
          <td>0.8148</td>
          <td>0.000506</td>
          <td>0.000476</td>
          <td>0.0001876</td>
          <td>534</td>
          <td>354</td>
          <td>56</td>
          <td>65</td>
          <td>4</td>
          <td>251</td>
          <td>30</td>
          <td>526</td>
          <td>3</td>
          <td>63</td>
          <td>92</td>
          <td>13792</td>
          <td>8264</td>
          <td>20804</td>
          <td>17143</td>
          <td>7595</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by Return Rate</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>IGIGI by Yuliya Raquel Plus Size Kandinsky Gown</td>
          <td>IGIGI by Yuliya Raquel</td>
          <td>Dresses</td>
          <td>325.0</td>
          <td>136.17</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>13</td>
          <td>0</td>
          <td>3</td>
          <td>5</td>
          <td>5</td>
          <td>2600.0</td>
          <td>1510.6</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.3846</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>7.17e-05</td>
          <td>236</td>
          <td>300</td>
          <td>22532</td>
          <td>22532</td>
          <td>423</td>
          <td>22532</td>
          <td>151</td>
          <td>24</td>
          <td>3026</td>
          <td>7</td>
          <td>5</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>2333</td>
          <td>1</td>
        </tr>
        <tr>
          <td>MiH Jeans Women&#x27;s Aztec Jacket</td>
          <td>MiH Jeans</td>
          <td>Blazers &amp; Jackets</td>
          <td>495.0</td>
          <td>169.79</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>6</td>
          <td>0</td>
          <td>2</td>
          <td>2</td>
          <td>2</td>
          <td>1980.0</td>
          <td>1300.86</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.31e-05</td>
          <td>74</td>
          <td>157</td>
          <td>22532</td>
          <td>22532</td>
          <td>12532</td>
          <td>22532</td>
          <td>844</td>
          <td>2100</td>
          <td>17069</td>
          <td>16</td>
          <td>11</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>2619</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Canada Goose Men&#x27;s The Chateau Jacket</td>
          <td>Canada Goose</td>
          <td>Active</td>
          <td>815.0</td>
          <td>337.41</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>6</td>
          <td>0</td>
          <td>1</td>
          <td>4</td>
          <td>1</td>
          <td>4075.0</td>
          <td>2387.95</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.31e-05</td>
          <td>31</td>
          <td>39</td>
          <td>22532</td>
          <td>22532</td>
          <td>12532</td>
          <td>22532</td>
          <td>3978</td>
          <td>126</td>
          <td>23197</td>
          <td>1</td>
          <td>1</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>154</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Chilliwack Bomber</td>
          <td>Canada Goose</td>
          <td>Outerwear &amp; Coats</td>
          <td>695.0</td>
          <td>287.73</td>
          <td>695.0</td>
          <td>407.27</td>
          <td>8</td>
          <td>1</td>
          <td>3</td>
          <td>2</td>
          <td>2</td>
          <td>3475.0</td>
          <td>2036.35</td>
          <td>0.586</td>
          <td>0.75</td>
          <td>0.1667</td>
          <td>0.25</td>
          <td>0.6667</td>
          <td>0.0002575</td>
          <td>0.0002911</td>
          <td>4.41e-05</td>
          <td>46</td>
          <td>52</td>
          <td>294</td>
          <td>240</td>
          <td>5507</td>
          <td>13264</td>
          <td>151</td>
          <td>2100</td>
          <td>17069</td>
          <td>3</td>
          <td>2</td>
          <td>3719</td>
          <td>2834</td>
          <td>19436</td>
          <td>5542</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Mens Nike AirJordan Varsity Hoodie Jacket Grey / Black 451582-066</td>
          <td>Jordan</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>409.06</td>
          <td>903.0</td>
          <td>493.94</td>
          <td>8</td>
          <td>1</td>
          <td>2</td>
          <td>1</td>
          <td>4</td>
          <td>2709.0</td>
          <td>1481.82</td>
          <td>0.547</td>
          <td>0.6667</td>
          <td>0.1429</td>
          <td>0.125</td>
          <td>0.8</td>
          <td>0.0003345</td>
          <td>0.000353</td>
          <td>4.41e-05</td>
          <td>5</td>
          <td>14</td>
          <td>149</td>
          <td>153</td>
          <td>5507</td>
          <td>13264</td>
          <td>844</td>
          <td>7029</td>
          <td>6105</td>
          <td>5</td>
          <td>6</td>
          <td>7915</td>
          <td>3055</td>
          <td>20815</td>
          <td>14338</td>
          <td>7598</td>
        </tr>
        <tr>
          <td>Joseph Abboud Men&#x27;s Super 120&#x27;s Two Button Side Vent Single Pleat Pant Tuxedo With Grosgrain Notch Lapel</td>
          <td>Joseph Abboud</td>
          <td>Suits &amp; Sport Coats</td>
          <td>405.26</td>
          <td>145.08</td>
          <td>405.26</td>
          <td>260.18</td>
          <td>11</td>
          <td>1</td>
          <td>2</td>
          <td>3</td>
          <td>5</td>
          <td>2026.3</td>
          <td>1300.88</td>
          <td>0.642</td>
          <td>0.6667</td>
          <td>0.125</td>
          <td>0.2727</td>
          <td>0.8333</td>
          <td>0.0001501</td>
          <td>0.0001859</td>
          <td>6.07e-05</td>
          <td>108</td>
          <td>256</td>
          <td>961</td>
          <td>686</td>
          <td>1161</td>
          <td>13264</td>
          <td>844</td>
          <td>526</td>
          <td>3026</td>
          <td>13</td>
          <td>10</td>
          <td>361</td>
          <td>3055</td>
          <td>21675</td>
          <td>5408</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Mystique</td>
          <td>Canada Goose</td>
          <td>Outerwear &amp; Coats</td>
          <td>750.0</td>
          <td>353.25</td>
          <td>1500.0</td>
          <td>793.5</td>
          <td>6</td>
          <td>2</td>
          <td>3</td>
          <td>0</td>
          <td>1</td>
          <td>2250.0</td>
          <td>1190.25</td>
          <td>0.529</td>
          <td>0.6</td>
          <td>0.3333</td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>0.0005557</td>
          <td>0.0005671</td>
          <td>3.31e-05</td>
          <td>37</td>
          <td>35</td>
          <td>41</td>
          <td>44</td>
          <td>12532</td>
          <td>6114</td>
          <td>151</td>
          <td>17458</td>
          <td>23197</td>
          <td>9</td>
          <td>13</td>
          <td>9645</td>
          <td>4103</td>
          <td>9747</td>
          <td>17458</td>
          <td>24854</td>
        </tr>
        <tr>
          <td>DOLCE &amp; GABBANA DG4167 501/8G BLACK GRAY GRADIENT 5917</td>
          <td>Dolce &amp; Gabbana</td>
          <td>Accessories</td>
          <td>243.0</td>
          <td>94.67</td>
          <td>486.0</td>
          <td>294.03</td>
          <td>14</td>
          <td>2</td>
          <td>3</td>
          <td>5</td>
          <td>4</td>
          <td>1944.0</td>
          <td>1194.59</td>
          <td>0.605</td>
          <td>0.6</td>
          <td>0.2222</td>
          <td>0.3571</td>
          <td>0.6667</td>
          <td>0.00018</td>
          <td>0.0002101</td>
          <td>7.72e-05</td>
          <td>541</td>
          <td>948</td>
          <td>707</td>
          <td>527</td>
          <td>268</td>
          <td>6114</td>
          <td>151</td>
          <td>24</td>
          <td>6105</td>
          <td>18</td>
          <td>12</td>
          <td>2194</td>
          <td>4103</td>
          <td>17122</td>
          <td>2614</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Darla</td>
          <td>Alpha Industries</td>
          <td>Outerwear &amp; Coats</td>
          <td>999.0</td>
          <td>404.6</td>
          <td>1998.0</td>
          <td>1188.81</td>
          <td>7</td>
          <td>2</td>
          <td>2</td>
          <td>0</td>
          <td>3</td>
          <td>1998.0</td>
          <td>1188.81</td>
          <td>0.595</td>
          <td>0.5</td>
          <td>0.2857</td>
          <td>0.0</td>
          <td>0.6</td>
          <td>0.0007401</td>
          <td>0.0008496</td>
          <td>3.86e-05</td>
          <td>1</td>
          <td>16</td>
          <td>18</td>
          <td>15</td>
          <td>8625</td>
          <td>6114</td>
          <td>844</td>
          <td>17458</td>
          <td>10869</td>
          <td>14</td>
          <td>14</td>
          <td>2925</td>
          <td>4275</td>
          <td>13238</td>
          <td>17458</td>
          <td>16953</td>
        </tr>
        <tr>
          <td>Magaschoni Women&#x27;s Shimmer Jacket</td>
          <td>Magaschoni</td>
          <td>Blazers &amp; Jackets</td>
          <td>698.0</td>
          <td>258.96</td>
          <td>698.0</td>
          <td>439.04</td>
          <td>6</td>
          <td>1</td>
          <td>1</td>
          <td>2</td>
          <td>2</td>
          <td>2094.0</td>
          <td>1317.13</td>
          <td>0.629</td>
          <td>0.5</td>
          <td>0.25</td>
          <td>0.3333</td>
          <td>0.6667</td>
          <td>0.0002586</td>
          <td>0.0003138</td>
          <td>3.31e-05</td>
          <td>43</td>
          <td>58</td>
          <td>288</td>
          <td>201</td>
          <td>12532</td>
          <td>13264</td>
          <td>3978</td>
          <td>2100</td>
          <td>17069</td>
          <td>12</td>
          <td>9</td>
          <td>839</td>
          <td>4275</td>
          <td>14408</td>
          <td>2619</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Mystique</td>
          <td>Canada Goose</td>
          <td>Active</td>
          <td>750.0</td>
          <td>280.5</td>
          <td>750.0</td>
          <td>469.5</td>
          <td>9</td>
          <td>1</td>
          <td>1</td>
          <td>2</td>
          <td>5</td>
          <td>2250.0</td>
          <td>1408.5</td>
          <td>0.626</td>
          <td>0.5</td>
          <td>0.1429</td>
          <td>0.2222</td>
          <td>0.8333</td>
          <td>0.0002778</td>
          <td>0.0003355</td>
          <td>4.96e-05</td>
          <td>37</td>
          <td>53</td>
          <td>230</td>
          <td>170</td>
          <td>3355</td>
          <td>13264</td>
          <td>3978</td>
          <td>2100</td>
          <td>3026</td>
          <td>9</td>
          <td>8</td>
          <td>984</td>
          <td>4275</td>
          <td>20815</td>
          <td>7837</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>Spyder Women&#x27;s Jesst In Time Jacket</td>
          <td>Spyder</td>
          <td>Outerwear &amp; Coats</td>
          <td>650.0</td>
          <td>295.75</td>
          <td>3250.0</td>
          <td>1771.25</td>
          <td>10</td>
          <td>5</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>2600.0</td>
          <td>1417.0</td>
          <td>0.545</td>
          <td>0.4444</td>
          <td>0.5</td>
          <td>0.0</td>
          <td>0.1667</td>
          <td>0.0012039</td>
          <td>0.0012659</td>
          <td>5.52e-05</td>
          <td>52</td>
          <td>50</td>
          <td>3</td>
          <td>4</td>
          <td>1962</td>
          <td>251</td>
          <td>30</td>
          <td>17458</td>
          <td>23197</td>
          <td>7</td>
          <td>7</td>
          <td>8121</td>
          <td>8264</td>
          <td>3269</td>
          <td>17458</td>
          <td>27059</td>
        </tr>
        <tr>
          <td>Woolrich Arctic Parka DF</td>
          <td>Woolrich</td>
          <td>Outerwear &amp; Coats</td>
          <td>990.0</td>
          <td>478.17</td>
          <td>2970.0</td>
          <td>1535.49</td>
          <td>12</td>
          <td>3</td>
          <td>2</td>
          <td>1</td>
          <td>6</td>
          <td>2970.0</td>
          <td>1535.49</td>
          <td>0.517</td>
          <td>0.4</td>
          <td>0.2727</td>
          <td>0.0833</td>
          <td>0.6667</td>
          <td>0.0011002</td>
          <td>0.0010974</td>
          <td>6.62e-05</td>
          <td>3</td>
          <td>6</td>
          <td>5</td>
          <td>6</td>
          <td>694</td>
          <td>2358</td>
          <td>844</td>
          <td>7029</td>
          <td>1398</td>
          <td>4</td>
          <td>4</td>
          <td>10735</td>
          <td>8312</td>
          <td>14284</td>
          <td>17144</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>The North Face Denali Down Mens Jacket 2013</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>436.15</td>
          <td>2709.0</td>
          <td>1400.55</td>
          <td>13</td>
          <td>3</td>
          <td>2</td>
          <td>2</td>
          <td>6</td>
          <td>3612.0</td>
          <td>1867.4</td>
          <td>0.517</td>
          <td>0.4</td>
          <td>0.2727</td>
          <td>0.1538</td>
          <td>0.6667</td>
          <td>0.0010035</td>
          <td>0.001001</td>
          <td>7.17e-05</td>
          <td>5</td>
          <td>10</td>
          <td>7</td>
          <td>7</td>
          <td>423</td>
          <td>2358</td>
          <td>844</td>
          <td>2100</td>
          <td>1398</td>
          <td>2</td>
          <td>3</td>
          <td>10735</td>
          <td>8312</td>
          <td>14284</td>
          <td>12634</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>NIKE WOMEN&#x27;S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort*</td>
          <td>Nike</td>
          <td>Intimates</td>
          <td>903.0</td>
          <td>512.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>1</td>
          <td>2709.0</td>
          <td>1173.0</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.75</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.21e-05</td>
          <td>5</td>
          <td>4</td>
          <td>22532</td>
          <td>22532</td>
          <td>21053</td>
          <td>22532</td>
          <td>13463</td>
          <td>526</td>
          <td>23197</td>
          <td>5</td>
          <td>15</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>109</td>
          <td>1</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by Cancellation Rate</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
WHERE unit_orders_placed_rank &lt;= 15
ORDER BY
  cancellation_rate_rank ASC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Wrangler Men&#x27;s Rugged Wear Classic Fit Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.87</td>
          <td>22.23</td>
          <td>367.56</td>
          <td>169.24</td>
          <td>38</td>
          <td>9</td>
          <td>5</td>
          <td>9</td>
          <td>15</td>
          <td>596.43</td>
          <td>273.96</td>
          <td>0.4604</td>
          <td>0.3571</td>
          <td>0.3103</td>
          <td>0.2368</td>
          <td>0.625</td>
          <td>0.0001362</td>
          <td>0.000121</td>
          <td>0.0002096</td>
          <td>13688</td>
          <td>12514</td>
          <td>1205</td>
          <td>1552</td>
          <td>3</td>
          <td>5</td>
          <td>5</td>
          <td>1</td>
          <td>11</td>
          <td>440</td>
          <td>628</td>
          <td>16340</td>
          <td>8749</td>
          <td>13014</td>
          <td>7776</td>
          <td>16547</td>
        </tr>
        <tr>
          <td>Volcom Men&#x27;s Kinkade Jean</td>
          <td>Volcom</td>
          <td>Jeans</td>
          <td>66.67</td>
          <td>35.17</td>
          <td>269.9</td>
          <td>125.86</td>
          <td>27</td>
          <td>4</td>
          <td>3</td>
          <td>5</td>
          <td>15</td>
          <td>538.25</td>
          <td>254.63</td>
          <td>0.4663</td>
          <td>0.4286</td>
          <td>0.1818</td>
          <td>0.1852</td>
          <td>0.7895</td>
          <td>0.0001</td>
          <td>9e-05</td>
          <td>0.0001489</td>
          <td>7633</td>
          <td>6807</td>
          <td>2158</td>
          <td>2560</td>
          <td>12</td>
          <td>776</td>
          <td>151</td>
          <td>24</td>
          <td>11</td>
          <td>562</td>
          <td>723</td>
          <td>15806</td>
          <td>8270</td>
          <td>19358</td>
          <td>10467</td>
          <td>9273</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Leg Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>227.86</td>
          <td>123.14</td>
          <td>1452.0</td>
          <td>661.01</td>
          <td>28</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>15</td>
          <td>1430.0</td>
          <td>645.85</td>
          <td>0.4552</td>
          <td>0.125</td>
          <td>0.3043</td>
          <td>0.1786</td>
          <td>0.6818</td>
          <td>0.0005379</td>
          <td>0.0004724</td>
          <td>0.0001545</td>
          <td>646</td>
          <td>406</td>
          <td>45</td>
          <td>69</td>
          <td>9</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>11</td>
          <td>57</td>
          <td>95</td>
          <td>16801</td>
          <td>13444</td>
          <td>13032</td>
          <td>10715</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Hanes Men&#x27;s 4 Pack Boxer Brief</td>
          <td>Hanes</td>
          <td>Underwear</td>
          <td>25.0</td>
          <td>11.52</td>
          <td>250.0</td>
          <td>133.47</td>
          <td>28</td>
          <td>10</td>
          <td>2</td>
          <td>5</td>
          <td>11</td>
          <td>175.0</td>
          <td>92.77</td>
          <td>0.5339</td>
          <td>0.1667</td>
          <td>0.4348</td>
          <td>0.1786</td>
          <td>0.5238</td>
          <td>9.26e-05</td>
          <td>9.54e-05</td>
          <td>0.0001545</td>
          <td>19651</td>
          <td>20997</td>
          <td>2432</td>
          <td>2340</td>
          <td>9</td>
          <td>4</td>
          <td>844</td>
          <td>24</td>
          <td>43</td>
          <td>4152</td>
          <td>3935</td>
          <td>9232</td>
          <td>13196</td>
          <td>6738</td>
          <td>10715</td>
          <td>19500</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Genuine Tampa Cargo Short</td>
          <td>Wrangler</td>
          <td>Shorts</td>
          <td>31.37</td>
          <td>15.61</td>
          <td>229.94</td>
          <td>116.44</td>
          <td>29</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>16</td>
          <td>179.94</td>
          <td>90.54</td>
          <td>0.5064</td>
          <td>0.125</td>
          <td>0.2917</td>
          <td>0.1724</td>
          <td>0.6957</td>
          <td>8.52e-05</td>
          <td>8.32e-05</td>
          <td>0.00016</td>
          <td>17403</td>
          <td>17266</td>
          <td>2818</td>
          <td>2869</td>
          <td>8</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>7</td>
          <td>3935</td>
          <td>4081</td>
          <td>11924</td>
          <td>13444</td>
          <td>13236</td>
          <td>10730</td>
          <td>12964</td>
        </tr>
        <tr>
          <td>Volcom Men&#x27;s Vorta Slim Straight Leg Fit Jean</td>
          <td>Volcom</td>
          <td>Jeans</td>
          <td>73.57</td>
          <td>41.13</td>
          <td>574.85</td>
          <td>249.86</td>
          <td>27</td>
          <td>8</td>
          <td>1</td>
          <td>4</td>
          <td>14</td>
          <td>387.8</td>
          <td>166.89</td>
          <td>0.4347</td>
          <td>0.1111</td>
          <td>0.3478</td>
          <td>0.1481</td>
          <td>0.6364</td>
          <td>0.0002129</td>
          <td>0.0001786</td>
          <td>0.0001489</td>
          <td>6603</td>
          <td>5251</td>
          <td>467</td>
          <td>746</td>
          <td>12</td>
          <td>16</td>
          <td>3978</td>
          <td>126</td>
          <td>22</td>
          <td>1091</td>
          <td>1537</td>
          <td>18678</td>
          <td>13456</td>
          <td>9743</td>
          <td>12705</td>
          <td>16487</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Premium Performance Cowboy Cut Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>47.45</td>
          <td>25.88</td>
          <td>570.83</td>
          <td>264.22</td>
          <td>58</td>
          <td>12</td>
          <td>2</td>
          <td>7</td>
          <td>37</td>
          <td>417.81</td>
          <td>189.65</td>
          <td>0.4629</td>
          <td>0.1429</td>
          <td>0.2353</td>
          <td>0.1207</td>
          <td>0.7551</td>
          <td>0.0002115</td>
          <td>0.0001888</td>
          <td>0.00032</td>
          <td>12004</td>
          <td>10508</td>
          <td>470</td>
          <td>662</td>
          <td>1</td>
          <td>2</td>
          <td>844</td>
          <td>2</td>
          <td>1</td>
          <td>905</td>
          <td>1224</td>
          <td>16149</td>
          <td>13389</td>
          <td>17092</td>
          <td>15548</td>
          <td>9486</td>
        </tr>
        <tr>
          <td>7 For All Mankind Men&#x27;s Standard Classic Straight Leg Jean</td>
          <td>7 For All Mankind</td>
          <td>Jeans</td>
          <td>157.45</td>
          <td>80.97</td>
          <td>1435.0</td>
          <td>696.01</td>
          <td>42</td>
          <td>9</td>
          <td>5</td>
          <td>5</td>
          <td>23</td>
          <td>1673.0</td>
          <td>844.04</td>
          <td>0.485</td>
          <td>0.3571</td>
          <td>0.2432</td>
          <td>0.119</td>
          <td>0.7188</td>
          <td>0.0005316</td>
          <td>0.0004974</td>
          <td>0.0002317</td>
          <td>1798</td>
          <td>1488</td>
          <td>46</td>
          <td>60</td>
          <td>2</td>
          <td>5</td>
          <td>5</td>
          <td>24</td>
          <td>2</td>
          <td>32</td>
          <td>41</td>
          <td>14028</td>
          <td>8749</td>
          <td>17091</td>
          <td>15552</td>
          <td>12034</td>
        </tr>
        <tr>
          <td>Kenneth Cole REACTION Men&#x27;s Passcase Wallet</td>
          <td>Kenneth Cole REACTION</td>
          <td>Accessories</td>
          <td>18.91</td>
          <td>7.72</td>
          <td>152.71</td>
          <td>89.4</td>
          <td>34</td>
          <td>8</td>
          <td>4</td>
          <td>4</td>
          <td>18</td>
          <td>150.85</td>
          <td>90.57</td>
          <td>0.5854</td>
          <td>0.3333</td>
          <td>0.2667</td>
          <td>0.1176</td>
          <td>0.6923</td>
          <td>5.66e-05</td>
          <td>6.39e-05</td>
          <td>0.0001876</td>
          <td>23389</td>
          <td>24481</td>
          <td>4958</td>
          <td>4188</td>
          <td>4</td>
          <td>16</td>
          <td>30</td>
          <td>126</td>
          <td>4</td>
          <td>5015</td>
          <td>4078</td>
          <td>3806</td>
          <td>8752</td>
          <td>14395</td>
          <td>15553</td>
          <td>12966</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Wrancher Dress Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.4</td>
          <td>20.2</td>
          <td>242.4</td>
          <td>118.65</td>
          <td>27</td>
          <td>6</td>
          <td>2</td>
          <td>3</td>
          <td>16</td>
          <td>202.0</td>
          <td>102.05</td>
          <td>0.4895</td>
          <td>0.25</td>
          <td>0.25</td>
          <td>0.1111</td>
          <td>0.7273</td>
          <td>8.98e-05</td>
          <td>8.48e-05</td>
          <td>0.0001489</td>
          <td>13728</td>
          <td>13816</td>
          <td>2533</td>
          <td>2788</td>
          <td>12</td>
          <td>84</td>
          <td>844</td>
          <td>526</td>
          <td>7</td>
          <td>3236</td>
          <td>3382</td>
          <td>13585</td>
          <td>11344</td>
          <td>14408</td>
          <td>15570</td>
          <td>11980</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Long Pant</td>
          <td>HUGO BOSS</td>
          <td>Sleep &amp; Lounge</td>
          <td>74.72</td>
          <td>28.3</td>
          <td>1033.11</td>
          <td>648.16</td>
          <td>33</td>
          <td>14</td>
          <td>0</td>
          <td>3</td>
          <td>16</td>
          <td>233.01</td>
          <td>138.21</td>
          <td>0.6274</td>
          <td>0.0</td>
          <td>0.4667</td>
          <td>0.0909</td>
          <td>0.5333</td>
          <td>0.0003827</td>
          <td>0.0004632</td>
          <td>0.000182</td>
          <td>6501</td>
          <td>9383</td>
          <td>113</td>
          <td>75</td>
          <td>6</td>
          <td>1</td>
          <td>13463</td>
          <td>526</td>
          <td>7</td>
          <td>2702</td>
          <td>2165</td>
          <td>933</td>
          <td>13463</td>
          <td>6418</td>
          <td>16872</td>
          <td>19494</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>246.88</td>
          <td>129.05</td>
          <td>1366.0</td>
          <td>666.07</td>
          <td>34</td>
          <td>5</td>
          <td>4</td>
          <td>3</td>
          <td>22</td>
          <td>1400.0</td>
          <td>654.5</td>
          <td>0.4876</td>
          <td>0.4444</td>
          <td>0.1613</td>
          <td>0.0882</td>
          <td>0.8148</td>
          <td>0.000506</td>
          <td>0.000476</td>
          <td>0.0001876</td>
          <td>534</td>
          <td>354</td>
          <td>56</td>
          <td>65</td>
          <td>4</td>
          <td>251</td>
          <td>30</td>
          <td>526</td>
          <td>3</td>
          <td>63</td>
          <td>92</td>
          <td>13792</td>
          <td>8264</td>
          <td>20804</td>
          <td>17143</td>
          <td>7595</td>
        </tr>
        <tr>
          <td>Joe&#x27;s Jeans Men&#x27;s Slim Fit Straight Leg Brixton</td>
          <td>Joe&#x27;s Jeans</td>
          <td>Jeans</td>
          <td>194.26</td>
          <td>102.07</td>
          <td>1353.0</td>
          <td>647.44</td>
          <td>27</td>
          <td>7</td>
          <td>3</td>
          <td>2</td>
          <td>15</td>
          <td>976.0</td>
          <td>458.49</td>
          <td>0.4785</td>
          <td>0.3</td>
          <td>0.28</td>
          <td>0.0741</td>
          <td>0.6818</td>
          <td>0.0005012</td>
          <td>0.0004627</td>
          <td>0.0001489</td>
          <td>992</td>
          <td>729</td>
          <td>58</td>
          <td>76</td>
          <td>12</td>
          <td>33</td>
          <td>151</td>
          <td>2100</td>
          <td>11</td>
          <td>133</td>
          <td>207</td>
          <td>14773</td>
          <td>11276</td>
          <td>14282</td>
          <td>17370</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Dockers Men&#x27;s Suit Separate Coat</td>
          <td>Dockers</td>
          <td>Suits &amp; Sport Coats</td>
          <td>88.36</td>
          <td>33.97</td>
          <td>231.12</td>
          <td>140.98</td>
          <td>27</td>
          <td>3</td>
          <td>4</td>
          <td>2</td>
          <td>18</td>
          <td>542.11</td>
          <td>337.6</td>
          <td>0.61</td>
          <td>0.5714</td>
          <td>0.12</td>
          <td>0.0741</td>
          <td>0.8571</td>
          <td>8.56e-05</td>
          <td>0.0001008</td>
          <td>0.0001489</td>
          <td>5094</td>
          <td>7229</td>
          <td>2783</td>
          <td>2122</td>
          <td>12</td>
          <td>2358</td>
          <td>30</td>
          <td>2100</td>
          <td>4</td>
          <td>542</td>
          <td>391</td>
          <td>1873</td>
          <td>4252</td>
          <td>22129</td>
          <td>17370</td>
          <td>6057</td>
        </tr>
        <tr>
          <td>Joseph Abboud Men&#x27;s Two-button Side Vent Sport Coat</td>
          <td>Joseph Abboud</td>
          <td>Suits &amp; Sport Coats</td>
          <td>264.0</td>
          <td>101.9</td>
          <td>2904.0</td>
          <td>1759.82</td>
          <td>30</td>
          <td>11</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>1056.0</td>
          <td>656.57</td>
          <td>0.606</td>
          <td>0.1538</td>
          <td>0.3929</td>
          <td>0.0667</td>
          <td>0.5769</td>
          <td>0.0010758</td>
          <td>0.0012577</td>
          <td>0.0001655</td>
          <td>430</td>
          <td>734</td>
          <td>6</td>
          <td>5</td>
          <td>7</td>
          <td>3</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>112</td>
          <td>91</td>
          <td>2144</td>
          <td>13388</td>
          <td>9081</td>
          <td>17408</td>
          <td>18610</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by En Route Rate</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
WHERE unit_orders_placed_rank &lt;= 15
ORDER BY
  en_route_rate_rank ASC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Dockers Men&#x27;s Suit Separate Coat</td>
          <td>Dockers</td>
          <td>Suits &amp; Sport Coats</td>
          <td>88.36</td>
          <td>33.97</td>
          <td>231.12</td>
          <td>140.98</td>
          <td>27</td>
          <td>3</td>
          <td>4</td>
          <td>2</td>
          <td>18</td>
          <td>542.11</td>
          <td>337.6</td>
          <td>0.61</td>
          <td>0.5714</td>
          <td>0.12</td>
          <td>0.0741</td>
          <td>0.8571</td>
          <td>8.56e-05</td>
          <td>0.0001008</td>
          <td>0.0001489</td>
          <td>5094</td>
          <td>7229</td>
          <td>2783</td>
          <td>2122</td>
          <td>12</td>
          <td>2358</td>
          <td>30</td>
          <td>2100</td>
          <td>4</td>
          <td>542</td>
          <td>391</td>
          <td>1873</td>
          <td>4252</td>
          <td>22129</td>
          <td>17370</td>
          <td>6057</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>246.88</td>
          <td>129.05</td>
          <td>1366.0</td>
          <td>666.07</td>
          <td>34</td>
          <td>5</td>
          <td>4</td>
          <td>3</td>
          <td>22</td>
          <td>1400.0</td>
          <td>654.5</td>
          <td>0.4876</td>
          <td>0.4444</td>
          <td>0.1613</td>
          <td>0.0882</td>
          <td>0.8148</td>
          <td>0.000506</td>
          <td>0.000476</td>
          <td>0.0001876</td>
          <td>534</td>
          <td>354</td>
          <td>56</td>
          <td>65</td>
          <td>4</td>
          <td>251</td>
          <td>30</td>
          <td>526</td>
          <td>3</td>
          <td>63</td>
          <td>92</td>
          <td>13792</td>
          <td>8264</td>
          <td>20804</td>
          <td>17143</td>
          <td>7595</td>
        </tr>
        <tr>
          <td>Volcom Men&#x27;s Kinkade Jean</td>
          <td>Volcom</td>
          <td>Jeans</td>
          <td>66.67</td>
          <td>35.17</td>
          <td>269.9</td>
          <td>125.86</td>
          <td>27</td>
          <td>4</td>
          <td>3</td>
          <td>5</td>
          <td>15</td>
          <td>538.25</td>
          <td>254.63</td>
          <td>0.4663</td>
          <td>0.4286</td>
          <td>0.1818</td>
          <td>0.1852</td>
          <td>0.7895</td>
          <td>0.0001</td>
          <td>9e-05</td>
          <td>0.0001489</td>
          <td>7633</td>
          <td>6807</td>
          <td>2158</td>
          <td>2560</td>
          <td>12</td>
          <td>776</td>
          <td>151</td>
          <td>24</td>
          <td>11</td>
          <td>562</td>
          <td>723</td>
          <td>15806</td>
          <td>8270</td>
          <td>19358</td>
          <td>10467</td>
          <td>9273</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Premium Performance Cowboy Cut Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>47.45</td>
          <td>25.88</td>
          <td>570.83</td>
          <td>264.22</td>
          <td>58</td>
          <td>12</td>
          <td>2</td>
          <td>7</td>
          <td>37</td>
          <td>417.81</td>
          <td>189.65</td>
          <td>0.4629</td>
          <td>0.1429</td>
          <td>0.2353</td>
          <td>0.1207</td>
          <td>0.7551</td>
          <td>0.0002115</td>
          <td>0.0001888</td>
          <td>0.00032</td>
          <td>12004</td>
          <td>10508</td>
          <td>470</td>
          <td>662</td>
          <td>1</td>
          <td>2</td>
          <td>844</td>
          <td>2</td>
          <td>1</td>
          <td>905</td>
          <td>1224</td>
          <td>16149</td>
          <td>13389</td>
          <td>17092</td>
          <td>15548</td>
          <td>9486</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Wrancher Dress Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.4</td>
          <td>20.2</td>
          <td>242.4</td>
          <td>118.65</td>
          <td>27</td>
          <td>6</td>
          <td>2</td>
          <td>3</td>
          <td>16</td>
          <td>202.0</td>
          <td>102.05</td>
          <td>0.4895</td>
          <td>0.25</td>
          <td>0.25</td>
          <td>0.1111</td>
          <td>0.7273</td>
          <td>8.98e-05</td>
          <td>8.48e-05</td>
          <td>0.0001489</td>
          <td>13728</td>
          <td>13816</td>
          <td>2533</td>
          <td>2788</td>
          <td>12</td>
          <td>84</td>
          <td>844</td>
          <td>526</td>
          <td>7</td>
          <td>3236</td>
          <td>3382</td>
          <td>13585</td>
          <td>11344</td>
          <td>14408</td>
          <td>15570</td>
          <td>11980</td>
        </tr>
        <tr>
          <td>7 For All Mankind Men&#x27;s Standard Classic Straight Leg Jean</td>
          <td>7 For All Mankind</td>
          <td>Jeans</td>
          <td>157.45</td>
          <td>80.97</td>
          <td>1435.0</td>
          <td>696.01</td>
          <td>42</td>
          <td>9</td>
          <td>5</td>
          <td>5</td>
          <td>23</td>
          <td>1673.0</td>
          <td>844.04</td>
          <td>0.485</td>
          <td>0.3571</td>
          <td>0.2432</td>
          <td>0.119</td>
          <td>0.7188</td>
          <td>0.0005316</td>
          <td>0.0004974</td>
          <td>0.0002317</td>
          <td>1798</td>
          <td>1488</td>
          <td>46</td>
          <td>60</td>
          <td>2</td>
          <td>5</td>
          <td>5</td>
          <td>24</td>
          <td>2</td>
          <td>32</td>
          <td>41</td>
          <td>14028</td>
          <td>8749</td>
          <td>17091</td>
          <td>15552</td>
          <td>12034</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Genuine Tampa Cargo Short</td>
          <td>Wrangler</td>
          <td>Shorts</td>
          <td>31.37</td>
          <td>15.61</td>
          <td>229.94</td>
          <td>116.44</td>
          <td>29</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>16</td>
          <td>179.94</td>
          <td>90.54</td>
          <td>0.5064</td>
          <td>0.125</td>
          <td>0.2917</td>
          <td>0.1724</td>
          <td>0.6957</td>
          <td>8.52e-05</td>
          <td>8.32e-05</td>
          <td>0.00016</td>
          <td>17403</td>
          <td>17266</td>
          <td>2818</td>
          <td>2869</td>
          <td>8</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>7</td>
          <td>3935</td>
          <td>4081</td>
          <td>11924</td>
          <td>13444</td>
          <td>13236</td>
          <td>10730</td>
          <td>12964</td>
        </tr>
        <tr>
          <td>Chaps Big and Tall Solid V-Neck Vest</td>
          <td>Chaps</td>
          <td>Sweaters</td>
          <td>39.88</td>
          <td>20.32</td>
          <td>279.16</td>
          <td>134.91</td>
          <td>28</td>
          <td>7</td>
          <td>4</td>
          <td>1</td>
          <td>16</td>
          <td>199.4</td>
          <td>99.06</td>
          <td>0.4833</td>
          <td>0.3636</td>
          <td>0.2593</td>
          <td>0.0357</td>
          <td>0.6957</td>
          <td>0.0001034</td>
          <td>9.64e-05</td>
          <td>0.0001545</td>
          <td>14437</td>
          <td>13747</td>
          <td>2029</td>
          <td>2288</td>
          <td>9</td>
          <td>33</td>
          <td>30</td>
          <td>7029</td>
          <td>7</td>
          <td>3354</td>
          <td>3543</td>
          <td>14237</td>
          <td>8748</td>
          <td>14407</td>
          <td>17457</td>
          <td>12964</td>
        </tr>
        <tr>
          <td>Kenneth Cole REACTION Men&#x27;s Passcase Wallet</td>
          <td>Kenneth Cole REACTION</td>
          <td>Accessories</td>
          <td>18.91</td>
          <td>7.72</td>
          <td>152.71</td>
          <td>89.4</td>
          <td>34</td>
          <td>8</td>
          <td>4</td>
          <td>4</td>
          <td>18</td>
          <td>150.85</td>
          <td>90.57</td>
          <td>0.5854</td>
          <td>0.3333</td>
          <td>0.2667</td>
          <td>0.1176</td>
          <td>0.6923</td>
          <td>5.66e-05</td>
          <td>6.39e-05</td>
          <td>0.0001876</td>
          <td>23389</td>
          <td>24481</td>
          <td>4958</td>
          <td>4188</td>
          <td>4</td>
          <td>16</td>
          <td>30</td>
          <td>126</td>
          <td>4</td>
          <td>5015</td>
          <td>4078</td>
          <td>3806</td>
          <td>8752</td>
          <td>14395</td>
          <td>15553</td>
          <td>12966</td>
        </tr>
        <tr>
          <td>Joe&#x27;s Jeans Men&#x27;s Slim Fit Straight Leg Brixton</td>
          <td>Joe&#x27;s Jeans</td>
          <td>Jeans</td>
          <td>194.26</td>
          <td>102.07</td>
          <td>1353.0</td>
          <td>647.44</td>
          <td>27</td>
          <td>7</td>
          <td>3</td>
          <td>2</td>
          <td>15</td>
          <td>976.0</td>
          <td>458.49</td>
          <td>0.4785</td>
          <td>0.3</td>
          <td>0.28</td>
          <td>0.0741</td>
          <td>0.6818</td>
          <td>0.0005012</td>
          <td>0.0004627</td>
          <td>0.0001489</td>
          <td>992</td>
          <td>729</td>
          <td>58</td>
          <td>76</td>
          <td>12</td>
          <td>33</td>
          <td>151</td>
          <td>2100</td>
          <td>11</td>
          <td>133</td>
          <td>207</td>
          <td>14773</td>
          <td>11276</td>
          <td>14282</td>
          <td>17370</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Leg Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>227.86</td>
          <td>123.14</td>
          <td>1452.0</td>
          <td>661.01</td>
          <td>28</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>15</td>
          <td>1430.0</td>
          <td>645.85</td>
          <td>0.4552</td>
          <td>0.125</td>
          <td>0.3043</td>
          <td>0.1786</td>
          <td>0.6818</td>
          <td>0.0005379</td>
          <td>0.0004724</td>
          <td>0.0001545</td>
          <td>646</td>
          <td>406</td>
          <td>45</td>
          <td>69</td>
          <td>9</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>11</td>
          <td>57</td>
          <td>95</td>
          <td>16801</td>
          <td>13444</td>
          <td>13032</td>
          <td>10715</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Volcom Men&#x27;s Vorta Slim Straight Leg Fit Jean</td>
          <td>Volcom</td>
          <td>Jeans</td>
          <td>73.57</td>
          <td>41.13</td>
          <td>574.85</td>
          <td>249.86</td>
          <td>27</td>
          <td>8</td>
          <td>1</td>
          <td>4</td>
          <td>14</td>
          <td>387.8</td>
          <td>166.89</td>
          <td>0.4347</td>
          <td>0.1111</td>
          <td>0.3478</td>
          <td>0.1481</td>
          <td>0.6364</td>
          <td>0.0002129</td>
          <td>0.0001786</td>
          <td>0.0001489</td>
          <td>6603</td>
          <td>5251</td>
          <td>467</td>
          <td>746</td>
          <td>12</td>
          <td>16</td>
          <td>3978</td>
          <td>126</td>
          <td>22</td>
          <td>1091</td>
          <td>1537</td>
          <td>18678</td>
          <td>13456</td>
          <td>9743</td>
          <td>12705</td>
          <td>16487</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Rugged Wear Classic Fit Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.87</td>
          <td>22.23</td>
          <td>367.56</td>
          <td>169.24</td>
          <td>38</td>
          <td>9</td>
          <td>5</td>
          <td>9</td>
          <td>15</td>
          <td>596.43</td>
          <td>273.96</td>
          <td>0.4604</td>
          <td>0.3571</td>
          <td>0.3103</td>
          <td>0.2368</td>
          <td>0.625</td>
          <td>0.0001362</td>
          <td>0.000121</td>
          <td>0.0002096</td>
          <td>13688</td>
          <td>12514</td>
          <td>1205</td>
          <td>1552</td>
          <td>3</td>
          <td>5</td>
          <td>5</td>
          <td>1</td>
          <td>11</td>
          <td>440</td>
          <td>628</td>
          <td>16340</td>
          <td>8749</td>
          <td>13014</td>
          <td>7776</td>
          <td>16547</td>
        </tr>
        <tr>
          <td>Joseph Abboud Men&#x27;s Two-button Side Vent Sport Coat</td>
          <td>Joseph Abboud</td>
          <td>Suits &amp; Sport Coats</td>
          <td>264.0</td>
          <td>101.9</td>
          <td>2904.0</td>
          <td>1759.82</td>
          <td>30</td>
          <td>11</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>1056.0</td>
          <td>656.57</td>
          <td>0.606</td>
          <td>0.1538</td>
          <td>0.3929</td>
          <td>0.0667</td>
          <td>0.5769</td>
          <td>0.0010758</td>
          <td>0.0012577</td>
          <td>0.0001655</td>
          <td>430</td>
          <td>734</td>
          <td>6</td>
          <td>5</td>
          <td>7</td>
          <td>3</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>112</td>
          <td>91</td>
          <td>2144</td>
          <td>13388</td>
          <td>9081</td>
          <td>17408</td>
          <td>18610</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Long Pant</td>
          <td>HUGO BOSS</td>
          <td>Sleep &amp; Lounge</td>
          <td>74.72</td>
          <td>28.3</td>
          <td>1033.11</td>
          <td>648.16</td>
          <td>33</td>
          <td>14</td>
          <td>0</td>
          <td>3</td>
          <td>16</td>
          <td>233.01</td>
          <td>138.21</td>
          <td>0.6274</td>
          <td>0.0</td>
          <td>0.4667</td>
          <td>0.0909</td>
          <td>0.5333</td>
          <td>0.0003827</td>
          <td>0.0004632</td>
          <td>0.000182</td>
          <td>6501</td>
          <td>9383</td>
          <td>113</td>
          <td>75</td>
          <td>6</td>
          <td>1</td>
          <td>13463</td>
          <td>526</td>
          <td>7</td>
          <td>2702</td>
          <td>2165</td>
          <td>933</td>
          <td>13463</td>
          <td>6418</td>
          <td>16872</td>
          <td>19494</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by Units Completed</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
  units_completed_rank ASC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>HUGO BOSS Men&#x27;s Long Pant</td>
          <td>HUGO BOSS</td>
          <td>Sleep &amp; Lounge</td>
          <td>74.72</td>
          <td>28.3</td>
          <td>1033.11</td>
          <td>648.16</td>
          <td>33</td>
          <td>14</td>
          <td>0</td>
          <td>3</td>
          <td>16</td>
          <td>233.01</td>
          <td>138.21</td>
          <td>0.6274</td>
          <td>0.0</td>
          <td>0.4667</td>
          <td>0.0909</td>
          <td>0.5333</td>
          <td>0.0003827</td>
          <td>0.0004632</td>
          <td>0.000182</td>
          <td>6501</td>
          <td>9383</td>
          <td>113</td>
          <td>75</td>
          <td>6</td>
          <td>1</td>
          <td>13463</td>
          <td>526</td>
          <td>7</td>
          <td>2702</td>
          <td>2165</td>
          <td>933</td>
          <td>13463</td>
          <td>6418</td>
          <td>16872</td>
          <td>19494</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Premium Performance Cowboy Cut Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>47.45</td>
          <td>25.88</td>
          <td>570.83</td>
          <td>264.22</td>
          <td>58</td>
          <td>12</td>
          <td>2</td>
          <td>7</td>
          <td>37</td>
          <td>417.81</td>
          <td>189.65</td>
          <td>0.4629</td>
          <td>0.1429</td>
          <td>0.2353</td>
          <td>0.1207</td>
          <td>0.7551</td>
          <td>0.0002115</td>
          <td>0.0001888</td>
          <td>0.00032</td>
          <td>12004</td>
          <td>10508</td>
          <td>470</td>
          <td>662</td>
          <td>1</td>
          <td>2</td>
          <td>844</td>
          <td>2</td>
          <td>1</td>
          <td>905</td>
          <td>1224</td>
          <td>16149</td>
          <td>13389</td>
          <td>17092</td>
          <td>15548</td>
          <td>9486</td>
        </tr>
        <tr>
          <td>Joseph Abboud Men&#x27;s Two-button Side Vent Sport Coat</td>
          <td>Joseph Abboud</td>
          <td>Suits &amp; Sport Coats</td>
          <td>264.0</td>
          <td>101.9</td>
          <td>2904.0</td>
          <td>1759.82</td>
          <td>30</td>
          <td>11</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>1056.0</td>
          <td>656.57</td>
          <td>0.606</td>
          <td>0.1538</td>
          <td>0.3929</td>
          <td>0.0667</td>
          <td>0.5769</td>
          <td>0.0010758</td>
          <td>0.0012577</td>
          <td>0.0001655</td>
          <td>430</td>
          <td>734</td>
          <td>6</td>
          <td>5</td>
          <td>7</td>
          <td>3</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>112</td>
          <td>91</td>
          <td>2144</td>
          <td>13388</td>
          <td>9081</td>
          <td>17408</td>
          <td>18610</td>
        </tr>
        <tr>
          <td>Hanes Men&#x27;s 4 Pack Boxer Brief</td>
          <td>Hanes</td>
          <td>Underwear</td>
          <td>25.0</td>
          <td>11.52</td>
          <td>250.0</td>
          <td>133.47</td>
          <td>28</td>
          <td>10</td>
          <td>2</td>
          <td>5</td>
          <td>11</td>
          <td>175.0</td>
          <td>92.77</td>
          <td>0.5339</td>
          <td>0.1667</td>
          <td>0.4348</td>
          <td>0.1786</td>
          <td>0.5238</td>
          <td>9.26e-05</td>
          <td>9.54e-05</td>
          <td>0.0001545</td>
          <td>19651</td>
          <td>20997</td>
          <td>2432</td>
          <td>2340</td>
          <td>9</td>
          <td>4</td>
          <td>844</td>
          <td>24</td>
          <td>43</td>
          <td>4152</td>
          <td>3935</td>
          <td>9232</td>
          <td>13196</td>
          <td>6738</td>
          <td>10715</td>
          <td>19500</td>
        </tr>
        <tr>
          <td>Michael Kors Men&#x27;s Marlow Wool-Blend Single-Breasted Fitted Top Coat</td>
          <td>Michael Kors</td>
          <td>Outerwear &amp; Coats</td>
          <td>255.0</td>
          <td>102.26</td>
          <td>2295.0</td>
          <td>1374.7</td>
          <td>15</td>
          <td>9</td>
          <td>1</td>
          <td>2</td>
          <td>3</td>
          <td>765.0</td>
          <td>458.23</td>
          <td>0.599</td>
          <td>0.1</td>
          <td>0.6923</td>
          <td>0.1333</td>
          <td>0.25</td>
          <td>0.0008502</td>
          <td>0.0009825</td>
          <td>8.27e-05</td>
          <td>469</td>
          <td>728</td>
          <td>13</td>
          <td>8</td>
          <td>187</td>
          <td>5</td>
          <td>3978</td>
          <td>2100</td>
          <td>10869</td>
          <td>252</td>
          <td>208</td>
          <td>2612</td>
          <td>13461</td>
          <td>1184</td>
          <td>14317</td>
          <td>26348</td>
        </tr>
        <tr>
          <td>Joe&#x27;s Jeans Men&#x27;s Rebel Relaxed Fit Jean</td>
          <td>Joe&#x27;s Jeans</td>
          <td>Jeans</td>
          <td>139.29</td>
          <td>76.13</td>
          <td>1296.69</td>
          <td>583.03</td>
          <td>26</td>
          <td>9</td>
          <td>0</td>
          <td>3</td>
          <td>14</td>
          <td>339.69</td>
          <td>166.11</td>
          <td>0.4496</td>
          <td>0.0</td>
          <td>0.3913</td>
          <td>0.1154</td>
          <td>0.6087</td>
          <td>0.0004803</td>
          <td>0.0004167</td>
          <td>0.0001434</td>
          <td>2334</td>
          <td>1721</td>
          <td>68</td>
          <td>102</td>
          <td>17</td>
          <td>5</td>
          <td>13463</td>
          <td>526</td>
          <td>22</td>
          <td>1403</td>
          <td>1558</td>
          <td>17357</td>
          <td>13463</td>
          <td>9082</td>
          <td>15567</td>
          <td>16952</td>
        </tr>
        <tr>
          <td>7 For All Mankind Men&#x27;s Standard Classic Straight Leg Jean</td>
          <td>7 For All Mankind</td>
          <td>Jeans</td>
          <td>157.45</td>
          <td>80.97</td>
          <td>1435.0</td>
          <td>696.01</td>
          <td>42</td>
          <td>9</td>
          <td>5</td>
          <td>5</td>
          <td>23</td>
          <td>1673.0</td>
          <td>844.04</td>
          <td>0.485</td>
          <td>0.3571</td>
          <td>0.2432</td>
          <td>0.119</td>
          <td>0.7188</td>
          <td>0.0005316</td>
          <td>0.0004974</td>
          <td>0.0002317</td>
          <td>1798</td>
          <td>1488</td>
          <td>46</td>
          <td>60</td>
          <td>2</td>
          <td>5</td>
          <td>5</td>
          <td>24</td>
          <td>2</td>
          <td>32</td>
          <td>41</td>
          <td>14028</td>
          <td>8749</td>
          <td>17091</td>
          <td>15552</td>
          <td>12034</td>
        </tr>
        <tr>
          <td>3-Piece Matching Set Laura High Quality Strapless Bra Thong &amp; Bikini #SL101084 Made in Colombia</td>
          <td>Laura</td>
          <td>Intimates</td>
          <td>41.95</td>
          <td>20.45</td>
          <td>377.55</td>
          <td>193.56</td>
          <td>13</td>
          <td>9</td>
          <td>0</td>
          <td>2</td>
          <td>2</td>
          <td>83.9</td>
          <td>42.79</td>
          <td>0.5127</td>
          <td>0.0</td>
          <td>0.8182</td>
          <td>0.1538</td>
          <td>0.1818</td>
          <td>0.0001399</td>
          <td>0.0001383</td>
          <td>7.17e-05</td>
          <td>13574</td>
          <td>13665</td>
          <td>1157</td>
          <td>1202</td>
          <td>423</td>
          <td>5</td>
          <td>13463</td>
          <td>2100</td>
          <td>17069</td>
          <td>9768</td>
          <td>9702</td>
          <td>11272</td>
          <td>13463</td>
          <td>606</td>
          <td>12634</td>
          <td>27058</td>
        </tr>
        <tr>
          <td>State O Maine Big and Tall Fashion Flannel Pajama</td>
          <td>KNOTHE CORP.</td>
          <td>Sleep &amp; Lounge</td>
          <td>36.88</td>
          <td>15.59</td>
          <td>331.92</td>
          <td>192.51</td>
          <td>21</td>
          <td>9</td>
          <td>5</td>
          <td>1</td>
          <td>6</td>
          <td>221.28</td>
          <td>127.31</td>
          <td>0.58</td>
          <td>0.3571</td>
          <td>0.45</td>
          <td>0.0476</td>
          <td>0.4</td>
          <td>0.000123</td>
          <td>0.0001376</td>
          <td>0.0001158</td>
          <td>15350</td>
          <td>17283</td>
          <td>1492</td>
          <td>1214</td>
          <td>50</td>
          <td>5</td>
          <td>5</td>
          <td>7029</td>
          <td>1398</td>
          <td>2854</td>
          <td>2454</td>
          <td>4293</td>
          <td>8749</td>
          <td>6490</td>
          <td>17453</td>
          <td>23875</td>
        </tr>
        <tr>
          <td>JiMarti JM01 Sunglasses for Golf Fishing Cycling-Unbreakable-... Frame</td>
          <td>JiMarti</td>
          <td>Accessories</td>
          <td>29.95</td>
          <td>11.92</td>
          <td>269.55</td>
          <td>161.1</td>
          <td>22</td>
          <td>9</td>
          <td>2</td>
          <td>2</td>
          <td>9</td>
          <td>119.8</td>
          <td>72.12</td>
          <td>0.5977</td>
          <td>0.1818</td>
          <td>0.45</td>
          <td>0.0909</td>
          <td>0.5</td>
          <td>9.99e-05</td>
          <td>0.0001151</td>
          <td>0.0001214</td>
          <td>18166</td>
          <td>20613</td>
          <td>2175</td>
          <td>1707</td>
          <td>43</td>
          <td>5</td>
          <td>844</td>
          <td>2100</td>
          <td>140</td>
          <td>6868</td>
          <td>5540</td>
          <td>2758</td>
          <td>13193</td>
          <td>6490</td>
          <td>16872</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>PAIGE Women&#x27;s Skyline Skinny Jean</td>
          <td>PAIGE</td>
          <td>Jeans</td>
          <td>158.0</td>
          <td>90.19</td>
          <td>1422.0</td>
          <td>608.93</td>
          <td>19</td>
          <td>9</td>
          <td>0</td>
          <td>2</td>
          <td>8</td>
          <td>316.0</td>
          <td>135.88</td>
          <td>0.4282</td>
          <td>0.0</td>
          <td>0.5294</td>
          <td>0.1053</td>
          <td>0.4706</td>
          <td>0.0005268</td>
          <td>0.0004352</td>
          <td>0.0001048</td>
          <td>1714</td>
          <td>1108</td>
          <td>48</td>
          <td>90</td>
          <td>72</td>
          <td>5</td>
          <td>13463</td>
          <td>2100</td>
          <td>295</td>
          <td>1575</td>
          <td>2230</td>
          <td>19172</td>
          <td>13463</td>
          <td>3268</td>
          <td>16363</td>
          <td>23444</td>
        </tr>
        <tr>
          <td>Motherhood Maternity: Sports Clip Down Nursing Bra</td>
          <td>Motherhood Maternity</td>
          <td>Maternity</td>
          <td>22.54</td>
          <td>10.46</td>
          <td>200.82</td>
          <td>108.99</td>
          <td>25</td>
          <td>9</td>
          <td>2</td>
          <td>3</td>
          <td>11</td>
          <td>112.9</td>
          <td>60.37</td>
          <td>0.5427</td>
          <td>0.1818</td>
          <td>0.4091</td>
          <td>0.12</td>
          <td>0.55</td>
          <td>7.44e-05</td>
          <td>7.79e-05</td>
          <td>0.0001379</td>
          <td>21822</td>
          <td>22052</td>
          <td>3297</td>
          <td>3165</td>
          <td>21</td>
          <td>5</td>
          <td>844</td>
          <td>526</td>
          <td>43</td>
          <td>7249</td>
          <td>6811</td>
          <td>8373</td>
          <td>13193</td>
          <td>7481</td>
          <td>15549</td>
          <td>19449</td>
        </tr>
        <tr>
          <td>Belly Bandit post pregnancy tummy wrap belly band original Nude</td>
          <td>Belly Bandit</td>
          <td>Maternity</td>
          <td>54.95</td>
          <td>23.79</td>
          <td>489.55</td>
          <td>279.96</td>
          <td>20</td>
          <td>9</td>
          <td>1</td>
          <td>2</td>
          <td>8</td>
          <td>169.85</td>
          <td>97.62</td>
          <td>0.5719</td>
          <td>0.1</td>
          <td>0.5</td>
          <td>0.1</td>
          <td>0.4706</td>
          <td>0.0001813</td>
          <td>0.0002001</td>
          <td>0.0001103</td>
          <td>9960</td>
          <td>11605</td>
          <td>701</td>
          <td>588</td>
          <td>59</td>
          <td>5</td>
          <td>3978</td>
          <td>2100</td>
          <td>295</td>
          <td>4325</td>
          <td>3628</td>
          <td>5219</td>
          <td>13461</td>
          <td>3269</td>
          <td>16366</td>
          <td>23444</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Rugged Wear Classic Fit Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.87</td>
          <td>22.23</td>
          <td>367.56</td>
          <td>169.24</td>
          <td>38</td>
          <td>9</td>
          <td>5</td>
          <td>9</td>
          <td>15</td>
          <td>596.43</td>
          <td>273.96</td>
          <td>0.4604</td>
          <td>0.3571</td>
          <td>0.3103</td>
          <td>0.2368</td>
          <td>0.625</td>
          <td>0.0001362</td>
          <td>0.000121</td>
          <td>0.0002096</td>
          <td>13688</td>
          <td>12514</td>
          <td>1205</td>
          <td>1552</td>
          <td>3</td>
          <td>5</td>
          <td>5</td>
          <td>1</td>
          <td>11</td>
          <td>440</td>
          <td>628</td>
          <td>16340</td>
          <td>8749</td>
          <td>13014</td>
          <td>7776</td>
          <td>16547</td>
        </tr>
        <tr>
          <td>Ray-Ban Unisex RB4105 Folding Wayfarer Sunglasses</td>
          <td>Ray-Ban</td>
          <td>Accessories</td>
          <td>99.65</td>
          <td>36.84</td>
          <td>896.85</td>
          <td>562.92</td>
          <td>18</td>
          <td>9</td>
          <td>2</td>
          <td>3</td>
          <td>4</td>
          <td>498.25</td>
          <td>313.8</td>
          <td>0.6277</td>
          <td>0.1818</td>
          <td>0.6</td>
          <td>0.1667</td>
          <td>0.3077</td>
          <td>0.0003322</td>
          <td>0.0004023</td>
          <td>9.93e-05</td>
          <td>4069</td>
          <td>6340</td>
          <td>161</td>
          <td>113</td>
          <td>87</td>
          <td>5</td>
          <td>844</td>
          <td>526</td>
          <td>6105</td>
          <td>666</td>
          <td>476</td>
          <td>932</td>
          <td>13193</td>
          <td>2189</td>
          <td>10731</td>
          <td>26246</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by Units Returned</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Kenneth Cole Men&#x27;s Straight Leg Jean</td>
          <td>Kenneth Cole</td>
          <td>Jeans</td>
          <td>54.25</td>
          <td>27.11</td>
          <td>54.99</td>
          <td>26.89</td>
          <td>24</td>
          <td>1</td>
          <td>7</td>
          <td>4</td>
          <td>12</td>
          <td>632.25</td>
          <td>318.8</td>
          <td>0.489</td>
          <td>0.875</td>
          <td>0.05</td>
          <td>0.1667</td>
          <td>0.9231</td>
          <td>2.04e-05</td>
          <td>1.92e-05</td>
          <td>0.0001324</td>
          <td>10100</td>
          <td>9920</td>
          <td>13356</td>
          <td>13628</td>
          <td>30</td>
          <td>13264</td>
          <td>1</td>
          <td>126</td>
          <td>37</td>
          <td>380</td>
          <td>462</td>
          <td>13602</td>
          <td>2795</td>
          <td>22531</td>
          <td>10731</td>
          <td>5642</td>
        </tr>
        <tr>
          <td>Alex Stevens Men&#x27;s Chevron Cuff Cardigan</td>
          <td>Alex Stevens</td>
          <td>Sweaters</td>
          <td>26.0</td>
          <td>11.78</td>
          <td>26.0</td>
          <td>14.22</td>
          <td>14</td>
          <td>1</td>
          <td>7</td>
          <td>0</td>
          <td>6</td>
          <td>182.0</td>
          <td>99.55</td>
          <td>0.5469</td>
          <td>0.875</td>
          <td>0.0714</td>
          <td>0.0</td>
          <td>0.8571</td>
          <td>9.6e-06</td>
          <td>1.02e-05</td>
          <td>7.72e-05</td>
          <td>19363</td>
          <td>20777</td>
          <td>18768</td>
          <td>18407</td>
          <td>268</td>
          <td>13264</td>
          <td>1</td>
          <td>17458</td>
          <td>1398</td>
          <td>3788</td>
          <td>3516</td>
          <td>7983</td>
          <td>2795</td>
          <td>22525</td>
          <td>17458</td>
          <td>6057</td>
        </tr>
        <tr>
          <td>Womenâ€™s UA Baseâ„¢ 4.0 Leggings Bottoms by Under Armour</td>
          <td>Under Armour</td>
          <td>Active</td>
          <td>63.99</td>
          <td>23.93</td>
          <td>127.98</td>
          <td>80.12</td>
          <td>12</td>
          <td>2</td>
          <td>6</td>
          <td>2</td>
          <td>2</td>
          <td>511.92</td>
          <td>320.46</td>
          <td>0.626</td>
          <td>0.75</td>
          <td>0.2</td>
          <td>0.1667</td>
          <td>0.5</td>
          <td>4.74e-05</td>
          <td>5.73e-05</td>
          <td>6.62e-05</td>
          <td>8152</td>
          <td>11520</td>
          <td>6273</td>
          <td>4860</td>
          <td>694</td>
          <td>6114</td>
          <td>3</td>
          <td>2100</td>
          <td>17069</td>
          <td>616</td>
          <td>453</td>
          <td>984</td>
          <td>2834</td>
          <td>17510</td>
          <td>10731</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>G by GUESS Cosmos Slit-Front Top</td>
          <td>G by GUESS</td>
          <td>Tops &amp; Tees</td>
          <td>29.5</td>
          <td>16.87</td>
          <td>88.5</td>
          <td>37.88</td>
          <td>13</td>
          <td>3</td>
          <td>6</td>
          <td>1</td>
          <td>3</td>
          <td>206.5</td>
          <td>88.38</td>
          <td>0.428</td>
          <td>0.6667</td>
          <td>0.25</td>
          <td>0.0769</td>
          <td>0.5</td>
          <td>3.28e-05</td>
          <td>2.71e-05</td>
          <td>7.17e-05</td>
          <td>18349</td>
          <td>16195</td>
          <td>9301</td>
          <td>10674</td>
          <td>423</td>
          <td>2358</td>
          <td>3</td>
          <td>7029</td>
          <td>10869</td>
          <td>3172</td>
          <td>4221</td>
          <td>19180</td>
          <td>3055</td>
          <td>14408</td>
          <td>17286</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>G-Star Men&#x27;s Attacc Straight Vintage Jean</td>
          <td>G-Star</td>
          <td>Jeans</td>
          <td>210.0</td>
          <td>102.9</td>
          <td>210.0</td>
          <td>107.1</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>0</td>
          <td>1</td>
          <td>1050.0</td>
          <td>535.5</td>
          <td>0.51</td>
          <td>0.8333</td>
          <td>0.1429</td>
          <td>0.0</td>
          <td>0.5</td>
          <td>7.78e-05</td>
          <td>7.65e-05</td>
          <td>3.86e-05</td>
          <td>737</td>
          <td>713</td>
          <td>3106</td>
          <td>3251</td>
          <td>8625</td>
          <td>13264</td>
          <td>5</td>
          <td>17458</td>
          <td>23197</td>
          <td>113</td>
          <td>132</td>
          <td>11510</td>
          <td>2797</td>
          <td>20815</td>
          <td>17458</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>Quiksilver Waterman Men&#x27;s Cabo 3 Walkshort</td>
          <td>Quiksilver</td>
          <td>Shorts</td>
          <td>35.98</td>
          <td>18.39</td>
          <td>35.98</td>
          <td>17.59</td>
          <td>10</td>
          <td>1</td>
          <td>5</td>
          <td>1</td>
          <td>3</td>
          <td>215.88</td>
          <td>105.57</td>
          <td>0.4889</td>
          <td>0.8333</td>
          <td>0.1111</td>
          <td>0.1</td>
          <td>0.75</td>
          <td>1.33e-05</td>
          <td>1.26e-05</td>
          <td>5.52e-05</td>
          <td>15686</td>
          <td>15023</td>
          <td>16878</td>
          <td>17002</td>
          <td>1962</td>
          <td>13264</td>
          <td>5</td>
          <td>7029</td>
          <td>10869</td>
          <td>2994</td>
          <td>3212</td>
          <td>13683</td>
          <td>2797</td>
          <td>22130</td>
          <td>16366</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>Icebreaker Men&#x27;s Kodiak Zip Jacket</td>
          <td>Icebreaker</td>
          <td>Outerwear &amp; Coats</td>
          <td>250.0</td>
          <td>122.5</td>
          <td>250.0</td>
          <td>127.5</td>
          <td>13</td>
          <td>1</td>
          <td>5</td>
          <td>1</td>
          <td>6</td>
          <td>1500.0</td>
          <td>765.0</td>
          <td>0.51</td>
          <td>0.8333</td>
          <td>0.0833</td>
          <td>0.0769</td>
          <td>0.8571</td>
          <td>9.26e-05</td>
          <td>9.11e-05</td>
          <td>7.17e-05</td>
          <td>480</td>
          <td>413</td>
          <td>2432</td>
          <td>2507</td>
          <td>423</td>
          <td>13264</td>
          <td>5</td>
          <td>7029</td>
          <td>1398</td>
          <td>43</td>
          <td>60</td>
          <td>11510</td>
          <td>2797</td>
          <td>22497</td>
          <td>17286</td>
          <td>6057</td>
        </tr>
        <tr>
          <td>Levi&#x27;s Women&#x27;s Demi Curve Slim Fit Jean</td>
          <td>Levi&#x27;s</td>
          <td>Jeans</td>
          <td>44.99</td>
          <td>25.36</td>
          <td>359.92</td>
          <td>158.59</td>
          <td>22</td>
          <td>8</td>
          <td>5</td>
          <td>3</td>
          <td>6</td>
          <td>359.92</td>
          <td>157.29</td>
          <td>0.4406</td>
          <td>0.3846</td>
          <td>0.4211</td>
          <td>0.1364</td>
          <td>0.4286</td>
          <td>0.0001333</td>
          <td>0.0001133</td>
          <td>0.0001214</td>
          <td>12553</td>
          <td>10773</td>
          <td>1272</td>
          <td>1757</td>
          <td>43</td>
          <td>16</td>
          <td>5</td>
          <td>526</td>
          <td>1398</td>
          <td>1228</td>
          <td>1730</td>
          <td>18170</td>
          <td>8724</td>
          <td>7452</td>
          <td>14315</td>
          <td>23541</td>
        </tr>
        <tr>
          <td>Ames Walker Style 166 Men&#x27;s Microfiber Firm Support Travel Socks 15-20 - Available in Various Sizes and Colors</td>
          <td>Ames</td>
          <td>Socks</td>
          <td>12.99</td>
          <td>8.07</td>
          <td>12.99</td>
          <td>4.92</td>
          <td>11</td>
          <td>1</td>
          <td>5</td>
          <td>2</td>
          <td>3</td>
          <td>90.93</td>
          <td>34.46</td>
          <td>0.3788</td>
          <td>0.8333</td>
          <td>0.1111</td>
          <td>0.1818</td>
          <td>0.75</td>
          <td>4.8e-06</td>
          <td>3.5e-06</td>
          <td>6.07e-05</td>
          <td>25756</td>
          <td>24123</td>
          <td>21580</td>
          <td>22067</td>
          <td>1161</td>
          <td>13264</td>
          <td>5</td>
          <td>2100</td>
          <td>10869</td>
          <td>8965</td>
          <td>11517</td>
          <td>21711</td>
          <td>2797</td>
          <td>22130</td>
          <td>10468</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>Under Armour Igniter Pro Sport Sunglasses</td>
          <td>Under Armour</td>
          <td>Accessories</td>
          <td>94.99</td>
          <td>41.47</td>
          <td>284.97</td>
          <td>162.72</td>
          <td>17</td>
          <td>3</td>
          <td>5</td>
          <td>3</td>
          <td>6</td>
          <td>759.92</td>
          <td>424.04</td>
          <td>0.571</td>
          <td>0.625</td>
          <td>0.2143</td>
          <td>0.1765</td>
          <td>0.6667</td>
          <td>0.0001056</td>
          <td>0.0001163</td>
          <td>9.38e-05</td>
          <td>4573</td>
          <td>5187</td>
          <td>1952</td>
          <td>1668</td>
          <td>103</td>
          <td>2358</td>
          <td>5</td>
          <td>526</td>
          <td>1398</td>
          <td>255</td>
          <td>249</td>
          <td>5261</td>
          <td>4099</td>
          <td>17490</td>
          <td>10717</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Men&#x27;s Superior 150s Single Breasted Two Button Black Pinstripe Dress Suit European Cut</td>
          <td>Giorgio Cerruti</td>
          <td>Suits &amp; Sport Coats</td>
          <td>69.95</td>
          <td>27.98</td>
          <td>209.85</td>
          <td>125.91</td>
          <td>16</td>
          <td>3</td>
          <td>5</td>
          <td>0</td>
          <td>8</td>
          <td>349.75</td>
          <td>209.85</td>
          <td>0.6</td>
          <td>0.625</td>
          <td>0.1875</td>
          <td>0.0</td>
          <td>0.7273</td>
          <td>7.77e-05</td>
          <td>9e-05</td>
          <td>8.83e-05</td>
          <td>6978</td>
          <td>9517</td>
          <td>3144</td>
          <td>2557</td>
          <td>150</td>
          <td>2358</td>
          <td>5</td>
          <td>17458</td>
          <td>295</td>
          <td>1333</td>
          <td>1043</td>
          <td>2533</td>
          <td>4099</td>
          <td>19354</td>
          <td>17458</td>
          <td>11980</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Rugged Wear Classic Fit Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.87</td>
          <td>22.23</td>
          <td>367.56</td>
          <td>169.24</td>
          <td>38</td>
          <td>9</td>
          <td>5</td>
          <td>9</td>
          <td>15</td>
          <td>596.43</td>
          <td>273.96</td>
          <td>0.4604</td>
          <td>0.3571</td>
          <td>0.3103</td>
          <td>0.2368</td>
          <td>0.625</td>
          <td>0.0001362</td>
          <td>0.000121</td>
          <td>0.0002096</td>
          <td>13688</td>
          <td>12514</td>
          <td>1205</td>
          <td>1552</td>
          <td>3</td>
          <td>5</td>
          <td>5</td>
          <td>1</td>
          <td>11</td>
          <td>440</td>
          <td>628</td>
          <td>16340</td>
          <td>8749</td>
          <td>13014</td>
          <td>7776</td>
          <td>16547</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Original Cowboy Cut Relaxed Fit Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>42.99</td>
          <td>22.67</td>
          <td>228.46</td>
          <td>108.63</td>
          <td>25</td>
          <td>5</td>
          <td>5</td>
          <td>7</td>
          <td>8</td>
          <td>493.18</td>
          <td>228.73</td>
          <td>0.4755</td>
          <td>0.5</td>
          <td>0.2778</td>
          <td>0.28</td>
          <td>0.6154</td>
          <td>8.46e-05</td>
          <td>7.76e-05</td>
          <td>0.0001379</td>
          <td>13180</td>
          <td>12269</td>
          <td>2826</td>
          <td>3184</td>
          <td>21</td>
          <td>251</td>
          <td>5</td>
          <td>2</td>
          <td>295</td>
          <td>687</td>
          <td>895</td>
          <td>15040</td>
          <td>4275</td>
          <td>14283</td>
          <td>5404</td>
          <td>16940</td>
        </tr>
        <tr>
          <td>Robert Graham Men&#x27;s Cheshire</td>
          <td>Robert Graham</td>
          <td>Tops &amp; Tees</td>
          <td>179.99</td>
          <td>92.69</td>
          <td>179.99</td>
          <td>87.3</td>
          <td>11</td>
          <td>1</td>
          <td>5</td>
          <td>1</td>
          <td>4</td>
          <td>1079.94</td>
          <td>523.77</td>
          <td>0.485</td>
          <td>0.8333</td>
          <td>0.1</td>
          <td>0.0909</td>
          <td>0.8</td>
          <td>6.67e-05</td>
          <td>6.24e-05</td>
          <td>6.07e-05</td>
          <td>1179</td>
          <td>1014</td>
          <td>3947</td>
          <td>4329</td>
          <td>1161</td>
          <td>13264</td>
          <td>5</td>
          <td>7029</td>
          <td>6105</td>
          <td>110</td>
          <td>145</td>
          <td>14028</td>
          <td>2797</td>
          <td>22369</td>
          <td>16872</td>
          <td>7598</td>
        </tr>
        <tr>
          <td>Tolani Women&#x27;s Daphne Top</td>
          <td>Tolani</td>
          <td>Tops &amp; Tees</td>
          <td>194.0</td>
          <td>104.95</td>
          <td>388.0</td>
          <td>178.09</td>
          <td>12</td>
          <td>2</td>
          <td>5</td>
          <td>1</td>
          <td>4</td>
          <td>1164.0</td>
          <td>534.28</td>
          <td>0.459</td>
          <td>0.7143</td>
          <td>0.1818</td>
          <td>0.0833</td>
          <td>0.6667</td>
          <td>0.0001437</td>
          <td>0.0001273</td>
          <td>6.62e-05</td>
          <td>993</td>
          <td>654</td>
          <td>1103</td>
          <td>1402</td>
          <td>694</td>
          <td>6114</td>
          <td>5</td>
          <td>7029</td>
          <td>6105</td>
          <td>103</td>
          <td>134</td>
          <td>16449</td>
          <td>3052</td>
          <td>19358</td>
          <td>17144</td>
          <td>12990</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by Units Cancelled</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
  units_cancelled_rank ASC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Wrangler Men&#x27;s Rugged Wear Classic Fit Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.87</td>
          <td>22.23</td>
          <td>367.56</td>
          <td>169.24</td>
          <td>38</td>
          <td>9</td>
          <td>5</td>
          <td>9</td>
          <td>15</td>
          <td>596.43</td>
          <td>273.96</td>
          <td>0.4604</td>
          <td>0.3571</td>
          <td>0.3103</td>
          <td>0.2368</td>
          <td>0.625</td>
          <td>0.0001362</td>
          <td>0.000121</td>
          <td>0.0002096</td>
          <td>13688</td>
          <td>12514</td>
          <td>1205</td>
          <td>1552</td>
          <td>3</td>
          <td>5</td>
          <td>5</td>
          <td>1</td>
          <td>11</td>
          <td>440</td>
          <td>628</td>
          <td>16340</td>
          <td>8749</td>
          <td>13014</td>
          <td>7776</td>
          <td>16547</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Original Cowboy Cut Relaxed Fit Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>42.99</td>
          <td>22.67</td>
          <td>228.46</td>
          <td>108.63</td>
          <td>25</td>
          <td>5</td>
          <td>5</td>
          <td>7</td>
          <td>8</td>
          <td>493.18</td>
          <td>228.73</td>
          <td>0.4755</td>
          <td>0.5</td>
          <td>0.2778</td>
          <td>0.28</td>
          <td>0.6154</td>
          <td>8.46e-05</td>
          <td>7.76e-05</td>
          <td>0.0001379</td>
          <td>13180</td>
          <td>12269</td>
          <td>2826</td>
          <td>3184</td>
          <td>21</td>
          <td>251</td>
          <td>5</td>
          <td>2</td>
          <td>295</td>
          <td>687</td>
          <td>895</td>
          <td>15040</td>
          <td>4275</td>
          <td>14283</td>
          <td>5404</td>
          <td>16940</td>
        </tr>
        <tr>
          <td>ExOfficio Men&#x27;s Insect Shield Ziwa Convertible Pant</td>
          <td>ExOfficio</td>
          <td>Pants</td>
          <td>99.0</td>
          <td>43.86</td>
          <td>198.0</td>
          <td>110.29</td>
          <td>13</td>
          <td>2</td>
          <td>1</td>
          <td>7</td>
          <td>3</td>
          <td>792.0</td>
          <td>441.14</td>
          <td>0.557</td>
          <td>0.3333</td>
          <td>0.3333</td>
          <td>0.5385</td>
          <td>0.6</td>
          <td>7.33e-05</td>
          <td>7.88e-05</td>
          <td>7.17e-05</td>
          <td>4113</td>
          <td>4766</td>
          <td>3453</td>
          <td>3105</td>
          <td>423</td>
          <td>6114</td>
          <td>3978</td>
          <td>2</td>
          <td>10869</td>
          <td>234</td>
          <td>228</td>
          <td>6818</td>
          <td>8752</td>
          <td>9747</td>
          <td>476</td>
          <td>16953</td>
        </tr>
        <tr>
          <td>VH Apparel - Kissables Shea Butter Infused Double Layer Socks - One Size</td>
          <td>VH Apparel - Kissables</td>
          <td>Socks &amp; Hosiery</td>
          <td>11.49</td>
          <td>4.12</td>
          <td>22.98</td>
          <td>14.73</td>
          <td>12</td>
          <td>2</td>
          <td>0</td>
          <td>7</td>
          <td>3</td>
          <td>80.43</td>
          <td>51.56</td>
          <td>0.641</td>
          <td>0.0</td>
          <td>0.4</td>
          <td>0.5833</td>
          <td>0.6</td>
          <td>8.5e-06</td>
          <td>1.05e-05</td>
          <td>6.62e-05</td>
          <td>26551</td>
          <td>27584</td>
          <td>19789</td>
          <td>18178</td>
          <td>694</td>
          <td>6114</td>
          <td>13463</td>
          <td>2</td>
          <td>10869</td>
          <td>9911</td>
          <td>8134</td>
          <td>403</td>
          <td>13463</td>
          <td>7482</td>
          <td>426</td>
          <td>16953</td>
        </tr>
        <tr>
          <td>WeSC Men&#x27;s Eddy Chino Pant</td>
          <td>WESC</td>
          <td>Pants</td>
          <td>73.62</td>
          <td>33.02</td>
          <td>300.95</td>
          <td>165.16</td>
          <td>25</td>
          <td>4</td>
          <td>2</td>
          <td>7</td>
          <td>12</td>
          <td>657.75</td>
          <td>363.33</td>
          <td>0.5488</td>
          <td>0.3333</td>
          <td>0.2222</td>
          <td>0.28</td>
          <td>0.75</td>
          <td>0.0001115</td>
          <td>0.000118</td>
          <td>0.0001379</td>
          <td>6601</td>
          <td>7527</td>
          <td>1711</td>
          <td>1625</td>
          <td>21</td>
          <td>776</td>
          <td>844</td>
          <td>2</td>
          <td>37</td>
          <td>350</td>
          <td>333</td>
          <td>7797</td>
          <td>8752</td>
          <td>17122</td>
          <td>5404</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Premium Performance Cowboy Cut Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>47.45</td>
          <td>25.88</td>
          <td>570.83</td>
          <td>264.22</td>
          <td>58</td>
          <td>12</td>
          <td>2</td>
          <td>7</td>
          <td>37</td>
          <td>417.81</td>
          <td>189.65</td>
          <td>0.4629</td>
          <td>0.1429</td>
          <td>0.2353</td>
          <td>0.1207</td>
          <td>0.7551</td>
          <td>0.0002115</td>
          <td>0.0001888</td>
          <td>0.00032</td>
          <td>12004</td>
          <td>10508</td>
          <td>470</td>
          <td>662</td>
          <td>1</td>
          <td>2</td>
          <td>844</td>
          <td>2</td>
          <td>1</td>
          <td>905</td>
          <td>1224</td>
          <td>16149</td>
          <td>13389</td>
          <td>17092</td>
          <td>15548</td>
          <td>9486</td>
        </tr>
        <tr>
          <td>7 For All Mankind Women&#x27;s The Slim Cigarette Jean</td>
          <td>7 For All Mankind</td>
          <td>Jeans</td>
          <td>157.64</td>
          <td>84.21</td>
          <td>495.99</td>
          <td>230.84</td>
          <td>17</td>
          <td>3</td>
          <td>0</td>
          <td>7</td>
          <td>7</td>
          <td>993.96</td>
          <td>464.0</td>
          <td>0.4654</td>
          <td>0.0</td>
          <td>0.3</td>
          <td>0.4118</td>
          <td>0.7</td>
          <td>0.0001837</td>
          <td>0.000165</td>
          <td>9.38e-05</td>
          <td>1785</td>
          <td>1344</td>
          <td>678</td>
          <td>856</td>
          <td>103</td>
          <td>2358</td>
          <td>13463</td>
          <td>2</td>
          <td>623</td>
          <td>129</td>
          <td>200</td>
          <td>15893</td>
          <td>13463</td>
          <td>13033</td>
          <td>1688</td>
          <td>12849</td>
        </tr>
        <tr>
          <td>Savane Men&#x27;s Flat Front No-Iron Twill Pant</td>
          <td>Savane</td>
          <td>Pants</td>
          <td>41.19</td>
          <td>18.35</td>
          <td>121.97</td>
          <td>68.51</td>
          <td>20</td>
          <td>3</td>
          <td>3</td>
          <td>6</td>
          <td>8</td>
          <td>369.91</td>
          <td>205.55</td>
          <td>0.5617</td>
          <td>0.5</td>
          <td>0.2143</td>
          <td>0.3</td>
          <td>0.7273</td>
          <td>4.52e-05</td>
          <td>4.9e-05</td>
          <td>0.0001103</td>
          <td>13643</td>
          <td>15060</td>
          <td>6515</td>
          <td>5898</td>
          <td>59</td>
          <td>2358</td>
          <td>151</td>
          <td>8</td>
          <td>295</td>
          <td>1179</td>
          <td>1080</td>
          <td>6368</td>
          <td>4275</td>
          <td>17490</td>
          <td>4443</td>
          <td>11980</td>
        </tr>
        <tr>
          <td>Ed Garments Men&#x27;s Three-Ply Pleated Dress Pant. 2680</td>
          <td>Ed Garments</td>
          <td>Pants</td>
          <td>76.99</td>
          <td>31.72</td>
          <td>230.97</td>
          <td>135.81</td>
          <td>10</td>
          <td>3</td>
          <td>0</td>
          <td>6</td>
          <td>1</td>
          <td>461.94</td>
          <td>271.62</td>
          <td>0.588</td>
          <td>0.0</td>
          <td>0.75</td>
          <td>0.6</td>
          <td>0.25</td>
          <td>8.56e-05</td>
          <td>9.71e-05</td>
          <td>5.52e-05</td>
          <td>6231</td>
          <td>7981</td>
          <td>2785</td>
          <td>2261</td>
          <td>1962</td>
          <td>2358</td>
          <td>13463</td>
          <td>8</td>
          <td>23197</td>
          <td>780</td>
          <td>639</td>
          <td>3542</td>
          <td>13463</td>
          <td>746</td>
          <td>331</td>
          <td>26348</td>
        </tr>
        <tr>
          <td>Underworks Men&#x27;s Padded Rear Boxer Brief for Butt Lift</td>
          <td>Underworks</td>
          <td>Underwear</td>
          <td>29.99</td>
          <td>15.08</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>9</td>
          <td>0</td>
          <td>0</td>
          <td>6</td>
          <td>3</td>
          <td>179.94</td>
          <td>89.43</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>4.96e-05</td>
          <td>17719</td>
          <td>17696</td>
          <td>22532</td>
          <td>22532</td>
          <td>3355</td>
          <td>22532</td>
          <td>13463</td>
          <td>8</td>
          <td>10869</td>
          <td>3935</td>
          <td>4144</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>154</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Volcom Men&#x27;s Vapato Chino Pant</td>
          <td>Volcom</td>
          <td>Pants</td>
          <td>131.63</td>
          <td>62.16</td>
          <td>997.65</td>
          <td>526.94</td>
          <td>19</td>
          <td>7</td>
          <td>2</td>
          <td>6</td>
          <td>4</td>
          <td>881.6</td>
          <td>464.52</td>
          <td>0.5282</td>
          <td>0.2222</td>
          <td>0.5385</td>
          <td>0.3158</td>
          <td>0.3636</td>
          <td>0.0003696</td>
          <td>0.0003766</td>
          <td>0.0001048</td>
          <td>2563</td>
          <td>2619</td>
          <td>121</td>
          <td>128</td>
          <td>72</td>
          <td>33</td>
          <td>844</td>
          <td>8</td>
          <td>6105</td>
          <td>175</td>
          <td>199</td>
          <td>9720</td>
          <td>12628</td>
          <td>3262</td>
          <td>4416</td>
          <td>24848</td>
        </tr>
        <tr>
          <td>Tommy Hilfiger Mens Cambridge Passcase</td>
          <td>Tommy Hilfiger</td>
          <td>Accessories</td>
          <td>23.28</td>
          <td>10.2</td>
          <td>69.84</td>
          <td>39.25</td>
          <td>14</td>
          <td>3</td>
          <td>0</td>
          <td>6</td>
          <td>5</td>
          <td>139.68</td>
          <td>78.5</td>
          <td>0.562</td>
          <td>0.0</td>
          <td>0.375</td>
          <td>0.4286</td>
          <td>0.625</td>
          <td>2.59e-05</td>
          <td>2.81e-05</td>
          <td>7.72e-05</td>
          <td>21572</td>
          <td>22289</td>
          <td>11414</td>
          <td>10366</td>
          <td>268</td>
          <td>2358</td>
          <td>13463</td>
          <td>8</td>
          <td>3026</td>
          <td>5698</td>
          <td>5005</td>
          <td>6272</td>
          <td>13463</td>
          <td>9107</td>
          <td>1436</td>
          <td>16547</td>
        </tr>
        <tr>
          <td>Commando Sweaters GI Style Acrylic Command Sweater</td>
          <td>ANS</td>
          <td>Sweaters</td>
          <td>36.5</td>
          <td>19.56</td>
          <td>109.5</td>
          <td>50.81</td>
          <td>14</td>
          <td>3</td>
          <td>1</td>
          <td>6</td>
          <td>4</td>
          <td>255.5</td>
          <td>118.55</td>
          <td>0.464</td>
          <td>0.25</td>
          <td>0.375</td>
          <td>0.4286</td>
          <td>0.5714</td>
          <td>4.06e-05</td>
          <td>3.63e-05</td>
          <td>7.72e-05</td>
          <td>15396</td>
          <td>14224</td>
          <td>7458</td>
          <td>8189</td>
          <td>268</td>
          <td>2358</td>
          <td>3978</td>
          <td>8</td>
          <td>6105</td>
          <td>2306</td>
          <td>2714</td>
          <td>16011</td>
          <td>11344</td>
          <td>9107</td>
          <td>1436</td>
          <td>18611</td>
        </tr>
        <tr>
          <td>Columbia Men&#x27;s Tall Cathedral Peak Vest</td>
          <td>Columbia</td>
          <td>Outerwear &amp; Coats</td>
          <td>34.95</td>
          <td>14.4</td>
          <td>34.95</td>
          <td>20.55</td>
          <td>12</td>
          <td>1</td>
          <td>1</td>
          <td>6</td>
          <td>4</td>
          <td>244.65</td>
          <td>143.85</td>
          <td>0.588</td>
          <td>0.5</td>
          <td>0.1667</td>
          <td>0.5</td>
          <td>0.8</td>
          <td>1.29e-05</td>
          <td>1.47e-05</td>
          <td>6.62e-05</td>
          <td>16246</td>
          <td>18275</td>
          <td>17146</td>
          <td>15812</td>
          <td>694</td>
          <td>13264</td>
          <td>3978</td>
          <td>8</td>
          <td>6105</td>
          <td>2447</td>
          <td>2014</td>
          <td>3542</td>
          <td>4275</td>
          <td>19436</td>
          <td>477</td>
          <td>7598</td>
        </tr>
        <tr>
          <td>3 PAIR -30 BELOW THERMAL WINTER SOCKS (MERINO WOOL)</td>
          <td>J.B. Icelandic (Extreme Cold Activity)</td>
          <td>Socks</td>
          <td>33.0</td>
          <td>19.77</td>
          <td>33.0</td>
          <td>13.23</td>
          <td>10</td>
          <td>1</td>
          <td>0</td>
          <td>6</td>
          <td>3</td>
          <td>198.0</td>
          <td>79.4</td>
          <td>0.4009</td>
          <td>0.0</td>
          <td>0.25</td>
          <td>0.6</td>
          <td>0.75</td>
          <td>1.22e-05</td>
          <td>9.5e-06</td>
          <td>5.52e-05</td>
          <td>16766</td>
          <td>14097</td>
          <td>17399</td>
          <td>18866</td>
          <td>1962</td>
          <td>13264</td>
          <td>13463</td>
          <td>8</td>
          <td>10869</td>
          <td>3376</td>
          <td>4926</td>
          <td>20898</td>
          <td>13463</td>
          <td>14408</td>
          <td>331</td>
          <td>9487</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by Units En Route</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
  units_en_route_rank ASC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Wrangler Men&#x27;s Premium Performance Cowboy Cut Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>47.45</td>
          <td>25.88</td>
          <td>570.83</td>
          <td>264.22</td>
          <td>58</td>
          <td>12</td>
          <td>2</td>
          <td>7</td>
          <td>37</td>
          <td>417.81</td>
          <td>189.65</td>
          <td>0.4629</td>
          <td>0.1429</td>
          <td>0.2353</td>
          <td>0.1207</td>
          <td>0.7551</td>
          <td>0.0002115</td>
          <td>0.0001888</td>
          <td>0.00032</td>
          <td>12004</td>
          <td>10508</td>
          <td>470</td>
          <td>662</td>
          <td>1</td>
          <td>2</td>
          <td>844</td>
          <td>2</td>
          <td>1</td>
          <td>905</td>
          <td>1224</td>
          <td>16149</td>
          <td>13389</td>
          <td>17092</td>
          <td>15548</td>
          <td>9486</td>
        </tr>
        <tr>
          <td>7 For All Mankind Men&#x27;s Standard Classic Straight Leg Jean</td>
          <td>7 For All Mankind</td>
          <td>Jeans</td>
          <td>157.45</td>
          <td>80.97</td>
          <td>1435.0</td>
          <td>696.01</td>
          <td>42</td>
          <td>9</td>
          <td>5</td>
          <td>5</td>
          <td>23</td>
          <td>1673.0</td>
          <td>844.04</td>
          <td>0.485</td>
          <td>0.3571</td>
          <td>0.2432</td>
          <td>0.119</td>
          <td>0.7188</td>
          <td>0.0005316</td>
          <td>0.0004974</td>
          <td>0.0002317</td>
          <td>1798</td>
          <td>1488</td>
          <td>46</td>
          <td>60</td>
          <td>2</td>
          <td>5</td>
          <td>5</td>
          <td>24</td>
          <td>2</td>
          <td>32</td>
          <td>41</td>
          <td>14028</td>
          <td>8749</td>
          <td>17091</td>
          <td>15552</td>
          <td>12034</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>246.88</td>
          <td>129.05</td>
          <td>1366.0</td>
          <td>666.07</td>
          <td>34</td>
          <td>5</td>
          <td>4</td>
          <td>3</td>
          <td>22</td>
          <td>1400.0</td>
          <td>654.5</td>
          <td>0.4876</td>
          <td>0.4444</td>
          <td>0.1613</td>
          <td>0.0882</td>
          <td>0.8148</td>
          <td>0.000506</td>
          <td>0.000476</td>
          <td>0.0001876</td>
          <td>534</td>
          <td>354</td>
          <td>56</td>
          <td>65</td>
          <td>4</td>
          <td>251</td>
          <td>30</td>
          <td>526</td>
          <td>3</td>
          <td>63</td>
          <td>92</td>
          <td>13792</td>
          <td>8264</td>
          <td>20804</td>
          <td>17143</td>
          <td>7595</td>
        </tr>
        <tr>
          <td>Kenneth Cole REACTION Men&#x27;s Passcase Wallet</td>
          <td>Kenneth Cole REACTION</td>
          <td>Accessories</td>
          <td>18.91</td>
          <td>7.72</td>
          <td>152.71</td>
          <td>89.4</td>
          <td>34</td>
          <td>8</td>
          <td>4</td>
          <td>4</td>
          <td>18</td>
          <td>150.85</td>
          <td>90.57</td>
          <td>0.5854</td>
          <td>0.3333</td>
          <td>0.2667</td>
          <td>0.1176</td>
          <td>0.6923</td>
          <td>5.66e-05</td>
          <td>6.39e-05</td>
          <td>0.0001876</td>
          <td>23389</td>
          <td>24481</td>
          <td>4958</td>
          <td>4188</td>
          <td>4</td>
          <td>16</td>
          <td>30</td>
          <td>126</td>
          <td>4</td>
          <td>5015</td>
          <td>4078</td>
          <td>3806</td>
          <td>8752</td>
          <td>14395</td>
          <td>15553</td>
          <td>12966</td>
        </tr>
        <tr>
          <td>Dockers Men&#x27;s Suit Separate Coat</td>
          <td>Dockers</td>
          <td>Suits &amp; Sport Coats</td>
          <td>88.36</td>
          <td>33.97</td>
          <td>231.12</td>
          <td>140.98</td>
          <td>27</td>
          <td>3</td>
          <td>4</td>
          <td>2</td>
          <td>18</td>
          <td>542.11</td>
          <td>337.6</td>
          <td>0.61</td>
          <td>0.5714</td>
          <td>0.12</td>
          <td>0.0741</td>
          <td>0.8571</td>
          <td>8.56e-05</td>
          <td>0.0001008</td>
          <td>0.0001489</td>
          <td>5094</td>
          <td>7229</td>
          <td>2783</td>
          <td>2122</td>
          <td>12</td>
          <td>2358</td>
          <td>30</td>
          <td>2100</td>
          <td>4</td>
          <td>542</td>
          <td>391</td>
          <td>1873</td>
          <td>4252</td>
          <td>22129</td>
          <td>17370</td>
          <td>6057</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s 20X No. 33 Relaxed Straight Leg Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>55.0</td>
          <td>29.66</td>
          <td>220.0</td>
          <td>100.87</td>
          <td>24</td>
          <td>4</td>
          <td>1</td>
          <td>2</td>
          <td>17</td>
          <td>165.0</td>
          <td>74.2</td>
          <td>0.4585</td>
          <td>0.2</td>
          <td>0.1818</td>
          <td>0.0833</td>
          <td>0.8095</td>
          <td>8.15e-05</td>
          <td>7.21e-05</td>
          <td>0.0001324</td>
          <td>9673</td>
          <td>8784</td>
          <td>2941</td>
          <td>3526</td>
          <td>30</td>
          <td>776</td>
          <td>3978</td>
          <td>2100</td>
          <td>6</td>
          <td>4449</td>
          <td>5375</td>
          <td>16533</td>
          <td>12637</td>
          <td>19358</td>
          <td>17144</td>
          <td>7597</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Genuine Tampa Cargo Short</td>
          <td>Wrangler</td>
          <td>Shorts</td>
          <td>31.37</td>
          <td>15.61</td>
          <td>229.94</td>
          <td>116.44</td>
          <td>29</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>16</td>
          <td>179.94</td>
          <td>90.54</td>
          <td>0.5064</td>
          <td>0.125</td>
          <td>0.2917</td>
          <td>0.1724</td>
          <td>0.6957</td>
          <td>8.52e-05</td>
          <td>8.32e-05</td>
          <td>0.00016</td>
          <td>17403</td>
          <td>17266</td>
          <td>2818</td>
          <td>2869</td>
          <td>8</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>7</td>
          <td>3935</td>
          <td>4081</td>
          <td>11924</td>
          <td>13444</td>
          <td>13236</td>
          <td>10730</td>
          <td>12964</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Long Pant</td>
          <td>HUGO BOSS</td>
          <td>Sleep &amp; Lounge</td>
          <td>74.72</td>
          <td>28.3</td>
          <td>1033.11</td>
          <td>648.16</td>
          <td>33</td>
          <td>14</td>
          <td>0</td>
          <td>3</td>
          <td>16</td>
          <td>233.01</td>
          <td>138.21</td>
          <td>0.6274</td>
          <td>0.0</td>
          <td>0.4667</td>
          <td>0.0909</td>
          <td>0.5333</td>
          <td>0.0003827</td>
          <td>0.0004632</td>
          <td>0.000182</td>
          <td>6501</td>
          <td>9383</td>
          <td>113</td>
          <td>75</td>
          <td>6</td>
          <td>1</td>
          <td>13463</td>
          <td>526</td>
          <td>7</td>
          <td>2702</td>
          <td>2165</td>
          <td>933</td>
          <td>13463</td>
          <td>6418</td>
          <td>16872</td>
          <td>19494</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Wrancher Dress Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.4</td>
          <td>20.2</td>
          <td>242.4</td>
          <td>118.65</td>
          <td>27</td>
          <td>6</td>
          <td>2</td>
          <td>3</td>
          <td>16</td>
          <td>202.0</td>
          <td>102.05</td>
          <td>0.4895</td>
          <td>0.25</td>
          <td>0.25</td>
          <td>0.1111</td>
          <td>0.7273</td>
          <td>8.98e-05</td>
          <td>8.48e-05</td>
          <td>0.0001489</td>
          <td>13728</td>
          <td>13816</td>
          <td>2533</td>
          <td>2788</td>
          <td>12</td>
          <td>84</td>
          <td>844</td>
          <td>526</td>
          <td>7</td>
          <td>3236</td>
          <td>3382</td>
          <td>13585</td>
          <td>11344</td>
          <td>14408</td>
          <td>15570</td>
          <td>11980</td>
        </tr>
        <tr>
          <td>Chaps Big and Tall Solid V-Neck Vest</td>
          <td>Chaps</td>
          <td>Sweaters</td>
          <td>39.88</td>
          <td>20.32</td>
          <td>279.16</td>
          <td>134.91</td>
          <td>28</td>
          <td>7</td>
          <td>4</td>
          <td>1</td>
          <td>16</td>
          <td>199.4</td>
          <td>99.06</td>
          <td>0.4833</td>
          <td>0.3636</td>
          <td>0.2593</td>
          <td>0.0357</td>
          <td>0.6957</td>
          <td>0.0001034</td>
          <td>9.64e-05</td>
          <td>0.0001545</td>
          <td>14437</td>
          <td>13747</td>
          <td>2029</td>
          <td>2288</td>
          <td>9</td>
          <td>33</td>
          <td>30</td>
          <td>7029</td>
          <td>7</td>
          <td>3354</td>
          <td>3543</td>
          <td>14237</td>
          <td>8748</td>
          <td>14407</td>
          <td>17457</td>
          <td>12964</td>
        </tr>
        <tr>
          <td>TapouT Men&#x27;s Lock Up Hoodie</td>
          <td>TapouT</td>
          <td>Fashion Hoodies &amp; Sweatshirts</td>
          <td>36.61</td>
          <td>20.6</td>
          <td>229.12</td>
          <td>103.62</td>
          <td>23</td>
          <td>7</td>
          <td>0</td>
          <td>1</td>
          <td>15</td>
          <td>39.6</td>
          <td>16.16</td>
          <td>0.4523</td>
          <td>0.0</td>
          <td>0.3182</td>
          <td>0.0435</td>
          <td>0.6818</td>
          <td>8.49e-05</td>
          <td>7.41e-05</td>
          <td>0.0001269</td>
          <td>15388</td>
          <td>13556</td>
          <td>2822</td>
          <td>3414</td>
          <td>41</td>
          <td>33</td>
          <td>13463</td>
          <td>7029</td>
          <td>11</td>
          <td>16416</td>
          <td>17785</td>
          <td>17057</td>
          <td>13463</td>
          <td>13008</td>
          <td>17454</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Sarasota Agility Short</td>
          <td>Wrangler</td>
          <td>Shorts</td>
          <td>33.03</td>
          <td>16.36</td>
          <td>198.95</td>
          <td>101.37</td>
          <td>25</td>
          <td>6</td>
          <td>1</td>
          <td>3</td>
          <td>15</td>
          <td>138.97</td>
          <td>68.68</td>
          <td>0.5095</td>
          <td>0.1429</td>
          <td>0.2727</td>
          <td>0.12</td>
          <td>0.7143</td>
          <td>7.37e-05</td>
          <td>7.24e-05</td>
          <td>0.0001379</td>
          <td>16765</td>
          <td>16618</td>
          <td>3447</td>
          <td>3505</td>
          <td>21</td>
          <td>84</td>
          <td>3978</td>
          <td>526</td>
          <td>11</td>
          <td>5758</td>
          <td>5901</td>
          <td>11606</td>
          <td>13389</td>
          <td>14284</td>
          <td>15549</td>
          <td>12035</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Leg Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>227.86</td>
          <td>123.14</td>
          <td>1452.0</td>
          <td>661.01</td>
          <td>28</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>15</td>
          <td>1430.0</td>
          <td>645.85</td>
          <td>0.4552</td>
          <td>0.125</td>
          <td>0.3043</td>
          <td>0.1786</td>
          <td>0.6818</td>
          <td>0.0005379</td>
          <td>0.0004724</td>
          <td>0.0001545</td>
          <td>646</td>
          <td>406</td>
          <td>45</td>
          <td>69</td>
          <td>9</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>11</td>
          <td>57</td>
          <td>95</td>
          <td>16801</td>
          <td>13444</td>
          <td>13032</td>
          <td>10715</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Volcom Men&#x27;s Kinkade Jean</td>
          <td>Volcom</td>
          <td>Jeans</td>
          <td>66.67</td>
          <td>35.17</td>
          <td>269.9</td>
          <td>125.86</td>
          <td>27</td>
          <td>4</td>
          <td>3</td>
          <td>5</td>
          <td>15</td>
          <td>538.25</td>
          <td>254.63</td>
          <td>0.4663</td>
          <td>0.4286</td>
          <td>0.1818</td>
          <td>0.1852</td>
          <td>0.7895</td>
          <td>0.0001</td>
          <td>9e-05</td>
          <td>0.0001489</td>
          <td>7633</td>
          <td>6807</td>
          <td>2158</td>
          <td>2560</td>
          <td>12</td>
          <td>776</td>
          <td>151</td>
          <td>24</td>
          <td>11</td>
          <td>562</td>
          <td>723</td>
          <td>15806</td>
          <td>8270</td>
          <td>19358</td>
          <td>10467</td>
          <td>9273</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Rugged Wear Classic Fit Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.87</td>
          <td>22.23</td>
          <td>367.56</td>
          <td>169.24</td>
          <td>38</td>
          <td>9</td>
          <td>5</td>
          <td>9</td>
          <td>15</td>
          <td>596.43</td>
          <td>273.96</td>
          <td>0.4604</td>
          <td>0.3571</td>
          <td>0.3103</td>
          <td>0.2368</td>
          <td>0.625</td>
          <td>0.0001362</td>
          <td>0.000121</td>
          <td>0.0002096</td>
          <td>13688</td>
          <td>12514</td>
          <td>1205</td>
          <td>1552</td>
          <td>3</td>
          <td>5</td>
          <td>5</td>
          <td>1</td>
          <td>11</td>
          <td>440</td>
          <td>628</td>
          <td>16340</td>
          <td>8749</td>
          <td>13014</td>
          <td>7776</td>
          <td>16547</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by Lost Revenue</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Canada Goose Men&#x27;s The Chateau Jacket</td>
          <td>Canada Goose</td>
          <td>Active</td>
          <td>815.0</td>
          <td>337.41</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>6</td>
          <td>0</td>
          <td>1</td>
          <td>4</td>
          <td>1</td>
          <td>4075.0</td>
          <td>2387.95</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.31e-05</td>
          <td>31</td>
          <td>39</td>
          <td>22532</td>
          <td>22532</td>
          <td>12532</td>
          <td>22532</td>
          <td>3978</td>
          <td>126</td>
          <td>23197</td>
          <td>1</td>
          <td>1</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>154</td>
          <td>1</td>
        </tr>
        <tr>
          <td>The North Face Denali Down Mens Jacket 2013</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>436.15</td>
          <td>2709.0</td>
          <td>1400.55</td>
          <td>13</td>
          <td>3</td>
          <td>2</td>
          <td>2</td>
          <td>6</td>
          <td>3612.0</td>
          <td>1867.4</td>
          <td>0.517</td>
          <td>0.4</td>
          <td>0.2727</td>
          <td>0.1538</td>
          <td>0.6667</td>
          <td>0.0010035</td>
          <td>0.001001</td>
          <td>7.17e-05</td>
          <td>5</td>
          <td>10</td>
          <td>7</td>
          <td>7</td>
          <td>423</td>
          <td>2358</td>
          <td>844</td>
          <td>2100</td>
          <td>1398</td>
          <td>2</td>
          <td>3</td>
          <td>10735</td>
          <td>8312</td>
          <td>14284</td>
          <td>12634</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Chilliwack Bomber</td>
          <td>Canada Goose</td>
          <td>Outerwear &amp; Coats</td>
          <td>695.0</td>
          <td>287.73</td>
          <td>695.0</td>
          <td>407.27</td>
          <td>8</td>
          <td>1</td>
          <td>3</td>
          <td>2</td>
          <td>2</td>
          <td>3475.0</td>
          <td>2036.35</td>
          <td>0.586</td>
          <td>0.75</td>
          <td>0.1667</td>
          <td>0.25</td>
          <td>0.6667</td>
          <td>0.0002575</td>
          <td>0.0002911</td>
          <td>4.41e-05</td>
          <td>46</td>
          <td>52</td>
          <td>294</td>
          <td>240</td>
          <td>5507</td>
          <td>13264</td>
          <td>151</td>
          <td>2100</td>
          <td>17069</td>
          <td>3</td>
          <td>2</td>
          <td>3719</td>
          <td>2834</td>
          <td>19436</td>
          <td>5542</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Woolrich Arctic Parka DF</td>
          <td>Woolrich</td>
          <td>Outerwear &amp; Coats</td>
          <td>990.0</td>
          <td>478.17</td>
          <td>2970.0</td>
          <td>1535.49</td>
          <td>12</td>
          <td>3</td>
          <td>2</td>
          <td>1</td>
          <td>6</td>
          <td>2970.0</td>
          <td>1535.49</td>
          <td>0.517</td>
          <td>0.4</td>
          <td>0.2727</td>
          <td>0.0833</td>
          <td>0.6667</td>
          <td>0.0011002</td>
          <td>0.0010974</td>
          <td>6.62e-05</td>
          <td>3</td>
          <td>6</td>
          <td>5</td>
          <td>6</td>
          <td>694</td>
          <td>2358</td>
          <td>844</td>
          <td>7029</td>
          <td>1398</td>
          <td>4</td>
          <td>4</td>
          <td>10735</td>
          <td>8312</td>
          <td>14284</td>
          <td>17144</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Mens Nike AirJordan Varsity Hoodie Jacket Grey / Black 451582-066</td>
          <td>Jordan</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>409.06</td>
          <td>903.0</td>
          <td>493.94</td>
          <td>8</td>
          <td>1</td>
          <td>2</td>
          <td>1</td>
          <td>4</td>
          <td>2709.0</td>
          <td>1481.82</td>
          <td>0.547</td>
          <td>0.6667</td>
          <td>0.1429</td>
          <td>0.125</td>
          <td>0.8</td>
          <td>0.0003345</td>
          <td>0.000353</td>
          <td>4.41e-05</td>
          <td>5</td>
          <td>14</td>
          <td>149</td>
          <td>153</td>
          <td>5507</td>
          <td>13264</td>
          <td>844</td>
          <td>7029</td>
          <td>6105</td>
          <td>5</td>
          <td>6</td>
          <td>7915</td>
          <td>3055</td>
          <td>20815</td>
          <td>14338</td>
          <td>7598</td>
        </tr>
        <tr>
          <td>NIKE WOMEN&#x27;S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort*</td>
          <td>Nike</td>
          <td>Intimates</td>
          <td>903.0</td>
          <td>512.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>1</td>
          <td>2709.0</td>
          <td>1173.0</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.75</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.21e-05</td>
          <td>5</td>
          <td>4</td>
          <td>22532</td>
          <td>22532</td>
          <td>21053</td>
          <td>22532</td>
          <td>13463</td>
          <td>526</td>
          <td>23197</td>
          <td>5</td>
          <td>15</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>109</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Spyder Women&#x27;s Jesst In Time Jacket</td>
          <td>Spyder</td>
          <td>Outerwear &amp; Coats</td>
          <td>650.0</td>
          <td>295.75</td>
          <td>3250.0</td>
          <td>1771.25</td>
          <td>10</td>
          <td>5</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>2600.0</td>
          <td>1417.0</td>
          <td>0.545</td>
          <td>0.4444</td>
          <td>0.5</td>
          <td>0.0</td>
          <td>0.1667</td>
          <td>0.0012039</td>
          <td>0.0012659</td>
          <td>5.52e-05</td>
          <td>52</td>
          <td>50</td>
          <td>3</td>
          <td>4</td>
          <td>1962</td>
          <td>251</td>
          <td>30</td>
          <td>17458</td>
          <td>23197</td>
          <td>7</td>
          <td>7</td>
          <td>8121</td>
          <td>8264</td>
          <td>3269</td>
          <td>17458</td>
          <td>27059</td>
        </tr>
        <tr>
          <td>IGIGI by Yuliya Raquel Plus Size Kandinsky Gown</td>
          <td>IGIGI by Yuliya Raquel</td>
          <td>Dresses</td>
          <td>325.0</td>
          <td>136.17</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>13</td>
          <td>0</td>
          <td>3</td>
          <td>5</td>
          <td>5</td>
          <td>2600.0</td>
          <td>1510.6</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.3846</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>7.17e-05</td>
          <td>236</td>
          <td>300</td>
          <td>22532</td>
          <td>22532</td>
          <td>423</td>
          <td>22532</td>
          <td>151</td>
          <td>24</td>
          <td>3026</td>
          <td>7</td>
          <td>5</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>2333</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Mystique</td>
          <td>Canada Goose</td>
          <td>Active</td>
          <td>750.0</td>
          <td>280.5</td>
          <td>750.0</td>
          <td>469.5</td>
          <td>9</td>
          <td>1</td>
          <td>1</td>
          <td>2</td>
          <td>5</td>
          <td>2250.0</td>
          <td>1408.5</td>
          <td>0.626</td>
          <td>0.5</td>
          <td>0.1429</td>
          <td>0.2222</td>
          <td>0.8333</td>
          <td>0.0002778</td>
          <td>0.0003355</td>
          <td>4.96e-05</td>
          <td>37</td>
          <td>53</td>
          <td>230</td>
          <td>170</td>
          <td>3355</td>
          <td>13264</td>
          <td>3978</td>
          <td>2100</td>
          <td>3026</td>
          <td>9</td>
          <td>8</td>
          <td>984</td>
          <td>4275</td>
          <td>20815</td>
          <td>7837</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Mystique</td>
          <td>Canada Goose</td>
          <td>Outerwear &amp; Coats</td>
          <td>750.0</td>
          <td>353.25</td>
          <td>1500.0</td>
          <td>793.5</td>
          <td>6</td>
          <td>2</td>
          <td>3</td>
          <td>0</td>
          <td>1</td>
          <td>2250.0</td>
          <td>1190.25</td>
          <td>0.529</td>
          <td>0.6</td>
          <td>0.3333</td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>0.0005557</td>
          <td>0.0005671</td>
          <td>3.31e-05</td>
          <td>37</td>
          <td>35</td>
          <td>41</td>
          <td>44</td>
          <td>12532</td>
          <td>6114</td>
          <td>151</td>
          <td>17458</td>
          <td>23197</td>
          <td>9</td>
          <td>13</td>
          <td>9645</td>
          <td>4103</td>
          <td>9747</td>
          <td>17458</td>
          <td>24854</td>
        </tr>
        <tr>
          <td>Arc&#x27;teryx Moray Jacket - Women&#x27;s</td>
          <td>Arc&#x27;teryx</td>
          <td>Outerwear &amp; Coats</td>
          <td>699.0</td>
          <td>343.91</td>
          <td>2097.0</td>
          <td>1065.28</td>
          <td>9</td>
          <td>3</td>
          <td>0</td>
          <td>3</td>
          <td>3</td>
          <td>2097.0</td>
          <td>1065.28</td>
          <td>0.508</td>
          <td>0.0</td>
          <td>0.5</td>
          <td>0.3333</td>
          <td>0.5</td>
          <td>0.0007768</td>
          <td>0.0007613</td>
          <td>4.96e-05</td>
          <td>41</td>
          <td>36</td>
          <td>15</td>
          <td>20</td>
          <td>3355</td>
          <td>2358</td>
          <td>13463</td>
          <td>526</td>
          <td>10869</td>
          <td>11</td>
          <td>22</td>
          <td>11720</td>
          <td>13463</td>
          <td>3269</td>
          <td>2619</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>Magaschoni Women&#x27;s Shimmer Jacket</td>
          <td>Magaschoni</td>
          <td>Blazers &amp; Jackets</td>
          <td>698.0</td>
          <td>258.96</td>
          <td>698.0</td>
          <td>439.04</td>
          <td>6</td>
          <td>1</td>
          <td>1</td>
          <td>2</td>
          <td>2</td>
          <td>2094.0</td>
          <td>1317.13</td>
          <td>0.629</td>
          <td>0.5</td>
          <td>0.25</td>
          <td>0.3333</td>
          <td>0.6667</td>
          <td>0.0002586</td>
          <td>0.0003138</td>
          <td>3.31e-05</td>
          <td>43</td>
          <td>58</td>
          <td>288</td>
          <td>201</td>
          <td>12532</td>
          <td>13264</td>
          <td>3978</td>
          <td>2100</td>
          <td>17069</td>
          <td>12</td>
          <td>9</td>
          <td>839</td>
          <td>4275</td>
          <td>14408</td>
          <td>2619</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Joseph Abboud Men&#x27;s Super 120&#x27;s Two Button Side Vent Single Pleat Pant Tuxedo With Grosgrain Notch Lapel</td>
          <td>Joseph Abboud</td>
          <td>Suits &amp; Sport Coats</td>
          <td>405.26</td>
          <td>145.08</td>
          <td>405.26</td>
          <td>260.18</td>
          <td>11</td>
          <td>1</td>
          <td>2</td>
          <td>3</td>
          <td>5</td>
          <td>2026.3</td>
          <td>1300.88</td>
          <td>0.642</td>
          <td>0.6667</td>
          <td>0.125</td>
          <td>0.2727</td>
          <td>0.8333</td>
          <td>0.0001501</td>
          <td>0.0001859</td>
          <td>6.07e-05</td>
          <td>108</td>
          <td>256</td>
          <td>961</td>
          <td>686</td>
          <td>1161</td>
          <td>13264</td>
          <td>844</td>
          <td>526</td>
          <td>3026</td>
          <td>13</td>
          <td>10</td>
          <td>361</td>
          <td>3055</td>
          <td>21675</td>
          <td>5408</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>Darla</td>
          <td>Alpha Industries</td>
          <td>Outerwear &amp; Coats</td>
          <td>999.0</td>
          <td>404.6</td>
          <td>1998.0</td>
          <td>1188.81</td>
          <td>7</td>
          <td>2</td>
          <td>2</td>
          <td>0</td>
          <td>3</td>
          <td>1998.0</td>
          <td>1188.81</td>
          <td>0.595</td>
          <td>0.5</td>
          <td>0.2857</td>
          <td>0.0</td>
          <td>0.6</td>
          <td>0.0007401</td>
          <td>0.0008496</td>
          <td>3.86e-05</td>
          <td>1</td>
          <td>16</td>
          <td>18</td>
          <td>15</td>
          <td>8625</td>
          <td>6114</td>
          <td>844</td>
          <td>17458</td>
          <td>10869</td>
          <td>14</td>
          <td>14</td>
          <td>2925</td>
          <td>4275</td>
          <td>13238</td>
          <td>17458</td>
          <td>16953</td>
        </tr>
        <tr>
          <td>Alpha Industries Rip Stop Short</td>
          <td>Alpha Industries</td>
          <td>Shorts</td>
          <td>999.0</td>
          <td>482.52</td>
          <td>999.0</td>
          <td>516.48</td>
          <td>8</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>5</td>
          <td>1998.0</td>
          <td>1032.97</td>
          <td>0.517</td>
          <td>0.5</td>
          <td>0.1429</td>
          <td>0.125</td>
          <td>0.8333</td>
          <td>0.0003701</td>
          <td>0.0003691</td>
          <td>4.41e-05</td>
          <td>1</td>
          <td>5</td>
          <td>120</td>
          <td>134</td>
          <td>5507</td>
          <td>13264</td>
          <td>3978</td>
          <td>7029</td>
          <td>3026</td>
          <td>14</td>
          <td>25</td>
          <td>10735</td>
          <td>4275</td>
          <td>20815</td>
          <td>14338</td>
          <td>6580</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Top products by Lost Profit</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Canada Goose Men&#x27;s The Chateau Jacket</td>
          <td>Canada Goose</td>
          <td>Active</td>
          <td>815.0</td>
          <td>337.41</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>6</td>
          <td>0</td>
          <td>1</td>
          <td>4</td>
          <td>1</td>
          <td>4075.0</td>
          <td>2387.95</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.31e-05</td>
          <td>31</td>
          <td>39</td>
          <td>22532</td>
          <td>22532</td>
          <td>12532</td>
          <td>22532</td>
          <td>3978</td>
          <td>126</td>
          <td>23197</td>
          <td>1</td>
          <td>1</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>154</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Chilliwack Bomber</td>
          <td>Canada Goose</td>
          <td>Outerwear &amp; Coats</td>
          <td>695.0</td>
          <td>287.73</td>
          <td>695.0</td>
          <td>407.27</td>
          <td>8</td>
          <td>1</td>
          <td>3</td>
          <td>2</td>
          <td>2</td>
          <td>3475.0</td>
          <td>2036.35</td>
          <td>0.586</td>
          <td>0.75</td>
          <td>0.1667</td>
          <td>0.25</td>
          <td>0.6667</td>
          <td>0.0002575</td>
          <td>0.0002911</td>
          <td>4.41e-05</td>
          <td>46</td>
          <td>52</td>
          <td>294</td>
          <td>240</td>
          <td>5507</td>
          <td>13264</td>
          <td>151</td>
          <td>2100</td>
          <td>17069</td>
          <td>3</td>
          <td>2</td>
          <td>3719</td>
          <td>2834</td>
          <td>19436</td>
          <td>5542</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>The North Face Denali Down Mens Jacket 2013</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>436.15</td>
          <td>2709.0</td>
          <td>1400.55</td>
          <td>13</td>
          <td>3</td>
          <td>2</td>
          <td>2</td>
          <td>6</td>
          <td>3612.0</td>
          <td>1867.4</td>
          <td>0.517</td>
          <td>0.4</td>
          <td>0.2727</td>
          <td>0.1538</td>
          <td>0.6667</td>
          <td>0.0010035</td>
          <td>0.001001</td>
          <td>7.17e-05</td>
          <td>5</td>
          <td>10</td>
          <td>7</td>
          <td>7</td>
          <td>423</td>
          <td>2358</td>
          <td>844</td>
          <td>2100</td>
          <td>1398</td>
          <td>2</td>
          <td>3</td>
          <td>10735</td>
          <td>8312</td>
          <td>14284</td>
          <td>12634</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Woolrich Arctic Parka DF</td>
          <td>Woolrich</td>
          <td>Outerwear &amp; Coats</td>
          <td>990.0</td>
          <td>478.17</td>
          <td>2970.0</td>
          <td>1535.49</td>
          <td>12</td>
          <td>3</td>
          <td>2</td>
          <td>1</td>
          <td>6</td>
          <td>2970.0</td>
          <td>1535.49</td>
          <td>0.517</td>
          <td>0.4</td>
          <td>0.2727</td>
          <td>0.0833</td>
          <td>0.6667</td>
          <td>0.0011002</td>
          <td>0.0010974</td>
          <td>6.62e-05</td>
          <td>3</td>
          <td>6</td>
          <td>5</td>
          <td>6</td>
          <td>694</td>
          <td>2358</td>
          <td>844</td>
          <td>7029</td>
          <td>1398</td>
          <td>4</td>
          <td>4</td>
          <td>10735</td>
          <td>8312</td>
          <td>14284</td>
          <td>17144</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>IGIGI by Yuliya Raquel Plus Size Kandinsky Gown</td>
          <td>IGIGI by Yuliya Raquel</td>
          <td>Dresses</td>
          <td>325.0</td>
          <td>136.17</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>13</td>
          <td>0</td>
          <td>3</td>
          <td>5</td>
          <td>5</td>
          <td>2600.0</td>
          <td>1510.6</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.3846</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>7.17e-05</td>
          <td>236</td>
          <td>300</td>
          <td>22532</td>
          <td>22532</td>
          <td>423</td>
          <td>22532</td>
          <td>151</td>
          <td>24</td>
          <td>3026</td>
          <td>7</td>
          <td>5</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>2333</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Mens Nike AirJordan Varsity Hoodie Jacket Grey / Black 451582-066</td>
          <td>Jordan</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>409.06</td>
          <td>903.0</td>
          <td>493.94</td>
          <td>8</td>
          <td>1</td>
          <td>2</td>
          <td>1</td>
          <td>4</td>
          <td>2709.0</td>
          <td>1481.82</td>
          <td>0.547</td>
          <td>0.6667</td>
          <td>0.1429</td>
          <td>0.125</td>
          <td>0.8</td>
          <td>0.0003345</td>
          <td>0.000353</td>
          <td>4.41e-05</td>
          <td>5</td>
          <td>14</td>
          <td>149</td>
          <td>153</td>
          <td>5507</td>
          <td>13264</td>
          <td>844</td>
          <td>7029</td>
          <td>6105</td>
          <td>5</td>
          <td>6</td>
          <td>7915</td>
          <td>3055</td>
          <td>20815</td>
          <td>14338</td>
          <td>7598</td>
        </tr>
        <tr>
          <td>Spyder Women&#x27;s Jesst In Time Jacket</td>
          <td>Spyder</td>
          <td>Outerwear &amp; Coats</td>
          <td>650.0</td>
          <td>295.75</td>
          <td>3250.0</td>
          <td>1771.25</td>
          <td>10</td>
          <td>5</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>2600.0</td>
          <td>1417.0</td>
          <td>0.545</td>
          <td>0.4444</td>
          <td>0.5</td>
          <td>0.0</td>
          <td>0.1667</td>
          <td>0.0012039</td>
          <td>0.0012659</td>
          <td>5.52e-05</td>
          <td>52</td>
          <td>50</td>
          <td>3</td>
          <td>4</td>
          <td>1962</td>
          <td>251</td>
          <td>30</td>
          <td>17458</td>
          <td>23197</td>
          <td>7</td>
          <td>7</td>
          <td>8121</td>
          <td>8264</td>
          <td>3269</td>
          <td>17458</td>
          <td>27059</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Mystique</td>
          <td>Canada Goose</td>
          <td>Active</td>
          <td>750.0</td>
          <td>280.5</td>
          <td>750.0</td>
          <td>469.5</td>
          <td>9</td>
          <td>1</td>
          <td>1</td>
          <td>2</td>
          <td>5</td>
          <td>2250.0</td>
          <td>1408.5</td>
          <td>0.626</td>
          <td>0.5</td>
          <td>0.1429</td>
          <td>0.2222</td>
          <td>0.8333</td>
          <td>0.0002778</td>
          <td>0.0003355</td>
          <td>4.96e-05</td>
          <td>37</td>
          <td>53</td>
          <td>230</td>
          <td>170</td>
          <td>3355</td>
          <td>13264</td>
          <td>3978</td>
          <td>2100</td>
          <td>3026</td>
          <td>9</td>
          <td>8</td>
          <td>984</td>
          <td>4275</td>
          <td>20815</td>
          <td>7837</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>Magaschoni Women&#x27;s Shimmer Jacket</td>
          <td>Magaschoni</td>
          <td>Blazers &amp; Jackets</td>
          <td>698.0</td>
          <td>258.96</td>
          <td>698.0</td>
          <td>439.04</td>
          <td>6</td>
          <td>1</td>
          <td>1</td>
          <td>2</td>
          <td>2</td>
          <td>2094.0</td>
          <td>1317.13</td>
          <td>0.629</td>
          <td>0.5</td>
          <td>0.25</td>
          <td>0.3333</td>
          <td>0.6667</td>
          <td>0.0002586</td>
          <td>0.0003138</td>
          <td>3.31e-05</td>
          <td>43</td>
          <td>58</td>
          <td>288</td>
          <td>201</td>
          <td>12532</td>
          <td>13264</td>
          <td>3978</td>
          <td>2100</td>
          <td>17069</td>
          <td>12</td>
          <td>9</td>
          <td>839</td>
          <td>4275</td>
          <td>14408</td>
          <td>2619</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Joseph Abboud Men&#x27;s Super 120&#x27;s Two Button Side Vent Single Pleat Pant Tuxedo With Grosgrain Notch Lapel</td>
          <td>Joseph Abboud</td>
          <td>Suits &amp; Sport Coats</td>
          <td>405.26</td>
          <td>145.08</td>
          <td>405.26</td>
          <td>260.18</td>
          <td>11</td>
          <td>1</td>
          <td>2</td>
          <td>3</td>
          <td>5</td>
          <td>2026.3</td>
          <td>1300.88</td>
          <td>0.642</td>
          <td>0.6667</td>
          <td>0.125</td>
          <td>0.2727</td>
          <td>0.8333</td>
          <td>0.0001501</td>
          <td>0.0001859</td>
          <td>6.07e-05</td>
          <td>108</td>
          <td>256</td>
          <td>961</td>
          <td>686</td>
          <td>1161</td>
          <td>13264</td>
          <td>844</td>
          <td>526</td>
          <td>3026</td>
          <td>13</td>
          <td>10</td>
          <td>361</td>
          <td>3055</td>
          <td>21675</td>
          <td>5408</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>MiH Jeans Women&#x27;s Aztec Jacket</td>
          <td>MiH Jeans</td>
          <td>Blazers &amp; Jackets</td>
          <td>495.0</td>
          <td>169.79</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>6</td>
          <td>0</td>
          <td>2</td>
          <td>2</td>
          <td>2</td>
          <td>1980.0</td>
          <td>1300.86</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.31e-05</td>
          <td>74</td>
          <td>157</td>
          <td>22532</td>
          <td>22532</td>
          <td>12532</td>
          <td>22532</td>
          <td>844</td>
          <td>2100</td>
          <td>17069</td>
          <td>16</td>
          <td>11</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>2619</td>
          <td>1</td>
        </tr>
        <tr>
          <td>DOLCE &amp; GABBANA DG4167 501/8G BLACK GRAY GRADIENT 5917</td>
          <td>Dolce &amp; Gabbana</td>
          <td>Accessories</td>
          <td>243.0</td>
          <td>94.67</td>
          <td>486.0</td>
          <td>294.03</td>
          <td>14</td>
          <td>2</td>
          <td>3</td>
          <td>5</td>
          <td>4</td>
          <td>1944.0</td>
          <td>1194.59</td>
          <td>0.605</td>
          <td>0.6</td>
          <td>0.2222</td>
          <td>0.3571</td>
          <td>0.6667</td>
          <td>0.00018</td>
          <td>0.0002101</td>
          <td>7.72e-05</td>
          <td>541</td>
          <td>948</td>
          <td>707</td>
          <td>527</td>
          <td>268</td>
          <td>6114</td>
          <td>151</td>
          <td>24</td>
          <td>6105</td>
          <td>18</td>
          <td>12</td>
          <td>2194</td>
          <td>4103</td>
          <td>17122</td>
          <td>2614</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Mystique</td>
          <td>Canada Goose</td>
          <td>Outerwear &amp; Coats</td>
          <td>750.0</td>
          <td>353.25</td>
          <td>1500.0</td>
          <td>793.5</td>
          <td>6</td>
          <td>2</td>
          <td>3</td>
          <td>0</td>
          <td>1</td>
          <td>2250.0</td>
          <td>1190.25</td>
          <td>0.529</td>
          <td>0.6</td>
          <td>0.3333</td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>0.0005557</td>
          <td>0.0005671</td>
          <td>3.31e-05</td>
          <td>37</td>
          <td>35</td>
          <td>41</td>
          <td>44</td>
          <td>12532</td>
          <td>6114</td>
          <td>151</td>
          <td>17458</td>
          <td>23197</td>
          <td>9</td>
          <td>13</td>
          <td>9645</td>
          <td>4103</td>
          <td>9747</td>
          <td>17458</td>
          <td>24854</td>
        </tr>
        <tr>
          <td>Darla</td>
          <td>Alpha Industries</td>
          <td>Outerwear &amp; Coats</td>
          <td>999.0</td>
          <td>404.6</td>
          <td>1998.0</td>
          <td>1188.81</td>
          <td>7</td>
          <td>2</td>
          <td>2</td>
          <td>0</td>
          <td>3</td>
          <td>1998.0</td>
          <td>1188.81</td>
          <td>0.595</td>
          <td>0.5</td>
          <td>0.2857</td>
          <td>0.0</td>
          <td>0.6</td>
          <td>0.0007401</td>
          <td>0.0008496</td>
          <td>3.86e-05</td>
          <td>1</td>
          <td>16</td>
          <td>18</td>
          <td>15</td>
          <td>8625</td>
          <td>6114</td>
          <td>844</td>
          <td>17458</td>
          <td>10869</td>
          <td>14</td>
          <td>14</td>
          <td>2925</td>
          <td>4275</td>
          <td>13238</td>
          <td>17458</td>
          <td>16953</td>
        </tr>
        <tr>
          <td>NIKE WOMEN&#x27;S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort*</td>
          <td>Nike</td>
          <td>Intimates</td>
          <td>903.0</td>
          <td>512.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>1</td>
          <td>2709.0</td>
          <td>1173.0</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.75</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.21e-05</td>
          <td>5</td>
          <td>4</td>
          <td>22532</td>
          <td>22532</td>
          <td>21053</td>
          <td>22532</td>
          <td>13463</td>
          <td>526</td>
          <td>23197</td>
          <td>5</td>
          <td>15</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>109</td>
          <td>1</td>
        </tr>
      </tbody>
    </table>
  </div>

</details>
<details>
  <summary><strong>Bottom Products</strong></summary>

  <div style="margin-top: 12px;"></div>

  <p><strong>Bottom products by Revenue</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Marc Ecko Cut &amp; Sew Men&#x27;s Pinstripe and Plaid Pieced Vest</td>
          <td>Marc Ecko Cut &amp; Sew</td>
          <td>Suits &amp; Sport Coats</td>
          <td>47.43</td>
          <td>17.83</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>10</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>7</td>
          <td>142.29</td>
          <td>88.79</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.3</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5.52e-05</td>
          <td>12005</td>
          <td>15475</td>
          <td>22532</td>
          <td>22532</td>
          <td>1962</td>
          <td>22532</td>
          <td>13463</td>
          <td>526</td>
          <td>623</td>
          <td>5528</td>
          <td>4189</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>4443</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Dexter&#x27;s Wings - Dexter T-shirt</td>
          <td>Dexter</td>
          <td>Tops &amp; Tees</td>
          <td>19.95</td>
          <td>11.11</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>3</td>
          <td>39.9</td>
          <td>17.68</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.2</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.76e-05</td>
          <td>23040</td>
          <td>21439</td>
          <td>22532</td>
          <td>22532</td>
          <td>16887</td>
          <td>22532</td>
          <td>3978</td>
          <td>7029</td>
          <td>10869</td>
          <td>16370</td>
          <td>17124</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>8435</td>
          <td>1</td>
        </tr>
        <tr>
          <td>RSQ Miami Womens Jeggings</td>
          <td>RSQ</td>
          <td>Pants &amp; Capris</td>
          <td>39.99</td>
          <td>22.07</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>2</td>
          <td>79.98</td>
          <td>35.83</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.25</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.21e-05</td>
          <td>13925</td>
          <td>12599</td>
          <td>22532</td>
          <td>22532</td>
          <td>21053</td>
          <td>22532</td>
          <td>3978</td>
          <td>7029</td>
          <td>17069</td>
          <td>10039</td>
          <td>11208</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>5542</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Medela Sleep Bra Nude Large</td>
          <td>Medela</td>
          <td>Maternity</td>
          <td>15.99</td>
          <td>6.88</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>7</td>
          <td>0</td>
          <td>3</td>
          <td>1</td>
          <td>3</td>
          <td>63.96</td>
          <td>36.46</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.1429</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.86e-05</td>
          <td>24393</td>
          <td>25240</td>
          <td>22532</td>
          <td>22532</td>
          <td>8625</td>
          <td>22532</td>
          <td>151</td>
          <td>7029</td>
          <td>10869</td>
          <td>12226</td>
          <td>11055</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>12706</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Diesel Women&#x27;s Louvboot Slim Flare Jean</td>
          <td>Diesel</td>
          <td>Jeans</td>
          <td>198.0</td>
          <td>97.61</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>2</td>
          <td>2</td>
          <td>396.0</td>
          <td>200.77</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.5</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.21e-05</td>
          <td>875</td>
          <td>836</td>
          <td>22532</td>
          <td>22532</td>
          <td>21053</td>
          <td>22532</td>
          <td>13463</td>
          <td>2100</td>
          <td>17069</td>
          <td>1005</td>
          <td>1124</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>477</td>
          <td>1</td>
        </tr>
        <tr>
          <td>SockGuy Men&#x27;s Wooligan Socks</td>
          <td>SockGuy</td>
          <td>Socks</td>
          <td>12.95</td>
          <td>7.33</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>2</td>
          <td>2</td>
          <td>25.9</td>
          <td>11.24</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.5</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.21e-05</td>
          <td>25924</td>
          <td>24844</td>
          <td>22532</td>
          <td>22532</td>
          <td>21053</td>
          <td>22532</td>
          <td>13463</td>
          <td>2100</td>
          <td>17069</td>
          <td>19080</td>
          <td>19933</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>477</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Allegra K Mens Casual Vertical Stripes Pattern Decor NEW Stylish Short Trousers Deep Beige W31</td>
          <td>Allegra K</td>
          <td>Shorts</td>
          <td>15.95</td>
          <td>7.99</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>6</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>5</td>
          <td>15.95</td>
          <td>7.96</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.31e-05</td>
          <td>24488</td>
          <td>24197</td>
          <td>22532</td>
          <td>22532</td>
          <td>12532</td>
          <td>22532</td>
          <td>3978</td>
          <td>17458</td>
          <td>3026</td>
          <td>21250</td>
          <td>21221</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Southpole Men&#x27;s Angled Cross With Shadowed Background Print Fashion T-Shirt</td>
          <td>Southpole</td>
          <td>Tops &amp; Tees</td>
          <td>25.0</td>
          <td>13.52</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>6</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>5</td>
          <td>25.0</td>
          <td>11.48</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.1667</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.31e-05</td>
          <td>19651</td>
          <td>19040</td>
          <td>22532</td>
          <td>22532</td>
          <td>12532</td>
          <td>22532</td>
          <td>13463</td>
          <td>7029</td>
          <td>3026</td>
          <td>19164</td>
          <td>19837</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>10731</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Brushed-Back Satin Pajamas - Women&#x27;s Sizes</td>
          <td>Carol Wright Gifts</td>
          <td>Sleep &amp; Lounge</td>
          <td>24.99</td>
          <td>15.07</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>2</td>
          <td>24.99</td>
          <td>9.92</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.65e-05</td>
          <td>20698</td>
          <td>17708</td>
          <td>22532</td>
          <td>22532</td>
          <td>24645</td>
          <td>22532</td>
          <td>3978</td>
          <td>17458</td>
          <td>17069</td>
          <td>19500</td>
          <td>20477</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Tommy Hilfiger Men&#x27;s Tommy Tartan Boxer</td>
          <td>Tommy Hilfiger</td>
          <td>Underwear</td>
          <td>18.0</td>
          <td>8.69</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>3</td>
          <td>36.0</td>
          <td>18.61</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.2</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.76e-05</td>
          <td>23512</td>
          <td>23579</td>
          <td>22532</td>
          <td>22532</td>
          <td>16887</td>
          <td>22532</td>
          <td>3978</td>
          <td>7029</td>
          <td>10869</td>
          <td>16903</td>
          <td>16747</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>8435</td>
          <td>1</td>
        </tr>
        <tr>
          <td>One Pair MarcolianiMen&#x27;s Italian Cashmere and Silk Over-the-Calf Fancy Argyle Socks</td>
          <td>Marcoliani Milano</td>
          <td>Socks</td>
          <td>89.5</td>
          <td>49.58</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>89.5</td>
          <td>39.92</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.1e-05</td>
          <td>4936</td>
          <td>3880</td>
          <td>22532</td>
          <td>22532</td>
          <td>26863</td>
          <td>22532</td>
          <td>3978</td>
          <td>17458</td>
          <td>23197</td>
          <td>9283</td>
          <td>10290</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Allegra K Ladies Dotted Double V Neck Banded Dress Pink White M</td>
          <td>Allegra K</td>
          <td>Dresses</td>
          <td>10.15</td>
          <td>4.83</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>5</td>
          <td>0.0</td>
          <td>0.0</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.76e-05</td>
          <td>26937</td>
          <td>27097</td>
          <td>22532</td>
          <td>22532</td>
          <td>16887</td>
          <td>22532</td>
          <td>13463</td>
          <td>17458</td>
          <td>3026</td>
          <td>22642</td>
          <td>22642</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
        <tr>
          <td>7 For All Mankind Women&#x27;s Relaxed Mid Roll Up Short Authentic Nakita</td>
          <td>7 For All Mankind</td>
          <td>Shorts</td>
          <td>178.0</td>
          <td>82.95</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>6</td>
          <td>0</td>
          <td>2</td>
          <td>1</td>
          <td>3</td>
          <td>534.0</td>
          <td>285.16</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.1667</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3.31e-05</td>
          <td>1246</td>
          <td>1403</td>
          <td>22532</td>
          <td>22532</td>
          <td>12532</td>
          <td>22532</td>
          <td>844</td>
          <td>7029</td>
          <td>10869</td>
          <td>570</td>
          <td>582</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>10731</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Fox Men&#x27;s Essex Short</td>
          <td>Fox</td>
          <td>Shorts</td>
          <td>42.5</td>
          <td>19.51</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>2</td>
          <td>42.5</td>
          <td>22.99</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.65e-05</td>
          <td>13301</td>
          <td>14268</td>
          <td>22532</td>
          <td>22532</td>
          <td>24645</td>
          <td>22532</td>
          <td>13463</td>
          <td>7029</td>
          <td>17069</td>
          <td>15731</td>
          <td>15034</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>2619</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Motherhood Maternity: Plus Size Secret Fit Belly(r) Boot Cut Maternity Jeans</td>
          <td>Motherhood Maternity</td>
          <td>Maternity</td>
          <td>34.98</td>
          <td>15.74</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>3</td>
          <td>0.0</td>
          <td>0.0</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.65e-05</td>
          <td>16197</td>
          <td>17160</td>
          <td>22532</td>
          <td>22532</td>
          <td>24645</td>
          <td>22532</td>
          <td>13463</td>
          <td>17458</td>
          <td>10869</td>
          <td>22642</td>
          <td>22642</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by Profit</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>HUGO BOSS Men&#x27;s Bright Argyle Crew Sock</td>
          <td>HUGO BOSS</td>
          <td>Socks</td>
          <td>9.75</td>
          <td>5.68</td>
          <td>39.0</td>
          <td>15.65</td>
          <td>22</td>
          <td>4</td>
          <td>4</td>
          <td>4</td>
          <td>10</td>
          <td>78.0</td>
          <td>32.25</td>
          <td>0.4013</td>
          <td>0.5</td>
          <td>0.2222</td>
          <td>0.1818</td>
          <td>0.7143</td>
          <td>1.44e-05</td>
          <td>1.12e-05</td>
          <td>0.0001214</td>
          <td>27342</td>
          <td>26355</td>
          <td>16327</td>
          <td>17765</td>
          <td>43</td>
          <td>776</td>
          <td>30</td>
          <td>126</td>
          <td>77</td>
          <td>10368</td>
          <td>12068</td>
          <td>20837</td>
          <td>4275</td>
          <td>17122</td>
          <td>10468</td>
          <td>12035</td>
        </tr>
        <tr>
          <td>New Men&#x27;s Sexy Center Patch Bikini Swimsuit 3G by Gregg Homme</td>
          <td>Gregg Homme</td>
          <td>Swim</td>
          <td>13.22</td>
          <td>7.85</td>
          <td>54.6</td>
          <td>20.64</td>
          <td>25</td>
          <td>4</td>
          <td>2</td>
          <td>5</td>
          <td>14</td>
          <td>90.3</td>
          <td>38.29</td>
          <td>0.378</td>
          <td>0.3333</td>
          <td>0.2</td>
          <td>0.2</td>
          <td>0.7778</td>
          <td>2.02e-05</td>
          <td>1.48e-05</td>
          <td>0.0001379</td>
          <td>25672</td>
          <td>24345</td>
          <td>13422</td>
          <td>15782</td>
          <td>21</td>
          <td>776</td>
          <td>844</td>
          <td>24</td>
          <td>22</td>
          <td>8973</td>
          <td>10649</td>
          <td>21721</td>
          <td>8752</td>
          <td>17510</td>
          <td>8435</td>
          <td>9281</td>
        </tr>
        <tr>
          <td>Kenneth Cole Men&#x27;s Straight Leg Jean</td>
          <td>Kenneth Cole</td>
          <td>Jeans</td>
          <td>54.25</td>
          <td>27.11</td>
          <td>54.99</td>
          <td>26.89</td>
          <td>24</td>
          <td>1</td>
          <td>7</td>
          <td>4</td>
          <td>12</td>
          <td>632.25</td>
          <td>318.8</td>
          <td>0.489</td>
          <td>0.875</td>
          <td>0.05</td>
          <td>0.1667</td>
          <td>0.9231</td>
          <td>2.04e-05</td>
          <td>1.92e-05</td>
          <td>0.0001324</td>
          <td>10100</td>
          <td>9920</td>
          <td>13356</td>
          <td>13628</td>
          <td>30</td>
          <td>13264</td>
          <td>1</td>
          <td>126</td>
          <td>37</td>
          <td>380</td>
          <td>462</td>
          <td>13602</td>
          <td>2795</td>
          <td>22531</td>
          <td>10731</td>
          <td>5642</td>
        </tr>
        <tr>
          <td>Tommy Hilfiger Men Classic Fit T-shirt</td>
          <td>Tommy Hilfiger</td>
          <td>Tops &amp; Tees</td>
          <td>21.99</td>
          <td>12.22</td>
          <td>65.97</td>
          <td>28.41</td>
          <td>25</td>
          <td>3</td>
          <td>2</td>
          <td>5</td>
          <td>15</td>
          <td>153.93</td>
          <td>70.63</td>
          <td>0.4307</td>
          <td>0.4</td>
          <td>0.15</td>
          <td>0.2</td>
          <td>0.8333</td>
          <td>2.44e-05</td>
          <td>2.03e-05</td>
          <td>0.0001379</td>
          <td>22049</td>
          <td>20333</td>
          <td>11887</td>
          <td>13165</td>
          <td>21</td>
          <td>2358</td>
          <td>844</td>
          <td>24</td>
          <td>11</td>
          <td>4954</td>
          <td>5704</td>
          <td>18998</td>
          <td>8312</td>
          <td>20814</td>
          <td>8435</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>Volcom Juniors Pocket Blocket Long Sleeve Tee</td>
          <td>Volcom</td>
          <td>Tops &amp; Tees</td>
          <td>27.0</td>
          <td>15.34</td>
          <td>81.0</td>
          <td>33.86</td>
          <td>21</td>
          <td>3</td>
          <td>4</td>
          <td>5</td>
          <td>9</td>
          <td>243.0</td>
          <td>107.41</td>
          <td>0.418</td>
          <td>0.5714</td>
          <td>0.1875</td>
          <td>0.2381</td>
          <td>0.75</td>
          <td>3e-05</td>
          <td>2.42e-05</td>
          <td>0.0001158</td>
          <td>19072</td>
          <td>17500</td>
          <td>9846</td>
          <td>11622</td>
          <td>50</td>
          <td>2358</td>
          <td>30</td>
          <td>24</td>
          <td>140</td>
          <td>2456</td>
          <td>3131</td>
          <td>20016</td>
          <td>4252</td>
          <td>19354</td>
          <td>7773</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>Puma Men&#x27;s Socks</td>
          <td>PUMA</td>
          <td>Socks</td>
          <td>13.0</td>
          <td>7.78</td>
          <td>90.0</td>
          <td>35.98</td>
          <td>24</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>11</td>
          <td>78.0</td>
          <td>31.36</td>
          <td>0.3998</td>
          <td>0.125</td>
          <td>0.3684</td>
          <td>0.2083</td>
          <td>0.6111</td>
          <td>3.33e-05</td>
          <td>2.57e-05</td>
          <td>0.0001324</td>
          <td>25705</td>
          <td>24414</td>
          <td>8929</td>
          <td>11107</td>
          <td>30</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>43</td>
          <td>10368</td>
          <td>12295</td>
          <td>20955</td>
          <td>13444</td>
          <td>9637</td>
          <td>8433</td>
          <td>16951</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Striped Crew Sock</td>
          <td>HUGO BOSS</td>
          <td>Socks</td>
          <td>13.0</td>
          <td>8.14</td>
          <td>104.0</td>
          <td>40.17</td>
          <td>24</td>
          <td>8</td>
          <td>3</td>
          <td>4</td>
          <td>9</td>
          <td>91.0</td>
          <td>33.33</td>
          <td>0.3863</td>
          <td>0.2727</td>
          <td>0.4</td>
          <td>0.1667</td>
          <td>0.5294</td>
          <td>3.85e-05</td>
          <td>2.87e-05</td>
          <td>0.0001324</td>
          <td>25705</td>
          <td>24062</td>
          <td>7764</td>
          <td>10157</td>
          <td>30</td>
          <td>16</td>
          <td>151</td>
          <td>126</td>
          <td>140</td>
          <td>8958</td>
          <td>11794</td>
          <td>21483</td>
          <td>11342</td>
          <td>7482</td>
          <td>10731</td>
          <td>19498</td>
        </tr>
        <tr>
          <td>Lilly Pulitzer Women&#x27;s Callahan Short</td>
          <td>Lilly Pulitzer</td>
          <td>Shorts</td>
          <td>48.24</td>
          <td>24.35</td>
          <td>106.11</td>
          <td>53.14</td>
          <td>24</td>
          <td>2</td>
          <td>4</td>
          <td>5</td>
          <td>13</td>
          <td>420.02</td>
          <td>207.44</td>
          <td>0.5008</td>
          <td>0.6667</td>
          <td>0.1053</td>
          <td>0.2083</td>
          <td>0.8667</td>
          <td>3.93e-05</td>
          <td>3.8e-05</td>
          <td>0.0001324</td>
          <td>11747</td>
          <td>11307</td>
          <td>7626</td>
          <td>7813</td>
          <td>30</td>
          <td>6114</td>
          <td>30</td>
          <td>24</td>
          <td>31</td>
          <td>883</td>
          <td>1063</td>
          <td>12538</td>
          <td>3055</td>
          <td>22368</td>
          <td>8433</td>
          <td>6056</td>
        </tr>
        <tr>
          <td>Lee Men&#x27;s Relaxed Fit Slightly Tapered Leg Jean</td>
          <td>Lee</td>
          <td>Jeans</td>
          <td>30.99</td>
          <td>16.89</td>
          <td>122.96</td>
          <td>55.54</td>
          <td>21</td>
          <td>4</td>
          <td>5</td>
          <td>3</td>
          <td>9</td>
          <td>248.92</td>
          <td>113.31</td>
          <td>0.4517</td>
          <td>0.5556</td>
          <td>0.2222</td>
          <td>0.1429</td>
          <td>0.6923</td>
          <td>4.55e-05</td>
          <td>3.97e-05</td>
          <td>0.0001158</td>
          <td>17446</td>
          <td>16178</td>
          <td>6481</td>
          <td>7447</td>
          <td>50</td>
          <td>776</td>
          <td>5</td>
          <td>526</td>
          <td>140</td>
          <td>2405</td>
          <td>2891</td>
          <td>17150</td>
          <td>4274</td>
          <td>17122</td>
          <td>12706</td>
          <td>12966</td>
        </tr>
        <tr>
          <td>Bottoms Out Men&#x27;s Plaid Sleep Pant</td>
          <td>Bottoms Out</td>
          <td>Sleep &amp; Lounge</td>
          <td>13.49</td>
          <td>5.05</td>
          <td>94.43</td>
          <td>59.4</td>
          <td>25</td>
          <td>7</td>
          <td>2</td>
          <td>4</td>
          <td>12</td>
          <td>80.94</td>
          <td>50.64</td>
          <td>0.629</td>
          <td>0.2222</td>
          <td>0.3333</td>
          <td>0.16</td>
          <td>0.6316</td>
          <td>3.5e-05</td>
          <td>4.25e-05</td>
          <td>0.0001379</td>
          <td>25625</td>
          <td>26913</td>
          <td>8758</td>
          <td>6904</td>
          <td>21</td>
          <td>33</td>
          <td>844</td>
          <td>126</td>
          <td>37</td>
          <td>9890</td>
          <td>8299</td>
          <td>839</td>
          <td>12628</td>
          <td>9747</td>
          <td>12630</td>
          <td>16546</td>
        </tr>
        <tr>
          <td>RSQ London Mens Skinny Jeans</td>
          <td>RSQ</td>
          <td>Jeans</td>
          <td>44.99</td>
          <td>24.2</td>
          <td>134.97</td>
          <td>63.21</td>
          <td>21</td>
          <td>3</td>
          <td>5</td>
          <td>3</td>
          <td>10</td>
          <td>359.92</td>
          <td>163.94</td>
          <td>0.4683</td>
          <td>0.625</td>
          <td>0.1667</td>
          <td>0.1429</td>
          <td>0.7692</td>
          <td>5e-05</td>
          <td>4.52e-05</td>
          <td>0.0001158</td>
          <td>12553</td>
          <td>11383</td>
          <td>5908</td>
          <td>6477</td>
          <td>50</td>
          <td>2358</td>
          <td>5</td>
          <td>526</td>
          <td>77</td>
          <td>1228</td>
          <td>1608</td>
          <td>15636</td>
          <td>4099</td>
          <td>19436</td>
          <td>12706</td>
          <td>9471</td>
        </tr>
        <tr>
          <td>Diesel Men&#x27;s Blade Underpant</td>
          <td>Diesel</td>
          <td>Underwear</td>
          <td>22.14</td>
          <td>9.75</td>
          <td>122.0</td>
          <td>66.53</td>
          <td>22</td>
          <td>6</td>
          <td>0</td>
          <td>2</td>
          <td>14</td>
          <td>43.0</td>
          <td>23.83</td>
          <td>0.5453</td>
          <td>0.0</td>
          <td>0.3</td>
          <td>0.0909</td>
          <td>0.7</td>
          <td>4.52e-05</td>
          <td>4.75e-05</td>
          <td>0.0001214</td>
          <td>21886</td>
          <td>22702</td>
          <td>6504</td>
          <td>6114</td>
          <td>43</td>
          <td>84</td>
          <td>13463</td>
          <td>2100</td>
          <td>22</td>
          <td>15676</td>
          <td>14732</td>
          <td>8115</td>
          <td>13463</td>
          <td>13033</td>
          <td>16872</td>
          <td>12849</td>
        </tr>
        <tr>
          <td>Michael Kors Men&#x27;s 3 Pack Brief</td>
          <td>Michael Kors</td>
          <td>Underwear</td>
          <td>25.99</td>
          <td>12.48</td>
          <td>130.46</td>
          <td>67.73</td>
          <td>24</td>
          <td>5</td>
          <td>5</td>
          <td>4</td>
          <td>10</td>
          <td>232.38</td>
          <td>120.98</td>
          <td>0.5192</td>
          <td>0.5</td>
          <td>0.25</td>
          <td>0.1667</td>
          <td>0.6667</td>
          <td>4.83e-05</td>
          <td>4.84e-05</td>
          <td>0.0001324</td>
          <td>19456</td>
          <td>20053</td>
          <td>6070</td>
          <td>5979</td>
          <td>30</td>
          <td>251</td>
          <td>5</td>
          <td>126</td>
          <td>77</td>
          <td>2705</td>
          <td>2646</td>
          <td>10469</td>
          <td>4275</td>
          <td>14408</td>
          <td>10731</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>RUDE Dark Vintage Skinny Jeans</td>
          <td>Hot Topic</td>
          <td>Jeans</td>
          <td>36.5</td>
          <td>19.33</td>
          <td>146.0</td>
          <td>68.99</td>
          <td>24</td>
          <td>4</td>
          <td>4</td>
          <td>3</td>
          <td>13</td>
          <td>255.5</td>
          <td>123.41</td>
          <td>0.4725</td>
          <td>0.5</td>
          <td>0.1905</td>
          <td>0.125</td>
          <td>0.7647</td>
          <td>5.41e-05</td>
          <td>4.93e-05</td>
          <td>0.0001324</td>
          <td>15396</td>
          <td>14389</td>
          <td>5357</td>
          <td>5845</td>
          <td>30</td>
          <td>776</td>
          <td>30</td>
          <td>526</td>
          <td>31</td>
          <td>2306</td>
          <td>2570</td>
          <td>15319</td>
          <td>4275</td>
          <td>19353</td>
          <td>14338</td>
          <td>9484</td>
        </tr>
        <tr>
          <td>Bottoms Out Men&#x27;s Plaid Sleep Jam</td>
          <td>Bottoms Out</td>
          <td>Sleep &amp; Lounge</td>
          <td>25.0</td>
          <td>9.3</td>
          <td>125.0</td>
          <td>78.03</td>
          <td>24</td>
          <td>5</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>100.0</td>
          <td>63.2</td>
          <td>0.6242</td>
          <td>0.2857</td>
          <td>0.2273</td>
          <td>0.0833</td>
          <td>0.75</td>
          <td>4.63e-05</td>
          <td>5.58e-05</td>
          <td>0.0001324</td>
          <td>19651</td>
          <td>23078</td>
          <td>6364</td>
          <td>5026</td>
          <td>30</td>
          <td>251</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>7972</td>
          <td>6500</td>
          <td>1088</td>
          <td>11280</td>
          <td>17121</td>
          <td>17144</td>
          <td>9487</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by Profit Margin</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>The North Face Apex Bionic Soft Shell Jacket - Men&#x27;s</td>
          <td>The North Face</td>
          <td>Fashion Hoodies &amp; Sweatshirts</td>
          <td>903.0</td>
          <td>524.64</td>
          <td>1806.0</td>
          <td>756.71</td>
          <td>6</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>4</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.419</td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>0.000669</td>
          <td>0.0005408</td>
          <td>3.31e-05</td>
          <td>5</td>
          <td>3</td>
          <td>21</td>
          <td>55</td>
          <td>12532</td>
          <td>6114</td>
          <td>13463</td>
          <td>17458</td>
          <td>6105</td>
          <td>22642</td>
          <td>22642</td>
          <td>19960</td>
          <td>13463</td>
          <td>9747</td>
          <td>17458</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>PAIGE Women&#x27;s Skyline Skinny Jean</td>
          <td>PAIGE</td>
          <td>Jeans</td>
          <td>158.0</td>
          <td>90.19</td>
          <td>1422.0</td>
          <td>608.93</td>
          <td>19</td>
          <td>9</td>
          <td>0</td>
          <td>2</td>
          <td>8</td>
          <td>316.0</td>
          <td>135.88</td>
          <td>0.4282</td>
          <td>0.0</td>
          <td>0.5294</td>
          <td>0.1053</td>
          <td>0.4706</td>
          <td>0.0005268</td>
          <td>0.0004352</td>
          <td>0.0001048</td>
          <td>1714</td>
          <td>1108</td>
          <td>48</td>
          <td>90</td>
          <td>72</td>
          <td>5</td>
          <td>13463</td>
          <td>2100</td>
          <td>295</td>
          <td>1575</td>
          <td>2230</td>
          <td>19172</td>
          <td>13463</td>
          <td>3268</td>
          <td>16363</td>
          <td>23444</td>
        </tr>
        <tr>
          <td>7 For All Mankind Men&#x27;s Austyn Relaxed Straight Jean</td>
          <td>7 For All Mankind</td>
          <td>Jeans</td>
          <td>197.94</td>
          <td>111.63</td>
          <td>1399.0</td>
          <td>608.64</td>
          <td>17</td>
          <td>7</td>
          <td>0</td>
          <td>1</td>
          <td>9</td>
          <td>189.0</td>
          <td>83.35</td>
          <td>0.4351</td>
          <td>0.0</td>
          <td>0.4375</td>
          <td>0.0588</td>
          <td>0.5625</td>
          <td>0.0005182</td>
          <td>0.000435</td>
          <td>9.38e-05</td>
          <td>942</td>
          <td>526</td>
          <td>50</td>
          <td>91</td>
          <td>103</td>
          <td>33</td>
          <td>13463</td>
          <td>7029</td>
          <td>140</td>
          <td>3671</td>
          <td>4605</td>
          <td>18597</td>
          <td>13463</td>
          <td>6734</td>
          <td>17433</td>
          <td>19266</td>
        </tr>
        <tr>
          <td>Catherine Malandrino Women&#x27;s Stretch Leather Pant</td>
          <td>Catherine Malandrino</td>
          <td>Leggings</td>
          <td>528.81</td>
          <td>291.37</td>
          <td>1586.43</td>
          <td>712.31</td>
          <td>5</td>
          <td>3</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>528.81</td>
          <td>237.44</td>
          <td>0.449</td>
          <td>0.25</td>
          <td>0.6</td>
          <td>0.0</td>
          <td>0.25</td>
          <td>0.0005877</td>
          <td>0.0005091</td>
          <td>2.76e-05</td>
          <td>68</td>
          <td>51</td>
          <td>38</td>
          <td>59</td>
          <td>16887</td>
          <td>2358</td>
          <td>3978</td>
          <td>17458</td>
          <td>23197</td>
          <td>584</td>
          <td>835</td>
          <td>17380</td>
          <td>11344</td>
          <td>2189</td>
          <td>17458</td>
          <td>26348</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Leg Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>227.86</td>
          <td>123.14</td>
          <td>1452.0</td>
          <td>661.01</td>
          <td>28</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>15</td>
          <td>1430.0</td>
          <td>645.85</td>
          <td>0.4552</td>
          <td>0.125</td>
          <td>0.3043</td>
          <td>0.1786</td>
          <td>0.6818</td>
          <td>0.0005379</td>
          <td>0.0004724</td>
          <td>0.0001545</td>
          <td>646</td>
          <td>406</td>
          <td>45</td>
          <td>69</td>
          <td>9</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>11</td>
          <td>57</td>
          <td>95</td>
          <td>16801</td>
          <td>13444</td>
          <td>13032</td>
          <td>10715</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Diesel Men&#x27;s Shioner Skinny Straight Leg Jean</td>
          <td>Diesel</td>
          <td>Jeans</td>
          <td>295.98</td>
          <td>157.9</td>
          <td>1695.85</td>
          <td>779.71</td>
          <td>25</td>
          <td>6</td>
          <td>2</td>
          <td>3</td>
          <td>14</td>
          <td>1431.9</td>
          <td>657.85</td>
          <td>0.4598</td>
          <td>0.25</td>
          <td>0.2727</td>
          <td>0.12</td>
          <td>0.7</td>
          <td>0.0006282</td>
          <td>0.0005572</td>
          <td>0.0001379</td>
          <td>318</td>
          <td>201</td>
          <td>33</td>
          <td>50</td>
          <td>21</td>
          <td>84</td>
          <td>844</td>
          <td>526</td>
          <td>22</td>
          <td>56</td>
          <td>90</td>
          <td>16428</td>
          <td>11344</td>
          <td>14284</td>
          <td>15549</td>
          <td>12849</td>
        </tr>
        <tr>
          <td>True Religion Women&#x27;s Julie Super T Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>326.0</td>
          <td>172.13</td>
          <td>1956.0</td>
          <td>923.23</td>
          <td>8</td>
          <td>6</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>326.0</td>
          <td>153.87</td>
          <td>0.472</td>
          <td>0.0</td>
          <td>0.8571</td>
          <td>0.125</td>
          <td>0.1429</td>
          <td>0.0007246</td>
          <td>0.0006598</td>
          <td>4.41e-05</td>
          <td>233</td>
          <td>145</td>
          <td>19</td>
          <td>31</td>
          <td>5507</td>
          <td>84</td>
          <td>13463</td>
          <td>7029</td>
          <td>23197</td>
          <td>1487</td>
          <td>1788</td>
          <td>15335</td>
          <td>13463</td>
          <td>546</td>
          <td>14338</td>
          <td>27121</td>
        </tr>
        <tr>
          <td>Quiksilver Men&#x27;s Rockefeller Walkshort</td>
          <td>Quiksilver</td>
          <td>Shorts</td>
          <td>903.0</td>
          <td>472.27</td>
          <td>1806.0</td>
          <td>861.46</td>
          <td>6</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>4</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.477</td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>0.000669</td>
          <td>0.0006157</td>
          <td>3.31e-05</td>
          <td>5</td>
          <td>7</td>
          <td>21</td>
          <td>34</td>
          <td>12532</td>
          <td>6114</td>
          <td>13463</td>
          <td>17458</td>
          <td>6105</td>
          <td>22642</td>
          <td>22642</td>
          <td>14881</td>
          <td>13463</td>
          <td>9747</td>
          <td>17458</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>7 For All Mankind Men&#x27;s Standard Classic Straight Leg Jean</td>
          <td>7 For All Mankind</td>
          <td>Jeans</td>
          <td>157.45</td>
          <td>80.97</td>
          <td>1435.0</td>
          <td>696.01</td>
          <td>42</td>
          <td>9</td>
          <td>5</td>
          <td>5</td>
          <td>23</td>
          <td>1673.0</td>
          <td>844.04</td>
          <td>0.485</td>
          <td>0.3571</td>
          <td>0.2432</td>
          <td>0.119</td>
          <td>0.7188</td>
          <td>0.0005316</td>
          <td>0.0004974</td>
          <td>0.0002317</td>
          <td>1798</td>
          <td>1488</td>
          <td>46</td>
          <td>60</td>
          <td>2</td>
          <td>5</td>
          <td>5</td>
          <td>24</td>
          <td>2</td>
          <td>32</td>
          <td>41</td>
          <td>14028</td>
          <td>8749</td>
          <td>17091</td>
          <td>15552</td>
          <td>12034</td>
        </tr>
        <tr>
          <td>AIR JORDAN DOMINATE SHORTS MENS 465071-100</td>
          <td>Jordan</td>
          <td>Shorts</td>
          <td>903.0</td>
          <td>454.21</td>
          <td>2709.0</td>
          <td>1346.37</td>
          <td>5</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>2</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.497</td>
          <td>0.0</td>
          <td>0.6</td>
          <td>0.0</td>
          <td>0.4</td>
          <td>0.0010035</td>
          <td>0.0009622</td>
          <td>2.76e-05</td>
          <td>5</td>
          <td>8</td>
          <td>7</td>
          <td>9</td>
          <td>16887</td>
          <td>2358</td>
          <td>13463</td>
          <td>17458</td>
          <td>17069</td>
          <td>22642</td>
          <td>22642</td>
          <td>12874</td>
          <td>13463</td>
          <td>2189</td>
          <td>17458</td>
          <td>23875</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Expedition Parka</td>
          <td>Canada Goose</td>
          <td>Outerwear &amp; Coats</td>
          <td>795.0</td>
          <td>395.91</td>
          <td>2385.0</td>
          <td>1197.27</td>
          <td>4</td>
          <td>3</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>795.0</td>
          <td>399.09</td>
          <td>0.502</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.25</td>
          <td>0.0</td>
          <td>0.0008835</td>
          <td>0.0008557</td>
          <td>2.21e-05</td>
          <td>33</td>
          <td>19</td>
          <td>10</td>
          <td>13</td>
          <td>21053</td>
          <td>2358</td>
          <td>13463</td>
          <td>7029</td>
          <td>27145</td>
          <td>230</td>
          <td>277</td>
          <td>12357</td>
          <td>13463</td>
          <td>1</td>
          <td>5542</td>
          <td>27145</td>
        </tr>
        <tr>
          <td>Arc&#x27;teryx Moray Jacket - Women&#x27;s</td>
          <td>Arc&#x27;teryx</td>
          <td>Outerwear &amp; Coats</td>
          <td>699.0</td>
          <td>343.91</td>
          <td>2097.0</td>
          <td>1065.28</td>
          <td>9</td>
          <td>3</td>
          <td>0</td>
          <td>3</td>
          <td>3</td>
          <td>2097.0</td>
          <td>1065.28</td>
          <td>0.508</td>
          <td>0.0</td>
          <td>0.5</td>
          <td>0.3333</td>
          <td>0.5</td>
          <td>0.0007768</td>
          <td>0.0007613</td>
          <td>4.96e-05</td>
          <td>41</td>
          <td>36</td>
          <td>15</td>
          <td>20</td>
          <td>3355</td>
          <td>2358</td>
          <td>13463</td>
          <td>526</td>
          <td>10869</td>
          <td>11</td>
          <td>22</td>
          <td>11720</td>
          <td>13463</td>
          <td>3269</td>
          <td>2619</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>Barbour Sapper Jacket</td>
          <td>Barbour</td>
          <td>Outerwear &amp; Coats</td>
          <td>429.0</td>
          <td>210.21</td>
          <td>2145.0</td>
          <td>1093.95</td>
          <td>10</td>
          <td>5</td>
          <td>1</td>
          <td>1</td>
          <td>3</td>
          <td>858.0</td>
          <td>437.58</td>
          <td>0.51</td>
          <td>0.1667</td>
          <td>0.5556</td>
          <td>0.1</td>
          <td>0.375</td>
          <td>0.0007946</td>
          <td>0.0007818</td>
          <td>5.52e-05</td>
          <td>94</td>
          <td>81</td>
          <td>14</td>
          <td>18</td>
          <td>1962</td>
          <td>251</td>
          <td>3978</td>
          <td>7029</td>
          <td>10869</td>
          <td>185</td>
          <td>233</td>
          <td>11510</td>
          <td>13196</td>
          <td>3151</td>
          <td>16366</td>
          <td>24717</td>
        </tr>
        <tr>
          <td>Women&#x27;s Knee Length Overcoat in Pure Cashmere</td>
          <td>Cashmere Boutique</td>
          <td>Outerwear &amp; Coats</td>
          <td>399.0</td>
          <td>193.12</td>
          <td>1596.0</td>
          <td>814.76</td>
          <td>9</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>5</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.5105</td>
          <td>0.0</td>
          <td>0.4444</td>
          <td>0.0</td>
          <td>0.5556</td>
          <td>0.0005912</td>
          <td>0.0005823</td>
          <td>4.96e-05</td>
          <td>115</td>
          <td>100</td>
          <td>35</td>
          <td>40</td>
          <td>3355</td>
          <td>776</td>
          <td>13463</td>
          <td>17458</td>
          <td>3026</td>
          <td>22642</td>
          <td>22642</td>
          <td>11502</td>
          <td>13463</td>
          <td>6492</td>
          <td>17458</td>
          <td>19270</td>
        </tr>
        <tr>
          <td>Barbour Classic Beaufort Jacket / Beaufort Jacket</td>
          <td>Barbour</td>
          <td>Outerwear &amp; Coats</td>
          <td>399.0</td>
          <td>193.91</td>
          <td>1596.0</td>
          <td>820.34</td>
          <td>10</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>5</td>
          <td>399.0</td>
          <td>205.09</td>
          <td>0.514</td>
          <td>0.0</td>
          <td>0.4444</td>
          <td>0.1</td>
          <td>0.5556</td>
          <td>0.0005912</td>
          <td>0.0005863</td>
          <td>5.52e-05</td>
          <td>115</td>
          <td>98</td>
          <td>35</td>
          <td>38</td>
          <td>1962</td>
          <td>776</td>
          <td>13463</td>
          <td>7029</td>
          <td>3026</td>
          <td>985</td>
          <td>1084</td>
          <td>11041</td>
          <td>13463</td>
          <td>6492</td>
          <td>16366</td>
          <td>19270</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by Unit Orders</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Ulla Popken Plus Size Sequined Swing Jacket</td>
          <td>Ulla Popken</td>
          <td>Blazers &amp; Jackets</td>
          <td>169.0</td>
          <td>62.7</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>169.0</td>
          <td>106.3</td>
          <td></td>
          <td></td>
          <td></td>
          <td>1.0</td>
          <td></td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5.5e-06</td>
          <td>1446</td>
          <td>2577</td>
          <td>22532</td>
          <td>22532</td>
          <td>27983</td>
          <td>22532</td>
          <td>13463</td>
          <td>7029</td>
          <td>27145</td>
          <td>4331</td>
          <td>3178</td>
          <td>22532</td>
          <td>25326</td>
          <td>28303</td>
          <td>1</td>
          <td>28172</td>
        </tr>
        <tr>
          <td>Carhartt Women&#x27;s Wylie Flannel Hoodie</td>
          <td>Carhartt</td>
          <td>Fashion Hoodies &amp; Sweatshirts</td>
          <td>59.95</td>
          <td>27.76</td>
          <td>59.95</td>
          <td>32.19</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.5369</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.22e-05</td>
          <td>2.3e-05</td>
          <td>5.5e-06</td>
          <td>8808</td>
          <td>9607</td>
          <td>12711</td>
          <td>12060</td>
          <td>27983</td>
          <td>13264</td>
          <td>13463</td>
          <td>17458</td>
          <td>27145</td>
          <td>22642</td>
          <td>22642</td>
          <td>8960</td>
          <td>13463</td>
          <td>1</td>
          <td>17458</td>
          <td>27145</td>
        </tr>
        <tr>
          <td>Lucky Brand Mens 361 Vintage Straight Leg Jean</td>
          <td>Lucky Brand</td>
          <td>Jeans</td>
          <td>61.99</td>
          <td>35.27</td>
          <td>61.99</td>
          <td>26.72</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.431</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>2.3e-05</td>
          <td>1.91e-05</td>
          <td>5.5e-06</td>
          <td>8368</td>
          <td>6768</td>
          <td>12308</td>
          <td>13690</td>
          <td>27983</td>
          <td>13264</td>
          <td>13463</td>
          <td>17458</td>
          <td>27145</td>
          <td>22642</td>
          <td>22642</td>
          <td>18935</td>
          <td>13463</td>
          <td>1</td>
          <td>17458</td>
          <td>27145</td>
        </tr>
        <tr>
          <td>Solid Series Silk Scarves</td>
          <td>Wolfmark</td>
          <td>Accessories</td>
          <td>18.0</td>
          <td>7.56</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0.0</td>
          <td>0.0</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5.5e-06</td>
          <td>23512</td>
          <td>24629</td>
          <td>22532</td>
          <td>22532</td>
          <td>27983</td>
          <td>22532</td>
          <td>13463</td>
          <td>17458</td>
          <td>23197</td>
          <td>22642</td>
          <td>22642</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Bottoms Out - Mens Microfleece Lounge Pant Burgundy 23439</td>
          <td>Bottoms Out</td>
          <td>Sleep &amp; Lounge</td>
          <td>13.75</td>
          <td>5.71</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0.0</td>
          <td>0.0</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5.5e-06</td>
          <td>25545</td>
          <td>26326</td>
          <td>22532</td>
          <td>22532</td>
          <td>27983</td>
          <td>22532</td>
          <td>13463</td>
          <td>17458</td>
          <td>23197</td>
          <td>22642</td>
          <td>22642</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Acid Wash Jean Dark Leggings</td>
          <td>Yelete</td>
          <td>Leggings</td>
          <td>15.99</td>
          <td>9.35</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>15.99</td>
          <td>6.64</td>
          <td></td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td></td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5.5e-06</td>
          <td>24393</td>
          <td>23040</td>
          <td>22532</td>
          <td>22532</td>
          <td>27983</td>
          <td>22532</td>
          <td>3978</td>
          <td>17458</td>
          <td>27145</td>
          <td>21199</td>
          <td>21673</td>
          <td>22532</td>
          <td>1</td>
          <td>22532</td>
          <td>17458</td>
          <td>28172</td>
        </tr>
        <tr>
          <td>Corset-story WT-066 waist training corset</td>
          <td>Corset-story</td>
          <td>Intimates</td>
          <td>100.0</td>
          <td>54.1</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0.0</td>
          <td>0.0</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5.5e-06</td>
          <td>3867</td>
          <td>3383</td>
          <td>22532</td>
          <td>22532</td>
          <td>27983</td>
          <td>22532</td>
          <td>13463</td>
          <td>17458</td>
          <td>23197</td>
          <td>22642</td>
          <td>22642</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
        <tr>
          <td>prAna Women&#x27;s Diva Vest</td>
          <td>prAna</td>
          <td>Active</td>
          <td>119.0</td>
          <td>51.53</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0.0</td>
          <td>0.0</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5.5e-06</td>
          <td>3169</td>
          <td>3649</td>
          <td>22532</td>
          <td>22532</td>
          <td>27983</td>
          <td>22532</td>
          <td>13463</td>
          <td>17458</td>
          <td>23197</td>
          <td>22642</td>
          <td>22642</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
        <tr>
          <td>adidas Women&#x27;s Pursuit Pant</td>
          <td>adidas</td>
          <td>Active</td>
          <td>50.0</td>
          <td>18.65</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>50.0</td>
          <td>31.35</td>
          <td></td>
          <td></td>
          <td></td>
          <td>1.0</td>
          <td></td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5.5e-06</td>
          <td>10696</td>
          <td>14839</td>
          <td>22532</td>
          <td>22532</td>
          <td>27983</td>
          <td>22532</td>
          <td>13463</td>
          <td>7029</td>
          <td>27145</td>
          <td>14018</td>
          <td>12300</td>
          <td>22532</td>
          <td>25326</td>
          <td>28303</td>
          <td>1</td>
          <td>28172</td>
        </tr>
        <tr>
          <td>Volcom Juniors Frochickie 2 1/2 Inch Plain Front Short</td>
          <td>Volcom</td>
          <td>Shorts</td>
          <td>39.5</td>
          <td>21.17</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0.0</td>
          <td>0.0</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5.5e-06</td>
          <td>14466</td>
          <td>13153</td>
          <td>22532</td>
          <td>22532</td>
          <td>27983</td>
          <td>22532</td>
          <td>13463</td>
          <td>17458</td>
          <td>23197</td>
          <td>22642</td>
          <td>22642</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Nautica Mens 3 Pack Performance Casual Crew Track Socks</td>
          <td>Nautica</td>
          <td>Socks</td>
          <td>14.4</td>
          <td>8.12</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0.0</td>
          <td>0.0</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5.5e-06</td>
          <td>25223</td>
          <td>24070</td>
          <td>22532</td>
          <td>22532</td>
          <td>27983</td>
          <td>22532</td>
          <td>13463</td>
          <td>17458</td>
          <td>23197</td>
          <td>22642</td>
          <td>22642</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
        <tr>
          <td>TAUPE PALAZZO PANT SPLIT SKIRT GAUCHO - FITS (ONE SIZE) - L XL 1X 2X - U652S - LOTUSTRADERS</td>
          <td>LOTUSTRADERS</td>
          <td>Pants &amp; Capris</td>
          <td>42.99</td>
          <td>21.92</td>
          <td>42.99</td>
          <td>21.07</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.4901</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.59e-05</td>
          <td>1.51e-05</td>
          <td>5.5e-06</td>
          <td>13180</td>
          <td>12697</td>
          <td>15536</td>
          <td>15631</td>
          <td>27983</td>
          <td>13264</td>
          <td>13463</td>
          <td>17458</td>
          <td>27145</td>
          <td>22642</td>
          <td>22642</td>
          <td>13507</td>
          <td>13463</td>
          <td>1</td>
          <td>17458</td>
          <td>27145</td>
        </tr>
        <tr>
          <td>Arena Men&#x27;s Satamis Race Xtra Life Lycra Solid Brief Swimsuit</td>
          <td>Arena</td>
          <td>Swim</td>
          <td>24.95</td>
          <td>15.17</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0.0</td>
          <td>0.0</td>
          <td></td>
          <td></td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5.5e-06</td>
          <td>21005</td>
          <td>17618</td>
          <td>22532</td>
          <td>22532</td>
          <td>27983</td>
          <td>22532</td>
          <td>13463</td>
          <td>17458</td>
          <td>23197</td>
          <td>22642</td>
          <td>22642</td>
          <td>22532</td>
          <td>25326</td>
          <td>22532</td>
          <td>17458</td>
          <td>1</td>
        </tr>
        <tr>
          <td>Le Suit Safari Nights Jacket Dress</td>
          <td>Le Suit</td>
          <td>Suits</td>
          <td>141.62</td>
          <td>83.84</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>141.62</td>
          <td>57.78</td>
          <td></td>
          <td></td>
          <td></td>
          <td>1.0</td>
          <td></td>
          <td>0.0</td>
          <td>0.0</td>
          <td>5.5e-06</td>
          <td>2207</td>
          <td>1356</td>
          <td>22532</td>
          <td>22532</td>
          <td>27983</td>
          <td>22532</td>
          <td>13463</td>
          <td>7029</td>
          <td>27145</td>
          <td>5534</td>
          <td>7190</td>
          <td>22532</td>
          <td>25326</td>
          <td>28303</td>
          <td>1</td>
          <td>28172</td>
        </tr>
        <tr>
          <td>Trina Turk Women&#x27;s Pasha Pant</td>
          <td>Trina Turk</td>
          <td>Pants &amp; Capris</td>
          <td>288.0</td>
          <td>162.72</td>
          <td>288.0</td>
          <td>125.28</td>
          <td>1</td>
          <td>1</td>
          <td>0</td>
          <td>0</td>
          <td>0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.435</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.0001067</td>
          <td>8.95e-05</td>
          <td>5.5e-06</td>
          <td>338</td>
          <td>178</td>
          <td>1925</td>
          <td>2574</td>
          <td>27983</td>
          <td>13264</td>
          <td>13463</td>
          <td>17458</td>
          <td>27145</td>
          <td>22642</td>
          <td>22642</td>
          <td>18613</td>
          <td>13463</td>
          <td>1</td>
          <td>17458</td>
          <td>27145</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by Average Sale Price</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
  avg_product_sale_price_rank DESC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>HUGO BOSS Men&#x27;s Bright Argyle Crew Sock</td>
          <td>HUGO BOSS</td>
          <td>Socks</td>
          <td>9.75</td>
          <td>5.68</td>
          <td>39.0</td>
          <td>15.65</td>
          <td>22</td>
          <td>4</td>
          <td>4</td>
          <td>4</td>
          <td>10</td>
          <td>78.0</td>
          <td>32.25</td>
          <td>0.4013</td>
          <td>0.5</td>
          <td>0.2222</td>
          <td>0.1818</td>
          <td>0.7143</td>
          <td>1.44e-05</td>
          <td>1.12e-05</td>
          <td>0.0001214</td>
          <td>27342</td>
          <td>26355</td>
          <td>16327</td>
          <td>17765</td>
          <td>43</td>
          <td>776</td>
          <td>30</td>
          <td>126</td>
          <td>77</td>
          <td>10368</td>
          <td>12068</td>
          <td>20837</td>
          <td>4275</td>
          <td>17122</td>
          <td>10468</td>
          <td>12035</td>
        </tr>
        <tr>
          <td>Puma Men&#x27;s Socks</td>
          <td>PUMA</td>
          <td>Socks</td>
          <td>13.0</td>
          <td>7.78</td>
          <td>90.0</td>
          <td>35.98</td>
          <td>24</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>11</td>
          <td>78.0</td>
          <td>31.36</td>
          <td>0.3998</td>
          <td>0.125</td>
          <td>0.3684</td>
          <td>0.2083</td>
          <td>0.6111</td>
          <td>3.33e-05</td>
          <td>2.57e-05</td>
          <td>0.0001324</td>
          <td>25705</td>
          <td>24414</td>
          <td>8929</td>
          <td>11107</td>
          <td>30</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>43</td>
          <td>10368</td>
          <td>12295</td>
          <td>20955</td>
          <td>13444</td>
          <td>9637</td>
          <td>8433</td>
          <td>16951</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Striped Crew Sock</td>
          <td>HUGO BOSS</td>
          <td>Socks</td>
          <td>13.0</td>
          <td>8.14</td>
          <td>104.0</td>
          <td>40.17</td>
          <td>24</td>
          <td>8</td>
          <td>3</td>
          <td>4</td>
          <td>9</td>
          <td>91.0</td>
          <td>33.33</td>
          <td>0.3863</td>
          <td>0.2727</td>
          <td>0.4</td>
          <td>0.1667</td>
          <td>0.5294</td>
          <td>3.85e-05</td>
          <td>2.87e-05</td>
          <td>0.0001324</td>
          <td>25705</td>
          <td>24062</td>
          <td>7764</td>
          <td>10157</td>
          <td>30</td>
          <td>16</td>
          <td>151</td>
          <td>126</td>
          <td>140</td>
          <td>8958</td>
          <td>11794</td>
          <td>21483</td>
          <td>11342</td>
          <td>7482</td>
          <td>10731</td>
          <td>19498</td>
        </tr>
        <tr>
          <td>New Men&#x27;s Sexy Center Patch Bikini Swimsuit 3G by Gregg Homme</td>
          <td>Gregg Homme</td>
          <td>Swim</td>
          <td>13.22</td>
          <td>7.85</td>
          <td>54.6</td>
          <td>20.64</td>
          <td>25</td>
          <td>4</td>
          <td>2</td>
          <td>5</td>
          <td>14</td>
          <td>90.3</td>
          <td>38.29</td>
          <td>0.378</td>
          <td>0.3333</td>
          <td>0.2</td>
          <td>0.2</td>
          <td>0.7778</td>
          <td>2.02e-05</td>
          <td>1.48e-05</td>
          <td>0.0001379</td>
          <td>25672</td>
          <td>24345</td>
          <td>13422</td>
          <td>15782</td>
          <td>21</td>
          <td>776</td>
          <td>844</td>
          <td>24</td>
          <td>22</td>
          <td>8973</td>
          <td>10649</td>
          <td>21721</td>
          <td>8752</td>
          <td>17510</td>
          <td>8435</td>
          <td>9281</td>
        </tr>
        <tr>
          <td>Bottoms Out Men&#x27;s Plaid Sleep Pant</td>
          <td>Bottoms Out</td>
          <td>Sleep &amp; Lounge</td>
          <td>13.49</td>
          <td>5.05</td>
          <td>94.43</td>
          <td>59.4</td>
          <td>25</td>
          <td>7</td>
          <td>2</td>
          <td>4</td>
          <td>12</td>
          <td>80.94</td>
          <td>50.64</td>
          <td>0.629</td>
          <td>0.2222</td>
          <td>0.3333</td>
          <td>0.16</td>
          <td>0.6316</td>
          <td>3.5e-05</td>
          <td>4.25e-05</td>
          <td>0.0001379</td>
          <td>25625</td>
          <td>26913</td>
          <td>8758</td>
          <td>6904</td>
          <td>21</td>
          <td>33</td>
          <td>844</td>
          <td>126</td>
          <td>37</td>
          <td>9890</td>
          <td>8299</td>
          <td>839</td>
          <td>12628</td>
          <td>9747</td>
          <td>12630</td>
          <td>16546</td>
        </tr>
        <tr>
          <td>Kenneth Cole REACTION Men&#x27;s Passcase Wallet</td>
          <td>Kenneth Cole REACTION</td>
          <td>Accessories</td>
          <td>18.91</td>
          <td>7.72</td>
          <td>152.71</td>
          <td>89.4</td>
          <td>34</td>
          <td>8</td>
          <td>4</td>
          <td>4</td>
          <td>18</td>
          <td>150.85</td>
          <td>90.57</td>
          <td>0.5854</td>
          <td>0.3333</td>
          <td>0.2667</td>
          <td>0.1176</td>
          <td>0.6923</td>
          <td>5.66e-05</td>
          <td>6.39e-05</td>
          <td>0.0001876</td>
          <td>23389</td>
          <td>24481</td>
          <td>4958</td>
          <td>4188</td>
          <td>4</td>
          <td>16</td>
          <td>30</td>
          <td>126</td>
          <td>4</td>
          <td>5015</td>
          <td>4078</td>
          <td>3806</td>
          <td>8752</td>
          <td>14395</td>
          <td>15553</td>
          <td>12966</td>
        </tr>
        <tr>
          <td>Tommy Hilfiger Men Classic Fit T-shirt</td>
          <td>Tommy Hilfiger</td>
          <td>Tops &amp; Tees</td>
          <td>21.99</td>
          <td>12.22</td>
          <td>65.97</td>
          <td>28.41</td>
          <td>25</td>
          <td>3</td>
          <td>2</td>
          <td>5</td>
          <td>15</td>
          <td>153.93</td>
          <td>70.63</td>
          <td>0.4307</td>
          <td>0.4</td>
          <td>0.15</td>
          <td>0.2</td>
          <td>0.8333</td>
          <td>2.44e-05</td>
          <td>2.03e-05</td>
          <td>0.0001379</td>
          <td>22049</td>
          <td>20333</td>
          <td>11887</td>
          <td>13165</td>
          <td>21</td>
          <td>2358</td>
          <td>844</td>
          <td>24</td>
          <td>11</td>
          <td>4954</td>
          <td>5704</td>
          <td>18998</td>
          <td>8312</td>
          <td>20814</td>
          <td>8435</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>Diesel Men&#x27;s Blade Underpant</td>
          <td>Diesel</td>
          <td>Underwear</td>
          <td>22.14</td>
          <td>9.75</td>
          <td>122.0</td>
          <td>66.53</td>
          <td>22</td>
          <td>6</td>
          <td>0</td>
          <td>2</td>
          <td>14</td>
          <td>43.0</td>
          <td>23.83</td>
          <td>0.5453</td>
          <td>0.0</td>
          <td>0.3</td>
          <td>0.0909</td>
          <td>0.7</td>
          <td>4.52e-05</td>
          <td>4.75e-05</td>
          <td>0.0001214</td>
          <td>21886</td>
          <td>22702</td>
          <td>6504</td>
          <td>6114</td>
          <td>43</td>
          <td>84</td>
          <td>13463</td>
          <td>2100</td>
          <td>22</td>
          <td>15676</td>
          <td>14732</td>
          <td>8115</td>
          <td>13463</td>
          <td>13033</td>
          <td>16872</td>
          <td>12849</td>
        </tr>
        <tr>
          <td>Motherhood Maternity: Sports Clip Down Nursing Bra</td>
          <td>Motherhood Maternity</td>
          <td>Maternity</td>
          <td>22.54</td>
          <td>10.46</td>
          <td>200.82</td>
          <td>108.99</td>
          <td>25</td>
          <td>9</td>
          <td>2</td>
          <td>3</td>
          <td>11</td>
          <td>112.9</td>
          <td>60.37</td>
          <td>0.5427</td>
          <td>0.1818</td>
          <td>0.4091</td>
          <td>0.12</td>
          <td>0.55</td>
          <td>7.44e-05</td>
          <td>7.79e-05</td>
          <td>0.0001379</td>
          <td>21822</td>
          <td>22052</td>
          <td>3297</td>
          <td>3165</td>
          <td>21</td>
          <td>5</td>
          <td>844</td>
          <td>526</td>
          <td>43</td>
          <td>7249</td>
          <td>6811</td>
          <td>8373</td>
          <td>13193</td>
          <td>7481</td>
          <td>15549</td>
          <td>19449</td>
        </tr>
        <tr>
          <td>Hanes Men&#x27;s 4 Pack Boxer Brief</td>
          <td>Hanes</td>
          <td>Underwear</td>
          <td>25.0</td>
          <td>11.52</td>
          <td>250.0</td>
          <td>133.47</td>
          <td>28</td>
          <td>10</td>
          <td>2</td>
          <td>5</td>
          <td>11</td>
          <td>175.0</td>
          <td>92.77</td>
          <td>0.5339</td>
          <td>0.1667</td>
          <td>0.4348</td>
          <td>0.1786</td>
          <td>0.5238</td>
          <td>9.26e-05</td>
          <td>9.54e-05</td>
          <td>0.0001545</td>
          <td>19651</td>
          <td>20997</td>
          <td>2432</td>
          <td>2340</td>
          <td>9</td>
          <td>4</td>
          <td>844</td>
          <td>24</td>
          <td>43</td>
          <td>4152</td>
          <td>3935</td>
          <td>9232</td>
          <td>13196</td>
          <td>6738</td>
          <td>10715</td>
          <td>19500</td>
        </tr>
        <tr>
          <td>Bottoms Out Men&#x27;s Plaid Sleep Jam</td>
          <td>Bottoms Out</td>
          <td>Sleep &amp; Lounge</td>
          <td>25.0</td>
          <td>9.3</td>
          <td>125.0</td>
          <td>78.03</td>
          <td>24</td>
          <td>5</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>100.0</td>
          <td>63.2</td>
          <td>0.6242</td>
          <td>0.2857</td>
          <td>0.2273</td>
          <td>0.0833</td>
          <td>0.75</td>
          <td>4.63e-05</td>
          <td>5.58e-05</td>
          <td>0.0001324</td>
          <td>19651</td>
          <td>23078</td>
          <td>6364</td>
          <td>5026</td>
          <td>30</td>
          <td>251</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>7972</td>
          <td>6500</td>
          <td>1088</td>
          <td>11280</td>
          <td>17121</td>
          <td>17144</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>Michael Kors Men&#x27;s 3 Pack Brief</td>
          <td>Michael Kors</td>
          <td>Underwear</td>
          <td>25.99</td>
          <td>12.48</td>
          <td>130.46</td>
          <td>67.73</td>
          <td>24</td>
          <td>5</td>
          <td>5</td>
          <td>4</td>
          <td>10</td>
          <td>232.38</td>
          <td>120.98</td>
          <td>0.5192</td>
          <td>0.5</td>
          <td>0.25</td>
          <td>0.1667</td>
          <td>0.6667</td>
          <td>4.83e-05</td>
          <td>4.84e-05</td>
          <td>0.0001324</td>
          <td>19456</td>
          <td>20053</td>
          <td>6070</td>
          <td>5979</td>
          <td>30</td>
          <td>251</td>
          <td>5</td>
          <td>126</td>
          <td>77</td>
          <td>2705</td>
          <td>2646</td>
          <td>10469</td>
          <td>4275</td>
          <td>14408</td>
          <td>10731</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>State O Maine Big and Tall Solid Microfleece Lounge Pant</td>
          <td>KNOTHE CORP.</td>
          <td>Sleep &amp; Lounge</td>
          <td>26.99</td>
          <td>10.37</td>
          <td>161.94</td>
          <td>101.75</td>
          <td>24</td>
          <td>6</td>
          <td>2</td>
          <td>2</td>
          <td>14</td>
          <td>107.96</td>
          <td>69.2</td>
          <td>0.6283</td>
          <td>0.25</td>
          <td>0.2727</td>
          <td>0.0833</td>
          <td>0.7</td>
          <td>6e-05</td>
          <td>7.27e-05</td>
          <td>0.0001324</td>
          <td>19125</td>
          <td>22140</td>
          <td>4586</td>
          <td>3491</td>
          <td>30</td>
          <td>84</td>
          <td>844</td>
          <td>2100</td>
          <td>22</td>
          <td>7621</td>
          <td>5851</td>
          <td>878</td>
          <td>11344</td>
          <td>14284</td>
          <td>17144</td>
          <td>12849</td>
        </tr>
        <tr>
          <td>Volcom Juniors Pocket Blocket Long Sleeve Tee</td>
          <td>Volcom</td>
          <td>Tops &amp; Tees</td>
          <td>27.0</td>
          <td>15.34</td>
          <td>81.0</td>
          <td>33.86</td>
          <td>21</td>
          <td>3</td>
          <td>4</td>
          <td>5</td>
          <td>9</td>
          <td>243.0</td>
          <td>107.41</td>
          <td>0.418</td>
          <td>0.5714</td>
          <td>0.1875</td>
          <td>0.2381</td>
          <td>0.75</td>
          <td>3e-05</td>
          <td>2.42e-05</td>
          <td>0.0001158</td>
          <td>19072</td>
          <td>17500</td>
          <td>9846</td>
          <td>11622</td>
          <td>50</td>
          <td>2358</td>
          <td>30</td>
          <td>24</td>
          <td>140</td>
          <td>2456</td>
          <td>3131</td>
          <td>20016</td>
          <td>4252</td>
          <td>19354</td>
          <td>7773</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>JiMarti JM01 Sunglasses for Golf Fishing Cycling-Unbreakable-... Frame</td>
          <td>JiMarti</td>
          <td>Accessories</td>
          <td>29.95</td>
          <td>11.92</td>
          <td>269.55</td>
          <td>161.1</td>
          <td>22</td>
          <td>9</td>
          <td>2</td>
          <td>2</td>
          <td>9</td>
          <td>119.8</td>
          <td>72.12</td>
          <td>0.5977</td>
          <td>0.1818</td>
          <td>0.45</td>
          <td>0.0909</td>
          <td>0.5</td>
          <td>9.99e-05</td>
          <td>0.0001151</td>
          <td>0.0001214</td>
          <td>18166</td>
          <td>20613</td>
          <td>2175</td>
          <td>1707</td>
          <td>43</td>
          <td>5</td>
          <td>844</td>
          <td>2100</td>
          <td>140</td>
          <td>6868</td>
          <td>5540</td>
          <td>2758</td>
          <td>13193</td>
          <td>6490</td>
          <td>16872</td>
          <td>19501</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by Average Cost</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
  avg_product_cost_rank DESC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Bottoms Out Men&#x27;s Plaid Sleep Pant</td>
          <td>Bottoms Out</td>
          <td>Sleep &amp; Lounge</td>
          <td>13.49</td>
          <td>5.05</td>
          <td>94.43</td>
          <td>59.4</td>
          <td>25</td>
          <td>7</td>
          <td>2</td>
          <td>4</td>
          <td>12</td>
          <td>80.94</td>
          <td>50.64</td>
          <td>0.629</td>
          <td>0.2222</td>
          <td>0.3333</td>
          <td>0.16</td>
          <td>0.6316</td>
          <td>3.5e-05</td>
          <td>4.25e-05</td>
          <td>0.0001379</td>
          <td>25625</td>
          <td>26913</td>
          <td>8758</td>
          <td>6904</td>
          <td>21</td>
          <td>33</td>
          <td>844</td>
          <td>126</td>
          <td>37</td>
          <td>9890</td>
          <td>8299</td>
          <td>839</td>
          <td>12628</td>
          <td>9747</td>
          <td>12630</td>
          <td>16546</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Bright Argyle Crew Sock</td>
          <td>HUGO BOSS</td>
          <td>Socks</td>
          <td>9.75</td>
          <td>5.68</td>
          <td>39.0</td>
          <td>15.65</td>
          <td>22</td>
          <td>4</td>
          <td>4</td>
          <td>4</td>
          <td>10</td>
          <td>78.0</td>
          <td>32.25</td>
          <td>0.4013</td>
          <td>0.5</td>
          <td>0.2222</td>
          <td>0.1818</td>
          <td>0.7143</td>
          <td>1.44e-05</td>
          <td>1.12e-05</td>
          <td>0.0001214</td>
          <td>27342</td>
          <td>26355</td>
          <td>16327</td>
          <td>17765</td>
          <td>43</td>
          <td>776</td>
          <td>30</td>
          <td>126</td>
          <td>77</td>
          <td>10368</td>
          <td>12068</td>
          <td>20837</td>
          <td>4275</td>
          <td>17122</td>
          <td>10468</td>
          <td>12035</td>
        </tr>
        <tr>
          <td>Kenneth Cole REACTION Men&#x27;s Passcase Wallet</td>
          <td>Kenneth Cole REACTION</td>
          <td>Accessories</td>
          <td>18.91</td>
          <td>7.72</td>
          <td>152.71</td>
          <td>89.4</td>
          <td>34</td>
          <td>8</td>
          <td>4</td>
          <td>4</td>
          <td>18</td>
          <td>150.85</td>
          <td>90.57</td>
          <td>0.5854</td>
          <td>0.3333</td>
          <td>0.2667</td>
          <td>0.1176</td>
          <td>0.6923</td>
          <td>5.66e-05</td>
          <td>6.39e-05</td>
          <td>0.0001876</td>
          <td>23389</td>
          <td>24481</td>
          <td>4958</td>
          <td>4188</td>
          <td>4</td>
          <td>16</td>
          <td>30</td>
          <td>126</td>
          <td>4</td>
          <td>5015</td>
          <td>4078</td>
          <td>3806</td>
          <td>8752</td>
          <td>14395</td>
          <td>15553</td>
          <td>12966</td>
        </tr>
        <tr>
          <td>Puma Men&#x27;s Socks</td>
          <td>PUMA</td>
          <td>Socks</td>
          <td>13.0</td>
          <td>7.78</td>
          <td>90.0</td>
          <td>35.98</td>
          <td>24</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>11</td>
          <td>78.0</td>
          <td>31.36</td>
          <td>0.3998</td>
          <td>0.125</td>
          <td>0.3684</td>
          <td>0.2083</td>
          <td>0.6111</td>
          <td>3.33e-05</td>
          <td>2.57e-05</td>
          <td>0.0001324</td>
          <td>25705</td>
          <td>24414</td>
          <td>8929</td>
          <td>11107</td>
          <td>30</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>43</td>
          <td>10368</td>
          <td>12295</td>
          <td>20955</td>
          <td>13444</td>
          <td>9637</td>
          <td>8433</td>
          <td>16951</td>
        </tr>
        <tr>
          <td>New Men&#x27;s Sexy Center Patch Bikini Swimsuit 3G by Gregg Homme</td>
          <td>Gregg Homme</td>
          <td>Swim</td>
          <td>13.22</td>
          <td>7.85</td>
          <td>54.6</td>
          <td>20.64</td>
          <td>25</td>
          <td>4</td>
          <td>2</td>
          <td>5</td>
          <td>14</td>
          <td>90.3</td>
          <td>38.29</td>
          <td>0.378</td>
          <td>0.3333</td>
          <td>0.2</td>
          <td>0.2</td>
          <td>0.7778</td>
          <td>2.02e-05</td>
          <td>1.48e-05</td>
          <td>0.0001379</td>
          <td>25672</td>
          <td>24345</td>
          <td>13422</td>
          <td>15782</td>
          <td>21</td>
          <td>776</td>
          <td>844</td>
          <td>24</td>
          <td>22</td>
          <td>8973</td>
          <td>10649</td>
          <td>21721</td>
          <td>8752</td>
          <td>17510</td>
          <td>8435</td>
          <td>9281</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Striped Crew Sock</td>
          <td>HUGO BOSS</td>
          <td>Socks</td>
          <td>13.0</td>
          <td>8.14</td>
          <td>104.0</td>
          <td>40.17</td>
          <td>24</td>
          <td>8</td>
          <td>3</td>
          <td>4</td>
          <td>9</td>
          <td>91.0</td>
          <td>33.33</td>
          <td>0.3863</td>
          <td>0.2727</td>
          <td>0.4</td>
          <td>0.1667</td>
          <td>0.5294</td>
          <td>3.85e-05</td>
          <td>2.87e-05</td>
          <td>0.0001324</td>
          <td>25705</td>
          <td>24062</td>
          <td>7764</td>
          <td>10157</td>
          <td>30</td>
          <td>16</td>
          <td>151</td>
          <td>126</td>
          <td>140</td>
          <td>8958</td>
          <td>11794</td>
          <td>21483</td>
          <td>11342</td>
          <td>7482</td>
          <td>10731</td>
          <td>19498</td>
        </tr>
        <tr>
          <td>Bottoms Out Men&#x27;s Plaid Sleep Jam</td>
          <td>Bottoms Out</td>
          <td>Sleep &amp; Lounge</td>
          <td>25.0</td>
          <td>9.3</td>
          <td>125.0</td>
          <td>78.03</td>
          <td>24</td>
          <td>5</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>100.0</td>
          <td>63.2</td>
          <td>0.6242</td>
          <td>0.2857</td>
          <td>0.2273</td>
          <td>0.0833</td>
          <td>0.75</td>
          <td>4.63e-05</td>
          <td>5.58e-05</td>
          <td>0.0001324</td>
          <td>19651</td>
          <td>23078</td>
          <td>6364</td>
          <td>5026</td>
          <td>30</td>
          <td>251</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>7972</td>
          <td>6500</td>
          <td>1088</td>
          <td>11280</td>
          <td>17121</td>
          <td>17144</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>Diesel Men&#x27;s Blade Underpant</td>
          <td>Diesel</td>
          <td>Underwear</td>
          <td>22.14</td>
          <td>9.75</td>
          <td>122.0</td>
          <td>66.53</td>
          <td>22</td>
          <td>6</td>
          <td>0</td>
          <td>2</td>
          <td>14</td>
          <td>43.0</td>
          <td>23.83</td>
          <td>0.5453</td>
          <td>0.0</td>
          <td>0.3</td>
          <td>0.0909</td>
          <td>0.7</td>
          <td>4.52e-05</td>
          <td>4.75e-05</td>
          <td>0.0001214</td>
          <td>21886</td>
          <td>22702</td>
          <td>6504</td>
          <td>6114</td>
          <td>43</td>
          <td>84</td>
          <td>13463</td>
          <td>2100</td>
          <td>22</td>
          <td>15676</td>
          <td>14732</td>
          <td>8115</td>
          <td>13463</td>
          <td>13033</td>
          <td>16872</td>
          <td>12849</td>
        </tr>
        <tr>
          <td>State O Maine Big and Tall Solid Microfleece Lounge Pant</td>
          <td>KNOTHE CORP.</td>
          <td>Sleep &amp; Lounge</td>
          <td>26.99</td>
          <td>10.37</td>
          <td>161.94</td>
          <td>101.75</td>
          <td>24</td>
          <td>6</td>
          <td>2</td>
          <td>2</td>
          <td>14</td>
          <td>107.96</td>
          <td>69.2</td>
          <td>0.6283</td>
          <td>0.25</td>
          <td>0.2727</td>
          <td>0.0833</td>
          <td>0.7</td>
          <td>6e-05</td>
          <td>7.27e-05</td>
          <td>0.0001324</td>
          <td>19125</td>
          <td>22140</td>
          <td>4586</td>
          <td>3491</td>
          <td>30</td>
          <td>84</td>
          <td>844</td>
          <td>2100</td>
          <td>22</td>
          <td>7621</td>
          <td>5851</td>
          <td>878</td>
          <td>11344</td>
          <td>14284</td>
          <td>17144</td>
          <td>12849</td>
        </tr>
        <tr>
          <td>Motherhood Maternity: Sports Clip Down Nursing Bra</td>
          <td>Motherhood Maternity</td>
          <td>Maternity</td>
          <td>22.54</td>
          <td>10.46</td>
          <td>200.82</td>
          <td>108.99</td>
          <td>25</td>
          <td>9</td>
          <td>2</td>
          <td>3</td>
          <td>11</td>
          <td>112.9</td>
          <td>60.37</td>
          <td>0.5427</td>
          <td>0.1818</td>
          <td>0.4091</td>
          <td>0.12</td>
          <td>0.55</td>
          <td>7.44e-05</td>
          <td>7.79e-05</td>
          <td>0.0001379</td>
          <td>21822</td>
          <td>22052</td>
          <td>3297</td>
          <td>3165</td>
          <td>21</td>
          <td>5</td>
          <td>844</td>
          <td>526</td>
          <td>43</td>
          <td>7249</td>
          <td>6811</td>
          <td>8373</td>
          <td>13193</td>
          <td>7481</td>
          <td>15549</td>
          <td>19449</td>
        </tr>
        <tr>
          <td>Hanes Men&#x27;s 4 Pack Boxer Brief</td>
          <td>Hanes</td>
          <td>Underwear</td>
          <td>25.0</td>
          <td>11.52</td>
          <td>250.0</td>
          <td>133.47</td>
          <td>28</td>
          <td>10</td>
          <td>2</td>
          <td>5</td>
          <td>11</td>
          <td>175.0</td>
          <td>92.77</td>
          <td>0.5339</td>
          <td>0.1667</td>
          <td>0.4348</td>
          <td>0.1786</td>
          <td>0.5238</td>
          <td>9.26e-05</td>
          <td>9.54e-05</td>
          <td>0.0001545</td>
          <td>19651</td>
          <td>20997</td>
          <td>2432</td>
          <td>2340</td>
          <td>9</td>
          <td>4</td>
          <td>844</td>
          <td>24</td>
          <td>43</td>
          <td>4152</td>
          <td>3935</td>
          <td>9232</td>
          <td>13196</td>
          <td>6738</td>
          <td>10715</td>
          <td>19500</td>
        </tr>
        <tr>
          <td>JiMarti JM01 Sunglasses for Golf Fishing Cycling-Unbreakable-... Frame</td>
          <td>JiMarti</td>
          <td>Accessories</td>
          <td>29.95</td>
          <td>11.92</td>
          <td>269.55</td>
          <td>161.1</td>
          <td>22</td>
          <td>9</td>
          <td>2</td>
          <td>2</td>
          <td>9</td>
          <td>119.8</td>
          <td>72.12</td>
          <td>0.5977</td>
          <td>0.1818</td>
          <td>0.45</td>
          <td>0.0909</td>
          <td>0.5</td>
          <td>9.99e-05</td>
          <td>0.0001151</td>
          <td>0.0001214</td>
          <td>18166</td>
          <td>20613</td>
          <td>2175</td>
          <td>1707</td>
          <td>43</td>
          <td>5</td>
          <td>844</td>
          <td>2100</td>
          <td>140</td>
          <td>6868</td>
          <td>5540</td>
          <td>2758</td>
          <td>13193</td>
          <td>6490</td>
          <td>16872</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>Tommy Hilfiger Men Classic Fit T-shirt</td>
          <td>Tommy Hilfiger</td>
          <td>Tops &amp; Tees</td>
          <td>21.99</td>
          <td>12.22</td>
          <td>65.97</td>
          <td>28.41</td>
          <td>25</td>
          <td>3</td>
          <td>2</td>
          <td>5</td>
          <td>15</td>
          <td>153.93</td>
          <td>70.63</td>
          <td>0.4307</td>
          <td>0.4</td>
          <td>0.15</td>
          <td>0.2</td>
          <td>0.8333</td>
          <td>2.44e-05</td>
          <td>2.03e-05</td>
          <td>0.0001379</td>
          <td>22049</td>
          <td>20333</td>
          <td>11887</td>
          <td>13165</td>
          <td>21</td>
          <td>2358</td>
          <td>844</td>
          <td>24</td>
          <td>11</td>
          <td>4954</td>
          <td>5704</td>
          <td>18998</td>
          <td>8312</td>
          <td>20814</td>
          <td>8435</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>Michael Kors Men&#x27;s 3 Pack Brief</td>
          <td>Michael Kors</td>
          <td>Underwear</td>
          <td>25.99</td>
          <td>12.48</td>
          <td>130.46</td>
          <td>67.73</td>
          <td>24</td>
          <td>5</td>
          <td>5</td>
          <td>4</td>
          <td>10</td>
          <td>232.38</td>
          <td>120.98</td>
          <td>0.5192</td>
          <td>0.5</td>
          <td>0.25</td>
          <td>0.1667</td>
          <td>0.6667</td>
          <td>4.83e-05</td>
          <td>4.84e-05</td>
          <td>0.0001324</td>
          <td>19456</td>
          <td>20053</td>
          <td>6070</td>
          <td>5979</td>
          <td>30</td>
          <td>251</td>
          <td>5</td>
          <td>126</td>
          <td>77</td>
          <td>2705</td>
          <td>2646</td>
          <td>10469</td>
          <td>4275</td>
          <td>14408</td>
          <td>10731</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Volcom Juniors Pocket Blocket Long Sleeve Tee</td>
          <td>Volcom</td>
          <td>Tops &amp; Tees</td>
          <td>27.0</td>
          <td>15.34</td>
          <td>81.0</td>
          <td>33.86</td>
          <td>21</td>
          <td>3</td>
          <td>4</td>
          <td>5</td>
          <td>9</td>
          <td>243.0</td>
          <td>107.41</td>
          <td>0.418</td>
          <td>0.5714</td>
          <td>0.1875</td>
          <td>0.2381</td>
          <td>0.75</td>
          <td>3e-05</td>
          <td>2.42e-05</td>
          <td>0.0001158</td>
          <td>19072</td>
          <td>17500</td>
          <td>9846</td>
          <td>11622</td>
          <td>50</td>
          <td>2358</td>
          <td>30</td>
          <td>24</td>
          <td>140</td>
          <td>2456</td>
          <td>3131</td>
          <td>20016</td>
          <td>4252</td>
          <td>19354</td>
          <td>7773</td>
          <td>9487</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by Completion Rate</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
  completion_rate_rank DESC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Kenneth Cole Men&#x27;s Straight Leg Jean</td>
          <td>Kenneth Cole</td>
          <td>Jeans</td>
          <td>54.25</td>
          <td>27.11</td>
          <td>54.99</td>
          <td>26.89</td>
          <td>24</td>
          <td>1</td>
          <td>7</td>
          <td>4</td>
          <td>12</td>
          <td>632.25</td>
          <td>318.8</td>
          <td>0.489</td>
          <td>0.875</td>
          <td>0.05</td>
          <td>0.1667</td>
          <td>0.9231</td>
          <td>2.04e-05</td>
          <td>1.92e-05</td>
          <td>0.0001324</td>
          <td>10100</td>
          <td>9920</td>
          <td>13356</td>
          <td>13628</td>
          <td>30</td>
          <td>13264</td>
          <td>1</td>
          <td>126</td>
          <td>37</td>
          <td>380</td>
          <td>462</td>
          <td>13602</td>
          <td>2795</td>
          <td>22531</td>
          <td>10731</td>
          <td>5642</td>
        </tr>
        <tr>
          <td>Lilly Pulitzer Women&#x27;s Callahan Short</td>
          <td>Lilly Pulitzer</td>
          <td>Shorts</td>
          <td>48.24</td>
          <td>24.35</td>
          <td>106.11</td>
          <td>53.14</td>
          <td>24</td>
          <td>2</td>
          <td>4</td>
          <td>5</td>
          <td>13</td>
          <td>420.02</td>
          <td>207.44</td>
          <td>0.5008</td>
          <td>0.6667</td>
          <td>0.1053</td>
          <td>0.2083</td>
          <td>0.8667</td>
          <td>3.93e-05</td>
          <td>3.8e-05</td>
          <td>0.0001324</td>
          <td>11747</td>
          <td>11307</td>
          <td>7626</td>
          <td>7813</td>
          <td>30</td>
          <td>6114</td>
          <td>30</td>
          <td>24</td>
          <td>31</td>
          <td>883</td>
          <td>1063</td>
          <td>12538</td>
          <td>3055</td>
          <td>22368</td>
          <td>8433</td>
          <td>6056</td>
        </tr>
        <tr>
          <td>Dockers Men&#x27;s Suit Separate Coat</td>
          <td>Dockers</td>
          <td>Suits &amp; Sport Coats</td>
          <td>88.36</td>
          <td>33.97</td>
          <td>231.12</td>
          <td>140.98</td>
          <td>27</td>
          <td>3</td>
          <td>4</td>
          <td>2</td>
          <td>18</td>
          <td>542.11</td>
          <td>337.6</td>
          <td>0.61</td>
          <td>0.5714</td>
          <td>0.12</td>
          <td>0.0741</td>
          <td>0.8571</td>
          <td>8.56e-05</td>
          <td>0.0001008</td>
          <td>0.0001489</td>
          <td>5094</td>
          <td>7229</td>
          <td>2783</td>
          <td>2122</td>
          <td>12</td>
          <td>2358</td>
          <td>30</td>
          <td>2100</td>
          <td>4</td>
          <td>542</td>
          <td>391</td>
          <td>1873</td>
          <td>4252</td>
          <td>22129</td>
          <td>17370</td>
          <td>6057</td>
        </tr>
        <tr>
          <td>Tommy Hilfiger Men Classic Fit T-shirt</td>
          <td>Tommy Hilfiger</td>
          <td>Tops &amp; Tees</td>
          <td>21.99</td>
          <td>12.22</td>
          <td>65.97</td>
          <td>28.41</td>
          <td>25</td>
          <td>3</td>
          <td>2</td>
          <td>5</td>
          <td>15</td>
          <td>153.93</td>
          <td>70.63</td>
          <td>0.4307</td>
          <td>0.4</td>
          <td>0.15</td>
          <td>0.2</td>
          <td>0.8333</td>
          <td>2.44e-05</td>
          <td>2.03e-05</td>
          <td>0.0001379</td>
          <td>22049</td>
          <td>20333</td>
          <td>11887</td>
          <td>13165</td>
          <td>21</td>
          <td>2358</td>
          <td>844</td>
          <td>24</td>
          <td>11</td>
          <td>4954</td>
          <td>5704</td>
          <td>18998</td>
          <td>8312</td>
          <td>20814</td>
          <td>8435</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>246.88</td>
          <td>129.05</td>
          <td>1366.0</td>
          <td>666.07</td>
          <td>34</td>
          <td>5</td>
          <td>4</td>
          <td>3</td>
          <td>22</td>
          <td>1400.0</td>
          <td>654.5</td>
          <td>0.4876</td>
          <td>0.4444</td>
          <td>0.1613</td>
          <td>0.0882</td>
          <td>0.8148</td>
          <td>0.000506</td>
          <td>0.000476</td>
          <td>0.0001876</td>
          <td>534</td>
          <td>354</td>
          <td>56</td>
          <td>65</td>
          <td>4</td>
          <td>251</td>
          <td>30</td>
          <td>526</td>
          <td>3</td>
          <td>63</td>
          <td>92</td>
          <td>13792</td>
          <td>8264</td>
          <td>20804</td>
          <td>17143</td>
          <td>7595</td>
        </tr>
        <tr>
          <td>RSQ London Mens Skinny Jeans</td>
          <td>RSQ</td>
          <td>Jeans</td>
          <td>44.99</td>
          <td>24.2</td>
          <td>134.97</td>
          <td>63.21</td>
          <td>21</td>
          <td>3</td>
          <td>5</td>
          <td>3</td>
          <td>10</td>
          <td>359.92</td>
          <td>163.94</td>
          <td>0.4683</td>
          <td>0.625</td>
          <td>0.1667</td>
          <td>0.1429</td>
          <td>0.7692</td>
          <td>5e-05</td>
          <td>4.52e-05</td>
          <td>0.0001158</td>
          <td>12553</td>
          <td>11383</td>
          <td>5908</td>
          <td>6477</td>
          <td>50</td>
          <td>2358</td>
          <td>5</td>
          <td>526</td>
          <td>77</td>
          <td>1228</td>
          <td>1608</td>
          <td>15636</td>
          <td>4099</td>
          <td>19436</td>
          <td>12706</td>
          <td>9471</td>
        </tr>
        <tr>
          <td>Volcom Men&#x27;s Kinkade Jean</td>
          <td>Volcom</td>
          <td>Jeans</td>
          <td>66.67</td>
          <td>35.17</td>
          <td>269.9</td>
          <td>125.86</td>
          <td>27</td>
          <td>4</td>
          <td>3</td>
          <td>5</td>
          <td>15</td>
          <td>538.25</td>
          <td>254.63</td>
          <td>0.4663</td>
          <td>0.4286</td>
          <td>0.1818</td>
          <td>0.1852</td>
          <td>0.7895</td>
          <td>0.0001</td>
          <td>9e-05</td>
          <td>0.0001489</td>
          <td>7633</td>
          <td>6807</td>
          <td>2158</td>
          <td>2560</td>
          <td>12</td>
          <td>776</td>
          <td>151</td>
          <td>24</td>
          <td>11</td>
          <td>562</td>
          <td>723</td>
          <td>15806</td>
          <td>8270</td>
          <td>19358</td>
          <td>10467</td>
          <td>9273</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s 20X No. 33 Relaxed Straight Leg Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>55.0</td>
          <td>29.66</td>
          <td>220.0</td>
          <td>100.87</td>
          <td>24</td>
          <td>4</td>
          <td>1</td>
          <td>2</td>
          <td>17</td>
          <td>165.0</td>
          <td>74.2</td>
          <td>0.4585</td>
          <td>0.2</td>
          <td>0.1818</td>
          <td>0.0833</td>
          <td>0.8095</td>
          <td>8.15e-05</td>
          <td>7.21e-05</td>
          <td>0.0001324</td>
          <td>9673</td>
          <td>8784</td>
          <td>2941</td>
          <td>3526</td>
          <td>30</td>
          <td>776</td>
          <td>3978</td>
          <td>2100</td>
          <td>6</td>
          <td>4449</td>
          <td>5375</td>
          <td>16533</td>
          <td>12637</td>
          <td>19358</td>
          <td>17144</td>
          <td>7597</td>
        </tr>
        <tr>
          <td>Volcom Juniors Pocket Blocket Long Sleeve Tee</td>
          <td>Volcom</td>
          <td>Tops &amp; Tees</td>
          <td>27.0</td>
          <td>15.34</td>
          <td>81.0</td>
          <td>33.86</td>
          <td>21</td>
          <td>3</td>
          <td>4</td>
          <td>5</td>
          <td>9</td>
          <td>243.0</td>
          <td>107.41</td>
          <td>0.418</td>
          <td>0.5714</td>
          <td>0.1875</td>
          <td>0.2381</td>
          <td>0.75</td>
          <td>3e-05</td>
          <td>2.42e-05</td>
          <td>0.0001158</td>
          <td>19072</td>
          <td>17500</td>
          <td>9846</td>
          <td>11622</td>
          <td>50</td>
          <td>2358</td>
          <td>30</td>
          <td>24</td>
          <td>140</td>
          <td>2456</td>
          <td>3131</td>
          <td>20016</td>
          <td>4252</td>
          <td>19354</td>
          <td>7773</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>RUDE Dark Vintage Skinny Jeans</td>
          <td>Hot Topic</td>
          <td>Jeans</td>
          <td>36.5</td>
          <td>19.33</td>
          <td>146.0</td>
          <td>68.99</td>
          <td>24</td>
          <td>4</td>
          <td>4</td>
          <td>3</td>
          <td>13</td>
          <td>255.5</td>
          <td>123.41</td>
          <td>0.4725</td>
          <td>0.5</td>
          <td>0.1905</td>
          <td>0.125</td>
          <td>0.7647</td>
          <td>5.41e-05</td>
          <td>4.93e-05</td>
          <td>0.0001324</td>
          <td>15396</td>
          <td>14389</td>
          <td>5357</td>
          <td>5845</td>
          <td>30</td>
          <td>776</td>
          <td>30</td>
          <td>526</td>
          <td>31</td>
          <td>2306</td>
          <td>2570</td>
          <td>15319</td>
          <td>4275</td>
          <td>19353</td>
          <td>14338</td>
          <td>9484</td>
        </tr>
        <tr>
          <td>New Men&#x27;s Sexy Center Patch Bikini Swimsuit 3G by Gregg Homme</td>
          <td>Gregg Homme</td>
          <td>Swim</td>
          <td>13.22</td>
          <td>7.85</td>
          <td>54.6</td>
          <td>20.64</td>
          <td>25</td>
          <td>4</td>
          <td>2</td>
          <td>5</td>
          <td>14</td>
          <td>90.3</td>
          <td>38.29</td>
          <td>0.378</td>
          <td>0.3333</td>
          <td>0.2</td>
          <td>0.2</td>
          <td>0.7778</td>
          <td>2.02e-05</td>
          <td>1.48e-05</td>
          <td>0.0001379</td>
          <td>25672</td>
          <td>24345</td>
          <td>13422</td>
          <td>15782</td>
          <td>21</td>
          <td>776</td>
          <td>844</td>
          <td>24</td>
          <td>22</td>
          <td>8973</td>
          <td>10649</td>
          <td>21721</td>
          <td>8752</td>
          <td>17510</td>
          <td>8435</td>
          <td>9281</td>
        </tr>
        <tr>
          <td>Levi&#x27;s Men&#x27;s Wool Melton Peacoat</td>
          <td>Levi&#x27;s</td>
          <td>Outerwear &amp; Coats</td>
          <td>103.99</td>
          <td>47.71</td>
          <td>415.98</td>
          <td>225.14</td>
          <td>22</td>
          <td>4</td>
          <td>3</td>
          <td>3</td>
          <td>12</td>
          <td>623.97</td>
          <td>337.71</td>
          <td>0.5412</td>
          <td>0.4286</td>
          <td>0.2105</td>
          <td>0.1364</td>
          <td>0.75</td>
          <td>0.0001541</td>
          <td>0.0001609</td>
          <td>0.0001214</td>
          <td>3776</td>
          <td>4133</td>
          <td>937</td>
          <td>912</td>
          <td>43</td>
          <td>776</td>
          <td>151</td>
          <td>526</td>
          <td>37</td>
          <td>393</td>
          <td>389</td>
          <td>8481</td>
          <td>8270</td>
          <td>17508</td>
          <td>14315</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>Nike Classic Fleece Hooded Top</td>
          <td>Nike</td>
          <td>Active</td>
          <td>40.62</td>
          <td>16.88</td>
          <td>161.76</td>
          <td>98.38</td>
          <td>21</td>
          <td>4</td>
          <td>2</td>
          <td>2</td>
          <td>13</td>
          <td>162.86</td>
          <td>91.16</td>
          <td>0.6082</td>
          <td>0.3333</td>
          <td>0.2105</td>
          <td>0.0952</td>
          <td>0.7647</td>
          <td>5.99e-05</td>
          <td>7.03e-05</td>
          <td>0.0001158</td>
          <td>13704</td>
          <td>16183</td>
          <td>4588</td>
          <td>3666</td>
          <td>50</td>
          <td>776</td>
          <td>844</td>
          <td>2100</td>
          <td>31</td>
          <td>4548</td>
          <td>4039</td>
          <td>1985</td>
          <td>8752</td>
          <td>17508</td>
          <td>16870</td>
          <td>9484</td>
        </tr>
        <tr>
          <td>Lee Men&#x27;s Relaxed Fit Slightly Tapered Leg Jean</td>
          <td>Lee</td>
          <td>Jeans</td>
          <td>30.99</td>
          <td>16.89</td>
          <td>122.96</td>
          <td>55.54</td>
          <td>21</td>
          <td>4</td>
          <td>5</td>
          <td>3</td>
          <td>9</td>
          <td>248.92</td>
          <td>113.31</td>
          <td>0.4517</td>
          <td>0.5556</td>
          <td>0.2222</td>
          <td>0.1429</td>
          <td>0.6923</td>
          <td>4.55e-05</td>
          <td>3.97e-05</td>
          <td>0.0001158</td>
          <td>17446</td>
          <td>16178</td>
          <td>6481</td>
          <td>7447</td>
          <td>50</td>
          <td>776</td>
          <td>5</td>
          <td>526</td>
          <td>140</td>
          <td>2405</td>
          <td>2891</td>
          <td>17150</td>
          <td>4274</td>
          <td>17122</td>
          <td>12706</td>
          <td>12966</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Bright Argyle Crew Sock</td>
          <td>HUGO BOSS</td>
          <td>Socks</td>
          <td>9.75</td>
          <td>5.68</td>
          <td>39.0</td>
          <td>15.65</td>
          <td>22</td>
          <td>4</td>
          <td>4</td>
          <td>4</td>
          <td>10</td>
          <td>78.0</td>
          <td>32.25</td>
          <td>0.4013</td>
          <td>0.5</td>
          <td>0.2222</td>
          <td>0.1818</td>
          <td>0.7143</td>
          <td>1.44e-05</td>
          <td>1.12e-05</td>
          <td>0.0001214</td>
          <td>27342</td>
          <td>26355</td>
          <td>16327</td>
          <td>17765</td>
          <td>43</td>
          <td>776</td>
          <td>30</td>
          <td>126</td>
          <td>77</td>
          <td>10368</td>
          <td>12068</td>
          <td>20837</td>
          <td>4275</td>
          <td>17122</td>
          <td>10468</td>
          <td>12035</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by Return Rate</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>AIR JORDAN DOMINATE SHORTS MENS 465071-100</td>
          <td>Jordan</td>
          <td>Shorts</td>
          <td>903.0</td>
          <td>454.21</td>
          <td>2709.0</td>
          <td>1346.37</td>
          <td>5</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>2</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.497</td>
          <td>0.0</td>
          <td>0.6</td>
          <td>0.0</td>
          <td>0.4</td>
          <td>0.0010035</td>
          <td>0.0009622</td>
          <td>2.76e-05</td>
          <td>5</td>
          <td>8</td>
          <td>7</td>
          <td>9</td>
          <td>16887</td>
          <td>2358</td>
          <td>13463</td>
          <td>17458</td>
          <td>17069</td>
          <td>22642</td>
          <td>22642</td>
          <td>12874</td>
          <td>13463</td>
          <td>2189</td>
          <td>17458</td>
          <td>23875</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Expedition Parka</td>
          <td>Canada Goose</td>
          <td>Outerwear &amp; Coats</td>
          <td>795.0</td>
          <td>395.91</td>
          <td>2385.0</td>
          <td>1197.27</td>
          <td>4</td>
          <td>3</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>795.0</td>
          <td>399.09</td>
          <td>0.502</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.25</td>
          <td>0.0</td>
          <td>0.0008835</td>
          <td>0.0008557</td>
          <td>2.21e-05</td>
          <td>33</td>
          <td>19</td>
          <td>10</td>
          <td>13</td>
          <td>21053</td>
          <td>2358</td>
          <td>13463</td>
          <td>7029</td>
          <td>27145</td>
          <td>230</td>
          <td>277</td>
          <td>12357</td>
          <td>13463</td>
          <td>1</td>
          <td>5542</td>
          <td>27145</td>
        </tr>
        <tr>
          <td>True Religion Women&#x27;s Julie Super T Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>326.0</td>
          <td>172.13</td>
          <td>1956.0</td>
          <td>923.23</td>
          <td>8</td>
          <td>6</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>326.0</td>
          <td>153.87</td>
          <td>0.472</td>
          <td>0.0</td>
          <td>0.8571</td>
          <td>0.125</td>
          <td>0.1429</td>
          <td>0.0007246</td>
          <td>0.0006598</td>
          <td>4.41e-05</td>
          <td>233</td>
          <td>145</td>
          <td>19</td>
          <td>31</td>
          <td>5507</td>
          <td>84</td>
          <td>13463</td>
          <td>7029</td>
          <td>23197</td>
          <td>1487</td>
          <td>1788</td>
          <td>15335</td>
          <td>13463</td>
          <td>546</td>
          <td>14338</td>
          <td>27121</td>
        </tr>
        <tr>
          <td>Mountain Hardwear Women&#x27;s Chillwave Down Jacket</td>
          <td>Mountain Hardwear</td>
          <td>Outerwear &amp; Coats</td>
          <td>375.0</td>
          <td>179.25</td>
          <td>1875.0</td>
          <td>978.75</td>
          <td>6</td>
          <td>5</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>375.0</td>
          <td>195.75</td>
          <td>0.522</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.1667</td>
          <td>0.0</td>
          <td>0.0006946</td>
          <td>0.0006995</td>
          <td>3.31e-05</td>
          <td>155</td>
          <td>128</td>
          <td>20</td>
          <td>29</td>
          <td>12532</td>
          <td>251</td>
          <td>13463</td>
          <td>7029</td>
          <td>27145</td>
          <td>1150</td>
          <td>1161</td>
          <td>10227</td>
          <td>13463</td>
          <td>1</td>
          <td>10731</td>
          <td>27145</td>
        </tr>
        <tr>
          <td>Canada Goose Women&#x27;s Solaris</td>
          <td>Canada Goose</td>
          <td>Outerwear &amp; Coats</td>
          <td>695.0</td>
          <td>296.76</td>
          <td>2085.0</td>
          <td>1194.71</td>
          <td>6</td>
          <td>3</td>
          <td>0</td>
          <td>2</td>
          <td>1</td>
          <td>1390.0</td>
          <td>796.47</td>
          <td>0.573</td>
          <td>0.0</td>
          <td>0.75</td>
          <td>0.3333</td>
          <td>0.25</td>
          <td>0.0007724</td>
          <td>0.0008538</td>
          <td>3.31e-05</td>
          <td>46</td>
          <td>48</td>
          <td>17</td>
          <td>14</td>
          <td>12532</td>
          <td>2358</td>
          <td>13463</td>
          <td>2100</td>
          <td>23197</td>
          <td>67</td>
          <td>52</td>
          <td>5041</td>
          <td>13463</td>
          <td>746</td>
          <td>2619</td>
          <td>26348</td>
        </tr>
        <tr>
          <td>ASCIS Cushion Low Socks (Pack of 3)</td>
          <td>ASICS</td>
          <td>Active</td>
          <td>903.0</td>
          <td>373.84</td>
          <td>3612.0</td>
          <td>2116.63</td>
          <td>11</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>6</td>
          <td>903.0</td>
          <td>529.16</td>
          <td>0.586</td>
          <td>0.0</td>
          <td>0.4</td>
          <td>0.0909</td>
          <td>0.6</td>
          <td>0.001338</td>
          <td>0.0015127</td>
          <td>6.07e-05</td>
          <td>5</td>
          <td>28</td>
          <td>1</td>
          <td>1</td>
          <td>1161</td>
          <td>776</td>
          <td>13463</td>
          <td>7029</td>
          <td>1398</td>
          <td>155</td>
          <td>142</td>
          <td>3719</td>
          <td>13463</td>
          <td>7482</td>
          <td>16872</td>
          <td>16953</td>
        </tr>
        <tr>
          <td>Arc&#x27;teryx Moray Jacket - Women&#x27;s</td>
          <td>Arc&#x27;teryx</td>
          <td>Outerwear &amp; Coats</td>
          <td>699.0</td>
          <td>343.91</td>
          <td>2097.0</td>
          <td>1065.28</td>
          <td>9</td>
          <td>3</td>
          <td>0</td>
          <td>3</td>
          <td>3</td>
          <td>2097.0</td>
          <td>1065.28</td>
          <td>0.508</td>
          <td>0.0</td>
          <td>0.5</td>
          <td>0.3333</td>
          <td>0.5</td>
          <td>0.0007768</td>
          <td>0.0007613</td>
          <td>4.96e-05</td>
          <td>41</td>
          <td>36</td>
          <td>15</td>
          <td>20</td>
          <td>3355</td>
          <td>2358</td>
          <td>13463</td>
          <td>526</td>
          <td>10869</td>
          <td>11</td>
          <td>22</td>
          <td>11720</td>
          <td>13463</td>
          <td>3269</td>
          <td>2619</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>Men&#x27;s Classic Sheepskin B-3 Bomber Jacket</td>
          <td>Overland Sheepskin Co</td>
          <td>Outerwear &amp; Coats</td>
          <td>595.0</td>
          <td>270.73</td>
          <td>2380.0</td>
          <td>1297.1</td>
          <td>13</td>
          <td>4</td>
          <td>0</td>
          <td>2</td>
          <td>7</td>
          <td>1190.0</td>
          <td>648.55</td>
          <td>0.545</td>
          <td>0.0</td>
          <td>0.3636</td>
          <td>0.1538</td>
          <td>0.6364</td>
          <td>0.0008816</td>
          <td>0.000927</td>
          <td>7.17e-05</td>
          <td>60</td>
          <td>55</td>
          <td>12</td>
          <td>11</td>
          <td>423</td>
          <td>776</td>
          <td>13463</td>
          <td>2100</td>
          <td>623</td>
          <td>95</td>
          <td>94</td>
          <td>8121</td>
          <td>13463</td>
          <td>9638</td>
          <td>12634</td>
          <td>16487</td>
        </tr>
        <tr>
          <td>Michael Kors Men&#x27;s Marlow Wool-Blend Single-Breasted Fitted Top Coat</td>
          <td>Michael Kors</td>
          <td>Outerwear &amp; Coats</td>
          <td>255.0</td>
          <td>102.26</td>
          <td>2295.0</td>
          <td>1374.7</td>
          <td>15</td>
          <td>9</td>
          <td>1</td>
          <td>2</td>
          <td>3</td>
          <td>765.0</td>
          <td>458.23</td>
          <td>0.599</td>
          <td>0.1</td>
          <td>0.6923</td>
          <td>0.1333</td>
          <td>0.25</td>
          <td>0.0008502</td>
          <td>0.0009825</td>
          <td>8.27e-05</td>
          <td>469</td>
          <td>728</td>
          <td>13</td>
          <td>8</td>
          <td>187</td>
          <td>5</td>
          <td>3978</td>
          <td>2100</td>
          <td>10869</td>
          <td>252</td>
          <td>208</td>
          <td>2612</td>
          <td>13461</td>
          <td>1184</td>
          <td>14317</td>
          <td>26348</td>
        </tr>
        <tr>
          <td>Joseph Abboud Men&#x27;s Two-button Side Vent Sport Coat</td>
          <td>Joseph Abboud</td>
          <td>Suits &amp; Sport Coats</td>
          <td>264.0</td>
          <td>101.9</td>
          <td>2904.0</td>
          <td>1759.82</td>
          <td>30</td>
          <td>11</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>1056.0</td>
          <td>656.57</td>
          <td>0.606</td>
          <td>0.1538</td>
          <td>0.3929</td>
          <td>0.0667</td>
          <td>0.5769</td>
          <td>0.0010758</td>
          <td>0.0012577</td>
          <td>0.0001655</td>
          <td>430</td>
          <td>734</td>
          <td>6</td>
          <td>5</td>
          <td>7</td>
          <td>3</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>112</td>
          <td>91</td>
          <td>2144</td>
          <td>13388</td>
          <td>9081</td>
          <td>17408</td>
          <td>18610</td>
        </tr>
        <tr>
          <td>Barbour Sapper Jacket</td>
          <td>Barbour</td>
          <td>Outerwear &amp; Coats</td>
          <td>429.0</td>
          <td>210.21</td>
          <td>2145.0</td>
          <td>1093.95</td>
          <td>10</td>
          <td>5</td>
          <td>1</td>
          <td>1</td>
          <td>3</td>
          <td>858.0</td>
          <td>437.58</td>
          <td>0.51</td>
          <td>0.1667</td>
          <td>0.5556</td>
          <td>0.1</td>
          <td>0.375</td>
          <td>0.0007946</td>
          <td>0.0007818</td>
          <td>5.52e-05</td>
          <td>94</td>
          <td>81</td>
          <td>14</td>
          <td>18</td>
          <td>1962</td>
          <td>251</td>
          <td>3978</td>
          <td>7029</td>
          <td>10869</td>
          <td>185</td>
          <td>233</td>
          <td>11510</td>
          <td>13196</td>
          <td>3151</td>
          <td>16366</td>
          <td>24717</td>
        </tr>
        <tr>
          <td>Diesel Men&#x27;s Lagnum Leather Jacket</td>
          <td>Diesel</td>
          <td>Outerwear &amp; Coats</td>
          <td>598.0</td>
          <td>267.9</td>
          <td>2392.0</td>
          <td>1320.38</td>
          <td>7</td>
          <td>4</td>
          <td>1</td>
          <td>1</td>
          <td>1</td>
          <td>1196.0</td>
          <td>660.19</td>
          <td>0.552</td>
          <td>0.2</td>
          <td>0.6667</td>
          <td>0.1429</td>
          <td>0.2</td>
          <td>0.0008861</td>
          <td>0.0009437</td>
          <td>3.86e-05</td>
          <td>57</td>
          <td>56</td>
          <td>9</td>
          <td>10</td>
          <td>8625</td>
          <td>776</td>
          <td>3978</td>
          <td>7029</td>
          <td>23197</td>
          <td>92</td>
          <td>89</td>
          <td>7373</td>
          <td>12637</td>
          <td>1185</td>
          <td>12706</td>
          <td>26859</td>
        </tr>
        <tr>
          <td>The North Face Women&#x27;s S-XL Oso Jacket</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>378.36</td>
          <td>3612.0</td>
          <td>2098.57</td>
          <td>10</td>
          <td>4</td>
          <td>1</td>
          <td>1</td>
          <td>4</td>
          <td>1806.0</td>
          <td>1049.29</td>
          <td>0.581</td>
          <td>0.2</td>
          <td>0.4444</td>
          <td>0.1</td>
          <td>0.5</td>
          <td>0.001338</td>
          <td>0.0014998</td>
          <td>5.52e-05</td>
          <td>5</td>
          <td>25</td>
          <td>1</td>
          <td>2</td>
          <td>1962</td>
          <td>776</td>
          <td>3978</td>
          <td>7029</td>
          <td>6105</td>
          <td>22</td>
          <td>24</td>
          <td>4209</td>
          <td>12637</td>
          <td>6492</td>
          <td>16366</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>Bergama Natural Raccoon Hooded Stroller - - Multicolor</td>
          <td>Bergama</td>
          <td>Outerwear &amp; Coats</td>
          <td>749.99</td>
          <td>306.75</td>
          <td>2999.96</td>
          <td>1772.98</td>
          <td>10</td>
          <td>4</td>
          <td>1</td>
          <td>0</td>
          <td>5</td>
          <td>749.99</td>
          <td>443.24</td>
          <td>0.591</td>
          <td>0.2</td>
          <td>0.4</td>
          <td>0.0</td>
          <td>0.5556</td>
          <td>0.0011113</td>
          <td>0.0012671</td>
          <td>5.52e-05</td>
          <td>40</td>
          <td>43</td>
          <td>4</td>
          <td>3</td>
          <td>1962</td>
          <td>776</td>
          <td>3978</td>
          <td>17458</td>
          <td>3026</td>
          <td>267</td>
          <td>224</td>
          <td>3279</td>
          <td>12637</td>
          <td>7482</td>
          <td>17458</td>
          <td>19270</td>
        </tr>
        <tr>
          <td>Diesel Men&#x27;s Jimeneo Jacket</td>
          <td>Diesel</td>
          <td>Suits &amp; Sport Coats</td>
          <td>698.0</td>
          <td>304.33</td>
          <td>2094.0</td>
          <td>1181.02</td>
          <td>13</td>
          <td>3</td>
          <td>1</td>
          <td>1</td>
          <td>8</td>
          <td>1396.0</td>
          <td>787.34</td>
          <td>0.564</td>
          <td>0.25</td>
          <td>0.25</td>
          <td>0.0769</td>
          <td>0.7273</td>
          <td>0.0007757</td>
          <td>0.0008441</td>
          <td>7.17e-05</td>
          <td>43</td>
          <td>46</td>
          <td>16</td>
          <td>16</td>
          <td>423</td>
          <td>2358</td>
          <td>3978</td>
          <td>7029</td>
          <td>295</td>
          <td>65</td>
          <td>54</td>
          <td>6066</td>
          <td>11344</td>
          <td>14408</td>
          <td>17286</td>
          <td>11980</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by Cancellation Rate</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
WHERE unit_orders_placed_rank &lt;= 25
ORDER BY
  cancellation_rate_rank DESC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Chaps Big and Tall Solid V-Neck Vest</td>
          <td>Chaps</td>
          <td>Sweaters</td>
          <td>39.88</td>
          <td>20.32</td>
          <td>279.16</td>
          <td>134.91</td>
          <td>28</td>
          <td>7</td>
          <td>4</td>
          <td>1</td>
          <td>16</td>
          <td>199.4</td>
          <td>99.06</td>
          <td>0.4833</td>
          <td>0.3636</td>
          <td>0.2593</td>
          <td>0.0357</td>
          <td>0.6957</td>
          <td>0.0001034</td>
          <td>9.64e-05</td>
          <td>0.0001545</td>
          <td>14437</td>
          <td>13747</td>
          <td>2029</td>
          <td>2288</td>
          <td>9</td>
          <td>33</td>
          <td>30</td>
          <td>7029</td>
          <td>7</td>
          <td>3354</td>
          <td>3543</td>
          <td>14237</td>
          <td>8748</td>
          <td>14407</td>
          <td>17457</td>
          <td>12964</td>
        </tr>
        <tr>
          <td>Joseph Abboud Men&#x27;s Two-button Side Vent Sport Coat</td>
          <td>Joseph Abboud</td>
          <td>Suits &amp; Sport Coats</td>
          <td>264.0</td>
          <td>101.9</td>
          <td>2904.0</td>
          <td>1759.82</td>
          <td>30</td>
          <td>11</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>1056.0</td>
          <td>656.57</td>
          <td>0.606</td>
          <td>0.1538</td>
          <td>0.3929</td>
          <td>0.0667</td>
          <td>0.5769</td>
          <td>0.0010758</td>
          <td>0.0012577</td>
          <td>0.0001655</td>
          <td>430</td>
          <td>734</td>
          <td>6</td>
          <td>5</td>
          <td>7</td>
          <td>3</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>112</td>
          <td>91</td>
          <td>2144</td>
          <td>13388</td>
          <td>9081</td>
          <td>17408</td>
          <td>18610</td>
        </tr>
        <tr>
          <td>Joe&#x27;s Jeans Men&#x27;s Slim Fit Straight Leg Brixton</td>
          <td>Joe&#x27;s Jeans</td>
          <td>Jeans</td>
          <td>194.26</td>
          <td>102.07</td>
          <td>1353.0</td>
          <td>647.44</td>
          <td>27</td>
          <td>7</td>
          <td>3</td>
          <td>2</td>
          <td>15</td>
          <td>976.0</td>
          <td>458.49</td>
          <td>0.4785</td>
          <td>0.3</td>
          <td>0.28</td>
          <td>0.0741</td>
          <td>0.6818</td>
          <td>0.0005012</td>
          <td>0.0004627</td>
          <td>0.0001489</td>
          <td>992</td>
          <td>729</td>
          <td>58</td>
          <td>76</td>
          <td>12</td>
          <td>33</td>
          <td>151</td>
          <td>2100</td>
          <td>11</td>
          <td>133</td>
          <td>207</td>
          <td>14773</td>
          <td>11276</td>
          <td>14282</td>
          <td>17370</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Dockers Men&#x27;s Suit Separate Coat</td>
          <td>Dockers</td>
          <td>Suits &amp; Sport Coats</td>
          <td>88.36</td>
          <td>33.97</td>
          <td>231.12</td>
          <td>140.98</td>
          <td>27</td>
          <td>3</td>
          <td>4</td>
          <td>2</td>
          <td>18</td>
          <td>542.11</td>
          <td>337.6</td>
          <td>0.61</td>
          <td>0.5714</td>
          <td>0.12</td>
          <td>0.0741</td>
          <td>0.8571</td>
          <td>8.56e-05</td>
          <td>0.0001008</td>
          <td>0.0001489</td>
          <td>5094</td>
          <td>7229</td>
          <td>2783</td>
          <td>2122</td>
          <td>12</td>
          <td>2358</td>
          <td>30</td>
          <td>2100</td>
          <td>4</td>
          <td>542</td>
          <td>391</td>
          <td>1873</td>
          <td>4252</td>
          <td>22129</td>
          <td>17370</td>
          <td>6057</td>
        </tr>
        <tr>
          <td>UltraClub Adult Sherpa-Lined Full-Zip Fleece with Hood</td>
          <td>UltraClub</td>
          <td>Fashion Hoodies &amp; Sweatshirts</td>
          <td>51.47</td>
          <td>28.47</td>
          <td>360.9</td>
          <td>161.23</td>
          <td>26</td>
          <td>7</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>203.71</td>
          <td>91.12</td>
          <td>0.4467</td>
          <td>0.2222</td>
          <td>0.2917</td>
          <td>0.0769</td>
          <td>0.6818</td>
          <td>0.0001337</td>
          <td>0.0001152</td>
          <td>0.0001434</td>
          <td>10603</td>
          <td>9302</td>
          <td>1222</td>
          <td>1705</td>
          <td>17</td>
          <td>33</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>3228</td>
          <td>4041</td>
          <td>17630</td>
          <td>12628</td>
          <td>13236</td>
          <td>17286</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Lucky Brand Mens Men&#x27;s 361 Vintage Straight Denim Jean</td>
          <td>Lucky Brand</td>
          <td>Jeans</td>
          <td>99.0</td>
          <td>52.65</td>
          <td>594.0</td>
          <td>275.91</td>
          <td>25</td>
          <td>6</td>
          <td>3</td>
          <td>2</td>
          <td>14</td>
          <td>495.0</td>
          <td>228.59</td>
          <td>0.4645</td>
          <td>0.3333</td>
          <td>0.2609</td>
          <td>0.08</td>
          <td>0.7</td>
          <td>0.00022</td>
          <td>0.0001972</td>
          <td>0.0001379</td>
          <td>4113</td>
          <td>3525</td>
          <td>427</td>
          <td>608</td>
          <td>21</td>
          <td>84</td>
          <td>151</td>
          <td>2100</td>
          <td>22</td>
          <td>674</td>
          <td>896</td>
          <td>15993</td>
          <td>8752</td>
          <td>14406</td>
          <td>17285</td>
          <td>12849</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>246.88</td>
          <td>129.05</td>
          <td>1366.0</td>
          <td>666.07</td>
          <td>34</td>
          <td>5</td>
          <td>4</td>
          <td>3</td>
          <td>22</td>
          <td>1400.0</td>
          <td>654.5</td>
          <td>0.4876</td>
          <td>0.4444</td>
          <td>0.1613</td>
          <td>0.0882</td>
          <td>0.8148</td>
          <td>0.000506</td>
          <td>0.000476</td>
          <td>0.0001876</td>
          <td>534</td>
          <td>354</td>
          <td>56</td>
          <td>65</td>
          <td>4</td>
          <td>251</td>
          <td>30</td>
          <td>526</td>
          <td>3</td>
          <td>63</td>
          <td>92</td>
          <td>13792</td>
          <td>8264</td>
          <td>20804</td>
          <td>17143</td>
          <td>7595</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Long Pant</td>
          <td>HUGO BOSS</td>
          <td>Sleep &amp; Lounge</td>
          <td>74.72</td>
          <td>28.3</td>
          <td>1033.11</td>
          <td>648.16</td>
          <td>33</td>
          <td>14</td>
          <td>0</td>
          <td>3</td>
          <td>16</td>
          <td>233.01</td>
          <td>138.21</td>
          <td>0.6274</td>
          <td>0.0</td>
          <td>0.4667</td>
          <td>0.0909</td>
          <td>0.5333</td>
          <td>0.0003827</td>
          <td>0.0004632</td>
          <td>0.000182</td>
          <td>6501</td>
          <td>9383</td>
          <td>113</td>
          <td>75</td>
          <td>6</td>
          <td>1</td>
          <td>13463</td>
          <td>526</td>
          <td>7</td>
          <td>2702</td>
          <td>2165</td>
          <td>933</td>
          <td>13463</td>
          <td>6418</td>
          <td>16872</td>
          <td>19494</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Wrancher Dress Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.4</td>
          <td>20.2</td>
          <td>242.4</td>
          <td>118.65</td>
          <td>27</td>
          <td>6</td>
          <td>2</td>
          <td>3</td>
          <td>16</td>
          <td>202.0</td>
          <td>102.05</td>
          <td>0.4895</td>
          <td>0.25</td>
          <td>0.25</td>
          <td>0.1111</td>
          <td>0.7273</td>
          <td>8.98e-05</td>
          <td>8.48e-05</td>
          <td>0.0001489</td>
          <td>13728</td>
          <td>13816</td>
          <td>2533</td>
          <td>2788</td>
          <td>12</td>
          <td>84</td>
          <td>844</td>
          <td>526</td>
          <td>7</td>
          <td>3236</td>
          <td>3382</td>
          <td>13585</td>
          <td>11344</td>
          <td>14408</td>
          <td>15570</td>
          <td>11980</td>
        </tr>
        <tr>
          <td>Joe&#x27;s Jeans Men&#x27;s Rebel Relaxed Fit Jean</td>
          <td>Joe&#x27;s Jeans</td>
          <td>Jeans</td>
          <td>139.29</td>
          <td>76.13</td>
          <td>1296.69</td>
          <td>583.03</td>
          <td>26</td>
          <td>9</td>
          <td>0</td>
          <td>3</td>
          <td>14</td>
          <td>339.69</td>
          <td>166.11</td>
          <td>0.4496</td>
          <td>0.0</td>
          <td>0.3913</td>
          <td>0.1154</td>
          <td>0.6087</td>
          <td>0.0004803</td>
          <td>0.0004167</td>
          <td>0.0001434</td>
          <td>2334</td>
          <td>1721</td>
          <td>68</td>
          <td>102</td>
          <td>17</td>
          <td>5</td>
          <td>13463</td>
          <td>526</td>
          <td>22</td>
          <td>1403</td>
          <td>1558</td>
          <td>17357</td>
          <td>13463</td>
          <td>9082</td>
          <td>15567</td>
          <td>16952</td>
        </tr>
        <tr>
          <td>RVCA Men&#x27;s Heavy Chev Denim Pant</td>
          <td>RVCA</td>
          <td>Jeans</td>
          <td>77.05</td>
          <td>43.62</td>
          <td>599.7</td>
          <td>260.01</td>
          <td>26</td>
          <td>8</td>
          <td>2</td>
          <td>3</td>
          <td>13</td>
          <td>395.9</td>
          <td>171.93</td>
          <td>0.4336</td>
          <td>0.2</td>
          <td>0.3478</td>
          <td>0.1154</td>
          <td>0.619</td>
          <td>0.0002222</td>
          <td>0.0001858</td>
          <td>0.0001434</td>
          <td>6221</td>
          <td>4800</td>
          <td>406</td>
          <td>687</td>
          <td>17</td>
          <td>16</td>
          <td>844</td>
          <td>526</td>
          <td>31</td>
          <td>1032</td>
          <td>1457</td>
          <td>18759</td>
          <td>12637</td>
          <td>9743</td>
          <td>15567</td>
          <td>16938</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s 20x Collection Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>55.0</td>
          <td>29.7</td>
          <td>440.0</td>
          <td>202.51</td>
          <td>26</td>
          <td>8</td>
          <td>2</td>
          <td>3</td>
          <td>13</td>
          <td>275.0</td>
          <td>133.27</td>
          <td>0.4602</td>
          <td>0.2</td>
          <td>0.3478</td>
          <td>0.1154</td>
          <td>0.619</td>
          <td>0.000163</td>
          <td>0.0001447</td>
          <td>0.0001434</td>
          <td>9673</td>
          <td>8763</td>
          <td>847</td>
          <td>1122</td>
          <td>17</td>
          <td>16</td>
          <td>844</td>
          <td>526</td>
          <td>31</td>
          <td>2032</td>
          <td>2300</td>
          <td>16343</td>
          <td>12637</td>
          <td>9743</td>
          <td>15567</td>
          <td>16938</td>
        </tr>
        <tr>
          <td>Kenneth Cole REACTION Men&#x27;s Passcase Wallet</td>
          <td>Kenneth Cole REACTION</td>
          <td>Accessories</td>
          <td>18.91</td>
          <td>7.72</td>
          <td>152.71</td>
          <td>89.4</td>
          <td>34</td>
          <td>8</td>
          <td>4</td>
          <td>4</td>
          <td>18</td>
          <td>150.85</td>
          <td>90.57</td>
          <td>0.5854</td>
          <td>0.3333</td>
          <td>0.2667</td>
          <td>0.1176</td>
          <td>0.6923</td>
          <td>5.66e-05</td>
          <td>6.39e-05</td>
          <td>0.0001876</td>
          <td>23389</td>
          <td>24481</td>
          <td>4958</td>
          <td>4188</td>
          <td>4</td>
          <td>16</td>
          <td>30</td>
          <td>126</td>
          <td>4</td>
          <td>5015</td>
          <td>4078</td>
          <td>3806</td>
          <td>8752</td>
          <td>14395</td>
          <td>15553</td>
          <td>12966</td>
        </tr>
        <tr>
          <td>7 For All Mankind Men&#x27;s Standard Classic Straight Leg Jean</td>
          <td>7 For All Mankind</td>
          <td>Jeans</td>
          <td>157.45</td>
          <td>80.97</td>
          <td>1435.0</td>
          <td>696.01</td>
          <td>42</td>
          <td>9</td>
          <td>5</td>
          <td>5</td>
          <td>23</td>
          <td>1673.0</td>
          <td>844.04</td>
          <td>0.485</td>
          <td>0.3571</td>
          <td>0.2432</td>
          <td>0.119</td>
          <td>0.7188</td>
          <td>0.0005316</td>
          <td>0.0004974</td>
          <td>0.0002317</td>
          <td>1798</td>
          <td>1488</td>
          <td>46</td>
          <td>60</td>
          <td>2</td>
          <td>5</td>
          <td>5</td>
          <td>24</td>
          <td>2</td>
          <td>32</td>
          <td>41</td>
          <td>14028</td>
          <td>8749</td>
          <td>17091</td>
          <td>15552</td>
          <td>12034</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Sarasota Agility Short</td>
          <td>Wrangler</td>
          <td>Shorts</td>
          <td>33.03</td>
          <td>16.36</td>
          <td>198.95</td>
          <td>101.37</td>
          <td>25</td>
          <td>6</td>
          <td>1</td>
          <td>3</td>
          <td>15</td>
          <td>138.97</td>
          <td>68.68</td>
          <td>0.5095</td>
          <td>0.1429</td>
          <td>0.2727</td>
          <td>0.12</td>
          <td>0.7143</td>
          <td>7.37e-05</td>
          <td>7.24e-05</td>
          <td>0.0001379</td>
          <td>16765</td>
          <td>16618</td>
          <td>3447</td>
          <td>3505</td>
          <td>21</td>
          <td>84</td>
          <td>3978</td>
          <td>526</td>
          <td>11</td>
          <td>5758</td>
          <td>5901</td>
          <td>11606</td>
          <td>13389</td>
          <td>14284</td>
          <td>15549</td>
          <td>12035</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by En Route Rate</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
WHERE unit_orders_placed_rank &lt;= 25
ORDER BY
  en_route_rate_rank DESC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Hanes Men&#x27;s 4 Pack Boxer Brief</td>
          <td>Hanes</td>
          <td>Underwear</td>
          <td>25.0</td>
          <td>11.52</td>
          <td>250.0</td>
          <td>133.47</td>
          <td>28</td>
          <td>10</td>
          <td>2</td>
          <td>5</td>
          <td>11</td>
          <td>175.0</td>
          <td>92.77</td>
          <td>0.5339</td>
          <td>0.1667</td>
          <td>0.4348</td>
          <td>0.1786</td>
          <td>0.5238</td>
          <td>9.26e-05</td>
          <td>9.54e-05</td>
          <td>0.0001545</td>
          <td>19651</td>
          <td>20997</td>
          <td>2432</td>
          <td>2340</td>
          <td>9</td>
          <td>4</td>
          <td>844</td>
          <td>24</td>
          <td>43</td>
          <td>4152</td>
          <td>3935</td>
          <td>9232</td>
          <td>13196</td>
          <td>6738</td>
          <td>10715</td>
          <td>19500</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Long Pant</td>
          <td>HUGO BOSS</td>
          <td>Sleep &amp; Lounge</td>
          <td>74.72</td>
          <td>28.3</td>
          <td>1033.11</td>
          <td>648.16</td>
          <td>33</td>
          <td>14</td>
          <td>0</td>
          <td>3</td>
          <td>16</td>
          <td>233.01</td>
          <td>138.21</td>
          <td>0.6274</td>
          <td>0.0</td>
          <td>0.4667</td>
          <td>0.0909</td>
          <td>0.5333</td>
          <td>0.0003827</td>
          <td>0.0004632</td>
          <td>0.000182</td>
          <td>6501</td>
          <td>9383</td>
          <td>113</td>
          <td>75</td>
          <td>6</td>
          <td>1</td>
          <td>13463</td>
          <td>526</td>
          <td>7</td>
          <td>2702</td>
          <td>2165</td>
          <td>933</td>
          <td>13463</td>
          <td>6418</td>
          <td>16872</td>
          <td>19494</td>
        </tr>
        <tr>
          <td>Motherhood Maternity: Sports Clip Down Nursing Bra</td>
          <td>Motherhood Maternity</td>
          <td>Maternity</td>
          <td>22.54</td>
          <td>10.46</td>
          <td>200.82</td>
          <td>108.99</td>
          <td>25</td>
          <td>9</td>
          <td>2</td>
          <td>3</td>
          <td>11</td>
          <td>112.9</td>
          <td>60.37</td>
          <td>0.5427</td>
          <td>0.1818</td>
          <td>0.4091</td>
          <td>0.12</td>
          <td>0.55</td>
          <td>7.44e-05</td>
          <td>7.79e-05</td>
          <td>0.0001379</td>
          <td>21822</td>
          <td>22052</td>
          <td>3297</td>
          <td>3165</td>
          <td>21</td>
          <td>5</td>
          <td>844</td>
          <td>526</td>
          <td>43</td>
          <td>7249</td>
          <td>6811</td>
          <td>8373</td>
          <td>13193</td>
          <td>7481</td>
          <td>15549</td>
          <td>19449</td>
        </tr>
        <tr>
          <td>Joseph Abboud Men&#x27;s Two-button Side Vent Sport Coat</td>
          <td>Joseph Abboud</td>
          <td>Suits &amp; Sport Coats</td>
          <td>264.0</td>
          <td>101.9</td>
          <td>2904.0</td>
          <td>1759.82</td>
          <td>30</td>
          <td>11</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>1056.0</td>
          <td>656.57</td>
          <td>0.606</td>
          <td>0.1538</td>
          <td>0.3929</td>
          <td>0.0667</td>
          <td>0.5769</td>
          <td>0.0010758</td>
          <td>0.0012577</td>
          <td>0.0001655</td>
          <td>430</td>
          <td>734</td>
          <td>6</td>
          <td>5</td>
          <td>7</td>
          <td>3</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>112</td>
          <td>91</td>
          <td>2144</td>
          <td>13388</td>
          <td>9081</td>
          <td>17408</td>
          <td>18610</td>
        </tr>
        <tr>
          <td>Joe&#x27;s Jeans Men&#x27;s Rebel Relaxed Fit Jean</td>
          <td>Joe&#x27;s Jeans</td>
          <td>Jeans</td>
          <td>139.29</td>
          <td>76.13</td>
          <td>1296.69</td>
          <td>583.03</td>
          <td>26</td>
          <td>9</td>
          <td>0</td>
          <td>3</td>
          <td>14</td>
          <td>339.69</td>
          <td>166.11</td>
          <td>0.4496</td>
          <td>0.0</td>
          <td>0.3913</td>
          <td>0.1154</td>
          <td>0.6087</td>
          <td>0.0004803</td>
          <td>0.0004167</td>
          <td>0.0001434</td>
          <td>2334</td>
          <td>1721</td>
          <td>68</td>
          <td>102</td>
          <td>17</td>
          <td>5</td>
          <td>13463</td>
          <td>526</td>
          <td>22</td>
          <td>1403</td>
          <td>1558</td>
          <td>17357</td>
          <td>13463</td>
          <td>9082</td>
          <td>15567</td>
          <td>16952</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Original Cowboy Cut Relaxed Fit Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>42.99</td>
          <td>22.67</td>
          <td>228.46</td>
          <td>108.63</td>
          <td>25</td>
          <td>5</td>
          <td>5</td>
          <td>7</td>
          <td>8</td>
          <td>493.18</td>
          <td>228.73</td>
          <td>0.4755</td>
          <td>0.5</td>
          <td>0.2778</td>
          <td>0.28</td>
          <td>0.6154</td>
          <td>8.46e-05</td>
          <td>7.76e-05</td>
          <td>0.0001379</td>
          <td>13180</td>
          <td>12269</td>
          <td>2826</td>
          <td>3184</td>
          <td>21</td>
          <td>251</td>
          <td>5</td>
          <td>2</td>
          <td>295</td>
          <td>687</td>
          <td>895</td>
          <td>15040</td>
          <td>4275</td>
          <td>14283</td>
          <td>5404</td>
          <td>16940</td>
        </tr>
        <tr>
          <td>RVCA Men&#x27;s Heavy Chev Denim Pant</td>
          <td>RVCA</td>
          <td>Jeans</td>
          <td>77.05</td>
          <td>43.62</td>
          <td>599.7</td>
          <td>260.01</td>
          <td>26</td>
          <td>8</td>
          <td>2</td>
          <td>3</td>
          <td>13</td>
          <td>395.9</td>
          <td>171.93</td>
          <td>0.4336</td>
          <td>0.2</td>
          <td>0.3478</td>
          <td>0.1154</td>
          <td>0.619</td>
          <td>0.0002222</td>
          <td>0.0001858</td>
          <td>0.0001434</td>
          <td>6221</td>
          <td>4800</td>
          <td>406</td>
          <td>687</td>
          <td>17</td>
          <td>16</td>
          <td>844</td>
          <td>526</td>
          <td>31</td>
          <td>1032</td>
          <td>1457</td>
          <td>18759</td>
          <td>12637</td>
          <td>9743</td>
          <td>15567</td>
          <td>16938</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s 20x Collection Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>55.0</td>
          <td>29.7</td>
          <td>440.0</td>
          <td>202.51</td>
          <td>26</td>
          <td>8</td>
          <td>2</td>
          <td>3</td>
          <td>13</td>
          <td>275.0</td>
          <td>133.27</td>
          <td>0.4602</td>
          <td>0.2</td>
          <td>0.3478</td>
          <td>0.1154</td>
          <td>0.619</td>
          <td>0.000163</td>
          <td>0.0001447</td>
          <td>0.0001434</td>
          <td>9673</td>
          <td>8763</td>
          <td>847</td>
          <td>1122</td>
          <td>17</td>
          <td>16</td>
          <td>844</td>
          <td>526</td>
          <td>31</td>
          <td>2032</td>
          <td>2300</td>
          <td>16343</td>
          <td>12637</td>
          <td>9743</td>
          <td>15567</td>
          <td>16938</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Rugged Wear Classic Fit Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>40.87</td>
          <td>22.23</td>
          <td>367.56</td>
          <td>169.24</td>
          <td>38</td>
          <td>9</td>
          <td>5</td>
          <td>9</td>
          <td>15</td>
          <td>596.43</td>
          <td>273.96</td>
          <td>0.4604</td>
          <td>0.3571</td>
          <td>0.3103</td>
          <td>0.2368</td>
          <td>0.625</td>
          <td>0.0001362</td>
          <td>0.000121</td>
          <td>0.0002096</td>
          <td>13688</td>
          <td>12514</td>
          <td>1205</td>
          <td>1552</td>
          <td>3</td>
          <td>5</td>
          <td>5</td>
          <td>1</td>
          <td>11</td>
          <td>440</td>
          <td>628</td>
          <td>16340</td>
          <td>8749</td>
          <td>13014</td>
          <td>7776</td>
          <td>16547</td>
        </tr>
        <tr>
          <td>Bottoms Out Men&#x27;s Plaid Sleep Pant</td>
          <td>Bottoms Out</td>
          <td>Sleep &amp; Lounge</td>
          <td>13.49</td>
          <td>5.05</td>
          <td>94.43</td>
          <td>59.4</td>
          <td>25</td>
          <td>7</td>
          <td>2</td>
          <td>4</td>
          <td>12</td>
          <td>80.94</td>
          <td>50.64</td>
          <td>0.629</td>
          <td>0.2222</td>
          <td>0.3333</td>
          <td>0.16</td>
          <td>0.6316</td>
          <td>3.5e-05</td>
          <td>4.25e-05</td>
          <td>0.0001379</td>
          <td>25625</td>
          <td>26913</td>
          <td>8758</td>
          <td>6904</td>
          <td>21</td>
          <td>33</td>
          <td>844</td>
          <td>126</td>
          <td>37</td>
          <td>9890</td>
          <td>8299</td>
          <td>839</td>
          <td>12628</td>
          <td>9747</td>
          <td>12630</td>
          <td>16546</td>
        </tr>
        <tr>
          <td>Volcom Men&#x27;s Vorta Slim Straight Leg Fit Jean</td>
          <td>Volcom</td>
          <td>Jeans</td>
          <td>73.57</td>
          <td>41.13</td>
          <td>574.85</td>
          <td>249.86</td>
          <td>27</td>
          <td>8</td>
          <td>1</td>
          <td>4</td>
          <td>14</td>
          <td>387.8</td>
          <td>166.89</td>
          <td>0.4347</td>
          <td>0.1111</td>
          <td>0.3478</td>
          <td>0.1481</td>
          <td>0.6364</td>
          <td>0.0002129</td>
          <td>0.0001786</td>
          <td>0.0001489</td>
          <td>6603</td>
          <td>5251</td>
          <td>467</td>
          <td>746</td>
          <td>12</td>
          <td>16</td>
          <td>3978</td>
          <td>126</td>
          <td>22</td>
          <td>1091</td>
          <td>1537</td>
          <td>18678</td>
          <td>13456</td>
          <td>9743</td>
          <td>12705</td>
          <td>16487</td>
        </tr>
        <tr>
          <td>UltraClub Adult Sherpa-Lined Full-Zip Fleece with Hood</td>
          <td>UltraClub</td>
          <td>Fashion Hoodies &amp; Sweatshirts</td>
          <td>51.47</td>
          <td>28.47</td>
          <td>360.9</td>
          <td>161.23</td>
          <td>26</td>
          <td>7</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>203.71</td>
          <td>91.12</td>
          <td>0.4467</td>
          <td>0.2222</td>
          <td>0.2917</td>
          <td>0.0769</td>
          <td>0.6818</td>
          <td>0.0001337</td>
          <td>0.0001152</td>
          <td>0.0001434</td>
          <td>10603</td>
          <td>9302</td>
          <td>1222</td>
          <td>1705</td>
          <td>17</td>
          <td>33</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>3228</td>
          <td>4041</td>
          <td>17630</td>
          <td>12628</td>
          <td>13236</td>
          <td>17286</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Leg Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>227.86</td>
          <td>123.14</td>
          <td>1452.0</td>
          <td>661.01</td>
          <td>28</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>15</td>
          <td>1430.0</td>
          <td>645.85</td>
          <td>0.4552</td>
          <td>0.125</td>
          <td>0.3043</td>
          <td>0.1786</td>
          <td>0.6818</td>
          <td>0.0005379</td>
          <td>0.0004724</td>
          <td>0.0001545</td>
          <td>646</td>
          <td>406</td>
          <td>45</td>
          <td>69</td>
          <td>9</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>11</td>
          <td>57</td>
          <td>95</td>
          <td>16801</td>
          <td>13444</td>
          <td>13032</td>
          <td>10715</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Joe&#x27;s Jeans Men&#x27;s Slim Fit Straight Leg Brixton</td>
          <td>Joe&#x27;s Jeans</td>
          <td>Jeans</td>
          <td>194.26</td>
          <td>102.07</td>
          <td>1353.0</td>
          <td>647.44</td>
          <td>27</td>
          <td>7</td>
          <td>3</td>
          <td>2</td>
          <td>15</td>
          <td>976.0</td>
          <td>458.49</td>
          <td>0.4785</td>
          <td>0.3</td>
          <td>0.28</td>
          <td>0.0741</td>
          <td>0.6818</td>
          <td>0.0005012</td>
          <td>0.0004627</td>
          <td>0.0001489</td>
          <td>992</td>
          <td>729</td>
          <td>58</td>
          <td>76</td>
          <td>12</td>
          <td>33</td>
          <td>151</td>
          <td>2100</td>
          <td>11</td>
          <td>133</td>
          <td>207</td>
          <td>14773</td>
          <td>11276</td>
          <td>14282</td>
          <td>17370</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Kenneth Cole REACTION Men&#x27;s Passcase Wallet</td>
          <td>Kenneth Cole REACTION</td>
          <td>Accessories</td>
          <td>18.91</td>
          <td>7.72</td>
          <td>152.71</td>
          <td>89.4</td>
          <td>34</td>
          <td>8</td>
          <td>4</td>
          <td>4</td>
          <td>18</td>
          <td>150.85</td>
          <td>90.57</td>
          <td>0.5854</td>
          <td>0.3333</td>
          <td>0.2667</td>
          <td>0.1176</td>
          <td>0.6923</td>
          <td>5.66e-05</td>
          <td>6.39e-05</td>
          <td>0.0001876</td>
          <td>23389</td>
          <td>24481</td>
          <td>4958</td>
          <td>4188</td>
          <td>4</td>
          <td>16</td>
          <td>30</td>
          <td>126</td>
          <td>4</td>
          <td>5015</td>
          <td>4078</td>
          <td>3806</td>
          <td>8752</td>
          <td>14395</td>
          <td>15553</td>
          <td>12966</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by Units Completed</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
  units_completed_rank DESC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Kenneth Cole Men&#x27;s Straight Leg Jean</td>
          <td>Kenneth Cole</td>
          <td>Jeans</td>
          <td>54.25</td>
          <td>27.11</td>
          <td>54.99</td>
          <td>26.89</td>
          <td>24</td>
          <td>1</td>
          <td>7</td>
          <td>4</td>
          <td>12</td>
          <td>632.25</td>
          <td>318.8</td>
          <td>0.489</td>
          <td>0.875</td>
          <td>0.05</td>
          <td>0.1667</td>
          <td>0.9231</td>
          <td>2.04e-05</td>
          <td>1.92e-05</td>
          <td>0.0001324</td>
          <td>10100</td>
          <td>9920</td>
          <td>13356</td>
          <td>13628</td>
          <td>30</td>
          <td>13264</td>
          <td>1</td>
          <td>126</td>
          <td>37</td>
          <td>380</td>
          <td>462</td>
          <td>13602</td>
          <td>2795</td>
          <td>22531</td>
          <td>10731</td>
          <td>5642</td>
        </tr>
        <tr>
          <td>Lilly Pulitzer Women&#x27;s Callahan Short</td>
          <td>Lilly Pulitzer</td>
          <td>Shorts</td>
          <td>48.24</td>
          <td>24.35</td>
          <td>106.11</td>
          <td>53.14</td>
          <td>24</td>
          <td>2</td>
          <td>4</td>
          <td>5</td>
          <td>13</td>
          <td>420.02</td>
          <td>207.44</td>
          <td>0.5008</td>
          <td>0.6667</td>
          <td>0.1053</td>
          <td>0.2083</td>
          <td>0.8667</td>
          <td>3.93e-05</td>
          <td>3.8e-05</td>
          <td>0.0001324</td>
          <td>11747</td>
          <td>11307</td>
          <td>7626</td>
          <td>7813</td>
          <td>30</td>
          <td>6114</td>
          <td>30</td>
          <td>24</td>
          <td>31</td>
          <td>883</td>
          <td>1063</td>
          <td>12538</td>
          <td>3055</td>
          <td>22368</td>
          <td>8433</td>
          <td>6056</td>
        </tr>
        <tr>
          <td>Volcom Juniors Pocket Blocket Long Sleeve Tee</td>
          <td>Volcom</td>
          <td>Tops &amp; Tees</td>
          <td>27.0</td>
          <td>15.34</td>
          <td>81.0</td>
          <td>33.86</td>
          <td>21</td>
          <td>3</td>
          <td>4</td>
          <td>5</td>
          <td>9</td>
          <td>243.0</td>
          <td>107.41</td>
          <td>0.418</td>
          <td>0.5714</td>
          <td>0.1875</td>
          <td>0.2381</td>
          <td>0.75</td>
          <td>3e-05</td>
          <td>2.42e-05</td>
          <td>0.0001158</td>
          <td>19072</td>
          <td>17500</td>
          <td>9846</td>
          <td>11622</td>
          <td>50</td>
          <td>2358</td>
          <td>30</td>
          <td>24</td>
          <td>140</td>
          <td>2456</td>
          <td>3131</td>
          <td>20016</td>
          <td>4252</td>
          <td>19354</td>
          <td>7773</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>Tommy Hilfiger Men Classic Fit T-shirt</td>
          <td>Tommy Hilfiger</td>
          <td>Tops &amp; Tees</td>
          <td>21.99</td>
          <td>12.22</td>
          <td>65.97</td>
          <td>28.41</td>
          <td>25</td>
          <td>3</td>
          <td>2</td>
          <td>5</td>
          <td>15</td>
          <td>153.93</td>
          <td>70.63</td>
          <td>0.4307</td>
          <td>0.4</td>
          <td>0.15</td>
          <td>0.2</td>
          <td>0.8333</td>
          <td>2.44e-05</td>
          <td>2.03e-05</td>
          <td>0.0001379</td>
          <td>22049</td>
          <td>20333</td>
          <td>11887</td>
          <td>13165</td>
          <td>21</td>
          <td>2358</td>
          <td>844</td>
          <td>24</td>
          <td>11</td>
          <td>4954</td>
          <td>5704</td>
          <td>18998</td>
          <td>8312</td>
          <td>20814</td>
          <td>8435</td>
          <td>6580</td>
        </tr>
        <tr>
          <td>RSQ London Mens Skinny Jeans</td>
          <td>RSQ</td>
          <td>Jeans</td>
          <td>44.99</td>
          <td>24.2</td>
          <td>134.97</td>
          <td>63.21</td>
          <td>21</td>
          <td>3</td>
          <td>5</td>
          <td>3</td>
          <td>10</td>
          <td>359.92</td>
          <td>163.94</td>
          <td>0.4683</td>
          <td>0.625</td>
          <td>0.1667</td>
          <td>0.1429</td>
          <td>0.7692</td>
          <td>5e-05</td>
          <td>4.52e-05</td>
          <td>0.0001158</td>
          <td>12553</td>
          <td>11383</td>
          <td>5908</td>
          <td>6477</td>
          <td>50</td>
          <td>2358</td>
          <td>5</td>
          <td>526</td>
          <td>77</td>
          <td>1228</td>
          <td>1608</td>
          <td>15636</td>
          <td>4099</td>
          <td>19436</td>
          <td>12706</td>
          <td>9471</td>
        </tr>
        <tr>
          <td>Dockers Men&#x27;s Suit Separate Coat</td>
          <td>Dockers</td>
          <td>Suits &amp; Sport Coats</td>
          <td>88.36</td>
          <td>33.97</td>
          <td>231.12</td>
          <td>140.98</td>
          <td>27</td>
          <td>3</td>
          <td>4</td>
          <td>2</td>
          <td>18</td>
          <td>542.11</td>
          <td>337.6</td>
          <td>0.61</td>
          <td>0.5714</td>
          <td>0.12</td>
          <td>0.0741</td>
          <td>0.8571</td>
          <td>8.56e-05</td>
          <td>0.0001008</td>
          <td>0.0001489</td>
          <td>5094</td>
          <td>7229</td>
          <td>2783</td>
          <td>2122</td>
          <td>12</td>
          <td>2358</td>
          <td>30</td>
          <td>2100</td>
          <td>4</td>
          <td>542</td>
          <td>391</td>
          <td>1873</td>
          <td>4252</td>
          <td>22129</td>
          <td>17370</td>
          <td>6057</td>
        </tr>
        <tr>
          <td>Lee Men&#x27;s Relaxed Fit Slightly Tapered Leg Jean</td>
          <td>Lee</td>
          <td>Jeans</td>
          <td>30.99</td>
          <td>16.89</td>
          <td>122.96</td>
          <td>55.54</td>
          <td>21</td>
          <td>4</td>
          <td>5</td>
          <td>3</td>
          <td>9</td>
          <td>248.92</td>
          <td>113.31</td>
          <td>0.4517</td>
          <td>0.5556</td>
          <td>0.2222</td>
          <td>0.1429</td>
          <td>0.6923</td>
          <td>4.55e-05</td>
          <td>3.97e-05</td>
          <td>0.0001158</td>
          <td>17446</td>
          <td>16178</td>
          <td>6481</td>
          <td>7447</td>
          <td>50</td>
          <td>776</td>
          <td>5</td>
          <td>526</td>
          <td>140</td>
          <td>2405</td>
          <td>2891</td>
          <td>17150</td>
          <td>4274</td>
          <td>17122</td>
          <td>12706</td>
          <td>12966</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Bright Argyle Crew Sock</td>
          <td>HUGO BOSS</td>
          <td>Socks</td>
          <td>9.75</td>
          <td>5.68</td>
          <td>39.0</td>
          <td>15.65</td>
          <td>22</td>
          <td>4</td>
          <td>4</td>
          <td>4</td>
          <td>10</td>
          <td>78.0</td>
          <td>32.25</td>
          <td>0.4013</td>
          <td>0.5</td>
          <td>0.2222</td>
          <td>0.1818</td>
          <td>0.7143</td>
          <td>1.44e-05</td>
          <td>1.12e-05</td>
          <td>0.0001214</td>
          <td>27342</td>
          <td>26355</td>
          <td>16327</td>
          <td>17765</td>
          <td>43</td>
          <td>776</td>
          <td>30</td>
          <td>126</td>
          <td>77</td>
          <td>10368</td>
          <td>12068</td>
          <td>20837</td>
          <td>4275</td>
          <td>17122</td>
          <td>10468</td>
          <td>12035</td>
        </tr>
        <tr>
          <td>RUDE Dark Vintage Skinny Jeans</td>
          <td>Hot Topic</td>
          <td>Jeans</td>
          <td>36.5</td>
          <td>19.33</td>
          <td>146.0</td>
          <td>68.99</td>
          <td>24</td>
          <td>4</td>
          <td>4</td>
          <td>3</td>
          <td>13</td>
          <td>255.5</td>
          <td>123.41</td>
          <td>0.4725</td>
          <td>0.5</td>
          <td>0.1905</td>
          <td>0.125</td>
          <td>0.7647</td>
          <td>5.41e-05</td>
          <td>4.93e-05</td>
          <td>0.0001324</td>
          <td>15396</td>
          <td>14389</td>
          <td>5357</td>
          <td>5845</td>
          <td>30</td>
          <td>776</td>
          <td>30</td>
          <td>526</td>
          <td>31</td>
          <td>2306</td>
          <td>2570</td>
          <td>15319</td>
          <td>4275</td>
          <td>19353</td>
          <td>14338</td>
          <td>9484</td>
        </tr>
        <tr>
          <td>7 For All Mankind Men&#x27;s The Straight Modern Jean</td>
          <td>7 For All Mankind</td>
          <td>Jeans</td>
          <td>175.57</td>
          <td>89.48</td>
          <td>575.0</td>
          <td>267.13</td>
          <td>21</td>
          <td>4</td>
          <td>3</td>
          <td>5</td>
          <td>9</td>
          <td>1447.0</td>
          <td>714.47</td>
          <td>0.4646</td>
          <td>0.4286</td>
          <td>0.25</td>
          <td>0.2381</td>
          <td>0.6923</td>
          <td>0.000213</td>
          <td>0.0001909</td>
          <td>0.0001158</td>
          <td>1310</td>
          <td>1144</td>
          <td>466</td>
          <td>647</td>
          <td>50</td>
          <td>776</td>
          <td>151</td>
          <td>24</td>
          <td>140</td>
          <td>54</td>
          <td>70</td>
          <td>15992</td>
          <td>8270</td>
          <td>14408</td>
          <td>7773</td>
          <td>12966</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s 20X No. 33 Relaxed Straight Leg Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>55.0</td>
          <td>29.66</td>
          <td>220.0</td>
          <td>100.87</td>
          <td>24</td>
          <td>4</td>
          <td>1</td>
          <td>2</td>
          <td>17</td>
          <td>165.0</td>
          <td>74.2</td>
          <td>0.4585</td>
          <td>0.2</td>
          <td>0.1818</td>
          <td>0.0833</td>
          <td>0.8095</td>
          <td>8.15e-05</td>
          <td>7.21e-05</td>
          <td>0.0001324</td>
          <td>9673</td>
          <td>8784</td>
          <td>2941</td>
          <td>3526</td>
          <td>30</td>
          <td>776</td>
          <td>3978</td>
          <td>2100</td>
          <td>6</td>
          <td>4449</td>
          <td>5375</td>
          <td>16533</td>
          <td>12637</td>
          <td>19358</td>
          <td>17144</td>
          <td>7597</td>
        </tr>
        <tr>
          <td>Nike Classic Fleece Hooded Top</td>
          <td>Nike</td>
          <td>Active</td>
          <td>40.62</td>
          <td>16.88</td>
          <td>161.76</td>
          <td>98.38</td>
          <td>21</td>
          <td>4</td>
          <td>2</td>
          <td>2</td>
          <td>13</td>
          <td>162.86</td>
          <td>91.16</td>
          <td>0.6082</td>
          <td>0.3333</td>
          <td>0.2105</td>
          <td>0.0952</td>
          <td>0.7647</td>
          <td>5.99e-05</td>
          <td>7.03e-05</td>
          <td>0.0001158</td>
          <td>13704</td>
          <td>16183</td>
          <td>4588</td>
          <td>3666</td>
          <td>50</td>
          <td>776</td>
          <td>844</td>
          <td>2100</td>
          <td>31</td>
          <td>4548</td>
          <td>4039</td>
          <td>1985</td>
          <td>8752</td>
          <td>17508</td>
          <td>16870</td>
          <td>9484</td>
        </tr>
        <tr>
          <td>New Men&#x27;s Sexy Center Patch Bikini Swimsuit 3G by Gregg Homme</td>
          <td>Gregg Homme</td>
          <td>Swim</td>
          <td>13.22</td>
          <td>7.85</td>
          <td>54.6</td>
          <td>20.64</td>
          <td>25</td>
          <td>4</td>
          <td>2</td>
          <td>5</td>
          <td>14</td>
          <td>90.3</td>
          <td>38.29</td>
          <td>0.378</td>
          <td>0.3333</td>
          <td>0.2</td>
          <td>0.2</td>
          <td>0.7778</td>
          <td>2.02e-05</td>
          <td>1.48e-05</td>
          <td>0.0001379</td>
          <td>25672</td>
          <td>24345</td>
          <td>13422</td>
          <td>15782</td>
          <td>21</td>
          <td>776</td>
          <td>844</td>
          <td>24</td>
          <td>22</td>
          <td>8973</td>
          <td>10649</td>
          <td>21721</td>
          <td>8752</td>
          <td>17510</td>
          <td>8435</td>
          <td>9281</td>
        </tr>
        <tr>
          <td>Levi&#x27;s Men&#x27;s Wool Melton Peacoat</td>
          <td>Levi&#x27;s</td>
          <td>Outerwear &amp; Coats</td>
          <td>103.99</td>
          <td>47.71</td>
          <td>415.98</td>
          <td>225.14</td>
          <td>22</td>
          <td>4</td>
          <td>3</td>
          <td>3</td>
          <td>12</td>
          <td>623.97</td>
          <td>337.71</td>
          <td>0.5412</td>
          <td>0.4286</td>
          <td>0.2105</td>
          <td>0.1364</td>
          <td>0.75</td>
          <td>0.0001541</td>
          <td>0.0001609</td>
          <td>0.0001214</td>
          <td>3776</td>
          <td>4133</td>
          <td>937</td>
          <td>912</td>
          <td>43</td>
          <td>776</td>
          <td>151</td>
          <td>526</td>
          <td>37</td>
          <td>393</td>
          <td>389</td>
          <td>8481</td>
          <td>8270</td>
          <td>17508</td>
          <td>14315</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>WeSC Men&#x27;s Eddy Chino Pant</td>
          <td>WESC</td>
          <td>Pants</td>
          <td>73.62</td>
          <td>33.02</td>
          <td>300.95</td>
          <td>165.16</td>
          <td>25</td>
          <td>4</td>
          <td>2</td>
          <td>7</td>
          <td>12</td>
          <td>657.75</td>
          <td>363.33</td>
          <td>0.5488</td>
          <td>0.3333</td>
          <td>0.2222</td>
          <td>0.28</td>
          <td>0.75</td>
          <td>0.0001115</td>
          <td>0.000118</td>
          <td>0.0001379</td>
          <td>6601</td>
          <td>7527</td>
          <td>1711</td>
          <td>1625</td>
          <td>21</td>
          <td>776</td>
          <td>844</td>
          <td>2</td>
          <td>37</td>
          <td>350</td>
          <td>333</td>
          <td>7797</td>
          <td>8752</td>
          <td>17122</td>
          <td>5404</td>
          <td>9487</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by Units Returned</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>TapouT Men&#x27;s Lock Up Hoodie</td>
          <td>TapouT</td>
          <td>Fashion Hoodies &amp; Sweatshirts</td>
          <td>36.61</td>
          <td>20.6</td>
          <td>229.12</td>
          <td>103.62</td>
          <td>23</td>
          <td>7</td>
          <td>0</td>
          <td>1</td>
          <td>15</td>
          <td>39.6</td>
          <td>16.16</td>
          <td>0.4523</td>
          <td>0.0</td>
          <td>0.3182</td>
          <td>0.0435</td>
          <td>0.6818</td>
          <td>8.49e-05</td>
          <td>7.41e-05</td>
          <td>0.0001269</td>
          <td>15388</td>
          <td>13556</td>
          <td>2822</td>
          <td>3414</td>
          <td>41</td>
          <td>33</td>
          <td>13463</td>
          <td>7029</td>
          <td>11</td>
          <td>16416</td>
          <td>17785</td>
          <td>17057</td>
          <td>13463</td>
          <td>13008</td>
          <td>17454</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Long Pant</td>
          <td>HUGO BOSS</td>
          <td>Sleep &amp; Lounge</td>
          <td>74.72</td>
          <td>28.3</td>
          <td>1033.11</td>
          <td>648.16</td>
          <td>33</td>
          <td>14</td>
          <td>0</td>
          <td>3</td>
          <td>16</td>
          <td>233.01</td>
          <td>138.21</td>
          <td>0.6274</td>
          <td>0.0</td>
          <td>0.4667</td>
          <td>0.0909</td>
          <td>0.5333</td>
          <td>0.0003827</td>
          <td>0.0004632</td>
          <td>0.000182</td>
          <td>6501</td>
          <td>9383</td>
          <td>113</td>
          <td>75</td>
          <td>6</td>
          <td>1</td>
          <td>13463</td>
          <td>526</td>
          <td>7</td>
          <td>2702</td>
          <td>2165</td>
          <td>933</td>
          <td>13463</td>
          <td>6418</td>
          <td>16872</td>
          <td>19494</td>
        </tr>
        <tr>
          <td>Joe&#x27;s Jeans Men&#x27;s Rebel Relaxed Fit Jean</td>
          <td>Joe&#x27;s Jeans</td>
          <td>Jeans</td>
          <td>139.29</td>
          <td>76.13</td>
          <td>1296.69</td>
          <td>583.03</td>
          <td>26</td>
          <td>9</td>
          <td>0</td>
          <td>3</td>
          <td>14</td>
          <td>339.69</td>
          <td>166.11</td>
          <td>0.4496</td>
          <td>0.0</td>
          <td>0.3913</td>
          <td>0.1154</td>
          <td>0.6087</td>
          <td>0.0004803</td>
          <td>0.0004167</td>
          <td>0.0001434</td>
          <td>2334</td>
          <td>1721</td>
          <td>68</td>
          <td>102</td>
          <td>17</td>
          <td>5</td>
          <td>13463</td>
          <td>526</td>
          <td>22</td>
          <td>1403</td>
          <td>1558</td>
          <td>17357</td>
          <td>13463</td>
          <td>9082</td>
          <td>15567</td>
          <td>16952</td>
        </tr>
        <tr>
          <td>Diesel Men&#x27;s Blade Underpant</td>
          <td>Diesel</td>
          <td>Underwear</td>
          <td>22.14</td>
          <td>9.75</td>
          <td>122.0</td>
          <td>66.53</td>
          <td>22</td>
          <td>6</td>
          <td>0</td>
          <td>2</td>
          <td>14</td>
          <td>43.0</td>
          <td>23.83</td>
          <td>0.5453</td>
          <td>0.0</td>
          <td>0.3</td>
          <td>0.0909</td>
          <td>0.7</td>
          <td>4.52e-05</td>
          <td>4.75e-05</td>
          <td>0.0001214</td>
          <td>21886</td>
          <td>22702</td>
          <td>6504</td>
          <td>6114</td>
          <td>43</td>
          <td>84</td>
          <td>13463</td>
          <td>2100</td>
          <td>22</td>
          <td>15676</td>
          <td>14732</td>
          <td>8115</td>
          <td>13463</td>
          <td>13033</td>
          <td>16872</td>
          <td>12849</td>
        </tr>
        <tr>
          <td>Ray-Ban Women&#x27;s 4101 Jackie Ohh Sunglasses</td>
          <td>Ray-Ban</td>
          <td>Accessories</td>
          <td>97.5</td>
          <td>41.94</td>
          <td>486.16</td>
          <td>280.13</td>
          <td>22</td>
          <td>5</td>
          <td>1</td>
          <td>5</td>
          <td>11</td>
          <td>586.32</td>
          <td>330.97</td>
          <td>0.5762</td>
          <td>0.1667</td>
          <td>0.2941</td>
          <td>0.2273</td>
          <td>0.6875</td>
          <td>0.0001801</td>
          <td>0.0002002</td>
          <td>0.0001214</td>
          <td>4451</td>
          <td>5084</td>
          <td>706</td>
          <td>587</td>
          <td>43</td>
          <td>251</td>
          <td>3978</td>
          <td>24</td>
          <td>43</td>
          <td>472</td>
          <td>408</td>
          <td>4708</td>
          <td>13196</td>
          <td>13232</td>
          <td>7836</td>
          <td>12983</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s 20X No. 33 Relaxed Straight Leg Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>55.0</td>
          <td>29.66</td>
          <td>220.0</td>
          <td>100.87</td>
          <td>24</td>
          <td>4</td>
          <td>1</td>
          <td>2</td>
          <td>17</td>
          <td>165.0</td>
          <td>74.2</td>
          <td>0.4585</td>
          <td>0.2</td>
          <td>0.1818</td>
          <td>0.0833</td>
          <td>0.8095</td>
          <td>8.15e-05</td>
          <td>7.21e-05</td>
          <td>0.0001324</td>
          <td>9673</td>
          <td>8784</td>
          <td>2941</td>
          <td>3526</td>
          <td>30</td>
          <td>776</td>
          <td>3978</td>
          <td>2100</td>
          <td>6</td>
          <td>4449</td>
          <td>5375</td>
          <td>16533</td>
          <td>12637</td>
          <td>19358</td>
          <td>17144</td>
          <td>7597</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Sarasota Agility Short</td>
          <td>Wrangler</td>
          <td>Shorts</td>
          <td>33.03</td>
          <td>16.36</td>
          <td>198.95</td>
          <td>101.37</td>
          <td>25</td>
          <td>6</td>
          <td>1</td>
          <td>3</td>
          <td>15</td>
          <td>138.97</td>
          <td>68.68</td>
          <td>0.5095</td>
          <td>0.1429</td>
          <td>0.2727</td>
          <td>0.12</td>
          <td>0.7143</td>
          <td>7.37e-05</td>
          <td>7.24e-05</td>
          <td>0.0001379</td>
          <td>16765</td>
          <td>16618</td>
          <td>3447</td>
          <td>3505</td>
          <td>21</td>
          <td>84</td>
          <td>3978</td>
          <td>526</td>
          <td>11</td>
          <td>5758</td>
          <td>5901</td>
          <td>11606</td>
          <td>13389</td>
          <td>14284</td>
          <td>15549</td>
          <td>12035</td>
        </tr>
        <tr>
          <td>True Religion Men&#x27;s Ricky Straight Leg Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>227.86</td>
          <td>123.14</td>
          <td>1452.0</td>
          <td>661.01</td>
          <td>28</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>15</td>
          <td>1430.0</td>
          <td>645.85</td>
          <td>0.4552</td>
          <td>0.125</td>
          <td>0.3043</td>
          <td>0.1786</td>
          <td>0.6818</td>
          <td>0.0005379</td>
          <td>0.0004724</td>
          <td>0.0001545</td>
          <td>646</td>
          <td>406</td>
          <td>45</td>
          <td>69</td>
          <td>9</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>11</td>
          <td>57</td>
          <td>95</td>
          <td>16801</td>
          <td>13444</td>
          <td>13032</td>
          <td>10715</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Fred Perry Men&#x27;s Crew Neck Sweater</td>
          <td>Fred Perry</td>
          <td>Sweaters</td>
          <td>104.69</td>
          <td>54.65</td>
          <td>815.72</td>
          <td>392.52</td>
          <td>24</td>
          <td>8</td>
          <td>1</td>
          <td>1</td>
          <td>14</td>
          <td>214.74</td>
          <td>106.77</td>
          <td>0.4812</td>
          <td>0.1111</td>
          <td>0.3478</td>
          <td>0.0417</td>
          <td>0.6364</td>
          <td>0.0003022</td>
          <td>0.0002805</td>
          <td>0.0001324</td>
          <td>3741</td>
          <td>3335</td>
          <td>188</td>
          <td>264</td>
          <td>30</td>
          <td>16</td>
          <td>3978</td>
          <td>7029</td>
          <td>22</td>
          <td>3010</td>
          <td>3162</td>
          <td>14461</td>
          <td>13456</td>
          <td>9743</td>
          <td>17456</td>
          <td>16487</td>
        </tr>
        <tr>
          <td>Volcom Men&#x27;s Vorta Slim Straight Leg Fit Jean</td>
          <td>Volcom</td>
          <td>Jeans</td>
          <td>73.57</td>
          <td>41.13</td>
          <td>574.85</td>
          <td>249.86</td>
          <td>27</td>
          <td>8</td>
          <td>1</td>
          <td>4</td>
          <td>14</td>
          <td>387.8</td>
          <td>166.89</td>
          <td>0.4347</td>
          <td>0.1111</td>
          <td>0.3478</td>
          <td>0.1481</td>
          <td>0.6364</td>
          <td>0.0002129</td>
          <td>0.0001786</td>
          <td>0.0001489</td>
          <td>6603</td>
          <td>5251</td>
          <td>467</td>
          <td>746</td>
          <td>12</td>
          <td>16</td>
          <td>3978</td>
          <td>126</td>
          <td>22</td>
          <td>1091</td>
          <td>1537</td>
          <td>18678</td>
          <td>13456</td>
          <td>9743</td>
          <td>12705</td>
          <td>16487</td>
        </tr>
        <tr>
          <td>Puma Men&#x27;s Socks</td>
          <td>PUMA</td>
          <td>Socks</td>
          <td>13.0</td>
          <td>7.78</td>
          <td>90.0</td>
          <td>35.98</td>
          <td>24</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>11</td>
          <td>78.0</td>
          <td>31.36</td>
          <td>0.3998</td>
          <td>0.125</td>
          <td>0.3684</td>
          <td>0.2083</td>
          <td>0.6111</td>
          <td>3.33e-05</td>
          <td>2.57e-05</td>
          <td>0.0001324</td>
          <td>25705</td>
          <td>24414</td>
          <td>8929</td>
          <td>11107</td>
          <td>30</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>43</td>
          <td>10368</td>
          <td>12295</td>
          <td>20955</td>
          <td>13444</td>
          <td>9637</td>
          <td>8433</td>
          <td>16951</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Genuine Tampa Cargo Short</td>
          <td>Wrangler</td>
          <td>Shorts</td>
          <td>31.37</td>
          <td>15.61</td>
          <td>229.94</td>
          <td>116.44</td>
          <td>29</td>
          <td>7</td>
          <td>1</td>
          <td>5</td>
          <td>16</td>
          <td>179.94</td>
          <td>90.54</td>
          <td>0.5064</td>
          <td>0.125</td>
          <td>0.2917</td>
          <td>0.1724</td>
          <td>0.6957</td>
          <td>8.52e-05</td>
          <td>8.32e-05</td>
          <td>0.00016</td>
          <td>17403</td>
          <td>17266</td>
          <td>2818</td>
          <td>2869</td>
          <td>8</td>
          <td>33</td>
          <td>3978</td>
          <td>24</td>
          <td>7</td>
          <td>3935</td>
          <td>4081</td>
          <td>11924</td>
          <td>13444</td>
          <td>13236</td>
          <td>10730</td>
          <td>12964</td>
        </tr>
        <tr>
          <td>Bottoms Out Men&#x27;s Plaid Sleep Pant</td>
          <td>Bottoms Out</td>
          <td>Sleep &amp; Lounge</td>
          <td>13.49</td>
          <td>5.05</td>
          <td>94.43</td>
          <td>59.4</td>
          <td>25</td>
          <td>7</td>
          <td>2</td>
          <td>4</td>
          <td>12</td>
          <td>80.94</td>
          <td>50.64</td>
          <td>0.629</td>
          <td>0.2222</td>
          <td>0.3333</td>
          <td>0.16</td>
          <td>0.6316</td>
          <td>3.5e-05</td>
          <td>4.25e-05</td>
          <td>0.0001379</td>
          <td>25625</td>
          <td>26913</td>
          <td>8758</td>
          <td>6904</td>
          <td>21</td>
          <td>33</td>
          <td>844</td>
          <td>126</td>
          <td>37</td>
          <td>9890</td>
          <td>8299</td>
          <td>839</td>
          <td>12628</td>
          <td>9747</td>
          <td>12630</td>
          <td>16546</td>
        </tr>
        <tr>
          <td>JiMarti JM01 Sunglasses for Golf Fishing Cycling-Unbreakable-... Frame</td>
          <td>JiMarti</td>
          <td>Accessories</td>
          <td>29.95</td>
          <td>11.92</td>
          <td>269.55</td>
          <td>161.1</td>
          <td>22</td>
          <td>9</td>
          <td>2</td>
          <td>2</td>
          <td>9</td>
          <td>119.8</td>
          <td>72.12</td>
          <td>0.5977</td>
          <td>0.1818</td>
          <td>0.45</td>
          <td>0.0909</td>
          <td>0.5</td>
          <td>9.99e-05</td>
          <td>0.0001151</td>
          <td>0.0001214</td>
          <td>18166</td>
          <td>20613</td>
          <td>2175</td>
          <td>1707</td>
          <td>43</td>
          <td>5</td>
          <td>844</td>
          <td>2100</td>
          <td>140</td>
          <td>6868</td>
          <td>5540</td>
          <td>2758</td>
          <td>13193</td>
          <td>6490</td>
          <td>16872</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Premium Performance Cowboy Cut Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>47.45</td>
          <td>25.88</td>
          <td>570.83</td>
          <td>264.22</td>
          <td>58</td>
          <td>12</td>
          <td>2</td>
          <td>7</td>
          <td>37</td>
          <td>417.81</td>
          <td>189.65</td>
          <td>0.4629</td>
          <td>0.1429</td>
          <td>0.2353</td>
          <td>0.1207</td>
          <td>0.7551</td>
          <td>0.0002115</td>
          <td>0.0001888</td>
          <td>0.00032</td>
          <td>12004</td>
          <td>10508</td>
          <td>470</td>
          <td>662</td>
          <td>1</td>
          <td>2</td>
          <td>844</td>
          <td>2</td>
          <td>1</td>
          <td>905</td>
          <td>1224</td>
          <td>16149</td>
          <td>13389</td>
          <td>17092</td>
          <td>15548</td>
          <td>9486</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by Units Cancelled</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
  units_cancelled_rank DESC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>State O Maine Big and Tall Fashion Flannel Pajama</td>
          <td>KNOTHE CORP.</td>
          <td>Sleep &amp; Lounge</td>
          <td>36.88</td>
          <td>15.59</td>
          <td>331.92</td>
          <td>192.51</td>
          <td>21</td>
          <td>9</td>
          <td>5</td>
          <td>1</td>
          <td>6</td>
          <td>221.28</td>
          <td>127.31</td>
          <td>0.58</td>
          <td>0.3571</td>
          <td>0.45</td>
          <td>0.0476</td>
          <td>0.4</td>
          <td>0.000123</td>
          <td>0.0001376</td>
          <td>0.0001158</td>
          <td>15350</td>
          <td>17283</td>
          <td>1492</td>
          <td>1214</td>
          <td>50</td>
          <td>5</td>
          <td>5</td>
          <td>7029</td>
          <td>1398</td>
          <td>2854</td>
          <td>2454</td>
          <td>4293</td>
          <td>8749</td>
          <td>6490</td>
          <td>17453</td>
          <td>23875</td>
        </tr>
        <tr>
          <td>Chaps Big and Tall Solid V-Neck Vest</td>
          <td>Chaps</td>
          <td>Sweaters</td>
          <td>39.88</td>
          <td>20.32</td>
          <td>279.16</td>
          <td>134.91</td>
          <td>28</td>
          <td>7</td>
          <td>4</td>
          <td>1</td>
          <td>16</td>
          <td>199.4</td>
          <td>99.06</td>
          <td>0.4833</td>
          <td>0.3636</td>
          <td>0.2593</td>
          <td>0.0357</td>
          <td>0.6957</td>
          <td>0.0001034</td>
          <td>9.64e-05</td>
          <td>0.0001545</td>
          <td>14437</td>
          <td>13747</td>
          <td>2029</td>
          <td>2288</td>
          <td>9</td>
          <td>33</td>
          <td>30</td>
          <td>7029</td>
          <td>7</td>
          <td>3354</td>
          <td>3543</td>
          <td>14237</td>
          <td>8748</td>
          <td>14407</td>
          <td>17457</td>
          <td>12964</td>
        </tr>
        <tr>
          <td>TapouT Men&#x27;s Lock Up Hoodie</td>
          <td>TapouT</td>
          <td>Fashion Hoodies &amp; Sweatshirts</td>
          <td>36.61</td>
          <td>20.6</td>
          <td>229.12</td>
          <td>103.62</td>
          <td>23</td>
          <td>7</td>
          <td>0</td>
          <td>1</td>
          <td>15</td>
          <td>39.6</td>
          <td>16.16</td>
          <td>0.4523</td>
          <td>0.0</td>
          <td>0.3182</td>
          <td>0.0435</td>
          <td>0.6818</td>
          <td>8.49e-05</td>
          <td>7.41e-05</td>
          <td>0.0001269</td>
          <td>15388</td>
          <td>13556</td>
          <td>2822</td>
          <td>3414</td>
          <td>41</td>
          <td>33</td>
          <td>13463</td>
          <td>7029</td>
          <td>11</td>
          <td>16416</td>
          <td>17785</td>
          <td>17057</td>
          <td>13463</td>
          <td>13008</td>
          <td>17454</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Fred Perry Men&#x27;s Crew Neck Sweater</td>
          <td>Fred Perry</td>
          <td>Sweaters</td>
          <td>104.69</td>
          <td>54.65</td>
          <td>815.72</td>
          <td>392.52</td>
          <td>24</td>
          <td>8</td>
          <td>1</td>
          <td>1</td>
          <td>14</td>
          <td>214.74</td>
          <td>106.77</td>
          <td>0.4812</td>
          <td>0.1111</td>
          <td>0.3478</td>
          <td>0.0417</td>
          <td>0.6364</td>
          <td>0.0003022</td>
          <td>0.0002805</td>
          <td>0.0001324</td>
          <td>3741</td>
          <td>3335</td>
          <td>188</td>
          <td>264</td>
          <td>30</td>
          <td>16</td>
          <td>3978</td>
          <td>7029</td>
          <td>22</td>
          <td>3010</td>
          <td>3162</td>
          <td>14461</td>
          <td>13456</td>
          <td>9743</td>
          <td>17456</td>
          <td>16487</td>
        </tr>
        <tr>
          <td>KAMALIKULTURE Women&#x27;s Long Sleeve Side Draped Dress</td>
          <td>KAMALIKULTURE</td>
          <td>Dresses</td>
          <td>83.65</td>
          <td>40.23</td>
          <td>467.96</td>
          <td>240.96</td>
          <td>23</td>
          <td>6</td>
          <td>2</td>
          <td>1</td>
          <td>14</td>
          <td>233.98</td>
          <td>119.93</td>
          <td>0.5149</td>
          <td>0.25</td>
          <td>0.2727</td>
          <td>0.0435</td>
          <td>0.7</td>
          <td>0.0001734</td>
          <td>0.0001722</td>
          <td>0.0001269</td>
          <td>5490</td>
          <td>5477</td>
          <td>768</td>
          <td>793</td>
          <td>41</td>
          <td>84</td>
          <td>844</td>
          <td>7029</td>
          <td>22</td>
          <td>2696</td>
          <td>2677</td>
          <td>11003</td>
          <td>11344</td>
          <td>14284</td>
          <td>17454</td>
          <td>12849</td>
        </tr>
        <tr>
          <td>Nike Classic Fleece Hooded Top</td>
          <td>Nike</td>
          <td>Active</td>
          <td>40.62</td>
          <td>16.88</td>
          <td>161.76</td>
          <td>98.38</td>
          <td>21</td>
          <td>4</td>
          <td>2</td>
          <td>2</td>
          <td>13</td>
          <td>162.86</td>
          <td>91.16</td>
          <td>0.6082</td>
          <td>0.3333</td>
          <td>0.2105</td>
          <td>0.0952</td>
          <td>0.7647</td>
          <td>5.99e-05</td>
          <td>7.03e-05</td>
          <td>0.0001158</td>
          <td>13704</td>
          <td>16183</td>
          <td>4588</td>
          <td>3666</td>
          <td>50</td>
          <td>776</td>
          <td>844</td>
          <td>2100</td>
          <td>31</td>
          <td>4548</td>
          <td>4039</td>
          <td>1985</td>
          <td>8752</td>
          <td>17508</td>
          <td>16870</td>
          <td>9484</td>
        </tr>
        <tr>
          <td>UltraClub Adult Sherpa-Lined Full-Zip Fleece with Hood</td>
          <td>UltraClub</td>
          <td>Fashion Hoodies &amp; Sweatshirts</td>
          <td>51.47</td>
          <td>28.47</td>
          <td>360.9</td>
          <td>161.23</td>
          <td>26</td>
          <td>7</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>203.71</td>
          <td>91.12</td>
          <td>0.4467</td>
          <td>0.2222</td>
          <td>0.2917</td>
          <td>0.0769</td>
          <td>0.6818</td>
          <td>0.0001337</td>
          <td>0.0001152</td>
          <td>0.0001434</td>
          <td>10603</td>
          <td>9302</td>
          <td>1222</td>
          <td>1705</td>
          <td>17</td>
          <td>33</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>3228</td>
          <td>4041</td>
          <td>17630</td>
          <td>12628</td>
          <td>13236</td>
          <td>17286</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Joseph Abboud Men&#x27;s Two-button Side Vent Sport Coat</td>
          <td>Joseph Abboud</td>
          <td>Suits &amp; Sport Coats</td>
          <td>264.0</td>
          <td>101.9</td>
          <td>2904.0</td>
          <td>1759.82</td>
          <td>30</td>
          <td>11</td>
          <td>2</td>
          <td>2</td>
          <td>15</td>
          <td>1056.0</td>
          <td>656.57</td>
          <td>0.606</td>
          <td>0.1538</td>
          <td>0.3929</td>
          <td>0.0667</td>
          <td>0.5769</td>
          <td>0.0010758</td>
          <td>0.0012577</td>
          <td>0.0001655</td>
          <td>430</td>
          <td>734</td>
          <td>6</td>
          <td>5</td>
          <td>7</td>
          <td>3</td>
          <td>844</td>
          <td>2100</td>
          <td>11</td>
          <td>112</td>
          <td>91</td>
          <td>2144</td>
          <td>13388</td>
          <td>9081</td>
          <td>17408</td>
          <td>18610</td>
        </tr>
        <tr>
          <td>State O Maine Big and Tall Solid Microfleece Lounge Pant</td>
          <td>KNOTHE CORP.</td>
          <td>Sleep &amp; Lounge</td>
          <td>26.99</td>
          <td>10.37</td>
          <td>161.94</td>
          <td>101.75</td>
          <td>24</td>
          <td>6</td>
          <td>2</td>
          <td>2</td>
          <td>14</td>
          <td>107.96</td>
          <td>69.2</td>
          <td>0.6283</td>
          <td>0.25</td>
          <td>0.2727</td>
          <td>0.0833</td>
          <td>0.7</td>
          <td>6e-05</td>
          <td>7.27e-05</td>
          <td>0.0001324</td>
          <td>19125</td>
          <td>22140</td>
          <td>4586</td>
          <td>3491</td>
          <td>30</td>
          <td>84</td>
          <td>844</td>
          <td>2100</td>
          <td>22</td>
          <td>7621</td>
          <td>5851</td>
          <td>878</td>
          <td>11344</td>
          <td>14284</td>
          <td>17144</td>
          <td>12849</td>
        </tr>
        <tr>
          <td>Lucky Brand Mens Men&#x27;s 361 Vintage Straight Denim Jean</td>
          <td>Lucky Brand</td>
          <td>Jeans</td>
          <td>99.0</td>
          <td>52.65</td>
          <td>594.0</td>
          <td>275.91</td>
          <td>25</td>
          <td>6</td>
          <td>3</td>
          <td>2</td>
          <td>14</td>
          <td>495.0</td>
          <td>228.59</td>
          <td>0.4645</td>
          <td>0.3333</td>
          <td>0.2609</td>
          <td>0.08</td>
          <td>0.7</td>
          <td>0.00022</td>
          <td>0.0001972</td>
          <td>0.0001379</td>
          <td>4113</td>
          <td>3525</td>
          <td>427</td>
          <td>608</td>
          <td>21</td>
          <td>84</td>
          <td>151</td>
          <td>2100</td>
          <td>22</td>
          <td>674</td>
          <td>896</td>
          <td>15993</td>
          <td>8752</td>
          <td>14406</td>
          <td>17285</td>
          <td>12849</td>
        </tr>
        <tr>
          <td>Joe&#x27;s Jeans Men&#x27;s Slim Fit Straight Leg Brixton</td>
          <td>Joe&#x27;s Jeans</td>
          <td>Jeans</td>
          <td>194.26</td>
          <td>102.07</td>
          <td>1353.0</td>
          <td>647.44</td>
          <td>27</td>
          <td>7</td>
          <td>3</td>
          <td>2</td>
          <td>15</td>
          <td>976.0</td>
          <td>458.49</td>
          <td>0.4785</td>
          <td>0.3</td>
          <td>0.28</td>
          <td>0.0741</td>
          <td>0.6818</td>
          <td>0.0005012</td>
          <td>0.0004627</td>
          <td>0.0001489</td>
          <td>992</td>
          <td>729</td>
          <td>58</td>
          <td>76</td>
          <td>12</td>
          <td>33</td>
          <td>151</td>
          <td>2100</td>
          <td>11</td>
          <td>133</td>
          <td>207</td>
          <td>14773</td>
          <td>11276</td>
          <td>14282</td>
          <td>17370</td>
          <td>12986</td>
        </tr>
        <tr>
          <td>Rusty Men&#x27;s Goombah Too Boardshort</td>
          <td>Rusty</td>
          <td>Swim</td>
          <td>54.5</td>
          <td>32.55</td>
          <td>272.5</td>
          <td>108.89</td>
          <td>21</td>
          <td>5</td>
          <td>3</td>
          <td>2</td>
          <td>11</td>
          <td>272.5</td>
          <td>107.04</td>
          <td>0.3996</td>
          <td>0.375</td>
          <td>0.2632</td>
          <td>0.0952</td>
          <td>0.6875</td>
          <td>0.0001009</td>
          <td>7.78e-05</td>
          <td>0.0001158</td>
          <td>10044</td>
          <td>7672</td>
          <td>2094</td>
          <td>3171</td>
          <td>50</td>
          <td>251</td>
          <td>151</td>
          <td>2100</td>
          <td>43</td>
          <td>2048</td>
          <td>3147</td>
          <td>20957</td>
          <td>8725</td>
          <td>14405</td>
          <td>16870</td>
          <td>12983</td>
        </tr>
        <tr>
          <td>Van Heusen Men&#x27;s Tall Wrinkle Free Poplin Long Sleeve Shirt</td>
          <td>Van Heusen</td>
          <td>Tops &amp; Tees</td>
          <td>36.73</td>
          <td>20.07</td>
          <td>225.42</td>
          <td>102.03</td>
          <td>22</td>
          <td>6</td>
          <td>3</td>
          <td>2</td>
          <td>11</td>
          <td>192.47</td>
          <td>86.91</td>
          <td>0.4526</td>
          <td>0.3333</td>
          <td>0.3</td>
          <td>0.0909</td>
          <td>0.6471</td>
          <td>8.35e-05</td>
          <td>7.29e-05</td>
          <td>0.0001214</td>
          <td>15384</td>
          <td>13898</td>
          <td>2852</td>
          <td>3476</td>
          <td>43</td>
          <td>84</td>
          <td>151</td>
          <td>2100</td>
          <td>43</td>
          <td>3601</td>
          <td>4316</td>
          <td>17055</td>
          <td>8752</td>
          <td>13033</td>
          <td>16872</td>
          <td>16473</td>
        </tr>
        <tr>
          <td>Diesel Men&#x27;s Blade Underpant</td>
          <td>Diesel</td>
          <td>Underwear</td>
          <td>22.14</td>
          <td>9.75</td>
          <td>122.0</td>
          <td>66.53</td>
          <td>22</td>
          <td>6</td>
          <td>0</td>
          <td>2</td>
          <td>14</td>
          <td>43.0</td>
          <td>23.83</td>
          <td>0.5453</td>
          <td>0.0</td>
          <td>0.3</td>
          <td>0.0909</td>
          <td>0.7</td>
          <td>4.52e-05</td>
          <td>4.75e-05</td>
          <td>0.0001214</td>
          <td>21886</td>
          <td>22702</td>
          <td>6504</td>
          <td>6114</td>
          <td>43</td>
          <td>84</td>
          <td>13463</td>
          <td>2100</td>
          <td>22</td>
          <td>15676</td>
          <td>14732</td>
          <td>8115</td>
          <td>13463</td>
          <td>13033</td>
          <td>16872</td>
          <td>12849</td>
        </tr>
        <tr>
          <td>Dockers Men&#x27;s Suit Separate Coat</td>
          <td>Dockers</td>
          <td>Suits &amp; Sport Coats</td>
          <td>88.36</td>
          <td>33.97</td>
          <td>231.12</td>
          <td>140.98</td>
          <td>27</td>
          <td>3</td>
          <td>4</td>
          <td>2</td>
          <td>18</td>
          <td>542.11</td>
          <td>337.6</td>
          <td>0.61</td>
          <td>0.5714</td>
          <td>0.12</td>
          <td>0.0741</td>
          <td>0.8571</td>
          <td>8.56e-05</td>
          <td>0.0001008</td>
          <td>0.0001489</td>
          <td>5094</td>
          <td>7229</td>
          <td>2783</td>
          <td>2122</td>
          <td>12</td>
          <td>2358</td>
          <td>30</td>
          <td>2100</td>
          <td>4</td>
          <td>542</td>
          <td>391</td>
          <td>1873</td>
          <td>4252</td>
          <td>22129</td>
          <td>17370</td>
          <td>6057</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by Units En Route</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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
  units_en_route_rank DESC
LIMIT 15;</code></pre>


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>State O Maine Big and Tall Fashion Flannel Pajama</td>
          <td>KNOTHE CORP.</td>
          <td>Sleep &amp; Lounge</td>
          <td>36.88</td>
          <td>15.59</td>
          <td>331.92</td>
          <td>192.51</td>
          <td>21</td>
          <td>9</td>
          <td>5</td>
          <td>1</td>
          <td>6</td>
          <td>221.28</td>
          <td>127.31</td>
          <td>0.58</td>
          <td>0.3571</td>
          <td>0.45</td>
          <td>0.0476</td>
          <td>0.4</td>
          <td>0.000123</td>
          <td>0.0001376</td>
          <td>0.0001158</td>
          <td>15350</td>
          <td>17283</td>
          <td>1492</td>
          <td>1214</td>
          <td>50</td>
          <td>5</td>
          <td>5</td>
          <td>7029</td>
          <td>1398</td>
          <td>2854</td>
          <td>2454</td>
          <td>4293</td>
          <td>8749</td>
          <td>6490</td>
          <td>17453</td>
          <td>23875</td>
        </tr>
        <tr>
          <td>Levi&#x27;s Women&#x27;s Demi Curve Slim Fit Jean</td>
          <td>Levi&#x27;s</td>
          <td>Jeans</td>
          <td>44.99</td>
          <td>25.36</td>
          <td>359.92</td>
          <td>158.59</td>
          <td>22</td>
          <td>8</td>
          <td>5</td>
          <td>3</td>
          <td>6</td>
          <td>359.92</td>
          <td>157.29</td>
          <td>0.4406</td>
          <td>0.3846</td>
          <td>0.4211</td>
          <td>0.1364</td>
          <td>0.4286</td>
          <td>0.0001333</td>
          <td>0.0001133</td>
          <td>0.0001214</td>
          <td>12553</td>
          <td>10773</td>
          <td>1272</td>
          <td>1757</td>
          <td>43</td>
          <td>16</td>
          <td>5</td>
          <td>526</td>
          <td>1398</td>
          <td>1228</td>
          <td>1730</td>
          <td>18170</td>
          <td>8724</td>
          <td>7452</td>
          <td>14315</td>
          <td>23541</td>
        </tr>
        <tr>
          <td>7 For All Mankind Women&#x27;s Roxanne Slim Fit Jean</td>
          <td>7 For All Mankind</td>
          <td>Jeans</td>
          <td>173.19</td>
          <td>90.65</td>
          <td>863.98</td>
          <td>407.88</td>
          <td>21</td>
          <td>5</td>
          <td>4</td>
          <td>5</td>
          <td>7</td>
          <td>1495.96</td>
          <td>719.25</td>
          <td>0.4721</td>
          <td>0.4444</td>
          <td>0.3125</td>
          <td>0.2381</td>
          <td>0.5833</td>
          <td>0.0003201</td>
          <td>0.0002915</td>
          <td>0.0001158</td>
          <td>1348</td>
          <td>1093</td>
          <td>169</td>
          <td>237</td>
          <td>50</td>
          <td>251</td>
          <td>30</td>
          <td>24</td>
          <td>623</td>
          <td>48</td>
          <td>67</td>
          <td>15325</td>
          <td>8264</td>
          <td>13009</td>
          <td>7773</td>
          <td>18592</td>
        </tr>
        <tr>
          <td>Original Penguin Men&#x27;s Volley Swim Short</td>
          <td>Original Penguin</td>
          <td>Swim</td>
          <td>69.0</td>
          <td>42.12</td>
          <td>483.0</td>
          <td>190.09</td>
          <td>21</td>
          <td>7</td>
          <td>3</td>
          <td>3</td>
          <td>8</td>
          <td>414.0</td>
          <td>160.42</td>
          <td>0.3936</td>
          <td>0.3</td>
          <td>0.3889</td>
          <td>0.1429</td>
          <td>0.5333</td>
          <td>0.0001789</td>
          <td>0.0001359</td>
          <td>0.0001158</td>
          <td>7231</td>
          <td>5048</td>
          <td>713</td>
          <td>1236</td>
          <td>50</td>
          <td>33</td>
          <td>151</td>
          <td>526</td>
          <td>295</td>
          <td>914</td>
          <td>1664</td>
          <td>21241</td>
          <td>11276</td>
          <td>9083</td>
          <td>12706</td>
          <td>19494</td>
        </tr>
        <tr>
          <td>Wrangler Men&#x27;s Original Cowboy Cut Relaxed Fit Jean</td>
          <td>Wrangler</td>
          <td>Jeans</td>
          <td>42.99</td>
          <td>22.67</td>
          <td>228.46</td>
          <td>108.63</td>
          <td>25</td>
          <td>5</td>
          <td>5</td>
          <td>7</td>
          <td>8</td>
          <td>493.18</td>
          <td>228.73</td>
          <td>0.4755</td>
          <td>0.5</td>
          <td>0.2778</td>
          <td>0.28</td>
          <td>0.6154</td>
          <td>8.46e-05</td>
          <td>7.76e-05</td>
          <td>0.0001379</td>
          <td>13180</td>
          <td>12269</td>
          <td>2826</td>
          <td>3184</td>
          <td>21</td>
          <td>251</td>
          <td>5</td>
          <td>2</td>
          <td>295</td>
          <td>687</td>
          <td>895</td>
          <td>15040</td>
          <td>4275</td>
          <td>14283</td>
          <td>5404</td>
          <td>16940</td>
        </tr>
        <tr>
          <td>Volcom Juniors Pocket Blocket Long Sleeve Tee</td>
          <td>Volcom</td>
          <td>Tops &amp; Tees</td>
          <td>27.0</td>
          <td>15.34</td>
          <td>81.0</td>
          <td>33.86</td>
          <td>21</td>
          <td>3</td>
          <td>4</td>
          <td>5</td>
          <td>9</td>
          <td>243.0</td>
          <td>107.41</td>
          <td>0.418</td>
          <td>0.5714</td>
          <td>0.1875</td>
          <td>0.2381</td>
          <td>0.75</td>
          <td>3e-05</td>
          <td>2.42e-05</td>
          <td>0.0001158</td>
          <td>19072</td>
          <td>17500</td>
          <td>9846</td>
          <td>11622</td>
          <td>50</td>
          <td>2358</td>
          <td>30</td>
          <td>24</td>
          <td>140</td>
          <td>2456</td>
          <td>3131</td>
          <td>20016</td>
          <td>4252</td>
          <td>19354</td>
          <td>7773</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Striped Crew Sock</td>
          <td>HUGO BOSS</td>
          <td>Socks</td>
          <td>13.0</td>
          <td>8.14</td>
          <td>104.0</td>
          <td>40.17</td>
          <td>24</td>
          <td>8</td>
          <td>3</td>
          <td>4</td>
          <td>9</td>
          <td>91.0</td>
          <td>33.33</td>
          <td>0.3863</td>
          <td>0.2727</td>
          <td>0.4</td>
          <td>0.1667</td>
          <td>0.5294</td>
          <td>3.85e-05</td>
          <td>2.87e-05</td>
          <td>0.0001324</td>
          <td>25705</td>
          <td>24062</td>
          <td>7764</td>
          <td>10157</td>
          <td>30</td>
          <td>16</td>
          <td>151</td>
          <td>126</td>
          <td>140</td>
          <td>8958</td>
          <td>11794</td>
          <td>21483</td>
          <td>11342</td>
          <td>7482</td>
          <td>10731</td>
          <td>19498</td>
        </tr>
        <tr>
          <td>7 For All Mankind Men&#x27;s The Straight Modern Jean</td>
          <td>7 For All Mankind</td>
          <td>Jeans</td>
          <td>175.57</td>
          <td>89.48</td>
          <td>575.0</td>
          <td>267.13</td>
          <td>21</td>
          <td>4</td>
          <td>3</td>
          <td>5</td>
          <td>9</td>
          <td>1447.0</td>
          <td>714.47</td>
          <td>0.4646</td>
          <td>0.4286</td>
          <td>0.25</td>
          <td>0.2381</td>
          <td>0.6923</td>
          <td>0.000213</td>
          <td>0.0001909</td>
          <td>0.0001158</td>
          <td>1310</td>
          <td>1144</td>
          <td>466</td>
          <td>647</td>
          <td>50</td>
          <td>776</td>
          <td>151</td>
          <td>24</td>
          <td>140</td>
          <td>54</td>
          <td>70</td>
          <td>15992</td>
          <td>8270</td>
          <td>14408</td>
          <td>7773</td>
          <td>12966</td>
        </tr>
        <tr>
          <td>JiMarti JM01 Sunglasses for Golf Fishing Cycling-Unbreakable-... Frame</td>
          <td>JiMarti</td>
          <td>Accessories</td>
          <td>29.95</td>
          <td>11.92</td>
          <td>269.55</td>
          <td>161.1</td>
          <td>22</td>
          <td>9</td>
          <td>2</td>
          <td>2</td>
          <td>9</td>
          <td>119.8</td>
          <td>72.12</td>
          <td>0.5977</td>
          <td>0.1818</td>
          <td>0.45</td>
          <td>0.0909</td>
          <td>0.5</td>
          <td>9.99e-05</td>
          <td>0.0001151</td>
          <td>0.0001214</td>
          <td>18166</td>
          <td>20613</td>
          <td>2175</td>
          <td>1707</td>
          <td>43</td>
          <td>5</td>
          <td>844</td>
          <td>2100</td>
          <td>140</td>
          <td>6868</td>
          <td>5540</td>
          <td>2758</td>
          <td>13193</td>
          <td>6490</td>
          <td>16872</td>
          <td>19501</td>
        </tr>
        <tr>
          <td>Lee Men&#x27;s Relaxed Fit Slightly Tapered Leg Jean</td>
          <td>Lee</td>
          <td>Jeans</td>
          <td>30.99</td>
          <td>16.89</td>
          <td>122.96</td>
          <td>55.54</td>
          <td>21</td>
          <td>4</td>
          <td>5</td>
          <td>3</td>
          <td>9</td>
          <td>248.92</td>
          <td>113.31</td>
          <td>0.4517</td>
          <td>0.5556</td>
          <td>0.2222</td>
          <td>0.1429</td>
          <td>0.6923</td>
          <td>4.55e-05</td>
          <td>3.97e-05</td>
          <td>0.0001158</td>
          <td>17446</td>
          <td>16178</td>
          <td>6481</td>
          <td>7447</td>
          <td>50</td>
          <td>776</td>
          <td>5</td>
          <td>526</td>
          <td>140</td>
          <td>2405</td>
          <td>2891</td>
          <td>17150</td>
          <td>4274</td>
          <td>17122</td>
          <td>12706</td>
          <td>12966</td>
        </tr>
        <tr>
          <td>RSQ London Mens Skinny Jeans</td>
          <td>RSQ</td>
          <td>Jeans</td>
          <td>44.99</td>
          <td>24.2</td>
          <td>134.97</td>
          <td>63.21</td>
          <td>21</td>
          <td>3</td>
          <td>5</td>
          <td>3</td>
          <td>10</td>
          <td>359.92</td>
          <td>163.94</td>
          <td>0.4683</td>
          <td>0.625</td>
          <td>0.1667</td>
          <td>0.1429</td>
          <td>0.7692</td>
          <td>5e-05</td>
          <td>4.52e-05</td>
          <td>0.0001158</td>
          <td>12553</td>
          <td>11383</td>
          <td>5908</td>
          <td>6477</td>
          <td>50</td>
          <td>2358</td>
          <td>5</td>
          <td>526</td>
          <td>77</td>
          <td>1228</td>
          <td>1608</td>
          <td>15636</td>
          <td>4099</td>
          <td>19436</td>
          <td>12706</td>
          <td>9471</td>
        </tr>
        <tr>
          <td>HUGO BOSS Men&#x27;s Bright Argyle Crew Sock</td>
          <td>HUGO BOSS</td>
          <td>Socks</td>
          <td>9.75</td>
          <td>5.68</td>
          <td>39.0</td>
          <td>15.65</td>
          <td>22</td>
          <td>4</td>
          <td>4</td>
          <td>4</td>
          <td>10</td>
          <td>78.0</td>
          <td>32.25</td>
          <td>0.4013</td>
          <td>0.5</td>
          <td>0.2222</td>
          <td>0.1818</td>
          <td>0.7143</td>
          <td>1.44e-05</td>
          <td>1.12e-05</td>
          <td>0.0001214</td>
          <td>27342</td>
          <td>26355</td>
          <td>16327</td>
          <td>17765</td>
          <td>43</td>
          <td>776</td>
          <td>30</td>
          <td>126</td>
          <td>77</td>
          <td>10368</td>
          <td>12068</td>
          <td>20837</td>
          <td>4275</td>
          <td>17122</td>
          <td>10468</td>
          <td>12035</td>
        </tr>
        <tr>
          <td>Michael Kors Men&#x27;s 3 Pack Brief</td>
          <td>Michael Kors</td>
          <td>Underwear</td>
          <td>25.99</td>
          <td>12.48</td>
          <td>130.46</td>
          <td>67.73</td>
          <td>24</td>
          <td>5</td>
          <td>5</td>
          <td>4</td>
          <td>10</td>
          <td>232.38</td>
          <td>120.98</td>
          <td>0.5192</td>
          <td>0.5</td>
          <td>0.25</td>
          <td>0.1667</td>
          <td>0.6667</td>
          <td>4.83e-05</td>
          <td>4.84e-05</td>
          <td>0.0001324</td>
          <td>19456</td>
          <td>20053</td>
          <td>6070</td>
          <td>5979</td>
          <td>30</td>
          <td>251</td>
          <td>5</td>
          <td>126</td>
          <td>77</td>
          <td>2705</td>
          <td>2646</td>
          <td>10469</td>
          <td>4275</td>
          <td>14408</td>
          <td>10731</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Ray-Ban Women&#x27;s 4101 Jackie Ohh Sunglasses</td>
          <td>Ray-Ban</td>
          <td>Accessories</td>
          <td>97.5</td>
          <td>41.94</td>
          <td>486.16</td>
          <td>280.13</td>
          <td>22</td>
          <td>5</td>
          <td>1</td>
          <td>5</td>
          <td>11</td>
          <td>586.32</td>
          <td>330.97</td>
          <td>0.5762</td>
          <td>0.1667</td>
          <td>0.2941</td>
          <td>0.2273</td>
          <td>0.6875</td>
          <td>0.0001801</td>
          <td>0.0002002</td>
          <td>0.0001214</td>
          <td>4451</td>
          <td>5084</td>
          <td>706</td>
          <td>587</td>
          <td>43</td>
          <td>251</td>
          <td>3978</td>
          <td>24</td>
          <td>43</td>
          <td>472</td>
          <td>408</td>
          <td>4708</td>
          <td>13196</td>
          <td>13232</td>
          <td>7836</td>
          <td>12983</td>
        </tr>
        <tr>
          <td>Motherhood Maternity: Sports Clip Down Nursing Bra</td>
          <td>Motherhood Maternity</td>
          <td>Maternity</td>
          <td>22.54</td>
          <td>10.46</td>
          <td>200.82</td>
          <td>108.99</td>
          <td>25</td>
          <td>9</td>
          <td>2</td>
          <td>3</td>
          <td>11</td>
          <td>112.9</td>
          <td>60.37</td>
          <td>0.5427</td>
          <td>0.1818</td>
          <td>0.4091</td>
          <td>0.12</td>
          <td>0.55</td>
          <td>7.44e-05</td>
          <td>7.79e-05</td>
          <td>0.0001379</td>
          <td>21822</td>
          <td>22052</td>
          <td>3297</td>
          <td>3165</td>
          <td>21</td>
          <td>5</td>
          <td>844</td>
          <td>526</td>
          <td>43</td>
          <td>7249</td>
          <td>6811</td>
          <td>8373</td>
          <td>13193</td>
          <td>7481</td>
          <td>15549</td>
          <td>19449</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by Lost Revenue</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>Steinbock Tyrolean Sport Coat</td>
          <td>Orvis</td>
          <td>Suits &amp; Sport Coats</td>
          <td>350.0</td>
          <td>154.0</td>
          <td>1400.0</td>
          <td>784.0</td>
          <td>11</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>7</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.56</td>
          <td>0.0</td>
          <td>0.3636</td>
          <td>0.0</td>
          <td>0.6364</td>
          <td>0.0005186</td>
          <td>0.0005603</td>
          <td>6.07e-05</td>
          <td>180</td>
          <td>217</td>
          <td>49</td>
          <td>48</td>
          <td>1161</td>
          <td>776</td>
          <td>13463</td>
          <td>17458</td>
          <td>623</td>
          <td>22642</td>
          <td>22642</td>
          <td>6489</td>
          <td>13463</td>
          <td>9638</td>
          <td>17458</td>
          <td>16487</td>
        </tr>
        <tr>
          <td>The North Face Apex Bionic Soft Shell Jacket - Men&#x27;s</td>
          <td>The North Face</td>
          <td>Fashion Hoodies &amp; Sweatshirts</td>
          <td>903.0</td>
          <td>524.64</td>
          <td>1806.0</td>
          <td>756.71</td>
          <td>6</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>4</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.419</td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>0.000669</td>
          <td>0.0005408</td>
          <td>3.31e-05</td>
          <td>5</td>
          <td>3</td>
          <td>21</td>
          <td>55</td>
          <td>12532</td>
          <td>6114</td>
          <td>13463</td>
          <td>17458</td>
          <td>6105</td>
          <td>22642</td>
          <td>22642</td>
          <td>19960</td>
          <td>13463</td>
          <td>9747</td>
          <td>17458</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>Women&#x27;s Knee Length Overcoat in Pure Cashmere</td>
          <td>Cashmere Boutique</td>
          <td>Outerwear &amp; Coats</td>
          <td>399.0</td>
          <td>193.12</td>
          <td>1596.0</td>
          <td>814.76</td>
          <td>9</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>5</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.5105</td>
          <td>0.0</td>
          <td>0.4444</td>
          <td>0.0</td>
          <td>0.5556</td>
          <td>0.0005912</td>
          <td>0.0005823</td>
          <td>4.96e-05</td>
          <td>115</td>
          <td>100</td>
          <td>35</td>
          <td>40</td>
          <td>3355</td>
          <td>776</td>
          <td>13463</td>
          <td>17458</td>
          <td>3026</td>
          <td>22642</td>
          <td>22642</td>
          <td>11502</td>
          <td>13463</td>
          <td>6492</td>
          <td>17458</td>
          <td>19270</td>
        </tr>
        <tr>
          <td>Mountain Hardwear Men&#x27;s Chillwave Down Parka</td>
          <td>Mountain Hardwear</td>
          <td>Outerwear &amp; Coats</td>
          <td>375.0</td>
          <td>176.63</td>
          <td>1500.0</td>
          <td>793.5</td>
          <td>5</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.529</td>
          <td>0.0</td>
          <td>0.8</td>
          <td>0.0</td>
          <td>0.2</td>
          <td>0.0005557</td>
          <td>0.0005671</td>
          <td>2.76e-05</td>
          <td>155</td>
          <td>135</td>
          <td>41</td>
          <td>44</td>
          <td>16887</td>
          <td>776</td>
          <td>13463</td>
          <td>17458</td>
          <td>23197</td>
          <td>22642</td>
          <td>22642</td>
          <td>9645</td>
          <td>13463</td>
          <td>607</td>
          <td>17458</td>
          <td>26859</td>
        </tr>
        <tr>
          <td>AIR JORDAN DOMINATE SHORTS MENS 465071-100</td>
          <td>Jordan</td>
          <td>Shorts</td>
          <td>903.0</td>
          <td>454.21</td>
          <td>2709.0</td>
          <td>1346.37</td>
          <td>5</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>2</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.497</td>
          <td>0.0</td>
          <td>0.6</td>
          <td>0.0</td>
          <td>0.4</td>
          <td>0.0010035</td>
          <td>0.0009622</td>
          <td>2.76e-05</td>
          <td>5</td>
          <td>8</td>
          <td>7</td>
          <td>9</td>
          <td>16887</td>
          <td>2358</td>
          <td>13463</td>
          <td>17458</td>
          <td>17069</td>
          <td>22642</td>
          <td>22642</td>
          <td>12874</td>
          <td>13463</td>
          <td>2189</td>
          <td>17458</td>
          <td>23875</td>
        </tr>
        <tr>
          <td>Quiksilver Men&#x27;s Rockefeller Walkshort</td>
          <td>Quiksilver</td>
          <td>Shorts</td>
          <td>903.0</td>
          <td>472.27</td>
          <td>1806.0</td>
          <td>861.46</td>
          <td>6</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>4</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.477</td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>0.000669</td>
          <td>0.0006157</td>
          <td>3.31e-05</td>
          <td>5</td>
          <td>7</td>
          <td>21</td>
          <td>34</td>
          <td>12532</td>
          <td>6114</td>
          <td>13463</td>
          <td>17458</td>
          <td>6105</td>
          <td>22642</td>
          <td>22642</td>
          <td>14881</td>
          <td>13463</td>
          <td>9747</td>
          <td>17458</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>The North Face Nuptse 2 Jacket - Noah Green/TNF Black</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>370.23</td>
          <td>1806.0</td>
          <td>1065.54</td>
          <td>8</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>6</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.59</td>
          <td>0.0</td>
          <td>0.25</td>
          <td>0.0</td>
          <td>0.75</td>
          <td>0.000669</td>
          <td>0.0007615</td>
          <td>4.41e-05</td>
          <td>5</td>
          <td>29</td>
          <td>21</td>
          <td>19</td>
          <td>5507</td>
          <td>6114</td>
          <td>13463</td>
          <td>17458</td>
          <td>1398</td>
          <td>22642</td>
          <td>22642</td>
          <td>3353</td>
          <td>13463</td>
          <td>14408</td>
          <td>17458</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>The North Face Denali Down Womens Jacket 2013</td>
          <td>The North Face</td>
          <td>Active</td>
          <td>903.0</td>
          <td>395.51</td>
          <td>1806.0</td>
          <td>1014.97</td>
          <td>8</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>6</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.562</td>
          <td>0.0</td>
          <td>0.25</td>
          <td>0.0</td>
          <td>0.75</td>
          <td>0.000669</td>
          <td>0.0007254</td>
          <td>4.41e-05</td>
          <td>5</td>
          <td>20</td>
          <td>21</td>
          <td>25</td>
          <td>5507</td>
          <td>6114</td>
          <td>13463</td>
          <td>17458</td>
          <td>1398</td>
          <td>22642</td>
          <td>22642</td>
          <td>6272</td>
          <td>13463</td>
          <td>14408</td>
          <td>17458</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>HALSTON HERITAGE Women&#x27;s Sleeveless Ponte Pleated Dress</td>
          <td>Halston Heritage</td>
          <td>Dresses</td>
          <td>357.0</td>
          <td>161.36</td>
          <td>1428.0</td>
          <td>782.54</td>
          <td>9</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>5</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.548</td>
          <td>0.0</td>
          <td>0.4444</td>
          <td>0.0</td>
          <td>0.5556</td>
          <td>0.000529</td>
          <td>0.0005593</td>
          <td>4.96e-05</td>
          <td>172</td>
          <td>181</td>
          <td>47</td>
          <td>49</td>
          <td>3355</td>
          <td>776</td>
          <td>13463</td>
          <td>17458</td>
          <td>3026</td>
          <td>22642</td>
          <td>22642</td>
          <td>7812</td>
          <td>13463</td>
          <td>6492</td>
          <td>17458</td>
          <td>19270</td>
        </tr>
        <tr>
          <td>7 For All Mankind Men&#x27;s Austyn Relaxed Straight Jean</td>
          <td>7 For All Mankind</td>
          <td>Jeans</td>
          <td>197.94</td>
          <td>111.63</td>
          <td>1399.0</td>
          <td>608.64</td>
          <td>17</td>
          <td>7</td>
          <td>0</td>
          <td>1</td>
          <td>9</td>
          <td>189.0</td>
          <td>83.35</td>
          <td>0.4351</td>
          <td>0.0</td>
          <td>0.4375</td>
          <td>0.0588</td>
          <td>0.5625</td>
          <td>0.0005182</td>
          <td>0.000435</td>
          <td>9.38e-05</td>
          <td>942</td>
          <td>526</td>
          <td>50</td>
          <td>91</td>
          <td>103</td>
          <td>33</td>
          <td>13463</td>
          <td>7029</td>
          <td>140</td>
          <td>3671</td>
          <td>4605</td>
          <td>18597</td>
          <td>13463</td>
          <td>6734</td>
          <td>17433</td>
          <td>19266</td>
        </tr>
        <tr>
          <td>PAIGE Women&#x27;s Skyline Skinny Jean</td>
          <td>PAIGE</td>
          <td>Jeans</td>
          <td>158.0</td>
          <td>90.19</td>
          <td>1422.0</td>
          <td>608.93</td>
          <td>19</td>
          <td>9</td>
          <td>0</td>
          <td>2</td>
          <td>8</td>
          <td>316.0</td>
          <td>135.88</td>
          <td>0.4282</td>
          <td>0.0</td>
          <td>0.5294</td>
          <td>0.1053</td>
          <td>0.4706</td>
          <td>0.0005268</td>
          <td>0.0004352</td>
          <td>0.0001048</td>
          <td>1714</td>
          <td>1108</td>
          <td>48</td>
          <td>90</td>
          <td>72</td>
          <td>5</td>
          <td>13463</td>
          <td>2100</td>
          <td>295</td>
          <td>1575</td>
          <td>2230</td>
          <td>19172</td>
          <td>13463</td>
          <td>3268</td>
          <td>16363</td>
          <td>23444</td>
        </tr>
        <tr>
          <td>True Religion Women&#x27;s Julie Super T Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>326.0</td>
          <td>172.13</td>
          <td>1956.0</td>
          <td>923.23</td>
          <td>8</td>
          <td>6</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>326.0</td>
          <td>153.87</td>
          <td>0.472</td>
          <td>0.0</td>
          <td>0.8571</td>
          <td>0.125</td>
          <td>0.1429</td>
          <td>0.0007246</td>
          <td>0.0006598</td>
          <td>4.41e-05</td>
          <td>233</td>
          <td>145</td>
          <td>19</td>
          <td>31</td>
          <td>5507</td>
          <td>84</td>
          <td>13463</td>
          <td>7029</td>
          <td>23197</td>
          <td>1487</td>
          <td>1788</td>
          <td>15335</td>
          <td>13463</td>
          <td>546</td>
          <td>14338</td>
          <td>27121</td>
        </tr>
        <tr>
          <td>Mountain Hardwear Women&#x27;s Chillwave Down Jacket</td>
          <td>Mountain Hardwear</td>
          <td>Outerwear &amp; Coats</td>
          <td>375.0</td>
          <td>179.25</td>
          <td>1875.0</td>
          <td>978.75</td>
          <td>6</td>
          <td>5</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>375.0</td>
          <td>195.75</td>
          <td>0.522</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.1667</td>
          <td>0.0</td>
          <td>0.0006946</td>
          <td>0.0006995</td>
          <td>3.31e-05</td>
          <td>155</td>
          <td>128</td>
          <td>20</td>
          <td>29</td>
          <td>12532</td>
          <td>251</td>
          <td>13463</td>
          <td>7029</td>
          <td>27145</td>
          <td>1150</td>
          <td>1161</td>
          <td>10227</td>
          <td>13463</td>
          <td>1</td>
          <td>10731</td>
          <td>27145</td>
        </tr>
        <tr>
          <td>Barbour Bedale Jacket / Bedale Jacket</td>
          <td>Barbour</td>
          <td>Outerwear &amp; Coats</td>
          <td>379.0</td>
          <td>173.96</td>
          <td>1516.0</td>
          <td>820.16</td>
          <td>8</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>3</td>
          <td>379.0</td>
          <td>205.04</td>
          <td>0.541</td>
          <td>0.0</td>
          <td>0.5714</td>
          <td>0.125</td>
          <td>0.4286</td>
          <td>0.0005616</td>
          <td>0.0005862</td>
          <td>4.41e-05</td>
          <td>147</td>
          <td>142</td>
          <td>39</td>
          <td>39</td>
          <td>5507</td>
          <td>776</td>
          <td>13463</td>
          <td>7029</td>
          <td>10869</td>
          <td>1133</td>
          <td>1085</td>
          <td>8491</td>
          <td>13463</td>
          <td>2847</td>
          <td>14338</td>
          <td>23541</td>
        </tr>
        <tr>
          <td>Barbour Classic Beaufort Jacket / Beaufort Jacket</td>
          <td>Barbour</td>
          <td>Outerwear &amp; Coats</td>
          <td>399.0</td>
          <td>193.91</td>
          <td>1596.0</td>
          <td>820.34</td>
          <td>10</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>5</td>
          <td>399.0</td>
          <td>205.09</td>
          <td>0.514</td>
          <td>0.0</td>
          <td>0.4444</td>
          <td>0.1</td>
          <td>0.5556</td>
          <td>0.0005912</td>
          <td>0.0005863</td>
          <td>5.52e-05</td>
          <td>115</td>
          <td>98</td>
          <td>35</td>
          <td>38</td>
          <td>1962</td>
          <td>776</td>
          <td>13463</td>
          <td>7029</td>
          <td>3026</td>
          <td>985</td>
          <td>1084</td>
          <td>11041</td>
          <td>13463</td>
          <td>6492</td>
          <td>16366</td>
          <td>19270</td>
        </tr>
      </tbody>
    </table>
  </div>

  <p><strong>Bottom products by Lost Profit</strong></p>

  <pre><code class="language-sql">WITH first_layer AS (
SELECT
  p.name AS product_name,
  p.brand AS product_brand,
  p.category AS product_category,
  ROUND(AVG(oi.sale_price), 2) AS avg_product_sale_price,
  ROUND(AVG(p.cost), 2) AS avg_product_cost,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN oi.sale_price ELSE 0 END), 2) AS
revenue,
ROUND(SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN (oi.sale_price - p.cost) ELSE 0
END), 2) AS profit,
COUNT(*) AS unit_orders_placed,
SUM(CASE WHEN oi.status = &#x27;Complete&#x27; THEN 1 ELSE 0 END) AS units_completed,
SUM(CASE WHEN oi.status = &#x27;Returned&#x27; THEN 1 ELSE 0 END) AS units_returned,
SUM(CASE WHEN oi.status = &#x27;Cancelled&#x27; THEN 1 ELSE 0 END) AS units_cancelled,
SUM(CASE WHEN oi.status IN (&#x27;Shipped&#x27;, &#x27;Processing&#x27;) THEN 1 ELSE 0 END) AS units_en_route,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN oi.sale_price ELSE 0 END), 2) AS lost_revenue,
ROUND(SUM(CASE WHEN oi.status IN (&#x27;Returned&#x27;, &#x27;Cancelled&#x27;) THEN (oi.sale_price - p.cost) ELSE 0 END), 2) AS lost_profit
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


  <div style="overflow-x: auto; max-width: 100%;">
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
        <tr>
          <td>The North Face Denali Down Womens Jacket 2013</td>
          <td>The North Face</td>
          <td>Active</td>
          <td>903.0</td>
          <td>395.51</td>
          <td>1806.0</td>
          <td>1014.97</td>
          <td>8</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>6</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.562</td>
          <td>0.0</td>
          <td>0.25</td>
          <td>0.0</td>
          <td>0.75</td>
          <td>0.000669</td>
          <td>0.0007254</td>
          <td>4.41e-05</td>
          <td>5</td>
          <td>20</td>
          <td>21</td>
          <td>25</td>
          <td>5507</td>
          <td>6114</td>
          <td>13463</td>
          <td>17458</td>
          <td>1398</td>
          <td>22642</td>
          <td>22642</td>
          <td>6272</td>
          <td>13463</td>
          <td>14408</td>
          <td>17458</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>Women&#x27;s Knee Length Overcoat in Pure Cashmere</td>
          <td>Cashmere Boutique</td>
          <td>Outerwear &amp; Coats</td>
          <td>399.0</td>
          <td>193.12</td>
          <td>1596.0</td>
          <td>814.76</td>
          <td>9</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>5</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.5105</td>
          <td>0.0</td>
          <td>0.4444</td>
          <td>0.0</td>
          <td>0.5556</td>
          <td>0.0005912</td>
          <td>0.0005823</td>
          <td>4.96e-05</td>
          <td>115</td>
          <td>100</td>
          <td>35</td>
          <td>40</td>
          <td>3355</td>
          <td>776</td>
          <td>13463</td>
          <td>17458</td>
          <td>3026</td>
          <td>22642</td>
          <td>22642</td>
          <td>11502</td>
          <td>13463</td>
          <td>6492</td>
          <td>17458</td>
          <td>19270</td>
        </tr>
        <tr>
          <td>AIR JORDAN DOMINATE SHORTS MENS 465071-100</td>
          <td>Jordan</td>
          <td>Shorts</td>
          <td>903.0</td>
          <td>454.21</td>
          <td>2709.0</td>
          <td>1346.37</td>
          <td>5</td>
          <td>3</td>
          <td>0</td>
          <td>0</td>
          <td>2</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.497</td>
          <td>0.0</td>
          <td>0.6</td>
          <td>0.0</td>
          <td>0.4</td>
          <td>0.0010035</td>
          <td>0.0009622</td>
          <td>2.76e-05</td>
          <td>5</td>
          <td>8</td>
          <td>7</td>
          <td>9</td>
          <td>16887</td>
          <td>2358</td>
          <td>13463</td>
          <td>17458</td>
          <td>17069</td>
          <td>22642</td>
          <td>22642</td>
          <td>12874</td>
          <td>13463</td>
          <td>2189</td>
          <td>17458</td>
          <td>23875</td>
        </tr>
        <tr>
          <td>Steinbock Tyrolean Sport Coat</td>
          <td>Orvis</td>
          <td>Suits &amp; Sport Coats</td>
          <td>350.0</td>
          <td>154.0</td>
          <td>1400.0</td>
          <td>784.0</td>
          <td>11</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>7</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.56</td>
          <td>0.0</td>
          <td>0.3636</td>
          <td>0.0</td>
          <td>0.6364</td>
          <td>0.0005186</td>
          <td>0.0005603</td>
          <td>6.07e-05</td>
          <td>180</td>
          <td>217</td>
          <td>49</td>
          <td>48</td>
          <td>1161</td>
          <td>776</td>
          <td>13463</td>
          <td>17458</td>
          <td>623</td>
          <td>22642</td>
          <td>22642</td>
          <td>6489</td>
          <td>13463</td>
          <td>9638</td>
          <td>17458</td>
          <td>16487</td>
        </tr>
        <tr>
          <td>Mountain Hardwear Men&#x27;s Chillwave Down Parka</td>
          <td>Mountain Hardwear</td>
          <td>Outerwear &amp; Coats</td>
          <td>375.0</td>
          <td>176.63</td>
          <td>1500.0</td>
          <td>793.5</td>
          <td>5</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>1</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.529</td>
          <td>0.0</td>
          <td>0.8</td>
          <td>0.0</td>
          <td>0.2</td>
          <td>0.0005557</td>
          <td>0.0005671</td>
          <td>2.76e-05</td>
          <td>155</td>
          <td>135</td>
          <td>41</td>
          <td>44</td>
          <td>16887</td>
          <td>776</td>
          <td>13463</td>
          <td>17458</td>
          <td>23197</td>
          <td>22642</td>
          <td>22642</td>
          <td>9645</td>
          <td>13463</td>
          <td>607</td>
          <td>17458</td>
          <td>26859</td>
        </tr>
        <tr>
          <td>The North Face Nuptse 2 Jacket - Noah Green/TNF Black</td>
          <td>The North Face</td>
          <td>Outerwear &amp; Coats</td>
          <td>903.0</td>
          <td>370.23</td>
          <td>1806.0</td>
          <td>1065.54</td>
          <td>8</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>6</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.59</td>
          <td>0.0</td>
          <td>0.25</td>
          <td>0.0</td>
          <td>0.75</td>
          <td>0.000669</td>
          <td>0.0007615</td>
          <td>4.41e-05</td>
          <td>5</td>
          <td>29</td>
          <td>21</td>
          <td>19</td>
          <td>5507</td>
          <td>6114</td>
          <td>13463</td>
          <td>17458</td>
          <td>1398</td>
          <td>22642</td>
          <td>22642</td>
          <td>3353</td>
          <td>13463</td>
          <td>14408</td>
          <td>17458</td>
          <td>9487</td>
        </tr>
        <tr>
          <td>HALSTON HERITAGE Women&#x27;s Sleeveless Ponte Pleated Dress</td>
          <td>Halston Heritage</td>
          <td>Dresses</td>
          <td>357.0</td>
          <td>161.36</td>
          <td>1428.0</td>
          <td>782.54</td>
          <td>9</td>
          <td>4</td>
          <td>0</td>
          <td>0</td>
          <td>5</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.548</td>
          <td>0.0</td>
          <td>0.4444</td>
          <td>0.0</td>
          <td>0.5556</td>
          <td>0.000529</td>
          <td>0.0005593</td>
          <td>4.96e-05</td>
          <td>172</td>
          <td>181</td>
          <td>47</td>
          <td>49</td>
          <td>3355</td>
          <td>776</td>
          <td>13463</td>
          <td>17458</td>
          <td>3026</td>
          <td>22642</td>
          <td>22642</td>
          <td>7812</td>
          <td>13463</td>
          <td>6492</td>
          <td>17458</td>
          <td>19270</td>
        </tr>
        <tr>
          <td>Quiksilver Men&#x27;s Rockefeller Walkshort</td>
          <td>Quiksilver</td>
          <td>Shorts</td>
          <td>903.0</td>
          <td>472.27</td>
          <td>1806.0</td>
          <td>861.46</td>
          <td>6</td>
          <td>2</td>
          <td>0</td>
          <td>0</td>
          <td>4</td>
          <td>0.0</td>
          <td>0.0</td>
          <td>0.477</td>
          <td>0.0</td>
          <td>0.3333</td>
          <td>0.0</td>
          <td>0.6667</td>
          <td>0.000669</td>
          <td>0.0006157</td>
          <td>3.31e-05</td>
          <td>5</td>
          <td>7</td>
          <td>21</td>
          <td>34</td>
          <td>12532</td>
          <td>6114</td>
          <td>13463</td>
          <td>17458</td>
          <td>6105</td>
          <td>22642</td>
          <td>22642</td>
          <td>14881</td>
          <td>13463</td>
          <td>9747</td>
          <td>17458</td>
          <td>12990</td>
        </tr>
        <tr>
          <td>True Religion Women&#x27;s Julie Super T Jean</td>
          <td>True Religion</td>
          <td>Jeans</td>
          <td>326.0</td>
          <td>172.13</td>
          <td>1956.0</td>
          <td>923.23</td>
          <td>8</td>
          <td>6</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>326.0</td>
          <td>153.87</td>
          <td>0.472</td>
          <td>0.0</td>
          <td>0.8571</td>
          <td>0.125</td>
          <td>0.1429</td>
          <td>0.0007246</td>
          <td>0.0006598</td>
          <td>4.41e-05</td>
          <td>233</td>
          <td>145</td>
          <td>19</td>
          <td>31</td>
          <td>5507</td>
          <td>84</td>
          <td>13463</td>
          <td>7029</td>
          <td>23197</td>
          <td>1487</td>
          <td>1788</td>
          <td>15335</td>
          <td>13463</td>
          <td>546</td>
          <td>14338</td>
          <td>27121</td>
        </tr>
        <tr>
          <td>Mountain Hardwear Women&#x27;s Chillwave Down Jacket</td>
          <td>Mountain Hardwear</td>
          <td>Outerwear &amp; Coats</td>
          <td>375.0</td>
          <td>179.25</td>
          <td>1875.0</td>
          <td>978.75</td>
          <td>6</td>
          <td>5</td>
          <td>0</td>
          <td>1</td>
          <td>0</td>
          <td>375.0</td>
          <td>195.75</td>
          <td>0.522</td>
          <td>0.0</td>
          <td>1.0</td>
          <td>0.1667</td>
          <td>0.0</td>
          <td>0.0006946</td>
          <td>0.0006995</td>
          <td>3.31e-05</td>
          <td>155</td>
          <td>128</td>
          <td>20</td>
          <td>29</td>
          <td>12532</td>
          <td>251</td>
          <td>13463</td>
          <td>7029</td>
          <td>27145</td>
          <td>1150</td>
          <td>1161</td>
          <td>10227</td>
          <td>13463</td>
          <td>1</td>
          <td>10731</td>
          <td>27145</td>
        </tr>
        <tr>
          <td>Barbour Bedale Jacket / Bedale Jacket</td>
          <td>Barbour</td>
          <td>Outerwear &amp; Coats</td>
          <td>379.0</td>
          <td>173.96</td>
          <td>1516.0</td>
          <td>820.16</td>
          <td>8</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>3</td>
          <td>379.0</td>
          <td>205.04</td>
          <td>0.541</td>
          <td>0.0</td>
          <td>0.5714</td>
          <td>0.125</td>
          <td>0.4286</td>
          <td>0.0005616</td>
          <td>0.0005862</td>
          <td>4.41e-05</td>
          <td>147</td>
          <td>142</td>
          <td>39</td>
          <td>39</td>
          <td>5507</td>
          <td>776</td>
          <td>13463</td>
          <td>7029</td>
          <td>10869</td>
          <td>1133</td>
          <td>1085</td>
          <td>8491</td>
          <td>13463</td>
          <td>2847</td>
          <td>14338</td>
          <td>23541</td>
        </tr>
        <tr>
          <td>Barbour Classic Beaufort Jacket / Beaufort Jacket</td>
          <td>Barbour</td>
          <td>Outerwear &amp; Coats</td>
          <td>399.0</td>
          <td>193.91</td>
          <td>1596.0</td>
          <td>820.34</td>
          <td>10</td>
          <td>4</td>
          <td>0</td>
          <td>1</td>
          <td>5</td>
          <td>399.0</td>
          <td>205.09</td>
          <td>0.514</td>
          <td>0.0</td>
          <td>0.4444</td>
          <td>0.1</td>
          <td>0.5556</td>
          <td>0.0005912</td>
          <td>0.0005863</td>
          <td>5.52e-05</td>
          <td>115</td>
          <td>98</td>
          <td>35</td>
          <td>38</td>
          <td>1962</td>
          <td>776</td>
          <td>13463</td>
          <td>7029</td>
          <td>3026</td>
          <td>985</td>
          <td>1084</td>
          <td>11041</td>
          <td>13463</td>
          <td>6492</td>
          <td>16366</td>
          <td>19270</td>
        </tr>
        <tr>
          <td>Carhartt Men&#x27;s Canvas Shirt Jacket</td>
          <td>Carhartt</td>
          <td>Outerwear &amp; Coats</td>
          <td>448.99</td>
          <td>181.39</td>
          <td>1346.97</td>
          <td>802.79</td>
          <td>5</td>
          <td>3</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>448.99</td>
          <td>267.6</td>
          <td>0.596</td>
          <td>0.0</td>
          <td>0.75</td>
          <td>0.2</td>
          <td>0.25</td>
          <td>0.000499</td>
          <td>0.0005737</td>
          <td>2.76e-05</td>
          <td>92</td>
          <td>120</td>
          <td>61</td>
          <td>42</td>
          <td>16887</td>
          <td>2358</td>
          <td>13463</td>
          <td>7029</td>
          <td>23197</td>
          <td>828</td>
          <td>658</td>
          <td>2857</td>
          <td>13463</td>
          <td>746</td>
          <td>8435</td>
          <td>26348</td>
        </tr>
        <tr>
          <td>Jones New York Women&#x27;s Hidden Snap Notch Collar Coat</td>
          <td>Jones New York</td>
          <td>Outerwear &amp; Coats</td>
          <td>599.0</td>
          <td>253.38</td>
          <td>1797.0</td>
          <td>1036.87</td>
          <td>5</td>
          <td>3</td>
          <td>0</td>
          <td>1</td>
          <td>1</td>
          <td>599.0</td>
          <td>345.62</td>
          <td>0.577</td>
          <td>0.0</td>
          <td>0.75</td>
          <td>0.2</td>
          <td>0.25</td>
          <td>0.0006657</td>
          <td>0.000741</td>
          <td>2.76e-05</td>
          <td>56</td>
          <td>61</td>
          <td>28</td>
          <td>24</td>
          <td>16887</td>
          <td>2358</td>
          <td>13463</td>
          <td>7029</td>
          <td>23197</td>
          <td>428</td>
          <td>368</td>
          <td>4613</td>
          <td>13463</td>
          <td>746</td>
          <td>8435</td>
          <td>26348</td>
        </tr>
        <tr>
          <td>Rebecca Minkoff Women&#x27;s Leather Luciana Skirt</td>
          <td>Rebecca Minkoff</td>
          <td>Skirts</td>
          <td>598.0</td>
          <td>249.96</td>
          <td>1794.0</td>
          <td>1044.11</td>
          <td>7</td>
          <td>3</td>
          <td>1</td>
          <td>0</td>
          <td>3</td>
          <td>598.0</td>
          <td>348.04</td>
          <td>0.582</td>
          <td>0.25</td>
          <td>0.4286</td>
          <td>0.0</td>
          <td>0.5</td>
          <td>0.0006646</td>
          <td>0.0007462</td>
          <td>3.86e-05</td>
          <td>57</td>
          <td>62</td>
          <td>30</td>
          <td>22</td>
          <td>8625</td>
          <td>2358</td>
          <td>3978</td>
          <td>17458</td>
          <td>10869</td>
          <td>430</td>
          <td>358</td>
          <td>4095</td>
          <td>11344</td>
          <td>6739</td>
          <td>17458</td>
          <td>19501</td>
        </tr>
      </tbody>
    </table>
  </div>

</details>
<details>
  <summary><strong>Top Brands</strong></summary>

  <div style="margin-top: 12px;"></div>

</details>
<details>
  <summary><strong>Bottom Brands</strong></summary>

  <div style="margin-top: 12px;"></div>

</details>
<details>
  <summary><strong>Top Categories</strong></summary>

  <div style="margin-top: 12px;"></div>

</details>
<details>
  <summary><strong>Bottom Categories</strong></summary>

  <div style="margin-top: 12px;"></div>

</details>
<details>
  <summary><strong>Long Term Trends</strong></summary>

  <div style="margin-top: 12px;"></div>

</details>
<details>
  <summary><strong>Seasonal Trends</strong></summary>

  <div style="margin-top: 12px;"></div>

</details>
<details>
  <summary><strong>Top Customers</strong></summary>

  <div style="margin-top: 12px;"></div>

</details>
<details>
  <summary><strong>Bottom Customers</strong></summary>

  <div style="margin-top: 12px;"></div>

</details>
<details>
  <summary><strong>Conclusion</strong></summary>

  <div style="margin-top: 12px;"></div>

</details>
