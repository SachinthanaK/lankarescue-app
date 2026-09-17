FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy dependency configuration
COPY services/resource-matcher/pyproject.toml /app/services/resource-matcher/
COPY libs /app/libs

# Install dependencies directly
RUN pip install --no-cache-dir /app/services/resource-matcher

# Copy application code
COPY services/resource-matcher/src /app/services/resource-matcher/src

# Setup Python Path for shared libraries
ENV PYTHONPATH="/app/services/resource-matcher/src:/app/libs/auth:/app/libs/database:/app/libs/events:/app/libs/observability"

EXPOSE 8000

CMD ["uvicorn", "resource_matcher.main:app", "--host", "0.0.0.0", "--port", "8000"]
