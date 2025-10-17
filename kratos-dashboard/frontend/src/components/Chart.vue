<template>
  <div class="card p-6">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-semibold text-white">{{ title }}</h3>
      <select 
        v-model="selectedPeriod" 
        class="bg-gray-700 border border-gray-600 text-white text-sm rounded-lg px-3 py-1.5 focus:ring-2 focus:ring-indigo-500"
      >
        <option value="week">Última semana</option>
        <option value="month">Último mes</option>
        <option value="quarter">Último trimestre</option>
      </select>
    </div>

    <div class="h-80">
      <svg class="w-full h-full" viewBox="0 0 800 300">
        <!-- Grid lines -->
        <defs>
          <pattern id="grid" width="80" height="30" patternUnits="userSpaceOnUse">
            <path d="M 80 0 L 0 0 0 30" fill="none" stroke="#374151" stroke-width="1" opacity="0.3"/>
          </pattern>
        </defs>
        <rect width="800" height="300" fill="url(#grid)" />

        <!-- Y-axis labels -->
        <g v-for="(tick, index) in yAxisTicks" :key="`y-${index}`">
          <text 
            :x="40" 
            :y="280 - (index * 60)" 
            class="text-xs fill-gray-400" 
            text-anchor="end"
          >
            {{ formatCurrency(tick) }}
          </text>
        </g>

        <!-- X-axis labels -->
        <g v-for="(label, index) in chartData.labels" :key="`x-${index}`">
          <text 
            :x="80 + (index * 100)" 
            y="295" 
            class="text-xs fill-gray-400" 
            text-anchor="middle"
          >
            {{ label }}
          </text>
        </g>

        <!-- Bars for sales -->
        <g v-for="(value, index) in chartData.ventas" :key="`bar-ventas-${index}`">
          <rect
            :x="60 + (index * 100)"
            :y="280 - (value / maxValue * 240)"
            width="15"
            :height="value / maxValue * 240"
            fill="#10b981"
            class="opacity-80 hover:opacity-100 transition-opacity"
          />
        </g>

        <!-- Bars for purchases -->
        <g v-for="(value, index) in chartData.compras" :key="`bar-compras-${index}`">
          <rect
            :x="80 + (index * 100)"
            :y="280 - (value / maxValue * 240)"
            width="15"
            :height="value / maxValue * 240"
            fill="#6366f1"
            class="opacity-80 hover:opacity-100 transition-opacity"
          />
        </g>

        <!-- Legend -->
        <g transform="translate(600, 20)">
          <rect x="0" y="0" width="15" height="15" fill="#10b981" />
          <text x="20" y="12" class="text-sm fill-white">Ventas</text>
          <rect x="0" y="25" width="15" height="15" fill="#6366f1" />
          <text x="20" y="37" class="text-sm fill-white">Compras</text>
        </g>
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  title: String,
  data: Object
})

const selectedPeriod = ref('month')

const chartData = computed(() => {
  return props.data || {
    labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
    ventas: [120000, 150000, 180000, 160000, 200000, 220000],
    compras: [80000, 90000, 110000, 95000, 130000, 140000]
  }
})

const maxValue = computed(() => {
  const allValues = [...chartData.value.ventas, ...chartData.value.compras]
  return Math.max(...allValues)
})

const yAxisTicks = computed(() => {
  const max = maxValue.value
  const step = max / 4
  return [0, step, step * 2, step * 3, max]
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}
</script>
