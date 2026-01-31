---
layout: default
title: Tableau — Olist Ops & Customer Experience
---

# Tableau — Olist E-commerce Operations & Customer Experience Analysis

> A comprehensive Tableau analysis of the Olist Brazilian E-commerce dataset, focusing on order fulfillment performance, delivery efficiency, and customer experience metrics across 99,441 orders from September 2016 to August 2018.

---

<details>
  <summary><strong>Project Overview</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Overview</h3>
  <p>
    This project analyzes operational performance and customer experience in the Olist e-commerce marketplace using Tableau. 
    The analysis examines order fulfillment metrics, delivery performance, late delivery patterns, and order status distribution 
    to identify operational bottlenecks and opportunities for improvement in customer experience.
  </p>

  <h3>Business Context</h3>
  <p>
    E-commerce marketplaces depend on reliable fulfillment and delivery performance to maintain customer satisfaction and drive repeat purchases. 
    This analysis provides operations and customer experience teams with visibility into delivery times, completion rates, 
    and late delivery patterns to support data-driven decision making.
  </p>

  <h3>Objectives</h3>
  <ul>
    <li>Measure and track core operational KPIs: total orders, average delivery time, order completion rate, and late delivery rate</li>
    <li>Analyze delivery time trends and patterns across the September 2016 to August 2018 time period</li>
    <li>Identify periods of operational stress with elevated late delivery rates</li>
    <li>Examine the distribution of delivery times to understand fulfillment consistency</li>
    <li>Provide actionable insights to improve delivery performance and customer satisfaction</li>
  </ul>

  <h3>Dataset Overview</h3>
  <ul>
    <li><strong>Source:</strong> Olist Brazilian E-commerce Public Dataset (Kaggle)</li>
    <li><strong>Time range:</strong> September 2016 – August 2018</li>
    <li><strong>Granularity:</strong> Order-level data with customer, seller, product, payment, and review information</li>
    <li><strong>Tables used:</strong> Orders, Order Items, Customers, Sellers, Products, Product Category Translation, Order Payments, Order Reviews</li>
    <li><strong>Total orders analyzed:</strong> 99,441</li>
  </ul>

  <h3>Tools &amp; Skills Demonstrated</h3>
  <ul>
    <li><strong>Tableau Desktop:</strong> Data relationships, calculated fields, parameters, filters, dashboards</li>
    <li><strong>Data Modeling:</strong> Multi-table relationships using order_id, customer_id, product_id, seller_id</li>
    <li><strong>Calculated Fields:</strong> Delivery days, late delivery flags, completion rate, aggregated metrics</li>
    <li><strong>Visualization:</strong> KPI cards, time series line charts, bar charts, histograms, dashboard design</li>
    <li><strong>Analysis:</strong> Trend analysis, distribution analysis, operational performance measurement</li>
  </ul>

  <h3>Key Metrics Defined</h3>
  <ul>
    <li><strong>Total Orders:</strong> COUNT(DISTINCT Order ID) for orders with status "delivered"</li>
    <li><strong>Average Delivery Time:</strong> AVG(Order Delivered Customer Date - Order Purchase Timestamp) in days</li>
    <li><strong>Order Completion Rate:</strong> Percentage of orders with status "delivered" out of all orders</li>
    <li><strong>Late Delivery Rate:</strong> Percentage of delivered orders where actual delivery date exceeded estimated delivery date</li>
    <li><strong>Delivery Days:</strong> Time between order purchase and customer delivery (in days)</li>
  </ul>

</details>

---

<details>
  <summary><strong>Data Modeling & Preparation</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Tableau Data Model</h3>
  <p>
    The Olist dataset consists of 8 related tables connected through common keys. I used Tableau's 
    relationship model (rather than joins) to maintain flexibility and proper granularity across different levels of analysis.
  </p>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/tableau-data-connections.png"
      alt="Tableau data model showing relationships between Olist tables"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Tableau data model showing table relationships.
      <span style="display:block; margin-top:4px;">
        <a href="images/tableau-data-connections.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/TableauProjectDataPage.png"
      alt="Tableau Data Source page showing all connected tables"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Tableau Data Source page with all 8 tables from the Olist dataset.
      <span style="display:block; margin-top:4px;">
        <a href="images/TableauProjectDataPage.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Table Relationships</h3>
  <ul>
    <li><strong>olist_orders_dataset:</strong> Central fact table (order_id as primary key)</li>
    <li><strong>olist_customers_dataset:</strong> Linked via customer_id</li>
    <li><strong>olist_order_items_dataset:</strong> Linked via order_id (many-to-one with orders)</li>
    <li><strong>olist_products_dataset:</strong> Linked via product_id</li>
    <li><strong>product_category_name_translation:</strong> Linked via product_category_name (English translations)</li>
    <li><strong>olist_sellers_dataset:</strong> Linked via seller_id</li>
    <li><strong>olist_order_payments_dataset:</strong> Linked via order_id</li>
    <li><strong>olist_order_reviews_dataset:</strong> Linked via order_id</li>
  </ul>

  <h3>Data Preparation Notes</h3>
  <ul>
    <li>Connected all tables using relationships rather than joins to maintain flexibility</li>
    <li>Created calculated fields for delivery time analysis (days between purchase and delivery)</li>
    <li>Built late delivery flag by comparing actual delivery date to estimated delivery date</li>
    <li>Filtered to "delivered" orders for completion rate and delivery time calculations</li>
    <li>Used live connection for real-time filtering and exploration</li>
  </ul>

  <h3>Key Calculated Fields</h3>
  <ul>
    <li><strong>Delivery Days:</strong> DATEDIFF('day', [Order Purchase Timestamp], [Order Delivered Customer Date])</li>
    <li><strong>Late Delivery Flag:</strong> IF [Order Delivered Customer Date] > [Order Estimated Delivery Date] THEN 1 ELSE 0 END</li>
    <li><strong>Is Delivered:</strong> IF [Order Status] = "delivered" THEN 1 ELSE 0 END</li>
    <li><strong>Order Completion Rate:</strong> SUM([Is Delivered]) / COUNT([Order Id])</li>
    <li><strong>Late Delivery Rate:</strong> SUM([Late Delivery Flag]) / COUNT([Order Id]) for delivered orders</li>
  </ul>

</details>

---

<details>
  <summary><strong>Analysis 1 — Order Fulfillment Performance Metrics (Sep 2016 – Aug 2018)</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>
    How is the Olist marketplace performing on core operational and customer experience metrics? What are the overall 
    fulfillment KPIs (total orders, average delivery time, order completion rate, late delivery rate), and how have 
    delivery performance and late deliveries trended over the September 2016 to August 2018 period?
  </p>

  <h3>Method</h3>
  <ul>
    <li>Built KPI summary cards for Total Orders, Average Delivery Time, Order Completion Rate, and Late Delivery Rate</li>
    <li>Created time series visualizations showing monthly order volume and late delivery rate trends</li>
    <li>Analyzed order status distribution to understand completion patterns</li>
    <li>Examined the distribution of delivery times using a histogram to assess fulfillment consistency</li>
    <li>Analyzed average delivery time by month to identify seasonal or operational patterns</li>
  </ul>

  <h3>Results — KPI Summary Cards</h3>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/tableau-analysis-1-total-orders.png"
      alt="Total Orders KPI card showing 99,441 orders"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Total Orders KPI (99,441 delivered orders analyzed).
      <span style="display:block; margin-top:4px;">
        <a href="images/tableau-analysis-1-total-orders.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/tableau-analysis-1-average-delivery-time-kpi-card.png"
      alt="Average Delivery Time KPI card showing 12.5 days"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Average Delivery Time KPI (12.5 days from purchase to customer delivery).
      <span style="display:block; margin-top:4px;">
        <a href="images/tableau-analysis-1-average-delivery-time-kpi-card.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/tableau-analysis-1-order-completion-rate-kpi-card.png"
      alt="Order Completion Rate KPI card showing 97.0%"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Order Completion Rate KPI (97.0% of orders successfully delivered).
      <span style="display:block; margin-top:4px;">
        <a href="images/tableau-analysis-1-order-completion-rate-kpi-card.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/tableau-analysis-1-late-delivery-rate-kpi-card.png"
      alt="Late Delivery Rate KPI card showing 6.8%"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Late Delivery Rate KPI (6.8% of delivered orders arrived after estimated delivery date).
      <span style="display:block; margin-top:4px;">
        <a href="images/tableau-analysis-1-late-delivery-rate-kpi-card.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Results — Trends & Distributions</h3>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/tableau-analysis-1-monthly-order-volume.png"
      alt="Monthly order volume trend from Sep 2016 to Aug 2018"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Monthly order volume showing dramatic growth from late 2016 through mid-2018, with a sharp decline in Aug 2018.
      <span style="display:block; margin-top:4px;">
        <a href="images/tableau-analysis-1-monthly-order-volume.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/tableau-analysis-1-late-delivery-rate.png"
      alt="Late delivery rate percentage over time"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Late delivery rate by month showing an initial spike (100% in early 2016 with limited data) stabilizing to ~10% baseline with notable spikes.
      <span style="display:block; margin-top:4px;">
        <a href="images/tableau-analysis-1-late-delivery-rate.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/tableau-analysis-1-average-delivery-time.png"
      alt="Average delivery time by month in days"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Average delivery time by month showing significant improvement from ~55 days in early operations to stabilizing around 10-15 days by 2017-2018.
      <span style="display:block; margin-top:4px;">
        <a href="images/tableau-analysis-1-average-delivery-time.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/tableau-analysis-1-order-status-distribution.png"
      alt="Order status distribution showing delivered, shipped, canceled, unavailable, etc."
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Order status distribution: 97.02% delivered, 1.11% shipped, 0.63% canceled, and small percentages of other statuses.
      <span style="display:block; margin-top:4px;">
        <a href="images/tableau-analysis-1-order-status-distribution.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/tableau-analysis-1-distribution-of-delivery-times.png"
      alt="Histogram showing distribution of delivery times in days"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Distribution of delivery times: heavily concentrated in 0-30 day range with a peak around 10-15 days and long tail extending beyond 60 days.
      <span style="display:block; margin-top:4px;">
        <a href="images/tableau-analysis-1-distribution-of-delivery-times.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Results — Dashboard</h3>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="images/tableau-analysis-1-dashboard.png"
      alt="Complete dashboard showing all order fulfillment performance metrics"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Interactive dashboard combining all order fulfillment KPIs, trends, and distributions.
      <span style="display:block; margin-top:4px;">
        <a href="images/tableau-analysis-1-dashboard.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Key Findings</h3>
  <ul>
    <li><strong>Strong order completion:</strong> 97% order completion rate indicates reliable fulfillment operations</li>
    <li><strong>Significant growth trajectory:</strong> Monthly order volume grew dramatically from ~400 orders in late 2016 to peak of ~7,500 orders in early 2018</li>
    <li><strong>Improved delivery speed over time:</strong> Average delivery time improved from 50+ days in early operations to stabilizing around 12.5 days by 2017-2018</li>
    <li><strong>Acceptable but improvable late delivery rate:</strong> 6.8% overall late delivery rate with periodic spikes reaching 10-20%</li>
    <li><strong>Consistent delivery performance:</strong> Most orders delivered within 10-30 days, though a long tail of delayed orders exists</li>
    <li><strong>Early operational challenges:</strong> August-November 2016 showed 100% late delivery rates, likely due to launch phase and operational scaling</li>
    <li><strong>Stabilization period:</strong> Operations stabilized by early 2017 with late delivery rates settling to ~10% baseline</li>
  </ul>

  <h3>Business Recommendations</h3>
  <ul>
    <li><strong>Investigate late delivery spikes:</strong> Drill into periods with elevated late delivery rates (10-20%) to identify root causes—carrier issues, regional bottlenecks, high-volume periods, or seller performance problems</li>
    <li><strong>Focus on the long tail:</strong> Analyze orders taking 45+ days to identify patterns (specific product categories, seller locations, or customer regions) and implement targeted interventions</li>
    <li><strong>Set SLA targets by segment:</strong> Not all products require the same delivery speed—consider differentiated targets for product categories with different customer expectations</li>
    <li><strong>Monitor completion rate proactively:</strong> 97% is strong but track this metric by region, seller, and product category to catch deterioration early</li>
    <li><strong>Celebrate and replicate improvement:</strong> Document the operational improvements that reduced average delivery time from 50+ to 12.5 days and apply these lessons to remaining problem areas</li>
    <li><strong>Operationalize delivery time monitoring:</strong> Create alerts for when weekly/monthly delivery times exceed thresholds to enable faster operational response</li>
  </ul>

</details>

---

<details>
  <summary><strong>Tableau Public & Downloads</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Interactive Dashboard</h3>
  <p>
    <strong>Tableau Public Link:</strong> [Coming soon - dashboard will be published to Tableau Public]
  </p>

  <h3>Project Files</h3>
  <p>
    The Olist dataset is publicly available on Kaggle: 
    <a href="https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce" target="_blank" rel="noopener">
      Brazilian E-commerce Public Dataset by Olist
    </a>
  </p>

</details>

---

<details>
  <summary><strong>Limitations & Future Analysis</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Limitations</h3>
  <ul>
    <li><strong>August 2018 data completeness:</strong> The sharp drop in order volume in August 2018 suggests incomplete data for that month</li>
    <li><strong>Early period sample size:</strong> August-November 2016 had very limited orders, making trend analysis less reliable for that period</li>
    <li><strong>Missing contextual data:</strong> No information on carrier performance, warehouse locations, or external factors (holidays, promotions) that may impact delivery times</li>
    <li><strong>Geographic detail:</strong> Customer and seller location data limited to city/state level without distance calculations</li>
    <li><strong>No customer satisfaction scores tied to delivery:</strong> Review scores exist but aren't directly linked to delivery performance in this analysis</li>
  </ul>

  <h3>Next Steps</h3>
  <ul>
    <li><strong>Customer experience deep-dive:</strong> Analyze correlation between delivery performance and review scores/ratings</li>
    <li><strong>Seller performance analysis:</strong> Identify top and bottom performers by delivery time and late delivery rate</li>
    <li><strong>Geographic analysis:</strong> Map customer and seller locations to identify high-performing and problem regions</li>
    <li><strong>Product category analysis:</strong> Examine delivery performance by product category to identify category-specific patterns</li>
    <li><strong>Payment and delivery correlation:</strong> Analyze if payment method impacts delivery speed or completion rates</li>
    <li><strong>Cohort analysis:</strong> Track delivery performance improvements or deterioration for customers over time</li>
  </ul>

</details>
