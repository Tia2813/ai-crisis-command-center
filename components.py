"""Reusable HTML component renderers for the Emergency Response Platform UI."""

import streamlit as st

SEVERITY_BADGE = {
    "Critical": "badge-critical",
    "High": "badge-critical",
    "Moderate": "badge-warning",
    "Low": "badge-success",
}


def topbar(user_email: str, page_title: str):
    st.markdown(
        f"""
        <div class="topbar">
          <div class="topbar-logo">
            <span class="topbar-logo-text">{page_title}</span>
          </div>
          <div class="topbar-right">
            <span>{user_email}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def summary_card(label: str, value: str, color: str = "var(--primary)"):
    st.markdown(
        f"""
        <div class="card metric-card" style="border-top:3px solid {color};">
          <div class="metric-value">{value}</div>
          <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def severity_badge(severity: str) -> str:
    cls = SEVERITY_BADGE.get(severity, "badge-info")
    return f'<span class="badge {cls}">{severity}</span>'


def agent_card(name: str, desc: str, responsibilities: list, status: str = "Online"):
    resp_html = "".join(f"<li class='agent-resp'>{r}</li>" for r in responsibilities)
    st.markdown(
        f"""
        <div class="card agent-card">
          <div class="agent-name">{name}</div>
          <div class="agent-desc">{desc}</div>
          <ul style="margin:4px 0 0 18px; padding:0;">{resp_html}</ul>
          <span class="badge badge-success" style="margin-top:auto; width:fit-content;">{status}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def notification_card(text: str, time: str):
    st.markdown(
        f"""
        <div class="notif-card">
          <span>{text}</span>
          <span class="notif-time">{time}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def timeline(steps: list):
    """steps: list of (time_label, title) tuples"""
    items = ""
    for i, (t, title) in enumerate(steps):
        line = '<div class="timeline-line"></div>' if i > 0 else ""
        items += f"""
        <div class="timeline-step">
          {line}
          <div class="timeline-dot"></div>
          <div class="timeline-time">{t}</div>
          <div class="timeline-title">{title}</div>
        </div>
        """
    st.markdown(f'<div class="timeline-wrap">{items}</div>', unsafe_allow_html=True)


def map_placeholder(location: str = ""):
    st.markdown(
        f"""
        <div class="map-placeholder">
          <div>Map view — incident location, routes, hospitals & shelters</div>
          <div style="color:var(--accent); font-weight:600;">{location or "Location pending"}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer():
    st.markdown(
        """
        <div class="app-footer">
          <span>v1.0.0 · AI-Crisis Command Center</span>
          <span>System Status: Operational</span>
          <span>Last Updated: Just now</span>
          <span>Support: support@example.com</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
