import logging
import random
import requests
import string
from flask import session
from flask_socketio import emit, join_room, leave_room
from app import metrics


logger = logging.getLogger("gunicorn.error")

def init(app, socketio):
    @socketio.on("player_move")
    def _player_move(data):
        logger.info(f"player_move: {data}")
        # broadcast the move to everyone in the game
        emit("player_move", data, room=session.get("gameid", None))
        # get a chess engine move for non-human opponents
        if data["opponent"] != "human":
            r = requests.post(
                f'{app.config["chess_engine_url_scheme"]}://{app.config["chess_engine_url_host"]}:{app.config["chess_engine_url_port"]}/get_move',
                json=data
            )
            logger.info(r.json())
            emit("player_move", r.json(), room=session.get("gameid", None))

    @socketio.on("join_game")
    def _join_game(data):
        logger.info(f"join_game: {data}")
        session["gameid"] = data["gameid"]
        join_room(data["gameid"])
        emit("join_game", data, room=session.get("gameid", None))

    @socketio.on("status")
    def _status(data):
        logger.info(f"status: {data}")
        # broadcast the status to everyone in the game
        emit("status", data, room=session.get("gameid", None))
