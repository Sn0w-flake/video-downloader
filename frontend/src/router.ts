import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import Result from "./views/Result.vue";

const routes: RouteRecordRaw[] = [
  { path: "/", name: "home", component: () => import("./views/Home.vue") },
  { path: "/result", name: "result", component: Result },
  { path: "/pricing", name: "pricing", component: () => import("./views/Pricing.vue") },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});
