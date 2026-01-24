"""

This script is used for creating a dev db while we are still workign on the data structure.
Once this is more fixed will move to migrations and db will be created by admin service not the frontend.

"""

import sqlite3
import os


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
DB_NAME = os.path.join(ROOT_DIR, "data", "arcade.db")


def init_db():
  
    # Delete old DB if it exists (for testing fresh starts)
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Deleted old database... \n   {DB_NAME}")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create Tables
    cursor.execute("""
        CREATE TABLE systems (
            id INTEGER PRIMARY KEY,
            name TEXT,
            emulator_cmd TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE games (
            id INTEGER PRIMARY KEY,
            system_id INTEGER,
            title TEXT,
            filename TEXT,
            year INTEGER,
            play_count INTEGER DEFAULT 0,
            FOREIGN KEY(system_id) REFERENCES systems(id)
        )
    """)

    # Seed Dummy Data
    print("Seeding data...")
    
    # Add Systems
    cursor.execute("INSERT INTO systems (name, emulator_cmd) VALUES (?, ?)", 
                   ("SNES", "snes9x.exe"))
    snes_id = cursor.lastrowid
    
    cursor.execute("INSERT INTO systems (name, emulator_cmd) VALUES (?, ?)", 
                   ("MAME", "mame.exe"))
    mame_id = cursor.lastrowid

    # Add Games
    games = [
        (snes_id, "Super Mario World", "mario.sfc", 1990),
        (snes_id, "F-Zero", "fzero.sfc", 1990),
        (snes_id, "Chrono Trigger", "chrono.sfc", 1995),
        (mame_id, "Pac-Man", "pacman.zip", 1980),
        (mame_id, "Street Fighter II", "sf2.zip", 1991),
        (mame_id, "Metal Slug", "mslug.zip", 1996)
    ]
    
    cursor.executemany("""
        INSERT INTO games (system_id, title, filename, year) 
        VALUES (?, ?, ?, ?)
    """, games)

    conn.commit()
    conn.close()
    print(f"Database {DB_NAME} created successfully!")

if __name__ == "__main__":
    init_db()