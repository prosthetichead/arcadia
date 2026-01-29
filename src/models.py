from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Setting(Base):
    __tablename__ = 'settings'
    
    name = Column(String, primary_key=True)
    value = Column(String)
    type = Column(String)
    display_section = Column(String)
    display_name = Column(String)
    description = Column(String)

class Platform(Base):
    __tablename__ = 'platforms'
    
    id = Column(Integer, primary_key=True)
    screenscraper_id = Column(Integer, nullable=True)
    name = Column(String)
    emulator_cmd = Column(String)
    
    games = relationship("Game", back_populates="platform")

class Game(Base):
    __tablename__ = 'games'
    
    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    screenscraper_id = Column(Integer, nullable=True)
    title = Column(String)
    filename = Column(String)
    
    release_year = Column(Integer, nullable=True)
    developer = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    players = Column(String, nullable=True)
    playtime_minutes = Column(Integer, nullable=True)
    play_count = Column(Integer, default=0)
    
    platform = relationship("Platform", back_populates="games")
    playlist_associations = relationship("PlaylistGame", back_populates="game")

class Playlist(Base):
    __tablename__ = 'playlists'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String, nullable=True)
    is_dynamic = Column(Boolean, default=False)
    filter_query = Column(String, nullable=True)
    
    game_associations = relationship("PlaylistGame", back_populates="playlist")

class PlaylistGame(Base):
    __tablename__ = 'playlist_games'
    
    playlist_id = Column(Integer, ForeignKey('playlists.id'), primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'), primary_key=True)
    display_order = Column(Integer, default=0)
    
    playlist = relationship("Playlist", back_populates="game_associations")
    game = relationship("Game", back_populates="playlist_associations")