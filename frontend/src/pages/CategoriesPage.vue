<script setup lang="ts">
import { ref } from "vue";
import CategoryForm from "../components/CategoryForm.vue";
import CategoryTable from "../components/CategoryTable.vue";

const showForm = ref(false);

const openAddCategory = () => {
  showForm.value = true;
};

const closeForm = () => {
  showForm.value = false;
};
</script>

<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h1>Categories</h1>
        <p class="text-muted mb-0">
          Manage your transaction categories
        </p>
      </div>

      <button
        type="button"
        class="btn btn-primary"
        @click="openAddCategory"
      >
        Add Category
      </button>
    </div>

    <div class="card shadow-sm">
      <div class="card-body">
        <CategoryTable />
      </div>
    </div>

    <!-- Add Category Modal -->
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
              @click="closeForm"
            ></button>
          </div>

          <div class="modal-body">
            <CategoryForm />
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
              @click="closeForm"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="showForm"
      class="modal-backdrop fade show"
    ></div>
  </div>
</template>
