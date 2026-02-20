"""Geocoding via Nominatim."""

from typing import Optional, Tuple

from geopy.geocoders import Nominatim


def geocode_location(
    town_name: str,
    province_name: str,
    user_agent: str = "fresquito-geocoder",
) -> Optional[Tuple[float, float]]:
    """Geocode town and province in Spain. Returns (lat, lon) or None."""
    try:
        location_string = f"{town_name}, {province_name}, Spain"
        locator = Nominatim(user_agent=user_agent)
        location = locator.geocode(location_string)
        if location is None:
            return None
        return (location.latitude, location.longitude)
    except Exception:
        return None
