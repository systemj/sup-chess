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

# In a multiprocess configuration Prometheus Gauges have the following mode options:
# multiprocess_mode = all (all dead/alive pids), liveall, livesum, min, max
# Counters, Summaries, and Histograms work normally

# start_time_epoch_seconds = Gauge("start_time_epoch_seconds", "App start epoch timestamp", multiprocess_mode="min")
#hello_total = Counter("hello_total", "Total of all hello values")

# your metrics...


def init(app):
    """ initialize app metrics """
    metrics.init_app(app)
