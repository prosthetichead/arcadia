from fastapi import APIRouter, Depends
from web.dependencies import get_data_manager

router = APIRouter(prefix="/games", tags=["games"])

@router.get("/")
def get_games(data_manager = Depends(get_data_manager)):
    # Quick hack: Load the first playlist (usually All Games) to test connection
    playlists = data_manager.load_playlists()
    if playlists:
        games = data_manager.load_playlist_games(playlists[0].id)
        return [{"id": g.id, "title": g.title, "filename": g.filename} for g in games]
    return []