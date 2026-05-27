<script setup lang="ts">
import { computed, ref } from "vue";
import { marked } from "marked";
import { fetchSubtitles, summarize, translate, readableError } from "../api";

const props = defineProps<{ url: string }>();
const isDouyin = computed(() => /douyin\.com|iesdouyin\.com/i.test(props.url));

type Tab = "summary" | "translate";
const tab = ref<Tab>("summary");

const summary = ref<string>("");
const summaryLoading = ref(false);
const summaryError = ref("");

const srtRaw = ref("");
const srtLang = ref("");
const translateLang = ref("zh-Hans");
const translateLoading = ref(false);
const translateError = ref("");
const translatedSrt = ref("");

async function runSummary() {
  summaryLoading.value = true;
  summaryError.value = "";
  summary.value = "";
  try {
    const data = await summarize(props.url);
    summary.value = data.summary;
  } catch (e) {
    summaryError.value = readableError(e);
  } finally {
    summaryLoading.value = false;
  }
}

async function loadSubtitles() {
  translateError.value = "";
  try {
    const data = await fetchSubtitles(props.url);
    srtRaw.value = data.content;
    srtLang.value = data.lang;
  } catch (e) {
    translateError.value = readableError(e);
    srtRaw.value = "";
  }
}

async function runTranslate() {
  if (!srtRaw.value) await loadSubtitles();
  if (!srtRaw.value) return;
  translateLoading.value = true;
  translateError.value = "";
  translatedSrt.value = "";
  try {
    const data = await translate(srtRaw.value, translateLang.value);
    translatedSrt.value = data.srt;
  } catch (e) {
    translateError.value = readableError(e);
  } finally {
    translateLoading.value = false;
  }
}

function saveText(filename: string, text: string) {
  const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

const summaryHtml = (md: string) => marked.parse(md, { breaks: true }) as string;
</script>

<template>
  <div class="surface p-5 sm:p-6">
    <div class="flex items-center justify-between gap-3">
      <h3 class="text-base font-semibold text-slate-900 flex items-center gap-2">
        <span class="grid h-7 w-7 place-items-center rounded-lg bg-brand-gradient text-white">
          <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l2.39 4.84L20 8l-4 3.9.94 5.49L12 14.77 7.06 17.39 8 11.9 4 8l5.61-1.16L12 2z"/></svg>
        </span>
        AI 工具
        <span class="pro-pill">Pro</span>
      </h3>
      <div v-if="!isDouyin" class="inline-flex rounded-lg border border-slate-200 bg-white p-0.5">
        <button
          class="rounded-md px-3 py-1.5 text-sm font-medium cursor-pointer transition-colors"
          :class="tab === 'summary' ? 'bg-brand-gradient text-white shadow-[0_4px_14px_-6px_rgba(124,58,237,0.5)]' : 'text-slate-600 hover:text-slate-900'"
          @click="tab = 'summary'"
        >视频总结</button>
        <button
          class="rounded-md px-3 py-1.5 text-sm font-medium cursor-pointer transition-colors"
          :class="tab === 'translate' ? 'bg-brand-gradient text-white shadow-[0_4px_14px_-6px_rgba(124,58,237,0.5)]' : 'text-slate-600 hover:text-slate-900'"
          @click="tab = 'translate'"
        >字幕翻译</button>
      </div>
    </div>

    <div v-if="isDouyin" class="mt-3 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
      抖音视频无原生字幕轨，暂不支持 AI 总结 / 字幕翻译。
    </div>

    <div v-else-if="tab === 'summary'" class="mt-4">
      <p class="text-sm text-slate-600">基于视频字幕自动生成中文要点 + 时间线。需要服务端已配置 OpenAI 兼容的 API。</p>
      <button class="btn-brand mt-3" :disabled="summaryLoading" @click="runSummary">
        <svg class="h-4 w-4" :class="summaryLoading ? 'animate-spin' : ''" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <template v-if="!summaryLoading"><path d="M21 12a9 9 0 1 1-6.22-8.56"/><polyline points="22 4 12 14.01 9 11.01"/></template>
          <template v-else><circle cx="12" cy="12" r="10" stroke-opacity="0.3"/><path d="M22 12a10 10 0 0 1-10 10"/></template>
        </svg>
        {{ summaryLoading ? "生成中（可能需要 30 秒）" : "生成总结" }}
      </button>

      <div v-if="summaryError" class="mt-3 rounded-xl border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700">
        {{ summaryError === "LLM_NOT_CONFIGURED" ? "服务端未配置 LLM Key，请在 backend/.env 填入 OPENAI_API_KEY 并重启" : summaryError }}
      </div>

      <div v-if="summary" class="prose-tight mt-4 max-h-[400px] overflow-auto scrollbar-thin" v-html="summaryHtml(summary)" />
      <div v-else-if="summaryLoading" class="mt-4 space-y-2">
        <div class="h-3 rounded bg-slate-100 animate-pulse"></div>
        <div class="h-3 rounded bg-slate-100 animate-pulse w-11/12"></div>
        <div class="h-3 rounded bg-slate-100 animate-pulse w-10/12"></div>
        <div class="h-3 rounded bg-slate-100 animate-pulse w-9/12"></div>
      </div>
    </div>

    <div v-else class="mt-4">
      <p class="text-sm text-slate-600">提取视频原生字幕并翻译到目标语言，保留时间戳，可下载译文 SRT。</p>
      <div class="mt-3 flex flex-wrap items-center gap-2">
        <label class="text-sm text-slate-600">目标语言</label>
        <select v-model="translateLang" class="rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-sm focus:border-brand-400 focus:outline-none cursor-pointer">
          <option value="zh-Hans">简体中文</option>
          <option value="zh-Hant">繁体中文</option>
          <option value="en">English</option>
          <option value="ja">日本語</option>
          <option value="ko">한국어</option>
          <option value="es">Español</option>
        </select>
        <button class="btn-brand" :disabled="translateLoading" @click="runTranslate">
          <svg class="h-4 w-4" :class="translateLoading ? 'animate-spin' : ''" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <template v-if="!translateLoading"><path d="M5 8l6 6"/><path d="M4 14l6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="M22 22l-5-10-5 10"/><path d="M14 18h6"/></template>
            <template v-else><circle cx="12" cy="12" r="10" stroke-opacity="0.3"/><path d="M22 12a10 10 0 0 1-10 10"/></template>
          </svg>
          {{ translateLoading ? "翻译中" : "提取并翻译" }}
        </button>
        <button v-if="translatedSrt" class="btn-ghost" @click="saveText(`subtitle.${translateLang}.srt`, translatedSrt)">
          <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          下载 SRT
        </button>
      </div>
      <div v-if="translateError" class="mt-3 rounded-xl border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700">
        {{ translateError === "LLM_NOT_CONFIGURED" ? "服务端未配置 LLM Key" : (translateError === "SUBTITLE_NOT_FOUND" ? "该视频未提供字幕（原生 + 自动均未找到）" : translateError) }}
      </div>
      <div v-if="srtRaw || translatedSrt" class="mt-4 grid gap-3 md:grid-cols-2">
        <div>
          <div class="text-xs text-slate-500 mb-1">原文 ({{ srtLang || "?" }})</div>
          <pre class="max-h-[360px] overflow-auto scrollbar-thin rounded-xl border border-slate-200 bg-slate-50 p-3 text-xs leading-relaxed whitespace-pre-wrap">{{ srtRaw || "—" }}</pre>
        </div>
        <div>
          <div class="text-xs text-slate-500 mb-1">译文 ({{ translateLang }})</div>
          <pre class="max-h-[360px] overflow-auto scrollbar-thin rounded-xl border border-slate-200 bg-slate-50 p-3 text-xs leading-relaxed whitespace-pre-wrap">{{ translatedSrt || (translateLoading ? "翻译中…" : "—") }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>
