<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { fetchInfo, readableError, type VideoInfo } from "../api";
import FormatPicker from "../components/FormatPicker.vue";
import AIPanel from "../components/AIPanel.vue";

const route = useRoute();
const router = useRouter();

const info = ref<VideoInfo | null>(null);
const loading = ref(true);
const error = ref("");

const url = computed(() => String(route.query.url || ""));

async function load() {
  if (!url.value) {
    error.value = "缺少 url 参数";
    return;
  }
  loading.value = true;
  error.value = "";
  info.value = null;
  try {
    info.value = await fetchInfo(url.value);
  } catch (e) {
    error.value = readableError(e);
  } finally {
    loading.value = false;
  }
}

function durFmt(sec?: number) {
  if (!sec) return "";
  const s = Math.floor(sec);
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const ss = s % 60;
  return h > 0 ? `${h}:${String(m).padStart(2, "0")}:${String(ss).padStart(2, "0")}` : `${m}:${String(ss).padStart(2, "0")}`;
}

onMounted(load);
watch(() => route.query.url, load);
</script>

<template>
  <div class="container-page py-8 sm:py-12">
    <button
      class="inline-flex items-center gap-1.5 text-sm text-slate-600 hover:text-brand-700 cursor-pointer mb-4 transition-colors"
      @click="router.push('/')"
    >
      <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
      返回首页
    </button>

    <div v-if="loading" class="space-y-4">
      <div class="flex items-center gap-2 text-sm text-slate-600">
        <svg class="h-4 w-4 animate-spin text-brand-600" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-opacity="0.25" stroke-width="3"/><path d="M22 12a10 10 0 0 1-10 10" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>
        正在解析视频信息，通常 5-30 秒，请稍候…
      </div>
      <div class="grid gap-6 lg:grid-cols-[2fr_1fr]">
      <div class="surface p-6 flex gap-4">
        <div class="h-32 w-56 rounded-xl bg-slate-100 animate-pulse"></div>
        <div class="flex-1 space-y-3 py-2">
          <div class="h-5 w-3/4 rounded bg-slate-100 animate-pulse"></div>
          <div class="h-3 w-1/2 rounded bg-slate-100 animate-pulse"></div>
          <div class="h-3 w-2/3 rounded bg-slate-100 animate-pulse"></div>
          <div class="h-3 w-1/3 rounded bg-slate-100 animate-pulse"></div>
        </div>
      </div>
      <div class="surface p-6 space-y-3">
        <div class="h-4 w-1/3 rounded bg-slate-100 animate-pulse"></div>
        <div class="h-10 rounded bg-slate-100 animate-pulse"></div>
        <div class="h-10 rounded bg-slate-100 animate-pulse"></div>
        <div class="h-10 rounded bg-slate-100 animate-pulse"></div>
      </div>
      </div>
    </div>

    <div v-else-if="error" class="surface p-8 text-center">
      <div class="mx-auto grid h-14 w-14 place-items-center rounded-full bg-rose-50 text-rose-500">
        <svg viewBox="0 0 24 24" class="h-7 w-7" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
      </div>
      <h3 class="mt-4 text-lg font-semibold text-slate-900">解析失败</h3>
      <p class="mt-1 text-sm text-slate-600 break-all">{{ error }}</p>
      <div class="mt-5 flex justify-center gap-2">
        <button class="btn-ghost" @click="load">重试</button>
        <button class="btn-brand" @click="router.push('/')">返回首页</button>
      </div>
    </div>

    <div v-else-if="info" class="space-y-6">
      <div class="surface p-5 sm:p-6">
        <div class="flex flex-col sm:flex-row gap-5">
          <div class="shrink-0">
            <img
              v-if="info.thumbnail"
              :src="info.thumbnail"
              :alt="info.title"
              class="w-full sm:w-64 aspect-video rounded-xl object-cover bg-slate-100"
              loading="lazy"
            />
            <div v-else class="w-full sm:w-64 aspect-video rounded-xl bg-slate-100 grid place-items-center text-slate-400">无封面</div>
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="chip border-brand-200 bg-brand-50 text-brand-700">{{ info.extractor }}</span>
              <span v-if="info.duration" class="chip">
                <svg viewBox="0 0 24 24" class="h-3 w-3" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                {{ durFmt(info.duration) }}
              </span>
              <span v-if="info.subtitles.length" class="chip">字幕: {{ info.subtitles.slice(0, 3).join(", ") }}{{ info.subtitles.length > 3 ? "…" : "" }}</span>
            </div>
            <h2 class="mt-3 text-xl sm:text-2xl font-bold text-slate-900 leading-snug break-words">{{ info.title }}</h2>
            <p v-if="info.uploader" class="mt-1.5 text-sm text-slate-600">
              <svg viewBox="0 0 24 24" class="inline h-4 w-4 mr-1 text-slate-400" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              {{ info.uploader }}
            </p>
            <p v-if="info.description" class="mt-3 text-sm text-slate-600 line-clamp-3 leading-relaxed">{{ info.description }}</p>
            <a
              :href="info.url"
              target="_blank"
              rel="noreferrer"
              class="mt-3 inline-flex items-center gap-1.5 text-xs text-slate-500 hover:text-brand-700 cursor-pointer transition-colors break-all"
            >
              <svg viewBox="0 0 24 24" class="h-3.5 w-3.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
              查看原页面
            </a>
          </div>
        </div>
      </div>

      <div class="grid gap-6 lg:grid-cols-2">
        <FormatPicker :info="info" />
        <AIPanel :url="info.url" />
      </div>
    </div>
  </div>
</template>
