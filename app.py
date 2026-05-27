
import html
import json
import random
import time
import uuid
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
DEMO_DATA_PATH = PROJECT_ROOT / "dummy_demo_data.json"


def fake_processing_delay():
    time.sleep(random.uniform(8, 11))


st.set_page_config(
    page_title="Clinical KG Assistant",
    page_icon="🩺",
    layout="wide",
)


st.markdown(
    """
    <style>
    :root {
        --app-content-width: 980px;
        --app-side-padding: 2rem;
        --app-subtle-border: rgba(128, 128, 128, 0.20);
    }

    section.main > div.block-container,
    .main .block-container,
    div[data-testid="stAppViewContainer"] section[data-testid="stMain"] > div[data-testid="stMainBlockContainer"],
    div[data-testid="stMainBlockContainer"] {
        max-width: var(--app-content-width) !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-left: var(--app-side-padding) !important;
        padding-right: var(--app-side-padding) !important;
        padding-top: 0.75rem !important;
        padding-bottom: 8rem !important;
    }

    div[class*="st-key-top_header"] {
        position: sticky !important;
        top: 0 !important;
        z-index: 1000 !important;
        background: var(--background-color) !important;
        padding: 0.85rem 0 0.75rem 0 !important;
        margin-bottom: 1rem !important;
        border-bottom: 1px solid var(--app-subtle-border) !important;
    }

    div[class*="st-key-top_header"] h1 {
        margin-top: 0 !important;
        margin-bottom: 0.2rem !important;
    }

    div[class*="st-key-flag"] button {
        padding: 0.05rem 0.25rem !important;
        min-height: 1.15rem !important;
        height: 1.15rem !important;
        line-height: 1 !important;
        font-size: 0.68rem !important;
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        color: inherit !important;
    }

    div[class*="st-key-flag"] button:hover {
        background: rgba(128, 128, 128, 0.08) !important;
        border: none !important;
        color: inherit !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 0.85rem !important;
        border-color: rgba(128, 128, 128, 0.18) !important;
        background: rgba(128, 128, 128, 0.035) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(128, 128, 128, 0.32) !important;
        background: rgba(128, 128, 128, 0.055) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlock"] {
        row-gap: 0.45rem !important;
    }

    .candidate-title {
        font-size: 0.96rem;
        line-height: 1.25;
        font-weight: 650;
        margin-bottom: 0.15rem;
    }

    .relation-title {
        font-size: 0.91rem;
        line-height: 1.28;
        font-weight: 600;
        margin-bottom: 0.15rem;
    }

    .score-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 999px;
        padding: 0.14rem 0.46rem;
        font-size: 0.72rem;
        font-weight: 600;
        background: rgba(128, 128, 128, 0.16);
        border: 1px solid rgba(128, 128, 128, 0.16);
        white-space: nowrap;
    }

    .source-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.32rem;
        margin-top: 0.55rem;
        margin-bottom: 0.55rem;
        padding-bottom: 0.15rem;
    }

    .source-chip {
        display: inline-flex;
        border-radius: 999px;
        padding: 0.08rem 0.42rem;
        font-size: 0.70rem;
        line-height: 1.2;
        background: rgba(49, 130, 206, 0.12);
        border: 1px solid rgba(49, 130, 206, 0.18);
        text-decoration: none !important;
        max-width: 100%;
    }

    .muted-small {
        font-size: 0.72rem;
        opacity: 0.60;
        margin-top: 0.45rem;
        margin-bottom: 0.55rem;
        padding-bottom: 0.15rem;
    }

    .section-help {
        font-size: 0.86rem;
        opacity: 0.68;
        margin-top: -0.4rem;
        margin-bottom: 1rem;
    }

    .selected-count {
        font-size: 0.84rem;
        opacity: 0.72;
        margin-top: 0.25rem;
        margin-bottom: 0.75rem;
    }

    div[data-testid="stToggle"] label {
        min-height: 1.35rem !important;
    }

    div[role="dialog"] button[aria-label="Close"],
    div[data-testid="stDialog"] button[aria-label="Close"] {
        display: none !important;
    }

    div[data-testid="stBottom"],
    div[data-testid="stBottom"] > div,
    div[data-testid="stBottomBlockContainer"],
    .stChatFloatingInputContainer {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        left: 0 !important;
        right: 0 !important;
        transform: none !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stBottomBlockContainer"],
    div[data-testid="stBottom"] > div > div,
    .stChatFloatingInputContainer > div {
        width: min(var(--app-content-width), calc(100vw - 2 * var(--app-side-padding))) !important;
        max-width: min(var(--app-content-width), calc(100vw - 2 * var(--app-side-padding))) !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stBottomBlockContainer"] > div,
    div[data-testid="stChatInput"],
    div[data-testid="stChatInput"] > div {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    @media (max-width: 900px) {
        :root {
            --app-side-padding: 1rem;
        }

        .candidate-title,
        .relation-title {
            font-size: 0.9rem;
        }

        div[class*="st-key-demo_input_bar"] {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_demo_data():
    with open(DEMO_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_json(value):
    try:
        json.dumps(value)
        return value
    except Exception:
        return str(value)


def init_state():
    defaults = {
        "messages": [],
        "patient_note": None,
        "diagnosis_candidates": [],
        "selected_candidates": [],
        "selected_node_ids": [],
        "relation_candidates": [],
        "selected_relations": [],
        "nodes_confirmed": False,
        "relations_confirmed": False,
        "final_output": None,
        "payload": None,
        "errors": [],
        "request_id": None,
        "feedback_target": None,
        "feedback_log": [],
        "app_started": False,
        "pending_node_search": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_state():
    preserved_keys = set()
    for key in list(st.session_state.keys()):
        if key not in preserved_keys:
            del st.session_state[key]
    st.rerun()


def start_case():
    demo_data = load_demo_data()

    st.session_state.messages = [
        {
            "role": "user",
            "content": demo_data["patient_note"],
        }
    ]

    st.session_state.patient_note = demo_data["patient_note"]
    st.session_state.diagnosis_candidates = []
    st.session_state.selected_candidates = []
    st.session_state.selected_node_ids = []
    st.session_state.relation_candidates = []
    st.session_state.selected_relations = []
    st.session_state.nodes_confirmed = False
    st.session_state.relations_confirmed = False
    st.session_state.final_output = None
    st.session_state.payload = None
    st.session_state.errors = []
    st.session_state.feedback_target = None
    st.session_state.request_id = str(uuid.uuid4())
    st.session_state.app_started = True
    st.session_state.pending_node_search = True


def finish_node_search():
    demo_data = load_demo_data()
    st.session_state.diagnosis_candidates = demo_data.get("diagnosis_candidates", [])
    st.session_state.pending_node_search = False


def node_label(candidate):
    name = str(candidate.get("name") or candidate.get("canonical_name") or "").strip()
    label = str(candidate.get("label") or "").strip()

    if name and label:
        return f"{name} ({label})"

    return name or label or str(candidate.get("node_id", "Unknown node"))


def relation_label(relation):
    source = str(relation.get("source_name") or "").strip()
    relation_type = str(relation.get("type") or "").strip()
    target = str(relation.get("target_name") or "").strip()

    return f"{source} — {relation_type} — {target}"


def get_score(item):
    for key in ["llm_relevance", "relevance_score", "score"]:
        value = item.get(key)

        if value is None:
            continue

        try:
            return float(value)
        except Exception:
            continue

    return None


def compact_score_text(item):
    score = get_score(item)

    if score is None:
        return "N/A"

    return f"{score:.2f}"


def render_score_pill(item):
    st.markdown(
        f"<span class='score-pill'>Score {html.escape(compact_score_text(item))}</span>",
        unsafe_allow_html=True,
    )


def source_link_base_label(url):
    parsed = urlparse(str(url))
    path_parts = [part for part in parsed.path.split("/") if part]

    if not path_parts:
        return parsed.netloc or "source"

    return path_parts[-1]


def source_link_labels(urls):
    base_counts = {}
    labels = []

    for url in urls:
        base = source_link_base_label(url)
        base_counts[base] = base_counts.get(base, 0) + 1

        if base_counts[base] == 1:
            labels.append(base)
        else:
            labels.append(f"{base}{base_counts[base]}")

    return labels


def clean_source_urls(urls):
    clean_urls = []
    seen = set()

    for url in urls or []:
        url = str(url).strip()

        if not url or url in seen:
            continue

        seen.add(url)
        clean_urls.append(url)

    return clean_urls


def source_chips_html(urls, max_visible=3):
    clean_urls = clean_source_urls(urls)

    if not clean_urls:
        return "<div class='muted-small'>No source URL found.</div>"

    visible_urls = clean_urls[:max_visible]
    labels = source_link_labels(visible_urls)
    links = []

    for label, url in zip(labels, visible_urls):
        links.append(
            f"<a class='source-chip' href='{html.escape(url, quote=True)}' target='_blank'>"
            f"{html.escape(label)}</a>"
        )

    remaining = len(clean_urls) - len(visible_urls)

    if remaining > 0:
        links.append(f"<span class='source-chip'>+{remaining} more</span>")

    return "<div class='source-row'>" + "".join(links) + "</div>"


def node_source_urls(candidate, source_url_map):
    node_id = candidate.get("node_id")

    if node_id is None:
        return []

    return (
        source_url_map.get(str(node_id))
        or source_url_map.get(int(node_id), [])
        or candidate.get("source_urls")
        or []
    )


def clear_feedback_target():
    st.session_state.feedback_target = None


@st.dialog("Flag content")
def feedback_dialog():
    target = st.session_state.get("feedback_target")

    if not target:
        st.write("No feedback target selected.")
        if st.button("Close", key="feedback_dialog_close_empty"):
            clear_feedback_target()
            st.rerun()
        return

    feedback_key = target.get("feedback_key") or "default"

    st.caption(target.get("item_label") or "Selected item")

    feedback_text = st.text_area(
        "Explain what is wrong or should be improved",
        height=160,
        key=f"feedback_dialog_text_{feedback_key}",
    )

    button_cols = st.columns([0.42, 0.58], gap="small")

    with button_cols[0]:
        if st.button("Submit feedback", type="primary", key=f"submit_feedback_dialog_{feedback_key}"):
            if not feedback_text.strip():
                st.warning("Please write a short explanation first.")
                return

            st.session_state.feedback_log.append(
                {
                    "request_id": st.session_state.get("request_id"),
                    "item_type": target.get("item_type"),
                    "item_id": target.get("item_id"),
                    "item_label": target.get("item_label"),
                    "feedback_text": feedback_text.strip(),
                    "item_json": safe_json(target.get("item_json") or {}),
                }
            )

            clear_feedback_target()
            st.success("Feedback saved.")
            st.rerun()

    with button_cols[1]:
        if st.button("Close", key=f"close_feedback_dialog_{feedback_key}"):
            clear_feedback_target()
            st.rerun()


def feedback_button(item_type, item_id, item_label, item_json, key):
    clicked = st.button("🚩", key=key, help="Flag this item and explain what is wrong.")

    if clicked:
        st.session_state.feedback_target = {
            "item_type": item_type,
            "item_id": str(item_id) if item_id is not None else None,
            "item_label": item_label,
            "item_json": safe_json(item_json or {}),
            "feedback_key": str(uuid.uuid4()),
        }
        feedback_dialog()


def process_feedback_button(label, item_type, item_label, item_json, key):
    clicked = st.button(label, key=key, help="Flag this whole step and explain what went wrong.")

    if clicked:
        st.session_state.feedback_target = {
            "item_type": item_type,
            "item_id": None,
            "item_label": item_label,
            "item_json": safe_json(item_json or {}),
            "feedback_key": str(uuid.uuid4()),
        }
        feedback_dialog()


def render_section_header(title, feedback_label, item_type, item_label, item_json, key):
    left_col, right_col = st.columns([0.74, 0.26], gap="small")

    with left_col:
        st.subheader(title)

    with right_col:
        st.markdown("<div style='height: 0.35rem;'></div>", unsafe_allow_html=True)
        process_feedback_button(
            label=feedback_label,
            item_type=item_type,
            item_label=item_label,
            item_json=item_json,
            key=key,
        )


def render_node_candidate_card(candidate, idx, source_url_map, default_selected):
    candidate_label = node_label(candidate)

    with st.container(border=True):
        top_cols = st.columns([0.10, 0.64, 0.18, 0.08], gap="small")

        with top_cols[0]:
            selected = st.toggle(
                "Select node",
                value=default_selected,
                key=f"node_candidate_{idx}",
                label_visibility="collapsed",
            )

        with top_cols[1]:
            st.markdown(
                f"<div class='candidate-title'>{html.escape(candidate_label)}</div>",
                unsafe_allow_html=True,
            )

        with top_cols[2]:
            render_score_pill(candidate)

        with top_cols[3]:
            feedback_button(
                item_type="node",
                item_id=candidate.get("node_id"),
                item_label=candidate_label,
                item_json=candidate,
                key=f"flag_node_candidate_{candidate.get('node_id')}_{idx}",
            )

        st.markdown(
            source_chips_html(node_source_urls(candidate, source_url_map)),
            unsafe_allow_html=True,
        )

    return selected


def render_selected_node_card(candidate, idx, source_url_map):
    candidate_label = node_label(candidate)

    with st.container(border=True):
        top_cols = st.columns([0.74, 0.18, 0.08], gap="small")

        with top_cols[0]:
            st.markdown(
                f"<div class='candidate-title'>{html.escape(candidate_label)}</div>",
                unsafe_allow_html=True,
            )

        with top_cols[1]:
            render_score_pill(candidate)

        with top_cols[2]:
            feedback_button(
                item_type="node",
                item_id=candidate.get("node_id"),
                item_label=candidate_label,
                item_json=candidate,
                key=f"flag_selected_node_{candidate.get('node_id')}_{idx}",
            )

        st.markdown(
            source_chips_html(node_source_urls(candidate, source_url_map)),
            unsafe_allow_html=True,
        )


def render_relation_candidate_card(relation, idx, default_selected):
    rel_label = relation_label(relation)

    with st.container(border=True):
        top_cols = st.columns([0.10, 0.64, 0.18, 0.08], gap="small")

        with top_cols[0]:
            selected = st.toggle(
                "Select relation",
                value=default_selected,
                key=f"relation_candidate_{idx}",
                label_visibility="collapsed",
            )

        with top_cols[1]:
            st.markdown(
                f"<div class='relation-title'>{html.escape(rel_label)}</div>",
                unsafe_allow_html=True,
            )

        with top_cols[2]:
            render_score_pill(relation)

        with top_cols[3]:
            feedback_button(
                item_type="relation",
                item_id=relation.get("relationship_id"),
                item_label=rel_label,
                item_json=relation,
                key=f"flag_relation_candidate_{relation.get('relationship_id')}_{idx}",
            )

    return selected


def render_selected_relation_card(relation, idx):
    rel_label = relation_label(relation)

    with st.container(border=True):
        top_cols = st.columns([0.74, 0.18, 0.08], gap="small")

        with top_cols[0]:
            st.markdown(
                f"<div class='relation-title'>{html.escape(rel_label)}</div>",
                unsafe_allow_html=True,
            )

        with top_cols[1]:
            render_score_pill(relation)

        with top_cols[2]:
            feedback_button(
                item_type="relation",
                item_id=relation.get("relationship_id"),
                item_label=rel_label,
                item_json=relation,
                key=f"flag_selected_relation_{relation.get('relationship_id')}_{idx}",
            )


def selected_node_default_ids(demo_data):
    return {
        item.get("node_id")
        for item in demo_data.get("selected_candidates", [])
        if item.get("node_id") is not None
    }


def selected_relation_default_ids(demo_data):
    return {
        item.get("relationship_id")
        for item in demo_data.get("selected_relations", [])
        if item.get("relationship_id") is not None
    }


def get_selected_node_ids(selected_candidates):
    selected_node_ids = []
    seen = set()

    for item in selected_candidates:
        node_id = item.get("node_id")

        if node_id is not None and node_id not in seen:
            seen.add(node_id)
            selected_node_ids.append(node_id)

    return selected_node_ids



init_state()
demo_data = load_demo_data()

top_header = st.container(key="top_header")

with top_header:
    title_col, reset_col = st.columns([0.82, 0.18], gap="small")

    with title_col:
        st.title("Clinical KG Assistant")
        st.caption("Enter a patient note, choose relevant nodes, then choose relevant relations.")

    with reset_col:
        st.markdown("<div style='height: 1.25rem;'></div>", unsafe_allow_html=True)
        if st.button("Reset", key="reset_app"):
            reset_state()


user_input = st.chat_input("Paste patient note here...")

if user_input:
    start_case()
    st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if st.session_state.pending_node_search:
    with st.spinner("Searching the knowledge graph..."):
        fake_processing_delay()
        finish_node_search()
    st.rerun()


source_url_map = demo_data.get("source_url_map", {})

main_area = st.container()

with main_area:
    if st.session_state.selected_candidates:
        st.subheader("Selected nodes")
        st.markdown(
            "<div class='section-help'>Nodes currently included for relation expansion.</div>",
            unsafe_allow_html=True,
        )
        cols = st.columns(2, gap="medium")

        for idx, candidate in enumerate(st.session_state.selected_candidates):
            with cols[idx % 2]:
                render_selected_node_card(
                    candidate=candidate,
                    idx=idx,
                    source_url_map=source_url_map,
                )

    if st.session_state.selected_relations:
        st.subheader("Selected relations")
        st.markdown(
            "<div class='section-help'>Relations currently included in the final answer payload.</div>",
            unsafe_allow_html=True,
        )
        cols = st.columns(2, gap="medium")

        for idx, relation in enumerate(st.session_state.selected_relations):
            with cols[idx % 2]:
                render_selected_relation_card(relation=relation, idx=idx)

    if st.session_state.final_output:
        render_section_header(
            title="Weighted-KG answer",
            feedback_label="🚩 Flag output",
            item_type="final_output_step",
            item_label="Final Weighted-KG answer",
            item_json={
                "patient_note": st.session_state.patient_note,
                "selected_relations": st.session_state.selected_relations,
                "payload": st.session_state.payload,
                "final_output": st.session_state.final_output,
                "errors": st.session_state.errors,
            },
            key="process_feedback_final_output",
        )
        st.markdown(st.session_state.final_output)

        st.stop()

    if st.session_state.diagnosis_candidates and not st.session_state.nodes_confirmed:
        render_section_header(
            title="Select relevant nodes",
            feedback_label="🚩 Flag node search",
            item_type="node_search_step",
            item_label="Node search / diagnosis candidate retrieval",
            item_json={
                "patient_note": st.session_state.patient_note,
                "diagnosis_candidates": st.session_state.diagnosis_candidates,
                "candidate_count": len(st.session_state.diagnosis_candidates or []),
                "errors": st.session_state.errors,
            },
            key="process_feedback_node_search",
        )
        st.markdown(
            "<div class='section-help'>Review the suggested nodes. Toggle the ones that should be used for relation retrieval. Source links are kept as compact chips inside each card.</div>",
            unsafe_allow_html=True,
        )

        selected_indices = []
        cols = st.columns(2, gap="medium")
        default_node_ids = selected_node_default_ids(demo_data)

        for idx, candidate in enumerate(st.session_state.diagnosis_candidates):
            with cols[idx % 2]:
                default_selected = candidate.get("node_id") in default_node_ids
                selected = render_node_candidate_card(
                    candidate=candidate,
                    idx=idx,
                    source_url_map=source_url_map,
                    default_selected=default_selected,
                )

                if selected:
                    selected_indices.append(idx)

        st.markdown(
            f"<div class='selected-count'>{len(selected_indices)} node(s) selected</div>",
            unsafe_allow_html=True,
        )

        submitted = st.button(
            "Continue to relation selection",
            type="primary",
            key="continue_to_relation_selection",
        )

        if submitted:
            selected_candidates = [
                st.session_state.diagnosis_candidates[i]
                for i in selected_indices
            ]

            if not selected_candidates:
                st.error("Please select at least one node, or flag the node search if none of the suggestions are relevant.")
                st.stop()

            with st.spinner("Retrieving relation candidates..."):
                fake_processing_delay()
                st.session_state.selected_candidates = selected_candidates
                st.session_state.selected_node_ids = get_selected_node_ids(selected_candidates)
                st.session_state.relation_candidates = demo_data.get("relation_candidates", [])
                st.session_state.nodes_confirmed = True
            st.rerun()

        st.stop()

    if st.session_state.nodes_confirmed and not st.session_state.relations_confirmed:
        render_section_header(
            title="Select relevant relations",
            feedback_label="🚩 Flag relation search",
            item_type="relation_search_step",
            item_label="Relation search / relation candidate retrieval",
            item_json={
                "patient_note": st.session_state.patient_note,
                "selected_nodes": st.session_state.selected_candidates,
                "selected_node_ids": st.session_state.selected_node_ids,
                "relation_candidates": st.session_state.relation_candidates,
                "candidate_count": len(st.session_state.relation_candidates or []),
                "errors": st.session_state.errors,
            },
            key="process_feedback_relation_search",
        )
        st.markdown(
            "<div class='section-help'>Review the relation candidates. Toggle the relations that should be included in the Weighted-KG answer.</div>",
            unsafe_allow_html=True,
        )

        if not st.session_state.relation_candidates:
            st.warning("No relation candidates were found from the selected nodes.")

        selected_relation_indices = []
        cols = st.columns(2, gap="medium")
        default_relation_ids = selected_relation_default_ids(demo_data)

        for idx, relation in enumerate(st.session_state.relation_candidates):
            default_selected = relation.get("relationship_id") in default_relation_ids

            if not default_selected:
                default_selected = bool(relation.get("include_in_payload", False))

            if not default_selected:
                score = relation.get("llm_relevance")
                default_selected = float(score or 0) > 0

            with cols[idx % 2]:
                selected = render_relation_candidate_card(
                    relation=relation,
                    idx=idx,
                    default_selected=default_selected,
                )

                if selected:
                    selected_relation_indices.append(idx)

        st.markdown(
            f"<div class='selected-count'>{len(selected_relation_indices)} relation(s) selected</div>",
            unsafe_allow_html=True,
        )

        submitted = st.button(
            "Generate answer",
            type="primary",
            key="generate_answer",
        )

        if submitted:
            selected_relations = [
                st.session_state.relation_candidates[i]
                for i in selected_relation_indices
            ]

            if not selected_relations:
                st.error("Please select at least one relation, or flag the relation search if none of the suggestions are relevant.")
                st.stop()

            with st.spinner("Generating Weighted-KG answer..."):
                fake_processing_delay()
                st.session_state.selected_relations = selected_relations
                st.session_state.payload = demo_data.get("payload")
                st.session_state.final_output = demo_data.get("final_output")
                st.session_state.relations_confirmed = True
            st.rerun()

        st.stop()

