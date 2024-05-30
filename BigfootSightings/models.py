from typing import Dict

from flask_login import UserMixin
from psycopg2 import sql

from BigfootSightings import login_manager, db_cursor, conn, app


@login_manager.user_loader
def load_user(username):
    sql = """
    SELECT * FROM Users
    WHERE username = %s
    """
    db_cursor.execute(sql, (username,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    print("fetched used: ", user)
    return user


class User(UserMixin):
    def __init__(self, user_data: Dict):
        self.username = user_data.get('username')
        self.password = user_data.get('password')
        self.is_active = user_data.get('is_active', True)

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.is_active

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False



class Sighting():
    def __init__(self, sighting_data: Dict):
        self.nr = sighting_data.get('nr')
        self.username = sighting_data.get('username')
        self.title = sighting_data.get('title')
        self.timestamp = sighting_data.get('timestamp')


