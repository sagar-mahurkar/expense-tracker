import { defineStore } from "pinia";
import { login as loginApi } from "../services/auth";
import type { AuthUser } from "../services/auth";

const TOKEN_KEY = "access_token";
const USER_KEY = "auth_user";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem(TOKEN_KEY),
    user: JSON.parse(
      localStorage.getItem(USER_KEY) || "null",
    ) as AuthUser | null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(email: string, password: string) {
      const response = await loginApi({
        email,
        password,
      });

      this.token = response.data.access_token;
      this.user = response.data.user;

      localStorage.setItem(TOKEN_KEY, this.token);
      localStorage.setItem(
        USER_KEY,
        JSON.stringify(this.user),
      );
    },

    logout() {
      this.token = null;
      this.user = null;

      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
    },
  },
});
