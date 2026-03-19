import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from db__.session import init_session, get_df, set_df
from pipeline.loader import load_sample
from analysis.eda import numeric_cols, categorical_cols, datetime_cols

st.set_page_config(page_title="Visualise · DataPulse", page_icon="📈", layout="wide")
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
.stSelectbox>div>div{background:var(--card)!important;border:1px solid var(--border)!important;color:var(--text)!important;}
</style>
""", unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="JetBrains Mono", color="#e8eaf0", size=11),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(showgrid=True, gridcolor="#1e2235", zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="#1e2235", zeroline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)
PALETTES = {
    "Pulse":   ["#00e5ff","#7b61ff","#00ffa3","#ffb647","#ff4d6d","#e879f9"],
    "Neon":    ["#39ff14","#ff073a","#00b4ff","#ffff00","#ff8c00","#ff00ff"],
    "Ocean":   px.colors.sequential.Teal,
    "Sunset":  px.colors.sequential.Sunset,
    "Viridis": px.colors.sequential.Viridis,
}

init_session()
df = get_df()

with st.sidebar:
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
        color:#00e5ff;letter-spacing:2px;padding:20px 0 14px">⚡ DATAPULSE</div>""", unsafe_allow_html=True)
    if df is None:
        df = load_sample("sales"); set_df(df, "sales_sample.csv")

    st.markdown("---")
    st.markdown("**CHART SETTINGS**")
    chart_type = st.selectbox("Chart type", [
        "Bar", "Horizontal Bar", "Line", "Area", "Scatter",
        "Bubble", "Pie", "Donut", "Heatmap", "Histogram", "Funnel"
    ])
    palette_name = st.selectbox("Color palette", list(PALETTES.keys()))
    palette      = PALETTES[palette_name]
    chart_height = st.slider("Height (px)", 300, 700, 420, step=20)
    st.markdown("---")

ncols = numeric_cols(df)
ccols = categorical_cols(df)
dcols = datetime_cols(df)
all_cols = df.columns.tolist()

st.markdown("""
<div style="padding:30px 0 10px">
    <span style="font-family:'Syne',sans-serif;font-size:30px;font-weight:800;">
        📈 Visualisations
    </span>
    <span style="font-size:12px;color:#6b7280;margin-left:14px;letter-spacing:1px;">
        CHART BUILDER
    </span>
</div>
""", unsafe_allow_html=True)

# ── Config panel ──────────────────────────────────────────────────────────────
cfg = st.expander("⚙️  Configure Chart", expanded=True)
with cfg:
    col1, col2, col3 = st.columns(3)
    with col1:
        x_col = st.selectbox("X axis", all_cols, index=0)
    with col2:
        y_col = st.selectbox("Y axis / Value", ncols if ncols else all_cols, index=0)
    with col3:
        color_col = st.selectbox("Color by", ["None"] + ccols)
        color_col = None if color_col == "None" else color_col

    col4, col5 = st.columns(2)
    with col4:
        size_col = st.selectbox("Size by (Bubble)", ["None"] + ncols)
        size_col = None if size_col == "None" else size_col
    with col5:
        agg_func = st.selectbox("Aggregate Y by", ["sum", "mean", "count", "median", "max", "min"])

    chart_title = st.text_input("Chart title", value=f"{chart_type}: {y_col} by {x_col}")

# ── Build figure ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def build_fig(chart_type, df_json, x_col, y_col, color_col, size_col,
              agg_func, palette, height, title):
    _df = pd.read_json(df_json, orient="split")

    # Aggregate
    if agg_func and chart_type not in ("Scatter", "Bubble", "Histogram"):
        grp_cols = [c for c in [x_col, color_col] if c]
        if grp_cols:
            _df = _df.groupby(grp_cols)[y_col].agg(agg_func).reset_index()

    kw = dict(color_discrete_sequence=palette)
    fig = None

    if chart_type == "Bar":
        fig = px.bar(_df, x=x_col, y=y_col, color=color_col, **kw, barmode="group")
    elif chart_type == "Horizontal Bar":
        fig = px.bar(_df, x=y_col, y=x_col, color=color_col, orientation="h", **kw)
    elif chart_type == "Line":
        fig = px.line(_df, x=x_col, y=y_col, color=color_col, **kw, markers=True)
    elif chart_type == "Area":
        fig = px.area(_df, x=x_col, y=y_col, color=color_col, **kw)
    elif chart_type == "Scatter":
        fig = px.scatter(_df, x=x_col, y=y_col, color=color_col, **kw, opacity=0.7)
    elif chart_type == "Bubble":
        fig = px.scatter(_df, x=x_col, y=y_col, color=color_col, size=size_col, **kw, opacity=0.7)
    elif chart_type == "Pie":
        fig = px.pie(_df, names=x_col, values=y_col, color_discrete_sequence=palette)
        fig.update_traces(textfont_color="#e8eaf0")
    elif chart_type == "Donut":
        fig = px.pie(_df, names=x_col, values=y_col, hole=0.55, color_discrete_sequence=palette)
        fig.update_traces(textfont_color="#e8eaf0")
    elif chart_type == "Heatmap":
        pivot = _df.pivot_table(index=x_col, columns=color_col or y_col, values=y_col, aggfunc=agg_func)
        fig = px.imshow(pivot, color_continuous_scale=["#ff4d6d","#141720","#00e5ff"],
                        text_auto=".1f", aspect="auto")
        fig.update_traces(textfont_color="#e8eaf0")
    elif chart_type == "Histogram":
        fig = px.histogram(_df, x=x_col, color=color_col, **kw, nbins=40, marginal="rug")
    elif chart_type == "Funnel":
        grp = _df.groupby(x_col)[y_col].sum().reset_index().sort_values(y_col, ascending=False)
        fig = go.Figure(go.Funnel(y=grp[x_col], x=grp[y_col],
                                   marker_color=palette[:len(grp)]))

    if fig is not None:
        layout = PLOTLY_LAYOUT.copy()
        layout.update(title=title, height=height)
        fig.update_layout(**layout)
    return fig

try:
    fig = build_fig(
        chart_type,
        df.to_json(orient="split", date_format="iso"),
        x_col, y_col, color_col, size_col,
        agg_func, palette, chart_height, chart_title
    )
    if fig:
        st.plotly_chart(fig, use_container_width=True)
        st.session_state["chart_count"] = st.session_state.get("chart_count", 0) + 1
except Exception as e:
    st.error(f"Chart error: {e}")

# ── Download ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.download_button(
    "⬇️  Download data as CSV",
    data=df.to_csv(index=False),
    file_name="datapulse_export.csv",
    mime="text/csv",
)
