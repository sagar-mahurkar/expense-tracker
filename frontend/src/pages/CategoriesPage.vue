<script setup lang="ts">
import { onMounted, ref } from "vue";
import CategoryForm from "../components/CategoryForm.vue";
import CategoryTable from "../components/CategoryTable.vue";
import {
  createCategory,
  deleteCategory,
  getCategories,
} from "../services/categories";
import type { Category } from "../services/categories";

const categories = ref<Category[]>([]);
const showForm = ref(false);
const errorMessage = ref("");

const loadCategories = async () => {
  errorMessage.value = "";

  try {
    const response = await getCategories();
    categories.value = response.data;
  } catch (error: any) {
    errorMessage.value =
      error.response?.data?.error?.message ||
      "Unable to load categories.";
  }
};

const handleCreateCategory = async (
  data: { name: string; type: "income" | "expense" },
) => {
  errorMessage.value = "";

  try {
    await createCategory(data);
    showForm.value = false;
    await loadCategories();
  } catch (error: any) {
    errorMessage.value =
      error.response?.data?.error?.message ||
      "Unable to create category.";
  }
};

const handleDeleteCategory = async (id: string) => {
  errorMessage.value = "";

  try {
    await deleteCategory(id);
    await loadCategories();
  } catch (error: any) {
    errorMessage.value =
      error.response?.data?.error?.message ||
      "Unable to delete category.";
  }
};

onMounted(loadCategories);
</script>

<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h1>Categories</h1>
        <p class="text-muted mb-0">Manage your transaction categories</p>
      </div>

      <button
        type="button"
        class="btn btn-primary"
        @click="showForm = true"
      >
        Add Category
      </button>
    </div>

    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>

    <div class="card shadow-sm">
      <div class="card-body">
        <CategoryTable
          :categories="categories"
          @delete="handleDeleteCategory"
        />
      </div>
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
            <h5 class="modal-title">Add Category</h5>

            <button
              type="button"
              class="btn-close"
              aria-label="Close"
              @click="showForm = false"
            ></button>
          </div>

          <div class="modal-body">
            <CategoryForm @submit="handleCreateCategory" />
          </div>

          <div class="modal-footer">
            <button
              type="submit"
              form="category-form"
              class="btn btn-primary"
            >
              Save Category
            </button>

            <button
              type="button"
              class="btn btn-secondary"
              @click="showForm = false"
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
