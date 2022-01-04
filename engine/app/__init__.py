""" app initialization """
from flask import Flask
from app import log
from app import metrics
from app import routes


def create_app(config_file="config.yaml"):
    """ Flask app factory function """
    app = Flask(__name__)

    # set context for handling multiple worker processes
    with app.app_context():
        # initialize logging
        log.init(app)

        # initialize metrics
        metrics.init(app)

        # load routes
        routes.init(app)

        return app
