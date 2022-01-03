#!/usr/bin/env python3
import asyncio
import chess
import websockets


import chess.engine

engine = chess.engine.SimpleEngine.popen_uci(["/usr/games/gnuchess", "--uci"])

board = chess.Board("r1bqkb1r/pppp1ppp/2n2n2/4p3/Q1P5/5P2/PP1PP1PP/RNB1KBNR w KQkq - 2 4")
while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=1))
    print(result.move.uci())
    board.push(result.move)
    print(board)

engine.quit()