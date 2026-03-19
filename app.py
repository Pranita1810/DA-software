import streamlit as st
from db__.session import init_session

st.set_page_config(
    page_title="DataPulse Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #08090d;
    --surface:   #0f1118;
    --card:      #141720;
    --border:    #1e2235;
    --accent:    #00e5ff;
    --accent2:   #7b61ff;
    --green:     #00ffa3;
    --amber:     #ffb647;
    --red:       #ff4d6d;
    --text:      #e8eaf0;
    --muted:     #6b7280;
    --font-head: 'Syne', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: var(--font-mono);
    background-color: var(--bg) !important;
    color: var(--text);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: var(--text) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px !important;
}
[data-testid="metric-container"] label { color: var(--muted) !important; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--accent) !important; font-family: var(--font-head); font-size: 2rem !important; }
[data-testid="metric-container"] [data-testid="stMetricDelta"] svg { display: inline; }

/* ── Buttons ── */
.stButton > button {
    background: transparent;
    border: 1px solid var(--accent);
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 12px;
    letter-spacing: 1px;
    border-radius: 6px;
    padding: 8px 20px;
    transition: all .2s;
}
.stButton > button:hover {
    background: var(--accent);
    color: var(--bg);
    box-shadow: 0 0 20px rgba(0,229,255,.3);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: transparent;
    border-bottom: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--muted);
    font-family: var(--font-mono);
    font-size: 12px;
    letter-spacing: 1px;
    border-radius: 4px 4px 0 0;
    padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: var(--card) !important;
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* ── Selectbox / input ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: var(--font-mono);
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: var(--font-mono);
}

/* ── DataFrame ── */
.stDataFrame { border: 1px solid var(--border); border-radius: 8px; }
iframe[title="st_aggrid"] { border: none; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--card);
    border: 1px dashed var(--border);
    border-radius: 12px;
    padding: 10px;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Plotly charts background ── */
.js-plotly-plot .plotly .main-svg { background: transparent !important; }

/* ── Toast / alerts ── */
.stAlert { background: var(--card); border-left: 3px solid var(--accent); border-radius: 6px; }

/* ── Progress bar ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session ─────────────────────────────────────────────────────────────────
init_session()

# ── Sidebar brand ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 0 30px">
        <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
                    color:#00e5ff;letter-spacing:2px;">⚡ DATAPULSE</div>
        <div style="font-size:10px;color:#6b7280;letter-spacing:3px;margin-top:2px;">
            ANALYTICS PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:10px;color:#6b7280;letter-spacing:2px;margin-bottom:12px;">NAVIGATION</div>
    """, unsafe_allow_html=True)

# ── Home page ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 40px 0 20px">
    <div style="font-family:'Syne',sans-serif;font-size:48px;font-weight:800;
                line-height:1.1;letter-spacing:-1px;">
        Data <span style="color:#00e5ff;">Intelligence</span><br>
        at your fingertips.
    </div>
    <div style="color:#6b7280;font-size:14px;margin-top:16px;letter-spacing:.5px;">
        Upload · Explore · Analyse · Visualise · Report
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Nav cards ────────────────────────────────────────────────────────────────
cols = st.columns(5)
pages = [
    ("📊", "Dashboard",      "KPI overview & live metrics",   "#00e5ff"),
    ("📁", "Data Upload",    "CSV / Excel / Parquet ingestion","#7b61ff"),
    ("🔍", "EDA",            "Auto exploratory analysis",      "#00ffa3"),
    ("📈", "Visualisations", "Interactive chart builder",      "#ffb647"),
    ("📋", "Reports",        "Export PDF / Excel reports",     "#ff4d6d"),
]
for col, (icon, title, desc, color) in zip(cols, pages):
    with col:
        st.markdown(f"""
        <div style="background:#141720;border:1px solid #1e2235;border-radius:14px;
                    padding:24px 18px;cursor:pointer;transition:all .2s;
                    border-top:3px solid {color};">
            <div style="font-size:28px;margin-bottom:10px">{icon}</div>
            <div style="font-family:'Syne',sans-serif;font-weight:700;
                        font-size:14px;color:{color};letter-spacing:.5px">{title}</div>
            <div style="font-size:11px;color:#6b7280;margin-top:6px;line-height:1.5">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Quick status ────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'Syne',sans-serif;font-size:11px;
            color:#6b7280;letter-spacing:2px;margin-bottom:16px;">SYSTEM STATUS</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Datasets Loaded",  st.session_state.get("dataset_count", 0),  "ready")
c2.metric("Rows Processed",   st.session_state.get("rows_processed", 0), "records")
c3.metric("Charts Created",   st.session_state.get("chart_count", 0),    "plots")
c4.metric("Reports Exported", st.session_state.get("report_count", 0),   "files")

st.markdown("---")
st.markdown("""
<div style="font-size:10px;color:#3a3f52;text-align:center;padding:10px 0">
    ⚡ DATAPULSE v1.0 · Built with Streamlit · © 2026
</div>
""", unsafe_allow_html=True)
