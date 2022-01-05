#!/usr/bin/env python3
import asyncio
import chess
import chess.engine
import logging

logger = logging.getLogger("gunicorn.error")

engines = {
    "gnuchess": {
        "command": ["/usr/games/gnuchess", "--uci"]
    }
}

def get_move(board_state: str = "", time_limit: int = 1, engine: str = "gnuchess") -> str:
    logger.info(f"board: {board_state}")
    engine = chess.engine.SimpleEngine.popen_uci(engines[engine]["command"])
    board = chess.Board(board_state)
    result = engine.play(board, chess.engine.Limit(time=time_limit))
    move = result.move
    board.push(move)
    logger.info(f"move: {move.uci()}")
    engine.quit()
    return { "board": board.fen(), "from": chess.square_name(move.from_square), "to": chess.square_name(move.to_square), "uci": move.uci() }

def valid_moves(board_state: str = "", engine: str = "gnuchess"):
    logger.info(f"board: {board_state}")
    engine = chess.engine.SimpleEngine.popen_uci(engines[engine]["command"])
    board = chess.Board(board_state)
    legal_moves = []
    for move in board.legal_moves:
        legal_moves.append(move.uci())
    logger.info(f"legal_moves: {legal_moves}")
    engine.quit()
    return legal_moves
