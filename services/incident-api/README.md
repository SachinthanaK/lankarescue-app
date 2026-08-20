# Incident API

Phase 1 FastAPI service for anonymous relief-request submission and secure tracking.

Run from the repository root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn incident_api.main:app --app-dir services/incident-api/src --reload --port 8000
```

OpenAPI is available at `http://localhost:8000/docs`. The repository is in-memory in Phase 1, so data is lost when the process restarts.

