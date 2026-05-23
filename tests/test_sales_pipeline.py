import unittest
import pandas as pd
from src.data_manager import get_sales_metrics
from src.aggregations import (
    get_customer_summary,
    get_product_summary,
    get_monthly_revenue_summary,
)
from src.pipeline import build_sales_dataset


class SalesPipelineTests(unittest.TestCase):
    def setUp(self):
        self.orders = pd.DataFrame(
            {
                "OrderID": [1, 2, 3],
                "CustomerID": [10, 10, 20],
                "ProductID": [100, 101, 100],
                "OrderDate": ["2024-01-01", "2024-01-15", "2024-02-01"],
                "Quantity": [2, 1, 3],
                "TotalSales": [200.0, 150.0, 300.0],
            }
        )
        self.customers = pd.DataFrame(
            {
                "CustomerID": [10, 20],
                "CustomerName": ["Asha Rao", "Ben Kim"],
                "Region": ["West", "East"],
                "Age": [34, 45],
                "Gender": ["Female", "Male"],
                "CustomerSince": ["2022-01-01", "2023-05-20"],
                "Email": ["asha@example.com", "ben@example.com"],
            }
        )
        self.products = pd.DataFrame(
            {
                "ProductID": [100, 101],
                "ProductName": ["Desk", "Chair"],
                "Category": ["Office", "Office"],
                "UnitPrice": [100.0, 150.0],
                "Supplier": ["Acme", "Acme"],
            }
        )
        self.sales = build_sales_dataset(self.orders, self.customers, self.products)

    def test_build_sales_dataset_joins_all_tables(self):
        self.assertEqual(len(self.sales), 3)
        self.assertIn("CustomerName", self.sales.columns)
        self.assertIn("ProductName", self.sales.columns)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.sales["OrderDate"]))

    def test_sales_metrics(self):
        metrics = get_sales_metrics(self.sales)
        self.assertEqual(metrics["total_orders"], 3)
        self.assertEqual(metrics["unique_customers"], 2)
        self.assertEqual(metrics["units_sold"], 6)
        self.assertAlmostEqual(metrics["total_revenue"], 650.0)
        self.assertAlmostEqual(metrics["avg_order_value"], 216.6666667)

    def test_product_customer_and_revenue_summaries(self):
        products = get_product_summary(self.sales)
        customers = get_customer_summary(self.sales)
        revenue = get_monthly_revenue_summary(self.sales)

        self.assertEqual(products.iloc[0]["ProductName"], "Desk")
        self.assertEqual(customers.iloc[0]["CustomerName"], "Asha Rao")
        self.assertEqual(list(revenue["OrderDate"]), ["2024-01", "2024-02"])


if __name__ == "__main__":
    unittest.main()
