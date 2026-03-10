FROM python:3.11-slim

# unzip is required by Reflex's bun installer
RUN apt-get update && apt-get install -y --no-install-recommends curl unzip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App source (.web is included; node_modules is excluded via .dockerignore)
COPY . .

# Generate .web/, install bun, build the frontend
# reflex init installs bun to /root/.bun/bin — add it to PATH for subsequent steps
RUN reflex init
ENV PATH="/root/.bun/bin:${PATH}"
RUN cd .web && bun install
RUN reflex export --frontend-only --no-zip

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

# Backend-only mode: serves pre-built static frontend + API + WebSocket
CMD ["reflex", "run", "--env", "prod", "--backend-only", \
     "--backend-host", "0.0.0.0", "--backend-port", "8000"]
