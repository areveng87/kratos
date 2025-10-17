<template>
  <div class="metric-card">
    <div class="flex items-center justify-between mb-4">
      <div>
        <p class="text-sm font-medium text-gray-400">{{ title }}</p>
        <p class="text-2xl font-bold text-white">{{ formattedValue }}</p>
      </div>
      <div :class="[
        'p-3 rounded-lg',
        iconBgColor
      ]">
        <component :is="icon" :class="['h-6 w-6', iconColor]" />
      </div>
    </div>
    
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-2">
        <span :class="[
          'text-sm font-medium',
          changeType === 'positive' ? 'text-green-400' : 
          changeType === 'negative' ? 'text-red-400' : 'text-gray-400'
        ]">
          {{ changeText }}
        </span>
        <component 
          v-if="changeType !== 'neutral'" 
          :is="changeType === 'positive' ? TrendingUp : TrendingDown" 
          :class="[
            'h-4 w-4',
            changeType === 'positive' ? 'text-green-400' : 'text-red-400'
          ]" 
        />
      </div>
      <span class="text-xs text-gray-500">vs mes anterior</span>
    </div>

    <!-- Mini chart -->
    <div v-if="chartData" class="mt-4 h-16">
      <svg class="w-full h-full" viewBox="0 0 200 60">
        <polyline
          :points="chartPoints"
          fill="none"
          :stroke="chartColor"
          stroke-width="2"
          class="opacity-70"
        />
        <defs>
          <linearGradient :id="`gradient-${title}`" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" :stop-color="chartColor" stop-opacity="0.3"/>
            <stop offset="100%" :stop-color="chartColor" stop-opacity="0"/>
          </linearGradient>
        </defs>
        <polygon
          :points="`${chartPoints} 200,60 0,60`"
          :fill="`url(#gradient-${title})`"
        />
      </svg>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { TrendingUp, TrendingDown } from 'lucide-vue-next'

const props = defineProps({
  title: String,
  value: [Number, String],
  change: Number,
  icon: Object,
  iconBgColor: {
    type: String,
    default: 'bg-indigo-600'
  },
  iconColor: {
    type: String,
    default: 'text-white'
  },
  chartData: Array,
  chartColor: {
    type: String,
    default: '#6366f1'
  },
  format: {
    type: String,
    default: 'number' // 'number', 'currency', 'percentage'
  }
})

const formattedValue = computed(() => {
  if (props.format === 'currency') {
    return new Intl.NumberFormat('es-CL', {
      style: 'currency',
      currency: 'CLP'
    }).format(props.value)
  } else if (props.format === 'percentage') {
    return `${props.value}%`
  } else {
    return new Intl.NumberFormat('es-CL').format(props.value)
  }
})

const changeType = computed(() => {
  if (props.change > 0) return 'positive'
  if (props.change < 0) return 'negative'
  return 'neutral'
})

const changeText = computed(() => {
  const absChange = Math.abs(props.change)
  const sign = props.change > 0 ? '+' : props.change < 0 ? '-' : ''
  return `${sign}${absChange}%`
})

const chartPoints = computed(() => {
  if (!props.chartData || props.chartData.length === 0) return ''
  
  const max = Math.max(...props.chartData)
  const min = Math.min(...props.chartData)
  const range = max - min || 1
  
  return props.chartData
    .map((value, index) => {
      const x = (index / (props.chartData.length - 1)) * 200
      const y = 60 - ((value - min) / range) * 40 - 10
      return `${x},${y}`
    })
    .join(' ')
})
</script>
