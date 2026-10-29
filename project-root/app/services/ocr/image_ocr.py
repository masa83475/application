import pytesseract
from PIL import Image

def extract_text_from_image(image_path: str) -> str:
    """
    PNG/JPG を OCR してテキスト抽出する
    """
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang="jpn")
    return text
