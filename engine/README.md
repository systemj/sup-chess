# chess via flask
This is completely stateless; the expected use case is to receive a board state (FEN) and return a move or a list of valid moves.

# chess gameserver

## build
```bash
docker build -t chess-engine .
```
## run
```bash
docker run -i -t --rm -v"$(pwd):/app" -p 8000:8000 chess-engine
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

### chess engine
- /get_move
  - description: get a move from a chess engine
  - methods: POST
  - data (sample):
    ```yaml
    {
      # the board state in FEN format
      "board_state": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
      # (optional) opponent chess engine identifier (gnuchess/stockchess/etc)
      "opponent": "gnuchess",
      # (optional) a time limit for non-human opponents to respond
      "time_limit": 1
    }
    ```
  - response:
    ```yaml
    {
      # the new board state in FEN format
      'board_state': 'rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2',
      # the source and destination chess squares
      'from': 'd7',
      'to': 'd5',
      # the move in uci notation
      'uci': 'd7d5'
    }

- /valid_moves
  - description: get a list of valid moves from the current board state
  - methods: POST
  - data (sample):
    ```yaml
    {
      # the board state in FEN format
      "board_state": "r1bqkb1r/pppp1ppp/2n2n2/4p3/Q1P5/5P2/PP1PP1PP/RNB1KBNR w KQkq - 2 4"
    }
    ```
  - response:
    ```yaml
    {
      # a list of valid possible moves in uci notation
      "valid_moves": [
        "a4a7",
        "a4c6",
        "a4a6",
        # ...
        "b2b4"
      ]
    }
    ```

### endpoint tests
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
- https://en.wikipedia.org/wiki/Algebraic_notation_(chess)
- https://en.wikipedia.org/wiki/Universal_Chess_Interface
