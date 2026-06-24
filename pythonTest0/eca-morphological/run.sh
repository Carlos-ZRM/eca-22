#!/bin/bash
# Run the web app from the project root with timestamps in logs
PYTHONPATH=src uvicorn web-app:app --reload --log-config src/log_config.json
