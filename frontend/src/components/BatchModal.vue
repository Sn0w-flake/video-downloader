<script setup lang="ts">
import { ref, watch } from "vue";
import { fetchBatch, downloadUrl, readableError, type BatchItem } from "../api";

const props = defineProps<{ open: boolean }>();
const emit = defineEmits<{ (e: "close"): void }>();

const text = ref("");
const loading = ref(false);
const results = ref<BatchItem[]>([]);
const error = ref("");

watch(
  () => props.open,
  (v) => {
    if (!v) {
      text.value = "";
      results.value = [];
      error.value = "";
    }
  },
);

async function go() {
  const urls = text.value
    .split(/\s+|\n+/)
    .map((s) => s.trim())
    .filter((s) => /^https?:\/\//i.test(s));
  if (urls.length === 0) {
    error.value = "请粘贴至少一个 http(s) 链接，按换行或空格分隔";
    return;
  }
  loading.value = true;
  error.value = "";
  try {
    results.value = await fetchBatch(urls);
  } catch (e) {
    error.value = readableError(e);
  } finally {
    loading.value = false;
  }
}

function pickBest(item: BatchItem): { id: string; label: string } | null {
  if (!item.info) return null;
  const f = item.info.formats.find((x) => x.kind === "video") || item.info.formats[0];
  if (!f) return null;
  return { id: f.format_id, label: `${f.resolution || f.format_note || ""} ${f.ext || ""}`.trim() };
}
</script>

<template>
  <transition name="modal">
    <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" @click="emit('close')" />
      <div class="surface relative w-full max-w-2xl max-h-[85vh] flex flex-col overflow-hidden">
        <div class="flex items-center justify-between border-b border-slate-200 px-5 py-3.5">
          <h3 class="text-base font-semibold flex items-center gap-2">
            <svg viewBox="0 0 24 24" class="h-5 w-5 text-brand-600" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
            批量下载
          </h3>
          <button class="rounded-lg p-1.5 text-slate-400 hover:text-slate-900 cursor-pointer" @click="emit('close')" aria-label="关闭">
            <svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
          </button>
        </div>
        <div class="p-5 overflow-auto scrollbar-thin">
          <p class="text-sm text-slate-600">每行一条链接，最多并发解析 5 个。解析完成后逐条点击下载。</p>
          <textarea
            v-model="text"
            rows="6"
            class="mt-3 w-full rounded-xl border border-slate-200 bg-white p-3 text-sm focus:border-brand-400 focus:outline-none focus:shadow-cardHover transition-all"
            placeholder="https://www.youtube.com/watch?v=...
https://www.bilibili.com/video/BV...
https://www.tiktok.com/@user/video/..."
          />
          <p v-if="error" class="mt-2 text-xs text-rose-600">{{ error }}</p>

          <div v-if="results.length" class="mt-5 space-y-3">
            <div v-for="r in results" :key="r.url" class="rounded-xl border border-slate-200 p-3 flex items-center gap-3">
              <template v-if="r.ok && r.info">
                <img v-if="r.info.thumbnail" :src="r.info.thumbnail" :alt="r.info.title" class="h-16 w-28 rounded-lg object-cover bg-slate-100" />
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-slate-900 truncate">{{ r.info.title }}</p>
                  <p class="text-xs text-slate-500 truncate">{{ r.info.uploader || r.info.extractor }}</p>
                </div>
                <a
                  v-if="pickBest(r)"
                  :href="downloadUrl(r.url, pickBest(r)!.id)"
                  class="btn-primary text-sm py-2 px-3 shrink-0"
                  download
                >
                  下载 {{ pickBest(r)!.label }}
                </a>
              </template>
              <template v-else>
                <div class="grid h-16 w-28 place-items-center rounded-lg bg-rose-50 text-rose-500 shrink-0">
                  <svg viewBox="0 0 24 24" class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-slate-900 truncate">{{ r.url }}</p>
                  <p class="text-xs text-rose-600 truncate">{{ r.error }}</p>
                </div>
              </template>
            </div>
          </div>
        </div>
        <div class="border-t border-slate-200 px-5 py-3 flex justify-end gap-2 bg-slate-50/50">
          <button class="btn-ghost" @click="emit('close')">关闭</button>
          <button class="btn-primary text-sm" :disabled="loading" @click="go">
            <span v-if="!loading">解析全部</span>
            <span v-else class="flex items-center gap-1.5">
              <svg class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-opacity="0.25" stroke-width="3"/><path d="M22 12a10 10 0 0 1-10 10" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>
              解析中
            </span>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.modal-enter-active, .modal-leave-active { transition: opacity 200ms ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
