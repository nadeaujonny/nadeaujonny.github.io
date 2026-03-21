WITH metrics AS (
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
ORDER BY month;
