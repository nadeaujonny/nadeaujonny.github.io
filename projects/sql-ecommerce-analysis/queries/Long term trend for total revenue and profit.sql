SELECT
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
ORDER BY month;