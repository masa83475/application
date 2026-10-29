import pytesseract
from app.config.settings import POPPLER_PATH
import tempfile
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    紙PDF（画像ベース）を OCR してテキスト抽出する
    """
    text = ""

    # PDF → 画像化（300dpi）
    images = convert_from_path(
        pdf_path,
        poppler_path=str(POPPLER_PATH)
)

    for img in images:
        # 一時ファイルに画像保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            img.save(tmp.name, "PNG")
            tmp_path = tmp.name

        # OCR実行（日本語）
        page_text = pytesseract.image_to_string(tmp_path, lang="jpn")
        text += page_text + "\n"

        # 一時ファイル削除
        os.remove(tmp_path)

    return text
