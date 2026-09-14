#!/bin/bash
set -euo pipefail

# ------------------------------------------------------------------
# Help
# ------------------------------------------------------------------
usage() {
  cat <<HELP
Usage: $(basename "$0") [OPTIONS]

  Run the ECA web app locally with Poetry (hot-reload enabled).

Options:
  --log-level <lvl>  Set uvicorn log level: debug | info (default) | warning | error | critical

  --debug-lines      Enable [lines] debug output in the browser console
  --debug-triangles  Enable [triangles] debug output in the browser console
  --debug-draw       Enable [draw] debug output in the browser console

  --port <port>      Port to listen on (default: 8000)

  -h, --help         Show this help message and exit

Examples:
  ./$(basename "$0")                              Default — INFO log, no JS debug
  ./$(basename "$0") --log-level debug            Verbose uvicorn output
  ./$(basename "$0") --debug-lines --debug-draw   Enable canvas JS debug flags
  ./$(basename "$0") --port 8080                  Run on port 8080

Notes:
  - Requires Poetry and the project's virtualenv to be set up.
  - App reloads automatically on source changes (--reload).
  - Debug flags are read by the Jinja2 template at request time via env vars.
  - App will be available at http://localhost:<port>
HELP
  exit 0
}

# ------------------------------------------------------------------
# Defaults
# ------------------------------------------------------------------
LOG_LEVEL="info"
PORT=8000
export DEBUG_LINES=0
export DEBUG_TRIANGLES=0
export DEBUG_DRAW=0

# ------------------------------------------------------------------
# Flags
# ------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --log-level)        LOG_LEVEL="$2"     ; shift 2 ;;
    --port)             PORT="$2"           ; shift 2 ;;
    --debug-lines)      export DEBUG_LINES=1     ; shift ;;
    --debug-triangles)  export DEBUG_TRIANGLES=1 ; shift ;;
    --debug-draw)       export DEBUG_DRAW=1      ; shift ;;
    -h|--help)          usage ;;
    *) echo "Unknown flag: $1" >&2; usage ;;
  esac
done

# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------
echo "[run] log-level : $LOG_LEVEL"
echo "[run] port      : $PORT"
[[ "$DEBUG_LINES"     == 1 ]] && echo "[run] debug     : lines"
[[ "$DEBUG_TRIANGLES" == 1 ]] && echo "[run] debug     : triangles"
[[ "$DEBUG_DRAW"      == 1 ]] && echo "[run] debug     : draw"
echo ""

# ------------------------------------------------------------------
# Launch
# ------------------------------------------------------------------
export PYTHONPATH=src

poetry run uvicorn web-app:app \
  --reload \
  --host 127.0.0.1 \
  --port "$PORT" \
  --log-level "$LOG_LEVEL" \
  --log-config src/log_config.json
