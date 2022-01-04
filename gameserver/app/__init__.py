""" app initialization """
from flask import Flask
from flask_socketio import SocketIO
from app import log
from app import metrics
from app import routes
from app import events

socketio = SocketIO()

def create_app(config_file="config.yaml"):
    """ Flask app factory function """
    app = Flask(__name__)
    app.debug = True
    # set context for handling multiple worker processes
    with app.app_context():
        # initialize socketio
        socketio.init_app(app)

        # initialize logging
        log.init(app)

        # initialize metrics
        metrics.init(app)

        # load routes
        routes.init(app)

        # load events
        events.init(socketio)

        return app
