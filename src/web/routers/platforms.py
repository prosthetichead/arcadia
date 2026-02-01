from fastapi import APIRouter, Depends
from web.dependencies import get_data_manager
from web.schemas import PlatformCreate
from shared.models import Platform

router = APIRouter(prefix="/platforms", tags=["platforms"])

@router.post("/")
def add_platform(platform: PlatformCreate, data_manager = Depends(get_data_manager)):
    session = data_manager.Session()
    try:
        new_platform = Platform(
            name=platform.name,
            emulator_directory=platform.emulator_path,
            rom_directory=platform.rom_directory,
            emulator_cmd=platform.command,
            asset_directory=platform.asset_directory,
            screenscraper_id=platform.screenscraper_id
        )
        session.add(new_platform)
        session.commit()
        return {"status": "success", "platform_id": new_platform.id}
    finally:
        session.close()