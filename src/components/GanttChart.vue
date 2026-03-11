<template>
  <div class="gantt-chart">
    <!-- 工具栏 -->
    <div class="gantt-toolbar">
      <div class="view-switcher">
        <button 
          class="btn btn-sm" 
          :class="{ 'btn-primary': viewMode === 'day' }"
          @click="viewMode = 'day'"
        >日</button>
        <button 
          class="btn btn-sm" 
          :class="{ 'btn-primary': viewMode === 'week' }"
          @click="viewMode = 'week'"
        >周</button>
        <button 
          class="btn btn-sm" 
          :class="{ 'btn-primary': viewMode === 'month' }"
          @click="viewMode = 'month'"
        >月</button>
      </div>
      <div class="toolbar-actions">
        <button class="btn btn-sm btn-outline" @click="scrollToToday">今天</button>
        <button class="btn btn-sm btn-outline" @click="zoomIn">放大</button>
        <button class="btn btn-sm btn-outline" @click="zoomOut">缩小</button>
        <button class="btn btn-sm btn-primary" @click="addTask">+ 添加任务</button>
      </div>
    </div>

    <div class="gantt-container">
      <!-- 任务列表 -->
      <div class="task-list-panel">
        <div class="task-list-header">
          <div class="task-header-cell">任务名称</div>
          <div class="task-header-cell" style="width: 100px;">开始日期</div>
          <div class="task-header-cell" style="width: 100px;">结束日期</div>
          <div class="task-header-cell" style="width: 80px;">进度</div>
          <div class="task-header-cell" style="width: 60px;">操作</div>
        </div>
        <div class="task-list-body" ref="taskListBody" @scroll="syncScroll">
          <div 
            v-for="task in visibleTasks" 
            :key="task.id"
            class="task-row"
            :class="{ 'is-expanded': task.expanded, 'is-group': task.isGroup }"
          >
            <div class="task-cell task-name-cell">
              <span 
                v-if="task.isGroup" 
                class="expand-toggle"
                @click="toggleExpand(task)"
              >
                {{ task.expanded ? '▼' : '▶' }}
              </span>
              <span class="task-icon" :style="{ color: task.color }">
                {{ task.isGroup ? '📁' : '📋' }}
              </span>
              <span class="task-name">{{ task.name }}</span>
            </div>
            <div class="task-cell">
              <input 
                type="date" 
                class="input input-sm"
                :value="formatDate(task.startDate)"
                @change="updateTaskDate(task, 'startDate', $event.target.value)"
              />
            </div>
            <div class="task-cell">
              <input 
                type="date" 
                class="input input-sm"
                :value="formatDate(task.endDate)"
                @change="updateTaskDate(task, 'endDate', $event.target.value)"
              />
            </div>
            <div class="task-cell">
              <div class="progress-bar-small">
                <div class="progress-fill" :style="{ width: task.progress + '%' }"></div>
              </div>
              <span class="progress-text">{{ task.progress }}%</span>
            </div>
            <div class="task-cell">
              <button class="btn btn-xs btn-outline" @click="deleteTask(task.id)">×</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 时间线图表 -->
      <div class="timeline-panel" ref="timelinePanel" @scroll="syncScroll">
        <!-- 时间刻度 -->
        <div class="timeline-header">
          <div class="timeline-scale-top">
            <div 
              v-for="(scale, index) in topScales" 
              :key="'top-' + index"
              class="scale-item-top"
              :style="{ width: cellWidth * scale.days + 'px', left: scale.left + 'px' }"
            >
              {{ scale.label }}
            </div>
          </div>
          <div class="timeline-scale-bottom">
            <div 
              v-for="(scale, index) in bottomScales" 
              :key="'bottom-' + index"
              class="scale-item-bottom"
              :style="{ width: cellWidth + 'px' }"
            >
              {{ scale.label }}
            </div>
          </div>
        </div>

        <!-- 网格背景 -->
        <div class="timeline-body" ref="timelineBody">
          <div class="grid-background">
            <div 
              v-for="(line, index) in gridLines" 
              :key="index"
              class="grid-line"
              :class="{ 'is-weekend': line.isWeekend, 'is-today': line.isToday }"
              :style="{ left: line.left + 'px' }"
            ></div>
          </div>

          <!-- 任务条 -->
          <div 
            v-for="task in visibleTasks" 
            :key="task.id + '-bar'"
            class="task-bar-wrapper"
            :style="{ top: (task._rowIndex * rowHeight) + 'px' }"
          >
            <div 
              v-if="!task.isGroup"
              class="task-bar"
              :class="{ 'is-dragging': draggingTaskId === task.id }"
              :style="{
                left: getTaskLeft(task) + 'px',
                width: getTaskWidth(task) + 'px',
                backgroundColor: task.color
              }"
              @mousedown="startDragTask($event, task)"
            >
              <div class="task-bar-progress" :style="{ width: task.progress + '%' }"></div>
              <div class="task-bar-label">{{ task.name }}</div>
              <div 
                class="task-bar-handle task-bar-handle-left"
                @mousedown.stop="startResizeTask($event, task, 'left')"
              ></div>
              <div 
                class="task-bar-handle task-bar-handle-right"
                @mousedown.stop="startResizeTask($event, task, 'right')"
              ></div>
            </div>
            <div 
              v-else
              class="group-bar"
              :style="{
                left: getTaskLeft(task) + 'px',
                width: getTaskWidth(task) + 'px'
              }"
            >
              <div class="group-bar-line" :style="{ backgroundColor: task.color }"></div>
            </div>
          </div>

          <!-- 今天标记线 -->
          <div class="today-marker" :style="{ left: todayPosition + 'px' }">
            <div class="today-label">今天</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加任务弹窗 -->
    <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
      <div class="modal">
        <div class="modal-header">
          <h3>添加新任务</h3>
          <button class="btn btn-sm btn-outline" @click="showAddModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>任务名称</label>
            <input 
              v-model="newTask.name" 
              type="text" 
              class="input" 
              placeholder="请输入任务名称"
            />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>开始日期</label>
              <input 
                v-model="newTask.startDate" 
                type="date" 
                class="input"
              />
            </div>
            <div class="form-group">
              <label>结束日期</label>
              <input 
                v-model="newTask.endDate" 
                type="date" 
                class="input"
              />
            </div>
          </div>
          <div class="form-group">
            <label>进度 (%)</label>
            <input 
              v-model.number="newTask.progress" 
              type="number" 
              class="input" 
              min="0" 
              max="100"
            />
          </div>
          <div class="form-group">
            <label>任务颜色</label>
            <div class="color-picker">
              <button 
                v-for="color in presetColors" 
                :key="color"
                class="color-btn"
                :class="{ 'is-active': newTask.color === color }"
                :style="{ backgroundColor: color }"
                @click="newTask.color = color"
              ></button>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="showAddModal = false">取消</button>
          <button class="btn btn-primary" @click="confirmAddTask">确认添加</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  tasks: {
    type: Array,
    default: () => []
  },
  startDate: {
    type: String,
    default: null
  },
  endDate: {
    type: String,
    default: null
  },
  rowHeight: {
    type: Number,
    default: 44
  },
  cellWidth: {
    type: Number,
    default: 40
  }
})

const emit = defineEmits(['update:tasks', 'task-change', 'task-click'])

// 响应式数据
const viewMode = ref('day')
const showAddModal = ref(false)
const draggingTaskId = ref(null)
const dragStartPos = ref({ x: 0, y: 0 })
const dragStartTask = ref(null)
const resizingTask = ref(null)
const resizeDirection = ref('')
const zoomLevel = ref(1)

const taskListBody = ref(null)
const timelinePanel = ref(null)
const timelineBody = ref(null)

const presetColors = [
  '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
  '#ec4899', '#06b6d4', '#84cc16', '#f97316', '#6366f1'
]

const newTask = reactive({
  name: '',
  startDate: formatDate(new Date()),
  endDate: formatDate(new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)),
  progress: 0,
  color: '#3b82f6',
  isGroup: false
})

// 默认任务数据
const defaultTasks = ref([
  {
    id: 'group-1',
    name: '项目规划',
    startDate: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    endDate: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000),
    progress: 100,
    color: '#3b82f6',
    isGroup: true,
    expanded: true,
    children: [
      {
        id: 'task-1',
        name: '需求分析',
        startDate: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
        endDate: new Date(Date.now() + 1 * 24 * 60 * 60 * 1000),
        progress: 100,
        color: '#3b82f6',
        isGroup: false
      },
      {
        id: 'task-2',
        name: '技术选型',
        startDate: new Date(Date.now()),
        endDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
        progress: 80,
        color: '#10b981',
        isGroup: false
      }
    ]
  },
  {
    id: 'group-2',
    name: '开发阶段',
    startDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
    endDate: new Date(Date.now() + 20 * 24 * 60 * 60 * 1000),
    progress: 30,
    color: '#f59e0b',
    isGroup: true,
    expanded: true,
    children: [
      {
        id: 'task-3',
        name: '前端开发',
        startDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
        endDate: new Date(Date.now() + 12 * 24 * 60 * 60 * 1000),
        progress: 40,
        color: '#8b5cf6',
        isGroup: false
      },
      {
        id: 'task-4',
        name: '后端开发',
        startDate: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000),
        endDate: new Date(Date.now() + 15 * 24 * 60 * 60 * 1000),
        progress: 20,
        color: '#ec4899',
        isGroup: false
      },
      {
        id: 'task-5',
        name: '接口联调',
        startDate: new Date(Date.now() + 12 * 24 * 60 * 60 * 1000),
        endDate: new Date(Date.now() + 20 * 24 * 60 * 60 * 1000),
        progress: 0,
        color: '#06b6d4',
        isGroup: false
      }
    ]
  },
  {
    id: 'task-6',
    name: '测试与部署',
    startDate: new Date(Date.now() + 18 * 24 * 60 * 60 * 1000),
    endDate: new Date(Date.now() + 25 * 24 * 60 * 60 * 1000),
    progress: 0,
    color: '#f97316',
    isGroup: false
  }
])

const tasks = ref(props.tasks.length > 0 ? props.tasks : defaultTasks.value)

// 计算可见任务（扁平化）
const visibleTasks = computed(() => {
  const result = []
  let rowIndex = 0
  
  const flatten = (taskList) => {
    for (const task of taskList) {
      task._rowIndex = rowIndex++
      result.push(task)
      if (task.isGroup && task.expanded && task.children) {
        flatten(task.children)
      }
    }
  }
  
  flatten(tasks.value)
  return result
})

// 计算日期范围
const dateRange = computed(() => {
  let minDate = new Date()
  let maxDate = new Date()
  
  if (props.startDate && props.endDate) {
    minDate = new Date(props.startDate)
    maxDate = new Date(props.endDate)
  } else {
    const allDates = []
    const collectDates = (taskList) => {
      for (const task of taskList) {
        allDates.push(new Date(task.startDate), new Date(task.endDate))
        if (task.children) collectDates(task.children)
      }
    }
    collectDates(visibleTasks.value)
    
    if (allDates.length > 0) {
      minDate = new Date(Math.min(...allDates))
      maxDate = new Date(Math.max(...allDates))
    }
    
    // 添加缓冲
    minDate.setDate(minDate.getDate() - 7)
    maxDate.setDate(maxDate.getDate() + 14)
  }
  
  // 确保最小日期是周一
  const day = minDate.getDay()
  const diff = minDate.getDate() - day + (day === 0 ? -6 : 1)
  minDate = new Date(minDate.setDate(diff))
  
  return { minDate, maxDate }
})

// 计算总天数
const totalDays = computed(() => {
  return Math.ceil((dateRange.value.maxDate - dateRange.value.minDate) / (1000 * 60 * 60 * 24))
})

// 顶部刻度（月/周）
const topScales = computed(() => {
  const scales = []
  const current = new Date(dateRange.value.minDate)
  
  while (current <= dateRange.value.maxDate) {
    if (viewMode.value === 'month') {
      const monthStart = new Date(current.getFullYear(), current.getMonth(), 1)
      const monthEnd = new Date(current.getFullYear(), current.getMonth() + 1, 0)
      const days = Math.ceil((monthEnd - monthStart) / (1000 * 60 * 60 * 24)) + 1
      const left = (monthStart - dateRange.value.minDate) / (1000 * 60 * 60 * 24) * cellWidth.value
      
      scales.push({
        label: `${current.getFullYear()}年${current.getMonth() + 1}月`,
        days,
        left
      })
      
      current.setMonth(current.getMonth() + 1)
    } else {
      // 周视图
      const weekStart = new Date(current)
      const weekEnd = new Date(current)
      weekEnd.setDate(weekEnd.getDate() + 6)
      
      const left = (weekStart - dateRange.value.minDate) / (1000 * 60 * 60 * 24) * cellWidth.value
      
      scales.push({
        label: `第${getWeekNumber(current)}周`,
        days: 7,
        left
      })
      
      current.setDate(current.getDate() + 7)
    }
  }
  
  return scales
})

// 底部刻度（日）
const bottomScales = computed(() => {
  const scales = []
  const current = new Date(dateRange.value.minDate)
  
  while (current <= dateRange.value.maxDate) {
    if (viewMode.value === 'day') {
      scales.push({
        label: current.getDate(),
        date: new Date(current)
      })
      current.setDate(current.getDate() + 1)
    } else if (viewMode.value === 'week') {
      scales.push({
        label: ['一', '二', '三', '四', '五', '六', '日'][current.getDay() === 0 ? 6 : current.getDay() - 1],
        date: new Date(current)
      })
      current.setDate(current.getDate() + 1)
    } else {
      // 月视图显示周
      scales.push({
        label: current.getDate(),
        date: new Date(current)
      })
      current.setDate(current.getDate() + 1)
    }
  }
  
  return scales
})

// 网格线
const gridLines = computed(() => {
  const lines = []
  const current = new Date(dateRange.value.minDate)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  let index = 0
  while (current <= dateRange.value.maxDate) {
    const dateCopy = new Date(current)
    const isToday = dateCopy.toDateString() === today.toDateString()
    const isWeekend = current.getDay() === 0 || current.getDay() === 6
    
    lines.push({
      left: index * cellWidth.value,
      isWeekend,
      isToday
    })
    
    current.setDate(current.getDate() + 1)
    index++
  }
  
  return lines
})

// 今天的位置
const todayPosition = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const diff = (today - dateRange.value.minDate) / (1000 * 60 * 60 * 24)
  return diff * cellWidth.value
})

// 计算单元格宽度
const cellWidth = computed(() => {
  const base = props.cellWidth * zoomLevel.value
  if (viewMode.value === 'month') return base * 0.5
  if (viewMode.value === 'week') return base
  return base * 1.5
})

// 辅助函数
function formatDate(date) {
  if (!date) return ''
  const d = new Date(date)
  return d.toISOString().split('T')[0]
}

function getWeekNumber(date) {
  const d = new Date(date)
  d.setHours(0, 0, 0, 0)
  d.setDate(d.getDate() + 4 - (d.getDay() || 7))
  const yearStart = new Date(d.getFullYear(), 0, 1)
  return Math.ceil(((d - yearStart) / 86400000 + 1) / 7)
}

// 获取任务左边位置
function getTaskLeft(task) {
  const start = new Date(task.startDate)
  start.setHours(0, 0, 0, 0)
  const diff = (start - dateRange.value.minDate) / (1000 * 60 * 60 * 24)
  return Math.max(0, diff * cellWidth.value)
}

// 获取任务宽度
function getTaskWidth(task) {
  const start = new Date(task.startDate)
  const end = new Date(task.endDate)
  start.setHours(0, 0, 0, 0)
  end.setHours(0, 0, 0, 0)
  const diff = (end - start) / (1000 * 60 * 60 * 24) + 1
  return Math.max(20, diff * cellWidth.value - 4)
}

// 展开/折叠
function toggleExpand(task) {
  task.expanded = !task.expanded
}

// 滚动到今天
function scrollToToday() {
  if (timelinePanel.value) {
    timelinePanel.value.scrollLeft = todayPosition.value - 200
  }
}

// 缩放
function zoomIn() {
  zoomLevel.value = Math.min(2, zoomLevel.value + 0.2)
}

function zoomOut() {
  zoomLevel.value = Math.max(0.5, zoomLevel.value - 0.2)
}

// 同步滚动
function syncScroll(e) {
  if (e.target === taskListBody.value) {
    timelineBody.value.scrollTop = taskListBody.value.scrollTop
  } else if (e.target === timelinePanel.value) {
    taskListBody.value.scrollTop = timelinePanel.value.scrollTop
  }
}

// 任务拖拽
function startDragTask(e, task) {
  e.preventDefault()
  draggingTaskId.value = task.id
  dragStartPos.value = { x: e.clientX, y: e.clientY }
  dragStartTask.value = { 
    startDate: new Date(task.startDate),
    endDate: new Date(task.endDate)
  }
  
  document.addEventListener('mousemove', onDragTask)
  document.addEventListener('mouseup', stopDragTask)
}

function onDragTask(e) {
  if (!draggingTaskId.value || !dragStartTask.value) return
  
  const task = findTask(draggingTaskId.value)
  if (!task) return
  
  const deltaX = e.clientX - dragStartPos.value.x
  const deltaDays = Math.round(deltaX / cellWidth.value)
  
  if (deltaDays !== 0) {
    const newStart = new Date(dragStartTask.value.startDate)
    const newEnd = new Date(dragStartTask.value.endDate)
    newStart.setDate(newStart.getDate() + deltaDays)
    newEnd.setDate(newEnd.getDate() + deltaDays)
    
    task.startDate = newStart
    task.endDate = newEnd
  }
}

function stopDragTask() {
  draggingTaskId.value = null
  dragStartTask.value = null
  document.removeEventListener('mousemove', onDragTask)
  document.removeEventListener('mouseup', stopDragTask)
  emitChange()
}

// 调整任务大小
function startResizeTask(e, task, direction) {
  e.preventDefault()
  e.stopPropagation()
  
  resizingTask.value = task
  resizeDirection.value = direction
  dragStartPos.value = { x: e.clientX, y: e.clientY }
  dragStartTask.value = { 
    startDate: new Date(task.startDate),
    endDate: new Date(task.endDate)
  }
  
  document.addEventListener('mousemove', onResizeTask)
  document.addEventListener('mouseup', stopResizeTask)
}

function onResizeTask(e) {
  if (!resizingTask.value || !dragStartTask.value) return
  
  const deltaX = e.clientX - dragStartPos.value.x
  const deltaDays = Math.round(deltaX / cellWidth.value)
  
  if (resizeDirection.value === 'right') {
    const newEnd = new Date(dragStartTask.value.endDate)
    newEnd.setDate(newEnd.getDate() + deltaDays)
    if (newEnd > resizingTask.value.startDate) {
      resizingTask.value.endDate = newEnd
    }
  } else {
    const newStart = new Date(dragStartTask.value.startDate)
    newStart.setDate(newStart.getDate() + deltaDays)
    if (newStart < resizingTask.value.endDate) {
      resizingTask.value.startDate = newStart
    }
  }
}

function stopResizeTask() {
  resizingTask.value = null
  dragStartTask.value = null
  document.removeEventListener('mousemove', onResizeTask)
  document.removeEventListener('mouseup', stopResizeTask)
  emitChange()
}

// 查找任务
function findTask(id, taskList = tasks.value) {
  for (const task of taskList) {
    if (task.id === id) return task
    if (task.children) {
      const found = findTask(id, task.children)
      if (found) return found
    }
  }
  return null
}

// 更新任务日期
function updateTaskDate(task, field, value) {
  task[field] = new Date(value)
  emitChange()
}

// 添加任务
function addTask() {
  newTask.name = ''
  newTask.startDate = formatDate(new Date())
  newTask.endDate = formatDate(new Date(Date.now() + 7 * 24 * 60 * 60 * 1000))
  newTask.progress = 0
  newTask.color = '#3b82f6'
  showAddModal.value = true
}

function confirmAddTask() {
  const task = {
    id: 'task-' + Date.now(),
    name: newTask.name,
    startDate: new Date(newTask.startDate),
    endDate: new Date(newTask.endDate),
    progress: newTask.progress,
    color: newTask.color,
    isGroup: false
  }
  
  tasks.value.push(task)
  showAddModal.value = false
  emitChange()
}

// 删除任务
function deleteTask(id) {
  const removeFromList = (list) => {
    for (let i = 0; i < list.length; i++) {
      if (list[i].id === id) {
        list.splice(i, 1)
        return true
      }
      if (list[i].children) {
        if (removeFromList(list[i].children)) {
          if (list[i].children.length === 0) {
            list[i].isGroup = false
          }
          return true
        }
      }
    }
    return false
  }
  
  removeFromList(tasks.value)
  emitChange()
}

function emitChange() {
  emit('update:tasks', tasks.value)
  emit('task-change', tasks.value)
}

// 更新分组任务的日期范围
watch(visibleTasks, () => {
  const updateGroupDates = (groups) => {
    for (const group of groups) {
      if (group.isGroup && group.children) {
        updateGroupDates(group.children)
        
        let minDate = new Date()
        let maxDate = new Date(0)
        let totalProgress = 0
        
        for (const child of group.children) {
          const start = new Date(child.startDate)
          const end = new Date(child.endDate)
          if (start < minDate) minDate = start
          if (end > maxDate) maxDate = end
          totalProgress += child.progress
        }
        
        group.startDate = minDate
        group.endDate = maxDate
        group.progress = Math.round(totalProgress / group.children.length)
      }
    }
  }
  
  updateGroupDates(tasks.value)
}, { deep: true })

onUnmounted(() => {
  document.removeEventListener('mousemove', onDragTask)
  document.removeEventListener('mouseup', stopDragTask)
  document.removeEventListener('mousemove', onResizeTask)
  document.removeEventListener('mouseup', stopResizeTask)
})

defineExpose({
  tasks,
  addTask,
  deleteTask,
  scrollToToday
})
</script>

<style scoped>
.gantt-chart {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-lg);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.gantt-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-md) var(--space-lg);
  background: var(--gray-50);
  border-bottom: 1px solid var(--gray-200);
}

.view-switcher {
  display: flex;
  gap: var(--space-xs);
}

.toolbar-actions {
  display: flex;
  gap: var(--space-sm);
}

.gantt-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 任务列表 */
.task-list-panel {
  width: 400px;
  border-right: 1px solid var(--gray-200);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.task-list-header {
  display: flex;
  background: var(--gray-100);
  border-bottom: 1px solid var(--gray-200);
  font-weight: 600;
  font-size: var(--text-sm);
  color: var(--gray-700);
}

.task-header-cell {
  padding: var(--space-sm) var(--space-md);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.task-list-body {
  flex: 1;
  overflow: auto;
}

.task-row {
  display: flex;
  border-bottom: 1px solid var(--gray-100);
  height: 44px;
  align-items: center;
}

.task-row.is-group {
  background: var(--gray-50);
  font-weight: 500;
}

.task-row:hover {
  background: var(--primary-50);
}

.task-cell {
  padding: var(--space-xs) var(--space-sm);
  flex: 1;
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: var(--text-sm);
}

.task-name-cell {
  padding-left: var(--space-md);
}

.expand-toggle {
  cursor: pointer;
  width: 20px;
  text-align: center;
  color: var(--gray-500);
  user-select: none;
}

.task-icon {
  font-size: 14px;
}

.task-name {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.input-sm {
  padding: var(--space-xs) var(--space-sm);
  font-size: var(--text-xs);
}

.progress-bar-small {
  width: 50px;
  height: 6px;
  background: var(--gray-200);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--success);
  transition: width 0.2s;
}

.progress-text {
  font-size: var(--text-xs);
  color: var(--gray-600);
  min-width: 30px;
}

/* 时间线面板 */
.timeline-panel {
  flex: 1;
  overflow: auto;
  position: relative;
}

.timeline-header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: white;
  border-bottom: 1px solid var(--gray-200);
}

.timeline-scale-top {
  display: flex;
  position: relative;
  height: 30px;
  background: var(--gray-100);
  border-bottom: 1px solid var(--gray-200);
}

.scale-item-top {
  position: absolute;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--gray-700);
  border-right: 1px solid var(--gray-200);
}

.timeline-scale-bottom {
  display: flex;
  height: 24px;
  background: var(--gray-50);
}

.scale-item-bottom {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-xs);
  color: var(--gray-600);
  border-right: 1px solid var(--gray-200);
  flex-shrink: 0;
}

.timeline-body {
  position: relative;
  min-height: calc(100% - 54px);
}

.grid-background {
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
  width: 1px;
  background: var(--gray-100);
}

.grid-line.is-weekend {
  background: var(--gray-200);
  width: 2px;
}

.grid-line.is-today {
  background: var(--danger);
  width: 2px;
}

.task-bar-wrapper {
  position: absolute;
  left: 0;
  right: 0;
  height: 44px;
  padding: 6px 8px;
  box-sizing: border-box;
}

.task-bar {
  position: absolute;
  height: 32px;
  border-radius: var(--radius-md);
  cursor: move;
  display: flex;
  align-items: center;
  padding: 0 var(--space-sm);
  box-shadow: var(--shadow);
  transition: box-shadow 0.2s, transform 0.1s;
  overflow: hidden;
  min-width: 40px;
}

.task-bar:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.task-bar.is-dragging {
  opacity: 0.8;
  box-shadow: var(--shadow-lg);
  z-index: 100;
}

.task-bar-progress {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background: rgba(0, 0, 0, 0.2);
  pointer-events: none;
}

.task-bar-label {
  color: white;
  font-size: var(--text-sm);
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  position: relative;
  z-index: 1;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.task-bar-handle {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 12px;
  cursor: ew-resize;
  opacity: 0;
  transition: opacity 0.2s;
}

.task-bar:hover .task-bar-handle {
  opacity: 1;
}

.task-bar-handle-left {
  left: 0;
  border-radius: var(--radius-md) 0 0 var(--radius-md);
}

.task-bar-handle-right {
  right: 0;
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
}

.task-bar-handle:hover {
  background: rgba(255, 255, 255, 0.3);
}

.group-bar {
  position: absolute;
  height: 32px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.group-bar-line {
  height: 4px;
  border-radius: 2px;
  position: relative;
}

.group-bar-line::before,
.group-bar-line::after {
  content: '';
  position: absolute;
  width: 8px;
  height: 8px;
  border: 3px solid currentColor;
  border-radius: 50%;
  top: 50%;
  transform: translateY(-50%);
}

.group-bar-line::before {
  left: -4px;
}

.group-bar-line::after {
  right: -4px;
}

.today-marker {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--danger);
  z-index: 50;
  pointer-events: none;
}

.today-label {
  position: sticky;
  top: 55px;
  left: 2px;
  background: var(--danger);
  color: white;
  font-size: var(--text-xs);
  padding: 2px 6px;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  white-space: nowrap;
}

/* 弹窗 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: var(--radius-lg);
  width: 90%;
  max-width: 500px;
  box-shadow: var(--shadow-xl);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-lg);
  border-bottom: 1px solid var(--gray-200);
}

.modal-header h3 {
  margin: 0;
  font-size: var(--text-lg);
}

.modal-body {
  padding: var(--space-lg);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-sm);
  padding: var(--space-lg);
  border-top: 1px solid var(--gray-200);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
}

.color-picker {
  display: flex;
  gap: var(--space-sm);
  flex-wrap: wrap;
}

.color-btn {
  width: 32px;
  height: 32px;
  border: 3px solid transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: transform 0.2s;
}

.color-btn:hover {
  transform: scale(1.1);
}

.color-btn.is-active {
  border-color: var(--gray-800);
}

.btn-xs {
  padding: var(--space-xs);
  font-size: var(--text-xs);
  line-height: 1;
}
</style>