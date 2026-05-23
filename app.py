from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.config import APP_TITLE, PAGE_ICON, PAGES
from src.styles import DASHBOARD_CSS, HERO_HTML, section_title, DASHBOARD_PLOT_LAYOUT
from src.data_manager import load_sales_data, get_sales_metrics
from src.aggregations import (
    get_customer_summary,
    get_product_summary,
    get_monthly_revenue_summary,
    get_revenue_by_region,
    get_revenue_by_category,
    get_regional_monthly_revenue,
)
from src.components import render_kpi_metrics, render_chart, format_money


st.set_page_config(page_title=APP_TITLE, page_icon=PAGE_ICON, layout="wide")


@st.cache_data(show_spinner=False)
def get_data():
    return load_sales_data()


def build_sidebar(df):
    with st.sidebar:
        st.title("DataPulse")
        page = st.radio("View", PAGES, label_visibility="collapsed")
        st.divider()

        regions = sorted(df["Region"].dropna().unique())
        categories = sorted(df["Category"].dropna().unique())
        selected_regions = st.multiselect("Regions", regions, default=regions)
        selected_categories = st.multiselect("Categories", categories, default=categories)

        min_date = df["OrderDate"].min().date()
        max_date = df["OrderDate"].max().date()
        date_range = st.date_input("Order date range", (min_date, max_date))

    filtered = df.copy()
    if selected_regions:
        filtered = filtered[filtered["Region"].isin(selected_regions)]
    if selected_categories:
        filtered = filtered[filtered["Category"].isin(selected_categories)]
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
        filtered = filtered[
            (filtered["OrderDate"].dt.date >= start)
            & (filtered["OrderDate"].dt.date <= end)
        ]

    return page, filtered


def show_home(df):
    st.markdown(HERO_HTML, unsafe_allow_html=True)
    render_kpi_metrics(get_sales_metrics(df))

    monthly = get_monthly_revenue_summary(df)
    fig = px.area(
        monthly,
        x="OrderDate",
        y="Revenue",
        markers=True,
        color_discrete_sequence=["#14b8a6"],
    )
    render_chart(fig, "Revenue Trend")

    left, right = st.columns(2)
    with left:
        region = get_revenue_by_region(df)
        fig = px.bar(
            region,
            x="TotalSales",
            y="Region",
            orientation="h",
            color="Region",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_layout(showlegend=False)
        render_chart(fig, "Revenue by Region", height=320)

    with right:
        category = get_revenue_by_category(df)
        fig = px.pie(
            category,
            names="Category",
            values="TotalSales",
            hole=0.48,
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        render_chart(fig, "Category Mix", height=320)


def show_revenue(df):
    st.markdown(section_title("Revenue Overview"), unsafe_allow_html=True)
    render_kpi_metrics(get_sales_metrics(df))

    monthly = get_monthly_revenue_summary(df)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=monthly["OrderDate"],
            y=monthly["Revenue"],
            name="Revenue",
            mode="lines+markers",
            line={"color": "#14b8a6", "width": 3},
        )
    )
    fig.add_trace(
        go.Bar(
            x=monthly["OrderDate"],
            y=monthly["Orders"],
            name="Orders",
            yaxis="y2",
            marker_color="rgba(139, 92, 246, 0.35)",
        )
    )
    layout = DASHBOARD_PLOT_LAYOUT.copy()
    layout["yaxis2"] = {
        "overlaying": "y",
        "side": "right",
        "showgrid": False,
        "tickfont": {"color": "#94a3b8"},
    }
    fig.update_layout(**layout)
    render_chart(fig, height=420)

    region_category = df.pivot_table(
        values="TotalSales",
        index="Region",
        columns="Category",
        aggfunc="sum",
        fill_value=0,
    )
    fig = px.imshow(
        region_category,
        text_auto=".2s",
        color_continuous_scale=["#101421", "#14b8a6", "#f59e0b"],
        aspect="auto",
    )
    render_chart(fig, "Region x Category Revenue", height=360)


def show_products(df):
    st.markdown(section_title("Product Performance"), unsafe_allow_html=True)
    product = get_product_summary(df)

    cols = st.columns(3)
    cols[0].metric("Products", f"{product['ProductID'].nunique():,}")
    cols[1].metric("Units sold", f"{product['Units'].sum():,}")
    cols[2].metric("Top product", product.iloc[0]["ProductName"])

    top = product.head(12).sort_values("Revenue")
    fig = px.bar(
        top,
        x="Revenue",
        y="ProductName",
        color="Category",
        orientation="h",
        hover_data=["Units", "Orders"],
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    render_chart(fig, height=430)
    st.dataframe(product, use_container_width=True, hide_index=True)


def show_customers(df):
    st.markdown(section_title("Customer Segments"), unsafe_allow_html=True)
    customer = get_customer_summary(df)

    cols = st.columns(3)
    cols[0].metric("Customers", f"{customer['CustomerID'].nunique():,}")
    cols[1].metric("Repeat order rate", f"{(customer['Orders'].gt(1).mean() * 100):.1f}%")
    cols[2].metric("Median customer revenue", format_money(customer["Revenue"].median()))

    left, right = st.columns(2)
    with left:
        age_bins = [0, 20, 30, 40, 50, 60, 120]
        age_labels = ["<20", "20-29", "30-39", "40-49", "50-59", "60+"]
        customer["AgeGroup"] = pd.cut(customer["Age"], bins=age_bins, labels=age_labels)
        age = customer.groupby("AgeGroup", observed=True, as_index=False)["Revenue"].sum()
        fig = px.bar(age, x="AgeGroup", y="Revenue", color_discrete_sequence=["#8b5cf6"])
        render_chart(fig, height=340)

    with right:
        region = customer.groupby("Region", as_index=False)["Revenue"].sum()
        fig = px.pie(
            region,
            names="Region",
            values="Revenue",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        render_chart(fig, height=340)

    st.dataframe(customer.head(50), use_container_width=True, hide_index=True)


def show_data_quality(df):
    st.markdown(section_title("Data Quality"), unsafe_allow_html=True)

    cols = st.columns(4)
    cols[0].metric("Rows", f"{len(df):,}")
    cols[1].metric("Columns", f"{df.shape[1]:,}")
    cols[2].metric("Duplicate rows", f"{df.duplicated().sum():,}")
    cols[3].metric("Missing cells", f"{int(df.isna().sum().sum()):,}")

    profile = (
        df.isna()
        .sum()
        .rename("missing")
        .to_frame()
        .assign(
            dtype=df.dtypes.astype(str).values,
            missing_pct=lambda x: (x["missing"] / len(df) * 100).round(2),
            unique=df.nunique(dropna=True).values,
        )
        .reset_index()
        .rename(columns={"index": "column"})
    )
    st.dataframe(profile, use_container_width=True, hide_index=True)

    st.markdown(section_title("Sample Records"), unsafe_allow_html=True)
    st.dataframe(df.head(25), use_container_width=True, hide_index=True)


def show_3d_analytics(df):
    st.markdown(section_title("3D Insights"), unsafe_allow_html=True)
    
    st.info("Interactive 3D visualizations for deeper data exploration.")
    
    tab1, tab2, tab3 = st.tabs(["Customer Segments", "Product Performance", "Regional Trends"])
    
    with tab1:
        customer = get_customer_summary(df)
        fig = px.scatter_3d(
            customer,
            x="Age",
            y="Revenue",
            z="Orders",
            color="Region",
            symbol="Gender",
            opacity=0.7,
            labels={"Revenue": "Total Revenue ($)", "Orders": "Order Count"},
        )
        render_chart(fig, "Customer Segmentation (Age vs Revenue vs Orders)", height=650)

    with tab2:
        product = get_product_summary(df)
        product["AvgPrice"] = product["Revenue"] / product["Units"].replace(0, 1)
        fig = px.scatter_3d(
            product,
            x="Units",
            y="Revenue",
            z="AvgPrice",
            color="Category",
            hover_name="ProductName",
            opacity=0.7,
            labels={"AvgPrice": "Avg Unit Price ($)"},
        )
        render_chart(fig, "Product Landscape (Units vs Revenue vs Price)", height=650)

    with tab3:
        regional_monthly = get_regional_monthly_revenue(df)
        regional_monthly = regional_monthly.sort_values("OrderDate")
        
        fig = px.scatter_3d(
            regional_monthly,
            x="OrderDate",
            y="Region",
            z="Revenue",
            color="Region",
            size="Revenue",
            opacity=0.8,
        )
        render_chart(fig, "Regional Revenue Evolution", height=650)


def main():
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)
    df = get_data()
    
    if df.empty:
        st.error("No data found. Please run the pipeline first: `python -m src.pipeline`")
        return
        
    page, filtered = build_sidebar(df)

    if filtered.empty:
        st.warning("No rows match the current filters.")
        return

    pages = {
        "Home": show_home,
        "Revenue": show_revenue,
        "Products": show_products,
        "Customers": show_customers,
        "3D Analytics": show_3d_analytics,
        "Data Quality": show_data_quality,
    }
    
    pages[page](filtered)


if __name__ == "__main__":
    main()
