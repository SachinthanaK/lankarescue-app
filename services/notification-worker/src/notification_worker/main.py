from lankarescue_observability import create_service_app

app = create_service_app(
    service_name="notification-worker",
    version="0.1.0",
    environment="local",
    log_level="INFO",
    description="Consumes notification jobs in later asynchronous phases.",
)
