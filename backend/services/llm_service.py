from __future__ import annotations

import re
from typing import Iterable

from openai import OpenAI

from config import settings


def _client() -> OpenAI:
    return OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)


def _chat(messages: list[dict], max_tokens: int = 1500) -> tuple[str, int]:
    client = _client()
    resp = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        temperature=0.3,
        max_tokens=max_tokens,
    )
    text = resp.choices[0].message.content or ""
    usage = getattr(resp, "usage", None)
    return text, (usage.total_tokens if usage else 0)


_SRT_BLOCK = re.compile(r"(\d+)\s*\n([\d:,]+\s*-->\s*[\d:,]+)\s*\n((?:.+\n?)+?)(?=\n\d+\s*\n|\Z)", re.MULTILINE)


def parse_srt(srt: str) -> list[tuple[str, str, str]]:
    out = []
    for m in _SRT_BLOCK.finditer(srt.strip() + "\n\n"):
        idx, ts, text = m.group(1), m.group(2), m.group(3).strip()
        out.append((idx, ts, text))
    return out


def srt_to_plain_with_ts(srt: str) -> str:
    blocks = parse_srt(srt)
    lines = []
    for _, ts, text in blocks:
        start = ts.split("-->")[0].strip().split(",")[0]
        h, m, s = start.split(":")
        lines.append(f"[{h}:{m}:{s}] {text}")
    return "\n".join(lines)


def _chunks(items: list, size: int) -> Iterable[list]:
    for i in range(0, len(items), size):
        yield items[i : i + size]


def summarize_video(title: str, srt: str) -> tuple[str, int]:
    plain = srt_to_plain_with_ts(srt)
    if len(plain) <= 12000:
        msgs = [
            {"role": "system", "content": "你是一名专业的中文视频总结助手，输出 Markdown。"},
            {"role": "user", "content": f"视频标题：{title}\n\n字幕（含时间戳）：\n{plain}\n\n请输出：\n## 一句话总结\n## 核心要点（5-8 条 bullet）\n## 时间线（HH:MM 关键节点 + 简要描述）"},
        ]
        return _chat(msgs, max_tokens=1500)

    lines = plain.splitlines()
    partials = []
    total_tokens = 0
    for batch in _chunks(lines, 200):
        msgs = [
            {"role": "system", "content": "你是视频字幕摘要助手，输出中文要点列表，每条带时间戳。"},
            {"role": "user", "content": "对下面这一段字幕做要点提取（带时间戳）：\n" + "\n".join(batch)},
        ]
        text, used = _chat(msgs, max_tokens=600)
        partials.append(text)
        total_tokens += used
    merged = "\n\n".join(partials)
    final_msgs = [
        {"role": "system", "content": "你是中文视频总结助手，输出 Markdown。"},
        {"role": "user", "content": f"视频标题：{title}\n\n以下是分段要点，请合并去重并输出最终总结：\n\n{merged}\n\n格式：\n## 一句话总结\n## 核心要点\n## 时间线"},
    ]
    text, used = _chat(final_msgs, max_tokens=1500)
    return text, total_tokens + used


_TS_LINE = re.compile(r"^\d+\s*$|-->", re.MULTILINE)


def translate_srt(srt: str, target_lang: str) -> tuple[str, int]:
    blocks = parse_srt(srt)
    if not blocks:
        raise ValueError("INVALID_SRT")

    out_blocks: list[str] = []
    total_tokens = 0
    batch_size = 40
    for batch in _chunks(blocks, batch_size):
        payload = "\n".join(f"[{i}] {text}" for i, (_, _, text) in enumerate(batch))
        msgs = [
            {"role": "system", "content": f"你是字幕翻译助手。把每一行翻译为 {target_lang}，保持序号格式 [N] 翻译文本，每行一条，不要合并、不要拆分、不要解释。"},
            {"role": "user", "content": payload},
        ]
        text, used = _chat(msgs, max_tokens=1200)
        total_tokens += used

        mapping: dict[int, str] = {}
        for ln in text.splitlines():
            m = re.match(r"^\s*\[(\d+)\]\s*(.+)$", ln)
            if m:
                mapping[int(m.group(1))] = m.group(2).strip()

        for i, (idx, ts, original) in enumerate(batch):
            translated = mapping.get(i, original)
            out_blocks.append(f"{idx}\n{ts}\n{translated}\n")

    return "\n".join(out_blocks), total_tokens
