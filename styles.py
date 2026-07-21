"""
Central design-system stylesheet for the Emergency Response Platform.
Injected once per page via `inject_css()`.
"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@500;600;700;800&display=swap');

:root {
  --bg: #0F172A;
  --card: #1E293B;
  --card-hover: #263449;
  --primary: #2563EB;
  --primary-light: #3B82F6;
  --success: #22C55E;
  --warning: #F59E0B;
  --critical: #EF4444;
  --accent: #06B6D4;
  --text: #E2E8F0;
  --text-dim: #94A3B8;
  --border: #334155;
  --radius: 16px;
}

html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
h1, h2, h3, .display-font { font-family: 'Poppins', sans-serif; }

/* App background */
.stApp {
  background: radial-gradient(circle at 20% 0%, #142038 0%, var(--bg) 45%) fixed;
  color: var(--text);
}

/* Hide default streamlit chrome we don't want, but keep the header itself
   so the sidebar expand/collapse arrow (inside it) still works. */
#MainMenu, footer {visibility: hidden; height: 0;}
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] {display: none;}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: #0B1223;
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.2rem; }

/* Buttons */
.stButton>button {
  background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  padding: 0.6rem 1.2rem;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  box-shadow: 0 2px 10px rgba(37, 99, 235, 0.25);
}
.stButton>button:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.4);
}
.stButton>button:active { transform: translateY(0); }

/* Sidebar nav buttons (secondary look) */
.nav-btn .stButton>button {
  background: transparent;
  box-shadow: none;
  color: var(--text-dim);
  text-align: left;
  justify-content: flex-start;
  width: 100%;
  font-weight: 500;
}
.nav-btn .stButton>button:hover {
  background: rgba(37, 99, 235, 0.12);
  color: white;
}
.nav-btn-active .stButton>button {
  background: rgba(37, 99, 235, 0.18) !important;
  color: white !important;
  border-left: 3px solid var(--primary);
}

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div, .stNumberInput input {
  background: var(--card) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 2px rgba(37,99,235,0.25) !important;
}

/* Expanders as cards */
div[data-testid="stExpander"] {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  margin-bottom: 14px;
  animation: fadeIn 0.4s ease;
}
div[data-testid="stExpander"] summary {
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  padding: 6px 4px;
}

/* Generic card class for raw HTML cards */
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.25);
  transition: transform 0.15s ease, border-color 0.15s ease;
  animation: fadeIn 0.5s ease;
}
.card:hover { transform: translateY(-2px); border-color: var(--primary); }

.metric-card { display: flex; flex-direction: column; gap: 6px; }
.metric-icon { font-size: 26px; }
.metric-value { font-family: 'Poppins', sans-serif; font-size: 28px; font-weight: 700; }
.metric-label { color: var(--text-dim); font-size: 13px; letter-spacing: 0.02em; }

/* Badges */
.badge {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 4px 12px; border-radius: 999px;
  font-size: 12px; font-weight: 600; letter-spacing: 0.02em;
}
.badge-critical { background: rgba(239,68,68,0.15); color: var(--critical); }
.badge-warning { background: rgba(245,158,11,0.15); color: var(--warning); }
.badge-success { background: rgba(34,197,94,0.15); color: var(--success); }
.badge-info { background: rgba(6,182,212,0.15); color: var(--accent); }

/* Top navbar */
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 4px 22px 4px; border-bottom: 1px solid var(--border);
  margin-bottom: 24px;
}
.topbar-logo { display: flex; align-items: center; gap: 10px; }
.topbar-logo-text { font-family:'Poppins',sans-serif; font-weight:700; font-size:19px; }
.topbar-right { display:flex; align-items:center; gap: 18px; color: var(--text-dim); }

/* Agent cards */
.agent-card { display:flex; flex-direction:column; gap:10px; height: 100%; }
.agent-icon { font-size: 34px; }
.agent-name { font-family:'Poppins',sans-serif; font-weight:700; font-size:17px; }
.agent-desc { color: var(--text-dim); font-size: 14px; line-height:1.5; }
.agent-resp { font-size: 13px; color: var(--text); }

/* Timeline */
.timeline-wrap { display:flex; overflow-x:auto; gap: 0; padding: 20px 4px; }
.timeline-step { min-width: 160px; text-align:center; position: relative; padding: 0 10px; }
.timeline-dot {
  width: 14px; height:14px; border-radius:50%;
  background: var(--primary); margin: 0 auto 10px auto;
  box-shadow: 0 0 0 4px rgba(37,99,235,0.2);
}
.timeline-line {
  position:absolute; top:6px; left:-50%; width:100%; height:2px; background: var(--border); z-index:-1;
}
.timeline-time { color: var(--accent); font-size:12px; font-weight:700; }
.timeline-title { font-size: 13px; margin-top:4px; color: var(--text); }

/* Notification card */
.notif-card {
  display:flex; align-items:center; gap:12px;
  background: var(--card); border: 1px solid var(--border); border-left: 3px solid var(--primary);
  border-radius: 12px; padding: 12px 16px; margin-bottom:10px;
  animation: fadeIn 0.4s ease;
}
.notif-time { color: var(--text-dim); font-size:12px; margin-left:auto; white-space:nowrap; }

/* Footer */
.app-footer {
  margin-top: 40px; padding: 18px 4px; border-top: 1px solid var(--border);
  display:flex; justify-content:space-between; color: var(--text-dim); font-size:12px; flex-wrap:wrap; gap:8px;
}

/* Login page */
.login-title { text-align:center; font-family:'Poppins',sans-serif; font-weight:800; font-size:24px; margin-top: 10px; }
.login-subtitle { text-align:center; color: var(--text-dim); font-size:13px; margin-bottom:24px; }
/* Style Streamlit's native bordered container (st.container(border=True)) as our card */
div[data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--card);
  border-radius: 20px !important;
  box-shadow: 0 20px 60px rgba(0,0,0,0.35);
}

/* Animations */
@keyframes fadeIn { from {opacity:0; transform: translateY(6px);} to {opacity:1; transform: translateY(0);} }

/* Section header */
.section-header {
  font-family:'Poppins',sans-serif; font-weight:700; font-size:20px; margin: 26px 0 14px 0;
  display:flex; align-items:center; gap:10px;
}

/* Map placeholder */
.map-placeholder {
  border-radius: var(--radius); border: 1px dashed var(--border);
  background: repeating-linear-gradient(45deg, #16213a, #16213a 10px, #142038 10px, #142038 20px);
  height: 320px; display:flex; align-items:center; justify-content:center;
  color: var(--text-dim); font-size:14px; flex-direction:column; gap:8px;
}
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)
