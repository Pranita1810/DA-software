import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from db__.session import init_session, set_df, get_df
from pipeline.loader import load_uploaded_file, load_sample, clean_dataframe

st.set_page_config(page_title="Upload · DataPulse", page_icon="📁", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');
:root{--bg:#08090d;--surface:#0f1118;--card:#141720;--border:#1e2235;
      --accent:#00e5ff;--accent2:#7b61ff;--green:#00ffa3;--amber:#ffb647;
      --red:#ff4d6d;--text:#e8eaf0;--muted:#6b7280;
      --font-head:'Syne',sans-serif;--font-mono:'JetBrains Mono',monospace;}
html,body,[class*="css"]{font-family:var(--font-mono);background:var(--bg)!important;color:var(--text);}
[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border);}
[data-testid="metric-container"]{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px!important;}
[data-testid="metric-container"] label{color:var(--muted)!important;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:var(--accent)!important;font-family:var(--font-head);font-size:2rem!important;}
.stButton>button{background:transparent;border:1px solid var(--accent);color:var(--accent);
    font-family:var(--font-mono);font-size:12px;letter-spacing:1px;border-radius:6px;padding:8px 20px;transition:all .2s;}
.stButton>button:hover{background:var(--accent);color:var(--bg);}
[data-testid="stFileUploader"]{background:var(--card);border:1px dashed var(--border);border-radius:12px;padding:10px;}
hr{border-color:var(--border)!important;}
</style>
""", unsafe_allow_html=True)

init_session()

with st.sidebar:
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
        color:#00e5ff;letter-spacing:2px;padding:20px 0 30px">⚡ DATAPULSE</div>""",
        unsafe_allow_html=True)

st.markdown("""
<div style="padding:30px 0 10px">
    <span style="font-family:'Syne',sans-serif;font-size:30px;font-weight:800;">
        📁 Data Upload
    </span>
    <span style="font-size:12px;color:#6b7280;margin-left:14px;letter-spacing:1px;">
        INGEST
    </span>
</div>
""", unsafe_allow_html=True)

# ── Upload or sample ──────────────────────────────────────────────────────────
tab_up, tab_sample = st.tabs(["  UPLOAD FILE  ", "  SAMPLE DATA  "])

with tab_up:
    st.markdown("<br>", unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Drop your file here",
        type=["csv", "xlsx", "xls", "parquet", "json"],
        help="Supported: CSV, Excel, Parquet, JSON",
    )
    c1, c2 = st.columns(2)
    with c1:
        auto_clean = st.checkbox("Auto-clean on load", value=True)
    with c2:
        preview_rows = st.number_input("Preview rows", 5, 100, 10, step=5)

    if uploaded:
        with st.spinner("Loading…"):
            try:
                df = load_uploaded_file(uploaded)
                if auto_clean:
                    df = clean_dataframe(df)
                set_df(df, uploaded.name)
                st.success(f"✅ Loaded **{uploaded.name}** — {len(df):,} rows × {df.shape[1]} columns")
            except Exception as e:
                st.error(f"❌ {e}")

with tab_sample:
    st.markdown("<br>", unsafe_allow_html=True)
    sample_name = st.selectbox("Choose sample dataset", ["sales", "hr"])
    st.markdown("""
    <div style="background:#141720;border:1px solid #1e2235;border-radius:10px;padding:16px 20px;font-size:12px;color:#6b7280;">
        <b style="color:#00e5ff">sales</b> — 500 rows of regional sales with revenue, profit, units & CSAT<br>
        <b style="color:#7b61ff">hr</b>    — 300 rows of employee data with salary, tenure & performance
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Load Sample Dataset"):
        df = load_sample(sample_name)
        set_df(df, f"{sample_name}_sample.csv")
        st.success(f"✅ Loaded **{sample_name}** sample — {len(df):,} rows × {df.shape[1]} cols")

# ── Preview ───────────────────────────────────────────────────────────────────
st.markdown("---")
df = get_df()
if df is not None:
    st.markdown(f"""
    <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;
                margin-bottom:12px;">
        Active Dataset:
        <span style="color:#00e5ff">{st.session_state.get('df_name','—')}</span>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rows",    f"{df.shape[0]:,}")
    m2.metric("Columns", f"{df.shape[1]}")
    m3.metric("Numeric cols", str(df.select_dtypes("number").shape[1]))
    m4.metric("Missing cells", f"{df.isna().sum().sum():,}")

    st.markdown("<br>", unsafe_allow_html=True)

    c_left, c_right = st.columns([3, 1])
    with c_left:
        st.markdown("**DATA PREVIEW**", unsafe_allow_html=False)
        st.dataframe(df.head(int(preview_rows if 'preview_rows' in dir() else 10)),
                     use_container_width=True)
    with c_right:
        st.markdown("**DTYPES**", unsafe_allow_html=False)
        dtype_df = df.dtypes.reset_index()
        dtype_df.columns = ["column", "dtype"]
        st.dataframe(dtype_df, use_container_width=True, height=350)
else:
    st.info("No dataset loaded yet. Upload a file or load a sample above.")
