# frontend/Dockerfile

# --- 1. The "Builder" Stage ---
# This stage installs all dependencies, including build-time tools.
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Add the virtual environment's bin to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Install system dependencies needed to build some Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ \
    && rm -rf /var/lib/apt/lists/*

# Create and activate a virtual environment
RUN python -m venv .venv

# Copy and install Python dependencies into the virtual environment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# --- 2. The "Final" Stage ---
# This stage creates the clean, final production image.
FROM python:3.11-slim AS final

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser

# Copy the virtual environment with installed packages from the builder stage
COPY --from=builder --chown=appuser:appuser /app/.venv ./.venv

# Copy the application code
COPY --chown=appuser:appuser . .

# Switch to the non-root user
USER appuser

# Expose the port Streamlit runs on
EXPOSE 8501

# Health check using Streamlit's built-in endpoint
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the Streamlit application, ensuring it's accessible from outside the container
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]