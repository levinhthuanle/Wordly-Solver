FROM python:3.13.10-slim-trixie

ENV UV_HOME="/root/.local/bin" \
    PATH="/root/.local/bin:$PATH"

# Install curl for health checks and download certificates for uv installer
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Download and install uv
ADD https://astral.sh/uv/install.sh /tmp/uv-installer.sh
RUN sh /tmp/uv-installer.sh \
    && rm /tmp/uv-installer.sh

WORKDIR /app

# Copy lock files (and README needed for build metadata) first to leverage cache
COPY pyproject.toml uv.lock README.md ./

# Install dependencies into the managed virtualenv
RUN uv sync --frozen --no-dev

# Copy application source
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run with uvicorn using uv's managed environment
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
