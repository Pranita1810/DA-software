from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from typing import Dict, Any

from src.config import APP_TITLE, PAGE_ICON, PAGES
from src.styles import DASHBOARD_CSS, HERO_HTML, section_title, DASHBOARD_PLOT_LAYOUT
from src.components import render_kpi_metrics, render_chart, format_money

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title=APP_TITLE, page_icon=PAGE_ICON, layout="wide")

def call_api(endpoint: str, params: Dict[str, Any] = None) -> Any:
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def build_sidebar():
    filters = call_api("/filters")
    if not filters:
        return None, {}

    with st.sidebar:
        st.title("DataPulse")
        page = st.radio("View", PAGES, label_visibility="collapsed")
        st.divider()

        regions = filters["regions"]
        categories = filters["categories"]
        selected_regions = st.multiselect("Regions", regions, default=regions)
        selected_categories = st.multiselect("Categories", categories, default=categories)

        min_date = pd.to_datetime(filters["date_range"]["min"]).date()
        max_date = pd.to_datetime(filters["date_range"]["max"]).date()
        date_range = st.date_input("Order date range", (min_date, max_date))

    api_params = {
        "regions": selected_regions,
        "categories": selected_categories,
    }
    if isinstance(date_range, tuple) and len(date_range) == 2:
        api_params["start_date"] = date_range[0].isoformat()
        api_params["end_date"] = date_range[1].isoformat()

    return page, api_params

def show_home(params):
    st.markdown(HERO_HTML, unsafe_allow_html=True)
    metrics = call_api("/metrics", params)
    if metrics:
        render_kpi_metrics(metrics)

    monthly_data = call_api("/revenue/monthly", params)
    if monthly_data:
        monthly = pd.DataFrame(monthly_data)
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
        region_data = call_api("/revenue/by-region", params)
        if region_data:
            region = pd.DataFrame(region_data)
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
        category_data = call_api("/revenue/by-category", params)
        if category_data:
            category = pd.DataFrame(category_data)
            fig = px.pie(
                category,
                names="Category",
                values="TotalSales",
                hole=0.48,
                color_discrete_sequence=px.colors.qualitative.Bold,
            )
            render_chart(fig, "Category Mix", height=320)

def show_revenue(params):
    st.markdown(section_title("Revenue Overview"), unsafe_allow_html=True)
    metrics = call_api("/metrics", params)
    if metrics:
        render_kpi_metrics(metrics)

    monthly_data = call_api("/revenue/monthly", params)
    if monthly_data:
        monthly = pd.DataFrame(monthly_data)
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

    heatmap_data = call_api("/revenue/region-category", params)
    if heatmap_data:
        region_category = pd.DataFrame.from_dict(heatmap_data, orient="index")
        fig = px.imshow(
            region_category,
            text_auto=".2s",
            color_continuous_scale=["#101421", "#14b8a6", "#f59e0b"],
            aspect="auto",
        )
        render_chart(fig, "Region x Category Revenue", height=360)

def show_products(params):
    st.markdown(section_title("Product Performance"), unsafe_allow_html=True)
    product_data = call_api("/products", params)
    if product_data:
        product = pd.DataFrame(product_data)
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

def show_customers(params):
    st.markdown(section_title("Customer Segments"), unsafe_allow_html=True)
    customer_data = call_api("/customers", params)
    if customer_data:
        customer = pd.DataFrame(customer_data)
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

def show_data_quality(params):
    st.markdown(section_title("Data Quality"), unsafe_allow_html=True)
    dq_data = call_api("/data-quality")
    if dq_data:
        stats = dq_data["stats"]
        cols = st.columns(4)
        cols[0].metric("Rows", f"{stats['rows']:,}")
        cols[1].metric("Columns", f"{stats['columns']:,}")
        cols[2].metric("Duplicate rows", f"{stats['duplicate_rows']:,}")
        cols[3].metric("Missing cells", f"{stats['missing_cells']:,}")

        profile = pd.DataFrame(dq_data["profile"])
        st.dataframe(profile, use_container_width=True, hide_index=True)

def show_3d_analytics(params):
    st.markdown(section_title("3D Insights"), unsafe_allow_html=True)
    st.info("Interactive 3D visualizations for deeper data exploration.")
    
    tab1, tab2, tab3 = st.tabs(["Customer Segments", "Product Performance", "Regional Trends"])
    
    with tab1:
        customer_data = call_api("/customers", params)
        if customer_data:
            customer = pd.DataFrame(customer_data)
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
        product_data = call_api("/products", params)
        if product_data:
            product = pd.DataFrame(product_data)
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
        regional_monthly_data = call_api("/revenue/regional-monthly", params)
        if regional_monthly_data:
            regional_monthly = pd.DataFrame(regional_monthly_data)
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
    
    page, params = build_sidebar()
    if not page:
        st.error("Could not connect to the API. Please ensure the backend is running.")
        return

    pages = {
        "Home": show_home,
        "Revenue": show_revenue,
        "Products": show_products,
        "Customers": show_customers,
        "3D Analytics": show_3d_analytics,
        "Data Quality": show_data_quality,
    }
    
    pages[page](params)

if __name__ == "__main__":
    main()
