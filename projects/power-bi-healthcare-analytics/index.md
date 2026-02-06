---
layout: default
title: Healthcare Analytics Dashboard (Power BI)
description: "A comprehensive Power BI healthcare analytics dashboard showcasing advanced DAX, Power Query, data modeling, and executive-level insights."
breadcrumbs:
  - title: Projects
    url: /projects/
  - title: Healthcare Analytics Dashboard (Power BI)
---

<a href="/projects/" class="back-to-projects btn">← Back to Projects</a>

# Healthcare Analytics Dashboard (Power BI)

> This project demonstrates advanced Power BI proficiency through comprehensive analysis of public health data, focusing on healthcare outcomes, population health trends, and resource allocation insights.

---

## Project Overview

This portfolio project is designed to highlight end-to-end Power BI capabilities: data ingestion, Power Query transformations, data modeling, advanced DAX measures, and interactive dashboards for healthcare stakeholders.

## Dataset Information

**Source (public health databases):**
- CDC, WHO, or U.S. Department of Health & Human Services public health databases

**Primary Sources:**
- data.gov (healthcare datasets)
- healthdata.gov
- CDC Wonder database
- data.cms.gov (Medicare/Medicaid data)

**Potential datasets:**
- Hospital readmission rates
- Chronic disease prevalence by demographics
- Vaccination coverage rates
- Healthcare quality metrics
- Patient outcome indicators

**Data volume:** 50,000+ records across multiple related tables

**Time period:** Multi-year trend analysis (2018–2023 recommended)

## Project Objectives

- Demonstrate Power BI technical proficiency (DAX, Power Query M, data modeling, advanced visualization)
- Deliver healthcare business intelligence on outcomes, disparities, and resource optimization
- Show domain versatility beyond e-commerce/retail analytics
- Prove multi-source data integration skills and complex relationships handling

---

## Analysis Structure

### Analysis 1 — Population Health Overview Dashboard

**Focus:** High-level health metrics and population trends

**KPIs:**
- Total population covered
- Overall health outcome score
- Year-over-year health improvement rate
- Healthcare access rate
- Primary health indicators (life expectancy, disease prevalence)

**Visualizations:**
- KPI cards with sparklines
- Geographic heat map (state/region)
- Line chart: health metrics over time
- Bar chart: top 10 states by health outcomes
- Donut chart: population distribution by risk category

**Power BI features:**
- DAX time intelligence (YoY, MoM)
- Conditional KPI formatting
- Custom tooltips
- Bookmarks for view states
- Drill-through to regional details

### Analysis 2 — Healthcare Disparities & Demographics

**Focus:** Health equity across demographic groups

**Key metrics:**
- Disparity index by demographic group
- Access gap percentage
- Outcome variance across populations
- Social determinants impact score

**Visualizations:**
- Clustered bars: outcomes by age, ethnicity, income
- Scatter plot: social determinants vs outcomes
- Matrix with conditional formatting
- Small multiples across demographic segments
- Waterfall chart: disparity contributing factors

**Power BI features:**
- Row-level security (demonstration)
- CALCULATE/FILTER DAX measures
- Accessibility-aware color palettes
- Field parameters for dynamic metrics
- What-if parameters

### Analysis 3 — Resource Utilization & Efficiency

**Focus:** Facility performance and resource allocation

**Key metrics:**
- Average length of stay (ALOS)
- Readmission rate
- Cost per patient
- Bed utilization rate
- Patient satisfaction scores

**Visualizations:**
- Cost vs quality performance quadrant
- Gauge charts vs benchmarks
- Area chart: utilization over time
- Treemap: spending by department
- Top/Bottom N facility performance

**Power BI features:**
- Advanced DAX (RANKX, TOPN, SUMX)
- Decomposition tree
- Q&A visual
- Key influencers visual
- Mobile-optimized layout

### Analysis 4 — Disease/Condition Deep Dive

**Focus:** Targeted condition analysis (e.g., diabetes, heart disease)

**Key metrics:**
- Prevalence rate
- Incidence rate (new cases)
- Mortality rate
- Treatment adherence percentage
- Complication rate

**Visualizations:**
- Ribbon chart: prevalence trends by demographic
- Funnel chart: patient care journey
- Line/clustered column combo: cases vs mortality
- Slicer panel: condition, region, demographic
- Custom visuals: timeline slider, image navigation

**Power BI features:**
- Power Query advanced transformations (unpivot, merge)
- Calculated columns vs measures
- Date table with fiscal calendar
- Hierarchies for drill-down
- Cross-filter direction management

### Analysis 5 — Executive Summary Dashboard

**Focus:** C-suite level overview and navigation

**Components:**
- Critical KPIs from all analysis areas
- Executive summary cards
- Trend indicators with directional arrows
- Alert banners for out-of-threshold metrics
- Navigation buttons to detailed dashboards

**Power BI features:**
- Page navigation actions
- Button visuals with conditional formatting
- Dashboard templates and themes
- Performance optimization techniques
- Publishing to Power BI Service (if available)
- Scheduled refresh setup demonstration

---

## Technical Implementation Checklist

### Data Preparation (Power Query)
- Connect to multiple data sources
- Clean and transform data (nulls, duplicates)
- Create custom columns using M language
- Merge/append queries
- Establish proper data types
- Create date dimension table
- Implement data validation checks
- Document transformation steps

### Data Modeling
- Build a star schema (fact + dimension tables)
- Establish relationships (one-to-many, many-to-many)
- Set proper cardinality and cross-filter directions
- Create hierarchies (geographic, date, demographic)
- Hide unnecessary fields from report view
- Organize tables into display folders
- Validate model using DAX Studio (optional)

### DAX Measures & Calculations
- Basic aggregations (SUM, AVERAGE, COUNT)
- Time intelligence (YoY, YTD, QoQ)
- CALCULATE with multiple filters
- Iterator functions (SUMX, AVERAGEX)
- Ranking (RANKX, TOPN)
- Statistical measures (STDEV, MEDIAN)
- Conditional logic (IF, SWITCH, HASONEVALUE)
- Variables for optimization
- Measure documentation with comments

### Visualizations & Design
- Consistent color scheme and branding
- Accessible color choices (colorblind-friendly)
- Proper chart type selection
- Clear titles and labels
- Legend positioning and formatting
- Data labels when appropriate
- Appropriate use of white space
- Mobile layout for each page

### Interactivity & User Experience
- Slicers with appropriate selection modes
- Cross-filtering between visuals
- Drill-through pages
- Tooltips (default and custom)
- Bookmarks for saved views
- Buttons for navigation
- Sync slicers across pages
- Clear visual hierarchy

---

## Key Business Insights to Highlight

- Health outcome trends by region and demographic segment
- Disparity analysis with targeted intervention recommendations
- Resource optimization across facilities and departments
- Cost-effectiveness comparison for programs and providers
- Risk stratification for preventive care prioritization
- Policy recommendations grounded in data-driven evidence

## Project Deliverables

**Power BI Desktop File (.pbix)**
- Complete data model
- All dashboards and reports
- Documented DAX measures

**Portfolio Web Page**
- Project overview and business context
- Key insights and recommendations
- Dashboard screenshots with annotations
- Technical approach explanation
- Embedded Power BI report (if published) or high-quality images
- Tools and techniques used section

**Supporting Documentation**
- Data dictionary
- DAX measure documentation
- Data source citations
- Methodology notes
- Business recommendations summary

## Skills Demonstrated

**Technical skills:**
- Power Query M language for ETL
- Advanced DAX (time intelligence, iterators, context transition)
- Data modeling (star schema, relationships)
- Power BI Service publishing and sharing
- Mobile layout design
- Performance optimization

**Business skills:**
- Healthcare domain knowledge
- Population health analytics
- Health equity analysis
- Resource allocation strategy
- Executive-level communication
- Policy recommendation formulation

**Data skills:**
- Multi-source data integration
- Data quality assurance
- Statistical analysis
- Trend identification
- Comparative analysis

## Differentiation from Other Portfolio Projects

| Aspect | SQL/Excel/Tableau Projects | Power BI Project |
| --- | --- | --- |
| Domain | E-commerce, Retail | Healthcare, Public Health |
| Data Type | Transactional, Sales | Population health, Clinical outcomes |
| Analysis Focus | Business performance | Health equity, Outcomes, Policy |
| Tool Strength | Querying, Dashboards, Visualization | DAX, Data modeling, Self-service BI |
| Audience | Business stakeholders | Healthcare administrators, Policy makers |

## Timeline & Milestones

- **Week 1:** Data acquisition, cleaning, and initial Power Query setup
- **Week 2:** Data modeling and DAX measure creation
- **Week 3:** Dashboard design and visualization development
- **Week 4:** Insights documentation, web page creation, final refinements

## Success Criteria

- Dashboard loads in under 3 seconds
- At least 15 custom DAX measures demonstrating various functions
- Five distinct dashboard pages with clear purposes
- Mobile-optimized layouts for all pages
- 3–5 key business recommendations based on data
- Professional, accessible design following best practices
- Clear documentation of all technical choices

## Notes for Portfolio Presentation

When presenting this project to potential employers, emphasize:
- Domain versatility in a regulated healthcare context
- Technical depth in DAX and data modeling
- Business value tied to actionable recommendations
- Self-service BI enablement for stakeholders
- Scalability through performance optimization

---

## Project Assets (to be added)

- Power BI report screenshots: `images/`
- Source datasets and data dictionary: `data/`
- Power BI workbook: `workbook/`
