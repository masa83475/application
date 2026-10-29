import os
import csv
import json

from pdf2image import (
    convert_from_path,
    pdfinfo_from_path
)

import pytesseract
from pytesseract import Output


# =========================
# Tesseract設定
# =========================

from app.config.settings import (
    TESSERACT_PATH,
    POPPLER_PATH,
    TEMP_DIR
)

pytesseract.pytesseract.tesseract_cmd = str(
    TESSERACT_PATH
)

PROGRESS_FILE = TEMP_DIR / "progress.json"


def update_progress(
    current,
    total,
    status="running"
):

    percent = 0

    if total > 0:
        percent = round(
            current / total * 100,
            1
        )

    with open(
        PROGRESS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "status": status,
                "current": current,
                "total": total,
                "percent": percent
            },
            f,
            ensure_ascii=False
        )


def extract_text_horizontal(image):

    print("===== OCR START =====")
    print(
        "Tesseract Version:",
        pytesseract.get_tesseract_version()
    )

    data = pytesseract.image_to_data(
        image,
        lang="jpn",
        output_type=Output.DICT
    )

    rows = []

    count = len(
        data["text"]
    )

    for i in range(count):

        text = data["text"][i].strip()

        if not text:
            continue

        rows.append(
            {
                "text": text,
                "top": data["top"][i],
                "left": data["left"][i]
            }
        )

    rows.sort(
        key=lambda x: (
            round(x["top"] / 15),
            x["left"]
        )
    )

    return rows


def merge_rows(rows):

    merged_lines = []

    current_row = []
    current_top = None

    for row in rows:

        top_group = round(
            row["top"] / 15
        )

        if current_top is None:
            current_top = top_group

        if current_top != top_group:

            merged_lines.append(
                " ".join(current_row)
            )

            current_row = []
            current_top = top_group

        current_row.append(
            row["text"]
        )

    if current_row:

        merged_lines.append(
            " ".join(current_row)
        )

    return merged_lines


def pdf_to_csv(
    pdf_path,
    csv_path
):

    print("===== PDF INFO =====")

    info = pdfinfo_from_path(
    pdf_path,
    poppler_path=str(POPPLER_PATH)
)

    total_pages = info["Pages"]

    print(
        f"Total Pages: {total_pages}"
    )

    update_progress(
        0,
        total_pages
    )

    result_lines = []

    for page_no in range(
        1,
        total_pages + 1
    ):

        print(
            f"Page {page_no}"
        )

        update_progress(
            page_no,
            total_pages
        )

        print("convert start")

        images = convert_from_path(
            pdf_path,
            first_page=page_no,
            last_page=page_no,
            poppler_path=str(POPPLER_PATH)
        )
        print("convert done")

        image = images[0]

        rows = extract_text_horizontal(
            image
        )

        print("ocr done")

        lines = merge_rows(
            rows
        )

        result_lines.extend(
            lines
        )

    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            ["OCR結果"]
        )

        for line in result_lines:

            writer.writerow(
                [line]
            )

    update_progress(
        total_pages,
        total_pages,
        "completed"
    )

    return csv_path