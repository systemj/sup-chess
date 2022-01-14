#!/usr/bin/env python3
import asyncio
import chess
import chess.engine
import logging

logger = logging.getLogger("gunicorn.error")

opponents = {
    "gnuchess": {
        "command": ["/usr/games/gnuchess", "--uci"]
    },
    "stockfish": {
        "command": ["/usr/games/stockfish"]
    }
}

def get_move(board_state: str = "", time_limit: int = 1, opponent: str = "gnuchess", **kwargs) -> str:
    logger.info(f"board_state: {board_state}")
    engine = chess.engine.SimpleEngine.popen_uci(opponents[opponent]["command"])
    board = chess.Board(board_state)
    result = engine.play(board, chess.engine.Limit(time=time_limit))
    move = result.move
    board.push(move)
    logger.info(f"move: {move.uci()}")
    engine.quit()
    return { "board_state": board.fen(), "from": chess.square_name(move.from_square), "to": chess.square_name(move.to_square), "uci": move.uci() }

def valid_moves(board_state: str = "", opponent: str = "gnuchess", **kwargs):
    logger.info(f"board_state: {board_state}")
    engine = chess.engine.SimpleEngine.popen_uci(opponents[opponent]["command"])
    board = chess.Board(board_state)
    legal_moves = []
    for move in board.legal_moves:
        legal_moves.append(move.uci())
    logger.info(f"legal_moves: {legal_moves}")
    engine.quit()
    return legal_moves
