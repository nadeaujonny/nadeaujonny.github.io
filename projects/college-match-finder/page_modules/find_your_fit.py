"""
Find Your Fit tab — Phase 12.2c of the College Match Finder.

Renders the 60-item RIASEC questionnaire (O*NET Interest Profiler Short Form),
gates the submit button until all 60 items are answered, scores responses on
submit, and displays the user's Holland Code + interest profile bar chart plus
their top 10 aligned majors. The `riasec_user_vector` session key written here
is consumed by Phase 12.3 (Major Explorer alignment badges).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from riasec_questionnaire import get_items, get_response_scale, score_responses, validate_responses
from riasec_matching import compute_holland_code, get_top_n_matches
from major_descriptions import get_description
from page_modules.major_explorer import set_major_explorer_cip
from page_modules.about_the_data import render_about_the_data, OLDEST_DATE, NEWEST_DATE
from config import RIASEC_DIMENSIONS, PALETTE
from url_state import encode_riasec
from utils import make_button_key

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DIMENSION_NAMES = {
    'R': 'Realistic',
    'I': 'Investigative',
    'A': 'Artistic',
    'S': 'Social',
    'E': 'Enterprising',
    'C': 'Conventional',
}

DIMENSION_DESCRIPTIONS = {
    'R': 'Hands-on, practical work — building, fixing, working with tools, machines, plants, or animals.',
    'I': 'Investigative work — researching, analyzing, solving problems, and working with ideas.',
    'A': 'Creative and artistic work — writing, designing, performing, or expressing yourself.',
    'S': 'Helping, teaching, and working with people in caring or supportive roles.',
    'E': 'Leading, persuading, selling, or starting and managing things.',
    'C': 'Organizing, managing data, working with details, and following clear procedures.',
}

SESSION_KEYS = {
    'responses':       'fyf_responses',       # dict mapping item_id -> Likert int
    'submitted':       'fyf_submitted',       # bool — has the user submitted?
    'user_vector':     'riasec_user_vector',  # dict R/I/A/S/E/C floats — consumed by Phase 12.3
    'holland_code':    'fyf_holland_code',    # str — derived for display
    'expander_states': 'fyf_expander_states', # dict[dim_letter, bool] — open/closed per section
}


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------

def _init_session_state() -> None:
    st.session_state.setdefault(SESSION_KEYS['responses'], {})
    st.session_state.setdefault(SESSION_KEYS['submitted'], False)
    st.session_state.setdefault(SESSION_KEYS['user_vector'], None)
    st.session_state.setdefault(SESSION_KEYS['holland_code'], None)
    st.session_state.setdefault(
        SESSION_KEYS['expander_states'],
        {dim: False for dim in RIASEC_DIMENSIONS},
    )


def _reset_session_state() -> None:
    st.session_state[SESSION_KEYS['responses']] = {}
    st.session_state[SESSION_KEYS['submitted']] = False
    st.session_state[SESSION_KEYS['user_vector']] = None
    st.session_state[SESSION_KEYS['holland_code']] = None
    st.session_state[SESSION_KEYS['expander_states']] = {dim: False for dim in RIASEC_DIMENSIONS}
    for key in list(st.session_state.keys()):
        if key.startswith('fyf_item_'):
            del st.session_state[key]


# ---------------------------------------------------------------------------
# Radio on-change callback
# ---------------------------------------------------------------------------

def _radio_on_change(item_id: str, widget_key: str, dim: str) -> None:
    label = st.session_state.get(widget_key)
    if label is not None:
        scale = get_response_scale()
        label_to_int = {v: k for k, v in scale['labels'].items()}
        st.session_state[SESSION_KEYS['responses']][item_id] = label_to_int[label]
    st.session_state[SESSION_KEYS['expander_states']][dim] = True


# ---------------------------------------------------------------------------
# Render sections
# ---------------------------------------------------------------------------

def _render_header() -> None:
    st.header("Find Your Fit")
    st.markdown(
        "This questionnaire is based on the **O\\*NET Interest Profiler Short Form** — "
        "60 work activities that measure your interests across six Holland dimensions. "
        "It takes about 10 minutes. When you finish, you'll see a personalized list of "
        "majors whose interest profiles most closely match yours. "
        "\n\n"
        "This is a **surfacing tool, not a prescription.** The app's job is to show "
        "what's out there that aligns with your interests — the decision of what to "
        "study is yours. Pursue what genuinely excites you."
    )
    st.caption(
        "Rate each work activity on a 5-point scale from **Strongly Dislike** to "
        "**Strongly Like**. Answer based on how you'd feel doing the activity, not "
        "whether you have experience with it."
    )


def _render_questionnaire() -> None:
    scale = get_response_scale()
    labels = [scale['labels'][i] for i in range(scale['min'], scale['max'] + 1)]

    items = get_items()
    items_by_dim: dict = {dim: [] for dim in RIASEC_DIMENSIONS}
    for item in items:
        items_by_dim[item['dimension']].append(item)

    responses = st.session_state[SESSION_KEYS['responses']]

    expander_states = st.session_state[SESSION_KEYS['expander_states']]

    for dim in RIASEC_DIMENSIONS:
        dim_items = items_by_dim[dim]
        answered_count = sum(1 for it in dim_items if it['id'] in responses)
        with st.expander(DIMENSION_NAMES[dim], expanded=expander_states[dim]):
            st.caption(f"**{answered_count} / 10 answered** — {DIMENSION_DESCRIPTIONS[dim]}")
            for item in dim_items:
                widget_key = f"fyf_item_{item['id']}"
                st.radio(
                    item['text'],
                    options=labels,
                    index=None,
                    horizontal=True,
                    key=widget_key,
                    on_change=_radio_on_change,
                    args=(item['id'], widget_key, dim),
                )

    total_answered = len(responses)
    st.progress(total_answered / 60, text=f"{total_answered} / 60 answered")

    is_complete = total_answered == 60
    if st.button(
        "See my results",
        disabled=not is_complete,
        type='primary',
        key='fyf_submit',
    ):
        errors = validate_responses(responses)
        if errors:
            for err in errors:
                st.error(err)
        else:
            user_vector = dict(score_responses(responses))
            holland_code = compute_holland_code(user_vector)
            st.session_state[SESSION_KEYS['user_vector']] = user_vector
            st.session_state[SESSION_KEYS['holland_code']] = holland_code
            st.session_state[SESSION_KEYS['submitted']] = True
            # Phase 13.4b: encode vector into URL so results are shareable.
            encoded = encode_riasec(user_vector)
            if encoded:
                st.session_state["_url_riasec_vector"] = encoded
                st.session_state["_active_tab"] = "find_your_fit"
            st.rerun()


def _render_results() -> None:
    user_vector = st.session_state[SESSION_KEYS['user_vector']]
    holland_code = st.session_state[SESSION_KEYS['holland_code']]

    # --- User profile section ---
    st.subheader("Your Interest Profile")

    st.metric("Your Holland Code", holland_code)
    letters = list(holland_code)
    st.markdown(
        f"That's **{DIMENSION_NAMES[letters[0]]}**, "
        f"**{DIMENSION_NAMES[letters[1]]}**, and "
        f"**{DIMENSION_NAMES[letters[2]]}** — your three strongest interest areas."
    )

    dim_labels = [DIMENSION_NAMES[d] for d in RIASEC_DIMENSIONS]
    dim_scores = [user_vector[d] for d in RIASEC_DIMENSIONS]

    fig = go.Figure(go.Bar(
        x=dim_scores,
        y=dim_labels,
        orientation='h',
        marker_color=PALETTE["categorical_primary"],
        text=[f"{s:.0f}" for s in dim_scores],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Score: %{x:.0f} / 40<extra></extra>',
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 40], title='Score (0–40)'),
        yaxis=dict(title=''),
        height=320,
        margin=dict(l=10, r=40, t=20, b=40),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Horizontal bar chart of your 6 RIASEC interest dimension scores from the "
        "O*NET Interest Profiler Short Form. Higher = stronger interest in that dimension."
    )

    st.divider()

    # --- Aligned majors section ---
    st.subheader("Majors Aligned with Your Interests")
    st.markdown(
        "These are the top 10 majors whose RIASEC interest profiles correlate most "
        "strongly with yours. Correlation measures profile *shape* similarity — a major "
        "that emphasizes the same dimensions you do, in a similar balance. "
        "Many other majors will also align well. Visit the **Major Explorer** tab to "
        "browse all 414 majors with alignment indicators."
    )

    top_10 = get_top_n_matches(user_vector, n=10)

    # Phase 13.4b: shared-results banner — placed before the empty-results guard so
    # users can dismiss even when the shared vector has zero variance.
    if st.session_state.get("_url_riasec_decoded") and not st.session_state.get("_riasec_shared_results_dismissed", False):
        cols = st.columns([5, 1])
        cols[0].info(
            "📌 Showing results from a shared link. "
            "These recommendations come from someone else's RIASEC scores."
        )
        if cols[1].button("Take the quiz yourself →", key="dismiss_shared_results"):
            # Mirror _reset_session_state() exactly
            st.session_state[SESSION_KEYS['responses']] = {}
            st.session_state[SESSION_KEYS['submitted']] = False
            st.session_state[SESSION_KEYS['user_vector']] = None
            st.session_state[SESSION_KEYS['holland_code']] = None
            st.session_state[SESSION_KEYS['expander_states']] = {dim: False for dim in RIASEC_DIMENSIONS}
            for key in list(st.session_state.keys()):
                if key.startswith('fyf_item_'):
                    del st.session_state[key]
            # Clear URL-driven state and mark dismissed
            st.session_state["_riasec_shared_results_dismissed"] = True
            st.session_state.pop("_url_riasec_vector", None)
            st.session_state.pop("_url_riasec_decoded", None)
            st.rerun()

    if top_10.empty:
        st.warning(
            "Your responses had no variation — every question got the same answer. "
            "To get personalized major recommendations, retake the quiz with more varied "
            "responses (some 'Strongly Like', some 'Strongly Dislike', some 'Unsure')."
        )
        return

    # Banner: shown on the rerun immediately after an Explore button click
    last_cip = st.session_state.pop("_last_xtab_cip", None)
    if last_cip is not None:
        st.success("Major Explorer is pre-loaded — click the tab to see it →")

    # Column header row
    hdr = st.columns([1, 7, 2, 2])
    hdr[0].markdown("**#**")
    hdr[1].markdown("**Major**")
    hdr[2].markdown("**Alignment**")
    hdr[3].markdown("")

    for rank_idx, (_, row) in enumerate(top_10.iterrows(), start=1):
        cip4 = row['cip4']
        desc = get_description(cip4)
        major_name = desc['name'] if desc is not None else cip4
        cols = st.columns([1, 7, 2, 2])
        cols[0].write(f"#{rank_idx}")
        cols[1].write(major_name)
        cols[2].write(f"r = {row['correlation']:.2f}")
        cols[3].button(
            "Explore →",
            key=make_button_key("explore_riasec", cip4),
            on_click=set_major_explorer_cip,
            args=(cip4,),
            help=f"Explore the {major_name} major in Major Explorer",
        )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def render() -> None:
    """Render the Find Your Fit tab — RIASEC questionnaire + recommendations."""
    _init_session_state()
    _render_header()

    # Phase 13.4b: if a URL-supplied RIASEC vector is present, skip the questionnaire
    # and render results directly using the shared vector.
    url_vector = st.session_state.get("_url_riasec_decoded")
    if url_vector and not st.session_state.get("_riasec_shared_results_dismissed", False):
        st.session_state[SESSION_KEYS['user_vector']] = url_vector
        st.session_state[SESSION_KEYS['holland_code']] = compute_holland_code(url_vector)
        st.session_state[SESSION_KEYS['submitted']] = True

    if st.session_state[SESSION_KEYS['submitted']]:
        _render_results()
        if st.button('Retake the questionnaire', key='fyf_retake'):
            _reset_session_state()
            st.rerun()
    else:
        _render_questionnaire()

    st.caption(
        f"Data through {OLDEST_DATE}, with some sources updated as recently as "
        f"{NEWEST_DATE}. See About the Data for per-source dates."
    )
    render_about_the_data()
