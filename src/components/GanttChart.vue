<template>
  <div class="gantt-chart-container" ref="containerRef">
    <div class="gantt-header">
      <div class="gantt-sidebar-header">
        <span class="gantt-title">{{ title }}</span>
      </div>
      <div class="gantt-timeline-header">
        <div class="gantt-timeline-scroll" ref="timelineScrollRef">
          <div class="gantt-months-row">
            <div 
              v-for="month in months" 
              :key="month.key" 
              class="gantt-month-cell"
              :style="{ width: month.width + 'px' }"
            >
              {{ month.label }}
            </div>
          </div>
          <div class="gantt-days-row">
            <div 
              v-for="day in days" 
              :key="day.key" 
              class="gantt-day-cell"
              :class="{ 'gantt-day-weekend': day.isWeekend }"
              :style="{ width: dayWidth + 'px' }"
            >
              {{ day.label }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="gantt-body">
      <div class="gantt-sidebar">
        <div 
          v-for="task in tasks" 
          :key="task.id" 
          class="gantt-task-row"
          :style="{ height: rowHeight + 'px' }"
        >
          <div 
            class="gantt-task-name"
            :style="{ paddingLeft: (task.level || 0) * 20 + 'px' }"
          >
            <span v-if="hasChildren(task.id)" class="gantt-expand-icon" @click="toggleExpand(task)">
              {{ task.expanded ? '▼' : '▶' }}
            </span>
            <span class="gantt-task-text">{{ task.name }}</span>
          </div>
          <div class="gantt-task-duration">{{ formatDuration(task) }}</div>
        </div>
      </div>
      
      <div class="gantt-timeline" ref="timelineRef">
        <div class="gantt-timeline-grid">
          <div 
            v-for="day in days" 
            :key="'grid-' + day.key" 
            class="gantt-grid-line"
            :class="{ 'gantt-grid-weekend': day.isWeekend }"
            :style="{ 
              left: getDayPosition(day.date) + 'px',
              width: dayWidth + 'px',
              height: (tasks.filter(t => !t.hidden).length * rowHeight) + 'px'
            }"
          ></div>
        </div>
        
        <div class="gantt-today-line" v-if="todayPosition >= 0" :style="{ left: todayPosition + 'px' }">
          <div class="gantt-today-label">今天</div>
        </div>
        
        <div 
          v-for="(dependency, index) in dependencies" 
          :key="'dep-' + index"
          class="gantt-dependency-line"
        >
          <svg :width="dependency.width" :height="dependency.height">
            <path
              :d="dependency.path"
              fill="none"
              stroke="#94a3b8"
              stroke-width="2"
              marker-end="url(#arrowhead)"
            />
          </svg>
        </div>
        
        <svg class="gantt-arrow-marker" width="0" height="0">
          <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#94a3b8" />
            </marker>
          </defs>
        </svg>
        
        <div 
          v-for="task in visibleTasks" 
          :key="task.id" 
          class="gantt-task-bar-wrapper"
          :style="{ 
            top: getTaskTop(task) + 'px',
            height: rowHeight + 'px'
          }"
        >
          <div 
            class="gantt-task-bar"
            :class="getTaskBarClass(task)"
            :style="getTaskBarStyle(task)"
            @mousedown.stop="startDragTask($event, task)"
          >
            <div class="gantt-task-bar-progress" v-if="!isMilestone(task)" :style="{ width: (task.progress || 0) + '%' }"></div>
            <div class="gantt-task-bar-label">{{ task.progress ? Math.round(task.progress) + '%' : '' }}</div>
            <div 
              class="gantt-resize-handle gantt-resize-left"
              @mousedown.stop="startResizeTask($event, task, 'left')"
            ></div>
            <div 
              class="gantt-resize-handle gantt-resize-right"
              @mousedown.stop="startResizeTask($event, task, 'right')"
            ></div>
          </div>
          
          <div 
            v-if="isMilestone(task)"
            class="gantt-milestone"
            :style="{ left: getTaskPosition(task).left + 'px', top: (rowHeight - 20) / 2 + 'px' }"
          >
            ◆
          </div>
        </div>
      </div>
    </div>
    
    <div class="gantt-tooltip" v-if="tooltipTask" :style="{ left: tooltipPosition.x + 'px', top: tooltipPosition.y + 'px' }">
      <div class="gantt-tooltip-title">{{ tooltipTask.name }}</div>
      <div class="gantt-tooltip-content">
        <div>开始: {{ formatDate(tooltipTask.start) }}</div>
        <div>结束: {{ formatDate(getEndDate(tooltipTask)) }}</div>
        <div v-if="tooltipTask.progress">进度: {{ Math.round(tooltipTask.progress) }}%</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  tasks: {
    type: Array,
    default: () => []
  },
  title: {
    type: String,
    default: '项目甘特图'
  },
  rowHeight: {
    type: Number,
    default: 40
  },
  dayWidth: {
    type: Number,
    default: 30
  },
  startDate: {
    type: String,
    default: null
  },
  endDate: {
    type: String,
    default: null
  },
  editable: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:tasks', 'task-change', 'task-move', 'task-resize'])

const containerRef = ref(null)
const timelineRef = ref(null)
const timelineScrollRef = ref(null)
const tooltipTask = ref(null)
const tooltipPosition = ref({ x: 0, y: 0 })
const draggingTask = ref(null)
const dragType = ref(null)
const dragStartX = ref(0)
const dragTaskStart = ref(null)

const internalTasks = ref([])
const expandedTasks = ref(new Set())

const initTasks = () => {
  internalTasks.value = props.tasks.map((task, index) => {
    const expanded = expandedTasks.value.has(task.id) || task.expanded !== false
    return {
      ...task,
      _index: index,
      expanded: expanded,
      hidden: false,
      level: task.parentId ? getTaskLevel(task.parentId) : 0
    }
  })
  updateVisibility()
}

const getTaskLevel = (taskId) => {
  const task = props.tasks.find(t => t.id === taskId)
  if (!task) return 0
  return task.parentId ? getTaskLevel(task.parentId) + 1 : 1
}

const hasChildren = (taskId) => {
  return props.tasks.some(t => t.parentId === taskId)
}

const toggleExpand = (task) => {
  task.expanded = !task.expanded
  if (task.expanded) {
    expandedTasks.value.add(task.id)
  } else {
    expandedTasks.value.delete(task.id)
  }
  updateVisibility()
}

const updateVisibility = () => {
  const hideChildren = (parentId) => {
    internalTasks.value.forEach(task => {
      if (task.parentId === parentId) {
        task.hidden = true
        hideChildren(task.id)
      }
    })
  }
  
  internalTasks.value.forEach(task => {
    task.hidden = false
  })
  
  internalTasks.value.forEach(task => {
    if (!task.expanded && hasChildren(task.id)) {
      hideChildren(task.id)
    }
  })
}

const visibleTasks = computed(() => internalTasks.value.filter(t => !t.hidden))

const chartStartDate = computed(() => {
  if (props.startDate) return new Date(props.startDate)
  const dates = props.tasks.map(t => new Date(t.start))
  const min = new Date(Math.min(...dates))
  min.setDate(min.getDate() - 3)
  return min
})

const chartEndDate = computed(() => {
  if (props.endDate) return new Date(props.endDate)
  const dates = props.tasks.map(t => {
    const end = new Date(t.start)
    end.setDate(end.getDate() + (t.duration || 1))
    return end
  })
  const max = new Date(Math.max(...dates))
  max.setDate(max.getDate() + 3)
  return max
})

const months = computed(() => {
  const result = []
  const current = new Date(chartStartDate.value)
  current.setDate(1)
  
  while (current <= chartEndDate.value) {
    const monthStart = new Date(current)
    const monthEnd = new Date(current.getFullYear(), current.getMonth() + 1, 0)
    const actualStart = monthStart < chartStartDate.value ? chartStartDate.value : monthStart
    const actualEnd = monthEnd > chartEndDate.value ? chartEndDate.value : monthEnd
    
    const daysInView = Math.ceil((actualEnd - actualStart) / (1000 * 60 * 60 * 24)) + 1
    
    result.push({
      key: `${current.getFullYear()}-${current.getMonth()}`,
      label: `${current.getFullYear()}年${current.getMonth() + 1}月`,
      width: daysInView * props.dayWidth
    })
    
    current.setMonth(current.getMonth() + 1)
  }
  
  return result
})

const days = computed(() => {
  const result = []
  const current = new Date(chartStartDate.value)
  
  while (current <= chartEndDate.value) {
    const dayOfWeek = current.getDay()
    result.push({
      key: current.toISOString().split('T')[0],
      date: new Date(current),
      label: current.getDate(),
      isWeekend: dayOfWeek === 0 || dayOfWeek === 6
    })
    current.setDate(current.getDate() + 1)
  }
  
  return result
})

const todayPosition = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return getDayPosition(today)
})

const getDayPosition = (date) => {
  const start = new Date(chartStartDate.value)
  start.setHours(0, 0, 0, 0)
  const target = new Date(date)
  target.setHours(0, 0, 0, 0)
  const daysDiff = Math.ceil((target - start) / (1000 * 60 * 60 * 24))
  return daysDiff * props.dayWidth
}

const getTaskPosition = (task) => {
  const left = getDayPosition(new Date(task.start))
  const width = isMilestone(task) ? 0 : (task.duration || 1) * props.dayWidth
  return { left, width }
}

const getTaskTop = (task) => {
  const index = visibleTasks.value.findIndex(t => t.id === task.id)
  return index * props.rowHeight
}

const getTaskBarStyle = (task) => {
  if (isMilestone(task)) return { display: 'none' }
  const pos = getTaskPosition(task)
  return {
    left: pos.left + 'px',
    width: Math.max(20, pos.width) + 'px',
    backgroundColor: task.color || '#3b82f6'
  }
}

const getTaskBarClass = (task) => {
  return {
    'gantt-task-summary': hasChildren(task.id) || task.isSummary
  }
}

const isMilestone = (task) => {
  return task.isMilestone || task.duration === 0
}

const getEndDate = (task) => {
  const end = new Date(task.start)
  end.setDate(end.getDate() + (task.duration || 1))
  return end
}

const dependencies = computed(() => {
  const deps = []
  
  internalTasks.value.forEach(task => {
    if (task.dependencies && Array.isArray(task.dependencies)) {
      task.dependencies.forEach(depId => {
        const depTask = internalTasks.value.find(t => t.id === depId)
        if (depTask && !task.hidden && !depTask.hidden) {
          const depEnd = getTaskPosition(depTask).left + getTaskPosition(depTask).width
          const taskStart = getTaskPosition(task).left
          const depTop = getTaskTop(depTask) + props.rowHeight / 2
          const taskTop = getTaskTop(task) + props.rowHeight / 2
          
          const minX = Math.min(depEnd, taskStart)
          const maxX = Math.max(depEnd, taskStart)
          const minY = Math.min(depTop, taskTop)
          const maxY = Math.max(depTop, taskTop)
          
          const width = maxX - minX + 20
          const height = maxY - minY + 10
          
          const startOffsetX = depEnd - minX
          const endOffsetX = taskStart - minX
          const startOffsetY = depTop - minY + 5
          const endOffsetY = taskTop - minY + 5
          
          let path
          if (Math.abs(depTop - taskTop) < 10) {
            path = `M ${startOffsetX} ${startOffsetY} L ${endOffsetX} ${endOffsetY}`
          } else {
            const midX = (startOffsetX + endOffsetX) / 2
            path = `M ${startOffsetX} ${startOffsetY} L ${midX} ${startOffsetY} L ${midX} ${endOffsetY} L ${endOffsetX} ${endOffsetY}`
          }
          
          deps.push({
            width,
            height,
            path,
            top: minY - 5,
            left: minX - 10
          })
        }
      })
    }
  })
  
  return deps
})

const formatDuration = (task) => {
  if (isMilestone(task)) return '里程碑'
  const duration = task.duration || 1
  return duration + '天'
}

const formatDate = (date) => {
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const startDragTask = (event, task) => {
  if (!props.editable || isMilestone(task)) return
  draggingTask.value = task
  dragType.value = 'move'
  dragStartX.value = event.clientX
  dragTaskStart.value = { start: new Date(task.start), duration: task.duration }
  event.preventDefault()
}

const startResizeTask = (event, task, side) => {
  if (!props.editable) return
  draggingTask.value = task
  dragType.value = side
  dragStartX.value = event.clientX
  dragTaskStart.value = { start: new Date(task.start), duration: task.duration }
  event.preventDefault()
}

const handleMouseMove = (event) => {
  if (!draggingTask.value) return
  
  const dx = event.clientX - dragStartX.value
  const daysMoved = Math.round(dx / props.dayWidth)
  
  const task = internalTasks.value.find(t => t.id === draggingTask.value.id)
  if (!task) return
  
  if (dragType.value === 'move') {
    const newStart = new Date(dragTaskStart.value.start)
    newStart.setDate(newStart.getDate() + daysMoved)
    task.start = newStart.toISOString().split('T')[0]
  } else if (dragType.value === 'right') {
    task.duration = Math.max(1, dragTaskStart.value.duration + daysMoved)
  } else if (dragType.value === 'left') {
    const newStart = new Date(dragTaskStart.value.start)
    newStart.setDate(newStart.getDate() + daysMoved)
    const newDuration = dragTaskStart.value.duration - daysMoved
    if (newDuration >= 1) {
      task.start = newStart.toISOString().split('T')[0]
      task.duration = newDuration
    }
  }
  
  emit('task-move', task)
}

const handleMouseUp = () => {
  if (draggingTask.value) {
    emit('update:tasks', internalTasks.value.map(t => ({
      id: t.id,
      name: t.name,
      start: t.start,
      duration: t.duration,
      progress: t.progress,
      color: t.color,
      parentId: t.parentId,
      dependencies: t.dependencies,
      isMilestone: t.isMilestone,
      expanded: t.expanded
    })))
    emit('task-change', internalTasks.value)
  }
  draggingTask.value = null
  dragType.value = null
}

watch(() => props.tasks, initTasks, { deep: true, immediate: true })

onMounted(() => {
  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
})

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)
})
</script>

<style scoped>
.gantt-chart-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  background: white;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.gantt-header {
  display: flex;
  border-bottom: 2px solid #e5e7eb;
  background: #f9fafb;
  position: sticky;
  top: 0;
  z-index: 10;
}

.gantt-sidebar-header {
  width: 240px;
  min-width: 240px;
  padding: 12px 16px;
  border-right: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
}

.gantt-title {
  font-weight: 600;
  font-size: 14px;
  color: #374151;
}

.gantt-timeline-header {
  flex: 1;
  overflow: hidden;
}

.gantt-timeline-scroll {
  display: inline-block;
}

.gantt-months-row {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
}

.gantt-month-cell {
  padding: 8px;
  text-align: center;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  border-right: 1px solid #e5e7eb;
  background: #f3f4f6;
}

.gantt-days-row {
  display: flex;
}

.gantt-day-cell {
  padding: 6px 0;
  text-align: center;
  font-size: 11px;
  color: #6b7280;
  border-right: 1px solid #e5e7eb;
}

.gantt-day-weekend {
  background: #f9fafb;
}

.gantt-body {
  display: flex;
  flex: 1;
  overflow: auto;
}

.gantt-sidebar {
  width: 240px;
  min-width: 240px;
  background: #fafafa;
  border-right: 1px solid #e5e7eb;
}

.gantt-task-row {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e5e7eb;
  padding: 0 8px;
  gap: 8px;
}

.gantt-task-name {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #374151;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.gantt-expand-icon {
  cursor: pointer;
  color: #9ca3af;
  font-size: 10px;
  width: 16px;
  text-align: center;
}

.gantt-expand-icon:hover {
  color: #3b82f6;
}

.gantt-task-text {
  overflow: hidden;
  text-overflow: ellipsis;
}

.gantt-task-duration {
  font-size: 11px;
  color: #9ca3af;
  min-width: 40px;
  text-align: right;
}

.gantt-timeline {
  flex: 1;
  position: relative;
  background: #fff;
  overflow-x: auto;
}

.gantt-timeline-grid {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  pointer-events: none;
}

.gantt-grid-line {
  position: absolute;
  top: 0;
  border-right: 1px solid #f0f0f0;
}

.gantt-grid-weekend {
  background: #fafafa;
}

.gantt-today-line {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #ef4444;
  z-index: 5;
}

.gantt-today-label {
  position: absolute;
  top: 0;
  left: -20px;
  background: #ef4444;
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
}

.gantt-task-bar-wrapper {
  position: absolute;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
}

.gantt-task-bar {
  position: absolute;
  height: 26px;
  border-radius: 4px;
  cursor: move;
  display: flex;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.gantt-task-bar:hover {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.gantt-task-bar-progress {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background: rgba(0, 0, 0, 0.15);
}

.gantt-task-bar-label {
  width: 100%;
  text-align: center;
  font-size: 11px;
  color: white;
  font-weight: 500;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  z-index: 1;
}

.gantt-task-summary {
  border-radius: 0;
  background: transparent !important;
  border: none;
}

.gantt-task-summary::before,
.gantt-task-summary::after {
  content: '';
  position: absolute;
  background: #374151;
}

.gantt-task-summary::before {
  left: 0;
  top: 50%;
  width: 100%;
  height: 4px;
  transform: translateY(-50%);
  border-radius: 2px;
}

.gantt-task-summary::after {
  left: 0;
  top: 50%;
  width: 12px;
  height: 12px;
  transform: translateY(-50%);
  border-radius: 2px;
  box-shadow: calc(100% - 24px) 0 0 #374151;
}

.gantt-resize-handle {
  position: absolute;
  width: 8px;
  height: 100%;
  cursor: ew-resize;
  opacity: 0;
  transition: opacity 0.2s;
}

.gantt-task-bar:hover .gantt-resize-handle {
  opacity: 1;
}

.gantt-resize-left {
  left: 0;
  cursor: w-resize;
}

.gantt-resize-right {
  right: 0;
  cursor: e-resize;
}

.gantt-milestone {
  position: absolute;
  font-size: 24px;
  color: #f59e0b;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.gantt-dependency-line {
  position: absolute;
  pointer-events: none;
  z-index: 2;
}

.gantt-arrow-marker {
  position: absolute;
  width: 0;
  height: 0;
}

.gantt-tooltip {
  position: fixed;
  background: #1f2937;
  color: white;
  padding: 10px 12px;
  border-radius: 6px;
  font-size: 12px;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
  max-width: 250px;
}

.gantt-tooltip-title {
  font-weight: 600;
  margin-bottom: 6px;
}

.gantt-tooltip-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  opacity: 0.9;
}
</style>