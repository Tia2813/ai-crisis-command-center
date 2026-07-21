import pandas as pd
import streamlit as st

from components import section_header


def render():
    section_header("Incident History")

    incidents = st.session_state.incidents
    if not incidents:
        st.markdown(
            "<div class='card' style='color:var(--text-dim);'>"
            "No incidents recorded yet.</div>",
            unsafe_allow_html=True,
        )
        return

    df = pd.DataFrame([
        {
            "ID": i["id"],
            "Type": i["type"],
            "Location": i["location"],
            "Severity": i["severity"],
            "Status": i["status"],
            "Reported": i["timestamp"],
            "Response Time (s)": i.get("elapsed", "—"),
        }
        for i in reversed(incidents)
    ])

    st.dataframe(df, width="stretch", hide_index=True)

    with st.expander("View a specific incident's full plan"):
        chosen = st.selectbox(
            "Select incident",
            options=[i["id"] for i in incidents],
            format_func=lambda x: next(
                f"{i['type']} — {i['location']} ({i['timestamp']})" for i in incidents if i["id"] == x
            ),
        )
        record = next(i for i in incidents if i["id"] == chosen)
        plan = record["plan"]
        st.markdown("**Risk summary:** " + plan["risk"].affected_area_summary)
        st.markdown("**Public alert:**")
        st.info(plan["comms"].public_alert_message)
