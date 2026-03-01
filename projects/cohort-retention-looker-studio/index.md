---
layout: default
title: "Cohort Retention Analysis – Looker Studio"
description: "Analyzing customer retention patterns using BigQuery cohort analysis and an interactive Looker Studio dashboard — covering retention matrices, revenue retention, acquisition channel performance, lifecycle segmentation, and cumulative LTV."
---

<a href="/projects/" class="back-to-projects btn">&larr; Back to Projects</a>

# Cohort Retention Analysis – Looker Studio

> This project builds a complete cohort retention analysis pipeline using SQL in BigQuery and delivers an interactive Looker Studio dashboard. It covers customer retention, revenue retention, acquisition channel performance, lifecycle segmentation, and cumulative lifetime value.

---

<details>
  <summary><strong>Project Overview</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Overview</h3>
  <p>
    This project demonstrates end-to-end cohort retention analysis — from writing SQL queries in BigQuery to
    building a self-service Looker Studio dashboard. The goal is to transform raw transactional data into
    retention insights that support marketing, product, and growth decisions.
  </p>

  <h3>Business Context</h3>
  <p>
    Retention is one of the most important levers for sustainable growth. Acquiring new customers is expensive;
    understanding how long they stay, when they churn, and which channels produce the most durable customers
    allows teams to allocate resources more effectively. This analysis simulates the role of an analyst supporting
    growth and marketing teams at an e-commerce company.
  </p>

  <h3>Objectives</h3>
  <ul>
    <li>Size monthly acquisition cohorts and track new customer volume over time</li>
    <li>Build a full retention matrix showing how each cohort retains month-over-month</li>
    <li>Measure revenue retention to understand how cohort spending evolves over time</li>
    <li>Compare retention rates across acquisition channels (traffic sources)</li>
    <li>Segment customers into lifecycle stages (Active, At-Risk, Churned) and detect reactivations</li>
    <li>Track cumulative revenue per customer to understand long-term lifetime value by cohort</li>
    <li>Deliver all insights through an interactive Looker Studio dashboard</li>
  </ul>

  <h3>Dataset</h3>
  <p>
    <code>thelook_ecommerce</code> is a public BigQuery dataset simulating an online retail business.
    It contains transactional order data, line-item purchases, product attributes, and customer information.
    Only completed orders (<code>status = 'Complete'</code>) with <code>created_at &lt; '2025-01-01'</code>
    are included to ensure a clean, bounded analysis window.
  </p>

  <h4>Core Tables Used</h4>
  <ul>
    <li><code>orders</code> — one row per order (timestamps, status, user_id)</li>
    <li><code>order_items</code> — one row per item purchased (sale_price, product_id, order_id)</li>
    <li><code>users</code> — customer attributes (traffic_source, demographics)</li>
  </ul>

  <h3>SQL Techniques Demonstrated</h3>
  <ul>
    <li>Common Table Expressions (CTEs) for modular, readable query design</li>
    <li>Window functions (<code>LAG</code>, <code>SUM() OVER</code>) for gap detection and running totals</li>
    <li><code>DATE_TRUNC</code> and <code>DATE_DIFF</code> for cohort assignment and period calculation</li>
    <li>Multi-table joins (orders, order_items, users)</li>
    <li><code>CASE</code> statements for lifecycle segmentation</li>
    <li>Self-joins for baseline comparisons (revenue retention)</li>
  </ul>

  <h3>KPI Definitions</h3>
  <ul>
    <li><strong>Cohort Month</strong> — the month of a customer's first completed order</li>
    <li><strong>Period Number</strong> — months elapsed since cohort month (0 = first month)</li>
    <li><strong>Retention %</strong> — <code>active_users / cohort_size &times; 100</code></li>
    <li><strong>Revenue Retention %</strong> — <code>period_revenue / baseline_revenue &times; 100</code></li>
    <li><strong>Customer Status</strong> — Active (&le;90 days since last order), At-Risk (91–180 days), Churned (&gt;180 days)</li>
    <li><strong>Cumulative Revenue per Customer</strong> — running total of revenue divided by cohort size</li>
  </ul>

  <h3>Tools Used</h3>
  <ul>
    <li>Google BigQuery (SQL)</li>
    <li>Google Looker Studio (dashboard &amp; visualization)</li>
    <li>GitHub (version control)</li>
    <li>GitHub Pages (documentation &amp; portfolio publishing)</li>
  </ul>

</details>
<details>
  <summary><strong>Analysis 1 — Cohort Sizing</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>How many new customers are acquired each month, and how has acquisition volume changed over time?</p>

  <h3>Method</h3>
  <p>
    Each customer is assigned to a cohort based on the month of their first completed order. This query counts
    distinct customers per cohort month to establish baseline cohort sizes — the foundation for all downstream
    retention analysis.
  </p>

  <h3>SQL Query</h3>
  <pre><code class="language-sql">SELECT
  cohort_month,
  COUNT(DISTINCT user_id) AS new_customers
FROM (
  SELECT
    user_id,
    DATE(DATE_TRUNC(MIN(created_at), MONTH)) AS cohort_month
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
  GROUP BY user_id
)
GROUP BY cohort_month
ORDER BY cohort_month</code></pre>

  <h3>Insights</h3>
  <ul>
    <li>Cohort sizes establish the denominator for all retention calculations — accuracy here is critical.</li>
    <li>Growth in monthly new customers indicates whether the acquisition engine is scaling or plateauing.</li>
    <li>Months with unusually large or small cohorts may reflect marketing campaigns, seasonality, or data anomalies worth investigating.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Monitor acquisition trends:</strong> track cohort sizes monthly to detect growth slowdowns early.</li>
    <li><strong>Correlate with spend:</strong> overlay acquisition costs per cohort to understand CAC trends alongside volume.</li>
    <li><strong>Flag anomalies:</strong> investigate cohorts with unusual sizes to separate organic growth from one-time events.</li>
  </ul>

</details>
<details>
  <summary><strong>Analysis 2 — Customer Retention Matrix</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>What percentage of each monthly cohort returns to make a purchase in subsequent months?</p>

  <h3>Method</h3>
  <p>
    This is the core retention analysis. Four CTEs work together: (1) assign each customer to their cohort month,
    (2) capture every distinct month each customer was active, (3) join cohorts to activity and calculate the
    period number (months since first purchase), and (4) compute cohort sizes. The final output is a full
    retention matrix with retention percentage for every cohort-period combination.
  </p>

  <h3>SQL Query</h3>
  <pre><code class="language-sql">WITH customer_cohorts AS (
  -- CTE 1: Get each customer's cohort month (first order month)
  SELECT
    user_id,
    DATE(DATE_TRUNC(MIN(created_at), MONTH)) AS cohort_month
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
  GROUP BY user_id
),

monthly_activity AS (
  -- CTE 2: Get every distinct month each customer placed an order
  SELECT DISTINCT
    user_id,
    DATE(DATE_TRUNC(created_at, MONTH)) AS activity_month
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
),

retention_data AS (
  -- CTE 3: Join cohorts to activity, calculate period number
  SELECT
    c.cohort_month,
    DATE_DIFF(DATE(a.activity_month), DATE(c.cohort_month), MONTH) AS period_number,
    COUNT(DISTINCT c.user_id) AS active_users
  FROM customer_cohorts c
  JOIN monthly_activity a
    ON c.user_id = a.user_id
  GROUP BY c.cohort_month, period_number
),

cohort_sizes AS (
  -- Get total customers per cohort for retention % calculation
  SELECT
    cohort_month,
    COUNT(DISTINCT user_id) AS cohort_size
  FROM customer_cohorts
  GROUP BY cohort_month
)

-- Final query: retention matrix
SELECT
  r.cohort_month,
  r.period_number,
  r.active_users,
  s.cohort_size,
  ROUND(r.active_users / s.cohort_size * 100, 2) AS retention_pct
FROM retention_data r
JOIN cohort_sizes s
  ON r.cohort_month = s.cohort_month
WHERE r.period_number >= 0
ORDER BY r.cohort_month, r.period_number</code></pre>

  <h3>Insights</h3>
  <ul>
    <li>Retention typically drops steeply after Period 0, with the largest churn occurring between the first and second month.</li>
    <li>Cohorts that survive the initial drop-off tend to stabilize, suggesting a "loyal core" forms early.</li>
    <li>Comparing retention curves across cohorts reveals whether product or marketing changes are improving stickiness over time.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Focus on Month 1 activation:</strong> the biggest retention lever is reducing early churn — invest in onboarding, post-purchase emails, and first-repeat incentives.</li>
    <li><strong>Benchmark cohorts:</strong> set retention targets per period and flag cohorts that underperform for root-cause investigation.</li>
    <li><strong>Track improvement over time:</strong> newer cohorts retaining better than older ones signals that product or CX investments are working.</li>
  </ul>

</details>
<details>
  <summary><strong>Analysis 3 — Revenue Retention by Cohort</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>How does cohort revenue evolve over time relative to the first month, and are retained customers spending more or less?</p>

  <h3>Method</h3>
  <p>
    This query extends retention analysis from headcount to revenue. For each cohort-period, it calculates
    total revenue and compares it to the cohort's Period 0 (baseline) revenue. Revenue retention above 100%
    means retained customers are spending more per period than the original cohort did in their first month.
  </p>

  <h3>SQL Query</h3>
  <pre><code class="language-sql">WITH customer_cohorts AS (
  SELECT
    user_id,
    DATE(DATE_TRUNC(MIN(created_at), MONTH)) AS cohort_month
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
  GROUP BY user_id
),

monthly_revenue AS (
  SELECT
    oi.user_id,
    DATE(DATE_TRUNC(oi.created_at, MONTH)) AS activity_month,
    SUM(oi.sale_price) AS monthly_revenue
  FROM `bigquery-public-data.thelook_ecommerce.order_items` oi
  JOIN `bigquery-public-data.thelook_ecommerce.orders` o
    ON oi.order_id = o.order_id
  WHERE o.status = 'Complete'
    AND o.created_at < '2025-01-01'
  GROUP BY oi.user_id, activity_month
),

revenue_by_period AS (
  SELECT
    c.cohort_month,
    DATE_DIFF(r.activity_month, c.cohort_month, MONTH) AS period_number,
    SUM(r.monthly_revenue) AS period_revenue
  FROM customer_cohorts c
  JOIN monthly_revenue r
    ON c.user_id = r.user_id
  GROUP BY c.cohort_month, period_number
),

period_zero_revenue AS (
  SELECT
    cohort_month,
    period_revenue AS baseline_revenue
  FROM revenue_by_period
  WHERE period_number = 0
)

SELECT
  r.cohort_month,
  r.period_number,
  ROUND(r.period_revenue, 2) AS period_revenue,
  ROUND(p.baseline_revenue, 2) AS baseline_revenue,
  ROUND(r.period_revenue / p.baseline_revenue * 100, 2) AS revenue_retention_pct
FROM revenue_by_period r
JOIN period_zero_revenue p
  ON r.cohort_month = p.cohort_month
WHERE r.period_number >= 0
ORDER BY r.cohort_month, r.period_number</code></pre>

  <h3>Insights</h3>
  <ul>
    <li>Revenue retention declines more gradually than customer retention when retained customers increase their spending over time.</li>
    <li>Cohorts with revenue retention above 100% in later periods indicate strong upsell or cross-sell dynamics among loyal customers.</li>
    <li>Divergence between customer retention and revenue retention highlights whether value is concentrating in a smaller, higher-spending group.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Separate volume from value:</strong> track both customer retention and revenue retention to get the full picture.</li>
    <li><strong>Invest in retained customers:</strong> if revenue retention outpaces headcount retention, double down on loyalty programs and personalized recommendations.</li>
    <li><strong>Identify revenue decay:</strong> cohorts where revenue drops faster than headcount may signal pricing pressure or reduced engagement.</li>
  </ul>

</details>
<details>
  <summary><strong>Analysis 4 — Retention by Acquisition Channel</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>Which acquisition channels produce the most durable customers, and how does retention vary by traffic source?</p>

  <h3>Method</h3>
  <p>
    This query joins the <code>users</code> table to bring in <code>traffic_source</code> as the acquisition
    channel dimension. Instead of grouping by cohort month, retention is calculated per channel across all
    cohorts — revealing which channels produce customers with the best long-term retention.
  </p>

  <h3>SQL Query</h3>
  <pre><code class="language-sql">WITH customer_cohorts AS (
  SELECT
    o.user_id,
    u.traffic_source,
    DATE(DATE_TRUNC(MIN(o.created_at), MONTH)) AS cohort_month
  FROM `bigquery-public-data.thelook_ecommerce.orders` o
  JOIN `bigquery-public-data.thelook_ecommerce.users` u
    ON o.user_id = u.id
  WHERE o.status = 'Complete'
    AND o.created_at < '2025-01-01'
  GROUP BY o.user_id, u.traffic_source
),

monthly_activity AS (
  SELECT DISTINCT
    user_id,
    DATE(DATE_TRUNC(created_at, MONTH)) AS activity_month
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
),

retention_data AS (
  SELECT
    c.traffic_source,
    DATE_DIFF(a.activity_month, c.cohort_month, MONTH) AS period_number,
    COUNT(DISTINCT c.user_id) AS active_users
  FROM customer_cohorts c
  JOIN monthly_activity a
    ON c.user_id = a.user_id
  GROUP BY c.traffic_source, period_number
),

channel_sizes AS (
  SELECT
    traffic_source,
    COUNT(DISTINCT user_id) AS channel_size
  FROM customer_cohorts
  GROUP BY traffic_source
)

SELECT
  r.traffic_source,
  r.period_number,
  r.active_users,
  s.channel_size,
  ROUND(r.active_users / s.channel_size * 100, 2) AS retention_pct
FROM retention_data r
JOIN channel_sizes s
  ON r.traffic_source = s.traffic_source
WHERE r.period_number >= 0
ORDER BY r.traffic_source, r.period_number</code></pre>

  <h3>Insights</h3>
  <ul>
    <li>Not all acquisition channels are equal — some drive volume but produce customers who churn quickly.</li>
    <li>Organic and search channels often retain better than paid channels, reflecting higher purchase intent at acquisition.</li>
    <li>Channel-level retention curves help distinguish between channels that drive short-term revenue vs. long-term customer value.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Shift budget toward durable channels:</strong> factor retention into CAC/LTV calculations when allocating marketing spend.</li>
    <li><strong>Improve onboarding for low-retention channels:</strong> customers from paid or social channels may need stronger post-purchase engagement to stick.</li>
    <li><strong>Set channel-specific targets:</strong> benchmark each channel's retention curve and flag underperformance early.</li>
  </ul>

</details>
<details>
  <summary><strong>Analysis 5 — Customer Lifecycle Segmentation</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>What proportion of customers are currently Active, At-Risk, or Churned — and how many have reactivated after a long gap?</p>

  <h3>Method</h3>
  <p>
    This analysis takes a snapshot approach. Using recency (days since last order as of 2024-12-31), each
    customer is classified into a lifecycle segment: <strong>Active</strong> (&le;90 days), <strong>At-Risk</strong>
    (91–180 days), or <strong>Churned</strong> (&gt;180 days). A separate CTE detects reactivations — customers
    who returned after a gap of 90+ days between consecutive orders.
  </p>

  <h3>SQL Query — Lifecycle Segments</h3>
  <pre><code class="language-sql">WITH customer_activity AS (
  SELECT
    user_id,
    DATE(MIN(created_at)) AS first_order_date,
    DATE(MAX(created_at)) AS last_order_date,
    COUNT(DISTINCT order_id) AS total_orders,
    DATE_DIFF(
      DATE('2024-12-31'),
      DATE(MAX(created_at)),
      DAY
    ) AS days_since_last_order
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
  GROUP BY user_id
),

customer_segments AS (
  SELECT
    user_id,
    first_order_date,
    last_order_date,
    total_orders,
    days_since_last_order,
    CASE
      WHEN days_since_last_order <= 90 THEN 'Active'
      WHEN days_since_last_order <= 180 THEN 'At-Risk'
      ELSE 'Churned'
    END AS customer_status
  FROM customer_activity
),

-- Bonus: detect reactivations (customers who returned after a 90+ day gap)
order_gaps AS (
  SELECT
    user_id,
    DATE(created_at) AS order_date,
    LAG(DATE(created_at)) OVER (PARTITION BY user_id ORDER BY created_at) AS prev_order_date,
    DATE_DIFF(
      DATE(created_at),
      LAG(DATE(created_at)) OVER (PARTITION BY user_id ORDER BY created_at),
      DAY
    ) AS days_between_orders
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
),

reactivations AS (
  SELECT
    COUNT(DISTINCT user_id) AS reactivated_customers
  FROM order_gaps
  WHERE days_between_orders > 90
)

-- Main output: segment counts
SELECT
  customer_status,
  COUNT(*) AS customer_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS pct_of_total,
  ROUND(AVG(total_orders), 2) AS avg_orders,
  ROUND(AVG(days_since_last_order), 0) AS avg_days_since_last_order
FROM customer_segments
GROUP BY customer_status
ORDER BY customer_count DESC</code></pre>

  <h3>SQL Query — Reactivated Customers</h3>
  <pre><code class="language-sql">SELECT
  COUNT(DISTINCT user_id) AS reactivated_customers
FROM (
  SELECT
    user_id,
    DATE_DIFF(
      DATE(created_at),
      LAG(DATE(created_at)) OVER (PARTITION BY user_id ORDER BY created_at),
      DAY
    ) AS days_between_orders
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
)
WHERE days_between_orders > 90</code></pre>

  <h3>Insights</h3>
  <ul>
    <li>Lifecycle segmentation provides a real-time health check of the customer base beyond just acquisition and retention curves.</li>
    <li>The At-Risk segment represents an actionable window — these customers haven't churned yet but are showing signs of disengagement.</li>
    <li>Reactivation counts prove that churn isn't always permanent; win-back campaigns have a viable audience.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Prioritize At-Risk outreach:</strong> deploy targeted re-engagement campaigns (email, offers, reminders) before customers cross into Churned.</li>
    <li><strong>Build win-back flows:</strong> since reactivations happen naturally, structured win-back campaigns should improve the rate further.</li>
    <li><strong>Track segment movement:</strong> monitor shifts between Active, At-Risk, and Churned over time to detect systemic retention changes.</li>
  </ul>

</details>
<details>
  <summary><strong>Analysis 6 — Cumulative Revenue & Customer LTV</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>How does cumulative revenue per customer grow over time by cohort, and which cohorts generate the highest long-term value?</p>

  <h3>Method</h3>
  <p>
    This query calculates period-level revenue per cohort, then uses a window function (<code>SUM() OVER</code>)
    to compute a running cumulative total. Dividing cumulative revenue by cohort size produces
    <strong>cumulative revenue per customer</strong> — a proxy for lifetime value (LTV) at each period.
  </p>

  <h3>SQL Query</h3>
  <pre><code class="language-sql">WITH customer_cohorts AS (
  SELECT
    user_id,
    DATE(DATE_TRUNC(MIN(created_at), MONTH)) AS cohort_month
  FROM `bigquery-public-data.thelook_ecommerce.orders`
  WHERE status = 'Complete'
    AND created_at < '2025-01-01'
  GROUP BY user_id
),

cohort_sizes AS (
  SELECT
    cohort_month,
    COUNT(DISTINCT user_id) AS cohort_size
  FROM customer_cohorts
  GROUP BY cohort_month
),

monthly_revenue AS (
  SELECT
    c.cohort_month,
    DATE_DIFF(DATE(DATE_TRUNC(oi.created_at, MONTH)), c.cohort_month, MONTH) AS period_number,
    SUM(oi.sale_price) AS period_revenue
  FROM customer_cohorts c
  JOIN `bigquery-public-data.thelook_ecommerce.order_items` oi
    ON c.user_id = oi.user_id
  JOIN `bigquery-public-data.thelook_ecommerce.orders` o
    ON oi.order_id = o.order_id
  WHERE o.status = 'Complete'
    AND o.created_at < '2025-01-01'
  GROUP BY c.cohort_month, period_number
)

SELECT
  r.cohort_month,
  r.period_number,
  ROUND(r.period_revenue, 2) AS period_revenue,
  ROUND(
    SUM(r.period_revenue) OVER (
      PARTITION BY r.cohort_month
      ORDER BY r.period_number
    ), 2
  ) AS cumulative_revenue,
  s.cohort_size,
  ROUND(
    SUM(r.period_revenue) OVER (
      PARTITION BY r.cohort_month
      ORDER BY r.period_number
    ) / s.cohort_size, 2
  ) AS cumulative_revenue_per_customer
FROM monthly_revenue r
JOIN cohort_sizes s
  ON r.cohort_month = s.cohort_month
WHERE r.period_number >= 0
ORDER BY r.cohort_month, r.period_number</code></pre>

  <h3>Insights</h3>
  <ul>
    <li>Cumulative revenue per customer is the clearest measure of long-term cohort value and directly informs LTV estimates.</li>
    <li>Older cohorts with more periods of data reveal the true shape of the LTV curve — how quickly it flattens determines payback period.</li>
    <li>Cohort-level LTV differences can signal changes in product-market fit, customer mix, or competitive dynamics over time.</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Set CAC limits from LTV:</strong> use cumulative revenue per customer curves to define maximum acceptable acquisition cost by channel.</li>
    <li><strong>Compare cohort trajectories:</strong> newer cohorts tracking below older ones at the same period may indicate a retention or monetization problem.</li>
    <li><strong>Forecast revenue:</strong> use mature cohort LTV curves to project future revenue from recent cohorts.</li>
  </ul>

</details>
<details>
  <summary><strong>Live Dashboard</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Interactive Looker Studio Dashboard</h3>
  <p>
    The dashboard below connects directly to the BigQuery query results and provides interactive exploration
    of all retention analyses. Use the filters and controls to drill into specific cohorts, time periods,
    and acquisition channels.
  </p>

  <div style="margin: 20px 0; text-align: center;">
    <iframe width="100%" height="675" src="https://lookerstudio.google.com/embed/reporting/44cf727a-85c5-4eca-9ba2-b2553d5164ae/page/wzjqF" frameborder="0" style="border:0; max-width:1200px; border-radius:6px;" allowfullscreen sandbox="allow-storage-access-by-user-activation allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"></iframe>
  </div>

  <p style="font-size:0.9em; color:#888; text-align:center;">
    <a href="https://lookerstudio.google.com/reporting/44cf727a-85c5-4eca-9ba2-b2553d5164ae" target="_blank" rel="noopener">Open dashboard in Looker Studio &rarr;</a>
  </p>

</details>
<details>
  <summary><strong>Conclusion</strong></summary>

  <div style="margin-top: 12px;"></div>

  <p>
    This project demonstrates a complete cohort retention analysis pipeline — from SQL query design in BigQuery
    to an interactive Looker Studio dashboard. Across six analyses, I built retention matrices, measured revenue
    retention, compared acquisition channels, segmented customer lifecycles, and tracked cumulative lifetime value.
  </p>

  <h3>Key Takeaways</h3>
  <ul>
    <li><strong>Early churn is the biggest lever:</strong> the steepest retention drop occurs between Month 0 and Month 1 — onboarding and first-repeat activation deserve the most investment.</li>
    <li><strong>Revenue retention tells a different story than headcount:</strong> retained customers often spend more over time, meaning customer retention understates the value of loyalty.</li>
    <li><strong>Channel quality varies:</strong> acquisition channels that drive volume don't always produce durable customers — retention-adjusted LTV should inform budget allocation.</li>
    <li><strong>Lifecycle segmentation is actionable:</strong> At-Risk customers represent a real-time intervention opportunity, and reactivation data proves win-back campaigns have a viable audience.</li>
    <li><strong>LTV curves drive strategy:</strong> cumulative revenue per customer by cohort provides the foundation for CAC limits, revenue forecasting, and long-term growth planning.</li>
  </ul>

  <p>
    Together, these analyses show how SQL-based cohort analysis paired with a self-service dashboard transforms
    raw transactional data into retention insights that support marketing, product, and growth decisions.
  </p>

</details>
