# AGENTS.md — r-ab-testing-simulated

## Project goals
- Maintain this project as a **portfolio-grade A/B testing pipeline in R**.
- Keep analyses reproducible, interpretable, and presentation-ready for stakeholder review.

## Hard rules
- **Do not change result numbers** unless rerunning the project scripts regenerates outputs with updated values.
- **Do not commit RStudio user files** (e.g., `.Rproj.user`, `.Rhistory`).
- All generated outputs must be written to:
  - `/tables`
  - `/figures`
- Scripts must remain modular and runnable in sequence **00–06**.

## Style rules
- Save tables as **CSV** files with a **timestamp suffix** in the filename.
- Use consistent naming prefixes:
  - `qc_`
  - `primary_metric_`
  - `guardrail_`
  - `bootstrap_`
  - `reg_`
  - `power_`

## How to validate changes
- Run scripts **00–06** in order.
- Confirm `/tables` and `/figures` regenerate without errors.
