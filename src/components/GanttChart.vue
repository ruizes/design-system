<template>
  <div class="gantt-chart">
    <!-- 头部信息 -->
    <div class="gantt-header">
      <div class="gantt-title">
        <slot name="title">
          <h3>项目进度甘特图</h3>
        </slot>
      </div>
      <div class="gantt-legend">
        <div
          v-for="status in statusList"
          :key="status.value"
          class="legend-item"
        >
          <span
            class="legend-color"
            :style="{ background: status.color }"
          />
          <span class="legend-label">{{ status.label }}</span>
        </div>
      </div>
    </div>

    <!-- 甘特图主体 -->
    <div class="gantt-body">
      <!-- 左侧任务列表 -->
      <div class="gantt-sidebar" :style="{ width: `${sidebarWidth}px` }">
        <div class="sidebar-header">
          <span>任务名称</span>
        </div>
        <div class="sidebar-content">
          <div
            v-for="task in tasks"
            :key="task.id"
            class="task-row"
            :style="{ height: `${rowHeight}px` }"
          >
            <div class="task-info">
              <span class="task-name">{{ task.name }}</span>
              <span
                v-if="task.progress !== undefined"
                class="task-progress"
              >{{ task.progress }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧时间轴 -->
      <div ref="timelineRef" class="gantt-timeline" @scroll="handleScroll">
        <!-- 时间刻度 -->
        <div class="timeline-header">
          <div
            v-for="(date, index) in dateRange"
            :key="index"
            class="date-cell"
            :style="{ width: `${dayWidth}px` }"
            :class="{ 'is-weekend': date.isWeekend, 'is-today': date.isToday }"
          >
            <div class="date-day">{{ date.day }}</div>
            <div class="date-week">{{ date.weekDay }}</div>
          </div>
        </div>

        <!-- 时间网格和任务条 -->
        <div class="timeline-content">
          <!-- 网格背景 -->
          <div class="timeline-grid">
            <div
              v-for="(date, index) in dateRange"
              :key="`grid-${index}`"
              class="grid-column"
              :style="{ width: `${dayWidth}px` }"
              :class="{ 'is-weekend': date.isWeekend, 'is-today': date.isToday }"
            />
          </div>

          <!-- 今天标记线 -->
          <div
            v-if="todayPosition >= 0"
            class="today-line"
            :style="{ left: `${todayPosition}px` }"
          >
            <span class="today-label">今天</span>
          </div>

          <!-- 任务条 -->
          <div class="task-bars">
            <div
              v-for="(task, index) in tasksWithPosition"
              :key="`bar-${task.id}`"
              class="task-bar-wrapper"
              :style="{
                top: `${index * rowHeight}px`,
                height: `${rowHeight}px`
              }"
            >
              <div
                class="task-bar"
                :class="`status-${task.status}`"
                :style="{
                  left: `${task.left}px`,
                  width: `${task.width}px`,
                  background: getStatusColor(task.status)
                }"
                @click="handleTaskClick(task)"
              >
                <!-- 进度条 -->
                <div
                  v-if="task.progress !== undefined"
                  class="task-progress-bar"
                  :style="{ width: `${task.progress}%` }"
                />

                <!-- 任务标签 -->
                <span class="task-bar-label">{{ task.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部工具栏 -->
    <div class="gantt-footer">
      <slot name="footer">
        <div class="gantt-stats">
          <span>总任务: {{ tasks.length }}</span>
          <span>已完成: {{ completedTasks }}</span>
          <span>进行中: {{ inProgressTasks }}</span>
        </div>
      </slot>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  tasks: {
    type: Array,
    default: () => []
  },
  dependencies: {
    type: Array,
    default: () => []
  },
  startDate: {
    type: String,
    default: () => {
      const now = new Date()
      return new Date(now.getFullYear(), now.getMonth(), 1).toISOString().split('T')[0]
    }
  },
  endDate: {
    type: String,
    default: () => {
      const now = new Date()
      return new Date(now.getFullYear(), now.getMonth() + 1, 0).toISOString().split('T')[0]
    }
  },
  dayWidth: {
    type: Number,
    default: 50
  },
  rowHeight: {
    type: Number,
    default: 48
  },
  sidebarWidth: {
    type: Number,
    default: 200
  },
  showDependencies: {
    type: Boolean,
    default: true
  },
  draggable: {
    type: Boolean,
    default: false
  },
  statusColors: {
    type: Object,
    default: () => ({
      todo: '#94a3b8',
      inprogress: '#3b82f6',
      done: '#10b981',
      delay: '#ef4444'
    })
  }
})

const emit = defineEmits(['taskClick', 'taskUpdate'])

const timelineRef = ref(null)

// 状态列表
const statusList = [
  { value: 'todo', label: '待办', color: props.statusColors.todo },
  { value: 'inprogress', label: '进行中', color: props.statusColors.inprogress },
  { value: 'done', label: '已完成', color: props.statusColors.done },
  { value: 'delay', label: '延期', color: props.statusColors.delay }
]

// 解析日期
const parseDate = (dateStr) => {
  if (!dateStr) return new Date()
  return new Date(dateStr)
}

// 格式化日期
const formatDate = (date) => {
  return date.toISOString().split('T')[0]
}

// 获取日期差（天数）
const getDaysDiff = (date1, date2) => {
  const d1 = new Date(date1)
  const d2 = new Date(date2)
  const diffTime = d2 - d1
  return Math.floor(diffTime / (1000 * 60 * 60 * 24))
}

// 添加天数
const addDays = (date, days) => {
  const result = new Date(date)
  result.setDate(result.getDate() + days)
  return result
}

// 判断是否是周末
const isWeekend = (date) => {
  const day = date.getDay()
  return day === 0 || day === 6
}

// 判断是否是今天
const isToday = (date) => {
  const today = new Date()
  return date.getDate() === today.getDate() &&
         date.getMonth() === today.getMonth() &&
         date.getFullYear() === today.getFullYear()
}

// 获取星期几
const getWeekDay = (date) => {
  const days = ['日', '一', '二', '三', '四', '五', '六']
  return days[date.getDay()]
}

// 计算日期范围
const dateRange = computed(() => {
  const start = parseDate(props.startDate)
  const end = parseDate(props.endDate)
  const dates = []

  let current = new Date(start)
  const endTime = end.getTime()

  while (current.getTime() <= endTime) {
    dates.push({
      date: formatDate(current),
      day: current.getDate(),
      weekDay: getWeekDay(current),
      isWeekend: isWeekend(current),
      isToday: isToday(current)
    })
    current = addDays(current, 1)
  }

  return dates
})

// 计算今天位置
const todayPosition = computed(() => {
  const today = new Date()
  const start = parseDate(props.startDate)
  const end = parseDate(props.endDate)

  if (today < start || today > end) {
    return -1
  }

  const daysDiff = getDaysDiff(start, today)
  return daysDiff * props.dayWidth
})

// 计算任务位置
const tasksWithPosition = computed(() => {
  const start = parseDate(props.startDate)

  return props.tasks.map((task) => {
    const taskStart = parseDate(task.startDate)
    const taskEnd = parseDate(task.endDate)

    const startDiff = getDaysDiff(start, taskStart)
    const duration = getDaysDiff(taskStart, taskEnd) + 1

    return {
      ...task,
      left: startDiff * props.dayWidth,
      width: Math.max(duration * props.dayWidth, props.dayWidth)
    }
  })
})

// 统计
const completedTasks = computed(() =>
  props.tasks.filter(t => t.status === 'done').length
)

const inProgressTasks = computed(() =>
  props.tasks.filter(t => t.status === 'inprogress').length
)

// 获取状态颜色
const getStatusColor = (status) => {
  return props.statusColors[status] || props.statusColors.todo
}

// 处理任务点击
const handleTaskClick = (task) => {
  emit('taskClick', task)
}

// 处理滚动
const handleScroll = () => {
  // 可以在这里处理同步滚动
}
</script>

<style scoped>
.gantt-chart {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.gantt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-lg) var(--space-xl);
  border-bottom: 1px solid var(--gray-200);
}

.gantt-title h3 {
  margin: 0;
  font-size: var(--text-lg);
  color: var(--gray-900);
}

.gantt-legend {
  display: flex;
  gap: var(--space-lg);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: var(--radius-sm);
}

.legend-label {
  font-size: var(--text-sm);
  color: var(--gray-600);
}

.gantt-body {
  display: flex;
  overflow: hidden;
}

.gantt-sidebar {
  flex-shrink: 0;
  border-right: 1px solid var(--gray-200);
  background: var(--gray-50);
}

.sidebar-header {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 var(--space-lg);
  font-weight: 600;
  color: var(--gray-700);
  border-bottom: 1px solid var(--gray-200);
}

.sidebar-content {
  overflow: hidden;
}

.task-row {
  display: flex;
  align-items: center;
  padding: 0 var(--space-lg);
  border-bottom: 1px solid var(--gray-100);
}

.task-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.task-name {
  font-size: var(--text-sm);
  color: var(--gray-800);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.task-progress {
  font-size: var(--text-xs);
  color: var(--gray-500);
  margin-left: var(--space-sm);
}

.gantt-timeline {
  flex: 1;
  overflow: auto;
}

.timeline-header {
  display: flex;
  height: 60px;
  border-bottom: 1px solid var(--gray-200);
  background: var(--gray-50);
}

.date-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-right: 1px solid var(--gray-100);
  flex-shrink: 0;
}

.date-cell.is-weekend {
  background: var(--gray-100);
}

.date-cell.is-today {
  background: rgba(59, 130, 246, 0.1);
}

.date-day {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--gray-800);
}

.date-week {
  font-size: var(--text-xs);
  color: var(--gray-500);
}

.timeline-content {
  position: relative;
  min-height: 200px;
}

.timeline-grid {
  display: flex;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.grid-column {
  border-right: 1px solid var(--gray-100);
  flex-shrink: 0;
}

.grid-column.is-weekend {
  background: var(--gray-50);
}

.grid-column.is-today {
  background: rgba(59, 130, 246, 0.05);
}

.today-line {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #ef4444;
  z-index: 10;
}

.today-label {
  position: absolute;
  top: 4px;
  left: 50%;
  transform: translateX(-50%);
  font-size: var(--text-xs);
  color: #ef4444;
  background: white;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  white-space: nowrap;
}

.task-bars {
  position: relative;
  padding: var(--space-sm) 0;
}

.task-bar-wrapper {
  position: relative;
  padding: var(--space-xs) 0;
}

.task-bar {
  position: absolute;
  height: 32px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  padding: 0 var(--space-sm);
  cursor: pointer;
  transition: all 0.2s ease;
  overflow: hidden;
}

.task-bar:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.task-progress-bar {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: rgba(255, 255, 255, 0.3);
}

.task-bar-label {
  position: relative;
  z-index: 1;
  font-size: var(--text-xs);
  color: white;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.gantt-footer {
  padding: var(--space-md) var(--space-xl);
  border-top: 1px solid var(--gray-200);
  background: var(--gray-50);
}

.gantt-stats {
  display: flex;
  gap: var(--space-xl);
  font-size: var(--text-sm);
  color: var(--gray-600);
}
</style>
