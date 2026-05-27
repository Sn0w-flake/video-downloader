from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routers import ai as ai_router
from routers import video as video_router

app = FastAPI(title="Universal Video Downloader", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(video_router.router)
app.include_router(ai_router.router)


@app.get("/api/health")
def health():
    return {"ok": True, "llm_enabled": settings.llm_enabled}
