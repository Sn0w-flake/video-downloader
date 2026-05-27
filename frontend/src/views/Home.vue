<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import HeroInput from "../components/HeroInput.vue";
import PlatformCard from "../components/PlatformCard.vue";
import FeatureCard from "../components/FeatureCard.vue";
import BatchModal from "../components/BatchModal.vue";
import { platforms, features } from "../data/platforms";

const router = useRouter();
const batchOpen = ref(false);

const stats = [
  { value: "1000+", label: "支持平台" },
  { value: "4K / 8K", label: "原画质" },
  { value: "无水印", label: "无广告" },
  { value: "Free", label: "立即使用" },
];
</script>

<template>
  <section class="relative overflow-hidden">
    <div class="hero-glow animate-glow"></div>
    <div class="absolute top-32 -left-20 h-72 w-72 rounded-full bg-brand-300/30 blur-3xl animate-floaty hidden md:block" aria-hidden="true"></div>
    <div class="absolute top-12 -right-16 h-80 w-80 rounded-full bg-pink-300/30 blur-3xl animate-floaty hidden md:block" aria-hidden="true" style="animation-delay:-3s"></div>

    <div class="container-page relative pt-12 sm:pt-20 pb-16 sm:pb-24">
      <div class="flex justify-center">
        <span class="inline-flex items-center gap-2 rounded-full border border-brand-200 bg-white/80 px-3.5 py-1.5 text-xs font-medium text-brand-700 backdrop-blur shadow-sm">
          <span class="grid h-4 w-4 place-items-center rounded-full bg-brand-gradient">
            <svg viewBox="0 0 24 24" class="h-2.5 w-2.5 text-white" fill="currentColor"><path d="M12 2l2.39 4.84L20 8l-4 3.9.94 5.49L12 14.77 7.06 17.39 8 11.9 4 8l5.61-1.16L12 2z"/></svg>
          </span>
          AI 视频下载新姿势 · 限时免费
        </span>
      </div>

      <h1 class="mt-6 text-center text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight leading-tight">
        <span class="text-slate-900">万能视频下载，</span>
        <span class="text-gradient">一键搞定</span>
      </h1>
      <p class="mt-4 text-center text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed px-2">
        粘贴链接即可下载 1000+ 平台视频 · 高清无水印 · AI 字幕翻译与视频总结 · 手机也能跑
      </p>

      <div class="mt-8 sm:mt-10 max-w-3xl mx-auto">
        <HeroInput @batch="batchOpen = true" />
      </div>

      <div class="mt-10 sm:mt-14 grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-6 max-w-3xl mx-auto">
        <div v-for="s in stats" :key="s.label" class="surface px-4 py-3 sm:py-4 text-center">
          <div class="text-xl sm:text-2xl font-bold text-gradient">{{ s.value }}</div>
          <div class="mt-0.5 text-xs sm:text-sm text-slate-600">{{ s.label }}</div>
        </div>
      </div>
    </div>
  </section>

  <section id="features" class="container-page py-16 sm:py-24">
    <div class="text-center">
      <p class="text-sm font-semibold text-brand-700 tracking-wider uppercase">Features</p>
      <h2 class="mt-2 text-3xl sm:text-4xl font-bold tracking-tight text-slate-900">
        为什么选 <span class="text-gradient">VidGrab</span>
      </h2>
      <p class="mt-3 text-slate-600 max-w-2xl mx-auto">
        基于 19w star 开源 yt-dlp 引擎，覆盖最广；叠加 AI 增值能力，让保存视频变成获取信息。
      </p>
    </div>
    <div class="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <FeatureCard v-for="f in features" :key="f.title" v-bind="f" />
    </div>
  </section>

  <section id="platforms" class="container-page py-16 sm:py-20">
    <div class="text-center">
      <p class="text-sm font-semibold text-brand-700 tracking-wider uppercase">Platforms</p>
      <h2 class="mt-2 text-3xl sm:text-4xl font-bold tracking-tight text-slate-900">
        支持的<span class="text-gradient">主流平台</span>
      </h2>
      <p class="mt-3 text-slate-600 max-w-2xl mx-auto">
        以下仅列举热门站点，实际依托 yt-dlp 覆盖 1000+ 网站，持续更新。
      </p>
    </div>
    <div class="mt-10 grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
      <PlatformCard v-for="p in platforms" :key="p.name" v-bind="p" />
    </div>
  </section>

  <section class="container-page py-12 sm:py-20">
    <div class="surface relative overflow-hidden">
      <div class="absolute inset-0 bg-brand-gradient opacity-95"></div>
      <div class="absolute -top-20 -right-10 h-72 w-72 rounded-full bg-white/20 blur-3xl"></div>
      <div class="absolute -bottom-16 -left-10 h-64 w-64 rounded-full bg-orange-300/40 blur-3xl"></div>
      <div class="relative px-6 sm:px-10 py-12 sm:py-16 flex flex-col md:flex-row md:items-center md:justify-between gap-8">
        <div class="text-white">
          <p class="text-xs font-semibold tracking-widest uppercase opacity-80">Upgrade to Pro</p>
          <h2 class="mt-2 text-3xl sm:text-4xl font-bold leading-tight">
            解锁 4K · 批量下载 · 全部 AI 能力
          </h2>
          <p class="mt-3 text-white/85 max-w-xl">
            年费 ¥199，平均每天 5 毛钱。所有付费功能终身可用，每日不限次数。立省 5 杯咖啡。
          </p>
          <div class="mt-5 flex flex-wrap gap-2">
            <span class="rounded-full bg-white/15 px-3 py-1 text-xs font-medium text-white backdrop-blur">4K / 8K 下载</span>
            <span class="rounded-full bg-white/15 px-3 py-1 text-xs font-medium text-white backdrop-blur">批量下载不限量</span>
            <span class="rounded-full bg-white/15 px-3 py-1 text-xs font-medium text-white backdrop-blur">AI 视频总结</span>
            <span class="rounded-full bg-white/15 px-3 py-1 text-xs font-medium text-white backdrop-blur">AI 字幕翻译</span>
            <span class="rounded-full bg-white/15 px-3 py-1 text-xs font-medium text-white backdrop-blur">优先服务器</span>
          </div>
        </div>
        <div class="flex flex-col sm:flex-row gap-3 shrink-0">
          <button class="btn-primary text-base px-6 py-3.5" @click="router.push('/pricing')">
            立即升级 Pro
            <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
          </button>
          <a href="#features" class="inline-flex items-center justify-center gap-2 rounded-xl border border-white/40 bg-white/10 px-5 py-3 text-sm font-semibold text-white backdrop-blur hover:bg-white/20 cursor-pointer transition-colors">
            查看全部功能
          </a>
        </div>
      </div>
    </div>
  </section>

  <BatchModal :open="batchOpen" @close="batchOpen = false" />
</template>
