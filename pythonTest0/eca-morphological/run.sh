#!/bin/bash
# Run the web app from the project root with timestamps in logs
PYTHONPATH=src;
poetry run uvicorn web-app:app --reload --log-config src/log_config.json
