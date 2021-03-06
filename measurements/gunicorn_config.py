from .config import PROMETHEUS_PORT

# This config is taken from:
# https://github.com/rycus86/prometheus_flask_exporter#multiprocess-applications
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics


def when_ready(server):
    GunicornPrometheusMetrics.start_http_server_when_ready(PROMETHEUS_PORT)


def child_exit(server, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)
