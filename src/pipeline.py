from __future__ import annotations

import logging
from pathlib import Path
import pandas as pd
from src.config import RAW_DATA_FILES, FINAL_DATA_PATH, DATE_COLUMNS

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def parse_date_series(series: pd.Series) -> pd.Series:
    """Parse ISO and day-first dates consistently."""
    return pd.to_datetime(series, format="mixed", dayfirst=True, errors="coerce")


def load_source_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the orders, customers, and products source tables."""
    logger.info("Loading source CSV files...")
    try:
        orders = pd.read_csv(RAW_DATA_FILES["orders"])
        customers = pd.read_csv(RAW_DATA_FILES["customers"])
        products = pd.read_csv(RAW_DATA_FILES["products"])
        return orders, customers, products
    except FileNotFoundError as e:
        logger.error(f"Failed to load source files: {e}")
        raise


def build_sales_dataset(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    """Clean and join source tables into the dashboard-ready sales dataset."""
    logger.info("Processing and joining tables...")
    
    # Cleaning
    orders = orders.drop_duplicates().copy()
    customers = customers.drop_duplicates().copy()
    products = products.drop_duplicates().copy()

    # Date parsing
    if "OrderDate" in orders.columns:
        orders["OrderDate"] = parse_date_series(orders["OrderDate"])
    if "CustomerSince" in customers.columns:
        customers["CustomerSince"] = parse_date_series(customers["CustomerSince"])

    # Joins
    sales_data = orders.merge(customers, on="CustomerID", validate="many_to_one")
    sales_data = sales_data.merge(products, on="ProductID", validate="many_to_one")
    
    logger.info(f"Dataset built successfully. Total rows: {len(sales_data):,}")
    return sales_data


def run_pipeline():
    """Execute the full ETL process."""
    logger.info("Starting Sales Data Pipeline")
    orders, customers, products = load_source_tables()
    sales_data = build_sales_dataset(orders, customers, products)
    
    FINAL_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    sales_data.to_csv(FINAL_DATA_PATH, index=False)
    logger.info(f"Pipeline completed. Output saved to: {FINAL_DATA_PATH}")
    return sales_data


if __name__ == "__main__":
    run_pipeline()
