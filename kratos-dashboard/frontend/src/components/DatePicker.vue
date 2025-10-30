<template>
  <div class="relative">
    <div class="flex items-center gap-2">
      <button
        type="button"
        @click="toggleCalendar"
        class="flex items-center gap-2 px-3 py-2 rounded-md theme-input w-full text-left"
        style="border: 1px solid var(--color-border)"
      >
        <Calendar class="w-4 h-4" style="color: var(--color-text-secondary)" />
        <span class="theme-text">{{ displayDate }}</span>
      </button>
    </div>

    <!-- Calendar Dropdown -->
    <div
      v-if="showCalendar"
      class="absolute z-50 mt-2 p-4 rounded-lg shadow-lg"
      style="background-color: var(--color-bg-primary); border: 1px solid var(--color-border); min-width: 280px"
    >
      <!-- Header -->
      <div class="flex items-center justify-between mb-4">
        <button
          type="button"
          @click="previousMonth"
          class="p-1 rounded hover:opacity-70"
        >
          <ChevronLeft class="w-5 h-5 theme-text" />
        </button>
        <div class="font-semibold theme-text">
          {{ monthNames[currentMonth] }} {{ currentYear }}
        </div>
        <button
          type="button"
          @click="nextMonth"
          class="p-1 rounded hover:opacity-70"
        >
          <ChevronRight class="w-5 h-5 theme-text" />
        </button>
      </div>

      <!-- Days of week -->
      <div class="grid grid-cols-7 gap-1 mb-2">
        <div
          v-for="day in dayNames"
          :key="day"
          class="text-center text-xs font-medium theme-text-secondary p-1"
        >
          {{ day }}
        </div>
      </div>

      <!-- Calendar days -->
      <div class="grid grid-cols-7 gap-1">
        <div
          v-for="(day, index) in calendarDays"
          :key="index"
          class="text-center"
        >
          <button
            v-if="day"
            type="button"
            @click="selectDate(day)"
            :disabled="isDateDisabled(day)"
            class="w-8 h-8 rounded text-sm transition-colors"
            :class="{
              'theme-text': !isDateDisabled(day) && !isSelectedDate(day),
              'opacity-30 cursor-not-allowed': isDateDisabled(day),
              'font-bold': isSelectedDate(day)
            }"
            :style="isSelectedDate(day) ? 'background-color: var(--color-primary); color: white' : ''"
          >
            {{ day }}
          </button>
        </div>
      </div>

      <!-- Footer buttons -->
      <div class="flex gap-2 mt-4 pt-3" style="border-top: 1px solid var(--color-border)">
        <button
          type="button"
          @click="selectToday"
          class="flex-1 px-3 py-1.5 text-sm rounded theme-text"
          style="border: 1px solid var(--color-border)"
        >
          Hoy
        </button>
        <button
          type="button"
          @click="clearDate"
          class="flex-1 px-3 py-1.5 text-sm rounded theme-text"
          style="border: 1px solid var(--color-border)"
        >
          Limpiar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { Calendar, ChevronLeft, ChevronRight } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  minDate: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])

const showCalendar = ref(false)
const currentMonth = ref(new Date().getMonth())
const currentYear = ref(new Date().getFullYear())

const monthNames = [
  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

const dayNames = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']

const displayDate = computed(() => {
  if (!props.modelValue) return 'Seleccionar fecha...'
  const date = new Date(props.modelValue + 'T00:00:00')
  return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`
})

const calendarDays = computed(() => {
  const firstDay = new Date(currentYear.value, currentMonth.value, 1)
  const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0)
  const daysInMonth = lastDay.getDate()
  const startingDayOfWeek = firstDay.getDay()

  const days = []
  
  // Add empty slots for days before the first day of the month
  for (let i = 0; i < startingDayOfWeek; i++) {
    days.push(null)
  }
  
  // Add all days of the month
  for (let day = 1; day <= daysInMonth; day++) {
    days.push(day)
  }
  
  return days
})

const toggleCalendar = () => {
  showCalendar.value = !showCalendar.value
  if (showCalendar.value && props.modelValue) {
    const date = new Date(props.modelValue + 'T00:00:00')
    currentMonth.value = date.getMonth()
    currentYear.value = date.getFullYear()
  }
}

const previousMonth = () => {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value++
  }
}

const selectDate = (day) => {
  if (isDateDisabled(day)) return
  
  const date = new Date(currentYear.value, currentMonth.value, day)
  const formattedDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  emit('update:modelValue', formattedDate)
  showCalendar.value = false
}

const selectToday = () => {
  const today = new Date()
  const formattedDate = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`
  emit('update:modelValue', formattedDate)
  showCalendar.value = false
}

const clearDate = () => {
  emit('update:modelValue', '')
  showCalendar.value = false
}

const isDateDisabled = (day) => {
  if (!props.minDate) return false
  
  const date = new Date(currentYear.value, currentMonth.value, day)
  const minDate = new Date(props.minDate + 'T00:00:00')
  return date < minDate
}

const isSelectedDate = (day) => {
  if (!props.modelValue) return false
  
  const selectedDate = new Date(props.modelValue + 'T00:00:00')
  return (
    selectedDate.getDate() === day &&
    selectedDate.getMonth() === currentMonth.value &&
    selectedDate.getFullYear() === currentYear.value
  )
}

// Close calendar when clicking outside
const handleClickOutside = (event) => {
  const calendar = event.target.closest('.relative')
  if (!calendar && showCalendar.value) {
    showCalendar.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
