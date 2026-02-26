<template>
  <div class="components-page">
    <div class="container">
      <div class="page-header">
        <h1>组件库</h1>
        <p>GridLayout 可拖拽网格布局 + GanttChart 甘特图</p>
      </div>

      <!-- 网格布局组件 -->
      <section class="component-section">
        <h2>网格布局 GridLayout</h2>
        <p class="component-description">可拖拽调整的网格布局组件，支持实时对齐网格、碰撞检测与挤压、自动向上吸附</p>
        <div class="component-demo">
          <GridLayout
            v-model="gridItems"
            :col-num="12"
            :row-height="60"
            :gap="10"
            :show-grid="true"
            :compact-up="true"
            :prevent-collision="true"
            style="margin: 20px 0;"
          >
            <template #gantt1="{ item }">
              <div class="grid-demo-gantt">
                <GanttChart
                  :tasks="ganttTasks"
                  title="项目进度"
                  :row-height="35"
                  :day-width="25"
                  style="height: 100%;"
                />
              </div>
            </template>
          </GridLayout>
        </div>
        <div class="demo-controls">
          <button class="btn btn-primary btn-sm" @click="addGridItem">添加组件</button>
          <button class="btn btn-secondary btn-sm" @click="resetGrid">重置布局</button>
        </div>
      </section>

      <!-- 甘特图组件 -->
      <section class="component-section">
        <h2>甘特图 GanttChart</h2>
        <p class="component-description">项目进度甘特图组件，支持拖拽调整任务时间、任务依赖、里程碑展示</p>
        <div class="component-demo">
          <div style="height: 400px; margin: 20px 0;">
            <GanttChart
              :tasks="ganttTasks"
              title="项目开发计划"
              :row-height="40"
              :day-width="30"
              :editable="true"
              @task-change="onTaskChange"
            />
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { GridLayout, GanttChart } from '../components'

const gridItems = ref([
  { id: 'item1', title: '卡片组件 A', x: 0, y: 0, w: 4, h: 2, content: '这是一个可拖拽的卡片组件' },
  { id: 'item2', title: '统计数据', x: 4, y: 0, w: 4, h: 2, content: '数据统计面板' },
  { id: 'item3', title: '任务列表', x: 8, y: 0, w: 4, h: 3, content: '待办事项列表' },
  { id: 'gantt1', title: '甘特图展示', x: 0, y: 2, w: 8, h: 3 },
  { id: 'item5', title: '通知中心', x: 8, y: 3, w: 4, h: 2, content: '系统通知消息' },
  { id: 'item6', title: '图表组件', x: 0, y: 5, w: 6, h: 2, content: '数据可视化图表' },
  { id: 'item7', title: '用户信息', x: 6, y: 5, w: 6, h: 2, content: '用户个人资料卡片' }
])

const ganttTasks = ref([
  { id: 'phase1', name: '项目启动', start: '2025-01-01', duration: 5, isSummary: true },
  { id: 'task1', name: '需求分析', start: '2025-01-01', duration: 3, progress: 100, color: '#10b981', parentId: 'phase1' },
  { id: 'task2', name: '团队组建', start: '2025-01-04', duration: 2, progress: 100, color: '#10b981', parentId: 'phase1' },
  { id: 'milestone1', name: '项目启动会', start: '2025-01-06', duration: 0, isMilestone: true, dependencies: ['task1', 'task2'] },
  { id: 'phase2', name: '设计阶段', start: '2025-01-07', duration: 10, isSummary: true },
  { id: 'task3', name: 'UI设计', start: '2025-01-07', duration: 5, progress: 80, color: '#3b82f6', parentId: 'phase2' },
  { id: 'task4', name: '原型制作', start: '2025-01-12', duration: 5, progress: 60, color: '#3b82f6', parentId: 'phase2', dependencies: ['task3'] },
  { id: 'phase3', name: '开发阶段', start: '2025-01-21', duration: 15, isSummary: true },
  { id: 'task5', name: '前端开发', start: '2025-01-21', duration: 10, progress: 30, color: '#f59e0b', parentId: 'phase3', dependencies: ['task4'] },
  { id: 'task6', name: '后端开发', start: '2025-01-21', duration: 10, progress: 40, color: '#f59e0b', parentId: 'phase3', dependencies: ['task4'] },
  { id: 'task7', name: '接口联调', start: '2025-01-31', duration: 5, progress: 0, color: '#f59e0b', parentId: 'phase3', dependencies: ['task5', 'task6'] },
  { id: 'phase4', name: '测试上线', start: '2025-02-05', duration: 8, isSummary: true },
  { id: 'task8', name: '功能测试', start: '2025-02-05', duration: 4, progress: 0, color: '#ef4444', parentId: 'phase4' },
  { id: 'task9', name: 'Bug修复', start: '2025-02-09', duration: 2, progress: 0, color: '#ef4444', parentId: 'phase4', dependencies: ['task8'] },
  { id: 'milestone2', name: '项目上线', start: '2025-02-12', duration: 0, isMilestone: true, dependencies: ['task9'] },
  { id: 'task10', name: '文档编写', start: '2025-02-05', duration: 3, progress: 0, color: '#8b5cf6', parentId: 'phase4' }
])

let itemCounter = 8

const addGridItem = () => {
  gridItems.value.push({
    id: `item${itemCounter}`,
    title: `新组件 ${itemCounter}`,
    x: 0,
    y: 10,
    w: 3,
    h: 2,
    content: `这是新添加的组件 ${itemCounter}`
  })
  itemCounter++
}

const resetGrid = () => {
  gridItems.value = [
    { id: 'item1', title: '卡片组件 A', x: 0, y: 0, w: 4, h: 2, content: '这是一个可拖拽的卡片组件' },
    { id: 'item2', title: '统计数据', x: 4, y: 0, w: 4, h: 2, content: '数据统计面板' },
    { id: 'item3', title: '任务列表', x: 8, y: 0, w: 4, h: 3, content: '待办事项列表' },
    { id: 'gantt1', title: '甘特图展示', x: 0, y: 2, w: 8, h: 3 },
    { id: 'item5', title: '通知中心', x: 8, y: 3, w: 4, h: 2, content: '系统通知消息' },
    { id: 'item6', title: '图表组件', x: 0, y: 5, w: 6, h: 2, content: '数据可视化图表' },
    { id: 'item7', title: '用户信息', x: 6, y: 5, w: 6, h: 2, content: '用户个人资料卡片' }
  ]
  itemCounter = 8
}

const onTaskChange = (tasks) => {
  console.log('任务变更:', tasks)
}
</script>

<style scoped>
.components-page {
  padding: var(--space-3xl) 0;
}

.page-header {
  text-align: center;
  margin-bottom: var(--space-3xl);
}

.page-header h1 {
  font-size: var(--text-4xl);
  font-weight: 700;
  margin-bottom: var(--space-md);
  color: var(--gray-900);
}

.page-header p {
  font-size: var(--text-xl);
  color: var(--gray-600);
}

.component-section {
  margin-bottom: var(--space-3xl);
  padding: var(--space-2xl);
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
}

.component-section h2 {
  font-size: var(--text-2xl);
  margin-bottom: var(--space-xl);
  color: var(--gray-900);
  padding-bottom: var(--space-md);
  border-bottom: 2px solid var(--gray-200);
}

.component-demo {
  margin-bottom: var(--space-xl);
}

.component-description {
  color: var(--gray-600);
  margin-bottom: var(--space-lg);
  font-size: var(--text-base);
}

.demo-controls {
  display: flex;
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}

.grid-demo-gantt {
  width: 100%;
  height: 100%;
  min-height: 150px;
  overflow: hidden;
}
</style>
