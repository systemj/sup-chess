# chess gameserver

## testing
### build
```bash
docker build -t chess-server .
```
### run
```bash
docker run -i -t --rm -v"$(pwd):/app" -p 8000:8000 --entrypoint /bin/bash chess-server
gunicorn --config gunicorn_config.py --worker-class eventlet --workers 1 --bind 0.0.0.0:8000 wsgi:app
```

### endpoints
```bash
curl -X POST -H "Content-type: application/json" 'http://localhost:8000/get_move' \
  -d '{"board_state": "r1bqkb1r/pppp1ppp/2n2n2/4p3/Q1P5/5P2/PP1PP1PP/RNB1KBNR w KQkq - 2 4", "time_limit": 1}'
```

## references
- https://flask-socketio.readthedocs.io/en/latest/
- https://codeburst.io/building-your-first-chat-application-using-flask-in-7-minutes-f98de4adfa5d
