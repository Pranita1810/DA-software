import pandas as pd
import os

# Resolve paths relative to project root — works on any OS / Docker
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DS = os.path.join(BASE_DIR, "DataSets")

# Load data
orders    = pd.read_csv(os.path.join(DS, "Orders.csv"))
customers = pd.read_csv(os.path.join(DS, "Customers.csv"))
products  = pd.read_csv(os.path.join(DS, "Products.csv"))

# Clean data
orders    = orders.drop_duplicates()
customers = customers.drop_duplicates()
products  = products.drop_duplicates()

orders["OrderDate"]        = pd.to_datetime(orders["OrderDate"])
customers["CustomerSince"] = pd.to_datetime(customers["CustomerSince"])

# Merge data (Star Schema join)
sales_data = orders.merge(customers, on="CustomerID")
sales_data = sales_data.merge(products, on="ProductID")

# Export merged dataset
output_path = os.path.join(DS, "FinalSalesData.csv")
sales_data.to_csv(output_path, index=False)

print(f"Pipeline completed — {len(sales_data):,} rows written to {output_path}")
