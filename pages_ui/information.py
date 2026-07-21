import streamlit as st
from components import agent_card, section_header

AGENTS = [
    {
        "name": "Risk Analyst",
        "desc": "Analyzes the incident severity and identifies immediate risks.",
        "responsibilities": [
            "Classify incident type and severity",
            "Identify key hazards",
            "Set immediate priorities",
        ],
    },
    {
        "name": "Logistics Lead",
        "desc": "Plans rescue resources and equipment allocation.",
        "responsibilities": [
            "Determine required personnel & vehicles",
            "Allocate supplies to locations",
            "Balance scarce resources by priority",
        ],
    },
    {
        "name": "Route Planner",
        "desc": "Finds the safest and fastest rescue and evacuation routes.",
        "responsibilities": [
            "Plan civilian evacuation routes",
            "Plan rescue-team access routes",
            "Flag congested or blocked roads",
        ],
    },
    {
        "name": "Triage Director",
        "desc": "Prioritizes victims and medical response based on urgency.",
        "responsibilities": [
            "Define medical triage zones",
            "Set medical supply priorities",
            "Coordinate with resource allocation",
        ],
    },
    {
        "name": "Communications Officer",
        "desc": "Creates public alerts and communication briefs.",
        "responsibilities": [
            "Draft ready-to-broadcast public alerts",
            "Recommend communication channels",
            "List key dos and don'ts for the public",
        ],
    },
]


def render():
    section_header("AI Agents")
    st.caption(
        "Five specialized agents run sequentially, each passing structured context to the next — "
        "turning one raw incident report into a complete response plan."
    )

    cols = st.columns(3)
    for i, agent in enumerate(AGENTS):
        with cols[i % 3]:
            agent_card(agent["name"], agent["desc"], agent["responsibilities"])
            st.write("")
