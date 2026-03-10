FROM python:3.11-slim

# Install system deps + bun (Reflex's JS runtime)
RUN apt-get update && apt-get install -y --no-install-recommends curl unzip && \
    rm -rf /var/lib/apt/lists/* && \
    curl -fsSL https://bun.sh/install | bash

ENV PATH="/root/.bun/bin:${PATH}"

WORKDIR /app

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App source
COPY . .

# Generate .web/ structure, install JS deps, pre-build the frontend
RUN reflex init
RUN cd .web && bun install
RUN reflex export --frontend-only --no-zip

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

# Backend-only mode: serves pre-built static frontend + API + WebSocket
CMD ["reflex", "run", "--env", "prod", "--backend-only", \
     "--backend-host", "0.0.0.0", "--backend-port", "8000"]
