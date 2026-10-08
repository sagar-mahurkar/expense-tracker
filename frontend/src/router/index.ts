import { createRouter, createWebHistory } from "vue-router";

import CategoriesPage from "../pages/CategoriesPage.vue";
import DashboardPage from "../pages/DashboardPage.vue";
import LoginPage from "../pages/LoginPage.vue";
import RegisterPage from "../pages/RegisterPage.vue";
import TransactionsPage from "../pages/TransactionsPage.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "dashboard",
      component: DashboardPage,
    },
    {
      path: "/login",
      name: "login",
      component: LoginPage,
    },
    {
      path: "/register",
      name: "register",
      component: RegisterPage,
    },
    {
      path: "/transactions",
      name: "transactions",
      component: TransactionsPage,
    },
    {
      path: "/categories",
      name: "categories",
      component: CategoriesPage,
    },
  ],
});

export default router;
