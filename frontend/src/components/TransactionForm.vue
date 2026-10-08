<script setup lang="ts">
import { ref } from "vue";

const type = ref("expense");
const amount = ref("");
const category = ref("");
const description = ref("");
const transactionDate = ref("");

const handleSubmit = () => {
  console.log("Transaction submitted", {
    type: type.value,
    amount: amount.value,
    category: category.value,
    description: description.value,
    transactionDate: transactionDate.value,
  });
};
</script>

<template>
  <form id="transaction-form" @submit.prevent="handleSubmit">
    <div class="mb-3">
      <label for="transaction-type" class="form-label">Type</label>
      <select
        id="transaction-type"
        v-model="type"
        class="form-select"
        required
      >
        <option value="expense">Expense</option>
        <option value="income">Income</option>
      </select>
    </div>

    <div class="mb-3">
      <label for="transaction-amount" class="form-label">Amount</label>
      <input
        id="transaction-amount"
        v-model="amount"
        type="number"
        class="form-control"
        min="0.01"
        step="0.01"
        required
      />
    </div>

    <div class="mb-3">
      <label for="transaction-category" class="form-label">Category</label>
      <select
        id="transaction-category"
        v-model="category"
        class="form-select"
        required
      >
        <option value="" disabled>Select category</option>
        <option value="salary">Salary</option>
        <option value="food">Food</option>
        <option value="utilities">Utilities</option>
      </select>
    </div>

    <div class="mb-3">
      <label for="transaction-description" class="form-label">
        Description
      </label>
      <textarea
        id="transaction-description"
        v-model="description"
        class="form-control"
        rows="3"
        maxlength="500"
      ></textarea>
    </div>

    <div>
      <label for="transaction-date" class="form-label">
        Transaction Date
      </label>
      <input
        id="transaction-date"
        v-model="transactionDate"
        type="date"
        class="form-control"
        required
      />
    </div>
  </form>
</template>