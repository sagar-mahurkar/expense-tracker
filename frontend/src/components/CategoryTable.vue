<script setup lang="ts">
const categories = [
  {
    id: 1,
    name: "Salary",
  },
  {
    id: 2,
    name: "Food",
  },
  {
    id: 3,
    name: "Utilities",
  },
];

const handleDelete = (categoryName: string) => {
  // API integration will be implemented in Phase 12.
  console.log("Delete category", categoryName);
};
</script>

<template>
  <div class="table-responsive">
    <table class="table table-striped table-hover align-middle mb-0">
      <thead>
        <tr>
          <th>Name</th>
          <th class="text-end">Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="category in categories" :key="category.id">
          <td>{{ category.name }}</td>

          <td class="text-end">
            <button
              type="button"
              class="btn btn-sm btn-outline-danger"
              @click="handleDelete(category.name)"
            >
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
