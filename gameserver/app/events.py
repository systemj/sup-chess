import logging
import random
import requests
import string
from flask import session
from flask_socketio import emit, join_room, leave_room
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
        # broadcast the move to everyone in the game
        emit("remote_move", data, room=session.get("gameid", None))
        # get a chess engine move for non-human opponents
        if data["opponent"] != "human":
            r = requests.post("http://chess-engine:8000/get_move", json=data)
            logger.info(r.json())
            emit("remote_move", r.json(), room=session.get("gameid", None))

    @socketio.on("join_game")
    def _join_game(data):
        logger.info(f"join_game: {data}")
        session["gameid"] = data["gameid"]
        join_room(data["gameid"])
        emit("joined_game", {"gameid": data["gameid"]})
