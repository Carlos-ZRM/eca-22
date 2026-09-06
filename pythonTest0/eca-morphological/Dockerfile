FROM registry.access.redhat.com/ubi9/python-314:9.8-1788411927

WORKDIR /app

# ── System libs required by OpenCV ────────────────────────────────────────────
USER root
RUN dnf install -y --nodocs \
        libGL \
        libGLU \
        glib2 \
    && dnf clean all

# ── Poetry ────────────────────────────────────────────────────────────────────
RUN pip install --no-cache-dir poetry

# Install into the system Python (no virtualenv inside the container)
# PYO3_USE_ABI3_FORWARD_COMPATIBILITY lets pydantic-core (PyO3 ≤0.24) build
# against the stable ABI on Python 3.14+ until pydantic-core ships native support
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1

# ── Dependencies ──────────────────────────────────────────────────────────────
COPY pyproject.toml poetry.lock* ./
RUN poetry install --only main --no-root

# ── Application source ────────────────────────────────────────────────────────
COPY src/       ./src/
COPY templates/ ./templates/
COPY static/    ./static/

# ── Runtime config ────────────────────────────────────────────────────────────
ENV PYTHONPATH=/app/src \
    MPLCONFIGDIR=/tmp

# OpenShift-compatible permissions
RUN chown -R 0:0 /app && chmod -R g=u /app
USER 1001

EXPOSE 8080

CMD ["uvicorn", "web-app:app", \
     "--host", "0.0.0.0", \
     "--port", "8080", \
     "--log-config", "src/log_config.json"]
