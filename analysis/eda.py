import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from db__.session import init_session, get_df, set_df
from pipeline.loader import load_sample
from analysis.eda import (summary_stats, full_missing_report, correlation_matrix,
                           outlier_summary, value_counts_top, numeric_cols, categorical_cols)
from analysis.stats import normality_tests
from src.styles import EDA_CSS, EDA_PLOT_LAYOUT, EDA_COLORS
from src.config import APP_TITLE, PAGE_ICON

st.set_page_config(page_title=f"EDA · {APP_TITLE}", page_icon=PAGE_ICON, layout="wide")
st.markdown(EDA_CSS, unsafe_allow_html=True)

init_session()
df = get_df()

with st.sidebar:
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
        color:#00e5ff;letter-spacing:2px;padding:20px 0 30px">⚡ DATAPULSE</div>""", unsafe_allow_html=True)
    if df is None:
        st.warning("Loading sample for demo")
        df = load_sample("sales"); set_df(df, "sales_sample.csv")

st.markdown("""
<div style="padding:30px 0 10px">
    <span style="font-family:'Syne',sans-serif;font-size:30px;font-weight:800;">
        🔍 Exploratory Analysis
    </span>
    <span style="font-size:12px;color:#6b7280;margin-left:14px;letter-spacing:1px;">EDA</span>
</div>
""", unsafe_allow_html=True)

# ── Quick stats bar ───────────────────────────────────────────────────────────
q1, q2, q3, q4, q5 = st.columns(5)
q1.metric("Rows",     f"{df.shape[0]:,}")
q2.metric("Columns",  f"{df.shape[1]}")
q3.metric("Numeric",  str(len(numeric_cols(df))))
q4.metric("Categorical", str(len(categorical_cols(df))))
q5.metric("Missing%", f"{df.isna().mean().mean()*100:.1f}%")
st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
t1, t2, t3, t4, t5, t6, t7 = st.tabs([
    "  OVERVIEW  ","  DISTRIBUTIONS  ","  CORRELATION  ",
    "  OUTLIERS  ","  CATEGORICAL  ","  NORMALITY  ", "  MULTIVARIATE 3D  "
])

# ─ 1. Overview ───────────────────────────────────────────────────────────────
with t1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**SUMMARY STATISTICS**")
        st.dataframe(summary_stats(df), use_container_width=True)
    with col_b:
        st.markdown("**COLUMN PROFILE**")
        st.dataframe(full_missing_report(df), use_container_width=True)

# ─ 2. Distributions ──────────────────────────────────────────────────────────
with t2:
    ncols = numeric_cols(df)
    if ncols:
        sel_col = st.selectbox("Select column", ncols, key="dist_col")
        chart_type = st.radio("Chart type", ["Histogram", "Box", "Violin"], horizontal=True)

        series = df[sel_col].dropna()
        if chart_type == "Histogram":
            fig = px.histogram(df, x=sel_col, nbins=40,
                               color_discrete_sequence=["#00e5ff"],
                               marginal="rug")
            fig.update_layout(**EDA_PLOT_LAYOUT, title=f"Distribution: {sel_col}", height=380)
        elif chart_type == "Box":
            cat_cols = categorical_cols(df)
            group_by = st.selectbox("Group by (optional)", ["None"] + cat_cols, key="box_grp")
            color_by = None if group_by == "None" else group_by
            fig = px.box(df, y=sel_col, x=color_by, color=color_by,
                         color_discrete_sequence=EDA_COLORS)
            fig.update_layout(**EDA_PLOT_LAYOUT, title=f"Box: {sel_col}", height=380)
        else:
            fig = px.violin(df, y=sel_col, box=True, points="outliers",
                            color_discrete_sequence=["#7b61ff"])
            fig.update_layout(**EDA_PLOT_LAYOUT, title=f"Violin: {sel_col}", height=380)
        st.plotly_chart(fig, use_container_width=True)

        # quick stats
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Mean",   f"{series.mean():.3f}")
        s2.metric("Median", f"{series.median():.3f}")
        s3.metric("Std",    f"{series.std():.3f}")
        s4.metric("Range",  f"{series.max()-series.min():.3f}")
    else:
        st.warning("No numeric columns found.")

# ─ 3. Correlation ─────────────────────────────────────────────────────────────
with t3:
    method = st.radio("Method", ["pearson", "spearman", "kendall"], horizontal=True)
    corr   = correlation_matrix(df, method)
    if not corr.empty:
        fig = px.imshow(corr, color_continuous_scale=["#ff4d6d","#141720","#00e5ff"],
                        zmin=-1, zmax=1, text_auto=".2f", aspect="auto")
        fig.update_layout(**EDA_PLOT_LAYOUT, title=f"{method.title()} Correlation Matrix",
                          coloraxis_colorbar=dict(tickfont=dict(color="#e8eaf0")), height=450)
        fig.update_traces(textfont_color="#e8eaf0")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Need at least 2 numeric columns.")

# ─ 4. Outliers ────────────────────────────────────────────────────────────────
with t4:
    out_df = outlier_summary(df)
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.markdown("**IQR OUTLIER SUMMARY**")
        st.dataframe(out_df, use_container_width=True)
    with col_r:
        if not out_df.empty:
            fig = px.bar(out_df.head(10), x="column", y="outlier_%",
                         color="outlier_%",
                         color_continuous_scale=["#00ffa3","#ffb647","#ff4d6d"])
            fig.update_layout(**EDA_PLOT_LAYOUT, title="Outlier % by Column", height=320,
                              coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

# ─ 5. Categorical ─────────────────────────────────────────────────────────────
with t5:
    cat_cols = categorical_cols(df)
    if cat_cols:
        sel_cat = st.selectbox("Select column", cat_cols, key="cat_sel")
        top_n   = st.slider("Top N values", 5, 30, 15, key="cat_top")
        vc = value_counts_top(df, sel_cat, top_n)
        fig = px.bar(vc, x="count", y=sel_cat, orientation="h",
                     color="count", color_continuous_scale=["#7b61ff","#00e5ff"],
                     text="pct")
        fig.update_traces(texttemplate="%{text}%", textposition="outside",
                          textfont_color="#e8eaf0")
        fig.update_layout(**EDA_PLOT_LAYOUT, title=f"Top {top_n}: {sel_cat}",
                          height=max(300, top_n * 25), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No categorical columns found.")

# ─ 6. Normality ───────────────────────────────────────────────────────────────
with t6:
    st.markdown("**SHAPIRO–WILK NORMALITY TEST** (n ≤ 5000)")
    try:
        norm_df = normality_tests(df)
        st.dataframe(norm_df, use_container_width=True)
        normal_count = (norm_df["normal?"] == "✅ Yes").sum()
        st.markdown(f"""
        <div style="background:#141720;border:1px solid #1e2235;border-radius:10px;
                    padding:16px 20px;font-size:12px;margin-top:12px;">
            <span style="color:#00ffa3;font-weight:700">{normal_count}</span> of
            <span style="color:#00e5ff">{len(norm_df)}</span> numeric columns
            appear normally distributed (p &gt; 0.05).
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"scipy required: pip install scipy ({e})")


# ─ 7. Multivariate 3D ─────────────────────────────────────────────────────────
with t7:
    st.markdown("**MULTIVARIATE 3D RELATIONSHIPS**")
    ncols = numeric_cols(df)
    if len(ncols) >= 3:
        c1, c2, c3 = st.columns(3)
        x_col = c1.selectbox("X Axis", ncols, index=0, key="3d_x")
        y_col = c2.selectbox("Y Axis", ncols, index=min(1, len(ncols)-1), key="3d_y")
        z_col = c3.selectbox("Z Axis", ncols, index=min(2, len(ncols)-1), key="3d_z")
        
        cat_cols = categorical_cols(df)
        color_col = st.selectbox("Color by (optional)", ["None"] + cat_cols, key="3d_color")
        
        fig = px.scatter_3d(
            df, 
            x=x_col, y=y_col, z=z_col,
            color=None if color_col == "None" else color_col,
            opacity=0.7,
            color_discrete_sequence=EDA_COLORS
        )
        fig.update_layout(**EDA_PLOT_LAYOUT, height=600)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Need at least 3 numeric columns for 3D scatter plot.")
