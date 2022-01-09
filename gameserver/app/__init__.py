""" app initialization """
from flask import Flask
from flask_socketio import SocketIO
from app import conf
from app import log
from app import metrics
from app import routes
from app import events

socketio = SocketIO()


def create_app(config_file="config.yaml"):
    """ Flask app factory function """
    app = Flask(__name__)
    app.config["config_file"] = config_file

    # set context for handling multiple worker processes
    with app.app_context():
        # load config
        conf.init(app)

        # initialize logging
        log.init(app)

        # initialize metrics
        metrics.init(app)

        # load routes
        routes.init(app)

        # initialize socketio
        socketio.init_app(app, async_mode='eventlet',
            cors_allowed_origins="*",
            message_queue=f"redis://{app.config["redis_host"]}:{app.config["redis_port"]}")

        # load events
        events.init(app, socketio)

        return app
