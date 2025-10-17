<template>
  <div class="ml-4">
    <div class="flex items-center space-x-2 py-1 hover:bg-gray-50 rounded px-2">
      <button
        v-if="!nodo.archivo"
        @click="expanded = !expanded"
        class="text-gray-500"
      >
        {{ expanded ? '▼' : '▶' }}
      </button>
      <span v-else class="w-4"></span>
      <!-- <span>{{ nodo.archivo ? '📄' : '📁' }} -->
        <div v-if="!nodo.archivo" class="flex items-center">
          <Folder class="h-5 w-5 text-indigo-400 mr-2" />
        </div>
        <div v-else class="flex items-center">
          <File class="h-5 w-5 text-indigo-400 mr-2" />
        </div>
      <!-- </span> -->
      <span class="flex-1">{{ nodo.nombre }}</span>
      <button
        @click="$emit('editar', nodo)"
        class="text-blue-600 hover:text-blue-900 text-sm"
      >
        <Edit class="h-4 w-4" />
      </button>
      <button
        @click="$emit('eliminar', nodo)"
        class="text-red-600 hover:text-red-900 text-sm"
      >
        <Trash2 class="h-4 w-4" />
      </button>
    </div>
    <div v-if="expanded && nodo.hijos && nodo.hijos.length > 0">
      <TreeNode
        v-for="hijo in nodo.hijos"
        :key="hijo.idcarpeta"
        :nodo="hijo"
        @editar="$emit('editar', $event)"
        @eliminar="$emit('eliminar', $event)"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Plus, Edit, Trash2, X, Folder, File } from 'lucide-vue-next'

defineProps({
  nodo: {
    type: Object,
    required: true
  }
})

defineEmits(['editar', 'eliminar'])

const expanded = ref(true)
</script>
