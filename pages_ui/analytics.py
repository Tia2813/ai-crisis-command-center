from collections import Counter

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components import section_header

PLOTLY_TEMPLATE = "plotly_dark"
COLOR_SEQ = ["#2563EB", "#06B6D4", "#22C55E", "#F59E0B", "#EF4444", "#8B5CF6"]

DEMO_TYPES = {"Flood": 8, "Earthquake": 5, "Fire": 4, "Chemical Leak": 2, "Cyclone": 3}
DEMO_SEVERITY = {"Critical": 4, "High": 7, "Moderate": 8, "Low": 3}
DEMO_MONTHLY = {"Feb": 3, "Mar": 5, "Apr": 4, "May": 7, "Jun": 6, "Jul": 9}


def _style(fig):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E2E8F0"),
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig


def render():
    section_header("Analytics")

    incidents = st.session_state.incidents
    is_demo = len(incidents) == 0
    if is_demo:
        st.caption("Showing demo data — analytics will reflect real incidents as you generate plans.")

    type_counts = Counter(i["type"] for i in incidents) if incidents else DEMO_TYPES
    severity_counts = Counter(i["severity"] for i in incidents) if incidents else DEMO_SEVERITY

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Incident Types**")
        fig = px.pie(
            names=list(type_counts.keys()), values=list(type_counts.values()),
            color_discrete_sequence=COLOR_SEQ, hole=0.45,
        )
        st.plotly_chart(_style(fig), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Severity Distribution**")
        fig = px.bar(
            x=list(severity_counts.keys()), y=list(severity_counts.values()),
            color=list(severity_counts.keys()),
            color_discrete_sequence=COLOR_SEQ,
        )
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(_style(fig), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Monthly Responses**")
        months = list(DEMO_MONTHLY.keys())
        values = list(DEMO_MONTHLY.values())
        fig = go.Figure(go.Scatter(x=months, y=values, mode="lines+markers",
                                    line=dict(color="#06B6D4", width=3)))
        st.plotly_chart(_style(fig), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Average Rescue Time**")
        times = [i.get("elapsed") for i in incidents if i.get("elapsed")] or [22, 18, 25, 19, 21]
        fig = px.line(y=times, markers=True, color_discrete_sequence=["#F59E0B"])
        fig.update_layout(xaxis_title="Run #", yaxis_title="Seconds", showlegend=False)
        st.plotly_chart(_style(fig), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    with c5:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Resource Usage**")
        resources = {"Fire Trucks": 12, "Ambulances": 18, "Helicopters": 3, "Rescue Teams": 9, "Comms Vans": 5}
        fig = px.bar(x=list(resources.values()), y=list(resources.keys()), orientation="h",
                     color_discrete_sequence=["#2563EB"])
        fig.update_layout(xaxis_title=None, yaxis_title=None)
        st.plotly_chart(_style(fig), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with c6:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Mission Success Rate**")
        success_rate = 92 if is_demo else round(
            100 * len([i for i in incidents if i["status"] == "Resolved"]) / max(len(incidents), 1)
        )
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=success_rate,
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#22C55E"},
                "bgcolor": "rgba(0,0,0,0)",
            },
            number={"suffix": "%"},
        ))
        st.plotly_chart(_style(fig), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)
