from __future__ import annotations

import asyncio
import urllib.parse
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from yt_dlp.utils import DownloadError

from schemas import BatchItem, BatchRequest, BatchResponse, SubtitleResponse, VideoInfo
from services import douyin_service, ytdlp_service

router = APIRouter(prefix="/api", tags=["video"])


def _pick(url: str):
    return douyin_service if douyin_service.is_douyin_url(url) else ytdlp_service

_EXT_MIME = {
    "mp4": "video/mp4",
    "webm": "video/webm",
    "mkv": "video/x-matroska",
    "m4a": "audio/mp4",
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "ogg": "audio/ogg",
}


@router.get("/info", response_model=VideoInfo)
async def get_info(url: str = Query(..., min_length=4)):
    try:
        info = await _pick(url).extract_info(url)
        return info
    except DownloadError as e:
        raise HTTPException(status_code=422, detail=f"UNSUPPORTED_OR_INVALID_URL: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"EXTRACT_FAILED: {e}")


@router.get("/download")
async def download(
    url: str = Query(..., min_length=4),
    format_id: str = Query(...),
    filename: Optional[str] = Query(default=None),
):
    try:
        gen, default_name, ext = await _pick(url).stream_download(url, format_id)
    except DownloadError as e:
        raise HTTPException(status_code=422, detail=f"UNSUPPORTED_OR_INVALID_URL: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DOWNLOAD_FAILED: {e}")

    fn = filename or default_name
    mime = _EXT_MIME.get(ext, "application/octet-stream")
    disposition = "attachment; filename*=UTF-8''" + urllib.parse.quote(fn)
    headers = {"Content-Disposition": disposition, "X-Accel-Buffering": "no"}
    return StreamingResponse(gen, media_type=mime, headers=headers)


@router.post("/batch", response_model=BatchResponse)
async def batch(payload: BatchRequest):
    if not payload.urls:
        raise HTTPException(status_code=400, detail="EMPTY_URLS")

    sem = asyncio.Semaphore(5)

    async def one(u: str) -> BatchItem:
        async with sem:
            try:
                info = await _pick(u).extract_info(u)
                return BatchItem(url=u, ok=True, info=info)
            except DownloadError as e:
                return BatchItem(url=u, ok=False, error=f"UNSUPPORTED_OR_INVALID_URL: {e}")
            except Exception as e:
                return BatchItem(url=u, ok=False, error=f"EXTRACT_FAILED: {e}")

    results = await asyncio.gather(*(one(u) for u in payload.urls))
    return BatchResponse(results=results)


@router.get("/subtitles", response_model=SubtitleResponse)
async def subtitles(url: str = Query(...), lang: str = Query(default="zh-Hans")):
    try:
        result = await _pick(url).extract_subtitles(url, lang)
    except DownloadError as e:
        raise HTTPException(status_code=422, detail=f"UNSUPPORTED_OR_INVALID_URL: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SUBTITLE_FETCH_FAILED: {e}")
    if not result:
        raise HTTPException(status_code=404, detail="SUBTITLE_NOT_FOUND")
    chosen_lang, content = result
    return SubtitleResponse(lang=chosen_lang, format="srt", content=content)
