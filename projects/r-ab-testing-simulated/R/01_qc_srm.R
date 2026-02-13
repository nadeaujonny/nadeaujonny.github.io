# 01_qc_srm.R
# Purpose: Data quality checks + Sample Ratio Mismatch (SRM) detection
# - Verifies randomization assignment split (expected 50/50)
# - Checks baseline covariate balance between groups
# - Saves QC outputs to tables/
# - Stops pipeline if SRM is detected

library(tidyverse)
library(broom)
library(janitor)

message("Running QC + SRM checks...")

# ----------------------------
# Load data
# ----------------------------
infile <- "data/ab_test_data.csv"
stopifnot(file.exists(infile))

df <- readr::read_csv(infile, show_col_types = FALSE) %>%
  janitor::clean_names()

# Basic schema checks (fail fast if missing)
required_cols <- c("user_id", "variant", "pre_sessions_7d", "converted", "time_to_complete")
missing <- setdiff(required_cols, names(df))
if (length(missing) > 0) stop("Missing required columns: ", paste(missing, collapse = ", "))

# ----------------------------
# SRM test (expected 50/50)
# ----------------------------
counts <- df %>%
  count(variant) %>%
  arrange(variant) %>%
  mutate(expected_prop = 1 / n_distinct(df$variant),
         expected_n = nrow(df) * expected_prop,
         observed_prop = n / sum(n))

chisq <- chisq.test(x = counts$n, p = counts$expected_prop)

srm_result <- tibble(
  n_total = nrow(df),
  groups = paste(sort(unique(df$variant)), collapse = " vs "),
  chisq_stat = unname(chisq$statistic),
  df = unname(chisq$parameter),
  p_value = unname(chisq$p.value)
)

# Save SRM outputs
readr::write_csv(counts, "tables/qc_srm_group_counts.csv")
readr::write_csv(srm_result, "tables/qc_srm_test.csv")

message(sprintf("SRM chi-square p-value: %.6f", srm_result$p_value))

# Fail loudly if SRM detected (use 0.01 as a strong SRM flag)
if (srm_result$p_value < 0.01) {
  stop("SRM detected (p < 0.01). Investigate randomization / logging before proceeding.")
}

# ----------------------------
# Baseline covariate balance (pre_sessions_7d)
# ----------------------------
balance_summary <- df %>%
  group_by(variant) %>%
  summarise(
    n = n(),
    mean_pre_sessions = mean(pre_sessions_7d),
    sd_pre_sessions = sd(pre_sessions_7d),
    median_pre_sessions = median(pre_sessions_7d),
    .groups = "drop"
  )

# Simple two-sample t-test for baseline covariate balance
# (In real experiments you'd also look at standardized mean differences)
tt <- t.test(pre_sessions_7d ~ variant, data = df)

balance_test <- broom::tidy(tt) %>%
  transmute(
    estimate_diff = estimate,         # difference in means
    conf_low = conf.low,
    conf_high = conf.high,
    p_value = p.value,
    method = method
  )

# Save baseline balance outputs
readr::write_csv(balance_summary, "tables/qc_baseline_balance_summary.csv")
readr::write_csv(balance_test, "tables/qc_baseline_balance_test.csv")

message("QC + SRM checks complete. Outputs saved to tables/.")
