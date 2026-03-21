WITH metrics AS (
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
ORDER BY month;
