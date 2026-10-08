<script setup lang="ts">
import { onMounted, ref } from "vue";
import { getSummary, type Summary } from "../services/summary";

const summary = ref<Summary>({
  balance: "0.00",
  income: "0.00",
  expense: "0.00",
});

const loading = ref(false);
const error = ref("");

const loadSummary = async () => {
  loading.value = true;
  error.value = "";

  try {
    const response = await getSummary();
    summary.value = response.data;
  } catch (err: any) {
    error.value =
      err.response?.data?.error?.message ||
      "Failed to load dashboard summary.";
  } finally {
    loading.value = false;
  }
};

onMounted(loadSummary);
</script>

<template>
  <div
    v-if="error"
    class="alert alert-danger"
    role="alert"
  >
    {{ error }}
  </div>

  <div
    v-if="loading"
    class="text-center py-4"
  >
    Loading summary...
  </div>

  <div
    v-else
    class="row g-4"
  >
    <div class="col-md-4">
      <div class="card shadow-sm h-100">
        <div class="card-body">
          <h5 class="card-title">Balance</h5>
          <p class="display-6 mb-0">₹{{ summary.balance }}</p>
        </div>
      </div>
    </div>

    <div class="col-md-4">
      <div class="card shadow-sm h-100">
        <div class="card-body">
          <h5 class="card-title">Income</h5>
          <p class="display-6 mb-0">₹{{ summary.income }}</p>
        </div>
      </div>
    </div>

    <div class="col-md-4">
      <div class="card shadow-sm h-100">
        <div class="card-body">
          <h5 class="card-title">Expense</h5>
          <p class="display-6 mb-0">₹{{ summary.expense }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
