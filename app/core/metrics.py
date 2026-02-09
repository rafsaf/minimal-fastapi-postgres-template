import prometheus_client

NAMESPACE = "org"
SUBSYSTEM = "app"

APP_STARTED = prometheus_client.Counter(
    "app_started_total",
    "FastAPI application start count",
    labelnames=(),
    namespace=NAMESPACE,
    subsystem=SUBSYSTEM,
)

APP_STOPPED = prometheus_client.Counter(
    "app_stopped",
    "FastAPI application stop count",
    labelnames=(),
    namespace=NAMESPACE,
    subsystem=SUBSYSTEM,
)
