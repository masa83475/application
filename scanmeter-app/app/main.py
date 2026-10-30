import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers.upload_router import router as upload_router
from app.routers.cleanup_router import router as cleanup_router
from app.routers.progress_router import router as progress_router


# --------------------------------------------------
# パス設定
# --------------------------------------------------

if getattr(sys, "frozen", False):
    # PyInstaller実行時
    BASE_DIR = Path(sys._MEIPASS)
else:
    # 通常実行時
    BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = BASE_DIR / "app" / "static"
TEMPLATE_DIR = BASE_DIR / "app" / "templates"


# --------------------------------------------------
# FastAPI
# --------------------------------------------------

app = FastAPI(
    title="scanmeter-app"
)


# --------------------------------------------------
# Static Files
# --------------------------------------------------

if STATIC_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(STATIC_DIR)),
        name="static"
    )


# --------------------------------------------------
# Templates
# --------------------------------------------------

templates = Jinja2Templates(
    directory=str(TEMPLATE_DIR)
)


# --------------------------------------------------
# Top Page
# --------------------------------------------------

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok"
    }


# --------------------------------------------------
# Routers
# --------------------------------------------------

app.include_router(upload_router)
app.include_router(cleanup_router)
app.include_router(progress_router)