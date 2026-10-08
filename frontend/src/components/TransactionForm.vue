<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import {
  createTransaction,
  updateTransaction,
  type Transaction,
  type TransactionInput,
} from "../services/transactions";
import {
  getCategories,
  type Category,
} from "../services/categories";

const props = defineProps<{
  transaction?: Transaction | null;
}>();

const emit = defineEmits<{
  submit: [];
  cancel: [];
}>();

const type = ref<"expense" | "income">("expense");
const amount = ref("");
const categoryId = ref("");
const description = ref("");
const transactionDate = ref("");

const categories = ref<Category[]>([]);
const loading = ref(false);
const loadingCategories = ref(false);
const error = ref("");

const isEditMode = () => !!props.transaction;

const populateForm = () => {
  if (!props.transaction) {
    type.value = "expense";
    amount.value = "";
    categoryId.value = "";
    description.value = "";
    transactionDate.value = "";
    return;
  }

  type.value = props.transaction.type;
  amount.value = props.transaction.amount;
  categoryId.value = props.transaction.category_id;
  description.value = props.transaction.description || "";
  transactionDate.value = props.transaction.transaction_date;
};

const loadCategories = async () => {
  loadingCategories.value = true;

  try {
    const response = await getCategories();
    categories.value = response.data;
  } catch (err: any) {
    error.value =
      err.response?.data?.error?.message ||
      "Failed to load categories.";
  } finally {
    loadingCategories.value = false;
  }
};

const handleSubmit = async () => {
  error.value = "";

  if (!categoryId.value) {
    error.value = "Please select a category.";
    return;
  }

  loading.value = true;

  const data: TransactionInput = {
    type: type.value,
    amount: amount.value,
    category_id: categoryId.value,
    description: description.value || undefined,
    transaction_date: transactionDate.value,
  };

  try {
    if (props.transaction) {
      await updateTransaction(props.transaction.id, data);
    } else {
      await createTransaction(data);
    }

    emit("submit");
  } catch (err: any) {
    error.value =
      err.response?.data?.error?.message ||
      `Failed to ${isEditMode() ? "update" : "create"} transaction.`;
  } finally {
    loading.value = false;
  }
};

watch(
  () => props.transaction,
  () => {
    populateForm();
  },
  { immediate: true },
);

onMounted(loadCategories);
</script>

<template>
  <form id="transaction-form" @submit.prevent="handleSubmit">
    <div
      v-if="error"
      class="alert alert-danger"
      role="alert"
    >
      {{ error }}
    </div>

    <div class="mb-3">
      <label for="transaction-type" class="form-label">
        Type
      </label>

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
      <label for="transaction-amount" class="form-label">
        Amount
      </label>

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
      <label for="transaction-category" class="form-label">
        Category
      </label>

      <select
        id="transaction-category"
        v-model="categoryId"
        class="form-select"
        :disabled="loadingCategories"
        required
      >
        <option value="" disabled>
          {{ loadingCategories ? "Loading categories..." : "Select category" }}
        </option>

        <option
          v-for="category in categories"
          :key="category.id"
          :value="category.id"
        >
          {{ category.name }}
        </option>
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

    <div class="mb-3">
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

    <div class="d-flex justify-content-end gap-2">
      <button
        type="button"
        class="btn btn-secondary"
        @click="emit('cancel')"
      >
        Cancel
      </button>

      <button
        type="submit"
        class="btn btn-primary"
        :disabled="loading || loadingCategories"
      >
        {{
          loading
            ? "Saving..."
            : isEditMode()
              ? "Update Transaction"
              : "Add Transaction"
        }}
      </button>
    </div>
  </form>
</template>
