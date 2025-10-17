import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useToastStore = defineStore('toast', () => {
  const toasts = ref([])

  const push = (message, type = 'info', timeout = 3000) => {
    const id = Date.now() + Math.random()
    toasts.value.push({ id, message, type })
    if (timeout) setTimeout(() => remove(id), timeout)
  }

  const remove = (id) => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  return { toasts, push, remove }
})
