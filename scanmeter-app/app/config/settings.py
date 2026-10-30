import sys
from pathlib import Path


# --------------------------------------------------
# ベースディレクトリ
# --------------------------------------------------

if getattr(sys, "frozen", False):
    # PyInstaller EXE実行時
    BASE_DIR = Path(sys.executable).parent
else:
    # 通常のPython実行時
    BASE_DIR = Path(__file__).resolve().parent.parent.parent


# --------------------------------------------------
# アプリフォルダ
# --------------------------------------------------

RUNTIME_DIR = BASE_DIR / "runtime"
TEMP_DIR = BASE_DIR / "temp"


# --------------------------------------------------
# Tesseract
# --------------------------------------------------

TESSERACT_PATH = (
    RUNTIME_DIR
    / "tesseract"
    / "tesseract.exe"
)


# --------------------------------------------------
# Poppler
# --------------------------------------------------

POPPLER_PATH = (
    RUNTIME_DIR
    / "poppler"
    / "Library"
    / "bin"
)
