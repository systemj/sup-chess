import logging
from flask_socketio import send, emit
from app import metrics


logger = logging.getLogger("gunicorn.error")

def init(socketio):
    @socketio.on("test event")
    def _test_event_handler(data):
        logger.info(f"got event: {data}")
        emit("stuff", {"x": "y"})
