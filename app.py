"""
AI-Crisis Command Center — Streamlit Dashboard

Takes a single unstructured incident report and runs it through a 5-agent
CrewAI pipeline (Risk Analyst -> Logistics Lead -> Route Planner ->
Triage Director -> Communications Officer), then renders the structured
output as checklists, tables, and a public alert brief.

Run with:
    streamlit run app.py
"""

import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from crew import run_pipeline

load_dotenv()

st.set_page_config(
    page_title="AI-Crisis Command Center",
    page_icon="🚨",
    layout="wide",
)

# ---------------------------------------------------------------------
# Session state: cache the last result so Streamlit re-renders (widget
# interactions, etc.) don't silently re-trigger paid API calls.
# ---------------------------------------------------------------------
if "plan" not in st.session_state:
    st.session_state.plan = None
if "last_report" not in st.session_state:
    st.session_state.last_report = ""

st.title("🚨 AI-Crisis Command Center")
st.caption(
    "Multi-agent pipeline (CrewAI + Gemini) that turns a raw incident report "
    "into a structured emergency response plan."
)

with st.sidebar:
    st.header("About")
    st.write(
        "Five agents run in sequence, each handing structured context to the next:\n\n"
        "1. **Risk Analyst**\n"
        "2. **Logistics Lead**\n"
        "3. **Route Planner**\n"
        "4. **Triage Director**\n"
        "5. **Communications Officer**"
    )
    st.divider()
    st.caption("Set `GEMINI_API_KEY` in a `.env` file before running.")

incident_report = st.text_area(
    "Incident report (raw, unstructured field input)",
    height=180,
    placeholder=(
        "e.g. Heavy rainfall since last night has flooded the low-lying areas "
        "near Sector 12. Reports of 30+ families stranded on rooftops, one "
        "collapsed bridge blocking the main access road, and a hospital "
        "reporting rising water in its ground floor ward..."
    ),
    value=st.session_state.last_report,
)

run_clicked = st.button("Generate Response Plan", type="primary", use_container_width=True)

if run_clicked:
    if not incident_report.strip():
        st.warning("Please enter an incident report before generating a plan.")
    else:
        st.session_state.last_report = incident_report
        start = time.time()
        with st.spinner("Running 5-agent pipeline..."):
            try:
                risk, resources, routes, triage, comms = run_pipeline(incident_report)
                st.session_state.plan = {
                    "risk": risk,
                    "resources": resources,
                    "routes": routes,
                    "triage": triage,
                    "comms": comms,
                    "elapsed": round(time.time() - start, 1),
                }
            except Exception as e:
                st.session_state.plan = None
                st.error(f"Pipeline failed: {e}")

plan = st.session_state.plan

if plan:
    st.success(f"Response plan generated in {plan['elapsed']}s")

    tabs = st.tabs(
        ["🧭 Risk Assessment", "📦 Resources", "🛣️ Routes", "🏥 Triage", "📢 Public Alert"]
    )

    # --- Risk Assessment ---
    with tabs[0]:
        risk = plan["risk"]
        col1, col2 = st.columns(2)
        col1.metric("Incident Type", risk.incident_type)
        col2.metric("Severity", risk.severity_level)
        st.subheader("Affected Area")
        st.write(risk.affected_area_summary)
        st.subheader("Key Hazards")
        for h in risk.key_hazards:
            st.markdown(f"- {h}")
        st.subheader("Immediate Priorities (Checklist)")
        for p in risk.immediate_priorities:
            st.checkbox(p, key=f"priority_{p}")

    # --- Resources ---
    with tabs[1]:
        res = plan["resources"]
        if res.resources:
            df = pd.DataFrame([r.model_dump() for r in res.resources])
            st.dataframe(df, use_container_width=True, hide_index=True)
        if res.notes:
            st.caption(res.notes)

    # --- Routes ---
    with tabs[2]:
        routes = plan["routes"]
        st.subheader("Evacuation Routes")
        if routes.evacuation_routes:
            df_evac = pd.DataFrame([r.model_dump() for r in routes.evacuation_routes])
            st.dataframe(df_evac, use_container_width=True, hide_index=True)
        st.subheader("Rescue Access Routes")
        if routes.rescue_access_routes:
            df_rescue = pd.DataFrame([r.model_dump() for r in routes.rescue_access_routes])
            st.dataframe(df_rescue, use_container_width=True, hide_index=True)

    # --- Triage ---
    with tabs[3]:
        triage = plan["triage"]
        st.subheader("Triage Zones")
        if triage.triage_zones:
            df_triage = pd.DataFrame([z.model_dump() for z in triage.triage_zones])
            st.dataframe(df_triage, use_container_width=True, hide_index=True)
        st.subheader("Medical Supply Priorities")
        for m in triage.medical_supply_priorities:
            st.markdown(f"- {m}")

    # --- Comms ---
    with tabs[4]:
        comms = plan["comms"]
        st.subheader("Public Alert Message")
        st.info(comms.public_alert_message)
        st.subheader("Recommended Channels")
        for c in comms.recommended_channels:
            st.markdown(f"- {c}")
        st.subheader("Key Do's and Don'ts")
        for d in comms.key_dos_and_donts:
            st.markdown(f"- {d}")
else:
    st.info("Enter an incident report above and click **Generate Response Plan** to begin.")
