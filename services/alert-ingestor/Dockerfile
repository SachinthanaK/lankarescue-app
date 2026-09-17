FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy dependency configuration
COPY services/alert-ingestor/pyproject.toml /app/services/alert-ingestor/
COPY libs /app/libs

# Install dependencies directly
RUN pip install --no-cache-dir /app/services/alert-ingestor

# Copy application code
COPY services/alert-ingestor/src /app/services/alert-ingestor/src

# Setup Python Path for shared libraries
ENV PYTHONPATH="/app/services/alert-ingestor/src:/app/libs/auth:/app/libs/database:/app/libs/events:/app/libs/observability"

EXPOSE 8000

CMD ["uvicorn", "alert_ingestor.main:app", "--host", "0.0.0.0", "--port", "8000"]
