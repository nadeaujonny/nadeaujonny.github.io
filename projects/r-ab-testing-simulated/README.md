# A/B Testing in R (Simulated SaaS Onboarding)

## Overview
End-to-end experimentation workflow in R for a simulated control vs. treatment onboarding test. The project covers experiment QA (SRM + baseline checks), primary KPI inference, guardrails, robustness checks (bootstrap/permutation/regression-adjusted), and power/MDE planning.

## Repository Structure
```text
projects/r-ab-testing-simulated/
├── R/
├── data/
├── tables/
├── figures/
└── reports/
```

## Run End-to-End
From `projects/r-ab-testing-simulated/`:

```r
source("requirements.R")
source("R/00_generate_data.R")
source("R/01_qc_srm.R")
source("R/02_primary_metric.R")
source("R/03_secondary_guardrails.R")
source("R/04_bootstrap_permutation.R")
source("R/05_regression_adjusted.R")
source("R/06_power_mde.R")
```

## Script Guide (00–06)
- `00_generate_data.R`: Simulates user-level experiment data and writes `data/ab_test_data.csv`.
- `01_qc_srm.R`: Runs integrity checks (assignment split + baseline covariate balance) and flags SRM issues.
- `02_primary_metric.R`: Computes conversion lift, confidence intervals, and hypothesis-test results for the primary KPI.
- `03_secondary_guardrails.R`: Evaluates the guardrail metric (`time_to_complete`) with parametric and non-parametric tests.
- `04_bootstrap_permutation.R`: Adds bootstrap confidence intervals and permutation tests for conversion lift robustness.
- `05_regression_adjusted.R`: Estimates regression-adjusted treatment effects (conversion + guardrail) with robust standard errors.
- `06_power_mde.R`: Produces MDE and sample-size planning outputs for future test design.

## Outputs Generated
Typical artifacts are written to `tables/` and `figures/`.

- **Tables (examples):**
  - `tables/qc_srm_test.csv`
  - `tables/primary_metric_results.csv`
  - `tables/guardrail_time_results.csv`
  - `tables/bootstrap_perm_summary.csv`
  - `tables/reg_conv_adjusted_effect_*.csv`
  - `tables/power_mde_summary_*.csv`
- **Figures (examples):**
  - `figures/guardrail_time_to_complete.png`
  - `figures/bootstrap_abs_lift.png`

## Dependencies
Install/load required R packages with:

```r
source("requirements.R")
```

Key packages: `tidyverse`, `broom`, `janitor`, `infer`, `gt`, `patchwork`, `effectsize`.

## Decision Summary
Final recommendation: **ship treatment with a staged ramp and monitoring gates**.

Evidence from generated tables:
- Primary KPI improved: control conversion **10.19%** vs treatment **11.52%**, absolute lift **+1.33 pp** (95% CI **+0.11 to +2.55 pp**), p = **0.0320** (`tables/primary_metric_summary.csv`, `tables/primary_metric_results.csv`).
- Guardrail also improved: `time_to_complete` difference (treatment - control) **-0.341** with bootstrap 95% CI **-0.460 to -0.223**, strong p-values (`tables/guardrail_time_results.csv`).
- Integrity checks passed: SRM p-value **0.7339** (`tables/qc_srm_test.csv`).
- Current design context: estimated 80% power MDE is **1.77 pp** at ~4,983 users/group (`tables/power_mde_summary_20260213_124611.csv`).
