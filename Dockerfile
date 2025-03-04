# === Stage 1: Builder Stage ===
FROM python:3.9-slim AS builder

# Set working directory
WORKDIR /app

# Copy only requirements file first to leverage caching
COPY requirements.txt .

# Install dependencies in a virtual environment
RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir -r requirements.txt

# === Stage 2: Final Lightweight Image ===
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy only necessary files from the builder stage
COPY --from=builder /venv /venv
COPY s3_proxy.py ./

# Use the pre-installed virtual environment
ENV PATH="/venv/bin:$PATH"

# Expose the API port
EXPOSE 5001

# Run the application
CMD ["python", "s3_proxy.py"]
