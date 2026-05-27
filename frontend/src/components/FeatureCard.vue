<script setup lang="ts">
defineProps<{
  title: string;
  desc: string;
  icon: string;
  pro?: boolean;
  tone?: "violet" | "pink" | "orange" | "cyan" | "emerald" | "amber";
}>();

const toneMap: Record<string, string> = {
  violet: "from-violet-500 to-violet-700",
  pink: "from-pink-500 to-rose-600",
  orange: "from-orange-400 to-orange-600",
  cyan: "from-cyan-400 to-sky-600",
  emerald: "from-emerald-400 to-teal-600",
  amber: "from-amber-400 to-orange-500",
};
</script>

<template>
  <div class="surface card-hover p-6 relative cursor-default">
    <span v-if="pro" class="pro-pill absolute top-4 right-4">Pro</span>
    <div
      class="grid h-12 w-12 place-items-center rounded-2xl text-white shadow-[0_8px_24px_-10px_rgba(124,58,237,0.45)] bg-gradient-to-br"
      :class="toneMap[tone || 'violet']"
    >
      <svg viewBox="0 0 24 24" class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" v-html="icon" />
    </div>
    <h3 class="mt-4 text-lg font-semibold text-slate-900">{{ title }}</h3>
    <p class="mt-1.5 text-sm leading-relaxed text-slate-600">{{ desc }}</p>
  </div>
</template>
