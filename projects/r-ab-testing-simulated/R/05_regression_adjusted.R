# ------------------------------------------------------------
# 05_regression_adjusted.R
# Regression-adjusted treatment effects (conversion + guardrail)
# Robust SEs computed directly (no lmtest/coeftest dependency)
# ------------------------------------------------------------

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(sandwich)
})

set.seed(123)

# ---- Paths ----
data_path   <- "data/ab_test_data.csv"
tables_dir  <- "tables"
figures_dir <- "figures"

if (!dir.exists(tables_dir))  dir.create(tables_dir, recursive = TRUE)
if (!dir.exists(figures_dir)) dir.create(figures_dir, recursive = TRUE)

# ---- Load ----
df <- read_csv(data_path, show_col_types = FALSE)

# ---- Defensive checks ----
required_cols <- c("variant", "converted", "time_to_complete", "pre_sessions_7d")
missing_cols <- setdiff(required_cols, names(df))
stopifnot(length(missing_cols) == 0)

stopifnot(all(df$converted %in% c(0, 1)))
stopifnot(is.numeric(df$time_to_complete))
stopifnot(is.numeric(df$pre_sessions_7d))

# ---- Clean / factor handling ----
df <- df %>%
  mutate(
    variant = factor(variant, levels = c("control", "treatment")),
    log1p_pre_sessions_7d = log1p(pre_sessions_7d)
  )

# Optional covariates (script won’t break if absent)
optional_covars <- c("device", "channel", "region", "new_user")
covars_present <- optional_covars[optional_covars %in% names(df)]

if ("device" %in% covars_present)  df <- df %>% mutate(device  = factor(device))
if ("channel" %in% covars_present) df <- df %>% mutate(channel = factor(channel))
if ("region" %in% covars_present)  df <- df %>% mutate(region  = factor(region))
if ("new_user" %in% covars_present) {
  df <- df %>%
    mutate(
      new_user = ifelse(is.na(new_user), 0, new_user),
      new_user = factor(new_user, levels = c(0, 1))
    )
}

stamp <- format(Sys.time(), "%Y%m%d_%H%M%S")

# ------------------------------------------------------------
# Helper: robust coefficient table (glm uses z, lm uses t)
# ------------------------------------------------------------
robust_table_glm <- function(model, vcov_mat) {
  b  <- coef(model)
  se <- sqrt(diag(vcov_mat))
  z  <- b / se
  p  <- 2 * pnorm(-abs(z))
  
  tibble(
    term      = names(b),
    estimate  = as.numeric(b),
    std_error = as.numeric(se),
    stat_value = as.numeric(z),
    p_value   = as.numeric(p)
  )
}

robust_table_lm <- function(model, vcov_mat) {
  b  <- coef(model)
  se <- sqrt(diag(vcov_mat))
  t  <- b / se
  df_res <- df.residual(model)
  p  <- 2 * pt(-abs(t), df = df_res)
  
  tibble(
    term      = names(b),
    estimate  = as.numeric(b),
    std_error = as.numeric(se),
    stat_value = as.numeric(t),
    p_value   = as.numeric(p)
  )
}

# ------------------------------------------------------------
# 1) Conversion: logistic regression + robust SE + adjusted RD
# ------------------------------------------------------------

rhs_terms_conv <- c("variant", "log1p_pre_sessions_7d", covars_present)
f_conv <- as.formula(paste("converted ~", paste(rhs_terms_conv, collapse = " + ")))

m_conv <- glm(f_conv, data = df, family = binomial())

vc_conv <- sandwich::vcovHC(m_conv, type = "HC3")
conv_coefs <- robust_table_glm(m_conv, vc_conv) %>%
  mutate(
    odds_ratio = exp(estimate),
    ci_low_or  = exp(estimate - 1.96 * std_error),
    ci_high_or = exp(estimate + 1.96 * std_error)
  )

# Adjusted risk difference (pp) via predicted probabilities
df_control <- df %>% mutate(variant = factor("control", levels = levels(df$variant)))
df_treat   <- df %>% mutate(variant = factor("treatment", levels = levels(df$variant)))

p_control <- predict(m_conv, newdata = df_control, type = "response")
p_treat   <- predict(m_conv, newdata = df_treat,   type = "response")

adj_rd <- mean(p_treat - p_control)
adj_pp <- adj_rd * 100

# Bootstrap CI for adjusted RD
B <- 1000
n <- nrow(df)

boot_rd <- replicate(B, {
  idx <- sample.int(n, size = n, replace = TRUE)
  d_b <- df[idx, , drop = FALSE]
  
  m_b <- glm(f_conv, data = d_b, family = binomial())
  
  d0 <- d_b %>% mutate(variant = factor("control", levels = levels(df$variant)))
  d1 <- d_b %>% mutate(variant = factor("treatment", levels = levels(df$variant)))
  
  mean(predict(m_b, newdata = d1, type = "response") -
         predict(m_b, newdata = d0, type = "response"))
})

rd_ci <- quantile(boot_rd, probs = c(0.025, 0.975), names = FALSE) * 100

conv_effect_summary <- tibble(
  metric = "converted (logit, regression-adjusted)",
  adjusted_lift_pp = adj_pp,
  ci_low_pp = rd_ci[1],
  ci_high_pp = rd_ci[2]
)

conv_treatment_row <- conv_coefs %>%
  filter(term == "varianttreatment") %>%
  transmute(
    term,
    log_odds = estimate,
    odds_ratio,
    ci_low_or,
    ci_high_or,
    p_value
  )

# ------------------------------------------------------------
# 2) Guardrail: OLS regression + robust SE (time_to_complete)
# ------------------------------------------------------------

rhs_terms_time <- c("variant", "log1p_pre_sessions_7d", covars_present)
f_time <- as.formula(paste("time_to_complete ~", paste(rhs_terms_time, collapse = " + ")))

m_time <- lm(f_time, data = df)

vc_time <- sandwich::vcovHC(m_time, type = "HC3")
time_coefs <- robust_table_lm(m_time, vc_time) %>%
  mutate(
    ci_low  = estimate - 1.96 * std_error,
    ci_high = estimate + 1.96 * std_error
  )

time_effect_summary <- time_coefs %>%
  filter(term == "varianttreatment") %>%
  transmute(
    metric = "time_to_complete (OLS, regression-adjusted)",
    adjusted_diff = estimate,
    ci_low = ci_low,
    ci_high = ci_high,
    p_value = p_value
  )

# ------------------------------------------------------------
# 3) Save outputs
# ------------------------------------------------------------

write_csv(conv_coefs, file.path(tables_dir, paste0("reg_conv_coefficients_", stamp, ".csv")))
write_csv(conv_effect_summary, file.path(tables_dir, paste0("reg_conv_adjusted_effect_", stamp, ".csv")))
write_csv(conv_treatment_row, file.path(tables_dir, paste0("reg_conv_treatment_row_", stamp, ".csv")))

write_csv(time_coefs, file.path(tables_dir, paste0("reg_time_coefficients_", stamp, ".csv")))
write_csv(time_effect_summary, file.path(tables_dir, paste0("reg_time_adjusted_effect_", stamp, ".csv")))

message("✅ Script 05 complete.")
message("Saved tables to /tables/:")
message(" - reg_conv_coefficients_*")
message(" - reg_conv_adjusted_effect_*")
message(" - reg_conv_treatment_row_*")
message(" - reg_time_coefficients_*")
message(" - reg_time_adjusted_effect_*")
