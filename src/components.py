import streamlit as st
import plotly.express as px
from src.styles import DASHBOARD_PLOT_LAYOUT, section_title

def format_money(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:,.0f}"

def render_kpi_metrics(metrics: dict):
    cols = st.columns(4)
    cols[0].metric("Revenue", format_money(metrics["total_revenue"]))
    cols[1].metric("Orders", f"{metrics['total_orders']:,}")
    cols[2].metric("Customers", f"{metrics['unique_customers']:,}")
    cols[3].metric("Avg order value", format_money(metrics["avg_order_value"]))

def render_chart(fig, title=None, height=330):
    if title:
        st.markdown(section_title(title), unsafe_allow_html=True)
    fig.update_layout(**DASHBOARD_PLOT_LAYOUT, height=height)
    st.plotly_chart(fig, use_container_width=True)
