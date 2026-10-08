<script setup lang="ts">
import { ref } from "vue";

const name = ref("");
const type = ref<"income" | "expense">("expense");

const emit = defineEmits<{
  submit: [data: { name: string; type: "income" | "expense" }];
}>();

const handleSubmit = () => {
  emit("submit", {
    name: name.value,
    type: type.value,
  });
};
</script>

<template>
  <form id="category-form" @submit.prevent="handleSubmit">
    <div class="mb-3">
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

    <div>
      <label for="category-type" class="form-label">Type</label>
      <select
        id="category-type"
        v-model="type"
        class="form-select"
        required
      >
        <option value="expense">Expense</option>
        <option value="income">Income</option>
      </select>
    </div>
  </form>
</template>
