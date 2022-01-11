# a web chess thing

## local testing
```
docker-compose up
```
- http://localhost:8000

## helm install
```
cd deploy/helm
helm upgrade --install --create-namespace --namespace sup-chess sup-chess .
```

## references
### frontend
- https://websockets.readthedocs.io/en/stable/
- https://javascript.info/websocket
- https://chessboardjs.com/index.html
- https://github.com/jhlywa/chess.js
