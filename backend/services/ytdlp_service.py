from __future__ import annotations

import asyncio
import re
from typing import AsyncIterator, Optional

import httpx
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


_BASE_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
    "skip_download": True,
    "extract_flat": False,
}


def _classify(fmt: dict) -> str:
    v = (fmt.get("vcodec") or "").lower()
    a = (fmt.get("acodec") or "").lower()
    if v and v != "none" and a and a != "none":
        return "video"
    if (not v or v == "none") and a and a != "none":
        return "audio"
    if v and v != "none" and (not a or a == "none"):
        return "video_only"
    return "unknown"


def _trim_formats(formats: list[dict]) -> list[dict]:
    items = []
    for f in formats or []:
        kind = _classify(f)
        items.append({
            "format_id": f.get("format_id"),
            "ext": f.get("ext"),
            "resolution": f.get("resolution") or (f"{f.get('width')}x{f.get('height')}" if f.get("width") and f.get("height") else None),
            "fps": f.get("fps"),
            "filesize": f.get("filesize"),
            "filesize_approx": f.get("filesize_approx"),
            "vcodec": f.get("vcodec"),
            "acodec": f.get("acodec"),
            "format_note": f.get("format_note"),
            "tbr": f.get("tbr"),
            "abr": f.get("abr"),
            "kind": kind,
            "url": f.get("url"),
            "http_headers": f.get("http_headers"),
        })
    return items


def _extract_sync(url: str, opts: Optional[dict] = None) -> dict:
    merged = {**_BASE_OPTS, **(opts or {})}
    with YoutubeDL(merged) as ydl:
        info = ydl.extract_info(url, download=False)
        return ydl.sanitize_info(info)


async def extract_info(url: str) -> dict:
    raw = await asyncio.to_thread(_extract_sync, url)
    if raw.get("_type") == "playlist":
        entries = [e for e in (raw.get("entries") or []) if e]
        raw = entries[0] if entries else raw

    subs_keys = list((raw.get("subtitles") or {}).keys()) + list((raw.get("automatic_captions") or {}).keys())
    return {
        "url": url,
        "title": raw.get("title") or "untitled",
        "uploader": raw.get("uploader") or raw.get("channel"),
        "thumbnail": raw.get("thumbnail"),
        "duration": raw.get("duration"),
        "extractor": raw.get("extractor_key") or raw.get("extractor"),
        "description": (raw.get("description") or "")[:600],
        "formats": _trim_formats(raw.get("formats") or []),
        "subtitles": sorted(set(subs_keys)),
    }


def _resolve_direct_url_sync(url: str, format_id: str) -> tuple[str, dict, str, str]:
    opts = {**_BASE_OPTS, "format": format_id}
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if info.get("_type") == "playlist":
            entries = [e for e in (info.get("entries") or []) if e]
            info = entries[0]
        chosen = info.get("requested_formats") or [info]
        target = chosen[0]
        direct = target.get("url")
        headers = target.get("http_headers") or {}
        ext = target.get("ext") or "mp4"
        title = info.get("title") or "video"
        if not direct:
            raise RuntimeError("yt-dlp 未能返回直链，可能该格式需要合并 (video+audio)，请选用合并格式或单独 video/audio")
        return direct, headers, ext, title


async def stream_download(url: str, format_id: str) -> tuple[AsyncIterator[bytes], str, str]:
    direct, headers, ext, title = await asyncio.to_thread(_resolve_direct_url_sync, url, format_id)
    safe_title = re.sub(r'[\\/:*?"<>|\r\n]+', "_", title)[:120].strip() or "video"
    filename = f"{safe_title}.{ext}"

    async def gen() -> AsyncIterator[bytes]:
        timeout = httpx.Timeout(60.0, connect=20.0, read=None)
        async with httpx.AsyncClient(headers=headers, timeout=timeout, follow_redirects=True) as client:
            async with client.stream("GET", direct) as resp:
                resp.raise_for_status()
                async for chunk in resp.aiter_bytes(chunk_size=64 * 1024):
                    yield chunk

    return gen(), filename, ext


def _extract_subs_sync(url: str, lang: str) -> tuple[str, str] | None:
    """返回 (lang, srt_text)，找不到返回 None"""
    opts = {**_BASE_OPTS, "writesubtitles": True, "writeautomaticsub": True}
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if info.get("_type") == "playlist":
            entries = [e for e in (info.get("entries") or []) if e]
            info = entries[0]
        subs = info.get("subtitles") or {}
        auto = info.get("automatic_captions") or {}

        candidates = [lang, "zh-Hans", "zh-CN", "zh", "zh-Hant", "en", "en-US"]
        candidates = list(dict.fromkeys(candidates))
        chosen_lang = None
        chosen_tracks = None
        for code in candidates:
            if code in subs:
                chosen_lang, chosen_tracks = code, subs[code]
                break
        if not chosen_tracks:
            for code in candidates:
                if code in auto:
                    chosen_lang, chosen_tracks = code, auto[code]
                    break
        if not chosen_tracks:
            return None

        srt = next((t for t in chosen_tracks if t.get("ext") == "srt"), None)
        vtt = next((t for t in chosen_tracks if t.get("ext") == "vtt"), None)
        json3 = next((t for t in chosen_tracks if t.get("ext") == "json3"), None)
        target = srt or vtt or json3 or chosen_tracks[0]
        track_url = target.get("url")
        if not track_url:
            return None
        with httpx.Client(timeout=30.0) as c:
            r = c.get(track_url)
            r.raise_for_status()
            text = r.text
        if target.get("ext") == "srt":
            return chosen_lang, text
        if target.get("ext") == "vtt":
            return chosen_lang, _vtt_to_srt(text)
        if target.get("ext") == "json3":
            return chosen_lang, _json3_to_srt(text)
        return chosen_lang, text


def _vtt_to_srt(vtt: str) -> str:
    lines = vtt.splitlines()
    out, idx, buf = [], 0, []
    started = False
    for ln in lines:
        if ln.strip().startswith("WEBVTT") or ln.strip().startswith("NOTE") or ln.strip().startswith("Kind:") or ln.strip().startswith("Language:"):
            continue
        if "-->" in ln:
            if buf:
                idx += 1
                out.append(str(idx))
                out.extend(buf)
                out.append("")
                buf = []
            ts = ln.replace(".", ",")
            buf.append(ts)
            started = True
            continue
        if started:
            buf.append(ln)
    if buf:
        idx += 1
        out.append(str(idx))
        out.extend(buf)
        out.append("")
    return "\n".join(out)


def _json3_to_srt(payload: str) -> str:
    import json
    data = json.loads(payload)
    events = data.get("events") or []
    out = []
    idx = 0
    for ev in events:
        segs = ev.get("segs") or []
        text = "".join((s.get("utf8") or "") for s in segs).strip()
        if not text:
            continue
        start = int(ev.get("tStartMs", 0))
        dur = int(ev.get("dDurationMs", 2000))
        end = start + dur
        idx += 1
        out.append(str(idx))
        out.append(f"{_ms_to_ts(start)} --> {_ms_to_ts(end)}")
        out.append(text)
        out.append("")
    return "\n".join(out)


def _ms_to_ts(ms: int) -> str:
    h = ms // 3600000
    m = (ms % 3600000) // 60000
    s = (ms % 60000) // 1000
    ms2 = ms % 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms2:03d}"


async def extract_subtitles(url: str, lang: str = "zh-Hans") -> tuple[str, str] | None:
    return await asyncio.to_thread(_extract_subs_sync, url, lang)


__all__ = ["extract_info", "stream_download", "extract_subtitles", "DownloadError"]
