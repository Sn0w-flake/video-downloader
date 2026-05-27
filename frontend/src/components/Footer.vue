<script setup lang="ts"></script>

<template>
  <footer class="mt-24 border-t border-slate-200 bg-white/60">
    <div class="container-page py-10">
      <div class="grid gap-8 md:grid-cols-3">
        <div>
          <div class="flex items-center gap-2">
            <span class="grid h-9 w-9 place-items-center rounded-xl bg-brand-gradient">
              <svg viewBox="0 0 24 24" class="h-5 w-5 text-white" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
            </span>
            <span class="text-lg font-bold text-gradient">VidGrab</span>
          </div>
          <p class="mt-3 text-sm text-slate-600 leading-relaxed">
            基于 yt-dlp 的万能视频下载工具，支持 1000+ 平台，高清无水印，AI 字幕翻译与视频总结。
          </p>
        </div>
        <div>
          <h4 class="text-sm font-semibold text-slate-900">产品</h4>
          <ul class="mt-3 space-y-2 text-sm text-slate-600">
            <li><router-link class="hover:text-brand-700 cursor-pointer" to="/">首页</router-link></li>
            <li><router-link class="hover:text-brand-700 cursor-pointer" to="/pricing">定价</router-link></li>
            <li><a class="hover:text-brand-700 cursor-pointer" href="/#features">功能特性</a></li>
            <li><a class="hover:text-brand-700 cursor-pointer" href="/#platforms">支持平台</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-sm font-semibold text-slate-900">法律与说明</h4>
          <ul class="mt-3 space-y-2 text-sm text-slate-600">
            <li>本工具仅供个人合法学习使用</li>
            <li>请勿用于侵犯他人版权的下载</li>
            <li>不存储任何视频内容</li>
          </ul>
        </div>
      </div>
      <div class="mt-10 border-t border-slate-200 pt-5 text-xs text-slate-500 flex flex-wrap items-center justify-between gap-2">
        <span>© {{ new Date().getFullYear() }} VidGrab. Powered by yt-dlp.</span>
        <span>Made with care · 浅浅地省点钱 ✨</span>
      </div>
    </div>
  </footer>
</template>
