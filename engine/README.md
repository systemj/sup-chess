# chess via flask
This is completely stateless; the expected use case is to receive a board state (FEN) and return a move or a list of valid moves.

## testing
### build
```bash
docker build -t chess-engine .
```
### run
```bash
docker run -i -t --rm -v"$(pwd):/app" -p 8000:8000 --entrypoint /bin/bash chess-engine
gunicorn --config gunicorn_config.py --workers 4 --bind 0.0.0.0:8000 wsgi:app
```

### endpoints
```bash
curl -X POST -H "Content-type: application/json" 'http://localhost:8000/get_move' \
  -d '{"board_state": "r1bqkb1r/pppp1ppp/2n2n2/4p3/Q1P5/5P2/PP1PP1PP/RNB1KBNR w KQkq - 2 4", "time_limit": 1}'

curl -X POST -H "Content-type: application/json" 'http://localhost:8000/valid_moves' \
  -d '{"board_state": "r1bqkb1r/pppp1ppp/2n2n2/4p3/Q1P5/5P2/PP1PP1PP/RNB1KBNR w KQkq - 2 4"}'
```

## references
- https://python-chess.readthedocs.io/en/latest/
- https://www.gnu.org/software/chess/manual/gnuchess.html
- https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
