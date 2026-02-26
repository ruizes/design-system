<template>
  <div class="components-page">
    <div class="container">
      <div class="page-header">
        <h1>组件库文档</h1>
        <p>完整的设计系统组件库和使用指南</p>
      </div>

      <!-- 可拖拽网格布局组件 -->
      <section class="component-section grid-layout-section">
        <h2>可拖拽网格布局 Draggable Grid Layout</h2>
        <p class="component-desc">
          支持拖拽调整、网格对齐、碰撞检测与挤压、自动向上吸附的网格布局组件。
        </p>
        <div class="feature-list">
          <h4>功能特性：</h4>
          <ul>
            <li><strong>网格对齐</strong>：拖拽过程中实时对齐到网格</li>
            <li><strong>碰撞检测与挤压</strong>：组件移动到其他组件位置时，自动让路</li>
            <li><strong>自动向上吸附</strong>：移走组件后，下方组件自动上浮填补空缺</li>
          </ul>
        </div>
        <div class="component-demo">
          <div class="grid-layout-demo">
            <GridLayout
              ref="gridLayoutRef"
              v-model="gridLayoutItems"
              :cols="12"
              :cell-width="80"
              :cell-height="60"
              :gap="8"
              :show-grid-lines="true"
              @change="onGridLayoutChange"
              @drag-start="onDragStart"
              @drag-end="onDragEnd"
            >
              <template #item1>
                <div class="grid-item-custom">
                  <span class="item-icon">📊</span>
                  <span class="item-title">数据统计</span>
                </div>
              </template>
              <template #item2>
                <div class="grid-item-custom item-blue">
                  <span class="item-icon">📈</span>
                  <span class="item-title">趋势图表</span>
                </div>
              </template>
              <template #item3>
                <div class="grid-item-custom item-green">
                  <span class="item-icon">✅</span>
                  <span class="item-title">任务列表</span>
                </div>
              </template>
              <template #item4>
                <div class="grid-item-custom item-orange">
                  <span class="item-icon">📅</span>
                  <span class="item-title">日程安排</span>
                </div>
              </template>
              <template #item5>
                <div class="grid-item-custom item-purple">
                  <span class="item-icon">👤</span>
                  <span class="item-title">用户信息</span>
                </div>
              </template>
            </GridLayout>
          </div>
        </div>
      </section>

      <!-- 甘特图组件 -->
      <section class="component-section">
        <h2>甘特图 Gantt Chart</h2>
        <p class="component-desc">
          可视化项目进度管理组件，支持缩放、今日线、任务状态显示等功能。
        </p>
        <div class="component-demo">
          <div class="gantt-demo">
            <GanttChart
              :tasks="ganttTasks"
              :start-date="ganttStartDate"
              :end-date="ganttEndDate"
              :day-width="40"
              :row-height="40"
              :show-today-line="true"
              :show-legend="true"
              @task-click="onTaskClick"
              @task-hover="onTaskHover"
            />
          </div>
        </div>
      </section>

      <!-- 按钮组件 -->
      <section class="component-section">
        <h2>按钮 Buttons</h2>
        <div class="component-demo">
          <div class="demo-group">
            <button class="btn btn-primary">主要按钮</button>
            <button class="btn btn-secondary">次要按钮</button>
            <button class="btn btn-outline">边框按钮</button>
          </div>
          <div class="demo-group">
            <button class="btn btn-primary btn-sm">小按钮</button>
            <button class="btn btn-primary">默认按钮</button>
            <button class="btn btn-primary btn-lg">大按钮</button>
          </div>
        </div>
      </section>

      <!-- 卡片组件 -->
      <section class="component-section">
        <h2>卡片 Cards</h2>
        <div class="grid grid-3">
          <div class="card">
            <h3>基础卡片</h3>
            <p>这是一个基础卡片组件，包含标题和内容。</p>
          </div>
          <div class="card">
            <div class="card-icon">📊</div>
            <h3>图标卡片</h3>
            <p>带有图标的卡片组件。</p>
          </div>
          <div class="card">
            <h3>交互卡片</h3>
            <p>悬停时有动画效果的卡片。</p>
            <button class="btn btn-primary btn-sm">了解更多</button>
          </div>
        </div>
      </section>

      <!-- 表单组件 -->
      <section class="component-section">
        <h2>表单 Forms</h2>
        <div class="component-demo">
          <div class="form-group">
            <label>文本输入框</label>
            <input type="text" class="input" placeholder="请输入内容">
          </div>
          <div class="form-group">
            <label>邮箱输入框</label>
            <input type="email" class="input" placeholder="your@email.com">
          </div>
          <div class="form-group">
            <label>文本域</label>
            <textarea class="input" rows="3" placeholder="请输入详细内容"></textarea>
          </div>
        </div>
      </section>

      <!-- 标签组件 -->
      <section class="component-section">
        <h2>标签 Badges</h2>
        <div class="component-demo">
          <span class="badge">默认标签</span>
          <span class="badge badge-primary">主要标签</span>
          <span class="badge badge-success">成功标签</span>
        </div>
      </section>

      <!-- 网格系统 -->
      <section class="component-section">
        <h2>网格系统 Grid</h2>
        <div class="grid grid-3">
          <div class="grid-demo-item">列 1</div>
          <div class="grid-demo-item">列 2</div>
          <div class="grid-demo-item">列 3</div>
        </div>
      </section>

      <!-- 设计令牌 -->
      <section class="component-section">
        <h2>设计令牌 Design Tokens</h2>
        <h3>配色方案</h3>
        <div class="color-palette">
          <div class="color-item">
            <div class="color-swatch" style="background: var(--primary)"></div>
            <div class="color-name">Primary</div>
            <div class="color-value">#2563eb</div>
          </div>
          <div class="color-item">
            <div class="color-swatch" style="background: var(--secondary)"></div>
            <div class="color-name">Secondary</div>
            <div class="color-value">#10b981</div>
          </div>
          <div class="color-item">
            <div class="color-swatch" style="background: var(--accent)"></div>
            <div class="color-name">Accent</div>
            <div class="color-value">#f59e0b</div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import GridLayout from '../components/GridLayout.vue'
import GanttChart from '../components/GanttChart.vue'

const gridLayoutRef = ref(null)

const gridLayoutItems = ref([
  { id: 'item1', x: 0, y: 0, w: 3, h: 2, title: '数据统计' },
  { id: 'item2', x: 3, y: 0, w: 4, h: 2, title: '趋势图表' },
  { id: 'item3', x: 7, y: 0, w: 3, h: 2, title: '任务列表' },
  { id: 'item4', x: 0, y: 2, w: 4, h: 2, title: '日程安排' },
  { id: 'item5', x: 4, y: 2, w: 3, h: 2, title: '用户信息' }
])

const today = new Date()
const ganttStartDate = new Date(today.getFullYear(), today.getMonth(), 1)
const ganttEndDate = new Date(today.getFullYear(), today.getMonth() + 1, 15)

const ganttTasks = ref([
  {
    id: 'task1',
    name: '需求分析',
    start: new Date(today.getFullYear(), today.getMonth(), 1),
    end: new Date(today.getFullYear(), today.getMonth(), 5),
    color: '#2563eb',
    status: { value: 'completed', label: '已完成', color: '#10b981' }
  },
  {
    id: 'task2',
    name: 'UI设计',
    start: new Date(today.getFullYear(), today.getMonth(), 4),
    end: new Date(today.getFullYear(), today.getMonth(), 10),
    color: '#8b5cf6',
    status: { value: 'in_progress', label: '进行中', color: '#2563eb' }
  },
  {
    id: 'task3',
    name: '前端开发',
    start: new Date(today.getFullYear(), today.getMonth(), 8),
    end: new Date(today.getFullYear(), today.getMonth(), 18),
    color: '#f59e0b',
    status: { value: 'in_progress', label: '进行中', color: '#2563eb' }
  },
  {
    id: 'task4',
    name: '后端开发',
    start: new Date(today.getFullYear(), today.getMonth(), 10),
    end: new Date(today.getFullYear(), today.getMonth(), 20),
    color: '#10b981',
    status: { value: 'pending', label: '待开始', color: '#6b7280' }
  },
  {
    id: 'task5',
    name: '测试与部署',
    start: new Date(today.getFullYear(), today.getMonth(), 18),
    end: new Date(today.getFullYear(), today.getMonth(), 25),
    color: '#ef4444',
    status: { value: 'pending', label: '待开始', color: '#6b7280' }
  }
])

function onGridLayoutChange(items) {
  console.log('Layout changed:', items)
}

function onDragStart({ item, event }) {
  console.log('Drag started:', item)
}

function onDragEnd({ item, event }) {
  console.log('Drag ended:', item)
}

function onTaskClick(task) {
  console.log('Task clicked:', task)
}

function onTaskHover(task) {
  console.log('Task hovered:', task)
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

.component-section h3 {
  font-size: var(--text-xl);
  margin: var(--space-xl) 0 var(--space-md);
  color: var(--gray-800);
}

.component-demo {
  margin-bottom: var(--space-xl);
}

.demo-group {
  display: flex;
  gap: var(--space-md);
  margin-bottom: var(--space-md);
  flex-wrap: wrap;
}

.form-group {
  margin-bottom: var(--space-lg);
}

.form-group label {
  display: block;
  margin-bottom: var(--space-sm);
  font-weight: 500;
  color: var(--gray-700);
}

.grid-demo-item {
  background: var(--primary);
  color: white;
  padding: var(--space-xl);
  border-radius: var(--radius-md);
  text-align: center;
  font-weight: 500;
}

.color-palette {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: var(--space-lg);
  margin-top: var(--space-lg);
}

.color-item {
  text-align: center;
}

.color-swatch {
  width: 100%;
  height: 100px;
  border-radius: var(--radius-md);
  margin-bottom: var(--space-md);
  box-shadow: var(--shadow);
}

.color-name {
  font-weight: 600;
  margin-bottom: var(--space-xs);
  color: var(--gray-900);
}

.color-value {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  color: var(--gray-600);
}

.card-icon {
  font-size: 2.5rem;
  margin-bottom: var(--space-md);
}

.component-desc {
  color: var(--gray-600);
  margin-bottom: var(--space-lg);
  line-height: 1.6;
}

.feature-list {
  margin-bottom: var(--space-xl);
  padding: var(--space-lg);
  background: var(--gray-50);
  border-radius: var(--radius-md);
}

.feature-list h4 {
  margin: 0 0 var(--space-md);
  color: var(--gray-800);
}

.feature-list ul {
  margin: 0;
  padding-left: var(--space-xl);
}

.feature-list li {
  margin-bottom: var(--space-sm);
  color: var(--gray-600);
  line-height: 1.6;
}

.grid-layout-section {
  padding: var(--space-2xl);
  background: white;
  box-shadow: var(--shadow);
}

.grid-layout-section h2 {
  margin-bottom: var(--space-lg);
}

.grid-layout-section .component-desc {
  margin-bottom: var(--space-lg);
}

.grid-layout-section .feature-list {
  margin-bottom: var(--space-xl);
}

.grid-layout-section .component-demo {
  margin-bottom: 0;
}

.grid-layout-demo {
  height: 500px;
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-md);
  overflow: auto;
}

.gantt-demo {
  height: 300px;
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.grid-item-custom {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  border-radius: 8px;
  gap: 8px;
}

.grid-item-custom.item-blue {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
}

.grid-item-custom.item-green {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
}

.grid-item-custom.item-orange {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
}

.grid-item-custom.item-purple {
  background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%);
}

.item-icon {
  font-size: 24px;
}

.item-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--gray-700);
}

@media (max-width: 768px) {
  .demo-group {
    flex-direction: column;
  }
  
  .grid-layout-demo {
    height: 300px;
  }
  
  .gantt-demo {
    height: 250px;
  }
}
</style>
