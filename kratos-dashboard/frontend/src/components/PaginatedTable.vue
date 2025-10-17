<template>
  <div class="card overflow-hidden">
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead class="table-header table-border">
          <tr>
            <th 
              v-for="column in columns" 
              :key="column.key"
              :class="[
                'px-4 py-3 text-left text-xs font-medium table-header-text uppercase tracking-wider',
                column.headerClass || ''
              ]"
            >
              {{ column.label }}
            </th>
          </tr>
        </thead>
        <tbody class="table-divider">
          <tr
            v-for="item in paginatedItems"
            :key="getItemKey(item)"
            class="transition-colors hover:bg-[#6366f3] hover:text-white cursor-pointer"
            @dblclick="handleRowDoubleClick(item)"
          >
            <td 
              v-for="column in columns" 
              :key="column.key"
              :class="[
                'px-4 py-3 whitespace-nowrap text-sm',
                column.cellClass || 'theme-text'
              ]"
            >
              <slot 
                :name="`cell-${column.key}`" 
                :item="item" 
                :value="getColumnValue(item, column.key)"
              >
                {{ getColumnValue(item, column.key) || '-' }}
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="text-gray-500">{{ loadingText }}</div>
    </div>

    <!-- Empty state -->
    <div v-else-if="items.length === 0" class="flex justify-center items-center py-8">
      <div class="text-gray-500">{{ emptyText }}</div>
    </div>

    <!-- Pagination controls -->
    <div class="pagination-bg px-6 py-3 pagination-border flex items-center justify-between">
      <div class="flex items-center space-x-2">
        <span class="text-sm text-gray-400">Mostrar</span>
        <select v-model="itemsPerPage" @change="currentPage = 1" class="pagination-select">
          <option :value="10">10</option>
          <option :value="50">50</option>
          <option :value="100">100</option>
        </select>
        <span class="text-sm text-gray-400">de {{ totalItems }} registros</span>
      </div>
      
      <div class="flex items-center space-x-2">
        <span class="text-sm text-gray-400">
          Página {{ currentPage }} de {{ totalPages }}
        </span>
        <div class="flex space-x-1">
          <button
            @click="currentPage = 1"
            :disabled="currentPage === 1"
            class="pagination-button"
          >
            ««
          </button>
          <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="pagination-button"
          >
            «
          </button>
          <button
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="pagination-button"
          >
            »
          </button>
          <button
            @click="currentPage = totalPages"
            :disabled="currentPage === totalPages"
            class="pagination-button"
          >
            »»
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    required: true,
    default: () => []
  },
  columns: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  loadingText: {
    type: String,
    default: 'Cargando datos...'
  },
  emptyText: {
    type: String,
    default: 'No se encontraron registros'
  },
  keyField: {
    type: String,
    default: 'id'
  },
  initialItemsPerPage: {
    type: Number,
    default: 10
  }
})

const emit = defineEmits(['page-change', 'items-per-page-change', 'row-double-click'])

const currentPage = ref(1)
const itemsPerPage = ref(props.initialItemsPerPage)

const totalItems = computed(() => (props.items || []).length)
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))

const paginatedItems = computed(() => {
  if (!props.items || !Array.isArray(props.items)) {
    return []
  }
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return props.items.slice(start, end)
})

const getItemKey = (item) => {
  return item[props.keyField] || item.id || Math.random()
}

const getColumnValue = (item, key) => {
  return key.split('.').reduce((obj, k) => obj?.[k], item)
}

// Watch for changes and emit events
watch(currentPage, (newPage) => {
  emit('page-change', newPage)
})

watch(itemsPerPage, (newItemsPerPage) => {
  emit('items-per-page-change', newItemsPerPage)
})

// Reset to first page when items change
watch(() => props.items, () => {
  currentPage.value = 1
})

const handleRowDoubleClick = (item) => {
  emit('row-double-click', item)
}
</script>

<style scoped>
.card {
  border-radius: 0.5rem;
  border: 1px solid var(--color-border);
  background-color: var(--color-bg-primary);
}

.table-header {
  background-color: var(--color-bg-secondary);
}

.table-header-text {
  color: var(--color-text-secondary);
}

.table-border {
  border-color: var(--color-border);
}

.table-row-hover {
  transition: background-color 0.3s;
}

.table-divider {
  border-color: var(--color-border);
}

.theme-text {
  color: var(--color-text-primary);
}

.pagination-bg {
  background-color: var(--color-bg-secondary);
}

.pagination-border {
  border-top: 1px solid var(--color-border);
}

.pagination-select {
  border: 1px solid var(--color-border);
  border-radius: 0.25rem;
  padding: 0.25rem 0.5rem;
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
  font-size: 0.875rem;
}

.pagination-button {
  border: 1px solid var(--color-border);
  border-radius: 0.25rem;
  padding: 0.25rem 0.5rem;
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.pagination-button:hover:not(:disabled) {
  background-color: var(--color-bg-secondary);
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
