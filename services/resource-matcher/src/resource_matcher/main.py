from lankarescue_observability import create_service_app

app = create_service_app(
    service_name="resource-matcher",
    version="0.1.0",
    environment="local",
    log_level="INFO",
    description="Matches verified requests with available resources in later phases.",
)
