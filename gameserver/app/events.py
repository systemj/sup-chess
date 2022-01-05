import logging
import requests
from flask_socketio import send, emit
from app import metrics


logger = logging.getLogger("gunicorn.error")

def init(socketio):
    @socketio.on("test event")
    def _test_event_handler(data):
        logger.info(f"got event: {data}")
        emit("stuff", {"x": "y"})
    
    @socketio.on("player_move")
    def _player_move(data):
        logger.info(f"player_move: {data}")
        r = requests.post("http://chess-engine:8000/get_move", json=data)
        emit("remote_move", r.json())
        logger.info(r.json())
