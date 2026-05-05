# Phase 6 Inventory — Read-Only Inspection Pass

Generated: 2026-05-04  
Test baseline confirmed: **256 tests collected**

---

## Section 1 — Tab and Surface Structure

### Three top-level tabs (app.py line 2511)

```python
school_finder_tab, major_explorer_tab, find_your_fit_tab = st.tabs(
    ["School Finder", "Major Explorer", "Find Your Fit"]
)
```

### Shared Sidebar (app.py lines 418–620, `render_sidebar()`)

Renders on every tab. Sub-sections in order:

- Title + caption
- `---` divider
- **Filters** subheader
  - State multiselect
  - School type multiselect
  - Campus setting multiselect
  - School size multiselect
  - Minimum % Pell Grant slider
  - Mission-driven institutions expander (multiselect inside)
  - Schools' avg SAT range slider
  - Undergraduate enrollment slider
  - Show small schools checkbox
  - Filter by major (CIP) selectbox (Phase 13.2)
- `---` divider
- **Your test scores (optional)** subheader
  - SAT composite number_input
  - ACT composite number_input
  - Family income bracket selectbox
- `---` divider
- **Priorities** subheader
  - Quick start selectbox (preset profiles)
  - 7× scoring dimension weight sliders

---

### School Finder tab (app.py lines 2523–2603)

Primary render file: `app.py`; helper file: `page_modules/school_finder.py` (59 lines, cross-tab helpers only)  
Approximate lines in app.py owned by this tab's render logic: ~1,900 (sidebar helpers, PDF/CSV export, pin, results, map, comparison, detail cards)

Sub-sections in render order:

1. **Title** — "Results" (`st.title`)
2. **Cross-tab CIP banner** — shown once after Major Explorer handoff (app.py 2527–2531)
3. **Summary banner** — school count + active priorities + filter summary (app.py 2534, `render_summary_banner()`)
4. **Export row** — rows-to-export `number_input` + CSV download button + PDF download button (app.py 2536, `render_export_row()`)
5. **Pin selector** — multiselect + Clear pins button (app.py 2538, `render_pin_selector()`)
6. **Results table** — `st.dataframe` with 14 columns including `ProgressColumn` for Match score (app.py 2540, `render_results()`)
7. **Map expander** — "🗺️ Map of matching schools (N schools)" (app.py 2542, `render_map()`)
8. **Comparison expander** — "📊 Compare pinned schools (2–4)" containing side-by-side table + grouped bar chart (app.py 2544, `render_comparison()`)
9. **Pinned school detail cards** — one bordered card per pinned school (app.py 2546, `render_pinned_cards()`)
   - Each card contains: context badges (Carnegie/test policy/MSI/religion), header with acceptance badge, "Why this rank?" explainer, CI bar, sensitivity tier badge, key metrics grid (8 metrics), radar chart, Student Body section (demographics stacked bar + outcomes detail), Earnings Mobility section (grouped bar chart), Program-level outcomes section (4 metric tiles), Programs offered expander (table with Explore buttons)
10. **About the Data expander** — methodology for BLS/OEWS/EP/geographic/work-environment data (app.py 2548–2601)

---

### Major Explorer tab (page_modules/major_explorer.py — 1,135 lines)

Primary render file: `page_modules/major_explorer.py`, `render()` at line 1106

Sub-sections in render order:

1. **Header + caption** — "Major Explorer" (lines 1108–1111)
2. **Alignment context banner** — Phase 12.3: tip (quiz not taken), success (quiz taken), or silent (zero-variance vector) (lines 1124–1136)
3. **Major picker** — `st.selectbox` "Select a major", annotated with ⭐ for aligned majors (lines 1161–1171)
4. **Major description block** — Phase 11.1A: hand-authored overview + "What you'll learn" + "Typical classes" + related majors, or stub NCES text (lines 1183–1187)
5. **"See schools strong in this major →" button** — Phase 13.2 cross-tab handoff to School Finder (lines 1190–1200)
6. **NY Fed Labor Market Outcomes** — Phase 11.2B.3: 5 `st.metric` tiles (unemployment, underemployment, early wage, mid-career wage, grad degree share) (lines 1205–1207)
7. **Scorecard Outcomes panel** — 4 `st.metric` tiles (earnings 1yr/4yr/5yr, debt); "About these numbers" expander (lines 1217–1256)
8. **Wages and projections summary** — Phase 9.5: 4 `st.metric` tiles (median wage, 10yr growth, total employment, routing occupations count) (lines 1261–1263)
9. **Career paths and occupations** — Phase 9.4: `st.dataframe` of routing occupations with wage/growth/openings/education columns (lines 1267–1269)
10. **Industries that hire this major** — Phase 11.3.3: horizontal bar chart (top 10 NAICS + optional Other row) (lines 1273–1275)
11. **Work environment** — Phase 10.5: horizontal bar chart, 13 O*NET work-context elements colored by quartile (lines 1279–1283)
12. **Where these jobs are** — Phase 10.4: side-by-side USA choropleths (Total Employment + Location Quotient) (lines 1287–1290)
13. **Schools strong in this major** — Phase 8.4: ranked table of top 25 schools with "📌 Pin" buttons (lines 1294–1350)

---

### Find Your Fit tab (page_modules/find_your_fit.py — 262 lines)

Primary render file: `page_modules/find_your_fit.py`, `render()` at line 288

Sub-sections in render order (pre-submission state):

1. **Header + intro** — "Find Your Fit", O*NET methodology description (lines 97–112)
2. **Questionnaire** — 6 `st.expander` sections (one per RIASEC dimension), each with 10 `st.radio` items on a 5-point Likert scale (lines 115–145)
3. **Progress bar** — `st.progress(total_answered / 60)` (line 146)
4. **"See my results" button** — disabled until all 60 items answered (lines 149–170)

Post-submission state (`fyf_submitted == True`):

5. **Your Interest Profile** — Holland Code `st.metric` + horizontal bar chart (6 RIASEC dimensions) (lines 178–208)
6. **Majors Aligned with Your Interests** — top 10 table with correlation scores + "Explore →" buttons (lines 213–281)
7. **Shared results banner** — shown when `?riasec=...` URL param detected (Phase 13.4b) (lines 226–246)
8. **"Retake the questionnaire" button** (line 303)

---

## Section 2 — Chart Inventory

| # | Tab / Sub-section | Library | Chart type | File : approx. line | Accessibility annotation |
|---|-------------------|---------|------------|---------------------|--------------------------|
| 1 | School Finder / Map expander | `plotly.graph_objects` | Scattermapbox (2 traces: black outline + RdYlGn score-colored markers) | app.py : 2096–2141 | Caption below: "Each dot is one school, colored by match score (red = low match, green = high match)." No alt text / aria-label. |
| 2 | School Finder / Pinned card — Percentile profile | `plotly.graph_objects` | Scatterpolar (radar / spider) | app.py : 1378–1401 | `hovertemplate` with dimension label + percentile. No alt text / aria-label. |
| 3 | School Finder / Pinned card — Student Body | `plotly.graph_objects` | Bar (horizontal stacked — gender row + race/ethnicity row) | app.py : 1471–1513 | Per-segment hovertemplate with label + %. No alt text / aria-label. |
| 4 | School Finder / Pinned card — Earnings Mobility | `plotly.graph_objects` | Bar (vertical grouped — 3 income terciles) | app.py : 1600–1622 | Per-bar hovertemplate + text labels on bars. Caption below with source note. No alt text / aria-label. |
| 5 | School Finder / Pinned card — Match score CI | `plotly.graph_objects` | Custom (shapes + annotations, no trace type) — confidence interval band + point estimate marker | app.py : 1648–1712 | Caption below with score + CI range + dimensions reported. No alt text / aria-label. |
| 6 | School Finder / Comparison expander | `plotly.graph_objects` | Bar (grouped — one group per scoring dimension, one bar per school) | app.py : 2343–2390 | Caption below: "Bar heights are percentile ranks within the filtered population…". No alt text / aria-label. |
| 7 | Major Explorer / Work environment | `plotly.graph_objects` | Bar (horizontal — 13 O*NET elements, color-coded by quartile) | major_explorer.py : 591–615 | Caption below with quartile color legend. No alt text / aria-label. |
| 8 | Major Explorer / Where these jobs are (left) | `plotly.graph_objects` | Choropleth (USA states — Viridis scale, total employment) | major_explorer.py : 684–701 | hover template with state, employment, coverage %. No alt text / aria-label. |
| 9 | Major Explorer / Where these jobs are (right) | `plotly.graph_objects` | Choropleth (USA states — Viridis scale, location quotient) | major_explorer.py : 714–734 | hover template with state, LQ, coverage %. Caption: color scale capped at 5.0. No alt text / aria-label. |
| 10 | Major Explorer / Industries that hire this major | `plotly.graph_objects` | Bar (horizontal — top 10 NAICS3 + optional Other row) | major_explorer.py : 1032–1056 | hover template with title + share %. Caption below with source/methodology. No alt text / aria-label. |
| 11 | Find Your Fit / Your Interest Profile | `plotly.graph_objects` | Bar (horizontal — 6 RIASEC dimension scores) | find_your_fit.py : 191–208 | hover template with dimension + score. No alt text / aria-label. |

**None of the 11 charts have Streamlit-level alt text, `aria-label`, or a programmatic descriptive caption rendered as accessible text above the chart.** Hover templates exist on all but chart #5, but those are not screen-reader accessible.

---

## Section 3 — Interactive Element Inventory

### `st.multiselect` (6 instances)

| Widget | Key | Location | Label descriptiveness |
|--------|-----|----------|-----------------------|
| State filter | `filter_states` | Sidebar, app.py 427 | Descriptive |
| School type filter | `filter_controls` | Sidebar, app.py 435 | Descriptive |
| Campus setting filter | `filter_settings` | Sidebar, app.py 444 | Descriptive |
| School size filter | `filter_sizes` | Sidebar, app.py 450 | Descriptive |
| Mission-driven (inside expander) | `filter_mission` | Sidebar, app.py 464 | Descriptive |
| Pin schools for detail view | `pinned_schools` | School Finder main area, app.py 1158 | Descriptive ("📌 Pin schools for detail view") |

- Keys follow consistent `filter_*` pattern for sidebar filters; `pinned_schools` is its own category.

### `st.selectbox` (4 instances)

| Widget | Key | Location | Label descriptiveness |
|--------|-----|----------|-----------------------|
| Filter by major (CIP) | `cip_filter_widget` | Sidebar, app.py 511 | Descriptive |
| Family income bracket | `selected_income_bracket` | Sidebar, app.py 553 | Descriptive |
| Quick start (preset) | *(no key)* | Sidebar, app.py 582 | Descriptive |
| Select a major | `major_picker_widget` | Major Explorer, major_explorer.py 1161 | Descriptive |

- Quick start selectbox intentionally has no `key=` (value is derived from weights, not state).

### `st.slider` / `st.select_slider` (10 instances total)

| Widget | Key | Location |
|--------|-----|----------|
| Min % Pell Grant recipients | `filter_pell_min` | Sidebar, app.py 453 |
| Schools' avg SAT range | *(no key)* | Sidebar, app.py 473 |
| Undergraduate enrollment | *(no key)* | Sidebar, app.py 483 |
| Weight: Low Net Price | `weight_affordability` | Sidebar, app.py 597 |
| Weight: High Graduation Rate | `weight_graduation_rate` | Sidebar, app.py 597 |
| Weight: High Retention Rate | `weight_retention_rate` | Sidebar, app.py 597 |
| Weight: High Earnings After Graduation | `weight_earnings` | Sidebar, app.py 597 |
| Weight: High Selectivity | `weight_selectivity` | Sidebar, app.py 597 |
| Weight: Low Student Debt | `weight_low_debt` | Sidebar, app.py 597 |
| Weight: High Loan Repayment Rate | `weight_repayment` | Sidebar, app.py 597 |

- Weight slider keys follow consistent `weight_{dim_key}` pattern.
- SAT range and enrollment range sliders have **no key** (intentionally excluded from URL state, per comment at app.py 127).

### `st.checkbox` (1 instance)

| Widget | Key | Location | Label |
|--------|-----|----------|-------|
| Show small schools | `filter_show_small` | Sidebar, app.py 488 | "Show schools with <250 students (less reliable metrics)" — descriptive |

### `st.number_input` (3 instances)

| Widget | Key | Location |
|--------|-----|----------|
| Your SAT composite (400–1600) | `user_sat_raw` | Sidebar, app.py 537 |
| Your ACT composite (1–36) | `user_act_raw` | Sidebar, app.py 543 |
| Rows to export | `csv_export_top_n` | School Finder export row, app.py 1103 |

### `st.radio` (60 instances — FYF questionnaire)

- All 60 items rendered in `find_your_fit.py:_render_questionnaire()` lines 115–143
- Keys: `fyf_item_{item_id}` — consistent `fyf_item_` prefix
- Labels: verbatim O*NET Interest Profiler Short Form activity text — descriptive by design

### `st.button` / `st.form_submit_button`

| Button label | Key | Location | Type |
|-------------|-----|----------|------|
| Clear pins | *(generated)* | Pin selector, app.py 1172 | Regular |
| "📌 Pin" (×25 per major) | `pin_btn_{unit_id}_{cip_code}` | Major Explorer schools table, major_explorer.py 1340 | Regular |
| "See schools strong in this major →" | `see_schools_{cip4_str}` | Major Explorer, major_explorer.py 1190 | Regular |
| "Explore →" (×10, top-10 table) | `explore_riasec_{cip4}` | FYF results, find_your_fit.py 276 | Regular |
| "Explore →" (×N, programs offered) | `explore_program_{unitid}_{cip4}` | School Finder programs expander, app.py 1817 | Regular |
| "See my results" | `fyf_submit` | FYF questionnaire, find_your_fit.py 149 | `type='primary'` |
| "Retake the questionnaire" | `fyf_retake` | FYF results, find_your_fit.py 303 | Regular |
| "Take the quiz yourself →" | `dismiss_shared_results` | FYF shared results banner, find_your_fit.py 233 | Regular |

- Dynamic buttons (`pin_btn_*`, `explore_riasec_*`, `explore_program_*`, `see_schools_*`) encode enough identity in the key to be unique per rerun.
- Labels are descriptive except "Explore →" which lacks context without surrounding row content (open question for accessibility).

### `st.download_button` (2 instances)

| Label | Key | Location |
|-------|-----|----------|
| Download CSV | *(generated)* | Export row, app.py 1120 |
| Download PDF | *(generated)* | Export row, app.py 1134 |

### `st.tabs` (1 instance)

- `st.tabs(["School Finder", "Major Explorer", "Find Your Fit"])` — app.py 2511
- Cannot be programmatically switched; cross-tab handoffs use banners instead.

### `st.expander` (11 instances)

| Expander title | Default expanded | Location |
|----------------|-----------------|----------|
| "Mission-driven institutions" | False | Sidebar, app.py 462 |
| "🗺️ Map of matching schools (N schools)" | False | School Finder, app.py 2200 |
| "📊 Compare pinned schools (N pinned)" | False | School Finder, app.py 2408 |
| "All programs offered (N)" | False | Pinned card, app.py 1790 |
| "About the Data" | False | School Finder, app.py 2548 |
| "About these numbers" | False | Major Explorer outcomes, major_explorer.py 1241 |
| "Realistic" (RIASEC dim) | Session-state-controlled | FYF questionnaire, find_your_fit.py 131 |
| "Investigative" (RIASEC dim) | Session-state-controlled | FYF questionnaire, find_your_fit.py 131 |
| "Artistic" (RIASEC dim) | Session-state-controlled | FYF questionnaire, find_your_fit.py 131 |
| "Social" (RIASEC dim) | Session-state-controlled | FYF questionnaire, find_your_fit.py 131 |
| "Enterprising" (RIASEC dim) | Session-state-controlled | FYF questionnaire, find_your_fit.py 131 |
| "Conventional" (RIASEC dim) | Session-state-controlled | FYF questionnaire, find_your_fit.py 131 |

- RIASEC expander state is persisted in `st.session_state["fyf_expander_states"]` keyed by dimension letter.

### Custom HTML (1 instance)

- **Earnings Mobility empty state** — `st.markdown(..., unsafe_allow_html=True)` with inline `<div style='background:#f0f0f0;...'>` (app.py 1583–1587). No ARIA role.

---

## Section 4 — Data Source Inventory

| # | Source name | File path on disk | Loader function | Snapshot / version | In "About the Data" expander? |
|---|-------------|------------------|-----------------|-------------------|-------------------------------|
| 1 | College Scorecard Institution-Level | `data/cleaned/colleges_cleaned.csv` | `app.py:load_colleges()` | "Most-Recent-Cohorts-Institution.csv" — no date in filename; version not pinned in code | Not explicitly (expander covers BLS/OEWS/geographic/work-env only) |
| 2 | College Scorecard Field of Study | `data/cleaned/field_of_study_cleaned.csv` | `major_explorer.py:load_field_of_study()` | "Most-Recent-Cohorts-Field-of-Study.csv" — same vintage as #1, not pinned | Not explicitly |
| 3 | BLS OEWS National (May 2024) | `data/cleaned/occupations_master.csv` | `major_explorer.py:_load_career_paths_data()` | May 2024 (traceable from raw file `national_M2024_dl.xlsx`) | Yes — "BLS Occupational Employment and Wage Statistics, May 2024" |
| 4 | BLS Employment Projections 2024–2034 | `data/cleaned/occupations_master.csv` (merged into same file as #3) | `major_explorer.py:_load_career_paths_data()` | 2024–2034 (from raw file `occupation.xlsx`; BLS EP release cycle not pinned) | Yes — "BLS Employment Projections, 2024–2034" |
| 5 | BLS OEWS State-Level (May 2024) | `data/cleaned/state_occupations.csv` → `data/cleaned/cip4_state_employment.csv` | `major_explorer.py:_load_cip4_state_employment()` | May 2024 (same OEWS release as #3) | Yes — geographic distribution methodology note |
| 6 | NCES CIP–SOC Crosswalk | `data/cleaned/cip4_to_soc.csv` | `major_explorer.py:_load_career_paths_data()` (second return value) | CIP 2020 → SOC 2018 (raw: `CIP2020_SOC2018_Crosswalk.xlsx`) | Yes — "NCES CIP–SOC Crosswalk (CIP 2020 → SOC 2018)" |
| 7 | BLS OEWS NAICS Industry Distribution | `data/cleaned/soc_to_naics3.csv` → `data/cleaned/cip4_naics3_distribution.csv` | `naics_distribution.py:get_naics_distribution()` via `naics_distribution._load()` | May 2024 (same OEWS release) | Yes — "BLS Occupational Employment and Wage Statistics, May 2024 release (3-digit NAICS)" in chart caption; not in About the Data expander body |
| 8 | O*NET Work Context v30.2 | `data/cleaned/work_context.csv` → `data/cleaned/cip4_work_context.csv` | `major_explorer.py:_load_cip4_work_context()` | O*NET 30.2 (from chart caption; raw prep in `data_prep_workcontext.py`) | Yes — work environment methodology note in About the Data expander |
| 9 | NY Fed Labor Market Outcomes (Feb 2026) | `data/processed/nyfed_outcomes.parquet` | `nyfed_outcomes.py:get_nyfed_outcomes()` via `_load_outcomes_df()` | February 2026 release (from caption in Major Explorer NY Fed panel, major_explorer.py 961) | Not in About the Data expander; source/date only in chart caption |
| 10 | CIP4 RIASEC Interest Profiles | `data/cleaned/cip4_riasec.csv` | `riasec_distribution.py:_load_riasec_data()` | O*NET (version implicit in source; not pinned in code or filenames) | Not mentioned |
| 11 | NCES Major Descriptions (hand-authored) | `data/major_descriptions.yaml` | `major_descriptions.py:load_major_descriptions()` | Internal; no versioning | Not mentioned |
| 12 | BLS OEWS Major-Level Aggregates | `data/cleaned/major_outcomes.csv` | `major_explorer.py:_load_major_outcomes()` | Derived from #3+#6 (May 2024 OEWS + CIP 2020 crosswalk) | Yes — implicitly via the wages/projections methodology note |

**Open question:** `data/processed/top_60_cip4.csv` exists on disk (`scripts/rank_top_cip4.py` produces it) but is not consumed by the runtime app. Not counted above.

---

## Section 5 — Color and Palette Usage

### Centralized palette

- **No centralized palette constant in `config.py`.**
- A named dict `_DEMO_COLORS` exists in `app.py` at lines 1408–1421 (module-level, not in config). It is used only for demographics + earnings mobility charts.
- A local `palette` list `["#0072B2", "#E69F00", "#009E73", "#CC79A7"]` is defined inline in `_build_comparison_chart()` (app.py 2348) — not shared.

### Color literals by usage area

#### Demographics / Earnings Mobility charts — `_DEMO_COLORS` dict (app.py 1408–1421, Wong 2011 colorblind-safe)

| Token | Hex | Used for |
|-------|-----|---------|
| Women | `#CC79A7` | Gender stacked bar |
| Men/Other | `#56B4E9` | Gender stacked bar |
| Black/AA | `#0072B2` | Race/eth stacked bar |
| Hispanic | `#E69F00` | Race/eth stacked bar |
| Asian | `#009E73` | Race/eth stacked bar |
| White | `#56B4E9` | Race/eth stacked bar (**same hex as Men/Other**) |
| Non-resident | `#D55E00` | Race/eth stacked bar |
| Other/Unknown | `#999999` | Race/eth stacked bar |
| Low Income | `#0072B2` | Mobility bar (**same hex as Black/AA**) |
| Mid Income | `#E69F00` | Mobility bar (**same hex as Hispanic**) |
| High Income | `#009E73` | Mobility bar (**same hex as Asian**) |

#### Comparison chart — inline local palette (app.py 2348)

`["#0072B2", "#E69F00", "#009E73", "#CC79A7"]` — up to 4 schools, Wong 2011

#### CI bar chart (app.py 1652–1677)

| Element | Color |
|---------|-------|
| Background track | `rgba(200,200,200,0.15)` |
| CI band fill | `rgba(99,143,255,0.22)` |
| CI band border | `rgba(0,114,178,0.35)` |
| Point estimate line | `#0072B2` |
| Score annotation | `#0072B2` |

#### Work environment quartile coloring (major_explorer.py 514–523)

| Quartile | Hex | Label |
|----------|-----|-------|
| Bottom (< Q25) | `#94a3b8` | Medium gray |
| Below average (Q25–Q50) | `#cbd5e1` | Light gray |
| Above average (Q50–Q75) | `#7da7e8` | Light blue |
| Top (≥ Q75) | `#2563eb` | Dark blue |

- Colors are hardcoded in `_quartile_color()` local function; not imported from config.

#### NAICS distribution chart (major_explorer.py 974–975)

| Element | Hex | Note |
|---------|-----|------|
| Real industries | `#1f77b4` | Default Plotly blue — **NOT Wong palette** |
| "Other" row | `#999999` | Muted gray |

#### RIASEC interest profile bar (find_your_fit.py 195)

- `#1f77b4` — default Plotly blue, **NOT Wong palette**, inconsistent with comparison/demo charts

#### Choropleth color scales (major_explorer.py 688, 724)

- Both Total Employment and Location Quotient choropleths use Plotly named scale **"Viridis"**

#### Map scatter (app.py 2116)

- Color scale: **"RdYlGn"** (Plotly named scale, mapped to match score 0–100)
- Marker outline: `"black"` (named)
- Map land: `"lightgray"` (named), subunit borders: `"white"` (named)

#### Acceptance badges — emoji + PDF colors

| Label | Emoji | PDF RGB |
|-------|-------|---------|
| Safety | 🟢 | `(200, 230, 200)` — green tint |
| Match | 🟡 | `(255, 243, 200)` — yellow tint |
| Reach | 🔴 | `(255, 210, 210)` — red tint |
| N/A | ⚪ | `(220, 220, 220)` — gray |

Rank emojis in comparison table: 🟢 = best, 🟡 = middle, 🔴 = worst — defined inline at app.py 1244–1249 and 2262–2270.

#### Miscellaneous

| Element | Value | Location |
|---------|-------|---------|
| Earnings Mobility empty-state div bg | `#f0f0f0` | app.py 1583 |
| Earnings Mobility empty-state text | `#888` | app.py 1584 |
| PDF card background | RGB `(245, 245, 245)` | app.py 93 |
| PDF card border | RGB `(180, 180, 180)` | app.py 94 |
| Chart gridlines (multiple) | `rgba(180,180,180,0.25)` | app.py 1685, 2378 |

---

## Section 6 — URL State and Shareable Surfaces

All URL state is managed by `_parse_url_into_session_state()` (app.py 324–383) and `_write_session_state_to_url()` (app.py 386–412). The canonical parameter map is `URL_PARAM_MAP` (app.py 132–163). The encoding helpers (`encode_tab`, `decode_tab`, `encode_riasec`, `decode_riasec`) live in `url_state.py`.

### Complete URL parameter map

| URL param | session_state key | Type | Default | Affected surface |
|-----------|------------------|------|---------|-----------------|
| `w_aff` | `weight_affordability` | int | 3 | Sidebar weight slider |
| `w_grad` | `weight_graduation_rate` | int | 3 | Sidebar weight slider |
| `w_ret` | `weight_retention_rate` | int | 3 | Sidebar weight slider |
| `w_earn` | `weight_earnings` | int | 3 | Sidebar weight slider |
| `w_sel` | `weight_selectivity` | int | 3 | Sidebar weight slider |
| `w_debt` | `weight_low_debt` | int | 3 | Sidebar weight slider |
| `w_repay` | `weight_repayment` | int | 3 | Sidebar weight slider |
| `sat` | `user_sat_raw` | int | 0 | Acceptance badges |
| `act` | `user_act_raw` | int | 0 | Acceptance badges |
| `states` | `filter_states` | list (comma-joined) | `[]` | School Finder state filter |
| `control` | `filter_controls` | list | `[]` | School Finder type filter |
| `setting` | `filter_settings` | list | `[]` | School Finder setting filter |
| `size` | `filter_sizes` | list | `[]` | School Finder size filter |
| `mission` | `filter_mission` | list | `[]` | School Finder mission filter |
| `pell` | `filter_pell_min` | int | 0 | Pell % floor slider |
| `small` | `filter_show_small` | bool (`1`/`0`) | False | Small schools checkbox |
| `pins` | `pinned_schools` | list (comma-joined school names) | `[]` | Pinned school detail cards |
| `cip` | `selected_cip` | int | 0 | Major Explorer picker |
| `income` | `selected_income_bracket` | str | `"Don't know / skip"` | Net price bracket scoring |
| `tab` | `_active_tab` | str | `"school_finder"` | Tab hint banner only (st.tabs can't be programmatically switched) |
| `riasec` | `_url_riasec_vector` | str (12-char encoded) | `""` | Find Your Fit shared results |

**Intentionally omitted:** SAT range slider, enrollment range slider (tuple values, excluded per comment at app.py 127–130).

### Clamping and validation logic

- **List params**: `_clamp_filter_list(key, valid_list)` drops any value not in the current dataset (guards against stale URLs from old data versions).
- **Income bracket**: clamped to `config.INCOME_BRACKETS` keys; garbage resets to `"Don't know / skip"` (app.py 380–381).
- **Tab**: `decode_tab()` in `url_state.py` accepts only `{"school_finder", "major_explorer", "find_your_fit"}`; any other value returns None and is dropped. Default (`"school_finder"`) is also dropped so it doesn't appear in URLs.
- **RIASEC**: `decode_riasec()` validates exact 18-char format (`R##I##A##S##E##C##`), dimension order, and score range 0–40. Any failure returns None.
- **`_url_parsed` guard**: entire parse runs exactly once per browser session to prevent subsequent widget interactions from being overwritten (app.py 330–331).

---

## Section 7 — Empty State and Error Handling

| # | Trigger condition | File : line | User-facing message |
|---|------------------|-------------|---------------------|
| 1 | Cleaned colleges CSV not found on disk | app.py : 209 | `st.error("Cleaned data file not found at {path}. Run python data_prep.py to generate it.")` + `st.stop()` |
| 2 | No schools match current filters (results table) | app.py : 1187 | `st.info("No schools match the current filters. Try loosening them.")` |
| 3 | No schools match + map opened | app.py : 2201 | `st.info("No schools match the current filters — nothing to map.")` |
| 4 | Schools exist but none have coordinates (map) | app.py : 2208 | `st.info("None of the matching schools have published coordinates — nothing to plot. Try loosening your filters.")` |
| 5 | Map marker cap applied | app.py : 2222 | `st.caption("⚠️ Showing the top 2,000 schools by match score (of N matching). Rendering all of them slows the map.")` |
| 6 | Map: schools excluded for missing coordinates | app.py : 2228 | `st.caption("ℹ️ {N} school(s) excluded — no published coordinates.")` |
| 7 | Comparison opened with < 2 pinned schools | app.py : 2411 | `st.info("Pin 2 to 4 schools above to compare them side by side. You currently have N pinned.")` |
| 8 | Comparison: fewer than 2 schools have data | app.py : 2447 | `st.info("Need at least 2 schools with available data to compare.")` |
| 9 | Comparison: > 4 schools pinned | app.py : 2418 | `st.warning("Comparison is limited to 4 schools. Showing the first 4 of your N pinned schools (in pin order).")` |
| 10 | Comparison: named school not found in data | app.py : 2441 | `st.caption("⚠️ Couldn't find data for: {names}. Skipped from the comparison.")` |
| 11 | Pinned card: named school not found in data | app.py : 2012 | `st.warning("Couldn't find data for {name}.")` |
| 12 | School demographics all missing | app.py : 1528 | `st.caption("Demographic breakdown not reported.")` |
| 13 | Earnings Mobility all three income terciles missing | app.py : 1582 | Inline HTML div: "Mobility data not reported for this school." |
| 14 | Program-level outcomes: school doesn't offer selected major | app.py : 1745 | `st.caption("{name} does not offer this major.")` |
| 15 | Program-level outcomes: school offers major but cohort < 30 | app.py : 1752 | `st.caption("{name} offers this major, but the program's cohort size fell below the Scorecard's reporting threshold (n < 30).")` |
| 16 | Schools strong in major: no 5yr earnings data | major_explorer.py : 1302 | `st.info("No institutions report 5-year graduate earnings for this major…")` |
| 17 | BLS wages/projections: no major_outcomes row for this CIP | major_explorer.py : 424 | `st.info("BLS occupational data is not available for this major (CIP {cip4_str}).")` |
| 18 | Career paths: no routing SOCs in crosswalk | major_explorer.py : 776 | `st.info("No BLS-defined routing occupations were found for this major (CIP {cip4_str})…")` |
| 19 | Career paths: routing SOCs found but all aggregation-level (no OEWS match) | major_explorer.py : 796 | `st.warning("This major routes to {N} occupations in the crosswalk, but none of them have wage or projection data available at the detailed SOC level.")` |
| 20 | Career paths: cip4_str empty (no selection yet) | major_explorer.py : 769 | `st.info("Select a major above to see its career paths.")` |
| 21 | NY Fed outcomes: CIP4 outside NY Fed 73 major categories | major_explorer.py : 916 | `st.info("Labor market outcomes are not available for this major…")` |
| 22 | NAICS distribution: no distribution data for this CIP | major_explorer.py : 997 | `st.info("Industry distribution is not available for this major…")` |
| 23 | Geographic: no employment or LQ rows for this CIP | major_explorer.py : 651 | `st.info("ℹ️ Geographic distribution data is not available for this major…")` |
| 24 | Geographic: total employment column all-null for this CIP | major_explorer.py : 682 | `st.info("No state employment data available for this major.")` |
| 25 | Geographic: LQ column all-null for this CIP | major_explorer.py : 711 | `st.info("No location quotient data available for this major.")` |
| 26 | Work environment: no O*NET data for this CIP | major_explorer.py : 539 | `st.info("ℹ️ Work environment data is not available for this major…")` |
| 27 | Work environment: pct_coverage NaN or all elements NaN | major_explorer.py : 553 | Same as #26 |
| 28 | Work environment: plot_df empty after filtering | major_explorer.py : 581 | Same as #26 |
| 29 | Major description: CIP not in authored YAML or FoS data | major_descriptions.py : 62 | `return None` — no render; section is silently skipped |
| 30 | Major description: stub (CIP in FoS but not authored) | major_explorer.py : 864 | `st.info("This major isn't yet covered by a detailed description in our library…")` |
| 31 | FYF: all 60 items not yet answered (submit blocked) | find_your_fit.py : 149 | `st.button(disabled=not is_complete)` — no error message, just grayed button |
| 32 | FYF: submitted but validate_responses finds errors | find_your_fit.py : 157 | `st.error(err)` for each error |
| 33 | FYF: RIASEC vector has zero variance (all same response) | find_your_fit.py : 249 | `st.warning("Your responses had no variation — every question got the same answer…")` |

---

## Section 8 — Cross-Tab Navigation

### Navigation buttons

| Button | Label | From tab | To tab | File : line |
|--------|-------|----------|--------|-------------|
| "See schools strong in this major →" | Major Explorer | School Finder | major_explorer.py : 1190 |
| "📌 Pin" (schools table) | Major Explorer | School Finder (pin visible) | major_explorer.py : 1340 |
| "Explore →" (top-10 RIASEC matches) | Find Your Fit | Major Explorer | find_your_fit.py : 276 |
| "Explore →" (programs offered) | School Finder pinned card | Major Explorer | app.py : 1817 |

**Note:** No button directly navigates the tab widget. `st.tabs()` cannot be programmatically switched in Streamlit. All cross-tab transitions require the user to manually click the target tab after seeing a success/info banner.

### Session state keys involved in cross-tab handoffs

| Key | Written by | Consumed by | Effect |
|-----|-----------|-------------|--------|
| `cip_filter_widget` | `set_school_finder_cip()` (school_finder.py 25) | School Finder sidebar CIP selectbox (app.py 510) | Pre-selects major filter in sidebar |
| `_last_xtab_cip_filter` | `set_school_finder_cip()` (school_finder.py 26) | `main()` School Finder tab block (app.py 2527) | Triggers one-shot cross-tab banner, then popped |
| `selected_cip` (= `SELECTED_CIP_KEY`) | `set_major_explorer_cip()` (major_explorer.py 322) | Major Explorer picker default index (major_explorer.py 1143) | Pre-selects major in Major Explorer picker |
| `_last_xtab_cip` | `set_major_explorer_cip()` (major_explorer.py 323) | FYF `_render_results()` (find_your_fit.py 257) | Triggers "Major Explorer is pre-loaded" banner, then popped |
| `_last_xtab_pinned` | `_pin_school_callback()` (major_explorer.py 309) | Major Explorer `render()` schools table block (major_explorer.py 1317) | Triggers "X is now pinned" success banner, then popped |
| `_active_tab` | All three set_*_cip helpers + FYF submit | `_write_session_state_to_url()` (app.py 386) + banner (app.py 2515) | Written to `?tab=` URL; triggers one-shot load banner |
| `_url_tab_banner` | `_parse_url_into_session_state()` (app.py 367) | `main()` before tab blocks (app.py 2515) | Shows "This URL is set up for the X tab" info banner, then popped |
| `pinned_schools` | `_pin_school_callback()` (major_explorer.py 306) | Pin selector widget (app.py 1153) + all detail card renders | Adds school to pin list |

### Focus management / scroll behavior

- **None exists.** No `st.rerun()` scroll-to-top behavior, no JavaScript focus management, no `st.empty()` scroll anchors.
- After clicking a cross-tab button, the user sees a banner on the current tab or must scroll up to see the banner on the target tab after switching.

---

## Section 9 — Test File Inventory

| File | Test count | Description |
|------|-----------|-------------|
| `tests/test_data_prep_majors.py` | 39 | Validates all pipeline outputs from `data_prep_majors.py`: CIP→SOC crosswalk, OEWS/EP merge into `occupations_master.csv`, `major_outcomes.csv` aggregation, `cip4_state_employment.csv` shape and LQ math, `cip4_work_context.csv` schema |
| `tests/test_scoring.py` | 27 | Unit tests for `scoring.py`: `compute_scores()`, `compute_sensitivity()`, `generate_explainer()`, CI computation, edge cases (all-NaN, zero weights, single school) |
| `tests/test_naics_data_prep.py` | **26 ⚠️** | See cohesion note below |
| `tests/test_major_explorer_alignment.py` | **21 ⚠️** | See cohesion note below |
| `tests/test_riasec_matching.py` | 17 | `compute_holland_code()` and `get_top_n_matches()` in `riasec_matching.py`: Pearson correlation, top-N shape, zero-variance vector behavior |
| `tests/test_url_state.py` | 16 | `url_state.py` encode/decode functions: `encode_tab`, `decode_tab`, `encode_riasec`, `decode_riasec`, round-trip correctness, invalid inputs |
| `tests/test_riasec_questionnaire.py` | 16 | `riasec_questionnaire.py`: `get_items()` count and structure, `get_response_scale()`, `score_responses()`, `validate_responses()` error conditions |
| `tests/test_utils.py` | 15 | `utils.py`: `haversine()` known distances and edge cases, `classify_acceptance()` Safety/Match/Reach/N/A classification logic |
| `tests/test_profiles.py` | 13 | `profiles.py`: `match_profile()` preset recognition, `get_preset_weights()` correct values, Custom profile detection |
| `tests/test_riasec_distribution.py` | 12 | `riasec_distribution.py`: `get_riasec_for_cip4()` known CIPs, zero-coverage CIPs, `get_all_cip4_vectors()` shape and coverage |
| `tests/test_data_prep_workcontext.py` | 12 | `work_context.csv` schema + `cip4_work_context.csv` schema, element column presence, value ranges, diagnostic columns |
| `tests/test_riasec_data_prep.py` | 10 | `cip4_riasec.csv`: schema, row count, score ranges, null coverage for Liberal Arts / Military Tech edge cases |
| `tests/test_data_prep_geo.py` | 10 | `colleges_cleaned.csv` geo enrichment: lat/lng presence for major schools, Carnegie label mapping, MSI flag derivation, religion label mapping |
| `tests/test_crosswalk.py` | 9 | `data/nyfed_crosswalk.yaml` and `data/processed/nyfed_outcomes.parquet`: CIP4 coverage, metric columns, no-duplicate constraint, source xlsx round-trip |
| `tests/test_major_descriptions.py` | 8 | `major_descriptions.py:get_description()`: authored entries return full dict, unknown CIP returns None, FoS-only CIP returns stub dict |
| `tests/test_find_your_fit_page.py` | 5 | FYF page module: `_render_results()` smoke test with mocked session state, URL-shared RIASEC vector decoding flow |

### Oversized files — cohesion analysis

#### `tests/test_naics_data_prep.py` (26 tests, 205 lines)

Three distinct sub-groupings, each with its own `scope="module"` fixture:

1. **`soc_to_naics3` fixture group** (lines 1–112, 8 tests): validates `data/cleaned/soc_to_naics3.csv` schema, shape, share-sum invariant, suppression-marker cleanup, and two spot-checks (Software Devs → NAICS 541, RNs → NAICS 622).
2. **`cip4_naics3_dist` fixture group** (lines 113–220, 9 tests): validates `data/cleaned/cip4_naics3_distribution.csv` schema, share-sum invariant, CIP4/NAICS3 format, spot-checks, routing-dilution observable, and Military Tech empty-state.
3. **Loader + utility group** (lines 221–273, 7 tests + 2 utility tests): validates `naics_distribution.get_naics_distribution()` behavior, `normalize_cip4()` utility with 3 format variants.

**Natural split lines:** → `test_soc_to_naics3.py` (group 1), `test_cip4_naics3_distribution.py` (group 2), `test_naics_loader.py` (group 3). The 2 `normalize_cip4` tests in group 3 could go into `test_utils.py`.

#### `tests/test_major_explorer_alignment.py` (21 tests, 200 lines)

Four distinct sub-groupings, covering four separate Phases and four separate functions/modules:

1. **Phase 12.3 — `_get_aligned_cip4_set()`** (lines 36–104, 6 tests): no-quiz-taken gate, shape when quiz taken, zero-variance case, caching, cache invalidation, dot-format contract.
2. **Phase 13.1 — `set_major_explorer_cip()`** (lines 111–130, 3 tests): session-state writes, no-dot format normalization, overwrite behavior.
3. **Phase 13.2 — `set_school_finder_cip()`, `initial_cip_filter_index()`, `apply_cip_filter()`** (lines 133–203, 8 tests): session-state writes, filter restricts to offering schools, stale-value fallback.
4. **Phase 13.3 — `get_school_all_programs()`** (lines 207–266, 4 tests): sort order, empty-school case, NaN-last sort, cip4 dot-format in output.

**Natural split lines:** → `test_riasec_alignment.py` (group 1), `test_major_explorer_xtab.py` (groups 2+3), `test_programs_offered.py` (group 4).
