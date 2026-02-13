---
layout: default
title: "A/B Testing & Experimentation in R"
description: "Decision-oriented experimentation case study for a simulated SaaS onboarding A/B test, including QA checks, causal estimation, robustness testing, and power planning."
---

<a href="/projects/" class="back-to-projects btn">&larr; Back to Projects</a>

# A/B Testing &amp; Experimentation in R
## Simulated SaaS Onboarding Experiment

## Executive Summary
This experiment evaluates whether a redesigned onboarding flow should be shipped to all new users. In a balanced 50/50 randomized test with 10,000 users, treatment increased conversion from **10.19%** to **11.52%** (**+1.33 percentage points**, **+13.10% relative lift**, p = 0.032). The guardrail metric (time to complete onboarding) also improved by **-0.34** units in treatment (p &lt; 1e-7), indicating no speed/UX tradeoff. Classical, bootstrap, permutation, and regression-adjusted analyses are directionally consistent, supporting a **ship recommendation with a staged rollout**.

## Objectives
- Estimate the causal impact of onboarding treatment on conversion (primary KPI).
- Ensure experiment validity via SRM and baseline balance checks.
- Verify no adverse guardrail impact on onboarding completion time.
- Test robustness using classical inference, bootstrap, permutation, and regression adjustment.
- Translate findings into an implementation decision and future test plan.

## Experiment Design
- **Design:** Two-arm randomized controlled experiment (control vs treatment).
- **Randomization unit:** User (`user_id`).
- **Allocation target:** 50% control / 50% treatment.
- **Observed sample size:** 10,000 users total (5,017 control; 4,983 treatment).
- **Duration assumption:** Single test window over one onboarding cycle (simulated).
- **Primary metric:** `converted` (binary), reported as conversion rate.
- **Guardrail metric:** `time_to_complete` (continuous), lower is better.
- **Pre-treatment covariate for adjustment:** `pre_sessions_7d`.

### Metric Definitions
- **Absolute lift (pp):** \( p_{treat} - p_{control} \), reported in percentage points.
- **Relative lift:** \( (p_{treat} - p_{control}) / p_{control} \).
- **Decision threshold:** Two-sided α = 0.05 for primary confirmatory inference.

## Data Generation &amp; Dataset Fields
The dataset is generated via script and persisted to `data/ab_test_data.csv`.

| Column | Type | Description |
|---|---|---|
| `user_id` | integer | Unique user identifier |
| `variant` | categorical | Assigned arm (`control`, `treatment`) |
| `pre_sessions_7d` | integer | Prior 7-day activity proxy (pre-treatment covariate) |
| `converted` | binary (0/1) | Primary outcome: conversion indicator |
| `time_to_complete` | numeric | Guardrail: onboarding completion time |

## Methods &amp; Validation Checks
- **SRM (Sample Ratio Mismatch):** Chi-square test on assignment counts to confirm randomization integrity.
- **Covariate balance:** Welch two-sample test on pre-experiment activity (`pre_sessions_7d`).
- **Primary metric inference:** Two-proportion test with confidence interval on lift.
- **Guardrail inference:** Mean difference with bootstrap CI + t-test and Wilcoxon test.
- **Bootstrap robustness:** Resampling for empirical lift distribution and interval stability.
- **Permutation robustness:** Label-shuffling test for non-parametric p-values.
- **Regression adjustment:** Model-based adjustment (logit for conversion, OLS for time) using pre-period covariate.
- **Power / MDE planning:** Post-analysis sensitivity based on baseline conversion and observed n.

## Results

### 1) Experiment Integrity (SRM + Baseline Balance)
- Allocation was effectively balanced: 50.17% control vs 49.83% treatment.
- SRM test was non-significant (χ² = 0.1156, p = 0.7339), supporting assignment integrity.
- Baseline covariate balance was acceptable (difference = 0.0453, p = 0.1876).

**Key artifacts:**
- [SRM group counts](./tables/qc_srm_group_counts.csv)
- [SRM test](./tables/qc_srm_test.csv)
- [Baseline balance test](./tables/qc_baseline_balance_test.csv)

### 2) Primary KPI: Conversion
- Control conversion: **10.19%** (511 / 5,017).
- Treatment conversion: **11.52%** (574 / 4,983).
- **Absolute lift:** **+1.33 pp** (95% CI: +0.11 to +2.55 pp).
- **Relative lift:** **+13.10%**.
- Statistical significance: p = 0.0320.

<table>
  <thead>
    <tr>
      <th>Metric</th>
      <th>Control</th>
      <th>Treatment</th>
      <th>Lift</th>
      <th>95% CI</th>
      <th>p-value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Conversion rate</td>
      <td>10.19%</td>
      <td>11.52%</td>
      <td>+1.33 pp (+13.10%)</td>
      <td>[+0.11, +2.55] pp</td>
      <td>0.0320</td>
    </tr>
  </tbody>
</table>

**Key artifacts:**
- [Primary metric summary](./tables/primary_metric_summary.csv)
- [Primary metric test results](./tables/primary_metric_results.csv)

### 3) Guardrail: Onboarding Completion Time
- Mean control: **7.873**
- Mean treatment: **7.532**
- Difference (treat - control): **-0.341** (bootstrap 95% CI: -0.460 to -0.223)
- Parametric and non-parametric tests agree (t-test p ≈ 1.39e-08; Wilcoxon p ≈ 1.32e-08).

<div style="text-align:center; margin: 16px 0;">
  <img src="./figures/guardrail_time_to_complete.png" alt="Distribution of time to complete by experiment variant" style="max-width: 900px; width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;" />
  <p><em>Figure 1. Guardrail outcome by variant: treatment users complete onboarding faster on average.</em></p>
</div>

**Key artifacts:**
- [Guardrail summary & tests](./tables/guardrail_time_results.csv)
- [Detailed guardrail tests](./tables/guardrail_time_tests.csv)

### 4) Robustness: Bootstrap, Permutation, Regression Adjustment
- **Bootstrap:** Lift distribution centered above zero, consistent with classical estimate.
- **Permutation tests:** Two-sided p-values 0.036 (manual) and 0.033 (`infer`), reinforcing significance.
- **Regression-adjusted conversion effect:** +1.334 pp (95% CI: +0.249 to +2.566 pp).
- **Regression-adjusted guardrail effect:** -0.341 (95% CI: -0.459 to -0.224; p ≈ 1.31e-08).

<div style="text-align:center; margin: 16px 0;">
  <img src="./figures/bootstrap_abs_lift.png" alt="Bootstrap distribution of conversion absolute lift" style="max-width: 900px; width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;" />
  <p><em>Figure 2. Bootstrap distribution of absolute conversion lift (treatment minus control), with mass concentrated above zero.</em></p>
</div>

**Key artifacts:**
- [Bootstrap summary](./tables/bootstrap_perm_summary.csv)
- [Bootstrap + classical proportion test output](./tables/bootstrap_perm_prop_test.csv)
- [Permutation test (manual)](./tables/permutation_results.csv)
- [Permutation test (`infer`)](./tables/infer_permutation_results.csv)
- [Regression-adjusted conversion effect](./tables/reg_conv_adjusted_effect_20260213_123853.csv)
- [Regression-adjusted guardrail effect](./tables/reg_time_adjusted_effect_20260213_123853.csv)

### 5) Power &amp; MDE Context
At the current sample size (~4,983 per arm), the estimated detectable effect at 80% power is about **1.77 pp**. The observed effect (**1.33 pp**) is below that planning threshold, but still reached significance in this realized sample. For future tests targeting smaller lifts, larger samples are required.

Example planning outputs:
- 1.0 pp target lift requires ~14,981 users per group.
- 1.5 pp target lift requires ~6,794 users per group.
- 2.0 pp target lift requires ~3,898 users per group.

**Key artifacts:**
- [Power/MDE summary](./tables/power_mde_summary_20260213_124611.csv)
- [Sample size requirements](./tables/power_sample_size_requirements_20260213_124611.csv)
- [Power curve data](./tables/power_curve_20260213_124611.csv)

## Interpretation &amp; Business Recommendation
**Recommendation: Ship with a staged ramp (e.g., 25% → 50% → 100%) and monitoring gates.**

Why:
- The treatment improves the primary KPI with statistically and practically meaningful lift (+1.33 pp; +13.10% relative).
- The guardrail moves in the favorable direction (faster completion), reducing rollout risk.
- Robustness checks agree across classical, bootstrap, permutation, and regression-adjusted estimators.

Operationally, this supports rollout, with ongoing monitoring for post-launch drift and segment-level effects.

## Limitations &amp; Next Steps
- **Simulation context:** Results are from synthetic data; production rollout should revalidate with live traffic.
- **Heterogeneity:** Analyze lift by user segments (new vs returning, activity cohorts, acquisition channel).
- **Multiple testing discipline:** Pre-register confirmatory metrics; control false discovery for exploratory cuts.
- **Sequential monitoring:** Use explicit alpha-spending or Bayesian monitoring if peeking during ramp.
- **Long-run impact:** Add retention/revenue follow-up windows to confirm durable gains.

## Reproducibility
### Run Order
From the project directory (`projects/r-ab-testing-simulated/`):

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

### Artifacts &amp; References
- [Project README](./README.md)
- [R package requirements](./requirements.R)
- [R scripts folder](./R/)
- [Tables output folder](./tables/)
- [Figures output folder](./figures/)

---

**Last Updated:** 2026-02-13
