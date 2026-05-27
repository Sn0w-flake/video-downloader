from __future__ import annotations

import re
from typing import AsyncIterator

import httpx
from f2.apps.douyin.handler import DouyinHandler
from f2.apps.douyin.utils import AwemeIdFetcher, TokenManager, VerifyFpManager


_DOUYIN_RE = re.compile(r"(douyin\.com|iesdouyin\.com)", re.I)

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://www.douyin.com/",
}


def _build_kwargs() -> dict:
    ttwid = TokenManager.gen_ttwid()
    ms_token = TokenManager.gen_false_msToken()
    s_v_web_id = VerifyFpManager.gen_s_v_web_id()
    cookie = f"ttwid={ttwid}; msToken={ms_token}; s_v_web_id={s_v_web_id}"
    return {
        "headers": dict(_HEADERS),
        "proxies": {"http://": None, "https://": None},
        "cookie": cookie,
    }


def is_douyin_url(url: str) -> bool:
    return bool(_DOUYIN_RE.search(url or ""))


async def _aweme_id(url: str) -> str:
    m = re.search(r"(?:modal_id=|/video/|/note/|/share/video/)(\d{15,})", url)
    if m:
        return m.group(1)
    return await AwemeIdFetcher.get_aweme_id(url)


async def extract_info(url: str) -> dict:
    aid = await _aweme_id(url)
    kwargs = _build_kwargs()
    video = await DouyinHandler(kwargs).fetch_one_video(aweme_id=aid)
    raw = video._to_raw() or {}
    detail = raw.get("aweme_detail") or {}
    v = detail.get("video") or {}
    author = detail.get("author") or {}

    formats = []
    for i, br in enumerate(v.get("bit_rate") or []):
        play = br.get("play_addr") or {}
        urls = play.get("url_list") or []
        if not urls:
            continue
        w, h = play.get("width"), play.get("height")
        formats.append({
            "format_id": f"dy-{br.get('gear_name') or i}",
            "ext": "mp4",
            "resolution": f"{w}x{h}" if w and h else None,
            "filesize": play.get("data_size"),
            "vcodec": br.get("HDR_type") or "h264",
            "acodec": "aac",
            "format_note": br.get("gear_name"),
            "kind": "video",
            "_direct_url": urls[0],
        })

    if not formats:
        play = v.get("play_addr") or {}
        urls = play.get("url_list") or []
        if urls:
            formats.append({
                "format_id": "dy-default",
                "ext": "mp4",
                "resolution": None,
                "vcodec": "h264",
                "acodec": "aac",
                "kind": "video",
                "_direct_url": urls[0],
            })

    cover_urls = (v.get("origin_cover") or v.get("cover") or {}).get("url_list") or []
    dur_ms = v.get("duration") or detail.get("duration") or 0
    return {
        "url": url,
        "title": detail.get("desc") or "douyin_video",
        "uploader": author.get("nickname"),
        "thumbnail": cover_urls[0] if cover_urls else None,
        "duration": dur_ms / 1000 if dur_ms else None,
        "extractor": "Douyin",
        "description": detail.get("desc"),
        "formats": formats,
        "subtitles": [],
    }


async def stream_download(url: str, format_id: str) -> tuple[AsyncIterator[bytes], str, str]:
    info = await extract_info(url)
    fmt = next((f for f in info["formats"] if f["format_id"] == format_id), None)
    if not fmt:
        raise RuntimeError("FORMAT_NOT_FOUND")
    direct = fmt["_direct_url"]
    safe = re.sub(r'[\\/:*?"<>|\r\n]+', "_", info["title"])[:120].strip() or "video"
    filename = f"{safe}.mp4"

    async def gen() -> AsyncIterator[bytes]:
        timeout = httpx.Timeout(60.0, connect=20.0, read=None)
        async with httpx.AsyncClient(headers=_HEADERS, timeout=timeout, follow_redirects=True) as c:
            async with c.stream("GET", direct) as r:
                r.raise_for_status()
                async for chunk in r.aiter_bytes(64 * 1024):
                    yield chunk

    return gen(), filename, "mp4"


async def extract_subtitles(url: str, lang: str = "zh-Hans"):
    return None


__all__ = ["is_douyin_url", "extract_info", "stream_download", "extract_subtitles"]
