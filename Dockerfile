FROM python:3.11-slim

# Install Node.js 20 (needed to build the Reflex frontend)
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App source (.web is included; node_modules is excluded via .dockerignore)
COPY . .

# Install Node dependencies and pre-build the frontend
RUN cd .web && npm install
RUN reflex export --frontend-only --no-zip

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

# Backend-only mode: serves pre-built static frontend + API + WebSocket
CMD ["reflex", "run", "--env", "prod", "--backend-only", \
     "--backend-host", "0.0.0.0", "--backend-port", "8000"]
