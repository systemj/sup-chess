# a web chess thing
Play chess against chess engines or human opponents via web browser.

## local testing
```bash
docker-compose up
```
- http://localhost:8000

## Deploy to Kubernets via Helm
```bash
cd deploy/helm
helm upgrade --install --create-namespace --namespace sup-chess sup-chess .
```

## documentation
Refer to the README.md in each component directory for additional details.
