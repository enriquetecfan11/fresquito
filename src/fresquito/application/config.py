"""Configuration: paths and pipeline tuning."""

import os
from pathlib import Path
from typing import Optional

# Base directory: current working directory when app runs (e.g. /app in Docker)
BASE_DIR = Path(os.environ.get("FRESQUITO_BASE_DIR", ".")).resolve()

# All CSV/XLSX and generated artifacts live under data/ (single place to store and backup)
DATA_DIR = BASE_DIR / os.environ.get("FRESQUITO_DATA_DIR", "data")

# Town index paths
TOWN_INDEX_PATH = os.environ.get("TOWN_INDEX_PATH", str(DATA_DIR / "town_index.csv"))
NEW_TOWN_INDEX_PATH = os.environ.get(
    "NEW_TOWN_INDEX_PATH", str(DATA_DIR / "new_town_index.csv")
)

# Output paths (generated CSVs, map, nginx index)
DATOS_TIEMPO_PATH = os.environ.get(
    "DATOS_TIEMPO_PATH", str(DATA_DIR / "datos_tiempo.csv")
)
MAP_PATH = os.environ.get("MAP_PATH", str(DATA_DIR / "map.html"))
OUTPUT_CSV_PATH = os.environ.get("OUTPUT_CSV_PATH", str(DATA_DIR / "output.csv"))
NGINX_INDEX_PATH = os.environ.get(
    "NGINX_INDEX_PATH", str(DATA_DIR / "index.nginx-debian.html")
)
WEATHER_DATA_PATH = os.environ.get(
    "WEATHER_DATA_PATH", str(DATA_DIR / "weather_data.csv")
)

# Pipeline tuning
MAX_THREADS = int(os.environ.get("MAX_THREADS", "8"))
NUM_LOCATIONS_SCRIPT1 = int(os.environ.get("NUM_LOCATIONS", "2000"))
NUM_LOCATIONS_SCRIPT2: Optional[int] = None  # no limit for "new script"

# Geocoder
GEOCODER_USER_AGENT = os.environ.get("GEOCODER_USER_AGENT", "fresquito-geocoder")

# Static files (interfaz)
INTERFAZ_DIR = BASE_DIR / "interfaz"
