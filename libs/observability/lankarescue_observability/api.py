import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .logging import configure_logging


class HealthResponse(BaseModel):
    status: str
    service: str


class MetadataResponse(BaseModel):
    service: str
    version: str
    environment: str


def create_service_app(
    *,
    service_name: str,
    version: str,
    environment: str,
    log_level: str,
    allowed_origins: list[str] | None = None,
    description: str = "",
) -> FastAPI:
    configure_logging(log_level)
    logger = logging.getLogger(service_name)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        logger.info("service_started", extra={"service": service_name})
        yield
        logger.info("service_stopped", extra={"service": service_name})

    app = FastAPI(
        title=service_name,
        version=version,
        description=description,
        lifespan=lifespan,
    )
    app.state.service_name = service_name
    app.state.environment = environment

    if allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=False,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["Content-Type", "X-Correlation-ID"],
        )

    @app.middleware("http")
    async def correlation_middleware(request: Request, call_next: Any) -> Any:
        correlation_id = request.headers.get("x-correlation-id") or str(uuid4())
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        logger.info(
            "request_completed",
            extra={
                "service": service_name,
                "correlation_id": correlation_id,
                "path": request.url.path,
                "method": request.method,
                "status_code": response.status_code,
            },
        )
        return response

    @app.exception_handler(Exception)
    async def unhandled_error(request: Request, error: Exception) -> JSONResponse:
        correlation_id = getattr(request.state, "correlation_id", str(uuid4()))
        logger.exception(
            "unhandled_error",
            extra={"service": service_name, "correlation_id": correlation_id},
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred."},
                "correlationId": correlation_id,
            },
        )

    @app.get("/health/live", response_model=HealthResponse, tags=["health"])
    async def live() -> HealthResponse:
        return HealthResponse(status="ok", service=service_name)

    @app.get("/health/ready", response_model=HealthResponse, tags=["health"])
    async def ready() -> HealthResponse:
        return HealthResponse(status="ready", service=service_name)

    @app.get("/meta", response_model=MetadataResponse, tags=["metadata"])
    async def metadata() -> MetadataResponse:
        return MetadataResponse(service=service_name, version=version, environment=environment)

    return app
