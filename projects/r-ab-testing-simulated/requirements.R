# Install required packages (only runs if missing)

packages <- c(
  "tidyverse",
  "broom",
  "janitor",
  "infer",
  "gt",
  "patchwork",
  "effectsize"
)

installed <- packages %in% installed.packages()

if (any(!installed)) {
  install.packages(packages[!installed])
}

lapply(packages, library, character.only = TRUE)

