class AppState:
    def __init__(self):
        self.playlists = []
        self.games = []
        self.selected_game_index = 1
        self.selected_game = None
        self.selected_playlist_index = 1
        self.selected_playlist = None
        self.game_running = True