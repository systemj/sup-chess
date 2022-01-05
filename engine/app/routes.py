import logging
from flask import abort, request, Response, jsonify
from app import metrics
from app import engine

logger = logging.getLogger("gunicorn.error")

def init(app):
    # kubernetes pod routes
    @app.route("/healthz")
    def _healthz():
        return jsonify({"healthz": True})

    @app.route("/ready")
    def _ready():
        return jsonify({"ready": True})

    @app.route("/get_move", methods=['POST'])
    def _get_move():
        data = request.get_json()
        result = engine.get_move(**data)
        return jsonify(result), 200

    @app.route("/valid_moves", methods=['POST'])
    def _valid_moves():
        data = request.get_json()
        moves = engine.valid_moves(**data)
        return jsonify({"valid_moves": moves}), 200

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