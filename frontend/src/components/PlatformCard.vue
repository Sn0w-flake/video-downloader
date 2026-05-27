<script setup lang="ts">
defineProps<{
  name: string;
  color: string;
  logo: string;
  features?: string[];
}>();
</script>

<template>
  <div
    class="surface card-hover overflow-hidden cursor-pointer group"
    role="article"
    :aria-label="`支持 ${name}`"
  >
    <div
      class="relative aspect-[16/10] flex items-center justify-center overflow-hidden"
      :style="{ background: `linear-gradient(135deg, ${color} 0%, ${color}cc 70%, ${color}99 100%)` }"
    >
      <div class="absolute inset-0 opacity-30 group-hover:opacity-50 transition-opacity duration-300" style="background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.4), transparent 60%)"></div>
      <svg
        viewBox="0 0 24 24"
        class="h-12 w-12 text-white drop-shadow-md transition-transform duration-300 group-hover:scale-105"
        fill="currentColor"
        aria-hidden="true"
        v-html="logo"
      />
    </div>
    <div class="p-4">
      <div class="flex items-center justify-between">
        <h3 class="text-base font-semibold text-slate-900">{{ name }}</h3>
        <span class="text-xs text-slate-400">支持下载</span>
      </div>
      <div class="mt-2 flex flex-wrap gap-1.5">
        <span v-for="f in features || ['下载','字幕']" :key="f" class="chip text-[11px] py-0.5 px-2">
          {{ f }}
        </span>
      </div>
    </div>
  </div>
</template>
