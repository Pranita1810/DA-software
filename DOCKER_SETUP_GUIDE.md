# 🐳 EDA Software — Docker Setup Guide

## What's in this package

| File | Purpose |
|---|---|
| `Dockerfile` | Builds the container image |
| `docker-compose.yml` | Runs the container with one command |
| `requirements_docker.txt` | Python deps (Windows-only packages removed) |
| `src/analysis.py` | Fixed — relative paths replace hardcoded Windows paths |
| `src/pipeline.py` | Fixed — relative paths replace hardcoded Windows paths |

---

## Step 1 — Place files into your project folder

Your final project folder should look like this:

```
EDA SOFTWARE/
├── Dockerfile                  ← paste here
├── docker-compose.yml          ← paste here
├── requirements_docker.txt     ← paste here
├── app.py
├── src/
│   ├── analysis.py             ← replace with fixed version
│   ├── pipeline.py             ← replace with fixed version
│   └── ...
└── DataSets/
    ├── FinalSalesData.csv
    ├── Orders.csv
    ├── Customers.csv
    └── Products.csv
```

> ⚠️ Replace `src/analysis.py` and `src/pipeline.py` with the fixed versions
> provided — the originals have hardcoded Windows paths that break on Linux/Docker.

---

## Step 2 — Install Docker Desktop

Download from: https://www.docker.com/products/docker-desktop/

- **Windows**: Install Docker Desktop, enable WSL2 backend when prompted
- **Mac**: Install Docker Desktop for Mac (Apple Silicon or Intel)
- **Linux**: Install Docker Engine + Docker Compose plugin

Verify installation:
```bash
docker --version
docker compose version
```

---

## Step 3 — No venv needed inside Docker

Docker itself is the isolated environment. The `Dockerfile` installs all dependencies
inside the container using `pip` — you do NOT need to activate a venv.

However, if you want to run the app **locally** (outside Docker) too, set up a venv:
```bash
# Inside the EDA SOFTWARE folder:
python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install:
pip install -r requirements_docker.txt
```

---

## Step 4 — Build and run with Docker Compose

Open a terminal, navigate to the `EDA SOFTWARE` folder, and run:

```bash
# Build the image and start the container
docker compose up --build
```

First run takes ~3–5 minutes (downloading base image + installing packages).
Subsequent runs are fast (cached layers).

You'll see output like:
```
✔ Container eda_software  Started
...
  You can now view your Streamlit app in your browser.
  URL: http://0.0.0.0:8501
```

---

## Step 5 — Open the app

Visit in your browser: **http://localhost:8501**

---

## Useful Docker commands

```bash
# Run in background (detached mode)
docker compose up --build -d

# View logs
docker compose logs -f

# Stop the container
docker compose down

# Rebuild after code changes
docker compose up --build

# Access container shell (for debugging)
docker exec -it eda_software bash
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Port 8501 already in use | Change `"8501:8501"` to `"8502:8501"` in docker-compose.yml |
| Module not found error | Run `docker compose up --build` to rebuild |
| CSV not found error | Make sure `DataSets/` folder is present with all CSVs |
| Docker daemon not running | Open Docker Desktop app first |

---

## How it works

```
Your Machine
└── docker compose up
    └── Docker builds image:
        ├── python:3.11-slim base
        ├── pip install requirements_docker.txt
        └── COPY project files
    └── Docker runs container:
        └── streamlit run app.py --server.port=8501
            └── Accessible at localhost:8501
```
