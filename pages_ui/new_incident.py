import time
import uuid
from datetime import datetime

import streamlit as st

from components import section_header, severity_badge, timeline, map_placeholder
from crew import run_pipeline

INCIDENT_TYPES = [
    "Earthquake", "Fire", "Flood", "Tsunami", "Building Collapse",
    "Chemical Leak", "Cyclone", "Landslide", "Other",
]

DEFAULT_TIMELINE = [
    ("0-10 min", "Emergency Alert"),
    ("10-20 min", "Deploy Response Teams"),
    ("20-45 min", "Medical Evacuation"),
    ("45-90 min", "Infrastructure Inspection"),
    ("2 Hours", "Recovery Phase"),
]


def _build_report_text(incident_type, location, severity, description, lat, lng):
    parts = [f"Incident type: {incident_type}.", f"Location: {location}."]
    if severity:
        parts.append(f"Reporter-assessed severity: {severity}.")
    if lat and lng:
        parts.append(f"GPS coordinates: {lat}, {lng}.")
    parts.append(description)
    return " ".join(p for p in parts if p)


def render():
    section_header("New Incident Report")

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            incident_type = st.selectbox("Incident Type", INCIDENT_TYPES)
        with c2:
            location = st.text_input("Location", placeholder="e.g. Sector 12, riverside colony")

        c3, c4 = st.columns(2)
        with c3:
            severity = st.selectbox("Severity", ["Low", "Moderate", "High", "Critical"], index=2)
        with c4:
            gps = st.text_input("GPS Coordinates (optional)", placeholder="lat, lng")

        description = st.text_area(
            "Description",
            height=150,
            placeholder="Describe what's happening on the ground — hazards, people affected, "
                        "access issues, anything relevant...",
        )

        c5, c6 = st.columns(2)
        with c5:
            image = st.file_uploader("Upload Image (optional)", type=["png", "jpg", "jpeg"])
        with c6:
            video = st.file_uploader("Upload Video (optional)", type=["mp4", "mov"])

        if image is not None:
            st.image(image, caption="Attached image (for records — not analyzed by the AI yet)", width=220)
        if video is not None:
            st.caption(f"Video attached: {video.name} (stored for records — not analyzed by the AI yet)")

        generate_clicked = st.button("Generate Plan", width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    if generate_clicked:
        if not description.strip() or not location.strip():
            st.warning("Please fill in at least Location and Description before generating a plan.")
            return

        lat, lng = "", ""
        if gps and "," in gps:
            lat, lng = [x.strip() for x in gps.split(",", 1)]

        report_text = _build_report_text(incident_type, location, severity, description, lat, lng)

        with st.spinner("Running the 5-agent pipeline (Risk, Logistics, Routes, Triage, Comms)..."):
            start = time.time()
            try:
                risk, resources, routes, triage, comms = run_pipeline(report_text)
                elapsed = round(time.time() - start, 1)
            except Exception as e:
                st.error(f"Pipeline failed: {e}")
                return

        record = {
            "id": str(uuid.uuid4())[:8],
            "type": incident_type,
            "location": location,
            "severity": severity,
            "timestamp": datetime.now().strftime("%d %b, %H:%M"),
            "status": "Active",
            "elapsed": elapsed,
            "plan": {
                "risk": risk, "resources": resources, "routes": routes,
                "triage": triage, "comms": comms,
            },
        }
        st.session_state.incidents.append(record)
        st.session_state.notifications.append({
            "text": f"New {incident_type} report — {location}",
            "time": "just now",
        })
        st.session_state.last_plan_id = record["id"]
        st.success(f"Response plan generated in {elapsed}s")

    # Show the most recently generated plan (if any) below the form
    last_id = st.session_state.get("last_plan_id")
    if last_id:
        record = next((i for i in st.session_state.incidents if i["id"] == last_id), None)
        if record:
            _render_response(record)


def _render_response(record):
    plan = record["plan"]
    risk, resources, routes, triage, comms = (
        plan["risk"], plan["resources"], plan["routes"], plan["triage"], plan["comms"]
    )

    section_header("Situation Summary")
    st.markdown(
        f"""<div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div><b>{record['type']}</b> — {record['location']}</div>
          {severity_badge(risk.severity_level)}
        </div>
        <div style="color:var(--text-dim);">{risk.affected_area_summary}</div>
        </div>""",
        unsafe_allow_html=True,
    )

    with st.expander("Risk Assessment", expanded=True):
        st.markdown(f"**Incident type:** {risk.incident_type}")
        st.markdown("**Key hazards:**")
        for h in risk.key_hazards:
            st.markdown(f"- {h}")
        st.markdown("**Immediate priorities:**")
        for p in risk.immediate_priorities:
            st.checkbox(p, key=f"pri_{record['id']}_{p}")

    with st.expander("Resource Allocation"):
        if resources.resources:
            for r in resources.resources:
                st.markdown(
                    f"**{r.resource}** — {r.quantity} → {r.assigned_location} "
                    f"({severity_badge(r.priority) if r.priority in ('Critical','High','Moderate','Low') else r.priority})",
                    unsafe_allow_html=True,
                )
        if resources.notes:
            st.caption(resources.notes)

    with st.expander("Evacuation Routes"):
        st.markdown("**Evacuation routes:**")
        for r in routes.evacuation_routes:
            st.markdown(f"- {r.origin} → {r.destination} ({r.mode}) — {r.status}. {r.notes or ''}")
        st.markdown("**Rescue access routes:**")
        for r in routes.rescue_access_routes:
            st.markdown(f"- {r.origin} → {r.destination} ({r.mode}) — {r.status}. {r.notes or ''}")
        map_placeholder(record["location"])

    with st.expander("Medical Triage"):
        for z in triage.triage_zones:
            st.markdown(f"- **{z.zone_name}** — {z.condition}. Action: {z.recommended_action}")
        st.markdown("**Medical supply priorities:**")
        for m in triage.medical_supply_priorities:
            st.markdown(f"- {m}")

    with st.expander("Public Communication"):
        st.info(comms.public_alert_message)
        st.markdown("**Channels:** " + ", ".join(comms.recommended_channels))
        st.markdown("**Dos and don'ts:**")
        for d in comms.key_dos_and_donts:
            st.markdown(f"- {d}")

    with st.expander("Execution Timeline"):
        timeline(DEFAULT_TIMELINE)

    with st.expander("Live Progress"):
        st.progress(35, text="Response in progress — resources en route")
