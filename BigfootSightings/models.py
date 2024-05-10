from typing import Dict

from flask_login import UserMixin
from psycopg2 import sql

from BigfootSightings import login_manager, db_cursor, conn, app


@login_manager.user_loader
def load_user(username):
    user_sql = sql.SQL("""
    SELECT * FROM Users
    WHERE username = %s
    """).format(sql.Identifier('username'))

    db_cursor.execute(user_sql, username)
    return User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None


class User():
    def __init__(self, user_data: Dict):
        self.username = user_data.get('username')
        self.password = user_data.get('password')
        self.is_active = False



class Sighting():
    def __init__(self, sighting_data: Dict):
        self.title = sighting_data.get('title')
        self.latitude = sighting_data.get('latitude')
        self.longitude = sighting_data.get('longitude')


