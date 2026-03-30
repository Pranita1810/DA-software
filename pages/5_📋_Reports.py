import streamlit as st
import pandas as pd
import io
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from db__.session import init_session, get_df, set_df
from pipeline.loader import load_sample
from analysis.eda import summary_stats, full_missing_report, outlier_summary, correlation_matrix

st.set_page_config(page_title="Reports · DataPulse", page_icon="📋", layout="wide")
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
.stButton>button{background:transparent;border:1px solid var(--accent);color:var(--accent);font-family:var(--font-mono);font-size:12px;letter-spacing:1px;border-radius:6px;padding:8px 20px;transition:all .2s;}
.stButton>button:hover{background:var(--accent);color:var(--bg);}
hr{border-color:var(--border)!important;}
</style>
""", unsafe_allow_html=True)

init_session()
df = get_df()

with st.sidebar:
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
        color:#00e5ff;letter-spacing:2px;padding:20px 0 30px">⚡ DATAPULSE</div>""", unsafe_allow_html=True)
    if df is None:
        df = load_sample("sales"); set_df(df, "sales_sample.csv")

st.markdown("""
<div style="padding:30px 0 10px">
    <span style="font-family:'Syne',sans-serif;font-size:30px;font-weight:800;">
        📋 Reports
    </span>
    <span style="font-size:12px;color:#6b7280;margin-left:14px;letter-spacing:1px;">
        EXPORT
    </span>
</div>
""", unsafe_allow_html=True)

# ── Report config ─────────────────────────────────────────────────────────────
with st.expander("⚙️  Report Options", expanded=True):
    c1, c2 = st.columns(2)
    with c1:
        report_title  = st.text_input("Report title", "DataPulse Analytics Report")
        include_stats = st.checkbox("Summary statistics", True)
        include_miss  = st.checkbox("Missing data profile", True)
    with c2:
        include_corr  = st.checkbox("Correlation matrix", True)
        include_out   = st.checkbox("Outlier summary", True)
        include_raw   = st.checkbox("Raw data (first 200 rows)", False)

# ── Build report dict ─────────────────────────────────────────────────────────
report_sections = {}
if include_stats: report_sections["Summary Statistics"]   = summary_stats(df)
if include_miss:  report_sections["Missing Data Profile"] = full_missing_report(df)
if include_corr:
    c = correlation_matrix(df)
    if not c.empty: report_sections["Correlation Matrix"] = c
if include_out:   report_sections["Outlier Summary"]       = outlier_summary(df)
if include_raw:   report_sections["Raw Data (first 200)"]  = df.head(200)

# ── Preview ───────────────────────────────────────────────────────────────────
st.markdown("---")
for section, data in report_sections.items():
    with st.expander(f"📄 {section}", expanded=False):
        st.dataframe(data, use_container_width=True)

# ── Export as Excel ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;
            margin-bottom:16px;">Export Report</div>
""", unsafe_allow_html=True)

c_excel, c_csv, c_md = st.columns(3)

# Excel export
with c_excel:
    if st.button("📥  Export Excel"):
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            for sheet_name, data in report_sections.items():
                safe_name = sheet_name[:31]
                data.reset_index().to_excel(writer, sheet_name=safe_name, index=False)
        buf.seek(0)
        st.download_button(
            "⬇️  Download .xlsx",
            data=buf.getvalue(),
            file_name="datapulse_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        st.session_state["report_count"] = st.session_state.get("report_count", 0) + 1

# CSV export
with c_csv:
    if st.button("📥  Export CSV"):
        buf = io.StringIO()
        for section, data in report_sections.items():
            buf.write(f"\n\n=== {section} ===\n")
            data.reset_index().to_csv(buf, index=False)
        st.download_button(
            "⬇️  Download .csv",
            data=buf.getvalue(),
            file_name="datapulse_report.csv",
            mime="text/csv",
        )

# Markdown report
with c_md:
    if st.button("📥  Export Markdown"):
        lines = [f"# {report_title}\n\n"]
        lines.append(f"**Dataset:** {st.session_state.get('df_name','—')}  \n")
        lines.append(f"**Rows:** {df.shape[0]:,} | **Columns:** {df.shape[1]}  \n\n---\n")
        for section, data in report_sections.items():
            lines.append(f"\n## {section}\n\n")
            lines.append(data.reset_index().to_markdown(index=False))
            lines.append("\n")
        md_text = "\n".join(lines)
        st.download_button(
            "⬇️  Download .md",
            data=md_text,
            file_name="datapulse_report.md",
            mime="text/markdown",
        )

st.markdown("---")
# ── Dataset export ────────────────────────────────────────────────────────────
st.markdown("**EXPORT ACTIVE DATASET**")
col1, col2 = st.columns(2)
with col1:
    st.download_button("⬇️  Full Dataset CSV", df.to_csv(index=False),
                       "dataset_full.csv", "text/csv")
with col2:
    buf2 = io.BytesIO()
    df.to_parquet(buf2, index=False)
    st.download_button("⬇️  Full Dataset Parquet", buf2.getvalue(),
                       "dataset_full.parquet",
                       "application/octet-stream")
