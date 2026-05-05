# Phase 4.5 Verification Report

## Detail card renderer location
- File: `app.py`
- Function: `render_detail_card`
- Lines: 1644–1766
- Helper called by it: `_render_program_outcomes` — Lines 1588–1641

---

## FoS data in detail card?

**Found.** `_render_program_outcomes` is called at the bottom of `render_detail_card` (line 1766) and does exactly what Phase 8.5 requires:

```python
# app.py lines 1588–1641

def _render_program_outcomes(school_row: pd.Series, name: str) -> None:
    """
    Phase 8 — Step 8.5. Render the school's program-level outcomes for the
    major currently selected on the Major Explorer tab. Three cases:

      Case 1: school does not offer the major at all
      Case 2: school offers the major but reports no values for it
      Case 3: at least one value is reported — render metric tiles
    """
    cip_code = st.session_state.get("selected_cip")   # ← reads the bridge key
    if cip_code is None or cip_code == 0:
        return

    unit_id_val = school_row.get("unit_id")
    if pd.isna(unit_id_val):
        return

    fos_df = major_explorer.load_field_of_study()     # ← loads field_of_study_cleaned.csv
    major_label = major_explorer.get_selected_major_label(fos_df, int(cip_code))
    if major_label is None:
        return

    program = major_explorer.get_school_program_outcomes(
        fos_df, int(unit_id_val), int(cip_code)       # ← per-school FoS lookup
    )

    st.markdown(f"**Program-level outcomes — {major_label}**")

    # Case 1: school does not offer this major
    if program is None:
        st.caption(f"_{name} does not offer this major._")
        return

    # Case 2: offers but all four metrics are NaN (cohort below n=30)
    all_missing = all(pd.isna(v) for v in program.values())
    if all_missing:
        st.caption(
            f"_{name} offers this major, but the program's cohort size fell "
            "below the Scorecard's reporting threshold (n < 30)._"
        )
        return

    # Case 3: render metric tiles
    cols = st.columns(4)
    tiles = [
        ("median_earnings_1yr", "Earnings, 1yr"),
        ("median_earnings_4yr", "Earnings, 4yr"),
        ("median_earnings_5yr", "Earnings, 5yr"),
        ("median_debt",         "Median debt"),
    ]
    for col_widget, (col_name, label) in zip(cols, tiles):
        val = program[col_name]
        display = "—" if pd.isna(val) else f"${val:,.0f}"
        col_widget.metric(label, display)
```

The call site in `render_detail_card`:

```python
# app.py line 1764–1766
        # Phase 8 — Step 8.5: Program-level outcomes for the major
        # currently selected on the Major Explorer tab.
        _render_program_outcomes(school_row, name)
```

---

## Session_state bridge from Major Explorer?

**Found.** `pages/major_explorer.py` defines the key constant and writes it on every render:

```python
# major_explorer.py lines 41–44
# Session-state key for the currently selected CIP code (stored as int to
# match the dtype in the source CSV). Read by Steps 8.3-8.5 and by the
# School Finder tab in Step 8.5.
SELECTED_CIP_KEY = "selected_cip"

# major_explorer.py line 872 (inside render())
    st.session_state[SELECTED_CIP_KEY] = int(selected_row["cip_code"])
```

Additionally, `app.py` wires `selected_cip` into the URL parameter system so
the selection survives page shares/bookmarks (line 166):

```python
# app.py line 166
    "cip":     ("selected_cip",           int,  0),
```

---

## Verdict: A — Fully shipped

Phase 4.5 is **fully implemented**. The Major Explorer tab writes
`st.session_state["selected_cip"]` whenever a user picks a major (or on
first load, defaulting to 0). The School Finder's `render_detail_card`
function calls `_render_program_outcomes`, which reads that same key, loads
`field_of_study_cleaned.csv` via the cached `major_explorer.load_field_of_study()`
helper, looks up the specific school–major combination, and renders four
`st.metric` tiles (1yr earnings, 4yr earnings, 5yr earnings, median debt)
directly inside each pinned school's detail card. All three required cases
are handled: major not offered, offered but below reporting threshold, and
offered with reportable data. No missing code — both sides of the bridge
exist and are connected.

## If verdict is B or C — what's missing

N/A — verdict is A.
