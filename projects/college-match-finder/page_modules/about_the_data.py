"""
page_modules/about_the_data.py — Data provenance expander for Phase 6D.

render_about_the_data() is idempotent and safe to call from every tab footer.
OLDEST_DATE / NEWEST_DATE feed the per-tab freshness caption in each render() caller.
"""

import streamlit as st

# Oldest and newest authoritative snapshot dates across all 12 data sources.
# Update these when sources are refreshed; they feed the per-tab freshness caption.
OLDEST_DATE = "May 2024"       # BLS OEWS National / State / Industry-level
NEWEST_DATE = "February 2026"  # O*NET 30.2 + NY Fed (Feb 4, 2026 release)


def render_about_the_data() -> None:
    """Render the 'About the Data' expander. Idempotent — safe to call from every tab."""
    with st.expander("ℹ️ About the Data", expanded=False):

        # ── Schools ──────────────────────────────────────────────────────────
        st.markdown("### Schools")
        st.markdown(
            "**College Scorecard — Institution-Level Data**\n\n"
            "*Snapshot:* October 2025 release │ "
            "*Source:* [U.S. Dept. of Education](https://collegescorecard.ed.gov/data/)\n\n"
            "*Methodology:* Provides per-institution admissions rates, test scores, enrollment, "
            "net prices, and earnings outcomes that drive the School Finder’s scoring "
            "dimensions and filters."
        )
        st.markdown(
            "**College Scorecard — Field of Study Data**\n\n"
            "*Snapshot:* April 2025 release │ "
            "*Source:* [U.S. Dept. of Education](https://collegescorecard.ed.gov/data/)\n\n"
            "*Methodology:* Provides program-level 1-year and 5-year graduate earnings and "
            "median debt by institution and CIP code, displayed in school detail cards and "
            "Major Explorer’s “Schools strong in this major” table."
        )

        # ── Majors ───────────────────────────────────────────────────────────
        st.markdown("### Majors")
        st.markdown(
            "**NCES CIP–SOC Crosswalk** (CIP 2020 → SOC 2018)\n\n"
            "*Snapshot:* CIP 2020 edition (no annual release cycle) │ "
            "*Source:* [NCES IPEDS](https://nces.ed.gov/ipeds/cipcode/Files/CIP2020_SOC2018_Crosswalk.xlsx)\n\n"
            "*Methodology:* Many-to-many mapping from CIP codes to SOC occupations; the app "
            "takes the union of routing occupations across each 4-digit CIP’s 6-digit "
            "children to join academic programs to BLS and O\\*NET data."
        )
        st.markdown(
            "**Major Descriptions** (hand-authored)\n\n"
            "*Snapshot:* Internal — authored 2026\n\n"
            "*Methodology:* Hand-authored name and summary for 60 top-enrolled CIP4 majors, "
            "displayed as descriptive text in Major Explorer; auto-generated stubs for the "
            "remaining ∼350 majors are derived from Scorecard field-of-study titles."
        )
        st.markdown(
            "**Major Outcomes** (derived table)\n\n"
            "*Snapshot:* Derived — no independent date\n\n"
            "*Methodology:* Per-CIP4 employment-weighted aggregates of median wage, projected "
            "growth rate, and annual openings; produced from BLS OEWS National + BLS "
            "Employment Projections + NCES CIP–SOC Crosswalk and used throughout Major "
            "Explorer’s outcomes panel."
        )

        # ── Careers ──────────────────────────────────────────────────────────
        st.markdown("### Careers")
        st.markdown(
            "**BLS Occupational Employment and Wage Statistics (OEWS), National — May 2024**\n\n"
            "*Snapshot:* May 2024 │ "
            "*Source:* [BLS OEWS National](https://www.bls.gov/oes/special-requests/oesm24nat.zip)\n\n"
            "*Methodology:* Provides wage percentiles (10th–90th) and total employment by "
            "SOC occupation; joined to CIP4 via the CIP–SOC crosswalk and "
            "employment-weighted to produce major-level wage estimates."
        )
        st.markdown(
            "**BLS Employment Projections, 2024–2034**\n\n"
            "*Snapshot:* 2024–2034 cycle (released August 2025) │ "
            "*Source:* [BLS Employment Projections](https://www.bls.gov/emp/ind-occ-matrix/occupation.xlsx)\n\n"
            "*Methodology:* Provides 10-year percent employment change, annual job openings, "
            "and entry-level education requirements by SOC, joined to CIP4 and weighted to "
            "produce major-level projected growth."
        )
        st.markdown(
            "**BLS NAICS-by-SOC Industry Distribution — May 2024**\n\n"
            "*Snapshot:* May 2024 │ "
            "*Source:* [BLS OEWS Industry-Level](https://www.bls.gov/oes/special-requests/oesm24in4.zip)\n\n"
            "*Methodology:* Provides each occupation’s employment share across 3-digit "
            "NAICS industries; aggregated via CIP–SOC crosswalk to produce the "
            "“Top industries” distribution panel in Major Explorer."
        )

        # ── Geography ────────────────────────────────────────────────────────
        st.markdown("### Geography")
        st.markdown(
            "**BLS OEWS State-Level — May 2024**\n\n"
            "*Snapshot:* May 2024 │ "
            "*Source:* [BLS OEWS State](https://www.bls.gov/oes/special-requests/oesm24st.zip)\n\n"
            "*Methodology:* State-level occupation employment counts and location quotients, "
            "aggregated via CIP–SOC crosswalk to produce the geographic concentration "
            "choropleth in Major Explorer."
        )

        # ── Interests ────────────────────────────────────────────────────────
        st.markdown("### Interests")
        st.markdown(
            "**O\\*NET Work Context** (v30.2)\n\n"
            "*Snapshot:* O\\*NET 30.2 (February 2026) │ "
            "*Source:* [O\\*NET Work Context](https://www.onetcenter.org/dl_files/database/db_30_2_excel/Work%20Context.xlsx)\n\n"
            "*Methodology:* Per-occupation ratings for 13 curated work-environment elements, "
            "aggregated to CIP4 by BLS-employment-weighted average and displayed as "
            "quartile-colored bars in Major Explorer. Used under CC BY 4.0."
        )
        st.markdown(
            "**O\\*NET RIASEC Interest Profiles** (v30.2)\n\n"
            "*Snapshot:* O\\*NET 30.2 (February 2026) │ "
            "*Source:* [O\\*NET Interests](https://www.onetcenter.org/dl_files/database/db_30_2_excel/Interests.xlsx)\n\n"
            "*Methodology:* Per-occupation RIASEC interest-dimension scores aggregated to CIP4 "
            "by BLS-employment-weighted average, compared against user questionnaire responses "
            "to rank major recommendations in Find Your Fit. Used under CC BY 4.0."
        )
        st.markdown(
            "**NY Fed Labor Market Outcomes for Recent College Graduates**\n\n"
            "*Snapshot:* February 4, 2026 release │ "
            "*Source:* [NY Fed College Labor Market](https://www.newyorkfed.org/research/college-labor-market)\n\n"
            "*Methodology:* Provides unemployment rate, underemployment rate, early- and "
            "mid-career wages, and graduate-degree share by broad major; mapped to CIP4 codes "
            "via a hand-curated crosswalk and displayed in Major Explorer’s "
            "labor-market panel."
        )

        # ── Methodology & limitations ─────────────────────────────────────────
        st.markdown("### Methodology & limitations")
        st.markdown(
            "**Aggregation method.** The Field of Study Scorecard reports earnings at the "
            "4-digit CIP level (e.g., `11.07` = Computer Science), while the crosswalk maps "
            "occupations at the 6-digit CIP level (e.g., `11.0701`, `11.0702`, etc.). For each "
            "4-digit CIP, the union of all routing occupations across its 6-digit children is "
            "taken. This slightly broadens the routing set but matches the Scorecard’s "
            "reporting granularity.\n\n"
            "**Weighting decision.** Major-level wage and growth numbers are computed as the "
            "employment-weighted average across the routing occupations, with weights "
            "proportional to each occupation’s 2024 total employment. For example, a "
            "Computer Science major’s weighted median wage is heavily anchored by "
            "Software Developers (1.65 million workers, $133,080 median) rather than Computer "
            "Science Teachers, Postsecondary (38,000 workers, $94,310 median), because the "
            "labor market actually concentrates graduates in the larger destination. "
            "Equal-weighted aggregation was rejected because it overstates the influence of "
            "small academic-side occupations and understates the dominant industry "
            "destinations.\n\n"
            "**Limitations.**\n\n"
            "- The CIP–SOC crosswalk is not based on actual destination-tracking data "
            "— it reflects expert judgment from BLS and NCES about which occupations "
            "require the skills a given program teaches. Real placement data would be richer "
            "but is not publicly available at this granularity.\n"
            "- Routing-set employment-weighting tells you what the average graduate’s "
            "destination occupation looks like in aggregate, not what any individual graduate "
            "will do. A Computer Science major can become a postsecondary teacher; the "
            "weighted median doesn’t predict their wage.\n"
            "- Some routing occupations from the crosswalk are aggregation-level SOC codes that "
            "BLS publishes only as detailed sub-codes in OEWS and the Employment Projections. "
            "These are silently dropped from the weighted average, which means the routing set "
            "displayed in the careers panel may be smaller than the raw crosswalk count for "
            "that CIP.\n"
            "- Wage data covers wage-and-salary workers and excludes the self-employed and "
            "partners in unincorporated firms. For majors that route heavily to self-employed "
            "roles (some arts, some trades), the OEWS median understates total "
            "compensation.\n\n"
            "**State-level geographic distribution.** The “Where these jobs are” "
            "panel uses BLS OEWS May 2024 state-level employment data, aggregated from "
            "per-occupation to per-major using the NCES CIP–SOC crosswalk. Total "
            "employment shows raw job counts by state. Location quotient (LQ) shows "
            "concentration relative to the national average — LQ = 1.0 means "
            "the major’s careers are represented at the national rate. The LQ color scale "
            "is capped at 5.0 for readability; hover tooltips show uncapped values. States "
            "with insufficient data (less than 50% of routing occupations observed at state "
            "level due to BLS confidentiality suppression) render as light gray.\n\n"
            "**Work environment characteristics.** The “Work environment” panel uses "
            "O\\*NET® 30.2 Work Context data, aggregated from per-occupation to per-major "
            "using the NCES CIP–SOC crosswalk. Each of the 13 elements is reported on "
            "O\\*NET’s 1–5 scale (frequency / importance / amount, depending on "
            "element type) and weighted by 2024 BLS employment when aggregating to the major "
            "level. Bars are colored by quartile rank across all 414 majors so users can see "
            "which characteristics distinguish a given major from typical work. Majors where "
            "less than 50% of routing occupations have O\\*NET coverage are flagged with a "
            "“data not available” message rather than partial results. "
            "This page includes information from the O\\*NET® 30.2 Database by the "
            "U.S. Department of Labor, Employment and Training Administration (USDOL/ETA), "
            "used under the CC BY 4.0 license. Jonathan Nadeau has modified all or some of "
            "this information. USDOL/ETA has not approved, endorsed, or tested these "
            "modifications."
        )
