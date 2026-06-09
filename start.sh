#!/bin/bash

# Start FastAPI in the background
uvicorn api:app --host 0.0.0.0 --port 8000 &

# Start Streamlit in the foreground
streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
