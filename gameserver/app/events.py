import logging
import random
import requests
import string
from flask import session
from flask_socketio import emit, join_room, leave_room
from app import metrics


logger = logging.getLogger("gunicorn.error")

def init(socketio):
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
        emit("joined_game", data, room=session.get("gameid", None))

    # @socketio.on("status_request")
    # def _status_request(data):
    #     logger.info(f"status_request: {data}")
    #     # broadcast the status request to everyone in the game
    #     emit("status_request", data, room=session.get("gameid", None))

    @socketio.on("status")
    def _status(data):
        logger.info(f"status: {data}")
        # broadcast the status to everyone in the game
        emit("status", data, room=session.get("gameid", None))
