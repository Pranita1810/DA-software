import pandas as pd
import os

# Resolve path relative to this file — works on any OS / Docker
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "DataSets", "FinalSalesData.csv")

df = pd.read_csv(DATA_PATH)

# Parse dates
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# Total Revenue
total_revenue = df["TotalSales"].sum()

# Sales by Category
sales_by_category = df.groupby("Category")["TotalSales"].sum().sort_values(ascending=False)

# Top Products
top_products = df.groupby("ProductName")["TotalSales"].sum().sort_values(ascending=False).head(10)

# Sales by Region
sales_by_region = df.groupby("Region")["TotalSales"].sum().sort_values(ascending=False)

# Monthly Sales Trend
df["Month"] = df["OrderDate"].dt.to_period("M")
monthly_sales = df.groupby("Month")["TotalSales"].sum()
