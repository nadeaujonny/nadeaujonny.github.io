# Master Outline & Study Guide
## A/B Testing & Experimentation Analysis (R) — a 7-script SaaS experiment pipeline

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.
>
> **One sentence to anchor everything:** This project is a rigorous, 7-script R pipeline
> that analyzes a simulated SaaS onboarding A/B test the way a real experimentation team
> would — **SRM check → primary metric → guardrail → distribution-free validation →
> regression adjustment → power analysis** — and the whole thing is built on *simulated
> data with a known ground truth* so the pipeline can prove it recovers the right answer.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Context)](#2-why-this-project-exists-context)
3. [The Tech Stack](#3-the-tech-stack)
4. [The Dataset — A Simulated SaaS Experiment](#4-the-dataset--a-simulated-saas-experiment)
5. [The 7-Script Pipeline (Architecture)](#5-the-7-script-pipeline-architecture)
6. [Script 00 — Data Generation](#6-script-00--data-generation)
7. [Script 01 — QC & SRM Detection](#7-script-01--qc--srm-detection)
8. [Script 02 — Primary Metric (Conversion)](#8-script-02--primary-metric-conversion)
9. [Script 03 — Secondary Guardrail (Time-to-Complete)](#9-script-03--secondary-guardrail-time-to-complete)
10. [Script 04 — Bootstrap & Permutation Inference](#10-script-04--bootstrap--permutation-inference)
11. [Script 05 — Regression-Adjusted Effects (CUPED)](#11-script-05--regression-adjusted-effects-cuped)
12. [Script 06 — Power & MDE Analysis](#12-script-06--power--mde-analysis)
13. [Key Results & The Ship Decision](#13-key-results--the-ship-decision)
14. [A/B Testing & Statistics Concepts to Know Cold](#14-ab-testing--statistics-concepts-to-know-cold)
15. [Limitations & Honest Caveats](#15-limitations--honest-caveats)
16. [Interview Q&A](#16-interview-qa)
17. [How to Walk Through This Project Live](#17-how-to-walk-through-this-project-live)
18. [Glossary](#18-glossary)

---

## 1. The 30-Second Pitch

This project is a **complete A/B testing pipeline in R** — seven modular scripts that take
a simulated SaaS onboarding experiment from raw data all the way to a defensible
ship/no-ship decision. It compares a **new onboarding flow (treatment)** against the
**current experience (control)** across **10,000 users**.

The pipeline follows the methodology real experimentation teams (Microsoft, Booking.com,
Netflix) use, in the correct order: **(00)** generate the data, **(01)** verify
randomization integrity with a **Sample Ratio Mismatch (SRM)** check before looking at any
results, **(02)** analyze the **primary metric** (conversion rate), **(03)** check a
**guardrail metric** (time-to-complete) for unintended harm, **(04)** validate with
**distribution-free inference** (bootstrap + permutation), **(05)** refine the estimate with
**regression adjustment (CUPED)**, and **(06)** run a **power / MDE analysis** for future
experiment design.

The deliberate trick: the data is **simulated with a known ground truth** (+1.5pp
conversion lift, −0.5 min time reduction). If the pipeline recovers those planted effects,
the methodology is validated — which is exactly how experimentation platforms are tested
before they touch a real experiment. The result: a +1.33pp conversion lift (p = 0.032), a
faster onboarding guardrail, and a "ship with staged ramp" recommendation.

**One-line version:** "I built a seven-script R pipeline that runs the full rigorous A/B
testing workflow — SRM check, primary and guardrail metrics, bootstrap and permutation
inference, CUPED regression adjustment, and power analysis — on a simulated experiment with
a known ground truth, so the pipeline proves it recovers the right answer."

---

## 2. Why This Project Exists (Context)

**The problem.** A/B testing is the **gold standard for measuring the *causal* impact** of
a product change — randomization is what lets you attribute a difference to the treatment
rather than to confounders. But analyzing an experiment *correctly* is harder than it
looks: you have to verify the randomization worked, pick the right test, guard against
unintended harm, quantify uncertainty honestly, and know whether the experiment was even
powered to detect the effect. Doing it wrong produces confident, wrong decisions.

**The simulated scenario.** A SaaS company redesigns its onboarding flow, expecting it to
**lift conversion** and **reduce time-to-complete**. The pipeline's job: turn the raw
experiment data into a **defensible ship/no-ship decision with quantified uncertainty.**

**Why simulate the data — the single smartest design choice in the project.** The data is
generated with a **known ground truth** (a planted +1.5pp lift, −0.5 min reduction). That
means the pipeline can be *validated*: if the analysis recovers the planted effects, the
methodology is proven correct. This is exactly how real experimentation platforms are
tested — teams at Microsoft and Netflix simulate experiments to verify their analysis code
before deploying it on live experiments, because you can't validate analysis code against
real data where you don't know the true answer.

**Why it's a strong portfolio project.** It is the portfolio's deepest **statistics /
causal-inference** project. It demonstrates not just running a t-test, but the full
*discipline* of experimentation: integrity checks first, multiple inference methods,
variance reduction, power analysis, and an honest decision memo. It shows you understand
*why* each step exists and the order it must happen in.

---

## 3. The Tech Stack

| Tool / Package | Role |
|---|---|
| **R** | The language for the entire pipeline. |
| **tidyverse / dplyr** | Data manipulation, piping, summarization. |
| **ggplot2** | Publication-quality figures (box plot, bootstrap histogram, power curve). |
| **infer** | A tidy framework for permutation/bootstrap inference — used as a clean cross-check. |
| **broom** | Tidies model output (`tidy`, `glance`) into data frames. |
| **sandwich** | **HC3 robust standard errors** for the regression-adjusted models. |
| **janitor** | `clean_names()` and data cleaning. |
| **scales / readr** | Number formatting (percent, comma) and CSV I/O. |

**The mental model.** Seven R scripts, run **in sequence 00 → 06**. Each script reads from
`data/`, writes result tables to `tables/` (as timestamped CSVs) and figures to `figures/`.
It's a **modular pipeline** — every script is independently runnable and produces
inspectable artifacts.

**Two engineering disciplines worth citing:**
- **Reproducibility** — `set.seed(123)` everywhere, so every run produces identical data
  and identical results.
- **Defensive coding** — every script does fail-fast schema checks (`stopifnot()`,
  `setdiff()` on required columns) and Script 01 will **halt the entire pipeline** if SRM
  is detected. "Fail loudly" is built in.

*(There is also a `reports/ab_test_report.Rmd` — but note it's a **template/skeleton** with
placeholder text and commented-out code, not a filled-in report. The real analysis lives in
the seven scripts; see §15.)*

---

## 4. The Dataset — A Simulated SaaS Experiment

There is **no real dataset** — Script 00 *generates* it. That's the point.

| Attribute | Value |
|---|---|
| Type | **Simulated** with a known ground truth |
| Sample size | **10,000 users** |
| Variants | Control / Treatment, **50/50** random assignment |
| Primary metric | **Conversion** — binary (did the user complete onboarding) |
| Secondary / guardrail metric | **Time-to-complete** — continuous, minutes |
| Covariate | **`pre_sessions_7d`** — pre-experiment engagement, Poisson(λ=3) |
| **Ground truth (planted effects)** | **+1.5pp conversion lift** · **−0.5 min** time reduction |

**The planted effects in detail:**
- **Conversion:** control baseline **10%**; treatment = baseline **+ 1.5pp = 11.5%** true
  rate. `converted` is then drawn from `rbinom` using each user's true probability.
- **Time-to-complete:** drawn from a Normal — control centered at **8.0 min**, treatment at
  **7.5 min** (0.5 min faster), both SD = 3 (floored at 0.5 to avoid negatives).
- **The covariate `pre_sessions_7d`** is *pre-experiment* — it exists to enable the
  regression adjustment (CUPED) in Script 05. Because it's pre-experiment, a good
  randomization should leave it balanced across groups (Script 01 confirms this).

**The five data columns:** `user_id`, `variant`, `pre_sessions_7d`, `converted`,
`time_to_complete` — 10,000 rows, saved to `data/ab_test_data.csv`.

---

## 5. The 7-Script Pipeline (Architecture)

```
  00_generate_data.R        → data/ab_test_data.csv  (10,000 simulated users)
        │
        ▼
  01_qc_srm.R               SRM check + covariate balance  ── HALTS if SRM detected
        │
        ▼
  02_primary_metric.R       conversion: two-proportion z-test, lift, CI, Cohen's h
        │
        ▼
  03_secondary_guardrails.R time-to-complete: t-test + Wilcoxon + bootstrap CI
        │
        ▼
  04_bootstrap_permutation.R bootstrap CI (B=4,000) + permutation test (B=4,000)
        │
        ▼
  05_regression_adjusted.R  CUPED — logistic + OLS, HC3 robust SE, adjusted effects
        │
        ▼
  06_power_mde.R            MDE at 80% power, sample-size table, power curve
        │
        ▼
  tables/*.csv  +  figures/*.png   (all artifacts)
```

**The key architectural idea — the *order* is the methodology.** This isn't an arbitrary
sequence; it's the *correct* sequence a rigorous experiment analysis must follow:

1. **Integrity before results.** Script 01 checks SRM *first* — you must never look at the
   primary metric until you've confirmed the randomization is sound.
2. **Primary before guardrails.** Script 02 measures the metric the decision hinges on;
   Script 03 then checks for collateral damage.
3. **Validate before trusting.** Script 04 re-derives the primary result with
   assumption-free methods to confirm the classical test wasn't an artifact.
4. **Refine, then plan.** Script 05 tightens the estimate; Script 06 assesses whether the
   experiment was even powered — and informs the *next* experiment's design.

Each script is modular: reads `data/`, writes `tables/` + `figures/`. Result tables carry
**timestamp suffixes** in their filenames (a project convention).

---

## 6. Script 00 — Data Generation

**File:** `00_generate_data.R` · **Output:** `data/ab_test_data.csv`

**What it does.** With `set.seed(123)` for reproducibility, it builds a 10,000-row tibble:
each user gets a `user_id`, a random 50/50 `variant` assignment (`sample()`), and a
`pre_sessions_7d` covariate from `rpois(λ=3)`. Then it plants the effects:
- `conversion_prob` is set by variant (0.10 control, 0.115 treatment) via `case_when`,
  and `converted` is drawn from `rbinom(n, 1, conversion_prob)`.
- `time_to_complete` is drawn from `rnorm` — mean 8.0 (control) or 7.5 (treatment), SD 3 —
  then floored at 0.5 minutes so no times go negative.

It saves the five-column CSV.

**The teachable point.** Generating data with a *known* answer is what makes the rest of
the pipeline a *validation*, not just an analysis. The whole project's credibility rests on
this: every downstream result can be checked against the planted +1.5pp / −0.5 min truth.

---

## 7. Script 01 — QC & SRM Detection

**File:** `01_qc_srm.R` · **Outputs:** `qc_srm_group_counts.csv`, `qc_srm_test.csv`,
`qc_baseline_balance_*.csv`

**This is the gate. Know it cold — SRM is the project's signature concept.**

**What SRM is.** **Sample Ratio Mismatch** — when the *observed* split between variants
deviates significantly from the *expected* split (here, 50/50). If you expected 50/50 and
got 52/48 with a tiny p-value, **something is broken** — an assignment bug, a logging
error, bot traffic, a redirect that drops users. SRM is "the single most critical quality
check" because **a compromised randomization invalidates everything downstream.**

**What the script does:**
1. **Schema check** — confirms the five required columns exist; stops if any are missing.
2. **The SRM test** — counts users per variant, then runs a **chi-square goodness-of-fit
   test** against the expected 50/50 proportions.
3. **Fail loudly** — `if (p_value < 0.01) stop("SRM detected...")`. The pipeline
   **halts** — because *analyzing results from a broken randomization is worse than
   analyzing nothing.*
4. **Covariate balance** — a **Welch two-sample t-test** on `pre_sessions_7d` to confirm
   the pre-experiment covariate is balanced across variants (no pre-existing group
   difference).

**Results:** Control 5,017 (observed 0.502) vs. Treatment 4,983 (0.498). **Chi-square = 0.116, p = 0.734** — far above the 0.01 threshold → **no SRM, randomization is intact.**
Covariate balance: control mean `pre_sessions_7d` 3.006 vs. treatment 2.961, **t-test
p = 0.188** — balanced.

**The teachable point — why a *high* p-value is the good outcome here.** This flips the
usual intuition. For SRM you *want* a high p-value: it means the observed split is
consistent with the expected 50/50. A *low* SRM p-value is the alarm. Being able to explain
that inversion cleanly is a strong signal of experimentation literacy.

---

## 8. Script 02 — Primary Metric (Conversion)

**File:** `02_primary_metric.R` · **Outputs:** `primary_metric_summary.csv`,
`primary_metric_results.csv`, `primary_metric_results_pretty.csv`

**What it does.** Conversion rate is the **primary decision metric**. The script:
1. Summarizes conversions and rate by variant.
2. Runs a **two-proportion z-test** — `stats::prop.test(x = c(conversions), n = c(totals),
   correct = FALSE)`. *(`correct = FALSE` turns off the Yates continuity correction so the
   test matches the standard large-sample two-proportion z-test.)*
3. Computes **absolute lift** (treatment rate − control rate, in percentage points),
   **relative lift** ((treatment/control) − 1), the **95% CI** for the difference, and
   **Cohen's h** (a standardized effect size for two proportions, computed manually as
   `2·asin(√p_treat) − 2·asin(√p_control)`).

*(One careful detail in the code: `prop.test`'s CI is for `p_control − p_treatment` by
default, so the script flips the signs to report the lift as `treatment − control` — the
direction stakeholders expect.)*

**Results:**

| Variant | n | Conversions | Rate |
|---|---|---|---|
| Control | 5,017 | 511 | 10.19% |
| Treatment | 4,983 | 574 | 11.52% |

**Absolute lift +1.33pp · relative lift +13.1% · 95% CI [0.11pp, 2.55pp] · p = 0.032 ·
Cohen's h = 0.043.**

**Key findings.** The +1.33pp observed lift is **close to the planted 1.5pp** (sampling
variability accounts for the gap) — the pipeline recovered the ground truth. The 95% CI
**excludes zero**, so it's significant at α = 0.05. Cohen's h ≈ 0.043 is a **small** effect
size — typical for product A/B tests.

**The teachable point.** Always report the **confidence interval alongside the p-value.**
The CI [0.11pp, 2.55pp] tells you the *range of plausible effects* — far more informative
than a binary "significant / not significant." And note the project distinguishes
**statistical** significance from **practical** significance: a +1.33pp lift on a 10%
baseline is ~13% relative, which *is* practically meaningful for an onboarding funnel.

---

## 9. Script 03 — Secondary Guardrail (Time-to-Complete)

**File:** `03_secondary_guardrails.R` · **Outputs:** `guardrail_time_*.csv`,
`figures/guardrail_time_to_complete.png`

**What a guardrail metric is.** A metric you check to make sure the treatment didn't cause
**unintended harm.** Even if conversion improves, if onboarding got *slower*, the user
experience degraded — possibly causing downstream churn that offsets the conversion win. A
guardrail "guards" against shipping a change that wins on the primary metric but loses
overall.

**What the script does — three complementary tests on the same question:**
1. **Welch t-test** — parametric, compares means.
2. **Wilcoxon rank-sum test** — non-parametric, robust if the distribution is skewed.
3. **Bootstrap CI** (B = 2,000) — distribution-free, resamples within each group to build a
   CI for the mean difference.
It also produces a box plot of time-to-complete by variant.

**Results:** Control mean **7.87 min**, Treatment **7.53 min** → **mean difference
−0.34 min** (treatment is faster). **Bootstrap CI [−0.46, −0.22]** (entirely below zero);
**t-test and Wilcoxon both p < 0.001.**

**Key findings.** The guardrail **improved** — treatment is both *more effective* (higher
conversion) *and* faster. All three methods agree, which is the point of running three:
when a parametric, a non-parametric, and a resampling method all converge, the result is
robust to distributional assumptions.

**The teachable point.** Using **multiple testing approaches** isn't redundancy — it's a
robustness check. If the t-test (which assumes roughly normal data) disagreed with the
Wilcoxon and bootstrap, you'd suspect the normality assumption. Agreement across all three
means the conclusion doesn't hinge on any one assumption.

---

## 10. Script 04 — Bootstrap & Permutation Inference

**File:** `04_bootstrap_permutation.R` · **Outputs:** `bootstrap_*.csv`, `permutation_*.csv`,
`infer_permutation_results.csv`, `figures/bootstrap_abs_lift.png`

**The purpose.** Re-derive the **primary conversion result** using **distribution-free**
(computational) inference — methods that don't rely on normality or large-sample
approximations. If these agree with the classical `prop.test`, the result is trustworthy.

**The two methods (both B = 4,000):**

- **Bootstrap CI.** Resample *with replacement* within each group, recompute the lift each
  time, repeat 4,000 times → a distribution of plausible lifts. The 2.5th and 97.5th
  percentiles are the 95% CI. It directly answers "what range of lifts is consistent with
  the data?"
- **Permutation test.** **Shuffle the variant labels** randomly, recompute the lift each
  time → this builds the **null distribution** (what lifts look like when there's *no real
  effect*, because the labels are now meaningless). The p-value is the fraction of permuted
  lifts as extreme as the observed lift. It directly answers "could this result be due to
  chance?"

The script also runs the **`infer` package** version of the permutation test as a clean
tidy-workflow cross-check.

**Results — three methods, one answer:**

| Method | p-value |
|---|---|
| `prop.test` (classical z-test) | 0.032 |
| Manual permutation (B = 4,000) | 0.036 |
| `infer` permutation (B = 4,000) | 0.033 |

**Bootstrap 95% CI: [+0.12pp, +2.57pp]** — essentially identical to the analytical CI from
`prop.test` ([+0.11pp, +2.55pp]).

**The teachable point — convergence is the evidence.** Three independent inference
approaches — a classical parametric test, a manual permutation test, and a packaged
permutation test — all land within 0.004 of each other on the p-value, and the bootstrap CI
matches the analytical CI. That **convergence is itself the finding**: the result is real,
not an artifact of one method's assumptions. The bootstrap histogram is also a great
stakeholder visual — "here's the lift across 4,000 resamples of your data."

---

## 11. Script 05 — Regression-Adjusted Effects (CUPED)

**File:** `05_regression_adjusted.R` · **Outputs:** `reg_conv_*.csv`, `reg_time_*.csv`

**What CUPED is.** **C**ontrolled-experiment **U**sing **P**re-**E**xperiment **D**ata —
the industry name for using a pre-experiment covariate to **reduce residual variance**,
which produces **tighter confidence intervals without needing more users.** It's standard
at Microsoft, Netflix, and Uber. The intuition: if you can explain away some of the
outcome's noise with a pre-experiment variable, the leftover noise is smaller, so the
treatment effect is estimated more precisely. *Free precision.*

**What the script does — two regressions:**

1. **Conversion (logistic regression).** `glm(converted ~ variant + log1p(pre_sessions_7d),
   family = binomial())`. Then it computes the **adjusted risk difference via marginal
   means (G-computation)**: predict each user's conversion probability *as if* they were
   control, then *as if* treatment, and average the difference. This converts the model's
   odds ratio into an interpretable **percentage-point lift**. A **bootstrap CI** (B =
   1,000) gives distribution-free uncertainty for that adjusted risk difference.
2. **Time-to-complete (OLS regression).** `lm(time_to_complete ~ variant +
   log1p(pre_sessions_7d))` — here the treatment coefficient *is* the adjusted mean
   difference directly.

Both use **HC3 robust standard errors** (`sandwich::vcovHC`) — heteroskedasticity-consistent
SEs that protect against non-constant error variance and mild model misspecification.

**Results:** Logistic model — treatment log-odds **+0.138**, **odds ratio 1.148** (95% CI
[1.012, 1.303]), p = 0.032. **Adjusted conversion lift = +1.33pp**, bootstrap CI
**[+0.25pp, +2.57pp]**. OLS model — treatment coefficient **−0.341 min** (95% CI
[−0.459, −0.224]), p < 0.001. The covariate `pre_sessions_7d` is **not significant** in
either model (p > 0.38).

**The teachable point.** The adjusted lift (+1.33pp) **matches the unadjusted estimate** —
adjustment *confirmed* rather than changed the conclusion, and the adjusted CI is slightly
**tighter** (lower bound +0.25 vs. +0.11). And here's the honest nuance: the covariate
turned out not to predict the outcome, so the precision gain was small — *expected* in a
clean simulation where randomization already balanced everything. In a real experiment with
a covariate that genuinely predicts the outcome, CUPED's variance reduction is much larger.
Knowing *why* the gain was small here is the sophisticated answer.

---

## 12. Script 06 — Power & MDE Analysis

**File:** `06_power_mde.R` · **Outputs:** `power_mde_summary_*.csv`,
`power_sample_size_requirements_*.csv`, `power_curve_*.csv`, `figures/power_curve.png`

**The purpose.** Power analysis answers the *pre-experiment* design question: **"given our
sample size, what is the smallest effect we can reliably detect?"** That smallest effect is
the **MDE — Minimum Detectable Effect.** If the MDE is *larger* than the effect you expect,
the experiment is **underpowered** and likely to come back inconclusive — a waste.

**What the script does:**
1. **MDE at the current sample size** — numerically searches for the smallest lift that
   `power.prop.test` says reaches **80% power** at α = 0.05, given ~4,983 users per group
   and the 10.19% observed baseline.
2. **Required sample sizes** — for target lifts of 0.5, 1.0, 1.5, 2.0 pp, computes the
   `n` per group needed for 80% power.
3. **A power curve** — power as a function of effect size, with the 80% target and the MDE
   marked.

**Results:** **MDE = 1.77pp** at 80% power. Sample-size requirements:

| Target lift | n per group | Total n |
|---|---|---|
| 0.5pp | 58,686 | 117,372 |
| 1.0pp | 14,981 | 29,962 |
| 1.5pp | 6,794 | 13,588 |
| 2.0pp | 3,898 | 7,796 |

**The most important — and most honest — finding.** The **MDE (1.77pp) is *larger* than the
observed lift (1.33pp)**. That means the experiment was **slightly underpowered** — at a
1.33pp true effect, the power was only ~55%, not 80%. It also explains *why* the p-value
(0.032) was significant but not overwhelming. The planted 1.5pp effect sits right at the
edge of detectability for this sample size.

**The teachable point — and the maturity signal.** A naive project reports "significant
result, ship it." This project does power analysis *and admits the experiment was
underpowered*. That's the sophisticated read: the result held up, but it was a close call,
and a properly powered re-test (or CUPED to lower the effective MDE) would give a more
decisive answer. Also note the sample-size table's lesson — **small effects demand huge
experiments**: detecting a 0.5pp lift needs ~12× the users of detecting a 2.0pp lift.

---

## 13. Key Results & The Ship Decision

Memorize the headline numbers.

| Metric | Result |
|---|---|
| Users | 10,000 (control 5,017 / treatment 4,983) |
| SRM check | chi-square p = **0.734** → no mismatch, randomization intact |
| Covariate balance | t-test p = 0.188 → balanced |
| Control conversion | **10.19%** (511/5,017) |
| Treatment conversion | **11.52%** (574/4,983) |
| **Primary result** | **+1.33pp absolute lift, +13.1% relative, p = 0.032**, 95% CI [0.11, 2.55] |
| Effect size | Cohen's h = 0.043 (small) |
| Guardrail (time) | −0.34 min (treatment faster), bootstrap CI [−0.46, −0.22], p < 0.001 |
| Bootstrap / permutation | CI [+0.12, +2.57]; permutation p = 0.036; infer p = 0.033 |
| Regression-adjusted lift | +1.33pp, bootstrap CI [+0.25, +2.57] |
| Power / MDE | MDE = **1.77pp** at 80% power (experiment slightly underpowered) |
| Ground truth recovered | planted +1.5pp / −0.5 min ✓ (observed +1.33pp / −0.34 min) |

**The decision: ship treatment with a staged ramp and monitoring gates.** The reasoning —
the primary metric improved and is statistically significant; the guardrail *also*
improved (no regression — the change is both more effective and faster); the result is
robust across five inference methods; regression adjustment confirmed it. The one caveat
that justifies a *staged* ramp rather than a full launch: the experiment was slightly
underpowered, so a phased rollout with monitoring de-risks the close call.

**The validation result.** The pipeline recovered the planted ground truth — observed
+1.33pp vs. planted +1.5pp, observed −0.34 min vs. planted −0.5 min — both within sampling
variability. The methodology is confirmed correct.

---

## 14. A/B Testing & Statistics Concepts to Know Cold

An interview for an analyst/DS role will probe these — this project is essentially a tour
of them.

**A/B test / randomized controlled experiment** — randomly split users into control and
treatment; randomization is what makes the measured difference *causal*.

**SRM (Sample Ratio Mismatch)** — the observed variant split deviating significantly from
the expected split; a sign the randomization or logging is broken. Tested with a chi-square
goodness-of-fit test. **You check it first, and a high p-value is the good outcome.**

**Primary metric vs. guardrail metric** — the primary metric is what the decision hinges on
(conversion); a guardrail metric is checked to make sure the treatment didn't cause
unintended harm (time-to-complete).

**Two-proportion z-test** — the standard test for comparing two binary rates; `prop.test`
in R.

**Absolute vs. relative lift** — absolute = treatment rate − control rate (in pp); relative
= (treatment/control) − 1 (in %). +1.33pp absolute = +13.1% relative on a ~10% baseline.

**Confidence interval** — the range of plausible values for the true effect; if a 95% CI
excludes zero, the result is significant at α = 0.05. Report it *with* the p-value.

**p-value** — the probability of seeing a result this extreme if the null (no effect) were
true; < 0.05 is the conventional significance threshold.

**Statistical vs. practical significance** — statistical = "unlikely to be chance";
practical = "big enough to matter for the business." Both must hold to ship.

**Effect size (Cohen's h)** — a standardized measure of how big a difference between two
proportions is, independent of sample size.

**Bootstrap** — resample the data *with replacement* many times to build a distribution of
a statistic; the percentiles give a distribution-free confidence interval.

**Permutation test** — shuffle the group labels many times to build the *null distribution*
(what the data looks like with no real effect); the p-value is how often a shuffled result
is as extreme as the observed one.

**Parametric vs. non-parametric** — parametric tests (t-test) assume a distribution;
non-parametric tests (Wilcoxon) don't. Running both is a robustness check.

**CUPED / regression adjustment** — using a *pre-experiment* covariate in a regression to
strip out outcome noise, producing tighter CIs without more users.

**G-computation / marginal means** — converting a model (e.g., a logistic regression's
odds ratio) into an interpretable average effect by predicting outcomes under each
treatment for everyone and averaging the difference.

**Robust (HC3) standard errors** — standard errors that stay valid when error variance is
not constant (heteroskedasticity).

**Statistical power** — the probability of detecting an effect that truly exists; the
convention is 80%.

**MDE (Minimum Detectable Effect)** — the smallest effect an experiment can detect at a
given power and sample size. If MDE > expected effect, the experiment is underpowered.

**Power analysis** — computing MDE or required sample size *before* running an experiment
to make sure it's worth running.

---

## 15. Limitations & Honest Caveats

Volunteer these — they show experimentation maturity.

1. **The data is simulated.** Real experiments are messier — non-compliance (users
   assigned to treatment who don't experience it), network effects, novelty/primacy bias,
   seasonality, outliers. The simulation is clean by construction; the *methodology* is the
   transferable asset, not the specific numbers.
2. **The experiment was slightly underpowered.** MDE (1.77pp) exceeded the observed lift
   (1.33pp) — power at the true effect was ~55%. The result held, but it was a close call.
3. **A single primary metric, no multiple-comparison correction.** Real experiments track
   several correlated metrics, which inflates the false-positive rate and needs a
   correction (Bonferroni, Benjamini-Hochberg). This pipeline analyzes one primary metric,
   so it doesn't need one — but a multi-metric version would.
4. **No heterogeneous treatment effects.** The analysis estimates one average effect; it
   doesn't check whether the lift differs by user segment (CATE analysis) — a noted future
   enhancement.
5. **No sequential testing.** The pipeline analyzes the experiment once at the end. Real
   platforms often use sequential / always-valid methods for safe early stopping.
6. **The `reports/ab_test_report.Rmd` is a template, not a finished report.** It contains
   placeholder text (`[X%]`, `[Ship/No-ship]`), commented-out code chunks, and even
   references a `revenue` column that isn't in the actual data. The real, completed analysis
   is the seven R scripts and the portfolio write-up — be aware of this if an interviewer
   opens the Rmd. (If you want the materials fully consistent, the Rmd would need to be
   filled in from the script outputs.)
7. **The covariate didn't help much.** `pre_sessions_7d` wasn't predictive of the outcome,
   so CUPED's precision gain was minimal here — a property of the clean simulation, not a
   flaw in the method.

---

## 16. Interview Q&A

Practice these out loud. Answers are written the way you'd actually speak.

**Q1. Walk me through this project.**
"It's a complete A/B testing pipeline in R — seven scripts that take a simulated SaaS
onboarding experiment from data generation to a ship decision. It compares a new onboarding
flow against the current one across 10,000 users. The scripts run in order: generate the
data, check randomization integrity with an SRM test, analyze the primary conversion
metric, check a guardrail metric, validate with bootstrap and permutation tests, refine
with regression adjustment, and finish with a power analysis. The data is simulated with a
known ground truth, so the pipeline can prove it recovers the right answer."

**Q2. Why simulate the data instead of using a real dataset?**
"Because it lets me *validate the analysis pipeline itself*. I planted a known effect — a
1.5 percentage-point conversion lift and a half-minute time reduction — so if my analysis
recovers those numbers, I've proven the methodology is correct. You can't do that with real
data, where you never know the true answer. It's actually how real experimentation
platforms are tested — teams at Microsoft and Netflix simulate experiments to verify their
analysis code before it touches a live test."

**Q3. What is SRM and why do you check it first?**
"SRM is Sample Ratio Mismatch — when the observed split between variants differs
significantly from what you expected, here 50/50. If you expected an even split and got
something off with a tiny p-value, the randomization or logging is broken — an assignment
bug, bot traffic, a redirect dropping users. I check it before looking at any results
because analyzing an experiment with a broken randomization is worse than analyzing nothing
— you'd make a confident, wrong decision. I used a chi-square goodness-of-fit test; it came
back p = 0.734, well clear, so the randomization was intact. And the script halts the whole
pipeline if SRM is detected."

**Q4. For SRM, why is a high p-value good? Isn't a low p-value usually what you want?**
"It's the opposite of the usual intuition, yes. For SRM, the null hypothesis is 'the split
is the expected 50/50.' A high p-value means the observed split is consistent with that —
the randomization is fine. A *low* p-value is the alarm: it says the split is
significantly off, so something's wrong. So here a high p-value is exactly what you want to
see."

**Q5. What's a guardrail metric?**
"A metric you check to make sure the treatment didn't cause unintended harm. My primary
metric was conversion — but even if conversion goes up, if the onboarding got slower, the
user experience degraded and that could drive downstream churn. So time-to-complete is the
guardrail. It came back improved — treatment was 0.34 minutes faster — so the change was
both more effective and faster. If the guardrail had regressed, I'd think hard before
shipping even with a conversion win."

**Q6. You used bootstrap and permutation tests — why, when you already had a z-test?**
"To validate the result without relying on distributional assumptions. The classical
two-proportion z-test is a large-sample approximation. The bootstrap resamples the data
with replacement to build a distribution-free confidence interval, and the permutation test
shuffles the variant labels to build the null distribution directly. The point is
convergence — my prop.test p-value was 0.032, the permutation test 0.036, the infer
permutation 0.033, and the bootstrap CI matched the analytical CI almost exactly. When
three independent methods agree that closely, the result isn't an artifact of any one
method's assumptions."

**Q7. Explain a permutation test in plain terms.**
"A permutation test answers 'could this result be due to chance?' The logic: if the
treatment had no real effect, the variant labels would be meaningless — you could shuffle
them and get a similar lift. So I shuffle the labels thousands of times, recompute the lift
each time, and that builds the null distribution — what lifts look like when there's
genuinely no effect. The p-value is the fraction of those shuffled lifts that are as
extreme as the one I actually observed. If almost none are, the real result is unlikely to
be chance."

**Q8. What is CUPED / regression adjustment, and did it help here?**
"CUPED is using a pre-experiment covariate in a regression to strip noise out of the
outcome, which tightens the confidence interval without needing more users — free
precision. I fit a logistic regression for conversion and an OLS for time, both adjusting
for pre-experiment sessions, with HC3 robust standard errors. The adjusted lift, 1.33
percentage points, matched the unadjusted estimate — so it confirmed the conclusion — and
the CI got slightly tighter. Honestly, the gain was small here, because in my clean
simulation the covariate didn't actually predict the outcome. In a real experiment with a
covariate that genuinely correlates with the outcome, CUPED's variance reduction is much
bigger."

**Q9. How did you convert a logistic regression into a percentage-point lift?**
"A logistic regression gives you an odds ratio, which stakeholders don't intuitively
understand. So I used G-computation, also called marginal means: I predict every user's
conversion probability as if they were in control, then again as if they were in
treatment, and average the difference. That turns the model into an adjusted risk
difference in percentage points — a '1.33pp lift' instead of an 'odds ratio of 1.148.'"

**Q10. Your result was significant — why does the power analysis still matter?**
"Because it told me the experiment was slightly underpowered. The minimum detectable effect
at 80% power was 1.77 percentage points, but the observed lift was only 1.33 — so at the
true effect size, my power was closer to 55%. The result held up, but it was a close call,
and that's exactly why my recommendation was a *staged* ramp with monitoring rather than a
full launch. Power analysis also tells you how to design the next experiment — to reliably
detect a half-point lift, I'd need almost 60,000 users per group."

**Q11. What's the difference between statistical and practical significance?**
"Statistical significance means the result is unlikely to be chance — my p-value of 0.032
clears that. Practical significance means the effect is big enough to matter to the
business. My lift was 1.33 percentage points on a 10% baseline — about a 13% relative
improvement — which for an onboarding funnel is genuinely meaningful; at 100,000 annual
signups that's over 1,300 extra conversions a year. You need both: a statistically
significant but tiny effect isn't worth shipping, and a large effect that isn't
significant isn't trustworthy."

**Q12. What was your final recommendation and why?**
"Ship the treatment, but with a staged ramp and monitoring gates. The reasoning: the
primary metric improved significantly, the guardrail also improved so there's no
regression, the result was robust across five different inference methods, and regression
adjustment confirmed it. The one reason for a staged rollout rather than a full launch is
that the experiment was slightly underpowered — a phased ramp with monitoring de-risks that
close call."

**Q13. What would you add to make this more like a real experiment analysis?**
"A few things. Multiple-comparison correction once there's more than one metric. A
heterogeneous-treatment-effects analysis — does the lift differ by user segment. Sequential
testing so the experiment could be stopped early safely. And I'd actually fill in the
R Markdown report — right now it's a template scaffold; the finished analysis lives in the
seven scripts."

---

## 17. How to Walk Through This Project Live

If asked to screen-share, use this order:

1. **State the structure and the order** — "seven scripts, run 00 to 06, and the *order is
   the methodology*: integrity check before results, primary before guardrail, validate
   before trusting, then refine and assess power."
2. **Script 00** — explain the simulated data with a *known ground truth* and why that
   makes the pipeline self-validating.
3. **Script 01 — spend real time here.** SRM is the signature concept. Explain what it is,
   why it's first, why a high p-value is the good outcome, and that the pipeline *halts* if
   SRM is detected.
4. **Script 02** — the primary result: +1.33pp, p = 0.032, and the CI. Make the
   statistical-vs-practical-significance point.
5. **Script 03** — the guardrail; explain *why* a guardrail exists and that you ran three
   tests as a robustness check.
6. **Script 04** — bootstrap and permutation; the headline is *convergence* across five
   methods.
7. **Script 05** — CUPED; explain variance reduction and G-computation, and be honest the
   gain was small here.
8. **Script 06 — close with the honest finding** — the experiment was slightly
   underpowered (MDE 1.77 > observed 1.33). End on the staged-ramp recommendation.

**Pacing tip:** spend the most time on SRM (Script 01), the inference convergence (Script
04), and the power analysis (Script 06). Those three — checking integrity first, validating
with multiple methods, and honestly assessing power — are what separate a rigorous
experiment analysis from "I ran a t-test."

---

## 18. Glossary

- **A/B test** — a randomized controlled experiment comparing two variants.
- **Control / treatment** — the unchanged baseline group / the group receiving the new
  experience.
- **Variant** — which group a user was assigned to.
- **SRM (Sample Ratio Mismatch)** — the observed variant split deviating significantly from
  the expected split; an integrity alarm.
- **Chi-square goodness-of-fit test** — the test used to detect SRM (observed vs. expected
  counts).
- **Covariate balance** — whether a pre-experiment variable is evenly distributed across
  variants (it should be, under good randomization).
- **`pre_sessions_7d`** — the pre-experiment engagement covariate; enables CUPED.
- **Primary metric** — the metric the ship decision depends on (conversion).
- **Guardrail metric** — a metric checked to ensure no unintended harm (time-to-complete).
- **Conversion rate** — the share of users who completed the target action.
- **Absolute lift** — treatment rate − control rate, in percentage points.
- **Relative lift** — (treatment rate / control rate) − 1, in percent.
- **Two-proportion z-test** — the standard test for comparing two binary rates
  (`prop.test`).
- **Confidence interval (CI)** — the plausible range for the true effect; excludes zero ⇒
  significant.
- **p-value** — the probability of a result this extreme under the null hypothesis.
- **Cohen's h** — a standardized effect size for the difference between two proportions.
- **Statistical significance** — the result is unlikely to be chance (p < α).
- **Practical significance** — the effect is large enough to matter to the business.
- **Welch t-test** — a two-sample t-test that doesn't assume equal variances.
- **Wilcoxon rank-sum test** — a non-parametric two-group comparison (no distribution
  assumption).
- **Bootstrap** — resampling with replacement to build a distribution-free confidence
  interval.
- **Permutation test** — shuffling group labels to build the null distribution and a
  p-value.
- **Parametric vs. non-parametric** — assumes a distribution vs. does not.
- **CUPED** — Controlled-experiment Using Pre-Experiment Data; regression adjustment for
  variance reduction.
- **Regression adjustment** — adding covariates to a model to tighten the effect estimate.
- **Logistic regression (GLM)** — a model for a binary outcome (`converted`).
- **OLS regression** — ordinary least squares; a model for a continuous outcome (time).
- **Odds ratio** — the multiplicative change in odds from a logistic regression coefficient.
- **G-computation / marginal means** — predicting outcomes under each treatment for everyone
  and averaging to get an interpretable average effect.
- **Adjusted risk difference** — the regression-adjusted treatment effect expressed in
  percentage points.
- **HC3 robust standard errors** — heteroskedasticity-consistent SEs (the `sandwich`
  package).
- **Statistical power** — the probability of detecting a real effect; convention is 80%.
- **MDE (Minimum Detectable Effect)** — the smallest effect detectable at a given power and
  sample size.
- **Underpowered** — when the MDE exceeds the effect you're trying to detect.
- **Power curve** — power plotted against effect size.
- **Ground truth** — the known true effect planted in the simulated data.
- **`set.seed(123)`** — fixes R's random number generator so results are reproducible.

---

*This study guide documents the project as built. The authoritative references are the
seven R scripts in `R/` (the actual analysis code), the result tables in `tables/`, the
figures in `figures/`, and the portfolio page `index.md`. The `reports/ab_test_report.Rmd`
is a template skeleton, not a finished report. When this guide and the scripts disagree,
the scripts win.*