# a web chess thing

## testing
### startup
```bash
docker run -i -t --rm -v"$(pwd):/app" --entrypoint /bin/bash chess
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
### frontend
- https://websockets.readthedocs.io/en/stable/
- https://javascript.info/websocket
- https://chessboardjs.com/index.html
- https://github.com/jhlywa/chess.js
### backend
- https://python-chess.readthedocs.io/en/latest/
- https://www.gnu.org/software/chess/manual/gnuchess.html
