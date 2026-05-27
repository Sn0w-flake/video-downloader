<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

const props = defineProps<{ loading?: boolean }>();
const emit = defineEmits<{ (e: "batch"): void }>();
const router = useRouter();
const url = ref("");
const error = ref("");

function go() {
  const v = url.value.trim();
  if (!v) {
    error.value = "请粘贴视频链接";
    return;
  }
  if (!/^https?:\/\//i.test(v)) {
    error.value = "链接需要以 http(s):// 开头";
    return;
  }
  error.value = "";
  router.push({ name: "result", query: { url: v } });
}

async function pasteFromClipboard() {
  try {
    const t = await navigator.clipboard.readText();
    if (t) url.value = t.trim();
  } catch {
    /* ignore */
  }
}

const chips = ["YouTube", "Bilibili", "TikTok", "抖音", "X / Twitter", "Instagram", "Twitch", "微博", "小红书"];
</script>

<template>
  <div class="relative">
    <label for="hero-url" class="sr-only">视频链接</label>
    <div
      class="flex flex-col sm:flex-row items-stretch gap-3 rounded-2xl border border-slate-200 bg-white p-2 shadow-card focus-within:border-brand-400 focus-within:shadow-cardHover transition-all duration-200"
    >
      <div class="flex items-center gap-2 px-3 flex-1">
        <svg viewBox="0 0 24 24" class="h-5 w-5 text-slate-400 shrink-0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
        </svg>
        <input
          id="hero-url"
          v-model="url"
          type="url"
          inputmode="url"
          placeholder="粘贴 YouTube / Bilibili / TikTok 等视频链接…"
          autocomplete="off"
          spellcheck="false"
          class="flex-1 bg-transparent py-3 text-base text-slate-900 placeholder:text-slate-400 focus:outline-none"
          @keyup.enter="go"
        />
        <button
          v-if="!url"
          class="hidden sm:inline-flex items-center gap-1 rounded-lg border border-slate-200 px-2.5 py-1 text-xs text-slate-500 hover:text-slate-900 hover:border-brand-400 cursor-pointer transition-colors"
          type="button"
          @click="pasteFromClipboard"
        >
          <svg viewBox="0 0 24 24" class="h-3.5 w-3.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/></svg>
          粘贴
        </button>
        <button
          v-else
          class="rounded-lg p-1.5 text-slate-400 hover:text-slate-900 cursor-pointer"
          type="button"
          aria-label="清除"
          @click="url = ''"
        >
          <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
        </button>
      </div>
      <button
        class="btn-primary text-base px-6 sm:px-7"
        :disabled="props.loading"
        @click="go"
      >
        <span v-if="!props.loading">立即解析</span>
        <span v-else class="flex items-center gap-2">
          <svg class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-opacity="0.25" stroke-width="3"/><path d="M22 12a10 10 0 0 1-10 10" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>
          解析中
        </span>
        <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M5 12h14M13 6l6 6-6 6"/>
        </svg>
      </button>
    </div>

    <p v-if="error" class="mt-2 ml-2 text-xs text-rose-600">{{ error }}</p>

    <div class="mt-5 flex flex-wrap items-center justify-center gap-2">
      <span class="text-xs text-slate-500 mr-1">支持：</span>
      <span v-for="c in chips" :key="c" class="chip">{{ c }}</span>
      <button
        class="chip border-brand-200 bg-brand-50 text-brand-700 hover:border-brand-400 cursor-pointer transition-colors"
        type="button"
        @click="emit('batch')"
      >
        <svg viewBox="0 0 24 24" class="h-3 w-3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
        批量下载
      </button>
    </div>
  </div>
</template>
