---
layout: default
title: "R Project: A/B Testing & Experimentation (Simulated SaaS Onboarding)"
permalink: /projects/r-ab-testing-simulated/
---

# R Project: A/B Testing & Experimentation (Simulated SaaS Onboarding)

**Goal:** Assess whether a redesigned onboarding flow improves trial-to-paid conversion while maintaining guardrail metrics (time-to-complete and early churn risk). This project demonstrates an end-to-end experimentation workflow from design through business recommendation.

<details class="dropdown-section">
  <summary><strong>Project Overview</strong></summary>

  <div style="margin-top: 12px;"></div>

  <p>This portfolio project simulates a SaaS onboarding A/B test with treatment/control assignment, conversion outcomes, and operational guardrails.</p>
  <ul>
    <li><strong>Use case:</strong> Product team wants evidence before rolling out a new onboarding experience.</li>
    <li><strong>Decision focus:</strong> Lift in paid conversion versus risk to user experience.</li>
    <li><strong>Deliverable:</strong> Clear go / no-go recommendation grounded in statistical and business impact.</li>
  </ul>
</details>

<details class="dropdown-section">
  <summary><strong>Objectives</strong></summary>

  <div style="margin-top: 12px;"></div>

  <ul>
    <li>Validate experiment setup and randomization quality.</li>
    <li>Estimate treatment lift on primary conversion KPI.</li>
    <li>Check practical significance with confidence intervals and effect size.</li>
    <li>Assess heterogeneity by device, region, and acquisition channel.</li>
    <li>Translate findings into rollout guidance and next test plan.</li>
  </ul>
</details>

<details class="dropdown-section">
  <summary><strong>Dataset</strong></summary>

  <div style="margin-top: 12px;"></div>

  <ul>
    <li><strong>Source:</strong> Simulated SaaS onboarding event dataset.</li>
    <li><strong>Unit of analysis:</strong> User-level trial cohort.</li>
    <li><strong>Core fields:</strong> Variant assignment, conversion flag, device type, region, acquisition channel, onboarding completion time.</li>
    <li><strong>Design:</strong> Parallel A/B split with pre-defined primary metric and guardrails.</li>
  </ul>
</details>

<details class="dropdown-section">
  <summary><strong>Tools &amp; Skills Demonstrated</strong></summary>

  <div style="margin-top: 12px;"></div>

  <ul>
    <li><strong>R:</strong> Data wrangling, statistical testing, regression adjustment, bootstrap/permutation workflows.</li>
    <li><strong>Experimentation:</strong> Hypothesis framing, power planning, SRM and balance checks, multiple-testing awareness.</li>
    <li><strong>Communication:</strong> Business-focused interpretation and action-oriented recommendations.</li>
    <li><strong>Reproducibility:</strong> Scripted pipeline, saved figures/tables, and report-ready outputs.</li>
  </ul>
</details>

<details class="dropdown-section">
  <summary><strong>Methodology (Experiment Design)</strong></summary>

  <div style="margin-top: 12px;"></div>

  <ul>
    <li><strong>Population:</strong> New trial users entering onboarding.</li>
    <li><strong>Randomization:</strong> User-level assignment into control vs treatment.</li>
    <li><strong>Primary KPI:</strong> Trial-to-paid conversion rate.</li>
    <li><strong>Guardrails:</strong> Time-to-complete and early-friction proxy metrics.</li>
    <li><strong>Inference:</strong> Difference-in-proportions, interval estimation, robustness checks, and segment diagnostics.</li>
  </ul>
</details>

<details class="dropdown-section">
  <summary><strong>Analysis 1 — Hypotheses &amp; Primary Metrics</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>Did the new onboarding increase paid conversion versus control, and is the lift meaningful for growth targets?</p>

  <h3>Approach / Method</h3>
  <ul>
    <li>Defined null/alternative hypotheses for conversion lift.</li>
    <li>Calculated baseline and treatment conversion rates.</li>
    <li>Estimated absolute/relative lift with confidence intervals.</li>
  </ul>

  <h3>Key Output (placeholder for screenshot/table/plot)</h3>
  <!-- IMAGE: r-analysis-1-metric-summary.png -->
  ![Placeholder](images/PLACEHOLDER.png)

  <h3>Insights</h3>
  <ul>
    <li>Primary KPI movement indicates directional impact of treatment.</li>
    <li>Confidence interval width informs certainty level for decision-making.</li>
  </ul>

  <h3>Business Recommendation</h3>
  <p>Proceed to decision only after validating randomization quality and confirming guardrails remain acceptable.</p>
</details>

<details class="dropdown-section">
  <summary><strong>Analysis 2 — Randomization / Balance Checks</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>Can we trust that observed lift comes from treatment rather than assignment bias?</p>

  <h3>Approach / Method</h3>
  <ul>
    <li>Ran sample ratio mismatch (SRM) check.</li>
    <li>Compared baseline covariates across variants.</li>
    <li>Flagged any imbalance requiring adjustment or re-run.</li>
  </ul>

  <h3>Key Output (placeholder for screenshot/table/plot)</h3>
  <!-- IMAGE: r-analysis-2-randomization-balance-checks.png -->
  ![Placeholder](images/PLACEHOLDER.png)

  <h3>Insights</h3>
  <ul>
    <li>Balanced groups strengthen causal interpretation.</li>
    <li>Any imbalance informs need for regression-adjusted estimates.</li>
  </ul>

  <h3>Business Recommendation</h3>
  <p>Only treat uplift as credible if SRM and baseline balance are within acceptable thresholds.</p>
</details>

<details class="dropdown-section">
  <summary><strong>Analysis 3 — Power &amp; Sample Size Planning</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>Was the test sufficiently powered to detect a realistic minimum detectable effect (MDE)?</p>

  <h3>Approach / Method</h3>
  <ul>
    <li>Set target alpha, power, and baseline conversion assumptions.</li>
    <li>Computed required sample size across candidate MDE values.</li>
    <li>Benchmarked achieved sample against requirement.</li>
  </ul>

  <h3>Key Output (placeholder for screenshot/table/plot)</h3>
  <!-- IMAGE: r-analysis-3-power-curve-and-sample-size.png -->
  ![Placeholder](images/PLACEHOLDER.png)

  <h3>Insights</h3>
  <ul>
    <li>Power shortfall increases false-negative risk.</li>
    <li>Adequate power supports confident interpretation of null/positive findings.</li>
  </ul>

  <h3>Business Recommendation</h3>
  <p>If underpowered, extend runtime or increase allocation before final rollout decisions.</p>
</details>

<details class="dropdown-section">
  <summary><strong>Analysis 4 — Test Results (Conversion Lift)</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>What is the estimated conversion lift, and does it justify implementation cost and roadmap priority?</p>

  <h3>Approach / Method</h3>
  <ul>
    <li>Ran primary difference-in-proportions test.</li>
    <li>Used bootstrap/permutation inference for robustness.</li>
    <li>Estimated practical impact in expected additional paid users.</li>
  </ul>

  <h3>Key Output (placeholder for screenshot/table/plot)</h3>
  <!-- IMAGE: r-analysis-4-conversion-lift-results.png -->
  ![Placeholder](images/PLACEHOLDER.png)

  <h3>Insights</h3>
  <ul>
    <li>Statistical significance is evaluated alongside business effect size.</li>
    <li>Robustness checks reduce overreliance on a single test assumption.</li>
  </ul>

  <h3>Business Recommendation</h3>
  <p>Roll out if uplift is both statistically credible and operationally material; otherwise iterate on onboarding variants.</p>
</details>

<details class="dropdown-section">
  <summary><strong>Analysis 5 — Segmented Results (Device / Region / Channel)</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>Where does treatment perform best or worst across key user segments?</p>

  <h3>Approach / Method</h3>
  <ul>
    <li>Computed segment-level lift for device, region, and channel.</li>
    <li>Compared consistency of treatment direction and magnitude.</li>
    <li>Flagged segments with potential differential response.</li>
  </ul>

  <h3>Key Output (placeholder for screenshot/table/plot)</h3>
  <!-- IMAGE: r-analysis-5-segmented-lift-device-region-channel.png -->
  ![Placeholder](images/PLACEHOLDER.png)

  <h3>Insights</h3>
  <ul>
    <li>Segment dispersion highlights where onboarding UX may need tailoring.</li>
    <li>Uneven performance can inform phased or targeted rollout strategy.</li>
  </ul>

  <h3>Business Recommendation</h3>
  <p>Adopt targeted enablement for high-response segments first while refining low-response segments.</p>
</details>

<details class="dropdown-section">
  <summary><strong>Sensitivity Checks (Multiple Testing / Assumptions)</strong></summary>

  <div style="margin-top: 12px;"></div>

  <h3>Business Question</h3>
  <p>Do conclusions remain stable after adjusting for multiple comparisons and modeling assumptions?</p>

  <h3>Approach / Method</h3>
  <ul>
    <li>Applied multiple-testing correction where relevant.</li>
    <li>Compared parametric and non-parametric inference outputs.</li>
    <li>Reviewed assumption sensitivity for practical decision stability.</li>
  </ul>

  <h3>Key Output (placeholder for screenshot/table/plot)</h3>
  <!-- IMAGE: r-sensitivity-checks-multiple-testing-assumptions.png -->
  ![Placeholder](images/PLACEHOLDER.png)

  <h3>Insights</h3>
  <ul>
    <li>Stable direction under sensitivity checks increases confidence.</li>
    <li>Fragile findings indicate need for confirmatory testing.</li>
  </ul>

  <h3>Business Recommendation</h3>
  <p>Use corrected and robustness-aware conclusions for executive go/no-go decisions.</p>
</details>

<details class="dropdown-section">
  <summary><strong>Business Recommendations</strong></summary>

  <div style="margin-top: 12px;"></div>

  <ul>
    <li>Roll out progressively with KPI monitoring if lift is credible and guardrails remain stable.</li>
    <li>Pair rollout with segment-level tracking dashboard for early anomaly detection.</li>
    <li>Predefine rollback triggers tied to conversion deterioration or guardrail breaches.</li>
  </ul>
</details>

<details class="dropdown-section">
  <summary><strong>Limitations</strong></summary>

  <div style="margin-top: 12px;"></div>

  <ul>
    <li>Simulated data may not capture all production behaviors.</li>
    <li>Short test windows can miss delayed conversion effects.</li>
    <li>Segment sample sizes may limit precision for smaller cohorts.</li>
  </ul>
</details>

<details class="dropdown-section">
  <summary><strong>Next Steps</strong></summary>

  <div style="margin-top: 12px;"></div>

  <ul>
    <li>Run confirmatory test with refined onboarding variant(s).</li>
    <li>Add retention and activation milestones as follow-up KPIs.</li>
    <li>Operationalize experimentation scorecard for ongoing product releases.</li>
  </ul>
</details>

<details class="dropdown-section">
  <summary><strong>Code &amp; Reproducibility (links to .R/.Rmd and outputs)</strong></summary>

  <div style="margin-top: 12px;"></div>

  <ul>
    <li><a href="./R/">R scripts (00–06 pipeline)</a></li>
    <li><a href="./reports/ab_test_report.Rmd">R Markdown report</a></li>
    <li><a href="./tables/">Generated tables</a></li>
    <li><a href="./figures/">Generated figures</a></li>
    <li><a href="./README.md">Project README</a></li>
  </ul>
</details>
