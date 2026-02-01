from pydantic import BaseModel
from typing import Optional

class PlatformCreate(BaseModel):
    name: str
    emulator_path: str
    rom_directory: str
    command: str
    asset_directory: Optional[str] = None
    screenscraper_id: Optional[int] = None