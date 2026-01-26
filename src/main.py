import sqlite3
import pyray as pr
import subprocess
import time
import os
import sys
import json
from components.game_list import GameList

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
DB_NAME = os.path.join(ROOT_DIR, "data", "arcade.db")

SETTINGS = {}

def load_settings():
    global SETTINGS
    SETTINGS.clear()

    if not os.path.exists(DB_NAME):
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT name, value, type FROM settings")
        for name, value, type_ in cursor.fetchall():
            if type_ == "int":
                SETTINGS[name] = int(value)
            elif type_ == "bool":
                SETTINGS[name] = (str(value).lower() == "true")
            else:
                SETTINGS[name] = value
    finally:
        conn.close()

COMPONENT_MAP = {
    "GameList": GameList
}

# --- Main Entry Point ---
def main():

    load_settings()
    
    pr.init_window(SETTINGS.get("screen_res_width", 800), SETTINGS.get("screen_res_height", 600), "ARCADIA")
    pr.set_target_fps(60)

    # --- Load Theme ---
    current_theme = SETTINGS.get("theme", "default")
    components = []
    theme_path = os.path.join(ROOT_DIR, "themes", current_theme, "theme.json")
    if os.path.exists(theme_path):
        try:
            with open(theme_path, "r") as f:
                theme_data = json.load(f)

            for comp_data in theme_data.get("components", []):
                comp_type = comp_data.get("type")
                if comp_type in COMPONENT_MAP:
                    x = comp_data.get("x", 0)
                    y = comp_data.get("y", 0)
                    width = comp_data.get("width", 0)
                    height = comp_data.get("height", 0)
                    props = comp_data.get("props", {})
                    instance = COMPONENT_MAP[comp_type](x, y, width, height, props)
                    components.append(instance)
            print(f"Loaded theme: {current_theme}")
        except Exception as e:
            print(f"Error loading theme: {e}")

    # --- The Loop ---
    while not pr.window_should_close():
        
        # INPUT

        # UPDATE
        for component in components:
            if hasattr(component, "update"):
                component.update()

        # DRAWING
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)

        for component in components:
            if hasattr(component, "draw"):
                component.draw()
        
        pr.end_drawing()

    pr.close_window()

if __name__ == "__main__":
    main()


# --- The Launcher Logic ---
""" def launch_game(game_title, emulator, rom_file):
    print(f"--- LAUNCHING: {game_title} ---")
            
    try:
        # This freezes Arcadia until the game closes
        subprocess.run(
            [sys.executable, "mock_game.py", game_title], 
            check=True
        )

    except Exception as e:
        print(f"Error launching game: {e}")

    print("--- GAME OVER ---")
    
    pr.set_window_focused() """