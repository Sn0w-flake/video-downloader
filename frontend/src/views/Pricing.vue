<script setup lang="ts">
import { ref } from "vue";

const toast = ref("");
function pickPlan(name: string) {
  toast.value = `${name} · 即将上线，敬请期待 ✨`;
  setTimeout(() => (toast.value = ""), 2400);
}

const plans = [
  {
    name: "免费",
    price: "¥0",
    suffix: "/ 永久",
    desc: "尝鲜不要钱",
    cta: "当前方案",
    disabled: true,
    features: [
      "1080p 以内下载",
      "单条解析",
      "原生字幕导出",
      "1000+ 平台覆盖",
      "无广告无水印",
    ],
  },
  {
    name: "Pro · 月度",
    price: "¥29",
    suffix: "/ 月",
    desc: "灵活按月，随时取消",
    cta: "升级 Pro",
    badge: "热门",
    highlight: true,
    features: [
      "4K / 8K 高清下载",
      "批量下载不限量",
      "AI 视频总结",
      "AI 字幕翻译（多语种）",
      "优先解析服务器",
      "邮件技术支持",
    ],
  },
  {
    name: "Pro · 年度",
    price: "¥199",
    suffix: "/ 年",
    desc: "立省 ¥149，平均每天 5 毛",
    cta: "立省 43%",
    features: [
      "包含月度全部能力",
      "全年 AI 总结 / 翻译额度",
      "新功能优先体验",
      "VIP 专属交流群",
      "提前解锁未来 Pro 功能",
    ],
  },
];
</script>

<template>
  <section class="container-page relative pt-10 sm:pt-16 pb-24">
    <div class="hero-glow animate-glow"></div>

    <div class="relative text-center max-w-2xl mx-auto">
      <p class="text-sm font-semibold text-brand-700 tracking-wider uppercase">Pricing</p>
      <h1 class="mt-2 text-3xl sm:text-4xl font-bold text-slate-900 tracking-tight">
        简单透明，<span class="text-gradient">立即上手</span>
      </h1>
      <p class="mt-3 text-slate-600">
        免费永久可用；想要 4K、批量、AI 能力解锁，升级 Pro 即可，月度年度任你选。
      </p>
    </div>

    <div class="relative mt-12 grid gap-6 md:grid-cols-3 max-w-6xl mx-auto">
      <div
        v-for="p in plans"
        :key="p.name"
        class="surface relative p-6 flex flex-col card-hover"
        :class="p.highlight ? 'border-brand-400 ring-2 ring-brand-200 shadow-cardHover' : ''"
      >
        <span v-if="p.badge" class="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-cta-gradient px-3 py-0.5 text-xs font-bold text-white shadow-cta">{{ p.badge }}</span>
        <div>
          <h3 class="text-lg font-semibold text-slate-900">{{ p.name }}</h3>
          <div class="mt-3 flex items-baseline gap-1">
            <span class="text-4xl font-extrabold tracking-tight" :class="p.highlight ? 'text-gradient' : 'text-slate-900'">{{ p.price }}</span>
            <span class="text-sm text-slate-500">{{ p.suffix }}</span>
          </div>
          <p class="mt-1.5 text-sm text-slate-600">{{ p.desc }}</p>
        </div>
        <ul class="mt-6 space-y-2.5 text-sm text-slate-700">
          <li v-for="f in p.features" :key="f" class="flex items-start gap-2">
            <svg viewBox="0 0 24 24" class="mt-0.5 h-4 w-4 shrink-0" :class="p.highlight ? 'text-brand-600' : 'text-emerald-500'" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            {{ f }}
          </li>
        </ul>
        <div class="mt-7 pt-1">
          <button
            class="w-full"
            :class="p.highlight ? 'btn-primary' : p.disabled ? 'btn-ghost opacity-70 cursor-default' : 'btn-brand'"
            :disabled="p.disabled"
            @click="!p.disabled && pickPlan(p.name)"
          >
            {{ p.cta }}
          </button>
        </div>
      </div>
    </div>

    <p class="mt-10 text-center text-xs text-slate-500">
      所有付费功能仅为占位演示，本期不接入真实支付。
    </p>

    <transition name="toast">
      <div v-if="toast" class="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 rounded-xl bg-slate-900 px-5 py-3 text-sm text-white shadow-2xl">
        {{ toast }}
      </div>
    </transition>
  </section>
</template>

<style scoped>
.toast-enter-active, .toast-leave-active { transition: all 200ms ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translate(-50%, 10px); }
</style>
