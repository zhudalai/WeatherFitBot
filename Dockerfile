# ===== Stage 1: Build frontend =====
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./

RUN npm install

COPY frontend/ ./
RUN npm run build

# ===== Stage 2: Backend + serve frontend =====
FROM python:3.11-slim

WORKDIR /app

# Copy backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

# Copy frontend build artifacts
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist/

WORKDIR /app/backend

ENV APP_ENV=production
ENV APP_PORT=7860
ENV CORS_ORIGINS=*

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
