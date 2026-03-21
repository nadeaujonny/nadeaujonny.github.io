WITH customer_order_counts AS (
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
ORDER BY segment;