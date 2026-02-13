# 04_bootstrap_permutation.R
# Purpose: Bootstrap CI + permutation test for conversion lift
# Compares modern inference vs classical prop.test result
# Outputs: tables/ + figures/

set.seed(123)

library(tidyverse)
library(broom)
library(infer)
library(janitor)
library(scales)

message("Running bootstrap + permutation inference for conversion...")

# ----------------------------
# Paths + setup
# ----------------------------
infile <- "data/ab_test_data.csv"
stopifnot(file.exists(infile))

if (!dir.exists("tables")) dir.create("tables", recursive = TRUE)
if (!dir.exists("figures")) dir.create("figures", recursive = TRUE)

# ----------------------------
# Load data
# ----------------------------
df <- readr::read_csv(infile, show_col_types = FALSE) %>%
  janitor::clean_names() %>%
  mutate(
    variant       = factor(variant),
    converted_num = as.integer(converted),                 # 0/1 numeric for math
    converted_fct = factor(converted_num, levels = c(0, 1))# factor for infer
  )

# Sanity checks
required_cols <- c("variant", "converted_num", "converted_fct")
missing <- setdiff(required_cols, names(df))
if (length(missing) > 0) stop("Missing required columns: ", paste(missing, collapse = ", "))

if (n_distinct(df$variant) < 2) stop("variant must have 2+ levels (control/treatment).")
if (!all(sort(unique(df$converted_num)) %in% c(0, 1))) stop("converted must be 0/1.")
if (any(is.na(df$variant)) || any(is.na(df$converted_num))) stop("variant/converted contain NA.")

# Ensure expected ordering if present
# (Not required, but helps consistent reporting)
if (all(c("control", "treatment") %in% levels(df$variant))) {
  df <- df %>% mutate(variant = fct_relevel(variant, "control", "treatment"))
}

# ----------------------------
# Observed summary
# ----------------------------
summary_tbl <- df %>%
  group_by(variant) %>%
  summarise(
    n = n(),
    x = sum(converted_num),
    p = mean(converted_num),
    .groups = "drop"
  )

# Pull observed stats
p_control <- summary_tbl %>% filter(variant == levels(df$variant)[1]) %>% pull(p)
p_treat   <- summary_tbl %>% filter(variant == levels(df$variant)[2]) %>% pull(p)
x_control <- summary_tbl %>% filter(variant == levels(df$variant)[1]) %>% pull(x)
x_treat   <- summary_tbl %>% filter(variant == levels(df$variant)[2]) %>% pull(x)
n_control <- summary_tbl %>% filter(variant == levels(df$variant)[1]) %>% pull(n)
n_treat   <- summary_tbl %>% filter(variant == levels(df$variant)[2]) %>% pull(n)

obs_diff <- p_treat - p_control  # absolute lift (treat - control)

# ----------------------------
# Classical test (prop.test)
# ----------------------------
prop_test <- prop.test(
  x = c(x_control, x_treat),
  n = c(n_control, n_treat),
  correct = FALSE
)

prop_tidy <- broom::tidy(prop_test) %>%
  mutate(
    method = "prop.test (two-proportion z-test approx)",
    p_control = p_control,
    p_treat = p_treat,
    abs_lift = obs_diff
  )

# ----------------------------
# Bootstrap CI for absolute lift
# ----------------------------
B <- 4000

control_rows <- df %>% filter(variant == levels(df$variant)[1])
treat_rows   <- df %>% filter(variant == levels(df$variant)[2])

boot_diffs <- replicate(B, {
  p_c <- mean(sample(control_rows$converted_num, size = nrow(control_rows), replace = TRUE))
  p_t <- mean(sample(treat_rows$converted_num,   size = nrow(treat_rows),   replace = TRUE))
  p_t - p_c
})

boot_ci <- quantile(boot_diffs, probs = c(0.025, 0.975), names = FALSE)

boot_results <- tibble(
  B = B,
  p_control = p_control,
  p_treat = p_treat,
  abs_lift = obs_diff,
  ci_low = boot_ci[1],
  ci_high = boot_ci[2]
)

# Optional: save full bootstrap distribution (nice for portfolio)
boot_dist_tbl <- tibble(boot_diff = boot_diffs)

# ----------------------------
# Permutation test for absolute lift
# ----------------------------
# Shuffle variant labels, recompute diff each time
perm_diffs <- replicate(B, {
  df_perm <- df %>%
    mutate(variant_perm = sample(variant, size = n(), replace = FALSE))
  
  p_c <- df_perm %>%
    filter(variant_perm == levels(df$variant)[1]) %>%
    summarise(p = mean(converted_num)) %>%
    pull(p)
  
  p_t <- df_perm %>%
    filter(variant_perm == levels(df$variant)[2]) %>%
    summarise(p = mean(converted_num)) %>%
    pull(p)
  
  p_t - p_c
})

# Two-sided p-value
perm_p_value <- mean(abs(perm_diffs) >= abs(obs_diff))

perm_results <- tibble(
  B = B,
  observed_abs_lift = obs_diff,
  perm_p_value_two_sided = perm_p_value
)

perm_dist_tbl <- tibble(perm_diff = perm_diffs)

# ----------------------------
# (Optional) infer version (same idea, cleaner API)
# ----------------------------
# This is mainly for demonstration; results should align with perm_results
infer_perm_p <- df %>%
  infer::specify(converted_fct ~ variant, success = "1") %>%
  infer::hypothesize(null = "independence") %>%
  infer::generate(reps = B, type = "permute") %>%
  infer::calculate(stat = "diff in props", order = c(levels(df$variant)[2], levels(df$variant)[1])) %>%
  infer::get_p_value(
    obs_stat = obs_diff,
    direction = "two_sided"
  ) %>%
  dplyr::pull(p_value)

infer_results <- tibble(
  B = B,
  observed_abs_lift = obs_diff,
  infer_perm_p_value_two_sided = infer_perm_p
)

# ----------------------------
# Plot: bootstrap distribution (absolute lift)
# ----------------------------
boot_plot <- ggplot(boot_dist_tbl, aes(x = boot_diff)) +
  geom_histogram(bins = 40) +
  geom_vline(xintercept = obs_diff, linetype = "dashed") +
  labs(
    title = "Bootstrap distribution: absolute lift (treatment - control)",
    x = "Absolute lift",
    y = "Count"
  )

ggsave(
  filename = "figures/bootstrap_abs_lift.png",
  plot = boot_plot,
  width = 9,
  height = 5,
  dpi = 200
)

# ----------------------------
# Save outputs
# ----------------------------
readr::write_csv(summary_tbl,      "tables/bootstrap_perm_summary.csv")
readr::write_csv(prop_tidy,        "tables/bootstrap_perm_prop_test.csv")
readr::write_csv(boot_results,     "tables/bootstrap_results.csv")
readr::write_csv(boot_dist_tbl,    "tables/bootstrap_distribution.csv")
readr::write_csv(perm_results,     "tables/permutation_results.csv")
readr::write_csv(perm_dist_tbl,    "tables/permutation_distribution.csv")
readr::write_csv(infer_results,    "tables/infer_permutation_results.csv")

message("Bootstrap + permutation complete. Outputs saved to tables/ and figures/.")
message(
  "Control: ", percent(p_control, accuracy = 0.1),
  " | Treatment: ", percent(p_treat, accuracy = 0.1),
  " | Abs lift: ", round(obs_diff, 4),
  " | prop.test p: ", signif(prop_tidy$p.value[1], 4),
  " | perm p: ", signif(perm_p_value, 4)
)
