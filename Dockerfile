# --- Stage 1: Build Frontend ---
FROM node:20 AS frontend-builder
WORKDIR /frontend-build
# Copy package files first for better caching
COPY frontend/package*.json ./
RUN npm install
# Copy the rest of the frontend source
COPY frontend/ ./
RUN npm run build

# --- Stage 2: Build Backend ---
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy backend dependency files
COPY backend/pyproject.toml backend/uv.lock ./
# Install dependencies without the project itself to cache faster
RUN uv sync --frozen --no-dev --no-install-project

# Copy the actual backend code
COPY backend/ .

# Install the project now that source is present
RUN uv sync --frozen --no-dev

# Copy built frontend from Stage 1 into the static directory
COPY --from=frontend-builder /frontend-build/dist ./static

# Expose the port for Cloud Run
EXPOSE 8080

# Production Environment Variables
ENV GOOGLE_LOCATION="us-central1"
ENV ENVIRONMENT="production"
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
