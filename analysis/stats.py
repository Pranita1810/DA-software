from __future__ import annotations

import pandas as pd
from scipy import stats as scipy_stats


def zscore_table(df: pd.DataFrame) -> pd.DataFrame:
    numeric = df.select_dtypes(include="number")
    return numeric.apply(scipy_stats.zscore, nan_policy="omit")


def normality_tests(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for column in df.select_dtypes(include="number").columns:
        series = df[column].dropna()
        if len(series) < 8:
            continue
        stat, p_value = scipy_stats.shapiro(series[:5000])
        rows.append(
            {
                "column": column,
                "shapiro_W": round(float(stat), 4),
                "p_value": round(float(p_value), 4),
                "normal?": "Yes" if p_value > 0.05 else "No",
            }
        )
    return pd.DataFrame(rows)


def group_agg(df: pd.DataFrame, group_col: str, value_col: str) -> pd.DataFrame:
    return (
        df.groupby(group_col)[value_col]
        .agg(count="count", mean="mean", median="median", std="std", min="min", max="max")
        .round(2)
        .reset_index()
    )


def time_series_resample(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    freq: str = "W",
) -> pd.DataFrame:
    ts = df.set_index(pd.to_datetime(df[date_col]))[value_col]
    resampled = ts.resample(freq).agg(["sum", "mean", "count"]).reset_index()
    resampled.columns = ["date", "sum", "mean", "count"]
    return resampled
