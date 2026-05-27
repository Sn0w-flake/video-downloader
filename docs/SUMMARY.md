# 项目总结

> 视频下载核心功能已完成（2026-05）。本文档记录架构、关键决策与排障结论，便于后续维护。

## 概览

VidGrab：万能视频下载站。粘贴链接即下，支持 1000+ 平台高清无水印，并集成 AI 视频总结与字幕翻译。

技术栈：FastAPI + Vue3 + Vite + Tailwind + yt-dlp + f2 + OpenAI 兼容 API。

## 架构

```
┌─────────────┐   /api/info        ┌──────────────┐
│  Frontend   │ ─────────────────▶ │   FastAPI    │
│ (Vue3+Vite) │   /api/download    │   Routers    │
│             │ ─────────────────▶ │              │
│  Home /     │   /api/subtitles   │              │
│  Result /   │ ─────────────────▶ │              │
│  Pricing    │   /api/ai/*        │              │
└─────────────┘ ─────────────────▶ └──────┬───────┘
                                          │
                            ┌─────────────┼─────────────┐
                            │             │             │
                       is_douyin?    yt-dlp        LLM (OpenAI)
                            │             │             │
                       ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
                       │   f2    │   │ ytdlp_  │   │  llm_   │
                       │ douyin_ │   │ service │   │ service │
                       │ service │   │         │   │         │
                       └─────────┘   └─────────┘   └─────────┘
```

请求按平台分发：抖音走 `f2`（无 Cookie 解析），其他走 `yt-dlp`，统一返回 `VideoInfo` schema。

## 关键决策

| 问题 | 选型 | 理由 |
|---|---|---|
| 视频解析引擎 | yt-dlp | 19w star，覆盖 1000+ 平台 |
| 抖音解析 | f2 (Apache 2.0) | 内置 `a_bogus`/`ttwid`/`s_v_web_id` 签名，无需用户 Cookie |
| 多平台分发 | 路由层 `_pick(url)` | 简单、零迁移成本 |
| 长耗时反馈 | Result 首帧 loading + 文案 | 不引入 SSE/WS，零后端改动 |
| AI 总结 | 基于字幕 → LLM | 抖音无字幕轨，前端直接禁用 AI tab |

## 关键问题与修复

1. **解析无反馈**：路由懒加载 + `out-in` 过渡导致点击后白屏。修复：Result 改为直接 import + 去掉过渡 + 首帧 `loading=true` + 骨架文案。
2. **抖音 Unsupported URL**：yt-dlp 需要 Cookie。引入 f2，路由层按域名分发。
3. **f2 schema 映射**：`_to_dict()` 返回扁平 properties 而非嵌套 JSON。改用 `_to_raw().aweme_detail.*` 直读原始字段。
4. **f2 空响应**：默认空 Cookie 抖音返回空。补 `TokenManager.gen_ttwid() / gen_false_msToken()` + `VerifyFpManager.gen_s_v_web_id()` 拼装访客 Cookie。
5. **AI 总结失败**：抖音无字幕。前端按 URL 检测并隐藏 AI tab，提示「该平台暂不支持」。

## 目录结构

```
video-downloader/
├── backend/
│   ├── main.py                # FastAPI 入口
│   ├── config.py              # OPENAI_* / CORS 配置
│   ├── schemas.py             # 统一响应模型
│   ├── routers/
│   │   ├── video.py           # /api/info /download /batch /subtitles
│   │   └── ai.py              # /api/ai/summarize /translate
│   └── services/
│       ├── ytdlp_service.py   # yt-dlp 解析 + 流式下载 + 字幕
│       ├── douyin_service.py  # f2 抖音解析
│       └── llm_service.py     # LLM 总结 + 字幕翻译
├── frontend/
│   └── src/
│       ├── views/             # Home / Result / Pricing
│       ├── components/        # HeroInput / FormatPicker / AIPanel / BatchModal
│       └── api.ts             # axios 封装
└── docs/                      # 本文档
```

## 启动

后端：
```powershell
cd backend
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload --port 8000
```

前端：
```powershell
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173 。

## 平台支持

- **yt-dlp 路径**：YouTube / Bilibili / TikTok / X / Instagram / Twitch / 微博 / Vimeo / Reddit 等
- **f2 路径**：抖音（含 `v.douyin.com` 短链、`/video/` 长链、`/jingxuan?modal_id=` 推荐流）

## 已知限制

- 抖音不支持 AI 总结 / 字幕翻译（无原生字幕轨）
- f2 / yt-dlp 依赖平台接口，对方变更需同步升级 (`pip install -U f2 yt-dlp`)
- 单实例无任务队列，长视频解析会占用 worker
- 没有用户系统 / 鉴权 / 限速

## 功能完成清单

| 模块 | 状态 | 说明 |
|------|------|------|
| 首页粘贴解析 | 完成 | HeroInput → Result，骨架屏 + 耗时提示 |
| 视频信息解析 | 完成 | `/api/info`，yt-dlp + 抖音 f2 双引擎 |
| 多清晰度下载 | 完成 | `/api/download` 流式代理，FormatPicker 选格式 |
| 批量解析 | 完成 | `/api/batch`，最多 5 路并发 |
| 字幕导出 | 完成 | `/api/subtitles` → SRT（yt-dlp 平台） |
| AI 视频总结 | 完成 | `/api/ai/summarize`（需字幕 + LLM Key） |
| AI 字幕翻译 | 完成 | `/api/ai/translate` |
| 抖音下载 | 完成 | f2 无 Cookie，多码率直链 |
| 抖音 AI | 禁用 | 前端提示，无字幕轨 |
| 定价页 / 响应式 | 完成 | Pricing + Tailwind 移动端适配 |

## 后续可改进

- 抖音 AI 总结：接 Whisper API 做 ASR（需 ffmpeg + ≤25MB 限制处理）
- 增加快手 / 小红书 / 微信视频号
- SSE 推送解析进度
- Redis 缓存已解析 URL，避免重复请求
- Docker Compose 一键部署
