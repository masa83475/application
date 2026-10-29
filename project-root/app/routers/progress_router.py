import json
import os

from fastapi import APIRouter

router = APIRouter()

from app.config.settings import TEMP_DIR

PROGRESS_FILE = TEMP_DIR / "progress.json"


@router.get("/progress")
async def get_progress():

    # progressファイルが無い場合
    if not os.path.exists(PROGRESS_FILE):

        return {
            "current": 0,
            "total": 0,
            "percent": 0,
            "status": "idle"
        }

    try:

        with open(
            PROGRESS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            progress = json.load(f)

        return progress

    except Exception:

        return {
            "current": 0,
            "total": 0,
            "percent": 0,
            "status": "error"
        }