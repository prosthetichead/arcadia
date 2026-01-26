import sqlite3
import os

class DataManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def _fetch_all(self, query, params=()):
        """Helper to execute a query and return all rows as dictionaries."""
        if not os.path.exists(self.db_path):
            return []
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row  # Allows accessing columns by name
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def load_settings(self):
        settings = {}
        rows = self._fetch_all("SELECT name, value, type FROM settings")
        
        for row in rows:
            name = row['name']
            val = row['value']
            type_ = row['type']
            
            if type_ == "int":
                settings[name] = int(val)
            elif type_ == "bool":
                settings[name] = (str(val).lower() == "true")
            else:
                settings[name] = val
                
        return settings

    def load_games(self):
        # Returns a list of sqlite3.Row objects, which behave like dicts/tuples
        games = self._fetch_all("SELECT title FROM games")
        
        if not games:
            # Fallback data for testing
            games = [("Arcade Game 1",), ("Arcade Game 2",), ("Arcade Game 3",)]
            
        return games