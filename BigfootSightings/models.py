from typing import Dict

from flask_login import UserMixin
from psycopg2 import sql
import sys
import os

# Add the parent directory to the system path (needed for some imports)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from BigfootSightings import login_manager, db_cursor


@login_manager.user_loader
def load_user(username):
    sql = """
    SELECT * FROM Users
    WHERE username = %s
    """
    db_cursor.execute(sql, (username,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return user


class User(UserMixin):
    def __init__(self, user_data: Dict):
        self.username = user_data.get("username")
        self.password = user_data.get("password")
        self.is_active = user_data.get("is_active", True)

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.is_active

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False


class Location:
    def __init__(self, location_data: Dict):
        self.id = location_data.get("id")
        self.country = location_data.get("country")
        self.state = location_data.get("state")
        self.state_name = location_data.get("state_name")
        self.city = location_data.get("city")


class Sighting:
    def __init__(self, sighting_data: Dict):
        self.nr = sighting_data.get("nr")
        self.username = sighting_data.get("username")
        self.title = sighting_data.get("title")
        self.report_time = sighting_data.get("report_time")
        self.latitude = sighting_data.get("latitude")
        self.longitude = sighting_data.get("longitude")
        # local import to avoid circular imports
        from BigfootSightings.queries import get_location_by_id

        self.location = Location(get_location_by_id(sighting_data.get("location_id")))
