#!/usr/bin/env bash
set -e

# ── Setup venv if missing ─────────────────────────────────────────────────────
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3.11 -m venv .venv
fi

# ── Install / sync Python deps ────────────────────────────────────────────────
echo "Installing Python dependencies..."
.venv/bin/pip install -q -r requirements.txt

# ── Reflex init (generates .web/ if missing) ──────────────────────────────────
if [ ! -d ".web" ]; then
  echo "Initializing Reflex..."
  .venv/bin/reflex init
fi

# ── Install Node deps if missing ─────────────────────────────────────────────
if [ ! -d ".web/node_modules" ]; then
  echo "Installing Node dependencies..."
  (cd .web && npm install)
fi

# ── Run ───────────────────────────────────────────────────────────────────────
echo "Starting ProHandyman..."
.venv/bin/reflex run
