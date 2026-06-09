# DataPulse Sales Dashboard

DataPulse is a full-stack analytics application for exploring retail sales data. It features a FastAPI backend for data processing and a Streamlit frontend for interactive visualization.

## Features

- **FastAPI Backend**: Robust API serving metrics, aggregations, and data quality stats.
- **Streamlit Frontend**: Interactive dashboard with real-time filtering and rich visualizations.
- Revenue KPIs: total revenue, orders, customers, and average order value.
- Sidebar filters for region, category, and order date range.
- Revenue trend, region/category heatmap, and category mix charts.
- Product leaderboard with units, orders, and revenue.
- Customer segmentation by region and age group.
- Data-quality profile with missing values, duplicate rows, and sample records.
- Docker support for reproducible multi-service local runs.

## Project Structure

```text
EDA SOFTWARE/
├── api.py                    # FastAPI backend server
├── app.py                    # Streamlit dashboard (consumes API)
├── start.sh                  # Startup script for both services
├── DataSets/                 # Orders, customers, products, merged sales data
├── src/
│   ├── config.py             # App configurations and constants
│   ├── data_manager.py       # Sales data loading and KPI helpers
│   ├── aggregations.py       # Core data aggregation logic
│   ├── pipeline.py           # Source-table join pipeline
│   ├── components.py         # Streamlit UI components
│   └── styles.py             # CSS and HTML styling
├── analysis/                 # General EDA/statistics helpers
├── db__/                     # DB session helpers
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
# Run the API in one terminal
python api.py
# Run Streamlit in another terminal
streamlit run app.py
```

Then open `http://localhost:8501` for the dashboard and `http://localhost:8000/docs` for the API documentation.

## Run With Docker

```bash
docker compose up --build
```

- Dashboard: `http://localhost:8501`
- API: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`

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
