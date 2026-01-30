<template>
  <div class="gantt-chart" :style="{ width: width + 'px' }">
    <!-- 时间轴头部 -->
    <div class="gantt-header">
      <div class="task-info-header">任务</div>
      <div class="timeline-header" :style="{ width: timelineWidth + 'px' }">
        <!-- 月份行 -->
        <div class="timeline-months">
          <div
            v-for="month in months"
            :key="month.value"
            class="timeline-month"
            :style="{ width: month.width + 'px' }"
          >
            {{ month.label }}
          </div>
        </div>
        <!-- 日期行 -->
        <div class="timeline-days">
          <div
            v-for="day in days"
            :key="day.value"
            class="timeline-day"
            :class="{ 'today': day.isToday, 'weekend': day.isWeekend }"
            :style="{ width: dayWidth + 'px' }"
          >
            {{ day.day }}
          </div>
        </div>
      </div>
    </div>

    <!-- 任务行 -->
    <div class="gantt-body">
      <div class="task-list">
        <!-- 任务信息列 -->
        <div class="task-info-column">
          <div
            v-for="task in tasks"
            :key="task.id"
            class="task-info"
            :style="{ height: rowHeight + 'px' }"
          >
            <div class="task-name">{{ task.name }}</div>
            <div class="task-assignee">{{ task.assignee }}</div>
          </div>
        </div>

        <!-- 时间轴区域 -->
        <div class="timeline-area" :style="{ width: timelineWidth + 'px' }">
          <!-- 网格背景 -->
          <div class="timeline-grid" :style="{ width: timelineWidth + 'px' }">
            <div
              v-for="day in days"
              :key="'grid-' + day.value"
              class="grid-column"
              :class="{ 'today': day.isToday, 'weekend': day.isWeekend }"
              :style="{ width: dayWidth + 'px' }"
            ></div>
          </div>

          <!-- 任务条 -->
          <div class="task-bars">
            <div
              v-for="task in tasks"
              :key="'bar-' + task.id"
              class="task-bar"
              :class="{ 'critical': task.critical }"
              :style="getTaskBarStyle(task)"
              @click="selectTask(task)"
            >
              <div class="task-progress" :style="{ width: task.progress + '%' }"></div>
              <div class="task-label">{{ task.name }}</div>
            </div>
          </div>

          <!-- 今日线 -->
          <div
            v-if="showTodayLine"
            class="today-line"
            :style="{ left: todayPosition + 'px' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- 任务详情弹窗 -->
    <div v-if="selectedTask" class="task-detail-modal" @click="closeTaskDetail">
      <div class="task-detail-content" @click.stop>
        <div class="task-detail-header">
          <h3>{{ selectedTask.name }}</h3>
          <button class="close-btn" @click="closeTaskDetail">×</button>
        </div>
        <div class="task-detail-body">
          <div class="detail-row">
            <span class="detail-label">负责人:</span>
            <span class="detail-value">{{ selectedTask.assignee }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">开始日期:</span>
            <span class="detail-value">{{ formatDate(selectedTask.startDate) }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">结束日期:</span>
            <span class="detail-value">{{ formatDate(selectedTask.endDate) }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">进度:</span>
            <span class="detail-value">{{ selectedTask.progress }}%</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">描述:</span>
            <span class="detail-value">{{ selectedTask.description || '暂无描述' }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'GanttChart',
  props: {
    // 任务数据
    tasks: {
      type: Array,
      default: () => []
    },
    // 开始日期
    startDate: {
      type: Date,
      default: () => new Date()
    },
    // 结束日期
    endDate: {
      type: Date,
      default: () => {
        const date = new Date()
        date.setMonth(date.getMonth() + 3)
        return date
      }
    },
    // 行高
    rowHeight: {
      type: Number,
      default: 50
    },
    // 每天宽度
    dayWidth: {
      type: Number,
      default: 30
    },
    // 图表总宽度
    width: {
      type: Number,
      default: 1200
    },
    // 是否显示今日线
    showTodayLine: {
      type: Boolean,
      default: true
    }
  },
  emits: ['task-select'],
  setup(props, { emit }) {
    const selectedTask = ref(null)
    
    // 计算时间轴宽度
    const timelineWidth = computed(() => {
      const daysCount = Math.ceil((props.endDate - props.startDate) / (1000 * 60 * 60 * 24)) + 1
      return daysCount * props.dayWidth
    })
    
    // 生成日期数组
    const days = computed(() => {
      const daysArray = []
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      
      const current = new Date(props.startDate)
      current.setHours(0, 0, 0, 0)
      
      while (current <= props.endDate) {
        const dayOfWeek = current.getDay()
        const isWeekend = dayOfWeek === 0 || dayOfWeek === 6
        const isToday = current.getTime() === today.getTime()
        
        daysArray.push({
          value: current.toISOString().split('T')[0],
          day: current.getDate(),
          isWeekend,
          isToday,
          date: new Date(current)
        })
        
        current.setDate(current.getDate() + 1)
      }
      
      return daysArray
    })
    
    // 生成月份数组
    const months = computed(() => {
      const monthNames = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
      const monthsArray = []
      
      if (!days.value || days.value.length === 0) return monthsArray
      
      let currentMonth = days.value[0].date.getMonth()
      let currentYear = days.value[0].date.getFullYear()
      let monthStartIndex = 0
      let daysInCurrentMonth = 0
      
      for (let i = 0; i < days.value.length; i++) {
        const day = days.value[i]
        
        if (day.date.getMonth() === currentMonth && day.date.getFullYear() === currentYear) {
          daysInCurrentMonth++
        } else {
          // 添加上个月
          monthsArray.push({
            value: `${currentYear}-${currentMonth + 1}`,
            label: `${currentYear}年${monthNames[currentMonth]}`,
            width: daysInCurrentMonth * props.dayWidth
          })
          
          // 重置为新月份
          currentMonth = day.date.getMonth()
          currentYear = day.date.getFullYear()
          monthStartIndex = i
          daysInCurrentMonth = 1
        }
      }
      
      // 添加最后一个月
      if (daysInCurrentMonth > 0) {
        monthsArray.push({
          value: `${currentYear}-${currentMonth + 1}`,
          label: `${currentYear}年${monthNames[currentMonth]}`,
          width: daysInCurrentMonth * props.dayWidth
        })
      }
      
      return monthsArray
    })
    
    // 计算今日线位置
    const todayPosition = computed(() => {
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      
      const startDate = new Date(props.startDate)
      startDate.setHours(0, 0, 0, 0)
      
      const daysDiff = Math.ceil((today - startDate) / (1000 * 60 * 60 * 24))
      
      if (daysDiff >= 0 && days.value && daysDiff <= days.value.length) {
        return daysDiff * props.dayWidth + props.dayWidth / 2
      }
      
      return -1 // 不在显示范围内
    })
    
    // 获取任务条样式
    const getTaskBarStyle = (task) => {
      const taskStart = new Date(task.startDate)
      taskStart.setHours(0, 0, 0, 0)
      
      const taskEnd = new Date(task.endDate)
      taskEnd.setHours(0, 0, 0, 0)
      
      const startDate = new Date(props.startDate)
      startDate.setHours(0, 0, 0, 0)
      
      // 计算开始位置
      const startDaysDiff = Math.ceil((taskStart - startDate) / (1000 * 60 * 60 * 24))
      const left = Math.max(0, startDaysDiff * props.dayWidth)
      
      // 计算宽度
      const durationDays = Math.ceil((taskEnd - taskStart) / (1000 * 60 * 60 * 24)) + 1
      const width = durationDays * props.dayWidth
      
      // 计算垂直位置
      const taskIndex = props.tasks.findIndex(t => t.id === task.id)
      const top = taskIndex * props.rowHeight + 5 // 5px的上下边距
      
      return {
        left: `${left}px`,
        top: `${top}px`,
        width: `${width}px`,
        height: `${props.rowHeight - 10}px`
      }
    }
    
    // 选择任务
    const selectTask = (task) => {
      selectedTask.value = task
      emit('task-select', task)
    }
    
    // 关闭任务详情
    const closeTaskDetail = () => {
      selectedTask.value = null
    }
    
    // 格式化日期
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    return {
      selectedTask,
      timelineWidth,
      days,
      months,
      todayPosition,
      getTaskBarStyle,
      selectTask,
      closeTaskDetail,
      formatDate
    }
  }
}
</script>

<style scoped>
.gantt-chart {
  font-family: var(--font-sans);
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-lg);
  overflow: hidden;
  background-color: white;
  box-shadow: var(--shadow);
}

.gantt-header {
  display: flex;
  background-color: var(--gray-50);
  border-bottom: 1px solid var(--gray-200);
}

.task-info-header {
  width: 200px;
  padding: var(--space-md);
  font-weight: 600;
  color: var(--gray-800);
  border-right: 1px solid var(--gray-200);
  display: flex;
  align-items: center;
  justify-content: center;
}

.timeline-header {
  overflow: hidden;
}

.timeline-months {
  display: flex;
  border-bottom: 1px solid var(--gray-200);
}

.timeline-month {
  padding: var(--space-sm) var(--space-md);
  font-weight: 600;
  color: var(--gray-700);
  border-right: 1px solid var(--gray-100);
  text-align: center;
}

.timeline-days {
  display: flex;
}

.timeline-day {
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-sm);
  border-right: 1px solid var(--gray-100);
  color: var(--gray-600);
}

.timeline-day.today {
  background-color: rgba(37, 99, 235, 0.1);
  color: var(--primary);
  font-weight: 600;
}

.timeline-day.weekend {
  background-color: var(--gray-50);
  color: var(--gray-500);
}

.gantt-body {
  overflow-y: auto;
  max-height: 500px;
}

.task-list {
  display: flex;
}

.task-info-column {
  width: 200px;
  border-right: 1px solid var(--gray-200);
}

.task-info {
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid var(--gray-100);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.task-name {
  font-weight: 500;
  color: var(--gray-800);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.task-assignee {
  font-size: var(--text-sm);
  color: var(--gray-500);
  margin-top: 2px;
}

.timeline-area {
  position: relative;
}

.timeline-grid {
  display: flex;
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  z-index: 1;
}

.grid-column {
  height: 100%;
  border-right: 1px solid var(--gray-100);
}

.grid-column.today {
  background-color: rgba(37, 99, 235, 0.05);
}

.grid-column.weekend {
  background-color: var(--gray-50);
}

.task-bars {
  position: relative;
  z-index: 2;
}

.task-bar {
  position: absolute;
  background-color: var(--primary);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: var(--transition);
  overflow: hidden;
}

.task-bar:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.task-bar.critical {
  background-color: var(--error);
}

.task-progress {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.3);
}

.task-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: var(--text-sm);
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  width: 90%;
  text-align: center;
}

.today-line {
  position: absolute;
  top: 0;
  width: 2px;
  height: 100%;
  background-color: var(--error);
  z-index: 3;
}

.task-detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.task-detail-content {
  background-color: white;
  border-radius: var(--radius-lg);
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
}

.task-detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-lg);
  border-bottom: 1px solid var(--gray-200);
}

.task-detail-header h3 {
  margin: 0;
  color: var(--gray-900);
}

.close-btn {
  background: none;
  border: none;
  font-size: var(--text-2xl);
  cursor: pointer;
  color: var(--gray-500);
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  transition: var(--transition);
}

.close-btn:hover {
  background-color: var(--gray-100);
  color: var(--gray-700);
}

.task-detail-body {
  padding: var(--space-lg);
}

.detail-row {
  display: flex;
  margin-bottom: var(--space-md);
}

.detail-row:last-child {
  margin-bottom: 0;
}

.detail-label {
  font-weight: 600;
  color: var(--gray-700);
  width: 100px;
  flex-shrink: 0;
}

.detail-value {
  color: var(--gray-600);
  flex-grow: 1;
}
</style>