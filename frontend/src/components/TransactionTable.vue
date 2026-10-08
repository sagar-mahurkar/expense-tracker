<script setup lang="ts">
const transactions = [
  {
    date: "2026-10-08",
    description: "Monthly salary",
    category: "Salary",
    type: "income",
    amount: "40,000.00",
  },
  {
    date: "2026-10-07",
    description: "Grocery shopping",
    category: "Food",
    type: "expense",
    amount: "2,500.00",
  },
  {
    date: "2026-10-06",
    description: "Electricity bill",
    category: "Utilities",
    type: "expense",
    amount: "1,500.00",
  },
];
</script>

<template>
  <div class="table-responsive">
    <table class="table table-striped table-hover align-middle">
      <thead>
        <tr>
          <th>Date</th>
          <th>Description</th>
          <th>Category</th>
          <th>Type</th>
          <th class="text-end">Amount</th>
          <th class="text-end">Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="transaction in transactions" :key="transaction.date + transaction.description">
          <td>{{ transaction.date }}</td>
          <td>{{ transaction.description }}</td>
          <td>{{ transaction.category }}</td>
          <td>
            <span
              class="badge"
              :class="
                transaction.type === 'income'
                  ? 'text-bg-success'
                  : 'text-bg-danger'
              "
            >
              {{ transaction.type }}
            </span>
          </td>
          <td class="text-end">₹{{ transaction.amount }}</td>
          <td class="text-end">
            <button type="button" class="btn btn-sm btn-outline-primary me-2">
              Edit
            </button>
            <button type="button" class="btn btn-sm btn-outline-danger">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
