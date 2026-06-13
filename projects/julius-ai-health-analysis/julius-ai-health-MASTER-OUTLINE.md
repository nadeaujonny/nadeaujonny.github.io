# Master Outline & Study Guide
## Julius AI — U.S. Chronic Disease Indicators Analysis (AI-assisted EDA on CDC public-health data)

> **Purpose of this document:** A complete, self-contained reference for studying this
> portfolio project. Use it to prepare for interviews — to explain what was built, how it
> works, why each decision was made, and to answer probing technical questions. When
> studying with Claude, this is the file Claude reads to teach and quiz you.
>
> **One sentence to anchor everything:** This project uses **Julius AI** — a
> natural-language data-analysis tool — to explore the **CDC's 96 MB U.S. Chronic Disease
> Indicators dataset** through six plain-English prompts, and the real skills on display
> are *prompt engineering, public-health data literacy, interpretation, and critical
> evaluation of AI output* — not manual coding.
>
> **Read §16 first if you're prepping for an interview.** An AI-assisted project invites a
> specific kind of skeptical question, and §16 is how you answer it well.

---

## Table of Contents

1. [The 30-Second Pitch](#1-the-30-second-pitch)
2. [Why This Project Exists (Context)](#2-why-this-project-exists-context)
3. [What Julius AI Is (and What It Does Under the Hood)](#3-what-julius-ai-is-and-what-it-does-under-the-hood)
4. [The Dataset — CDC Chronic Disease Indicators](#4-the-dataset--cdc-chronic-disease-indicators)
5. [The Workflow & Prompt Engineering](#5-the-workflow--prompt-engineering)
6. [Analysis 1 — Diabetes Prevalence: California vs. Texas](#6-analysis-1--diabetes-prevalence-california-vs-texas)
7. [Analysis 2 — Asthma Prevalence by Race/Ethnicity](#7-analysis-2--asthma-prevalence-by-raceethnicity)
8. [Analysis 3 — Physical Inactivity vs. Cardiovascular Disease Mortality](#8-analysis-3--physical-inactivity-vs-cardiovascular-disease-mortality)
9. [Analysis 4 — Mental Health Distress: Males vs. Females](#9-analysis-4--mental-health-distress-males-vs-females)
10. [Analysis 5 — Cigarette Smoking by Race/Ethnicity](#10-analysis-5--cigarette-smoking-by-raceethnicity)
11. [Analysis 6 — National Obesity Trend](#11-analysis-6--national-obesity-trend)
12. [Key Findings & Recommendations](#12-key-findings--recommendations)
13. [Julius AI — Tool Evaluation](#13-julius-ai--tool-evaluation)
14. [Public Health Data Literacy (Concepts to Know)](#14-public-health-data-literacy-concepts-to-know)
15. [Limitations & Honest Caveats](#15-limitations--honest-caveats)
16. [How to Position This Project in an Interview](#16-how-to-position-this-project-in-an-interview)
17. [Interview Q&A](#17-interview-qa)
18. [How to Walk Through This Project Live](#18-how-to-walk-through-this-project-live)
19. [Glossary](#19-glossary)

---

## 1. The 30-Second Pitch

This project uses **Julius AI** — an AI-powered, chat-based data-analysis platform — to
explore the **CDC's U.S. Chronic Disease Indicators (CDI)** dataset: a **96 MB CSV with
800,000+ rows** of chronic-disease surveillance data covering all 50 states, multiple
years, and dozens of health topics.

The work was done **entirely through natural-language prompts** — no manual coding. Six
analyses, each driven by one plain-English question: (1) diabetes prevalence trends in
California vs. Texas, (2) asthma disparities by race/ethnicity, (3) the correlation between
physical inactivity and cardiovascular-disease mortality, (4) the gender gap in frequent
mental distress, (5) cigarette-smoking disparities by race/ethnicity, and (6) the national
obesity trend. Julius generated the Python (pandas) code, ran it, and produced the charts;
the project frames the questions, engineers the prompts, and interprets the output.

It is deliberately a **two-part project**: a *public-health EDA* **and** a *structured
evaluation of an AI analysis tool* — when it works well, where it falls short, and when an
analyst should and shouldn't reach for it.

**One-line version:** "I used Julius AI to run six exploratory analyses on the CDC's 96 MB
Chronic Disease Indicators dataset through natural-language prompts — demonstrating prompt
engineering, public-health data literacy, and a critical evaluation of where AI-assisted
analysis is and isn't appropriate."

---

## 2. Why This Project Exists (Context)

**The premise.** Public-health agencies rely on chronic-disease surveillance data to find
at-risk populations, allocate resources, and evaluate programs. But the CDC's CDI dataset
is **large and technically demanding** — 96 MB, hundreds of thousands of records, dozens of
stratifications. Querying and visualizing it traditionally requires real SQL or Python
skill. **AI tools like Julius lower that barrier**: a non-technical stakeholder can explore
the same data through conversation.

**So the project asks two questions at once:**
1. *A public-health question* — what do six specific chronic-disease indicators actually
   show across states and demographics?
2. *A tooling question* — is an AI analysis platform a viable way to explore a large
   public-health dataset, and where are its limits?

**Why it's a legitimate portfolio project.** This is the honest framing to internalize: the
project does **not** claim to demonstrate coding ability. It demonstrates a *different and
genuinely valuable* skill set — the things that remain hard even when an AI writes the code:

- **Framing the right business question** out of a messy 800k-row dataset.
- **Prompt engineering** — phrasing a question precisely enough that the AI produces a
  correct, targeted analysis.
- **Public-health data literacy** — knowing what age-adjusted prevalence means, what BRFSS
  is, why a stratification matters.
- **Interpretation and data storytelling** — turning numbers and charts into a coherent
  narrative with actionable recommendations.
- **Critical evaluation** — checking the AI's output for statistical validity and knowing
  when *not* to trust it.

The project is current and relevant: it shows you can *adopt and critically assess new
tools*, which is itself a sought-after analyst trait. (How to defend this in an interview
is §16 — read it.)

---

## 3. What Julius AI Is (and What It Does Under the Hood)

**Julius AI** is a chat-based, AI-powered data-analysis platform. You upload a data file,
ask questions in plain English, and it carries out the analysis and returns results and
charts. The version used here, shown in the screenshots, is **"Julius 1.0 Lite."**

**What it actually does under the hood — know this; it's the answer to "but you didn't
code it":**

Julius does **not** invent numbers. For each prompt it:
1. **Generates Python code** — the screenshots show a "Generated Code" / "Python" panel
   with real pandas code, e.g. `df = pd.read_csv('U.S._Chronic_Disease_Indicators_20260206.csv', encoding='utf-8')`.
2. **Executes that code** in a sandboxed environment against the uploaded file.
3. **Returns the result** — tables, statistics, and matplotlib/plotly-style charts — plus a
   plain-language explanation.
4. **Shows its work** — the generated code is visible and inspectable, and a "Data Explorer"
   panel lets you browse the dataset.

So Julius is essentially **an LLM that writes and runs pandas/Python data-analysis code on
your behalf.** It's the same analysis a Python analyst would do — `read_csv`, filter,
`groupby`, aggregate, correlate, plot — with the LLM translating English → code. That
matters for interviews: the analysis is real, reproducible-in-principle Python; the AI is
the *interface*, not a black box that fabricates results. The honest caveat (see §13, §15)
is that you must *read* that generated code to confirm the method is sound.

**Why a tool like this exists.** It collapses the 30–60 minutes of manual coding a routine
EDA task takes into a sub-minute conversational turn — which is genuinely useful for *rapid
exploration and hypothesis generation*, the stage before formal analysis.

---

## 4. The Dataset — CDC Chronic Disease Indicators

**What it is.** The **U.S. Chronic Disease Indicators (CDI)**, published by the **Centers
for Disease Control and Prevention (CDC)**. It's a standardized, nationwide set of
chronic-disease surveillance measures — the data public-health agencies use to track
conditions like diabetes, asthma, cardiovascular disease, mental health, tobacco use, and
obesity.

**Scale.** The file used was `U.S._Chronic_Disease_Indicators_20260206.csv` — **96 MB**,
**800,000+ rows**, covering **all 50 states plus territories**, **multiple years**, and
**dozens of health topics**.

**The structure — one row per indicator-measurement.** Each row is a single measured value
for one indicator, in one place, in one year, for one demographic slice. The key columns:

| Column | What it holds |
|---|---|
| `YearStart` / `YearEnd` | The reporting period for the record |
| `LocationAbbr` / `LocationDesc` | State/territory abbreviation and full name (also "United States" for national) |
| `Topic` | The chronic-disease category (Diabetes, Asthma, Cardiovascular Disease, Mental Health, …) |
| `Question` | The specific indicator measured (e.g., the exact wording of the metric) |
| `DataValueType` | The *kind* of measure — **age-adjusted prevalence**, crude rate, number, etc. |
| `DataValue` | The actual reported numeric value |
| `Stratification1` | The demographic breakdown — race/ethnicity, gender, or "Overall" |
| `DataSource` | The surveillance system the record came from (BRFSS, NVSS, …) |

**Where the data comes from.** Primarily the **Behavioral Risk Factor Surveillance System
(BRFSS)** — CDC's large telephone health survey — and the **National Vital Statistics
System (NVSS)** — official death-record data (the source for mortality measures like
cardiovascular-disease deaths).

**The single most important structural fact — `DataValueType`.** Because the same indicator
can appear as a crude rate, an age-adjusted rate, a raw count, etc., **every analysis must
filter to the right `DataValueType`** — almost always **age-adjusted prevalence** for fair
cross-population comparison (see §14). Picking the wrong measure type silently produces a
wrong answer. This is the dataset's main "gotcha."

**The long/stacked shape.** CDI is a "long" (tidy/stacked) dataset — one measurement per
row rather than one column per metric. Analysis means *filtering* down to the Topic +
Question + DataValueType + Stratification you want, then aggregating.

---

## 5. The Workflow & Prompt Engineering

**The end-to-end workflow:**

```
  CDC CDI dataset (96 MB CSV, 800k+ rows)
        │  uploaded directly to Julius AI
        ▼
  ┌─────────────────────────────────────────────────────┐
  │ JULIUS AI — one conversation per analysis            │
  │  1. Frame a business question                         │
  │  2. Write a natural-language prompt                    │
  │  3. Julius generates + runs Python (pandas) code      │
  │  4. Julius returns a chart + explanation               │
  │  5. (optional) refine with a follow-up prompt          │
  └───────────────────────────┬─────────────────────────┘
                              │  human interpretation
                              ▼
  ┌─────────────────────────────────────────────────────┐
  │ Insights → narrative → public-health recommendations  │
  │ + a structured evaluation of the tool itself          │
  └─────────────────────────────────────────────────────┘
```

**Prompt engineering — the actual technical skill on display.** The quality of the output
depends heavily on the prompt. The six prompts show a deliberate progression from simple to
highly specified. Compare:

- A **looser** prompt (Analysis 1): *"How has the prevalence of 'Diabetes' changed in
  California vs. Texas over the last 5 years?"* — names the topic, the locations, the time
  window.
- A **highly specified** prompt (Analysis 3): *"Is there a correlation between states with
  high 'Physical Inactivity' and states with high 'Cardiovascular Disease' mortality? Make
  a scatter plot with a regression line with physical inactivity plotted on the x axis and
  cardiovascular disease plotted on the y axes and each point being a state."*

**The lesson the project draws (and you should be able to state):** the more the prompt
**specifies the method** — the exact chart type, what each axis is, the unit of
observation ("each point being a state"), the year — the more reliable and targeted the AI
output. Vague prompts let the AI make assumptions; precise prompts constrain it. Good
prompting is essentially *writing a clear analysis spec in English*.

**Effective-prompt ingredients used across the six analyses:** name the exact `Topic`/
`Question` in quotes, specify the locations or "entire United States," pin the year(s),
state the demographic stratification, and — when it matters — dictate the chart type and
the axes. That precision is what made Julius reliably pick the right slice out of 800k rows.

---

## 6. Analysis 1 — Diabetes Prevalence: California vs. Texas

**Business question.** How has diabetes prevalence changed in California vs. Texas over the
last ~5 years?

**The prompt.** *"How has the prevalence of 'Diabetes' changed in California vs. Texas over
the last 5 years?"*

**What Julius did.** Filtered the CDI dataset to diabetes-prevalence records for CA and TX,
pulled **age-adjusted rates** for 2019–2022, and produced a comparative **line chart**.

**Key findings.**
- **Texas is consistently higher** — ~11.2%–13.4% vs. California's ~9.3%–10.9% across all
  four years.
- **Both trend upward** 2019→2022 (CA ~9.5%→10.7%; TX peaks at 13.4% in 2022).
- **Texas 2021 dip then 2022 surge** — a temporary decline to ~11.2% in 2021, then a jump
  to 13.4% — plausibly delayed reporting or post-pandemic diagnostic catch-up.
- **A persistent 2–3 percentage-point gap** — stable enough to suggest structural
  differences in demographics, risk factors, or healthcare access, not noise.

**The teachable point.** A *consistent* gap is more informative than a one-year difference —
it points at a structural cause. Note also the honest hedge on the 2021→2022 spike
("potentially reflecting reporting effects") rather than over-claiming.

---

## 7. Analysis 2 — Asthma Prevalence by Race/Ethnicity

**Business question.** Which racial/ethnic groups are disproportionately affected by asthma?

**The prompt.** *"Break down 'Asthma' prevalence by Race/Ethnicity. Which groups are
disproportionately affected?"*

**What Julius did.** Filtered to asthma prevalence by racial/ethnic `Stratification`,
aggregated **median rates across states** using the most recent available year per state,
and produced a **ranked summary**.

**Key findings.**
- **Multiracial, non-Hispanic highest** — 15.6%, over 50% above the White, non-Hispanic
  rate of 10.1%.
- **American Indian / Alaska Native, non-Hispanic** — second highest at 12.6%.
- **Black, non-Hispanic** — 11.9%, above the overall average, consistent with established
  research on environmental exposure and healthcare-access disparities.
- **Asian, non-Hispanic lowest** — 1.0%, a large gap that *may partly reflect data
  reporting differences*, not only true prevalence.
- **Hispanic** — 8.3%, below the White rate, but this likely **masks heterogeneity** across
  Hispanic subpopulations.

**The teachable point.** Two pieces of analytical maturity here: (1) using a **median
across states** to avoid one outlier state distorting a group's rate, and (2) flagging that
the strikingly low Asian figure and the aggregated Hispanic figure may be **data
artifacts** — not accepting a surprising number at face value.

---

## 8. Analysis 3 — Physical Inactivity vs. Cardiovascular Disease Mortality

**This is the most statistically substantive analysis — know its numbers cold.**

**Business question.** Is there a correlation between states with high physical inactivity
and states with high cardiovascular-disease mortality?

**The prompt.** *"Is there a correlation between states with high 'Physical Inactivity' and
states with high 'Cardiovascular Disease' mortality? Make a scatter plot with a regression
line with physical inactivity plotted on the x axis and cardiovascular disease plotted on
the y axes and each point being a state."* — the most specified prompt of the six.

**What Julius did.** Extracted per-state physical-inactivity rates and per-state
cardiovascular-disease mortality rates, **merged** them by state, computed correlation
statistics, and produced a **scatter plot with a regression line** annotated with the stats.

**The statistics — memorize these:**
- **Pearson r = 0.721** — a **strong positive** correlation.
- **R² = 0.52** — physical inactivity alone explains **~52% of the state-to-state
  variation** in cardiovascular mortality.
- **p < 0.001** — **highly statistically significant**; extremely unlikely to be chance.

**Key findings.**
- States above **~28% adult inactivity** cluster at the highest cardiovascular mortality
  (220–260 deaths per 100,000).
- A clear gradient runs from ~16% inactivity / ~130 deaths per 100k to ~30% inactivity /
  ~240 deaths per 100k — a **dose-response** pattern.
- Policy implication: population-level interventions against sedentary behavior could
  meaningfully cut cardiovascular deaths.

**The teachable point — and the one caveat you must volunteer: correlation is not
causation.** r = 0.721 is strong, but a cross-sectional state-level correlation can't
*prove* inactivity causes the deaths — confounders (age structure, income, healthcare
access, diet) plausibly drive both. This is also an **ecological analysis** (states, not
individuals), so an **ecological fallacy** risk applies: a state-level relationship doesn't
necessarily hold for individuals. Being able to say "strong, significant, but not causal,
and ecological" is exactly the statistical literacy an interviewer is testing for.

---

## 9. Analysis 4 — Mental Health Distress: Males vs. Females

**Business question.** How do rates of frequent mental distress compare between men and
women across the most populous states?

**The prompt.** *"Compare the rates of 'Frequent Mental Distress' between men and women
across the top 10 most populous states."*

**What Julius did.** Identified the top 10 states, filtered to frequent-mental-distress
records stratified by gender for **2022**, and produced a **grouped bar chart** with
labeled percentages.

**Key findings.**
- **Females higher in every state** — gaps of ~4 to 9.5 percentage points; the
  female-exceeds-male pattern is universal across the states examined.
- **Tennessee highest** — 15.4% (male) and **24.9% (female)** — nearly one in four women.
- **Largest gap in Tennessee** — 9.5 points.
- **Regional pattern** — Southern states (TN, AR, AL, MO) higher for both genders; NE, MN,
  MA lower.
- **Nebraska lowest** — 8.6% (M) / 15.7% (F) — *but still shows the female-higher pattern*,
  meaning the gender disparity holds regardless of baseline.

**The teachable point — an honest data caveat the project itself flags.** The prompt asked
for the "top 10 most populous states," but the screenshot notes Julius actually selected
the **top 10 states by data-record volume**, which is a *proxy* for population, not true
population rank. They overlap heavily but aren't identical — a small example of the AI
interpreting a prompt slightly differently than intended, and exactly why you must read
what the AI did, not just the chart.

---

## 10. Analysis 5 — Cigarette Smoking by Race/Ethnicity

**Business question.** How does current cigarette-smoking prevalence vary across
racial/ethnic groups?

**The prompt.** *"Visualize the disparity in 'Current Cigarette Smoking' among different
race/ethnicity categories for the year 2021."*

**What Julius did.** Filtered to current-cigarette-smoking records for **2021**, stratified
by race/ethnicity, pulled **age-adjusted prevalence**, and produced a **horizontal bar
chart** ranked high to low.

**Key findings.**
- **American Indian / Alaska Native, non-Hispanic highest** — **27.1%**, more than **2.6×**
  the Hispanic rate.
- **Multiracial, non-Hispanic** — 19.3%, well above the national average.
- **Black (15.7%) and White (15.0%) non-Hispanic** — similar to each other.
- **Hispanic lowest** — 10.4%; the project notes this echoes the **"Hispanic health
  paradox"** in epidemiology (Hispanic populations sometimes show better-than-expected
  outcomes despite socioeconomic disadvantage).
- **A ~17-point spread** between highest and lowest → the case for **culturally tailored**
  cessation programs over one-size-fits-all.

**The teachable point.** Naming the "Hispanic health paradox" shows domain knowledge — it
demonstrates you're interpreting the number through public-health literature, not just
reading a bar height.

---

## 11. Analysis 6 — National Obesity Trend

**Business question.** What is the national trend in adult obesity prevalence over time?

**The prompt.** *"Plot the trend of 'Obesity among adults' from the earliest available year
to the latest for the entire United States."*

**What Julius did.** Filtered to national-level ("United States") adult-obesity records,
aggregated by year, and produced a **time-series line chart** for 2019–2022.

**Key findings.**
- **2021 peak** — ~34.9%, up from ~33.5% in 2020 — likely pandemic-era lifestyle
  disruption (less activity, more sedentary time, dietary change).
- **2022 partial reversal** — back to ~33.5% as restrictions eased.
- **Narrow range, alarming baseline** — the whole span is only ~1.4 points (33.5–34.9%),
  but **roughly one in three U.S. adults** was obese throughout.
- **No sustained improvement** — 2022 (~33.5%) is essentially unchanged from 2019 (~33.6%);
  existing interventions have not bent the curve.

**The teachable point.** The headline isn't the small year-to-year wobble — it's that the
*baseline* is ~33% and *flat*. A good analyst reads the level, not just the slope, and
resists over-interpreting a 1.4-point range as a "trend."

*(Minor filename note for a walkthrough: the Analysis 6 image files are named
`Chart_6_Diabetes_Across_Nation.png` / `Question_6_…` even though Analysis 6 is the obesity
trend — a leftover naming slip, not a content error.)*

---

## 12. Key Findings & Recommendations

**The five public-health findings (the synthesis across all six analyses):**

1. **Chronic-disease burden varies sharply by state** — Texas diabetes (~13.4%) ran 2–3
   points above California (~10.7%).
2. **Racial/ethnic disparities are pervasive** — American Indian/Alaska Native and
   Multiracial populations carried disproportionate burden in *both* asthma and tobacco use.
3. **Physical inactivity is a powerful predictor** — r = 0.721 with cardiovascular
   mortality; population-level activity promotion could meaningfully cut heart-disease
   deaths.
4. **Mental distress disproportionately affects women** — females higher in every state
   examined, widest in the South.
5. **Obesity is stuck high** — ~33–35% nationally with no real downward trend.

Plus the **sixth, meta-finding**: AI-assisted analysis is *viable* for rapid exploration of
a large public-health dataset.

**The recommendations (what an agency should do):** prioritize high-burden states (TX for
diabetes, TN for mental health) for funding; build **culturally tailored** programs for the
hardest-hit groups (especially AI/AN communities); invest in physical-activity
infrastructure given the inactivity↔CVD link; expand **gender-responsive** mental-health
services; and use AI tools for **rapid initial surveillance and hypothesis generation**
ahead of formal statistical work.

**The framing to remember:** every analysis ends in a *decision*, not just a chart. The
recommendations are appropriately scoped as *directional* — "prioritize," "invest,"
"explore" — because exploratory analysis supports hypotheses, it doesn't prove causal
policy effects.

---

## 13. Julius AI — Tool Evaluation

The project's second half is a **structured evaluation of the tool itself** — and this is
where the "critical thinking" skill shows. Be ready to discuss both columns.

**What worked well:**
- **Handled the large dataset** — loaded and queried a 96 MB / 800k-row CSV with no
  performance issues.
- **Speed** — each of the six analyses completed in **under a minute** through one
  conversational prompt; the equivalent manual Python work is ~30–60 minutes each.
- **Automatic, well-formatted visualization** — correct scales, labels, legends, and even
  on-chart statistical annotations, with no manual styling.
- **Statistical awareness** — correctly computed Pearson r, R², and p-values when asked,
  and applied sensible transformations (age-adjusted rates, median aggregation).
- **Iterative refinement** — follow-up prompts adjusted charts and drilled into subsets
  without rewriting code.

**Limitations observed:**
- **Black-box methodology** — Julius shows its generated code, but the user must *read it*
  to confirm the statistical approach fits the data and question.
- **Prompt sensitivity** — output quality varied with phrasing; specific prompts (axes,
  chart type, year) gave more reliable results.
- **Reproducibility** — exact outputs can vary between sessions, so scripted workflows are
  preferable for production or regulatory work.
- **Interpretation still required** — Julius produces numbers and charts; **domain
  expertise is still needed** to contextualize them.

**When to use Julius (the project's verdict):**

| Use case | Suitability |
|---|---|
| Initial data profiling / EDA on large datasets | **Excellent** |
| Exploring an unfamiliar dataset through conversation | **Excellent** |
| Quick hypothesis testing with visualizations | Good |
| Generating presentation-ready charts | Good |
| Production data pipelines | **Not recommended** |
| Highly regulated / reproducible analysis | **Not recommended** |

**The teachable point.** The honest verdict — *excellent for exploration, not for
production or regulated work* — is the most important single output of the project. It
shows you can adopt a new tool *and* judge its proper scope, which is more valuable than
uncritical enthusiasm.

---

## 14. Public Health Data Literacy (Concepts to Know)

An interviewer for an analyst role — especially in health, government, or insurance — may
probe whether you *understand* the data, not just chart it. Know these.

**Age-adjusted rate.** A rate statistically standardized to a reference age distribution so
two populations can be compared *fairly*. Florida (older population) and Utah (younger)
will look different on a crude disease rate purely because of age; the age-adjusted rate
removes that distortion. The CDI dataset offers this via `DataValueType` — and this project
correctly uses **age-adjusted prevalence** for its comparisons. If asked "why age-adjusted?"
— *so the comparison reflects disease burden, not just demographic age structure.*

**Prevalence vs. incidence.** *Prevalence* = the share of a population that *has* a
condition at a point in time (what this project measures). *Incidence* = the rate of *new*
cases over a period. Chronic-disease surveillance is mostly prevalence.

**Crude rate vs. age-adjusted rate.** A *crude* rate is the raw count over the population,
unadjusted. Age-adjusted is the comparison-safe version. The `DataValueType` column
distinguishes them — picking the wrong one is the dataset's main trap.

**BRFSS (Behavioral Risk Factor Surveillance System).** CDC's large annual telephone
health survey of U.S. adults — the source for *self-reported* indicators like diabetes,
asthma, smoking, inactivity, mental distress. Because it's self-reported and survey-based,
it carries sampling error and reporting bias.

**NVSS (National Vital Statistics System).** Official birth/death-record data — the source
for *mortality* indicators like cardiovascular-disease deaths. Death records are far more
complete and reliable than survey self-report.

**Mortality rate "per 100,000."** Deaths are reported per 100,000 population so states of
different sizes are comparable — the CVD mortality figures in Analysis 3 (~130–260 per
100k) are in these units.

**Stratification.** Splitting a measure by a demographic dimension — race/ethnicity,
gender, or "Overall." Disparities analysis *is* comparing across stratifications.

**Ecological analysis / ecological fallacy.** Analysis 3 correlates *state-level*
aggregates. An **ecological analysis** uses groups, not individuals, as the unit. The
**ecological fallacy** is wrongly assuming a group-level relationship holds at the
individual level. A state-level inactivity↔mortality correlation does not prove an
inactive *person* will die of heart disease.

**Correlation ≠ causation.** The single most important caveat for Analysis 3 — covered in
§8. Strong, significant, but cross-sectional and confoundable.

---

## 15. Limitations & Honest Caveats

Volunteer these — they show analytical maturity and pre-empt the skeptical questions.

1. **It's exploratory analysis, not causal proof.** Every finding is a *pattern* or
   *association*. Analysis 3's r = 0.721 is a strong correlation, not evidence that
   inactivity *causes* cardiovascular deaths.
2. **Ecological / aggregate data.** State- and group-level analysis — subject to the
   ecological fallacy (§14); conclusions don't transfer to individuals.
3. **Self-reported survey data.** Most indicators come from BRFSS, a telephone survey —
   so they carry self-report bias, sampling error, and coverage gaps. Surprising values
   (e.g., the 1.0% Asian asthma rate) may be **data artifacts**, and the project says so.
4. **AI black-box risk.** Julius generated the code; the analyst must read it to confirm
   the method. The project flags this explicitly as a limitation.
5. **Reproducibility.** AI outputs can vary between sessions — unsuitable for production or
   regulatory reporting. The project states this.
6. **Prompt-interpretation drift.** Analysis 4 is a concrete example — "top 10 most
   populous states" was answered as "top 10 by data-record volume," a proxy. The AI's
   interpretation must be checked against intent.
7. **No raw data or notebook committed.** The 96 MB CSV was uploaded to Julius, not stored
   in the repo; the project's artifacts are the charts, prompts, and write-up. The analysis
   is not re-runnable from this folder alone.
8. **Small time windows.** Several analyses cover only 2019–2022 — short for genuine "trend"
   claims; year-to-year movement can be reporting noise as much as real change.
9. **The skill shown is not coding.** Stated plainly because it's the honest framing — this
   project demonstrates prompt engineering, data literacy, interpretation, and tool
   evaluation. Coding ability is demonstrated by the *other* portfolio projects.

---

## 16. How to Position This Project in an Interview

**Read this section carefully — an AI-assisted project invites one specific skeptical
question, and how you answer it determines whether this project helps or hurts you.**

**The question you will get, in some form:** *"You didn't actually write any code here —
what does this project show me?"*

**The wrong answer:** getting defensive, or overclaiming ("it's basically the same as
coding it myself").

**The right answer — three moves:**

1. **Name the skill honestly and reframe it as valuable.** "You're right that I didn't
   hand-write the pandas code — Julius generated it. What this project demonstrates is the
   layer *around* the code: framing the right question out of an 800,000-row dataset,
   engineering prompts precise enough to get a correct analysis, reading the generated code
   to confirm the method, and interpreting the results with public-health context. Those
   are the parts that stay hard even when an AI writes the code."

2. **Prove you understand what's under the hood.** "Julius isn't a black box that invents
   numbers — it writes and runs real Python and pandas. I can read that generated code, and
   I'd write the same `read_csv` → filter → `groupby` → correlate → plot myself — my SQL and
   Python projects show that. Here the point was the *tool*, not re-proving I can code."

3. **Lead with the critical evaluation.** "Half the project is a structured evaluation of
   the tool — where it's excellent (rapid EDA on big files) and where it's *not* acceptable
   (production pipelines, regulated or reproducible analysis). I caught the AI quietly
   reinterpreting one of my prompts. Knowing when *not* to trust a tool is the skill I'd
   most want you to take from this."

**Why this project genuinely strengthens a portfolio** (say a version of this):
- It's **current** — fluency with AI analysis tools is now an explicitly sought trait.
- It shows **range** — paired with the SQL/Python/Excel projects, it proves you pick the
  right tool for the job rather than reflexively using one.
- It shows **judgment** — the willingness to write down a tool's limitations is rarer and
  more valuable than tool enthusiasm.
- It shows **domain literacy** — age-adjusted rates, BRFSS vs. NVSS, the ecological
  fallacy, the Hispanic health paradox — that's public-health knowledge, not coding.

**The one-sentence positioning:** "It's an AI-assisted exploratory analysis *and* a
critical evaluation of the tool — it demonstrates prompt engineering, public-health data
literacy, and the judgment to know where AI analysis belongs and where it doesn't."

---

## 17. Interview Q&A

Practice these out loud. Answers are written the way you'd actually speak.

**Q1. Walk me through this project.**
"I used Julius AI — an AI data-analysis platform — to explore the CDC's U.S. Chronic
Disease Indicators dataset, a 96 MB file with over 800,000 rows. I ran six analyses, each
from a single plain-English prompt: diabetes trends in California versus Texas, asthma
disparities by race, the link between physical inactivity and cardiovascular mortality, the
gender gap in mental distress, smoking disparities by race, and the national obesity trend.
Julius generated and ran the Python code; I framed the questions, engineered the prompts,
and interpreted the results. The second half of the project is a structured evaluation of
the tool itself."

**Q2. You didn't write the code — what does this project actually demonstrate?**
"Fair question, and I'd answer it directly. It demonstrates the work that stays hard even
when an AI writes the code: framing a good question out of 800,000 rows, prompt engineering
precise enough to get a correct analysis, reading the generated code to verify the method,
and interpreting results with public-health context. My SQL and Python projects show I can
write the code; this one shows I can use an AI tool effectively and — just as important —
evaluate where it shouldn't be used."

**Q3. What is Julius AI actually doing under the hood?**
"It's a large language model that writes and runs Python and pandas code for you. When I
ask a question, it generates real code — I saw `pd.read_csv` on the CDC file, then
filtering, grouping, aggregation, plotting — runs it in a sandbox, and returns the chart
plus an explanation. The generated code is visible, so it's not a black box that fabricates
numbers. It's the same analysis a Python analyst would do; the AI is the interface that
translates English into code."

**Q4. How did you make sure the AI's analysis was correct?**
"A few ways. I read the generated code to confirm it filtered to the right indicator and
the right `DataValueType` — age-adjusted prevalence, which is the dataset's main trap. I
sanity-checked the numbers against what's plausible in public-health literature. And I
caught at least one prompt-interpretation drift — in the mental-health analysis I asked for
the top 10 most populous states and Julius used the top 10 by data-record volume as a
proxy. That's exactly why you read what the AI did, not just the chart."

**Q5. What's age-adjusted prevalence and why does it matter here?**
"It's a rate standardized to a common age distribution so two populations can be compared
fairly. Florida has an older population than Utah, so a crude disease rate would look worse
in Florida purely because of age. Age-adjusting removes that, so the comparison reflects
actual disease burden. The CDI dataset has a `DataValueType` column, and I made sure every
comparison used the age-adjusted version."

**Q6. Tell me about the strongest statistical finding.**
"The physical-inactivity versus cardiovascular-mortality analysis. Across states, the
Pearson correlation was 0.721 — strong and positive — with an R² of 0.52 and a p-value
below 0.001. So inactivity alone explains about half the state-to-state variation in heart-
disease mortality, and it's highly significant. But I'd immediately add the caveat:
correlation isn't causation, it's a cross-sectional state-level analysis, so confounders
like age and income plausibly drive both — and it's ecological, meaning the state-level
relationship doesn't necessarily hold for individuals."

**Q7. What's the ecological fallacy, and does it apply here?**
"It's the mistake of assuming a relationship that holds for groups also holds for
individuals. Analysis 3 correlates state-level rates — states are the unit of observation.
The ecological fallacy would be concluding that an inactive *person* will die of heart
disease. The state-level link is real and useful for policy targeting, but I wouldn't
extend it to individual risk."

**Q8. What were Julius AI's limitations?**
"Four main ones. It's a partial black box — it shows the code but you have to read it to
trust the method. It's prompt-sensitive — vague prompts give worse results. Outputs aren't
perfectly reproducible between sessions, so it's wrong for production or regulated work. And
it produces numbers, not understanding — you still need domain expertise to interpret them.
My verdict was: excellent for rapid exploration and hypothesis generation, not appropriate
for production pipelines or regulatory reporting."

**Q9. When should an analyst use a tool like Julius, and when not?**
"Use it for the exploratory stage — profiling an unfamiliar dataset, quick hypothesis
testing, fast presentation charts. That's where the sub-minute turnaround is a real
advantage. Don't use it for production data pipelines or anything that has to be
reproducible and auditable — regulatory reporting, for instance — because outputs can vary
between runs. The right move is AI for exploration, then scripted Python or SQL for the
formal, reproducible analysis."

**Q10. What was the most important public-health finding?**
"The pervasiveness of racial and ethnic disparities. American Indian and Alaska Native
populations had the highest cigarette-smoking rate at 27.1% — more than two and a half
times the Hispanic rate — and were also near the top for asthma. That kind of consistent,
cross-condition disparity is the strongest argument for culturally tailored interventions
rather than one-size-fits-all programs."

**Q11. How did prompt engineering affect your results?**
"A lot. The more I specified, the better the output. My loosest prompt just named the topic
and locations. My most specified one — the inactivity-versus-mortality one — named both
indicators, asked for a scatter plot with a regression line, and said each point should be
a state and which variable went on which axis. That precision is essentially writing an
analysis spec in English, and it produced a much more reliable result. Vague prompts let
the AI make assumptions; precise prompts constrain it."

**Q12. What would you do differently or next?**
"For anything beyond exploration I'd take Julius's generated code, move it into a proper
Python notebook, and make it reproducible — pin the data version, set the filters
explicitly, and re-run it as a script. I'd also want longer time windows; several of my
trends only covered 2019 to 2022, which is short. And I'd treat these findings as
hypotheses — the inactivity-mortality link, for instance, would justify a proper
multivariable model that controls for confounders."

---

## 18. How to Walk Through This Project Live

If asked to screen-share or talk through the project page, use this order:

1. **State the dual purpose up front** — "this is two projects in one: an exploratory
   public-health analysis, and an evaluation of an AI analysis tool." Saying that first
   pre-empts the "you didn't code it" question.
2. **Show the dataset** — the CDC CDI: 96 MB, 800k+ rows, the long/stacked structure, and
   the key columns. Emphasize `DataValueType` and why age-adjusted prevalence matters.
3. **Show one Julius prompt screenshot** — point at the *generated Python code* panel.
   Make the point explicitly: "it writes and runs real pandas; it's not fabricating
   numbers."
4. **Walk the strongest analysis — Analysis 3** (inactivity vs. CVD mortality). Give the
   stats (r = 0.721, R² = 0.52, p < 0.001) and *immediately* give the caveat (correlation
   ≠ causation, ecological). Leading with the caveat is what signals statistical maturity.
5. **Show one disparities analysis** — asthma or smoking by race — and name a piece of
   domain knowledge (the Hispanic health paradox, or flagging the suspicious 1.0% figure
   as a possible data artifact).
6. **Spend real time on the tool evaluation** — the "what worked / limitations / when to
   use" verdict. This is the critical-thinking payload.
7. **Close on the positioning** — "AI for exploration, scripted code for production; the
   skill here is prompt engineering, data literacy, and knowing the tool's limits."

**Pacing tip:** don't oversell the six analyses as if they were the hard part — they're
solid EDA. Spend your time on (a) what Julius does under the hood, (b) Analysis 3's stats
*with* its caveats, and (c) the tool evaluation. Those three show judgment.

---

## 19. Glossary

- **Julius AI** — a chat-based, AI-powered data-analysis platform; generates and runs
  Python/pandas code from natural-language prompts. Version used: "Julius 1.0 Lite."
- **Prompt engineering** — crafting natural-language instructions precise enough to get a
  correct, targeted analysis from an AI tool.
- **CDI (U.S. Chronic Disease Indicators)** — the CDC's standardized nationwide set of
  chronic-disease surveillance measures; the dataset analyzed (96 MB, 800k+ rows).
- **CDC** — Centers for Disease Control and Prevention; publisher of the dataset.
- **BRFSS (Behavioral Risk Factor Surveillance System)** — CDC's large annual telephone
  health survey; the source of most self-reported indicators in CDI.
- **NVSS (National Vital Statistics System)** — official U.S. birth/death-record data; the
  source of mortality indicators.
- **Prevalence** — the share of a population that has a condition at a point in time (what
  this project measures).
- **Incidence** — the rate of *new* cases over a period (distinct from prevalence).
- **Age-adjusted rate** — a rate standardized to a reference age distribution so
  populations with different age structures can be compared fairly.
- **Crude rate** — an unadjusted raw rate (count ÷ population).
- **`DataValueType`** — the CDI column specifying which kind of measure a row holds
  (age-adjusted prevalence, crude rate, number, …); filtering to the right one is essential.
- **Stratification** — a demographic breakdown of a measure (race/ethnicity, gender,
  "Overall").
- **Pearson r** — a correlation coefficient from −1 to +1; 0.721 here = strong positive.
- **R²** — the share of variance in one variable explained by the other; 0.52 = ~52%.
- **p-value** — the probability the observed relationship arose by chance; p < 0.001 =
  highly significant.
- **Regression line** — the best-fit line through a scatter plot summarizing the trend.
- **Correlation ≠ causation** — a relationship between two variables doesn't prove one
  causes the other.
- **Ecological analysis** — analysis using groups (e.g., states) as the unit of
  observation rather than individuals.
- **Ecological fallacy** — wrongly assuming a group-level relationship holds for
  individuals.
- **Confounder** — a third variable that influences both variables in a correlation,
  potentially explaining the apparent link.
- **Hispanic health paradox** — the epidemiological observation that Hispanic populations
  sometimes show better-than-expected health outcomes despite socioeconomic disadvantage.
- **EDA (Exploratory Data Analysis)** — the initial, open-ended stage of investigating a
  dataset to find patterns and generate hypotheses.

---

*This study guide documents the project as presented. The authoritative reference is the
project page `index.md` and the prompt/chart screenshots in `images/`. The underlying 96 MB
CDC dataset was uploaded to Julius AI and is not stored in this folder. When this guide and
the project page disagree, the project page wins.*