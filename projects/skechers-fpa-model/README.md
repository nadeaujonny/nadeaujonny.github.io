# FP&A Financial Model — Skechers U.S.A. (SKX)

A fully-integrated 3-statement financial model for Skechers U.S.A., Inc. — built from public SEC 10-K filings.

**Author:** Jonathan Nadeau
**Portfolio:** [nadeaujonny.github.io](https://nadeaujonny.github.io)
**Full Project Writeup:** [Portfolio Project Page](https://nadeaujonny.github.io/projects/skechers-fpa-model/)

---

## Project Overview

A complete three-statement financial model for Skechers U.S.A. (NYSE: SKX) — income statement, balance sheet, and cash flow statement that fully articulate. Five years of historical actuals (FY2020–FY2024) reconstructed from SEC 10-K filings, plus a three-year forecast (FY2025–FY2027) driven by switchable Bear/Base/Bull assumptions.

The model balances to zero and the cash flow ties to the balance sheet exactly — verified by audit to hold across all three scenarios in every forecast year.

---

## The Analytical Thesis

Skechers runs two segments: Wholesale and Direct-to-Consumer (DTC). DTC grew from 38.5% of revenue (FY2020) to 43.1% (FY2024) and carries a much higher gross margin (~66%) than Wholesale (~40–43%). Each point of mix shift toward DTC expands the blended margin. The model forecasts each segment separately so the margin-expansion story is explicit and auditable.

---

## Base-Case Headline Outputs (FY2025)

| Metric | Value |
|---|---|
| Total Revenue | ~$9.76B |
| Gross Margin | 53.3% |
| Operating Margin | 10.4% |
| Diluted EPS | $4.40 |
| Free Cash Flow | $343.8M |

Both revenue and EPS land inside the company's February 2025 forward guidance.

---

## Scenario Outputs (FY2025, audited)

| Output | Bear | Base | Bull |
|---|---|---|---|
| Total Revenue ($000s) | 9,405,554 | 9,764,330 | 10,174,111 |
| Diluted EPS | $2.48 | $4.40 | $6.18 |
| Free Cash Flow ($000s) | 208,516 | 343,841 | 480,462 |

---

## Repository Structure

```
skechers-fpa-model/
├── README.md
├── index.md                                    # Full portfolio writeup (rendered page)
├── excel/
│   └── SKX_Financial_Analysis_Project_Final.xlsx   # Complete 10-tab model
└── images/
    └── (dashboard + key-tab screenshots)
```

---

## Model Tabs

| Tab | Purpose |
|---|---|
| Historical Financials | FY2020–24 IS/BS/CF + segment detail from 10-Ks; balance checks tie to zero |
| Assumptions | Bear/Base/Bull driver sets; active set via CHOOSE/MATCH dropdown |
| Supporting Schedules | PP&E/D&A, debt, and shares rollforwards |
| Income Statement Forecast | Segment-level Wholesale/DTC build → consolidated IS |
| Balance Sheet Forecast | Working capital via DSO/DIO/DPO; equity rollforward |
| Cash Flow Forecast | Indirect method; ending cash flows back to BS for a genuine tie |
| Variance Analysis | Guidance-calibrated budget vs. actuals; $/% variances |
| Scenario Analysis | Bear/Base/Bull recap + live two-variable sensitivity tables |
| KPI Dashboard | Year-selectable scorecard, 5 charts, live integrity PASS/FAIL table |
| README | Cover page: model map, color legend, data sources, caveats |

---

## Key Design Decisions

- **Genuine 3-statement tie** — cash built as a temporary plug, CF built independently, ending cash swapped in; the balance check is a real integrity test, not a forced zero.
- **No circular reference** — interest on beginning-of-period debt breaks the interest→NI→cash→debt loop.
- **Segment-level build** — Wholesale and DTC modeled separately so the DTC mix-shift margin thesis is visible and auditable.
- **Switchable scenarios** — CHOOSE/MATCH drives the entire model from one dropdown; flipping it re-drives every statement, the dashboard, and the integrity checks together.

---

## Skills Demonstrated

- 3-statement financial modeling · segment revenue/margin build · DSO/DIO/DPO working-capital forecasting · scenario analysis (CHOOSE/MATCH) · two-variable sensitivity tables · variance analysis · PP&E/debt/share rollforwards · circular-reference avoidance · named-range architecture · KPI dashboarding with model-integrity checks · reconstructing financials from SEC 10-Ks

---

## Data Sources

- Skechers U.S.A. SEC EDGAR 10-K filings, FY2020–FY2024
- Skechers February 2025 forward guidance (Base-case calibration)

*Note: 3G Capital took Skechers private in September 2025 ($9.4B / $63 per share). The model uses public data through FY2024 and stands as a portfolio demonstration of modeling methodology.*

---

## Status

✅ **Complete** — model built, audited (balances across Bear/Base/Bull), and documented.

---

## Contact

**Jonathan Nadeau**
- Portfolio: [nadeaujonny.github.io](https://nadeaujonny.github.io)
- LinkedIn: [linkedin.com/in/nadeau-jonathan](https://linkedin.com/in/nadeau-jonathan)
- GitHub: [github.com/nadeaujonny](https://github.com/nadeaujonny)
- Email: nadeau.jonny@gmail.com
