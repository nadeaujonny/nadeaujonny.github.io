# PROJECT_STATUS.md — College Match Finder

**Last updated:** May 5, 2026 (Phase 7 in progress — Block 3 complete)
**Project:** College Match Finder (Streamlit app)
**Repo root:** local working copy at `C:\Users\nadea\OneDrive\Desktop\Data Analysis\college-match-finder\college-match-finder`
**Author:** Jonathan Nadeau
**Goal:** Polish → deploy to Streamlit Community Cloud → portfolio writeup.

---

## How to use this document

Single resume document for new chat sessions. Paste at the start of any session and Claude has full context on where the project stands and what comes next. Update after each focused multi-phase work session.

Authoritative planning docs:
- `College_Match_Finder_Project_Outline_V4.docx` — V4 (School Finder) scope
- `College_Match_Finder_Phase_8_Plus_Addendum.docx` — Major Explorer scope (Phases 8–14)
- **`PHASE_6_PLAN.md` — refreshed Phase 6 plan (drafted May 4, supersedes V4 §9 Phase 6 bullets)**
- **`PHASE_6_INVENTORY.md` — May 4 structural inventory (source of truth for Phase 6 scope)**

---

## Current State (one-paragraph summary)

**297 tests passing.** All planned features for both V4 (School Finder) and the Phase 8+ Addendum (Major Explorer) are shipped. Final code audit complete (May 4, 16 findings, 8 actioned, 5 deferred to Phase 6 polish, 3 deferred to Phase 7). **Phase 6 (Polish & Accessibility) is fully complete: 6A ✅ 6B ✅ 6C-1 ✅ 6C-2 ✅ 6D ✅ 6E ✅.** A cross-tab widget-state shadowing bug was found and fixed during 6E verification (both School Finder → and Find Your Fit → Major Explorer paths affected). Lighthouse Accessibility score: 86, zero automated failures. Next up: Phase 7 — Deployment & Documentation. Realistic estimate to live deployment + writeup: 2 focused sessions remaining.

---

---

## Overall Phase Progress

| Phase | Description | Status |
|---|---|---|
| **V4 Phase 1** | Data Acquisition & Prep | ✅ Complete |
| **V4 Phase 2** | Scoring Engine (school-side) | ✅ Complete |
| **V4 Phase 3** | Core Streamlit App | ✅ Complete |
| **V4 Phase 4.1** | Multiselect pin widget | ✅ Complete |
| **V4 Phase 4.2** | Acceptance likelihood badges | ✅ Complete |
| **V4 Phase 4.3** | (V3 scope cut applied) | ✅ N/A |
| **V4 Phase 4.4** | Income-bracket net price selector | ✅ Complete |
| **V4 Phase 4.5** | Field-of-study data in school detail cards | ✅ Complete |
| **V4 Stat Depth A** | Demographics, outcomes, mobility, filters | ✅ Complete |
| **V4 Stat Depth B** | Repayment rate as 7th school scoring dimension | ✅ Complete |
| **V4 Stat Depth C** | Confidence intervals on match scores | ✅ Complete |
| **V4 Stat Depth D** | Sensitivity analysis on pinned schools | ✅ Complete |
| **V4 Stat Depth E** | Preset profiles for first-time users | ✅ Complete |
| **V4 Stat Depth F** | URL state for shareable rankings | ✅ Complete |
| **Addendum Phase 8** | Major Picker + Field-of-Study Detail | ✅ Complete |
| **Addendum Phase 8.5** | Cross-tab pin (school name → School Finder detail card) | ✅ Complete |
| **Addendum Phase 9** | BLS Occupational Layer | ✅ Complete |
| **Addendum Phase 10** | Geographic and Work Context | ✅ Complete |
| **Addendum Phase 11.1A/B/C** | Major descriptions infrastructure + 60 hand-authored + long-tail stubs | ✅ Complete |
| **Addendum Phase 11.2A/B** | NY Fed crosswalk + outcomes panel | ✅ Complete |
| **Addendum Phase 11.3.1/2/3** | BLS NAICS-by-SOC industry distribution | ✅ Complete |
| **Addendum Phase 12.1–12.3** | RIASEC questionnaire + matching + Find Your Fit page + Major Explorer alignment | ✅ Complete |
| **Addendum Phase 13.1–13.4b** | Cross-surface integration (5 sub-phases) | ✅ Complete |
| **Addendum Phase 14** | Polish + redeploy | ⬜ Folded into V4 Phase 6 |
| **V4 Phase 5** | Comparison mode, CSV/PDF export, Map | ✅ Complete |
| **Final Code Audit** | Comprehensive review pass + 2 cleanup batches | ✅ Complete |
| **V4 Phase 6A** | Audit cleanup (sentinels doc, button-key helper, test file split) | ✅ Complete (May 4) |
| **V4 Phase 6B** | Color palette consolidation | ✅ Complete (May 4) |
| **V4 Phase 6C-1** | Chart & content accessibility (captions, ARIA, contrast tests) | ✅ Complete (May 4) — pending visual smoke test |
| **V4 Phase 6C-2** | Interactive accessibility (keyboard nav, button labels, badge text fallbacks) | ✅ Complete (May 5, 2026) |
| **V4 Phase 6D** | Transparency surface (About the Data expansion, freshness badge) | ✅ Complete (May 5, 2026) |
| **V4 Phase 6E** | Mobile + Dark Mode + Lighthouse | ✅ Complete (May 5, 2026) |
| **V4 Phase 7 — Block 1** | Repo cleanup, monorepo integration, requirements pinned | ✅ Complete (May 5, 2026) |
| **V4 Phase 7 — Block 2** | Streamlit Cloud deployment — live at nadeaujonnycollegematchfinder.streamlit.app | ✅ Complete (May 5, 2026) |
| **V4 Phase 7 — Block 3** | README authoring (Option C scope, LICENSE, screenshots) | ✅ Complete (May 5, 2026) |
| **V4 Phase 7 — Block 4** | index.md (portfolio page, Jekyll, non-technical audience) | ⬜ **NEXT** |
| **V4 Phase 7 — Block 5** | Phase 7 close-out, PROJECT_STATUS.md final update | ⬜ Outstanding |
| **Phase 7.5** | Master Project Narrative (docs/PROJECT_NARRATIVE.md) | ⬜ Outstanding |
| **Portfolio writeup** | Public consolidation linked from nadeaujonny.github.io | ⬜ Outstanding |

---

## Test Suite Status

**297 tests passing** as of May 5, 2026 (post-6E — Phase 6 complete).

### Test count progression through Phase 6

| Sub-session | Δ | Running total | What changed |
|---|---|---|---|
| Pre-Phase 6 baseline | — | 256 | Audit Batch 2 close |
| 6A | +3 | 259 | `make_button_key` helper unit tests |
| 6B | +3 | 262 | PALETTE regression guards (key presence, demo/mobility collision, demo uniqueness) |
| 6C-1 | +27 | 289 | 4 contrast helper unit tests + 21 parametrized PALETTE contrast tests + 2 standalone (comparison, coverage) |
| 6C-2 | +4 | 293 | 4 parametrized badge regression tests (`format_acceptance_badge` — safety/match/reach/unknown) |
| 6D | +4 | 297 | 4 structural invariant tests in `tests/test_about_the_data.py` (all-12-sources, source-count-exactly-12, constants-non-empty, no-duplication-in-app-py) |
| 6E | 0 net (−1 +1) | 297 | `empty_text` PALETTE contrast test retired (key removed); cross-tab widget-state shadowing regression test added (`test_set_major_explorer_cip_clears_picker_widget_state`) |

### Authoritative breakdown

Run `pytest --collect-only -q` for the authoritative breakdown by file. Updated table after 6A and 6C-1 file work:

| File | Approx. tests | Notes |
|---|---|---|
| `test_data_prep_majors.py` | 39 | Phase 8/9/10 majors data prep |
| `test_scoring.py` | 27 | V4 school-side scoring engine + sensitivity |
| `tests/test_utils.py` | ~26 | Original 15 + 3 `make_button_key` (6A) + 3 `normalize_cip4` (relocated 6A) + 4 contrast helpers (6C-1) + 4 badge regression tests (6C-2) |
| `tests/test_riasec_matching.py` | 17 | Phase 12.2b |
| `tests/test_url_state.py` | 16 | Phase 13.4a + 13.4b |
| `tests/test_riasec_questionnaire.py` | 16 | Phase 12.2a |
| `tests/test_profiles.py` | 13 | Stat Depth E pure-function helpers |
| `tests/test_riasec_distribution.py` | 12 | Phase 12.1d |
| `tests/test_data_prep_workcontext.py` | 12 | Phase 10 work context |
| `tests/test_major_explorer_xtab.py` | 12 | 6A split (Phase 13.1+13.2 combined); +1 widget-state regression test (6E) |
| `tests/test_cip4_naics3_distribution.py` | 10 | 6A split (Phase 11.3.2) |
| `tests/test_riasec_data_prep.py` | 10 | Phase 12.1 |
| `tests/test_data_prep_geo.py` | 10 | Phase 10 geographic data prep |
| `tests/test_soc_to_naics3.py` | 9 | 6A split (Phase 11.3.1) |
| `tests/test_crosswalk.py` | 9 | Phase 11.2A + 11.2B |
| `tests/test_major_descriptions.py` | 8 | Phase 11.1A + 11.1C combined |
| `tests/test_riasec_alignment.py` | 6 | 6A split (Phase 12.3) |
| `tests/test_find_your_fit_page.py` | 5 | Phase 12.2c |
| `tests/test_naics_loader.py` | 4 | 6A split (Phase 11.3.3 loader portion) |
| `tests/test_programs_offered.py` | 4 | 6A split (Phase 13.3) |
| `tests/test_config.py` | ~29 | 3 from 6B + ~26 contrast tests from 6C-1 |
| `tests/test_about_the_data.py` | 4 | Phase 6D structural invariant tests (new file) |
| **Total** | **~297** | |

When in doubt, run `pytest --collect-only -q`. Total count is what matters. Both `pytest` and `pytest tests/` invocations report the same total (test discovery drift was resolved in audit Batch 1).

---

## What Phase 7 produced (so far)

### Block 3 — README, LICENSE, Screenshots (May 5, 2026)

README authored at Option C scope (~90 lines): live URL, features, "Why this project" framing, Highlights section with specific technical depth (test count, WCAG AA, cross-tab bug catch), tech stack, data sources redirect, quick-start, annotated project structure tree. LICENSE: MIT, Copyright 2026 Jonathan Nadeau. 3 screenshots from the live deployed app embedded in `assets/` folder (`hero.png`, `major-explorer.png`, `find-your-fit.png`). Portfolio page link stubbed with HTML comment — to be uncommented after Block 4 (index.md) ships.

### Block 2 — Deployment (May 5, 2026)

Live at **https://nadeaujonnycollegematchfinder.streamlit.app**. Deployed from `nadeaujonny/nadeaujonny.github.io` monorepo, main file path `projects/college-match-finder/app.py`. Two deployment bugs found and fixed post-deploy: (1) `major_explorer.py` used bare `Path("data/...")` strings that resolved to repo root on Cloud — refactored to `config.DATA_CLEANED_DIR`; (2) `riasec_items.yaml` was in `data/raw/` (gitignored) — moved to `data/`. Both fixed in a single commit, auto-redeployed. All smoke tests passed.

### Block 1 — Repo cleanup & monorepo integration (May 5, 2026)

Architecture pivot from standalone repo to monorepo under `nadeaujonny.github.io/projects/college-match-finder/`. `requirements.txt` pinned to exact versions; pytest removed from production deps; `pillow` added. `data/processed/top_60_cip4.csv` culled (zero runtime references). Initial commit: 74 files, 189,970 insertions.

---

## What Phase 6 produced

### 6E — Mobile, Dark Mode, Lighthouse (May 5, 2026)

**Mobile verified at phone viewport (375 × 812)** across all three tabs. Sidebar hamburger overlay, ranked cards, acceptance badges, pinned detail panel, comparison expander reflow, map, RIASEC questionnaire, and `st.dataframe` horizontal scroll all render correctly at narrow width. No app-fixable mobile issues found. Tablet (768 × 1024) considered covered by phone verification — Streamlit reflow only adds flexibility at wider viewports.

**Dark mode documented as accepted limitation.** The hardcoded `[theme]` block in `.streamlit/config.toml` (`base = "light"` + four explicit hex overrides) is the intended default. Full dark-mode parity would require removing the hardcoded theme or building a parallel color system — neither justified for a portfolio app. The one custom HTML element (Earnings Mobility empty state) was migrated from hardcoded `#f0f0f0` / `#888` to `var(--secondary-background-color, #f0f0f0)` / `var(--text-color, #555)` so it adapts if the user overrides the theme at the browser level.

**`empty_bg` / `empty_text` PALETTE keys retired.** The two keys were the only consumers of the hardcoded hex values in the Earnings Mobility element. Keys removed from `config.py`, the coverage test (`test_palette_coverage_complete`), the contrast-test pairing (`_TOKEN_BACKGROUNDS`), and `_EXCLUDED_TOKENS`. One parametrized test retired (−1), one regression test added (+1), net count 297.

**Lighthouse baseline captured:** Performance 12 (framework ceiling, accepted), Accessibility 86 (zero automated failures — 14-point gap is manual-check territory), Best Practices 81, SEO 82.

**Cross-tab widget-state shadowing bug found and fixed.** `set_major_explorer_cip()` wrote `session_state["selected_cip"]` but did not clear `session_state["major_picker_widget"]`. Streamlit's keyed-widget behavior ignores the programmatic `index` parameter when a prior value is persisted under the widget key — so clicking `Explore →` updated the within-card display correctly but left the Major Explorer picker stuck on its prior value. Fix: add `st.session_state.pop("major_picker_widget", None)` to `set_major_explorer_cip()`. Both affected paths (School Finder → and Find Your Fit →) now pre-select correctly. Regression test added to `tests/test_major_explorer_xtab.py`.

### 6D — Transparency Surface (May 5, 2026)

**All 12 data sources documented in a single `render_about_the_data()` helper** in `page_modules/about_the_data.py`. Sources are grouped into 5 subheadings (Schools / Majors / Careers / Geography / Interests) with a 4-line provenance block per source (name, snapshot date, source URL, methodology one-liner). A 6th subheading — Methodology & limitations — ports the existing BLS/O\*NET methodology prose verbatim (aggregation method, weighting rationale with Computer Science worked example, 4-bullet limitations list, state-level geographic distribution paragraph, work environment paragraph, and full USDOL/ETA CC BY 4.0 attribution).

**Expander rendered on all 3 tabs** via a single call to `render_about_the_data()` at the footer of each tab. School Finder's old inline expander (covering only 5 sources with verbose prose scattered in app.py) was replaced. Major Explorer and Find Your Fit each received the call at the end of their `render()` functions. No markdown duplication across files — one source of truth.

**Freshness caption rendered above the expander on all 3 tabs:** `"Data through May 2024, with some sources updated as recently as February 2026. See About the Data for per-source dates."` `OLDEST_DATE` and `NEWEST_DATE` are module-level constants in `about_the_data.py`.

**`page_modules/about_the_data.py` is the correct home** (not `utils.py`) because: (1) function imports `streamlit`; `utils.py` has no `st` dependency and is imported by non-Streamlit test code; (2) content is ~170 lines with methodology section, over the 120-line extraction threshold.

**4 new tests in `tests/test_about_the_data.py`:** all-12-sources present, source-count-exactly-12 regression guard, constants-defined-and-non-empty, old-expander-not-in-app-py duplication guard.

**Smoke-test items deferred to 6E** (rendering verification requires the browser): O\*NET `O\\*NET` backslash-escape rendering (should display as `O*NET`, not `O\*NET`); `│` box-drawing separator rendering (fallback: em-dash). These are flagged in the 6E What's Next note above.

### 6A — Audit Cleanup (May 4)

**Three deferred audit register items closed:**

- **Sentinel naming** — Option A documented. New file `docs/SESSION_STATE.md` catalogs all 5 cross-tab event sentinels (`_last_xtab_pinned`, `_last_xtab_cip`, `_last_xtab_cip_filter`, `_url_tab_banner`, `_active_tab`) with writer file:line, consumer file:line, lifecycle (one-shot pop vs. persistent), and signal description. No code change.
- **Button-key helper** — `make_button_key(prefix, *parts)` added to `utils.py`. Refactored 4 dynamic button `key=` call sites in `major_explorer.py` (2 sites), `find_your_fit.py`, and `app.py`. Slider/chart dynamic keys (5 instances) intentionally left as-is — the helper is button-only. 3 new unit tests in `test_utils.py`.
- **Test file split** — `tests/test_naics_data_prep.py` (26 tests) → `test_soc_to_naics3.py` (9), `test_cip4_naics3_distribution.py` (10), `test_naics_loader.py` (4); 3 `normalize_cip4` tests relocated to `test_utils.py`. `tests/test_major_explorer_alignment.py` (21 tests) → `test_riasec_alignment.py` (6), `test_major_explorer_xtab.py` (11, groups 2+3 combined), `test_programs_offered.py` (4). Both originals deleted.

**Smoke test passed.** No followups.

### 6B — Color Palette Consolidation (May 4)

**`PALETTE` dict added to `config.py`** with 35+ tokens (initially 31 from plan; 3 added in Step 0 for unlisted literals: `ci_label_text`, `naics_chart_bg`, `gridline_light`; 4 token rename from `map_*` to `choropleth_*` for accuracy). Inline WCAG verification notes above mobility and `demo_white` tokens.

**Consumers refactored** in `app.py`, `major_explorer.py`, `find_your_fit.py`. Module-level constants deleted (`_DEMO_COLORS`, `_BAR_COLOR`, `_OTHER_BAR_COLOR`, `PDF_CARD_BG`, `PDF_CARD_BORDER`, `PDF_ACCEPTANCE_COLORS`). All consumers read directly from `PALETTE`.

**3 deliberate visual changes shipped:**

1. Race/ethnicity "White" segment: sky blue → ochre `#9A7D0A` (resolves collision with Men/Other)
2. Earnings Mobility bars: blue/orange/green → purple `#7B3294` / amethyst `#9B59B6` / emerald `#1E8449` (resolves collisions with race/eth bars; dark→light = low→high preserved)
3. NAICS distribution + RIASEC profile bars: default Plotly blue `#1f77b4` → Wong primary `#0072B2` (consistency with rest of palette)

**WCAG AA contrast verified** on the 3 mobility hexes and `demo_white` against white background. Initial proposals (`#C2A5CF`, `#A6DBA0`, `#F0E442`) failed and were replaced.

**3 regression-guard tests in `test_config.py`:** key presence, demo/mobility hex collisions, demo internal uniqueness.

### 6C-2 — Interactive Element Accessibility (May 5, 2026)

**Step 0 inspection found the inventory overcounted both work items.** Acceptance badges at `app.py:1870` and `app.py:2316` already paired emoji + text. Only 3 `Explore →` buttons existed (not ~35+), and 1 of the 3 was already fully disambiguated. No production badge code changed; a `format_acceptance_badge` helper was extracted from the inline pattern and both call sites were updated to use it.

**`format_acceptance_badge(label)` helper added to `utils.py`.** Returns `"EMOJI label"` for a given acceptance label. `ACCEPTANCE_BADGE_EMOJI` dict moved from `app.py` to `utils.py` to live beside `classify_acceptance`. Both web render sites (`render_detail_card` and `_build_comparison_table`) now call the helper rather than assembling the string inline.

**2 `Explore →` buttons disambiguated** with `help=` tooltip (tooltip-only approach). Label disambiguation was ruled out because 228 of 393 major names exceed 30 chars (max 116 chars). Buttons at `app.py:1807` (school detail card → Major Explorer) and `find_your_fit.py:281` (RIASEC results → Major Explorer) now carry `help=f"Explore the {major_name} major in Major Explorer"`.

**`docs/ACCESSIBILITY.md` created.** Three sections: Streamlit framework limitations (7 accepted limitations with AT impact notes), accessibility features by tab, and what's tested (26 contrast tests + 4 badge regression tests with rationale).

**+4 tests:** 4 parametrized badge regression tests in `tests/test_utils.py` covering all 4 acceptance categories (safety/match/reach/unknown).

### 6C-1 — Chart & Content Accessibility (May 4)

**Concern 1 — Chart captions.** All 11 charts have screen-reader-accessible captions. 5 already had adequate captions (#1 Map, #4 Mobility, #6 Comparison, #7 Work Environment, #9 LQ Choropleth). Captions added below: #2 Radar, #3 Demographics, #8 Employment Choropleth, #11 RIASEC. Borderline captions expanded with structural prefixes: #5 CI bar (added "Confidence interval band showing..." prefix), #10 NAICS (added "Top 10 industries (3-digit NAICS) employing workers..." prefix).

**Concern 2 — Custom HTML accessibility.** Earnings Mobility empty-state `<div>` at `app.py:1575` got `role='status'` (Option A — preserves the deliberate gray-box design). No visual change to sighted users; screen readers now announce the message. Was the only `unsafe_allow_html=True` block in the entire codebase (Step 0 verified).

**Concern 3 — Color contrast verification.** Two new helpers in `utils.py`: `relative_luminance(hex)` and `contrast_ratio(hex_a, hex_b)` — pure WCAG 2.1 §1.4.3 math, no dependencies. 4 unit tests. Then 21 parametrized contrast assertions in `test_config.py` covering every chart-color hex against its rendering background, plus 2 standalone tests (comparison palette passing entries, coverage check that ensures no PALETTE key is silently untested).

**Quartile color replacements (Set 1):** 3 of 4 quartile hexes failed the 3:1 floor and were replaced with darker blues that pass while preserving the dark→light = top→bottom gradient ordering:
- `quartile_above_avg`: `#7da7e8` (2.45:1) → `#2f7dc5` (4.32:1)
- `quartile_below_avg`: `#cbd5e1` (1.48:1) → `#4a8cca` (3.56:1)
- `quartile_bottom`: `#94a3b8` (2.56:1) → `#5596cd` (3.17:1)
- `quartile_top`: `#2563eb` unchanged (already 5.17:1)

Even luminance steps (~0.04 between each) for a uniform perceptual gradient.

**Wong-derived tokens excluded from contrast tests with documented reasoning** (8 tokens): `wong_orange`, `wong_sky`, `wong_yellow`, `wong_gray`, `demo_men_other`, `demo_hispanic`, `demo_other`, `categorical_other`. Reason: Wong (2011) palette mid-tones are optimized for colorblind distinguishability, not luminance contrast against white. Replacing them with darker variants would re-introduce colorblindness ambiguity. Trade-off explicitly documented in `EXCLUDED_TOKENS` dict with each token's measured contrast ratio. **This is the most important documented decision in 6C-1** — it acknowledges that the Wong palette has a different design goal than WCAG and we're respecting that intentionally.

---

## What's Next — Phase 7: Deployment & Documentation

Phase 6 is fully closed. Phase 7 is the next session.

### Phase 7 scope (one session)

- **Streamlit Community Cloud deploy** — connect GitHub repo, configure secrets (if any), confirm the app loads on the cloud URL. Streamlit Community Cloud is free-tier for public repos; the main step is connecting the account and authorizing the repo.
- **README authoring** — project description, screenshots of all three tabs, architecture diagram (data sources → processing → Streamlit tabs), how-to-run instructions for local use.
- **Repo cleanup** — audit `.gitignore` (ensure `__pycache__/`, `.venv/`, any `.pkl` build artifacts, and local data CSVs are excluded or documented as build artifacts); confirm cleaned data files commit cleanly or are documented.
- **Portfolio link** — add a project card on `nadeaujonny.github.io` pointing to the live Streamlit URL and the GitHub repo.

### After Phase 7

- **Portfolio writeup** (~1 session): All-in-one consolidation linked from portfolio site — architecture decisions, methodology, what was built and why.

**Total outstanding effort estimate: 2 focused sessions to live deployment + writeup.**

---

## Workflow Reminders

- **One Claude Code session per sub-session.** Fresh window for 6C-2, 6D, 6E. Within a sub-session, stay in the same window through Step 0 → approval → edits → tests → smoke test.
- **Max effort** for all Phase 6 sub-sessions. Surface area is broad and regression risk on visual/accessibility work is silent (no tests fail when colors render wrong).
- **Per-edit diff approval enabled.**
- **Step 0 inspection is non-negotiable.** The stop-and-confirm methodology has now caught real spec errors in 13 consecutive phases (9 prior + 6A + 6B + 6C-1 + 6C-2). Every Step 0 has surfaced something the planning didn't fully anticipate. Skipping it is rework debt.
- **Smoke test in Streamlit before declaring a sub-session done.** Tests don't catch visual regressions. The 6C-1 smoke test is currently the one outstanding manual verification item.

---

## Architectural Decisions Worth Remembering — Phase 6 additions

(Earlier decisions from Phases 1–13 + audit batches 1 and 2 are preserved in prior status doc revisions.)

### 6E — Dark mode and Lighthouse Performance ceiling accepted

- **Hardcoded light theme is the intended default; dark-mode parity not pursued.** The `[theme]` block in `.streamlit/config.toml` pins the app to a custom light palette. Achieving full dark-mode parity would require either removing the hardcoded theme (changing the visual identity) or maintaining a parallel dark-mode color system. For a single-user-theme portfolio app, neither is justified. The one `unsafe_allow_html` element was migrated to CSS variables so it adapts if the user overrides the theme at the browser level. Documented in `docs/ACCESSIBILITY.md`.
- **Lighthouse Performance ceiling of ~12 is a known Streamlit framework property.** Streamlit's Python→WebSocket architecture and large frontend bundle produce low Performance scores on the Lighthouse Mobile preset. Accepted without remediation.
- **Cross-tab widget-state shadowing: `pop` the widget key in the callback, not in the renderer.** When a Streamlit `st.selectbox` has a `key=` and a prior value is persisted under that key, the `index` parameter is silently ignored on re-render. The fix belongs in the `on_click` callback (`set_major_explorer_cip`) — clearing the widget key there ensures the picker initializes from the programmatic index on the very next render, without requiring coordination in `render()`. Pattern applies to any keyed widget that needs to be programmatically reset by a cross-component event.

### 6D — About the Data location

- **`page_modules/about_the_data.py` over `utils.py`** for `render_about_the_data()`. `utils.py` has no `streamlit` import and is imported by test code that runs without a Streamlit session; adding `st` there would be a layering regression. Content is also ~170 lines with the methodology section, above the 120-line threshold for extraction.
- **Footer on every tab (not sidebar, not single tab).** Portfolio reviewers can land on any tab; sidebar collapses on mobile; footer matches data-journalism convention. One call to `render_about_the_data()` at the end of each tab's render function — no markdown duplication.
- **Oldest-date framing for the freshness caption.** "Data through May 2024, with some sources updated as recently as February 2026" — the 21-month gap between oldest (BLS OEWS) and newest (O\*NET 30.2 + NY Fed) makes the "as recently as" phrasing informative rather than contradictory.
- **Methodology & limitations as 6th subheading, not deleted.** The existing expander had detailed methodology prose (weighting rationale, CS worked example, 4-bullet limitations, state/work-env panel notes) that a portfolio reviewer would want. Rather than dropping it for the 4-line-per-source format, both were kept: the 4-line blocks give provenance per source; the 6th section gives reasoning behind aggregation choices.

### 6A — Sentinel naming

- **Documentation over consolidation.** Five cross-tab sentinels with distinct triggers and consumers were documented in `docs/SESSION_STATE.md` rather than consolidated into a single `_xtab_event` dispatch dict. The audit register's "consider whether to consolidate" framing made documentation the lower-risk close.

### 6A — Button-key helper

- **`make_button_key(prefix, *parts)` for dynamic keys only.** Slider and chart `key=f"..."` patterns intentionally not refactored — sliders need stable keys for state persistence; chart keys serve a different purpose than collision avoidance.

### 6B — Centralized PALETTE

- **`config.PALETTE` is the single canonical source for every color decision.** No inline hex literals remain in `app.py`, `major_explorer.py`, or `find_your_fit.py`. Module-level color constants deleted (`_DEMO_COLORS`, `_BAR_COLOR`, etc.) — direct `PALETTE` reads preferred over thin pass-through layers.
- **Token rename: `map_land`/`map_borders` → `choropleth_land`/`choropleth_borders`.** The Step 0 inspection caught that these colors actually live in the choropleth layout in `major_explorer.py`, not the School Finder scattermapbox. Misnaming would have confused future palette work.
- **Mobility palette deliberately broken away from Wong primary tokens.** Purple `#7B3294` / amethyst `#9B59B6` / emerald `#1E8449` are not in the Wong family — chosen specifically to avoid hex collisions with demographics tokens (the original `#0072B2` / `#E69F00` / `#009E73` mobility colors collided with Black/Hispanic/Asian race/eth tokens). Trade-off accepted: mobility loses Wong's colorblindness optimization but gains screen-reader unambiguity.

### 6C-2 — Button disambiguation

- **Tooltip-only (`help=`) over label-in-button.** 58% of major names exceed 30 chars (max 116); embedding names in button labels would produce unwieldy text. `help=` tooltips provide the same disambiguation for AT users without degrading the visual layout.
- **`format_acceptance_badge` extracted to `utils.py`.** The inline `f"{emoji} {label}"` pattern at two call sites was the only factoring available before this session. Extracting it to a helper makes the "always include both" contract testable and locates badge-rendering logic beside `classify_acceptance` where it belongs.
- **Step 0 methodology continues to catch real spec errors.** The inventory overcounted both work items in 6C-2. The stop-and-confirm step caught this in 13 consecutive phases (9 prior + 6A + 6B + 6C-1 + 6C-2).

### 6C-1 — Wong palette and WCAG

- **Two design goals can conflict and must be acknowledged.** Wong (2011) was designed for colorblind distinguishability; WCAG 1.4.11 is about luminance contrast against background. 8 Wong-derived PALETTE tokens fail WCAG AA non-text 3:1 against white. Replacing them with darker variants would re-introduce colorblindness ambiguity. The hybrid resolution: replace where there's no design trade-off (quartile colors — pure lightness gradient, no colorblind constraint), exclude with documentation where the trade-off is real (Wong primaries and demo derivatives).
- **`EXCLUDED_TOKENS` dict in `test_config.py` records each excluded token with reason and measured contrast ratio.** Future palette additions are caught by `test_palette_coverage_complete` — every key must be either tested or explicitly excluded.

---

## Key Files Modified in Phase 6

| File | What changed |
|---|---|
| `config.py` | Added `PALETTE` dict (~35 tokens) at end of file |
| `utils.py` | Added `make_button_key()` (6A), `relative_luminance()` and `contrast_ratio()` (6C-1), `ACCEPTANCE_BADGE_EMOJI` dict + `format_acceptance_badge()` moved from `app.py` (6C-2) |
| `app.py` | Deleted module-level color constants; refactored all color literals to `PALETTE`; added captions below 2 charts; expanded CI bar caption; added `role='status'` to mobility empty-state HTML (6C-1); removed local `ACCEPTANCE_BADGE_EMOJI`, updated badge render sites to use `format_acceptance_badge`, added `help=` to `explore_program` button (6C-2); replaced old School Finder expander with `about_the_data.render_about_the_data()` + freshness caption; added `from page_modules import about_the_data` import (6D) |
| `page_modules/major_explorer.py` | Refactored color literals to `PALETTE`; added caption below employment choropleth; replaced source-only NAICS caption with content + source (6B/6C-1); added freshness caption + `render_about_the_data()` at end of `render()` (6D) |
| `page_modules/find_your_fit.py` | Refactored RIASEC profile color to `PALETTE`; added caption below RIASEC chart (6C-1); added `help=` to `explore_riasec` button (6C-2); added freshness caption + `render_about_the_data()` at end of `render()` (6D) |
| `page_modules/about_the_data.py` | New file (6D): `OLDEST_DATE`/`NEWEST_DATE` constants + `render_about_the_data()` — 12-source expander with 5 provenance categories + Methodology & limitations section |
| `tests/test_about_the_data.py` | New file (6D): 4 structural invariant tests |
| `docs/ACCESSIBILITY.md` | Added "Data provenance (all tabs)" section (6D); dark mode limitation, mobile responsiveness, Lighthouse baseline, Phase 6 close-out sections (6E) |
| `page_modules/major_explorer.py` | Added `st.session_state.pop("major_picker_widget", None)` to `set_major_explorer_cip()` — fixes cross-tab picker pre-selection bug (6E) |
| `app.py` | Earnings Mobility empty-state HTML migrated from hardcoded hex to CSS variables (6E) |
| `config.py` | Removed `empty_bg` / `empty_text` PALETTE keys (6E) |
| `tests/test_major_explorer_xtab.py` | +1 regression test: `test_set_major_explorer_cip_clears_picker_widget_state` (6E) |
| `tests/test_config.py` | Removed `empty_text` contrast-test pairing, `empty_bg` EXCLUDED_TOKENS entry, and dead `if bg == "empty_bg"` branch (6E) |
| `tests/test_utils.py` | +3 `make_button_key` tests, +3 `normalize_cip4` tests (relocated), +4 contrast helper tests (6C-1), +4 badge regression tests (6C-2) = ~26 total |
| `tests/test_config.py` | +3 PALETTE regression guards (6B), +26 contrast tests (6C-1) = ~29 total |
| `docs/ACCESSIBILITY.md` | NEW (6C-2) — framework limitations, per-tab features, what's tested |
| `tests/test_naics_data_prep.py` | DELETED (split in 6A) |
| `tests/test_major_explorer_alignment.py` | DELETED (split in 6A) |
| `tests/test_soc_to_naics3.py` | NEW (6A split) |
| `tests/test_cip4_naics3_distribution.py` | NEW (6A split) |
| `tests/test_naics_loader.py` | NEW (6A split) |
| `tests/test_riasec_alignment.py` | NEW (6A split) |
| `tests/test_major_explorer_xtab.py` | NEW (6A split) |
| `tests/test_programs_offered.py` | NEW (6A split) |
| `docs/SESSION_STATE.md` | NEW (6A) — sentinel reference doc |

---

## Files in Project Knowledge

Keep:
- `College_Match_Finder_Project_Outline_V4.docx` — V4 planning document
- `College_Match_Finder_Phase_8_Plus_Addendum.docx` — Phase 8+ planning document
- `PROJECT_STATUS.md` — this file (single resume doc for new sessions)
- `PHASE_6_PLAN.md` — refreshed Phase 6 plan
- `PHASE_6_INVENTORY.md` — May 4 structural inventory
- `College_Match_App_Plan_After_Finishing` — short post-completion note (consolidate outlines into one master, then write up)

---

## Tomorrow's First Action

1. **Run smoke test for 6C-1** (see "Pending pickup item" section above) — `streamlit run app.py`, verify the 5 checklist items, flag anything off.
2. **If smoke test clean: ask Claude for the 6C-2 instruction file.** I (Claude) will draft `Phase_6C_2_Instructions.md` against the post-6C-1 state, sized for one fresh Claude Code window with the same Step 0 / approval / edits / smoke test pattern.
3. **If smoke test reveals issues: report findings before drafting 6C-2.** Issues from 6C-1 take priority over starting new work.

---

*End of PROJECT_STATUS.md — 289 tests passing. Phase 6 in progress: 6A ✅ 6B ✅ 6C-1 ✅. Next up: 6C-1 visual smoke test (manual) → 6C-2 (interactive accessibility) → 6D (transparency) → 6E (mobile/dark/Lighthouse) → Phase 7 (deploy) → portfolio writeup. ~4 focused sessions remaining.*
