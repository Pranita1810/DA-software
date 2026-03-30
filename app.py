import streamlit as st
from src.analysis import df, total_revenue, top_products, sales_by_category, sales_by_region, monthly_sales
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Dashboard", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

* { font-family: 'Outfit', sans-serif; }

/* ── Sidebar Background ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0a0e2a 0%, #130d2e 40%, #1a0a35 100%);
    border-right: 1px solid rgba(139, 92, 246, 0.2);
    box-shadow: 4px 0 30px rgba(88, 28, 235, 0.15);
}

[data-testid="stSidebar"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 280px; height: 100vh;
    background:
        radial-gradient(ellipse at 20% 20%, rgba(88, 28, 235, 0.18) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 80%, rgba(139, 92, 246, 0.12) 0%, transparent 55%);
    pointer-events: none;
    z-index: 0;
}

/* ── Header ── */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    background: linear-gradient(90deg, #a78bfa, #7c3aed, #c4b5fd) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 1px solid rgba(139, 92, 246, 0.3) !important;
    margin-bottom: 1.2rem !important;
    position: relative;
}

            
/* ── Nav Radio / Buttons ── */
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] p {
    color: #c4b5fd !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em;
}

[data-testid="stSidebar"] .stButton button {
    width: 100%;
    background: linear-gradient(135deg, rgba(109, 40, 217, 0.35), rgba(139, 92, 246, 0.15));
    color: #ddd6fe !important;
    border: 1px solid rgba(139, 92, 246, 0.4) !important;
    border-radius: 10px !important;
    padding: 0.55rem 1rem !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase;
    transition: all 0.25s ease !important;
    margin-bottom: 0.4rem;
    backdrop-filter: blur(6px);
}

[data-testid="stSidebar"] .stButton button:hover {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.6), rgba(109, 40, 217, 0.4)) !important;
    border-color: rgba(196, 181, 253, 0.7) !important;
    box-shadow: 0 0 18px rgba(139, 92, 246, 0.45), inset 0 0 10px rgba(196,181,253,0.05) !important;
    transform: translateX(3px) !important;
    color: #fff !important;
}

/* ── Selectbox ── */
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    background: rgba(109, 40, 217, 0.2) !important;
    border: 1px solid rgba(139, 92, 246, 0.4) !important;
    border-radius: 10px !important;
    color: #ddd6fe !important;
}

/* ── Divider ── */
[data-testid="stSidebar"] hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.5), transparent) !important;
    margin: 1rem 0 !important;
}

/* ── Sidebar text / labels ── */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p {
    color: #a78bfa !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em !important;
}

/* ── Scrollbar ── */
[data-testid="stSidebar"]::-webkit-scrollbar { width: 4px; }
[data-testid="stSidebar"]::-webkit-scrollbar-track { background: transparent; }
[data-testid="stSidebar"]::-webkit-scrollbar-thumb {
    background: rgba(139, 92, 246, 0.4);
    border-radius: 4px;
}

/* ── Main area ── */
.main { background: #07091a; }
.main .block-container { color: #c4b5fd; }
</style>
""", unsafe_allow_html=True)


def show_home():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    .home-wrap * { font-family: 'DM Sans', sans-serif; }

    /* ── Hero ── */
    .hero {
        position: relative;
        padding: 3.5rem 2.5rem 2.5rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #0d0f2b 0%, #130d2e 50%, #1a0635 100%);
        border: 1px solid rgba(139,92,246,0.25);
        overflow: hidden;
        margin-bottom: 2rem;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 320px; height: 320px;
        background: radial-gradient(circle, rgba(124,58,237,0.3) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero::after {
        content: '';
        position: absolute;
        bottom: -40px; left: 30%;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(88,28,235,0.2) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-eyebrow {
        font-size: 0.75rem;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: #a78bfa;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .hero-eyebrow::before {
        content: '';
        display: inline-block;
        width: 28px; height: 1px;
        background: #7c3aed;
    }
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.1;
        background: linear-gradient(90deg, #ffffff 0%, #c4b5fd 50%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    .hero-sub {
        color: #8b7db5;
        font-size: 1rem;
        font-weight: 300;
        max-width: 520px;
        line-height: 1.7;
        margin-bottom: 2rem;
    }
    .hero-badges {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
    }
    .badge {
        background: rgba(124,58,237,0.15);
        border: 1px solid rgba(139,92,246,0.3);
        border-radius: 50px;
        padding: 0.3rem 0.9rem;
        font-size: 0.75rem;
        color: #c4b5fd;
        letter-spacing: 0.05em;
    }

    /* ── KPI Cards ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background: linear-gradient(145deg, rgba(13,15,43,0.9), rgba(19,13,46,0.9));
        border: 1px solid rgba(139,92,246,0.2);
        border-radius: 16px;
        padding: 1.4rem 1.2rem;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s, border-color 0.2s;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(139,92,246,0.6), transparent);
    }
    .kpi-icon {
        font-size: 1.4rem;
        margin-bottom: 0.6rem;
    }
    .kpi-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #6b5fa0;
        margin-bottom: 0.3rem;
    }
    .kpi-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #fff;
        line-height: 1;
        margin-bottom: 0.4rem;
    }
    .kpi-delta {
        font-size: 0.75rem;
        color: #34d399;
        display: flex;
        align-items: center;
        gap: 0.2rem;
    }
    .kpi-delta.down { color: #f87171; }

    /* ── Section Cards ── */
    .section-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .section-card {
        background: linear-gradient(145deg, rgba(13,15,43,0.8), rgba(26,6,53,0.6));
        border: 1px solid rgba(139,92,246,0.18);
        border-radius: 16px;
        padding: 1.6rem;
        cursor: pointer;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    .section-card:hover {
        border-color: rgba(139,92,246,0.5);
        box-shadow: 0 8px 32px rgba(88,28,235,0.2);
        transform: translateY(-3px);
    }
    .section-card-icon {
        font-size: 2rem;
        margin-bottom: 0.8rem;
    }
    .section-card-title {
        font-family: 'Syne', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: #ddd6fe;
        margin-bottom: 0.4rem;
    }
    .section-card-desc {
        font-size: 0.8rem;
        color: #6b5fa0;
        line-height: 1.5;
    }
    .section-card-arrow {
        position: absolute;
        bottom: 1.2rem; right: 1.2rem;
        font-size: 1rem;
        color: rgba(139,92,246,0.4);
    }

    /* ── Footer strip ── */
    .footer-strip {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 1.5rem;
        background: rgba(13,15,43,0.6);
        border: 1px solid rgba(139,92,246,0.12);
        border-radius: 12px;
        font-size: 0.78rem;
        color: #4a3f6b;
    }
    .footer-dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: #34d399;
        display: inline-block;
        margin-right: 0.4rem;
        box-shadow: 0 0 6px #34d399;
    }
    </style>

    <div class="home-wrap">

      <!-- Hero -->
      <div class="hero">
        <div class="hero-eyebrow">Sales Intelligence Platform</div>
        <div class="hero-title">Business Analytics<br>Command Center</div>
        <div class="hero-sub">
          Real-time insights powered by a Star Schema data warehouse.
          Explore revenue trends, product performance, and customer behaviour — all in one place.
        </div>
        <div class="hero-badges">
          <span class="badge">⬡ Star Schema</span>
          <span class="badge">📡 Live Data</span>
          <span class="badge">🔮 Predictive</span>
          <span class="badge">📦 Multi-Region</span>
        </div>
      </div>

      <!-- KPIs -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-icon">💰</div>
          <div class="kpi-label">Total Revenue</div>
          <div class="kpi-value">$4.2M</div>
          <div class="kpi-delta">▲ 12.4% vs last month</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-icon">🛒</div>
          <div class="kpi-label">Total Orders</div>
          <div class="kpi-value">18,340</div>
          <div class="kpi-delta">▲ 8.1% vs last month</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-icon">👥</div>
          <div class="kpi-label">Active Customers</div>
          <div class="kpi-value">6,821</div>
          <div class="kpi-delta">▲ 5.3% vs last month</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-icon">📦</div>
          <div class="kpi-label">Avg Order Value</div>
          <div class="kpi-value">$229</div>
          <div class="kpi-delta down">▼ 2.1% vs last month</div>
        </div>
      </div>

      <!-- Section Cards -->
      <div class="section-grid">
        <div class="section-card">
          <div class="section-card-icon">🔬</div>
          <div class="section-card-title">Exploratory Data Analysis</div>
          <div class="section-card-desc">Deep-dive into distributions, correlations, outliers, and hidden patterns across your datasets.</div>
          <div class="section-card-arrow">→</div>
        </div>
        <div class="section-card">
          <div class="section-card-icon">🔁</div>
          <div class="section-card-title">Data Pipeline</div>
          <div class="section-card-desc">Automated ETL workflows, real-time ingestion, and Star Schema warehouse transformation.</div>
          <div class="section-card-arrow">→</div>
        </div>
        <div class="section-card">
          <div class="section-card-icon">🤖</div>
          <div class="section-card-title">ML Models</div>
          <div class="section-card-desc">Predictive forecasting, churn detection, segmentation, and demand planning models.</div>
          <div class="section-card-arrow">→</div>
        </div>

      </div>
      <!-- Footer -->
      <div class="footer-strip">
        <span><span class="footer-dot"></span>All systems operational · Last sync 2 min ago</span>
        <span>Data Warehouse v2.4.1 · Star Schema Model</span>
        <span>FY 2024 · Q4</span>
      </div>

    </div>
    """, unsafe_allow_html=True)



# ── Theme Colors ───────────────────────────────────────────────────────────
PURPLE   = "#7c3aed"
VIOLET   = "#a78bfa"
PINK     = "#c4b5fd"
DARK     = "#0a0e2a"
BG       = "rgba(0,0,0,0)"
GRID     = "rgba(139,92,246,0.1)"
FONT_CLR = "#8b7db5"

def base_layout(height=280):
    return dict(
        plot_bgcolor=BG, paper_bgcolor=BG,
        font=dict(family="DM Sans", color=FONT_CLR, size=11),
        xaxis=dict(gridcolor=GRID, showline=False, tickfont=dict(color=FONT_CLR)),
        yaxis=dict(gridcolor=GRID, showline=False, tickfont=dict(color=FONT_CLR)),
        margin=dict(l=10, r=10, t=36, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=FONT_CLR)),
        height=height,
    )

def chart_wrap(title, subtitle=""):
    st.markdown(f"""
    <div class="chart-wrap">
    <div class="chart-title">{title}</div>
    <div class="chart-sub">{subtitle}</div>
    """, unsafe_allow_html=True)

def chart_end():
    st.markdown("</div>", unsafe_allow_html=True)

# ── KPI Calculations ───────────────────────────────────────────────────────
total_sales_rev  = df["TotalSales"].sum()
total_orders     = df["OrderDate"].count()
unique_customers = df["CustomerName"].nunique()
avg_order_val    = df["TotalSales"].sum() / total_orders

months_sorted = df.groupby(df["OrderDate"].dt.to_period("M"))["TotalSales"].sum().sort_index()
if len(months_sorted) >= 2:
    rev_delta = ((months_sorted.iloc[-1] - months_sorted.iloc[-2]) / months_sorted.iloc[-2]) * 100
else:
    rev_delta = 0.0

def delta_arrow(val):
    return ("▲", "kpi-delta", f"{abs(val):.1f}%") if val >= 0 else ("▼", "kpi-delta down", f"{abs(val):.1f}%")

arr, cls, pct = delta_arrow(rev_delta)

def show_revenue():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

    .rev-wrap * { font-family: 'DM Sans', sans-serif; }

    /* Hero */
    .rev-hero {
        position: relative; padding: 2.8rem 2.5rem 2.2rem;
        border-radius: 20px;
        background: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1400&q=80') center/cover no-repeat,
                    linear-gradient(135deg,#0d0f2b,#1a0635);
        background-blend-mode: overlay;
        border: 1px solid rgba(139,92,246,0.25);
        margin-bottom: 1.8rem; overflow: hidden;
    }
    .rev-hero::before {
        content:''; position:absolute; inset:0;
        background: linear-gradient(135deg,rgba(10,14,42,0.85),rgba(26,6,53,0.78));
    }
    .rev-hero-content { position:relative; z-index:1; }
    .rev-eyebrow {
        font-size:0.72rem; letter-spacing:0.22em; text-transform:uppercase;
        color:#a78bfa; margin-bottom:0.6rem;
        display:flex; align-items:center; gap:0.5rem;
    }
    .rev-eyebrow::before { content:''; width:28px; height:1px; background:#7c3aed; }
    .rev-title {
        font-family:'Syne',sans-serif; font-size:2.6rem; font-weight:800; line-height:1.1;
        background:linear-gradient(90deg,#fff 0%,#c4b5fd 55%,#7c3aed 100%);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        background-clip:text; margin-bottom:0.6rem;
    }
    .rev-sub { color:#9d8ec4; font-size:0.9rem; font-weight:300; line-height:1.6; }

    /* KPI Cards */
    .kpi-grid {
        display:grid; grid-template-columns:repeat(4,1fr);
        gap:1rem; margin-bottom:1.6rem;
    }
    .kpi-card {
        background:linear-gradient(145deg,rgba(13,15,43,0.95),rgba(19,13,46,0.9));
        border:1px solid rgba(139,92,246,0.2); border-radius:16px;
        padding:1.3rem 1.1rem; position:relative; overflow:hidden;
    }
    .kpi-card::before {
        content:''; position:absolute; top:0; left:0; right:0; height:2px;
        background:linear-gradient(90deg,transparent,rgba(139,92,246,0.7),transparent);
    }
    .kpi-icon  { font-size:1.3rem; margin-bottom:0.5rem; }
    .kpi-label { font-size:0.7rem; text-transform:uppercase; letter-spacing:0.12em; color:#6b5fa0; margin-bottom:0.25rem; }
    .kpi-value { font-family:'Syne',sans-serif; font-size:1.75rem; font-weight:700; color:#fff; line-height:1; margin-bottom:0.35rem; }
    .kpi-delta       { font-size:0.72rem; color:#34d399; }
    .kpi-delta.down  { color:#f87171; }

    /* Chart Wrap */
    .chart-wrap {
        background:linear-gradient(145deg,rgba(13,15,43,0.95),rgba(19,13,46,0.9));
        border:1px solid rgba(139,92,246,0.2); border-radius:16px;
        padding:1.3rem 1.2rem; position:relative; overflow:hidden;
        margin-bottom:0;
    }
    .chart-wrap::before {
        content:''; position:absolute; top:0; left:0; right:0; height:2px;
        background:linear-gradient(90deg,transparent,rgba(139,92,246,0.6),transparent);
    }
    .chart-title { font-family:'Syne',sans-serif; font-size:0.95rem; font-weight:700; color:#ddd6fe; margin-bottom:0.1rem; }
    .chart-sub   { font-size:0.75rem; color:#6b5fa0; margin-bottom:0.5rem; }

    /* Footer */
    .footer-strip {
        display:flex; justify-content:space-between; align-items:center;
        padding:0.9rem 1.4rem; margin-top:1.4rem;
        background:rgba(13,15,43,0.6);
        border:1px solid rgba(139,92,246,0.12); border-radius:12px;
        font-size:0.75rem; color:#4a3f6b;
    }
    .footer-dot {
        width:6px; height:6px; border-radius:50%; background:#34d399;
        display:inline-block; margin-right:0.4rem; box-shadow:0 0 6px #34d399;
    }
    </style>

    <div class="rev-wrap">
      <div class="rev-hero">
        <div class="rev-hero-content">
          <div class="rev-eyebrow">Revenue Intelligence</div>
          <div class="rev-title">Revenue Dashboard</div>
          <div class="rev-sub">Sales performance powered by real transactional data · Star Schema Warehouse</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ──
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-value">${total_sales_rev/1e6:.2f}M</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-icon">🛒</div>
        <div class="kpi-label">Total Orders</div>
        <div class="kpi-value">{total_orders:,}</div>
        <div class="kpi-delta">All time transactions</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon">💳</div>
        <div class="kpi-label">Avg Order Value</div>
        <div class="kpi-value">${avg_order_val:,.0f}</div>
        <div class="kpi-delta">Per transaction</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 1: Monthly Trend + Revenue by Region ──
    c1, c2 = st.columns([3, 2])

    with c1:
        chart_wrap("Monthly Revenue Trend", "TotalSales aggregated by month")
        monthly = df.groupby(df["OrderDate"].dt.to_period("M")).agg(
            Revenue=("TotalSales","sum"),
            Orders=("TotalSales","count")
        ).reset_index()
        monthly["OrderDate"] = monthly["OrderDate"].astype(str)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly["OrderDate"], y=monthly["Revenue"],
            mode="lines+markers", name="Revenue",
            line=dict(color=PURPLE, width=2.5),
            marker=dict(color=VIOLET, size=6),
            fill="tozeroy", fillcolor="rgba(124,58,237,0.08)"
        ))
        fig.add_trace(go.Bar(
            x=monthly["OrderDate"], y=monthly["Orders"],
            name="Orders", marker_color="rgba(196,181,253,0.15)",
            yaxis="y2"
        ))
        layout = base_layout(280)
        layout["yaxis2"] = dict(overlaying="y", side="right", showgrid=False,
                                 tickfont=dict(color=FONT_CLR), gridcolor=GRID)
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        chart_end()

    with c2:
        chart_wrap("Revenue by Region", "TotalSales per region")
        region = df.groupby("Region")["TotalSales"].sum().reset_index().sort_values("TotalSales", ascending=True)
        fig2 = go.Figure(go.Bar(
            x=region["TotalSales"], y=region["Region"],
            orientation="h",
            marker=dict(
                color=region["TotalSales"],
                colorscale=[[0,"#1a0635"],[0.5,"#7c3aed"],[1,"#c4b5fd"]],
                showscale=False
            ),
            text=[f"${v/1e3:.0f}K" for v in region["TotalSales"]],
            textfont=dict(color="#ddd6fe"), textposition="outside"
        ))
        fig2.update_layout(**base_layout(280))
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        chart_end()

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Row 2: Revenue by Category + Top Products ──
    c3, c4 = st.columns(2)

    with c3:
        chart_wrap("Revenue by Category", "TotalSales per product category")
        cat = df.groupby("Category")["TotalSales"].sum().reset_index().sort_values("TotalSales", ascending=False)
        fig3 = go.Figure(go.Pie(
            labels=cat["Category"], values=cat["TotalSales"],
            hole=0.55,
            marker=dict(colors=["#7c3aed","#a78bfa","#5b21b6","#c4b5fd","#3b0764","#6d28d9","#ede9fe"]),
            textfont=dict(color="#fff", size=11),
        ))
        fig3.update_layout(
            plot_bgcolor=BG, paper_bgcolor=BG,
            font=dict(family="DM Sans", color=FONT_CLR),
            margin=dict(l=10,r=10,t=10,b=10),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=FONT_CLR, size=10)),
            height=280,
            annotations=[dict(text="Category", x=0.5, y=0.5,
                              font_size=12, font_color="#a78bfa", showarrow=False)]
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
        chart_end()

    with c4:
        chart_wrap("Top 10 Products", "Highest revenue generating products")
        top_prod = df.groupby("ProductName")["TotalSales"].sum().reset_index()\
                     .sort_values("TotalSales", ascending=True).tail(10)
        fig4 = go.Figure(go.Bar(
            x=top_prod["TotalSales"], y=top_prod["ProductName"],
            orientation="h",
            marker=dict(
                color=top_prod["TotalSales"],
                colorscale=[[0,"#3b0764"],[0.5,"#7c3aed"],[1,"#c4b5fd"]],
                showscale=False
            ),
            text=[f"${v/1e3:.1f}K" for v in top_prod["TotalSales"]],
            textfont=dict(color="#ddd6fe"), textposition="outside"
        ))
        fig4.update_layout(**base_layout(280))
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
        chart_end()

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── Row 3: Customer Age Distribution (full width) ──
    chart_wrap("Customer Age Distribution", "Revenue contribution by age group")
    df["AgeGroup"] = pd.cut(df["Age"],
                            bins=[0,20,30,40,50,60,100],
                            labels=["<20","20-30","30-40","40-50","50-60","60+"])
    age_grp = df.groupby("AgeGroup", observed=True)["TotalSales"].sum().reset_index()

    fig5 = go.Figure()
    fig5.add_trace(go.Bar(
        x=age_grp["AgeGroup"].astype(str),
        y=age_grp["TotalSales"],
        marker=dict(
            color=age_grp["TotalSales"],
            colorscale=[[0,"#1a0635"],[0.4,"#5b21b6"],[0.7,"#7c3aed"],[1,"#c4b5fd"]],
            showscale=False
        ),
        text=[f"${v/1e3:.0f}K" for v in age_grp["TotalSales"]],
        textfont=dict(color="#ddd6fe"), textposition="outside"
    ))
    fig5.update_layout(**base_layout(240))
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
    chart_end()

    # ── Footer ──
    st.markdown(f"""
    <div class="footer-strip">
        <span><span class="footer-dot"></span>Live Dataset · {len(df):,} records loaded</span>
        <span>Columns: OrderDate · TotalSales · Region · Category · ProductName · Age</span>
        <span>Star Schema v2.4.1</span>
    </div>
    """, unsafe_allow_html=True)


# --- Sidebar ---
with st.sidebar:
    st.header("⬡ Menu")

    Home              = st.button("🏠  Home Page",  use_container_width=True)
    Revenue_analysis  = st.button("📊  Revenue",    use_container_width=True)
    Product_analysis  = st.button("🛰  Product",    use_container_width=True)
    Customer_analysis = st.button("⚙️  Customer",   use_container_width=True)

    st.markdown("---")
    st.selectbox("Workspace", ["Production", "Staging", "Dev"])
    st.markdown("---")
    st.markdown("v2.4.1 · Dark Build")



# --- Pages ---
if Revenue_analysis:
    show_revenue()

elif Product_analysis:
    st.title("🛰 Product Analysis")
    st.markdown("### Product page content here")

elif Customer_analysis:
    st.title("⚙️ Customer Analysis")
    st.markdown("### Customer page content here")

else: 
    show_home()
