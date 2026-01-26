import pyray as pr
import subprocess
import time
import os
import sys
import json
import importlib
import importlib.util
import inspect
from app_state import AppState
from data_manager import DataManager

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
DB_NAME = os.path.join(ROOT_DIR, "data", "arcade.db")

# Registry to store available component classes: {"GameList": <class GameList>, ...}
COMPONENT_REGISTRY = {}

def scan_components(directory, package_prefix=None):
    """Scans a directory for .py files and registers classes found inside."""
    if not os.path.exists(directory):
        return

    for filename in os.listdir(directory):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            try:
                module = None
                if package_prefix:
                    # Import as part of the package (e.g. components.game_list)
                    # This ensures relative imports inside them work
                    module = importlib.import_module(f"{package_prefix}.{module_name}")
                else:
                    # Load standalone file (themes)
                    path = os.path.join(directory, filename)
                    spec = importlib.util.spec_from_file_location(module_name, path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                if module:
                    # Find classes defined in this module
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        # Only register classes defined in this specific module (avoids imports)
                        if obj.__module__ == module.__name__:
                            COMPONENT_REGISTRY[name] = obj
            except Exception as e:
                print(f"Error loading module {filename}: {e}")

# --- Main Entry Point ---
def main():
    data_manager = DataManager(DB_NAME)
    settings = data_manager.load_settings()
    
    app_state = AppState()
    app_state.games = data_manager.load_games()
    
    pr.init_window(settings.get("screen_res_width", 800), settings.get("screen_res_height", 600), "ARCADIA")
    pr.set_target_fps(60)

    # Load Components
    scan_components(os.path.join(SRC_DIR, "components"), package_prefix="components")

    # --- Load Theme ---
    current_theme = settings.get("theme", "default")
    components = []
    theme_dir = os.path.join(ROOT_DIR, "themes", current_theme)
    theme_path = os.path.join(theme_dir, "theme.json")
    # Load theme-specific components (overrides core if names match)
    scan_components(theme_dir)
    

    if os.path.exists(theme_path):
        try:
            with open(theme_path, "r") as f:
                theme_data = json.load(f)

            for comp_data in theme_data.get("components", []):
                comp_type = comp_data.get("type")
                comp_class = COMPONENT_REGISTRY.get(comp_type)
                if comp_class:
                    x = comp_data.get("x", 0)
                    y = comp_data.get("y", 0)
                    width = comp_data.get("width", 0)
                    height = comp_data.get("height", 0)
                    props = comp_data.get("props", {})
                    instance = comp_class(x, y, width, height, props, app_state)
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