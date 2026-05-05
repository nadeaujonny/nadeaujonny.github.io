# Cross-Tab Session State Sentinels

These are the short-lived session_state keys that coordinate cross-tab navigation
and one-shot UI banners. Each is written by one site and consumed (usually popped)
by a single consumer on the next rerun.

---

## `_last_xtab_pinned`

| Field | Value |
|---|---|
| **Written by** | `page_modules/major_explorer.py:309` — `_pin_school_callback()` |
| **Consumed by** | `page_modules/major_explorer.py:1317` — schools table banner block |
| **Lifecycle** | One-shot pop — consumed with `.pop()` on the first rerun after a pin click |
| **Signals** | A school was just pinned from the Major Explorer schools table; value is the school name string to display in the instruction banner |

---

## `_last_xtab_cip`

| Field | Value |
|---|---|
| **Written by** | `page_modules/major_explorer.py:323` — `set_major_explorer_cip()` |
| **Consumed by** | `page_modules/find_your_fit.py:257` — `_render_results()` banner block |
| **Lifecycle** | One-shot pop — consumed with `.pop()` on the first rerun after an Explore button click |
| **Signals** | A CIP4 was just sent from Find Your Fit results to Major Explorer; value is the dot-format CIP4 string (e.g. `"11.07"`) to display in the FYF confirmation banner |

---

## `_last_xtab_cip_filter`

| Field | Value |
|---|---|
| **Written by** | `page_modules/school_finder.py:26` — `set_school_finder_cip()` |
| **Consumed by** | `app.py:2527` — School Finder tab banner block in `main()` |
| **Lifecycle** | One-shot pop — consumed with `.pop()` on the first rerun after a "See schools" button click |
| **Signals** | School Finder was just pre-filtered to a CIP4 by a cross-tab handoff; value is the dot-format CIP4 string to display in the School Finder banner |

---

## `_url_tab_banner`

| Field | Value |
|---|---|
| **Written by** | `app.py:367` — `_parse_url_into_session_state()` |
| **Consumed by** | `app.py:2515` — `main()` before tab blocks |
| **Lifecycle** | One-shot pop — consumed with `.pop()` on the first render after a deep-link URL load |
| **Signals** | The page was loaded with a `?tab=` query parameter pointing to a non-default tab; value is the validated tab name string to display in the "switch to this tab" banner |

---

## `_active_tab`

| Field | Value |
|---|---|
| **Written by** | `page_modules/major_explorer.py:324` — `set_major_explorer_cip()`; `page_modules/school_finder.py:27` — `set_school_finder_cip()`; `page_modules/find_your_fit.py:169` — FYF submit handler |
| **Consumed by** | `app.py:358` — `_parse_url_into_session_state()` (URL writer reads it); `app.py:365` — persisted or cleaned depending on validity |
| **Lifecycle** | Persistent — survives reruns; cleaned at `app.py:363` only when the decoded value is invalid or default |
| **Signals** | The tab the user should be on (or was last sent to via cross-tab handoff); drives the `?tab=` URL parameter written by `_write_session_state_to_url()` |
