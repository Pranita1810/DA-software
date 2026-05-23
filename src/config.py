from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "DataSets"
RAW_DATA_FILES = {
    "orders": DATA_DIR / "Orders.csv",
    "customers": DATA_DIR / "Customers.csv",
    "products": DATA_DIR / "Products.csv",
}
FINAL_DATA_PATH = DATA_DIR / "FinalSalesData.csv"

# --- Column Definitions ---
DATE_COLUMNS = ["OrderDate", "CustomerSince"]
ID_COLUMNS = ["OrderID", "CustomerID", "ProductID"]

# --- Dashboard Metadata ---
APP_TITLE = "DataPulse Sales Dashboard"
PAGE_ICON = "⚡"

# --- UI Constants ---
PAGES = ["Home", "Revenue", "Products", "Customers", "Data Quality"]
COLORS = {
    "primary": "#14b8a6",
    "secondary": "#8b5cf6",
    "background": "#090b12",
    "surface": "#101421",
    "line": "#273148",
    "text": "#eef3ff",
    "muted": "#94a3b8",
}
