from __future__ import annotations

import pandas as pd


def get_customer_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate customer-level revenue and order activity."""
    return (
        data.groupby(["CustomerID", "CustomerName", "Region", "Gender"], as_index=False)
        .agg(Revenue=("TotalSales", "sum"), Orders=("OrderID", "count"), Age=("Age", "first"))
        .sort_values("Revenue", ascending=False)
    )


def get_product_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate product-level sales performance."""
    return (
        data.groupby(["ProductID", "ProductName", "Category"], as_index=False)
        .agg(Revenue=("TotalSales", "sum"), Units=("Quantity", "sum"), Orders=("OrderID", "count"))
        .sort_values("Revenue", ascending=False)
    )


def get_monthly_revenue_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate monthly revenue and order counts."""
    summary = (
        data.groupby(data["OrderDate"].dt.to_period("M"))
        .agg(Revenue=("TotalSales", "sum"), Orders=("OrderID", "count"))
        .reset_index()
    )
    summary["OrderDate"] = summary["OrderDate"].astype(str)
    return summary


def get_revenue_by_region(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.groupby("Region", as_index=False)["TotalSales"]
        .sum()
        .sort_values("TotalSales", ascending=False)
    )


def get_revenue_by_category(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.groupby("Category", as_index=False)["TotalSales"]
        .sum()
        .sort_values("TotalSales", ascending=False)
    )


def get_regional_monthly_revenue(data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue by region and month for 3D analysis."""
    summary = (
        data.groupby(["Region", data["OrderDate"].dt.to_period("M")], as_index=False)
        .agg(Revenue=("TotalSales", "sum"))
    )
    summary["OrderDate"] = summary["OrderDate"].astype(str)
    return summary
