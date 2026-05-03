# --- Stage 1: Build Frontend ---
FROM node:20-slim AS frontend-builder
WORKDIR /frontend-build
COPY ../frontend/package*.json ./
RUN npm install
COPY ../frontend ./
RUN npm run build

# --- Stage 2: Build Backend ---
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Copy built frontend from Stage 1
COPY --from=frontend-builder /frontend-build/dist ./static

# Expose the port
EXPOSE 8080

ENV ENVIRONMENT="production"

# Run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
