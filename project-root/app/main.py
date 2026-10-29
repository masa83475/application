from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers.upload_router import router as upload_router
from app.routers.cleanup_router import router as cleanup_router
from app.routers.progress_router import router as progress_router

app = FastAPI(
    title="scanmeter-app"
)

# Static Files
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# Templates
templates = Jinja2Templates(
    directory="app/templates"
)

# Top Page
@app.get("/")
async def index(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# Health Check
@app.get("/health")
async def health():

    return {
        "status": "ok"
    }

# Routers
app.include_router(upload_router)
app.include_router(cleanup_router)
app.include_router(progress_router)