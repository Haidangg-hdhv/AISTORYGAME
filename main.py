from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_debug import router as debug_router
from app.api.routes_game import router as game_router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Backend cho đồ án AI Story Adventure",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_router)
app.include_router(debug_router)


@app.get("/")
def root() -> dict:
    return {
        "message": "AI Story Adventure Backend đang chạy.",
        "docs": "/docs",
    }