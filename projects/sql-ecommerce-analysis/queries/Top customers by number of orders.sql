WITH first_layer AS (
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
LIMIT 15;