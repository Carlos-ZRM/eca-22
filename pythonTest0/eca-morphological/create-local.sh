#!/bin/bash
set -euo pipefail

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------
IMAGE_NAME=eca-morphological
CONTAINER_NAME=eca-morphological
HOST_PORT=8080
CONTAINER_PORT=8080

# ------------------------------------------------------------------
# Help
# ------------------------------------------------------------------
usage() {
  cat <<HELP
Usage: $(basename "$0") [OPTIONS]

  Rebuild the $IMAGE_NAME image with Poetry and recreate the container.
  Every run performs a full stop → remove → build → start cycle.

Options:
  -h, --help    Show this help message and exit

Examples:
  ./$(basename "$0")          Full rebuild and recreate
  podman logs -f $CONTAINER_NAME   Follow container logs after start

Notes:
  - Requires Podman and a valid Dockerfile in the current directory.
  - Poetry is used inside the image to install dependencies.
  - App will be available at http://localhost:$HOST_PORT
HELP
  exit 0
}

# ------------------------------------------------------------------
# Flags
# ------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage ;;
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
  podman run \
    --detach \
    --name   "$CONTAINER_NAME" \
    --publish "$HOST_PORT:$CONTAINER_PORT" \
    --restart unless-stopped \
    "$IMAGE_NAME"
  ok "Container $CONTAINER_NAME running → http://localhost:$HOST_PORT"
}

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
stop_container
remove_image
build_image
run_container

log "Done. Follow logs with: podman logs -f $CONTAINER_NAME"
