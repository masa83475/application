import json
import os
import threading

from uuid import uuid4

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException

from fastapi.responses import FileResponse

from app.services.ocr_service import pdf_to_csv

router = APIRouter()

from app.config.settings import TEMP_DIR

UPLOAD_DIR = TEMP_DIR
PROGRESS_FILE = TEMP_DIR / "progress.json"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

CURRENT_CSV = None


def run_ocr(
    pdf_path,
    csv_path
):
    global CURRENT_CSV

    try:

        result_csv = pdf_to_csv(
            pdf_path,
            csv_path
        )

        if os.path.exists(
            pdf_path
        ):
            os.remove(
                pdf_path
            )

        CURRENT_CSV = result_csv

    except Exception as e:

        with open(
            PROGRESS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {
                    "status": "error",
                    "current": 0,
                    "total": 0,
                    "percent": 0,
                    "message": str(e)
                },
                f,
                ensure_ascii=False
            )


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    global CURRENT_CSV

    CURRENT_CSV = None

    with open(
        PROGRESS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "status": "starting",
                "current": 0,
                "total": 0,
                "percent": 0
            },
            f,
            ensure_ascii=False
        )

    pdf_path = UPLOAD_DIR / f"{uuid4()}_{file.filename}"

    with open(
        pdf_path,
        "wb"
    ) as f:

        f.write(
            await file.read()
        )

    csv_path = pdf_path.with_suffix(".csv")

    thread = threading.Thread(
    target=run_ocr,
    args=(
        str(pdf_path),
        str(csv_path)
    ),
    daemon=True
)

    thread.start()

    return {
        "status": "started"
    }


@router.get("/download")
def download_csv():

    global CURRENT_CSV

    if not CURRENT_CSV:
        raise HTTPException(
            status_code=404,
            detail="CSV未生成"
        )

    return FileResponse(
        CURRENT_CSV,
        filename="result.csv",
        media_type="text/csv"
    )