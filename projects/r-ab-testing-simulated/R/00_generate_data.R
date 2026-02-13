# 00_generate_data.R
# Purpose: Generate simulated A/B test data for a SaaS onboarding experiment

set.seed(123)

library(tidyverse)
library(janitor)

message("Generating simulated A/B test dataset...")

# ----------------------------
# Parameters
# ----------------------------

n_users <- 10000
baseline_conversion <- 0.10
treatment_lift <- 0.015  # +1.5 percentage points
baseline_time_mean <- 8
baseline_time_sd <- 3

# ----------------------------
# Simulate user-level data
# ----------------------------

df <- tibble(
  user_id = 1:n_users,
  
  # Random assignment (50/50)
  variant = sample(c("control", "treatment"), 
                   size = n_users, 
                   replace = TRUE),
  
  # Pre-experiment engagement covariate
  pre_sessions_7d = rpois(n_users, lambda = 3)
)

# ----------------------------
# Simulate conversion
# ----------------------------

df <- df %>%
  mutate(
    conversion_prob = case_when(
      variant == "control" ~ baseline_conversion,
      variant == "treatment" ~ baseline_conversion + treatment_lift
    ),
    
    converted = rbinom(n_users, 1, conversion_prob)
  )

# ----------------------------
# Simulate time-to-complete
# ----------------------------

df <- df %>%
  mutate(
    time_to_complete = rnorm(
      n_users,
      mean = ifelse(variant == "treatment",
                    baseline_time_mean - 0.5,
                    baseline_time_mean),
      sd = baseline_time_sd
    )
  )

# Ensure no negative times
df <- df %>%
  mutate(time_to_complete = pmax(time_to_complete, 0.5))

# ----------------------------
# Final cleanup
# ----------------------------

df <- df %>%
  select(user_id, variant, pre_sessions_7d,
         converted, time_to_complete) %>%
  clean_names()

# ----------------------------
# Save dataset
# ----------------------------

write_csv(df, "data/ab_test_data.csv")

message("Dataset saved to data/ab_test_data.csv")
