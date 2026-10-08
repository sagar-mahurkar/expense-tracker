<script setup lang="ts">
import { ref } from "vue";

const name = ref("");

const handleSubmit = () => {
  // API integration will be implemented in Phase 12.
  console.log("Category submitted", {
    name: name.value,
  });
};
</script>

<template>
  <form id="category-form" @submit.prevent="handleSubmit">
    <div>
      <label for="category-name" class="form-label">Name</label>
      <input
        id="category-name"
        v-model="name"
        type="text"
        class="form-control"
        maxlength="100"
        required
      />
    </div>
  </form>
</template>
