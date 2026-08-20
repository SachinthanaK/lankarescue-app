from lankarescue_observability import create_service_app

from .providers import MockAlertProvider, ProviderAlert

app = create_service_app(
    service_name="alert-ingestor",
    version="0.1.0",
    environment="local",
    log_level="INFO",
    description="Normalizes external alert providers; Phase 1 uses a mock provider.",
)
provider = MockAlertProvider()


@app.get("/api/v1/demo/alerts", response_model=list[ProviderAlert], tags=["local demo"])
async def demo_alerts() -> list[ProviderAlert]:
    return await provider.fetch()
