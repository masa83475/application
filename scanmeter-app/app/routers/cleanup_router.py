import json
from pathlib import Path

from fastapi import APIRouter

from app.config.settings import TEMP_DIR

router = APIRouter()

PROGRESS_FILE = TEMP_DIR / "progress.json"


@router.post("/cleanup")
async def cleanup():

    deleted_files = []

    # CSV削除
    for file in TEMP_DIR.glob("*.csv"):
        try:
            file.unlink()
            deleted_files.append(file.name)
        except Exception as e:
            print(f"CSV削除エラー: {file} -> {e}")

    # PDF削除
    for file in TEMP_DIR.glob("*.pdf"):
        try:
            file.unlink()
            deleted_files.append(file.name)
        except Exception as e:
            print(f"PDF削除エラー: {file} -> {e}")

    # progress初期化
    try:
        progress = {
            "status": "idle",
            "current": 0,
            "total": 0,
            "percent": 0
        }

        with open(
            PROGRESS_FILE,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                progress,
                f,
                ensure_ascii=False
            )

    except Exception as e:
        print(f"progress初期化エラー: {e}")

        return {
            "status": "error",
            "message": str(e)
        }

    return {
        "status": "ok",
        "deleted_count": len(deleted_files),
        "deleted_files": deleted_files
    }