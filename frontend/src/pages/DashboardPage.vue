<script setup lang="ts">
import DashboardSummary from "../components/DashboardSummary.vue";
</script>

<template>
  <div class="container py-4">
    <div class="mb-4">
      <h1>Dashboard</h1>
      <p class="text-muted">Overview of your finances</p>
    </div>

    <DashboardSummary />

    <div class="card shadow-sm mt-4">
      <div class="card-body">
        <h5 class="card-title">Recent Transactions</h5>
        <p class="text-muted mb-0">
          Your recent transactions will appear here.
        </p>
      </div>
    </div>
  </div>
</template>
