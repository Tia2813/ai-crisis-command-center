"""
AI-Crisis Command Center — Emergency Response Platform

Entry point: handles auth gating, sidebar navigation, and page routing.
Run with:  streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv

from styles import inject_css
from components import topbar, footer
from auth import render_login
from pages_ui import dashboard, new_incident, active_incidents, history, analytics, information, settings

load_dotenv()

st.set_page_config(
    page_title="AI-Crisis Command Center",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ---------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------
defaults = {
    "authenticated": False,
    "user_email": "",
    "current_page": "Dashboard",
    "incidents": [],       # list of generated incident records
    "notifications": [],   # list of {text, time}
    "last_plan_id": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------------------------------------------------------------
# Auth gate
# ---------------------------------------------------------------------
if not st.session_state.authenticated:
    render_login()
    st.stop()

# ---------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------
NAV_ITEMS = [
    "Dashboard",
    "New Incident",
    "Active Incidents",
    "Incident History",
    "Analytics",
    "Information",
    "Settings",
]

with st.sidebar:
    st.markdown(
        "<div style='padding: 4px 0 20px 0;'>"
        "<span style='font-family:Poppins,sans-serif; font-weight:700; font-size:17px;'>Crisis Command</span>"
        "</div>",
        unsafe_allow_html=True,
    )

    for label in NAV_ITEMS:
        is_active = st.session_state.current_page == label
        wrapper_class = "nav-btn-active" if is_active else "nav-btn"
        st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
        if st.button(label, key=f"nav_{label}", width="stretch"):
            st.session_state.current_page = label
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        f"<div style='font-size:13px; color:var(--text-dim);'>{st.session_state.user_email}</div>",
        unsafe_allow_html=True,
    )
    if st.button("Logout", width="stretch"):
        st.session_state.authenticated = False
        st.rerun()

# ---------------------------------------------------------------------
# Page routing
# ---------------------------------------------------------------------
PAGES = {
    "Dashboard": dashboard,
    "New Incident": new_incident,
    "Active Incidents": active_incidents,
    "Incident History": history,
    "Analytics": analytics,
    "Information": information,
    "Settings": settings,
}

topbar(st.session_state.user_email, st.session_state.current_page)
PAGES[st.session_state.current_page].render()
footer()
