import os
import streamlit as st
from components import section_header


def render():
    section_header("Settings")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Account**")
    st.text_input("Email", value=st.session_state.user_email, disabled=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Preferences**")
    st.toggle("Dark mode", value=True, disabled=True, help="This platform is dark-themed by default.")
    st.toggle("Email me on new critical incidents", value=True)
    st.toggle("Desktop notifications", value=False)
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**API Configuration**")
    key_set = bool(os.environ.get("GEMINI_API_KEY"))
    status = "Configured" if key_set else "Not set — add GEMINI_API_KEY to your .env file"
    st.markdown(f"Gemini API Key: {status}")
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("")

    if st.button("Log out"):
        st.session_state.authenticated = False
        st.rerun()
