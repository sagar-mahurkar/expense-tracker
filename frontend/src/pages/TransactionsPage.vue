<script setup lang="ts">
import { ref } from "vue";
import TransactionForm from "../components/TransactionForm.vue";
import TransactionTable from "../components/TransactionTable.vue";

const showForm = ref(false);

const openAddTransaction = () => {
  showForm.value = true;
};

const closeForm = () => {
  showForm.value = false;
};

const search = ref("");
const typeFilter = ref("");
const date = ref("");
const page = ref(1);

</script>

<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h1>Transactions</h1>
        <p class="text-muted mb-0">
          Manage your income and expenses
        </p>
      </div>

      <button
        type="button"
        class="btn btn-primary"
        @click="openAddTransaction"
      >
        Add Transaction
      </button>
    </div>

    <div class="card shadow-sm mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-5">
            <label for="transaction-search" class="form-label">
              Search
            </label>
            <input
              id="transaction-search"
              v-model="search"
              type="search"
              class="form-control"
              placeholder="Search by description"
            />
          </div>

          <div class="col-md-3">
            <label for="transaction-type-filter" class="form-label">
              Type
            </label>
            <select
              id="transaction-type-filter"
              v-model="typeFilter"
              class="form-select"
            >
              <option value="">All</option>
              <option value="income">Income</option>
              <option value="expense">Expense</option>
            </select>
          </div>

          <div class="col-md-3">
            <label for="transaction-date-filter" class="form-label">
              Date
            </label>
            <input
              id="transaction-date-filter"
              v-model="date"
              type="date"
              class="form-control"
            />
          </div>

          <div class="col-md-1 d-flex align-items-end">
            <button
              type="button"
              class="btn btn-outline-secondary w-100"
              @click="search = ''; typeFilter = ''; date = ''; page = 1"
            >
              Clear
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow-sm">
      <div class="card-body">
        <TransactionTable />
        <nav aria-label="Transaction pagination" class="mt-4">
          <ul class="pagination justify-content-center mb-0">
            <li class="page-item disabled">
              <button class="page-link">Previous</button>
            </li>

            <li class="page-item active">
              <button class="page-link">1</button>
            </li>

            <li class="page-item">
              <button class="page-link">2</button>
            </li>

            <li class="page-item">
              <button class="page-link">Next</button>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <!-- Add Transaction Modal -->
    <div
      v-if="showForm"
      class="modal fade show d-block"
      tabindex="-1"
      role="dialog"
      aria-modal="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Transaction</h5>

            <button
              type="button"
              class="btn-close"
              aria-label="Close"
              @click="closeForm"
            ></button>
          </div>

          <div class="modal-body">
            <TransactionForm />
          </div>

          <div class="modal-footer">
            <button
              type="submit"
              form="transaction-form"
              class="btn btn-primary"
            >
              Save Transaction
            </button>

            <button
              type="button"
              class="btn btn-secondary"
              @click="closeForm"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showForm" class="modal-backdrop fade show"></div>
  </div>
</template>
