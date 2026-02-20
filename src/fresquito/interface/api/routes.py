"""Flask API routes. Contract: same URLs and JSON responses as legacy app."""

import logging
from typing import TYPE_CHECKING

from flask import jsonify, send_file, send_from_directory

from fresquito.application import config, services

if TYPE_CHECKING:
    from flask import Flask

logger = logging.getLogger(__name__)


def register_routes(app: "Flask") -> None:
    """Register all API and static routes on the Flask app."""

    @app.route("/", methods=["GET"])
    def index():
        return jsonify({"message": "Welcome to the Weather API"}), 200

    @app.route("/run_script", methods=["GET"])
    def run_script():
        logger.info("Running pipeline (town_index, limited locations)")
        try:
            services.run_pipeline_town_index()
            return jsonify({"message": "Script ejecutado correctamente."}), 200
        except Exception as e:
            logger.exception("Pipeline failed")
            return jsonify({"error": str(e)}), 500

    @app.route("/run_newscript", methods=["GET"])
    def run_newscript():
        logger.info("Running pipeline (new_town_index, all locations)")
        try:
            services.run_pipeline_new_town_index()
            return jsonify({"message": "Script ejecutado correctamente."}), 200
        except Exception as e:
            logger.exception("Pipeline failed")
            return jsonify({"error": str(e)}), 500

    @app.route("/get_all_data", methods=["GET"])
    def get_all_data():
        try:
            data_list = services.get_weather_records()
            return jsonify(data_list), 200
        except Exception as e:
            logger.exception("get_all_data failed")
            return jsonify({"error": str(e)}), 500

    @app.route("/get_map", methods=["GET"])
    def get_map():
        try:
            return send_file(
                services.get_map_path(),
                mimetype="text/html",
            )
        except Exception as e:
            logger.exception("get_map failed")
            return jsonify({"error": str(e)}), 500

    @app.route("/<path:filename>", methods=["GET"])
    def serve_static(filename):
        return send_from_directory(str(config.INTERFAZ_DIR), filename)
