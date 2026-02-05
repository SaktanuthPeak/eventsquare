# Multi-stage build for Python FastAPI backend
FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false

# Add poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock poetry.toml ./

# Install dependencies (without dev dependencies for production)
RUN poetry install --no-root --only main

# Copy application code
COPY . .

# Install the package in editable mode so Python can find api_app
RUN poetry install --only-root

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Set PYTHONPATH to ensure api_app is found
ENV PYTHONPATH=/app

# Expose port
EXPOSE 9000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:9000/docs')" || exit 1

# Default command (can be overridden in docker-compose)
CMD ["python", "-m", "uvicorn", "api_app.cmd.api:app", "--host", "0.0.0.0", "--port", "9000"]
