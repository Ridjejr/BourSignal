import logging
import os
import time

from flask import Response, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
    multiprocess,
)

logger = logging.getLogger(__name__)

http_requests_total = Counter(
    "http_requests_total",
    "Nombre total de requêtes HTTP",
    ["method", "endpoint", "status"]
)

http_request_duration = Histogram(
    "http_request_duration_seconds",
    "Durée des requêtes HTTP en secondes",
    ["method", "endpoint"]
)

active_requests = Gauge(
    "active_requests", "Requêtes en cours de traitement",
    multiprocess_mode="livesum"
)


def init_metrics(app):
    """Instrumente toutes les routes via before/after_request et expose /metrics."""

    @app.before_request
    def _start_timer():
        request._start_time = time.time()
        active_requests.inc()

    @app.after_request
    def _record_metrics(response):
        duration = time.time() - getattr(request, "_start_time", time.time())
        http_requests_total.labels(
            method=request.method, endpoint=request.path, status=str(response.status_code)
        ).inc()
        http_request_duration.labels(
            method=request.method, endpoint=request.path
        ).observe(duration)
        active_requests.dec()

        logger.info(
            f"{request.method} {request.path} {response.status_code} {duration * 1000:.1f}ms",
            extra={
                "method": request.method,
                "endpoint": request.path,
                "status": response.status_code,
                "duration_ms": round(duration * 1000, 1)
            }
        )
        return response

    @app.route("/metrics")
    def metrics():
        if "PROMETHEUS_MULTIPROC_DIR" in os.environ:
            registry = CollectorRegistry()
            multiprocess.MultiProcessCollector(registry)
            return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
