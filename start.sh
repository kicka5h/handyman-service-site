#!/usr/bin/env bash
set -e

reflex db init
exec reflex run --env prod --backend-host 0.0.0.0 --backend-port 8000
