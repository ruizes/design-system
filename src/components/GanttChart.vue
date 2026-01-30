<template>
  <div class="gantt-chart">
    <div class="gantt-header">
      <div class="gantt-title">
        <h3>{{ title }}</h3>
        <div class="gantt-controls">
          <button class="btn btn-sm btn-outline" @click="zoomIn">放大</button>
          <button class="btn btn-sm btn-outline" @click="zoomOut">缩小</button>
          <button class="btn btn-sm btn-outline" @click="resetZoom">重置</button>
        </div>
      </div>
    </div>

    <div class="gantt-body">
      <div class="gantt-sidebar">
        <div class="gantt-sidebar-header">
          <span>任务</span>
        </div>
        <div class="gantt-tasks-list">
          <div
            v-for="task in tasks"
            :key="task.id"
            class="gantt-task-row"
            :style="{ paddingLeft: `${task.level * 20}px` }"
          >
            <span class="task-name">{{ task.name }}</span>
            <span class="task-duration">{{ formatDuration(task) }}</span>
          </div>
        </div>
      </div>

      <div class="gantt-timeline-container" ref="timelineRef">
        <div class="gantt-timeline-header">
          <div class="gantt-months-row">
            <div
              v-for="month in months"
              :key="month.key"
              class="gantt-month"
              :style="{ width: `${month.width * zoom}px` }"
            >
              {{ month.label }}
            </div>
          </div>
          <div class="gantt-days-row">
            <div
              v-for="day in days"
              :key="day.key"
              class="gantt-day"
              :style="{ width: `${dayWidth * zoom}px` }"
              :class="{ 'gantt-day-weekend': day.isWeekend }"
            >
              {{ day.label }}
            </div>
          </div>
        </div>

        <div class="gantt-timeline-body">
          <div class="gantt-grid">
            <div
              v-for="(day, index) in days"
              :key="`grid-${index}`"
              class="gantt-grid-line"
              :style="{ left: `${index * dayWidth * zoom}px`, width: `${dayWidth * zoom}px` }"
              :class="{ 'gantt-grid-weekend': day.isWeekend }"
            ></div>
          </div>

          <div class="gantt-bars-container">
            <div
              v-for="task in tasks"
              :key="`bar-${task.id}`"
              class="gantt-bar-row"
            >
              <div
                class="gantt-bar"
                :class="{
                  'gantt-bar-milestone': task.isMilestone,
                  'gantt-bar-summary': task.isSummary
                }"
                :style="getBarStyle(task)"
                @mousedown="startDragBar($event, task)"
              >
                <div class="gantt-bar-progress" v-if="task.progress !== undefined" :style="{ width: `${task.progress}%` }"></div>
                <span class="gantt-bar-label">{{ task.name }}</span>
                <div
                  v-if="!task.isMilestone && !task.isSummary"
                  class="gantt-bar-handle gantt-bar-handle-left"
                  @mousedown.stop="startResizeBar($event, task, 'left')"
                ></div>
                <div
                  v-if="!task.isMilestone && !task.isSummary"
                  class="gantt-bar-handle gantt-bar-handle-right"
                  @mousedown.stop="startResizeBar($event, task, 'right')"
                ></div>
              </div>
            </div>
          </div>

          <svg class="gantt-dependencies">
            <path
              v-for="dependency in dependencies"
              :key="dependency.id"
              :d="getDependencyPath(dependency)"
              class="gantt-dependency-line"
              fill="none"
              stroke="var(--gray-400)"
              stroke-width="2"
              marker-end="url(#arrowhead)"
            />
            <defs>
              <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="var(--gray-400)" />
              </marker>
            </defs>
          </svg>
        </div>
      </div>
    </div>

    <div class="gantt-tooltip" v-if="tooltipVisible" :style="tooltipStyle">
      <div class="tooltip-title">{{ tooltipTask?.name }}</div>
      <div class="tooltip-dates">{{ formatDateRange(tooltipTask) }}</div>
      <div class="tooltip-progress" v-if="tooltipTask?.progress !== undefined">
        进度: {{ tooltipTask.progress }}%
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  title: {
    type: String,
    default: '项目甘特图'
  },
  tasks: {
    type: Array,
    required: true
  },
  dependencies: {
    type: Array,
    default: () => []
  },
  startDate: {
    type: String,
    default: () => new Date().toISOString().split('T')[0]
  },
  endDate: {
    type: String,
    default: () => {
      const date = new Date();
      date.setMonth(date.getMonth() + 3);
      return date.toISOString().split('T')[0];
    }
  },
  barHeight: {
    type: Number,
    default: 30
  },
  rowHeight: {
    type: Number,
    default: 40
  }
});

const emit = defineEmits(['task-moved', 'task-resized', 'task-clicked']);

const timelineRef = ref(null);
const zoom = ref(1);
const dayWidth = ref(30);
const draggingTask = ref(null);
const resizingTask = ref(null);
const resizeHandle = ref(null);
const dragStartPos = ref({ x: 0, y: 0 });
const taskStartDate = ref(null);
const tooltipVisible = ref(false);
const tooltipTask = ref(null);
const tooltipStyle = ref({});

const start = computed(() => new Date(props.startDate));
const end = computed(() => new Date(props.endDate));
const totalDays = computed(() => {
  return Math.ceil((end.value - start.value) / (1000 * 60 * 60 * 24));
});

const months = computed(() => {
  const result = [];
  const current = new Date(start.value);
  while (current <= end.value) {
    const monthStart = new Date(current.getFullYear(), current.getMonth(), 1);
    const monthEnd = new Date(current.getFullYear(), current.getMonth() + 1, 0);
    const daysInMonth = Math.min(monthEnd.getDate(), totalDays.value);
    result.push({
      label: `${current.getFullYear()}年${current.getMonth() + 1}月`,
      width: daysInMonth * dayWidth.value,
      key: `${current.getFullYear()}-${current.getMonth()}`
    });
    current.setMonth(current.getMonth() + 1);
  }
  return result;
});

const days = computed(() => {
  const result = [];
  const current = new Date(start.value);
  for (let i = 0; i < totalDays.value; i++) {
    const dayOfWeek = current.getDay();
    result.push({
      label: current.getDate(),
      key: i,
      isWeekend: dayOfWeek === 0 || dayOfWeek === 6
    });
    current.setDate(current.getDate() + 1);
  }
  return result;
});

const getDayOffset = (dateStr) => {
  const date = new Date(dateStr);
  return Math.ceil((date - start.value) / (1000 * 60 * 60 * 24));
};

const getBarStyle = (task) => {
  const startOffset = getDayOffset(task.startDate);
  const endOffset = getDayOffset(task.endDate);
  const duration = endOffset - startOffset;
  const taskIndex = props.tasks.findIndex(t => t.id === task.id);
  
  if (task.isMilestone) {
    return {
      left: `${startOffset * dayWidth.value * zoom.value}px`,
      top: `${taskIndex * props.rowHeight + 5}px`,
      width: `${props.barHeight}px`,
      height: `${props.barHeight}px`,
      background: 'var(--accent)',
      transform: 'rotate(45deg)'
    };
  }
  
  return {
    left: `${startOffset * dayWidth.value * zoom.value}px`,
    top: `${taskIndex * props.rowHeight + 5}px`,
    width: `${Math.max(duration * dayWidth.value * zoom.value, 30)}px`,
    height: `${props.barHeight}px`,
    background: task.color || 'var(--primary)'
  };
};

const formatDuration = (task) => {
  const start = new Date(task.startDate);
  const end = new Date(task.endDate);
  const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
  return `${days}天`;
};

const formatDateRange = (task) => {
  const start = new Date(task.startDate);
  const end = new Date(task.endDate);
  return `${start.toLocaleDateString('zh-CN')} - ${end.toLocaleDateString('zh-CN')}`;
};

const zoomIn = () => {
  zoom.value = Math.min(zoom.value * 1.2, 3);
};

const zoomOut = () => {
  zoom.value = Math.max(zoom.value / 1.2, 0.5);
};

const resetZoom = () => {
  zoom.value = 1;
};

const startDragBar = (event, task) => {
  if (task.isMilestone || task.isSummary) return;
  event.preventDefault();
  draggingTask.value = task;
  dragStartPos.value = { x: event.clientX, y: event.clientY };
  taskStartDate.value = new Date(task.startDate);
  document.addEventListener('mousemove', handleBarDrag);
  document.addEventListener('mouseup', stopDragBar);
};

const handleBarDrag = (event) => {
  if (!draggingTask.value) return;
  const deltaX = event.clientX - dragStartPos.value.x;
  const daysDelta = Math.round(deltaX / (dayWidth.value * zoom.value));
  
  if (daysDelta !== 0) {
    const newStart = new Date(taskStartDate.value);
    newStart.setDate(newStart.getDate() + daysDelta);
    
    const taskDuration = Math.ceil(
      (new Date(draggingTask.value.endDate) - new Date(draggingTask.value.startDate)) / (1000 * 60 * 60 * 24)
    );
    const newEnd = new Date(newStart);
    newEnd.setDate(newEnd.getDate() + taskDuration);
    
    emit('task-moved', {
      task: draggingTask.value,
      newStartDate: newStart.toISOString().split('T')[0],
      newEndDate: newEnd.toISOString().split('T')[0]
    });
    
    dragStartPos.value = { x: event.clientX, y: event.clientY };
    taskStartDate.value = newStart;
  }
};

const stopDragBar = () => {
  draggingTask.value = null;
  document.removeEventListener('mousemove', handleBarDrag);
  document.removeEventListener('mouseup', stopDragBar);
};

const startResizeBar = (event, task, handle) => {
  event.preventDefault();
  resizingTask.value = task;
  resizeHandle.value = handle;
  dragStartPos.value = { x: event.clientX, y: event.clientY };
  document.addEventListener('mousemove', handleBarResize);
  document.addEventListener('mouseup', stopResizeBar);
};

const handleBarResize = (event) => {
  if (!resizingTask.value) return;
  const deltaX = event.clientX - dragStartPos.value.x;
  const daysDelta = Math.round(deltaX / (dayWidth.value * zoom.value));
  
  if (daysDelta !== 0) {
    const newDates = {
      startDate: resizingTask.value.startDate,
      endDate: resizingTask.value.endDate
    };
    
    if (resizeHandle.value === 'left') {
      const newStart = new Date(resizingTask.value.startDate);
      newStart.setDate(newStart.getDate() + daysDelta);
      newDates.startDate = newStart.toISOString().split('T')[0];
    } else {
      const newEnd = new Date(resizingTask.value.endDate);
      newEnd.setDate(newEnd.getDate() + daysDelta);
      newDates.endDate = newEnd.toISOString().split('T')[0];
    }
    
    emit('task-resized', {
      task: resizingTask.value,
      ...newDates
    });
    
    dragStartPos.value = { x: event.clientX, y: event.clientY };
    if (resizeHandle.value === 'left') {
      resizingTask.value = { ...resizingTask.value, startDate: newDates.startDate };
    } else {
      resizingTask.value = { ...resizingTask.value, endDate: newDates.endDate };
    }
  }
};

const stopResizeBar = () => {
  resizingTask.value = null;
  resizeHandle.value = null;
  document.removeEventListener('mousemove', handleBarResize);
  document.removeEventListener('mouseup', stopResizeBar);
};

const getDependencyPath = (dependency) => {
  const fromTask = props.tasks.find(t => t.id === dependency.from);
  const toTask = props.tasks.find(t => t.id === dependency.to);
  
  if (!fromTask || !toTask) return '';
  
  const fromIndex = props.tasks.findIndex(t => t.id === fromTask.id);
  const toIndex = props.tasks.findIndex(t => t.id === toTask.id);
  
  const fromEnd = getDayOffset(fromTask.endDate) * dayWidth.value * zoom.value;
  const toStart = getDayOffset(toTask.startDate) * dayWidth.value * zoom.value;
  
  const fromY = fromIndex * props.rowHeight + props.barHeight / 2 + 5;
  const toY = toIndex * props.rowHeight + props.barHeight / 2 + 5;
  
  const midX = (fromEnd + toStart) / 2;
  
  return `M ${fromEnd} ${fromY} C ${midX} ${fromY}, ${midX} ${toY}, ${toStart - 10} ${toY}`;
};

onMounted(() => {
  // 可以在这里添加滚动同步等逻辑
});

onUnmounted(() => {
  document.removeEventListener('mousemove', handleBarDrag);
  document.removeEventListener('mouseup', stopDragBar);
  document.removeEventListener('mousemove', handleBarResize);
  document.removeEventListener('mouseup', stopResizeBar);
});
</script>

<style scoped>
.gantt-chart {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.gantt-header {
  padding: var(--space-lg);
  border-bottom: 1px solid var(--gray-200);
}

.gantt-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.gantt-title h3 {
  margin: 0;
  font-size: var(--text-xl);
  color: var(--gray-800);
}

.gantt-controls {
  display: flex;
  gap: var(--space-sm);
}

.gantt-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.gantt-sidebar {
  width: 200px;
  border-right: 1px solid var(--gray-200);
  flex-shrink: 0;
}

.gantt-sidebar-header {
  padding: var(--space-md);
  background: var(--gray-50);
  border-bottom: 1px solid var(--gray-200);
  font-weight: 600;
  color: var(--gray-700);
}

.gantt-tasks-list {
  overflow-y: auto;
}

.gantt-task-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid var(--gray-100);
  height: 40px;
  box-sizing: border-box;
}

.task-name {
  font-size: var(--text-sm);
  color: var(--gray-800);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.task-duration {
  font-size: var(--text-xs);
  color: var(--gray-500);
  margin-left: var(--space-sm);
}

.gantt-timeline-container {
  flex: 1;
  overflow-x: auto;
  overflow-y: hidden;
}

.gantt-timeline-header {
  background: var(--gray-50);
  border-bottom: 1px solid var(--gray-200);
}

.gantt-months-row {
  display: flex;
  border-bottom: 1px solid var(--gray-200);
}

.gantt-month {
  padding: var(--space-sm);
  text-align: center;
  font-weight: 600;
  font-size: var(--text-sm);
  color: var(--gray-700);
  border-right: 1px solid var(--gray-200);
  box-sizing: border-box;
}

.gantt-days-row {
  display: flex;
}

.gantt-day {
  padding: var(--space-xs);
  text-align: center;
  font-size: var(--text-xs);
  color: var(--gray-600);
  border-right: 1px solid var(--gray-200);
  box-sizing: border-box;
}

.gantt-day-weekend {
  background: rgba(0, 0, 0, 0.03);
}

.gantt-timeline-body {
  position: relative;
  min-height: 200px;
}

.gantt-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.gantt-grid-line {
  position: absolute;
  top: 0;
  bottom: 0;
  border-right: 1px solid var(--gray-100);
}

.gantt-grid-weekend {
  background: rgba(0, 0, 0, 0.02);
}

.gantt-bars-container {
  position: relative;
}

.gantt-bar-row {
  height: 40px;
  position: relative;
}

.gantt-bar {
  position: absolute;
  border-radius: var(--radius-sm);
  cursor: move;
  display: flex;
  align-items: center;
  padding: 0 var(--space-sm);
  box-sizing: border-box;
  overflow: hidden;
  transition: box-shadow 0.2s;
}

.gantt-bar:hover {
  box-shadow: var(--shadow-md);
}

.gantt-bar-progress {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.2);
  border-radius: var(--radius-sm) 0 0 var(--radius-sm);
}

.gantt-bar-label {
  font-size: var(--text-xs);
  color: white;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  position: relative;
  z-index: 1;
}

.gantt-bar-handle {
  position: absolute;
  width: 6px;
  top: 2px;
  bottom: 2px;
  cursor: ew-resize;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 2px;
}

.gantt-bar-handle-left {
  left: 2px;
}

.gantt-bar-handle-right {
  right: 2px;
}

.gantt-bar-milestone {
  cursor: pointer;
}

.gantt-bar-summary {
  background: var(--gray-400) !important;
  cursor: pointer;
}

.gantt-dependencies {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.gantt-dependency-line {
  fill: none;
}

.gantt-tooltip {
  position: fixed;
  background: white;
  padding: var(--space-md);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  z-index: 1000;
  max-width: 250px;
}

.tooltip-title {
  font-weight: 600;
  color: var(--gray-800);
  margin-bottom: var(--space-sm);
}

.tooltip-dates {
  font-size: var(--text-sm);
  color: var(--gray-600);
  margin-bottom: var(--space-xs);
}

.tooltip-progress {
  font-size: var(--text-sm);
  color: var(--primary);
}
</style>
