from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

RUNTIME_DIR = BASE_DIR /  "runtime"

TEMP_DIR = BASE_DIR / "temp"

TESSERACT_PATH = (
    RUNTIME_DIR /
    "tesseract" /
    "tesseract.exe"
)

POPPLER_PATH = (
    RUNTIME_DIR /
    "poppler" /
    "Library" /
    "bin"
)