<script setup lang="ts">
defineProps<{ url: string }>();
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
    </div>

    <div class="mt-4 rounded-xl border border-slate-200 bg-slate-50 px-4 py-10 text-center">
      <svg viewBox="0 0 24 24" class="mx-auto h-10 w-10 text-slate-300" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
      </svg>
      <p class="mt-3 text-sm font-medium text-slate-500">AI 视频总结 & 字幕翻译</p>
      <p class="mt-1 text-xs text-slate-400">功能开发中，即将上线</p>
    </div>
  </div>
</template>
