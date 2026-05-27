# API 设计说明

> 后端 FastAPI · 阶段 3 接口契约

Base URL（dev）：`http://127.0.0.1:8000`
统一前缀：`/api`
错误响应格式：`{ "detail": "<msg>", "code": "<MACHINE_CODE>" }`

## 1. 视频解析与下载

### 1.1 `GET /api/info`

解析单个 URL，返回视频元信息和可下载格式列表。

**Query**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `url` | string | ✅ | 视频链接 |

**Response 200**

```json
{
  "url": "https://...",
  "title": "...",
  "uploader": "...",
  "thumbnail": "https://...",
  "duration": 612,
  "extractor": "youtube",
  "description": "...",
  "formats": [
    {
      "format_id": "137+140",
      "ext": "mp4",
      "resolution": "1920x1080",
      "fps": 30,
      "filesize": 84211200,
      "vcodec": "avc1",
      "acodec": "mp4a",
      "format_note": "1080p",
      "kind": "video"
    },
    { "format_id": "140", "ext": "m4a", "filesize": 5242880, "vcodec": "none", "acodec": "mp4a", "kind": "audio" }
  ],
  "subtitles": ["zh-Hans", "en"]
}
```

**Error**

- 422 `INVALID_URL` / `UNSUPPORTED_SITE`
- 500 `EXTRACT_FAILED`

### 1.2 `GET /api/download`

下载指定格式，`StreamingResponse` 直推浏览器。

**Query**

| 参数 | 必填 | 说明 |
|---|---|---|
| `url` | ✅ | 视频链接 |
| `format_id` | ✅ | `/api/info` 中的 `format_id` |
| `filename` | ❌ | 自定义文件名（默认用 title） |

**Response**：二进制流，`Content-Disposition: attachment; filename="..."`，`Content-Type` 按 ext 自动设置。

### 1.3 `POST /api/batch`

批量解析。下载仍由前端逐条调 `/api/download`。

**Body**

```json
{ "urls": ["https://...", "https://..."] }
```

**Response 200**

```json
{
  "results": [
    { "url": "...", "ok": true, "info": { /* 同 /api/info */ } },
    { "url": "...", "ok": false, "error": "UNSUPPORTED_SITE" }
  ]
}
```

并发上限：默认 5（避免被平台限速）。

### 1.4 `GET /api/subtitles`

提取字幕，返回 SRT 文本。

**Query**

| 参数 | 必填 | 说明 |
|---|---|---|
| `url` | ✅ | 视频链接 |
| `lang` | ❌ | 默认按 `zh-Hans` → `zh` → `en` 顺序兜底 |
| `auto` | ❌ | 默认 `true`：允许使用自动字幕 |

**Response 200**

```json
{ "lang": "zh-Hans", "format": "srt", "content": "1\n00:00:00,000 --> ..." }
```

**Error**

- 404 `SUBTITLE_NOT_FOUND`

## 2. AI 增值

### 2.1 `POST /api/ai/summarize`

对视频做中文要点 + 时间线总结。

**Body**

```json
{ "url": "https://...", "lang": "zh-Hans" }
```

内部流程：先 `/api/subtitles` 拿字幕 → 字幕分块 → LLM map-reduce → 输出 markdown。

**Response 200**

```json
{
  "title": "...",
  "summary": "## 一句话\n...\n\n## 要点\n- ...\n\n## 时间线\n- 00:01:23 ...",
  "tokens_used": 1234
}
```

**Error**

- 503 `LLM_NOT_CONFIGURED`（未配 OPENAI_API_KEY）
- 404 `SUBTITLE_NOT_FOUND`

### 2.2 `POST /api/ai/translate`

翻译 SRT 字幕，保留时间戳。

**Body**

```json
{ "srt": "1\n00:00:00,000 --> ...", "target_lang": "zh-Hans" }
```

**Response 200**

```json
{ "target_lang": "zh-Hans", "srt": "1\n00:00:00,000 --> ...", "tokens_used": 2345 }
```

**Error**

- 503 `LLM_NOT_CONFIGURED`
- 422 `INVALID_SRT`

## 3. 环境变量（.env）

```ini
# AI（可留空，留空时 /api/ai/* 返回 503）
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat

# 跨域（dev 留空即可，走 vite 代理）
CORS_ALLOW_ORIGINS=*

# 下载限速（可选，bytes/s，0=不限）
DOWNLOAD_RATELIMIT=0
```

## 4. 状态码约定

| Code | 含义 | 何时返回 |
|---|---|---|
| 200 | OK |  |
| 400 | 请求体无法解析 |  |
| 404 | 资源不存在 | 字幕缺失等 |
| 422 | 业务校验失败 | URL 不合法 / SRT 不合法 |
| 503 | 依赖不可用 | LLM 未配置、上游平台 5xx |
| 500 | 内部错误 | yt-dlp 抛异常 |
