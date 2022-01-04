""" gunicorn configuration """

# helper class for prometheus_flask_exporter multiprocess mode
from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics


def child_exit(_server, worker):
    """ handle cleanup of dead worker metrics """
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)
