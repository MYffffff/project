FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Default environment (can be overridden by env_file)
ENV POSTGRES_HOST=db \
    POSTGRES_PORT=5432 \
    POSTGRES_DB=moviesdb \
    POSTGRES_USER=appuser \
    POSTGRES_PASSWORD=appsecret \
    APP_PORT=8000 \
    APP_HOST=0.0.0.0

EXPOSE 8000

# Simple entrypoint to run migrations then start app
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
