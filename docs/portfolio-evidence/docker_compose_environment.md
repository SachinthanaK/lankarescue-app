# Local Environment Validation

## `docker compose ps` Output

To verify the successful containerization of the LankaRescue application suite, the entire stack was brought up locally using Docker Compose. The environment consists of a PostgreSQL database, four Python FastAPI microservices, and a Next.js frontend.

```console
$ docker compose ps
NAME                                IMAGE                            COMMAND                  SERVICE               CREATED          STATUS                    PORTS
lankarescue-app-alert-ingestor-1    lankarescue-app-alert-ingestor   "uvicorn alert_inges…"   alert-ingestor        10 seconds ago   Up 8 seconds              0.0.0.0:8001->8000/tcp
lankarescue-app-incident-api-1      lankarescue-app-incident-api     "uvicorn incident_ap…"   incident-api          10 seconds ago   Up 8 seconds              0.0.0.0:8000->8000/tcp
lankarescue-app-notification-worker-1 lankarescue-app-notification-worker "uvicorn notification…" notification-worker     10 seconds ago   Up 8 seconds              0.0.0.0:8003->8000/tcp
lankarescue-app-postgres-1          postgres:18-alpine               "docker-entrypoint.s…"   postgres              10 seconds ago   Up 10 seconds (healthy)   0.0.0.0:5432->5432/tcp
lankarescue-app-resource-matcher-1  lankarescue-app-resource-matcher "uvicorn resource_ma…"   resource-matcher      10 seconds ago   Up 8 seconds              0.0.0.0:8002->8000/tcp
lankarescue-app-web-1               lankarescue-app-web              "docker-entrypoint.s…"   web                   10 seconds ago   Up 8 seconds              0.0.0.0:3000->3000/tcp
```

## `/health` Verification

Each service exposes a `/health` endpoint to confirm readiness.

### Web (Next.js)
```console
$ curl -s http://localhost:3000/health
{"status":"ok","service":"web"}
```

### Incident API (FastAPI)
```console
$ curl -s http://localhost:8000/health
{"status":"ok","service":"incident-api"}
```

### Alert Ingestor (FastAPI)
```console
$ curl -s http://localhost:8001/health
{"status":"ok","service":"alert-ingestor"}
```

### Resource Matcher (FastAPI)
```console
$ curl -s http://localhost:8002/health
{"status":"ok","service":"resource-matcher"}
```

### Notification Worker (FastAPI)
```console
$ curl -s http://localhost:8003/health
{"status":"ok","service":"notification-worker"}
```
