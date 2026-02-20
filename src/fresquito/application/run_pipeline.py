"""Pipeline orchestration: load index, scrape, merge, extremes, save CSV and map."""

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

from fresquito.domain.models import ExtremeTown
from fresquito.infrastructure import geocoding, scraping, storage

logger = logging.getLogger(__name__)


def _ensure_output_dirs(*paths: str) -> None:
    """Create parent directories for output paths so data/ exists when writing."""
    for p in paths:
        if p:
            Path(p).parent.mkdir(parents=True, exist_ok=True)


def run_pipeline(
    town_index_path: str,
    output_csv_path: str,
    map_output_path: str,
    datos_tiempo_path: str,
    nginx_index_path: Optional[str] = None,
    max_locations: Optional[int] = None,
    max_threads: int = 8,
    geocoder_user_agent: str = "fresquito-geocoder",
) -> None:
    """Run full pipeline: load towns, scrape weather, merge, find extremes, save CSV and map."""
    logger.info("Pipeline started: town_index=%s", town_index_path)
    _ensure_output_dirs(output_csv_path, map_output_path, datos_tiempo_path)
    if nginx_index_path:
        _ensure_output_dirs(nginx_index_path)
    start_time = pd.Timestamp.now()

    town_index = storage.load_town_index(town_index_path)
    pelmorex_list = town_index["pelmorex_id"].tolist()

    meteo_data = scraping.scrape_weather_data(
        pelmorex_list, max_threads=max_threads, max_locations=max_locations
    )
    meteo_df = pd.DataFrame(
        [(r.pelmorex_id, r.temp, r.timestamp) for r in meteo_data],
        columns=["pelmorex_id", "temp", "timestamp"],
    )

    output = pd.merge(town_index, meteo_df, on="pelmorex_id", how="left")
    storage.write_output_csv(output, output_csv_path)

    coldest_row = output[output["temp"] == output["temp"].min()].sample()
    hottest_row = output[output["temp"] == output["temp"].max()].sample()

    coldest = ExtremeTown(
        town_type="Coldest",
        name=str(coldest_row["name"].iloc[0]),
        province=str(coldest_row["province"].iloc[0]),
        temperature=float(coldest_row["temp"].iloc[0]),
    )
    hottest = ExtremeTown(
        town_type="Hottest",
        name=str(hottest_row["name"].iloc[0]),
        province=str(hottest_row["province"].iloc[0]),
        temperature=float(hottest_row["temp"].iloc[0]),
    )

    logger.info(
        "Coldest: %s, %s, %sºC",
        coldest.name,
        coldest.province,
        coldest.temperature,
    )
    logger.info(
        "Hottest: %s, %s, %sºC",
        hottest.name,
        hottest.province,
        hottest.temperature,
    )

    storage.append_extreme_record(hottest, datos_tiempo_path)
    storage.append_extreme_record(coldest, datos_tiempo_path)

    c_coords = geocoding.geocode_location(
        coldest.name, coldest.province, user_agent=geocoder_user_agent
    )
    h_coords = geocoding.geocode_location(
        hottest.name, hottest.province, user_agent=geocoder_user_agent
    )

    if c_coords and h_coords:
        storage.build_and_save_map(
            coldest, hottest, c_coords, h_coords, map_output_path, nginx_index_path
        )
        logger.info("Map generated successfully")
    else:
        logger.warning("Geocoding failed for coldest or hottest town.")

    elapsed = pd.Timestamp.now() - start_time
    logger.info("Pipeline finished in %s", elapsed)
