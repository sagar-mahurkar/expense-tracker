import type { RouteLocationNormalized } from "vue-router";
import { useAuthStore } from "../stores/auth";

export const requireAuth = (
  _to: RouteLocationNormalized,
  _from: RouteLocationNormalized,
) => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated) {
    return { name: "login" };
  }
};