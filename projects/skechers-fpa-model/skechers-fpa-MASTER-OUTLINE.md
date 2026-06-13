# Master Outline & Study Guide
## FP&A Financial Model — Skechers U.S.A. (SKX) (Excel · 3-Statement · Bear/Base/Bull · Sensitivity · KPI Dashboard)

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.
>
> **One sentence to anchor everything:** This is a full **three-statement FP&A model** for
> Skechers U.S.A. (NYSE: SKX) — five years of historical actuals reconstructed from SEC
> 10-Ks plus a three-year forecast — built around a segment-level revenue engine, switchable
> **Bear / Base / Bull** scenarios driven by a `CHOOSE`/`MATCH` selector, a genuine
> (not forced) three-statement tie, live two-variable sensitivity tables, and a
> self-checking KPI dashboard.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Business Context)](#2-why-this-project-exists-business-context)
3. [The Tech Stack & Skills](#3-the-tech-stack--skills)
4. [The Data Foundation — SEC 10-Ks](#4-the-data-foundation--sec-10-ks)
5. [The Workbook Architecture](#5-the-workbook-architecture)
6. [Tab 1 — README (cover page)](#6-tab-1--readme-cover-page)
7. [Tab 2 — Historical Financials (the anchor)](#7-tab-2--historical-financials-the-anchor)
8. [Tab 3 — Assumptions (the scenario engine)](#8-tab-3--assumptions-the-scenario-engine)
9. [Tab 4 — Supporting Schedules (PP&E, Debt, Shares)](#9-tab-4--supporting-schedules-ppe-debt-shares)
10. [Tab 5 — Income Statement Forecast](#10-tab-5--income-statement-forecast)
11. [Tab 6 — Balance Sheet Forecast](#11-tab-6--balance-sheet-forecast)
12. [Tab 7 — Cash Flow Forecast](#12-tab-7--cash-flow-forecast)
13. [Tab 8 — Variance Analysis](#13-tab-8--variance-analysis)
14. [Tab 9 — Scenario Analysis & Sensitivity Tables](#14-tab-9--scenario-analysis--sensitivity-tables)
15. [Tab 10 — KPI Dashboard](#15-tab-10--kpi-dashboard)
16. [The Three-Statement Tie (deep dive)](#16-the-three-statement-tie-deep-dive)
17. [Excel & Modeling Techniques Demonstrated](#17-excel--modeling-techniques-demonstrated)
18. [Key Results & Numbers to Memorize](#18-key-results--numbers-to-memorize)
19. [Limitations & Honest Caveats](#19-limitations--honest-caveats)
20. [Design Decisions & Trade-offs (the "Why")](#20-design-decisions--trade-offs-the-why)
21. [Interview Q&A](#21-interview-qa)
22. [How to Walk Through This Project Live](#22-how-to-walk-through-this-project-live)
23. [Glossary](#23-glossary)

---

## 1. The 30-Second Pitch

This is a **fully-integrated three-statement financial model** for **Skechers U.S.A.,
Inc. (NYSE: SKX)** — income statement, balance sheet, and cash flow statement that **fully
articulate**, so a change to any driver flows correctly through all three. It covers
**FY2020–FY2024 actuals** reconstructed from SEC 10-K filings plus a **FY2025–FY2027
forecast** driven by a transparent, **switchable Bear / Base / Bull** assumption set.

The analytical thesis is **channel mix shift**: Direct-to-Consumer (DTC) carries roughly
**66%** gross margin versus **40–43%** in Wholesale, and grew from **38.5%** of revenue
in FY2020 to **43.1%** in FY2024. The model forecasts each segment separately and
continues the mix shift (DTC **43.6% → 44.5%** across FY2025–27), making the
margin-expansion story explicit and auditable rather than buried in a single blended
revenue line.

The Base case lands **inside Skechers' February 2025 forward guidance** — FY2025 revenue
**~$9.76B**, gross margin **53.3%**, operating margin **10.4%**, diluted EPS **$4.40**, and
free cash flow **$343.8M**. The headline engineering result is **integrity**: the balance
sheet ties to zero and CF ending cash ties to BS cash exactly — across **all three
scenarios** in **every** forecast year — verified by audit.

**One-line version:** "I built a full three-statement Excel model for Skechers from public
10-Ks — a segment-level revenue engine, Bear/Base/Bull scenarios driven by
`CHOOSE`/`MATCH`, working capital from DSO/DIO/DPO, live two-variable sensitivity grids,
and a KPI dashboard with self-checking model-integrity gates that all read PASS."

**Deliverable:** `excel/SKX_Financial_Analysis_Project_Final.xlsx`

---

## 2. Why This Project Exists (Business Context)

**The simulated scenario.** The project plays the role of an FP&A analyst building a
defensible forecasting model for **Skechers U.S.A., Inc.** — a publicly-traded global
footwear company with two reportable segments (Wholesale and Direct-to-Consumer). The
model needs to support standard FP&A workflows: scenario planning, sensitivity analysis,
variance reporting, and executive-ready KPI reporting.

**The business questions it answers.** (1) How does Skechers' financial picture look on
a forward three-year horizon? (2) How sensitive is the answer to revenue growth, gross
margin, OpEx ratio, and CapEx? (3) What does the spread between a pessimistic, base, and
optimistic view actually look like in revenue, EPS, and free cash flow? (4) How did
FY2024 actuals land versus guidance, and what drove the variances? (5) Does the model
itself remain internally consistent under every scenario — and how is that proved, not
asserted?

**Why it's a strong portfolio project.** It demonstrates the full FP&A modeling toolkit
in one artifact: reading and reconstructing financials from **SEC 10-K filings**,
**segment-level revenue and margin modeling**, **working-capital forecasting** via days
ratios, **PP&E / debt / shares rollforward schedules**, **switchable scenarios** wired
through `CHOOSE`/`MATCH`, **two-variable sensitivity analysis**, **variance analysis**,
**named-range architecture**, and a **dashboard layer** that reports live model-integrity
results — not just charts. Each piece is something a real corporate-finance team would
actually build.

**The core principle behind the whole build:** *transparency and integrity*. Every
driver is editable; every formula is traceable; the three statements articulate
correctly; and the model proves its own integrity via four live PASS/FAIL checks on the
dashboard. The model is not "trust me, it ties" — it's "look, the dashboard tells you
it ties."

---

## 3. The Tech Stack & Skills

Everything is in **one Excel workbook**, **10 tabs**, designed to run from a single
scenario dropdown. The skills, and where each shows up:

| Skill area | What it covers | Where in the project |
|---|---|---|
| **Three-statement modeling** | IS, BS, CF that fully articulate | IS / BS / CF forecast tabs (cross-linked) |
| **Segment-level revenue build** | Wholesale + DTC modeled separately, blended GM check | Income Statement Forecast, rows 8–15 |
| **Working-capital forecasting** | AR, Inventory, AP from DSO/DIO/DPO | Balance Sheet Forecast, rows 9, 10, 20 |
| **Rollforward schedules** | PP&E (CapEx − D&A), debt (borrow − repay), shares (buyback − SBC) | Supporting Schedules |
| **Scenario engineering** | `CHOOSE`/`MATCH` driven by a dropdown | Assumptions!B5 → ScenarioIndex E5 → column L–N "Active" block |
| **Sensitivity analysis** | Three formula-filled two-variable grids | Scenario Analysis, rows 62–87 |
| **Variance analysis** | FY2024 budget vs. actuals with $ / % variances | Variance Analysis |
| **Named ranges** | 150+ named cells for clean cross-tab linkage | Throughout (e.g., `IS_NetEarnings_25`, `BS_BalanceCheck_25`) |
| **Model-integrity checks** | Live PASS/FAIL tests of the three-statement tie | README + KPI Dashboard |
| **KPI dashboarding** | Year-selectable scorecard with YoY deltas, scenario tables, charts | KPI Dashboard |
| **Reading 10-Ks** | Reconstructing 5 years of IS / BS / CF + segment from XBRL | Historical Financials |

**The mental model.** Think of the workbook as a **factory**:
- **Inputs:** the **Assumptions** tab (raw drivers, three scenarios side-by-side).
- **The selector switch:** `Scenario` dropdown on `Assumptions!B5`, fed into `ScenarioIndex`
  on `E5` via `MATCH`, then used in every `CHOOSE` formula in the "Active" block.
- **The mid-stream processors:** the **Supporting Schedules** tab turns assumptions into
  PP&E, D&A, interest expense, debt balances, and share counts.
- **The three engines:** the **IS / BS / CF Forecast** tabs build the financials.
- **The QA station:** the **Variance Analysis** + **Scenario Analysis** + dashboard
  integrity checks all confirm the output is internally consistent.
- **The shipping bay:** the **KPI Dashboard** presents the result.

**Why "switchable" is the recurring theme.** A static model that only shows one scenario
is a snapshot, not a tool. Flipping `Assumptions!B5` from Base to Bear or Bull re-drives
**every** forecast statement, **every** schedule, **every** dashboard KPI, **every**
scenario recap value, and **every** integrity check — together, in one click. That
switchability is what separates an FP&A *model* from a one-time analysis.

---

## 4. The Data Foundation — SEC 10-Ks

**What it is.** All historical data comes from **Skechers' SEC EDGAR 10-K filings for
FY2020–FY2024**, verified against the **XBRL instance documents** (the structured-data
filings that hold the exact numbers). The Base-case calibration is anchored to
**Skechers' February 2025 forward guidance**.

**What's reconstructed in the Historical Financials tab:**

| Section | Years | Notes |
|---|---|---|
| Consolidated Income Statement ($000s) | FY2020–FY2024 | Sales, COGS, SG&A split into Selling and G&A, EBIT, tax, NCI, net to SKX, EPS |
| Segment Revenue & Gross Margins ($000s) | FY2020–FY2024 | Wholesale and DTC each: revenue, growth %, gross margin %, DTC mix % |
| Consolidated Balance Sheet ($000s, Dec 31) | FY2020–FY2024 | Full asset, liability, and equity lines (Cash, AR, Inventory, PP&E, leases, AP, debt, etc.) with a **Balance Check = Assets − (L+E) = 0** in every year |
| Consolidated Cash Flow Statement ($M) | FY2020–FY2024 | Operating, investing, financing CF, FX adjustment, net change, plus a derived **Free Cash Flow = OCF + CapEx** line |
| Derived Metrics & Working Capital | FY2020–FY2024 | DSO, DIO, DPO, **CCC**, CapEx % of revenue, D&A as % of prior-year PP&E, total debt, NCI %, SBC % |

**Key historical facts to know cold:**
- **Revenue trajectory:** $4.61B (FY2020) → $8.97B (FY2024) — nearly doubled in 4 years.
- **Wholesale revenue:** $2.835B → $5.1005B; **DTC revenue:** $1.7784B → $3.8689B.
- **DTC mix:** **38.5% (FY2020) → 43.1% (FY2024)** — the central thesis.
- **Wholesale GM:** ~39.2% → 43.3% (general expansion).
- **DTC GM:** 61.5% → 66.2% (stable around the mid-60s).
- **Blended GM:** 47.8% → 53.2% (mix shift + WH GM improvement together).
- **FY2021 tax line is anomalous:** a **$346.8M one-time tax benefit** from an intra-entity
  IP transfer drove a *negative* effective tax rate of −43.2% and a one-year EPS spike to
  **$4.73**. This is documented in `A117` of the Historical Financials tab and called out
  again in the README caveats. Always mention it if asked why FY2021 looks weird.

**The Cash Flow Statement unit note.** The Historical CF is reported in **$M**, while the
rest of the workbook is in **$000s**. The forecast CF is in $000s. The conversion (×1000)
shows up explicitly in the formulas linking back, e.g., `=-B88*1000/B8` for CapEx % of
revenue.

---

## 5. The Workbook Architecture

The deliverable `SKX_Financial_Analysis_Project_Final.xlsx` has **10 sheets**. Knowing the
sheet roles and the flow between them is knowing the project's structure.

| # | Sheet | Role |
|---|---|---|
| 1 | **README** | Cover page: model map, color legend, data sources, design notes, **live integrity status** |
| 2 | **Historical Financials** | FY2020–FY2024 actuals reconstructed from 10-Ks (IS, segment, BS, CF, derived metrics) |
| 3 | **Assumptions** | Bear / Base / Bull driver blocks + the **Active** column block (live scenario via `CHOOSE`/`MATCH`) |
| 4 | **Supporting Schedules** | PP&E / D&A rollforward, debt rollforward, share-count rollforward |
| 5 | **Income Statement Forecast** | Segment build (WH + DTC) → consolidated IS, EPS, blended-GM check |
| 6 | **Balance Sheet Forecast** | Working-capital from DSO/DIO/DPO, PP&E + debt from schedules, equity rollforward, **balance check** |
| 7 | **Cash Flow Forecast** | Indirect method; ending cash flows back to BS; FCF memo; **3-statement tie check** |
| 8 | **Variance Analysis** | FY2024 guidance-calibrated budget vs. actuals; $ and % variances with commentary |
| 9 | **Scenario Analysis** | Bear/Base/Bull recap + self-contained FY2025 mini-model + 3 two-variable sensitivity grids |
| 10 | **KPI Dashboard** | Year-selectable scorecard (6 KPIs with YoY), scenario table, integrity check table, data staging |

**The data flow through the sheets** (read this as the model's "pipeline"):

```
Historical Financials (10-K data, FY2020–24)
            │
            ├──► Assumptions  ───[CHOOSE/MATCH on B5]──►  Active block (cols L–N)
            │                                                  │
            │                                                  ▼
            │                                       Supporting Schedules
            │                                       (PP&E, Debt, Shares)
            │                                                  │
            ▼                                                  ▼
       Income Statement Forecast  ────►  Balance Sheet Forecast
              │                                  │
              ▼                                  ▼
        Cash Flow Forecast  ──[ending cash]──►  BS Cash (closes the loop)
              │
              ├──► Variance Analysis (compares actuals vs. FY24 budget)
              ├──► Scenario Analysis (snapshots + sensitivity grids)
              └──► KPI Dashboard (year selector + integrity checks)
```

**The two control cells.** Two yellow-fill cells govern what the whole workbook displays:
- `Assumptions!B5` → the scenario dropdown (Bear / Base / Bull). Drives `ScenarioIndex` on
  `E5` via `=MATCH(B5,{"Bear","Base","Bull"},0)`. Every formula in the "Active" column
  block uses `=CHOOSE($E$5, …)` to pick the right scenario's value.
- `KPI Dashboard!B5` → the forecast year dropdown (FY2025 / FY2026 / FY2027). Drives
  `Dash_YearIdx` on `B6` via `=MATCH(B5,{"FY2025","FY2026","FY2027"},0)`. The scorecard
  KPIs use `=CHOOSE(Dash_YearIdx, …)` against three staging columns (X / Y / Z).

**Named-range architecture.** The workbook defines roughly **150 named ranges**. Every
cross-sheet reference is via a name, not a coordinate — e.g., the Income Statement uses
`Wh_Growth_25` instead of `Assumptions!L13`. Why this matters: names survive row inserts,
and they make formulas readable (`=B8*(1+Wh_Growth_25)` is obviously "prior-year sales
times next-year growth"). The forecast outputs are also exposed as names
(`IS_NetEarnings_25`, `BS_BalanceCheck_25`, `CF_TieCheck_25`, etc.) so the dashboard's
PASS/FAIL formulas read the live model without hard cell addresses.

---

## 6. Tab 1 — README (cover page)

The README is the model's front door and works **without opening any other tab**. It
contains seven sections:

1. **What this model is** — the one-paragraph thesis (channel mix, FY2025 Base outputs).
2. **How to read it — model map** — a 10-row table mapping each tab to a one-line role.
3. **Color legend** — the modeling convention used in cells:
   - **Blue text** = hardcoded input (the user can change).
   - **Black text** = formula / calculation.
   - **Green text** = link to another sheet in the workbook.
   - **Yellow fill** = the two selector cells (`Assumptions!B5` and `KPI Dashboard!B5`).
4. **Data sources** — SEC EDGAR 10-Ks + February 2025 forward guidance.
5. **Key design notes** — the three big architectural decisions: (a) **no circular
   reference** (interest on beginning-of-period debt), (b) **genuine three-statement tie**
   (cash built as plug first, then CF built independently, then swapped in), (c)
   **`CHOOSE`/`MATCH`-driven scenario & year switching**.
6. **Live integrity status** — a 3-row × 4-col table that reads the live model via named
   ranges:

   | Check | FY2025 | FY2026 | FY2027 |
   |---|---|---|---|
   | Balance Sheet (Assets = Liabilities + Equity) | PASS | PASS | PASS |
   | Cash Flow tie (CF ending cash = BS cash) | PASS | PASS | PASS |

   Formula example: `=IF(ABS(BS_BalanceCheck_25)<1,"PASS","FAIL")`. The `<1` tolerance is
   **$1K rounding** (the model is in $000s, so $1K is effectively zero).
7. **Limitations & caveats** — public data only, FY2021 tax-benefit anomaly,
   September-2025 3G Capital take-private, illustration-only purpose.

**Why this README earns its keep.** Most Excel models open to a wall of numbers. This one
opens to "here is what this is, here is how to read it, here is proof it works." It's
the **single most important onboarding artifact** in the file.

---

## 7. Tab 2 — Historical Financials (the anchor)

This is the **foundation tab** — five years of actuals that every forecast value
eventually compares against. **120 rows by 7 columns**, organized into five sections:

**(A) Consolidated Income Statement** (rows 7–34). Sales, COGS (with computed Gross
Profit and Gross Margin %), Selling vs. G&A separated, EBIT and Operating Margin %, Other
Income/Expense, EBT, tax expense and Effective Tax Rate %, Net Earnings, NCI, Net
Earnings Attributable to SKX, Net Margin %, Diluted EPS, Diluted Shares (M), plus
derived %-of-revenue lines for Selling and G&A and Revenue Growth % YoY.

**(B) Segment Revenue & Gross Margins** (rows 36–45). Wholesale revenue + growth + GM,
DTC revenue + growth + GM, and **DTC Mix % of Total Revenue**. This is where the channel
thesis is most visible.

**(C) Consolidated Balance Sheet ($000s, Dec 31)** (rows 47–75). Current assets (Cash,
ST Investments, AR, Inventory, Other CA → Total CA), non-current assets (PP&E, ROU
Assets, Other NCA → Total Assets), current liabilities (AP, Accrued, Current Leases,
Current Debt → Total CL), long-term (LT Debt, LT Leases, Other LT → Total Liabilities),
equity (Retained Earnings, Total Equity incl. NCI) → Total L+E, and a **Balance Check**
row that subtracts and shows 0 in every historical year. Note: Other Current Assets and
Other LT Liabilities are derived as **residuals** to make the balance sheet balance to
the as-reported totals.

**(D) Consolidated Cash Flow Statement ($M)** (rows 77–101). Operating section (net
income, D&A, SBC, other operating adjustments, AR/Inv/AP changes, other WC), Investing
(CapEx + other), Financing (debt issued/repaid, buyback, other), FX adjustment, Net
Change in Cash, plus a derived **Free Cash Flow = OCF + CapEx** line. **Units: $M** here,
unlike the rest of the workbook.

**(E) Derived Metrics & Working-Capital Analysis** (rows 103–114). DSO, DIO, DPO, CCC,
CapEx % of revenue, D&A as % of prior PP&E, total debt, NCI as % of net earnings, SBC as
% of revenue. These are the cells that **calibrate the forecast assumptions** — the
Base-case DSO 40, DIO 165, DPO 108 are anchored to what actually happened in FY2024.

**The notes block at the bottom** documents the FY2021 tax-benefit anomaly, the $M vs.
$000s convention, the residual derivation for Other CA / Other LT Liabilities, and the
XBRL verification.

**Why this tab is worth studying in itself.** Reading the entire historical block in
order is the cleanest way to learn the SKX business — and it makes the forecast tabs make
sense, because every forecast number is a continuation or normalization of a historical
trend visible here.

---

## 8. Tab 3 — Assumptions (the scenario engine)

This is the **single tab the user actually interacts with** to drive the model. Roughly
50 rows by 14 columns, organized into eight assumption groups.

**The control row** at the top:
- `B5` = the scenario dropdown ("Bear" / "Base" / "Bull"). Default: **Base**.
- `E5` = `=MATCH(B5,{"Bear","Base","Bull"},0)` → returns 1, 2, or 3.

**The column structure.** For each driver, three columns per forecast year for the three
scenarios — `B:D` for FY2025 (Bear/Base/Bull), `E:G` for FY2026, `H:J` for FY2027 — and
then the **"ACTIVE (live scenario)" block in columns L:N** for FY2025, FY2026, FY2027
respectively. Each "Active" cell is a `CHOOSE` formula:

```
L13 = =CHOOSE($E$5, B13, C13, D13)        ← FY2025 active value (Wholesale growth)
M13 = =CHOOSE($E$5, E13, F13, G13)        ← FY2026 active value
N13 = =CHOOSE($E$5, H13, I13, J13)        ← FY2027 active value
```

Every formula downstream in the model reads from the **Active block** via named ranges
(`Wh_Growth_25`, `DTC_Growth_25`, `Wh_GM_25`, `DSO`, `CapEx_25`, `Tax_25`, …). Flipping
`B5` re-drives `E5`, which re-drives every `CHOOSE`, which re-drives every named range,
which re-drives every forecast cell. Effectively a one-cell switchboard.

**The eight assumption groups, with FY2025 Base values:**

| Group | Driver | FY25 Bear | FY25 Base | FY25 Bull |
|---|---|---|---|---|
| **A. Revenue growth** | Wholesale YoY % | 4% | **8%** | 13% |
| | DTC YoY % | 6% | **10%** | 14% |
| **B. Gross margins** | Wholesale GM | 41.0% | **43.5%** | 45.0% |
| | DTC GM | 65.0% | **66.0%** | 67.0% |
| **C. OpEx (% of revenue)** | Selling % | 9.5% | **8.9%** | 8.5% |
| | G&A % | 35.5% | **34.0%** | 32.5% |
| **D. Tax & below-the-line** | Effective Tax Rate | 23.0% | **22.5%** | 22.0% |
| | Other Income/(Expense) ($000s) | (26,000) | **(26,000)** | (26,000) |
| | NCI % of Net Earnings | 12% | **12%** | 12% |
| **E. Working capital** | DSO (days) | 40 | **40** | 40 |
| | DIO (days) | 165 | **165** | 165 |
| | DPO (days) | 108 | **108** | 108 |
| | Accrued Exp % of Rev | 3.7% | **3.7%** | 3.7% |
| | Other CA % of Rev | 3.4% | **3.4%** | 3.4% |
| **F. CapEx & D&A** | CapEx ($000s) | 500,000 | **650,000** | 750,000 |
| | D&A as % of Prior PP&E | 14% | **14%** | 14% |
| **G. Debt** | New Borrowings | 0 | **0** | 0 |
| | Scheduled Repayments ($000s) | 50,000 | **50,000** | 50,000 |
| | Interest Rate | 5% | **5%** | 5% |
| **H. Shares & buyback** | Beginning Shares (M) | 153.8 | **153.8** | 153.8 |
| | Share Repurchases ($000s) | 150,000 | **350,000** | 500,000 |
| | Avg Repurchase Price ($/sh) | 65 | **65** | 65 |
| | SBC % of Revenue | 1% | **1%** | 1% |

**Calibration logic.** Notice what varies across scenarios versus what doesn't. Working
capital ratios (DSO/DIO/DPO/Accrued/OCA), tax rate, NCI, Other Income, interest rate,
and SBC are held flat — those are *structural* features of the business, not bets on the
future. Revenue growth, gross margin, OpEx ratio, CapEx, and buyback intensity vary
because those are where the *real* uncertainty and management discretion live.

---

## 9. Tab 4 — Supporting Schedules (PP&E, Debt, Shares)

This tab transforms a handful of high-level assumptions into the **balance-sheet-grade
detail** the forecast IS/BS/CF need. Roughly 28 rows by 7 columns, three rollforwards.

**(A) PP&E / D&A Rollforward** (rows 6–11). Standard "BASE" rollforward — Beginning +
Additions − Depreciation = Ending:

```
Beginning PP&E         (from prior period: FY24 actual for FY25, then prior FY ending)
(+) CapEx              = CapEx_25 / CapEx_26 / CapEx_27 (from Assumptions)
(-) D&A                = -Beginning PP&E × DA_Rate (14% of prior PP&E)
(=) Ending PP&E        = sum
```

A separate "D&A (positive, for CF add-back)" row exposes D&A with a positive sign for the
indirect-method cash flow.

**(B) Debt Schedule** (rows 13–20). Same BASE structure:

```
Beginning Debt         (FY24 total debt $454,919; then prior ending)
(+) New Borrowings     = New_Borrow (0 in all scenarios)
(-) Scheduled Repay    = -Repay ($50,000 each year)
(=) Ending Debt        = beginning + borrowings − repayments
Interest Expense       = Beginning Debt × 5%   ← the no-circular-reference trick
Current Portion        = Repay ($50,000)
Long-term Portion      = Ending Debt − Current Portion
```

**The interest-expense calculation is the single most important modeling decision in the
file.** Interest is computed on the **beginning-of-period** debt balance, not the average
or the ending balance. This is the industry-standard simplification that breaks the
circular loop:

> Interest expense → Net income → Cash flow → Cash balance → Debt balance → Interest expense

Computing on beginning debt freezes the input to interest before any of those downstream
effects can feed back. The workbook contains **zero circular references** and **does not
need iterative calculation enabled**.

**(C) Shares Outstanding Schedule** (rows 22–26). Same BASE structure, in millions:

```
Beginning Diluted Shares   (Shares_Begin = 153.8M for FY25, then prior ending)
(-) Shares Repurchased     = -Repurchase / Repurchase_Price / 1000  (e.g., $350K÷$65÷1000 = 5.38M)
(+) SBC Dilution           = (Revenue × SBC_Pct) / Repurchase_Price / 1000
(=) Ending Diluted Shares  = sum
```

The SBC dilution proxy is **revenue × 1% / $65 / 1000** — i.e., the dollar value of stock-
based compensation is converted to "new shares" at the assumed market price.

**Why the schedule names matter.** Every output from this tab is exposed as a named range
— `PPE_End_25`, `DA_25`, `Debt_End_25`, `Int_Exp_25`, `Debt_Curr_25`, `Debt_LT_25`,
`Shares_End_25` — so the IS/BS/CF tabs can just reference the names directly.

---

## 10. Tab 5 — Income Statement Forecast

The IS forecast is structured as a **segment build → consolidated IS → tax → EPS** flow.
42 rows by 7 columns.

**(A) Segment build** (rows 7–15). The heart of the channel-mix thesis:

```
Wholesale Revenue (FY25) = FY24 Wholesale × (1 + Wh_Growth_25)   ← Active scenario growth
DTC Revenue       (FY25) = FY24 DTC       × (1 + DTC_Growth_25)
Total Revenue            = Wholesale + DTC
DTC Mix %                = DTC / Total

Wholesale COGS = Wholesale Revenue × (1 − Wh_GM_25)
DTC COGS       = DTC Revenue       × (1 − DTC_GM_25)
Total COGS     = WH COGS + DTC COGS
```

**(B) Consolidated Income Statement** (rows 17–27). Sales = total revenue from the segment
build; Cost of Sales = total COGS; Gross Profit = difference; Gross Margin % = ratio.
Selling Expenses = Sales × Selling_Pct; G&A = Sales × GA_Pct; Total OpEx = Selling + G&A;
Earnings from Operations = Gross Profit − OpEx; Operating Margin % = ratio.

**(C) Below-the-line and bottom-line** (rows 29–39). Interest Expense pulled from
schedules (`=-Int_Exp_25`, shown negative as an expense); Other Income from assumptions;
EBT = EBIT + Interest + Other; Tax = EBT × Tax_25; Net Earnings = EBT − Tax; NCI =
Net Earnings × NCI_Pct; **Net Earnings Attributable to SKX** = Net Earnings − NCI;
Net Margin %; **Diluted EPS** = Net Earnings (SKX) / Shares_End / 1000 (the /1000 converts
$000s ÷ Millions of shares to $/share); Diluted Shares from the schedule.

**(D) Blended GM check** (row 42). A consistency check:

```
=GrossMargin% − ((WH Revenue × WH GM + DTC Revenue × DTC GM) / Total Revenue)
```

Should equal zero. If the segment-level build ties to the consolidated statement, the
blended GM% must equal the revenue-weighted segment GM%. **All three forecast years show
0.** This is the "did I do the segment math right" gate.

**FY2025 Base outputs the model produces:**

| Line | FY2025 Base ($000s) |
|---|---|
| Wholesale Revenue | 5,508,540 |
| DTC Revenue | 4,255,790 |
| **Total Revenue** | **9,764,330** |
| Gross Profit | 5,205,036 |
| **Gross Margin %** | **53.31%** |
| Operating Expenses | 4,188,898 |
| Earnings from Operations | 1,016,139 |
| **Operating Margin %** | **10.41%** |
| Interest Expense | (22,746) |
| EBT | 967,393 |
| Tax | (217,663) |
| Net Earnings | 749,729 |
| Less: NCI | (89,968) |
| **Net Earnings (SKX)** | **659,762** |
| **Diluted EPS** | **$4.40** |

---

## 11. Tab 6 — Balance Sheet Forecast

The BS forecast follows the same line ordering as the historical balance sheet so they're
trivially comparable. 38 rows by 7 columns.

**Where each line comes from** (the data lineage is the lesson here):

| Line | Source |
|---|---|
| **Cash & Equivalents** | `='Cash Flow Forecast'!C30` — **the CF ending cash** (closes the 3-statement loop) |
| Short-term Investments | Held flat at FY24 actual |
| **Trade Accounts Receivable** | `= Sales / 365 × DSO` |
| **Inventory** | `= COGS / 365 × DIO` |
| Other Current Assets | `= Sales × OCA_Pct` |
| **PP&E, net** | `= PPE_End_25` (from Supporting Schedules) |
| Right-of-Use Assets | Held flat at FY24 actual |
| Other Non-Current Assets | Held flat at FY24 actual |
| **Accounts Payable** | `= COGS / 365 × DPO` |
| Accrued Expenses | `= Sales × Accrued_Pct` |
| Current Lease Liabilities | Held flat |
| **Current Portion of Debt** | `= Debt_Curr_25` (from schedule, = Repay = $50K) |
| **Long-term Debt** | `= Debt_LT_25` (Ending Debt − Current Portion) |
| Long-term Lease Liabilities | Held flat |
| Other LT Liabilities | Held flat |
| **Retained Earnings** | `= Prior RE + Net Earnings (SKX)` ← equity rollforward |
| **Other Equity & NCI** | `= Prior + NCI − Repurchase + (Sales × SBC_Pct)` — NCI earnings retained, buyback reduces equity, SBC credited to paid-in capital |
| Total Equity | RE + Other Equity & NCI |
| **Balance Check** | `= Total Assets − Total L+E` → **0 in every forecast year** |

**Working-capital math, step by step.** AR = Sales × DSO / 365 means: "if I collect in
40 days, my receivables balance at year-end is 40/365 of a year's worth of sales."
Inventory = COGS × DIO / 365 ("if I hold 165 days of inventory…"). AP = COGS × DPO / 365
("if I pay vendors in 108 days…"). These three formulas are the bridge from the income
statement to the balance sheet — every dollar of revenue or COGS flowing into IS forecasts
generates a proportionate movement in working capital on the BS.

**Why the balance check being zero is the headline integrity test.** Cash was *originally*
built as the plug (any imbalance flows to cash), then the cash flow statement was built
independently and its ending cash swapped in. Now cash is **not** a free variable —
it's a calculated value from CF. So the only way Assets = L+E is if every *other* line
is right: working capital, PP&E, debt, retained earnings, and the equity rollforward all
have to articulate. **The zero in row 38 is the model proving itself.**

---

## 12. Tab 7 — Cash Flow Forecast

Indirect-method cash flow, derived from the forecast IS and the change in BS lines — no
new assumptions. 35 rows by 7 columns.

**The structure:**

```
OPERATING ACTIVITIES
  Net Earnings (incl. NCI)             ← from IS, IS_NetEarnings_25
  (+) D&A                              ← from Supporting Schedules, DA_25 (non-cash add-back)
  (+) SBC                              ← Revenue × SBC_Pct (non-cash add-back)
  (-) Increase in AR                   ← = Prior AR − Current AR  (asset increase = use of cash)
  (-) Increase in Inventory            ← = Prior Inv − Current Inv
  (+) Increase in AP                   ← = Current AP − Prior AP  (liability increase = source)
  (+) Increase in Accrued              ← same pattern
  (-) Increase in Other CA             ← same pattern
  = Net Cash from Operating

INVESTING ACTIVITIES
  CapEx                                ← -CapEx_25 (outflow)
  = Net Cash from Investing

FINANCING ACTIVITIES
  Debt Issued                          ← New_Borrow (= 0)
  Debt Repaid                          ← -Repay (= -50,000)
  Share Repurchases                    ← -Repurchase (= -350,000 Base)
  = Net Cash from Financing

NET CHANGE IN CASH = OCF + ICF + FCF
Beginning Cash                         ← Prior period ending cash
Ending Cash    = Beginning + Net Change   ← This is what BS Cash links to

Memo: Free Cash Flow = OCF + CapEx     ← Negative CapEx, so CF + CapEx = CF − |CapEx|
```

**The indirect-method working-capital convention is worth knowing cold.** "Δ" in this
context is signed for cash flow, not for the balance sheet:
- **Asset increase = use of cash** → AR rises means you sold but didn't collect → cash
  flow line is **negative**, computed as **prior − current** (so a bigger AR gives a
  negative number).
- **Liability increase = source of cash** → AP rises means you bought but didn't pay →
  cash flow line is **positive**, computed as **current − prior**.

**FY2025 Base CF outputs:**

| Line | FY2025 Base ($000s) |
|---|---|
| Net Earnings (incl. NCI) | 749,729 |
| D&A | 256,890 |
| SBC | 97,643 |
| Δ AR / Inv / AP / Accrued / OCA | (79,506) / (141,665) / 107,213 / 31,029 / (27,494) |
| **Operating Cash Flow** | **993,841** |
| CapEx | (650,000) |
| **Investing Cash Flow** | **(650,000)** |
| Debt Repaid + Share Repurchases | (400,000) |
| **Financing Cash Flow** | **(400,000)** |
| Net Change in Cash | (56,159) |
| Beginning Cash (= FY24 ending) | 1,116,516 |
| **Ending Cash** | **1,060,357** |
| **Free Cash Flow (memo)** | **343,841** |

**The CF tie check** (row 35): `= Ending Cash − BS_Cash_25`. Zero by construction
*after* the BS cash plug was swapped to point at this cell. The genuine integrity gate
is now the BS balance check, not this row — but the row is left in the model as a
visible "linkage holds" confirmation.

---

## 13. Tab 8 — Variance Analysis

A standard FP&A workflow: how did **FY2024 actuals** compare to a **budget calibrated to
February 2024 forward guidance**? 22 rows by 6 columns.

**Format.** For each line: **Budget** column (hardcoded), **Actual** column (linked to
the Historical Financials tab), **$ Variance** = Actual − Budget, **% Variance** =
$ Variance / Budget, plus a one-sentence **Commentary** explaining the driver.

**The lines covered.** Wholesale Revenue, DTC Revenue, Total Revenue, Gross Profit,
Gross Margin %, Selling, G&A, Earnings from Operations, Operating Margin %, Net Earnings
(SKX), Diluted EPS.

**Headline variances (FY2024 actual vs. February 2024 budget):**

| Line | Budget | Actual | $ Var | % Var |
|---|---|---|---|---|
| Wholesale Revenue | $4,955M | $5,100M | +$145M | +2.9% |
| DTC Revenue | $3,745M | $3,869M | +$124M | +3.3% |
| **Total Revenue** | **$8,700M** | **$8,969M** | **+$269M** | **+3.1%** |
| Gross Profit | $4,568M | $4,767M | +$199M | +4.4% |
| Gross Margin % | 52.5% | 53.2% | +65 bps | — |
| G&A Expenses | $2,914M | $3,063M | +$148M | +5.1% |
| Earnings from Operations | $913.5M | $904.3M | −$9.2M | −1.0% |
| **Net Earnings (SKX)** | **$577M** | **$639M** | **+$62M** | **+10.8%** |
| **Diluted EPS** | **$3.75** | **$4.16** | **+$0.41** | **+10.9%** |

**The story.** Revenue beat plan by ~3% (both segments), GM beat by ~65 bps (channel mix
+ freight). Operating income narrowly *missed* (−$9M) because G&A came in 5% above plan
on U.S./China distribution-center expansion and DTC store buildout. Below the line,
net earnings and EPS still beat by ~11% — the revenue + GM upside translating through,
plus buyback-driven share count reduction lifting EPS.

**The teachable framing.** This is the "what's the right way to talk about a beat that
isn't really a beat" exercise. Revenue **beat**, gross margin **beat**, but operating
income **missed** — and the EPS beat is partly a *share count* phenomenon, not pure
operating performance. An analyst reading just the EPS line gets the wrong story; an
analyst reading the whole variance stack gets the right one.

---

## 14. Tab 9 — Scenario Analysis & Sensitivity Tables

Two distinct things on one tab:

### 14.1 The Bear/Base/Bull recap table (rows 6–16)

A snapshot table comparing FY2025 outputs across all three scenarios:

| FY2025 Output | Bear | Base | Bull |
|---|---|---|---|
| Total Revenue ($000s) | 9,405,554 | 9,764,330 | 10,174,111 |
| Gross Margin % | 51.5% | 53.3% | 54.5% |
| Operating Margin % | 6.5% | 10.4% | 13.5% |
| Net Earnings (SKX, $000s) | 378,968 | 659,762 | 911,909 |
| Diluted EPS | $2.48 | $4.40 | $6.18 |
| Free Cash Flow ($000s) | 208,516 | 343,841 | 480,462 |
| Ending Cash ($000s) | 1,125,032 | 1,060,357 | 1,046,978 |

**The spread shows operating leverage at work.** A roughly **±4%** swing in revenue
(9.41B → 10.17B) drives roughly a **±40% swing in EPS** ($2.48 → $6.18), exactly as a
fixed-cost-bearing earnings stream should behave. That's the lesson: small changes at the
top become big changes at the bottom because fixed costs don't scale linearly.

**Why Bear/Bull values are pre-captured.** Because the model displays *one* scenario at
a time (whichever is selected on `Assumptions!B5`), the Bear and Bull columns in this
table are **captured snapshots**, not live formulas — they're blue inputs you can
overwrite by re-running the model in those scenarios. The Base column ties to the live
model.

### 14.2 The self-contained FY2025 sensitivity mini-model (rows 21–87)

The bottom of the Scenario tab carries a **separate, self-contained FY2025 mini-model**
— roughly 30 cells that recompute Net Earnings (SKX) and FCF from scratch with their own
input "knobs." That mini-model drives **three two-variable sensitivity grids**:

| Table | Output | Row variable | Column variable | Range |
|---|---|---|---|---|
| **Table 1** | Net Earnings (SKX) | Revenue Growth (4% → 14%) | Gross Margin (50% → 56%) | 6 × 7 grid |
| **Table 2** | FCF (pre-WC) | Revenue Growth (4% → 14%) | OpEx % (39% → 45%) | 6 × 7 grid |
| **Table 3** | FCF (pre-WC) | Revenue Growth (4% → 14%) | CapEx ($400K → $800K) | 6 × 5 grid |

**Every cell in every grid is a formula** — for instance Table 1's general form:

```
=(($B$33*(1+$B64))*C$63 − ($B$33*(1+$B64))*$B$40 − $B$34 + $B$28) × (1−$B$32) × (1−$B$29)
```

Reads as: **(Prior Revenue × (1 + Row growth)) × Column GM** *(gross profit)* **minus
that same revenue times the OpEx ratio** *(EBIT)* **minus Interest, plus Other Income,
then taxed and NCI-adjusted**.

**The engineering decision worth knowing.** Excel's built-in **Data Tables** can drive
sensitivity, but they require the input cells to be **direct, hardcoded** input cells.
The model's actual revenue-growth and gross-margin "inputs" are `CHOOSE`-driven formulas
in the Active block — Data Tables can't substitute into formula cells. So the equivalent
functionality was **engineered manually**: build a self-contained FY2025 mini-model whose
inputs *are* direct cells (`B38`, `B39`, `B40`, `B41`), then write each grid cell as a
formula that swaps in the row and column values directly. The result is **live,
formula-filled, fully auditable sensitivity grids** that recalculate on any change —
better than a static screenshot, and able to coexist with the `CHOOSE`-driven main model.

**The mini-model anchor cells** (the "base constants" you should know exist): prior-year
WH revenue (`B23 = 5,100,500`), prior DTC revenue (`B24 = 3,868,900`), prior PP&E
(`B25 = 1,834,930`), beginning debt (`B26 = 333,096`), interest rate (5%), Other Income
(-$26,000), NCI (12%), SBC (1%), D&A rate (14% × prior PP&E), tax rate (22.5%).

---

## 15. Tab 10 — KPI Dashboard

The executive deliverable. Roughly 51 rows by 26 columns, where columns **R:Z** are a
hidden-able **data-staging area** that pulls every series the dashboard needs from the
other tabs via cross-sheet links.

**The control cell.** `B5` is a forecast-year dropdown (FY2025 / FY2026 / FY2027) with
`Dash_YearIdx` on `B6 = MATCH(B5,{"FY2025","FY2026","FY2027"},0)`. Every KPI in the
scorecard uses `=CHOOSE(Dash_YearIdx, ...)` to pick the matching year from the staging
columns.

**The six-KPI scorecard** (one big cell per KPI, with a smaller "YoY change vs. prior
year" cell underneath each):
1. **Total Revenue** (A8 / A9)
2. **Gross Margin %** (D8 / D9)
3. **Operating Margin %** (G8 / G9)
4. **Net Earnings (SKX)** (A12 / A13)
5. **Diluted EPS** (D12 / D13)
6. **Free Cash Flow** (G12 / G13)

Example formula: `A8 = =CHOOSE(Dash_YearIdx, $X$8, $Y$8, $Z$8)` where X/Y/Z are the
staging columns for FY2025E / FY2026E / FY2027E. The YoY delta below is just the
selected-year value minus the prior-year value.

**The data-staging block (cols R:Z, hidden-friendly).** Three rows of context per
metric: row label (col R), then values for FY2020 / FY2021 / FY2022 / FY2023 / FY2024
(actual, cols S:W) / FY2025E / FY2026E / FY2027E (forecast, cols X:Z). The staging block
carries Wholesale revenue, DTC revenue, Total Revenue, Gross Margin %, Operating
Margin %, Net Margin %, DSO, DIO, DPO, Net Earnings (SKX), Diluted EPS, and Free Cash
Flow. The five charts (Revenue by Segment, Margin Trend, Working-Capital Days, FCF
Bridge, Scenario Comparison) all read from this staging area.

**The FY2025 scenario comparison block** (rows 19–22). Pulls the Bear / Base / Bull
Net Earnings and FCF figures directly from the Scenario Analysis tab so the dashboard
visualizes the spread without re-deriving it.

**The Model Integrity Checks table** (rows 45–51). The most important block on the
dashboard — four PASS/FAIL gates reading the live model:

| Check | FY2025 | FY2026 | FY2027 |
|---|---|---|---|
| BS Balance Check (Assets = L+E) | PASS | PASS | PASS |
| CF Ending Cash ties to BS Cash | PASS | PASS | PASS |
| IS Net Earnings = CF starting line | PASS | PASS | PASS |
| Retained Earnings consistent (via balance) | PASS | PASS | PASS |

**All four pass across every forecast year.** Formula example:
`=IF(ABS(BS_BalanceCheck_25)<1,"PASS","FAIL")`. The `<1` tolerance is **$1K rounding**.

**The dashboard is a model, not a screenshot.** Because every KPI, chart, and integrity
flag is a live formula reading the model via named ranges, flipping the scenario on
`Assumptions!B5` re-drives the entire dashboard. That's the wow factor — and it's also
the *honesty* factor, because the user can see the integrity checks update as the
scenario changes.

---

## 16. The Three-Statement Tie (deep dive)

If you only memorize one section of this model for an interview, memorize this one.

**What "three-statement tie" actually means.** The IS, BS, and CF aren't three
independent reports — they're three views of the same underlying activity. For the model
to be internally consistent:
1. The cash balance on the **BS** at year-end must equal the ending cash on the **CF**.
2. The change in **retained earnings** between years on the BS must equal **Net Earnings
   (SKX)** on the IS (less any dividends — Skechers pays none in this period).
3. Every change in a BS line must be reflected somewhere on the CF (working-capital
   changes, PP&E movements, debt rollforward, equity transactions).

If any of those break, you have a "model that doesn't tie."

**How this model achieves a *genuine* tie (not a forced one).** Standard junior-analyst
practice is to make cash a balancing plug — whatever number is needed to make Assets =
L+E. That works, but it hides errors: a mistake anywhere in the model just gets absorbed
into cash, and you'd never know.

This model does it the harder, better way:

1. **Cash starts as a plug.** The balance sheet was first built with cash as a
   temporary balancing variable, so every *other* line — working capital, PP&E, debt,
   retained earnings, equity rollforward — could be verified independently as correct.
2. **The cash flow statement is built separately.** The CF starts from Net Earnings,
   adds non-cash items (D&A, SBC), subtracts working-capital builds (which it derives
   from BS differences, using the indirect-method sign convention), nets out CapEx, debt
   repayments, and buybacks — and produces an ending cash balance entirely on its own.
3. **The CF ending cash is swapped into the BS cash line.** Now `BS Cash = CF Ending
   Cash` by **link**, not by plug.
4. **The balance check is now a real test.** With cash no longer free, the only way
   `Assets = L+E` is if every other line is right. **The fact that `B38 = 0` in every
   forecast year is the model proving its arithmetic.**

**The four integrity-check formulas on the dashboard** are the runtime evidence:
- BS Balance Check (`Assets − L+E` < $1K)
- CF Ending Cash ties to BS Cash (0 by linkage, but visible)
- IS Net Earnings = CF starting line (verifies the income-statement number is the same
  one flowing into the cash flow)
- Retained Earnings consistent (logically implied by the balance check passing)

**The other half: no circular reference.** Computing interest on beginning-of-period
debt freezes interest before it has a chance to feed back through NI → cash → debt →
interest. The workbook has **zero circular references**, **does not require iterative
calculation enabled**, and **recalculates cleanly on every change** in well under a
second.

---

## 17. Excel & Modeling Techniques Demonstrated

A consolidated checklist — useful for "what did you use?" questions.

**Excel mechanics**
- `CHOOSE` + `MATCH` for scenario and year switching.
- **Named ranges** (~150 of them) for cross-tab clarity and resilience to row inserts.
- **Cross-sheet references** with absolute and relative anchors.
- **Cell-level color coding** (blue / black / green / yellow).
- **`IF(ABS(x)<1,"PASS","FAIL")`** pattern for tolerance-based integrity checks.
- **Conditional formatting** on the Variance tab (direction-aware $/% variance display).
- Charts (line, bar, combo) wired to a staging area, not directly to the model.

**Financial modeling techniques**
- **Segment-level revenue and gross-margin build** (Wholesale + DTC) with a blended-GM
  consistency check.
- **BASE rollforwards** (Beginning + Additions − Subtractions = Ending) for PP&E, debt,
  and shares.
- **Interest on beginning-of-period debt** to break the circular loop.
- **Working capital from days ratios** (DSO/DIO/DPO converted to dollar balances via
  Sales/COGS × days / 365).
- **Indirect-method cash flow** with the correct sign convention (asset ↑ = use,
  liability ↑ = source).
- **Equity rollforward** combining net earnings, NCI, buybacks (treasury method), and
  SBC (paid-in capital).
- **CapEx-driven PP&E** with D&A as a fixed % of prior-year PP&E.
- **Two-variable sensitivity** built as a self-contained mini-model + formula-filled
  grids (engineered alternative to Excel Data Tables when inputs are formula cells).
- **Switchable Bear/Base/Bull** with three full driver blocks and a `CHOOSE`-driven
  Active block.

**FP&A workflow demonstrations**
- **Variance analysis** with budget calibration to public guidance, $/% variances, and
  written commentary.
- **Scenario recap** for executive comparison.
- **KPI dashboard** with year selector and YoY deltas.
- **Live model-integrity checks** reported on the dashboard.

**Data work**
- **Reconstruction of 5 years of full financials** from SEC 10-K filings, including
  segment detail and derived working-capital metrics.
- **XBRL-verified** balance-sheet numbers; residuals used to make "Other CA" and "Other
  LT Liabilities" reconcile to as-reported totals.

---

## 18. Key Results & Numbers to Memorize

Interviewers will want concrete numbers. Memorize the headline figures.

### FY2024 actuals (the launching pad)

| Metric | Value |
|---|---|
| Total Revenue | $8,969M |
| Gross Margin % | 53.2% |
| Operating Margin % | 10.1% |
| Net Earnings (SKX) | $639M |
| Diluted EPS | $4.16 |
| Free Cash Flow | $271M |
| Wholesale Rev / DTC Rev | $5,100M / $3,869M |
| DTC Mix % | 43.1% |
| Total Debt | $455M |
| Cash & Equivalents | $1,117M |
| Diluted Shares (M) | 153.8 |

### FY2025 Base (the headline forecast year)

| Metric | Value |
|---|---|
| Total Revenue | **$9,764M** |
| Gross Margin % | **53.3%** |
| Operating Margin % | **10.4%** |
| Net Earnings (SKX) | **$660M** |
| Diluted EPS | **$4.40** |
| Free Cash Flow | **$344M** |
| Ending Cash | **$1,060M** |
| DTC Mix % | 43.6% |

### Scenario spread (FY2025)

| Output | Bear | Base | Bull |
|---|---|---|---|
| Total Revenue ($000s) | 9,405,554 | 9,764,330 | 10,174,111 |
| Gross Margin % | 51.5% | 53.3% | 54.5% |
| Operating Margin % | 6.5% | 10.4% | 13.5% |
| Net Earnings (SKX, $000s) | 378,968 | 659,762 | 911,909 |
| Diluted EPS | $2.48 | $4.40 | $6.18 |
| Free Cash Flow ($000s) | 208,516 | 343,841 | 480,462 |

### Three-year Base trajectory

| Metric | FY2025E | FY2026E | FY2027E |
|---|---|---|---|
| Total Revenue ($000s) | 9,764,330 | 10,532,949 | 11,257,702 |
| Gross Margin % | 53.3% | 53.4% | 53.5% |
| Operating Margin % | 10.4% | 10.5% | 10.6% |
| Net Earnings (SKX) | 659,762 | 723,387 | 785,003 |
| Diluted EPS | $4.40 | $4.95 | $5.51 |
| Free Cash Flow | 343,841 | 552,999 | 721,724 |
| Ending Cash | 1,060,357 | 1,213,357 | 1,535,081 |
| Diluted Shares (M) | 149.9 | 146.2 | 142.5 |

### The four-takeaway story the model tells

1. **The DTC mix shift continues to expand blended gross margin.** DTC at 43.6% of revenue
   in FY2025E (vs. 43.1% in FY2024) lifts blended GM by ~10 bps; mix shift compounds out
   to 53.5% blended GM by FY2027.
2. **The Base case lines up with company guidance.** $9.76B revenue and $4.40 EPS land
   inside Skechers' February 2025 forward guidance — the Base case isn't a wishlist;
   it's calibrated.
3. **Operating leverage is real.** A roughly ±4% revenue swing across scenarios produces a
   ±40% EPS swing — buyback intensity (Bear $150K, Base $350K, Bull $500K in repurchases)
   amplifies it further.
4. **Cash generation strengthens through the period.** FCF rises from $344M (FY25) → $553M
   (FY26) → $722M (FY27) Base, as CapEx tapers from $650K → $550K → $500K and operating
   cash flow scales with the business.

---

## 19. Limitations & Honest Caveats

Volunteer these — knowing your model's limits signals maturity.

1. **Public data only.** Built entirely from SEC 10-K filings and the company's
   February 2025 forward guidance. No non-public diligence, no management interviews,
   no proprietary data.
2. **FY2021 tax-benefit anomaly.** FY2021 carries a **$346.8M one-time tax benefit** from
   an intra-entity IP transfer, which produces a *negative* effective tax rate of −43%
   and an artificially-high FY2021 EPS of $4.73. This is called out in the Historical
   tab (`A117`) and the README caveats. Comparing FY2021 numbers head-to-head with
   surrounding years without adjusting for this is misleading; the model uses the
   reported numbers as-is and documents the anomaly.
3. **The September 2025 take-private.** 3G Capital acquired Skechers in September 2025
   for **$9.4B / $63 per share**. The model is built on public data through FY2024 plus
   February-2025 guidance — the acquisition does not invalidate the modeling exercise,
   but it does mean the forecast can't be checked against subsequent public filings.
   This is documented in the README and the index.md page.
4. **Some lines are held flat.** Right-of-Use Assets, LT Lease Liabilities, Other
   Non-Current Assets, Other LT Liabilities, Current Lease Liabilities, Short-term
   Investments, and Other Equity (the non-RE portion's lease and other-account starting
   balance) are held at FY2024 values across all forecast years. A more thorough model
   would forecast lease activity and ST investment yield explicitly; this model
   deliberately holds them flat to keep the forecast focused on the operating drivers
   that matter for the thesis.
5. **Working capital is structural, not seasonal.** DSO/DIO/DPO are held flat in all
   scenarios because they're business-model features, not bets. A more sophisticated
   model would test sensitivity to working-capital intensity (especially DIO, where
   apparel/footwear inventory cycles can swing meaningfully).
6. **Beginning-of-period interest is a simplification.** It's the industry-standard way
   to avoid circular references, but it slightly under-states interest in years when
   debt rises and over-states it when debt falls. With $50K/year in repayments on a
   $455K starting balance, the effect is immaterial here — but worth flagging.
7. **No statistical or stochastic component.** This is a deterministic FP&A model. No
   Monte Carlo, no regression, no probabilistic distribution over scenarios. The
   Bear/Base/Bull spread is judgment, not statistics.
8. **Forecast is for analytical illustration; not investment advice.** Documented in the
   README.

---

## 20. Design Decisions & Trade-offs (the "Why")

Interviewers reward "why" answers. The deliberate choices and their rationale:

**Why model Wholesale and DTC separately rather than one blended revenue line?**
Because the thesis *is* the channel mix. Wholesale GM is ~40–43%; DTC GM is ~66%. Every
point of mix shift is worth ~25 bps of blended margin. Modeling them separately makes
the margin-expansion story visible and auditable. Blended growth would have hidden it.

**Why compute interest on beginning-of-period debt instead of average?**
Industry-standard simplification to break the interest → NI → cash → debt → interest
circular loop. Models without this either need iterative calculation enabled (slow,
opaque) or end up with circular-reference warnings the user has to ignore. With $50K
repayments on $455K starting balance, the precision loss is immaterial; the
architectural benefit (no circular references, fast recalc, clean dependency graph) is
substantial.

**Why build cash as a plug first, then swap in the CF ending cash?**
So the balance check is a real integrity test. If cash were a permanent plug, *any* error
anywhere in the model would silently flow into cash and the balance would always
"balance." By making cash a calculated value from CF, the balance check becomes the gate
— it can only equal zero if every other line is correct. The model proves itself.

**Why expose ~150 named ranges?**
Three reasons. (1) Readability: `=B8*(1+Wh_Growth_25)` is obviously next-year wholesale
revenue; `='Assumptions'!L13` is not. (2) Resilience: named ranges survive row inserts
that would break coordinate references. (3) Cross-sheet PASS/FAIL formulas: the
dashboard can read `IS_NetEarnings_25` from any tab without depending on the IS layout.

**Why three Bear/Base/Bull driver blocks side-by-side, plus an Active block?**
So all three scenarios are simultaneously visible (comparison without flipping the
selector) and the Active block isolates the single set of values the model actually uses
right now. Switching scenarios is one `CHOOSE` away. If the three blocks weren't visible
side-by-side, comparing the assumptions across scenarios would mean toggling the dropdown
three times.

**Why a self-contained FY2025 mini-model for the sensitivity tables?**
Because the main model's revenue-growth and gross-margin "inputs" are `CHOOSE`-driven
formula cells, and Excel's built-in Data Tables can only substitute into direct hardcoded
input cells. The engineering alternative — a self-contained FY2025 mini-model whose
inputs *are* direct cells, with each grid cell as a formula that swaps the row/column
values directly — preserves Bear/Base/Bull switchability *and* gives fully-live
sensitivity grids. The trade-off is that the sensitivity is on a simplified FY2025
mini-model (no WC dynamics, no buyback, no NCI on FCF), not the full forecast — which is
acceptable for a directional sensitivity view.

**Why three two-variable grids instead of one?**
Each highlights a different sensitivity surface. Grid 1 (Growth × GM) shows the **profit
sensitivity** of revenue size vs. margin quality. Grid 2 (Growth × OpEx %) shows the
**cost sensitivity** — same revenue size, what does the cost structure do to FCF. Grid 3
(Growth × CapEx) shows the **investment sensitivity** — what does reinvestment intensity
cost in near-term free cash flow.

**Why anchor the Base case to February 2025 forward guidance?**
Because the alternative is "I made up the numbers and they look reasonable to me." Tying
the Base case to management's public guidance makes the model defensible — the implicit
benchmark is the same one analysts and investors were working from.

**Why a year selector on the dashboard, not three side-by-side?**
Single-screen, executive-friendly layout. Three columns of KPIs would split attention;
one column of "current year" with a YoY delta line below each KPI gives a focused
scorecard. The user can flip the year to see the trajectory.

**Why does the dashboard show four integrity checks instead of one?**
Defense in depth. Each check tests a different part of the linkage — BS balance (overall
arithmetic), CF tie (the cash linkage specifically), IS-to-CF (the income statement
flows correctly into operating CF), and retained-earnings consistency. Showing all four
gives the reader confidence the model is consistent in multiple distinct senses, not
just by accident on one metric.

---

## 21. Interview Q&A

Practice these out loud. Answers are written the way you'd actually speak.

**Q1. Give me the overview of this model.**
"It's a full three-statement FP&A model for Skechers, built from public SEC 10-K filings.
I've got five years of historical actuals — 2020 through 2024 — and a three-year forecast
through 2027. The forecast is driven by a switchable Bear/Base/Bull set of assumptions
that I flip with one dropdown via `CHOOSE`/`MATCH`. The thesis is the DTC mix shift —
Skechers' direct channel grew from about 38.5% of revenue in 2020 to 43.1% in 2024, and
DTC carries roughly 66% gross margin versus 40–43% in Wholesale, so each point of mix
shift expands blended margin. I model the two segments separately to make that thesis
visible. The base case lands inside the company's February 2025 forward guidance, the
balance sheet ties to zero across all three scenarios in every forecast year, and the
dashboard has four live PASS/FAIL integrity checks that all read PASS."

**Q2. Walk me through the three-statement tie. How do you know it's a real tie and not a
forced plug?**
"I built it the harder way deliberately. The balance sheet was first built with cash as
a temporary plug — every other line, working capital, PP&E, debt, retained earnings, the
equity rollforward, all had to be independently correct. Then I built the cash flow
statement separately, indirect method, starting from net earnings, with the working
capital changes derived from the BS deltas. Then I swapped the CF ending cash into the
BS cash line. Now cash is no longer a free variable. The only way Assets equals L plus E
is if every other line is right. The balance check on the BS reads zero across all three
forecast years in all three scenarios — and that's a real arithmetic gate, not a forced
zero. The dashboard reports it as a live PASS."

**Q3. How do you handle the circular reference between interest expense and cash?**
"I compute interest on beginning-of-period debt. So FY25 interest is FY24 ending debt
times 5%, not FY25 average debt and not FY25 ending debt. That breaks the loop —
interest no longer depends on FY25 net income, cash, or debt movement, so there's no
circular dependency. It's the industry-standard simplification, the precision loss is
negligible at our debt levels — we're talking $50K of repayments on $455K starting
balance — and the architectural benefit is that the workbook has zero circular references
and doesn't need iterative calculation enabled."

**Q4. How does the scenario switching actually work?**
"There's a dropdown on the Assumptions tab in cell B5 — Bear, Base, or Bull. That feeds
a `MATCH` formula in E5 that returns 1, 2, or 3, called `ScenarioIndex`. Every assumption
on the Assumptions tab has its three scenario values side-by-side, and then an Active
column where each cell is a `CHOOSE($E$5, Bear, Base, Bull)` formula. The IS, BS, CF,
schedules, and dashboard all reference the Active column through named ranges. So
flipping the dropdown re-drives every forecast cell in the workbook in one click. The
Bear/Base/Bull recap table on the Scenario Analysis tab also pre-captures the snapshot
values, because the model can only display one scenario at a time."

**Q5. Why model Wholesale and DTC separately?**
"Because the channel mix shift *is* the story. DTC gross margin is roughly 66%,
Wholesale is 40–43%. Every point of mix shift toward DTC expands blended gross margin.
Skechers went from 38.5% DTC in 2020 to 43.1% in 2024, and that mix shift drove most of
the blended margin expansion over those years. If I modeled one blended revenue line,
the thesis disappears into an averaged number. By forecasting each segment separately —
with its own growth rate and its own gross margin — I make the mix-shift story explicit
and auditable. There's also a blended-GM consistency check on the IS that confirms the
segment math ties to the consolidated number."

**Q6. How does the working capital forecast work?**
"I drive accounts receivable, inventory, and accounts payable from days ratios. AR
equals sales times DSO over 365 — so 40 days of receivables on $9.76B of sales gives me
about $1.07B in AR. Inventory equals COGS times DIO over 365 — 165 days. AP equals COGS
times DPO over 365 — 108 days. These aren't hardcoded values; they're formulas that
respond to the revenue and COGS forecasts. The change in net working capital from year
to year automatically flows through to the indirect-method cash flow statement as
operating-cash-flow adjustments."

**Q7. Why a sensitivity grid built by hand instead of Excel's Data Tables?**
"Because my actual model inputs — the revenue-growth and gross-margin Active cells — are
`CHOOSE` formulas, not direct hardcoded cells. Excel Data Tables only substitute into
direct input cells, so they don't work here. The alternative I built is a self-contained
FY2025 mini-model on the Scenario tab, with its own four direct input cells — growth,
GM, OpEx %, CapEx — and three two-variable grids where each cell is a formula that swaps
the row and column values directly into a mini income statement. Each cell recomputes
live; the whole grid updates if I change any of the base constants. The trade-off is
that the sensitivity is on a simplified single-year mini-model — no working capital
movement, no NCI on FCF — but for a directional sensitivity view that's fine, and the
main forecast tabs still drive everything else."

**Q8. What's the Bear/Base/Bull spread tell you about Skechers' operating leverage?**
"That it's significant. The revenue spread across scenarios is about ±4% — Bear
$9.4B, Base $9.76B, Bull $10.17B. The EPS spread is about ±40% — Bear $2.48, Base
$4.40, Bull $6.18. So a small revenue swing produces a much bigger EPS swing. That's
classic operating leverage — fixed cost base that doesn't scale linearly with revenue, so
gross profit changes flow disproportionately to the bottom line. The buyback intensity
amplifies it too: Bear has $150K of buybacks, Base $350K, Bull $500K, so Bull also has
a lower share count to divide earnings into."

**Q9. Why anchor the Base case to forward guidance?**
"Two reasons. One, defensibility — saying 'I made these numbers up and they feel
reasonable' is not a good answer in a real meeting. Saying 'the Base case is calibrated
to management's February 2025 forward guidance' is. Two, it forces the model to be
honest. If my Base case had been $11B in revenue, I'd be implicitly betting against
management — and unless I have a non-public reason to do that, I shouldn't. Bear and Bull
are still my judgment calls, but they bracket a defensible Base."

**Q10. The dashboard has four PASS/FAIL checks. Why four and not one?**
"Defense in depth. Each one tests a different aspect of the model integrity. The first is
the overall balance check — Assets minus Liabilities plus Equity equals zero. The second
is the cash flow tie specifically — CF ending cash equals BS cash. The third is that
the income statement's net earnings number is the same number flowing into the CF as the
indirect-method starting line. The fourth is retained earnings consistency. They're not
all independent — if the balance check passes, retained earnings is consistent by
implication — but showing all four gives the reader confidence the model is consistent
in multiple distinct senses. It's also a UX thing: a single red FAIL would be ambiguous;
four green PASSes is unambiguous."

**Q11. What's the FY2021 weirdness with the tax line?**
"FY2021 has a $346.8M one-time tax benefit from an intra-entity IP transfer — Skechers
moved intellectual property between legal entities, which generated a one-time tax
benefit under U.S. tax law. So FY2021 effective tax rate is *negative* — minus 43% —
and net earnings and EPS spike that year. EPS was $4.73 in FY2021 versus $0.64 in FY2020.
I documented it in the historical tab notes and in the README caveats, because if you
just look at the FY2020-21 EPS jump without that context, the trend looks completely
wrong. It's the most important caveat in the historical data."

**Q12. What's a 'named range' and why did you use so many?**
"A named range is a label you attach to a cell or range of cells, so you can reference
it by name in formulas — `Wh_Growth_25` instead of `Assumptions!L13`. I used about 150
of them. Three reasons. One, readability: `=B8*(1+Wh_Growth_25)` is obviously next-year
wholesale revenue. Two, resilience: if I insert a row on the Assumptions tab, every
coordinate reference would silently shift; named ranges follow the cell automatically.
Three, the dashboard's integrity check formulas can read the live model — like
`IS_NetEarnings_25` — without depending on the IS tab's row layout."

**Q13. If you kept building this, what would you improve?**
"A few things. I'd model leases more explicitly instead of holding them flat — adding
new ROU assets and lease liabilities based on store-count and DTC-buildout assumptions.
I'd build sensitivity to working-capital intensity, because for an apparel/footwear
company DIO is a real lever — a 10-day swing in inventory days is meaningful on
$5B-plus of COGS. I'd add a discounted cash flow valuation tab as a logical extension
of the FCF forecast. And I'd build a stochastic layer — Monte Carlo over the key
drivers — to produce a probability distribution of FY25 EPS rather than three discrete
scenarios. Long term, this is a planning model; with a DCF and probabilistic layer
it would also be a valuation model."

**Q14. Why Excel and not Python for this?**
"Deliberate. FP&A teams run on Excel. Even teams that build big things in Python ship
the deliverable to leadership in Excel because that's where the audience lives. This
model is meant to read like real FP&A work — a senior person can open it, click through
the Assumptions tab, change the dropdown, and watch the dashboard re-drive. That's the
right artifact for the role. I also use Python to *build* the file via openpyxl as part
of the development workflow, but the deliverable is Excel."

**Q15. How do you know your forecast numbers are reasonable, not just internally
consistent?**
"Three calibration anchors. First, the Base-case FY2025 revenue is $9.76B and EPS is
$4.40 — both inside Skechers' February 2025 forward guidance, so the Base lines up
with what management itself was telling the market. Second, the working capital drivers
— DSO 40, DIO 165, DPO 108 — are calibrated to FY2024 actuals on the historical tab,
where I computed them from the as-reported balance sheet and income statement. Third,
the operating-margin trajectory of 10.4% to 10.6% across the forecast is consistent with
the historical trend of 10.1% in FY2024 — modest, plausible expansion driven by mix
shift, not a step-change. Internal consistency proves the model arithmetic; calibration
to actuals and guidance proves the inputs are reasonable."

---

## 22. How to Walk Through This Project Live

If asked to screen-share the workbook, use this order. About 8–10 minutes.

1. **Open the README first.** It's the front door. Point out the model map, the color
   legend, and especially the **live integrity status table** with all PASSes — "this is
   the headline: the model balances and ties across every forecast year."
2. **State the thesis** — "Skechers has two segments, Wholesale and DTC. DTC is roughly
   twice the gross margin of Wholesale and has been growing as a share of revenue. This
   model forecasts each segment separately so the mix-shift margin story is visible."
3. **Open the Historical Financials tab.** Walk the segment block briefly: DTC mix going
   from 38.5% to 43.1%, DTC gross margin around 66% vs. Wholesale at 40–43%. Mention the
   FY2021 tax anomaly if asked about EPS volatility.
4. **Open the Assumptions tab.** Show the dropdown on B5. Flip it once Bear → Base → Bull
   and let the watcher see the Active column on the right change. Point out that the
   working-capital ratios and tax rate are held flat — those are structural — while
   growth, margin, OpEx, and CapEx vary.
5. **Show the Income Statement Forecast.** Point out the segment build at the top — WH
   revenue × (1 + Wh_Growth), DTC revenue × (1 + DTC_Growth), the COGS lines using the
   segment GMs, and the consolidated build below. **Point out the blended-GM check at
   the bottom (= 0).**
6. **Open Supporting Schedules.** Spend a moment on the **interest-expense row** —
   "this is on beginning-of-period debt, which is the standard simplification that
   breaks the circular reference. No iterative calculation needed, no circular warning."
7. **Open the Cash Flow Forecast.** Show the indirect-method structure. Show the
   ending cash row. Show the tie check below — "this row equals zero because CF ending
   cash is what the BS cash line points at."
8. **Open the Balance Sheet Forecast.** Point at the cash line — "this links to CF
   ending cash." Then point at the **balance check at row 38 — zero across all three
   forecast years.** "That's a real test: cash is no longer a plug, so the only way
   that's zero is if every other line is right."
9. **Open the Scenario Analysis tab.** Show the recap table — Bear/Base/Bull side by side.
   Then scroll to the sensitivity grids. "Each grid cell is a formula, not a static
   value. I built a self-contained FY2025 mini-model on this tab so the sensitivity stays
   live even though the main model's inputs are `CHOOSE` formulas that Excel's built-in
   Data Tables can't drive."
10. **End on the KPI Dashboard.** Flip the year selector once (FY2025 → FY2026 → FY2027)
    to show the scorecard re-drive. Show the four-row integrity table — "all PASS, every
    year, every scenario." If time permits, flip the scenario back on Assumptions!B5 and
    watch the dashboard re-compute in real time.

**Pacing tip:** spend the most time on Assumptions + the three statement forecast tabs +
the integrity story. The dashboard is the wow factor to close on.

---

## 23. Glossary

- **3-statement model** — an income statement, balance sheet, and cash flow statement that
  fully articulate, so a change to any driver flows correctly through all three.
- **Active block** — the column block (L:N) on the Assumptions tab whose cells are
  `CHOOSE` formulas selecting one of the three scenario values. The whole model reads
  from this block.
- **Articulate / articulation** — when the three financial statements link to each other
  correctly: net income flows from IS to CF and to retained earnings on BS; cash on BS
  equals CF ending cash; WC changes on BS appear as adjustments on CF.
- **BASE rollforward** — the standard schedule structure: **B**eginning + **A**dditions −
  **S**ubtractions = **E**nding. Used here for PP&E, debt, and shares.
- **Bear / Base / Bull** — three scenarios capturing a pessimistic, central, and optimistic
  view of the forecast drivers.
- **Beginning-of-period interest** — computing interest expense on the debt balance at the
  start of the year, not the average or ending. Breaks the interest → NI → cash → debt
  circular loop.
- **Blended gross margin** — total gross profit ÷ total revenue, across all segments.
- **CapEx** — capital expenditures; cash outflow to acquire long-lived assets (PP&E).
- **Cash conversion cycle (CCC)** — DSO + DIO − DPO; days between paying for inputs and
  receiving cash from sales.
- **`CHOOSE`** — Excel function that returns one of a list of values based on an index.
  Used with `MATCH` for the scenario switch.
- **D&A** — depreciation and amortization; non-cash expense recognizing PP&E and
  intangible-asset consumption.
- **DSO / DIO / DPO** — Days Sales Outstanding (AR ÷ Sales × 365), Days Inventory
  Outstanding (Inv ÷ COGS × 365), Days Payable Outstanding (AP ÷ COGS × 365).
- **DTC (Direct-to-Consumer)** — Skechers' direct channel: e-commerce and company-owned
  retail stores. Higher gross margin than Wholesale.
- **EBIT / EBT / Net Earnings** — Earnings Before Interest and Tax / Before Tax / After
  Tax (and before/after NCI).
- **EBITDA** — Earnings Before Interest, Tax, Depreciation, and Amortization. Not a
  primary line in this model but implicitly = EBIT + D&A.
- **EPS (Diluted)** — Net Earnings (SKX) ÷ Diluted Shares Outstanding.
- **Free Cash Flow (FCF)** — Operating Cash Flow + CapEx (CapEx is negative, so this is
  OCF − |CapEx|). Cash left after maintenance investment.
- **Forecast period / projection period** — FY2025–FY2027 in this model.
- **G&A** — General & Administrative expenses; one of two operating expense buckets.
- **Indirect method** — the most common way to build the operating section of the cash
  flow statement: start from net income, add back non-cash items (D&A, SBC), adjust for
  working-capital changes.
- **Integrity check** — a formula that verifies the model is internally consistent
  (e.g., Assets = L+E, CF ending cash = BS cash).
- **`MATCH`** — Excel function that returns the position of a value in an array. Used
  here to convert the scenario name to an index (Bear → 1, Base → 2, Bull → 3).
- **Named range** — a label attached to a cell or range; can be used in formulas in place
  of the coordinate reference.
- **NCI (Non-Controlling Interest)** — the portion of a subsidiary's earnings/equity owned
  by minority shareholders, not the parent. Held at 12% of net earnings in this model.
- **OCF / ICF / FCF (CF sections)** — Operating, Investing, and Financing Cash Flow.
- **OpEx** — Operating Expenses; here = Selling + G&A.
- **Operating Leverage** — the degree to which a small change in revenue produces a
  larger change in operating income (and EPS), driven by a fixed-cost base.
- **PASS/FAIL gate** — an `IF(ABS(x)<tolerance,"PASS","FAIL")` formula on a check line.
- **Plug** — a balancing variable. In an early draft of the model, cash was the plug;
  it was replaced by a calculated value from CF.
- **PP&E** — Property, Plant, and Equipment. Long-lived productive assets, net of
  accumulated depreciation.
- **Retained Earnings (RE)** — the cumulative portion of past net earnings retained in
  the business rather than paid out. Rolls forward as `Prior RE + Net Earnings − Dividends`
  (Skechers pays no dividend in this period).
- **ROU (Right-of-Use) Assets** — the operating-lease asset under ASC 842 lease accounting.
- **SBC (Stock-Based Compensation)** — non-cash expense for employee stock awards. Added
  back on CF; credited to paid-in capital on BS.
- **Segment / Reportable Segment** — operating divisions a company discloses separately.
  Skechers reports Wholesale and DTC.
- **Sensitivity table / Data Table** — a two-input grid showing how an output changes as
  two drivers vary. Here, built as a self-contained mini-model with formula-filled grids.
- **Tax benefit / one-time item** — a non-recurring item (e.g., FY2021's $346.8M tax
  benefit from an intra-entity IP transfer) that distorts a single year's effective
  tax rate.
- **Three-statement tie** — the property that the IS, BS, and CF all articulate
  consistently — a change anywhere flows correctly to everywhere.
- **Wholesale** — Skechers' indirect channel: sales to retailers, distributors, and
  third-party platforms. Lower gross margin than DTC.
- **Working capital (WC)** — Current Assets − Current Liabilities (a balance sheet
  concept); the operating-cash investment required to run the business.
- **XBRL** — eXtensible Business Reporting Language; the structured-data format SEC
  filings use, which makes filings machine-readable.

---

*This study guide documents the model as built. The authoritative reference is the
workbook `excel/SKX_Financial_Analysis_Project_Final.xlsx` — its Assumptions dropdown,
the Active block, the IS/BS/CF forecast tabs, the Scenario Analysis sensitivity grids,
and the KPI Dashboard's live integrity checks. When this guide and the workbook
disagree, the workbook wins.*
