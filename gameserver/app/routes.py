import logging
from flask import abort, request, Response, jsonify
from app import metrics


logger = logging.getLogger("gunicorn.error")

def init(app):
    # kubernetes pod routes
    @app.route("/healthz")
    def _healthz():
        return jsonify({"healthz": True})

    @app.route("/ready")
    def _ready():
        return jsonify({"ready": True})

    # catch-all route for bad requests
    @app.route('/<path:path>')
    @metrics.metrics.do_not_track()
    def _catchall(path):
        abort(404)

    # error handlers
    @app.errorhandler(404)
    def _page_not_found(exception):
        """ flask logging - handle 404s with helpful message """
        return jsonify({"error": exception.description}), 404

    @app.errorhandler(Exception)
    def _exception(exception):
        """ flask logging - handle 500s """
        return jsonify({"error": exception.description}), 500