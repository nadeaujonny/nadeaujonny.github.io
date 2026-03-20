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

**Top products by Revenue**

```sql
WITH first_layer AS (
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
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ASCIS Cushion Low Socks (Pack of 3) | ASICS | Active | 903.0 | 373.84 | 3612.0 | 2116.63 | 11 | 4 | 0 | 1 | 6 | 903.0 | 529.16 | 0.586 | 0.0 | 0.4 | 0.0909 | 0.6 | 0.001338 | 0.0015127 | 6.07e-05 | 5 | 28 | 1 | 1 | 1161 | 776 | 13463 | 7029 | 1398 | 155 | 142 | 3719 | 13463 | 7482 | 16872 | 16953 |
| The North Face Women's S-XL Oso Jacket | The North Face | Outerwear & Coats | 903.0 | 378.36 | 3612.0 | 2098.57 | 10 | 4 | 1 | 1 | 4 | 1806.0 | 1049.29 | 0.581 | 0.2 | 0.4444 | 0.1 | 0.5 | 0.001338 | 0.0014998 | 5.52e-05 | 5 | 25 | 1 | 2 | 1962 | 776 | 3978 | 7029 | 6105 | 22 | 24 | 4209 | 12637 | 6492 | 16366 | 19501 |
| Spyder Women's Jesst In Time Jacket | Spyder | Outerwear & Coats | 650.0 | 295.75 | 3250.0 | 1771.25 | 10 | 5 | 4 | 0 | 1 | 2600.0 | 1417.0 | 0.545 | 0.4444 | 0.5 | 0.0 | 0.1667 | 0.0012039 | 0.0012659 | 5.52e-05 | 52 | 50 | 3 | 4 | 1962 | 251 | 30 | 17458 | 23197 | 7 | 7 | 8121 | 8264 | 3269 | 17458 | 27059 |
| Bergama Natural Raccoon Hooded Stroller - - Multicolor | Bergama | Outerwear & Coats | 749.99 | 306.75 | 2999.96 | 1772.98 | 10 | 4 | 1 | 0 | 5 | 749.99 | 443.24 | 0.591 | 0.2 | 0.4 | 0.0 | 0.5556 | 0.0011113 | 0.0012671 | 5.52e-05 | 40 | 43 | 4 | 3 | 1962 | 776 | 3978 | 17458 | 3026 | 267 | 224 | 3279 | 12637 | 7482 | 17458 | 19270 |
| Woolrich Arctic Parka DF | Woolrich | Outerwear & Coats | 990.0 | 478.17 | 2970.0 | 1535.49 | 12 | 3 | 2 | 1 | 6 | 2970.0 | 1535.49 | 0.517 | 0.4 | 0.2727 | 0.0833 | 0.6667 | 0.0011002 | 0.0010974 | 6.62e-05 | 3 | 6 | 5 | 6 | 694 | 2358 | 844 | 7029 | 1398 | 4 | 4 | 10735 | 8312 | 14284 | 17144 | 12990 |
| Joseph Abboud Men's Two-button Side Vent Sport Coat | Joseph Abboud | Suits & Sport Coats | 264.0 | 101.9 | 2904.0 | 1759.82 | 30 | 11 | 2 | 2 | 15 | 1056.0 | 656.57 | 0.606 | 0.1538 | 0.3929 | 0.0667 | 0.5769 | 0.0010758 | 0.0012577 | 0.0001655 | 430 | 734 | 6 | 5 | 7 | 3 | 844 | 2100 | 11 | 112 | 91 | 2144 | 13388 | 9081 | 17408 | 18610 |
| AIR JORDAN DOMINATE SHORTS MENS 465071-100 | Jordan | Shorts | 903.0 | 454.21 | 2709.0 | 1346.37 | 5 | 3 | 0 | 0 | 2 | 0.0 | 0.0 | 0.497 | 0.0 | 0.6 | 0.0 | 0.4 | 0.0010035 | 0.0009622 | 2.76e-05 | 5 | 8 | 7 | 9 | 16887 | 2358 | 13463 | 17458 | 17069 | 22642 | 22642 | 12874 | 13463 | 2189 | 17458 | 23875 |
| The North Face Denali Down Mens Jacket 2013 | The North Face | Outerwear & Coats | 903.0 | 436.15 | 2709.0 | 1400.55 | 13 | 3 | 2 | 2 | 6 | 3612.0 | 1867.4 | 0.517 | 0.4 | 0.2727 | 0.1538 | 0.6667 | 0.0010035 | 0.001001 | 7.17e-05 | 5 | 10 | 7 | 7 | 423 | 2358 | 844 | 2100 | 1398 | 2 | 3 | 10735 | 8312 | 14284 | 12634 | 12990 |
| Diesel Men's Lagnum Leather Jacket | Diesel | Outerwear & Coats | 598.0 | 267.9 | 2392.0 | 1320.38 | 7 | 4 | 1 | 1 | 1 | 1196.0 | 660.19 | 0.552 | 0.2 | 0.6667 | 0.1429 | 0.2 | 0.0008861 | 0.0009437 | 3.86e-05 | 57 | 56 | 9 | 10 | 8625 | 776 | 3978 | 7029 | 23197 | 92 | 89 | 7373 | 12637 | 1185 | 12706 | 26859 |
| Nobis Merideth Parka | Nobis | Outerwear & Coats | 795.0 | 382.39 | 2385.0 | 1237.82 | 7 | 3 | 1 | 1 | 2 | 1590.0 | 825.21 | 0.519 | 0.25 | 0.5 | 0.1429 | 0.4 | 0.0008835 | 0.0008847 | 3.86e-05 | 33 | 23 | 10 | 12 | 8625 | 2358 | 3978 | 7029 | 17069 | 37 | 45 | 10485 | 11344 | 3269 | 12706 | 23875 |
| Canada Goose Women's Expedition Parka | Canada Goose | Outerwear & Coats | 795.0 | 395.91 | 2385.0 | 1197.27 | 4 | 3 | 0 | 1 | 0 | 795.0 | 399.09 | 0.502 | 0.0 | 1.0 | 0.25 | 0.0 | 0.0008835 | 0.0008557 | 2.21e-05 | 33 | 19 | 10 | 13 | 21053 | 2358 | 13463 | 7029 | 27145 | 230 | 277 | 12357 | 13463 | 1 | 5542 | 27145 |
| Men's Classic Sheepskin B-3 Bomber Jacket | Overland Sheepskin Co | Outerwear & Coats | 595.0 | 270.73 | 2380.0 | 1297.1 | 13 | 4 | 0 | 2 | 7 | 1190.0 | 648.55 | 0.545 | 0.0 | 0.3636 | 0.1538 | 0.6364 | 0.0008816 | 0.000927 | 7.17e-05 | 60 | 55 | 12 | 11 | 423 | 776 | 13463 | 2100 | 623 | 95 | 94 | 8121 | 13463 | 9638 | 12634 | 16487 |
| Michael Kors Men's Marlow Wool-Blend Single-Breasted Fitted Top Coat | Michael Kors | Outerwear & Coats | 255.0 | 102.26 | 2295.0 | 1374.7 | 15 | 9 | 1 | 2 | 3 | 765.0 | 458.23 | 0.599 | 0.1 | 0.6923 | 0.1333 | 0.25 | 0.0008502 | 0.0009825 | 8.27e-05 | 469 | 728 | 13 | 8 | 187 | 5 | 3978 | 2100 | 10869 | 252 | 208 | 2612 | 13461 | 1184 | 14317 | 26348 |
| Barbour Sapper Jacket | Barbour | Outerwear & Coats | 429.0 | 210.21 | 2145.0 | 1093.95 | 10 | 5 | 1 | 1 | 3 | 858.0 | 437.58 | 0.51 | 0.1667 | 0.5556 | 0.1 | 0.375 | 0.0007946 | 0.0007818 | 5.52e-05 | 94 | 81 | 14 | 18 | 1962 | 251 | 3978 | 7029 | 10869 | 185 | 233 | 11510 | 13196 | 3151 | 16366 | 24717 |
| Arc'teryx Moray Jacket - Women's | Arc'teryx | Outerwear & Coats | 699.0 | 343.91 | 2097.0 | 1065.28 | 9 | 3 | 0 | 3 | 3 | 2097.0 | 1065.28 | 0.508 | 0.0 | 0.5 | 0.3333 | 0.5 | 0.0007768 | 0.0007613 | 4.96e-05 | 41 | 36 | 15 | 20 | 3355 | 2358 | 13463 | 526 | 10869 | 11 | 22 | 11720 | 13463 | 3269 | 2619 | 19501 |

</div>

**Top products by Profit**

```sql
WITH first_layer AS (
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
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ASCIS Cushion Low Socks (Pack of 3) | ASICS | Active | 903.0 | 373.84 | 3612.0 | 2116.63 | 11 | 4 | 0 | 1 | 6 | 903.0 | 529.16 | 0.586 | 0.0 | 0.4 | 0.0909 | 0.6 | 0.001338 | 0.0015127 | 6.07e-05 | 5 | 28 | 1 | 1 | 1161 | 776 | 13463 | 7029 | 1398 | 155 | 142 | 3719 | 13463 | 7482 | 16872 | 16953 |
| The North Face Women's S-XL Oso Jacket | The North Face | Outerwear & Coats | 903.0 | 378.36 | 3612.0 | 2098.57 | 10 | 4 | 1 | 1 | 4 | 1806.0 | 1049.29 | 0.581 | 0.2 | 0.4444 | 0.1 | 0.5 | 0.001338 | 0.0014998 | 5.52e-05 | 5 | 25 | 1 | 2 | 1962 | 776 | 3978 | 7029 | 6105 | 22 | 24 | 4209 | 12637 | 6492 | 16366 | 19501 |
| Bergama Natural Raccoon Hooded Stroller - - Multicolor | Bergama | Outerwear & Coats | 749.99 | 306.75 | 2999.96 | 1772.98 | 10 | 4 | 1 | 0 | 5 | 749.99 | 443.24 | 0.591 | 0.2 | 0.4 | 0.0 | 0.5556 | 0.0011113 | 0.0012671 | 5.52e-05 | 40 | 43 | 4 | 3 | 1962 | 776 | 3978 | 17458 | 3026 | 267 | 224 | 3279 | 12637 | 7482 | 17458 | 19270 |
| Spyder Women's Jesst In Time Jacket | Spyder | Outerwear & Coats | 650.0 | 295.75 | 3250.0 | 1771.25 | 10 | 5 | 4 | 0 | 1 | 2600.0 | 1417.0 | 0.545 | 0.4444 | 0.5 | 0.0 | 0.1667 | 0.0012039 | 0.0012659 | 5.52e-05 | 52 | 50 | 3 | 4 | 1962 | 251 | 30 | 17458 | 23197 | 7 | 7 | 8121 | 8264 | 3269 | 17458 | 27059 |
| Joseph Abboud Men's Two-button Side Vent Sport Coat | Joseph Abboud | Suits & Sport Coats | 264.0 | 101.9 | 2904.0 | 1759.82 | 30 | 11 | 2 | 2 | 15 | 1056.0 | 656.57 | 0.606 | 0.1538 | 0.3929 | 0.0667 | 0.5769 | 0.0010758 | 0.0012577 | 0.0001655 | 430 | 734 | 6 | 5 | 7 | 3 | 844 | 2100 | 11 | 112 | 91 | 2144 | 13388 | 9081 | 17408 | 18610 |
| Woolrich Arctic Parka DF | Woolrich | Outerwear & Coats | 990.0 | 478.17 | 2970.0 | 1535.49 | 12 | 3 | 2 | 1 | 6 | 2970.0 | 1535.49 | 0.517 | 0.4 | 0.2727 | 0.0833 | 0.6667 | 0.0011002 | 0.0010974 | 6.62e-05 | 3 | 6 | 5 | 6 | 694 | 2358 | 844 | 7029 | 1398 | 4 | 4 | 10735 | 8312 | 14284 | 17144 | 12990 |
| The North Face Denali Down Mens Jacket 2013 | The North Face | Outerwear & Coats | 903.0 | 436.15 | 2709.0 | 1400.55 | 13 | 3 | 2 | 2 | 6 | 3612.0 | 1867.4 | 0.517 | 0.4 | 0.2727 | 0.1538 | 0.6667 | 0.0010035 | 0.001001 | 7.17e-05 | 5 | 10 | 7 | 7 | 423 | 2358 | 844 | 2100 | 1398 | 2 | 3 | 10735 | 8312 | 14284 | 12634 | 12990 |
| Michael Kors Men's Marlow Wool-Blend Single-Breasted Fitted Top Coat | Michael Kors | Outerwear & Coats | 255.0 | 102.26 | 2295.0 | 1374.7 | 15 | 9 | 1 | 2 | 3 | 765.0 | 458.23 | 0.599 | 0.1 | 0.6923 | 0.1333 | 0.25 | 0.0008502 | 0.0009825 | 8.27e-05 | 469 | 728 | 13 | 8 | 187 | 5 | 3978 | 2100 | 10869 | 252 | 208 | 2612 | 13461 | 1184 | 14317 | 26348 |
| AIR JORDAN DOMINATE SHORTS MENS 465071-100 | Jordan | Shorts | 903.0 | 454.21 | 2709.0 | 1346.37 | 5 | 3 | 0 | 0 | 2 | 0.0 | 0.0 | 0.497 | 0.0 | 0.6 | 0.0 | 0.4 | 0.0010035 | 0.0009622 | 2.76e-05 | 5 | 8 | 7 | 9 | 16887 | 2358 | 13463 | 17458 | 17069 | 22642 | 22642 | 12874 | 13463 | 2189 | 17458 | 23875 |
| Diesel Men's Lagnum Leather Jacket | Diesel | Outerwear & Coats | 598.0 | 267.9 | 2392.0 | 1320.38 | 7 | 4 | 1 | 1 | 1 | 1196.0 | 660.19 | 0.552 | 0.2 | 0.6667 | 0.1429 | 0.2 | 0.0008861 | 0.0009437 | 3.86e-05 | 57 | 56 | 9 | 10 | 8625 | 776 | 3978 | 7029 | 23197 | 92 | 89 | 7373 | 12637 | 1185 | 12706 | 26859 |
| Men's Classic Sheepskin B-3 Bomber Jacket | Overland Sheepskin Co | Outerwear & Coats | 595.0 | 270.73 | 2380.0 | 1297.1 | 13 | 4 | 0 | 2 | 7 | 1190.0 | 648.55 | 0.545 | 0.0 | 0.3636 | 0.1538 | 0.6364 | 0.0008816 | 0.000927 | 7.17e-05 | 60 | 55 | 12 | 11 | 423 | 776 | 13463 | 2100 | 623 | 95 | 94 | 8121 | 13463 | 9638 | 12634 | 16487 |
| Nobis Merideth Parka | Nobis | Outerwear & Coats | 795.0 | 382.39 | 2385.0 | 1237.82 | 7 | 3 | 1 | 1 | 2 | 1590.0 | 825.21 | 0.519 | 0.25 | 0.5 | 0.1429 | 0.4 | 0.0008835 | 0.0008847 | 3.86e-05 | 33 | 23 | 10 | 12 | 8625 | 2358 | 3978 | 7029 | 17069 | 37 | 45 | 10485 | 11344 | 3269 | 12706 | 23875 |
| Canada Goose Women's Expedition Parka | Canada Goose | Outerwear & Coats | 795.0 | 395.91 | 2385.0 | 1197.27 | 4 | 3 | 0 | 1 | 0 | 795.0 | 399.09 | 0.502 | 0.0 | 1.0 | 0.25 | 0.0 | 0.0008835 | 0.0008557 | 2.21e-05 | 33 | 19 | 10 | 13 | 21053 | 2358 | 13463 | 7029 | 27145 | 230 | 277 | 12357 | 13463 | 1 | 5542 | 27145 |
| Canada Goose Women's Solaris | Canada Goose | Outerwear & Coats | 695.0 | 296.76 | 2085.0 | 1194.71 | 6 | 3 | 0 | 2 | 1 | 1390.0 | 796.47 | 0.573 | 0.0 | 0.75 | 0.3333 | 0.25 | 0.0007724 | 0.0008538 | 3.31e-05 | 46 | 48 | 17 | 14 | 12532 | 2358 | 13463 | 2100 | 23197 | 67 | 52 | 5041 | 13463 | 746 | 2619 | 26348 |
| Darla | Alpha Industries | Outerwear & Coats | 999.0 | 404.6 | 1998.0 | 1188.81 | 7 | 2 | 2 | 0 | 3 | 1998.0 | 1188.81 | 0.595 | 0.5 | 0.2857 | 0.0 | 0.6 | 0.0007401 | 0.0008496 | 3.86e-05 | 1 | 16 | 18 | 15 | 8625 | 6114 | 844 | 17458 | 10869 | 14 | 14 | 2925 | 4275 | 13238 | 17458 | 16953 |

</div>

**Top products by Profit Margin**

```sql
WITH first_layer AS (
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
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Plus Size Black Jazzy Jacket | Fashion Love | Blazers & Jackets | 34.99 | 11.58 | 104.97 | 70.22 | 5 | 3 | 0 | 1 | 1 | 34.99 | 23.41 | 0.669 | 0.0 | 0.75 | 0.2 | 0.25 | 3.89e-05 | 5.02e-05 | 2.76e-05 | 15963 | 20949 | 7698 | 5726 | 16887 | 2358 | 13463 | 7029 | 23197 | 17236 | 14884 | 1 | 13463 | 746 | 8435 | 26348 |
| Ulla Popken Plus Size Soutache Embroidered Jacket | Ulla Popken | Blazers & Jackets | 89.0 | 29.46 | 178.0 | 119.08 | 7 | 2 | 1 | 0 | 4 | 89.0 | 59.54 | 0.669 | 0.3333 | 0.2857 | 0.0 | 0.6667 | 6.59e-05 | 8.51e-05 | 3.86e-05 | 4994 | 8857 | 4102 | 2773 | 8625 | 6114 | 3978 | 17458 | 6105 | 9306 | 6919 | 1 | 8752 | 13238 | 17458 | 12990 |
| Ted Baker Women's Mowna | Ted Baker | Blazers & Jackets | 206.96 | 68.5 | 206.96 | 138.46 | 7 | 1 | 1 | 1 | 4 | 413.92 | 276.91 | 0.669 | 0.5 | 0.1667 | 0.1429 | 0.8 | 7.67e-05 | 9.9e-05 | 3.86e-05 | 771 | 2149 | 3223 | 2200 | 8625 | 13264 | 3978 | 7029 | 6105 | 925 | 621 | 1 | 4275 | 19436 | 12706 | 7598 |
| Eddie Bauer Signature Stretch Blazer | Eddie Bauer | Blazers & Jackets | 149.95 | 49.63 | 299.9 | 200.63 | 9 | 2 | 0 | 2 | 5 | 299.9 | 200.63 | 0.669 | 0.0 | 0.2857 | 0.2222 | 0.7143 | 0.0001111 | 0.0001434 | 4.96e-05 | 1956 | 3876 | 1775 | 1137 | 3355 | 6114 | 13463 | 2100 | 3026 | 1734 | 1126 | 1 | 13463 | 13238 | 7837 | 12035 |
| DKNYC Women's 2 Button Blazer | DKNYC | Blazers & Jackets | 99.09 | 32.8 | 198.18 | 132.58 | 6 | 2 | 2 | 0 | 2 | 198.18 | 132.58 | 0.669 | 0.5 | 0.3333 | 0.0 | 0.5 | 7.34e-05 | 9.48e-05 | 3.31e-05 | 4110 | 7591 | 3450 | 2363 | 12532 | 6114 | 844 | 17458 | 17069 | 3375 | 2320 | 1 | 4275 | 9747 | 17458 | 19501 |
| Allegra K Front Opening Long Sleeve Womenwear Form-fitting Blazer Off White XS | Allegra K | Blazers & Jackets | 18.68 | 6.18 | 37.36 | 24.99 | 6 | 2 | 0 | 1 | 3 | 18.68 | 12.5 | 0.6689 | 0.0 | 0.4 | 0.1667 | 0.6 | 1.38e-05 | 1.79e-05 | 3.31e-05 | 23425 | 25885 | 16627 | 14250 | 12532 | 6114 | 13463 | 7029 | 10869 | 20771 | 19355 | 6 | 13463 | 7482 | 10731 | 16953 |
| Allegra K Women Horizontal Stripes Bubble Sleeve Spring Coat Black XS | Allegra K | Blazers & Jackets | 11.67 | 3.86 | 23.34 | 15.61 | 10 | 2 | 1 | 0 | 7 | 11.67 | 7.81 | 0.6688 | 0.3333 | 0.2 | 0.0 | 0.7778 | 8.6e-06 | 1.12e-05 | 5.52e-05 | 26523 | 27736 | 19737 | 17784 | 1962 | 6114 | 3978 | 17458 | 623 | 21976 | 21271 | 7 | 8752 | 17510 | 17458 | 9281 |
| BB Dakota Yellow Marigold Naples Boxy Cropped Blazer Button up Front and Double Pockets | BB Dakota | Blazers & Jackets | 77.0 | 25.56 | 77.0 | 51.44 | 6 | 1 | 0 | 2 | 3 | 154.0 | 102.87 | 0.6681 | 0.0 | 0.25 | 0.3333 | 0.75 | 2.85e-05 | 3.68e-05 | 3.31e-05 | 6222 | 10673 | 10392 | 8077 | 12532 | 13264 | 13463 | 2100 | 10869 | 4944 | 3344 | 8 | 13463 | 14408 | 2619 | 9487 |
| Mango Women's Suit Cropped Blazer - Chipi | MANGO | Blazers & Jackets | 49.99 | 16.6 | 99.98 | 66.79 | 4 | 2 | 1 | 0 | 1 | 49.99 | 33.39 | 0.668 | 0.3333 | 0.5 | 0.0 | 0.3333 | 3.7e-05 | 4.77e-05 | 2.21e-05 | 10894 | 16411 | 8109 | 6088 | 21053 | 6114 | 3978 | 17458 | 23197 | 14347 | 11779 | 9 | 8752 | 3269 | 17458 | 24854 |
| Calvin Klein Jeans Women's Moto Jacket | Calvin Klein Jeans | Blazers & Jackets | 56.39 | 18.72 | 56.39 | 37.67 | 5 | 1 | 1 | 0 | 3 | 56.39 | 37.67 | 0.668 | 0.5 | 0.2 | 0.0 | 0.75 | 2.09e-05 | 2.69e-05 | 2.76e-05 | 9503 | 14790 | 13133 | 10707 | 16887 | 13264 | 3978 | 17458 | 10869 | 13238 | 10778 | 9 | 4275 | 17510 | 17458 | 9487 |
| Allegra K Women Double Breasted Long Sleeve Autumn Blazer Coat Army Green XS | Allegra K | Blazers & Jackets | 16.05 | 5.33 | 32.1 | 21.44 | 4 | 2 | 0 | 1 | 1 | 16.05 | 10.72 | 0.6679 | 0.0 | 0.6667 | 0.25 | 0.3333 | 1.19e-05 | 1.53e-05 | 2.21e-05 | 24296 | 26673 | 17542 | 15499 | 21053 | 6114 | 13463 | 7029 | 23197 | 21164 | 20129 | 11 | 13463 | 1185 | 5542 | 24854 |
| Pendleton Women's Trimmed Herringbone Blazer | Pendleton | Blazers & Jackets | 258.0 | 85.91 | 516.0 | 344.17 | 6 | 2 | 1 | 2 | 1 | 774.0 | 516.26 | 0.667 | 0.3333 | 0.5 | 0.3333 | 0.3333 | 0.0001911 | 0.000246 | 3.31e-05 | 462 | 1282 | 594 | 364 | 12532 | 6114 | 3978 | 2100 | 23197 | 251 | 153 | 12 | 8752 | 3269 | 2619 | 24854 |
| Corey Lynn Calter Women's Jessica Jacket | CoreyLynnCalter | Blazers & Jackets | 79.0 | 26.31 | 79.0 | 52.69 | 3 | 1 | 0 | 1 | 1 | 79.0 | 52.69 | 0.667 | 0.0 | 0.5 | 0.3333 | 0.5 | 2.93e-05 | 3.77e-05 | 1.65e-05 | 5951 | 10284 | 10194 | 7889 | 24645 | 13264 | 13463 | 7029 | 23197 | 10287 | 7953 | 12 | 13463 | 3269 | 2619 | 19501 |
| Only Hearts Women's Double Knit 2 Button Jacket | Only Hearts | Blazers & Jackets | 185.0 | 61.61 | 1110.0 | 740.37 | 11 | 6 | 0 | 0 | 5 | 0.0 | 0.0 | 0.667 | 0.0 | 0.5455 | 0.0 | 0.4545 | 0.0004112 | 0.0005291 | 6.07e-05 | 1114 | 2672 | 94 | 56 | 1161 | 84 | 13463 | 17458 | 3026 | 22642 | 22642 | 12 | 13463 | 3246 | 17458 | 23452 |
| Plus Size White Night Sky Top | Alex Evenings | Blazers & Jackets | 124.99 | 41.62 | 124.99 | 83.37 | 4 | 1 | 2 | 0 | 1 | 249.98 | 166.74 | 0.667 | 0.6667 | 0.25 | 0.0 | 0.5 | 4.63e-05 | 5.96e-05 | 2.21e-05 | 2939 | 5153 | 6403 | 4593 | 21053 | 13264 | 844 | 17458 | 23197 | 2385 | 1545 | 12 | 3055 | 14408 | 17458 | 19501 |

</div>

**Top products by Unit Orders**

```sql
WITH first_layer AS (
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
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Wrangler Men's Premium Performance Cowboy Cut Jean | Wrangler | Jeans | 47.45 | 25.88 | 570.83 | 264.22 | 58 | 12 | 2 | 7 | 37 | 417.81 | 189.65 | 0.4629 | 0.1429 | 0.2353 | 0.1207 | 0.7551 | 0.0002115 | 0.0001888 | 0.00032 | 12004 | 10508 | 470 | 662 | 1 | 2 | 844 | 2 | 1 | 905 | 1224 | 16149 | 13389 | 17092 | 15548 | 9486 |
| 7 For All Mankind Men's Standard Classic Straight Leg Jean | 7 For All Mankind | Jeans | 157.45 | 80.97 | 1435.0 | 696.01 | 42 | 9 | 5 | 5 | 23 | 1673.0 | 844.04 | 0.485 | 0.3571 | 0.2432 | 0.119 | 0.7188 | 0.0005316 | 0.0004974 | 0.0002317 | 1798 | 1488 | 46 | 60 | 2 | 5 | 5 | 24 | 2 | 32 | 41 | 14028 | 8749 | 17091 | 15552 | 12034 |
| Wrangler Men's Rugged Wear Classic Fit Jean | Wrangler | Jeans | 40.87 | 22.23 | 367.56 | 169.24 | 38 | 9 | 5 | 9 | 15 | 596.43 | 273.96 | 0.4604 | 0.3571 | 0.3103 | 0.2368 | 0.625 | 0.0001362 | 0.000121 | 0.0002096 | 13688 | 12514 | 1205 | 1552 | 3 | 5 | 5 | 1 | 11 | 440 | 628 | 16340 | 8749 | 13014 | 7776 | 16547 |
| True Religion Men's Ricky Straight Jean | True Religion | Jeans | 246.88 | 129.05 | 1366.0 | 666.07 | 34 | 5 | 4 | 3 | 22 | 1400.0 | 654.5 | 0.4876 | 0.4444 | 0.1613 | 0.0882 | 0.8148 | 0.000506 | 0.000476 | 0.0001876 | 534 | 354 | 56 | 65 | 4 | 251 | 30 | 526 | 3 | 63 | 92 | 13792 | 8264 | 20804 | 17143 | 7595 |
| Kenneth Cole REACTION Men's Passcase Wallet | Kenneth Cole REACTION | Accessories | 18.91 | 7.72 | 152.71 | 89.4 | 34 | 8 | 4 | 4 | 18 | 150.85 | 90.57 | 0.5854 | 0.3333 | 0.2667 | 0.1176 | 0.6923 | 5.66e-05 | 6.39e-05 | 0.0001876 | 23389 | 24481 | 4958 | 4188 | 4 | 16 | 30 | 126 | 4 | 5015 | 4078 | 3806 | 8752 | 14395 | 15553 | 12966 |
| HUGO BOSS Men's Long Pant | HUGO BOSS | Sleep & Lounge | 74.72 | 28.3 | 1033.11 | 648.16 | 33 | 14 | 0 | 3 | 16 | 233.01 | 138.21 | 0.6274 | 0.0 | 0.4667 | 0.0909 | 0.5333 | 0.0003827 | 0.0004632 | 0.000182 | 6501 | 9383 | 113 | 75 | 6 | 1 | 13463 | 526 | 7 | 2702 | 2165 | 933 | 13463 | 6418 | 16872 | 19494 |
| Joseph Abboud Men's Two-button Side Vent Sport Coat | Joseph Abboud | Suits & Sport Coats | 264.0 | 101.9 | 2904.0 | 1759.82 | 30 | 11 | 2 | 2 | 15 | 1056.0 | 656.57 | 0.606 | 0.1538 | 0.3929 | 0.0667 | 0.5769 | 0.0010758 | 0.0012577 | 0.0001655 | 430 | 734 | 6 | 5 | 7 | 3 | 844 | 2100 | 11 | 112 | 91 | 2144 | 13388 | 9081 | 17408 | 18610 |
| Wrangler Men's Genuine Tampa Cargo Short | Wrangler | Shorts | 31.37 | 15.61 | 229.94 | 116.44 | 29 | 7 | 1 | 5 | 16 | 179.94 | 90.54 | 0.5064 | 0.125 | 0.2917 | 0.1724 | 0.6957 | 8.52e-05 | 8.32e-05 | 0.00016 | 17403 | 17266 | 2818 | 2869 | 8 | 33 | 3978 | 24 | 7 | 3935 | 4081 | 11924 | 13444 | 13236 | 10730 | 12964 |
| Hanes Men's 4 Pack Boxer Brief | Hanes | Underwear | 25.0 | 11.52 | 250.0 | 133.47 | 28 | 10 | 2 | 5 | 11 | 175.0 | 92.77 | 0.5339 | 0.1667 | 0.4348 | 0.1786 | 0.5238 | 9.26e-05 | 9.54e-05 | 0.0001545 | 19651 | 20997 | 2432 | 2340 | 9 | 4 | 844 | 24 | 43 | 4152 | 3935 | 9232 | 13196 | 6738 | 10715 | 19500 |
| Chaps Big and Tall Solid V-Neck Vest | Chaps | Sweaters | 39.88 | 20.32 | 279.16 | 134.91 | 28 | 7 | 4 | 1 | 16 | 199.4 | 99.06 | 0.4833 | 0.3636 | 0.2593 | 0.0357 | 0.6957 | 0.0001034 | 9.64e-05 | 0.0001545 | 14437 | 13747 | 2029 | 2288 | 9 | 33 | 30 | 7029 | 7 | 3354 | 3543 | 14237 | 8748 | 14407 | 17457 | 12964 |
| True Religion Men's Ricky Straight Leg Jean | True Religion | Jeans | 227.86 | 123.14 | 1452.0 | 661.01 | 28 | 7 | 1 | 5 | 15 | 1430.0 | 645.85 | 0.4552 | 0.125 | 0.3043 | 0.1786 | 0.6818 | 0.0005379 | 0.0004724 | 0.0001545 | 646 | 406 | 45 | 69 | 9 | 33 | 3978 | 24 | 11 | 57 | 95 | 16801 | 13444 | 13032 | 10715 | 12986 |
| Joe's Jeans Men's Slim Fit Straight Leg Brixton | Joe's Jeans | Jeans | 194.26 | 102.07 | 1353.0 | 647.44 | 27 | 7 | 3 | 2 | 15 | 976.0 | 458.49 | 0.4785 | 0.3 | 0.28 | 0.0741 | 0.6818 | 0.0005012 | 0.0004627 | 0.0001489 | 992 | 729 | 58 | 76 | 12 | 33 | 151 | 2100 | 11 | 133 | 207 | 14773 | 11276 | 14282 | 17370 | 12986 |
| Dockers Men's Suit Separate Coat | Dockers | Suits & Sport Coats | 88.36 | 33.97 | 231.12 | 140.98 | 27 | 3 | 4 | 2 | 18 | 542.11 | 337.6 | 0.61 | 0.5714 | 0.12 | 0.0741 | 0.8571 | 8.56e-05 | 0.0001008 | 0.0001489 | 5094 | 7229 | 2783 | 2122 | 12 | 2358 | 30 | 2100 | 4 | 542 | 391 | 1873 | 4252 | 22129 | 17370 | 6057 |
| Volcom Men's Kinkade Jean | Volcom | Jeans | 66.67 | 35.17 | 269.9 | 125.86 | 27 | 4 | 3 | 5 | 15 | 538.25 | 254.63 | 0.4663 | 0.4286 | 0.1818 | 0.1852 | 0.7895 | 0.0001 | 9e-05 | 0.0001489 | 7633 | 6807 | 2158 | 2560 | 12 | 776 | 151 | 24 | 11 | 562 | 723 | 15806 | 8270 | 19358 | 10467 | 9273 |
| Wrangler Men's Wrancher Dress Jean | Wrangler | Jeans | 40.4 | 20.2 | 242.4 | 118.65 | 27 | 6 | 2 | 3 | 16 | 202.0 | 102.05 | 0.4895 | 0.25 | 0.25 | 0.1111 | 0.7273 | 8.98e-05 | 8.48e-05 | 0.0001489 | 13728 | 13816 | 2533 | 2788 | 12 | 84 | 844 | 526 | 7 | 3236 | 3382 | 13585 | 11344 | 14408 | 15570 | 11980 |

</div>

**Top products by Average Sale Price**

```sql
WITH first_layer AS (
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
  avg_product_sale_price_rank ASC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Alpha Industries Rip Stop Short | Alpha Industries | Shorts | 999.0 | 482.52 | 999.0 | 516.48 | 8 | 1 | 1 | 1 | 5 | 1998.0 | 1032.97 | 0.517 | 0.5 | 0.1429 | 0.125 | 0.8333 | 0.0003701 | 0.0003691 | 4.41e-05 | 1 | 5 | 120 | 134 | 5507 | 13264 | 3978 | 7029 | 3026 | 14 | 25 | 10735 | 4275 | 20815 | 14338 | 6580 |
| Darla | Alpha Industries | Outerwear & Coats | 999.0 | 404.6 | 1998.0 | 1188.81 | 7 | 2 | 2 | 0 | 3 | 1998.0 | 1188.81 | 0.595 | 0.5 | 0.2857 | 0.0 | 0.6 | 0.0007401 | 0.0008496 | 3.86e-05 | 1 | 16 | 18 | 15 | 8625 | 6114 | 844 | 17458 | 10869 | 14 | 14 | 2925 | 4275 | 13238 | 17458 | 16953 |
| Woolrich Arctic Parka DF | Woolrich | Outerwear & Coats | 990.0 | 478.17 | 2970.0 | 1535.49 | 12 | 3 | 2 | 1 | 6 | 2970.0 | 1535.49 | 0.517 | 0.4 | 0.2727 | 0.0833 | 0.6667 | 0.0011002 | 0.0010974 | 6.62e-05 | 3 | 6 | 5 | 6 | 694 | 2358 | 844 | 7029 | 1398 | 4 | 4 | 10735 | 8312 | 14284 | 17144 | 12990 |
| Nobis Yatesy Parka | Nobis | Outerwear & Coats | 950.0 | 381.9 | 0.0 | 0.0 | 7 | 0 | 0 | 1 | 6 | 950.0 | 568.1 |  |  | 0.0 | 0.1429 | 1.0 | 0.0 | 0.0 | 3.86e-05 | 4 | 24 | 22532 | 22532 | 8625 | 22532 | 13463 | 7029 | 1398 | 141 | 114 | 22532 | 25326 | 22532 | 12706 | 1 |
| The North Face Denali Down Womens Jacket 2013 | The North Face | Active | 903.0 | 395.51 | 1806.0 | 1014.97 | 8 | 2 | 0 | 0 | 6 | 0.0 | 0.0 | 0.562 | 0.0 | 0.25 | 0.0 | 0.75 | 0.000669 | 0.0007254 | 4.41e-05 | 5 | 20 | 21 | 25 | 5507 | 6114 | 13463 | 17458 | 1398 | 22642 | 22642 | 6272 | 13463 | 14408 | 17458 | 9487 |
| The North Face Freedom Mens Ski Pants 2013 | The North Face | Outerwear & Coats | 903.0 | 369.33 | 903.0 | 533.67 | 5 | 1 | 0 | 2 | 2 | 1806.0 | 1067.35 | 0.591 | 0.0 | 0.3333 | 0.4 | 0.6667 | 0.0003345 | 0.0003814 | 2.76e-05 | 5 | 31 | 149 | 122 | 16887 | 13264 | 13463 | 2100 | 17069 | 22 | 21 | 3279 | 13463 | 9747 | 1689 | 12990 |
| The North Face Women's S-XL Oso Jacket | The North Face | Outerwear & Coats | 903.0 | 378.36 | 3612.0 | 2098.57 | 10 | 4 | 1 | 1 | 4 | 1806.0 | 1049.29 | 0.581 | 0.2 | 0.4444 | 0.1 | 0.5 | 0.001338 | 0.0014998 | 5.52e-05 | 5 | 25 | 1 | 2 | 1962 | 776 | 3978 | 7029 | 6105 | 22 | 24 | 4209 | 12637 | 6492 | 16366 | 19501 |
| JORDAN DURASHEEN SHORT MENS 404309-109 | Jordan | Active | 903.0 | 370.23 | 903.0 | 532.77 | 4 | 1 | 1 | 0 | 2 | 903.0 | 532.77 | 0.59 | 0.5 | 0.25 | 0.0 | 0.6667 | 0.0003345 | 0.0003808 | 2.21e-05 | 5 | 29 | 149 | 123 | 21053 | 13264 | 3978 | 17458 | 17069 | 155 | 138 | 3353 | 4275 | 14408 | 17458 | 12990 |
| Nike Jordan Retro 11 Bred Bootie Socks | Jordan | Socks | 903.0 | 557.15 | 903.0 | 345.85 | 7 | 1 | 0 | 1 | 5 | 903.0 | 345.85 | 0.383 | 0.0 | 0.1667 | 0.1429 | 0.8333 | 0.0003345 | 0.0002472 | 3.86e-05 | 5 | 1 | 149 | 356 | 8625 | 13264 | 13463 | 7029 | 3026 | 155 | 367 | 21586 | 13463 | 19436 | 12706 | 6580 |
| The North Face Apex Bionic Soft Shell Jacket - Men's | The North Face | Outerwear & Coats | 903.0 | 363.01 | 0.0 | 0.0 | 4 | 0 | 1 | 0 | 3 | 903.0 | 539.99 |  | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 2.21e-05 | 5 | 34 | 22532 | 22532 | 21053 | 22532 | 3978 | 17458 | 10869 | 155 | 126 | 22532 | 1 | 22532 | 17458 | 1 |
| NIKE WOMEN'S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort* | Nike | Plus | 903.0 | 420.8 | 0.0 | 0.0 | 5 | 0 | 1 | 0 | 4 | 903.0 | 482.2 |  | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 2.76e-05 | 5 | 12 | 22532 | 22532 | 16887 | 22532 | 3978 | 17458 | 6105 | 155 | 177 | 22532 | 1 | 22532 | 17458 | 1 |
| The North Face Nuptse 2 Jacket - Noah Green/TNF Black | The North Face | Outerwear & Coats | 903.0 | 370.23 | 1806.0 | 1065.54 | 8 | 2 | 0 | 0 | 6 | 0.0 | 0.0 | 0.59 | 0.0 | 0.25 | 0.0 | 0.75 | 0.000669 | 0.0007615 | 4.41e-05 | 5 | 29 | 21 | 19 | 5507 | 6114 | 13463 | 17458 | 1398 | 22642 | 22642 | 3353 | 13463 | 14408 | 17458 | 9487 |
| NIKE WOMEN'S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort* | Nike | Active | 903.0 | 403.64 | 903.0 | 499.36 | 5 | 1 | 2 | 0 | 2 | 1806.0 | 998.72 | 0.553 | 0.6667 | 0.2 | 0.0 | 0.6667 | 0.0003345 | 0.0003569 | 2.76e-05 | 5 | 17 | 149 | 146 | 16887 | 13264 | 844 | 17458 | 17069 | 22 | 28 | 7266 | 3055 | 17510 | 17458 | 12990 |
| NIKE WOMEN'S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort* | Nike | Intimates | 903.0 | 512.0 | 0.0 | 0.0 | 4 | 0 | 0 | 3 | 1 | 2709.0 | 1173.0 |  |  | 0.0 | 0.75 | 1.0 | 0.0 | 0.0 | 2.21e-05 | 5 | 4 | 22532 | 22532 | 21053 | 22532 | 13463 | 526 | 23197 | 5 | 15 | 22532 | 25326 | 22532 | 109 | 1 |
| The North Face Denali Down Mens Jacket 2013 | The North Face | Outerwear & Coats | 903.0 | 436.15 | 2709.0 | 1400.55 | 13 | 3 | 2 | 2 | 6 | 3612.0 | 1867.4 | 0.517 | 0.4 | 0.2727 | 0.1538 | 0.6667 | 0.0010035 | 0.001001 | 7.17e-05 | 5 | 10 | 7 | 7 | 423 | 2358 | 844 | 2100 | 1398 | 2 | 3 | 10735 | 8312 | 14284 | 12634 | 12990 |

</div>

**Top products by Average Cost**

```sql
WITH first_layer AS (
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
  avg_product_cost_rank ASC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nike Jordan Retro 11 Bred Bootie Socks | Jordan | Socks | 903.0 | 557.15 | 903.0 | 345.85 | 7 | 1 | 0 | 1 | 5 | 903.0 | 345.85 | 0.383 | 0.0 | 0.1667 | 0.1429 | 0.8333 | 0.0003345 | 0.0002472 | 3.86e-05 | 5 | 1 | 149 | 356 | 8625 | 13264 | 13463 | 7029 | 3026 | 155 | 367 | 21586 | 13463 | 19436 | 12706 | 6580 |
| Jordan Low Quarter Sock Style # 427411 | Nike | Socks | 903.0 | 537.29 | 903.0 | 365.71 | 7 | 1 | 0 | 1 | 5 | 903.0 | 365.71 | 0.405 | 0.0 | 0.1667 | 0.1429 | 0.8333 | 0.0003345 | 0.0002614 | 3.86e-05 | 5 | 2 | 149 | 311 | 8625 | 13264 | 13463 | 7029 | 3026 | 155 | 323 | 20649 | 13463 | 19436 | 12706 | 6580 |
| The North Face Apex Bionic Soft Shell Jacket - Men's | The North Face | Fashion Hoodies & Sweatshirts | 903.0 | 524.64 | 1806.0 | 756.71 | 6 | 2 | 0 | 0 | 4 | 0.0 | 0.0 | 0.419 | 0.0 | 0.3333 | 0.0 | 0.6667 | 0.000669 | 0.0005408 | 3.31e-05 | 5 | 3 | 21 | 55 | 12532 | 6114 | 13463 | 17458 | 6105 | 22642 | 22642 | 19960 | 13463 | 9747 | 17458 | 12990 |
| NIKE WOMEN'S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort* | Nike | Intimates | 903.0 | 512.0 | 0.0 | 0.0 | 4 | 0 | 0 | 3 | 1 | 2709.0 | 1173.0 |  |  | 0.0 | 0.75 | 1.0 | 0.0 | 0.0 | 2.21e-05 | 5 | 4 | 22532 | 22532 | 21053 | 22532 | 13463 | 526 | 23197 | 5 | 15 | 22532 | 25326 | 22532 | 109 | 1 |
| Alpha Industries Rip Stop Short | Alpha Industries | Shorts | 999.0 | 482.52 | 999.0 | 516.48 | 8 | 1 | 1 | 1 | 5 | 1998.0 | 1032.97 | 0.517 | 0.5 | 0.1429 | 0.125 | 0.8333 | 0.0003701 | 0.0003691 | 4.41e-05 | 1 | 5 | 120 | 134 | 5507 | 13264 | 3978 | 7029 | 3026 | 14 | 25 | 10735 | 4275 | 20815 | 14338 | 6580 |
| Woolrich Arctic Parka DF | Woolrich | Outerwear & Coats | 990.0 | 478.17 | 2970.0 | 1535.49 | 12 | 3 | 2 | 1 | 6 | 2970.0 | 1535.49 | 0.517 | 0.4 | 0.2727 | 0.0833 | 0.6667 | 0.0011002 | 0.0010974 | 6.62e-05 | 3 | 6 | 5 | 6 | 694 | 2358 | 844 | 7029 | 1398 | 4 | 4 | 10735 | 8312 | 14284 | 17144 | 12990 |
| Quiksilver Men's Rockefeller Walkshort | Quiksilver | Shorts | 903.0 | 472.27 | 1806.0 | 861.46 | 6 | 2 | 0 | 0 | 4 | 0.0 | 0.0 | 0.477 | 0.0 | 0.3333 | 0.0 | 0.6667 | 0.000669 | 0.0006157 | 3.31e-05 | 5 | 7 | 21 | 34 | 12532 | 6114 | 13463 | 17458 | 6105 | 22642 | 22642 | 14881 | 13463 | 9747 | 17458 | 12990 |
| AIR JORDAN DOMINATE SHORTS MENS 465071-100 | Jordan | Shorts | 903.0 | 454.21 | 2709.0 | 1346.37 | 5 | 3 | 0 | 0 | 2 | 0.0 | 0.0 | 0.497 | 0.0 | 0.6 | 0.0 | 0.4 | 0.0010035 | 0.0009622 | 2.76e-05 | 5 | 8 | 7 | 9 | 16887 | 2358 | 13463 | 17458 | 17069 | 22642 | 22642 | 12874 | 13463 | 2189 | 17458 | 23875 |
| The North Face Denali Down Womens Jacket 2013 | The North Face | Outerwear & Coats | 903.0 | 437.05 | 903.0 | 465.95 | 5 | 1 | 0 | 1 | 3 | 903.0 | 465.95 | 0.516 | 0.0 | 0.25 | 0.2 | 0.75 | 0.0003345 | 0.000333 | 2.76e-05 | 5 | 9 | 149 | 173 | 16887 | 13264 | 13463 | 7029 | 10869 | 155 | 198 | 10830 | 13463 | 14408 | 8435 | 9487 |
| The North Face Denali Down Mens Jacket 2013 | The North Face | Outerwear & Coats | 903.0 | 436.15 | 2709.0 | 1400.55 | 13 | 3 | 2 | 2 | 6 | 3612.0 | 1867.4 | 0.517 | 0.4 | 0.2727 | 0.1538 | 0.6667 | 0.0010035 | 0.001001 | 7.17e-05 | 5 | 10 | 7 | 7 | 423 | 2358 | 844 | 2100 | 1398 | 2 | 3 | 10735 | 8312 | 14284 | 12634 | 12990 |
| Catherine Malandrino Women's Skinny Stretch Leather Pant | Catherine Malandrino | Pants & Capris | 895.0 | 434.07 | 895.0 | 460.93 | 7 | 1 | 1 | 1 | 4 | 1790.0 | 921.85 | 0.515 | 0.5 | 0.1667 | 0.1429 | 0.8 | 0.0003315 | 0.0003294 | 3.86e-05 | 29 | 11 | 162 | 180 | 8625 | 13264 | 3978 | 7029 | 6105 | 29 | 33 | 10918 | 4275 | 19436 | 12706 | 7598 |
| NIKE WOMEN'S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort* | Nike | Plus | 903.0 | 420.8 | 0.0 | 0.0 | 5 | 0 | 1 | 0 | 4 | 903.0 | 482.2 |  | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 2.76e-05 | 5 | 12 | 22532 | 22532 | 16887 | 22532 | 3978 | 17458 | 6105 | 155 | 177 | 22532 | 1 | 22532 | 17458 | 1 |
| The North Face Apex Bionic Mens Soft Shell Ski Jacket 2013 | The North Face | Outerwear & Coats | 903.0 | 419.9 | 1806.0 | 966.21 | 7 | 2 | 1 | 1 | 3 | 1806.0 | 966.21 | 0.535 | 0.3333 | 0.3333 | 0.1429 | 0.6 | 0.000669 | 0.0006905 | 3.86e-05 | 5 | 13 | 21 | 30 | 8625 | 6114 | 3978 | 7029 | 10869 | 22 | 30 | 9071 | 8752 | 9747 | 12706 | 16953 |
| Mens Nike AirJordan Varsity Hoodie Jacket Grey / Black 451582-066 | Jordan | Outerwear & Coats | 903.0 | 409.06 | 903.0 | 493.94 | 8 | 1 | 2 | 1 | 4 | 2709.0 | 1481.82 | 0.547 | 0.6667 | 0.1429 | 0.125 | 0.8 | 0.0003345 | 0.000353 | 4.41e-05 | 5 | 14 | 149 | 153 | 5507 | 13264 | 844 | 7029 | 6105 | 5 | 6 | 7915 | 3055 | 20815 | 14338 | 7598 |
| Diesel Men's Lophophora Leather Jacket | Diesel | Outerwear & Coats | 898.0 | 408.59 | 1796.0 | 978.82 | 5 | 2 | 0 | 2 | 1 | 1796.0 | 978.82 | 0.545 | 0.0 | 0.6667 | 0.4 | 0.3333 | 0.0006653 | 0.0006996 | 2.76e-05 | 28 | 15 | 29 | 28 | 16887 | 6114 | 13463 | 2100 | 23197 | 28 | 29 | 8121 | 13463 | 1185 | 1689 | 24854 |

</div>

**Top products by Completion Rate**

```sql
WITH first_layer AS (
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
WHERE unit_orders_placed_rank <= 15
ORDER BY
  completion_rate_rank ASC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HUGO BOSS Men's Long Pant | HUGO BOSS | Sleep & Lounge | 74.72 | 28.3 | 1033.11 | 648.16 | 33 | 14 | 0 | 3 | 16 | 233.01 | 138.21 | 0.6274 | 0.0 | 0.4667 | 0.0909 | 0.5333 | 0.0003827 | 0.0004632 | 0.000182 | 6501 | 9383 | 113 | 75 | 6 | 1 | 13463 | 526 | 7 | 2702 | 2165 | 933 | 13463 | 6418 | 16872 | 19494 |
| Hanes Men's 4 Pack Boxer Brief | Hanes | Underwear | 25.0 | 11.52 | 250.0 | 133.47 | 28 | 10 | 2 | 5 | 11 | 175.0 | 92.77 | 0.5339 | 0.1667 | 0.4348 | 0.1786 | 0.5238 | 9.26e-05 | 9.54e-05 | 0.0001545 | 19651 | 20997 | 2432 | 2340 | 9 | 4 | 844 | 24 | 43 | 4152 | 3935 | 9232 | 13196 | 6738 | 10715 | 19500 |
| Joseph Abboud Men's Two-button Side Vent Sport Coat | Joseph Abboud | Suits & Sport Coats | 264.0 | 101.9 | 2904.0 | 1759.82 | 30 | 11 | 2 | 2 | 15 | 1056.0 | 656.57 | 0.606 | 0.1538 | 0.3929 | 0.0667 | 0.5769 | 0.0010758 | 0.0012577 | 0.0001655 | 430 | 734 | 6 | 5 | 7 | 3 | 844 | 2100 | 11 | 112 | 91 | 2144 | 13388 | 9081 | 17408 | 18610 |
| Volcom Men's Vorta Slim Straight Leg Fit Jean | Volcom | Jeans | 73.57 | 41.13 | 574.85 | 249.86 | 27 | 8 | 1 | 4 | 14 | 387.8 | 166.89 | 0.4347 | 0.1111 | 0.3478 | 0.1481 | 0.6364 | 0.0002129 | 0.0001786 | 0.0001489 | 6603 | 5251 | 467 | 746 | 12 | 16 | 3978 | 126 | 22 | 1091 | 1537 | 18678 | 13456 | 9743 | 12705 | 16487 |
| Wrangler Men's Rugged Wear Classic Fit Jean | Wrangler | Jeans | 40.87 | 22.23 | 367.56 | 169.24 | 38 | 9 | 5 | 9 | 15 | 596.43 | 273.96 | 0.4604 | 0.3571 | 0.3103 | 0.2368 | 0.625 | 0.0001362 | 0.000121 | 0.0002096 | 13688 | 12514 | 1205 | 1552 | 3 | 5 | 5 | 1 | 11 | 440 | 628 | 16340 | 8749 | 13014 | 7776 | 16547 |
| True Religion Men's Ricky Straight Leg Jean | True Religion | Jeans | 227.86 | 123.14 | 1452.0 | 661.01 | 28 | 7 | 1 | 5 | 15 | 1430.0 | 645.85 | 0.4552 | 0.125 | 0.3043 | 0.1786 | 0.6818 | 0.0005379 | 0.0004724 | 0.0001545 | 646 | 406 | 45 | 69 | 9 | 33 | 3978 | 24 | 11 | 57 | 95 | 16801 | 13444 | 13032 | 10715 | 12986 |
| Wrangler Men's Genuine Tampa Cargo Short | Wrangler | Shorts | 31.37 | 15.61 | 229.94 | 116.44 | 29 | 7 | 1 | 5 | 16 | 179.94 | 90.54 | 0.5064 | 0.125 | 0.2917 | 0.1724 | 0.6957 | 8.52e-05 | 8.32e-05 | 0.00016 | 17403 | 17266 | 2818 | 2869 | 8 | 33 | 3978 | 24 | 7 | 3935 | 4081 | 11924 | 13444 | 13236 | 10730 | 12964 |
| Joe's Jeans Men's Slim Fit Straight Leg Brixton | Joe's Jeans | Jeans | 194.26 | 102.07 | 1353.0 | 647.44 | 27 | 7 | 3 | 2 | 15 | 976.0 | 458.49 | 0.4785 | 0.3 | 0.28 | 0.0741 | 0.6818 | 0.0005012 | 0.0004627 | 0.0001489 | 992 | 729 | 58 | 76 | 12 | 33 | 151 | 2100 | 11 | 133 | 207 | 14773 | 11276 | 14282 | 17370 | 12986 |
| Kenneth Cole REACTION Men's Passcase Wallet | Kenneth Cole REACTION | Accessories | 18.91 | 7.72 | 152.71 | 89.4 | 34 | 8 | 4 | 4 | 18 | 150.85 | 90.57 | 0.5854 | 0.3333 | 0.2667 | 0.1176 | 0.6923 | 5.66e-05 | 6.39e-05 | 0.0001876 | 23389 | 24481 | 4958 | 4188 | 4 | 16 | 30 | 126 | 4 | 5015 | 4078 | 3806 | 8752 | 14395 | 15553 | 12966 |
| Chaps Big and Tall Solid V-Neck Vest | Chaps | Sweaters | 39.88 | 20.32 | 279.16 | 134.91 | 28 | 7 | 4 | 1 | 16 | 199.4 | 99.06 | 0.4833 | 0.3636 | 0.2593 | 0.0357 | 0.6957 | 0.0001034 | 9.64e-05 | 0.0001545 | 14437 | 13747 | 2029 | 2288 | 9 | 33 | 30 | 7029 | 7 | 3354 | 3543 | 14237 | 8748 | 14407 | 17457 | 12964 |
| Wrangler Men's Wrancher Dress Jean | Wrangler | Jeans | 40.4 | 20.2 | 242.4 | 118.65 | 27 | 6 | 2 | 3 | 16 | 202.0 | 102.05 | 0.4895 | 0.25 | 0.25 | 0.1111 | 0.7273 | 8.98e-05 | 8.48e-05 | 0.0001489 | 13728 | 13816 | 2533 | 2788 | 12 | 84 | 844 | 526 | 7 | 3236 | 3382 | 13585 | 11344 | 14408 | 15570 | 11980 |
| 7 For All Mankind Men's Standard Classic Straight Leg Jean | 7 For All Mankind | Jeans | 157.45 | 80.97 | 1435.0 | 696.01 | 42 | 9 | 5 | 5 | 23 | 1673.0 | 844.04 | 0.485 | 0.3571 | 0.2432 | 0.119 | 0.7188 | 0.0005316 | 0.0004974 | 0.0002317 | 1798 | 1488 | 46 | 60 | 2 | 5 | 5 | 24 | 2 | 32 | 41 | 14028 | 8749 | 17091 | 15552 | 12034 |
| Wrangler Men's Premium Performance Cowboy Cut Jean | Wrangler | Jeans | 47.45 | 25.88 | 570.83 | 264.22 | 58 | 12 | 2 | 7 | 37 | 417.81 | 189.65 | 0.4629 | 0.1429 | 0.2353 | 0.1207 | 0.7551 | 0.0002115 | 0.0001888 | 0.00032 | 12004 | 10508 | 470 | 662 | 1 | 2 | 844 | 2 | 1 | 905 | 1224 | 16149 | 13389 | 17092 | 15548 | 9486 |
| Volcom Men's Kinkade Jean | Volcom | Jeans | 66.67 | 35.17 | 269.9 | 125.86 | 27 | 4 | 3 | 5 | 15 | 538.25 | 254.63 | 0.4663 | 0.4286 | 0.1818 | 0.1852 | 0.7895 | 0.0001 | 9e-05 | 0.0001489 | 7633 | 6807 | 2158 | 2560 | 12 | 776 | 151 | 24 | 11 | 562 | 723 | 15806 | 8270 | 19358 | 10467 | 9273 |
| True Religion Men's Ricky Straight Jean | True Religion | Jeans | 246.88 | 129.05 | 1366.0 | 666.07 | 34 | 5 | 4 | 3 | 22 | 1400.0 | 654.5 | 0.4876 | 0.4444 | 0.1613 | 0.0882 | 0.8148 | 0.000506 | 0.000476 | 0.0001876 | 534 | 354 | 56 | 65 | 4 | 251 | 30 | 526 | 3 | 63 | 92 | 13792 | 8264 | 20804 | 17143 | 7595 |

</div>

**Top products by Return Rate**

```sql
WITH first_layer AS (
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
WHERE lost_profit_rank <= 15
ORDER BY
  return_rate_rank ASC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IGIGI by Yuliya Raquel Plus Size Kandinsky Gown | IGIGI by Yuliya Raquel | Dresses | 325.0 | 136.17 | 0.0 | 0.0 | 13 | 0 | 3 | 5 | 5 | 2600.0 | 1510.6 |  | 1.0 | 0.0 | 0.3846 | 1.0 | 0.0 | 0.0 | 7.17e-05 | 236 | 300 | 22532 | 22532 | 423 | 22532 | 151 | 24 | 3026 | 7 | 5 | 22532 | 1 | 22532 | 2333 | 1 |
| MiH Jeans Women's Aztec Jacket | MiH Jeans | Blazers & Jackets | 495.0 | 169.79 | 0.0 | 0.0 | 6 | 0 | 2 | 2 | 2 | 1980.0 | 1300.86 |  | 1.0 | 0.0 | 0.3333 | 1.0 | 0.0 | 0.0 | 3.31e-05 | 74 | 157 | 22532 | 22532 | 12532 | 22532 | 844 | 2100 | 17069 | 16 | 11 | 22532 | 1 | 22532 | 2619 | 1 |
| Canada Goose Men's The Chateau Jacket | Canada Goose | Active | 815.0 | 337.41 | 0.0 | 0.0 | 6 | 0 | 1 | 4 | 1 | 4075.0 | 2387.95 |  | 1.0 | 0.0 | 0.6667 | 1.0 | 0.0 | 0.0 | 3.31e-05 | 31 | 39 | 22532 | 22532 | 12532 | 22532 | 3978 | 126 | 23197 | 1 | 1 | 22532 | 1 | 22532 | 154 | 1 |
| Canada Goose Women's Chilliwack Bomber | Canada Goose | Outerwear & Coats | 695.0 | 287.73 | 695.0 | 407.27 | 8 | 1 | 3 | 2 | 2 | 3475.0 | 2036.35 | 0.586 | 0.75 | 0.1667 | 0.25 | 0.6667 | 0.0002575 | 0.0002911 | 4.41e-05 | 46 | 52 | 294 | 240 | 5507 | 13264 | 151 | 2100 | 17069 | 3 | 2 | 3719 | 2834 | 19436 | 5542 | 12990 |
| Mens Nike AirJordan Varsity Hoodie Jacket Grey / Black 451582-066 | Jordan | Outerwear & Coats | 903.0 | 409.06 | 903.0 | 493.94 | 8 | 1 | 2 | 1 | 4 | 2709.0 | 1481.82 | 0.547 | 0.6667 | 0.1429 | 0.125 | 0.8 | 0.0003345 | 0.000353 | 4.41e-05 | 5 | 14 | 149 | 153 | 5507 | 13264 | 844 | 7029 | 6105 | 5 | 6 | 7915 | 3055 | 20815 | 14338 | 7598 |
| Joseph Abboud Men's Super 120's Two Button Side Vent Single Pleat Pant Tuxedo With Grosgrain Notch Lapel | Joseph Abboud | Suits & Sport Coats | 405.26 | 145.08 | 405.26 | 260.18 | 11 | 1 | 2 | 3 | 5 | 2026.3 | 1300.88 | 0.642 | 0.6667 | 0.125 | 0.2727 | 0.8333 | 0.0001501 | 0.0001859 | 6.07e-05 | 108 | 256 | 961 | 686 | 1161 | 13264 | 844 | 526 | 3026 | 13 | 10 | 361 | 3055 | 21675 | 5408 | 6580 |
| Canada Goose Women's Mystique | Canada Goose | Outerwear & Coats | 750.0 | 353.25 | 1500.0 | 793.5 | 6 | 2 | 3 | 0 | 1 | 2250.0 | 1190.25 | 0.529 | 0.6 | 0.3333 | 0.0 | 0.3333 | 0.0005557 | 0.0005671 | 3.31e-05 | 37 | 35 | 41 | 44 | 12532 | 6114 | 151 | 17458 | 23197 | 9 | 13 | 9645 | 4103 | 9747 | 17458 | 24854 |
| DOLCE & GABBANA DG4167 501/8G BLACK GRAY GRADIENT 5917 | Dolce & Gabbana | Accessories | 243.0 | 94.67 | 486.0 | 294.03 | 14 | 2 | 3 | 5 | 4 | 1944.0 | 1194.59 | 0.605 | 0.6 | 0.2222 | 0.3571 | 0.6667 | 0.00018 | 0.0002101 | 7.72e-05 | 541 | 948 | 707 | 527 | 268 | 6114 | 151 | 24 | 6105 | 18 | 12 | 2194 | 4103 | 17122 | 2614 | 12990 |
| Darla | Alpha Industries | Outerwear & Coats | 999.0 | 404.6 | 1998.0 | 1188.81 | 7 | 2 | 2 | 0 | 3 | 1998.0 | 1188.81 | 0.595 | 0.5 | 0.2857 | 0.0 | 0.6 | 0.0007401 | 0.0008496 | 3.86e-05 | 1 | 16 | 18 | 15 | 8625 | 6114 | 844 | 17458 | 10869 | 14 | 14 | 2925 | 4275 | 13238 | 17458 | 16953 |
| Magaschoni Women's Shimmer Jacket | Magaschoni | Blazers & Jackets | 698.0 | 258.96 | 698.0 | 439.04 | 6 | 1 | 1 | 2 | 2 | 2094.0 | 1317.13 | 0.629 | 0.5 | 0.25 | 0.3333 | 0.6667 | 0.0002586 | 0.0003138 | 3.31e-05 | 43 | 58 | 288 | 201 | 12532 | 13264 | 3978 | 2100 | 17069 | 12 | 9 | 839 | 4275 | 14408 | 2619 | 12990 |
| Canada Goose Women's Mystique | Canada Goose | Active | 750.0 | 280.5 | 750.0 | 469.5 | 9 | 1 | 1 | 2 | 5 | 2250.0 | 1408.5 | 0.626 | 0.5 | 0.1429 | 0.2222 | 0.8333 | 0.0002778 | 0.0003355 | 4.96e-05 | 37 | 53 | 230 | 170 | 3355 | 13264 | 3978 | 2100 | 3026 | 9 | 8 | 984 | 4275 | 20815 | 7837 | 6580 |
| Spyder Women's Jesst In Time Jacket | Spyder | Outerwear & Coats | 650.0 | 295.75 | 3250.0 | 1771.25 | 10 | 5 | 4 | 0 | 1 | 2600.0 | 1417.0 | 0.545 | 0.4444 | 0.5 | 0.0 | 0.1667 | 0.0012039 | 0.0012659 | 5.52e-05 | 52 | 50 | 3 | 4 | 1962 | 251 | 30 | 17458 | 23197 | 7 | 7 | 8121 | 8264 | 3269 | 17458 | 27059 |
| Woolrich Arctic Parka DF | Woolrich | Outerwear & Coats | 990.0 | 478.17 | 2970.0 | 1535.49 | 12 | 3 | 2 | 1 | 6 | 2970.0 | 1535.49 | 0.517 | 0.4 | 0.2727 | 0.0833 | 0.6667 | 0.0011002 | 0.0010974 | 6.62e-05 | 3 | 6 | 5 | 6 | 694 | 2358 | 844 | 7029 | 1398 | 4 | 4 | 10735 | 8312 | 14284 | 17144 | 12990 |
| The North Face Denali Down Mens Jacket 2013 | The North Face | Outerwear & Coats | 903.0 | 436.15 | 2709.0 | 1400.55 | 13 | 3 | 2 | 2 | 6 | 3612.0 | 1867.4 | 0.517 | 0.4 | 0.2727 | 0.1538 | 0.6667 | 0.0010035 | 0.001001 | 7.17e-05 | 5 | 10 | 7 | 7 | 423 | 2358 | 844 | 2100 | 1398 | 2 | 3 | 10735 | 8312 | 14284 | 12634 | 12990 |
| NIKE WOMEN'S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort* | Nike | Intimates | 903.0 | 512.0 | 0.0 | 0.0 | 4 | 0 | 0 | 3 | 1 | 2709.0 | 1173.0 |  |  | 0.0 | 0.75 | 1.0 | 0.0 | 0.0 | 2.21e-05 | 5 | 4 | 22532 | 22532 | 21053 | 22532 | 13463 | 526 | 23197 | 5 | 15 | 22532 | 25326 | 22532 | 109 | 1 |

</div>

**Top products by Cancellation Rate**

```sql
WITH first_layer AS (
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
WHERE unit_orders_placed_rank <= 15
ORDER BY
  cancellation_rate_rank ASC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Wrangler Men's Rugged Wear Classic Fit Jean | Wrangler | Jeans | 40.87 | 22.23 | 367.56 | 169.24 | 38 | 9 | 5 | 9 | 15 | 596.43 | 273.96 | 0.4604 | 0.3571 | 0.3103 | 0.2368 | 0.625 | 0.0001362 | 0.000121 | 0.0002096 | 13688 | 12514 | 1205 | 1552 | 3 | 5 | 5 | 1 | 11 | 440 | 628 | 16340 | 8749 | 13014 | 7776 | 16547 |
| Volcom Men's Kinkade Jean | Volcom | Jeans | 66.67 | 35.17 | 269.9 | 125.86 | 27 | 4 | 3 | 5 | 15 | 538.25 | 254.63 | 0.4663 | 0.4286 | 0.1818 | 0.1852 | 0.7895 | 0.0001 | 9e-05 | 0.0001489 | 7633 | 6807 | 2158 | 2560 | 12 | 776 | 151 | 24 | 11 | 562 | 723 | 15806 | 8270 | 19358 | 10467 | 9273 |
| True Religion Men's Ricky Straight Leg Jean | True Religion | Jeans | 227.86 | 123.14 | 1452.0 | 661.01 | 28 | 7 | 1 | 5 | 15 | 1430.0 | 645.85 | 0.4552 | 0.125 | 0.3043 | 0.1786 | 0.6818 | 0.0005379 | 0.0004724 | 0.0001545 | 646 | 406 | 45 | 69 | 9 | 33 | 3978 | 24 | 11 | 57 | 95 | 16801 | 13444 | 13032 | 10715 | 12986 |
| Hanes Men's 4 Pack Boxer Brief | Hanes | Underwear | 25.0 | 11.52 | 250.0 | 133.47 | 28 | 10 | 2 | 5 | 11 | 175.0 | 92.77 | 0.5339 | 0.1667 | 0.4348 | 0.1786 | 0.5238 | 9.26e-05 | 9.54e-05 | 0.0001545 | 19651 | 20997 | 2432 | 2340 | 9 | 4 | 844 | 24 | 43 | 4152 | 3935 | 9232 | 13196 | 6738 | 10715 | 19500 |
| Wrangler Men's Genuine Tampa Cargo Short | Wrangler | Shorts | 31.37 | 15.61 | 229.94 | 116.44 | 29 | 7 | 1 | 5 | 16 | 179.94 | 90.54 | 0.5064 | 0.125 | 0.2917 | 0.1724 | 0.6957 | 8.52e-05 | 8.32e-05 | 0.00016 | 17403 | 17266 | 2818 | 2869 | 8 | 33 | 3978 | 24 | 7 | 3935 | 4081 | 11924 | 13444 | 13236 | 10730 | 12964 |
| Volcom Men's Vorta Slim Straight Leg Fit Jean | Volcom | Jeans | 73.57 | 41.13 | 574.85 | 249.86 | 27 | 8 | 1 | 4 | 14 | 387.8 | 166.89 | 0.4347 | 0.1111 | 0.3478 | 0.1481 | 0.6364 | 0.0002129 | 0.0001786 | 0.0001489 | 6603 | 5251 | 467 | 746 | 12 | 16 | 3978 | 126 | 22 | 1091 | 1537 | 18678 | 13456 | 9743 | 12705 | 16487 |
| Wrangler Men's Premium Performance Cowboy Cut Jean | Wrangler | Jeans | 47.45 | 25.88 | 570.83 | 264.22 | 58 | 12 | 2 | 7 | 37 | 417.81 | 189.65 | 0.4629 | 0.1429 | 0.2353 | 0.1207 | 0.7551 | 0.0002115 | 0.0001888 | 0.00032 | 12004 | 10508 | 470 | 662 | 1 | 2 | 844 | 2 | 1 | 905 | 1224 | 16149 | 13389 | 17092 | 15548 | 9486 |
| 7 For All Mankind Men's Standard Classic Straight Leg Jean | 7 For All Mankind | Jeans | 157.45 | 80.97 | 1435.0 | 696.01 | 42 | 9 | 5 | 5 | 23 | 1673.0 | 844.04 | 0.485 | 0.3571 | 0.2432 | 0.119 | 0.7188 | 0.0005316 | 0.0004974 | 0.0002317 | 1798 | 1488 | 46 | 60 | 2 | 5 | 5 | 24 | 2 | 32 | 41 | 14028 | 8749 | 17091 | 15552 | 12034 |
| Kenneth Cole REACTION Men's Passcase Wallet | Kenneth Cole REACTION | Accessories | 18.91 | 7.72 | 152.71 | 89.4 | 34 | 8 | 4 | 4 | 18 | 150.85 | 90.57 | 0.5854 | 0.3333 | 0.2667 | 0.1176 | 0.6923 | 5.66e-05 | 6.39e-05 | 0.0001876 | 23389 | 24481 | 4958 | 4188 | 4 | 16 | 30 | 126 | 4 | 5015 | 4078 | 3806 | 8752 | 14395 | 15553 | 12966 |
| Wrangler Men's Wrancher Dress Jean | Wrangler | Jeans | 40.4 | 20.2 | 242.4 | 118.65 | 27 | 6 | 2 | 3 | 16 | 202.0 | 102.05 | 0.4895 | 0.25 | 0.25 | 0.1111 | 0.7273 | 8.98e-05 | 8.48e-05 | 0.0001489 | 13728 | 13816 | 2533 | 2788 | 12 | 84 | 844 | 526 | 7 | 3236 | 3382 | 13585 | 11344 | 14408 | 15570 | 11980 |
| HUGO BOSS Men's Long Pant | HUGO BOSS | Sleep & Lounge | 74.72 | 28.3 | 1033.11 | 648.16 | 33 | 14 | 0 | 3 | 16 | 233.01 | 138.21 | 0.6274 | 0.0 | 0.4667 | 0.0909 | 0.5333 | 0.0003827 | 0.0004632 | 0.000182 | 6501 | 9383 | 113 | 75 | 6 | 1 | 13463 | 526 | 7 | 2702 | 2165 | 933 | 13463 | 6418 | 16872 | 19494 |
| True Religion Men's Ricky Straight Jean | True Religion | Jeans | 246.88 | 129.05 | 1366.0 | 666.07 | 34 | 5 | 4 | 3 | 22 | 1400.0 | 654.5 | 0.4876 | 0.4444 | 0.1613 | 0.0882 | 0.8148 | 0.000506 | 0.000476 | 0.0001876 | 534 | 354 | 56 | 65 | 4 | 251 | 30 | 526 | 3 | 63 | 92 | 13792 | 8264 | 20804 | 17143 | 7595 |
| Joe's Jeans Men's Slim Fit Straight Leg Brixton | Joe's Jeans | Jeans | 194.26 | 102.07 | 1353.0 | 647.44 | 27 | 7 | 3 | 2 | 15 | 976.0 | 458.49 | 0.4785 | 0.3 | 0.28 | 0.0741 | 0.6818 | 0.0005012 | 0.0004627 | 0.0001489 | 992 | 729 | 58 | 76 | 12 | 33 | 151 | 2100 | 11 | 133 | 207 | 14773 | 11276 | 14282 | 17370 | 12986 |
| Dockers Men's Suit Separate Coat | Dockers | Suits & Sport Coats | 88.36 | 33.97 | 231.12 | 140.98 | 27 | 3 | 4 | 2 | 18 | 542.11 | 337.6 | 0.61 | 0.5714 | 0.12 | 0.0741 | 0.8571 | 8.56e-05 | 0.0001008 | 0.0001489 | 5094 | 7229 | 2783 | 2122 | 12 | 2358 | 30 | 2100 | 4 | 542 | 391 | 1873 | 4252 | 22129 | 17370 | 6057 |
| Joseph Abboud Men's Two-button Side Vent Sport Coat | Joseph Abboud | Suits & Sport Coats | 264.0 | 101.9 | 2904.0 | 1759.82 | 30 | 11 | 2 | 2 | 15 | 1056.0 | 656.57 | 0.606 | 0.1538 | 0.3929 | 0.0667 | 0.5769 | 0.0010758 | 0.0012577 | 0.0001655 | 430 | 734 | 6 | 5 | 7 | 3 | 844 | 2100 | 11 | 112 | 91 | 2144 | 13388 | 9081 | 17408 | 18610 |

</div>

**Top products by En Route Rate**

```sql
WITH first_layer AS (
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
WHERE unit_orders_placed_rank <= 15
ORDER BY
  en_route_rate_rank ASC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dockers Men's Suit Separate Coat | Dockers | Suits & Sport Coats | 88.36 | 33.97 | 231.12 | 140.98 | 27 | 3 | 4 | 2 | 18 | 542.11 | 337.6 | 0.61 | 0.5714 | 0.12 | 0.0741 | 0.8571 | 8.56e-05 | 0.0001008 | 0.0001489 | 5094 | 7229 | 2783 | 2122 | 12 | 2358 | 30 | 2100 | 4 | 542 | 391 | 1873 | 4252 | 22129 | 17370 | 6057 |
| True Religion Men's Ricky Straight Jean | True Religion | Jeans | 246.88 | 129.05 | 1366.0 | 666.07 | 34 | 5 | 4 | 3 | 22 | 1400.0 | 654.5 | 0.4876 | 0.4444 | 0.1613 | 0.0882 | 0.8148 | 0.000506 | 0.000476 | 0.0001876 | 534 | 354 | 56 | 65 | 4 | 251 | 30 | 526 | 3 | 63 | 92 | 13792 | 8264 | 20804 | 17143 | 7595 |
| Volcom Men's Kinkade Jean | Volcom | Jeans | 66.67 | 35.17 | 269.9 | 125.86 | 27 | 4 | 3 | 5 | 15 | 538.25 | 254.63 | 0.4663 | 0.4286 | 0.1818 | 0.1852 | 0.7895 | 0.0001 | 9e-05 | 0.0001489 | 7633 | 6807 | 2158 | 2560 | 12 | 776 | 151 | 24 | 11 | 562 | 723 | 15806 | 8270 | 19358 | 10467 | 9273 |
| Wrangler Men's Premium Performance Cowboy Cut Jean | Wrangler | Jeans | 47.45 | 25.88 | 570.83 | 264.22 | 58 | 12 | 2 | 7 | 37 | 417.81 | 189.65 | 0.4629 | 0.1429 | 0.2353 | 0.1207 | 0.7551 | 0.0002115 | 0.0001888 | 0.00032 | 12004 | 10508 | 470 | 662 | 1 | 2 | 844 | 2 | 1 | 905 | 1224 | 16149 | 13389 | 17092 | 15548 | 9486 |
| Wrangler Men's Wrancher Dress Jean | Wrangler | Jeans | 40.4 | 20.2 | 242.4 | 118.65 | 27 | 6 | 2 | 3 | 16 | 202.0 | 102.05 | 0.4895 | 0.25 | 0.25 | 0.1111 | 0.7273 | 8.98e-05 | 8.48e-05 | 0.0001489 | 13728 | 13816 | 2533 | 2788 | 12 | 84 | 844 | 526 | 7 | 3236 | 3382 | 13585 | 11344 | 14408 | 15570 | 11980 |
| 7 For All Mankind Men's Standard Classic Straight Leg Jean | 7 For All Mankind | Jeans | 157.45 | 80.97 | 1435.0 | 696.01 | 42 | 9 | 5 | 5 | 23 | 1673.0 | 844.04 | 0.485 | 0.3571 | 0.2432 | 0.119 | 0.7188 | 0.0005316 | 0.0004974 | 0.0002317 | 1798 | 1488 | 46 | 60 | 2 | 5 | 5 | 24 | 2 | 32 | 41 | 14028 | 8749 | 17091 | 15552 | 12034 |
| Wrangler Men's Genuine Tampa Cargo Short | Wrangler | Shorts | 31.37 | 15.61 | 229.94 | 116.44 | 29 | 7 | 1 | 5 | 16 | 179.94 | 90.54 | 0.5064 | 0.125 | 0.2917 | 0.1724 | 0.6957 | 8.52e-05 | 8.32e-05 | 0.00016 | 17403 | 17266 | 2818 | 2869 | 8 | 33 | 3978 | 24 | 7 | 3935 | 4081 | 11924 | 13444 | 13236 | 10730 | 12964 |
| Chaps Big and Tall Solid V-Neck Vest | Chaps | Sweaters | 39.88 | 20.32 | 279.16 | 134.91 | 28 | 7 | 4 | 1 | 16 | 199.4 | 99.06 | 0.4833 | 0.3636 | 0.2593 | 0.0357 | 0.6957 | 0.0001034 | 9.64e-05 | 0.0001545 | 14437 | 13747 | 2029 | 2288 | 9 | 33 | 30 | 7029 | 7 | 3354 | 3543 | 14237 | 8748 | 14407 | 17457 | 12964 |
| Kenneth Cole REACTION Men's Passcase Wallet | Kenneth Cole REACTION | Accessories | 18.91 | 7.72 | 152.71 | 89.4 | 34 | 8 | 4 | 4 | 18 | 150.85 | 90.57 | 0.5854 | 0.3333 | 0.2667 | 0.1176 | 0.6923 | 5.66e-05 | 6.39e-05 | 0.0001876 | 23389 | 24481 | 4958 | 4188 | 4 | 16 | 30 | 126 | 4 | 5015 | 4078 | 3806 | 8752 | 14395 | 15553 | 12966 |
| Joe's Jeans Men's Slim Fit Straight Leg Brixton | Joe's Jeans | Jeans | 194.26 | 102.07 | 1353.0 | 647.44 | 27 | 7 | 3 | 2 | 15 | 976.0 | 458.49 | 0.4785 | 0.3 | 0.28 | 0.0741 | 0.6818 | 0.0005012 | 0.0004627 | 0.0001489 | 992 | 729 | 58 | 76 | 12 | 33 | 151 | 2100 | 11 | 133 | 207 | 14773 | 11276 | 14282 | 17370 | 12986 |
| True Religion Men's Ricky Straight Leg Jean | True Religion | Jeans | 227.86 | 123.14 | 1452.0 | 661.01 | 28 | 7 | 1 | 5 | 15 | 1430.0 | 645.85 | 0.4552 | 0.125 | 0.3043 | 0.1786 | 0.6818 | 0.0005379 | 0.0004724 | 0.0001545 | 646 | 406 | 45 | 69 | 9 | 33 | 3978 | 24 | 11 | 57 | 95 | 16801 | 13444 | 13032 | 10715 | 12986 |
| Volcom Men's Vorta Slim Straight Leg Fit Jean | Volcom | Jeans | 73.57 | 41.13 | 574.85 | 249.86 | 27 | 8 | 1 | 4 | 14 | 387.8 | 166.89 | 0.4347 | 0.1111 | 0.3478 | 0.1481 | 0.6364 | 0.0002129 | 0.0001786 | 0.0001489 | 6603 | 5251 | 467 | 746 | 12 | 16 | 3978 | 126 | 22 | 1091 | 1537 | 18678 | 13456 | 9743 | 12705 | 16487 |
| Wrangler Men's Rugged Wear Classic Fit Jean | Wrangler | Jeans | 40.87 | 22.23 | 367.56 | 169.24 | 38 | 9 | 5 | 9 | 15 | 596.43 | 273.96 | 0.4604 | 0.3571 | 0.3103 | 0.2368 | 0.625 | 0.0001362 | 0.000121 | 0.0002096 | 13688 | 12514 | 1205 | 1552 | 3 | 5 | 5 | 1 | 11 | 440 | 628 | 16340 | 8749 | 13014 | 7776 | 16547 |
| Joseph Abboud Men's Two-button Side Vent Sport Coat | Joseph Abboud | Suits & Sport Coats | 264.0 | 101.9 | 2904.0 | 1759.82 | 30 | 11 | 2 | 2 | 15 | 1056.0 | 656.57 | 0.606 | 0.1538 | 0.3929 | 0.0667 | 0.5769 | 0.0010758 | 0.0012577 | 0.0001655 | 430 | 734 | 6 | 5 | 7 | 3 | 844 | 2100 | 11 | 112 | 91 | 2144 | 13388 | 9081 | 17408 | 18610 |
| HUGO BOSS Men's Long Pant | HUGO BOSS | Sleep & Lounge | 74.72 | 28.3 | 1033.11 | 648.16 | 33 | 14 | 0 | 3 | 16 | 233.01 | 138.21 | 0.6274 | 0.0 | 0.4667 | 0.0909 | 0.5333 | 0.0003827 | 0.0004632 | 0.000182 | 6501 | 9383 | 113 | 75 | 6 | 1 | 13463 | 526 | 7 | 2702 | 2165 | 933 | 13463 | 6418 | 16872 | 19494 |

</div>

**Top products by Units Completed**

```sql
WITH first_layer AS (
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
  units_completed_rank ASC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HUGO BOSS Men's Long Pant | HUGO BOSS | Sleep & Lounge | 74.72 | 28.3 | 1033.11 | 648.16 | 33 | 14 | 0 | 3 | 16 | 233.01 | 138.21 | 0.6274 | 0.0 | 0.4667 | 0.0909 | 0.5333 | 0.0003827 | 0.0004632 | 0.000182 | 6501 | 9383 | 113 | 75 | 6 | 1 | 13463 | 526 | 7 | 2702 | 2165 | 933 | 13463 | 6418 | 16872 | 19494 |
| Wrangler Men's Premium Performance Cowboy Cut Jean | Wrangler | Jeans | 47.45 | 25.88 | 570.83 | 264.22 | 58 | 12 | 2 | 7 | 37 | 417.81 | 189.65 | 0.4629 | 0.1429 | 0.2353 | 0.1207 | 0.7551 | 0.0002115 | 0.0001888 | 0.00032 | 12004 | 10508 | 470 | 662 | 1 | 2 | 844 | 2 | 1 | 905 | 1224 | 16149 | 13389 | 17092 | 15548 | 9486 |
| Joseph Abboud Men's Two-button Side Vent Sport Coat | Joseph Abboud | Suits & Sport Coats | 264.0 | 101.9 | 2904.0 | 1759.82 | 30 | 11 | 2 | 2 | 15 | 1056.0 | 656.57 | 0.606 | 0.1538 | 0.3929 | 0.0667 | 0.5769 | 0.0010758 | 0.0012577 | 0.0001655 | 430 | 734 | 6 | 5 | 7 | 3 | 844 | 2100 | 11 | 112 | 91 | 2144 | 13388 | 9081 | 17408 | 18610 |
| Hanes Men's 4 Pack Boxer Brief | Hanes | Underwear | 25.0 | 11.52 | 250.0 | 133.47 | 28 | 10 | 2 | 5 | 11 | 175.0 | 92.77 | 0.5339 | 0.1667 | 0.4348 | 0.1786 | 0.5238 | 9.26e-05 | 9.54e-05 | 0.0001545 | 19651 | 20997 | 2432 | 2340 | 9 | 4 | 844 | 24 | 43 | 4152 | 3935 | 9232 | 13196 | 6738 | 10715 | 19500 |
| Michael Kors Men's Marlow Wool-Blend Single-Breasted Fitted Top Coat | Michael Kors | Outerwear & Coats | 255.0 | 102.26 | 2295.0 | 1374.7 | 15 | 9 | 1 | 2 | 3 | 765.0 | 458.23 | 0.599 | 0.1 | 0.6923 | 0.1333 | 0.25 | 0.0008502 | 0.0009825 | 8.27e-05 | 469 | 728 | 13 | 8 | 187 | 5 | 3978 | 2100 | 10869 | 252 | 208 | 2612 | 13461 | 1184 | 14317 | 26348 |
| Joe's Jeans Men's Rebel Relaxed Fit Jean | Joe's Jeans | Jeans | 139.29 | 76.13 | 1296.69 | 583.03 | 26 | 9 | 0 | 3 | 14 | 339.69 | 166.11 | 0.4496 | 0.0 | 0.3913 | 0.1154 | 0.6087 | 0.0004803 | 0.0004167 | 0.0001434 | 2334 | 1721 | 68 | 102 | 17 | 5 | 13463 | 526 | 22 | 1403 | 1558 | 17357 | 13463 | 9082 | 15567 | 16952 |
| 7 For All Mankind Men's Standard Classic Straight Leg Jean | 7 For All Mankind | Jeans | 157.45 | 80.97 | 1435.0 | 696.01 | 42 | 9 | 5 | 5 | 23 | 1673.0 | 844.04 | 0.485 | 0.3571 | 0.2432 | 0.119 | 0.7188 | 0.0005316 | 0.0004974 | 0.0002317 | 1798 | 1488 | 46 | 60 | 2 | 5 | 5 | 24 | 2 | 32 | 41 | 14028 | 8749 | 17091 | 15552 | 12034 |
| 3-Piece Matching Set Laura High Quality Strapless Bra Thong & Bikini #SL101084 Made in Colombia | Laura | Intimates | 41.95 | 20.45 | 377.55 | 193.56 | 13 | 9 | 0 | 2 | 2 | 83.9 | 42.79 | 0.5127 | 0.0 | 0.8182 | 0.1538 | 0.1818 | 0.0001399 | 0.0001383 | 7.17e-05 | 13574 | 13665 | 1157 | 1202 | 423 | 5 | 13463 | 2100 | 17069 | 9768 | 9702 | 11272 | 13463 | 606 | 12634 | 27058 |
| State O Maine Big and Tall Fashion Flannel Pajama | KNOTHE CORP. | Sleep & Lounge | 36.88 | 15.59 | 331.92 | 192.51 | 21 | 9 | 5 | 1 | 6 | 221.28 | 127.31 | 0.58 | 0.3571 | 0.45 | 0.0476 | 0.4 | 0.000123 | 0.0001376 | 0.0001158 | 15350 | 17283 | 1492 | 1214 | 50 | 5 | 5 | 7029 | 1398 | 2854 | 2454 | 4293 | 8749 | 6490 | 17453 | 23875 |
| JiMarti JM01 Sunglasses for Golf Fishing Cycling-Unbreakable-... Frame | JiMarti | Accessories | 29.95 | 11.92 | 269.55 | 161.1 | 22 | 9 | 2 | 2 | 9 | 119.8 | 72.12 | 0.5977 | 0.1818 | 0.45 | 0.0909 | 0.5 | 9.99e-05 | 0.0001151 | 0.0001214 | 18166 | 20613 | 2175 | 1707 | 43 | 5 | 844 | 2100 | 140 | 6868 | 5540 | 2758 | 13193 | 6490 | 16872 | 19501 |
| PAIGE Women's Skyline Skinny Jean | PAIGE | Jeans | 158.0 | 90.19 | 1422.0 | 608.93 | 19 | 9 | 0 | 2 | 8 | 316.0 | 135.88 | 0.4282 | 0.0 | 0.5294 | 0.1053 | 0.4706 | 0.0005268 | 0.0004352 | 0.0001048 | 1714 | 1108 | 48 | 90 | 72 | 5 | 13463 | 2100 | 295 | 1575 | 2230 | 19172 | 13463 | 3268 | 16363 | 23444 |
| Motherhood Maternity: Sports Clip Down Nursing Bra | Motherhood Maternity | Maternity | 22.54 | 10.46 | 200.82 | 108.99 | 25 | 9 | 2 | 3 | 11 | 112.9 | 60.37 | 0.5427 | 0.1818 | 0.4091 | 0.12 | 0.55 | 7.44e-05 | 7.79e-05 | 0.0001379 | 21822 | 22052 | 3297 | 3165 | 21 | 5 | 844 | 526 | 43 | 7249 | 6811 | 8373 | 13193 | 7481 | 15549 | 19449 |
| Belly Bandit post pregnancy tummy wrap belly band original Nude | Belly Bandit | Maternity | 54.95 | 23.79 | 489.55 | 279.96 | 20 | 9 | 1 | 2 | 8 | 169.85 | 97.62 | 0.5719 | 0.1 | 0.5 | 0.1 | 0.4706 | 0.0001813 | 0.0002001 | 0.0001103 | 9960 | 11605 | 701 | 588 | 59 | 5 | 3978 | 2100 | 295 | 4325 | 3628 | 5219 | 13461 | 3269 | 16366 | 23444 |
| Wrangler Men's Rugged Wear Classic Fit Jean | Wrangler | Jeans | 40.87 | 22.23 | 367.56 | 169.24 | 38 | 9 | 5 | 9 | 15 | 596.43 | 273.96 | 0.4604 | 0.3571 | 0.3103 | 0.2368 | 0.625 | 0.0001362 | 0.000121 | 0.0002096 | 13688 | 12514 | 1205 | 1552 | 3 | 5 | 5 | 1 | 11 | 440 | 628 | 16340 | 8749 | 13014 | 7776 | 16547 |
| Ray-Ban Unisex RB4105 Folding Wayfarer Sunglasses | Ray-Ban | Accessories | 99.65 | 36.84 | 896.85 | 562.92 | 18 | 9 | 2 | 3 | 4 | 498.25 | 313.8 | 0.6277 | 0.1818 | 0.6 | 0.1667 | 0.3077 | 0.0003322 | 0.0004023 | 9.93e-05 | 4069 | 6340 | 161 | 113 | 87 | 5 | 844 | 526 | 6105 | 666 | 476 | 932 | 13193 | 2189 | 10731 | 26246 |

</div>

**Top products by Units Returned**

```sql
WITH first_layer AS (
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
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kenneth Cole Men's Straight Leg Jean | Kenneth Cole | Jeans | 54.25 | 27.11 | 54.99 | 26.89 | 24 | 1 | 7 | 4 | 12 | 632.25 | 318.8 | 0.489 | 0.875 | 0.05 | 0.1667 | 0.9231 | 2.04e-05 | 1.92e-05 | 0.0001324 | 10100 | 9920 | 13356 | 13628 | 30 | 13264 | 1 | 126 | 37 | 380 | 462 | 13602 | 2795 | 22531 | 10731 | 5642 |
| Alex Stevens Men's Chevron Cuff Cardigan | Alex Stevens | Sweaters | 26.0 | 11.78 | 26.0 | 14.22 | 14 | 1 | 7 | 0 | 6 | 182.0 | 99.55 | 0.5469 | 0.875 | 0.0714 | 0.0 | 0.8571 | 9.6e-06 | 1.02e-05 | 7.72e-05 | 19363 | 20777 | 18768 | 18407 | 268 | 13264 | 1 | 17458 | 1398 | 3788 | 3516 | 7983 | 2795 | 22525 | 17458 | 6057 |
| Womenâ€™s UA Baseâ„¢ 4.0 Leggings Bottoms by Under Armour | Under Armour | Active | 63.99 | 23.93 | 127.98 | 80.12 | 12 | 2 | 6 | 2 | 2 | 511.92 | 320.46 | 0.626 | 0.75 | 0.2 | 0.1667 | 0.5 | 4.74e-05 | 5.73e-05 | 6.62e-05 | 8152 | 11520 | 6273 | 4860 | 694 | 6114 | 3 | 2100 | 17069 | 616 | 453 | 984 | 2834 | 17510 | 10731 | 19501 |
| G by GUESS Cosmos Slit-Front Top | G by GUESS | Tops & Tees | 29.5 | 16.87 | 88.5 | 37.88 | 13 | 3 | 6 | 1 | 3 | 206.5 | 88.38 | 0.428 | 0.6667 | 0.25 | 0.0769 | 0.5 | 3.28e-05 | 2.71e-05 | 7.17e-05 | 18349 | 16195 | 9301 | 10674 | 423 | 2358 | 3 | 7029 | 10869 | 3172 | 4221 | 19180 | 3055 | 14408 | 17286 | 19501 |
| G-Star Men's Attacc Straight Vintage Jean | G-Star | Jeans | 210.0 | 102.9 | 210.0 | 107.1 | 7 | 1 | 5 | 0 | 1 | 1050.0 | 535.5 | 0.51 | 0.8333 | 0.1429 | 0.0 | 0.5 | 7.78e-05 | 7.65e-05 | 3.86e-05 | 737 | 713 | 3106 | 3251 | 8625 | 13264 | 5 | 17458 | 23197 | 113 | 132 | 11510 | 2797 | 20815 | 17458 | 19501 |
| Quiksilver Waterman Men's Cabo 3 Walkshort | Quiksilver | Shorts | 35.98 | 18.39 | 35.98 | 17.59 | 10 | 1 | 5 | 1 | 3 | 215.88 | 105.57 | 0.4889 | 0.8333 | 0.1111 | 0.1 | 0.75 | 1.33e-05 | 1.26e-05 | 5.52e-05 | 15686 | 15023 | 16878 | 17002 | 1962 | 13264 | 5 | 7029 | 10869 | 2994 | 3212 | 13683 | 2797 | 22130 | 16366 | 9487 |
| Icebreaker Men's Kodiak Zip Jacket | Icebreaker | Outerwear & Coats | 250.0 | 122.5 | 250.0 | 127.5 | 13 | 1 | 5 | 1 | 6 | 1500.0 | 765.0 | 0.51 | 0.8333 | 0.0833 | 0.0769 | 0.8571 | 9.26e-05 | 9.11e-05 | 7.17e-05 | 480 | 413 | 2432 | 2507 | 423 | 13264 | 5 | 7029 | 1398 | 43 | 60 | 11510 | 2797 | 22497 | 17286 | 6057 |
| Levi's Women's Demi Curve Slim Fit Jean | Levi's | Jeans | 44.99 | 25.36 | 359.92 | 158.59 | 22 | 8 | 5 | 3 | 6 | 359.92 | 157.29 | 0.4406 | 0.3846 | 0.4211 | 0.1364 | 0.4286 | 0.0001333 | 0.0001133 | 0.0001214 | 12553 | 10773 | 1272 | 1757 | 43 | 16 | 5 | 526 | 1398 | 1228 | 1730 | 18170 | 8724 | 7452 | 14315 | 23541 |
| Ames Walker Style 166 Men's Microfiber Firm Support Travel Socks 15-20 - Available in Various Sizes and Colors | Ames | Socks | 12.99 | 8.07 | 12.99 | 4.92 | 11 | 1 | 5 | 2 | 3 | 90.93 | 34.46 | 0.3788 | 0.8333 | 0.1111 | 0.1818 | 0.75 | 4.8e-06 | 3.5e-06 | 6.07e-05 | 25756 | 24123 | 21580 | 22067 | 1161 | 13264 | 5 | 2100 | 10869 | 8965 | 11517 | 21711 | 2797 | 22130 | 10468 | 9487 |
| Under Armour Igniter Pro Sport Sunglasses | Under Armour | Accessories | 94.99 | 41.47 | 284.97 | 162.72 | 17 | 3 | 5 | 3 | 6 | 759.92 | 424.04 | 0.571 | 0.625 | 0.2143 | 0.1765 | 0.6667 | 0.0001056 | 0.0001163 | 9.38e-05 | 4573 | 5187 | 1952 | 1668 | 103 | 2358 | 5 | 526 | 1398 | 255 | 249 | 5261 | 4099 | 17490 | 10717 | 12990 |
| Men's Superior 150s Single Breasted Two Button Black Pinstripe Dress Suit European Cut | Giorgio Cerruti | Suits & Sport Coats | 69.95 | 27.98 | 209.85 | 125.91 | 16 | 3 | 5 | 0 | 8 | 349.75 | 209.85 | 0.6 | 0.625 | 0.1875 | 0.0 | 0.7273 | 7.77e-05 | 9e-05 | 8.83e-05 | 6978 | 9517 | 3144 | 2557 | 150 | 2358 | 5 | 17458 | 295 | 1333 | 1043 | 2533 | 4099 | 19354 | 17458 | 11980 |
| Wrangler Men's Rugged Wear Classic Fit Jean | Wrangler | Jeans | 40.87 | 22.23 | 367.56 | 169.24 | 38 | 9 | 5 | 9 | 15 | 596.43 | 273.96 | 0.4604 | 0.3571 | 0.3103 | 0.2368 | 0.625 | 0.0001362 | 0.000121 | 0.0002096 | 13688 | 12514 | 1205 | 1552 | 3 | 5 | 5 | 1 | 11 | 440 | 628 | 16340 | 8749 | 13014 | 7776 | 16547 |
| Wrangler Men's Original Cowboy Cut Relaxed Fit Jean | Wrangler | Jeans | 42.99 | 22.67 | 228.46 | 108.63 | 25 | 5 | 5 | 7 | 8 | 493.18 | 228.73 | 0.4755 | 0.5 | 0.2778 | 0.28 | 0.6154 | 8.46e-05 | 7.76e-05 | 0.0001379 | 13180 | 12269 | 2826 | 3184 | 21 | 251 | 5 | 2 | 295 | 687 | 895 | 15040 | 4275 | 14283 | 5404 | 16940 |
| Robert Graham Men's Cheshire | Robert Graham | Tops & Tees | 179.99 | 92.69 | 179.99 | 87.3 | 11 | 1 | 5 | 1 | 4 | 1079.94 | 523.77 | 0.485 | 0.8333 | 0.1 | 0.0909 | 0.8 | 6.67e-05 | 6.24e-05 | 6.07e-05 | 1179 | 1014 | 3947 | 4329 | 1161 | 13264 | 5 | 7029 | 6105 | 110 | 145 | 14028 | 2797 | 22369 | 16872 | 7598 |
| Tolani Women's Daphne Top | Tolani | Tops & Tees | 194.0 | 104.95 | 388.0 | 178.09 | 12 | 2 | 5 | 1 | 4 | 1164.0 | 534.28 | 0.459 | 0.7143 | 0.1818 | 0.0833 | 0.6667 | 0.0001437 | 0.0001273 | 6.62e-05 | 993 | 654 | 1103 | 1402 | 694 | 6114 | 5 | 7029 | 6105 | 103 | 134 | 16449 | 3052 | 19358 | 17144 | 12990 |

</div>

**Top products by Units Cancelled**

```sql
WITH first_layer AS (
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
  units_cancelled_rank ASC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Wrangler Men's Rugged Wear Classic Fit Jean | Wrangler | Jeans | 40.87 | 22.23 | 367.56 | 169.24 | 38 | 9 | 5 | 9 | 15 | 596.43 | 273.96 | 0.4604 | 0.3571 | 0.3103 | 0.2368 | 0.625 | 0.0001362 | 0.000121 | 0.0002096 | 13688 | 12514 | 1205 | 1552 | 3 | 5 | 5 | 1 | 11 | 440 | 628 | 16340 | 8749 | 13014 | 7776 | 16547 |
| Wrangler Men's Original Cowboy Cut Relaxed Fit Jean | Wrangler | Jeans | 42.99 | 22.67 | 228.46 | 108.63 | 25 | 5 | 5 | 7 | 8 | 493.18 | 228.73 | 0.4755 | 0.5 | 0.2778 | 0.28 | 0.6154 | 8.46e-05 | 7.76e-05 | 0.0001379 | 13180 | 12269 | 2826 | 3184 | 21 | 251 | 5 | 2 | 295 | 687 | 895 | 15040 | 4275 | 14283 | 5404 | 16940 |
| ExOfficio Men's Insect Shield Ziwa Convertible Pant | ExOfficio | Pants | 99.0 | 43.86 | 198.0 | 110.29 | 13 | 2 | 1 | 7 | 3 | 792.0 | 441.14 | 0.557 | 0.3333 | 0.3333 | 0.5385 | 0.6 | 7.33e-05 | 7.88e-05 | 7.17e-05 | 4113 | 4766 | 3453 | 3105 | 423 | 6114 | 3978 | 2 | 10869 | 234 | 228 | 6818 | 8752 | 9747 | 476 | 16953 |
| VH Apparel - Kissables Shea Butter Infused Double Layer Socks - One Size | VH Apparel - Kissables | Socks & Hosiery | 11.49 | 4.12 | 22.98 | 14.73 | 12 | 2 | 0 | 7 | 3 | 80.43 | 51.56 | 0.641 | 0.0 | 0.4 | 0.5833 | 0.6 | 8.5e-06 | 1.05e-05 | 6.62e-05 | 26551 | 27584 | 19789 | 18178 | 694 | 6114 | 13463 | 2 | 10869 | 9911 | 8134 | 403 | 13463 | 7482 | 426 | 16953 |
| WeSC Men's Eddy Chino Pant | WESC | Pants | 73.62 | 33.02 | 300.95 | 165.16 | 25 | 4 | 2 | 7 | 12 | 657.75 | 363.33 | 0.5488 | 0.3333 | 0.2222 | 0.28 | 0.75 | 0.0001115 | 0.000118 | 0.0001379 | 6601 | 7527 | 1711 | 1625 | 21 | 776 | 844 | 2 | 37 | 350 | 333 | 7797 | 8752 | 17122 | 5404 | 9487 |
| Wrangler Men's Premium Performance Cowboy Cut Jean | Wrangler | Jeans | 47.45 | 25.88 | 570.83 | 264.22 | 58 | 12 | 2 | 7 | 37 | 417.81 | 189.65 | 0.4629 | 0.1429 | 0.2353 | 0.1207 | 0.7551 | 0.0002115 | 0.0001888 | 0.00032 | 12004 | 10508 | 470 | 662 | 1 | 2 | 844 | 2 | 1 | 905 | 1224 | 16149 | 13389 | 17092 | 15548 | 9486 |
| 7 For All Mankind Women's The Slim Cigarette Jean | 7 For All Mankind | Jeans | 157.64 | 84.21 | 495.99 | 230.84 | 17 | 3 | 0 | 7 | 7 | 993.96 | 464.0 | 0.4654 | 0.0 | 0.3 | 0.4118 | 0.7 | 0.0001837 | 0.000165 | 9.38e-05 | 1785 | 1344 | 678 | 856 | 103 | 2358 | 13463 | 2 | 623 | 129 | 200 | 15893 | 13463 | 13033 | 1688 | 12849 |
| Savane Men's Flat Front No-Iron Twill Pant | Savane | Pants | 41.19 | 18.35 | 121.97 | 68.51 | 20 | 3 | 3 | 6 | 8 | 369.91 | 205.55 | 0.5617 | 0.5 | 0.2143 | 0.3 | 0.7273 | 4.52e-05 | 4.9e-05 | 0.0001103 | 13643 | 15060 | 6515 | 5898 | 59 | 2358 | 151 | 8 | 295 | 1179 | 1080 | 6368 | 4275 | 17490 | 4443 | 11980 |
| Ed Garments Men's Three-Ply Pleated Dress Pant. 2680 | Ed Garments | Pants | 76.99 | 31.72 | 230.97 | 135.81 | 10 | 3 | 0 | 6 | 1 | 461.94 | 271.62 | 0.588 | 0.0 | 0.75 | 0.6 | 0.25 | 8.56e-05 | 9.71e-05 | 5.52e-05 | 6231 | 7981 | 2785 | 2261 | 1962 | 2358 | 13463 | 8 | 23197 | 780 | 639 | 3542 | 13463 | 746 | 331 | 26348 |
| Underworks Men's Padded Rear Boxer Brief for Butt Lift | Underworks | Underwear | 29.99 | 15.08 | 0.0 | 0.0 | 9 | 0 | 0 | 6 | 3 | 179.94 | 89.43 |  |  | 0.0 | 0.6667 | 1.0 | 0.0 | 0.0 | 4.96e-05 | 17719 | 17696 | 22532 | 22532 | 3355 | 22532 | 13463 | 8 | 10869 | 3935 | 4144 | 22532 | 25326 | 22532 | 154 | 1 |
| Volcom Men's Vapato Chino Pant | Volcom | Pants | 131.63 | 62.16 | 997.65 | 526.94 | 19 | 7 | 2 | 6 | 4 | 881.6 | 464.52 | 0.5282 | 0.2222 | 0.5385 | 0.3158 | 0.3636 | 0.0003696 | 0.0003766 | 0.0001048 | 2563 | 2619 | 121 | 128 | 72 | 33 | 844 | 8 | 6105 | 175 | 199 | 9720 | 12628 | 3262 | 4416 | 24848 |
| Tommy Hilfiger Mens Cambridge Passcase | Tommy Hilfiger | Accessories | 23.28 | 10.2 | 69.84 | 39.25 | 14 | 3 | 0 | 6 | 5 | 139.68 | 78.5 | 0.562 | 0.0 | 0.375 | 0.4286 | 0.625 | 2.59e-05 | 2.81e-05 | 7.72e-05 | 21572 | 22289 | 11414 | 10366 | 268 | 2358 | 13463 | 8 | 3026 | 5698 | 5005 | 6272 | 13463 | 9107 | 1436 | 16547 |
| Commando Sweaters GI Style Acrylic Command Sweater | ANS | Sweaters | 36.5 | 19.56 | 109.5 | 50.81 | 14 | 3 | 1 | 6 | 4 | 255.5 | 118.55 | 0.464 | 0.25 | 0.375 | 0.4286 | 0.5714 | 4.06e-05 | 3.63e-05 | 7.72e-05 | 15396 | 14224 | 7458 | 8189 | 268 | 2358 | 3978 | 8 | 6105 | 2306 | 2714 | 16011 | 11344 | 9107 | 1436 | 18611 |
| Columbia Men's Tall Cathedral Peak Vest | Columbia | Outerwear & Coats | 34.95 | 14.4 | 34.95 | 20.55 | 12 | 1 | 1 | 6 | 4 | 244.65 | 143.85 | 0.588 | 0.5 | 0.1667 | 0.5 | 0.8 | 1.29e-05 | 1.47e-05 | 6.62e-05 | 16246 | 18275 | 17146 | 15812 | 694 | 13264 | 3978 | 8 | 6105 | 2447 | 2014 | 3542 | 4275 | 19436 | 477 | 7598 |
| 3 PAIR -30 BELOW THERMAL WINTER SOCKS (MERINO WOOL) | J.B. Icelandic (Extreme Cold Activity) | Socks | 33.0 | 19.77 | 33.0 | 13.23 | 10 | 1 | 0 | 6 | 3 | 198.0 | 79.4 | 0.4009 | 0.0 | 0.25 | 0.6 | 0.75 | 1.22e-05 | 9.5e-06 | 5.52e-05 | 16766 | 14097 | 17399 | 18866 | 1962 | 13264 | 13463 | 8 | 10869 | 3376 | 4926 | 20898 | 13463 | 14408 | 331 | 9487 |

</div>

**Top products by Units En Route**

```sql
WITH first_layer AS (
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
  units_en_route_rank ASC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Wrangler Men's Premium Performance Cowboy Cut Jean | Wrangler | Jeans | 47.45 | 25.88 | 570.83 | 264.22 | 58 | 12 | 2 | 7 | 37 | 417.81 | 189.65 | 0.4629 | 0.1429 | 0.2353 | 0.1207 | 0.7551 | 0.0002115 | 0.0001888 | 0.00032 | 12004 | 10508 | 470 | 662 | 1 | 2 | 844 | 2 | 1 | 905 | 1224 | 16149 | 13389 | 17092 | 15548 | 9486 |
| 7 For All Mankind Men's Standard Classic Straight Leg Jean | 7 For All Mankind | Jeans | 157.45 | 80.97 | 1435.0 | 696.01 | 42 | 9 | 5 | 5 | 23 | 1673.0 | 844.04 | 0.485 | 0.3571 | 0.2432 | 0.119 | 0.7188 | 0.0005316 | 0.0004974 | 0.0002317 | 1798 | 1488 | 46 | 60 | 2 | 5 | 5 | 24 | 2 | 32 | 41 | 14028 | 8749 | 17091 | 15552 | 12034 |
| True Religion Men's Ricky Straight Jean | True Religion | Jeans | 246.88 | 129.05 | 1366.0 | 666.07 | 34 | 5 | 4 | 3 | 22 | 1400.0 | 654.5 | 0.4876 | 0.4444 | 0.1613 | 0.0882 | 0.8148 | 0.000506 | 0.000476 | 0.0001876 | 534 | 354 | 56 | 65 | 4 | 251 | 30 | 526 | 3 | 63 | 92 | 13792 | 8264 | 20804 | 17143 | 7595 |
| Kenneth Cole REACTION Men's Passcase Wallet | Kenneth Cole REACTION | Accessories | 18.91 | 7.72 | 152.71 | 89.4 | 34 | 8 | 4 | 4 | 18 | 150.85 | 90.57 | 0.5854 | 0.3333 | 0.2667 | 0.1176 | 0.6923 | 5.66e-05 | 6.39e-05 | 0.0001876 | 23389 | 24481 | 4958 | 4188 | 4 | 16 | 30 | 126 | 4 | 5015 | 4078 | 3806 | 8752 | 14395 | 15553 | 12966 |
| Dockers Men's Suit Separate Coat | Dockers | Suits & Sport Coats | 88.36 | 33.97 | 231.12 | 140.98 | 27 | 3 | 4 | 2 | 18 | 542.11 | 337.6 | 0.61 | 0.5714 | 0.12 | 0.0741 | 0.8571 | 8.56e-05 | 0.0001008 | 0.0001489 | 5094 | 7229 | 2783 | 2122 | 12 | 2358 | 30 | 2100 | 4 | 542 | 391 | 1873 | 4252 | 22129 | 17370 | 6057 |
| Wrangler Men's 20X No. 33 Relaxed Straight Leg Jean | Wrangler | Jeans | 55.0 | 29.66 | 220.0 | 100.87 | 24 | 4 | 1 | 2 | 17 | 165.0 | 74.2 | 0.4585 | 0.2 | 0.1818 | 0.0833 | 0.8095 | 8.15e-05 | 7.21e-05 | 0.0001324 | 9673 | 8784 | 2941 | 3526 | 30 | 776 | 3978 | 2100 | 6 | 4449 | 5375 | 16533 | 12637 | 19358 | 17144 | 7597 |
| Wrangler Men's Genuine Tampa Cargo Short | Wrangler | Shorts | 31.37 | 15.61 | 229.94 | 116.44 | 29 | 7 | 1 | 5 | 16 | 179.94 | 90.54 | 0.5064 | 0.125 | 0.2917 | 0.1724 | 0.6957 | 8.52e-05 | 8.32e-05 | 0.00016 | 17403 | 17266 | 2818 | 2869 | 8 | 33 | 3978 | 24 | 7 | 3935 | 4081 | 11924 | 13444 | 13236 | 10730 | 12964 |
| HUGO BOSS Men's Long Pant | HUGO BOSS | Sleep & Lounge | 74.72 | 28.3 | 1033.11 | 648.16 | 33 | 14 | 0 | 3 | 16 | 233.01 | 138.21 | 0.6274 | 0.0 | 0.4667 | 0.0909 | 0.5333 | 0.0003827 | 0.0004632 | 0.000182 | 6501 | 9383 | 113 | 75 | 6 | 1 | 13463 | 526 | 7 | 2702 | 2165 | 933 | 13463 | 6418 | 16872 | 19494 |
| Wrangler Men's Wrancher Dress Jean | Wrangler | Jeans | 40.4 | 20.2 | 242.4 | 118.65 | 27 | 6 | 2 | 3 | 16 | 202.0 | 102.05 | 0.4895 | 0.25 | 0.25 | 0.1111 | 0.7273 | 8.98e-05 | 8.48e-05 | 0.0001489 | 13728 | 13816 | 2533 | 2788 | 12 | 84 | 844 | 526 | 7 | 3236 | 3382 | 13585 | 11344 | 14408 | 15570 | 11980 |
| Chaps Big and Tall Solid V-Neck Vest | Chaps | Sweaters | 39.88 | 20.32 | 279.16 | 134.91 | 28 | 7 | 4 | 1 | 16 | 199.4 | 99.06 | 0.4833 | 0.3636 | 0.2593 | 0.0357 | 0.6957 | 0.0001034 | 9.64e-05 | 0.0001545 | 14437 | 13747 | 2029 | 2288 | 9 | 33 | 30 | 7029 | 7 | 3354 | 3543 | 14237 | 8748 | 14407 | 17457 | 12964 |
| TapouT Men's Lock Up Hoodie | TapouT | Fashion Hoodies & Sweatshirts | 36.61 | 20.6 | 229.12 | 103.62 | 23 | 7 | 0 | 1 | 15 | 39.6 | 16.16 | 0.4523 | 0.0 | 0.3182 | 0.0435 | 0.6818 | 8.49e-05 | 7.41e-05 | 0.0001269 | 15388 | 13556 | 2822 | 3414 | 41 | 33 | 13463 | 7029 | 11 | 16416 | 17785 | 17057 | 13463 | 13008 | 17454 | 12986 |
| Wrangler Men's Sarasota Agility Short | Wrangler | Shorts | 33.03 | 16.36 | 198.95 | 101.37 | 25 | 6 | 1 | 3 | 15 | 138.97 | 68.68 | 0.5095 | 0.1429 | 0.2727 | 0.12 | 0.7143 | 7.37e-05 | 7.24e-05 | 0.0001379 | 16765 | 16618 | 3447 | 3505 | 21 | 84 | 3978 | 526 | 11 | 5758 | 5901 | 11606 | 13389 | 14284 | 15549 | 12035 |
| True Religion Men's Ricky Straight Leg Jean | True Religion | Jeans | 227.86 | 123.14 | 1452.0 | 661.01 | 28 | 7 | 1 | 5 | 15 | 1430.0 | 645.85 | 0.4552 | 0.125 | 0.3043 | 0.1786 | 0.6818 | 0.0005379 | 0.0004724 | 0.0001545 | 646 | 406 | 45 | 69 | 9 | 33 | 3978 | 24 | 11 | 57 | 95 | 16801 | 13444 | 13032 | 10715 | 12986 |
| Volcom Men's Kinkade Jean | Volcom | Jeans | 66.67 | 35.17 | 269.9 | 125.86 | 27 | 4 | 3 | 5 | 15 | 538.25 | 254.63 | 0.4663 | 0.4286 | 0.1818 | 0.1852 | 0.7895 | 0.0001 | 9e-05 | 0.0001489 | 7633 | 6807 | 2158 | 2560 | 12 | 776 | 151 | 24 | 11 | 562 | 723 | 15806 | 8270 | 19358 | 10467 | 9273 |
| Wrangler Men's Rugged Wear Classic Fit Jean | Wrangler | Jeans | 40.87 | 22.23 | 367.56 | 169.24 | 38 | 9 | 5 | 9 | 15 | 596.43 | 273.96 | 0.4604 | 0.3571 | 0.3103 | 0.2368 | 0.625 | 0.0001362 | 0.000121 | 0.0002096 | 13688 | 12514 | 1205 | 1552 | 3 | 5 | 5 | 1 | 11 | 440 | 628 | 16340 | 8749 | 13014 | 7776 | 16547 |

</div>

**Top products by Lost Revenue**

```sql
WITH first_layer AS (
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
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Canada Goose Men's The Chateau Jacket | Canada Goose | Active | 815.0 | 337.41 | 0.0 | 0.0 | 6 | 0 | 1 | 4 | 1 | 4075.0 | 2387.95 |  | 1.0 | 0.0 | 0.6667 | 1.0 | 0.0 | 0.0 | 3.31e-05 | 31 | 39 | 22532 | 22532 | 12532 | 22532 | 3978 | 126 | 23197 | 1 | 1 | 22532 | 1 | 22532 | 154 | 1 |
| The North Face Denali Down Mens Jacket 2013 | The North Face | Outerwear & Coats | 903.0 | 436.15 | 2709.0 | 1400.55 | 13 | 3 | 2 | 2 | 6 | 3612.0 | 1867.4 | 0.517 | 0.4 | 0.2727 | 0.1538 | 0.6667 | 0.0010035 | 0.001001 | 7.17e-05 | 5 | 10 | 7 | 7 | 423 | 2358 | 844 | 2100 | 1398 | 2 | 3 | 10735 | 8312 | 14284 | 12634 | 12990 |
| Canada Goose Women's Chilliwack Bomber | Canada Goose | Outerwear & Coats | 695.0 | 287.73 | 695.0 | 407.27 | 8 | 1 | 3 | 2 | 2 | 3475.0 | 2036.35 | 0.586 | 0.75 | 0.1667 | 0.25 | 0.6667 | 0.0002575 | 0.0002911 | 4.41e-05 | 46 | 52 | 294 | 240 | 5507 | 13264 | 151 | 2100 | 17069 | 3 | 2 | 3719 | 2834 | 19436 | 5542 | 12990 |
| Woolrich Arctic Parka DF | Woolrich | Outerwear & Coats | 990.0 | 478.17 | 2970.0 | 1535.49 | 12 | 3 | 2 | 1 | 6 | 2970.0 | 1535.49 | 0.517 | 0.4 | 0.2727 | 0.0833 | 0.6667 | 0.0011002 | 0.0010974 | 6.62e-05 | 3 | 6 | 5 | 6 | 694 | 2358 | 844 | 7029 | 1398 | 4 | 4 | 10735 | 8312 | 14284 | 17144 | 12990 |
| Mens Nike AirJordan Varsity Hoodie Jacket Grey / Black 451582-066 | Jordan | Outerwear & Coats | 903.0 | 409.06 | 903.0 | 493.94 | 8 | 1 | 2 | 1 | 4 | 2709.0 | 1481.82 | 0.547 | 0.6667 | 0.1429 | 0.125 | 0.8 | 0.0003345 | 0.000353 | 4.41e-05 | 5 | 14 | 149 | 153 | 5507 | 13264 | 844 | 7029 | 6105 | 5 | 6 | 7915 | 3055 | 20815 | 14338 | 7598 |
| NIKE WOMEN'S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort* | Nike | Intimates | 903.0 | 512.0 | 0.0 | 0.0 | 4 | 0 | 0 | 3 | 1 | 2709.0 | 1173.0 |  |  | 0.0 | 0.75 | 1.0 | 0.0 | 0.0 | 2.21e-05 | 5 | 4 | 22532 | 22532 | 21053 | 22532 | 13463 | 526 | 23197 | 5 | 15 | 22532 | 25326 | 22532 | 109 | 1 |
| Spyder Women's Jesst In Time Jacket | Spyder | Outerwear & Coats | 650.0 | 295.75 | 3250.0 | 1771.25 | 10 | 5 | 4 | 0 | 1 | 2600.0 | 1417.0 | 0.545 | 0.4444 | 0.5 | 0.0 | 0.1667 | 0.0012039 | 0.0012659 | 5.52e-05 | 52 | 50 | 3 | 4 | 1962 | 251 | 30 | 17458 | 23197 | 7 | 7 | 8121 | 8264 | 3269 | 17458 | 27059 |
| IGIGI by Yuliya Raquel Plus Size Kandinsky Gown | IGIGI by Yuliya Raquel | Dresses | 325.0 | 136.17 | 0.0 | 0.0 | 13 | 0 | 3 | 5 | 5 | 2600.0 | 1510.6 |  | 1.0 | 0.0 | 0.3846 | 1.0 | 0.0 | 0.0 | 7.17e-05 | 236 | 300 | 22532 | 22532 | 423 | 22532 | 151 | 24 | 3026 | 7 | 5 | 22532 | 1 | 22532 | 2333 | 1 |
| Canada Goose Women's Mystique | Canada Goose | Active | 750.0 | 280.5 | 750.0 | 469.5 | 9 | 1 | 1 | 2 | 5 | 2250.0 | 1408.5 | 0.626 | 0.5 | 0.1429 | 0.2222 | 0.8333 | 0.0002778 | 0.0003355 | 4.96e-05 | 37 | 53 | 230 | 170 | 3355 | 13264 | 3978 | 2100 | 3026 | 9 | 8 | 984 | 4275 | 20815 | 7837 | 6580 |
| Canada Goose Women's Mystique | Canada Goose | Outerwear & Coats | 750.0 | 353.25 | 1500.0 | 793.5 | 6 | 2 | 3 | 0 | 1 | 2250.0 | 1190.25 | 0.529 | 0.6 | 0.3333 | 0.0 | 0.3333 | 0.0005557 | 0.0005671 | 3.31e-05 | 37 | 35 | 41 | 44 | 12532 | 6114 | 151 | 17458 | 23197 | 9 | 13 | 9645 | 4103 | 9747 | 17458 | 24854 |
| Arc'teryx Moray Jacket - Women's | Arc'teryx | Outerwear & Coats | 699.0 | 343.91 | 2097.0 | 1065.28 | 9 | 3 | 0 | 3 | 3 | 2097.0 | 1065.28 | 0.508 | 0.0 | 0.5 | 0.3333 | 0.5 | 0.0007768 | 0.0007613 | 4.96e-05 | 41 | 36 | 15 | 20 | 3355 | 2358 | 13463 | 526 | 10869 | 11 | 22 | 11720 | 13463 | 3269 | 2619 | 19501 |
| Magaschoni Women's Shimmer Jacket | Magaschoni | Blazers & Jackets | 698.0 | 258.96 | 698.0 | 439.04 | 6 | 1 | 1 | 2 | 2 | 2094.0 | 1317.13 | 0.629 | 0.5 | 0.25 | 0.3333 | 0.6667 | 0.0002586 | 0.0003138 | 3.31e-05 | 43 | 58 | 288 | 201 | 12532 | 13264 | 3978 | 2100 | 17069 | 12 | 9 | 839 | 4275 | 14408 | 2619 | 12990 |
| Joseph Abboud Men's Super 120's Two Button Side Vent Single Pleat Pant Tuxedo With Grosgrain Notch Lapel | Joseph Abboud | Suits & Sport Coats | 405.26 | 145.08 | 405.26 | 260.18 | 11 | 1 | 2 | 3 | 5 | 2026.3 | 1300.88 | 0.642 | 0.6667 | 0.125 | 0.2727 | 0.8333 | 0.0001501 | 0.0001859 | 6.07e-05 | 108 | 256 | 961 | 686 | 1161 | 13264 | 844 | 526 | 3026 | 13 | 10 | 361 | 3055 | 21675 | 5408 | 6580 |
| Darla | Alpha Industries | Outerwear & Coats | 999.0 | 404.6 | 1998.0 | 1188.81 | 7 | 2 | 2 | 0 | 3 | 1998.0 | 1188.81 | 0.595 | 0.5 | 0.2857 | 0.0 | 0.6 | 0.0007401 | 0.0008496 | 3.86e-05 | 1 | 16 | 18 | 15 | 8625 | 6114 | 844 | 17458 | 10869 | 14 | 14 | 2925 | 4275 | 13238 | 17458 | 16953 |
| Alpha Industries Rip Stop Short | Alpha Industries | Shorts | 999.0 | 482.52 | 999.0 | 516.48 | 8 | 1 | 1 | 1 | 5 | 1998.0 | 1032.97 | 0.517 | 0.5 | 0.1429 | 0.125 | 0.8333 | 0.0003701 | 0.0003691 | 4.41e-05 | 1 | 5 | 120 | 134 | 5507 | 13264 | 3978 | 7029 | 3026 | 14 | 25 | 10735 | 4275 | 20815 | 14338 | 6580 |

</div>

**Top products by Lost Profit**

```sql
WITH first_layer AS (
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
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Canada Goose Men's The Chateau Jacket | Canada Goose | Active | 815.0 | 337.41 | 0.0 | 0.0 | 6 | 0 | 1 | 4 | 1 | 4075.0 | 2387.95 |  | 1.0 | 0.0 | 0.6667 | 1.0 | 0.0 | 0.0 | 3.31e-05 | 31 | 39 | 22532 | 22532 | 12532 | 22532 | 3978 | 126 | 23197 | 1 | 1 | 22532 | 1 | 22532 | 154 | 1 |
| Canada Goose Women's Chilliwack Bomber | Canada Goose | Outerwear & Coats | 695.0 | 287.73 | 695.0 | 407.27 | 8 | 1 | 3 | 2 | 2 | 3475.0 | 2036.35 | 0.586 | 0.75 | 0.1667 | 0.25 | 0.6667 | 0.0002575 | 0.0002911 | 4.41e-05 | 46 | 52 | 294 | 240 | 5507 | 13264 | 151 | 2100 | 17069 | 3 | 2 | 3719 | 2834 | 19436 | 5542 | 12990 |
| The North Face Denali Down Mens Jacket 2013 | The North Face | Outerwear & Coats | 903.0 | 436.15 | 2709.0 | 1400.55 | 13 | 3 | 2 | 2 | 6 | 3612.0 | 1867.4 | 0.517 | 0.4 | 0.2727 | 0.1538 | 0.6667 | 0.0010035 | 0.001001 | 7.17e-05 | 5 | 10 | 7 | 7 | 423 | 2358 | 844 | 2100 | 1398 | 2 | 3 | 10735 | 8312 | 14284 | 12634 | 12990 |
| Woolrich Arctic Parka DF | Woolrich | Outerwear & Coats | 990.0 | 478.17 | 2970.0 | 1535.49 | 12 | 3 | 2 | 1 | 6 | 2970.0 | 1535.49 | 0.517 | 0.4 | 0.2727 | 0.0833 | 0.6667 | 0.0011002 | 0.0010974 | 6.62e-05 | 3 | 6 | 5 | 6 | 694 | 2358 | 844 | 7029 | 1398 | 4 | 4 | 10735 | 8312 | 14284 | 17144 | 12990 |
| IGIGI by Yuliya Raquel Plus Size Kandinsky Gown | IGIGI by Yuliya Raquel | Dresses | 325.0 | 136.17 | 0.0 | 0.0 | 13 | 0 | 3 | 5 | 5 | 2600.0 | 1510.6 |  | 1.0 | 0.0 | 0.3846 | 1.0 | 0.0 | 0.0 | 7.17e-05 | 236 | 300 | 22532 | 22532 | 423 | 22532 | 151 | 24 | 3026 | 7 | 5 | 22532 | 1 | 22532 | 2333 | 1 |
| Mens Nike AirJordan Varsity Hoodie Jacket Grey / Black 451582-066 | Jordan | Outerwear & Coats | 903.0 | 409.06 | 903.0 | 493.94 | 8 | 1 | 2 | 1 | 4 | 2709.0 | 1481.82 | 0.547 | 0.6667 | 0.1429 | 0.125 | 0.8 | 0.0003345 | 0.000353 | 4.41e-05 | 5 | 14 | 149 | 153 | 5507 | 13264 | 844 | 7029 | 6105 | 5 | 6 | 7915 | 3055 | 20815 | 14338 | 7598 |
| Spyder Women's Jesst In Time Jacket | Spyder | Outerwear & Coats | 650.0 | 295.75 | 3250.0 | 1771.25 | 10 | 5 | 4 | 0 | 1 | 2600.0 | 1417.0 | 0.545 | 0.4444 | 0.5 | 0.0 | 0.1667 | 0.0012039 | 0.0012659 | 5.52e-05 | 52 | 50 | 3 | 4 | 1962 | 251 | 30 | 17458 | 23197 | 7 | 7 | 8121 | 8264 | 3269 | 17458 | 27059 |
| Canada Goose Women's Mystique | Canada Goose | Active | 750.0 | 280.5 | 750.0 | 469.5 | 9 | 1 | 1 | 2 | 5 | 2250.0 | 1408.5 | 0.626 | 0.5 | 0.1429 | 0.2222 | 0.8333 | 0.0002778 | 0.0003355 | 4.96e-05 | 37 | 53 | 230 | 170 | 3355 | 13264 | 3978 | 2100 | 3026 | 9 | 8 | 984 | 4275 | 20815 | 7837 | 6580 |
| Magaschoni Women's Shimmer Jacket | Magaschoni | Blazers & Jackets | 698.0 | 258.96 | 698.0 | 439.04 | 6 | 1 | 1 | 2 | 2 | 2094.0 | 1317.13 | 0.629 | 0.5 | 0.25 | 0.3333 | 0.6667 | 0.0002586 | 0.0003138 | 3.31e-05 | 43 | 58 | 288 | 201 | 12532 | 13264 | 3978 | 2100 | 17069 | 12 | 9 | 839 | 4275 | 14408 | 2619 | 12990 |
| Joseph Abboud Men's Super 120's Two Button Side Vent Single Pleat Pant Tuxedo With Grosgrain Notch Lapel | Joseph Abboud | Suits & Sport Coats | 405.26 | 145.08 | 405.26 | 260.18 | 11 | 1 | 2 | 3 | 5 | 2026.3 | 1300.88 | 0.642 | 0.6667 | 0.125 | 0.2727 | 0.8333 | 0.0001501 | 0.0001859 | 6.07e-05 | 108 | 256 | 961 | 686 | 1161 | 13264 | 844 | 526 | 3026 | 13 | 10 | 361 | 3055 | 21675 | 5408 | 6580 |
| MiH Jeans Women's Aztec Jacket | MiH Jeans | Blazers & Jackets | 495.0 | 169.79 | 0.0 | 0.0 | 6 | 0 | 2 | 2 | 2 | 1980.0 | 1300.86 |  | 1.0 | 0.0 | 0.3333 | 1.0 | 0.0 | 0.0 | 3.31e-05 | 74 | 157 | 22532 | 22532 | 12532 | 22532 | 844 | 2100 | 17069 | 16 | 11 | 22532 | 1 | 22532 | 2619 | 1 |
| DOLCE & GABBANA DG4167 501/8G BLACK GRAY GRADIENT 5917 | Dolce & Gabbana | Accessories | 243.0 | 94.67 | 486.0 | 294.03 | 14 | 2 | 3 | 5 | 4 | 1944.0 | 1194.59 | 0.605 | 0.6 | 0.2222 | 0.3571 | 0.6667 | 0.00018 | 0.0002101 | 7.72e-05 | 541 | 948 | 707 | 527 | 268 | 6114 | 151 | 24 | 6105 | 18 | 12 | 2194 | 4103 | 17122 | 2614 | 12990 |
| Canada Goose Women's Mystique | Canada Goose | Outerwear & Coats | 750.0 | 353.25 | 1500.0 | 793.5 | 6 | 2 | 3 | 0 | 1 | 2250.0 | 1190.25 | 0.529 | 0.6 | 0.3333 | 0.0 | 0.3333 | 0.0005557 | 0.0005671 | 3.31e-05 | 37 | 35 | 41 | 44 | 12532 | 6114 | 151 | 17458 | 23197 | 9 | 13 | 9645 | 4103 | 9747 | 17458 | 24854 |
| Darla | Alpha Industries | Outerwear & Coats | 999.0 | 404.6 | 1998.0 | 1188.81 | 7 | 2 | 2 | 0 | 3 | 1998.0 | 1188.81 | 0.595 | 0.5 | 0.2857 | 0.0 | 0.6 | 0.0007401 | 0.0008496 | 3.86e-05 | 1 | 16 | 18 | 15 | 8625 | 6114 | 844 | 17458 | 10869 | 14 | 14 | 2925 | 4275 | 13238 | 17458 | 16953 |
| NIKE WOMEN'S PRO COMPRESSION SPORTS BRA *Outstanding Support and Comfort* | Nike | Intimates | 903.0 | 512.0 | 0.0 | 0.0 | 4 | 0 | 0 | 3 | 1 | 2709.0 | 1173.0 |  |  | 0.0 | 0.75 | 1.0 | 0.0 | 0.0 | 2.21e-05 | 5 | 4 | 22532 | 22532 | 21053 | 22532 | 13463 | 526 | 23197 | 5 | 15 | 22532 | 25326 | 22532 | 109 | 1 |

</div>


</details>
<details>
  <summary><strong>Bottom Products</strong></summary>

  <div style="margin-top: 12px;"></div>

**Bottom products by Revenue**

```sql
WITH first_layer AS (
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
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Marc Ecko Cut & Sew Men's Pinstripe and Plaid Pieced Vest | Marc Ecko Cut & Sew | Suits & Sport Coats | 47.43 | 17.83 | 0.0 | 0.0 | 10 | 0 | 0 | 3 | 7 | 142.29 | 88.79 |  |  | 0.0 | 0.3 | 1.0 | 0.0 | 0.0 | 5.52e-05 | 12005 | 15475 | 22532 | 22532 | 1962 | 22532 | 13463 | 526 | 623 | 5528 | 4189 | 22532 | 25326 | 22532 | 4443 | 1 |
| Dexter's Wings - Dexter T-shirt | Dexter | Tops & Tees | 19.95 | 11.11 | 0.0 | 0.0 | 5 | 0 | 1 | 1 | 3 | 39.9 | 17.68 |  | 1.0 | 0.0 | 0.2 | 1.0 | 0.0 | 0.0 | 2.76e-05 | 23040 | 21439 | 22532 | 22532 | 16887 | 22532 | 3978 | 7029 | 10869 | 16370 | 17124 | 22532 | 1 | 22532 | 8435 | 1 |
| RSQ Miami Womens Jeggings | RSQ | Pants & Capris | 39.99 | 22.07 | 0.0 | 0.0 | 4 | 0 | 1 | 1 | 2 | 79.98 | 35.83 |  | 1.0 | 0.0 | 0.25 | 1.0 | 0.0 | 0.0 | 2.21e-05 | 13925 | 12599 | 22532 | 22532 | 21053 | 22532 | 3978 | 7029 | 17069 | 10039 | 11208 | 22532 | 1 | 22532 | 5542 | 1 |
| Medela Sleep Bra Nude Large | Medela | Maternity | 15.99 | 6.88 | 0.0 | 0.0 | 7 | 0 | 3 | 1 | 3 | 63.96 | 36.46 |  | 1.0 | 0.0 | 0.1429 | 1.0 | 0.0 | 0.0 | 3.86e-05 | 24393 | 25240 | 22532 | 22532 | 8625 | 22532 | 151 | 7029 | 10869 | 12226 | 11055 | 22532 | 1 | 22532 | 12706 | 1 |
| Diesel Women's Louvboot Slim Flare Jean | Diesel | Jeans | 198.0 | 97.61 | 0.0 | 0.0 | 4 | 0 | 0 | 2 | 2 | 396.0 | 200.77 |  |  | 0.0 | 0.5 | 1.0 | 0.0 | 0.0 | 2.21e-05 | 875 | 836 | 22532 | 22532 | 21053 | 22532 | 13463 | 2100 | 17069 | 1005 | 1124 | 22532 | 25326 | 22532 | 477 | 1 |
| SockGuy Men's Wooligan Socks | SockGuy | Socks | 12.95 | 7.33 | 0.0 | 0.0 | 4 | 0 | 0 | 2 | 2 | 25.9 | 11.24 |  |  | 0.0 | 0.5 | 1.0 | 0.0 | 0.0 | 2.21e-05 | 25924 | 24844 | 22532 | 22532 | 21053 | 22532 | 13463 | 2100 | 17069 | 19080 | 19933 | 22532 | 25326 | 22532 | 477 | 1 |
| Allegra K Mens Casual Vertical Stripes Pattern Decor NEW Stylish Short Trousers Deep Beige W31 | Allegra K | Shorts | 15.95 | 7.99 | 0.0 | 0.0 | 6 | 0 | 1 | 0 | 5 | 15.95 | 7.96 |  | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 3.31e-05 | 24488 | 24197 | 22532 | 22532 | 12532 | 22532 | 3978 | 17458 | 3026 | 21250 | 21221 | 22532 | 1 | 22532 | 17458 | 1 |
| Southpole Men's Angled Cross With Shadowed Background Print Fashion T-Shirt | Southpole | Tops & Tees | 25.0 | 13.52 | 0.0 | 0.0 | 6 | 0 | 0 | 1 | 5 | 25.0 | 11.48 |  |  | 0.0 | 0.1667 | 1.0 | 0.0 | 0.0 | 3.31e-05 | 19651 | 19040 | 22532 | 22532 | 12532 | 22532 | 13463 | 7029 | 3026 | 19164 | 19837 | 22532 | 25326 | 22532 | 10731 | 1 |
| Brushed-Back Satin Pajamas - Women's Sizes | Carol Wright Gifts | Sleep & Lounge | 24.99 | 15.07 | 0.0 | 0.0 | 3 | 0 | 1 | 0 | 2 | 24.99 | 9.92 |  | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 1.65e-05 | 20698 | 17708 | 22532 | 22532 | 24645 | 22532 | 3978 | 17458 | 17069 | 19500 | 20477 | 22532 | 1 | 22532 | 17458 | 1 |
| Tommy Hilfiger Men's Tommy Tartan Boxer | Tommy Hilfiger | Underwear | 18.0 | 8.69 | 0.0 | 0.0 | 5 | 0 | 1 | 1 | 3 | 36.0 | 18.61 |  | 1.0 | 0.0 | 0.2 | 1.0 | 0.0 | 0.0 | 2.76e-05 | 23512 | 23579 | 22532 | 22532 | 16887 | 22532 | 3978 | 7029 | 10869 | 16903 | 16747 | 22532 | 1 | 22532 | 8435 | 1 |
| One Pair MarcolianiMen's Italian Cashmere and Silk Over-the-Calf Fancy Argyle Socks | Marcoliani Milano | Socks | 89.5 | 49.58 | 0.0 | 0.0 | 2 | 0 | 1 | 0 | 1 | 89.5 | 39.92 |  | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 1.1e-05 | 4936 | 3880 | 22532 | 22532 | 26863 | 22532 | 3978 | 17458 | 23197 | 9283 | 10290 | 22532 | 1 | 22532 | 17458 | 1 |
| Allegra K Ladies Dotted Double V Neck Banded Dress Pink White M | Allegra K | Dresses | 10.15 | 4.83 | 0.0 | 0.0 | 5 | 0 | 0 | 0 | 5 | 0.0 | 0.0 |  |  | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 2.76e-05 | 26937 | 27097 | 22532 | 22532 | 16887 | 22532 | 13463 | 17458 | 3026 | 22642 | 22642 | 22532 | 25326 | 22532 | 17458 | 1 |
| 7 For All Mankind Women's Relaxed Mid Roll Up Short Authentic Nakita | 7 For All Mankind | Shorts | 178.0 | 82.95 | 0.0 | 0.0 | 6 | 0 | 2 | 1 | 3 | 534.0 | 285.16 |  | 1.0 | 0.0 | 0.1667 | 1.0 | 0.0 | 0.0 | 3.31e-05 | 1246 | 1403 | 22532 | 22532 | 12532 | 22532 | 844 | 7029 | 10869 | 570 | 582 | 22532 | 1 | 22532 | 10731 | 1 |
| Fox Men's Essex Short | Fox | Shorts | 42.5 | 19.51 | 0.0 | 0.0 | 3 | 0 | 0 | 1 | 2 | 42.5 | 22.99 |  |  | 0.0 | 0.3333 | 1.0 | 0.0 | 0.0 | 1.65e-05 | 13301 | 14268 | 22532 | 22532 | 24645 | 22532 | 13463 | 7029 | 17069 | 15731 | 15034 | 22532 | 25326 | 22532 | 2619 | 1 |
| Motherhood Maternity: Plus Size Secret Fit Belly(r) Boot Cut Maternity Jeans | Motherhood Maternity | Maternity | 34.98 | 15.74 | 0.0 | 0.0 | 3 | 0 | 0 | 0 | 3 | 0.0 | 0.0 |  |  | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 1.65e-05 | 16197 | 17160 | 22532 | 22532 | 24645 | 22532 | 13463 | 17458 | 10869 | 22642 | 22642 | 22532 | 25326 | 22532 | 17458 | 1 |

</div>

**Bottom products by Profit**

```sql
WITH first_layer AS (
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
WHERE unit_orders_placed_rank <= 50
ORDER BY
  profit_rank DESC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HUGO BOSS Men's Bright Argyle Crew Sock | HUGO BOSS | Socks | 9.75 | 5.68 | 39.0 | 15.65 | 22 | 4 | 4 | 4 | 10 | 78.0 | 32.25 | 0.4013 | 0.5 | 0.2222 | 0.1818 | 0.7143 | 1.44e-05 | 1.12e-05 | 0.0001214 | 27342 | 26355 | 16327 | 17765 | 43 | 776 | 30 | 126 | 77 | 10368 | 12068 | 20837 | 4275 | 17122 | 10468 | 12035 |
| New Men's Sexy Center Patch Bikini Swimsuit 3G by Gregg Homme | Gregg Homme | Swim | 13.22 | 7.85 | 54.6 | 20.64 | 25 | 4 | 2 | 5 | 14 | 90.3 | 38.29 | 0.378 | 0.3333 | 0.2 | 0.2 | 0.7778 | 2.02e-05 | 1.48e-05 | 0.0001379 | 25672 | 24345 | 13422 | 15782 | 21 | 776 | 844 | 24 | 22 | 8973 | 10649 | 21721 | 8752 | 17510 | 8435 | 9281 |
| Kenneth Cole Men's Straight Leg Jean | Kenneth Cole | Jeans | 54.25 | 27.11 | 54.99 | 26.89 | 24 | 1 | 7 | 4 | 12 | 632.25 | 318.8 | 0.489 | 0.875 | 0.05 | 0.1667 | 0.9231 | 2.04e-05 | 1.92e-05 | 0.0001324 | 10100 | 9920 | 13356 | 13628 | 30 | 13264 | 1 | 126 | 37 | 380 | 462 | 13602 | 2795 | 22531 | 10731 | 5642 |
| Tommy Hilfiger Men Classic Fit T-shirt | Tommy Hilfiger | Tops & Tees | 21.99 | 12.22 | 65.97 | 28.41 | 25 | 3 | 2 | 5 | 15 | 153.93 | 70.63 | 0.4307 | 0.4 | 0.15 | 0.2 | 0.8333 | 2.44e-05 | 2.03e-05 | 0.0001379 | 22049 | 20333 | 11887 | 13165 | 21 | 2358 | 844 | 24 | 11 | 4954 | 5704 | 18998 | 8312 | 20814 | 8435 | 6580 |
| Volcom Juniors Pocket Blocket Long Sleeve Tee | Volcom | Tops & Tees | 27.0 | 15.34 | 81.0 | 33.86 | 21 | 3 | 4 | 5 | 9 | 243.0 | 107.41 | 0.418 | 0.5714 | 0.1875 | 0.2381 | 0.75 | 3e-05 | 2.42e-05 | 0.0001158 | 19072 | 17500 | 9846 | 11622 | 50 | 2358 | 30 | 24 | 140 | 2456 | 3131 | 20016 | 4252 | 19354 | 7773 | 9487 |
| Puma Men's Socks | PUMA | Socks | 13.0 | 7.78 | 90.0 | 35.98 | 24 | 7 | 1 | 5 | 11 | 78.0 | 31.36 | 0.3998 | 0.125 | 0.3684 | 0.2083 | 0.6111 | 3.33e-05 | 2.57e-05 | 0.0001324 | 25705 | 24414 | 8929 | 11107 | 30 | 33 | 3978 | 24 | 43 | 10368 | 12295 | 20955 | 13444 | 9637 | 8433 | 16951 |
| HUGO BOSS Men's Striped Crew Sock | HUGO BOSS | Socks | 13.0 | 8.14 | 104.0 | 40.17 | 24 | 8 | 3 | 4 | 9 | 91.0 | 33.33 | 0.3863 | 0.2727 | 0.4 | 0.1667 | 0.5294 | 3.85e-05 | 2.87e-05 | 0.0001324 | 25705 | 24062 | 7764 | 10157 | 30 | 16 | 151 | 126 | 140 | 8958 | 11794 | 21483 | 11342 | 7482 | 10731 | 19498 |
| Lilly Pulitzer Women's Callahan Short | Lilly Pulitzer | Shorts | 48.24 | 24.35 | 106.11 | 53.14 | 24 | 2 | 4 | 5 | 13 | 420.02 | 207.44 | 0.5008 | 0.6667 | 0.1053 | 0.2083 | 0.8667 | 3.93e-05 | 3.8e-05 | 0.0001324 | 11747 | 11307 | 7626 | 7813 | 30 | 6114 | 30 | 24 | 31 | 883 | 1063 | 12538 | 3055 | 22368 | 8433 | 6056 |
| Lee Men's Relaxed Fit Slightly Tapered Leg Jean | Lee | Jeans | 30.99 | 16.89 | 122.96 | 55.54 | 21 | 4 | 5 | 3 | 9 | 248.92 | 113.31 | 0.4517 | 0.5556 | 0.2222 | 0.1429 | 0.6923 | 4.55e-05 | 3.97e-05 | 0.0001158 | 17446 | 16178 | 6481 | 7447 | 50 | 776 | 5 | 526 | 140 | 2405 | 2891 | 17150 | 4274 | 17122 | 12706 | 12966 |
| Bottoms Out Men's Plaid Sleep Pant | Bottoms Out | Sleep & Lounge | 13.49 | 5.05 | 94.43 | 59.4 | 25 | 7 | 2 | 4 | 12 | 80.94 | 50.64 | 0.629 | 0.2222 | 0.3333 | 0.16 | 0.6316 | 3.5e-05 | 4.25e-05 | 0.0001379 | 25625 | 26913 | 8758 | 6904 | 21 | 33 | 844 | 126 | 37 | 9890 | 8299 | 839 | 12628 | 9747 | 12630 | 16546 |
| RSQ London Mens Skinny Jeans | RSQ | Jeans | 44.99 | 24.2 | 134.97 | 63.21 | 21 | 3 | 5 | 3 | 10 | 359.92 | 163.94 | 0.4683 | 0.625 | 0.1667 | 0.1429 | 0.7692 | 5e-05 | 4.52e-05 | 0.0001158 | 12553 | 11383 | 5908 | 6477 | 50 | 2358 | 5 | 526 | 77 | 1228 | 1608 | 15636 | 4099 | 19436 | 12706 | 9471 |
| Diesel Men's Blade Underpant | Diesel | Underwear | 22.14 | 9.75 | 122.0 | 66.53 | 22 | 6 | 0 | 2 | 14 | 43.0 | 23.83 | 0.5453 | 0.0 | 0.3 | 0.0909 | 0.7 | 4.52e-05 | 4.75e-05 | 0.0001214 | 21886 | 22702 | 6504 | 6114 | 43 | 84 | 13463 | 2100 | 22 | 15676 | 14732 | 8115 | 13463 | 13033 | 16872 | 12849 |
| Michael Kors Men's 3 Pack Brief | Michael Kors | Underwear | 25.99 | 12.48 | 130.46 | 67.73 | 24 | 5 | 5 | 4 | 10 | 232.38 | 120.98 | 0.5192 | 0.5 | 0.25 | 0.1667 | 0.6667 | 4.83e-05 | 4.84e-05 | 0.0001324 | 19456 | 20053 | 6070 | 5979 | 30 | 251 | 5 | 126 | 77 | 2705 | 2646 | 10469 | 4275 | 14408 | 10731 | 12990 |
| RUDE Dark Vintage Skinny Jeans | Hot Topic | Jeans | 36.5 | 19.33 | 146.0 | 68.99 | 24 | 4 | 4 | 3 | 13 | 255.5 | 123.41 | 0.4725 | 0.5 | 0.1905 | 0.125 | 0.7647 | 5.41e-05 | 4.93e-05 | 0.0001324 | 15396 | 14389 | 5357 | 5845 | 30 | 776 | 30 | 526 | 31 | 2306 | 2570 | 15319 | 4275 | 19353 | 14338 | 9484 |
| Bottoms Out Men's Plaid Sleep Jam | Bottoms Out | Sleep & Lounge | 25.0 | 9.3 | 125.0 | 78.03 | 24 | 5 | 2 | 2 | 15 | 100.0 | 63.2 | 0.6242 | 0.2857 | 0.2273 | 0.0833 | 0.75 | 4.63e-05 | 5.58e-05 | 0.0001324 | 19651 | 23078 | 6364 | 5026 | 30 | 251 | 844 | 2100 | 11 | 7972 | 6500 | 1088 | 11280 | 17121 | 17144 | 9487 |

</div>

**Bottom products by Profit Margin**

```sql
WITH first_layer AS (
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
WHERE revenue_rank <= 50
ORDER BY
  profit_margin_rank DESC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| The North Face Apex Bionic Soft Shell Jacket - Men's | The North Face | Fashion Hoodies & Sweatshirts | 903.0 | 524.64 | 1806.0 | 756.71 | 6 | 2 | 0 | 0 | 4 | 0.0 | 0.0 | 0.419 | 0.0 | 0.3333 | 0.0 | 0.6667 | 0.000669 | 0.0005408 | 3.31e-05 | 5 | 3 | 21 | 55 | 12532 | 6114 | 13463 | 17458 | 6105 | 22642 | 22642 | 19960 | 13463 | 9747 | 17458 | 12990 |
| PAIGE Women's Skyline Skinny Jean | PAIGE | Jeans | 158.0 | 90.19 | 1422.0 | 608.93 | 19 | 9 | 0 | 2 | 8 | 316.0 | 135.88 | 0.4282 | 0.0 | 0.5294 | 0.1053 | 0.4706 | 0.0005268 | 0.0004352 | 0.0001048 | 1714 | 1108 | 48 | 90 | 72 | 5 | 13463 | 2100 | 295 | 1575 | 2230 | 19172 | 13463 | 3268 | 16363 | 23444 |
| 7 For All Mankind Men's Austyn Relaxed Straight Jean | 7 For All Mankind | Jeans | 197.94 | 111.63 | 1399.0 | 608.64 | 17 | 7 | 0 | 1 | 9 | 189.0 | 83.35 | 0.4351 | 0.0 | 0.4375 | 0.0588 | 0.5625 | 0.0005182 | 0.000435 | 9.38e-05 | 942 | 526 | 50 | 91 | 103 | 33 | 13463 | 7029 | 140 | 3671 | 4605 | 18597 | 13463 | 6734 | 17433 | 19266 |
| Catherine Malandrino Women's Stretch Leather Pant | Catherine Malandrino | Leggings | 528.81 | 291.37 | 1586.43 | 712.31 | 5 | 3 | 1 | 0 | 1 | 528.81 | 237.44 | 0.449 | 0.25 | 0.6 | 0.0 | 0.25 | 0.0005877 | 0.0005091 | 2.76e-05 | 68 | 51 | 38 | 59 | 16887 | 2358 | 3978 | 17458 | 23197 | 584 | 835 | 17380 | 11344 | 2189 | 17458 | 26348 |
| True Religion Men's Ricky Straight Leg Jean | True Religion | Jeans | 227.86 | 123.14 | 1452.0 | 661.01 | 28 | 7 | 1 | 5 | 15 | 1430.0 | 645.85 | 0.4552 | 0.125 | 0.3043 | 0.1786 | 0.6818 | 0.0005379 | 0.0004724 | 0.0001545 | 646 | 406 | 45 | 69 | 9 | 33 | 3978 | 24 | 11 | 57 | 95 | 16801 | 13444 | 13032 | 10715 | 12986 |
| Diesel Men's Shioner Skinny Straight Leg Jean | Diesel | Jeans | 295.98 | 157.9 | 1695.85 | 779.71 | 25 | 6 | 2 | 3 | 14 | 1431.9 | 657.85 | 0.4598 | 0.25 | 0.2727 | 0.12 | 0.7 | 0.0006282 | 0.0005572 | 0.0001379 | 318 | 201 | 33 | 50 | 21 | 84 | 844 | 526 | 22 | 56 | 90 | 16428 | 11344 | 14284 | 15549 | 12849 |
| True Religion Women's Julie Super T Jean | True Religion | Jeans | 326.0 | 172.13 | 1956.0 | 923.23 | 8 | 6 | 0 | 1 | 1 | 326.0 | 153.87 | 0.472 | 0.0 | 0.8571 | 0.125 | 0.1429 | 0.0007246 | 0.0006598 | 4.41e-05 | 233 | 145 | 19 | 31 | 5507 | 84 | 13463 | 7029 | 23197 | 1487 | 1788 | 15335 | 13463 | 546 | 14338 | 27121 |
| Quiksilver Men's Rockefeller Walkshort | Quiksilver | Shorts | 903.0 | 472.27 | 1806.0 | 861.46 | 6 | 2 | 0 | 0 | 4 | 0.0 | 0.0 | 0.477 | 0.0 | 0.3333 | 0.0 | 0.6667 | 0.000669 | 0.0006157 | 3.31e-05 | 5 | 7 | 21 | 34 | 12532 | 6114 | 13463 | 17458 | 6105 | 22642 | 22642 | 14881 | 13463 | 9747 | 17458 | 12990 |
| 7 For All Mankind Men's Standard Classic Straight Leg Jean | 7 For All Mankind | Jeans | 157.45 | 80.97 | 1435.0 | 696.01 | 42 | 9 | 5 | 5 | 23 | 1673.0 | 844.04 | 0.485 | 0.3571 | 0.2432 | 0.119 | 0.7188 | 0.0005316 | 0.0004974 | 0.0002317 | 1798 | 1488 | 46 | 60 | 2 | 5 | 5 | 24 | 2 | 32 | 41 | 14028 | 8749 | 17091 | 15552 | 12034 |
| AIR JORDAN DOMINATE SHORTS MENS 465071-100 | Jordan | Shorts | 903.0 | 454.21 | 2709.0 | 1346.37 | 5 | 3 | 0 | 0 | 2 | 0.0 | 0.0 | 0.497 | 0.0 | 0.6 | 0.0 | 0.4 | 0.0010035 | 0.0009622 | 2.76e-05 | 5 | 8 | 7 | 9 | 16887 | 2358 | 13463 | 17458 | 17069 | 22642 | 22642 | 12874 | 13463 | 2189 | 17458 | 23875 |
| Canada Goose Women's Expedition Parka | Canada Goose | Outerwear & Coats | 795.0 | 395.91 | 2385.0 | 1197.27 | 4 | 3 | 0 | 1 | 0 | 795.0 | 399.09 | 0.502 | 0.0 | 1.0 | 0.25 | 0.0 | 0.0008835 | 0.0008557 | 2.21e-05 | 33 | 19 | 10 | 13 | 21053 | 2358 | 13463 | 7029 | 27145 | 230 | 277 | 12357 | 13463 | 1 | 5542 | 27145 |
| Arc'teryx Moray Jacket - Women's | Arc'teryx | Outerwear & Coats | 699.0 | 343.91 | 2097.0 | 1065.28 | 9 | 3 | 0 | 3 | 3 | 2097.0 | 1065.28 | 0.508 | 0.0 | 0.5 | 0.3333 | 0.5 | 0.0007768 | 0.0007613 | 4.96e-05 | 41 | 36 | 15 | 20 | 3355 | 2358 | 13463 | 526 | 10869 | 11 | 22 | 11720 | 13463 | 3269 | 2619 | 19501 |
| Barbour Sapper Jacket | Barbour | Outerwear & Coats | 429.0 | 210.21 | 2145.0 | 1093.95 | 10 | 5 | 1 | 1 | 3 | 858.0 | 437.58 | 0.51 | 0.1667 | 0.5556 | 0.1 | 0.375 | 0.0007946 | 0.0007818 | 5.52e-05 | 94 | 81 | 14 | 18 | 1962 | 251 | 3978 | 7029 | 10869 | 185 | 233 | 11510 | 13196 | 3151 | 16366 | 24717 |
| Women's Knee Length Overcoat in Pure Cashmere | Cashmere Boutique | Outerwear & Coats | 399.0 | 193.12 | 1596.0 | 814.76 | 9 | 4 | 0 | 0 | 5 | 0.0 | 0.0 | 0.5105 | 0.0 | 0.4444 | 0.0 | 0.5556 | 0.0005912 | 0.0005823 | 4.96e-05 | 115 | 100 | 35 | 40 | 3355 | 776 | 13463 | 17458 | 3026 | 22642 | 22642 | 11502 | 13463 | 6492 | 17458 | 19270 |
| Barbour Classic Beaufort Jacket / Beaufort Jacket | Barbour | Outerwear & Coats | 399.0 | 193.91 | 1596.0 | 820.34 | 10 | 4 | 0 | 1 | 5 | 399.0 | 205.09 | 0.514 | 0.0 | 0.4444 | 0.1 | 0.5556 | 0.0005912 | 0.0005863 | 5.52e-05 | 115 | 98 | 35 | 38 | 1962 | 776 | 13463 | 7029 | 3026 | 985 | 1084 | 11041 | 13463 | 6492 | 16366 | 19270 |

</div>

**Bottom products by Unit Orders**

```sql
WITH first_layer AS (
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
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ulla Popken Plus Size Sequined Swing Jacket | Ulla Popken | Blazers & Jackets | 169.0 | 62.7 | 0.0 | 0.0 | 1 | 0 | 0 | 1 | 0 | 169.0 | 106.3 |  |  |  | 1.0 |  | 0.0 | 0.0 | 5.5e-06 | 1446 | 2577 | 22532 | 22532 | 27983 | 22532 | 13463 | 7029 | 27145 | 4331 | 3178 | 22532 | 25326 | 28303 | 1 | 28172 |
| Carhartt Women's Wylie Flannel Hoodie | Carhartt | Fashion Hoodies & Sweatshirts | 59.95 | 27.76 | 59.95 | 32.19 | 1 | 1 | 0 | 0 | 0 | 0.0 | 0.0 | 0.5369 | 0.0 | 1.0 | 0.0 | 0.0 | 2.22e-05 | 2.3e-05 | 5.5e-06 | 8808 | 9607 | 12711 | 12060 | 27983 | 13264 | 13463 | 17458 | 27145 | 22642 | 22642 | 8960 | 13463 | 1 | 17458 | 27145 |
| Lucky Brand Mens 361 Vintage Straight Leg Jean | Lucky Brand | Jeans | 61.99 | 35.27 | 61.99 | 26.72 | 1 | 1 | 0 | 0 | 0 | 0.0 | 0.0 | 0.431 | 0.0 | 1.0 | 0.0 | 0.0 | 2.3e-05 | 1.91e-05 | 5.5e-06 | 8368 | 6768 | 12308 | 13690 | 27983 | 13264 | 13463 | 17458 | 27145 | 22642 | 22642 | 18935 | 13463 | 1 | 17458 | 27145 |
| Solid Series Silk Scarves | Wolfmark | Accessories | 18.0 | 7.56 | 0.0 | 0.0 | 1 | 0 | 0 | 0 | 1 | 0.0 | 0.0 |  |  | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 5.5e-06 | 23512 | 24629 | 22532 | 22532 | 27983 | 22532 | 13463 | 17458 | 23197 | 22642 | 22642 | 22532 | 25326 | 22532 | 17458 | 1 |
| Bottoms Out - Mens Microfleece Lounge Pant Burgundy 23439 | Bottoms Out | Sleep & Lounge | 13.75 | 5.71 | 0.0 | 0.0 | 1 | 0 | 0 | 0 | 1 | 0.0 | 0.0 |  |  | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 5.5e-06 | 25545 | 26326 | 22532 | 22532 | 27983 | 22532 | 13463 | 17458 | 23197 | 22642 | 22642 | 22532 | 25326 | 22532 | 17458 | 1 |
| Acid Wash Jean Dark Leggings | Yelete | Leggings | 15.99 | 9.35 | 0.0 | 0.0 | 1 | 0 | 1 | 0 | 0 | 15.99 | 6.64 |  | 1.0 | 0.0 | 0.0 |  | 0.0 | 0.0 | 5.5e-06 | 24393 | 23040 | 22532 | 22532 | 27983 | 22532 | 3978 | 17458 | 27145 | 21199 | 21673 | 22532 | 1 | 22532 | 17458 | 28172 |
| Corset-story WT-066 waist training corset | Corset-story | Intimates | 100.0 | 54.1 | 0.0 | 0.0 | 1 | 0 | 0 | 0 | 1 | 0.0 | 0.0 |  |  | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 5.5e-06 | 3867 | 3383 | 22532 | 22532 | 27983 | 22532 | 13463 | 17458 | 23197 | 22642 | 22642 | 22532 | 25326 | 22532 | 17458 | 1 |
| prAna Women's Diva Vest | prAna | Active | 119.0 | 51.53 | 0.0 | 0.0 | 1 | 0 | 0 | 0 | 1 | 0.0 | 0.0 |  |  | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 5.5e-06 | 3169 | 3649 | 22532 | 22532 | 27983 | 22532 | 13463 | 17458 | 23197 | 22642 | 22642 | 22532 | 25326 | 22532 | 17458 | 1 |
| adidas Women's Pursuit Pant | adidas | Active | 50.0 | 18.65 | 0.0 | 0.0 | 1 | 0 | 0 | 1 | 0 | 50.0 | 31.35 |  |  |  | 1.0 |  | 0.0 | 0.0 | 5.5e-06 | 10696 | 14839 | 22532 | 22532 | 27983 | 22532 | 13463 | 7029 | 27145 | 14018 | 12300 | 22532 | 25326 | 28303 | 1 | 28172 |
| Volcom Juniors Frochickie 2 1/2 Inch Plain Front Short | Volcom | Shorts | 39.5 | 21.17 | 0.0 | 0.0 | 1 | 0 | 0 | 0 | 1 | 0.0 | 0.0 |  |  | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 5.5e-06 | 14466 | 13153 | 22532 | 22532 | 27983 | 22532 | 13463 | 17458 | 23197 | 22642 | 22642 | 22532 | 25326 | 22532 | 17458 | 1 |
| Nautica Mens 3 Pack Performance Casual Crew Track Socks | Nautica | Socks | 14.4 | 8.12 | 0.0 | 0.0 | 1 | 0 | 0 | 0 | 1 | 0.0 | 0.0 |  |  | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 5.5e-06 | 25223 | 24070 | 22532 | 22532 | 27983 | 22532 | 13463 | 17458 | 23197 | 22642 | 22642 | 22532 | 25326 | 22532 | 17458 | 1 |
| TAUPE PALAZZO PANT SPLIT SKIRT GAUCHO - FITS (ONE SIZE) - L XL 1X 2X - U652S - LOTUSTRADERS | LOTUSTRADERS | Pants & Capris | 42.99 | 21.92 | 42.99 | 21.07 | 1 | 1 | 0 | 0 | 0 | 0.0 | 0.0 | 0.4901 | 0.0 | 1.0 | 0.0 | 0.0 | 1.59e-05 | 1.51e-05 | 5.5e-06 | 13180 | 12697 | 15536 | 15631 | 27983 | 13264 | 13463 | 17458 | 27145 | 22642 | 22642 | 13507 | 13463 | 1 | 17458 | 27145 |
| Arena Men's Satamis Race Xtra Life Lycra Solid Brief Swimsuit | Arena | Swim | 24.95 | 15.17 | 0.0 | 0.0 | 1 | 0 | 0 | 0 | 1 | 0.0 | 0.0 |  |  | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 5.5e-06 | 21005 | 17618 | 22532 | 22532 | 27983 | 22532 | 13463 | 17458 | 23197 | 22642 | 22642 | 22532 | 25326 | 22532 | 17458 | 1 |
| Le Suit Safari Nights Jacket Dress | Le Suit | Suits | 141.62 | 83.84 | 0.0 | 0.0 | 1 | 0 | 0 | 1 | 0 | 141.62 | 57.78 |  |  |  | 1.0 |  | 0.0 | 0.0 | 5.5e-06 | 2207 | 1356 | 22532 | 22532 | 27983 | 22532 | 13463 | 7029 | 27145 | 5534 | 7190 | 22532 | 25326 | 28303 | 1 | 28172 |
| Trina Turk Women's Pasha Pant | Trina Turk | Pants & Capris | 288.0 | 162.72 | 288.0 | 125.28 | 1 | 1 | 0 | 0 | 0 | 0.0 | 0.0 | 0.435 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0001067 | 8.95e-05 | 5.5e-06 | 338 | 178 | 1925 | 2574 | 27983 | 13264 | 13463 | 17458 | 27145 | 22642 | 22642 | 18613 | 13463 | 1 | 17458 | 27145 |

</div>

**Bottom products by Average Sale Price**

```sql
WITH first_layer AS (
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
WHERE unit_orders_placed_rank <= 50
ORDER BY
  avg_product_sale_price_rank DESC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HUGO BOSS Men's Bright Argyle Crew Sock | HUGO BOSS | Socks | 9.75 | 5.68 | 39.0 | 15.65 | 22 | 4 | 4 | 4 | 10 | 78.0 | 32.25 | 0.4013 | 0.5 | 0.2222 | 0.1818 | 0.7143 | 1.44e-05 | 1.12e-05 | 0.0001214 | 27342 | 26355 | 16327 | 17765 | 43 | 776 | 30 | 126 | 77 | 10368 | 12068 | 20837 | 4275 | 17122 | 10468 | 12035 |
| Puma Men's Socks | PUMA | Socks | 13.0 | 7.78 | 90.0 | 35.98 | 24 | 7 | 1 | 5 | 11 | 78.0 | 31.36 | 0.3998 | 0.125 | 0.3684 | 0.2083 | 0.6111 | 3.33e-05 | 2.57e-05 | 0.0001324 | 25705 | 24414 | 8929 | 11107 | 30 | 33 | 3978 | 24 | 43 | 10368 | 12295 | 20955 | 13444 | 9637 | 8433 | 16951 |
| HUGO BOSS Men's Striped Crew Sock | HUGO BOSS | Socks | 13.0 | 8.14 | 104.0 | 40.17 | 24 | 8 | 3 | 4 | 9 | 91.0 | 33.33 | 0.3863 | 0.2727 | 0.4 | 0.1667 | 0.5294 | 3.85e-05 | 2.87e-05 | 0.0001324 | 25705 | 24062 | 7764 | 10157 | 30 | 16 | 151 | 126 | 140 | 8958 | 11794 | 21483 | 11342 | 7482 | 10731 | 19498 |
| New Men's Sexy Center Patch Bikini Swimsuit 3G by Gregg Homme | Gregg Homme | Swim | 13.22 | 7.85 | 54.6 | 20.64 | 25 | 4 | 2 | 5 | 14 | 90.3 | 38.29 | 0.378 | 0.3333 | 0.2 | 0.2 | 0.7778 | 2.02e-05 | 1.48e-05 | 0.0001379 | 25672 | 24345 | 13422 | 15782 | 21 | 776 | 844 | 24 | 22 | 8973 | 10649 | 21721 | 8752 | 17510 | 8435 | 9281 |
| Bottoms Out Men's Plaid Sleep Pant | Bottoms Out | Sleep & Lounge | 13.49 | 5.05 | 94.43 | 59.4 | 25 | 7 | 2 | 4 | 12 | 80.94 | 50.64 | 0.629 | 0.2222 | 0.3333 | 0.16 | 0.6316 | 3.5e-05 | 4.25e-05 | 0.0001379 | 25625 | 26913 | 8758 | 6904 | 21 | 33 | 844 | 126 | 37 | 9890 | 8299 | 839 | 12628 | 9747 | 12630 | 16546 |
| Kenneth Cole REACTION Men's Passcase Wallet | Kenneth Cole REACTION | Accessories | 18.91 | 7.72 | 152.71 | 89.4 | 34 | 8 | 4 | 4 | 18 | 150.85 | 90.57 | 0.5854 | 0.3333 | 0.2667 | 0.1176 | 0.6923 | 5.66e-05 | 6.39e-05 | 0.0001876 | 23389 | 24481 | 4958 | 4188 | 4 | 16 | 30 | 126 | 4 | 5015 | 4078 | 3806 | 8752 | 14395 | 15553 | 12966 |
| Tommy Hilfiger Men Classic Fit T-shirt | Tommy Hilfiger | Tops & Tees | 21.99 | 12.22 | 65.97 | 28.41 | 25 | 3 | 2 | 5 | 15 | 153.93 | 70.63 | 0.4307 | 0.4 | 0.15 | 0.2 | 0.8333 | 2.44e-05 | 2.03e-05 | 0.0001379 | 22049 | 20333 | 11887 | 13165 | 21 | 2358 | 844 | 24 | 11 | 4954 | 5704 | 18998 | 8312 | 20814 | 8435 | 6580 |
| Diesel Men's Blade Underpant | Diesel | Underwear | 22.14 | 9.75 | 122.0 | 66.53 | 22 | 6 | 0 | 2 | 14 | 43.0 | 23.83 | 0.5453 | 0.0 | 0.3 | 0.0909 | 0.7 | 4.52e-05 | 4.75e-05 | 0.0001214 | 21886 | 22702 | 6504 | 6114 | 43 | 84 | 13463 | 2100 | 22 | 15676 | 14732 | 8115 | 13463 | 13033 | 16872 | 12849 |
| Motherhood Maternity: Sports Clip Down Nursing Bra | Motherhood Maternity | Maternity | 22.54 | 10.46 | 200.82 | 108.99 | 25 | 9 | 2 | 3 | 11 | 112.9 | 60.37 | 0.5427 | 0.1818 | 0.4091 | 0.12 | 0.55 | 7.44e-05 | 7.79e-05 | 0.0001379 | 21822 | 22052 | 3297 | 3165 | 21 | 5 | 844 | 526 | 43 | 7249 | 6811 | 8373 | 13193 | 7481 | 15549 | 19449 |
| Hanes Men's 4 Pack Boxer Brief | Hanes | Underwear | 25.0 | 11.52 | 250.0 | 133.47 | 28 | 10 | 2 | 5 | 11 | 175.0 | 92.77 | 0.5339 | 0.1667 | 0.4348 | 0.1786 | 0.5238 | 9.26e-05 | 9.54e-05 | 0.0001545 | 19651 | 20997 | 2432 | 2340 | 9 | 4 | 844 | 24 | 43 | 4152 | 3935 | 9232 | 13196 | 6738 | 10715 | 19500 |
| Bottoms Out Men's Plaid Sleep Jam | Bottoms Out | Sleep & Lounge | 25.0 | 9.3 | 125.0 | 78.03 | 24 | 5 | 2 | 2 | 15 | 100.0 | 63.2 | 0.6242 | 0.2857 | 0.2273 | 0.0833 | 0.75 | 4.63e-05 | 5.58e-05 | 0.0001324 | 19651 | 23078 | 6364 | 5026 | 30 | 251 | 844 | 2100 | 11 | 7972 | 6500 | 1088 | 11280 | 17121 | 17144 | 9487 |
| Michael Kors Men's 3 Pack Brief | Michael Kors | Underwear | 25.99 | 12.48 | 130.46 | 67.73 | 24 | 5 | 5 | 4 | 10 | 232.38 | 120.98 | 0.5192 | 0.5 | 0.25 | 0.1667 | 0.6667 | 4.83e-05 | 4.84e-05 | 0.0001324 | 19456 | 20053 | 6070 | 5979 | 30 | 251 | 5 | 126 | 77 | 2705 | 2646 | 10469 | 4275 | 14408 | 10731 | 12990 |
| State O Maine Big and Tall Solid Microfleece Lounge Pant | KNOTHE CORP. | Sleep & Lounge | 26.99 | 10.37 | 161.94 | 101.75 | 24 | 6 | 2 | 2 | 14 | 107.96 | 69.2 | 0.6283 | 0.25 | 0.2727 | 0.0833 | 0.7 | 6e-05 | 7.27e-05 | 0.0001324 | 19125 | 22140 | 4586 | 3491 | 30 | 84 | 844 | 2100 | 22 | 7621 | 5851 | 878 | 11344 | 14284 | 17144 | 12849 |
| Volcom Juniors Pocket Blocket Long Sleeve Tee | Volcom | Tops & Tees | 27.0 | 15.34 | 81.0 | 33.86 | 21 | 3 | 4 | 5 | 9 | 243.0 | 107.41 | 0.418 | 0.5714 | 0.1875 | 0.2381 | 0.75 | 3e-05 | 2.42e-05 | 0.0001158 | 19072 | 17500 | 9846 | 11622 | 50 | 2358 | 30 | 24 | 140 | 2456 | 3131 | 20016 | 4252 | 19354 | 7773 | 9487 |
| JiMarti JM01 Sunglasses for Golf Fishing Cycling-Unbreakable-... Frame | JiMarti | Accessories | 29.95 | 11.92 | 269.55 | 161.1 | 22 | 9 | 2 | 2 | 9 | 119.8 | 72.12 | 0.5977 | 0.1818 | 0.45 | 0.0909 | 0.5 | 9.99e-05 | 0.0001151 | 0.0001214 | 18166 | 20613 | 2175 | 1707 | 43 | 5 | 844 | 2100 | 140 | 6868 | 5540 | 2758 | 13193 | 6490 | 16872 | 19501 |

</div>

**Bottom products by Average Cost**

```sql
WITH first_layer AS (
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
WHERE unit_orders_placed_rank <= 50
ORDER BY
  avg_product_cost_rank DESC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bottoms Out Men's Plaid Sleep Pant | Bottoms Out | Sleep & Lounge | 13.49 | 5.05 | 94.43 | 59.4 | 25 | 7 | 2 | 4 | 12 | 80.94 | 50.64 | 0.629 | 0.2222 | 0.3333 | 0.16 | 0.6316 | 3.5e-05 | 4.25e-05 | 0.0001379 | 25625 | 26913 | 8758 | 6904 | 21 | 33 | 844 | 126 | 37 | 9890 | 8299 | 839 | 12628 | 9747 | 12630 | 16546 |
| HUGO BOSS Men's Bright Argyle Crew Sock | HUGO BOSS | Socks | 9.75 | 5.68 | 39.0 | 15.65 | 22 | 4 | 4 | 4 | 10 | 78.0 | 32.25 | 0.4013 | 0.5 | 0.2222 | 0.1818 | 0.7143 | 1.44e-05 | 1.12e-05 | 0.0001214 | 27342 | 26355 | 16327 | 17765 | 43 | 776 | 30 | 126 | 77 | 10368 | 12068 | 20837 | 4275 | 17122 | 10468 | 12035 |
| Kenneth Cole REACTION Men's Passcase Wallet | Kenneth Cole REACTION | Accessories | 18.91 | 7.72 | 152.71 | 89.4 | 34 | 8 | 4 | 4 | 18 | 150.85 | 90.57 | 0.5854 | 0.3333 | 0.2667 | 0.1176 | 0.6923 | 5.66e-05 | 6.39e-05 | 0.0001876 | 23389 | 24481 | 4958 | 4188 | 4 | 16 | 30 | 126 | 4 | 5015 | 4078 | 3806 | 8752 | 14395 | 15553 | 12966 |
| Puma Men's Socks | PUMA | Socks | 13.0 | 7.78 | 90.0 | 35.98 | 24 | 7 | 1 | 5 | 11 | 78.0 | 31.36 | 0.3998 | 0.125 | 0.3684 | 0.2083 | 0.6111 | 3.33e-05 | 2.57e-05 | 0.0001324 | 25705 | 24414 | 8929 | 11107 | 30 | 33 | 3978 | 24 | 43 | 10368 | 12295 | 20955 | 13444 | 9637 | 8433 | 16951 |
| New Men's Sexy Center Patch Bikini Swimsuit 3G by Gregg Homme | Gregg Homme | Swim | 13.22 | 7.85 | 54.6 | 20.64 | 25 | 4 | 2 | 5 | 14 | 90.3 | 38.29 | 0.378 | 0.3333 | 0.2 | 0.2 | 0.7778 | 2.02e-05 | 1.48e-05 | 0.0001379 | 25672 | 24345 | 13422 | 15782 | 21 | 776 | 844 | 24 | 22 | 8973 | 10649 | 21721 | 8752 | 17510 | 8435 | 9281 |
| HUGO BOSS Men's Striped Crew Sock | HUGO BOSS | Socks | 13.0 | 8.14 | 104.0 | 40.17 | 24 | 8 | 3 | 4 | 9 | 91.0 | 33.33 | 0.3863 | 0.2727 | 0.4 | 0.1667 | 0.5294 | 3.85e-05 | 2.87e-05 | 0.0001324 | 25705 | 24062 | 7764 | 10157 | 30 | 16 | 151 | 126 | 140 | 8958 | 11794 | 21483 | 11342 | 7482 | 10731 | 19498 |
| Bottoms Out Men's Plaid Sleep Jam | Bottoms Out | Sleep & Lounge | 25.0 | 9.3 | 125.0 | 78.03 | 24 | 5 | 2 | 2 | 15 | 100.0 | 63.2 | 0.6242 | 0.2857 | 0.2273 | 0.0833 | 0.75 | 4.63e-05 | 5.58e-05 | 0.0001324 | 19651 | 23078 | 6364 | 5026 | 30 | 251 | 844 | 2100 | 11 | 7972 | 6500 | 1088 | 11280 | 17121 | 17144 | 9487 |
| Diesel Men's Blade Underpant | Diesel | Underwear | 22.14 | 9.75 | 122.0 | 66.53 | 22 | 6 | 0 | 2 | 14 | 43.0 | 23.83 | 0.5453 | 0.0 | 0.3 | 0.0909 | 0.7 | 4.52e-05 | 4.75e-05 | 0.0001214 | 21886 | 22702 | 6504 | 6114 | 43 | 84 | 13463 | 2100 | 22 | 15676 | 14732 | 8115 | 13463 | 13033 | 16872 | 12849 |
| State O Maine Big and Tall Solid Microfleece Lounge Pant | KNOTHE CORP. | Sleep & Lounge | 26.99 | 10.37 | 161.94 | 101.75 | 24 | 6 | 2 | 2 | 14 | 107.96 | 69.2 | 0.6283 | 0.25 | 0.2727 | 0.0833 | 0.7 | 6e-05 | 7.27e-05 | 0.0001324 | 19125 | 22140 | 4586 | 3491 | 30 | 84 | 844 | 2100 | 22 | 7621 | 5851 | 878 | 11344 | 14284 | 17144 | 12849 |
| Motherhood Maternity: Sports Clip Down Nursing Bra | Motherhood Maternity | Maternity | 22.54 | 10.46 | 200.82 | 108.99 | 25 | 9 | 2 | 3 | 11 | 112.9 | 60.37 | 0.5427 | 0.1818 | 0.4091 | 0.12 | 0.55 | 7.44e-05 | 7.79e-05 | 0.0001379 | 21822 | 22052 | 3297 | 3165 | 21 | 5 | 844 | 526 | 43 | 7249 | 6811 | 8373 | 13193 | 7481 | 15549 | 19449 |
| Hanes Men's 4 Pack Boxer Brief | Hanes | Underwear | 25.0 | 11.52 | 250.0 | 133.47 | 28 | 10 | 2 | 5 | 11 | 175.0 | 92.77 | 0.5339 | 0.1667 | 0.4348 | 0.1786 | 0.5238 | 9.26e-05 | 9.54e-05 | 0.0001545 | 19651 | 20997 | 2432 | 2340 | 9 | 4 | 844 | 24 | 43 | 4152 | 3935 | 9232 | 13196 | 6738 | 10715 | 19500 |
| JiMarti JM01 Sunglasses for Golf Fishing Cycling-Unbreakable-... Frame | JiMarti | Accessories | 29.95 | 11.92 | 269.55 | 161.1 | 22 | 9 | 2 | 2 | 9 | 119.8 | 72.12 | 0.5977 | 0.1818 | 0.45 | 0.0909 | 0.5 | 9.99e-05 | 0.0001151 | 0.0001214 | 18166 | 20613 | 2175 | 1707 | 43 | 5 | 844 | 2100 | 140 | 6868 | 5540 | 2758 | 13193 | 6490 | 16872 | 19501 |
| Tommy Hilfiger Men Classic Fit T-shirt | Tommy Hilfiger | Tops & Tees | 21.99 | 12.22 | 65.97 | 28.41 | 25 | 3 | 2 | 5 | 15 | 153.93 | 70.63 | 0.4307 | 0.4 | 0.15 | 0.2 | 0.8333 | 2.44e-05 | 2.03e-05 | 0.0001379 | 22049 | 20333 | 11887 | 13165 | 21 | 2358 | 844 | 24 | 11 | 4954 | 5704 | 18998 | 8312 | 20814 | 8435 | 6580 |
| Michael Kors Men's 3 Pack Brief | Michael Kors | Underwear | 25.99 | 12.48 | 130.46 | 67.73 | 24 | 5 | 5 | 4 | 10 | 232.38 | 120.98 | 0.5192 | 0.5 | 0.25 | 0.1667 | 0.6667 | 4.83e-05 | 4.84e-05 | 0.0001324 | 19456 | 20053 | 6070 | 5979 | 30 | 251 | 5 | 126 | 77 | 2705 | 2646 | 10469 | 4275 | 14408 | 10731 | 12990 |
| Volcom Juniors Pocket Blocket Long Sleeve Tee | Volcom | Tops & Tees | 27.0 | 15.34 | 81.0 | 33.86 | 21 | 3 | 4 | 5 | 9 | 243.0 | 107.41 | 0.418 | 0.5714 | 0.1875 | 0.2381 | 0.75 | 3e-05 | 2.42e-05 | 0.0001158 | 19072 | 17500 | 9846 | 11622 | 50 | 2358 | 30 | 24 | 140 | 2456 | 3131 | 20016 | 4252 | 19354 | 7773 | 9487 |

</div>

**Bottom products by Completion Rate**

```sql
WITH first_layer AS (
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
WHERE unit_orders_placed_rank <= 50
ORDER BY
  completion_rate_rank DESC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kenneth Cole Men's Straight Leg Jean | Kenneth Cole | Jeans | 54.25 | 27.11 | 54.99 | 26.89 | 24 | 1 | 7 | 4 | 12 | 632.25 | 318.8 | 0.489 | 0.875 | 0.05 | 0.1667 | 0.9231 | 2.04e-05 | 1.92e-05 | 0.0001324 | 10100 | 9920 | 13356 | 13628 | 30 | 13264 | 1 | 126 | 37 | 380 | 462 | 13602 | 2795 | 22531 | 10731 | 5642 |
| Lilly Pulitzer Women's Callahan Short | Lilly Pulitzer | Shorts | 48.24 | 24.35 | 106.11 | 53.14 | 24 | 2 | 4 | 5 | 13 | 420.02 | 207.44 | 0.5008 | 0.6667 | 0.1053 | 0.2083 | 0.8667 | 3.93e-05 | 3.8e-05 | 0.0001324 | 11747 | 11307 | 7626 | 7813 | 30 | 6114 | 30 | 24 | 31 | 883 | 1063 | 12538 | 3055 | 22368 | 8433 | 6056 |
| Dockers Men's Suit Separate Coat | Dockers | Suits & Sport Coats | 88.36 | 33.97 | 231.12 | 140.98 | 27 | 3 | 4 | 2 | 18 | 542.11 | 337.6 | 0.61 | 0.5714 | 0.12 | 0.0741 | 0.8571 | 8.56e-05 | 0.0001008 | 0.0001489 | 5094 | 7229 | 2783 | 2122 | 12 | 2358 | 30 | 2100 | 4 | 542 | 391 | 1873 | 4252 | 22129 | 17370 | 6057 |
| Tommy Hilfiger Men Classic Fit T-shirt | Tommy Hilfiger | Tops & Tees | 21.99 | 12.22 | 65.97 | 28.41 | 25 | 3 | 2 | 5 | 15 | 153.93 | 70.63 | 0.4307 | 0.4 | 0.15 | 0.2 | 0.8333 | 2.44e-05 | 2.03e-05 | 0.0001379 | 22049 | 20333 | 11887 | 13165 | 21 | 2358 | 844 | 24 | 11 | 4954 | 5704 | 18998 | 8312 | 20814 | 8435 | 6580 |
| True Religion Men's Ricky Straight Jean | True Religion | Jeans | 246.88 | 129.05 | 1366.0 | 666.07 | 34 | 5 | 4 | 3 | 22 | 1400.0 | 654.5 | 0.4876 | 0.4444 | 0.1613 | 0.0882 | 0.8148 | 0.000506 | 0.000476 | 0.0001876 | 534 | 354 | 56 | 65 | 4 | 251 | 30 | 526 | 3 | 63 | 92 | 13792 | 8264 | 20804 | 17143 | 7595 |
| RSQ London Mens Skinny Jeans | RSQ | Jeans | 44.99 | 24.2 | 134.97 | 63.21 | 21 | 3 | 5 | 3 | 10 | 359.92 | 163.94 | 0.4683 | 0.625 | 0.1667 | 0.1429 | 0.7692 | 5e-05 | 4.52e-05 | 0.0001158 | 12553 | 11383 | 5908 | 6477 | 50 | 2358 | 5 | 526 | 77 | 1228 | 1608 | 15636 | 4099 | 19436 | 12706 | 9471 |
| Volcom Men's Kinkade Jean | Volcom | Jeans | 66.67 | 35.17 | 269.9 | 125.86 | 27 | 4 | 3 | 5 | 15 | 538.25 | 254.63 | 0.4663 | 0.4286 | 0.1818 | 0.1852 | 0.7895 | 0.0001 | 9e-05 | 0.0001489 | 7633 | 6807 | 2158 | 2560 | 12 | 776 | 151 | 24 | 11 | 562 | 723 | 15806 | 8270 | 19358 | 10467 | 9273 |
| Wrangler Men's 20X No. 33 Relaxed Straight Leg Jean | Wrangler | Jeans | 55.0 | 29.66 | 220.0 | 100.87 | 24 | 4 | 1 | 2 | 17 | 165.0 | 74.2 | 0.4585 | 0.2 | 0.1818 | 0.0833 | 0.8095 | 8.15e-05 | 7.21e-05 | 0.0001324 | 9673 | 8784 | 2941 | 3526 | 30 | 776 | 3978 | 2100 | 6 | 4449 | 5375 | 16533 | 12637 | 19358 | 17144 | 7597 |
| Volcom Juniors Pocket Blocket Long Sleeve Tee | Volcom | Tops & Tees | 27.0 | 15.34 | 81.0 | 33.86 | 21 | 3 | 4 | 5 | 9 | 243.0 | 107.41 | 0.418 | 0.5714 | 0.1875 | 0.2381 | 0.75 | 3e-05 | 2.42e-05 | 0.0001158 | 19072 | 17500 | 9846 | 11622 | 50 | 2358 | 30 | 24 | 140 | 2456 | 3131 | 20016 | 4252 | 19354 | 7773 | 9487 |
| RUDE Dark Vintage Skinny Jeans | Hot Topic | Jeans | 36.5 | 19.33 | 146.0 | 68.99 | 24 | 4 | 4 | 3 | 13 | 255.5 | 123.41 | 0.4725 | 0.5 | 0.1905 | 0.125 | 0.7647 | 5.41e-05 | 4.93e-05 | 0.0001324 | 15396 | 14389 | 5357 | 5845 | 30 | 776 | 30 | 526 | 31 | 2306 | 2570 | 15319 | 4275 | 19353 | 14338 | 9484 |
| New Men's Sexy Center Patch Bikini Swimsuit 3G by Gregg Homme | Gregg Homme | Swim | 13.22 | 7.85 | 54.6 | 20.64 | 25 | 4 | 2 | 5 | 14 | 90.3 | 38.29 | 0.378 | 0.3333 | 0.2 | 0.2 | 0.7778 | 2.02e-05 | 1.48e-05 | 0.0001379 | 25672 | 24345 | 13422 | 15782 | 21 | 776 | 844 | 24 | 22 | 8973 | 10649 | 21721 | 8752 | 17510 | 8435 | 9281 |
| Levi's Men's Wool Melton Peacoat | Levi's | Outerwear & Coats | 103.99 | 47.71 | 415.98 | 225.14 | 22 | 4 | 3 | 3 | 12 | 623.97 | 337.71 | 0.5412 | 0.4286 | 0.2105 | 0.1364 | 0.75 | 0.0001541 | 0.0001609 | 0.0001214 | 3776 | 4133 | 937 | 912 | 43 | 776 | 151 | 526 | 37 | 393 | 389 | 8481 | 8270 | 17508 | 14315 | 9487 |
| Nike Classic Fleece Hooded Top | Nike | Active | 40.62 | 16.88 | 161.76 | 98.38 | 21 | 4 | 2 | 2 | 13 | 162.86 | 91.16 | 0.6082 | 0.3333 | 0.2105 | 0.0952 | 0.7647 | 5.99e-05 | 7.03e-05 | 0.0001158 | 13704 | 16183 | 4588 | 3666 | 50 | 776 | 844 | 2100 | 31 | 4548 | 4039 | 1985 | 8752 | 17508 | 16870 | 9484 |
| Lee Men's Relaxed Fit Slightly Tapered Leg Jean | Lee | Jeans | 30.99 | 16.89 | 122.96 | 55.54 | 21 | 4 | 5 | 3 | 9 | 248.92 | 113.31 | 0.4517 | 0.5556 | 0.2222 | 0.1429 | 0.6923 | 4.55e-05 | 3.97e-05 | 0.0001158 | 17446 | 16178 | 6481 | 7447 | 50 | 776 | 5 | 526 | 140 | 2405 | 2891 | 17150 | 4274 | 17122 | 12706 | 12966 |
| HUGO BOSS Men's Bright Argyle Crew Sock | HUGO BOSS | Socks | 9.75 | 5.68 | 39.0 | 15.65 | 22 | 4 | 4 | 4 | 10 | 78.0 | 32.25 | 0.4013 | 0.5 | 0.2222 | 0.1818 | 0.7143 | 1.44e-05 | 1.12e-05 | 0.0001214 | 27342 | 26355 | 16327 | 17765 | 43 | 776 | 30 | 126 | 77 | 10368 | 12068 | 20837 | 4275 | 17122 | 10468 | 12035 |

</div>

**Bottom products by Return Rate**

```sql
WITH first_layer AS (
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
WHERE revenue_rank <= 20
ORDER BY
  return_rate_rank DESC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AIR JORDAN DOMINATE SHORTS MENS 465071-100 | Jordan | Shorts | 903.0 | 454.21 | 2709.0 | 1346.37 | 5 | 3 | 0 | 0 | 2 | 0.0 | 0.0 | 0.497 | 0.0 | 0.6 | 0.0 | 0.4 | 0.0010035 | 0.0009622 | 2.76e-05 | 5 | 8 | 7 | 9 | 16887 | 2358 | 13463 | 17458 | 17069 | 22642 | 22642 | 12874 | 13463 | 2189 | 17458 | 23875 |
| Canada Goose Women's Expedition Parka | Canada Goose | Outerwear & Coats | 795.0 | 395.91 | 2385.0 | 1197.27 | 4 | 3 | 0 | 1 | 0 | 795.0 | 399.09 | 0.502 | 0.0 | 1.0 | 0.25 | 0.0 | 0.0008835 | 0.0008557 | 2.21e-05 | 33 | 19 | 10 | 13 | 21053 | 2358 | 13463 | 7029 | 27145 | 230 | 277 | 12357 | 13463 | 1 | 5542 | 27145 |
| True Religion Women's Julie Super T Jean | True Religion | Jeans | 326.0 | 172.13 | 1956.0 | 923.23 | 8 | 6 | 0 | 1 | 1 | 326.0 | 153.87 | 0.472 | 0.0 | 0.8571 | 0.125 | 0.1429 | 0.0007246 | 0.0006598 | 4.41e-05 | 233 | 145 | 19 | 31 | 5507 | 84 | 13463 | 7029 | 23197 | 1487 | 1788 | 15335 | 13463 | 546 | 14338 | 27121 |
| Mountain Hardwear Women's Chillwave Down Jacket | Mountain Hardwear | Outerwear & Coats | 375.0 | 179.25 | 1875.0 | 978.75 | 6 | 5 | 0 | 1 | 0 | 375.0 | 195.75 | 0.522 | 0.0 | 1.0 | 0.1667 | 0.0 | 0.0006946 | 0.0006995 | 3.31e-05 | 155 | 128 | 20 | 29 | 12532 | 251 | 13463 | 7029 | 27145 | 1150 | 1161 | 10227 | 13463 | 1 | 10731 | 27145 |
| Canada Goose Women's Solaris | Canada Goose | Outerwear & Coats | 695.0 | 296.76 | 2085.0 | 1194.71 | 6 | 3 | 0 | 2 | 1 | 1390.0 | 796.47 | 0.573 | 0.0 | 0.75 | 0.3333 | 0.25 | 0.0007724 | 0.0008538 | 3.31e-05 | 46 | 48 | 17 | 14 | 12532 | 2358 | 13463 | 2100 | 23197 | 67 | 52 | 5041 | 13463 | 746 | 2619 | 26348 |
| ASCIS Cushion Low Socks (Pack of 3) | ASICS | Active | 903.0 | 373.84 | 3612.0 | 2116.63 | 11 | 4 | 0 | 1 | 6 | 903.0 | 529.16 | 0.586 | 0.0 | 0.4 | 0.0909 | 0.6 | 0.001338 | 0.0015127 | 6.07e-05 | 5 | 28 | 1 | 1 | 1161 | 776 | 13463 | 7029 | 1398 | 155 | 142 | 3719 | 13463 | 7482 | 16872 | 16953 |
| Arc'teryx Moray Jacket - Women's | Arc'teryx | Outerwear & Coats | 699.0 | 343.91 | 2097.0 | 1065.28 | 9 | 3 | 0 | 3 | 3 | 2097.0 | 1065.28 | 0.508 | 0.0 | 0.5 | 0.3333 | 0.5 | 0.0007768 | 0.0007613 | 4.96e-05 | 41 | 36 | 15 | 20 | 3355 | 2358 | 13463 | 526 | 10869 | 11 | 22 | 11720 | 13463 | 3269 | 2619 | 19501 |
| Men's Classic Sheepskin B-3 Bomber Jacket | Overland Sheepskin Co | Outerwear & Coats | 595.0 | 270.73 | 2380.0 | 1297.1 | 13 | 4 | 0 | 2 | 7 | 1190.0 | 648.55 | 0.545 | 0.0 | 0.3636 | 0.1538 | 0.6364 | 0.0008816 | 0.000927 | 7.17e-05 | 60 | 55 | 12 | 11 | 423 | 776 | 13463 | 2100 | 623 | 95 | 94 | 8121 | 13463 | 9638 | 12634 | 16487 |
| Michael Kors Men's Marlow Wool-Blend Single-Breasted Fitted Top Coat | Michael Kors | Outerwear & Coats | 255.0 | 102.26 | 2295.0 | 1374.7 | 15 | 9 | 1 | 2 | 3 | 765.0 | 458.23 | 0.599 | 0.1 | 0.6923 | 0.1333 | 0.25 | 0.0008502 | 0.0009825 | 8.27e-05 | 469 | 728 | 13 | 8 | 187 | 5 | 3978 | 2100 | 10869 | 252 | 208 | 2612 | 13461 | 1184 | 14317 | 26348 |
| Joseph Abboud Men's Two-button Side Vent Sport Coat | Joseph Abboud | Suits & Sport Coats | 264.0 | 101.9 | 2904.0 | 1759.82 | 30 | 11 | 2 | 2 | 15 | 1056.0 | 656.57 | 0.606 | 0.1538 | 0.3929 | 0.0667 | 0.5769 | 0.0010758 | 0.0012577 | 0.0001655 | 430 | 734 | 6 | 5 | 7 | 3 | 844 | 2100 | 11 | 112 | 91 | 2144 | 13388 | 9081 | 17408 | 18610 |
| Barbour Sapper Jacket | Barbour | Outerwear & Coats | 429.0 | 210.21 | 2145.0 | 1093.95 | 10 | 5 | 1 | 1 | 3 | 858.0 | 437.58 | 0.51 | 0.1667 | 0.5556 | 0.1 | 0.375 | 0.0007946 | 0.0007818 | 5.52e-05 | 94 | 81 | 14 | 18 | 1962 | 251 | 3978 | 7029 | 10869 | 185 | 233 | 11510 | 13196 | 3151 | 16366 | 24717 |
| Diesel Men's Lagnum Leather Jacket | Diesel | Outerwear & Coats | 598.0 | 267.9 | 2392.0 | 1320.38 | 7 | 4 | 1 | 1 | 1 | 1196.0 | 660.19 | 0.552 | 0.2 | 0.6667 | 0.1429 | 0.2 | 0.0008861 | 0.0009437 | 3.86e-05 | 57 | 56 | 9 | 10 | 8625 | 776 | 3978 | 7029 | 23197 | 92 | 89 | 7373 | 12637 | 1185 | 12706 | 26859 |
| The North Face Women's S-XL Oso Jacket | The North Face | Outerwear & Coats | 903.0 | 378.36 | 3612.0 | 2098.57 | 10 | 4 | 1 | 1 | 4 | 1806.0 | 1049.29 | 0.581 | 0.2 | 0.4444 | 0.1 | 0.5 | 0.001338 | 0.0014998 | 5.52e-05 | 5 | 25 | 1 | 2 | 1962 | 776 | 3978 | 7029 | 6105 | 22 | 24 | 4209 | 12637 | 6492 | 16366 | 19501 |
| Bergama Natural Raccoon Hooded Stroller - - Multicolor | Bergama | Outerwear & Coats | 749.99 | 306.75 | 2999.96 | 1772.98 | 10 | 4 | 1 | 0 | 5 | 749.99 | 443.24 | 0.591 | 0.2 | 0.4 | 0.0 | 0.5556 | 0.0011113 | 0.0012671 | 5.52e-05 | 40 | 43 | 4 | 3 | 1962 | 776 | 3978 | 17458 | 3026 | 267 | 224 | 3279 | 12637 | 7482 | 17458 | 19270 |
| Diesel Men's Jimeneo Jacket | Diesel | Suits & Sport Coats | 698.0 | 304.33 | 2094.0 | 1181.02 | 13 | 3 | 1 | 1 | 8 | 1396.0 | 787.34 | 0.564 | 0.25 | 0.25 | 0.0769 | 0.7273 | 0.0007757 | 0.0008441 | 7.17e-05 | 43 | 46 | 16 | 16 | 423 | 2358 | 3978 | 7029 | 295 | 65 | 54 | 6066 | 11344 | 14408 | 17286 | 11980 |

</div>

**Bottom products by Cancellation Rate**

```sql
WITH first_layer AS (
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
WHERE unit_orders_placed_rank <= 25
ORDER BY
  cancellation_rate_rank DESC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Chaps Big and Tall Solid V-Neck Vest | Chaps | Sweaters | 39.88 | 20.32 | 279.16 | 134.91 | 28 | 7 | 4 | 1 | 16 | 199.4 | 99.06 | 0.4833 | 0.3636 | 0.2593 | 0.0357 | 0.6957 | 0.0001034 | 9.64e-05 | 0.0001545 | 14437 | 13747 | 2029 | 2288 | 9 | 33 | 30 | 7029 | 7 | 3354 | 3543 | 14237 | 8748 | 14407 | 17457 | 12964 |
| Joseph Abboud Men's Two-button Side Vent Sport Coat | Joseph Abboud | Suits & Sport Coats | 264.0 | 101.9 | 2904.0 | 1759.82 | 30 | 11 | 2 | 2 | 15 | 1056.0 | 656.57 | 0.606 | 0.1538 | 0.3929 | 0.0667 | 0.5769 | 0.0010758 | 0.0012577 | 0.0001655 | 430 | 734 | 6 | 5 | 7 | 3 | 844 | 2100 | 11 | 112 | 91 | 2144 | 13388 | 9081 | 17408 | 18610 |
| Joe's Jeans Men's Slim Fit Straight Leg Brixton | Joe's Jeans | Jeans | 194.26 | 102.07 | 1353.0 | 647.44 | 27 | 7 | 3 | 2 | 15 | 976.0 | 458.49 | 0.4785 | 0.3 | 0.28 | 0.0741 | 0.6818 | 0.0005012 | 0.0004627 | 0.0001489 | 992 | 729 | 58 | 76 | 12 | 33 | 151 | 2100 | 11 | 133 | 207 | 14773 | 11276 | 14282 | 17370 | 12986 |
| Dockers Men's Suit Separate Coat | Dockers | Suits & Sport Coats | 88.36 | 33.97 | 231.12 | 140.98 | 27 | 3 | 4 | 2 | 18 | 542.11 | 337.6 | 0.61 | 0.5714 | 0.12 | 0.0741 | 0.8571 | 8.56e-05 | 0.0001008 | 0.0001489 | 5094 | 7229 | 2783 | 2122 | 12 | 2358 | 30 | 2100 | 4 | 542 | 391 | 1873 | 4252 | 22129 | 17370 | 6057 |
| UltraClub Adult Sherpa-Lined Full-Zip Fleece with Hood | UltraClub | Fashion Hoodies & Sweatshirts | 51.47 | 28.47 | 360.9 | 161.23 | 26 | 7 | 2 | 2 | 15 | 203.71 | 91.12 | 0.4467 | 0.2222 | 0.2917 | 0.0769 | 0.6818 | 0.0001337 | 0.0001152 | 0.0001434 | 10603 | 9302 | 1222 | 1705 | 17 | 33 | 844 | 2100 | 11 | 3228 | 4041 | 17630 | 12628 | 13236 | 17286 | 12986 |
| Lucky Brand Mens Men's 361 Vintage Straight Denim Jean | Lucky Brand | Jeans | 99.0 | 52.65 | 594.0 | 275.91 | 25 | 6 | 3 | 2 | 14 | 495.0 | 228.59 | 0.4645 | 0.3333 | 0.2609 | 0.08 | 0.7 | 0.00022 | 0.0001972 | 0.0001379 | 4113 | 3525 | 427 | 608 | 21 | 84 | 151 | 2100 | 22 | 674 | 896 | 15993 | 8752 | 14406 | 17285 | 12849 |
| True Religion Men's Ricky Straight Jean | True Religion | Jeans | 246.88 | 129.05 | 1366.0 | 666.07 | 34 | 5 | 4 | 3 | 22 | 1400.0 | 654.5 | 0.4876 | 0.4444 | 0.1613 | 0.0882 | 0.8148 | 0.000506 | 0.000476 | 0.0001876 | 534 | 354 | 56 | 65 | 4 | 251 | 30 | 526 | 3 | 63 | 92 | 13792 | 8264 | 20804 | 17143 | 7595 |
| HUGO BOSS Men's Long Pant | HUGO BOSS | Sleep & Lounge | 74.72 | 28.3 | 1033.11 | 648.16 | 33 | 14 | 0 | 3 | 16 | 233.01 | 138.21 | 0.6274 | 0.0 | 0.4667 | 0.0909 | 0.5333 | 0.0003827 | 0.0004632 | 0.000182 | 6501 | 9383 | 113 | 75 | 6 | 1 | 13463 | 526 | 7 | 2702 | 2165 | 933 | 13463 | 6418 | 16872 | 19494 |
| Wrangler Men's Wrancher Dress Jean | Wrangler | Jeans | 40.4 | 20.2 | 242.4 | 118.65 | 27 | 6 | 2 | 3 | 16 | 202.0 | 102.05 | 0.4895 | 0.25 | 0.25 | 0.1111 | 0.7273 | 8.98e-05 | 8.48e-05 | 0.0001489 | 13728 | 13816 | 2533 | 2788 | 12 | 84 | 844 | 526 | 7 | 3236 | 3382 | 13585 | 11344 | 14408 | 15570 | 11980 |
| Joe's Jeans Men's Rebel Relaxed Fit Jean | Joe's Jeans | Jeans | 139.29 | 76.13 | 1296.69 | 583.03 | 26 | 9 | 0 | 3 | 14 | 339.69 | 166.11 | 0.4496 | 0.0 | 0.3913 | 0.1154 | 0.6087 | 0.0004803 | 0.0004167 | 0.0001434 | 2334 | 1721 | 68 | 102 | 17 | 5 | 13463 | 526 | 22 | 1403 | 1558 | 17357 | 13463 | 9082 | 15567 | 16952 |
| RVCA Men's Heavy Chev Denim Pant | RVCA | Jeans | 77.05 | 43.62 | 599.7 | 260.01 | 26 | 8 | 2 | 3 | 13 | 395.9 | 171.93 | 0.4336 | 0.2 | 0.3478 | 0.1154 | 0.619 | 0.0002222 | 0.0001858 | 0.0001434 | 6221 | 4800 | 406 | 687 | 17 | 16 | 844 | 526 | 31 | 1032 | 1457 | 18759 | 12637 | 9743 | 15567 | 16938 |
| Wrangler Men's 20x Collection Jean | Wrangler | Jeans | 55.0 | 29.7 | 440.0 | 202.51 | 26 | 8 | 2 | 3 | 13 | 275.0 | 133.27 | 0.4602 | 0.2 | 0.3478 | 0.1154 | 0.619 | 0.000163 | 0.0001447 | 0.0001434 | 9673 | 8763 | 847 | 1122 | 17 | 16 | 844 | 526 | 31 | 2032 | 2300 | 16343 | 12637 | 9743 | 15567 | 16938 |
| Kenneth Cole REACTION Men's Passcase Wallet | Kenneth Cole REACTION | Accessories | 18.91 | 7.72 | 152.71 | 89.4 | 34 | 8 | 4 | 4 | 18 | 150.85 | 90.57 | 0.5854 | 0.3333 | 0.2667 | 0.1176 | 0.6923 | 5.66e-05 | 6.39e-05 | 0.0001876 | 23389 | 24481 | 4958 | 4188 | 4 | 16 | 30 | 126 | 4 | 5015 | 4078 | 3806 | 8752 | 14395 | 15553 | 12966 |
| 7 For All Mankind Men's Standard Classic Straight Leg Jean | 7 For All Mankind | Jeans | 157.45 | 80.97 | 1435.0 | 696.01 | 42 | 9 | 5 | 5 | 23 | 1673.0 | 844.04 | 0.485 | 0.3571 | 0.2432 | 0.119 | 0.7188 | 0.0005316 | 0.0004974 | 0.0002317 | 1798 | 1488 | 46 | 60 | 2 | 5 | 5 | 24 | 2 | 32 | 41 | 14028 | 8749 | 17091 | 15552 | 12034 |
| Wrangler Men's Sarasota Agility Short | Wrangler | Shorts | 33.03 | 16.36 | 198.95 | 101.37 | 25 | 6 | 1 | 3 | 15 | 138.97 | 68.68 | 0.5095 | 0.1429 | 0.2727 | 0.12 | 0.7143 | 7.37e-05 | 7.24e-05 | 0.0001379 | 16765 | 16618 | 3447 | 3505 | 21 | 84 | 3978 | 526 | 11 | 5758 | 5901 | 11606 | 13389 | 14284 | 15549 | 12035 |

</div>

**Bottom products by En Route Rate**

```sql
WITH first_layer AS (
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
WHERE unit_orders_placed_rank <= 25
ORDER BY
  en_route_rate_rank DESC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Hanes Men's 4 Pack Boxer Brief | Hanes | Underwear | 25.0 | 11.52 | 250.0 | 133.47 | 28 | 10 | 2 | 5 | 11 | 175.0 | 92.77 | 0.5339 | 0.1667 | 0.4348 | 0.1786 | 0.5238 | 9.26e-05 | 9.54e-05 | 0.0001545 | 19651 | 20997 | 2432 | 2340 | 9 | 4 | 844 | 24 | 43 | 4152 | 3935 | 9232 | 13196 | 6738 | 10715 | 19500 |
| HUGO BOSS Men's Long Pant | HUGO BOSS | Sleep & Lounge | 74.72 | 28.3 | 1033.11 | 648.16 | 33 | 14 | 0 | 3 | 16 | 233.01 | 138.21 | 0.6274 | 0.0 | 0.4667 | 0.0909 | 0.5333 | 0.0003827 | 0.0004632 | 0.000182 | 6501 | 9383 | 113 | 75 | 6 | 1 | 13463 | 526 | 7 | 2702 | 2165 | 933 | 13463 | 6418 | 16872 | 19494 |
| Motherhood Maternity: Sports Clip Down Nursing Bra | Motherhood Maternity | Maternity | 22.54 | 10.46 | 200.82 | 108.99 | 25 | 9 | 2 | 3 | 11 | 112.9 | 60.37 | 0.5427 | 0.1818 | 0.4091 | 0.12 | 0.55 | 7.44e-05 | 7.79e-05 | 0.0001379 | 21822 | 22052 | 3297 | 3165 | 21 | 5 | 844 | 526 | 43 | 7249 | 6811 | 8373 | 13193 | 7481 | 15549 | 19449 |
| Joseph Abboud Men's Two-button Side Vent Sport Coat | Joseph Abboud | Suits & Sport Coats | 264.0 | 101.9 | 2904.0 | 1759.82 | 30 | 11 | 2 | 2 | 15 | 1056.0 | 656.57 | 0.606 | 0.1538 | 0.3929 | 0.0667 | 0.5769 | 0.0010758 | 0.0012577 | 0.0001655 | 430 | 734 | 6 | 5 | 7 | 3 | 844 | 2100 | 11 | 112 | 91 | 2144 | 13388 | 9081 | 17408 | 18610 |
| Joe's Jeans Men's Rebel Relaxed Fit Jean | Joe's Jeans | Jeans | 139.29 | 76.13 | 1296.69 | 583.03 | 26 | 9 | 0 | 3 | 14 | 339.69 | 166.11 | 0.4496 | 0.0 | 0.3913 | 0.1154 | 0.6087 | 0.0004803 | 0.0004167 | 0.0001434 | 2334 | 1721 | 68 | 102 | 17 | 5 | 13463 | 526 | 22 | 1403 | 1558 | 17357 | 13463 | 9082 | 15567 | 16952 |
| Wrangler Men's Original Cowboy Cut Relaxed Fit Jean | Wrangler | Jeans | 42.99 | 22.67 | 228.46 | 108.63 | 25 | 5 | 5 | 7 | 8 | 493.18 | 228.73 | 0.4755 | 0.5 | 0.2778 | 0.28 | 0.6154 | 8.46e-05 | 7.76e-05 | 0.0001379 | 13180 | 12269 | 2826 | 3184 | 21 | 251 | 5 | 2 | 295 | 687 | 895 | 15040 | 4275 | 14283 | 5404 | 16940 |
| RVCA Men's Heavy Chev Denim Pant | RVCA | Jeans | 77.05 | 43.62 | 599.7 | 260.01 | 26 | 8 | 2 | 3 | 13 | 395.9 | 171.93 | 0.4336 | 0.2 | 0.3478 | 0.1154 | 0.619 | 0.0002222 | 0.0001858 | 0.0001434 | 6221 | 4800 | 406 | 687 | 17 | 16 | 844 | 526 | 31 | 1032 | 1457 | 18759 | 12637 | 9743 | 15567 | 16938 |
| Wrangler Men's 20x Collection Jean | Wrangler | Jeans | 55.0 | 29.7 | 440.0 | 202.51 | 26 | 8 | 2 | 3 | 13 | 275.0 | 133.27 | 0.4602 | 0.2 | 0.3478 | 0.1154 | 0.619 | 0.000163 | 0.0001447 | 0.0001434 | 9673 | 8763 | 847 | 1122 | 17 | 16 | 844 | 526 | 31 | 2032 | 2300 | 16343 | 12637 | 9743 | 15567 | 16938 |
| Wrangler Men's Rugged Wear Classic Fit Jean | Wrangler | Jeans | 40.87 | 22.23 | 367.56 | 169.24 | 38 | 9 | 5 | 9 | 15 | 596.43 | 273.96 | 0.4604 | 0.3571 | 0.3103 | 0.2368 | 0.625 | 0.0001362 | 0.000121 | 0.0002096 | 13688 | 12514 | 1205 | 1552 | 3 | 5 | 5 | 1 | 11 | 440 | 628 | 16340 | 8749 | 13014 | 7776 | 16547 |
| Bottoms Out Men's Plaid Sleep Pant | Bottoms Out | Sleep & Lounge | 13.49 | 5.05 | 94.43 | 59.4 | 25 | 7 | 2 | 4 | 12 | 80.94 | 50.64 | 0.629 | 0.2222 | 0.3333 | 0.16 | 0.6316 | 3.5e-05 | 4.25e-05 | 0.0001379 | 25625 | 26913 | 8758 | 6904 | 21 | 33 | 844 | 126 | 37 | 9890 | 8299 | 839 | 12628 | 9747 | 12630 | 16546 |
| Volcom Men's Vorta Slim Straight Leg Fit Jean | Volcom | Jeans | 73.57 | 41.13 | 574.85 | 249.86 | 27 | 8 | 1 | 4 | 14 | 387.8 | 166.89 | 0.4347 | 0.1111 | 0.3478 | 0.1481 | 0.6364 | 0.0002129 | 0.0001786 | 0.0001489 | 6603 | 5251 | 467 | 746 | 12 | 16 | 3978 | 126 | 22 | 1091 | 1537 | 18678 | 13456 | 9743 | 12705 | 16487 |
| UltraClub Adult Sherpa-Lined Full-Zip Fleece with Hood | UltraClub | Fashion Hoodies & Sweatshirts | 51.47 | 28.47 | 360.9 | 161.23 | 26 | 7 | 2 | 2 | 15 | 203.71 | 91.12 | 0.4467 | 0.2222 | 0.2917 | 0.0769 | 0.6818 | 0.0001337 | 0.0001152 | 0.0001434 | 10603 | 9302 | 1222 | 1705 | 17 | 33 | 844 | 2100 | 11 | 3228 | 4041 | 17630 | 12628 | 13236 | 17286 | 12986 |
| True Religion Men's Ricky Straight Leg Jean | True Religion | Jeans | 227.86 | 123.14 | 1452.0 | 661.01 | 28 | 7 | 1 | 5 | 15 | 1430.0 | 645.85 | 0.4552 | 0.125 | 0.3043 | 0.1786 | 0.6818 | 0.0005379 | 0.0004724 | 0.0001545 | 646 | 406 | 45 | 69 | 9 | 33 | 3978 | 24 | 11 | 57 | 95 | 16801 | 13444 | 13032 | 10715 | 12986 |
| Joe's Jeans Men's Slim Fit Straight Leg Brixton | Joe's Jeans | Jeans | 194.26 | 102.07 | 1353.0 | 647.44 | 27 | 7 | 3 | 2 | 15 | 976.0 | 458.49 | 0.4785 | 0.3 | 0.28 | 0.0741 | 0.6818 | 0.0005012 | 0.0004627 | 0.0001489 | 992 | 729 | 58 | 76 | 12 | 33 | 151 | 2100 | 11 | 133 | 207 | 14773 | 11276 | 14282 | 17370 | 12986 |
| Kenneth Cole REACTION Men's Passcase Wallet | Kenneth Cole REACTION | Accessories | 18.91 | 7.72 | 152.71 | 89.4 | 34 | 8 | 4 | 4 | 18 | 150.85 | 90.57 | 0.5854 | 0.3333 | 0.2667 | 0.1176 | 0.6923 | 5.66e-05 | 6.39e-05 | 0.0001876 | 23389 | 24481 | 4958 | 4188 | 4 | 16 | 30 | 126 | 4 | 5015 | 4078 | 3806 | 8752 | 14395 | 15553 | 12966 |

</div>

**Bottom products by Units Completed**

```sql
WITH first_layer AS (
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
WHERE unit_orders_placed_rank <= 50
ORDER BY
  units_completed_rank DESC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kenneth Cole Men's Straight Leg Jean | Kenneth Cole | Jeans | 54.25 | 27.11 | 54.99 | 26.89 | 24 | 1 | 7 | 4 | 12 | 632.25 | 318.8 | 0.489 | 0.875 | 0.05 | 0.1667 | 0.9231 | 2.04e-05 | 1.92e-05 | 0.0001324 | 10100 | 9920 | 13356 | 13628 | 30 | 13264 | 1 | 126 | 37 | 380 | 462 | 13602 | 2795 | 22531 | 10731 | 5642 |
| Lilly Pulitzer Women's Callahan Short | Lilly Pulitzer | Shorts | 48.24 | 24.35 | 106.11 | 53.14 | 24 | 2 | 4 | 5 | 13 | 420.02 | 207.44 | 0.5008 | 0.6667 | 0.1053 | 0.2083 | 0.8667 | 3.93e-05 | 3.8e-05 | 0.0001324 | 11747 | 11307 | 7626 | 7813 | 30 | 6114 | 30 | 24 | 31 | 883 | 1063 | 12538 | 3055 | 22368 | 8433 | 6056 |
| Volcom Juniors Pocket Blocket Long Sleeve Tee | Volcom | Tops & Tees | 27.0 | 15.34 | 81.0 | 33.86 | 21 | 3 | 4 | 5 | 9 | 243.0 | 107.41 | 0.418 | 0.5714 | 0.1875 | 0.2381 | 0.75 | 3e-05 | 2.42e-05 | 0.0001158 | 19072 | 17500 | 9846 | 11622 | 50 | 2358 | 30 | 24 | 140 | 2456 | 3131 | 20016 | 4252 | 19354 | 7773 | 9487 |
| Tommy Hilfiger Men Classic Fit T-shirt | Tommy Hilfiger | Tops & Tees | 21.99 | 12.22 | 65.97 | 28.41 | 25 | 3 | 2 | 5 | 15 | 153.93 | 70.63 | 0.4307 | 0.4 | 0.15 | 0.2 | 0.8333 | 2.44e-05 | 2.03e-05 | 0.0001379 | 22049 | 20333 | 11887 | 13165 | 21 | 2358 | 844 | 24 | 11 | 4954 | 5704 | 18998 | 8312 | 20814 | 8435 | 6580 |
| RSQ London Mens Skinny Jeans | RSQ | Jeans | 44.99 | 24.2 | 134.97 | 63.21 | 21 | 3 | 5 | 3 | 10 | 359.92 | 163.94 | 0.4683 | 0.625 | 0.1667 | 0.1429 | 0.7692 | 5e-05 | 4.52e-05 | 0.0001158 | 12553 | 11383 | 5908 | 6477 | 50 | 2358 | 5 | 526 | 77 | 1228 | 1608 | 15636 | 4099 | 19436 | 12706 | 9471 |
| Dockers Men's Suit Separate Coat | Dockers | Suits & Sport Coats | 88.36 | 33.97 | 231.12 | 140.98 | 27 | 3 | 4 | 2 | 18 | 542.11 | 337.6 | 0.61 | 0.5714 | 0.12 | 0.0741 | 0.8571 | 8.56e-05 | 0.0001008 | 0.0001489 | 5094 | 7229 | 2783 | 2122 | 12 | 2358 | 30 | 2100 | 4 | 542 | 391 | 1873 | 4252 | 22129 | 17370 | 6057 |
| Lee Men's Relaxed Fit Slightly Tapered Leg Jean | Lee | Jeans | 30.99 | 16.89 | 122.96 | 55.54 | 21 | 4 | 5 | 3 | 9 | 248.92 | 113.31 | 0.4517 | 0.5556 | 0.2222 | 0.1429 | 0.6923 | 4.55e-05 | 3.97e-05 | 0.0001158 | 17446 | 16178 | 6481 | 7447 | 50 | 776 | 5 | 526 | 140 | 2405 | 2891 | 17150 | 4274 | 17122 | 12706 | 12966 |
| HUGO BOSS Men's Bright Argyle Crew Sock | HUGO BOSS | Socks | 9.75 | 5.68 | 39.0 | 15.65 | 22 | 4 | 4 | 4 | 10 | 78.0 | 32.25 | 0.4013 | 0.5 | 0.2222 | 0.1818 | 0.7143 | 1.44e-05 | 1.12e-05 | 0.0001214 | 27342 | 26355 | 16327 | 17765 | 43 | 776 | 30 | 126 | 77 | 10368 | 12068 | 20837 | 4275 | 17122 | 10468 | 12035 |
| RUDE Dark Vintage Skinny Jeans | Hot Topic | Jeans | 36.5 | 19.33 | 146.0 | 68.99 | 24 | 4 | 4 | 3 | 13 | 255.5 | 123.41 | 0.4725 | 0.5 | 0.1905 | 0.125 | 0.7647 | 5.41e-05 | 4.93e-05 | 0.0001324 | 15396 | 14389 | 5357 | 5845 | 30 | 776 | 30 | 526 | 31 | 2306 | 2570 | 15319 | 4275 | 19353 | 14338 | 9484 |
| 7 For All Mankind Men's The Straight Modern Jean | 7 For All Mankind | Jeans | 175.57 | 89.48 | 575.0 | 267.13 | 21 | 4 | 3 | 5 | 9 | 1447.0 | 714.47 | 0.4646 | 0.4286 | 0.25 | 0.2381 | 0.6923 | 0.000213 | 0.0001909 | 0.0001158 | 1310 | 1144 | 466 | 647 | 50 | 776 | 151 | 24 | 140 | 54 | 70 | 15992 | 8270 | 14408 | 7773 | 12966 |
| Wrangler Men's 20X No. 33 Relaxed Straight Leg Jean | Wrangler | Jeans | 55.0 | 29.66 | 220.0 | 100.87 | 24 | 4 | 1 | 2 | 17 | 165.0 | 74.2 | 0.4585 | 0.2 | 0.1818 | 0.0833 | 0.8095 | 8.15e-05 | 7.21e-05 | 0.0001324 | 9673 | 8784 | 2941 | 3526 | 30 | 776 | 3978 | 2100 | 6 | 4449 | 5375 | 16533 | 12637 | 19358 | 17144 | 7597 |
| Nike Classic Fleece Hooded Top | Nike | Active | 40.62 | 16.88 | 161.76 | 98.38 | 21 | 4 | 2 | 2 | 13 | 162.86 | 91.16 | 0.6082 | 0.3333 | 0.2105 | 0.0952 | 0.7647 | 5.99e-05 | 7.03e-05 | 0.0001158 | 13704 | 16183 | 4588 | 3666 | 50 | 776 | 844 | 2100 | 31 | 4548 | 4039 | 1985 | 8752 | 17508 | 16870 | 9484 |
| New Men's Sexy Center Patch Bikini Swimsuit 3G by Gregg Homme | Gregg Homme | Swim | 13.22 | 7.85 | 54.6 | 20.64 | 25 | 4 | 2 | 5 | 14 | 90.3 | 38.29 | 0.378 | 0.3333 | 0.2 | 0.2 | 0.7778 | 2.02e-05 | 1.48e-05 | 0.0001379 | 25672 | 24345 | 13422 | 15782 | 21 | 776 | 844 | 24 | 22 | 8973 | 10649 | 21721 | 8752 | 17510 | 8435 | 9281 |
| Levi's Men's Wool Melton Peacoat | Levi's | Outerwear & Coats | 103.99 | 47.71 | 415.98 | 225.14 | 22 | 4 | 3 | 3 | 12 | 623.97 | 337.71 | 0.5412 | 0.4286 | 0.2105 | 0.1364 | 0.75 | 0.0001541 | 0.0001609 | 0.0001214 | 3776 | 4133 | 937 | 912 | 43 | 776 | 151 | 526 | 37 | 393 | 389 | 8481 | 8270 | 17508 | 14315 | 9487 |
| WeSC Men's Eddy Chino Pant | WESC | Pants | 73.62 | 33.02 | 300.95 | 165.16 | 25 | 4 | 2 | 7 | 12 | 657.75 | 363.33 | 0.5488 | 0.3333 | 0.2222 | 0.28 | 0.75 | 0.0001115 | 0.000118 | 0.0001379 | 6601 | 7527 | 1711 | 1625 | 21 | 776 | 844 | 2 | 37 | 350 | 333 | 7797 | 8752 | 17122 | 5404 | 9487 |

</div>

**Bottom products by Units Returned**

```sql
WITH first_layer AS (
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
WHERE unit_orders_placed_rank <= 50
ORDER BY
  units_returned_rank DESC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TapouT Men's Lock Up Hoodie | TapouT | Fashion Hoodies & Sweatshirts | 36.61 | 20.6 | 229.12 | 103.62 | 23 | 7 | 0 | 1 | 15 | 39.6 | 16.16 | 0.4523 | 0.0 | 0.3182 | 0.0435 | 0.6818 | 8.49e-05 | 7.41e-05 | 0.0001269 | 15388 | 13556 | 2822 | 3414 | 41 | 33 | 13463 | 7029 | 11 | 16416 | 17785 | 17057 | 13463 | 13008 | 17454 | 12986 |
| HUGO BOSS Men's Long Pant | HUGO BOSS | Sleep & Lounge | 74.72 | 28.3 | 1033.11 | 648.16 | 33 | 14 | 0 | 3 | 16 | 233.01 | 138.21 | 0.6274 | 0.0 | 0.4667 | 0.0909 | 0.5333 | 0.0003827 | 0.0004632 | 0.000182 | 6501 | 9383 | 113 | 75 | 6 | 1 | 13463 | 526 | 7 | 2702 | 2165 | 933 | 13463 | 6418 | 16872 | 19494 |
| Joe's Jeans Men's Rebel Relaxed Fit Jean | Joe's Jeans | Jeans | 139.29 | 76.13 | 1296.69 | 583.03 | 26 | 9 | 0 | 3 | 14 | 339.69 | 166.11 | 0.4496 | 0.0 | 0.3913 | 0.1154 | 0.6087 | 0.0004803 | 0.0004167 | 0.0001434 | 2334 | 1721 | 68 | 102 | 17 | 5 | 13463 | 526 | 22 | 1403 | 1558 | 17357 | 13463 | 9082 | 15567 | 16952 |
| Diesel Men's Blade Underpant | Diesel | Underwear | 22.14 | 9.75 | 122.0 | 66.53 | 22 | 6 | 0 | 2 | 14 | 43.0 | 23.83 | 0.5453 | 0.0 | 0.3 | 0.0909 | 0.7 | 4.52e-05 | 4.75e-05 | 0.0001214 | 21886 | 22702 | 6504 | 6114 | 43 | 84 | 13463 | 2100 | 22 | 15676 | 14732 | 8115 | 13463 | 13033 | 16872 | 12849 |
| Ray-Ban Women's 4101 Jackie Ohh Sunglasses | Ray-Ban | Accessories | 97.5 | 41.94 | 486.16 | 280.13 | 22 | 5 | 1 | 5 | 11 | 586.32 | 330.97 | 0.5762 | 0.1667 | 0.2941 | 0.2273 | 0.6875 | 0.0001801 | 0.0002002 | 0.0001214 | 4451 | 5084 | 706 | 587 | 43 | 251 | 3978 | 24 | 43 | 472 | 408 | 4708 | 13196 | 13232 | 7836 | 12983 |
| Wrangler Men's 20X No. 33 Relaxed Straight Leg Jean | Wrangler | Jeans | 55.0 | 29.66 | 220.0 | 100.87 | 24 | 4 | 1 | 2 | 17 | 165.0 | 74.2 | 0.4585 | 0.2 | 0.1818 | 0.0833 | 0.8095 | 8.15e-05 | 7.21e-05 | 0.0001324 | 9673 | 8784 | 2941 | 3526 | 30 | 776 | 3978 | 2100 | 6 | 4449 | 5375 | 16533 | 12637 | 19358 | 17144 | 7597 |
| Wrangler Men's Sarasota Agility Short | Wrangler | Shorts | 33.03 | 16.36 | 198.95 | 101.37 | 25 | 6 | 1 | 3 | 15 | 138.97 | 68.68 | 0.5095 | 0.1429 | 0.2727 | 0.12 | 0.7143 | 7.37e-05 | 7.24e-05 | 0.0001379 | 16765 | 16618 | 3447 | 3505 | 21 | 84 | 3978 | 526 | 11 | 5758 | 5901 | 11606 | 13389 | 14284 | 15549 | 12035 |
| True Religion Men's Ricky Straight Leg Jean | True Religion | Jeans | 227.86 | 123.14 | 1452.0 | 661.01 | 28 | 7 | 1 | 5 | 15 | 1430.0 | 645.85 | 0.4552 | 0.125 | 0.3043 | 0.1786 | 0.6818 | 0.0005379 | 0.0004724 | 0.0001545 | 646 | 406 | 45 | 69 | 9 | 33 | 3978 | 24 | 11 | 57 | 95 | 16801 | 13444 | 13032 | 10715 | 12986 |
| Fred Perry Men's Crew Neck Sweater | Fred Perry | Sweaters | 104.69 | 54.65 | 815.72 | 392.52 | 24 | 8 | 1 | 1 | 14 | 214.74 | 106.77 | 0.4812 | 0.1111 | 0.3478 | 0.0417 | 0.6364 | 0.0003022 | 0.0002805 | 0.0001324 | 3741 | 3335 | 188 | 264 | 30 | 16 | 3978 | 7029 | 22 | 3010 | 3162 | 14461 | 13456 | 9743 | 17456 | 16487 |
| Volcom Men's Vorta Slim Straight Leg Fit Jean | Volcom | Jeans | 73.57 | 41.13 | 574.85 | 249.86 | 27 | 8 | 1 | 4 | 14 | 387.8 | 166.89 | 0.4347 | 0.1111 | 0.3478 | 0.1481 | 0.6364 | 0.0002129 | 0.0001786 | 0.0001489 | 6603 | 5251 | 467 | 746 | 12 | 16 | 3978 | 126 | 22 | 1091 | 1537 | 18678 | 13456 | 9743 | 12705 | 16487 |
| Puma Men's Socks | PUMA | Socks | 13.0 | 7.78 | 90.0 | 35.98 | 24 | 7 | 1 | 5 | 11 | 78.0 | 31.36 | 0.3998 | 0.125 | 0.3684 | 0.2083 | 0.6111 | 3.33e-05 | 2.57e-05 | 0.0001324 | 25705 | 24414 | 8929 | 11107 | 30 | 33 | 3978 | 24 | 43 | 10368 | 12295 | 20955 | 13444 | 9637 | 8433 | 16951 |
| Wrangler Men's Genuine Tampa Cargo Short | Wrangler | Shorts | 31.37 | 15.61 | 229.94 | 116.44 | 29 | 7 | 1 | 5 | 16 | 179.94 | 90.54 | 0.5064 | 0.125 | 0.2917 | 0.1724 | 0.6957 | 8.52e-05 | 8.32e-05 | 0.00016 | 17403 | 17266 | 2818 | 2869 | 8 | 33 | 3978 | 24 | 7 | 3935 | 4081 | 11924 | 13444 | 13236 | 10730 | 12964 |
| Bottoms Out Men's Plaid Sleep Pant | Bottoms Out | Sleep & Lounge | 13.49 | 5.05 | 94.43 | 59.4 | 25 | 7 | 2 | 4 | 12 | 80.94 | 50.64 | 0.629 | 0.2222 | 0.3333 | 0.16 | 0.6316 | 3.5e-05 | 4.25e-05 | 0.0001379 | 25625 | 26913 | 8758 | 6904 | 21 | 33 | 844 | 126 | 37 | 9890 | 8299 | 839 | 12628 | 9747 | 12630 | 16546 |
| JiMarti JM01 Sunglasses for Golf Fishing Cycling-Unbreakable-... Frame | JiMarti | Accessories | 29.95 | 11.92 | 269.55 | 161.1 | 22 | 9 | 2 | 2 | 9 | 119.8 | 72.12 | 0.5977 | 0.1818 | 0.45 | 0.0909 | 0.5 | 9.99e-05 | 0.0001151 | 0.0001214 | 18166 | 20613 | 2175 | 1707 | 43 | 5 | 844 | 2100 | 140 | 6868 | 5540 | 2758 | 13193 | 6490 | 16872 | 19501 |
| Wrangler Men's Premium Performance Cowboy Cut Jean | Wrangler | Jeans | 47.45 | 25.88 | 570.83 | 264.22 | 58 | 12 | 2 | 7 | 37 | 417.81 | 189.65 | 0.4629 | 0.1429 | 0.2353 | 0.1207 | 0.7551 | 0.0002115 | 0.0001888 | 0.00032 | 12004 | 10508 | 470 | 662 | 1 | 2 | 844 | 2 | 1 | 905 | 1224 | 16149 | 13389 | 17092 | 15548 | 9486 |

</div>

**Bottom products by Units Cancelled**

```sql
WITH first_layer AS (
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
WHERE unit_orders_placed_rank <= 50
ORDER BY
  units_cancelled_rank DESC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| State O Maine Big and Tall Fashion Flannel Pajama | KNOTHE CORP. | Sleep & Lounge | 36.88 | 15.59 | 331.92 | 192.51 | 21 | 9 | 5 | 1 | 6 | 221.28 | 127.31 | 0.58 | 0.3571 | 0.45 | 0.0476 | 0.4 | 0.000123 | 0.0001376 | 0.0001158 | 15350 | 17283 | 1492 | 1214 | 50 | 5 | 5 | 7029 | 1398 | 2854 | 2454 | 4293 | 8749 | 6490 | 17453 | 23875 |
| Chaps Big and Tall Solid V-Neck Vest | Chaps | Sweaters | 39.88 | 20.32 | 279.16 | 134.91 | 28 | 7 | 4 | 1 | 16 | 199.4 | 99.06 | 0.4833 | 0.3636 | 0.2593 | 0.0357 | 0.6957 | 0.0001034 | 9.64e-05 | 0.0001545 | 14437 | 13747 | 2029 | 2288 | 9 | 33 | 30 | 7029 | 7 | 3354 | 3543 | 14237 | 8748 | 14407 | 17457 | 12964 |
| TapouT Men's Lock Up Hoodie | TapouT | Fashion Hoodies & Sweatshirts | 36.61 | 20.6 | 229.12 | 103.62 | 23 | 7 | 0 | 1 | 15 | 39.6 | 16.16 | 0.4523 | 0.0 | 0.3182 | 0.0435 | 0.6818 | 8.49e-05 | 7.41e-05 | 0.0001269 | 15388 | 13556 | 2822 | 3414 | 41 | 33 | 13463 | 7029 | 11 | 16416 | 17785 | 17057 | 13463 | 13008 | 17454 | 12986 |
| Fred Perry Men's Crew Neck Sweater | Fred Perry | Sweaters | 104.69 | 54.65 | 815.72 | 392.52 | 24 | 8 | 1 | 1 | 14 | 214.74 | 106.77 | 0.4812 | 0.1111 | 0.3478 | 0.0417 | 0.6364 | 0.0003022 | 0.0002805 | 0.0001324 | 3741 | 3335 | 188 | 264 | 30 | 16 | 3978 | 7029 | 22 | 3010 | 3162 | 14461 | 13456 | 9743 | 17456 | 16487 |
| KAMALIKULTURE Women's Long Sleeve Side Draped Dress | KAMALIKULTURE | Dresses | 83.65 | 40.23 | 467.96 | 240.96 | 23 | 6 | 2 | 1 | 14 | 233.98 | 119.93 | 0.5149 | 0.25 | 0.2727 | 0.0435 | 0.7 | 0.0001734 | 0.0001722 | 0.0001269 | 5490 | 5477 | 768 | 793 | 41 | 84 | 844 | 7029 | 22 | 2696 | 2677 | 11003 | 11344 | 14284 | 17454 | 12849 |
| Nike Classic Fleece Hooded Top | Nike | Active | 40.62 | 16.88 | 161.76 | 98.38 | 21 | 4 | 2 | 2 | 13 | 162.86 | 91.16 | 0.6082 | 0.3333 | 0.2105 | 0.0952 | 0.7647 | 5.99e-05 | 7.03e-05 | 0.0001158 | 13704 | 16183 | 4588 | 3666 | 50 | 776 | 844 | 2100 | 31 | 4548 | 4039 | 1985 | 8752 | 17508 | 16870 | 9484 |
| UltraClub Adult Sherpa-Lined Full-Zip Fleece with Hood | UltraClub | Fashion Hoodies & Sweatshirts | 51.47 | 28.47 | 360.9 | 161.23 | 26 | 7 | 2 | 2 | 15 | 203.71 | 91.12 | 0.4467 | 0.2222 | 0.2917 | 0.0769 | 0.6818 | 0.0001337 | 0.0001152 | 0.0001434 | 10603 | 9302 | 1222 | 1705 | 17 | 33 | 844 | 2100 | 11 | 3228 | 4041 | 17630 | 12628 | 13236 | 17286 | 12986 |
| Joseph Abboud Men's Two-button Side Vent Sport Coat | Joseph Abboud | Suits & Sport Coats | 264.0 | 101.9 | 2904.0 | 1759.82 | 30 | 11 | 2 | 2 | 15 | 1056.0 | 656.57 | 0.606 | 0.1538 | 0.3929 | 0.0667 | 0.5769 | 0.0010758 | 0.0012577 | 0.0001655 | 430 | 734 | 6 | 5 | 7 | 3 | 844 | 2100 | 11 | 112 | 91 | 2144 | 13388 | 9081 | 17408 | 18610 |
| State O Maine Big and Tall Solid Microfleece Lounge Pant | KNOTHE CORP. | Sleep & Lounge | 26.99 | 10.37 | 161.94 | 101.75 | 24 | 6 | 2 | 2 | 14 | 107.96 | 69.2 | 0.6283 | 0.25 | 0.2727 | 0.0833 | 0.7 | 6e-05 | 7.27e-05 | 0.0001324 | 19125 | 22140 | 4586 | 3491 | 30 | 84 | 844 | 2100 | 22 | 7621 | 5851 | 878 | 11344 | 14284 | 17144 | 12849 |
| Lucky Brand Mens Men's 361 Vintage Straight Denim Jean | Lucky Brand | Jeans | 99.0 | 52.65 | 594.0 | 275.91 | 25 | 6 | 3 | 2 | 14 | 495.0 | 228.59 | 0.4645 | 0.3333 | 0.2609 | 0.08 | 0.7 | 0.00022 | 0.0001972 | 0.0001379 | 4113 | 3525 | 427 | 608 | 21 | 84 | 151 | 2100 | 22 | 674 | 896 | 15993 | 8752 | 14406 | 17285 | 12849 |
| Joe's Jeans Men's Slim Fit Straight Leg Brixton | Joe's Jeans | Jeans | 194.26 | 102.07 | 1353.0 | 647.44 | 27 | 7 | 3 | 2 | 15 | 976.0 | 458.49 | 0.4785 | 0.3 | 0.28 | 0.0741 | 0.6818 | 0.0005012 | 0.0004627 | 0.0001489 | 992 | 729 | 58 | 76 | 12 | 33 | 151 | 2100 | 11 | 133 | 207 | 14773 | 11276 | 14282 | 17370 | 12986 |
| Rusty Men's Goombah Too Boardshort | Rusty | Swim | 54.5 | 32.55 | 272.5 | 108.89 | 21 | 5 | 3 | 2 | 11 | 272.5 | 107.04 | 0.3996 | 0.375 | 0.2632 | 0.0952 | 0.6875 | 0.0001009 | 7.78e-05 | 0.0001158 | 10044 | 7672 | 2094 | 3171 | 50 | 251 | 151 | 2100 | 43 | 2048 | 3147 | 20957 | 8725 | 14405 | 16870 | 12983 |
| Van Heusen Men's Tall Wrinkle Free Poplin Long Sleeve Shirt | Van Heusen | Tops & Tees | 36.73 | 20.07 | 225.42 | 102.03 | 22 | 6 | 3 | 2 | 11 | 192.47 | 86.91 | 0.4526 | 0.3333 | 0.3 | 0.0909 | 0.6471 | 8.35e-05 | 7.29e-05 | 0.0001214 | 15384 | 13898 | 2852 | 3476 | 43 | 84 | 151 | 2100 | 43 | 3601 | 4316 | 17055 | 8752 | 13033 | 16872 | 16473 |
| Diesel Men's Blade Underpant | Diesel | Underwear | 22.14 | 9.75 | 122.0 | 66.53 | 22 | 6 | 0 | 2 | 14 | 43.0 | 23.83 | 0.5453 | 0.0 | 0.3 | 0.0909 | 0.7 | 4.52e-05 | 4.75e-05 | 0.0001214 | 21886 | 22702 | 6504 | 6114 | 43 | 84 | 13463 | 2100 | 22 | 15676 | 14732 | 8115 | 13463 | 13033 | 16872 | 12849 |
| Dockers Men's Suit Separate Coat | Dockers | Suits & Sport Coats | 88.36 | 33.97 | 231.12 | 140.98 | 27 | 3 | 4 | 2 | 18 | 542.11 | 337.6 | 0.61 | 0.5714 | 0.12 | 0.0741 | 0.8571 | 8.56e-05 | 0.0001008 | 0.0001489 | 5094 | 7229 | 2783 | 2122 | 12 | 2358 | 30 | 2100 | 4 | 542 | 391 | 1873 | 4252 | 22129 | 17370 | 6057 |

</div>

**Bottom products by Units En Route**

```sql
WITH first_layer AS (
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
WHERE unit_orders_placed_rank <= 50
ORDER BY
  units_en_route_rank DESC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| State O Maine Big and Tall Fashion Flannel Pajama | KNOTHE CORP. | Sleep & Lounge | 36.88 | 15.59 | 331.92 | 192.51 | 21 | 9 | 5 | 1 | 6 | 221.28 | 127.31 | 0.58 | 0.3571 | 0.45 | 0.0476 | 0.4 | 0.000123 | 0.0001376 | 0.0001158 | 15350 | 17283 | 1492 | 1214 | 50 | 5 | 5 | 7029 | 1398 | 2854 | 2454 | 4293 | 8749 | 6490 | 17453 | 23875 |
| Levi's Women's Demi Curve Slim Fit Jean | Levi's | Jeans | 44.99 | 25.36 | 359.92 | 158.59 | 22 | 8 | 5 | 3 | 6 | 359.92 | 157.29 | 0.4406 | 0.3846 | 0.4211 | 0.1364 | 0.4286 | 0.0001333 | 0.0001133 | 0.0001214 | 12553 | 10773 | 1272 | 1757 | 43 | 16 | 5 | 526 | 1398 | 1228 | 1730 | 18170 | 8724 | 7452 | 14315 | 23541 |
| 7 For All Mankind Women's Roxanne Slim Fit Jean | 7 For All Mankind | Jeans | 173.19 | 90.65 | 863.98 | 407.88 | 21 | 5 | 4 | 5 | 7 | 1495.96 | 719.25 | 0.4721 | 0.4444 | 0.3125 | 0.2381 | 0.5833 | 0.0003201 | 0.0002915 | 0.0001158 | 1348 | 1093 | 169 | 237 | 50 | 251 | 30 | 24 | 623 | 48 | 67 | 15325 | 8264 | 13009 | 7773 | 18592 |
| Original Penguin Men's Volley Swim Short | Original Penguin | Swim | 69.0 | 42.12 | 483.0 | 190.09 | 21 | 7 | 3 | 3 | 8 | 414.0 | 160.42 | 0.3936 | 0.3 | 0.3889 | 0.1429 | 0.5333 | 0.0001789 | 0.0001359 | 0.0001158 | 7231 | 5048 | 713 | 1236 | 50 | 33 | 151 | 526 | 295 | 914 | 1664 | 21241 | 11276 | 9083 | 12706 | 19494 |
| Wrangler Men's Original Cowboy Cut Relaxed Fit Jean | Wrangler | Jeans | 42.99 | 22.67 | 228.46 | 108.63 | 25 | 5 | 5 | 7 | 8 | 493.18 | 228.73 | 0.4755 | 0.5 | 0.2778 | 0.28 | 0.6154 | 8.46e-05 | 7.76e-05 | 0.0001379 | 13180 | 12269 | 2826 | 3184 | 21 | 251 | 5 | 2 | 295 | 687 | 895 | 15040 | 4275 | 14283 | 5404 | 16940 |
| Volcom Juniors Pocket Blocket Long Sleeve Tee | Volcom | Tops & Tees | 27.0 | 15.34 | 81.0 | 33.86 | 21 | 3 | 4 | 5 | 9 | 243.0 | 107.41 | 0.418 | 0.5714 | 0.1875 | 0.2381 | 0.75 | 3e-05 | 2.42e-05 | 0.0001158 | 19072 | 17500 | 9846 | 11622 | 50 | 2358 | 30 | 24 | 140 | 2456 | 3131 | 20016 | 4252 | 19354 | 7773 | 9487 |
| HUGO BOSS Men's Striped Crew Sock | HUGO BOSS | Socks | 13.0 | 8.14 | 104.0 | 40.17 | 24 | 8 | 3 | 4 | 9 | 91.0 | 33.33 | 0.3863 | 0.2727 | 0.4 | 0.1667 | 0.5294 | 3.85e-05 | 2.87e-05 | 0.0001324 | 25705 | 24062 | 7764 | 10157 | 30 | 16 | 151 | 126 | 140 | 8958 | 11794 | 21483 | 11342 | 7482 | 10731 | 19498 |
| 7 For All Mankind Men's The Straight Modern Jean | 7 For All Mankind | Jeans | 175.57 | 89.48 | 575.0 | 267.13 | 21 | 4 | 3 | 5 | 9 | 1447.0 | 714.47 | 0.4646 | 0.4286 | 0.25 | 0.2381 | 0.6923 | 0.000213 | 0.0001909 | 0.0001158 | 1310 | 1144 | 466 | 647 | 50 | 776 | 151 | 24 | 140 | 54 | 70 | 15992 | 8270 | 14408 | 7773 | 12966 |
| JiMarti JM01 Sunglasses for Golf Fishing Cycling-Unbreakable-... Frame | JiMarti | Accessories | 29.95 | 11.92 | 269.55 | 161.1 | 22 | 9 | 2 | 2 | 9 | 119.8 | 72.12 | 0.5977 | 0.1818 | 0.45 | 0.0909 | 0.5 | 9.99e-05 | 0.0001151 | 0.0001214 | 18166 | 20613 | 2175 | 1707 | 43 | 5 | 844 | 2100 | 140 | 6868 | 5540 | 2758 | 13193 | 6490 | 16872 | 19501 |
| Lee Men's Relaxed Fit Slightly Tapered Leg Jean | Lee | Jeans | 30.99 | 16.89 | 122.96 | 55.54 | 21 | 4 | 5 | 3 | 9 | 248.92 | 113.31 | 0.4517 | 0.5556 | 0.2222 | 0.1429 | 0.6923 | 4.55e-05 | 3.97e-05 | 0.0001158 | 17446 | 16178 | 6481 | 7447 | 50 | 776 | 5 | 526 | 140 | 2405 | 2891 | 17150 | 4274 | 17122 | 12706 | 12966 |
| RSQ London Mens Skinny Jeans | RSQ | Jeans | 44.99 | 24.2 | 134.97 | 63.21 | 21 | 3 | 5 | 3 | 10 | 359.92 | 163.94 | 0.4683 | 0.625 | 0.1667 | 0.1429 | 0.7692 | 5e-05 | 4.52e-05 | 0.0001158 | 12553 | 11383 | 5908 | 6477 | 50 | 2358 | 5 | 526 | 77 | 1228 | 1608 | 15636 | 4099 | 19436 | 12706 | 9471 |
| HUGO BOSS Men's Bright Argyle Crew Sock | HUGO BOSS | Socks | 9.75 | 5.68 | 39.0 | 15.65 | 22 | 4 | 4 | 4 | 10 | 78.0 | 32.25 | 0.4013 | 0.5 | 0.2222 | 0.1818 | 0.7143 | 1.44e-05 | 1.12e-05 | 0.0001214 | 27342 | 26355 | 16327 | 17765 | 43 | 776 | 30 | 126 | 77 | 10368 | 12068 | 20837 | 4275 | 17122 | 10468 | 12035 |
| Michael Kors Men's 3 Pack Brief | Michael Kors | Underwear | 25.99 | 12.48 | 130.46 | 67.73 | 24 | 5 | 5 | 4 | 10 | 232.38 | 120.98 | 0.5192 | 0.5 | 0.25 | 0.1667 | 0.6667 | 4.83e-05 | 4.84e-05 | 0.0001324 | 19456 | 20053 | 6070 | 5979 | 30 | 251 | 5 | 126 | 77 | 2705 | 2646 | 10469 | 4275 | 14408 | 10731 | 12990 |
| Ray-Ban Women's 4101 Jackie Ohh Sunglasses | Ray-Ban | Accessories | 97.5 | 41.94 | 486.16 | 280.13 | 22 | 5 | 1 | 5 | 11 | 586.32 | 330.97 | 0.5762 | 0.1667 | 0.2941 | 0.2273 | 0.6875 | 0.0001801 | 0.0002002 | 0.0001214 | 4451 | 5084 | 706 | 587 | 43 | 251 | 3978 | 24 | 43 | 472 | 408 | 4708 | 13196 | 13232 | 7836 | 12983 |
| Motherhood Maternity: Sports Clip Down Nursing Bra | Motherhood Maternity | Maternity | 22.54 | 10.46 | 200.82 | 108.99 | 25 | 9 | 2 | 3 | 11 | 112.9 | 60.37 | 0.5427 | 0.1818 | 0.4091 | 0.12 | 0.55 | 7.44e-05 | 7.79e-05 | 0.0001379 | 21822 | 22052 | 3297 | 3165 | 21 | 5 | 844 | 526 | 43 | 7249 | 6811 | 8373 | 13193 | 7481 | 15549 | 19449 |

</div>

**Bottom products by Lost Revenue**

```sql
WITH first_layer AS (
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
WHERE revenue_rank <= 50
ORDER BY
  lost_revenue_rank DESC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Steinbock Tyrolean Sport Coat | Orvis | Suits & Sport Coats | 350.0 | 154.0 | 1400.0 | 784.0 | 11 | 4 | 0 | 0 | 7 | 0.0 | 0.0 | 0.56 | 0.0 | 0.3636 | 0.0 | 0.6364 | 0.0005186 | 0.0005603 | 6.07e-05 | 180 | 217 | 49 | 48 | 1161 | 776 | 13463 | 17458 | 623 | 22642 | 22642 | 6489 | 13463 | 9638 | 17458 | 16487 |
| The North Face Apex Bionic Soft Shell Jacket - Men's | The North Face | Fashion Hoodies & Sweatshirts | 903.0 | 524.64 | 1806.0 | 756.71 | 6 | 2 | 0 | 0 | 4 | 0.0 | 0.0 | 0.419 | 0.0 | 0.3333 | 0.0 | 0.6667 | 0.000669 | 0.0005408 | 3.31e-05 | 5 | 3 | 21 | 55 | 12532 | 6114 | 13463 | 17458 | 6105 | 22642 | 22642 | 19960 | 13463 | 9747 | 17458 | 12990 |
| Women's Knee Length Overcoat in Pure Cashmere | Cashmere Boutique | Outerwear & Coats | 399.0 | 193.12 | 1596.0 | 814.76 | 9 | 4 | 0 | 0 | 5 | 0.0 | 0.0 | 0.5105 | 0.0 | 0.4444 | 0.0 | 0.5556 | 0.0005912 | 0.0005823 | 4.96e-05 | 115 | 100 | 35 | 40 | 3355 | 776 | 13463 | 17458 | 3026 | 22642 | 22642 | 11502 | 13463 | 6492 | 17458 | 19270 |
| Mountain Hardwear Men's Chillwave Down Parka | Mountain Hardwear | Outerwear & Coats | 375.0 | 176.63 | 1500.0 | 793.5 | 5 | 4 | 0 | 0 | 1 | 0.0 | 0.0 | 0.529 | 0.0 | 0.8 | 0.0 | 0.2 | 0.0005557 | 0.0005671 | 2.76e-05 | 155 | 135 | 41 | 44 | 16887 | 776 | 13463 | 17458 | 23197 | 22642 | 22642 | 9645 | 13463 | 607 | 17458 | 26859 |
| AIR JORDAN DOMINATE SHORTS MENS 465071-100 | Jordan | Shorts | 903.0 | 454.21 | 2709.0 | 1346.37 | 5 | 3 | 0 | 0 | 2 | 0.0 | 0.0 | 0.497 | 0.0 | 0.6 | 0.0 | 0.4 | 0.0010035 | 0.0009622 | 2.76e-05 | 5 | 8 | 7 | 9 | 16887 | 2358 | 13463 | 17458 | 17069 | 22642 | 22642 | 12874 | 13463 | 2189 | 17458 | 23875 |
| Quiksilver Men's Rockefeller Walkshort | Quiksilver | Shorts | 903.0 | 472.27 | 1806.0 | 861.46 | 6 | 2 | 0 | 0 | 4 | 0.0 | 0.0 | 0.477 | 0.0 | 0.3333 | 0.0 | 0.6667 | 0.000669 | 0.0006157 | 3.31e-05 | 5 | 7 | 21 | 34 | 12532 | 6114 | 13463 | 17458 | 6105 | 22642 | 22642 | 14881 | 13463 | 9747 | 17458 | 12990 |
| The North Face Nuptse 2 Jacket - Noah Green/TNF Black | The North Face | Outerwear & Coats | 903.0 | 370.23 | 1806.0 | 1065.54 | 8 | 2 | 0 | 0 | 6 | 0.0 | 0.0 | 0.59 | 0.0 | 0.25 | 0.0 | 0.75 | 0.000669 | 0.0007615 | 4.41e-05 | 5 | 29 | 21 | 19 | 5507 | 6114 | 13463 | 17458 | 1398 | 22642 | 22642 | 3353 | 13463 | 14408 | 17458 | 9487 |
| The North Face Denali Down Womens Jacket 2013 | The North Face | Active | 903.0 | 395.51 | 1806.0 | 1014.97 | 8 | 2 | 0 | 0 | 6 | 0.0 | 0.0 | 0.562 | 0.0 | 0.25 | 0.0 | 0.75 | 0.000669 | 0.0007254 | 4.41e-05 | 5 | 20 | 21 | 25 | 5507 | 6114 | 13463 | 17458 | 1398 | 22642 | 22642 | 6272 | 13463 | 14408 | 17458 | 9487 |
| HALSTON HERITAGE Women's Sleeveless Ponte Pleated Dress | Halston Heritage | Dresses | 357.0 | 161.36 | 1428.0 | 782.54 | 9 | 4 | 0 | 0 | 5 | 0.0 | 0.0 | 0.548 | 0.0 | 0.4444 | 0.0 | 0.5556 | 0.000529 | 0.0005593 | 4.96e-05 | 172 | 181 | 47 | 49 | 3355 | 776 | 13463 | 17458 | 3026 | 22642 | 22642 | 7812 | 13463 | 6492 | 17458 | 19270 |
| 7 For All Mankind Men's Austyn Relaxed Straight Jean | 7 For All Mankind | Jeans | 197.94 | 111.63 | 1399.0 | 608.64 | 17 | 7 | 0 | 1 | 9 | 189.0 | 83.35 | 0.4351 | 0.0 | 0.4375 | 0.0588 | 0.5625 | 0.0005182 | 0.000435 | 9.38e-05 | 942 | 526 | 50 | 91 | 103 | 33 | 13463 | 7029 | 140 | 3671 | 4605 | 18597 | 13463 | 6734 | 17433 | 19266 |
| PAIGE Women's Skyline Skinny Jean | PAIGE | Jeans | 158.0 | 90.19 | 1422.0 | 608.93 | 19 | 9 | 0 | 2 | 8 | 316.0 | 135.88 | 0.4282 | 0.0 | 0.5294 | 0.1053 | 0.4706 | 0.0005268 | 0.0004352 | 0.0001048 | 1714 | 1108 | 48 | 90 | 72 | 5 | 13463 | 2100 | 295 | 1575 | 2230 | 19172 | 13463 | 3268 | 16363 | 23444 |
| True Religion Women's Julie Super T Jean | True Religion | Jeans | 326.0 | 172.13 | 1956.0 | 923.23 | 8 | 6 | 0 | 1 | 1 | 326.0 | 153.87 | 0.472 | 0.0 | 0.8571 | 0.125 | 0.1429 | 0.0007246 | 0.0006598 | 4.41e-05 | 233 | 145 | 19 | 31 | 5507 | 84 | 13463 | 7029 | 23197 | 1487 | 1788 | 15335 | 13463 | 546 | 14338 | 27121 |
| Mountain Hardwear Women's Chillwave Down Jacket | Mountain Hardwear | Outerwear & Coats | 375.0 | 179.25 | 1875.0 | 978.75 | 6 | 5 | 0 | 1 | 0 | 375.0 | 195.75 | 0.522 | 0.0 | 1.0 | 0.1667 | 0.0 | 0.0006946 | 0.0006995 | 3.31e-05 | 155 | 128 | 20 | 29 | 12532 | 251 | 13463 | 7029 | 27145 | 1150 | 1161 | 10227 | 13463 | 1 | 10731 | 27145 |
| Barbour Bedale Jacket / Bedale Jacket | Barbour | Outerwear & Coats | 379.0 | 173.96 | 1516.0 | 820.16 | 8 | 4 | 0 | 1 | 3 | 379.0 | 205.04 | 0.541 | 0.0 | 0.5714 | 0.125 | 0.4286 | 0.0005616 | 0.0005862 | 4.41e-05 | 147 | 142 | 39 | 39 | 5507 | 776 | 13463 | 7029 | 10869 | 1133 | 1085 | 8491 | 13463 | 2847 | 14338 | 23541 |
| Barbour Classic Beaufort Jacket / Beaufort Jacket | Barbour | Outerwear & Coats | 399.0 | 193.91 | 1596.0 | 820.34 | 10 | 4 | 0 | 1 | 5 | 399.0 | 205.09 | 0.514 | 0.0 | 0.4444 | 0.1 | 0.5556 | 0.0005912 | 0.0005863 | 5.52e-05 | 115 | 98 | 35 | 38 | 1962 | 776 | 13463 | 7029 | 3026 | 985 | 1084 | 11041 | 13463 | 6492 | 16366 | 19270 |

</div>

**Bottom products by Lost Profit**

```sql
WITH first_layer AS (
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
WHERE profit_rank <= 50
ORDER BY
  lost_profit_rank DESC
LIMIT 15;
```

<div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">

| product_name | product_brand | product_category | avg_product_sale_price | avg_product_cost | revenue | profit | unit_orders_placed | units_completed | units_returned | units_cancelled | units_en_route | lost_revenue | lost_profit | profit_margin | return_rate | completion_rate | cancellation_rate | en_route_rate | revenue_share | profit_share | unit_orders_placed_share | avg_product_sale_price_rank | avg_product_cost_rank | revenue_rank | profit_rank | unit_orders_placed_rank | units_completed_rank | units_returned_rank | units_cancelled_rank | units_en_route_rank | lost_revenue_rank | lost_profit_rank | profit_margin_rank | return_rate_rank | completion_rate_rank | cancellation_rate_rank | en_route_rate_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| The North Face Denali Down Womens Jacket 2013 | The North Face | Active | 903.0 | 395.51 | 1806.0 | 1014.97 | 8 | 2 | 0 | 0 | 6 | 0.0 | 0.0 | 0.562 | 0.0 | 0.25 | 0.0 | 0.75 | 0.000669 | 0.0007254 | 4.41e-05 | 5 | 20 | 21 | 25 | 5507 | 6114 | 13463 | 17458 | 1398 | 22642 | 22642 | 6272 | 13463 | 14408 | 17458 | 9487 |
| Women's Knee Length Overcoat in Pure Cashmere | Cashmere Boutique | Outerwear & Coats | 399.0 | 193.12 | 1596.0 | 814.76 | 9 | 4 | 0 | 0 | 5 | 0.0 | 0.0 | 0.5105 | 0.0 | 0.4444 | 0.0 | 0.5556 | 0.0005912 | 0.0005823 | 4.96e-05 | 115 | 100 | 35 | 40 | 3355 | 776 | 13463 | 17458 | 3026 | 22642 | 22642 | 11502 | 13463 | 6492 | 17458 | 19270 |
| AIR JORDAN DOMINATE SHORTS MENS 465071-100 | Jordan | Shorts | 903.0 | 454.21 | 2709.0 | 1346.37 | 5 | 3 | 0 | 0 | 2 | 0.0 | 0.0 | 0.497 | 0.0 | 0.6 | 0.0 | 0.4 | 0.0010035 | 0.0009622 | 2.76e-05 | 5 | 8 | 7 | 9 | 16887 | 2358 | 13463 | 17458 | 17069 | 22642 | 22642 | 12874 | 13463 | 2189 | 17458 | 23875 |
| Steinbock Tyrolean Sport Coat | Orvis | Suits & Sport Coats | 350.0 | 154.0 | 1400.0 | 784.0 | 11 | 4 | 0 | 0 | 7 | 0.0 | 0.0 | 0.56 | 0.0 | 0.3636 | 0.0 | 0.6364 | 0.0005186 | 0.0005603 | 6.07e-05 | 180 | 217 | 49 | 48 | 1161 | 776 | 13463 | 17458 | 623 | 22642 | 22642 | 6489 | 13463 | 9638 | 17458 | 16487 |
| Mountain Hardwear Men's Chillwave Down Parka | Mountain Hardwear | Outerwear & Coats | 375.0 | 176.63 | 1500.0 | 793.5 | 5 | 4 | 0 | 0 | 1 | 0.0 | 0.0 | 0.529 | 0.0 | 0.8 | 0.0 | 0.2 | 0.0005557 | 0.0005671 | 2.76e-05 | 155 | 135 | 41 | 44 | 16887 | 776 | 13463 | 17458 | 23197 | 22642 | 22642 | 9645 | 13463 | 607 | 17458 | 26859 |
| The North Face Nuptse 2 Jacket - Noah Green/TNF Black | The North Face | Outerwear & Coats | 903.0 | 370.23 | 1806.0 | 1065.54 | 8 | 2 | 0 | 0 | 6 | 0.0 | 0.0 | 0.59 | 0.0 | 0.25 | 0.0 | 0.75 | 0.000669 | 0.0007615 | 4.41e-05 | 5 | 29 | 21 | 19 | 5507 | 6114 | 13463 | 17458 | 1398 | 22642 | 22642 | 3353 | 13463 | 14408 | 17458 | 9487 |
| HALSTON HERITAGE Women's Sleeveless Ponte Pleated Dress | Halston Heritage | Dresses | 357.0 | 161.36 | 1428.0 | 782.54 | 9 | 4 | 0 | 0 | 5 | 0.0 | 0.0 | 0.548 | 0.0 | 0.4444 | 0.0 | 0.5556 | 0.000529 | 0.0005593 | 4.96e-05 | 172 | 181 | 47 | 49 | 3355 | 776 | 13463 | 17458 | 3026 | 22642 | 22642 | 7812 | 13463 | 6492 | 17458 | 19270 |
| Quiksilver Men's Rockefeller Walkshort | Quiksilver | Shorts | 903.0 | 472.27 | 1806.0 | 861.46 | 6 | 2 | 0 | 0 | 4 | 0.0 | 0.0 | 0.477 | 0.0 | 0.3333 | 0.0 | 0.6667 | 0.000669 | 0.0006157 | 3.31e-05 | 5 | 7 | 21 | 34 | 12532 | 6114 | 13463 | 17458 | 6105 | 22642 | 22642 | 14881 | 13463 | 9747 | 17458 | 12990 |
| True Religion Women's Julie Super T Jean | True Religion | Jeans | 326.0 | 172.13 | 1956.0 | 923.23 | 8 | 6 | 0 | 1 | 1 | 326.0 | 153.87 | 0.472 | 0.0 | 0.8571 | 0.125 | 0.1429 | 0.0007246 | 0.0006598 | 4.41e-05 | 233 | 145 | 19 | 31 | 5507 | 84 | 13463 | 7029 | 23197 | 1487 | 1788 | 15335 | 13463 | 546 | 14338 | 27121 |
| Mountain Hardwear Women's Chillwave Down Jacket | Mountain Hardwear | Outerwear & Coats | 375.0 | 179.25 | 1875.0 | 978.75 | 6 | 5 | 0 | 1 | 0 | 375.0 | 195.75 | 0.522 | 0.0 | 1.0 | 0.1667 | 0.0 | 0.0006946 | 0.0006995 | 3.31e-05 | 155 | 128 | 20 | 29 | 12532 | 251 | 13463 | 7029 | 27145 | 1150 | 1161 | 10227 | 13463 | 1 | 10731 | 27145 |
| Barbour Bedale Jacket / Bedale Jacket | Barbour | Outerwear & Coats | 379.0 | 173.96 | 1516.0 | 820.16 | 8 | 4 | 0 | 1 | 3 | 379.0 | 205.04 | 0.541 | 0.0 | 0.5714 | 0.125 | 0.4286 | 0.0005616 | 0.0005862 | 4.41e-05 | 147 | 142 | 39 | 39 | 5507 | 776 | 13463 | 7029 | 10869 | 1133 | 1085 | 8491 | 13463 | 2847 | 14338 | 23541 |
| Barbour Classic Beaufort Jacket / Beaufort Jacket | Barbour | Outerwear & Coats | 399.0 | 193.91 | 1596.0 | 820.34 | 10 | 4 | 0 | 1 | 5 | 399.0 | 205.09 | 0.514 | 0.0 | 0.4444 | 0.1 | 0.5556 | 0.0005912 | 0.0005863 | 5.52e-05 | 115 | 98 | 35 | 38 | 1962 | 776 | 13463 | 7029 | 3026 | 985 | 1084 | 11041 | 13463 | 6492 | 16366 | 19270 |
| Carhartt Men's Canvas Shirt Jacket | Carhartt | Outerwear & Coats | 448.99 | 181.39 | 1346.97 | 802.79 | 5 | 3 | 0 | 1 | 1 | 448.99 | 267.6 | 0.596 | 0.0 | 0.75 | 0.2 | 0.25 | 0.000499 | 0.0005737 | 2.76e-05 | 92 | 120 | 61 | 42 | 16887 | 2358 | 13463 | 7029 | 23197 | 828 | 658 | 2857 | 13463 | 746 | 8435 | 26348 |
| Jones New York Women's Hidden Snap Notch Collar Coat | Jones New York | Outerwear & Coats | 599.0 | 253.38 | 1797.0 | 1036.87 | 5 | 3 | 0 | 1 | 1 | 599.0 | 345.62 | 0.577 | 0.0 | 0.75 | 0.2 | 0.25 | 0.0006657 | 0.000741 | 2.76e-05 | 56 | 61 | 28 | 24 | 16887 | 2358 | 13463 | 7029 | 23197 | 428 | 368 | 4613 | 13463 | 746 | 8435 | 26348 |
| Rebecca Minkoff Women's Leather Luciana Skirt | Rebecca Minkoff | Skirts | 598.0 | 249.96 | 1794.0 | 1044.11 | 7 | 3 | 1 | 0 | 3 | 598.0 | 348.04 | 0.582 | 0.25 | 0.4286 | 0.0 | 0.5 | 0.0006646 | 0.0007462 | 3.86e-05 | 57 | 62 | 30 | 22 | 8625 | 2358 | 3978 | 17458 | 10869 | 430 | 358 | 4095 | 11344 | 6739 | 17458 | 19501 |

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
