<script setup lang="ts">
import { ref } from "vue";
import { RouterLink } from "vue-router";

const email = ref("");
const password = ref("");

const handleSubmit = () => {
  // API integration will be implemented in Phase 12.
  console.log("Login form submitted", {
    email: email.value,
    password: password.value,
  });
};
</script>

<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="card shadow p-5" style="width: 500px">
      <h1 class="mb-4 text-center">Login</h1>

      <form @submit.prevent="handleSubmit">
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            class="form-control"
            required
            autocomplete="email"
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            class="form-control"
            required
            autocomplete="current-password"
          />
        </div>

        <button type="submit" class="btn btn-primary w-100">
          Login
        </button>
      </form>

      <div class="mt-4 text-center">
        Don't have an account?
        <RouterLink to="/register">Register</RouterLink>
      </div>
    </div>
  </div>
</template>
