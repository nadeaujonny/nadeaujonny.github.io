# requirements.R
# Install (if missing) and load required packages for A/B testing analysis

# List of required packages
required_packages <- c(
  "tidyverse",
  "infer",
  "broom",
  "patchwork",
  "gt",
  "lmtest",
  "sandwich",
  "pwr",
  "ggeffects"
)

# Function to install and load packages
install_and_load <- function(package) {
  if (!require(package, character.only = TRUE, quietly = TRUE)) {
    message(paste("Installing", package, "..."))
    install.packages(package, dependencies = TRUE)
    library(package, character.only = TRUE)
  } else {
    library(package, character.only = TRUE)
    message(paste(package, "loaded successfully"))
  }
}

# Install and load all required packages
message("Checking and loading required packages...")
invisible(lapply(required_packages, install_and_load))

message("\nAll required packages are installed and loaded!")
message("You're ready to run the A/B testing analysis.")
