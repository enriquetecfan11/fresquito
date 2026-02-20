"""CSV and map file storage."""

import csv
import datetime
import logging
import os
from typing import Any, List, Optional

import folium
import pandas as pd

from fresquito.domain.models import ExtremeTown

logger = logging.getLogger(__name__)

EXTREME_CSV_HEADER = [
    "TIPO",
    "CIUDAD",
    "PROVINCIA",
    "GRADOS",
    "FECHA",
    "HORA UTC",
    "HORA MADRID (UTC+2)",
]


def load_town_index(path: str) -> pd.DataFrame:
    """Load town index CSV (columns: pelmorex_id, name, province, etc.)."""
    return pd.read_csv(path)


def read_weather_csv(path: str, encoding: str = "iso-8859-1") -> List[Any]:
    """Read datos_tiempo-style CSV and return list of dicts (rows)."""
    rows: List[Any] = []
    with open(path, "r", encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            rows.append(row)
    return rows


def append_extreme_record(extreme: ExtremeTown, filename: str) -> None:
    """Append one extreme (hottest/coldest) row to the CSV. Single file only."""
    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y")
    time_utc = now.strftime("%H:%M:%S")
    time_madrid = (now + datetime.timedelta(hours=2)).strftime("%H:%M:%S")
    formatted = {
        "TIPO": extreme.town_type,
        "CIUDAD": extreme.name,
        "PROVINCIA": extreme.province,
        "GRADOS": extreme.temperature,
        "FECHA": date,
        "HORA UTC": time_utc,
        "HORA MADRID (UTC+2)": time_madrid,
    }
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=EXTREME_CSV_HEADER)
        if not file_exists:
            writer.writeheader()
        writer.writerow(formatted)


def write_output_csv(output_df: pd.DataFrame, path: str) -> None:
    """Write merged output (towns + weather) to CSV."""
    output_df.to_csv(path, index=False)


def build_and_save_map(
    coldest: ExtremeTown,
    hottest: ExtremeTown,
    cold_coords: tuple[float, float],
    hot_coords: tuple[float, float],
    map_output_path: str,
    nginx_index_path: Optional[str] = None,
) -> None:
    """Build Folium map with coldest/hottest markers and save to file(s)."""
    temp_map = folium.Map()
    folium.Marker(
        location=cold_coords,
        popup=f"{coldest.name}, {coldest.province}\n{coldest.temperature}ºC",
        icon=folium.Icon(color="blue", icon="glyphicon glyphicon-cloud"),
    ).add_to(temp_map)
    folium.Marker(
        location=hot_coords,
        popup=f"{hottest.name}, {hottest.province}\n{hottest.temperature}ºC",
        icon=folium.Icon(color="red", icon="glyphicon glyphicon-fire"),
    ).add_to(temp_map)
    temp_map.fit_bounds([cold_coords, hot_coords])
    temp_map.save(outfile=map_output_path)
    if nginx_index_path:
        temp_map.save(outfile=nginx_index_path)
    logger.info("Map saved to %s", map_output_path)
