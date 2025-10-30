<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    @click.self="handleClickOutside"
  >
    <div
      class="rounded-lg p-6 w-full max-w-2xl"
      style="background-color: var(--color-bg-secondary); border: 1px solid var(--color-border)"
    >
      <!-- Header -->
      <div class="mb-4">
        <h2 class="text-xl font-bold" style="color: var(--color-text-primary)">
          {{ title }}
        </h2>
        <p v-if="description" class="mt-2" style="color: var(--color-text-secondary)">
          {{ description }}
        </p>
      </div>

      <!-- Textarea -->
      <div class="mb-6">
        <textarea
          v-model="texto"
          :placeholder="placeholder"
          :required="required"
          rows="6"
          class="w-full px-4 py-3 rounded-lg border resize-none focus:outline-none focus:ring-2"
          style="
            background-color: var(--color-bg-primary);
            border-color: var(--color-border);
            color: var(--color-text-primary);
          "
          :style="{ 'border-color': showError ? '#ef4444' : 'var(--color-border)' }"
        />
        <p v-if="showError" class="mt-2 text-sm" style="color: #ef4444">
          Este campo es obligatorio
        </p>
      </div>

      <!-- Botones de acción -->
      <div class="flex justify-end gap-3">
        <button @click="cancelar" class="btn-secondary">
          Cancelar
        </button>
        <button @click="guardar" class="btn-primary">
          Guardar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Escriba aquí...'
  },
  required: {
    type: Boolean,
    default: false
  },
  initialValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['save', 'cancel'])

const texto = ref(props.initialValue)
const showError = ref(false)

const guardar = () => {
  // Validar si es requerido y está vacío
  if (props.required && !texto.value.trim()) {
    showError.value = true
    return
  }
  
  showError.value = false
  emit('save', texto.value)
}

const cancelar = () => {
  emit('cancel')
}

const handleClickOutside = () => {
  // Si es requerido y no hay texto, no permitir cerrar
  if (props.required && !texto.value.trim()) {
    showError.value = true
    return
  }
  
  cancelar()
}
</script>

<style scoped>
.btn-primary {
  background-color: var(--color-primary);
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: opacity 0.2s;
}

.btn-primary:hover {
  opacity: 0.9;
}

.btn-secondary {
  background-color: var(--color-bg-tertiary);
  color: var(--color-text-primary);
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: background-color 0.2s;
  border: 1px solid var(--color-border);
}

.btn-secondary:hover {
  background-color: var(--color-bg-hover);
}

textarea:focus {
  border-color: var(--color-primary);
  ring-color: var(--color-primary);
}
</style>
