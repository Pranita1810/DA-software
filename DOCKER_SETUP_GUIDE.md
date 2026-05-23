# Docker Setup Guide

This project includes a Docker image for running the Streamlit dashboard without
creating a local Python environment.

## Build and Run

```bash
docker compose up --build
```

Open the app at `http://localhost:8501`.

## Run in the Background

```bash
docker compose up --build -d
```

## View Logs

```bash
docker compose logs -f
```

## Stop the App

```bash
docker compose down
```

## Rebuild the Sales Dataset

If the source CSV files change, rebuild the merged dataset locally:

```bash
python -m src.pipeline
```

The compose file mounts `./DataSets` into the container, so changes to datasets
are reflected when the app restarts.
