<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";

const scrolled = ref(false);
const router = useRouter();

function onScroll() {
  scrolled.value = window.scrollY > 12;
}
onMounted(() => {
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
});
onBeforeUnmount(() => window.removeEventListener("scroll", onScroll));
</script>

<template>
  <header
    class="sticky top-0 z-40 transition-all duration-200"
    :class="scrolled ? 'backdrop-blur-md bg-white/80 border-b border-slate-200/70' : 'bg-transparent'"
  >
    <div class="container-page flex h-16 items-center justify-between">
      <div class="flex items-center gap-2.5 cursor-pointer" @click="router.push('/')">
        <span class="grid h-9 w-9 place-items-center rounded-xl bg-brand-gradient shadow-[0_8px_24px_-10px_rgba(124,58,237,0.5)]">
          <svg viewBox="0 0 24 24" class="h-5 w-5 text-white" fill="currentColor" aria-hidden="true">
            <path d="M8 5v14l11-7z" />
          </svg>
        </span>
        <span class="text-lg font-bold tracking-tight">
          <span class="text-gradient">VidGrab</span>
          <span class="text-slate-700 font-semibold ml-1 hidden sm:inline">万能视频下载</span>
        </span>
      </div>

      <nav class="hidden md:flex items-center gap-7 text-sm font-medium text-slate-600">
        <router-link to="/" class="hover:text-slate-900 cursor-pointer transition-colors">首页</router-link>
        <a href="/#features" class="hover:text-slate-900 cursor-pointer transition-colors">功能特性</a>
        <a href="/#platforms" class="hover:text-slate-900 cursor-pointer transition-colors">支持平台</a>
        <router-link to="/pricing" class="hover:text-slate-900 cursor-pointer transition-colors">定价</router-link>
      </nav>

      <div class="flex items-center gap-2">
        <a
          href="https://github.com/yt-dlp/yt-dlp"
          target="_blank"
          rel="noreferrer"
          class="hidden sm:inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-900 cursor-pointer"
          aria-label="GitHub"
        >
          <svg viewBox="0 0 24 24" class="h-5 w-5" fill="currentColor"><path d="M12 .5C5.73.5.96 5.27.96 11.54c0 4.86 3.15 8.97 7.52 10.43.55.1.75-.24.75-.53v-1.85c-3.06.66-3.7-1.47-3.7-1.47-.5-1.27-1.22-1.61-1.22-1.61-1-.68.08-.67.08-.67 1.1.08 1.68 1.13 1.68 1.13.99 1.7 2.6 1.21 3.23.93.1-.72.39-1.21.7-1.49-2.44-.28-5-1.22-5-5.42 0-1.2.43-2.18 1.13-2.94-.11-.28-.49-1.4.11-2.92 0 0 .92-.3 3.02 1.12.88-.25 1.82-.37 2.76-.37s1.89.13 2.77.37c2.1-1.42 3.02-1.12 3.02-1.12.6 1.52.22 2.64.11 2.92.7.76 1.13 1.74 1.13 2.94 0 4.21-2.56 5.13-5.01 5.41.4.34.76 1.02.76 2.06v3.05c0 .29.2.64.76.53 4.36-1.46 7.51-5.57 7.51-10.43C23.04 5.27 18.27.5 12 .5Z"/></svg>
        </a>
        <button
          class="btn-brand"
          @click="router.push('/pricing')"
          aria-label="升级 Pro"
        >
          <svg viewBox="0 0 24 24" class="h-4 w-4" fill="currentColor"><path d="M12 2l2.39 4.84L20 8l-4 3.9.94 5.49L12 14.77 7.06 17.39 8 11.9 4 8l5.61-1.16L12 2z"/></svg>
          升级 Pro
        </button>
      </div>
    </div>
  </header>
</template>
