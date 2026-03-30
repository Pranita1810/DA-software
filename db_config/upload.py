import pyodbc
import pandas as pd
import numpy as np

# --- Read Data ---
orders_df = pd.read_csv(r"C:\Users\PANRIT\ALL\Pranit Main\PROJECTS\EDA SOFTWARE\DataSets\Orders.csv")
customer_df = pd.read_csv(r"C:\Users\PANRIT\ALL\Pranit Main\PROJECTS\EDA SOFTWARE\DataSets\Customers.csv")
product_df = pd.read_csv(r"C:\Users\PANRIT\ALL\Pranit Main\PROJECTS\EDA SOFTWARE\DataSets\Products.csv")


class DataUploader:

    def __init__(self):
        self.conn = pyodbc.connect(
            "DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=EDA_PROJECT;Trusted_Connection=yes"
        )
        self.cursor = self.conn.cursor()

    def clean_data(self, df, decimal_cols=[], int_cols=[], date_cols=[]):
        df = df.drop_duplicates().copy()

        for col in decimal_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        for col in int_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        for col in date_cols:
            if col in df.columns:
                # ✅ dayfirst=True fixes the DD-MM-YYYY warning
                df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)

        return df

    def safe_value(self, val, col_type):
        """Convert every value to a plain Python type SQL Server accepts."""
        if val is None:
            return None
        try:
            if isinstance(val, float) and np.isnan(val):
                return None
        except:
            pass
        if hasattr(val, 'item'):  # strip numpy scalars
            val = val.item()

        if col_type == 'decimal':
            try:
                return round(float(val), 2)
            except:
                return None

        elif col_type == 'int':
            try:
                return int(val)
            except:
                return None

        elif col_type == 'date':
            try:
                ts = pd.Timestamp(val)
                if pd.isnull(ts):
                    return None
                # ✅ Return as 'YYYY-MM-DD' string — works with all ODBC driver versions
                return ts.strftime('%Y-%m-%d')
            except:
                return None

        else:
            # string/varchar columns
            if isinstance(val, float) and np.isnan(val):
                return None
            return str(val).strip() if val is not None else None

    def upload_bulk(self, df, table_name, decimal_cols=[], int_cols=[], date_cols=[]):
        df = self.clean_data(df, decimal_cols, int_cols, date_cols)

        col_type_map = {}
        for c in decimal_cols: col_type_map[c] = 'decimal'
        for c in int_cols:     col_type_map[c] = 'int'
        for c in date_cols:    col_type_map[c] = 'date'

        columns = ",".join(df.columns)
        placeholders = ",".join(["?"] * len(df.columns))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        for _, row in df.iterrows():
            data = tuple(
                self.safe_value(row[col], col_type_map.get(col, 'str'))
                for col in df.columns
            )
            self.cursor.execute(query, data)

        self.conn.commit()
        print(f"✅ {table_name} uploaded successfully ({len(df)} rows)")


# --- Run ---
def main_uploader():
    uploader = DataUploader()

    uploader.upload_bulk(
        orders_df, "Orders",
        decimal_cols=["TotalSales"],
        int_cols=["OrderID", "CustomerID", "ProductID", "Quantity"],
        date_cols=["OrderDate"]
    )

    uploader.upload_bulk(
        customer_df, "Customers",
        int_cols=["CustomerID"],
        date_cols=["CustomerSince"]
    )

    uploader.upload_bulk(
        product_df, "Products",
        decimal_cols=["UnitPrice"],
        int_cols=["ProductID"]
    )