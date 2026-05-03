# --- Stage 1: Build Frontend ---
FROM node:20 AS frontend-builder
WORKDIR /frontend-build
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# --- Stage 2: Build Backend ---
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory to /app
WORKDIR /app

# Copy backend dependency files
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy the actual backend code
# IMPORTANT: We copy the content of backend/ into /app
COPY backend/ .

# Install the project
RUN uv sync --frozen --no-dev

# Copy built frontend into a 'static' folder inside the backend app directory
# This ensures FastAPI can find it at 'app/static' or './static'
COPY --from=frontend-builder /frontend-build/dist ./static

# Expose the port
EXPOSE 8080

# Production Environment Variables
ENV GOOGLE_LOCATION="us-central1"
ENV ENVIRONMENT="production"
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Command to run the application
# We use the full module path
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
