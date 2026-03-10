FROM python:3.11-slim

# nginx for static files, supervisor to manage processes, unzip+curl for bun
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl unzip nginx supervisor && \
    rm -rf /var/lib/apt/lists/* && \
    curl -fsSL https://bun.sh/install | bash

ENV PATH="/root/.bun/bin:${PATH}"

WORKDIR /app

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App source
COPY . .

# Generate .web/ scaffold and install JS deps
RUN reflex init
RUN cd .web && bun install

# Compile Python components → React, then build the frontend bundle
# Output lands in .web/build/client/ (what nginx serves)
RUN reflex export --frontend-only --no-zip

# Drop bun and node_modules — not needed at runtime, frees ~150mb
RUN rm -rf /root/.bun .web/node_modules

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV GRANIAN_WORKERS=1
ENV MALLOC_ARENA_MAX=2

# supervisord starts nginx (static files on :8000) and the Reflex
# backend-only process (WebSocket + API on 127.0.0.1:8001)
CMD ["/usr/bin/supervisord", "-c", "/app/supervisord.conf"]
