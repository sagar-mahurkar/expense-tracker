<script setup lang="ts">
const summary = {
  balance: "25,000.00",
  income: "40,000.00",
  expense: "15,000.00",
};
</script>

<template>
  <div class="row g-4">
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
