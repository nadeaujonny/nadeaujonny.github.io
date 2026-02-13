# 03_secondary_guardrails.R
# Purpose: Analyze secondary / guardrail metric (time_to_complete)
# - Summarize time-to-complete by group
# - Compare groups with t-test + nonparametric Wilcoxon
# - Bootstrap CI for mean difference (optional but nice)
# - Save outputs to tables/ and a figure to figures/

library(tidyverse)
library(broom)

message("Running secondary/guardrail metric analysis (time_to_complete)...")

# ----------------------------
# Load data
# ----------------------------
infile <- "data/ab_test_data.csv"
stopifnot(file.exists(infile))

df <- readr::read_csv(infile, show_col_types = FALSE) %>%
  janitor::clean_names()

required_cols <- c("variant", "time_to_complete")
missing <- setdiff(required_cols, names(df))
if (length(missing) > 0) stop("Missing required columns: ", paste(missing, collapse = ", "))

df <- df %>%
  mutate(
    variant = as.character(variant),
    time_to_complete = as.numeric(time_to_complete)
  ) %>%
  filter(!is.na(time_to_complete))

# ----------------------------
# Summary
# ----------------------------
summary_tbl <- df %>%
  group_by(variant) %>%
  summarise(
    n = n(),
    mean_time = mean(time_to_complete),
    median_time = median(time_to_complete),
    sd_time = sd(time_to_complete),
    p90_time = quantile(time_to_complete, 0.90),
    .groups = "drop"
  ) %>%
  arrange(variant)

# Ensure expected groups
if (!all(c("control", "treatment") %in% summary_tbl$variant)) {
  stop("Expected variants 'control' and 'treatment' not found. Found: ",
       paste(summary_tbl$variant, collapse = ", "))
}

mean_control <- summary_tbl %>% filter(variant == "control") %>% pull(mean_time)
mean_treat   <- summary_tbl %>% filter(variant == "treatment") %>% pull(mean_time)
diff_mean    <- mean_treat - mean_control  # negative = faster onboarding in treatment

# ----------------------------
# Tests
# ----------------------------
tt <- t.test(time_to_complete ~ variant, data = df)
tt_tidy <- broom::tidy(tt) %>%
  mutate(test = "t_test")

wt <- wilcox.test(time_to_complete ~ variant, data = df, exact = FALSE)
wt_tidy <- broom::tidy(wt) %>%
  mutate(test = "wilcoxon")

tests_tbl <- bind_rows(tt_tidy, wt_tidy)

# ----------------------------
# Simple bootstrap CI for mean difference
# ----------------------------
set.seed(123)
B <- 2000

boot_diffs <- replicate(B, {
  boot_df <- df %>%
    group_by(variant) %>%
    slice_sample(prop = 1, replace = TRUE) %>%
    ungroup()
  
  m_c <- mean(boot_df$time_to_complete[boot_df$variant == "control"])
  m_t <- mean(boot_df$time_to_complete[boot_df$variant == "treatment"])
  m_t - m_c
})

boot_ci <- quantile(boot_diffs, probs = c(0.025, 0.975))

results_tbl <- tibble(
  metric = "time_to_complete",
  mean_control = mean_control,
  mean_treatment = mean_treat,
  mean_diff_treat_minus_control = diff_mean,
  boot_ci_low = boot_ci[[1]],
  boot_ci_high = boot_ci[[2]],
  t_test_p_value = tt$p.value,
  wilcoxon_p_value = wt$p.value
)

# ----------------------------
# Figure (distribution + means)
# ----------------------------
p <- df %>%
  mutate(variant = factor(variant, levels = c("control", "treatment"))) %>%
  ggplot(aes(x = variant, y = time_to_complete)) +
  geom_boxplot(outlier.alpha = 0.2) +
  geom_jitter(width = 0.15, alpha = 0.08) +
  labs(
    title = "Onboarding Time-to-Complete by Variant",
    subtitle = "Guardrail metric: lower is better (faster onboarding)",
    x = NULL,
    y = "Time to complete onboarding (minutes)"
  ) +
  theme_minimal(base_size = 12)

ggsave("figures/guardrail_time_to_complete.png", p, width = 8, height = 5, dpi = 200)

# ----------------------------
# Save outputs
# ----------------------------
readr::write_csv(summary_tbl, "tables/guardrail_time_summary.csv")
readr::write_csv(tests_tbl, "tables/guardrail_time_tests.csv")
readr::write_csv(results_tbl, "tables/guardrail_time_results.csv")

message("Secondary/guardrail analysis complete. Outputs saved to tables/ and figures/.")
message(sprintf(
  "Mean control: %.2f | Mean treatment: %.2f | Diff (treat-control): %.2f | t-test p=%.4g",
  mean_control, mean_treat, diff_mean, tt$p.value
))
