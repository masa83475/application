import threading
import webbrowser
import uvicorn
from pathlib import Path

from app.main import app


HOST = "127.0.0.1"
PORT = 8000


def open_browser():
    webbrowser.open(
        f"http://{HOST}:{PORT}"
    )


def ensure_runtime_folders():
    base_dir = Path(__file__).resolve().parent

    (base_dir / "temp").mkdir(
        exist_ok=True
    )

    (base_dir / "logs").mkdir(
        exist_ok=True
    )


if __name__ == "__main__":

    ensure_runtime_folders()

    threading.Timer(
        2,
        open_browser
    ).start()

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=False,
        log_level="info"
    )