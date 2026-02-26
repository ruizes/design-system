<script setup>
import { ref } from 'vue'
import DraggableGrid from '../components/DraggableGrid.vue'
import GanttChart from '../components/GanttChart.vue'

// 可拖拽网格示例数据
const gridItems = ref([
  { id: '1', label: '卡片 1', w: 1, h: 1, col: 0, row: 0 },
  { id: '2', label: '卡片 2', w: 1, h: 1, col: 1, row: 0 },
  { id: '3', label: '宽卡片', w: 2, h: 1, col: 2, row: 0 },
  { id: '4', label: '高卡片', w: 1, h: 2, col: 0, row: 1 },
  { id: '5', label: '卡片 5', w: 1, h: 1, col: 1, row: 1 },
  { id: '6', label: '卡片 6', w: 1, h: 1, col: 2, row: 1 },
  { id: '7', label: '大卡片', w: 2, h: 2, col: 1, row: 2 }
])

const handleGridChange = (items) => {
  console.log('Grid changed:', items)
}

// 甘特图示例数据
const ganttTasks = ref([
  { id: '1', name: '需求分析', startDate: '2025-02-01', endDate: '2025-02-05', status: 'done', progress: 100 },
  { id: '2', name: 'UI设计', startDate: '2025-02-04', endDate: '2025-02-10', status: 'done', progress: 100 },
  { id: '3', name: '前端开发', startDate: '2025-02-08', endDate: '2025-02-20', status: 'inprogress', progress: 65 },
  { id: '4', name: '后端开发', startDate: '2025-02-10', endDate: '2025-02-22', status: 'inprogress', progress: 45 },
  { id: '5', name: '测试阶段', startDate: '2025-02-20', endDate: '2025-02-28', status: 'todo', progress: 0 },
  { id: '6', name: '部署上线', startDate: '2025-02-28', endDate: '2025-03-02', status: 'todo', progress: 0 }
])

const ganttDependencies = ref([
  { from: '1', to: '2' },
  { from: '2', to: '3' },
  { from: '2', to: '4' },
  { from: '3', to: '5' },
  { from: '4', to: '5' },
  { from: '5', to: '6' }
])

const handleTaskClick = (task) => {
  console.log('Task clicked:', task)
}

// 获取项目颜色
const getItemColor = (id) => {
  const colors = {
    '1': 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
    '2': 'linear-gradient(135deg, #10b981, #059669)',
    '3': 'linear-gradient(135deg, #f59e0b, #d97706)',
    '4': 'linear-gradient(135deg, #8b5cf6, #6d28d9)',
    '5': 'linear-gradient(135deg, #ec4899, #db2777)',
    '6': 'linear-gradient(135deg, #06b6d4, #0891b2)',
    '7': 'linear-gradient(135deg, #f97316, #ea580c)'
  }
  return colors[id] || 'linear-gradient(135deg, #6b7280, #4b5563)'
}

// 获取项目图标
const getItemIcon = (id) => {
  const icons = {
    '1': '📄',
    '2': '🎨',
    '3': '📊',
    '4': '📈',
    '5': '⚙️',
    '6': '🔧',
    '7': '🚀'
  }
  return icons[id] || '📦'
}
</script>

<template>
  <div class="components-page">
    <div class="container">
      <div class="page-header">
        <h1>组件库文档</h1>
        <p>完整的设计系统组件库和使用指南</p>
      </div>

      <!-- 可拖拽网格布局组件 -->
      <section class="component-section">
        <h2>可拖拽网格布局 DraggableGrid</h2>
        <p class="component-desc">支持网格对齐、二维碰撞检测与挤压、自动向上吸附的拖拽布局组件</p>
        <div class="component-demo">
          <DraggableGrid
            v-model:items="gridItems"
            :cols="4"
            :row-height="100"
            :gap="16"
            :show-grid="true"
            :compact="true"
            :container-height="400"
            @change="handleGridChange"
          >
            <template #default="slotProps">
              <div
                class="custom-grid-item"
                :class="{ 'is-dragging': slotProps.isDragging }"
                :style="{ background: getItemColor(slotProps.item.id) }"
              >
                <span class="item-icon">{{ getItemIcon(slotProps.item.id) }}</span>
                <span class="item-label">{{ slotProps.item.label }}</span>
              </div>
            </template>
          </DraggableGrid>
        </div>
      </section>

      <!-- 甘特图组件 -->
      <section class="component-section">
        <h2>甘特图 GanttChart</h2>
        <p class="component-desc">项目进度管理甘特图，支持任务依赖关系展示</p>
        <div class="component-demo">
          <GanttChart
            :tasks="ganttTasks"
            :dependencies="ganttDependencies"
            start-date="2025-02-01"
            end-date="2025-03-05"
            :day-width="50"
            :row-height="48"
            :show-dependencies="true"
            @task-click="handleTaskClick"
          />
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
  font-size: var(--text-base);
}

/* 自定义网格项样式 */
.custom-grid-item {
  width: 100%;
  height: 100%;
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 500;
  box-shadow: var(--shadow);
  transition: all 0.2s ease;
  cursor: grab;
}

.custom-grid-item:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.custom-grid-item.is-dragging {
  cursor: grabbing;
  transform: scale(1.02);
}

.item-icon {
  font-size: 1.5rem;
  margin-bottom: var(--space-xs);
}

.item-label {
  font-size: var(--text-sm);
}

@media (max-width: 768px) {
  .demo-group {
    flex-direction: column;
  }
}
</style>
