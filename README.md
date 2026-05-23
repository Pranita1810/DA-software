# DataPulse Sales Dashboard

DataPulse is a Streamlit dashboard for exploring a retail sales dataset. It joins
orders, customers, and products into a single analytics table, then provides
interactive views for revenue trends, product performance, customer segments,
and data quality.

## Features

- Revenue KPIs: total revenue, orders, customers, and average order value
- Sidebar filters for region, category, and order date range
- Revenue trend, region/category heatmap, and category mix charts
- Product leaderboard with units, orders, and revenue
- Customer segmentation by region and age group
- Data-quality profile with missing values, duplicate rows, and sample records
- Docker support for reproducible local runs

## Project Structure

```text
EDA SOFTWARE/
├── app.py                    # Streamlit dashboard
├── DataSets/                 # Orders, customers, products, merged sales data
├── src/
│   ├── analysis.py           # Sales data loading and KPI helpers
│   ├── pipeline.py           # Source-table join pipeline
│   ├── product_.py           # Product aggregation helper
│   ├── customer_.py          # Customer aggregation helper
│   └── rev_.py               # Revenue aggregation helper
├── analysis/                 # General EDA/statistics helpers
├── db__/                     # Streamlit session helpers
├── db_config/                # SQL/upload utilities
├── tests/                    # Unit tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── requirements_docker.txt
```

## Run Locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501`.

## Run With Docker

```bash
docker compose up --build
```

Then open `http://localhost:8501`.

## Rebuild the Merged Dataset

```bash
python -m src.pipeline
```

This reads `DataSets/Orders.csv`, `DataSets/Customers.csv`, and
`DataSets/Products.csv`, then writes `DataSets/FinalSalesData.csv`.

## Run Tests

```bash
python -m unittest discover -s tests
```

## Notes

The dashboard expects these columns in the merged data:

`OrderID`, `CustomerID`, `ProductID`, `OrderDate`, `Quantity`, `TotalSales`,
`CustomerName`, `Region`, `Age`, `Gender`, `CustomerSince`, `ProductName`,
`Category`, and `UnitPrice`.
