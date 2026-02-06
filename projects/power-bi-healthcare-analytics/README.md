# Power BI Healthcare Analytics Dashboard
## CDC Chronic Disease Indicators Analysis

### Project Overview
This project demonstrates advanced Power BI capabilities through analysis of the CDC's U.S. Chronic Disease Indicators (CDI) dataset. The analysis identifies high-burden states, tracks health trends, quantifies demographic disparities, and provides data-driven recommendations for public health interventions.

### Business Context
Healthcare policymakers need to allocate limited resources effectively across states and programs. This dashboard enables evidence-based decision-making by answering:
- Which states have the highest chronic disease burden?
- Which health indicators are improving vs. worsening?
- Where are demographic disparities largest?
- How should we prioritize prevention programs?

### Dataset
- **Source**: CDC Open Data — U.S. Chronic Disease Indicators
- **Records**: 500,000+ measurements across years, states, and demographics
- **Scope**: 6 core indicators (obesity, smoking, inactivity, diabetes, heart disease, hypertension)
- **Time Period**: 2011–2023
- **Geography**: 50 US states + DC

### Technical Implementation

#### Data Model
- **Architecture**: Star schema with 1 fact table and 4 dimension tables
- **Fact Table**: Fact_CDI (year, location, indicator, stratification → data value)
- **Dimensions**: Date, Location, Indicator, Stratification

#### Power Query ETL
- Imported and cleaned 500K+ row CSV
- Created dimension tables via duplicate query method
- Applied scope filters (indicators, years, geography)
- Standardized data types and handled nulls

#### DAX Measures (20+ measures)
- Core aggregations and context-aware calculations
- Time intelligence (YoY change, trend direction)
- Ranking functions (state rankings via RANKX)
- Disparity calculations (gaps and ratios)
- Composite burden index and priority scoring

#### Dashboard Features
- 5 interactive report pages
- Drill-through capabilities
- Custom tooltips
- Bookmarks and navigation
- Conditional formatting
- Mobile-optimized layouts

### Key Insights
1. Obesity rates increased 15% nationally from 2011–2023
2. Southern states show consistently higher burden across multiple indicators
3. Significant racial/ethnic disparities in diabetes and obesity
4. 12 states identified as high priority (high burden + worsening trends)
5. Risk factors (obesity, smoking, inactivity) drive 70%+ of health outcomes

### Business Recommendations
1. Deploy targeted prevention programs in 12 priority states
2. Expand screening initiatives in high-disparity communities
3. Focus on obesity reduction as primary prevention lever
4. Create peer learning networks between similar states
5. Shift healthcare investment from treatment to prevention

### Skills Demonstrated
- Power Query ETL and data transformation
- Star schema dimensional modeling
- Advanced DAX (time intelligence, ranking, composite measures)
- Interactive dashboard design
- Drill-through and navigation features
- Business intelligence storytelling
- Healthcare domain analysis

### Project Structure
```
power-bi-healthcare-analytics/
├── index.md                    # Project webpage
├── README.md                   # This file
├── images/                     # Dashboard screenshots
│   ├── model-star-schema.png
│   ├── power-query-steps.png
│   ├── dashboard-01-overview.png
│   ├── dashboard-02-trends.png
│   ├── dashboard-03-state-drill.png
│   ├── dashboard-04-disparities.png
│   └── dashboard-05-recommendations.png
├── data/                       # Raw/processed datasets
└── workbook/                   # Power BI Desktop file (.pbix)
```

### How to View
Visit the project webpage: [https://nadeaujonny.github.io/projects/power-bi-healthcare-analytics/](https://nadeaujonny.github.io/projects/power-bi-healthcare-analytics/)

### Contact
Jonathan Nadeau
[nadeau.jonny@gmail.com](mailto:nadeau.jonny@gmail.com)
[LinkedIn](https://linkedin.com/in/jonathan-nadeau) | [GitHub](https://github.com/nadeaujonny)
