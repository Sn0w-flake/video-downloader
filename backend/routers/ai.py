from __future__ import annotations

import asyncio

from fastapi import APIRouter, HTTPException

from config import settings
from schemas import (
    SummarizeRequest,
    SummarizeResponse,
    TranslateRequest,
    TranslateResponse,
)
from services import douyin_service, ytdlp_service, llm_service


def _pick(url: str):
    return douyin_service if douyin_service.is_douyin_url(url) else ytdlp_service

router = APIRouter(prefix="/api/ai", tags=["ai"])


def _require_llm():
    if not settings.llm_enabled:
        raise HTTPException(status_code=503, detail="LLM_NOT_CONFIGURED")


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(payload: SummarizeRequest):
    _require_llm()
    svc = _pick(payload.url)
    try:
        info = await svc.extract_info(payload.url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"EXTRACT_FAILED: {e}")

    sub = await svc.extract_subtitles(payload.url, payload.lang)
    if not sub:
        raise HTTPException(status_code=404, detail="SUBTITLE_NOT_FOUND")
    _, srt = sub

    try:
        summary, used = await asyncio.to_thread(llm_service.summarize_video, info["title"], srt)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM_FAILED: {e}")

    return SummarizeResponse(title=info["title"], summary=summary, tokens_used=used)


@router.post("/translate", response_model=TranslateResponse)
async def translate(payload: TranslateRequest):
    _require_llm()
    if not payload.srt.strip():
        raise HTTPException(status_code=422, detail="INVALID_SRT")
    try:
        translated, used = await asyncio.to_thread(llm_service.translate_srt, payload.srt, payload.target_lang)
    except ValueError:
        raise HTTPException(status_code=422, detail="INVALID_SRT")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM_FAILED: {e}")
    return TranslateResponse(target_lang=payload.target_lang, srt=translated, tokens_used=used)
