---
layout: default
title: "R Project: A/B Testing & Experimentation Analysis"
description: "End-to-end A/B testing and experimentation analysis of a simulated SaaS onboarding experiment using R — hypothesis testing, bootstrap inference, permutation tests, regression adjustment, and power analysis."
breadcrumbs:
  - title: Projects
    url: /projects/
  - title: "R A/B Testing & Experimentation"
---

<a href="/projects/" class="back-to-projects btn">&larr; Back to Projects</a>

# R Project: A/B Testing &amp; Experimentation Analysis

> Simulated SaaS onboarding experiment evaluating whether a redesigned onboarding flow improves trial-to-paid conversion while maintaining operational guardrails &mdash; full experimentation workflow from design through business recommendation.

**Tools:** R &middot; tidyverse &middot; infer &middot; broom &middot; sandwich &middot; ggplot2 &middot; patchwork &middot; RMarkdown

<p>
  <a href="https://github.com/nadeaujonny/nadeaujonny.github.io/tree/main/projects/r-ab-testing-simulated" target="_blank" rel="noopener">View on GitHub &rarr;</a>
</p>

---

<details class="dropdown-section">
  <summary><strong>Executive Summary</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Experiment Goal</h3>
  <p>
    Evaluate whether a new onboarding flow increases trial-to-paid conversion without harming the guardrail metric
    (onboarding time-to-complete).
  </p>

  <h3>Key Metrics</h3>
  <ul>
    <li><strong>Primary Metric:</strong> 30-day conversion rate (binary converted flag)</li>
    <li><strong>Guardrail:</strong> Onboarding time-to-complete (minutes) &mdash; lower is better</li>
  </ul>

  <h3>High-Level Outcome</h3>
  <p>
    Treatment increased conversion by <strong>+1.33 percentage points</strong> (10.2% &rarr; 11.5%, relative lift +13.1%)
    with a p-value of 0.032. All three inference methods (Z-test, bootstrap, permutation) converge on a statistically
    significant result. The guardrail metric <em>improved</em> &mdash; treatment users completed onboarding 0.34 minutes
    faster on average (p &lt; 0.001).
  </p>

  <h3>Final Recommendation</h3>
  <p>
    <strong>Decision: Ship with staged rollout and monitoring.</strong> The conversion lift is statistically significant
    and directionally consistent across all methods, while the guardrail moved favorably. However, the experiment was
    slightly underpowered (MDE at 80% power = 1.77 pp vs. observed 1.33 pp), so a staged ramp with ongoing monitoring
    is prudent before full deployment.
  </p>

  <h3>Why R?</h3>
  <p>
    R provides first-class support for statistical inference, resampling methods, power analysis, and fully
    reproducible reporting via RMarkdown &mdash; making it the ideal tool for rigorous experimentation workflows.
  </p>

</details>
<details class="dropdown-section">
  <summary><strong>Business Context &amp; Experiment Framing</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Problem</h3>
  <p>
    New users drop off during onboarding; conversion to paid subscriptions is below target. The product team
    hypothesizes that a redesigned onboarding flow can reduce friction and increase activation.
  </p>

  <h3>Proposed Change</h3>
  <p>
    Implement a new onboarding flow (treatment) designed to reduce time-to-complete and improve the rate at which
    trial users convert to paid subscriptions.
  </p>

  <h3>Business Value</h3>
  <p>
    Even small conversion improvements compound at scale. The guardrail metric (time-to-complete) ensures we
    do not trade conversion gains for a degraded onboarding experience.
  </p>

  <h3>Experiment Design</h3>
  <ul>
    <li><strong>Randomization Unit:</strong> Individual users</li>
    <li><strong>Split:</strong> 50/50 control vs. treatment</li>
    <li><strong>Observation Window:</strong> 30 days post-assignment</li>
    <li><strong>Sample Size:</strong> 10,000 users (5,017 control / 4,983 treatment)</li>
    <li><strong>Primary KPI:</strong> Conversion rate (binary)</li>
    <li><strong>Guardrail:</strong> Onboarding time-to-complete (minutes)</li>
  </ul>

</details>
<details class="dropdown-section">
  <summary><strong>Technical Stack &amp; Reproducibility</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Core Tools</h3>
  <ul>
    <li><strong>Language:</strong> R 4.x</li>
    <li><strong>IDE:</strong> RStudio / VS Code</li>
    <li><strong>Version Control:</strong> Git / GitHub</li>
    <li><strong>Reporting:</strong> RMarkdown (HTML output)</li>
  </ul>

  <h3>Key R Packages</h3>
  <ul>
    <li><code>tidyverse</code> &mdash; Data wrangling and visualization</li>
    <li><code>infer</code> &mdash; Tidy hypothesis testing workflows</li>
    <li><code>broom</code> &mdash; Model output tidying</li>
    <li><code>ggplot2</code>, <code>patchwork</code> &mdash; Advanced visualizations</li>
    <li><code>sandwich</code> &mdash; Robust (HC3) standard errors</li>
    <li><code>janitor</code> &mdash; Data cleaning utilities</li>
    <li><code>gt</code> &mdash; Publication-quality tables</li>
    <li><code>effectsize</code> &mdash; Standardized effect size measures</li>
  </ul>

  <h3>Repository Structure</h3>
  <pre><code>r-ab-testing-simulated/
├── data/
│   ├── raw/
│   ├── processed/
│   └── ab_test_data.csv
├── R/
│   ├── 00_generate_data.R
│   ├── 01_qc_srm.R
│   ├── 02_primary_metric.R
│   ├── 03_secondary_guardrails.R
│   ├── 04_bootstrap_permutation.R
│   ├── 05_regression_adjusted.R
│   └── 06_power_mde.R
├── figures/
├── tables/
├── reports/
├── requirements.R
└── README.md</code></pre>

  <h3>Reproducibility</h3>
  <p>
    All analysis is fully reproducible with <code>set.seed(123)</code> and documented dependencies. Scripts run
    sequentially (00&ndash;06) from data generation through power analysis. Outputs are saved to <code>tables/</code>
    and <code>figures/</code> directories with timestamped filenames.
  </p>

</details>
<details class="dropdown-section">
  <summary><strong>Dataset &amp; Simulation Design</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Dataset Type</h3>
  <p>
    Simulated dataset designed to mirror real-world product experimentation telemetry with realistic statistical
    properties. Generated via <code>00_generate_data.R</code> with controlled parameters.
  </p>

  <h3>Sample Size</h3>
  <ul>
    <li><strong>Total Users:</strong> 10,000</li>
    <li><strong>Control Group:</strong> 5,017</li>
    <li><strong>Treatment Group:</strong> 4,983</li>
  </ul>

  <h3>Column Dictionary</h3>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Column</th>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Type</th>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Description</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;"><code>user_id</code></td>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Integer</td>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Unique user identifier (1&ndash;10,000)</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;"><code>variant</code></td>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Character</td>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Experiment assignment: &ldquo;control&rdquo; or &ldquo;treatment&rdquo;</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;"><code>pre_sessions_7d</code></td>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Integer</td>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Count of sessions in 7 days pre-experiment (Poisson, &lambda; = 3)</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;"><code>converted</code></td>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Binary (0/1)</td>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Trial-to-paid conversion within 30 days (primary KPI)</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;"><code>time_to_complete</code></td>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Numeric</td>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Onboarding completion time in minutes (guardrail metric)</td>
      </tr>
    </tbody>
  </table>

  <h3>Data Generating Process (DGP)</h3>
  <p>The simulation incorporates:</p>
  <ul>
    <li><strong>Baseline conversion rate:</strong> 10% for control group</li>
    <li><strong>Treatment effect:</strong> +1.5 percentage point lift in conversion probability</li>
    <li><strong>Pre-experiment engagement:</strong> Poisson-distributed session counts (&lambda; = 3)</li>
    <li><strong>Onboarding time:</strong> Normal distribution (control mean = 8 min, treatment mean = 7.5 min, SD = 3 min), floored at 0.5 min</li>
    <li><strong>Reproducible seed:</strong> <code>set.seed(123)</code></li>
  </ul>

</details>
<details class="dropdown-section">
  <summary><strong>Data Quality &amp; Validation</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>QA Checklist</h3>
  <ul>
    <li>&#x2705; No missing values in any column</li>
    <li>&#x2705; No duplicate <code>user_id</code> values</li>
    <li>&#x2705; <code>converted</code> contains only 0/1 values</li>
    <li>&#x2705; <code>time_to_complete</code> contains no negative values (minimum &ge; 0.5)</li>
    <li>&#x2705; All required columns present: <code>user_id</code>, <code>variant</code>, <code>pre_sessions_7d</code>, <code>converted</code>, <code>time_to_complete</code></li>
    <li>&#x2705; Exactly two variant levels: &ldquo;control&rdquo; and &ldquo;treatment&rdquo;</li>
  </ul>

  <h3>Summary Statistics</h3>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Metric</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Control</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Treatment</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">N</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">5,017</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">4,983</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Conversion Rate</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">10.2%</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">11.5%</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Mean Pre-Sessions (7d)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">3.01</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">2.96</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Mean Time-to-Complete (min)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">7.87</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">7.53</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">SD Time-to-Complete</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">3.03</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">2.97</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">P90 Time-to-Complete (min)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">11.80</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">11.40</td>
      </tr>
    </tbody>
  </table>

</details>
<details class="dropdown-section">
  <summary><strong>Randomization Integrity &amp; SRM Checks</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Sample Ratio Mismatch (SRM) Test</h3>
  <p>
    Before examining treatment effects, the pipeline validates that the randomization split is trustworthy.
    A chi-square goodness-of-fit test compares the observed group sizes against the expected 50/50 allocation.
  </p>

  <h4>Expected vs. Observed Split</h4>
  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Group</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Expected</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Observed</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Difference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Control</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">50.00%</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">50.17%</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+0.17 pp</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Treatment</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">50.00%</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">49.83%</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&minus;0.17 pp</td>
      </tr>
    </tbody>
  </table>

  <h4>SRM Test Results</h4>
  <ul>
    <li><strong>Chi-Square Statistic:</strong> 0.116</li>
    <li><strong>P-Value:</strong> 0.734</li>
    <li><strong>Conclusion:</strong> &#x2705; <strong>PASS</strong> &mdash; No evidence of sample ratio mismatch. Randomization is trustworthy.</li>
  </ul>

  <h3>Covariate Balance Check</h3>
  <p>
    The only pre-experiment covariate (<code>pre_sessions_7d</code>) is compared between groups using a Welch
    two-sample t-test to confirm that randomization produced balanced groups.
  </p>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Metric</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Control</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Treatment</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Difference</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Mean Pre-Sessions</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">3.01</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">2.96</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.05</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">SD Pre-Sessions</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">1.72</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">1.71</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.01</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Median Pre-Sessions</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">3</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">3</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0</td>
      </tr>
    </tbody>
  </table>

  <ul>
    <li><strong>T-test P-Value:</strong> 0.188</li>
    <li><strong>95% CI for difference:</strong> [&minus;0.02, 0.11]</li>
    <li><strong>Conclusion:</strong> &#x2705; Baseline covariate is well-balanced between groups, confirming proper randomization.</li>
  </ul>

</details>
<details class="dropdown-section">
  <summary><strong>Analysis 1 &mdash; Primary Metric: Conversion Rate</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>
    Did the new onboarding flow increase trial-to-paid conversion, and is the lift statistically and practically significant?
  </p>

  <h3>Descriptive Results</h3>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Variant</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Users</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Conversions</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Conversion Rate</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Control</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">5,017</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">511</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">10.19%</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Treatment</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">4,983</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">574</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">11.52%</td>
      </tr>
    </tbody>
  </table>

  <h4>Effect Size</h4>
  <ul>
    <li><strong>Absolute Lift:</strong> +1.33 percentage points</li>
    <li><strong>Relative Lift:</strong> +13.1%</li>
    <li><strong>Cohen&rsquo;s h:</strong> 0.043 (small effect)</li>
  </ul>

  <h3>Statistical Inference &mdash; Multiple Methods</h3>

  <p>
    Three independent inference methods are applied to validate the result. Convergence across parametric,
    resampling, and permutation approaches strengthens confidence in the finding.
  </p>

  <h4>Method 1: Two-Proportion Z-Test</h4>
  <ul>
    <li><strong>Test Statistic (&chi;&sup2;):</strong> 4.598</li>
    <li><strong>P-Value:</strong> 0.032</li>
    <li><strong>95% Confidence Interval:</strong> [+0.11 pp, +2.55 pp]</li>
    <li><strong>Interpretation:</strong> Significant at &alpha; = 0.05</li>
  </ul>

  <h4>Method 2: Bootstrap Confidence Interval</h4>
  <ul>
    <li><strong>Bootstrap Iterations:</strong> 4,000</li>
    <li><strong>95% Bootstrap CI:</strong> [+0.12 pp, +2.57 pp]</li>
    <li><strong>Interpretation:</strong> Entire interval above zero &mdash; consistent with a positive treatment effect</li>
  </ul>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="figures/bootstrap_abs_lift.png"
      alt="Bootstrap distribution of the absolute conversion lift between treatment and control groups"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Bootstrap distribution of the absolute lift (treatment &minus; control). Dashed line marks the observed difference of +1.33 pp.
      <span style="display:block; margin-top:4px;">
        <a href="figures/bootstrap_abs_lift.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h4>Method 3: Permutation Test</h4>
  <ul>
    <li><strong>Permutation Iterations:</strong> 4,000</li>
    <li><strong>Observed Difference:</strong> +1.33 pp</li>
    <li><strong>Empirical P-Value (two-sided):</strong> 0.036</li>
    <li><strong>Infer Package P-Value:</strong> 0.033</li>
    <li><strong>Interpretation:</strong> Significant &mdash; observed lift falls in the extreme tail of the null distribution</li>
  </ul>

  <h3>Method Comparison Summary</h3>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Method</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Point Estimate</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">95% CI Lower</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">95% CI Upper</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">P-Value</th>
        <th style="text-align:center; border-bottom: 2px solid #ddd; padding: 8px 6px;">Significant?</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Z-Test</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+1.33 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+0.11 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+2.55 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.032</td>
        <td style="padding: 8px 6px; text-align:center; border-bottom: 1px solid #eee;">Yes</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Bootstrap</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+1.33 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+0.12 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+2.57 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&mdash;</td>
        <td style="padding: 8px 6px; text-align:center; border-bottom: 1px solid #eee;">Yes</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Permutation</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+1.33 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&mdash;</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&mdash;</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.036</td>
        <td style="padding: 8px 6px; text-align:center; border-bottom: 1px solid #eee;">Yes</td>
      </tr>
    </tbody>
  </table>

  <h3>Key Insights</h3>
  <ul>
    <li><strong>Consistent evidence:</strong> All three methods agree that the treatment effect is statistically significant at &alpha; = 0.05.</li>
    <li><strong>Narrow but positive CI:</strong> The lower bound of the confidence interval is close to zero (+0.11 pp), indicating the true effect could be small.</li>
    <li><strong>Small effect size:</strong> Cohen&rsquo;s h of 0.043 classifies this as a small effect, though even small conversion improvements can be meaningful at scale.</li>
  </ul>

  <h3>Business Recommendation</h3>
  <p>
    The conversion lift is real and directionally consistent across all methods. Proceed to guardrail and power analysis
    before making a final ship decision.
  </p>

</details>
<details class="dropdown-section">
  <summary><strong>Analysis 2 &mdash; Guardrail: Onboarding Time-to-Complete</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>
    Does the new onboarding flow maintain or improve the user experience, as measured by time-to-complete?
    A degradation here would indicate the treatment is creating friction despite improving conversion.
  </p>

  <h3>Time-to-Complete by Variant</h3>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Variant</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Mean (min)</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Median (min)</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">SD</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">P90</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Control</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">7.87</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">7.87</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">3.03</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">11.80</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Treatment</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">7.53</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">7.49</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">2.97</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">11.40</td>
      </tr>
    </tbody>
  </table>

  <h3>Statistical Tests</h3>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Test</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Difference</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">95% CI</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">P-Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Welch t-test</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&minus;0.34 min</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">[&minus;0.46, &minus;0.22]</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&lt; 0.001</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Wilcoxon rank-sum</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&minus;0.34 min</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&mdash;</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&lt; 0.001</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Bootstrap (B = 2,000)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&minus;0.34 min</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">[&minus;0.46, &minus;0.22]</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&mdash;</td>
      </tr>
    </tbody>
  </table>

  <figure style="margin: 0 0 18px 0;">
    <img
      src="figures/guardrail_time_to_complete.png"
      alt="Box plot comparing onboarding time-to-complete between control and treatment groups"
      loading="lazy"
      style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 6px;"
    >
    <figcaption style="font-size: 0.95em; color: #555; margin-top: 6px;">
      Onboarding time-to-complete by variant. Treatment users complete onboarding faster on average.
      <span style="display:block; margin-top:4px;">
        <a href="figures/guardrail_time_to_complete.png">Open full-size</a>
      </span>
    </figcaption>
  </figure>

  <h3>Key Insights</h3>
  <ul>
    <li><strong>Guardrail improved:</strong> Treatment users completed onboarding 0.34 minutes faster, a highly significant difference (p &lt; 0.001).</li>
    <li><strong>Consistent across tests:</strong> Parametric (t-test), nonparametric (Wilcoxon), and bootstrap methods all agree on the direction and magnitude.</li>
    <li><strong>No harm detected:</strong> The new onboarding flow reduced friction rather than increasing it, ruling out a speed-quality tradeoff concern.</li>
  </ul>

  <h3>Business Recommendation</h3>
  <p>
    The guardrail metric moves favorably &mdash; treatment not only improves conversion but also delivers a faster
    onboarding experience. No red flags for user experience degradation.
  </p>

</details>
<details class="dropdown-section">
  <summary><strong>Analysis 3 &mdash; Regression-Adjusted Treatment Effects</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>
    Does the treatment effect hold after adjusting for the pre-experiment engagement covariate? Regression adjustment
    can improve precision and verify that the unadjusted estimate is not confounded.
  </p>

  <h3>Conversion Model: Logistic Regression</h3>

  <h4>Model Specification</h4>
  <pre><code class="language-r">glm(converted ~ variant + log1p(pre_sessions_7d),
    data = df,
    family = binomial())</code></pre>

  <h4>Regression Coefficients (Robust HC3 Standard Errors)</h4>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Variable</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Log-Odds</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Std. Error</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Odds Ratio</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">OR 95% CI</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">P-Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">(Intercept)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&minus;2.183</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.099</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.113</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">[0.093, 0.137]</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&lt; 0.001</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;"><strong>Treatment</strong></td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;"><strong>0.138</strong></td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.064</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;"><strong>1.148</strong></td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;"><strong>[1.012, 1.303]</strong></td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;"><strong>0.032</strong></td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">log1p(Pre-Sessions)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.005</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.068</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">1.005</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">[0.879, 1.148]</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.943</td>
      </tr>
    </tbody>
  </table>

  <h4>Treatment Effect Interpretation</h4>
  <ul>
    <li><strong>Odds Ratio:</strong> 1.148 (95% CI: [1.012, 1.303])</li>
    <li><strong>Interpretation:</strong> Treatment increases the odds of conversion by 14.8%, controlling for pre-experiment engagement.</li>
  </ul>

  <h3>Marginal Effects &amp; Adjusted Risk Difference</h3>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Method</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Treatment Effect</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">95% CI</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Unadjusted (Simple Difference)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+1.33 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">[+0.11, +2.55]</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Regression-Adjusted (Marginal Effect)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+1.33 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">[+0.25, +2.57]</td>
      </tr>
    </tbody>
  </table>

  <p>
    <strong>Interpretation:</strong> The adjusted and unadjusted estimates are nearly identical (+1.33 pp), confirming that
    the pre-experiment covariate does not confound the treatment effect. This is expected given the confirmed randomization
    balance. The adjusted CI is slightly tighter, demonstrating the variance-reduction benefit of covariate adjustment.
  </p>

  <h3>Guardrail Model: OLS Regression</h3>

  <h4>Model Specification</h4>
  <pre><code class="language-r">lm(time_to_complete ~ variant + log1p(pre_sessions_7d),
   data = df)</code></pre>

  <h4>Treatment Effect (Robust HC3 Standard Errors)</h4>
  <ul>
    <li><strong>Adjusted Difference:</strong> &minus;0.34 minutes</li>
    <li><strong>95% CI:</strong> [&minus;0.46, &minus;0.22]</li>
    <li><strong>P-Value:</strong> &lt; 0.001</li>
    <li><strong>Interpretation:</strong> Treatment reduces onboarding time by 0.34 minutes, confirmed after adjustment.</li>
  </ul>

  <h3>Key Insights</h3>
  <ul>
    <li>Regression adjustment confirms the unadjusted estimates for both conversion and time-to-complete.</li>
    <li>Pre-experiment sessions have no meaningful relationship with conversion (p = 0.943), consistent with proper randomization.</li>
    <li>Robust (HC3) standard errors protect against heteroscedasticity without changing conclusions.</li>
  </ul>

</details>
<details class="dropdown-section">
  <summary><strong>Analysis 4 &mdash; Power Analysis &amp; Minimum Detectable Effect</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>
    Was the experiment adequately powered to detect the observed effect? What sample sizes would be needed for
    future experiments targeting specific lift thresholds?
  </p>

  <h3>Experiment Parameters</h3>
  <ul>
    <li><strong>Baseline Conversion Rate:</strong> 10.19%</li>
    <li><strong>Sample Size per Group:</strong> 4,983 (conservative, using smaller group)</li>
    <li><strong>Significance Level (&alpha;):</strong> 0.05</li>
    <li><strong>Target Power:</strong> 0.80</li>
  </ul>

  <h3>Minimum Detectable Effect (MDE)</h3>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Metric</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">MDE at 80% Power</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">1.77 pp</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Observed Lift</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">1.33 pp</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Estimated Power at Observed Lift</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">~55%</td>
      </tr>
    </tbody>
  </table>

  <p>
    The observed lift (1.33 pp) falls <em>below</em> the 80%-power MDE threshold (1.77 pp), meaning the experiment was
    slightly underpowered for the true effect size. This does not invalidate the significant result &mdash; it means
    there was approximately a 45% chance of missing a real effect of this magnitude.
  </p>

  <h3>Sample Size Requirements for Future Experiments</h3>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Target Lift</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">N per Group</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Total N</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+0.5 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">58,686</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">117,372</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+1.0 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">14,981</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">29,962</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+1.5 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">6,794</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">13,588</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+2.0 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">3,898</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">7,796</td>
      </tr>
    </tbody>
  </table>

  <h3>Power Curve (Selected Points)</h3>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Lift (pp)</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Power</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.5</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">12.6%</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">1.0</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">36.5%</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">1.5</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">67.0%</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">1.8</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">81.7%</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">2.0</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">88.6%</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">2.5</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">97.5%</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">3.0</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">99.7%</td>
      </tr>
    </tbody>
  </table>

  <h3>Key Insights</h3>
  <ul>
    <li>The experiment was slightly underpowered for the observed effect size (power ~55% vs. the standard 80% threshold).</li>
    <li>To reliably detect a +1.33 pp lift at 80% power, approximately 7,000+ users per group would be needed.</li>
    <li>Despite the power shortfall, the result was still statistically significant &mdash; the true effect may be larger than the point estimate.</li>
    <li>Future experiments targeting smaller lifts (&lt; 1 pp) would require substantially larger samples (30,000+ per group).</li>
  </ul>

  <h3>Business Recommendation</h3>
  <p>
    For confirmatory testing, increase sample size to 15,000+ per group to achieve 80% power for effects as small
    as 1.0 pp. This experiment provides a useful signal but should be validated with a larger follow-up if the business
    requires higher certainty for marginal effects.
  </p>

</details>
<details class="dropdown-section">
  <summary><strong>Analysis 5 &mdash; Sensitivity &amp; Robustness Checks</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Business Question</h3>
  <p>
    Do conclusions remain stable across different analytical approaches and assumptions?
  </p>

  <h3>Conversion Effect &mdash; Method Comparison</h3>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Method</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Point Estimate</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">95% CI</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">P-Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Two-Proportion Z-Test</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+1.33 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">[+0.11, +2.55]</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.032</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Bootstrap (B = 4,000)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+1.33 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">[+0.12, +2.57]</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&mdash;</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Permutation (B = 4,000)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+1.33 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&mdash;</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.036</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Infer Permutation (B = 4,000)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+1.33 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&mdash;</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.033</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Logistic Regression (HC3)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">+1.33 pp</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">[+0.25, +2.57]</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">0.032</td>
      </tr>
    </tbody>
  </table>

  <h3>Guardrail Effect &mdash; Method Comparison</h3>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Method</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Point Estimate</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">P-Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Welch t-test</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&minus;0.34 min</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&lt; 0.001</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Wilcoxon rank-sum</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&minus;0.34 min</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&lt; 0.001</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Bootstrap (B = 2,000)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&minus;0.34 min</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&mdash;</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">OLS Regression (HC3)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&minus;0.34 min</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">&lt; 0.001</td>
      </tr>
    </tbody>
  </table>

  <h3>Key Insights</h3>
  <ul>
    <li><strong>All five conversion methods converge</strong> on a +1.33 pp lift with p-values in the 0.032&ndash;0.036 range.</li>
    <li><strong>All four guardrail methods converge</strong> on a &minus;0.34 minute reduction with extreme significance.</li>
    <li>Confidence intervals are consistent across parametric and resampling approaches.</li>
    <li>The stability of results across methods increases confidence that the findings are not artifacts of a single analytical choice.</li>
  </ul>

</details>
<details class="dropdown-section">
  <summary><strong>Final Decision Memo</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Summary of Effects</h3>

  <h4>Primary Metric: Conversion Rate</h4>
  <ul>
    <li><strong>Observed Lift:</strong> +1.33 percentage points (+13.1% relative)</li>
    <li><strong>95% Confidence Interval:</strong> [+0.11 pp, +2.55 pp]</li>
    <li><strong>Statistical Significance:</strong> Yes (p = 0.032)</li>
    <li><strong>Practical Significance:</strong> Meaningful at scale &mdash; projects to meaningful incremental conversions annually</li>
  </ul>

  <h4>Guardrail: Time-to-Complete</h4>
  <ul>
    <li><strong>Observed Change:</strong> &minus;0.34 minutes (treatment is faster)</li>
    <li><strong>95% CI:</strong> [&minus;0.46, &minus;0.22]</li>
    <li><strong>Statistical Significance:</strong> Yes (p &lt; 0.001)</li>
    <li><strong>Assessment:</strong> &#x2705; Guardrail improved &mdash; no degradation</li>
  </ul>

  <h3>Business Impact Projection</h3>
  <p>Assuming 100,000 annual trial signups:</p>

  <table style="border-collapse: collapse; width: 100%; max-width: 780px; margin: 20px 0;">
    <thead>
      <tr>
        <th style="text-align:left; border-bottom: 2px solid #ddd; padding: 8px 6px;">Metric</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Current (Control)</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">New (Treatment)</th>
        <th style="text-align:right; border-bottom: 2px solid #ddd; padding: 8px 6px;">Incremental Gain</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Annual Conversions</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">10,190</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">11,520</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee; font-weight:700;">+1,330 paid users</td>
      </tr>
      <tr>
        <td style="padding: 8px 6px; border-bottom: 1px solid #eee;">Onboarding Time (avg)</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">7.87 min</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee;">7.53 min</td>
        <td style="padding: 8px 6px; text-align:right; border-bottom: 1px solid #eee; font-weight:700;">&minus;0.34 min per user</td>
      </tr>
    </tbody>
  </table>

  <h3>Risks &amp; Considerations</h3>
  <ol>
    <li><strong>Power gap:</strong> The experiment was slightly underpowered (MDE at 80% power = 1.77 pp vs. observed 1.33 pp). The true effect could be smaller than estimated.</li>
    <li><strong>Simulated data:</strong> Results reflect a controlled simulation; real-world behavior may introduce additional variability.</li>
    <li><strong>Short observation window:</strong> 30-day conversion may not capture long-term retention or LTV effects.</li>
  </ol>

  <h3>Mitigation Strategies</h3>
  <ol>
    <li>Deploy via staged rollout (25% &rarr; 50% &rarr; 100%) with real-time KPI monitoring.</li>
    <li>Run a confirmatory test at larger scale (15,000+ per group) to narrow the confidence interval.</li>
    <li>Add 90-day and 180-day retention follow-up metrics to assess long-term impact.</li>
  </ol>

  <h3>Recommendation</h3>

  <p><strong>&#x2705; SHIP &mdash; with staged rollout and monitoring gates.</strong></p>

  <p>
    The conversion lift is statistically significant across all five inference methods, the guardrail metric
    improved (faster onboarding), and the treatment effect is directionally consistent after covariate adjustment.
    Although the experiment was slightly underpowered for the observed effect size, the consistency of evidence
    across methods and the favorable guardrail signal support a ship decision with appropriate monitoring safeguards.
  </p>

  <h4>Rollout Plan</h4>
  <ul>
    <li><strong>Phase 1:</strong> Ship to 25% of new users for 2 weeks with daily KPI monitoring.</li>
    <li><strong>Phase 2:</strong> Scale to 100% if conversion and guardrail metrics hold within expected ranges.</li>
    <li><strong>Monitoring:</strong> Track conversion rate, time-to-complete, and support ticket volume weekly.</li>
  </ul>

  <h4>Next Experiments</h4>
  <ol>
    <li><strong>Onboarding Variant Tuning:</strong> Test specific onboarding steps to isolate which changes drive the most lift.</li>
    <li><strong>Retention Study:</strong> Measure 90-day and 180-day retention to validate long-term quality of converted users.</li>
    <li><strong>Larger Confirmatory Test:</strong> Run at 15,000+ users per group to achieve 80% power for a 1.0 pp lift.</li>
  </ol>

</details>
<details class="dropdown-section">
  <summary><strong>Code &amp; Reproducibility</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Prerequisites</h3>
  <ul>
    <li>R version 4.0 or higher</li>
    <li>RStudio (recommended)</li>
    <li>Git</li>
  </ul>

  <h3>Quick Start</h3>
  <pre><code class="language-bash"># Clone repository
git clone https://github.com/nadeaujonny/nadeaujonny.github.io.git
cd projects/r-ab-testing-simulated

# Install required packages
Rscript requirements.R

# Run full analysis pipeline (scripts 00-06)
Rscript R/00_generate_data.R
Rscript R/01_qc_srm.R
Rscript R/02_primary_metric.R
Rscript R/03_secondary_guardrails.R
Rscript R/04_bootstrap_permutation.R
Rscript R/05_regression_adjusted.R
Rscript R/06_power_mde.R</code></pre>

  <h3>Analysis Scripts (in order)</h3>
  <ol>
    <li><code>00_generate_data.R</code> &mdash; Create simulated dataset (10,000 users, seed = 123)</li>
    <li><code>01_qc_srm.R</code> &mdash; Data quality and SRM randomization checks</li>
    <li><code>02_primary_metric.R</code> &mdash; Conversion rate analysis with prop.test and effect sizes</li>
    <li><code>03_secondary_guardrails.R</code> &mdash; Time-to-complete guardrail analysis (t-test, Wilcoxon, bootstrap)</li>
    <li><code>04_bootstrap_permutation.R</code> &mdash; Bootstrap CI and permutation tests for conversion lift</li>
    <li><code>05_regression_adjusted.R</code> &mdash; Covariate-adjusted estimates with robust standard errors</li>
    <li><code>06_power_mde.R</code> &mdash; Power analysis and MDE calculations</li>
  </ol>

  <h3>Output Artifacts</h3>
  <ul>
    <li><code>data/ab_test_data.csv</code> &mdash; Clean analysis dataset</li>
    <li><code>figures/*.png</code> &mdash; All visualizations</li>
    <li><code>tables/*.csv</code> &mdash; Statistical results tables</li>
  </ul>

  <h3>Key Code Highlights</h3>

  <h4>Bootstrap Confidence Interval</h4>
  <pre><code class="language-r"># Bootstrap conversion rate difference (4,000 iterations)
boot_diffs <- replicate(B, {
  p_c <- mean(sample(control_rows$converted_num,
                     size = nrow(control_rows),
                     replace = TRUE))
  p_t <- mean(sample(treat_rows$converted_num,
                     size = nrow(treat_rows),
                     replace = TRUE))
  p_t - p_c
})

# 95% percentile CI
boot_ci <- quantile(boot_diffs, probs = c(0.025, 0.975))</code></pre>

  <h4>Regression-Adjusted Treatment Effect with Robust SEs</h4>
  <pre><code class="language-r">library(sandwich)

# Logistic regression with HC3 robust standard errors
m_conv <- glm(converted ~ variant + log1p(pre_sessions_7d),
              data = df, family = binomial())

vc_conv <- sandwich::vcovHC(m_conv, type = "HC3")

# Adjusted risk difference via predicted probabilities
df_control <- df %>% mutate(variant = "control")
df_treat   <- df %>% mutate(variant = "treatment")

adj_rd <- mean(predict(m_conv, df_treat, type = "response") -
               predict(m_conv, df_control, type = "response"))</code></pre>

  <h4>Power Curve</h4>
  <pre><code class="language-r"># Power at observed sample size across candidate lifts
power_curve <- tibble(
  lift_pp = seq(0.0, 3.0, by = 0.1),
  power = sapply(lift_pp / 100, function(d) {
    p1 <- min(max(p0 + d, 0), 1)
    power.prop.test(
      n = n_per_group, p1 = p0, p2 = p1,
      sig.level = 0.05, alternative = "two.sided"
    )$power
  })
)</code></pre>

</details>
<details class="dropdown-section">
  <summary><strong>Skills &amp; Techniques Demonstrated</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <h3>Statistical &amp; Analytical Skills</h3>
  <ul>
    <li><strong>Experimental Design:</strong> Sample size planning, power analysis, randomization integrity testing (SRM checks), covariate balance assessment</li>
    <li><strong>Hypothesis Testing:</strong> Multiple inference methods (parametric prop.test, bootstrap resampling, permutation tests) with appropriate handling of binary outcomes</li>
    <li><strong>Advanced Techniques:</strong> Bootstrap confidence intervals, permutation tests for exact p-values, regression adjustment for precision gains, robust (HC3) standard errors, marginal effects from logistic models</li>
    <li><strong>Sensitivity Analysis:</strong> Cross-method comparison to validate result stability across analytical assumptions</li>
  </ul>

  <h3>Technical Skills</h3>
  <ul>
    <li><strong>R Programming:</strong> Efficient data manipulation with <code>tidyverse</code>, statistical modeling with <code>glm</code>/<code>lm</code>, custom resampling functions, reproducible seed-controlled workflows</li>
    <li><strong>Data Visualization:</strong> Publication-quality plots with <code>ggplot2</code>, bootstrap distributions, box plots with jitter overlays</li>
    <li><strong>Statistical Packages:</strong> <code>infer</code> for tidy hypothesis testing, <code>broom</code> for model output tidying, <code>sandwich</code> for robust inference, <code>janitor</code> for data cleaning</li>
    <li><strong>Version Control:</strong> Git/GitHub with modular, sequential script architecture</li>
  </ul>

  <h3>Business &amp; Communication Skills</h3>
  <ul>
    <li><strong>Strategic Thinking:</strong> Clear problem framing, balancing statistical rigor with practical significance, guardrail metrics to prevent unintended harm</li>
    <li><strong>Decision Frameworks:</strong> Ship/no-ship recommendation grounded in multi-method statistical evidence, business impact projection, and risk assessment</li>
    <li><strong>Stakeholder Communication:</strong> Executive summary for non-technical audiences, clear visualization of uncertainty, actionable rollout plan with monitoring gates</li>
    <li><strong>Experimental Best Practices:</strong> Randomization validation before examining results, multiple inference methods without p-hacking, transparent reporting of power limitations</li>
  </ul>

</details>
<details class="dropdown-section">
  <summary><strong>Limitations</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <ul>
    <li>Simulated data may not capture all real-world production behaviors (e.g., network effects, seasonal patterns).</li>
    <li>The simplified simulation includes only one pre-experiment covariate (<code>pre_sessions_7d</code>); real experiments typically have richer covariate sets for segmentation and adjustment.</li>
    <li>The 30-day observation window may not capture delayed conversion effects or long-term retention impacts.</li>
    <li>The experiment was slightly underpowered for the observed effect size, which increases uncertainty around the point estimate.</li>
    <li>No revenue or lifetime value (LTV) data is included; conversion lift does not directly translate to revenue impact without additional modeling.</li>
  </ul>

</details>
<details class="dropdown-section">
  <summary><strong>Next Steps</strong></summary>

  <div style="margin-top: 12px;"></div>
  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 12px 0 20px 0;">

  <ul>
    <li>Run a confirmatory test with larger sample size (15,000+ per group) to achieve 80% power for a 1.0 pp lift.</li>
    <li>Add device, channel, and region covariates to enable heterogeneous treatment effect analysis and targeted rollout strategies.</li>
    <li>Incorporate revenue and retention metrics as secondary outcomes to quantify business value beyond conversion rate.</li>
    <li>Operationalize an experimentation scorecard for ongoing product releases with pre-registered hypotheses and decision criteria.</li>
    <li>Build a monitoring dashboard for staged rollout tracking with automated guardrail alerts.</li>
  </ul>

</details>
