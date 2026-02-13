# 02_primary_metric.R
# Purpose: Analyze the primary metric (conversion rate)
# - Summarize conversion by group
# - Two-proportion z-test (stats::prop.test)
# - Absolute + relative lift
# - 95% CI for absolute lift (difference in proportions)
# - Effect size (Cohen's h) computed manually
# - Save outputs to tables/

library(tidyverse)
library(broom)

message("Running primary metric analysis (conversion)...")

# ----------------------------
# Load data
# ----------------------------
infile <- "data/ab_test_data.csv"
stopifnot(file.exists(infile))

df <- readr::read_csv(infile, show_col_types = FALSE) %>%
  janitor::clean_names()

required_cols <- c("variant", "converted")
missing <- setdiff(required_cols, names(df))
if (length(missing) > 0) stop("Missing required columns: ", paste(missing, collapse = ", "))

df <- df %>%
  mutate(
    variant = as.character(variant),
    converted = as.integer(converted)
  )

# ----------------------------
# Summary by group
# ----------------------------
summary_tbl <- df %>%
  group_by(variant) %>%
  summarise(
    n = n(),
    conversions = sum(converted),
    conversion_rate = mean(converted),
    .groups = "drop"
  ) %>%
  arrange(variant)

if (!all(c("control", "treatment") %in% summary_tbl$variant)) {
  stop("Expected variants 'control' and 'treatment' not found. Found: ",
       paste(summary_tbl$variant, collapse = ", "))
}

p_control <- summary_tbl %>% filter(variant == "control") %>% pull(conversion_rate)
p_treat   <- summary_tbl %>% filter(variant == "treatment") %>% pull(conversion_rate)

n_control <- summary_tbl %>% filter(variant == "control") %>% pull(n)
n_treat   <- summary_tbl %>% filter(variant == "treatment") %>% pull(n)

x_control <- summary_tbl %>% filter(variant == "control") %>% pull(conversions)
x_treat   <- summary_tbl %>% filter(variant == "treatment") %>% pull(conversions)

abs_lift <- p_treat - p_control
rel_lift <- (p_treat / p_control) - 1

# ----------------------------
# Two-proportion test (force stats namespace)
# Order: control, treatment
# stats::prop.test CI is for (p_control - p_treat) by default, so we flip to (treat - control)
# ----------------------------
pt <- stats::prop.test(
  x = c(x_control, x_treat),
  n = c(n_control, n_treat),
  correct = FALSE
)

ci_control_minus_treat <- pt$conf.int
ci_abs_lift <- c(
  low  = -ci_control_minus_treat[2],
  high = -ci_control_minus_treat[1]
)

# ----------------------------
# Cohen's h (manual)
# h = 2*asin(sqrt(p1)) - 2*asin(sqrt(p2))
# We'll do: treatment vs control
# ----------------------------
cohens_h <- 2 * asin(sqrt(p_treat)) - 2 * asin(sqrt(p_control))

# ----------------------------
# Assemble results
# ----------------------------
results_tbl <- tibble(
  metric = "conversion_rate",
  p_control = p_control,
  p_treatment = p_treat,
  absolute_lift = abs_lift,
  relative_lift = rel_lift,
  ci_low = ci_abs_lift["low"],
  ci_high = ci_abs_lift["high"],
  p_value = unname(pt$p.value),
  cohens_h = unname(cohens_h)
)

results_pretty <- results_tbl %>%
  mutate(
    p_control_pct = scales::percent(p_control, accuracy = 0.1),
    p_treatment_pct = scales::percent(p_treatment, accuracy = 0.1),
    absolute_lift_pp = round(absolute_lift * 100, 2),
    relative_lift_pct = round(relative_lift * 100, 2),
    ci_low_pp = round(ci_low * 100, 2),
    ci_high_pp = round(ci_high * 100, 2)
  )

# ----------------------------
# Save outputs
# ----------------------------
readr::write_csv(summary_tbl, "tables/primary_metric_summary.csv")
readr::write_csv(results_tbl, "tables/primary_metric_results.csv")
readr::write_csv(results_pretty, "tables/primary_metric_results_pretty.csv")

message("Primary metric analysis complete. Outputs saved to tables/.")
message(sprintf(
  "Control: %.3f | Treatment: %.3f | Abs lift: %.4f | p-value: %.4g",
  p_control, p_treat, abs_lift, pt$p.value
))
