# chess gameserver
Communicates moves and game state to players and observers; joins clients to games (rooms).  Coordination between server instances is handled by socketio via Redis pub/sub.

## build
```bash
docker build -t chess-server .
```

## run
```bash
docker run -i -t --rm -v"$(pwd):/app" -p 8000:8000 chess-server
```

## http endpoints
### kubernetes probes
- /healthz
  - description: Kubernetes liveness probe
  - methods: GET
  - response:
    ```json
    {"healthz": true}
    ```

- /ready
  - description: Kubernetes readiness probe
  - methods: GET
  - response:
    ```json
    {"ready": true}
    ```

## socket.io events handled/emitted
- player_move
  - description: player chess move
  - data (sample):
    ```yaml
    {
      # the board state in FEN format
      "board_state": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
      # opponent identifier (human/gnuchess/etc)
      "opponent": "gnuchess",
      # the source and destination chess squares
      "from": "e2",
      "to": "e4"
      # (optional) a time limit for non-human opponents to respond
      "time_limit": 1,
    }
    ```
  - response: emits `player_move` event to room

- join_game
  - description: notification of player or observer joining the game
  - data (sample):
    ```yaml
    {
      # a random identifier assigned to the game
      "gameid": "abcde"
    }
    ```
  - response: emits `join_game` event to room

- status
  - description: notification of current board status
  - data (sample):
    ```yaml
    {
      # the board state in FEN format
      # https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
      "board_state": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
    }
    ```
  - response: emits `status` event to room

## references
- https://flask-socketio.readthedocs.io/en/latest/
- https://codeburst.io/building-your-first-chat-application-using-flask-in-7-minutes-f98de4adfa5d
- https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
- https://en.wikipedia.org/wiki/Algebraic_notation_(chess)
