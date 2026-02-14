# ------------------------------------------------------------
# 06_power_mde.R
# Power + MDE analysis for primary metric (conversion rate)
# ------------------------------------------------------------

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

set.seed(123)

# ---- Paths ----
data_path  <- "data/ab_test_data.csv"
tables_dir <- "tables"
figures_dir <- "figures"

if (!dir.exists(tables_dir))  dir.create(tables_dir, recursive = TRUE)
if (!dir.exists(figures_dir)) dir.create(figures_dir, recursive = TRUE)

# ---- Load ----
df <- read_csv(data_path, show_col_types = FALSE)

# ---- Defensive checks ----
required_cols <- c("variant", "converted")
missing_cols <- setdiff(required_cols, names(df))
stopifnot(length(missing_cols) == 0)
stopifnot(all(df$converted %in% c(0, 1)))

df <- df %>%
  mutate(variant = factor(variant, levels = c("control", "treatment")))

stamp <- format(Sys.time(), "%Y%m%d_%H%M%S")

# ------------------------------------------------------------
# Inputs (edit if you want scenario analysis)
# ------------------------------------------------------------
alpha <- 0.05
power_target <- 0.80
alternative <- "two.sided"  # keep consistent with prop.test

# Baseline conversion from observed control group
p0 <- df %>% filter(variant == "control") %>% summarise(p = mean(converted)) %>% pull(p)

# Sample size per group from observed data (balanced)
n0 <- df %>% filter(variant == "control") %>% summarise(n = n()) %>% pull(n)
n1 <- df %>% filter(variant == "treatment") %>% summarise(n = n()) %>% pull(n)

# Use the smaller group size for conservative MDE
n_per_group <- min(n0, n1)

# ------------------------------------------------------------
# 1) MDE given current sample size
# ------------------------------------------------------------
# We solve for p1 such that power.prop.test achieves desired power.
# Use a simple numeric search over possible lifts.

mde_solver <- function(p0, n, alpha, power_target, alternative) {
  # search lifts from tiny to 10pp (0.001 to 0.10)
  lifts <- seq(0.0005, 0.10, by = 0.0001)
  
  achieved_power <- sapply(lifts, function(d) {
    p1 <- min(max(p0 + d, 0), 1)
    out <- power.prop.test(
      n = n,
      p1 = p0,
      p2 = p1,
      sig.level = alpha,
      alternative = alternative
    )
    out$power
  })
  
  idx <- which(achieved_power >= power_target)[1]
  if (is.na(idx)) return(NA_real_)
  lifts[idx]
}

mde_abs <- mde_solver(p0, n_per_group, alpha, power_target, alternative)  # absolute lift (prob)
mde_pp <- mde_abs * 100

mde_summary <- tibble(
  baseline_rate = p0,
  n_per_group = n_per_group,
  alpha = alpha,
  target_power = power_target,
  mde_abs = mde_abs,
  mde_pp = mde_pp
)

# ------------------------------------------------------------
# 2) Required sample size for common target lifts
# ------------------------------------------------------------
target_lifts_pp <- c(0.5, 1.0, 1.5, 2.0)   # percentage points
target_lifts_abs <- target_lifts_pp / 100

sample_size_table <- lapply(target_lifts_abs, function(d) {
  p1 <- min(max(p0 + d, 0), 1)
  
  out <- power.prop.test(
    power = power_target,
    p1 = p0,
    p2 = p1,
    sig.level = alpha,
    alternative = alternative
  )
  
  tibble(
    baseline_rate = p0,
    target_lift_pp = d * 100,
    target_p2 = p1,
    alpha = alpha,
    target_power = power_target,
    n_per_group_required = ceiling(out$n),
    total_sample_required = 2 * ceiling(out$n)
  )
}) %>% bind_rows()

# ------------------------------------------------------------
# 3) Optional: power curve around observed sample size
# ------------------------------------------------------------
# Show how power changes for a range of lifts given current n
power_curve_lifts_pp <- seq(0.0, 3.0, by = 0.1)
power_curve <- tibble(
  lift_pp = power_curve_lifts_pp,
  power = sapply(power_curve_lifts_pp / 100, function(d) {
    p1 <- min(max(p0 + d, 0), 1)
    power.prop.test(
      n = n_per_group,
      p1 = p0,
      p2 = p1,
      sig.level = alpha,
      alternative = alternative
    )$power
  })
)

library(ggplot2)

ggplot(power_curve, aes(x = lift_pp, y = power)) +
  geom_line(linewidth = 1.2, color = "steelblue") +
  geom_hline(yintercept = 0.80, linetype = "dashed", color = "red") +
  annotate("text", x = 2.5, y = 0.82, label = "80% Power Target", color = "red") +
  geom_vline(xintercept = mde_pp, linetype = "dotted", color = "darkgreen") +
  annotate("text", x = mde_pp + 0.15, y = 0.5,
           label = paste0("MDE: ", round(mde_pp, 2), "pp"),
           color = "darkgreen", hjust = 0) +
  labs(
    title = "Statistical Power by Effect Size",
    subtitle = paste0("Baseline: ", round(p0 * 100, 1), "% | n per group: ", n_per_group),
    x = "Absolute Lift (percentage points)",
    y = "Power"
  ) +
  theme_minimal(base_size = 12)

ggsave("figures/power_curve.png", width = 9, height = 5, dpi = 200)

# ------------------------------------------------------------
# Save outputs
# ------------------------------------------------------------
write_csv(mde_summary, file.path(tables_dir, paste0("power_mde_summary_", stamp, ".csv")))
write_csv(sample_size_table, file.path(tables_dir, paste0("power_sample_size_requirements_", stamp, ".csv")))
write_csv(power_curve, file.path(tables_dir, paste0("power_curve_", stamp, ".csv")))

# ------------------------------------------------------------
# 4) Power curve visualization
# ------------------------------------------------------------
library(ggplot2)

ggplot(power_curve, aes(x = lift_pp, y = power)) +
  geom_line(linewidth = 1.2, color = "steelblue") +
  geom_hline(yintercept = 0.80, linetype = "dashed", color = "red") +
  annotate("text", x = 2.5, y = 0.82, label = "80% Power Target", color = "red") +
  geom_vline(xintercept = mde_pp, linetype = "dotted", color = "darkgreen") +
  annotate("text", x = mde_pp + 0.15, y = 0.5,
           label = paste0("MDE: ", round(mde_pp, 2), "pp"),
           color = "darkgreen", hjust = 0) +
  labs(
    title = "Statistical Power by Effect Size",
    subtitle = paste0("Baseline: ", round(p0 * 100, 1), "% | n per group: ", n_per_group),
    x = "Absolute Lift (percentage points)",
    y = "Power"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(figures_dir, "power_curve.png"), width = 9, height = 5, dpi = 200)

message("Script 06 complete.")
message("Saved tables to /tables/:")
message(" - power_mde_summary_*")
message(" - power_sample_size_requirements_*")
message(" - power_curve_*")
message("Saved figures to /figures/:")
message(" - power_curve.png")
