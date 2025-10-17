<template>
  <div class="fixed inset-0 pointer-events-none z-[100]">
    <div class="absolute top-4 right-4 space-y-2">
      <transition-group name="toast" tag="div">
        <div
          v-for="t in toast.toasts"
          :key="t.id"
          class="pointer-events-auto rounded-lg px-4 py-3 shadow-lg border flex items-start gap-2"
          :class="typeClass(t.type)"
        >
          <component :is="icon(t.type)" class="w-5 h-5 mt-0.5" />
          <span class="text-sm">{{ t.message }}</span>
          <button class="ml-3 opacity-60 hover:opacity-100" @click="toast.remove(t.id)">✕</button>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script setup>
import { useToastStore } from '../stores/toast'
import { CheckCircle, AlertTriangle, Info, XCircle } from 'lucide-vue-next'

const toast = useToastStore()
const icon = (type) =>
  type === 'success' ? CheckCircle :
  type === 'error'   ? XCircle :
  type === 'warning' ? AlertTriangle : Info

const typeClass = (type) => ({
  success: 'bg-green-50 border-green-200 text-green-800',
  error:   'bg-red-50 border-red-200 text-red-800',
  warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
  info:    'bg-slate-50 border-slate-200 text-slate-800',
}[type] ?? 'bg-slate-50 border-slate-200 text-slate-800')
</script>

<style scoped>
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(-6px); }
.toast-enter-active, .toast-leave-active { transition: all .18s ease; }
</style>
