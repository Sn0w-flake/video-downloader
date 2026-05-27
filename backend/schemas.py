from typing import Literal, Optional
from pydantic import BaseModel, Field


class FormatItem(BaseModel):
    format_id: str
    ext: Optional[str] = None
    resolution: Optional[str] = None
    fps: Optional[float] = None
    filesize: Optional[int] = None
    filesize_approx: Optional[int] = None
    vcodec: Optional[str] = None
    acodec: Optional[str] = None
    format_note: Optional[str] = None
    tbr: Optional[float] = None
    abr: Optional[float] = None
    kind: Literal["video", "audio", "video_only", "unknown"] = "unknown"


class VideoInfo(BaseModel):
    url: str
    title: str
    uploader: Optional[str] = None
    thumbnail: Optional[str] = None
    duration: Optional[float] = None
    extractor: Optional[str] = None
    description: Optional[str] = None
    formats: list[FormatItem] = Field(default_factory=list)
    subtitles: list[str] = Field(default_factory=list)


class BatchRequest(BaseModel):
    urls: list[str]


class BatchItem(BaseModel):
    url: str
    ok: bool
    info: Optional[VideoInfo] = None
    error: Optional[str] = None


class BatchResponse(BaseModel):
    results: list[BatchItem]


class SubtitleResponse(BaseModel):
    lang: str
    format: str = "srt"
    content: str


class SummarizeRequest(BaseModel):
    url: str
    lang: str = "zh-Hans"


class SummarizeResponse(BaseModel):
    title: str
    summary: str
    tokens_used: int = 0


class TranslateRequest(BaseModel):
    srt: str
    target_lang: str = "zh-Hans"


class TranslateResponse(BaseModel):
    target_lang: str
    srt: str
    tokens_used: int = 0
