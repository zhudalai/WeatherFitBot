from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.cache.redis_client import cache
from app.api import chat_router, weather_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时连接 Redis
    await cache.connect()
    yield
    # 关闭时断开 Redis
    await cache.disconnect()


app = FastAPI(
    title="WeatherFit API",
    description="天气穿搭助手 API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(chat_router)
app.include_router(weather_router)


@app.get("/")
async def root():
    return {"message": "WeatherFit API is running", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}
