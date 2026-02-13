---
layout: default
title: "A/B Testing & Experimentation in R"
description: "Statistical analysis of a simulated SaaS onboarding experiment using R, demonstrating A/B testing methodology, power analysis, and regression adjustment techniques."
---

# A/B Testing & Experimentation in R
## Simulated SaaS Onboarding Experiment

## Overview

This portfolio project demonstrates a comprehensive A/B testing analysis workflow using R. The project analyzes a simulated SaaS onboarding experiment where we test different onboarding flows to improve user conversion and revenue. Through this analysis, we cover statistical testing, power analysis, regression adjustment, heterogeneous treatment effects, and rigorous quality assurance checks including Sample Ratio Mismatch (SRM) detection and covariate balance verification.

## Key Features

- **Simulated Experimental Dataset**: Generated entirely from code with configurable parameters
- **Quality Assurance**: SRM detection and covariate balance verification
- **Statistical Testing**: Multiple approaches including bootstrap and permutation tests
- **Regression Adjustment**: CUPED methodology for variance reduction
- **Power Analysis**: MDE calculations and sample size planning
- **Comprehensive Reporting**: RMarkdown-based analysis report

## Analysis Components

1. **Quality Checks & SRM Detection** - Validates experimental integrity
2. **Primary Metric Analysis** - Conversion rate testing and inference
3. **Secondary Metrics & Guardrails** - Revenue and engagement metrics
4. **Bootstrap & Permutation Tests** - Non-parametric inference methods
5. **Regression-Adjusted Estimates** - CUPED variance reduction
6. **Power Analysis** - MDE calculations and future experiment planning

## Project Structure

```
r-ab-testing-simulated/
├── data/
│   ├── raw/              # Raw simulated experimental data
│   └── processed/        # Cleaned/transformed datasets
├── R/                    # Analysis scripts (run in numerical order)
│   ├── 00_generate_data.R
│   ├── 01_qc_srm.R
│   ├── 02_primary_metric.R
│   ├── 03_secondary_guardrails.R
│   ├── 04_bootstrap_permutation.R
│   ├── 05_regression_adjusted.R
│   └── 06_power_mde.R
├── reports/              # RMarkdown reports and rendered HTML
│   └── ab_test_report.Rmd
├── figures/              # Saved plots and visualizations
├── tables/               # Saved tables and summary statistics
├── README.md
├── requirements.R
└── .gitignore
```

## Technologies Used

- **R**: Statistical computing and analysis
- **tidyverse**: Data manipulation and visualization
- **infer**: Statistical inference framework
- **broom**: Tidy statistical model outputs
- **patchwork**: Combining multiple plots
- **gt**: Creating presentation-ready tables
- **lmtest & sandwich**: Robust statistical testing
- **pwr**: Power analysis calculations
- **ggeffects**: Visualizing model predictions
- **RMarkdown**: Reproducible reporting

## How to Run

1. **Set up the environment**
   ```r
   source("requirements.R")  # Install and load all required packages
   ```

2. **Generate the simulated dataset**
   ```r
   source("R/00_generate_data.R")
   ```

3. **Run analysis scripts in order**
   ```r
   source("R/01_qc_srm.R")
   source("R/02_primary_metric.R")
   source("R/03_secondary_guardrails.R")
   source("R/04_bootstrap_permutation.R")
   source("R/05_regression_adjusted.R")
   source("R/06_power_mde.R")
   ```

4. **Generate the final report**
   - Open `reports/ab_test_report.Rmd` in RStudio
   - Knit to HTML to generate the comprehensive analysis report

## Reproducibility

This project uses a **simulated dataset** generated entirely from code. The data is not based on real user data. All results are fully reproducible by running the scripts in order with the same random seed.

## Repository

View the complete code and analysis on [GitHub](https://github.com/nadeaujonny/nadeaujonny.github.io/tree/main/projects/r-ab-testing-simulated).

---

**Last Updated:** 2026-02-13
