""" prometheus metrics setup"""
import os
from datetime import datetime
from prometheus_client import Gauge, Counter
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

# try to create the multiproc data directory
try:
    os.makedirs(os.environ.get("prometheus_multiproc_dir", "/var/tmp/prometheus"), 0o0700)
except FileExistsError:
    pass

# initialize metrics via specialize multiprocess/gunicorn class
metrics = GunicornInternalPrometheusMetrics(app=None)

# app specific metrics

# static info metric
metrics.info("chess_engine_info", "Chess engine info", version="0.0.1")


def init(app):
    """ initialize app metrics """
    metrics.init_app(app)
