from __future__ import annotations
from fastapi import FastAPI, Query
from typing import List, Optional
import pandas as pd
from datetime import date

from src.data_manager import load_sales_data, get_sales_metrics
from src.aggregations import (
    get_customer_summary,
    get_product_summary,
    get_monthly_revenue_summary,
    get_revenue_by_region,
    get_revenue_by_category,
    get_regional_monthly_revenue,
)

app = FastAPI(title="DataPulse API", description="FastAPI backend for EDA Software")

# In-memory data cache
_df = None

def get_data():
    global _df
    if _df is None:
        _df = load_sales_data()
    return _df

def apply_filters(
    df: pd.DataFrame,
    regions: Optional[List[str]] = None,
    categories: Optional[List[str]] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> pd.DataFrame:
    if df.empty:
        return df
        
    filtered = df.copy()
    if regions:
        filtered = filtered[filtered["Region"].isin(regions)]
    if categories:
        filtered = filtered[filtered["Category"].isin(categories)]
    if start_date:
        filtered = filtered[filtered["OrderDate"].dt.date >= start_date]
    if end_date:
        filtered = filtered[filtered["OrderDate"].dt.date <= end_date]
    return filtered

@app.get("/")
def read_root():
    return {"message": "Welcome to DataPulse API", "status": "online"}

@app.get("/metrics")
def read_metrics(
    regions: Optional[List[str]] = Query(None),
    categories: Optional[List[str]] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    df = get_data()
    filtered = apply_filters(df, regions, categories, start_date, end_date)
    return get_sales_metrics(filtered)

@app.get("/customers")
def read_customers(
    regions: Optional[List[str]] = Query(None),
    categories: Optional[List[str]] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = 50
):
    df = get_data()
    filtered = apply_filters(df, regions, categories, start_date, end_date)
    summary = get_customer_summary(filtered)
    return summary.head(limit).to_dict(orient="records")

@app.get("/products")
def read_products(
    regions: Optional[List[str]] = Query(None),
    categories: Optional[List[str]] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = 50
):
    df = get_data()
    filtered = apply_filters(df, regions, categories, start_date, end_date)
    summary = get_product_summary(filtered)
    return summary.head(limit).to_dict(orient="records")

@app.get("/revenue/monthly")
def read_monthly_revenue(
    regions: Optional[List[str]] = Query(None),
    categories: Optional[List[str]] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    df = get_data()
    filtered = apply_filters(df, regions, categories, start_date, end_date)
    summary = get_monthly_revenue_summary(filtered)
    return summary.to_dict(orient="records")

@app.get("/revenue/by-region")
def read_revenue_by_region(
    regions: Optional[List[str]] = Query(None),
    categories: Optional[List[str]] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    df = get_data()
    filtered = apply_filters(df, regions, categories, start_date, end_date)
    summary = get_revenue_by_region(filtered)
    return summary.to_dict(orient="records")

@app.get("/revenue/by-category")
def read_revenue_by_category(
    regions: Optional[List[str]] = Query(None),
    categories: Optional[List[str]] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    df = get_data()
    filtered = apply_filters(df, regions, categories, start_date, end_date)
    summary = get_revenue_by_category(filtered)
    return summary.to_dict(orient="records")

@app.get("/revenue/regional-monthly")
def read_regional_monthly_revenue(
    regions: Optional[List[str]] = Query(None),
    categories: Optional[List[str]] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    df = get_data()
    filtered = apply_filters(df, regions, categories, start_date, end_date)
    summary = get_regional_monthly_revenue(filtered)
    return summary.to_dict(orient="records")

@app.get("/revenue/region-category")
def read_revenue_by_region_category(
    regions: Optional[List[str]] = Query(None),
    categories: Optional[List[str]] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    df = get_data()
    filtered = apply_filters(df, regions, categories, start_date, end_date)
    if filtered.empty:
        return []
    
    pivot = filtered.pivot_table(
        values="TotalSales",
        index="Region",
        columns="Category",
        aggfunc="sum",
        fill_value=0,
    )
    # Convert pivot table to a format suitable for px.imshow or similar
    return pivot.to_dict(orient="index")

@app.get("/data-quality")
def read_data_quality():
    df = get_data()
    if df.empty:
        return {"stats": {}, "profile": []}
        
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
    return {
        "stats": {
            "rows": len(df),
            "columns": df.shape[1],
            "duplicate_rows": int(df.duplicated().sum()),
            "missing_cells": int(df.isna().sum().sum()),
        },
        "profile": profile.to_dict(orient="records")
    }

@app.get("/filters")
def read_filters():
    df = get_data()
    if df.empty:
        return {"regions": [], "categories": [], "date_range": {}}
        
    return {
        "regions": sorted(df["Region"].dropna().unique().tolist()),
        "categories": sorted(df["Category"].dropna().unique().tolist()),
        "date_range": {
            "min": df["OrderDate"].min().date(),
            "max": df["OrderDate"].max().date()
        }
    }

# -- HERE ONLY RUN THE MAIN SCRIPT IF THE FILE NAME IS MAIN --
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
