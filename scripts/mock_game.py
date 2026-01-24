# mock_game.py
import tkinter as tk
import sys

# Grab the game name from arguments if provided
game_name = "Unknown Game"
if len(sys.argv) > 1:
    game_name = sys.argv[1]

# Create a simple window
root = tk.Tk()
root.title(f"Running: {game_name}")
root.geometry("600x400")
root.configure(bg="black")

# Add some text
label = tk.Label(root, text=f"GAME RUNNING: {game_name}\n\n(Close this window to return to Arcadia)", 
                 fg="#00ff00", bg="black", font=("Consolas", 14))
label.pack(expand=True)

# Force this window to the front
root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',False)

# This blocks the script until the window is closed
root.mainloop()