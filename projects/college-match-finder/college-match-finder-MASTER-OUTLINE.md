# Master Outline & Study Guide
## College Match Finder — a weighted multi-criteria college recommendation app (Streamlit / Python)

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.
>
> **One sentence to anchor everything:** College Match Finder lets a student define what
> "fit" means by weighting the criteria *themselves*, then scores every U.S. college on
> those weights using a transparent percentile-rank engine fed by 12 federal data sources —
> the hard part was never the UI, it was the data layer.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Context)](#2-why-this-project-exists-context)
3. [The Tech Stack at a Glance](#3-the-tech-stack-at-a-glance)
4. [End-to-End Architecture](#4-end-to-end-architecture)
5. [The Data Layer — 12 Federal Sources](#5-the-data-layer--12-federal-sources)
6. [The Data Prep Pipeline](#6-the-data-prep-pipeline)
7. [The Scoring Engine (the core technical piece)](#7-the-scoring-engine-the-core-technical-piece)
8. [Tab 1 — School Finder](#8-tab-1--school-finder)
9. [Tab 2 — Major Explorer](#9-tab-2--major-explorer)
10. [Tab 3 — Find Your Fit (RIASEC)](#10-tab-3--find-your-fit-riasec)
11. [Cross-Tab Integration & Session State](#11-cross-tab-integration--session-state)
12. [Statistical Depth Features](#12-statistical-depth-features)
13. [Accessibility (a real differentiator)](#13-accessibility-a-real-differentiator)
14. [Testing — 297 Tests](#14-testing--297-tests)
15. [Methodology Decisions (the "why we cut X" stories)](#15-methodology-decisions-the-why-we-cut-x-stories)
16. [Engineering Decisions & Code Highlights](#16-engineering-decisions--code-highlights)
17. [The Build Process](#17-the-build-process)
18. [Limitations & Honest Caveats](#18-limitations--honest-caveats)
19. [Interview Q&A](#19-interview-qa)
20. [How to Walk Through This Project Live](#20-how-to-walk-through-this-project-live)
21. [Glossary](#21-glossary)

---

## 1. The 30-Second Pitch

College Match Finder is an **interactive college recommendation tool** built in **Python
and Streamlit**. Instead of publishing one composite ranking it defines for you — the way
*U.S. News* does — it **exposes the weights and lets the user define "fit" themselves**. A
student sets sliders for the priorities they actually care about (cost, earnings,
graduation rate, selectivity, debt, retention, loan repayment), filters down to their
realistic applicant pool, and the app **scores and ranks every U.S. college** on *their*
weights.

It has **three tabs**: **School Finder** (rank schools on your weighted priorities),
**Major Explorer** (pick any of ~410 majors and see wages, job growth, top industries, a
geographic employment map, and which schools have the strongest programs), and **Find Your
Fit** (a 60-question RIASEC interest questionnaire that recommends majors aligned to your
interest profile).

The headline of the project is **the data layer**: 12 independent federal and labor-market
datasets — College Scorecard, BLS OEWS, BLS Employment Projections, O\*NET, NY Fed, NCES —
at different granularities and update cycles, joined and normalized into something
queryable in milliseconds from a browser. It ships with **297 automated tests**, WCAG-verified
accessibility, a PDF/CSV export, and a deployed live app.

**One-line version:** "I built a Streamlit app that lets students rank every U.S. college
on their own weighted priorities — the engineering challenge was integrating 12 federal
data sources into a transparent scoring engine, with a full test suite and verified
accessibility."

**Live app:** https://nadeaujonnycollegematchfinder.streamlit.app

---

## 2. Why This Project Exists (Context)

**The problem with college rankings.** Every ranking product — *U.S. News*, Niche, Forbes —
publishes a single composite score whose recipe *they* chose. A student who cares most
about graduating debt-free is handed the same #1 as a student chasing maximum prestige.
The weights are hidden, and they're not the user's.

**The product idea.** Flip it: make the weights the *input*. The user moves seven sliders
to say what matters to them, and the app ranks schools on *that*. "Fit" becomes
user-defined and transparent — you can always see *why* a school ranked where it did.

**The real engineering challenge — the data layer.** Building sliders is easy. The hard
part: **12 independent federal datasets**, each with its own granularity (institution,
program, occupation, state), its own update cadence (annual, biennial, irregular), its own
unit structure (CIP codes, SOC codes, NAICS codes, FIPS), and its own suppression and
missing-value conventions. Joining all of that into a coherent model that answers a query
in a few hundred milliseconds from a Streamlit frontend is the actual work.

**Who it's for.** Students, parents, and college counselors — a non-technical audience.
That drove decisions toward transparency (every score is explained, every data source is
documented in-app) and accessibility (screen-reader captions, WCAG-checked colors).

**Why it's a strong portfolio project.** It is a complete product, not a notebook: a real
data-integration pipeline, a defensible statistical scoring method, a three-surface
interactive app, a 297-test suite, documented accessibility work, and a live deployment.
It demonstrates data engineering, applied statistics, product thinking, and software
discipline together.

---

## 3. The Tech Stack at a Glance

| Layer | Choice | Role |
|---|---|---|
| **Language** | Python 3 | Everything — data prep, scoring, app. |
| **App framework** | **Streamlit** (1.56) | The entire UI — sidebar, three tabs, widgets, session state. Pure-Python, no separate frontend. |
| **Data** | **pandas** (3.0) + **NumPy** (2.4) | All cleaning, joining, aggregation, and the scoring math. |
| **Charts** | **Plotly** (6.7) | Every visual — radar charts, choropleths, scattermapbox, bar charts. |
| **PDF export** | **fpdf2** (2.8) | Generates the downloadable ranked-results PDF report. |
| **Config files** | **PyYAML** (6.0) | Loads `riasec_items.yaml`, `major_descriptions.yaml`, crosswalk YAML. |
| **Excel ingest** | **openpyxl** (3.1) | Reads the raw BLS/O\*NET/NCES `.xlsx` source files in the data-prep scripts. |
| **Testing** | **pytest** | 297 tests covering scoring, data pipeline, and UI contracts. |
| **Hosting** | **Streamlit Community Cloud** | Free deployment from the GitHub monorepo; the live app. |

**The mental model:** Streamlit *is* the app — there's no separate React frontend or API
server. The Python file `app.py` runs top-to-bottom on every interaction, reads/writes
`st.session_state`, and Streamlit diffs the result into the browser over a WebSocket. That
architecture is the source of both the project's simplicity and its quirks (see §11 and §13).

**What ships in the repo.** The cleaned data CSVs (`data/cleaned/`) are *committed*, so
`pip install -r requirements.txt && streamlit run app.py` works immediately. The
`data_prep_*.py` scripts regenerate those CSVs from raw federal files but are **not needed
for normal use** — they're the build tooling for the data layer.

---

## 4. End-to-End Architecture

```
  12 RAW FEDERAL DATA SOURCES  (College Scorecard, BLS OEWS, BLS Projections,
  (.csv / .xlsx in data/raw/)   O*NET, NY Fed, NCES crosswalk)
        │
        │   5 data-prep scripts (run once, offline — the "build" of the data layer)
        │   data_prep.py · data_prep_geo.py · data_prep_majors.py
        │   data_prep_riasec.py · data_prep_workcontext.py
        ▼
  ┌──────────────────────────────────────────────────────────────┐
  │ data/cleaned/  — 12 committed CSVs  +  data/processed/*.parquet │
  │  colleges_cleaned.csv (~2,477 schools) · field_of_study_cleaned │
  │  major_outcomes · occupations_master · cip4_to_soc ·           │
  │  cip4_state_employment · cip4_work_context · cip4_riasec ·     │
  │  soc_to_naics3 · cip4_naics3_distribution · state_occupations  │
  └──────────────────────────┬───────────────────────────────────┘
                             │  loaded at startup (cached with @st.cache_data)
                             ▼
  ┌──────────────────────────────────────────────────────────────┐
  │ app.py — Streamlit entry point                                 │
  │  · sidebar: filters + 7 weight sliders + presets               │
  │  · session state init + URL state parse/write                  │
  │  · st.tabs([School Finder, Major Explorer, Find Your Fit])      │
  │                                                                 │
  │  scoring.py   — the weighted multi-criteria scoring engine      │
  │  config.py    — column maps, scoring dimensions, PALETTE        │
  │  utils.py     — badges, CIP helpers, WCAG contrast math         │
  │  page_modules/— one module per tab                             │
  │  + domain modules (riasec_matching, profiles, url_state, …)     │
  └──────────────────────────┬───────────────────────────────────┘
                             │  deployed via Streamlit Community Cloud
                             ▼
              Live app — nadeaujonnycollegematchfinder.streamlit.app
```

**The two-stage design — the single most important architectural fact.** There is a hard
split between an **offline data-prep stage** and an **online app stage**:

- **Offline (build time):** the `data_prep_*.py` scripts ingest gigabytes of raw federal
  files, do all the heavy joining/aggregation/cleaning *once*, and write small, clean CSVs.
- **Online (run time):** the app only ever loads those small cleaned CSVs. It never touches
  a raw file. This is why the app is fast — all the expensive work already happened.

**The module layout** (a clean separation of concerns):

- `app.py` — entry point: sidebar, tab routing, session state, the School Finder tab's
  rendering, export, and map.
- `config.py` — *single source of truth* for constants: the raw→clean column rename map,
  category lookups, the 7 scoring-dimension definitions, and the `PALETTE` color dict.
- `scoring.py` — the pure scoring engine (no Streamlit import — fully unit-testable).
- `utils.py` — shared helpers: acceptance classification, CIP-code formatting, WCAG
  contrast math. Also no Streamlit import.
- `page_modules/` — one module per tab: `school_finder.py`, `major_explorer.py`,
  `find_your_fit.py`, `about_the_data.py`.
- Domain modules — `riasec_matching.py`, `riasec_questionnaire.py`,
  `riasec_distribution.py`, `profiles.py`, `url_state.py`, `major_descriptions.py`,
  `naics_distribution.py`, `nyfed_outcomes.py`.

**Layering rule worth knowing:** `scoring.py` and `utils.py` deliberately have **no
`import streamlit`** so they can be imported by test code that runs without a Streamlit
session. Anything that needs `st` lives in `app.py` or `page_modules/`. (This is exactly
why `render_about_the_data()` was placed in `page_modules/about_the_data.py` and not
`utils.py`.)

---

## 5. The Data Layer — 12 Federal Sources

All 12 sources are free, public U.S. government / federally-funded data. They group into
**five categories**. The live app documents every one in an in-app "About the Data"
expander with snapshot dates and URLs.

### Schools (2 sources)
1. **College Scorecard — Institution-Level data** (Oct 2025 release). The main file. One
   row per Title IV college, thousands of columns. Drives every School Finder scoring
   dimension: admissions, enrollment, test scores, net prices, graduation/retention,
   earnings, debt, repayment.
2. **College Scorecard — Field of Study data** (Apr 2025). Program-level (by CIP code)
   1-year and 5-year graduate earnings and median debt. Powers school detail cards and
   Major Explorer's program-outcomes panel.

### Majors (3 sources)
3. **NCES CIP–SOC Crosswalk** (CIP 2020 / SOC 2018 edition). A many-to-many map from
   6-digit CIP codes (academic programs) to 6-digit SOC codes (occupations). The backbone
   that lets the app route a *major* to its likely *occupations*.
4. **Hand-authored major descriptions** — 60 top-enrolled majors have hand-written
   descriptions; the remaining ~350 use auto-generated stubs.
5. **Derived Major Outcomes table** — aggregates wage/growth/openings per 4-digit CIP code.

### Careers (3 sources)
6. **BLS OEWS — Occupational Employment & Wage Statistics, National** (May 2024). Wage
   percentiles (10th/25th/median/75th/90th) by occupation.
7. **BLS Employment Projections** (2024–2034 cycle). 10-year projected employment growth
   and annual job openings per occupation.
8. **BLS NAICS-by-SOC industry distribution** (May 2024). Which industries employ each
   occupation — powers Major Explorer's "Top industries" panel.

### Geography (1 source)
9. **BLS OEWS — State-Level data** (May 2024). State-by-occupation employment counts and
   **location quotient** (concentration relative to the national average) — feeds the
   geographic choropleth.

### Interests (3 sources)
10. **O\*NET 30.2 Work Context** (Feb 2026). Per-occupation work-environment ratings
    (time pressure, autonomy, physical demands, etc.) — the Work Environment panel.
11. **O\*NET 30.2 RIASEC Interest Profiles** (Feb 2026). Per-occupation Holland-code
    interest scores — powers the Find Your Fit questionnaire matching.
12. **NY Fed Labor Market Outcomes for Recent College Graduates** (Feb 2026). Unemployment,
    underemployment, and early/mid-career wages by broad major.

**The "code soup" that ties it together — know these acronyms cold:**

- **CIP** = Classification of Instructional Programs — the code for an *academic program /
  major* (e.g., 11.07 = Computer Science). The app works at **CIP4** (4-digit) granularity.
- **SOC** = Standard Occupational Classification — the code for an *occupation / job*.
- **NAICS** = North American Industry Classification System — the code for an *industry*.
- The pipeline chains them: **CIP (major) → SOC (occupations) → NAICS (industries)**, and
  separately SOC → state employment, SOC → wages, SOC → RIASEC scores.

**Data recency spans ~21 months** — from May 2024 (BLS OEWS) to February 2026 (O\*NET 30.2,
NY Fed). The app's freshness caption states this honestly: "Data through May 2024, with
some sources updated as recently as February 2026."

---

## 6. The Data Prep Pipeline

Five `data_prep_*.py` scripts turn the raw federal files into the clean CSVs the app loads.
They run **offline, once** — they are the build system for the data layer. Each is a good
"ETL" talking point.

| Script | Ingests | Produces |
|---|---|---|
| **`data_prep.py`** | College Scorecard Institution-Level (3,300+ columns) + Field of Study + NY Fed Excel | `colleges_cleaned.csv` (~2,477 schools), `field_of_study_cleaned.csv`, `nyfed_outcomes.parquet` |
| **`data_prep_geo.py`** | BLS OEWS State May 2024 (`state_M2024_dl.xlsx`) | `state_occupations.csv` (~36k rows) |
| **`data_prep_majors.py`** | NCES CIP–SOC crosswalk + BLS OEWS National + BLS Employment Projections | `occupations_master.csv` (832 occs), `cip4_to_soc.csv`, `major_outcomes.csv` (~414 majors), `cip4_state_employment.csv`, `cip4_work_context.csv`, `soc_to_naics3.csv`, `cip4_naics3_distribution.csv` |
| **`data_prep_riasec.py`** | O\*NET 30.2 Interests | `cip4_riasec.csv` (416 majors × 6 RIASEC scores) |
| **`data_prep_workcontext.py`** | O\*NET 30.2 Work Context (~298k rows) | `work_context.csv` |

**The recurring data-engineering patterns** — these are what to talk about:

- **Column renaming as a contract.** Scorecard's raw columns have cryptic uppercase names
  (`ADM_RATE`, `MD_EARN_WNE_P10`, `NPT41_PUB`). `config.SCORECARD_COLUMN_RENAMES` maps every
  one to a readable snake_case name (`admission_rate`, `median_earnings_10yr`,
  `net_price_public_0_30k`). Renaming lives in *one place* so a source schema change is a
  one-line fix.
- **Leading-zero preservation.** CIP and SOC codes have meaningful leading zeros
  (`01.0901`). Every script reads them with `dtype=str` so pandas doesn't silently turn
  `01.09` into the number `1.09`.
- **Suppression handling.** BLS marks suppressed cells with sentinels (`*`, `**`, `#`).
  The geo script converts these to `NaN` rather than letting them poison numeric columns.
- **Employment-weighted aggregation — the signature transform.** A major (CIP) maps to
  *many* occupations (SOC). To get one wage/growth/RIASEC number per major, the pipeline
  takes an **employment-weighted average** across the major's routing occupations — an
  occupation that employs 500,000 people counts more than one employing 5,000. This is how
  `major_outcomes.csv` and `cip4_riasec.csv` are built.
- **Coverage thresholds.** `cip4_state_employment` only keeps a state-major cell if it
  meets a 50% data-coverage threshold; `cip4_riasec` records a `coverage_pct` per major so
  the app can flag low-confidence matches.

**`scripts/rank_top_cip4.py`** is a supporting script: it ranks majors by bachelor's
degrees conferred to pick the **top 60** that earned hand-authored descriptions.

---

## 7. The Scoring Engine (the core technical piece)

`scoring.py` is the heart of the project — a **pure, dependency-light, fully unit-tested**
weighted multi-criteria scoring engine. It imports only pandas, NumPy, and `config` — no
Streamlit — so all 27 of its tests run without a browser. **This is the section to know
best.**

### 7.1 The 7 scoring dimensions

Defined in `config.SCORING_DIMENSIONS`. Each has a column, a direction, and a label:

| Dimension key | Label | Column | Direction |
|---|---|---|---|
| `affordability` | Low Net Price | `net_price` (or income-bracket column) | lower is better |
| `graduation_rate` | High Graduation Rate | `graduation_rate` | higher is better |
| `retention_rate` | High Retention Rate | `retention_rate_4yr` | higher is better |
| `earnings` | High Earnings After Graduation | `median_earnings_10yr` | higher is better |
| `selectivity` | High Selectivity | `admission_rate` | lower is better |
| `low_debt` | Low Student Debt | `median_debt` | lower is better |
| `repayment` | High Loan Repayment Rate | `repayment_rate_3yr` | higher is better |

*(Accuracy note for interviews: the **code is authoritative — there are 7 dimensions, and
these are them.** The portfolio page and README describe the set slightly differently — the
README says "eight dimensions … diversity" and `index.md` mentions "student-to-faculty
ratio." Neither matches `config.py`; if asked, cite the seven above. The discrepancy is a
documentation drift, not a code issue.)*

### 7.2 `compute_scores()` — the four-step algorithm

This is the function to be able to narrate end to end:

**Step 1 — Drop zero-weighted dimensions.** Any slider the user left at 0 is removed
entirely. A school missing data on a dimension the user doesn't care about contributes
nothing either way.

**Step 2 — Normalize each dimension to a percentile rank.** `normalize_column()` converts
each raw metric column to a **percentile rank on [0, 1]** using
`series.rank(pct=True, method="average")`, where **1.0 = best in the filtered field.** Two
deliberate choices here:
- **Percentile rank, not min-max.** Min-max scaling lets a single outlier (one
  ultra-expensive school) compress everyone else into a narrow band. Percentile rank is
  outlier-robust, *and* the result is directly interpretable — "85th percentile for
  earnings" is a sentence a student understands.
- **Direction handled at normalization.** "Lower is better" metrics (net price, admission
  rate, debt) are inverted via the `ascending` flag so 1.0 always means "best."
- **`method="average"`** so tied schools (e.g., many at a 100% graduation rate) get the
  same rank.

**Step 3 — Impute missing values to the neutral 0.5.** If the Department of Education
didn't publish a metric for a school, that dimension's rank is set to **0.5 (the median)** —
the school is neither rewarded nor penalized for missing data, and still ranks on the
metrics it *does* report. This is a key design decision (see §7.5).

**Step 4 — Weighted average, scaled to 0–100.** The match score is the weighted average of
the per-dimension percentile ranks, with **weights normalized by their total** so the
*ratios* are what matter — sliders at 3-2-1 produce the identical ranking and identical
score magnitudes as 30-20-10. Result is `× 100`, rounded to one decimal, sorted descending.

**The output:** a copy of the input DataFrame with `score_<dimension>` columns (per-dim
percentile), a `match_score` column (0–100), and the confidence-interval columns from §12.

### 7.3 `generate_explainer()` — the "Why this rank?" sentence

For each pinned school the app shows a natural-language explanation. `generate_explainer()`
looks at the user's **top-2 weighted** dimensions and reports the school's percentile on
exactly those — e.g., *"Stanford University scores in the 99th percentile for earnings and
the 98th for graduation rate, which are your top priorities."* It deliberately ignores
dimensions the user weighted 0 — they didn't affect the ranking, so mentioning them would
be misleading.

### 7.4 Why "match score 100" means something specific

A match score of 100 does **not** mean "perfect school." It means **"best in the *currently
filtered pool* on *your current weights*."** Change the filters or the weights and the
percentile ranks recompute against a different field. This is why scoring always happens
*after* filtering, and why the same school can score differently in two views unless the
scoring pool is shared (see §16, `_build_pinned_scored_pool`).

### 7.5 Design choices to be able to defend

- **Percentile rank over min-max** — outlier robustness + interpretability (§7.2).
- **Missing → 0.5 imputation** — don't penalize a school for the government's missing data;
  the alternative (dropping the school, or scoring it 0) would be unfair and noisy.
- **Weight normalization** — makes the slider *scale* irrelevant; only relative priority
  matters.
- **Pure module, no Streamlit** — the engine is testable in isolation; 27 tests cover
  normalization, the weighted average, the explainer, CIs, and sensitivity.

---

## 8. Tab 1 — School Finder

The flagship tab. The flow: **filter → weight → score → rank → inspect → compare → export.**

### 8.1 The sidebar — filters and weights

- **Filters (the hard cut — who's even in the pool):** state, institution control
  (public / private nonprofit / private for-profit), campus setting (city/suburb/town/
  rural), enrollment size bucket, SAT range, Pell-share floor, minority-serving-institution
  designations, and a major (CIP) filter. Test-optional schools are *kept* unless the SAT
  range is actively narrowed.
- **The 250-enrollment floor.** By default, schools with fewer than 250 undergraduates are
  excluded; a "Show small schools" toggle re-includes them. (Rationale in §15.)
- **The 7 weight sliders** (0–5 each) — one per scoring dimension.
- **Preset profiles** — one-click weight bundles (Balanced, Career-focused,
  Affordability-focused, Selectivity-focused) for first-time users (see §12).

### 8.2 The ranked results

After `apply_filters()` cuts the pool and `compute_scores()` ranks it, the app shows ranked
school cards. Each carries:
- A **match score** (0–100) and rank.
- An **acceptance-likelihood badge** — **Safety / Match / Reach** (or N/A). `classify_
  acceptance()` compares the student's SAT (ACT is converted via a concordance table) to
  the school's 25th/75th-percentile SAT range. Each badge is emoji **+** text label
  (🟢 Safety / 🟡 Match / 🔴 Reach) so it's screen-reader-safe.
- A **confidence-interval bar** — a visual 95% CI around the score (see §12).

### 8.3 Pinned schools — the detail panel

A school can be **pinned** to a detail panel showing: context badges (Carnegie type, test
policy, MSI status, religious affiliation), the "Why this rank?" explainer, the CI bar, a
**sensitivity flag** (is this rank robust or volatile to small weight changes — §12), a
**7-axis percentile radar chart**, student-body demographics (a stacked bar), **earnings
mobility** (mean earnings by family-income tercile — does this school lift low-income
students?), and **program-level earnings & debt** for whatever major is currently selected
in Major Explorer.

### 8.4 Comparison, export, and map

- **Comparison table** — up to **4 pinned schools** side by side, metrics as rows, with
  🟢/🟡/🔴 emoji marking the best value per row.
- **CSV export** — the ranked results as a downloadable CSV.
- **PDF export** — a formatted report with a cover page (active filters + weights) and one
  card per school. Uses `fpdf2`; the `_pdf_safe()` helper handles its Latin-1 limitation
  (see §16).
- **Map** — a Plotly scattermapbox of all ranked schools, colored red→green by match score.
  Implemented as two traces (a black outline ring under the colored markers) because
  scattermapbox has no marker border.

---

## 9. Tab 2 — Major Explorer

A **majors-first** lens — flip the question from "which school?" to "which field?" Pick any
of ~410 CIP4 majors and the tab renders roughly eleven panels:

1. **Major description** — hand-authored for the top 60 majors (overview, what you'll
   learn, typical classes, related majors); an auto-generated stub for the rest.
2. **NY Fed labor outcomes** — unemployment, underemployment, early/mid-career wages,
   share with a graduate degree.
3. **Scorecard program outcomes** — median-of-medians 1/4/5-year graduate earnings and
   debt across institutions offering the major.
4. **Wages & projections** — employment-weighted median wage, the 25th–75th percentile
   wage range, 10-year projected employment growth, total routing employment.
5. **Career paths** — the table of BLS occupations the major routes to, by employment.
6. **Top industries (NAICS)** — a horizontal bar of the top-10 industries employing the
   major's occupations, with the long tail collapsed into an "Other (N combined)" row.
7. **Work environment** — 13 O\*NET work-context elements (time pressure, autonomy,
   physical demands…) as quartile-colored bars.
8. **Geographic concentration** — side-by-side US **choropleths**: total state employment,
   and **location quotient** (concentration vs. the national average; LQ is the primary
   metric because it's robust to BLS suppression). The color scale is capped at 5.0 so a
   few extreme states don't wash out the gradient; hover shows the true uncapped value.
9. **Schools strong in this major** — the top schools by program earnings, each with a
   one-click button to pin it straight into the School Finder.

### 9.1 The major picker

`build_major_picker_options()` builds the dropdown. Majors that align with a completed
RIASEC profile get a **⭐ prefix** — the top-40 RIASEC-aligned CIPs are computed (and
session-cached) so a user who finished Find Your Fit sees their best-fit majors flagged
here. This is one of the cross-tab integrations.

---

## 10. Tab 3 — Find Your Fit (RIASEC)

A **60-question interest inventory** that recommends majors — the project's most
distinctive feature.

### 10.1 What RIASEC is

**RIASEC** (a.k.a. the Holland Codes) is a standard vocational-psychology model with **six
interest dimensions**: **R**ealistic, **I**nvestigative, **A**rtistic, **S**ocial,
**E**nterprising, **C**onventional. The questionnaire is the **O\*NET Interest Profiler
Short Form** — a public-domain instrument from the U.S. Department of Labor.

### 10.2 The questionnaire

60 items, 10 per dimension, each a work activity rated on a **5-point Likert scale** (0 =
Strongly Dislike … 4 = Strongly Like). Summing a dimension's 10 items gives a score from
**0–40**. The submit button only appears once all 60 are answered (so focus is never
trapped on an inert control — an accessibility choice, §13).

### 10.3 The matching algorithm — the key technical point

The user's six summed scores form a **RIASEC vector**. Each of the ~410 majors also has a
six-value RIASEC vector — built by `data_prep_riasec.py` as the **employment-weighted
average** of the O\*NET RIASEC scores of the major's routing occupations.

The match is computed with **Pearson correlation** between the user's vector and each
major's vector. **Why Pearson, not Euclidean distance?** Pearson captures the *shape* of
the profile independent of *scale*. A user who likes everything moderately and a user who
likes everything intensely have the same *pattern* of relative interest — Pearson scores
them as matching the same majors; Euclidean distance would wrongly separate them by overall
magnitude.

The tab returns a ranked **top-10** majors, each with its `r` correlation value and an
"Explore →" button that opens it directly in Major Explorer. It also computes the user's
**Holland Code** — the 3-letter string of their top three dimensions (ties broken by
canonical R-I-A-S-E-C order).

### 10.4 Shareable results

A finished RIASEC profile is encoded into the URL (a compact `R##I##A##S##E##C##` string),
so results can be shared as a link — opening that link renders the results directly,
skipping the quiz.

---

## 11. Cross-Tab Integration & Session State

The three tabs are not silos — they hand off to each other, and that handoff is one of the
project's more sophisticated pieces of engineering.

### 11.1 The handoffs

- School detail card → **Major Explorer** (click a program's "Explore →").
- Find Your Fit recommendation → **Major Explorer** ("Explore →" on a top-10 major).
- Major Explorer "schools strong in this major" → **School Finder** (pin a school).
- A finished RIASEC profile flags aligned majors with ⭐ in the Major Explorer picker.

### 11.2 Why this is hard — Streamlit has no tab-switching API

Streamlit provides **no programmatic way to switch the active `st.tabs` tab**. The app
works around it with a **session-state sentinel pattern**: a cross-tab click writes a flag
to `st.session_state`, triggers a rerun, and the target tab reads the flag on load to
pre-populate itself. Five such sentinels are documented in `docs/SESSION_STATE.md` —
`_last_xtab_pinned`, `_last_xtab_cip`, `_last_xtab_cip_filter`, `_url_tab_banner`,
`_active_tab` — each with its writer, its consumer, and its lifecycle (most are "one-shot
pop": consumed and deleted on the first rerun after the click).

### 11.3 The widget-state shadowing bug (the headline engineering story)

This is the single best bug story in the project — **be ready to tell it.**

During final manual verification, clicking "Explore →" from a school detail card switched
to the Major Explorer tab but left the **major picker stuck on its previous selection**
instead of pre-selecting the intended major. **All 296 tests were passing.**

**The root cause:** `set_major_explorer_cip()` wrote the target CIP code to session state,
but Streamlit's `st.selectbox` for the major picker carries a `key="major_picker_widget"`.
When a keyed Streamlit widget has a value already persisted under its key, that persisted
value **silently overrides the programmatic `index=` parameter** on the next render. So the
code said "select this major" and Streamlit ignored it.

**The fix is one line** — in the callback, `pop` the widget key so Streamlit re-initializes
the widget from the `index` parameter:

```python
st.session_state.pop("major_picker_widget", None)  # clears the widget-key shadow
```

**Why no test caught it:** automated tests don't exercise Streamlit's widget initialization
sequence — that's a boundary the test suite structurally can't reach, not a test-suite
failure. A regression test was added before the phase closed, taking the suite to **297**.
The lesson: a passing test suite proves the *logic* is right; it doesn't prove the
*framework integration* is right — manual verification is not optional.

### 11.4 URL state

`url_state.py` encodes the full app state — active tab, filters, weights, selected CIP, the
RIASEC vector — into URL query parameters, so any ranking or result is a **shareable,
bookmarkable link**. `_write_session_state_to_url()` serializes only *non-default* values
to keep URLs short; `_parse_url_into_session_state()` reads them back once per session.

---

## 12. Statistical Depth Features

Beyond basic ranking, the app has a set of "statistical depth" features that make the
output more honest and more usable. Each is a good interview talking point.

**Confidence intervals on match scores.** `compute_score_uncertainty()` puts a **95% CI**
around each school's score. The logic: a school scored on fewer *reported* dimensions (more
of its score came from the neutral 0.5 imputation) and with more *disagreement* across the
dimensions it does report gets a **wider** interval. It's a coverage-adjusted standard
error — `1.96 × SE × 100`, where the SE is inflated by the fraction of dimensions actually
reported. A school with only one reported dimension gets a deliberately large fixed margin
(15.0) to signal low confidence rather than fake precision. The CI renders as a band behind
the score. **The point:** a "score of 82" built on two reported metrics is not the same as
an "82" built on all seven, and the CI shows that.

**Sensitivity analysis.** `compute_sensitivity()` answers "is this school's rank *real* or
an artifact of your exact slider positions?" For a pinned school it perturbs each weight by
**±1** (clamped to 0–5), recomputes the *entire* ranking for each perturbation, and measures
how often the school stays in the top N. It returns a tier: **robust** (stays in ≥ 70% of
perturbations), **borderline** (40–70%), or **volatile** (< 40%). The detail card surfaces
this so a user knows whether to trust a borderline ranking.

**Preset profiles** (`profiles.py`). Four one-click weight bundles — Balanced,
Career-focused, Affordability-focused, Selectivity-focused — for first-time users who don't
want to set seven sliders cold. `match_profile()` detects when the current sliders exactly
equal a preset and labels the state accordingly (or "Custom").

**URL state** (covered in §11.4) — shareable rankings.

**Income-bracket net price.** The affordability dimension can swap its column: instead of
the overall `net_price`, the user picks a family-income bracket and scoring uses that
bracket's net-price column (`net_price_public_0_30k`, etc.) — because a college's "price"
is wildly different for a $25k family vs. a $150k family.

---

## 13. Accessibility (a real differentiator)

Accessibility is not an afterthought here — it's a documented, tested feature, and it's one
of the strongest things to talk about because most portfolio projects ignore it entirely.

### 13.1 Colorblind-safe palette — and a real, unresolved trade-off

Every chart color is a token in `config.PALETTE`, built on the **Wong (2011)
colorblind-safe categorical palette**. But there's a genuine conflict, and the project is
honest about it:

- **WCAG AA non-text contrast** wants colors dark enough to hit a 3:1 luminance ratio
  against white.
- **The Wong palette** is optimized for *colorblind distinguishability*, which puts several
  of its colors in a mid-tone range that *fails* the 3:1 contrast threshold.

**Eight Wong-derived tokens fail WCAG AA contrast.** Darkening them would pass the contrast
test but **re-introduce colorblindness ambiguity** — the two goals genuinely conflict and
there is no color that satisfies both. The resolution: **replace colors where there's no
colorblind constraint** (the work-environment quartile gradient is a pure lightness ramp —
3 of its 4 colors were darkened to pass), and **preserve the Wong tokens where the
constraint is real**, documenting each excluded token with its measured contrast ratio.
The decision is recorded in `docs/ACCESSIBILITY.md` and in an `EXCLUDED_TOKENS` dict in the
test file. **The interview point:** sometimes two correct design goals conflict and the
mature move is to document the trade-off, not pretend one of them away.

### 13.2 Contrast verified programmatically

`utils.py` has pure WCAG 2.1 §1.4.3 math — `relative_luminance()` and `contrast_ratio()`.
The test suite then has **~26 parametrized contrast tests** that check every `PALETTE`
token against its rendering background. A coverage test (`test_palette_coverage_complete`)
ensures **no palette key can be silently added without being either tested or explicitly
excluded** — a future color regression fails CI before it ships.

### 13.3 Screen-reader and interaction accessibility

- Every chart (11 of them) has a **descriptive prose caption** for screen readers.
- Acceptance badges always carry **emoji + text** so they're not color-only.
- The empty-state for the earnings-mobility chart uses `role="status"` so assistive tech
  announces "no data" instead of skipping it silently.
- "Explore →" buttons carry `help=` tooltips naming the specific major (label-in-button was
  ruled out because 58% of major names exceed 30 characters).
- The RIASEC submit button is **absent from the DOM** until all 60 questions are answered,
  so keyboard/switch users never get trapped on an inert control.

### 13.4 Accepted framework limitations

`docs/ACCESSIBILITY.md` lists seven Streamlit limitations that **can't** be fixed at the
app layer (no programmatic tab switching, focus dropping to document body after a rerun,
expander state not announced, etc.). The honest move was to **document them with their
assistive-technology impact** rather than ship fragile hacks.

### 13.5 The Lighthouse numbers — and how to discuss them

A Lighthouse audit (Chrome, Mobile preset) scored: **Accessibility 86, Performance 12**,
Best Practices 81, SEO 82.
- **Accessibility 86** — zero machine-detectable failures. The 14-point gap is Lighthouse's
  *manual-check* territory (logical focus order, plain-language judgment) — items that
  can't be auto-scored, not defects.
- **Performance 12** — a **known Streamlit framework ceiling.** Streamlit's
  Python→WebSocket architecture and large frontend bundle produce 10–20 Performance scores
  by design. Chasing a higher number would mean replacing the framework. The ceiling is
  accepted and documented — *which is the right answer*, and saying so confidently in an
  interview shows you understand the framework's trade-offs rather than being embarrassed
  by the number.

---

## 14. Testing — 297 Tests

The project ships **297 passing pytest tests** across ~23 files in `tests/`. The suite is a
real engineering asset, not box-checking.

**What it covers:**
- **The scoring engine** (`test_scoring.py`, 27 tests) — normalization, the weighted
  average, the explainer text, confidence intervals, sensitivity tiers, with hand-built
  fixture DataFrames.
- **The data pipeline** (`test_data_prep_majors.py` ~39, plus geo/workcontext/crosswalk/
  NAICS/RIASEC prep tests) — suppression handling, employment-weighted aggregation,
  coverage thresholds, output schemas. This guards the *correctness of the data layer*.
- **RIASEC** (matching, questionnaire, distribution, alignment) — Pearson correlation,
  Holland-code tie-breaking, score ranges.
- **Utilities, config, profiles, URL state** — CIP formatting, acceptance classification,
  encode/decode round-trips.
- **UI component contracts** (`test_major_explorer_xtab.py`, `test_find_your_fit_page.py`,
  `test_about_the_data.py`) — cross-tab handoff session-state writes, the all-12-sources
  invariant.

**Notable testing approaches worth citing:**
- **WCAG contrast tests** — verifying *visual accessibility* in an automated suite is
  unusual and a strong signal (§13.2).
- **The coverage guard** — `test_palette_coverage_complete` makes it *impossible* to add a
  palette color without verifying or explicitly excusing it.
- **The cross-tab regression test** — added specifically for the widget-state shadowing bug
  (§11.3), so that exact bug can never silently return.
- **Provenance guards** — `test_about_the_data.py` asserts all 12 data sources are present
  in the rendered "About the Data" panel and that old duplicated prose was removed.

**The honest framing for interviews:** the suite is strong, but the widget-shadowing bug
proves its boundary — **automated tests verify logic; they cannot exercise Streamlit's
widget initialization sequence.** That's why the workflow paired tests with mandatory
manual smoke tests. Knowing what your tests *can't* catch is as important as the count.

---

## 15. Methodology Decisions (the "why we cut X" stories)

These are deliberate analytical decisions — interviewers love them because they show
judgment, not just coding. Each is a "we considered X and decided Y, here's why."

**Clery Act campus-safety scoring — evaluated and cut.** Campus crime data (Clery Act
reporting) was considered as an 8th scoring dimension and **deliberately scoped out.** Three
compounding data-quality problems: (1) reporting is **self-certified** by institutions with
no independent audit; (2) the geography is **on-campus only**, which doesn't match the
environment students actually live in; (3) normalizing crime counts by enrollment produces
rates **highly sensitive to how aggressively a school classifies incidents.** The net
effect: a "safety score" that mostly reflects institutional *reporting culture*, not actual
safety. It would look like a signal and mislead. It's left as a commented-out scope cut in
`config.py` so it's easy to revive if a cleaner source appears. **This is the single best
methodology story** — be ready to tell it.

**The 250-student enrollment floor.** Schools with fewer than 250 undergraduates are
excluded by default. Reason: tiny institutions dominated the top of retention- and
graduation-sorted rankings — not because they're exceptional, but because **small-cohort
statistics are noisy** and those schools aren't comparable to the universities most users
are evaluating. It's a data-quality decision, not a value judgment — and a "Show small
schools" toggle re-includes them.

**Weighted median as a population statistic.** Major-level wages are
employment-weighted medians across a major's routing occupations. They describe **where the
labor market concentrates graduates in aggregate** — not a prediction for any individual.
A Computer Science major can become a postsecondary teacher; the weighted median doesn't
forecast that. The app states this framing explicitly in "About the Data."

**The CIP–SOC crosswalk is expert judgment, not placement data.** The NCES crosswalk maps
programs to occupations based on **BLS/NCES judgment about which jobs a program's skills
suit** — it is *not* based on tracking actual graduates. Real destination data would be
richer but isn't public at this granularity. The crosswalk is good enough for *discovery*;
it should not be read as "graduates of this program become these workers."

**Missing-data imputation to the 50th percentile.** Covered in §7.5 — don't penalize a
school for the government's missing data.

**Scope cuts for source-availability reasons.** Historical Scorecard snapshots (for trend
arrows) and a ZIP→lat/long distance filter were planned and cut after the ED bulk-data host
moved and the features proved impractical to automate. Geographic filtering is handled by
the state multiselect instead. All cleanly documented as commented-out scope cuts in
`config.py`.

---

## 16. Engineering Decisions & Code Highlights

The three code highlights the portfolio page itself calls out — know these well, they're
likely to be probed.

**`_build_pinned_scored_pool()` — one source of truth for scoring.** Pinned schools appear
in *two* places: the detail cards and the comparison table. If each view scored
independently, a school could show **different numbers in the two views** when filter state
differed between renders. The fix: a shared helper both views call. It folds any
pinned-but-outside-the-filter schools into the scoring pool, runs `compute_scores()` **once**,
and hands both views the identical scored frame. The principle: *if two views must agree,
compute the shared thing once and pass it to both* — never compute it twice.

**`_pdf_safe()` — a Latin-1 helper instead of a heavy font dependency.** PDF export uses
`fpdf2`'s built-in Helvetica, which is **Latin-1 only**. Bundling a full Unicode font would
add ~2 MB to the deployment and complicate Streamlit Cloud setup. Instead `_pdf_safe()`
normalizes any string to Latin-1 in three steps: (1) an explicit replacement table for
common typographic characters (smart quotes, em-dashes, ellipsis → ASCII), (2) NFKD Unicode
normalization to strip accent/combining marks (so "é" → "e"), (3) a final
`encode/decode("latin-1", errors="ignore")` to drop anything still untranslatable. It
covers essentially all U.S. college names and major titles **without a production
dependency.** The principle: *a small, targeted helper can beat a heavyweight dependency
when the input domain is bounded.*

**The cross-tab widget-state shadowing bug** — covered fully in §11.3. The one-line fix,
why 296 tests missed it, and the regression test that followed.

**Other decisions worth knowing:**
- **`config.py` as the single source of truth** — every column rename, scoring dimension,
  category label, and color lives in one file; a source-schema change is a one-line edit.
- **`PALETTE` centralization** — no inline hex literals anywhere in the app code; one dict
  drives every chart, badge, and PDF color.
- **The no-Streamlit layering rule** — `scoring.py` and `utils.py` stay framework-free so
  they're unit-testable (§4).
- **Two-trace scattermapbox** — a black outline ring drawn under colored markers, the
  standard workaround for scattermapbox having no marker border.
- **Caching** — data loads and the expensive CSV/PDF byte-builders are wrapped in
  `@st.cache_data` so they don't recompute on every interaction.

---

## 17. The Build Process

The project was built in **numbered phases**, tracked in a living `PROJECT_STATUS.md`. The
shape is worth knowing because it shows disciplined, incremental delivery.

- **V4 Phases 1–5** — the School Finder: data acquisition & prep, the scoring engine, the
  core Streamlit app, pin/badge/income-bracket/field-of-study features, and comparison /
  CSV-PDF export / map.
- **"Stat Depth" A–F** — the statistical-depth layer: demographics & mobility, repayment as
  the 7th scoring dimension, confidence intervals, sensitivity analysis, preset profiles,
  URL state.
- **Addendum Phases 8–13** — the Major Explorer and Find Your Fit: the major picker &
  field-of-study detail, the BLS occupational layer (Phase 9), the geographic & work-context
  layer (Phase 10), major descriptions (Phase 11), the RIASEC questionnaire & matching
  (Phase 12), and cross-surface integration (Phase 13).
- **Final code audit** — a comprehensive review pass (May 2026): 16 findings, triaged and
  actioned across the cleanup batches and Phase 6.
- **Phase 6 (Polish & Accessibility)** — six sub-phases (6A–6E): audit cleanup, color
  palette consolidation into `PALETTE`, chart & interactive accessibility, the transparency
  surface ("About the Data" on every tab), and mobile / dark-mode / Lighthouse. The
  cross-tab bug was caught here, during 6E verification.
- **Phase 7 — Deployment & Documentation** — monorepo integration, pinned `requirements.txt`,
  Streamlit Community Cloud deploy, README, the portfolio page.

**Two process points worth citing:** (1) a recurring **"Step 0 inspection"** discipline —
inspect the actual code before each phase's edits — "caught real spec errors in 13
consecutive phases," meaning the plan was wrong often enough that verifying first was
always worth it. (2) **Manual smoke tests were mandatory** alongside the automated suite,
because visual/accessibility regressions don't fail tests — and that's exactly how the
widget-shadowing bug surfaced.

---

## 18. Limitations & Honest Caveats

Volunteer these — knowing your project's limits signals maturity.

1. **The CIP–SOC crosswalk isn't real placement data** (§15) — it's expert judgment about
   which jobs a program suits, not graduate tracking. Good for discovery, not destiny.
2. **Major-level wages are population statistics, not individual predictions** (§15) —
   an employment-weighted median, not a forecast for one student.
3. **Data spans ~21 months** (May 2024 → Feb 2026) and is a point-in-time snapshot — it is
   not live; sources refresh on their own federal cycles.
4. **Scoring is relative, not absolute.** A "match score 100" means best *in your filtered
   pool on your weights* — change either and it recomputes. It is not an objective quality
   score.
5. **Missing data is imputed to the median.** Fair, but it means a school with sparse
   reporting has a score partly built on neutral placeholders — which is exactly why the
   confidence interval exists.
6. **Lighthouse Performance is ~12** — a Streamlit framework ceiling, accepted (§13.5).
7. **Dark mode is not fully supported** — the app ships a hardcoded light theme; full
   dark-mode parity wasn't justified for a portfolio app and is documented as accepted.
8. **Eight palette colors fail WCAG AA contrast** — a genuine, documented conflict between
   colorblind-safety and luminance contrast (§13.1).
9. **Documentation drift to be aware of:** the README and portfolio page describe the
   scoring-dimension set slightly inconsistently (the README says "eight … diversity";
   `index.md` mentions "student-to-faculty ratio"). **`config.py` is authoritative — there
   are seven dimensions** (§7.1). Likewise the README's "3,500+ institutions" is looser
   than the committed data (`colleges_cleaned.csv` has ~2,477 schools; the code comments
   reference ~2,500). If asked for exact numbers, cite the code and the data files.

---

## 19. Interview Q&A

Practice these out loud. Answers are written the way you'd actually speak.

**Q1. Give me the overview of this project.**
"It's a college recommendation app built in Python and Streamlit. The idea: instead of
handing you one ranking the way *U.S. News* does, it lets you set the weights yourself —
you move sliders for cost, earnings, graduation rate, selectivity, and so on, and it scores
and ranks every U.S. college on *your* priorities. It has three tabs — School Finder for
ranking schools, Major Explorer for exploring fields of study, and Find Your Fit, a RIASEC
interest questionnaire that recommends majors. The real engineering was the data layer:
integrating 12 federal datasets into one coherent scoring model."

**Q2. Walk me through the scoring engine.**
"It's a weighted multi-criteria model in `scoring.py`. Four steps. First, drop any
dimension the user weighted zero. Second, normalize each remaining metric to a percentile
rank from 0 to 1 — I used percentile rank rather than min-max so outliers don't compress
the scale, and direction is handled here, so 'lower is better' metrics like net price get
inverted. Third, impute missing values to 0.5, the neutral median, so a school isn't
penalized for data the government didn't publish. Fourth, take a weighted average of those
percentile ranks, normalize by total weight so slider scale doesn't matter, multiply by
100. The result is a 0-to-100 match score, and every per-dimension percentile is kept so I
can explain the rank."

**Q3. Why percentile rank instead of min-max normalization?**
"Two reasons. Robustness — with min-max, one ultra-expensive or ultra-selective school
stretches the range and squashes everyone else into a narrow band. Percentile rank is
immune to that. And interpretability — '85th percentile for earnings' is a sentence a
student immediately understands; a min-max value of 0.73 isn't."

**Q4. How do you handle missing data?**
"I impute the missing dimension to the 50th percentile — the neutral median. The
alternative, scoring it zero or dropping the school, would punish a school for the
Department of Education simply not publishing a metric. The school still ranks on the
metrics it does report. And because imputation hides uncertainty, I pair it with a
confidence interval — a school scored mostly on imputed data gets a visibly wider interval."

**Q5. What does a match score of 100 actually mean?**
"It means best *in the currently filtered pool, on the user's current weights* — not
'perfect school.' Percentile ranks are computed against whoever passed the filters, so
change the filters or the sliders and everything recomputes. That relativity is why scoring
always happens after filtering."

**Q6. Tell me about the hardest bug.**
"A cross-tab navigation bug, and it's a good story because all 296 tests were passing when
I found it. Clicking 'Explore →' to jump to the Major Explorer tab switched tabs but left
the major picker stuck on its old value. The cause: that picker is a Streamlit selectbox
with a `key`, and when a keyed Streamlit widget already has a value stored under its key,
that stored value silently overrides the programmatic `index` you pass in. So my code said
'select this major' and Streamlit ignored it. The fix was one line — pop the widget's key
in the callback so it re-initializes from the index. The deeper lesson: automated tests
verify your logic, but they can't exercise Streamlit's widget initialization sequence —
that's why manual verification isn't optional. I added a regression test for it."

**Q7. The 12 data sources — what made integrating them hard?**
"They don't agree on anything. Different granularities — institution, program, occupation,
state. Different code systems — CIP for majors, SOC for occupations, NAICS for industries.
Different update cycles — annual, biennial, irregular. Different suppression conventions.
The work was building a clean spine: CIP maps to SOC through the NCES crosswalk, SOC maps
to wages, to state employment, to RIASEC scores, to NAICS industries. I did all that
joining offline in five data-prep scripts that output small clean CSVs, so the app at
runtime only ever loads cleaned data and stays fast."

**Q8. Explain the employment-weighted average.**
"A major routes to many occupations. To get one wage or one interest score per major, I
average across those occupations — but weighted by employment, so an occupation employing
500,000 people counts more than one employing 5,000. An unweighted average would let a tiny
niche occupation distort the major's profile. It's how I build the major-outcomes table and
the per-major RIASEC vectors."

**Q9. Why did you cut the campus-safety dimension?**
"I evaluated Clery Act crime data as an eighth scoring dimension and cut it on data-quality
grounds. Three problems compounded: reporting is self-certified with no independent audit;
the geography is on-campus only, which isn't where students actually live; and normalizing
by enrollment makes the rate hugely sensitive to how aggressively a school classifies
incidents. The result would look like a safety signal but mostly measure reporting culture.
A misleading metric is worse than no metric. I left it as a documented, commented-out scope
cut so it's easy to revive if a cleaner source appears."

**Q10. How does the RIASEC matching work?**
"Find Your Fit runs the 60-item O*NET Interest Profiler — six interest dimensions,
Realistic through Conventional, scored 0 to 40 each. That gives the user a six-value
vector. Every major also has a six-value RIASEC vector, built as the employment-weighted
average of its occupations' O*NET interest scores. I match with Pearson correlation, not
Euclidean distance — Pearson captures the *shape* of the interest profile independent of
scale, so someone who likes everything mildly and someone who likes everything intensely
get matched to the same majors if their relative pattern is the same."

**Q11. Why Streamlit, and what are its downsides?**
"Streamlit let me build a real interactive multi-tab app entirely in Python, with no
separate frontend — right for a solo data project. The downsides are real: there's no API
to switch tabs programmatically, so cross-tab navigation needs a session-state sentinel
pattern; keyed widgets shadow programmatic values, which caused my hardest bug; and
Lighthouse Performance is stuck around 12 because of the Python-to-WebSocket architecture.
I accepted and documented the framework ceilings rather than fighting them."

**Q12. Tell me about the accessibility work.**
"Every chart color is a token in a central palette built on the Wong colorblind-safe set.
I wrote WCAG 2.1 contrast math into the codebase and added about 26 automated tests that
check every color against its background — verifying visual accessibility in CI, which most
projects never do. There's an honest trade-off I documented: eight Wong colors fail the
WCAG luminance-contrast threshold, but darkening them would re-introduce colorblindness
ambiguity — the two goals genuinely conflict, so I fixed the colors where there was no
conflict and documented the ones where there was. Plus screen-reader captions on all 11
charts, emoji-and-text badges, and ARIA on the one custom HTML element."

**Q13. What does the confidence interval on a score represent?**
"It's a 95% interval that widens when a school's score is less trustworthy — specifically
when fewer of the seven dimensions were actually reported, so more of the score came from
median imputation, and when the reported dimensions disagree more. It's a coverage-adjusted
standard error. The point is honesty: an 82 built on two reported metrics shouldn't look as
solid as an 82 built on all seven, and the interval shows that visually."

**Q14. What's the sensitivity analysis for?**
"It answers 'is this ranking real or an artifact of my exact slider positions?' For a
pinned school it nudges each weight up and down by one, recomputes the full ranking each
time, and measures how often the school stays in the top N. If it holds in 70%-plus of
those perturbations it's labeled robust; under 40%, volatile. So a user knows whether a
borderline rank is trustworthy."

**Q15. If you kept building, what's next?**
"A few things. Real graduate-destination data if it ever becomes public at this
granularity, to replace the crosswalk's expert-judgment routing. Reviving the trend-arrows
and distance features that got scope-cut. And reconciling the documentation — the README
and portfolio page drifted slightly from the code on the dimension count, which I'd tighten
up. Longer term, the Streamlit performance ceiling means a different framework if this ever
needed to scale."

---

## 20. How to Walk Through This Project Live

If asked to screen-share, use this order:

1. **Open the live app** and lead with the *outcome* — set a couple of weight sliders on
   School Finder, show the ranking recompute, open a pinned school's detail card with its
   radar chart, "Why this rank?" explainer, and confidence interval.
2. **State the thesis** — "every ranking tool hides its weights; this one exposes them."
3. **Show the architecture** — the two-stage split: offline data prep (5 scripts, 12
   sources) → committed clean CSVs → the Streamlit app. Emphasize that the data layer was
   the hard part.
4. **Walk `scoring.py`** — the four-step `compute_scores()` algorithm. This is the
   technical core; narrate percentile-rank normalization, the 0.5 imputation, and weight
   normalization.
5. **Show one cross-cutting feature** — the confidence interval or the sensitivity
   analysis — to demonstrate statistical depth beyond a plain ranking.
6. **Tell the widget-shadowing bug story** — 296 tests passing, one-line fix, what the test
   suite structurally can't reach. It's the best engineering-judgment story you have.
7. **Show the Major Explorer or Find Your Fit tab** — pick whichever you can narrate best;
   for Find Your Fit, explain the Pearson-correlation matching.
8. **Close on a methodology decision** — the Clery Act safety cut. It shows analytical
   judgment, not just coding.

**Pacing tip:** spend the most time on the data integration and `scoring.py`. The three
tabs are the visible product, but the data layer and the scoring method are the
differentiated engineering — and the bug story and the safety-cut story are what make you
memorable.

---

## 21. Glossary

- **Streamlit** — the pure-Python web-app framework the whole UI is built on; the script
  re-runs top-to-bottom on every interaction.
- **`st.session_state`** — Streamlit's per-session key-value store; how the app remembers
  pins, weights, and cross-tab signals across reruns.
- **Match score** — a school's 0–100 weighted score; the weighted average of its
  per-dimension percentile ranks. Relative to the filtered pool and current weights.
- **Scoring dimension** — one of the seven weighted criteria (affordability, graduation
  rate, retention, earnings, selectivity, low debt, repayment).
- **Percentile rank** — a metric expressed as its rank position 0–1 within the pool; the
  normalization method the scoring engine uses.
- **Weight** — a 0–5 slider value expressing how much the user cares about a dimension.
- **Acceptance badge** — Safety / Match / Reach / N-A, from the student's SAT vs. the
  school's 25th–75th-percentile range.
- **Confidence interval** — a 95% band around a match score; wider when fewer dimensions
  were reported or they disagree.
- **Sensitivity analysis** — perturbing weights ±1 to test whether a school's rank is
  robust, borderline, or volatile.
- **CIP** — Classification of Instructional Programs; the federal code for an academic
  major. The app works at CIP4 (4-digit) granularity.
- **SOC** — Standard Occupational Classification; the federal code for an occupation.
- **NAICS** — North American Industry Classification System; the federal code for an
  industry.
- **CIP–SOC crosswalk** — the NCES many-to-many map from majors to occupations; expert
  judgment, not graduate tracking.
- **OEWS** — BLS Occupational Employment and Wage Statistics; the wage-percentile source.
- **Employment Projections** — BLS 10-year occupational growth and openings data.
- **Location quotient (LQ)** — a state's employment concentration in an occupation
  relative to the national average; the choropleth's primary metric.
- **RIASEC / Holland Codes** — the six vocational-interest dimensions (Realistic,
  Investigative, Artistic, Social, Enterprising, Conventional).
- **O\*NET Interest Profiler** — the public-domain 60-item RIASEC questionnaire used by
  Find Your Fit.
- **Holland Code** — the 3-letter string of a person's top three RIASEC dimensions.
- **Pearson correlation** — the metric matching a user's RIASEC vector to majors; captures
  profile *shape* independent of scale.
- **Employment-weighted average** — averaging an occupation-level metric up to a major,
  weighting each occupation by its employment.
- **College Scorecard** — the U.S. Department of Education dataset of college outcomes; the
  app's primary school-data source.
- **Net price** — the price a family actually pays after grants/scholarships; the
  affordability metric (selectable by income bracket).
- **Wong (2011) palette** — the colorblind-safe color set every chart color derives from.
- **WCAG** — Web Content Accessibility Guidelines; the contrast standard the palette is
  tested against.
- **`@st.cache_data`** — the Streamlit decorator that caches expensive loads/computations
  so they don't rerun on every interaction.
- **Data-prep scripts** — the five offline `data_prep_*.py` ETL scripts that turn raw
  federal files into the committed clean CSVs.

---

*This study guide documents the project as built. The authoritative references in the repo
are `scoring.py` (the engine), `config.py` (constants and the scoring dimensions),
`app.py` and `page_modules/` (the app), the `data_prep_*.py` scripts (the data layer), and
`docs/ACCESSIBILITY.md` / `PROJECT_STATUS.md` (the engineering record). When this guide and
the source disagree, the source wins.*
