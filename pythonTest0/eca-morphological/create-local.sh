#!/bin/bash
set -euo pipefail

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------
IMAGE_NAME=eca-morphological
CONTAINER_NAME=eca-morphological
HOST_PORT=8088
CONTAINER_PORT=8080

# ------------------------------------------------------------------
# Help
# ------------------------------------------------------------------
usage() {
  cat <<HELP
Usage: $(basename "$0") [OPTIONS]

  Build the $IMAGE_NAME image and run the container.
  By default (no flags) runs the full stop → remove → build → start cycle.

Options:
  --rebuild          Full cycle: stop container, remove image, build, start   (default)
  --rerun            Fast cycle: stop container, start — skips image build

  --theme <name>     Set the colour preset at runtime (no rebuild needed with --rerun)
                     Presets: atelier (default) | electric | sage | violet | lagoon |
                              foundry | stencil | gantry | lacquer | nocturne | primer | sorbet

  --debug-lines      Enable [lines] debug output in the browser console
  --debug-triangles  Enable [triangles] debug output in the browser console
  --debug-draw       Enable [draw] debug output in the browser console

  --log-level <lvl>  Set uvicorn log level: debug | info (default) | warning | error | critical

  -h, --help         Show this help message and exit

Examples:
  ./$(basename "$0")                                 Full rebuild, default theme, INFO log
  ./$(basename "$0") --rebuild --theme nocturne      Rebuild with Nocturne colour preset
  ./$(basename "$0") --rerun  --theme primer         Switch theme without rebuilding
  ./$(basename "$0") --rerun  --debug-lines --debug-draw   JS canvas debug, no rebuild
  ./$(basename "$0") --rebuild --log-level debug     Verbose uvicorn logs
  podman logs -f $CONTAINER_NAME                     Follow container logs after start

Notes:
  - Requires Podman and a valid Dockerfile in the current directory.
  - Poetry is used inside the image to install dependencies.
  - App will be available at http://localhost:$HOST_PORT
  - Debug flags inject env vars into the container and are read by the Jinja2
    template at request time — they affect only the running container, not the image.
HELP
  exit 0
}

# ------------------------------------------------------------------
# Flags
# ------------------------------------------------------------------
MODE=rebuild
THEME=""
LOG_LEVEL="info"
DEBUG_LINES=0
DEBUG_TRIANGLES=0
DEBUG_DRAW=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --rebuild)          MODE=rebuild         ; shift ;;
    --rerun)            MODE=rerun           ; shift ;;
    --theme)            THEME="$2"           ; shift 2 ;;
    --log-level)        LOG_LEVEL="$2"       ; shift 2 ;;
    --debug-lines)      DEBUG_LINES=1        ; shift ;;
    --debug-triangles)  DEBUG_TRIANGLES=1    ; shift ;;
    --debug-draw)       DEBUG_DRAW=1         ; shift ;;
    -h|--help)          usage ;;
    *) echo "Unknown flag: $1" >&2; usage ;;
  esac
done

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
log() { echo "[$(date '+%H:%M:%S')] $*"; }
ok()  { echo "[$(date '+%H:%M:%S')] ✓ $*"; }

stop_container() {
  if podman container exists "$CONTAINER_NAME" 2>/dev/null; then
    log "Stopping container $CONTAINER_NAME..."
    podman stop "$CONTAINER_NAME" --ignore >/dev/null
    log "Removing container $CONTAINER_NAME..."
    podman rm   "$CONTAINER_NAME" --force  >/dev/null
    ok "Container removed."
  else
    log "No existing container named $CONTAINER_NAME."
  fi
}

remove_image() {
  if podman image exists "$IMAGE_NAME" 2>/dev/null; then
    log "Removing old image $IMAGE_NAME..."
    podman rmi "$IMAGE_NAME" --force >/dev/null
    ok "Old image removed."
  fi
}

build_image() {
  log "Building image $IMAGE_NAME with Poetry..."
  podman build \
    --tag "$IMAGE_NAME" \
    --file Dockerfile \
    .
  ok "Image $IMAGE_NAME built."
}

run_container() {
  log "Starting container $CONTAINER_NAME on port $HOST_PORT..."

  # Build env-var args
  local env_args=(
    --env "UVICORN_LOG_LEVEL=${LOG_LEVEL}"
    --env "DEBUG_LINES=${DEBUG_LINES}"
    --env "DEBUG_TRIANGLES=${DEBUG_TRIANGLES}"
    --env "DEBUG_DRAW=${DEBUG_DRAW}"
  )
  [[ -n "$THEME" ]] && env_args+=(--env "THEME_PRESET=${THEME}")

  # Log active debug options
  [[ "$LOG_LEVEL" != "info" ]] && log "  log-level  : $LOG_LEVEL"
  [[ -n "$THEME"            ]] && log "  theme      : $THEME"
  [[ "$DEBUG_LINES"     == 1 ]] && log "  debug      : lines"
  [[ "$DEBUG_TRIANGLES" == 1 ]] && log "  debug      : triangles"
  [[ "$DEBUG_DRAW"      == 1 ]] && log "  debug      : draw"

  podman run \
    --detach \
    --name    "$CONTAINER_NAME" \
    --publish "$HOST_PORT:$CONTAINER_PORT" \
    --restart unless-stopped \
    "${env_args[@]}" \
    "$IMAGE_NAME"

  ok "Container $CONTAINER_NAME running → http://localhost:$HOST_PORT"
}

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
case "$MODE" in
  rebuild)
    log "Mode: full rebuild"
    stop_container
    remove_image
    build_image
    run_container
    ;;
  rerun)
    log "Mode: rerun (skipping image build)"
    stop_container
    run_container
    ;;
esac

log "Done. Follow logs with: podman logs -f $CONTAINER_NAME"
