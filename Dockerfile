# ── Base Image ────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ── System dependencies ────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Set working directory ──────────────────────────────────────────────────────
WORKDIR /app

# ── Copy requirements first (layer caching) ───────────────────────────────────
COPY requirements_docker.txt .

# ── Install Python dependencies ────────────────────────────────────────────────
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_docker.txt

# ── Copy entire project ────────────────────────────────────────────────────────
COPY . .

# ── Fix line endings for start.sh ──────────────────────────────────────────────
RUN apt-get update && apt-get install -y sed && \
    sed -i 's/\r$//' start.sh && \
    chmod +x start.sh

# ── Expose ports ─────────────────────────────────────────────────────────────
EXPOSE 8501 8000

# ── Healthcheck ───────────────────────────────────────────────────────────────
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# ── Entrypoint ────────────────────────────────────────────────────────────────
CMD ["./start.sh"]
