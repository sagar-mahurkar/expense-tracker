<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import TransactionForm from "../components/TransactionForm.vue";
import {
  deleteTransaction,
  getTransactions,
  type Transaction,
} from "../services/transactions";

import {
  getCategories,
  type Category,
} from "../services/categories";

const transactions = ref<Transaction[]>([]);
const selectedTransaction = ref<Transaction | null>(null);
const categories = ref<Category[]>([]);
const loading = ref(false);
const error = ref("");

const search = ref("");
const type = ref("");
const date = ref("");

const currentPage = ref(1);
const perPage = ref(10);

const totalPages = ref(1);
const total = ref(0);

const showForm = ref(false);

const loadTransactions = async () => {
  loading.value = true;
  error.value = "";

  try {
    const response = await getTransactions({
      type: type.value || undefined,
      search: search.value || undefined,
      start_date: date.value || undefined,
      end_date: date.value || undefined,
      page: currentPage.value,
      per_page: perPage.value,
    });

    transactions.value = response.data;
    totalPages.value = response.pagination.total_pages;
    total.value = response.pagination.total;
  } catch (err: any) {
    error.value =
      err.response?.data?.error?.message ||
      "Failed to load transactions.";
  } finally {
    loading.value = false;
  }
};

const loadCategories = async () => {
  try {
    const response = await getCategories();
    categories.value = response.data;
  } catch (err: any) {
    error.value =
      err.response?.data?.error?.message ||
      "Failed to load categories.";
  }
};

const getCategoryName = (categoryId: string) => {
  return categories.value.find(
    (category) => category.id === categoryId,
  )?.name || "-";
};

const handleSearch = () => {
  currentPage.value = 1;
  loadTransactions();
};

const handleClearFilters = async () => {
  search.value = "";
  type.value = "";
  date.value = "";
  currentPage.value = 1;

  await loadTransactions();
};

const handleTypeChange = () => {
  currentPage.value = 1;
  loadTransactions();
};

const handleDateChange = () => {
  currentPage.value = 1;
  loadTransactions();
};

const goToPage = (page: number) => {
  if (page < 1 || page > totalPages.value || page === currentPage.value) {
    return;
  }

  currentPage.value = page;
  loadTransactions();
};

watch(perPage, () => {
  currentPage.value = 1;
  loadTransactions();
});

const openForm = () => {
  selectedTransaction.value = null;
  showForm.value = true;
};

const closeForm = () => {
  showForm.value = false;
  selectedTransaction.value = null;
};

const handleTransactionCreated = async () => {
  showForm.value = false;
  selectedTransaction.value = null;
  currentPage.value = 1;
  await loadTransactions();
};


const openEditForm = (transaction: Transaction) => {
  selectedTransaction.value = transaction;
  showForm.value = true;
};

const handleTransactionDeleted = async (id: string) => {
  const confirmed = window.confirm(
    "Are you sure you want to delete this transaction?",
  );

  if (!confirmed) {
    return;
  }

  error.value = "";

  try {
    await deleteTransaction(id);

    if (transactions.value.length === 1 && currentPage.value > 1) {
      currentPage.value -= 1;
    }

    await loadTransactions();
  } catch (err: any) {
    error.value =
      err.response?.data?.error?.message ||
      "Failed to delete transaction.";
  }
};

onMounted(async () => {
  await loadCategories();
  await loadTransactions();
});
</script>

<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Transactions</h2>

      <button
        type="button"
        class="btn btn-primary"
        @click="openForm"
      >
        Add Transaction
      </button>
    </div>

    <!-- Filters -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <label class="form-label">Search</label>
            <div class="input-group">
              <input
                v-model="search"
                type="text"
                class="form-control"
                placeholder="Search description"
                @keyup.enter="handleSearch"
              />

              <button
                type="button"
                class="btn btn-outline-secondary"
                @click="handleSearch"
              >
                Search
              </button>
            </div>
          </div>

          <div class="col-md-3">
            <label class="form-label">Type</label>

            <select
              v-model="type"
              class="form-select"
              @change="handleTypeChange"
            >
              <option value="">All</option>
              <option value="income">Income</option>
              <option value="expense">Expense</option>
            </select>
          </div>

          <div class="col-md-3">
            <label class="form-label">Date</label>

            <input
              v-model="date"
              type="date"
              class="form-control"
              @change="handleDateChange"
            />
          </div>

          <div class="col-md-1">
            <label class="form-label">Per page</label>

            <select
              v-model="perPage"
              class="form-select"
            >
              <option :value="10">10</option>
              <option :value="20">20</option>
              <option :value="50">50</option>
            </select>
          </div>

          <div class="col-md-1">
            <label class="form-label">&nbsp;</label>

            <button
              type="button"
              class="btn btn-outline-secondary w-100"
              @click="handleClearFilters"
            >
              Clear
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Error -->
    <div
      v-if="error"
      class="alert alert-danger"
      role="alert"
    >
      {{ error }}
    </div>

    <!-- Loading -->
    <div
      v-if="loading"
      class="text-center py-5"
    >
      Loading transactions...
    </div>

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
            <TransactionForm
              :transaction="selectedTransaction"
              @submit="handleTransactionCreated"
              @cancel="closeForm"
            />
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="showForm"
      class="modal-backdrop fade show"
    ></div>

    <!-- Transactions -->
    <div
      v-else
      class="card"
    >
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover mb-0">
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
              <tr
                v-for="transaction in transactions"
                :key="transaction.id"
              >
                <td>{{ transaction.transaction_date }}</td>

                <td>
                  {{ transaction.description || "-" }}
                </td>

                <td>
                  {{ getCategoryName(transaction.category_id) }}
                </td>

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

                <td class="text-end">
                  {{ transaction.amount }}
                </td>

                <td class="text-end">
                  <button
                    type="button"
                    class="btn btn-sm btn-outline-primary me-2"
                    @click="openEditForm(transaction)"
                  >
                    Edit
                  </button>

                  <button
                    type="button"
                    class="btn btn-sm btn-outline-danger"
                    @click="handleTransactionDeleted(transaction.id)"
                  >
                    Delete
                  </button>
                </td>
              </tr>

              <tr v-if="transactions.length === 0">
                <td
                  colspan="6"
                  class="text-center py-4 text-muted"
                >
                  No transactions found.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pagination -->
      <div
        v-if="total > 0"
        class="card-footer d-flex justify-content-between align-items-center"
      >
        <span class="text-muted">
          {{ total }} transaction{{ total === 1 ? "" : "s" }}
        </span>

        <div class="btn-group">
          <button
            type="button"
            class="btn btn-outline-secondary"
            :disabled="currentPage === 1"
            @click="goToPage(currentPage - 1)"
          >
            Previous
          </button>

          <button
            type="button"
            class="btn btn-outline-secondary"
            disabled
          >
            Page {{ currentPage }} of {{ totalPages }}
          </button>

          <button
            type="button"
            class="btn btn-outline-secondary"
            :disabled="currentPage === totalPages"
            @click="goToPage(currentPage + 1)"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
