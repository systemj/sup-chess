import logging
from flask import request, jsonify

def init(app):
    """ initialize logging """
    if __name__ == "__main__":
        logger = logging.getLogger("chess-engine " + __name__)
        formatter = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        app.logger.handlers = logging.handlers
        app.logger.setLevel(logging.info)
        app.logger.setFormatter(formatter)
    else:
        logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = logging.handlers
        app.logger.setLevel(logger.level)

    @app.after_request
    def _after_request(response):
        """ flask logging - request log """
        # skip unhelpful endpoints
        if request.full_path not in ["/?", "/healthz?", "/ready?"]:
            logger.info('%s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path, response.status)
        return response
