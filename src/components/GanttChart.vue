<template>
  <div class="gantt-chart" :style="{ height: `${chartHeight}px` }">
    <!-- 左侧任务列表 -->
    <div class="gantt-sidebar" :style="{ width: `${sidebarWidth}px` }">
      <div class="gantt-header gantt-sidebar-header">
        <span>任务名称</span>
      </div>
      <div class="gantt-task-list">
        <div
          v-for="task in visibleTasks"
          :key="task.id"
          class="gantt-task-row"
          :class="{ 'is-group': task.isGroup, 'is-milestone': task.isMilestone }"
          :style="{ height: `${rowHeight}px` }"
        >
          <div
            class="gantt-task-name"
            :style="{ paddingLeft: `${(task.level || 0) * 20 + 16}px` }"
          >
            <span
              v-if="task.children && task.children.length"
              class="expand-icon"
              :class="{ expanded: !task.collapsed }"
              @click="toggleGroup(task)"
            >
              ▶
            </span>
            <span v-else class="expand-icon-placeholder"></span>
            <span class="task-icon">{{ getTaskIcon(task) }}</span>
            <span class="task-label">{{ task.name }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧时间轴 -->
    <div class="gantt-timeline" ref="timelineRef">
      <div class="gantt-header gantt-timeline-header">
        <div class="timeline-scale">
          <div
            v-for="(unit, index) in timeUnits"
            :key="index"
            class="time-unit"
            :style="{ width: `${unitWidth}px` }"
          >
            {{ unit.label }}
          </div>
        </div>
      </div>

      <div class="gantt-timeline-body" @scroll="handleScroll">
        <!-- 当前时间线 -->
        <div
          v-if="showCurrentTime"
          class="current-time-line"
          :style="{ left: `${currentTimePosition}px` }"
        ></div>

        <!-- 网格线 -->
        <div class="grid-lines">
          <div
            v-for="(unit, index) in timeUnits"
            :key="`grid-${index}`"
            class="grid-line"
            :class="{ weekend: unit.isWeekend }"
            :style="{ left: `${index * unitWidth}px`, width: `${unitWidth}px` }"
          ></div>
        </div>

        <!-- 任务条 -->
        <div class="gantt-bars">
          <div
            v-for="task in visibleTasks"
            :key="task.id"
            class="gantt-bar-row"
            :style="{ height: `${rowHeight}px` }"
          >
            <div
              v-if="!task.isMilestone"
              class="gantt-bar"
              :class="[
                `status-${task.status}`,
                { 'is-group': task.isGroup }
              ]"
              :style="getBarStyle(task)"
              @click="handleTaskClick(task)"
              @mouseenter="hoveredTask = task"
              @mouseleave="hoveredTask = null"
            >
              <div class="bar-progress" :style="{ width: `${task.progress}%` }"></div>
              <span class="bar-label">{{ task.name }}</span>

              <!-- 拖拽调整手柄 -->
              <div
                v-if="!task.isGroup && editable"
                class="resize-handle resize-left"
                @mousedown.stop="handleResizeStart($event, task, 'left')"
              ></div>
              <div
                v-if="!task.isGroup && editable"
                class="resize-handle resize-right"
                @mousedown.stop="handleResizeStart($event, task, 'right')"
              ></div>
            </div>

            <!-- 里程碑标记 -->
            <div
              v-else
              class="gantt-milestone"
              :class="`status-${task.status}`"
              :style="getMilestoneStyle(task)"
              @click="handleTaskClick(task)"
            >
              <span class="milestone-icon">◆</span>
            </div>
          </div>
        </div>

        <!-- 依赖线 -->
        <svg class="dependency-lines" v-if="showDependencies">
          <path
            v-for="(dep, index) in dependencyPaths"
            :key="index"
            :d="dep.path"
            class="dependency-line"
            :class="{ critical: dep.critical }"
          />
        </svg>
      </div>
    </div>

    <!-- 任务详情提示 -->
    <div
      v-if="hoveredTask"
      class="task-tooltip"
      :style="tooltipStyle"
    >
      <div class="tooltip-header">{{ hoveredTask.name }}</div>
      <div class="tooltip-body">
        <div>开始: {{ formatDate(hoveredTask.start) }}</div>
        <div>结束: {{ formatDate(hoveredTask.end) }}</div>
        <div>进度: {{ hoveredTask.progress }}%</div>
        <div>状态: {{ getStatusText(hoveredTask.status) }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  // 任务数据
  tasks: {
    type: Array,
    default: () => []
  },
  // 视图开始日期
  startDate: {
    type: Date,
    default: () => new Date()
  },
  // 视图天数
  viewDays: {
    type: Number,
    default: 30
  },
  // 时间单位宽度 (px)
  unitWidth: {
    type: Number,
    default: 50
  },
  // 行高 (px)
  rowHeight: {
    type: Number,
    default: 40
  },
  // 侧边栏宽度
  sidebarWidth: {
    type: Number,
    default: 200
  },
  // 是否显示当前时间线
  showCurrentTime: {
    type: Boolean,
    default: true
  },
  // 是否显示依赖线
  showDependencies: {
    type: Boolean,
    default: true
  },
  // 是否可编辑
  editable: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['taskClick', 'taskUpdate', 'taskToggle'])

const timelineRef = ref(null)
const hoveredTask = ref(null)
const tooltipPosition = ref({ x: 0, y: 0 })

// 计算图表高度
const chartHeight = computed(() => {
  return (visibleTasks.value.length + 1) * props.rowHeight + 40
})

// 可见任务（处理分组折叠）
const visibleTasks = computed(() => {
  const result = []

  const addTask = (task) => {
    result.push(task)
    if (task.children && task.children.length && !task.collapsed) {
      task.children.forEach(child => addTask({ ...child, level: (task.level || 0) + 1 }))
    }
  }

  props.tasks.forEach(task => addTask({ ...task, level: 0 }))
  return result
})

// 时间单位
const timeUnits = computed(() => {
  const units = []
  const start = new Date(props.startDate)

  for (let i = 0; i < props.viewDays; i++) {
    const date = new Date(start)
    date.setDate(start.getDate() + i)

    const dayOfWeek = date.getDay()
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6

    units.push({
      date: date,
      label: `${date.getMonth() + 1}/${date.getDate()}`,
      isWeekend: isWeekend,
      fullDate: date.toISOString().split('T')[0]
    })
  }

  return units
})

// 当前时间位置
const currentTimePosition = computed(() => {
  const now = new Date()
  const start = new Date(props.startDate)
  const diffDays = Math.floor((now - start) / (1000 * 60 * 60 * 24))

  if (diffDays < 0 || diffDays >= props.viewDays) return -1
  return diffDays * props.unitWidth + props.unitWidth / 2
})

// 工具提示样式
const tooltipStyle = computed(() => ({
  left: `${tooltipPosition.value.x}px`,
  top: `${tooltipPosition.value.y}px`
}))

// 依赖线路径
const dependencyPaths = computed(() => {
  if (!props.showDependencies) return []

  const paths = []

  visibleTasks.value.forEach((task, index) => {
    if (task.dependencies) {
      task.dependencies.forEach(depId => {
        const depTask = visibleTasks.value.find(t => t.id === depId)
        if (depTask) {
          const depIndex = visibleTasks.value.indexOf(depTask)
          paths.push({
            path: calculateDependencyPath(depTask, task, depIndex, index),
            critical: task.status === 'critical' || depTask.status === 'critical'
          })
        }
      })
    }
  })

  return paths
})

// 计算依赖线路径
const calculateDependencyPath = (fromTask, toTask, fromIndex, toIndex) => {
  const fromX = getTaskEndPosition(fromTask)
  const fromY = fromIndex * props.rowHeight + props.rowHeight / 2
  const toX = getTaskStartPosition(toTask)
  const toY = toIndex * props.rowHeight + props.rowHeight / 2

  const midX = (fromX + toX) / 2

  return `M ${fromX} ${fromY} L ${midX} ${fromY} L ${midX} ${toY} L ${toX} ${toY}`
}

// 获取任务条样式
const getBarStyle = (task) => {
  const start = getTaskStartPosition(task)
  const end = getTaskEndPosition(task)
  const width = end - start

  return {
    left: `${start}px`,
    width: `${width}px`,
    height: `${props.rowHeight - 12}px`
  }
}

// 获取里程碑样式
const getMilestoneStyle = (task) => {
  const position = getTaskStartPosition(task)

  return {
    left: `${position - 8}px`
  }
}

// 获取任务开始位置
const getTaskStartPosition = (task) => {
  const taskStart = new Date(task.start)
  const viewStart = new Date(props.startDate)
  const diffDays = Math.floor((taskStart - viewStart) / (1000 * 60 * 60 * 24))

  return Math.max(0, diffDays * props.unitWidth)
}

// 获取任务结束位置
const getTaskEndPosition = (task) => {
  const taskEnd = new Date(task.end)
  const viewStart = new Date(props.startDate)
  const diffDays = Math.floor((taskEnd - viewStart) / (1000 * 60 * 60 * 24))

  return Math.min(props.viewDays, diffDays + 1) * props.unitWidth
}

// 获取任务图标
const getTaskIcon = (task) => {
  if (task.isMilestone) return '🚩'
  if (task.isGroup) return task.collapsed ? '📁' : '📂'
  return '📄'
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    pending: '待开始',
    progress: '进行中',
    completed: '已完成',
    delayed: '已延期',
    critical: '关键路径'
  }
  return statusMap[status] || status
}

// 格式化日期
const formatDate = (date) => {
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

// 切换分组展开/折叠
const toggleGroup = (task) => {
  task.collapsed = !task.collapsed
  emit('taskToggle', task)
}

// 处理任务点击
const handleTaskClick = (task) => {
  emit('taskClick', task)
}

// 处理滚动
const handleScroll = (e) => {
  // 可以在这里处理同步滚动
}

// 调整大小相关
const resizingTask = ref(null)
const resizeDirection = ref(null)
const resizeStartX = ref(0)
const resizeStartDate = ref(null)

const handleResizeStart = (event, task, direction) => {
  if (!props.editable) return

  resizingTask.value = task
  resizeDirection.value = direction
  resizeStartX.value = event.clientX
  resizeStartDate.value = direction === 'left' ? new Date(task.start) : new Date(task.end)

  document.addEventListener('mousemove', handleResizeMove)
  document.addEventListener('mouseup', handleResizeEnd)
}

const handleResizeMove = (event) => {
  if (!resizingTask.value) return

  const deltaX = event.clientX - resizeStartX.value
  const deltaDays = Math.round(deltaX / props.unitWidth)

  if (resizeDirection.value === 'left') {
    const newStart = new Date(resizeStartDate.value)
    newStart.setDate(newStart.getDate() + deltaDays)
    resizingTask.value.start = newStart.toISOString().split('T')[0]
  } else {
    const newEnd = new Date(resizeStartDate.value)
    newEnd.setDate(newEnd.getDate() + deltaDays)
    resizingTask.value.end = newEnd.toISOString().split('T')[0]
  }
}

const handleResizeEnd = () => {
  if (resizingTask.value) {
    emit('taskUpdate', resizingTask.value)
  }

  resizingTask.value = null
  resizeDirection.value = null

  document.removeEventListener('mousemove', handleResizeMove)
  document.removeEventListener('mouseup', handleResizeEnd)
}

// 监听鼠标移动更新提示位置
watch(hoveredTask, (task) => {
  if (task && timelineRef.value) {
    const rect = timelineRef.value.getBoundingClientRect()
    tooltipPosition.value = {
      x: rect.left + getTaskStartPosition(task) + 20,
      y: rect.top + 60
    }
  }
})
</script>

<style scoped>
.gantt-chart {
  display: flex;
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: white;
  font-size: var(--text-sm);
}

.gantt-sidebar {
  flex-shrink: 0;
  border-right: 1px solid var(--gray-200);
  background: var(--gray-50);
}

.gantt-header {
  height: 40px;
  display: flex;
  align-items: center;
  padding: 0 var(--space-md);
  background: var(--gray-100);
  border-bottom: 1px solid var(--gray-200);
  font-weight: 600;
  color: var(--gray-700);
}

.gantt-task-list {
  overflow: hidden;
}

.gantt-task-row {
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--gray-100);
}

.gantt-task-row:hover {
  background: var(--gray-100);
}

.gantt-task-row.is-group {
  font-weight: 600;
  background: var(--gray-100);
}

.gantt-task-name {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  flex: 1;
  padding-right: var(--space-md);
  overflow: hidden;
}

.expand-icon {
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 10px;
  transition: transform 0.2s;
  color: var(--gray-500);
}

.expand-icon.expanded {
  transform: rotate(90deg);
}

.expand-icon-placeholder {
  width: 16px;
}

.task-icon {
  flex-shrink: 0;
}

.task-label {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.gantt-timeline {
  flex: 1;
  overflow: auto;
  position: relative;
}

.gantt-timeline-header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: var(--gray-100);
}

.timeline-scale {
  display: flex;
  height: 100%;
}

.time-unit {
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 1px solid var(--gray-200);
  font-size: var(--text-xs);
  color: var(--gray-600);
}

.time-unit:last-child {
  border-right: none;
}

.gantt-timeline-body {
  position: relative;
  min-height: calc(100% - 40px);
}

.grid-lines {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.grid-line {
  position: absolute;
  top: 0;
  bottom: 0;
  border-right: 1px solid var(--gray-100);
}

.grid-line.weekend {
  background: rgba(0, 0, 0, 0.02);
}

.current-time-line {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--error);
  z-index: 5;
  pointer-events: none;
}

.current-time-line::before {
  content: '';
  position: absolute;
  top: -4px;
  left: -4px;
  width: 10px;
  height: 10px;
  background: var(--error);
  border-radius: 50%;
}

.gantt-bars {
  position: relative;
  z-index: 2;
}

.gantt-bar-row {
  position: relative;
  display: flex;
  align-items: center;
}

.gantt-bar {
  position: absolute;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  padding: 0 var(--space-sm);
  cursor: pointer;
  overflow: hidden;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

.gantt-bar:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.bar-progress {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.3);
  pointer-events: none;
}

.bar-label {
  position: relative;
  z-index: 1;
  font-size: var(--text-xs);
  color: white;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 状态颜色 */
.gantt-bar.status-pending {
  background: var(--gray-400);
}

.gantt-bar.status-progress {
  background: var(--primary);
}

.gantt-bar.status-completed {
  background: var(--success);
}

.gantt-bar.status-delayed {
  background: var(--error);
}

.gantt-bar.status-critical {
  background: var(--accent);
}

.gantt-bar.is-group {
  background: var(--gray-600);
}

/* 里程碑 */
.gantt-milestone {
  position: absolute;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.milestone-icon {
  font-size: 16px;
}

.gantt-milestone.status-pending .milestone-icon { color: var(--gray-400); }
.gantt-milestone.status-progress .milestone-icon { color: var(--primary); }
.gantt-milestone.status-completed .milestone-icon { color: var(--success); }
.gantt-milestone.status-delayed .milestone-icon { color: var(--error); }
.gantt-milestone.status-critical .milestone-icon { color: var(--accent); }

/* 调整手柄 */
.resize-handle {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 8px;
  cursor: col-resize;
  opacity: 0;
  transition: opacity 0.2s;
}

.gantt-bar:hover .resize-handle {
  opacity: 1;
}

.resize-handle:hover {
  background: rgba(255, 255, 255, 0.3);
}

.resize-left {
  left: 0;
}

.resize-right {
  right: 0;
}

/* 依赖线 */
.dependency-lines {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.dependency-line {
  fill: none;
  stroke: var(--gray-400);
  stroke-width: 2;
}

.dependency-line.critical {
  stroke: var(--error);
  stroke-width: 2;
}

/* 工具提示 */
.task-tooltip {
  position: fixed;
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-md);
  padding: var(--space-md);
  box-shadow: var(--shadow-lg);
  z-index: 1000;
  min-width: 200px;
  pointer-events: none;
}

.tooltip-header {
  font-weight: 600;
  margin-bottom: var(--space-sm);
  color: var(--gray-900);
  border-bottom: 1px solid var(--gray-200);
  padding-bottom: var(--space-sm);
}

.tooltip-body {
  font-size: var(--text-sm);
  color: var(--gray-600);
  line-height: 1.6;
}

.tooltip-body div {
  margin-bottom: var(--space-xs);
}
</style>
