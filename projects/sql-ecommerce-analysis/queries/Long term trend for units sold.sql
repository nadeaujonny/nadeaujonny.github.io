SELECT
	DATE_TRUNC(DATE(o.created_at), MONTH) AS month,
	COUNT(*) AS units_sold
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.orders` AS o
ON oi.order_id = o.order_id
WHERE oi.status = 'Complete'
GROUP BY month
ORDER BY month;