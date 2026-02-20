"""Domain models for weather and extreme towns."""

from dataclasses import dataclass


@dataclass
class WeatherRecord:
    """Single weather reading from El Tiempo API."""

    pelmorex_id: str
    temp: float
    timestamp: str


@dataclass
class ExtremeTown:
    """Coldest or hottest town for the extreme CSV/map."""

    town_type: str  # "Hottest" | "Coldest"
    name: str
    province: str
    temperature: float
