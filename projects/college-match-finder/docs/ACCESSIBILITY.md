# Accessibility — College Match Finder

**Last updated:** May 5, 2026 (post-Phase 6C-2)

---

## Streamlit framework limitations (accepted)

These are limitations imposed by Streamlit's component architecture that cannot be
remediated at the app layer. Each is documented here rather than fixed because the
workaround is either already in place or the trade-off would degrade other UX.

1. **No programmatic `st.tabs` switching.**
   Streamlit provides no API to switch the active tab from code. The app uses a
   sentinel-driven rerun pattern: clicking a cross-tab button writes a flag to
   `st.session_state`, triggers `st.rerun()`, and the target tab reads the flag on
   load to pre-populate its state. A user with assistive technology will land on the
   new tab's content after the rerun, but the browser's focus is not directed to a
   specific element — they will need to navigate from the top of the page.

2. **Focus returns to document body after `st.rerun()`, not the triggering button.**
   Every `st.button` with an `on_click` callback that causes a rerun drops focus to
   the document body. This is a Streamlit rendering constraint; there is no hook to
   restore or redirect focus after a rerun cycle. No workaround is possible at the
   app layer. Users navigating by keyboard or switch access should expect to
   re-orient after any action that triggers a full rerrender.

3. **Sidebar Tab order follows DOM order, not visual order.**
   Streamlit renders the sidebar before the main pane in the HTML document, so Tab
   cycles through sidebar filters before reaching main-pane content. This matches
   the left-to-right reading order a screen reader would use and is consistent with
   standard Streamlit behavior. No remediation needed.

4. **`st.expander` keyboard activation works; state change is not announced.**
   Expander widgets respond to Enter/Space when focused, but Streamlit does not
   propagate an `aria-expanded` state update to the accessibility tree when the
   panel opens or closes. A screen reader user can activate expanders but will not
   receive a "expanded" / "collapsed" announcement. This is a Streamlit component
   limitation with no app-layer fix.

5. **"See my results" button is absent from DOM until all 60 RIASEC questions are answered.**
   Rather than rendering a disabled button, the app conditionally renders the submit
   button only when the questionnaire is complete. This means focus is never trapped
   on an inert control — the button simply does not exist in the DOM until it is
   actionable. An AT user working through the questionnaire will not encounter the
   button until they are ready to submit.

6. **Sidebar collapse on mobile uses native browser overlay behavior.**
   The hamburger toggle that hides/shows the sidebar on small screens is part of
   Streamlit's shell UI and is not configurable at the app layer. Behavior (focus
   trap within the open sidebar, Escape to close) is determined by the browser and
   Streamlit's internal component, not by app code.

7. **Cross-tab button focus after `st.rerun()` lands at document body.**
   After clicking "See schools strong in this major →" or any other cross-tab
   handoff button, the School Finder (or Major Explorer) tab becomes active but
   focus is at the document body. The user must Tab from the top to reach the filter
   panel or results table. This is a consequence of items 1 and 2 above; no
   app-layer fix is available.

---

## Accessibility features by tab

### School Finder

- Acceptance badge renders emoji + text label via `format_acceptance_badge` helper
  (e.g. "🟢 Safety", "🟡 Match", "🔴 Reach", "⚪ N/A") — emoji and label always
  travel together.
- CI bar chart includes a descriptive prose caption explaining the confidence
  interval band, point estimate, and data-coverage fraction.
- Radar chart (percentile profile) has a prose caption naming the school and
  describing what the axes represent.
- Gender breakdown stacked bar chart has a prose caption.
- Earnings Mobility chart has a prose caption; the empty state (no data) uses
  `role="status"` so assistive technology announces the absence of data.
- `Explore →` buttons in the school-detail program rows carry a `help=` tooltip
  (e.g. "Explore the Computer Science major in Major Explorer") that identifies
  the specific major and destination tab.

### Major Explorer

- Employment choropleth map has a prose caption naming the field and data source.
- NAICS industry distribution bar chart has a prose caption.
- "See schools strong in this major →" cross-tab button has a specific label (not
  a generic "Go" or "→") plus a `help=` tooltip naming the major and describing
  what pre-filter will be applied in School Finder.
- Work-environment quartile bars use a blue intensity gradient rather than
  red/green, avoiding red-green color blindness conflicts. Direction (dark = high
  quartile) is consistent throughout.

### Find Your Fit

- RIASEC profile bar chart has a prose caption describing the 6 interest
  dimensions and what a higher bar means.
- `Explore →` buttons in the top-10 recommendation rows carry a `help=` tooltip
  naming the specific major (e.g. "Explore the Psychology major in Major
  Explorer").
- Cross-tab handoff preserves the selected CIP4 code in `st.session_state` so
  context is not lost across the rerun boundary.

### Data provenance (all tabs)

All three tabs render an identical "ℹ️ About the Data" expander at the footer
via `page_modules.about_the_data.render_about_the_data()`. The expander documents
all 12 data sources grouped into 5 categories (Schools / Majors / Careers /
Geography / Interests), plus a Methodology & limitations section porting the
existing BLS/O*NET methodology prose. A freshness caption above the expander
states the oldest and newest snapshot dates across all sources so a user on any
tab can see data recency without opening the expander.

---

## What's tested

**26 WCAG contrast tests** in `tests/test_config.py` cover every rendered color
token in `config.PALETTE` against its expected background. The `EXCLUDED_TOKENS`
dict skips PDF tint swatches and internal sentinels that are never rendered as
on-screen text; this keeps the suite honest rather than noisy — a few PDF fill
colors are intentionally light and would fail if tested against white, but they
are only used as cell backgrounds in printed output, not as foreground text on
screen. Wong-palette hues (blue, green, vermilion, pink) all pass WCAG AA (≥ 4.5)
against both white and the app's dark-gray background.

**4 parametrized badge regression tests** in `tests/test_utils.py`
(`test_acceptance_badge_includes_emoji_and_label[safety|match|reach|unknown]`)
assert that `format_acceptance_badge` always returns a string containing both the
emoji from `ACCEPTANCE_BADGE_EMOJI` and the human-readable label from
`config.ACCEPTANCE_LABELS`. A future refactor that drops either component would
fail this test before reaching production.

---

## Dark mode (accepted limitation)

The app ships with a hardcoded light theme as its intended default, defined in
`.streamlit/config.toml` (`base = "light"` plus four explicit color overrides).
Streamlit's runtime theme switcher is partially overridden by this block, and
verifying full dark-mode parity would require either removing the hardcoded theme
(changing the intended default) or building a parallel dark-mode color system.
Neither is justified for a single-user-theme portfolio app.

The one custom HTML element — the Earnings Mobility empty state
(`app.py`, `_render_earnings_mobility_chart`) — was migrated during Phase 6E from
hardcoded hex values (`#f0f0f0` / `#888`) to theme-derived CSS variables
(`var(--secondary-background-color, #f0f0f0)` / `var(--text-color, #555)`) so it
adapts correctly if a user overrides the theme via browser-level preferences.
All other rendered colors flow through `config.PALETTE` tokens or Streamlit's own
component theming and carry no hardcoded-color dark-mode liability.

---

## Mobile responsiveness

Phone viewport (375 × 812, iPhone X reference) verified across all three tabs in
Chrome DevTools device-toolbar mode. All surfaces render correctly: sidebar
collapses to a hamburger overlay and filters are reachable inside it; ranked school
cards stack to a single column; score bars fit within card width; acceptance badges
(emoji + label) render without truncation; the pinned-school detail panel (radar
chart, gender stacked bar, earnings mobility chart) renders at narrow width; the
scattermapbox map renders and pan gesture works; the comparison expander reflows
acceptably via Streamlit's automatic layout; the employment choropleth is small at
phone width but legible; the RIASEC questionnaire radio buttons stack and remain
tappable; `st.dataframe` provides native horizontal scroll where column count
exceeds viewport width. No app-fixable issues found on any of the three tabs.

Tablet viewport (768 × 1024) was not verified independently. Streamlit's reflow
logic only adds layout flexibility at wider viewports — surfaces verified at 375px
are strictly more constrained than at 768px. Tablet is considered covered by
phone-width verification.

---

## Lighthouse baseline (May 5, 2026)

Audit run in Chrome incognito mode against local app (`http://localhost:8501`),
device set to Mobile.

| Category | Score |
|---|---|
| Performance | 12 |
| Accessibility | 86 |
| Best Practices | 81 |
| SEO | 82 |

**Accessibility (86):** Zero machine-detectable failed audits. The 14-point gap to
100 is Lighthouse's manual-check territory — judgment items that cannot be
automatically scored (logical focus order, plain language, link purpose in context).
The 6C-1 and 6C-2 accessibility work covered the full automated audit surface.

**Performance (12):** Framework-imposed ceiling. Streamlit's Python→WebSocket
architecture and large frontend bundle produce low Lighthouse Performance scores by
design; scores in the 10–20 range are typical for Streamlit apps on the mobile
preset. Chasing a higher score would require replacing the framework. Accepted as a
known Streamlit limitation.

**Best Practices (81) and SEO (82):** Informational. This app is not optimized for
search indexing and is not expected to meet SEO targets.

---

## Phase 6 close-out

Phase 6 — Polish & Accessibility ran across six sub-sessions: **6A** (audit
cleanup — sentinel documentation, `make_button_key` helper, test file split),
**6B** (color palette consolidation — 35-token `config.PALETTE`, all inline hex
literals removed, three deliberate visual corrections), **6C-1** (chart
accessibility — captions on all 11 charts, `role="status"` on the Earnings
Mobility empty state, WCAG contrast tests across the full palette), **6C-2**
(interactive accessibility — `format_acceptance_badge` helper, `help=` tooltip
disambiguation on all `Explore →` buttons), **6D** (transparency surface —
12-source `render_about_the_data()` helper on all three tabs, freshness caption),
and **6E** (mobile/dark mode/Lighthouse — viewport verification, Lighthouse
baseline, dark-mode limitation documented, cross-tab widget-state shadowing bug
fixed). Final test count: **297 passing**.

Accepted limitations throughout Phase 6 followed a consistent approach: Streamlit
framework constraints were documented here rather than worked around with fragile
overrides. The cross-tab `Explore →` pre-selection bug found during 6E verification
is a methodology success — the verification pass surfaced a real production bug
(widget-state shadowing in `set_major_explorer_cip`, affecting both the School
Finder and Find Your Fit `Explore →` paths) that the existing test suite did not
catch. The bug was fixed and a regression test added before Phase 6 closed.
