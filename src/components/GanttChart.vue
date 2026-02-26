<template>
  <div class="gantt-chart">
    <div class="gantt-header">
      <div class="gantt-title">
        <slot name="title">
          <h3>{{ title }}</h3>
        </slot>
      </div>
      <div class="gantt-controls" v-if="showControls">
        <button class="btn btn-sm btn-outline" @click="zoomIn" :disabled="zoom >= 3">
          <span>+</span>
        </button>
        <span class="zoom-level">{{ zoom }}x</span>
        <button class="btn btn-sm btn-outline" @click="zoomOut" :disabled="zoom <= 0.5">
          <span>-</span>
        </button>
      </div>
    </div>
    
    <div class="gantt-body">
      <div class="gantt-sidebar">
        <div class="gantt-sidebar-header">
          <span>任务名称</span>
        </div>
        <div class="gantt-sidebar-content">
          <div
            v-for="task in tasks"
            :key="task.id"
            class="gantt-task-name"
            :style="{ height: `${rowHeight}px` }"
          >
            <span class="task-indicator" :style="{ background: task.color || defaultColor }"></span>
            <span class="task-text">{{ task.name }}</span>
          </div>
        </div>
      </div>
      
      <div class="gantt-timeline" ref="timelineRef">
        <div class="gantt-timeline-header" :style="{ width: `${timelineWidth}px` }">
          <div
            v-for="(day, index) in days"
            :key="index"
            class="gantt-day-header"
            :class="{ 'is-today': isToday(day.date), 'is-weekend': isWeekend(day.date) }"
            :style="{ width: `${dayWidth * zoom}px` }"
          >
            <span class="day-number">{{ formatDay(day.date) }}</span>
            <span class="day-name">{{ formatDayName(day.date) }}</span>
          </div>
        </div>
        
        <div class="gantt-timeline-content" :style="{ width: `${timelineWidth}px` }">
          <div class="gantt-grid">
            <div
              v-for="(day, index) in days"
              :key="`grid-${index}`"
              class="gantt-grid-line"
              :class="{ 'is-today': isToday(day.date), 'is-weekend': isWeekend(day.date) }"
              :style="{ width: `${dayWidth * zoom}px` }"
            ></div>
          </div>
          
          <div class="gantt-tasks">
            <div
              v-for="task in tasks"
              :key="task.id"
              class="gantt-task-row"
              :style="{ height: `${rowHeight}px` }"
            >
              <div
                class="gantt-bar"
                :style="getTaskStyle(task)"
                @click="$emit('task-click', task)"
                @mouseenter="$emit('task-hover', task)"
              >
                <span class="gantt-bar-text" v-if="task.name && zoom >= 1">
                  {{ task.name }}
                </span>
              </div>
            </div>
          </div>
          
          <div v-if="showTodayLine" class="gantt-today-line" :style="todayLineStyle"></div>
        </div>
      </div>
    </div>
    
    <div class="gantt-legend" v-if="showLegend && tasks.length > 0">
      <div class="legend-item" v-for="status in uniqueStatuses" :key="status.value">
        <span class="legend-color" :style="{ background: status.color }"></span>
        <span class="legend-label">{{ status.label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: '甘特图'
  },
  tasks: {
    type: Array,
    default: () => []
  },
  startDate: {
    type: [Date, String],
    default: null
  },
  endDate: {
    type: [Date, String],
    default: null
  },
  dayWidth: {
    type: Number,
    default: 40
  },
  rowHeight: {
    type: Number,
    default: 40
  },
  showControls: {
    type: Boolean,
    default: true
  },
  showLegend: {
    type: Boolean,
    default: true
  },
  showTodayLine: {
    type: Boolean,
    default: true
  },
  defaultColor: {
    type: String,
    default: '#2563eb'
  }
})

const emit = defineEmits(['task-click', 'task-hover', 'zoom-change'])

const timelineRef = ref(null)
const zoom = ref(1)

const minDate = computed(() => {
  if (props.startDate) return new Date(props.startDate)
  if (props.tasks.length === 0) return new Date()
  const dates = props.tasks.flatMap(t => [new Date(t.start), new Date(t.end)])
  return new Date(Math.min(...dates))
})

const maxDate = computed(() => {
  if (props.endDate) return new Date(props.endDate)
  if (props.tasks.length === 0) {
    const d = new Date()
    d.setDate(d.getDate() + 30)
    return d
  }
  const dates = props.tasks.flatMap(t => [new Date(t.start), new Date(t.end)])
  return new Date(Math.max(...dates))
})

const days = computed(() => {
  const result = []
  const current = new Date(minDate.value)
  const end = new Date(maxDate.value)
  
  while (current <= end) {
    result.push({
      date: new Date(current),
      isWeekend: isWeekend(current),
      isToday: isToday(current)
    })
    current.setDate(current.getDate() + 1)
  }
  
  return result
})

const timelineWidth = computed(() => {
  return days.value.length * props.dayWidth * zoom.value
})

const uniqueStatuses = computed(() => {
  const statusMap = new Map()
  props.tasks.forEach(task => {
    if (task.status && !statusMap.has(task.status.value)) {
      statusMap.set(task.status.value, task.status)
    }
  })
  return Array.from(statusMap.values())
})

const todayLineStyle = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const start = new Date(minDate.value)
  start.setHours(0, 0, 0, 0)
  
  const diffDays = Math.floor((today - start) / (1000 * 60 * 60 * 24))
  const left = diffDays * props.dayWidth * zoom.value + (props.dayWidth * zoom.value) / 2
  
  return {
    left: `${left}px`,
    height: `${props.tasks.length * props.rowHeight}px`
  }
})

function getTaskStyle(task) {
  const start = new Date(task.start)
  const end = new Date(task.end)
  
  const minStart = new Date(minDate.value)
  minStart.setHours(0, 0, 0, 0)
  start.setHours(0, 0, 0, 0)
  end.setHours(0, 0, 0, 0)
  
  const startOffset = Math.floor((start - minStart) / (1000 * 60 * 60 * 24))
  const duration = Math.floor((end - start) / (1000 * 60 * 60 * 24)) + 1
  
  const left = startOffset * props.dayWidth * zoom.value
  const width = duration * props.dayWidth * zoom.value
  
  return {
    left: `${left}px`,
    width: `${Math.max(width, props.dayWidth * zoom.value)}px`,
    background: task.color || props.defaultColor,
    opacity: task.progress !== undefined ? 0.7 + task.progress * 0.3 : 1
  }
}

function formatDay(date) {
  return date.getDate()
}

function formatDayName(date) {
  const names = ['日', '一', '二', '三', '四', '五', '六']
  return names[date.getDay()]
}

function isWeekend(date) {
  const day = date.getDay()
  return day === 0 || day === 6
}

function isToday(date) {
  const today = new Date()
  return date.getDate() === today.getDate() &&
    date.getMonth() === today.getMonth() &&
    date.getFullYear() === today.getFullYear()
}

function zoomIn() {
  if (zoom.value < 3) {
    zoom.value = Math.min(3, zoom.value + 0.5)
    emit('zoom-change', zoom.value)
  }
}

function zoomOut() {
  if (zoom.value > 0.5) {
    zoom.value = Math.max(0.5, zoom.value - 0.5)
    emit('zoom-change', zoom.value)
  }
}

function scrollToDate(date) {
  if (!timelineRef.value) return
  
  const target = new Date(date)
  const minStart = new Date(minDate.value)
  const diffDays = Math.floor((target - minStart) / (1000 * 60 * 60 * 24))
  const scrollLeft = diffDays * props.dayWidth * zoom.value - timelineRef.value.offsetWidth / 2
  
  timelineRef.value.scrollLeft = Math.max(0, scrollLeft)
}

function scrollToday() {
  scrollToDate(new Date())
}

defineExpose({
  zoomIn,
  zoomOut,
  scrollToDate,
  scrollToday
})
</script>

<style scoped>
.gantt-chart {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.gantt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--gray-200);
  background: var(--gray-50);
}

.gantt-title h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--gray-900);
}

.gantt-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.zoom-level {
  font-size: 14px;
  color: var(--gray-600);
  min-width: 40px;
  text-align: center;
}

.gantt-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.gantt-sidebar {
  flex-shrink: 0;
  width: 180px;
  border-right: 1px solid var(--gray-200);
  background: var(--gray-50);
  display: flex;
  flex-direction: column;
}

.gantt-sidebar-header {
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 600;
  color: var(--gray-600);
  border-bottom: 1px solid var(--gray-200);
  background: white;
}

.gantt-sidebar-content {
  flex: 1;
  overflow-y: auto;
}

.gantt-task-name {
  display: flex;
  align-items: center;
  padding: 0 12px;
  border-bottom: 1px solid var(--gray-100);
  font-size: 13px;
  color: var(--gray-700);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.task-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 8px;
  flex-shrink: 0;
}

.task-text {
  overflow: hidden;
  text-overflow: ellipsis;
}

.gantt-timeline {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
}

.gantt-timeline-header {
  display: flex;
  border-bottom: 1px solid var(--gray-200);
  background: white;
  position: sticky;
  top: 0;
  z-index: 10;
}

.gantt-day-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4px;
  border-right: 1px solid var(--gray-100);
  font-size: 11px;
}

.gantt-day-header.is-weekend {
  background: var(--gray-50);
}

.gantt-day-header.is-today {
  background: rgba(37, 99, 235, 0.1);
}

.day-number {
  font-weight: 600;
  color: var(--gray-700);
}

.day-name {
  color: var(--gray-500);
  font-size: 10px;
}

.gantt-timeline-content {
  position: relative;
  flex: 1;
}

.gantt-grid {
  display: flex;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
}

.gantt-grid-line {
  border-right: 1px solid var(--gray-100);
  height: 100%;
}

.gantt-grid-line.is-weekend {
  background: rgba(0, 0, 0, 0.02);
}

.gantt-grid-line.is-today {
  background: rgba(37, 99, 235, 0.05);
}

.gantt-tasks {
  position: relative;
}

.gantt-task-row {
  position: relative;
  border-bottom: 1px solid var(--gray-100);
}

.gantt-bar {
  position: absolute;
  top: 4px;
  height: calc(100% - 8px);
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  overflow: hidden;
}

.gantt-bar:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.gantt-bar-text {
  font-size: 11px;
  color: white;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.gantt-today-line {
  position: absolute;
  top: 0;
  width: 2px;
  background: var(--error);
  z-index: 20;
  pointer-events: none;
}

.gantt-today-line::before {
  content: '';
  position: absolute;
  top: -4px;
  left: -4px;
  width: 10px;
  height: 10px;
  background: var(--error);
  border-radius: 50%;
}

.gantt-legend {
  display: flex;
  gap: 16px;
  padding: 12px 16px;
  border-top: 1px solid var(--gray-200);
  background: var(--gray-50);
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--gray-600);
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}
</style>
