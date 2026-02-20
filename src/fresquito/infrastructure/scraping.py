"""Scraping weather data from El Tiempo API."""

import logging
import threading
import time
from typing import List, Optional

import requests

from fresquito.domain.models import WeatherRecord

logger = logging.getLogger(__name__)

ELTIEMPO_API_URL = (
    "https://www.eltiempo.es/api/v1/get_current_conditions_by_pelmorex_id/{pelmorex_id}"
)


def fetch_weather_data(pelmorex_id: str, meteo: List[WeatherRecord]) -> None:
    """Fetch weather for one pelmorex_id and append to meteo list."""
    try:
        url = ELTIEMPO_API_URL.format(pelmorex_id=pelmorex_id)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        record = WeatherRecord(
            pelmorex_id=pelmorex_id,
            temp=float(data["temperature"]["c"]),
            timestamp=data["timestamp"]["local"],
        )
        meteo.append(record)
    except Exception as e:
        logger.debug("Failed to fetch %s: %s", pelmorex_id, e)


def scrape_weather_data(
    pelmorex_list: List[str],
    max_threads: int = 8,
    max_locations: Optional[int] = None,
) -> List[WeatherRecord]:
    """Scrape weather for all pelmorex IDs; optional limit. Returns list of WeatherRecord."""
    ids = pelmorex_list[:max_locations] if max_locations else pelmorex_list
    total = len(ids)
    logger.info("Total locations to scrape: %s", total)
    meteo: List[WeatherRecord] = []
    threads: List[threading.Thread] = []
    for i, pelmorex_id in enumerate(ids):
        logger.info(
            "Scraping data for location %s (%s of %s)",
            pelmorex_id,
            i + 1,
            total,
        )
        thread = threading.Thread(target=fetch_weather_data, args=(pelmorex_id, meteo))
        threads.append(thread)
        if len(threads) >= max_threads:
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            threads = []
            time.sleep(1)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return meteo
