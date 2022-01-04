""" gunicorn/flask wsgi entrypoint """
import os
from app import create_app, socketio

app = create_app()


if __name__ == "__main__":
    # start the app in the foreground for debugging if executed directly
    socketio.run(host="0.0.0.0", port=os.environ.get("gunicorn_port", "8000"))
