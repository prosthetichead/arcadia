import os
from sqlalchemy import create_engine
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base, Setting, Game, Platform, Playlist, PlaylistGame

class DataManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{self.db_path}")
        self.Session = sessionmaker(bind=self.engine)
        
        # Initialize DB if it doesn't exist
        if not os.path.exists(self.db_path):
            self._init_db()
        else:
            # Ensure tables exist even if file exists
            Base.metadata.create_all(self.engine)

    def _init_db(self):
        """Creates tables and seeds default data."""
        print("Initializing new database...")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        Base.metadata.create_all(self.engine)
        self._seed_defaults()

    def _seed_defaults(self):
        """Seeds the database with initial data."""
        session = self.Session()

        # Settings
        settings = [
            Setting(name="theme", value="default", type="string", display_section="Appearance", display_name="Theme", description="The visual theme to use for the interface."),
            Setting(name="fullscreen", value="true", type="bool", display_section="Video", display_name="Fullscreen", description="Run Arcadia in fullscreen exclusive mode."),
            Setting(name="screen_res_width", value="800", type="int", display_section="Video", display_name="Screen Width", description="Screen width in pixels"),
            Setting(name="screen_res_height", value="600", type="int", display_section="Video", display_name="Screen Height", description="Screen height in pixels")
        ]
        session.add_all(settings)

        # Platforms
        snes = Platform(name="SNES", emulator_cmd="snes9x.exe")
        mame = Platform(name="MAME", emulator_cmd="mame.exe")
        session.add(snes)
        session.add(mame)
        session.flush()

        # Games
        games = [
            Game(platform_id=snes.id, title="Super Mario World", filename="mario.sfc", release_year=1990),
            Game(platform_id=snes.id, title="F-Zero", filename="fzero.sfc", release_year=1990),
            Game(platform_id=snes.id, title="Chrono Trigger", filename="chrono.sfc", release_year=1995),
            Game(platform_id=mame.id, title="Pac-Man", filename="pacman.zip", release_year=1980),
            Game(platform_id=mame.id, title="Street Fighter II", filename="sf2.zip", release_year=1991),
            Game(platform_id=mame.id, title="Metal Slug", filename="mslug.zip", release_year=1996)
        ]
        session.add_all(games)
        session.flush()

        # Playlists
        # All Games (Dynamic, Empty Filter = All)
        all_games_playlist = Playlist(name="All Games", description="All available games", is_dynamic=True, filter_query=None)
        
        # Favorites (Static, Manual selection)
        fav_playlist = Playlist(name="Favorites", description="Manually selected favorite games", is_dynamic=False)
        
        # 90s Hits (Dynamic, Range Filter)
        nineties_playlist = Playlist(name="90s Hits", description="Games from the 1990s", is_dynamic=True, filter_query="release_year >= 1990 AND release_year < 2000")
        
        session.add(all_games_playlist)
        session.add(fav_playlist)
        session.add(nineties_playlist)
        session.flush()

        # Playlist Associations
        #session.add(PlaylistGame(playlist_id=fav_playlist.id, game_id=games[0].id, display_order=0))
        #session.add(PlaylistGame(playlist_id=fav_playlist.id, game_id=games[4].id, display_order=1))

        session.commit()
        session.close()


    def load_settings(self):
        session = self.Session()
        settings = {}
        rows = session.query(Setting).all()
        
        for row in rows:
            if row.type == "int":
                settings[row.name] = int(row.value)
            elif row.type == "bool":
                settings[row.name] = (str(row.value).lower() == "true")
            else:
                settings[row.name] = row.value
        
        session.close()
        return settings

    def load_playlists(self):
        """Returns a list of all playlists objects."""
        session = self.Session()
        playlists = session.query(Playlist).all()
        session.close()
        return playlists
    
    
    def load_playlist_games(self, playlist_id):
        """Returns a list of Game objects for a specific playlist."""
        session = self.Session()
        playlist = session.query(Playlist).get(playlist_id)
        
        if not playlist:
            session.close()
            return []
            
        games = []
        if playlist.is_dynamic:
            query = session.query(Game)
            
            # If filter_query is empty, it returns all games (like "All Games" playlist)
            if playlist.filter_query:
                query = query.filter(text(playlist.filter_query))
            
            games = query.all()
        else:
            # For static playlists, join through the association table
            games = session.query(Game).join(PlaylistGame).filter(PlaylistGame.playlist_id == playlist.id).order_by(PlaylistGame.display_order).all()
            
        session.close()
        if(games == None):
            return []
        return games