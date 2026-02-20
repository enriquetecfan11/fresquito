"""Flask app factory and CORS. Entry point for running the server."""

import logging

from flask import Flask
from flask_cors import CORS

from fresquito.interface.api.routes import register_routes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
register_routes(app)


def main() -> None:
    """Run the Flask app (host 0.0.0.0, port 5000)."""
    app.run(host="0.0.0.0", port=5000)
