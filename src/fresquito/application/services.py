"""Application services: run pipeline profiles, get data, get map path."""

import logging
from typing import Any, List

from fresquito.application import config
from fresquito.application.run_pipeline import run_pipeline
from fresquito.infrastructure import storage

logger = logging.getLogger(__name__)


def run_pipeline_town_index() -> None:
    """Run pipeline with town_index.csv and NUM_LOCATIONS limit (legacy run_script)."""
    run_pipeline(
        town_index_path=config.TOWN_INDEX_PATH,
        output_csv_path=config.OUTPUT_CSV_PATH,
        map_output_path=config.MAP_PATH,
        datos_tiempo_path=config.DATOS_TIEMPO_PATH,
        nginx_index_path=config.NGINX_INDEX_PATH,
        max_locations=config.NUM_LOCATIONS_SCRIPT1,
        max_threads=config.MAX_THREADS,
        geocoder_user_agent=config.GEOCODER_USER_AGENT,
    )


def run_pipeline_new_town_index() -> None:
    """Run pipeline with new_town_index.csv, no location limit (legacy run_newscript)."""
    run_pipeline(
        town_index_path=config.NEW_TOWN_INDEX_PATH,
        output_csv_path=config.OUTPUT_CSV_PATH,
        map_output_path=config.MAP_PATH,
        datos_tiempo_path=config.DATOS_TIEMPO_PATH,
        nginx_index_path=config.NGINX_INDEX_PATH,
        max_locations=config.NUM_LOCATIONS_SCRIPT2,
        max_threads=config.MAX_THREADS,
        geocoder_user_agent=config.GEOCODER_USER_AGENT,
    )


def get_weather_records() -> List[Any]:
    """Read datos_tiempo CSV and return list of dicts (for API get_all_data)."""
    return storage.read_weather_csv(config.DATOS_TIEMPO_PATH)


def get_map_path() -> str:
    """Return path to map.html for sending file."""
    return config.MAP_PATH
