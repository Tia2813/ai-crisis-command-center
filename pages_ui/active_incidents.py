import streamlit as st
from components import section_header, severity_badge


def render():
    section_header("Active Incidents")

    active = [i for i in st.session_state.incidents if i["status"] == "Active"]

    if not active:
        st.markdown(
            "<div class='card' style='color:var(--text-dim);'>"
            "No active incidents. Go to <b>New Incident</b> to report one.</div>",
            unsafe_allow_html=True,
        )
        return

    for inc in reversed(active):
        with st.expander(f"{inc['type']} — {inc['location']}  ·  {inc['timestamp']}"):
            top = st.columns([2, 2, 2, 1])
            top[0].markdown(f"**Severity:** {severity_badge(inc['severity'])}", unsafe_allow_html=True)
            top[1].markdown(f"**Reported:** {inc['timestamp']}")
            top[2].markdown(f"**Response time:** {inc.get('elapsed', '—')}s")
            resolve = top[3].button("Resolve", key=f"resolve_{inc['id']}")

            plan = inc["plan"]
            st.markdown("**Risk summary:** " + plan["risk"].affected_area_summary)
            st.markdown("**Public alert:**")
            st.info(plan["comms"].public_alert_message)

            if resolve:
                inc["status"] = "Resolved"
                st.session_state.notifications.append({
                    "text": f"{inc['type']} at {inc['location']} marked resolved",
                    "time": "just now",
                })
                st.rerun()
