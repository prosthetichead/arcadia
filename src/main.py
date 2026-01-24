import sqlite3
import pyray as pr
import subprocess
import time
import os
import sys

DB_NAME = "arcade.db"

# --- Database Logic ---
def get_games():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Fetch the emulator command too so we know what to run
    query = """
        SELECT games.title, games.year, systems.name, systems.emulator_cmd, games.filename 
        FROM games 
        JOIN systems ON games.system_id = systems.id
        ORDER BY systems.name, games.title
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

# --- The Launcher Logic ---
def launch_game(game_title, emulator, rom_file):
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
    
    pr.set_window_focused()

# --- Main Entry Point ---
def main():
    screen_width = 800
    screen_height = 600
    pr.init_window(screen_width, screen_height, "ARCADIA System")
    pr.set_target_fps(60)
    
    games_list = get_games()
    selected_index = 0
    
    # --- The Loop ---
    while not pr.window_should_close():
        
        # INPUT HANDLING
        if pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN):
            selected_index += 1
        if pr.is_key_pressed(pr.KeyboardKey.KEY_UP):
            selected_index -= 1
        
        # LAUNCH TRIGGER (Enter Key)
        if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
            # Unpack the data for the selected game
            # (title, year, system, emulator_cmd, filename)
            current_game = games_list[selected_index]
            
            # Pass data to the launcher function
            launch_game(current_game[0], current_game[3], current_game[4])

        # Wrap selection logic
        if selected_index >= len(games_list):
            selected_index = 0
        elif selected_index < 0:
            selected_index = len(games_list) - 1

        # DRAWING
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)

        # Header
        pr.draw_rectangle(0, 0, screen_width, 60, pr.DARKPURPLE)
        pr.draw_text("ARCADIA", 20, 20, 20, pr.WHITE)

        # List
        for i, (title, year, system, emu, rom) in enumerate(games_list):
            y_pos = 80 + (i * 40)
            
            if i == selected_index:
                pr.draw_rectangle(0, y_pos - 5, screen_width, 40, pr.MAROON)
                color = pr.YELLOW
                prefix = "> "
            else:
                color = pr.RAYWHITE
                prefix = "  "
            
            text = f"{prefix}{title} ({year}) - {system}"
            pr.draw_text(text, 50, y_pos, 20, color)

        # Instructions
        pr.draw_text("PRESS ENTER TO START GAME", 20, screen_height - 30, 10, pr.GRAY)

        pr.end_drawing()

    pr.close_window()

if __name__ == "__main__":
    main()