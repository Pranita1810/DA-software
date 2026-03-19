import io
import pandas as pd
import streamlit as st


SUPPORTED = {
    "csv":     pd.read_csv,
    "xlsx":    pd.read_excel,
    "xls":     pd.read_excel,
    "parquet": pd.read_parquet,
    "json":    pd.read_json,
}


def load_uploaded_file(uploaded) -> pd.DataFrame:
    """Read a Streamlit UploadedFile into a DataFrame."""
    ext = uploaded.name.rsplit(".", 1)[-1].lower()
    if ext not in SUPPORTED:
        raise ValueError(f"Unsupported file type: .{ext}")
    raw = uploaded.read()
    return SUPPORTED[ext](io.BytesIO(raw))


def load_sample(name: str = "sales") -> pd.DataFrame:
    """Return a built-in sample dataset for demo purposes."""
    import numpy as np
    rng = np.random.default_rng(42)

    if name == "sales":
        n = 500
        dates = pd.date_range("2024-01-01", periods=n, freq="D")[:n]
        df = pd.DataFrame({
            "date":     pd.to_datetime(rng.choice(dates, n)),
            "region":   rng.choice(["North", "South", "East", "West"], n),
            "product":  rng.choice(["Widget A", "Widget B", "Widget C", "Widget D"], n),
            "channel":  rng.choice(["Online", "Retail", "B2B"], n),
            "units":    rng.integers(1, 200, n),
            "revenue":  rng.uniform(500, 50_000, n).round(2),
            "cost":     rng.uniform(200, 20_000, n).round(2),
            "csat":     rng.uniform(2.5, 5.0, n).round(1),
        })
        df["profit"] = (df["revenue"] - df["cost"]).round(2)
        return df.sort_values("date").reset_index(drop=True)

    if name == "hr":
        n = 300
        df = pd.DataFrame({
            "emp_id":     range(1001, 1001 + n),
            "department": rng.choice(["Engineering","Sales","Marketing","HR","Finance"], n),
            "level":      rng.choice(["Junior","Mid","Senior","Lead","Manager"], n),
            "salary":     rng.integers(35_000, 180_000, n),
            "tenure_yrs": rng.uniform(0.5, 20, n).round(1),
            "perf_score": rng.uniform(1, 5, n).round(2),
            "remote":     rng.choice([True, False], n),
        })
        return df

    raise ValueError(f"Unknown sample: {name}")


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning: strip whitespace from string cols, parse obvious dates."""
    for col in df.select_dtypes("object").columns:
        df[col] = df[col].str.strip()
    return df
