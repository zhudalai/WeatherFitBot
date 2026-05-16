from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from app.cache.redis_client import cache
from app.api import chat_router, weather_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await cache.connect()
    yield
    await cache.disconnect()


app = FastAPI(
    title="WeatherFit API",
    description="天气穿搭助手 API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(weather_router)


@app.get("/health")
async def health():
    return {"status": "ok"}


# 生产环境：托管前端构建产物
_FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
_INDEX_FILE = _FRONTEND_DIST / "index.html"

if _INDEX_FILE.exists():
    _assets_dir = _FRONTEND_DIST / "assets"
    if _assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=str(_assets_dir)), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_frontend(full_path: str):
        return FileResponse(str(_INDEX_FILE))
