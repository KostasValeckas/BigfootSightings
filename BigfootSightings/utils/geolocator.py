"""
Module used for creating location descriptors from coordinates
"""

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


# initialize Nominatim API
geolocator = Nominatim(user_agent="BigfootSightings")


def get_location_descriptor(lat, long):
    """
    Returns a location descriptor for a given latitude and longitude
    """

    # not allowing any look-up to outlast 5 seconds
    try:
        location = geolocator.reverse(
            "{}, {}".format(lat, long), exactly_one=True, timeout=5
        )
    except GeocoderTimedOut as e:
        return None, None, None

    if location is None:
        return None, None, None

    address = location.raw["address"]
    country = address.get("country", "")

    state = address.get('state', None)

    city = address["city"] if "city" in address else None

    return country, state, city
