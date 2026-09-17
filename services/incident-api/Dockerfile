FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy dependency configuration
COPY services/incident-api/pyproject.toml /app/services/incident-api/
COPY libs /app/libs

# Install dependencies directly
RUN pip install --no-cache-dir /app/services/incident-api

# Copy application code, migrations, and alembic config
COPY services/incident-api/src /app/services/incident-api/src
COPY services/incident-api/migrations /app/services/incident-api/migrations
COPY services/incident-api/alembic.ini /app/services/incident-api/

# Setup Python Path for shared libraries
ENV PYTHONPATH="/app/services/incident-api/src:/app/libs/auth:/app/libs/database:/app/libs/events:/app/libs/observability"

EXPOSE 8000

CMD ["uvicorn", "incident_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
