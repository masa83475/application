import os
import glob
import json

from fastapi import APIRouter

router = APIRouter()

from app.config.settings import TEMP_DIR

PROGRESS_FILE = TEMP_DIR / "progress.json"


@router.post("/cleanup")
async def cleanup():

    # CSV削除
    for file in glob.glob(
        os.path.join(
            TEMP_DIR,
            "*.csv"
        )
    ):

        try:
            os.remove(file)
        except Exception:
            pass

    # PDF削除
    for file in glob.glob(
        os.path.join(
            TEMP_DIR,
            "*.pdf"
        )
    ):

        try:
            os.remove(file)
        except Exception:
            pass

    # progress初期化
    try:

        with open(
            PROGRESS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {
                    "status": "idle",
                    "current": 0,
                    "total": 0,
                    "percent": 0
                },
                f,
                ensure_ascii=False
            )

    except Exception:
        pass

    return {
        "status": "ok"
    }