import os
import sys
from fastapi import FastAPI

# --- PATH SETUP ---
# Ensure we can import from 'shared'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(SRC_DIR)

from shared.data_manager import DataManager

# --- CONFIG ---
ROOT_DIR = os.path.dirname(SRC_DIR)
DB_PATH = os.path.join(ROOT_DIR, "data", "arcade.db")

app = FastAPI(title="Arcadia Admin")
data_manager = DataManager(DB_PATH)

@app.get("/")
def read_root():
    return {"status": "Arcadia Admin Online"}

@app.get("/games")
def get_games():
    # We can reuse the logic from data_manager, or query directly
    # For now, let's just list all games from the "All Games" playlist logic
    # or we can add a method to DataManager to get_all_games()
    
    # Quick hack: Load the first playlist (usually All Games) to test connection
    playlists = data_manager.load_playlists()
    if playlists:
        games = data_manager.load_playlist_games(playlists[0].id)
        return [{"id": g.id, "title": g.title, "filename": g.filename} for g in games]
    return []

if __name__ == "__main__":
    import uvicorn
    # Run on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)