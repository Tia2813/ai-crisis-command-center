"""
Login page.

NOTE: This is a UI-layer mock login only — there is no real backend/user
database wired up. Any non-empty email + password combination logs you in.
If you need real authentication (hashed passwords, sessions, etc.), that's
a separate backend task — flag it and we can add it properly.
"""

import streamlit as st


def render_login():
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown(
            "<div class='login-title'>AI Crisis Command Center</div>"
            "<div class='login-subtitle'>AI-powered Multi-Agent Disaster Response Platform</div>",
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            email = st.text_input("Email", placeholder="you@agency.gov", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_pw")

            c1, c2 = st.columns([1, 1])
            with c1:
                st.checkbox("Remember me", key="remember_me")
            with c2:
                st.markdown(
                    "<div style='text-align:right; padding-top:8px;'>"
                    "<a href='#' style='color:var(--accent); font-size:13px; text-decoration:none;'>Forgot password?</a>"
                    "</div>",
                    unsafe_allow_html=True,
                )

            login_clicked = st.button("Login", width="stretch")

        st.markdown(
            "<div style='text-align:center; margin-top:14px; color:var(--text-dim); font-size:13px;'>"
            "New here? <a href='#' style='color:var(--accent); text-decoration:none;'>Sign up</a></div>",
            unsafe_allow_html=True,
        )

        if login_clicked:
            if email.strip() and password.strip():
                st.session_state.authenticated = True
                st.session_state.user_email = email.strip()
                st.rerun()
            else:
                st.error("Please enter both email and password.")
