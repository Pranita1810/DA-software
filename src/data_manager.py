from __future__ import annotations

from pathlib import Path
import pandas as pd
from src.config import FINAL_DATA_PATH, DATE_COLUMNS


def load_sales_data(path: str | Path = FINAL_DATA_PATH) -> pd.DataFrame:
    """Load the merged sales dataset and normalize key date columns."""
    if not Path(path).exists():
        # Fallback for CI or first runs if pipeline hasn't run
        return pd.DataFrame()
        
    data = pd.read_csv(path)
    for column in DATE_COLUMNS:
        if column in data.columns:
            data[column] = pd.to_datetime(
                data[column],
                format="mixed",
                dayfirst=True,
                errors="coerce",
            )
    return data


def get_sales_metrics(data: pd.DataFrame) -> dict[str, float | int]:
    """Calculate core KPI values."""
    if data.empty:
        return {
            "total_revenue": 0.0,
            "total_orders": 0,
            "unique_customers": 0,
            "avg_order_value": 0.0,
            "units_sold": 0,
        }

    total_orders = int(data["OrderID"].nunique()) if "OrderID" in data else len(data)
    total_revenue = float(data["TotalSales"].sum())
    
    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "unique_customers": int(data["CustomerID"].nunique()),
        "avg_order_value": total_revenue / total_orders if total_orders else 0.0,
        "units_sold": int(data["Quantity"].sum()) if "Quantity" in data else 0,
    }
