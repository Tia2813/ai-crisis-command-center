import streamlit as st
from components import summary_card, notification_card, section_header


def render():
    incidents = st.session_state.incidents
    active = [i for i in incidents if i["status"] == "Active"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        summary_card("Active Incidents", str(len(active)), "var(--critical)")
    with c2:
        summary_card("Rescue Teams", str(max(len(active) * 3, 4)), "var(--primary)")
    with c3:
        summary_card("Resources Deployed", str(max(len(active) * 7, 12)), "var(--accent)")
    with c4:
        avg = (
            round(sum(i.get("elapsed", 18) for i in incidents) / len(incidents), 1)
            if incidents else 18.4
        )
        summary_card("Avg. Response Time", f"{avg}s", "var(--warning)")

    section_header("Recent Notifications")
    if not st.session_state.notifications:
        st.markdown(
            "<div class='card' style='color:var(--text-dim);'>No notifications yet — "
            "generate a response plan from <b>New Incident</b> to see activity here.</div>",
            unsafe_allow_html=True,
        )
    else:
        for n in reversed(st.session_state.notifications[-6:]):
            notification_card(n["text"], n["time"])

    section_header("Active Incidents")
    if not active:
        st.markdown(
            "<div class='card' style='color:var(--text-dim);'>No active incidents right now. "
            "Nice and quiet.</div>",
            unsafe_allow_html=True,
        )
    else:
        for inc in active[:4]:
            cols = st.columns([3, 2, 2, 2])
            with cols[0]:
                st.markdown(f"**{inc['type']}** — {inc['location']}")
            with cols[1]:
                st.markdown(f"Severity: **{inc['severity']}**")
            with cols[2]:
                st.markdown(f"Reported: {inc['timestamp']}")
            with cols[3]:
                st.markdown(f"Status: {inc['status']}")
