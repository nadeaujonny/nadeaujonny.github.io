# Final Code Audit — Punch List

**Date:** May 4, 2026  
**Auditor:** Claude Code  
**Baseline:** 256 tests collected by `pytest --collect-only -q`; 248 pass when running `pytest tests/` only.

---

## Critical

### A5: Test count discrepancy — `test_major_descriptions.py` lives at the repo root, not in `tests/`

**Location:** `test_major_descriptions.py` (repo root, not `tests/test_major_descriptions.py`)

**Current state:** `pytest --collect-only -q` (no args) collects **256** tests — the 8 tests in `test_major_descriptions.py` at the root are included. But `pytest tests/` (the canonical command listed in PROJECT_STATUS.md's "256 tests passing" claim) collects only **248**. The PROJECT_STATUS.md breakdown table lists `tests/test_major_descriptions.py` under the `tests/` path, but the file does not exist there. `test_major_descriptions.py` at the root is collected by the default pytest discovery but silently excluded by `pytest tests/`. This is the exact 8-test gap the status doc flagged as an open audit item.

**Per-file count (authoritative — from `pytest --collect-only -q`):**
| File | Count |
|---|---|
| `test_major_descriptions.py` (root) | 8 |
| `tests/test_crosswalk.py` | 9 |
| `tests/test_data_prep_geo.py` | 10 |
| `tests/test_data_prep_majors.py` | 39 |
| `tests/test_data_prep_workcontext.py` | 12 |
| `tests/test_find_your_fit_page.py` | 5 |
| `tests/test_major_explorer_alignment.py` | 21 |
| `tests/test_naics_data_prep.py` | 26 |
| `tests/test_profiles.py` | 13 |
| `tests/test_riasec_data_prep.py` | 10 |
| `tests/test_riasec_distribution.py` | 12 |
| `tests/test_riasec_matching.py` | 17 |
| `tests/test_riasec_questionnaire.py` | 16 |
| `tests/test_scoring.py` | 27 |
| `tests/test_url_state.py` | 16 |
| `tests/test_utils.py` | 15 |
| **Total** | **256** |

All 248 tests inside `tests/` pass. The 8 root-level tests also pass when collected.

**Recommended fix:** Move `test_major_descriptions.py` into `tests/` so `pytest tests/` and `pytest` (no args) produce the same count. Update PROJECT_STATUS.md to show the correct path.

**Effort:** XS  
**Risk:** Low (no behavior change; fixes misleading dual-count situation)

---

## High-Value Cleanup

### A1: CIP-format helper trio — two nearly-identical formatters plus inline inverse

**Location:**
- `page_modules/major_explorer.py:179` — `_format_cip_code(cip: int) -> str`
- `page_modules/major_explorer.py:194` — `_cip_int_to_cip4_str(cip_int: int) -> str`
- `page_modules/major_explorer.py:351` — inline `int(cip4_str.replace(".", ""))`
- `page_modules/school_finder.py:15` — `_normalize_cip4(cip4_str: str) -> str` (separate, inverse)
- `page_modules/school_finder.py:75` — inline `int(cip_filter.replace(".", ""))`

**Current state:** `_format_cip_code` and `_cip_int_to_cip4_str` are functionally identical: both pad an int to 4 digits and insert a dot. The only difference is that `_cip_int_to_cip4_str` returns `""` when `cip_int == 0`, while `_format_cip_code` would return `"00.00"`. Additionally, the inverse operation (dot-format string → int) appears as inline expressions in `major_explorer.py:351`, `school_finder.py:75`, and implicitly inside `school_finder._normalize_cip4`. Four implementations of the same 2-line operation exist in two different modules.

```python
# _format_cip_code (major_explorer.py:179)
def _format_cip_code(cip: int) -> str:
    padded = f"{int(cip):04d}"
    return f"{padded[:2]}.{padded[2:]}"

# _cip_int_to_cip4_str (major_explorer.py:194)
def _cip_int_to_cip4_str(cip_int: int) -> str:
    if cip_int == 0:
        return ""
    padded = f"{cip_int:04d}"
    return f"{padded[:2]}.{padded[2:]}"
```

`_format_cip_code` is called at lines 171, 402, and 423 (used in vectorised `.apply()` and scalar contexts). `_cip_int_to_cip4_str` is called at line 1291. The two functions are NOT perfectly identical — `_cip_int_to_cip4_str` short-circuits on 0 while `_format_cip_code` does not — so consolidation requires choosing one behavior.

**Recommended fix:** Consolidate to a single `format_cip_code(cip: int) -> str` in a shared module (e.g., `utils.py` or a new `cip_utils.py`). Give it the `cip_int == 0 → ""` guard from `_cip_int_to_cip4_str` (correct for use as a sentinel check) and update all five call sites. Remove `_cip_int_to_cip4_str` and move `_normalize_cip4` from `school_finder.py` to the shared module as `parse_cip_code(s: str) -> str`.

**Effort:** S  
**Risk:** Low (pure refactor; behavior preserved; existing tests cover both paths)

---

### A4: RIASEC constant — 6 definitions of `["R", "I", "A", "S", "E", "C"]` across the codebase

**Location:**
- `riasec_distribution.py:20` — `_RIASEC_COLS = ["R", "I", "A", "S", "E", "C"]` (private)
- `riasec_matching.py:25` — `RIASEC_DIMENSIONS: list = ["R", "I", "A", "S", "E", "C"]` (public)
- `riasec_questionnaire.py:20` — `_DIMENSIONS = ["R", "I", "A", "S", "E", "C"]` (private)
- `url_state.py:54` — `RIASEC_DIMENSIONS = ("R", "I", "A", "S", "E", "C")` (tuple, public)
- `data_prep_riasec.py:32` — `RIASEC_DIMS = ["R", "I", "A", "S", "E", "C"]` (private)
- `page_modules/find_your_fit.py:51` — `_CANONICAL_ORDER = ['R', 'I', 'A', 'S', 'E', 'C']` (private)
- Test files: `tests/test_riasec_data_prep.py:17`, `tests/test_riasec_questionnaire.py:20` also define it locally.

**Current state:** The canonical RIASEC letter order is re-defined 6 times in production code (with varying names, types — list vs. tuple — and visibility). There is no single source of truth. `url_state.py` uses a tuple while all others use a list, creating a subtle inconsistency. Any future addition of a 7th or reordering requires touching all 6+ sites.

**Recommended fix:** Add `RIASEC_ORDER: tuple[str, ...] = ("R", "I", "A", "S", "E", "C")` to `config.py` (the established home of canonical constants). Import and reuse in all six modules. The tuple type (from `url_state.py`) is the most correct — it is immutable and ordered, matching the semantic intent. Data-prep scripts are separate processes but should import it the same way.

**Effort:** S  
**Risk:** Low (purely mechanical substitution; behavior is identical; one test per module verifies the list content)

---

### A7: Stale docstring comment in test file — wrong module path

**Location:** `tests/test_find_your_fit_page.py:1` (module docstring) and `tests/test_find_your_fit_page.py:11` (test docstring)

**Current state:**
- Line 1: `"""Tests for pages/find_your_fit.py — import integrity and constant correctness."""`
- Line 11 (inside `test_page_module_imports`): `"""pages.find_your_fit imports without error."""`

Both strings reference `pages/` and `pages.`, the old folder name from before the May 2 rename to `page_modules/`. The actual import at line 7 correctly says `import page_modules.find_your_fit as fyf_module`. The test passes, but the docstrings are misleading and would confuse a new contributor.

**Recommended fix:** Update line 1 to reference `page_modules/find_your_fit.py` and line 11 to say `page_modules.find_your_fit imports without error.`

**Effort:** XS  
**Risk:** Low

---

### A8: Stale module-path references in test file docstrings

**Location:** `tests/test_major_explorer_alignment.py:1`

**Current state:** Line 1 reads: `"""Tests for the Phase 12.3 alignment helper in pages/major_explorer.py."""` — references the old `pages/` path. The actual import at line 9 correctly says `from page_modules.major_explorer import _get_aligned_cip4_set`.

**Recommended fix:** Update the module docstring to reference `page_modules/major_explorer.py`.

**Effort:** XS  
**Risk:** Low

---

### B1: Swallowed exception in `_cip_filter_label` (app.py)

**Location:** `app.py:312–320`

**Current state:**
```python
def _cip_filter_label(cip4_str: str) -> str:
    try:
        fos_df = major_explorer.load_field_of_study()
        picker = major_explorer.build_major_picker_options(fos_df)
        match = picker[picker["cip_code_display"] == cip4_str]
        if not match.empty:
            return match.iloc[0]["display_name"]
    except Exception:
        pass
    return cip4_str
```

`except Exception: pass` silently swallows any error that occurs loading the field-of-study data. If `load_field_of_study()` fails (e.g., cleaned CSV not on disk at startup), the banner that follows shows the raw CIP string instead of the human-readable label. The underlying problem — missing data file — is hidden from the developer and the user sees an ugly "11.07" instead of "Computer Science (11.07)". This is the only bare `except Exception: pass` in the production codebase.

**Recommended fix:** Narrow the guard to specific exceptions (`FileNotFoundError`, `KeyError`) or at minimum log a warning before the `pass`. Since `load_field_of_study` uses `@st.cache_data` and calls `st.stop()` on a missing file, this guard may be entirely unnecessary.

**Effort:** XS  
**Risk:** Low (fallback behavior is acceptable; fix improves debuggability)

---

## Nice-to-Have

### A2: `_last_xtab_*` sentinel inventory — three ad-hoc keys, no dispatch mechanism

**Location:**
- `page_modules/major_explorer.py:338` — writes `_last_xtab_pinned` (value: school name string)
- `page_modules/major_explorer.py:352` — writes `_last_xtab_cip` (value: CIP4 dot-format string)
- `page_modules/school_finder.py:31` — writes `_last_xtab_cip_filter` (value: CIP4 dot-format string)
- `page_modules/major_explorer.py:1346` — reads `_last_xtab_pinned` via `.pop()`
- `page_modules/find_your_fit.py:258` — reads `_last_xtab_cip` via `.pop()`
- `app.py:2526` — reads `_last_xtab_cip_filter` via `.pop()`

**Current state:** Three separate one-shot banner sentinels with slightly inconsistent naming conventions. `_last_xtab_pinned` holds a string; the other two hold CIP4 strings. Each is `pop()`-ed in a different module. This works but is difficult to reason about holistically — there is no central registry of active sentinels. Adding a fourth cross-tab flow would require reading six files to understand the pattern.

**Recommended fix:** Consolidate into a single `_xtab_pending` dict in session state with a known schema, e.g., `{"action": "pinned" | "cip" | "cip_filter", "payload": ...}`. Or, at minimum, establish a naming convention doc comment at the top of each relevant file. The current 3-sentinel system is bounded and well-documented in PROJECT_STATUS.md, so this is genuinely a nice-to-have unless a fourth cross-tab flow is added.

**Effort:** S  
**Risk:** Low

---

### A3: Button-key pattern proliferation — three distinct per-row key patterns

**Location:**
- `page_modules/find_your_fit.py:279` — `key=f"explore_riasec_{cip4}"`
- `page_modules/major_explorer.py:1221` — `key=f"see_schools_{selected_row['cip_code_display']}"`
- `page_modules/major_explorer.py:1370` — `key=f"pin_btn_{int(row['unit_id'])}_{cip_code}"`
- `app.py:1818` — `key=f"explore_program_{unitid_int}_{row['cip4']}"`
- `page_modules/find_your_fit.py:233` — `key="dismiss_shared_results"` (singleton, no collision risk)

**Current state:** Four distinct f-string key patterns for per-row/per-item buttons. Each was written ad-hoc as the cross-tab features were added. No collision has occurred because each pattern uses distinct prefix + different uniqueness fields, but a future developer adding a fifth cross-tab button must know all four existing patterns to choose a non-colliding name.

**Recommended fix:** Extract a `make_button_key(*parts: str) -> str` helper (XS effort, lives in `utils.py`) that joins parts with `_` and strips dots. Document the key taxonomy in a single comment block. Reduces collision risk for Phase 6 additions.

**Effort:** XS  
**Risk:** Low

---

### A6: Test file organization — two files have crossed the 25-test cohesion threshold

**Location:**
- `tests/test_major_explorer_alignment.py` — 21 tests covering Phase 12.3 (alignment helper + caching), Phase 13.1 (`set_major_explorer_cip`), Phase 13.2 (`set_school_finder_cip`, `initial_cip_filter_index`, `apply_cip_filter`), and Phase 13.3 (`get_school_all_programs`)
- `tests/test_naics_data_prep.py` — 26 tests covering both the SOC-level (`soc_to_naics3.csv`) and CIP4-level (`cip4_naics_distribution.csv`) pipelines, plus the `_normalize_cip4` and `get_naics_distribution` loader functions

**Current state:** `test_major_explorer_alignment.py` mixes five distinct concerns under a Phase 12.3-only name. A developer looking for tests of the Phase 13.2 school-finder CIP filter would not find them without reading the full file. `test_naics_data_prep.py` mixes the SOC-level Phase 11.3.1 prep and the CIP4-level Phase 11.3.3 prep — two separate data flows — in one file.

**Recommended fix:** For `test_major_explorer_alignment.py`: split out Phase 13.1/13.2/13.3 helper tests into `tests/test_cross_tab_helpers.py`. For `test_naics_data_prep.py`: rename to `tests/test_naics_soc_level.py` and move CIP4-distribution tests to `tests/test_naics_cip4_level.py`. The test count per file would drop to 10–15, well within the original 25-test threshold.

**Effort:** S  
**Risk:** Low (no behavior change; `pytest tests/` result is identical; import paths change)

---

### B4: `=6.0` zero-byte file at repo root

**Location:** `=6.0` (repo root, confirmed 0 bytes)

**Current state:** A 0-byte file named `=6.0` exists at the repo root. This is almost certainly an accidental redirect artifact from a command like `pip install streamlit=6.0` where the shell interpreted `=6.0` as a redirect target instead of a version pin. Completely inert but will confuse anyone listing the directory.

**Recommended fix:** Delete the file. `git rm "=6.0"` or simple OS delete. No code references it.

**Effort:** XS  
**Risk:** Low

---

### B5: Magic numbers in `scoring.py` — robustness tier thresholds unnamed

**Location:** `scoring.py:231–235`

**Current state:**
```python
if robustness >= 0.70:
    tier = "robust"
elif robustness >= 0.40:
    tier = "borderline"
else:
    tier = "volatile"
```
The thresholds `0.70` and `0.40` are bare floats with no named constant. The `top_n=10` default at `app.py:1898` (and `riasec_matching.py:113` default of `n=10`) is similarly implicit. These thresholds have methodological meaning — they define what "robust" means for the sensitivity analysis — and should be documented at definition time.

**Recommended fix:** Add to `config.py` (or `scoring.py` module-level):
```python
SENSITIVITY_ROBUST_THRESHOLD = 0.70    # >= 70% of perturbations: robust
SENSITIVITY_BORDERLINE_THRESHOLD = 0.40  # >= 40%: borderline; < 40%: volatile
SENSITIVITY_DEFAULT_TOP_N = 10
```
Replace all three literals with the named constants.

**Effort:** XS  
**Risk:** Low

---

## Defer to Phase 6 / Phase 7

### B3: Streamlit-coupled vs. pure-function boundary in app.py

**Location:** `app.py` — functions `apply_filters` (line 220), `render_detail_card` (line 1824), `render_comparison` (estimated around line 2000), and the `_apply_income_bracket_column` helper (line 166)

**Current state:** `app.py` at 2,614 lines contains a mix of pure data-transformation functions (e.g., `apply_filters` takes a DataFrame and returns a DataFrame with no Streamlit calls) and Streamlit-coupled render functions that call `st.metric`, `st.markdown`, etc. The pure functions are untested because they are embedded in `app.py` and importing `app.py` from a test triggers `st.set_page_config()`. The boundary is understood (the team explicitly moved `apply_cip_filter` and `initial_cip_filter_index` out to `school_finder.py` for exactly this reason) but has not been systematically applied to `app.py`'s remaining pure helpers.

**Recommended fix:** In Phase 6, extract the three or four remaining pure data-transformation functions from `app.py` into a new `app_helpers.py` module (or add them to existing modules by concern). Priority candidates: `apply_filters`, `_apply_income_bracket_column`, and the `_build_results_csv_bytes`/`_build_results_pdf_bytes` builders. Each has clear inputs and outputs and no Streamlit dependencies.

**Effort:** M (requires careful extraction and regression testing)  
**Risk:** Medium (app.py is noted as fragile under surgical edits; prefer Phase 6 timing when a full regression pass is planned)

---

### B6: `app.py` exceeds 2,000-line threshold — sketch of extraction boundaries

**Location:** `app.py` (2,614 lines total)

**Current state:** At 2,614 lines, `app.py` is by far the longest file in the project. The file contains: data loading (lines 200–215), filter logic (lines 220–267), session state (lines 270–304), URL state orchestration (lines 306–420), four export builders (PDF, CSV — approx. lines 420–1000), six render functions for the School Finder tab (results table, pin selector, comparison view, detail cards, map, export row — approx. lines 1000–2500), and the main() entry point (lines 2400–2614).

**Natural extraction boundaries:**
- `app_export.py` — `_build_results_csv_bytes`, `_build_results_pdf_bytes`, `render_export_row`, all PDF layout constants (`PDF_*`)
- `app_filters.py` — `apply_filters`, `_apply_income_bracket_column`, `_net_price_column_and_label`
- `app_url.py` — `_parse_url_into_session_state`, `_write_session_state_to_url`, `URL_PARAM_MAP` (note: pure orchestration, unlike the pure encoders/decoders in `url_state.py`)

The render functions (`render_detail_card`, `render_comparison`, `render_map`, `render_results`, `render_pin_selector`) could move to `page_modules/school_finder.py` as they exclusively serve the School Finder tab — consistent with the existing convention that helpers live next to the page they serve.

**Recommended fix:** Phase 6 refactor — extract `app_export.py` first (largest self-contained chunk, ~500 lines, no circular import risk). Then `app_filters.py`. The render functions are riskier to extract due to the number of parameters they pass through; defer to Phase 7 unless the file becomes a maintenance problem earlier.

**Effort:** L (multi-session refactor; requires full regression pass)  
**Risk:** High (app.py is the entry point; Streamlit's reactive model makes some refactors non-obvious)

---

## Informational

### I1: `_normalize_cip4` is defined 3 times in production code

**Location:**
- `naics_distribution.py:29` — private, handles dot format and bare int string
- `riasec_distribution.py:33` — private, also handles float inputs (most robust version)
- `page_modules/school_finder.py:15` — private, handles dot and bare int string

**Current state:** Three private implementations of the same normalization logic. The `riasec_distribution.py` version is the most complete — it handles float inputs like `1.0` (which pandas produces when reading a CSV without `dtype=str`). The other two are slightly simpler and would fail on float inputs. All three are tested independently. This is related to A1 above — a consolidated `cip_utils.py` module (or additions to `utils.py`) would house a single canonical version.

**Effort:** S (subsumes into A1 fix)  
**Risk:** Low

---

### I2: `page_modules/major_explorer.py` is approaching the 1,500-line threshold

**Location:** `page_modules/major_explorer.py` (1,379 lines)

**Current state:** At 1,379 lines, `major_explorer.py` is 121 lines below the informal 1,500-line flag. It hosts data loaders, aggregation helpers, 8 render functions, and cross-tab helpers. Natural split: separate render functions (the `render_*` and `_render_*` functions, ~500 lines) from data functions (loaders, aggregations, cross-tab helpers). This is not yet urgent but worth watching as Phase 6 polish may add lines.

**Effort:** M (if extraction is done in Phase 6)  
**Risk:** Low (non-urgent)

---

### I3: `data_prep_majors.py` is the second-largest file at 907 lines

**Location:** `data_prep_majors.py` (907 lines)

**Current state:** A single data-preparation script covering Phases 9, 10.3, 10.3B, and 11.3. Not imported by the app at runtime (run once to produce CSVs). Its size is acceptable for a batch script but would benefit from being split by phase if further expansion is planned in Phase 14 or beyond.

**Effort:** S  
**Risk:** Low (offline batch script; no app runtime impact)

---

### I4: No `pytest.ini` or `pyproject.toml` — test discovery relies on pytest defaults

**Location:** Repo root (no `pytest.ini` or `pyproject.toml`)

**Current state:** Without a `testpaths` configuration, running `pytest` from the repo root discovers tests in both the root (finding `test_major_descriptions.py`) and `tests/`. The canonical `pytest tests/` command excludes the root-level file. Adding `testpaths = ["tests"]` to a `pytest.ini` (or `[tool.pytest.ini_options]` in `pyproject.toml`) would make both `pytest` and `pytest tests/` produce the same 248-test result — and moving the file (recommended in A5) is the cleaner fix.

**Effort:** XS  
**Risk:** Low

---

### I5: `CLEANED_ZIP_LATLONG` config constant is commented out but referenced in `utils.py`

**Location:** `config.py:49` (commented out), `utils.py:101`

**Current state:** `config.py` defines `CLEANED_ZIP_LATLONG` in a commented-out block (scope-cut). However, `utils.py:101` references `config.CLEANED_ZIP_LATLONG` in `_load_zip_table()`. This works because `utils.py` guards the access with `if not path.exists(): return None` — but if Python ever evaluates `config.CLEANED_ZIP_LATLONG` without the `if`, it will raise `AttributeError`. Currently it does not, because `_load_zip_table` is also gated. The guard chain is fragile — it relies on two separate levels of optional-path handling to not crash.

**Recommended fix:** Either un-comment `CLEANED_ZIP_LATLONG` in config.py (safe, it's just a string constant), or remove the `_load_zip_table` / `zip_to_coords` functions from `utils.py` since distance filtering was scope-cut. The functions are dead code — they are tested (indirectly, via the ZIP tests) but not called from any live code path.

**Effort:** XS  
**Risk:** Low

---

*End of audit. Total findings: 5 Critical/High-Value Cleanup, 6 Nice-to-Have, 2 Defer, 5 Informational.*
