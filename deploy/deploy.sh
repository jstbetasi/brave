#!/usr/bin/env bash
# Deploy script for the self-hosted server (Ubuntu + nginx + gunicorn).
# Run from the project root on the server: ./deploy/deploy.sh
set -euo pipefail

cd "$(dirname "$0")/.."

git pull
uv pip install -r requirements.txt
uv run python manage.py migrate
uv run python manage.py collectstatic --noinput
sudo systemctl restart no-bias-essay-grader
