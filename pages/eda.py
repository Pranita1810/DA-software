import pandas as pd
import numpy as np


# ── Summary ──────────────────────────────────────────────────────────────────
def summary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Extended describe for numeric columns."""
    num = df.select_dtypes(include="number")
    if num.empty:
        return pd.DataFrame()
    desc = num.describe().T
    desc["skewness"] = num.skew().round(3)
    desc["kurtosis"] = num.kurt().round(3)
    desc["missing"]  = num.isna().sum()
    desc["missing%"] = (num.isna().mean() * 100).round(1)
    return desc.round(3)


def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    total   = df.isna().sum()
    pct     = (df.isna().mean() * 100).round(2)
    dtype   = df.dtypes.astype(str)
    uniq    = df.nunique()
    report  = pd.DataFrame({
        "missing_count": total,
        "missing_%":     pct,
        "dtype":         dtype,
        "unique_vals":   uniq,
    })
    return report[report["missing_count"] > 0].sort_values("missing_%", ascending=False)


def full_missing_report(df: pd.DataFrame) -> pd.DataFrame:
    total   = df.isna().sum()
    pct     = (df.isna().mean() * 100).round(2)
    dtype   = df.dtypes.astype(str)
    uniq    = df.nunique()
    return pd.DataFrame({
        "dtype":         dtype,
        "unique_vals":   uniq,
        "missing_count": total,
        "missing_%":     pct,
    }).sort_values("missing_%", ascending=False)


# ── Correlation ──────────────────────────────────────────────────────────────
def correlation_matrix(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
    num = df.select_dtypes(include="number")
    if num.shape[1] < 2:
        return pd.DataFrame()
    return num.corr(method=method).round(3)


# ── Outlier detection ────────────────────────────────────────────────────────
def iqr_outliers(df: pd.DataFrame, col: str) -> pd.Series:
    q1, q3 = df[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    mask = (df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)
    return df[mask][col]


def outlier_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col in df.select_dtypes(include="number").columns:
        outs = iqr_outliers(df, col)
        rows.append({"column": col, "outlier_count": len(outs),
                     "outlier_%": round(len(outs) / len(df) * 100, 2)})
    return pd.DataFrame(rows).sort_values("outlier_count", ascending=False)


# ── Distribution helpers ─────────────────────────────────────────────────────
def value_counts_top(df: pd.DataFrame, col: str, n: int = 15) -> pd.DataFrame:
    vc = df[col].value_counts().head(n).reset_index()
    vc.columns = [col, "count"]
    vc["pct"] = (vc["count"] / len(df) * 100).round(2)
    return vc


def numeric_cols(df: pd.DataFrame):
    return df.select_dtypes(include="number").columns.tolist()


def categorical_cols(df: pd.DataFrame):
    return df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()


def datetime_cols(df: pd.DataFrame):
    return df.select_dtypes(include=["datetime64"]).columns.tolist()
