<script setup lang="ts">
import type { Category } from "../services/categories";

defineProps<{
  categories: Category[];
}>();

const emit = defineEmits<{
  delete: [id: string];
}>();
</script>

<template>
  <div class="table-responsive">
    <table class="table table-striped table-hover align-middle mb-0">
      <thead>
        <tr>
          <th>Name</th>
          <th>Type</th>
          <th class="text-end">Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="category in categories" :key="category.id">
          <td>{{ category.name }}</td>

          <td>
            <span
              class="badge"
              :class="
                category.type === 'income'
                  ? 'text-bg-success'
                  : 'text-bg-danger'
              "
            >
              {{ category.type }}
            </span>
          </td>

          <td class="text-end">
            <button
              type="button"
              class="btn btn-sm btn-outline-danger"
              @click="emit('delete', category.id)"
            >
              Delete
            </button>
          </td>
        </tr>

        <tr v-if="categories.length === 0">
          <td colspan="3" class="text-center text-muted py-4">
            No categories found.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
