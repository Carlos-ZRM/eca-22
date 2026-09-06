#!/bin/bash
set -euo pipefail

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------
appns=xpk
name=eca-morphological
appport=8080
routename="route-$name"

REBUILD=false
RECREATE=false

# ------------------------------------------------------------------
# Flags
# ------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --rebuild)
      REBUILD=true
      shift
      ;;
    --recreate)
      RECREATE=true
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [--rebuild] [--recreate]"
      echo "  --rebuild   Trigger a new build (bc/app/route must already exist)"
      echo "  --recreate  Delete and recreate bc/imagestream/app/route from scratch"
      exit 0
      ;;
    *)
      echo "Unknown flag: $1" >&2
      exit 1
      ;;
  esac
done

if $REBUILD && $RECREATE; then
  echo "Error: --rebuild and --recreate are mutually exclusive." >&2
  exit 1
fi

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
exists() {
  oc get "$1" "$2" -n "$appns" >/dev/null 2>&1
}

ensure_namespace() {
  if ! oc get namespace "$appns" >/dev/null 2>&1; then
    echo "Namespace $appns does not exist. Creating..."
    oc create namespace "$appns"
  else
    echo "Namespace $appns already exists."
  fi
  oc project "$appns"
}

ensure_buildconfig() {
  if exists bc "$name"; then
    echo "BuildConfig $name already exists."
  else
    echo "BuildConfig $name does not exist. Creating..."
    oc new-build --name "$name" --binary --strategy docker -n "$appns"
  fi
}

ensure_app() {
  if exists deployment "$name" || exists dc "$name"; then
    echo "App (Deployment) $name already exists."
  else
    echo "App $name does not exist. Creating..."
    oc new-app "image-registry.openshift-image-registry.svc:5000/$appns/$name" -n "$appns"
  fi
}

ensure_route() {
  if exists route "$routename"; then
    echo "Route $routename already exists."
  else
    echo "Route $routename does not exist. Creating..."
    oc create route edge "$routename" --service="$name" -n "$appns" --port="$appport"
  fi
}

run_build() {
  echo "Starting build for $name..."
  oc start-build "$name" --from-dir . --follow -n "$appns"
}

recreate_all() {
  echo "Recreating all resources for $name..."
  oc delete route      "$routename" -n "$appns" --ignore-not-found
  oc delete deployment "$name"      -n "$appns" --ignore-not-found
  oc delete dc         "$name"      -n "$appns" --ignore-not-found
  oc delete svc        "$name"      -n "$appns" --ignore-not-found
  oc delete bc         "$name"      -n "$appns" --ignore-not-found
  oc delete is         "$name"      -n "$appns" --ignore-not-found

  ensure_buildconfig
  run_build
  ensure_app
  ensure_route
}

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
ensure_namespace

if $REBUILD; then
  if ! exists bc "$name"; then
    echo "Error: BuildConfig $name not found. Run without --rebuild first (or use --recreate)." >&2
    exit 1
  fi
  run_build
  exit 0
fi

if $RECREATE; then
  recreate_all
  exit 0
fi

# Default: idempotent create-if-missing, then build
ensure_buildconfig
run_build
ensure_app
ensure_route
