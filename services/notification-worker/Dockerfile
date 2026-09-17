FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy dependency configuration
COPY services/notification-worker/pyproject.toml /app/services/notification-worker/
COPY libs /app/libs

# Install dependencies directly
RUN pip install --no-cache-dir /app/services/notification-worker

# Copy application code
COPY services/notification-worker/src /app/services/notification-worker/src

# Setup Python Path for shared libraries
ENV PYTHONPATH="/app/services/notification-worker/src:/app/libs/auth:/app/libs/database:/app/libs/events:/app/libs/observability"

EXPOSE 8000

CMD ["uvicorn", "notification_worker.main:app", "--host", "0.0.0.0", "--port", "8000"]
