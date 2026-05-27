<script setup lang="ts">
import { computed } from "vue";
import type { FormatItem, VideoInfo } from "../api";
import { downloadUrl } from "../api";

const props = defineProps<{ info: VideoInfo }>();

function fmtSize(n?: number) {
  if (!n) return "—";
  const units = ["B", "KB", "MB", "GB"];
  let v = n;
  let i = 0;
  while (v >= 1024 && i < units.length - 1) {
    v /= 1024;
    i++;
  }
  return `${v.toFixed(v < 10 && i > 0 ? 1 : 0)} ${units[i]}`;
}

const videoFormats = computed(() => {
  const items = props.info.formats.filter((f) => f.kind === "video" || f.kind === "video_only");
  const seen = new Set<string>();
  const uniq: FormatItem[] = [];
  for (const f of items) {
    const key = `${f.resolution || f.format_note}-${f.ext}-${f.vcodec}`;
    if (seen.has(key)) continue;
    seen.add(key);
    uniq.push(f);
  }
  return uniq.sort((a, b) => {
    const ah = parseInt((a.resolution || "0").split("x").pop() || "0", 10);
    const bh = parseInt((b.resolution || "0").split("x").pop() || "0", 10);
    return bh - ah;
  });
});

const audioFormats = computed(() =>
  props.info.formats
    .filter((f) => f.kind === "audio")
    .sort((a, b) => (b.abr || 0) - (a.abr || 0))
    .slice(0, 5),
);

const recommended = computed(() => videoFormats.value.find((f) => f.kind === "video") || videoFormats.value[0]);

function label(f: FormatItem) {
  const reso = f.resolution || f.format_note || "";
  const fps = f.fps && f.fps >= 50 ? `${Math.round(f.fps)}fps` : "";
  return [reso, fps].filter(Boolean).join(" · ");
}
</script>

<template>
  <div class="surface p-5 sm:p-6">
    <div class="flex items-center justify-between">
      <h3 class="text-base font-semibold text-slate-900 flex items-center gap-2">
        <svg viewBox="0 0 24 24" class="h-5 w-5 text-brand-600" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        下载选项
      </h3>
      <span class="text-xs text-slate-400">{{ info.formats.length }} 个格式</span>
    </div>

    <div class="mt-4 space-y-2">
      <div
        v-for="f in videoFormats"
        :key="f.format_id"
        class="group flex items-center gap-3 rounded-xl border border-slate-200 px-3 py-2.5 hover:border-brand-400 hover:bg-brand-50/40 transition-colors"
        :class="recommended && f.format_id === recommended.format_id ? 'border-brand-400 bg-brand-50/40' : ''"
      >
        <span
          v-if="recommended && f.format_id === recommended.format_id"
          class="hidden sm:inline-flex items-center rounded-md bg-cta-gradient px-2 py-0.5 text-[10px] font-semibold text-white"
        >推荐</span>
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 text-sm font-medium text-slate-900">
            <span>{{ label(f) || f.format_id }}</span>
            <span class="text-[11px] text-slate-500 uppercase">{{ f.ext }}</span>
            <span v-if="f.kind === 'video_only'" class="text-[10px] rounded bg-amber-100 text-amber-700 px-1.5 py-0.5">无音轨</span>
          </div>
          <div class="text-xs text-slate-500 truncate">
            {{ f.vcodec || "" }} <span v-if="f.acodec && f.acodec !== 'none'">· {{ f.acodec }}</span>
            <span v-if="f.filesize || f.filesize_approx"> · {{ fmtSize(f.filesize || f.filesize_approx) }}</span>
          </div>
        </div>
        <a
          :href="downloadUrl(info.url, f.format_id)"
          download
          class="inline-flex items-center gap-1.5 rounded-lg bg-cta-gradient px-3 py-2 text-sm font-semibold text-white shadow-cta hover:brightness-105 cursor-pointer transition-all"
        >
          <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          下载
        </a>
      </div>
      <p v-if="!videoFormats.length" class="text-sm text-slate-500">未发现可用的视频格式。</p>
    </div>

    <div v-if="audioFormats.length" class="mt-6">
      <h4 class="text-sm font-semibold text-slate-700 flex items-center gap-2">
        <svg viewBox="0 0 24 24" class="h-4 w-4 text-slate-500" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>
        仅音频
      </h4>
      <div class="mt-2 space-y-2">
        <div
          v-for="f in audioFormats"
          :key="f.format_id"
          class="flex items-center gap-3 rounded-xl border border-slate-200 px-3 py-2.5 hover:border-brand-400 transition-colors"
        >
          <div class="flex-1 min-w-0">
            <div class="text-sm font-medium text-slate-900">{{ f.abr ? `${Math.round(f.abr)} kbps` : f.format_id }} <span class="text-[11px] text-slate-500 uppercase ml-1">{{ f.ext }}</span></div>
            <div class="text-xs text-slate-500">{{ f.acodec || "" }} <span v-if="f.filesize || f.filesize_approx">· {{ fmtSize(f.filesize || f.filesize_approx) }}</span></div>
          </div>
          <a :href="downloadUrl(info.url, f.format_id)" download class="btn-ghost text-xs py-1.5 px-3">
            下载
          </a>
        </div>
      </div>
    </div>
  </div>
</template>
