# Universal Video Downloader (VidGrab)

基于 yt-dlp 的万能视频下载站。FastAPI + Vue3 + Vite + Tailwind，附 AI 视频总结与字幕翻译（OpenAI 兼容）。

详细文档：[docs/](./docs)。项目总结：[docs/SUMMARY.md](./docs/SUMMARY.md)。

## 启动

需要 Python 3.10+ 与 Node 18+。

### 后端

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# 编辑 .env：可留空跳过 AI；填好 OPENAI_API_KEY / BASE_URL / MODEL 即启用
uvicorn main:app --reload --port 8000
```

### 前端

```powershell
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173 。后端开发自动通过 vite 代理到 http://127.0.0.1:8000 。

## 自验清单

- [ ] http://127.0.0.1:8000/api/health 返回 `{"ok": true, ...}`
- [ ] http://localhost:5173 打开首页，Hero / 平台卡片 / 特性卡片 / CTA 渲染正常
- [ ] 粘贴 YouTube 链接 → 跳 Result → 选 1080p 下载到本地播放正常
- [ ] 粘贴 Bilibili 链接 → 解析 → 拿到中文字幕导出 SRT
- [ ] 批量弹窗：3 个 URL 并发返回，逐条下载
- [ ] 配 LLM key 后，AI 总结返回中文要点；未配置时友好提示
- [ ] 移动端模拟器 375px 宽，无横向滚动条
