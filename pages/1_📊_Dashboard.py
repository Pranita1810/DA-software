import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from db__.session import init_session, get_df
from pipeline.loader import load_sample

st.set_page_config(page_title="Dashboard · DataPulse", page_icon="📊", layout="wide")
st.info("Wassup big boi hehehehehehehehe")
# ── Shared CSS (imported from app.py via rerun or inline here) ───────────────
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
.stButton>button:hover{background:var(--accent);color:var(--bg);box-shadow:0 0 20px rgba(0,229,255,.3);}
hr{border-color:var(--border)!important;}
.stTabs [data-baseweb="tab-list"]{gap:4px;background:transparent;border-bottom:1px solid var(--border);}
.stTabs [data-baseweb="tab"]{background:transparent;color:var(--muted);font-family:var(--font-mono);font-size:12px;letter-spacing:1px;border-radius:4px 4px 0 0;padding:8px 18px;}
.stTabs [aria-selected="true"]{background:var(--card)!important;color:var(--accent)!important;border-bottom:2px solid var(--accent)!important;}
</style>
""", unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="JetBrains Mono", color="#e8eaf0", size=11),
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(showgrid=True, gridcolor="#1e2235", zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="#1e2235", zeroline=False),
)

COLORS = ["#00e5ff","#7b61ff","#00ffa3","#ffb647","#ff4d6d","#e879f9"]

# ── Data ─────────────────────────────────────────────────────────────────────
init_session()
df = get_df()

with st.sidebar:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
                color:#00e5ff;letter-spacing:2px;padding:20px 0 30px">⚡ DATAPULSE</div>
    """, unsafe_allow_html=True)
    if df is None:
        st.info("No dataset loaded. Using sample data.")
        df = load_sample("sales")

    st.markdown("---")
    st.markdown("**FILTERS**", unsafe_allow_html=False)

    regions   = ["All"] + sorted(df["region"].unique().tolist())  if "region"  in df.columns else ["All"]
    products  = ["All"] + sorted(df["product"].unique().tolist()) if "product" in df.columns else ["All"]
    channels  = ["All"] + sorted(df["channel"].unique().tolist()) if "channel" in df.columns else ["All"]

    sel_region  = st.selectbox("Region",  regions)
    sel_product = st.selectbox("Product", products)
    sel_channel = st.selectbox("Channel", channels)

    if "date" in df.columns:
        d_min = df["date"].min().date()
        d_max = df["date"].max().date()
        date_range = st.date_input("Date range", [d_min, d_max])
    else:
        date_range = None

# ── Apply filters ─────────────────────────────────────────────────────────────
fdf = df.copy()
if sel_region  != "All" and "region"  in fdf.columns: fdf = fdf[fdf["region"]  == sel_region]
if sel_product != "All" and "product" in fdf.columns: fdf = fdf[fdf["product"] == sel_product]
if sel_channel != "All" and "channel" in fdf.columns: fdf = fdf[fdf["channel"] == sel_channel]
if date_range and len(date_range) == 2 and "date" in fdf.columns:
    fdf = fdf[(fdf["date"].dt.date >= date_range[0]) & (fdf["date"].dt.date <= date_range[1])]

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:30px 0 10px">
    <span style="font-family:'Syne',sans-serif;font-size:30px;font-weight:800;letter-spacing:-1px;">
        📊 Dashboard
    </span>
    <span style="font-size:12px;color:#6b7280;margin-left:14px;letter-spacing:1px;">
        OVERVIEW
    </span>
</div>
""", unsafe_allow_html=True)

# ── KPI row ──────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
rev  = fdf["revenue"].sum()  if "revenue"  in fdf.columns else 0
prof = fdf["profit"].sum()   if "profit"   in fdf.columns else 0
units= fdf["units"].sum()    if "units"    in fdf.columns else 0
csat = fdf["csat"].mean()    if "csat"     in fdf.columns else 0
rows = len(fdf)

k1.metric("Total Revenue",  f"${rev:,.0f}",  f"+{rev/max(rows,1):.0f} avg/row")
k2.metric("Total Profit",   f"${prof:,.0f}", f"{prof/max(rev,1)*100:.1f}% margin")
k3.metric("Units Sold",     f"{units:,}",    "units")
k4.metric("Avg CSAT",       f"{csat:.2f} ⭐","out of 5.0")
k5.metric("Records",        f"{rows:,}",     "filtered rows")

st.markdown("---")

# ── Charts ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["  REVENUE TREND  ", "  BREAKDOWN  ", "  SCATTER  "])

with tab1:
    if "date" in fdf.columns and "revenue" in fdf.columns:
        ts = fdf.groupby(fdf["date"].dt.to_period("W").dt.start_time)["revenue"].sum().reset_index()
        ts.columns = ["week", "revenue"]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ts["week"], y=ts["revenue"],
            mode="lines", fill="tozeroy",
            line=dict(color="#00e5ff", width=2),
            fillcolor="rgba(0,229,255,0.08)",
            name="Revenue",
        ))
        if "profit" in fdf.columns:
            tp = fdf.groupby(fdf["date"].dt.to_period("W").dt.start_time)["profit"].sum().reset_index()
            tp.columns = ["week", "profit"]
            fig.add_trace(go.Scatter(
                x=tp["week"], y=tp["profit"],
                mode="lines",
                line=dict(color="#00ffa3", width=2, dash="dot"),
                name="Profit",
            ))
        fig.update_layout(**PLOTLY_LAYOUT, title="Weekly Revenue & Profit", height=350,
                          legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Date and Revenue columns required for this chart.")

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        if "region" in fdf.columns and "revenue" in fdf.columns:
            grp = fdf.groupby("region")["revenue"].sum().reset_index().sort_values("revenue", ascending=True)
            fig = px.bar(grp, x="revenue", y="region", orientation="h",
                         color_discrete_sequence=["#7b61ff"])
            fig.update_layout(**PLOTLY_LAYOUT, title="Revenue by Region", height=300)
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        if "product" in fdf.columns and "revenue" in fdf.columns:
            grp = fdf.groupby("product")["revenue"].sum().reset_index()
            fig = px.pie(grp, values="revenue", names="product",
                         color_discrete_sequence=COLORS, hole=0.55)
            fig.update_traces(textfont_color="#e8eaf0")
            fig.update_layout(**PLOTLY_LAYOUT, title="Revenue by Product", height=300,
                              legend=dict(bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig, use_container_width=True)

    if "channel" in fdf.columns and "revenue" in fdf.columns and "units" in fdf.columns:
        grp = fdf.groupby("channel").agg(revenue=("revenue","sum"), units=("units","sum")).reset_index()
        fig = px.bar(grp, x="channel", y=["revenue","units"], barmode="group",
                     color_discrete_sequence=["#00e5ff","#ffb647"])
        fig.update_layout(**PLOTLY_LAYOUT, title="Revenue & Units by Channel", height=280,
                          legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    if "revenue" in fdf.columns and "profit" in fdf.columns:
        color_by = "region" if "region" in fdf.columns else None
        fig = px.scatter(fdf.sample(min(300, len(fdf))),
                         x="revenue", y="profit",
                         color=color_by,
                         size="units" if "units" in fdf.columns else None,
                         color_discrete_sequence=COLORS,
                         opacity=0.7)
        fig.update_layout(**PLOTLY_LAYOUT, title="Revenue vs Profit (sample 300)", height=380,
                          legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Revenue and Profit columns required.")
