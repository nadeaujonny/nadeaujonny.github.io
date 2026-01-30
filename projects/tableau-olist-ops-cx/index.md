---
layout: default
title: Tableau — Olist Ops & Customer Experience
---

# Tableau — Marketplace Ops & Customer Experience (Olist)

<details open>
<summary><h2 style="display: inline;">📊 Project Introduction</h2></summary>

### Overview
This Tableau dashboard analyzes operations and customer experience metrics for Olist, a Brazilian e-commerce marketplace connecting small businesses with major marketplaces. The dashboard enables stakeholders to monitor order fulfillment performance, identify delivery bottlenecks, and assess customer satisfaction trends across the platform's two-year operational history.

### Business Context
- **Marketplace dynamics**: Olist operates as a SaaS platform where delivery performance directly impacts both seller reputation and customer retention
- **Operational efficiency**: Late deliveries and order cancellations create compounding costs through refunds, support tickets, and seller churn
- **Customer experience**: Review scores and delivery times are leading indicators of platform health and competitive positioning
- **Seller accountability**: Performance metrics enable data-driven seller management and quality assurance

### Business Questions
- What is our overall order fulfillment performance and how has it trended over time?
- Which geographic regions or product categories experience the highest late delivery rates?
- How do delivery times correlate with customer satisfaction (review scores)?
- What percentage of orders are delivered within estimated timeframes?
- Are there seasonal patterns in order volume, delivery performance, or customer complaints?

### Tools & Skills Demonstrated
- **Tableau Desktop**: Data relationships (7 tables), calculated fields, parameters, dashboard actions, interactive filtering
- **Data Preparation**: Power Query for data cleaning and transformation, custom column creation
- **Visualization Techniques**: KPI cards, time series analysis, distribution histograms, geographic mapping, status breakdowns
- **Business Metrics**: Order completion rate, late delivery rate, average delivery time, order status distribution

### Dataset
- **Source**: [Olist Brazilian E-commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle)
- **Time Range**: September 2016 - August 2018 (23 months)
- **Tables Used**: 
  - `olist_orders_dataset` (99,441 orders)
  - `olist_order_items_dataset` (112,650 items)
  - `olist_order_payments_dataset` (103,886 payment records)
  - `olist_order_reviews_dataset` (99,224 reviews)
  - `olist_customers_dataset` (99,441 customers)
  - `olist_sellers_dataset` (3,095 sellers)
  - `olist_products_dataset` (32,951 products)
  - `product_category_name_translation` (71 categories)
- **Notes**: 
  - August 2016 contains partial month data (excluded from trend analyses)
  - September 2018 has very limited data (dataset ends abruptly)
  - Some orders lack review scores (not all customers submit reviews)
  - Geolocation data available but not used in current analysis

### Data Modeling (Tableau)
- **Approach**: Used Tableau relationships (not joins) to preserve row-level detail across all tables
- **Primary Key**: `order_id` serves as the central relationship key connecting orders, items, payments, and reviews
- **Grain Considerations**: 
  - Order-level metrics: completion rate, delivery time, late delivery flag
  - Item-level metrics: product categories, freight costs, pricing
  - Payment-level metrics: payment type distribution, installment analysis
  - Review-level metrics: satisfaction scores, review text sentiment (future)
- **Extract Configuration**: Live connection for development; published extract refreshed weekly for production

### Definitions & Metrics

**Order Completion Rate**
- Calculation: `COUNT([Order Id]) WHERE [Order Status] = "delivered" / COUNT([Order Id])`
- Meaning: Percentage of orders successfully delivered to customers
- Current Value: 97.0%

**Late Delivery Rate**
- Calculation: `SUM([Is Delivered Late]) / COUNT([Order Id]) WHERE [Order Status] = "delivered"`
- Definition: Orders where actual delivery date > estimated delivery date
- Current Value: 6.8%

**Average Delivery Time**
- Calculation: `AVG([Delivery Days]) WHERE [Order Status] = "delivered"`
- Definition: Days between order purchase timestamp and delivery to customer timestamp
- Current Value: 12.5 days

**Delivery Days**
- Calculation: `DATEDIFF('day', [Order Purchase Timestamp], [Order Delivered Customer Date])`
- Note: Only calculated for delivered orders; null for canceled/unavailable orders

**Late Delivery Flag**
- Calculation: `IF [Order Delivered Customer Date] > [Order Estimated Delivery Date] THEN 1 ELSE 0 END`
- Binary indicator used for aggregation in late delivery rate

**Order Status Categories**
- `delivered`: Successfully fulfilled orders (97.02%)
- `shipped`: Orders in transit (1.11%)
- `canceled`: Customer or system cancellations (0.63%)
- `unavailable`: Out of stock or seller issues (0.61%)
- `invoiced`: Payment processed, awaiting shipment (0.30%)
- `processing`: Order being prepared (0.30%)
- `created`: Order placed, payment pending (0.00%)
- `approved`: Payment approved, not yet invoiced (0.00%)

</details>

---

<details open>
<summary><h2 style="display: inline;">🎯 Analysis 1: Order Fulfillment Performance Overview</h2></summary>

### Purpose
Provide executives and operations managers with a high-level view of core fulfillment metrics, identifying overall platform health and spotting anomalies that require deeper investigation.

### Key Visualizations

**1. KPI Summary Cards**
- Total Orders: 99,441
- Average Delivery Time: 12.5 days
- Order Completion Rate: 97.0%
- Late Delivery Rate: 6.8%

**2. Monthly Order Volume Trend (Sep 2016 - Aug 2018)**
- Line chart showing steady growth from ~400 orders/month (late 2016) to 7,000+ orders/month (mid-2018)
- Notable spike in November 2017 (~7,500 orders) correlating with Black Friday
- Sharp decline in August 2018 due to dataset cutoff (incomplete month)

**3. Late Delivery Rate Over Time**
- Line chart with reference line at 10% (operational target)
- High volatility in early months (100% in August 2016 due to data quality)
- Stabilization around 5-10% from February 2017 onward
- Slight uptick during high-volume periods (November-December)

**4. Order Status Distribution**
- Horizontal bar chart showing 97% of orders successfully delivered
- Small percentages of shipped (1.1%), canceled (0.6%), and unavailable (0.6%) orders
- Processing and invoiced orders represent <0.5% combined (minimal backlog)

**5. Average Delivery Time by Month**
- Line chart with trend line showing improvement over time
- Initial delivery times: 50+ days (August 2016, data quality issues)
- Improvement to 20-day average by November 2016
- Stabilization at 10-15 days from mid-2017 onward
- Trend line indicates 50% reduction in delivery time over operational period

**6. Distribution of Delivery Times (Histogram)**
- Histogram showing delivery day frequency distribution
- Modal delivery time: 10-15 days (30,000+ orders)
- Right-skewed distribution with long tail extending to 200+ days
- 80% of orders delivered within 20 days
- Outliers beyond 60 days represent edge cases (remote locations, complications)

### Key Filters & Interactivity
- **Date Range Slider**: Filter analyses to specific time periods
- **Order Status Multi-Select**: Focus on delivered vs. all orders
- **Delivery Status Toggle**: Filter to late vs. on-time deliveries

### Findings
1. **Strong baseline performance**: 97% order completion rate indicates reliable fulfillment infrastructure
2. **Improving efficiency**: Average delivery time decreased 50% from early 2017 to mid-2018
3. **Consistent late delivery challenge**: ~7% late delivery rate persists despite volume growth
4. **Seasonal volume spikes**: November-December show 30-40% order increases without proportional late delivery increases (good capacity management)
5. **Long tail of problematic deliveries**: While most orders arrive in 10-15 days, outliers skew averages and likely drive negative reviews

### Business Recommendations
1. **Investigate late delivery root causes**: 7% late rate represents ~6,800 orders annually—conduct RCA on geographic, seller, or carrier factors
2. **Set estimated delivery expectations conservatively**: Add 2-3 day buffer to algorithmic estimates to underpromise/overdeliver
3. **Proactive communication for delays**: Automate notifications for orders exceeding 20 days to reduce support tickets
4. **Seller performance tiering**: Create accountability metrics for sellers with >15% late delivery rates
5. **Black Friday preparation**: Given November spikes, ensure carrier capacity agreements and warehouse staffing 2 months in advance

</details>

---

<details>
<summary><h2 style="display: inline;">📦 Analysis 2: [Ready for Content]</h2></summary>

### Purpose
[Coming soon - space reserved for geographic delivery analysis, product category performance, or carrier comparison]

### Key Visualizations
[Placeholder for analysis 2 content]

### Key Filters & Interactivity
[Placeholder for analysis 2 filters]

### Findings
[Placeholder for analysis 2 findings]

### Business Recommendations
[Placeholder for analysis 2 recommendations]

</details>

---

<details>
<summary><h2 style="display: inline;">⭐ Analysis 3: [Ready for Content]</h2></summary>

### Purpose
[Coming soon - space reserved for customer satisfaction analysis, review score correlations, or seller performance metrics]

### Key Visualizations
[Placeholder for analysis 3 content]

### Key Filters & Interactivity
[Placeholder for analysis 3 filters]

### Findings
[Placeholder for analysis 3 findings]

### Business Recommendations
[Placeholder for analysis 3 recommendations]

</details>

---

<details>
<summary><h2 style="display: inline;">🗺️ Analysis 4: [Ready for Content]</h2></summary>

### Purpose
[Coming soon - space reserved for geographic insights, regional performance, or delivery route optimization]

### Key Visualizations
[Placeholder for analysis 4 content]

### Key Filters & Interactivity
[Placeholder for analysis 4 filters]

### Findings
[Placeholder for analysis 4 findings]

### Business Recommendations
[Placeholder for analysis 4 recommendations]

</details>

---

<details>
<summary><h2 style="display: inline;">💡 Analysis 5: [Ready for Content]</h2></summary>

### Purpose
[Coming soon - space reserved for additional analysis dimension]

### Key Visualizations
[Placeholder for analysis 5 content]

### Key Filters & Interactivity
[Placeholder for analysis 5 filters]

### Findings
[Placeholder for analysis 5 findings]

### Business Recommendations
[Placeholder for analysis 5 recommendations]

</details>

---

## 🔗 Tableau Public

**Dashboard Link**: [View Interactive Dashboard](https://public.tableau.com/app/profile/your-profile-name) *(Link to be added after publication)*

### Embedded Preview
*(Dashboard embed code to be added after Tableau Public publication)*

---

## ⚠️ Limitations

- **Incomplete time periods**: August 2016 and September 2018 contain partial data; excluded from trend analyses
- **Review score coverage**: Only 99,224 reviews for 99,441 orders (~0.2% of orders lack review data)
- **No carrier attribution**: Dataset doesn't identify which logistics companies handled deliveries, limiting root cause analysis
- **Missing customer segments**: No demographic data (age, income, customer type) to enable cohort analysis
- **Geographic granularity**: ZIP code prefix only (not full address), limiting precise location-based insights
- **Product details**: No product names, only category labels—limits SKU-level analysis

---

## 🚀 Next Steps

### For This Analysis
- Add geographic heat maps showing late delivery hot spots by region
- Create seller performance scorecards with delivery SLAs
- Build predictive model for estimated delivery time accuracy
- Incorporate review text sentiment analysis to correlate with delivery performance

### Skills Development
- Learn Tableau Prep for more complex ETL workflows
- Explore Tableau parameters for "what-if" scenario modeling
- Study LOD expressions for advanced calculated field techniques
- Practice dashboard performance optimization for larger datasets

### Portfolio Expansion
- Build complementary SQL project analyzing same dataset from database perspective
- Create Python analysis with predictive modeling for late delivery risk
- Develop Power BI version to demonstrate cross-platform expertise
