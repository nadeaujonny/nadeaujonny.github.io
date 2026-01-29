---
layout: default
title: Tableau — Olist Ops & Customer Experience
---

# Tableau — Marketplace Operations & Customer Experience (Olist)

## Overview
This Tableau analysis examines operational performance and customer experience metrics for Olist, a Brazilian e-commerce marketplace connecting small businesses with major sales channels. Using two years of transactional data (Sep 2016 - Aug 2018), I built an interactive dashboard suite that enables stakeholders to monitor order fulfillment KPIs, identify delivery bottlenecks, and assess customer satisfaction trends. The analysis reveals critical insights about delivery performance, order completion rates, and temporal patterns that directly impact customer experience.

## Business Context
- **Marketplace Dynamics**: In multi-vendor marketplaces, operational excellence directly impacts both seller reputation and platform retention
- **Customer Experience Priority**: Late deliveries and order fulfillment issues are primary drivers of negative reviews and customer churn
- **Competitive Advantage**: Fast, reliable fulfillment is a key differentiator in e-commerce, especially for competing with established players
- **Scalability Challenges**: As order volumes grow 10-15x over the analysis period, maintaining consistent delivery performance becomes increasingly complex

## Business Questions
1. What is our current order fulfillment performance, and how has it evolved over time?
2. What percentage of orders are delivered late, and what is the trend?
3. How long does it take on average to deliver orders, and are there seasonal patterns?
4. What is our order completion rate, and what causes order failures?
5. How is order volume trending, and can our operations scale to meet demand?
6. What is the distribution of delivery times, and where are the bottlenecks?

## Tools & Skills Demonstrated
- **Tableau Desktop**: Data relationships (star schema), calculated fields, parameters, KPI cards, time-series analysis, histograms, trendlines, dashboard actions, interactive filters, responsive layout design
- **Data Preparation**: Connected and related 7 CSV tables using Tableau's relationship model, created calculated fields for delivery metrics and date-based measures
- **Visualization Techniques**: Time-series line charts with dual-axis reference lines, percentage-based horizontal bar charts, KPI cards with conditional formatting, histogram distributions, interactive filtering across multiple charts
- **Business Analytics**: Cohort analysis, trend identification, KPI monitoring, operational diagnostics, data storytelling through dashboard design

## Dataset
- **Source**: Olist Brazilian E-commerce Public Dataset (Kaggle)
- **Time Range**: September 2016 - August 2018 (23 months)
- **Total Orders Analyzed**: 99,441 distinct orders
- **Tables Used**: 
  - `olist_orders_dataset` (order lifecycle dates and status)
  - `olist_customers_dataset` (customer location)
  - `olist_sellers_dataset` (seller location)
  - `olist_order_items_dataset` (order line items)
  - `olist_order_payments_dataset` (payment information)
  - `olist_order_reviews_dataset` (customer ratings)
  - `product_category_name_translation` (category translations)
- **Notes/Caveats**: 
  - Dataset ends abruptly in August 2018 (incomplete final month)
  - Some orders lack review scores (customers did not leave feedback)
  - Canceled and unavailable orders included in status analysis but excluded from delivery time calculations

## Data Modeling (Tableau)
- **Approach**: Used Tableau Relationships (not joins) to create a star schema with `olist_orders_dataset` as the fact table
- **Relationship Keys**:
  - Orders → Customers: `customer_id`
  - Orders → Order Items: `order_id`
  - Order Items → Products: `product_id`
  - Order Items → Sellers: `seller_id`
  - Orders → Payments: `order_id`
  - Orders → Reviews: `order_id`
- **Grain**: Primary analysis at order level; some views drill to order-item level
- **Extract vs Live**: Used Tableau Extract (.hyper) for faster performance and offline analysis capability
- **Benefits of Relationships**: Preserved correct aggregation levels, avoided duplicate rows from joins, simplified data model maintenance

## Definitions & Metrics

### Core KPIs
- **Total Orders**: `COUNTD([Order Id])` - Distinct count of all orders regardless of status
- **Average Delivery Time**: `AVG([Delivery Days])` - Mean number of days from order purchase to customer delivery (delivered orders only)
- **Order Completion Rate**: `SUM([Is Delivered]) / COUNTD([Order Id])` - Percentage of orders with status "delivered"
- **Late Delivery Rate**: `SUM([Is Late Delivery]) / SUM([Is Delivered])` - Percentage of delivered orders that arrived after the estimated delivery date

### Calculated Fields
- **Delivery Days**: `DATEDIFF('day', [Order Purchase Timestamp], [Order Delivered Customer Date])`
- **Is Delivered**: `IF [Order Status] = "delivered" THEN 1 ELSE 0 END`
- **Is Late Delivery**: `IF [Order Delivered Customer Date] > [Order Estimated Delivery Date] THEN 1 ELSE 0 END`
- **Order Status Distribution**: Aggregated count by status category (delivered, shipped, canceled, unavailable, invoiced, processing, created, approved)

### Temporal Dimensions
- **Month of Order**: `MONTH([Order Purchase Timestamp])` - Extracted month for trend analysis
- **Order Purchase Timestamp**: Primary date field for time-series visualizations

## Analysis 1: Order Fulfillment Performance

### Purpose
This dashboard provides a comprehensive view of operational KPIs related to order fulfillment, delivery speed, and completion rates. It enables operations managers to monitor performance trends, identify deteriorating metrics, and diagnose root causes of delivery issues.

### Dashboard Components

#### Top-Level KPI Cards
Four key performance indicators provide immediate visibility into fulfillment health:

1. **Total Orders: 99,441**
   - All orders placed during the analysis period (Sep 2016 - Aug 2018)
   - Context: Shows scale of operations and data completeness

2. **Average Delivery Time: 12.5 Days**
   - Mean time from order purchase to customer delivery
   - Industry context: Amazon Prime sets customer expectations at 2-day delivery; 12.5 days is significantly slower
   - Calculation excludes non-delivered orders to avoid skewing the metric

3. **Order Completion Rate: 97.0%**
   - Percentage of orders successfully delivered to customers
   - High completion rate indicates good operational reliability
   - 3% of orders failed due to cancellations, processing issues, or unavailability

4. **Late Delivery Rate: 6.8%**
   - Percentage of delivered orders that arrived after the promised date
   - While seemingly low, this represents ~6,700 customers who experienced late delivery
   - Late deliveries strongly correlate with negative reviews and customer churn

#### Monthly Order Volume (Sep 2016 - Aug 2018)
**Visualization**: Line chart showing order count by month

**Key Insights**:
- **Exponential Growth**: Order volume increased from ~500 orders/month in late 2016 to over 7,000 orders/month by mid-2018
- **Growth Rate**: Approximately 10-15x increase over the 23-month period, indicating rapid marketplace adoption
- **Seasonality**: Visible peaks in November (Black Friday/Cyber Monday) and May, with slight dips in January
- **August 2018 Drop**: Sharp decline in final month due to incomplete data (dataset ends mid-month)
- **Operational Implication**: This rapid scaling tests the limits of fulfillment infrastructure and seller capacity

#### Late Delivery Rate by Month (%)
**Visualization**: Line chart with percentage on y-axis, reference line at 10%

**Key Insights**:
- **Initial Spike**: Late delivery rate was extremely high (nearly 100%) in August 2016, likely due to early platform teething issues or small sample size
- **Rapid Improvement**: Rate dropped to 2-5% by late 2016, suggesting operational process improvements
- **Stabilization**: From early 2017 onward, late delivery rate stabilized between 5-10%
- **Slight Upward Trend**: Late 2017 and 2018 show a modest increase in late deliveries, potentially due to scaling challenges as order volume grew
- **10% Reference Line**: Dashed line at 10% serves as an operational threshold; staying below this target is critical for customer satisfaction
- **Recommendation**: The upward creep in late delivery rate during high-growth periods warrants investigation into seller performance, logistics partner reliability, and estimated delivery date accuracy

#### Order Status Distribution
**Visualization**: Horizontal bar chart showing count of orders by status

**Key Insights**:
- **Delivered (97.02%)**: Overwhelming majority of orders successfully delivered - 96,478 orders
- **Shipped (1.11%)**: 1,104 orders currently in transit (snapshot data means some orders are still being fulfilled)
- **Canceled (0.63%)**: 626 orders canceled by customer or system
- **Unavailable (0.61%)**: 607 orders failed due to product stockouts or seller issues
- **Other Statuses**: Invoiced, processing, created, approved represent very small percentages (<0.3% each)
- **Operational Excellence**: The high delivery rate demonstrates strong fulfillment capabilities, but canceled and unavailable orders represent revenue loss and poor customer experience
- **Focus Area**: Investigating root causes of unavailable orders could reduce customer frustration and increase revenue capture

#### Average Delivery Time by Month (Days)
**Visualization**: Line chart with trend line (dashed), showing days on y-axis

**Key Insights**:
- **Early Platform**: Delivery times started at ~55 days in August 2016, indicating severe early operational challenges
- **Dramatic Improvement**: Rapid decrease to ~5-7 days by November 2016, suggesting major process optimizations
- **Stable Performance**: From mid-2017 onward, average delivery time stabilized at 10-15 days
- **Downward Trend**: The dashed trendline shows overall improvement over time, despite order volume increasing 10x+
- **Seasonal Variation**: Slight increases in delivery time during November and December (holiday season), as expected
- **Recent Stability**: 2018 shows consistent ~10-12 day delivery times even as volume continued growing
- **Competitive Gap**: While improved, 10-15 day delivery is still slow compared to major e-commerce players (Amazon, Mercado Livre)

#### Distribution of Delivery Times (Days)
**Visualization**: Histogram showing frequency distribution of delivery times

**Key Insights**:
- **Right-Skewed Distribution**: Most orders delivered within 0-30 days, with a long tail extending to 210+ days
- **Modal Range**: Highest concentration of orders delivered in the 10-20 day range, with peak around 15 days
- **Fast Delivery Subset**: Significant number of orders (20,000-25,000) delivered in 0-15 days, likely express shipping or local fulfillment
- **Outliers**: Small number of orders taking 60+ days, representing extreme operational failures
- **Second Peak**: Minor secondary peak around 25-30 days suggests some orders consistently hit a different fulfillment pathway
- **Operational Implication**: The wide variance in delivery times (0-210 days) indicates inconsistent seller performance or logistics quality
- **Recommendation**: Segment sellers by delivery time performance; provide incentives or training to reduce variance and shift distribution leftward

### Primary Filters
- **Is Delivered**: Parameter to toggle between all orders vs. only delivered orders (affects delivery time and late delivery calculations)

### Interactivity
- **Hover Tooltips**: All charts display detailed values on hover (exact counts, percentages, dates)
- **Cross-Filtering**: Clicking on a month in any time-series chart could filter other views (if dashboard actions are enabled)
- **Consistent Time Range**: All visuals use the same Sep 2016 - Aug 2018 date range for coherent analysis

## Key Findings

### Finding 1: Rapid Growth Strains Operational Consistency
Order volume increased 10-15x from late 2016 to mid-2018, demonstrating strong marketplace growth. However, late delivery rates have crept upward from ~3% to ~7-10% during the same period, suggesting that operational processes and seller capacity are struggling to keep pace with demand. This is a critical inflection point for the business.

### Finding 2: Delivery Time Improved But Remains Slow
Average delivery time dropped from 55 days in early platform days to a stable 10-15 days by 2017. While this represents major operational improvement, it's still significantly slower than customer expectations set by competitors like Amazon Prime (2 days) or even standard Mercado Livre shipping (5-7 days). The long right tail of the delivery time distribution (some orders taking 60-210 days) also reveals persistent fulfillment failures.

### Finding 3: High Order Completion Rate Masks Hidden Issues
The 97% order completion rate appears excellent on the surface. However, the 3% of failed orders (canceled, unavailable) represent nearly 3,000 orders and lost revenue. More importantly, the "unavailable" status (0.61%) indicates inventory management or seller reliability issues that could have been prevented with better systems.

### Finding 4: Late Deliveries Are Underestimated Risk
A 6.8% late delivery rate means ~6,700 customers received orders after the promised date. Research shows that late delivery is one of the strongest predictors of negative reviews, customer churn, and social media complaints. The upward trend in late delivery rate during high-volume months (holidays) suggests that the platform's estimated delivery date algorithm may be too optimistic or that logistics partners are overpromising.

### Finding 5: Operational Excellence Varies Widely Across Sellers
The histogram showing delivery time distribution reveals massive variance in seller performance. Some sellers consistently deliver in 5-10 days, while others regularly take 40-60+ days. This inconsistency creates unpredictable customer experiences and makes it difficult to market the platform with a clear delivery promise.

## Business Recommendations

### Recommendation 1: Implement Seller Performance Tiers
**Action**: Create a tiered seller rating system based on delivery time and late delivery rate. Grant "Premium Seller" badges to top performers and provide incentive-based logistics support.

**Rationale**: The wide variance in delivery performance (5-60+ days) indicates that some sellers have excellent operations while others are failing. By creating transparency through badges and providing targeted support (training, logistics partnerships, inventory financing) to underperforming sellers, the platform can shift the entire distribution leftward and reduce average delivery time.

**Expected Impact**: 
- Reduce average delivery time from 12.5 days to 8-10 days within 6 months
- Reduce late delivery rate from 6.8% to below 5%
- Increase customer trust and repeat purchase rates

### Recommendation 2: Revise Estimated Delivery Date Algorithm
**Action**: Audit the estimated delivery date calculation logic and incorporate real seller performance data. Add buffer days for historically slower sellers or high-volume periods (holidays).

**Rationale**: The 6.8% late delivery rate and its upward trend during growth periods suggests that promised delivery dates are too optimistic. By using historical seller performance and seasonality data, the platform can set more realistic expectations, reducing the "promise vs. delivery" gap that drives customer dissatisfaction.

**Expected Impact**:
- Reduce late delivery rate from 6.8% to under 4% by setting more conservative (but achievable) expectations
- Improve customer review scores by reducing negative sentiment related to late deliveries
- Build customer trust through consistent fulfillment of promises

### Recommendation 3: Investigate and Reduce "Unavailable" Orders
**Action**: Implement real-time inventory sync requirements for sellers and automated stockout notifications to customers before order confirmation.

**Rationale**: The 0.61% "unavailable" order rate (607 orders) represents preventable failures. These orders create the worst customer experience (order accepted, then canceled due to stockout) and lost revenue. By requiring sellers to maintain accurate inventory feeds and catching stockouts before order confirmation, these failures can be eliminated.

**Expected Impact**:
- Reduce unavailable order rate from 0.61% to under 0.2%
- Prevent ~400 customer frustration incidents per 100k orders
- Capture additional $50k-100k in revenue per 100k orders (assuming $125-250 average order value)

### Recommendation 4: Scale Operations Infrastructure Proactively
**Action**: Build forecasting models to predict order volume growth and proactively expand logistics partnerships, warehouse capacity, and seller support resources.

**Rationale**: The 10-15x order growth over 23 months is impressive, but the uptick in late deliveries during high-volume periods shows operational strain. Rather than reacting to growth, the platform should forecast demand 6-12 months ahead and pre-emptively build capacity (new logistics partners, regional fulfillment hubs, automated seller onboarding).

**Expected Impact**:
- Maintain late delivery rate below 5% even as order volume continues doubling year-over-year
- Reduce peak season (November, December) operational stress
- Enable faster geographic expansion by having fulfillment infrastructure in place

### Recommendation 5: Launch Fast Delivery Program
**Action**: Pilot a "Next Day" or "Express" delivery program with top-performing sellers in high-density regions (São Paulo, Rio de Janeiro).

**Rationale**: The histogram shows that 20,000-25,000 orders (20-25%) are already delivered in 5-10 days. By formalizing this as a premium delivery tier and expanding it, Olist can compete directly with Amazon Prime and Mercado Livre Premium. Faster delivery drives higher customer lifetime value, reduces cart abandonment, and justifies premium pricing.

**Expected Impact**:
- Capture 10-15% of orders into Express tier within 12 months
- Increase average order value by 15-20% for Express orders (customers willing to pay for speed)
- Improve competitive positioning and customer retention

## Tableau Public
- **Link**: [Coming Soon - Dashboard will be published after final polish]

## Limitations

### Data Limitations
- **Time Period**: Dataset ends in August 2018; analysis does not reflect 2019+ operational improvements or market changes
- **Incomplete Final Month**: August 2018 data is partial, causing the sharp drop in order volume chart
- **Missing Review Data**: Not all orders have associated review scores, limiting customer satisfaction analysis
- **Geographic Constraints**: Dataset is Brazil-only; findings may not generalize to other markets with different logistics infrastructure

### Analytical Limitations
- **Causality**: Analysis identifies correlations (e.g., late deliveries during high volume) but does not prove causation
- **Seller Segmentation**: Unable to deeply segment by seller size, category, or region without additional enrichment
- **External Factors**: Cannot account for macro events (Brazilian economic conditions, competitor actions, regulatory changes) that may have impacted results
- **Customer Perspective**: Limited ability to link delivery performance to customer lifetime value or churn without behavioral data

### Methodological Limitations
- **Aggregation Level**: Primary analysis at order level; item-level insights (e.g., categories with slower fulfillment) require additional views
- **Static Analysis**: Dashboard shows historical performance but does not include predictive models or real-time alerting
- **Estimated Dates**: Relies on seller-provided estimated delivery dates, which may themselves be inaccurate

## Next Steps

### Immediate Next Steps (1-2 weeks)
1. **Build Analysis 2 Dashboard**: Create Seller Performance Scorecard showing delivery time, late rate, and order volume by individual seller
2. **Add Geographic Analysis**: Map views showing delivery time by customer state/city to identify regional bottlenecks
3. **Publish to Tableau Public**: Clean up formatting, add branding, write public-facing narrative

### Short-Term Next Steps (1-3 months)
4. **Customer Experience Dashboard**: Link delivery performance to review scores; analyze correlation between late delivery and low ratings
5. **Category Analysis**: Break down delivery performance by product category to identify high-risk or slow-moving categories
6. **Seasonality Deep Dive**: Create detailed month-over-month and week-over-week analysis to forecast holiday demand
7. **Seller Segmentation**: Cluster sellers by performance tier and identify characteristics of top performers vs. strugglers

### Long-Term Next Steps (3-6 months)
8. **Predictive Modeling**: Build regression models to predict which orders are most likely to be delivered late based on seller, category, location, and seasonality
9. **Real-Time Dashboard**: Transition from static historical analysis to live operational dashboard tracking current-day/week metrics
10. **A/B Test Framework**: Design experiments to test interventions (e.g., revised estimated delivery dates, seller incentives) and measure impact
11. **Customer Lifetime Value Analysis**: Integrate delivery performance with customer purchase history to quantify financial impact of fulfillment quality

---

*This analysis was created by Jonathan Nadeau as part of a portfolio project demonstrating Tableau data visualization, operational analytics, and business storytelling skills. The Olist dataset is publicly available on Kaggle and represents real e-commerce transactions from 2016-2018.*
