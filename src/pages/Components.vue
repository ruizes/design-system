<script setup>
import { ref } from 'vue'
import DraggableGrid from '../components/DraggableGrid.vue'
import GanttChart from '../components/GanttChart.vue'

// 可拖拽网格示例数据
const gridItems = ref([
  { id: 'item-1', label: '卡片 A', x: 0, y: 0, w: 1, h: 1 },
  { id: 'item-2', label: '卡片 B', x: 1, y: 0, w: 1, h: 1 },
  { id: 'item-3', label: '卡片 C', x: 2, y: 0, w: 1, h: 1 },
  { id: 'item-4', label: '宽卡片', x: 0, y: 1, w: 2, h: 1 },
  { id: 'item-5', label: '高卡片', x: 2, y: 1, w: 1, h: 2 },
  { id: 'item-6', label: '卡片 D', x: 3, y: 0, w: 1, h: 1 }
])

const gridRef = ref(null)

const addGridItem = () => {
  const labels = ['新卡片', '任务', '项目', '模块', '组件']
  const randomLabel = labels[Math.floor(Math.random() * labels.length)]
  gridRef.value?.addItem({
    label: `${randomLabel} ${gridItems.value.length + 1}`,
    w: Math.random() > 0.7 ? 2 : 1,
    h: Math.random() > 0.8 ? 2 : 1
  })
}

const removeLastItem = () => {
  if (gridItems.value.length > 0) {
    const lastItem = gridItems.value[gridItems.value.length - 1]
    gridRef.value?.removeItem(lastItem.id)
  }
}

const handleGridChange = (newLayout) => {
  console.log('Grid layout changed:', newLayout)
}

// 甘特图示例数据
const ganttTasks = ref([
  {
    id: 1,
    name: '项目启动',
    start: '2025-02-01',
    end: '2025-02-05',
    progress: 100,
    status: 'completed',
    isGroup: true,
    collapsed: false,
    children: [
      { id: 11, name: '需求分析', start: '2025-02-01', end: '2025-02-03', progress: 100, status: 'completed' },
      { id: 12, name: '项目计划', start: '2025-02-03', end: '2025-02-05', progress: 100, status: 'completed' }
    ]
  },
  {
    id: 2,
    name: '设计阶段',
    start: '2025-02-06',
    end: '2025-02-15',
    progress: 80,
    status: 'progress',
    isGroup: true,
    collapsed: false,
    children: [
      { id: 21, name: 'UI设计', start: '2025-02-06', end: '2025-02-12', progress: 90, status: 'progress' },
      { id: 22, name: '原型评审', start: '2025-02-12', end: '2025-02-15', progress: 60, status: 'progress' }
    ]
  },
  {
    id: 3,
    name: '开发阶段',
    start: '2025-02-16',
    end: '2025-03-10',
    progress: 30,
    status: 'progress',
    isGroup: true,
    collapsed: false,
    children: [
      { id: 31, name: '前端开发', start: '2025-02-16', end: '2025-03-05', progress: 40, status: 'progress' },
      { id: 32, name: '后端开发', start: '2025-02-16', end: '2025-03-05', progress: 35, status: 'progress' },
      { id: 33, name: '接口联调', start: '2025-03-05', end: '2025-03-10', progress: 0, status: 'pending' }
    ]
  },
  { id: 4, name: '测试阶段', start: '2025-03-11', end: '2025-03-20', progress: 0, status: 'pending' },
  { id: 5, name: '项目上线', start: '2025-03-21', end: '2025-03-21', progress: 0, status: 'pending', isMilestone: true },
  { id: 6, name: '关键路径任务', start: '2025-02-10', end: '2025-02-20', progress: 50, status: 'critical', dependencies: [11] }
])

const ganttStartDate = ref(new Date('2025-02-01'))

const handleTaskClick = (task) => {
  console.log('Task clicked:', task)
}

const handleTaskUpdate = (task) => {
  console.log('Task updated:', task)
}
</script>

<template>
  <div class="components-page">
    <div class="container">
      <div class="page-header">
        <h1>组件库文档</h1>
        <p>完整的设计系统组件库和使用指南</p>
      </div>

      <!-- 可拖拽网格组件 -->
      <section class="component-section">
        <h2>可拖拽网格 DraggableGrid</h2>
        <p class="component-desc">支持网格对齐、碰撞检测与挤压、自动向上吸附的拖拽布局组件</p>

        <div class="component-demo">
          <div class="demo-toolbar">
            <button class="btn btn-primary btn-sm" @click="addGridItem">
              <span>➕</span> 添加卡片
            </button>
            <button class="btn btn-outline btn-sm" @click="removeLastItem">
              <span>🗑️</span> 删除最后
            </button>
          </div>

          <DraggableGrid
            ref="gridRef"
            v-model="gridItems"
            :cols="4"
            :cell-width="120"
            :row-height="100"
            :gap="16"
            :auto-compact="true"
            :show-grid-lines="true"
            @change="handleGridChange"
          >
            <template #default="{ item, isDragging }">
              <div class="demo-grid-item" :class="{ 'is-dragging': isDragging }" v-if="item">
                <div class="item-icon">📦</div>
                <div class="item-label">{{ item.label || item.id }}</div>
                <div class="item-size">{{ item.w }}×{{ item.h }}</div>
              </div>
            </template>
          </DraggableGrid>
        </div>

        <div class="component-features">
          <h4>功能特性：</h4>
          <ul>
            <li><strong>网格对齐</strong> - 拖拽过程中实时对齐网格</li>
            <li><strong>碰撞检测与挤压</strong> - 拖拽组件A到组件B位置时，B自动让路</li>
            <li><strong>自动向上吸附</strong> - 组件移走后，下方组件自动上浮填补空缺</li>
          </ul>
        </div>

        <div class="code-example">
          <pre v-pre><code>&lt;DraggableGrid
  v-model="items"
  :cols="4"
  :cell-width="120"
  :row-height="100"
  :gap="16"
  :auto-compact="true"
&gt;
  &lt;template #default="{ item }"&gt;
    &lt;div class="grid-item"&gt;{{ item.label }}&lt;/div&gt;
  &lt;/template&gt;
&lt;/DraggableGrid&gt;</code></pre>
        </div>
      </section>

      <!-- 甘特图组件 -->
      <section class="component-section">
        <h2>甘特图 GanttChart</h2>
        <p class="component-desc">功能完整的项目管理甘特图组件，支持任务分组、里程碑、依赖关系</p>

        <div class="component-demo gantt-demo">
          <GanttChart
            :tasks="ganttTasks"
            :start-date="ganttStartDate"
            :view-days="60"
            :unit-width="40"
            :row-height="40"
            :sidebar-width="180"
            :show-current-time="true"
            :show-dependencies="true"
            @task-click="handleTaskClick"
            @task-update="handleTaskUpdate"
          />
        </div>

        <div class="component-features">
          <h4>功能特性：</h4>
          <ul>
            <li><strong>任务分组</strong> - 支持可折叠的任务组</li>
            <li><strong>里程碑</strong> - 标记关键节点</li>
            <li><strong>依赖关系</strong> - 可视化任务间的依赖连线</li>
            <li><strong>进度追踪</strong> - 显示任务完成百分比</li>
            <li><strong>当前时间线</strong> - 标记当前日期位置</li>
            <li><strong>状态标识</strong> - 待开始/进行中/已完成/已延期/关键路径</li>
          </ul>
        </div>

        <div class="code-example">
          <pre><code>&lt;GanttChart
  :tasks="tasks"
  :start-date="new Date('2025-02-01')"
  :view-days="60"
  :show-dependencies="true"
  @task-click="handleTaskClick"
/&gt;</code></pre>
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
        <div class="code-example">
          <pre><code>&lt;button class="btn btn-primary"&gt;主要按钮&lt;/button&gt;
&lt;button class="btn btn-secondary"&gt;次要按钮&lt;/button&gt;
&lt;button class="btn btn-outline"&gt;边框按钮&lt;/button&gt;</code></pre>
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
        <div class="code-example">
          <pre><code>&lt;div class="card"&gt;
  &lt;h3&gt;卡片标题&lt;/h3&gt;
  &lt;p&gt;卡片内容&lt;/p&gt;
&lt;/div&gt;</code></pre>
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
        <div class="code-example">
          <pre><code>&lt;input type="text" class="input" placeholder="请输入内容"&gt;</code></pre>
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
        <div class="code-example">
          <pre><code>&lt;span class="badge"&gt;默认标签&lt;/span&gt;
&lt;span class="badge badge-primary"&gt;主要标签&lt;/span&gt;</code></pre>
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
        <div class="code-example">
          <pre><code>&lt;div class="grid grid-3"&gt;
  &lt;div&gt;列 1&lt;/div&gt;
  &lt;div&gt;列 2&lt;/div&gt;
  &lt;div&gt;列 3&lt;/div&gt;
&lt;/div&gt;</code></pre>
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

.code-example {
  background: var(--gray-50);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  border: 1px solid var(--gray-200);
}

.code-example pre {
  margin: 0;
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  color: var(--gray-700);
  overflow-x: auto;
}

.code-example code {
  font-family: var(--font-mono);
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

/* 可拖拽网格组件样式 */
.component-desc {
  color: var(--gray-600);
  margin-bottom: var(--space-lg);
  font-size: var(--text-base);
}

.demo-toolbar {
  display: flex;
  gap: var(--space-md);
  margin-bottom: var(--space-lg);
  flex-wrap: wrap;
}

.demo-grid-item {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  transition: all 0.2s ease;
  box-shadow: var(--shadow);
}

.demo-grid-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.demo-grid-item.is-dragging {
  transform: scale(1.02);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.demo-grid-item .item-icon {
  font-size: 1.5rem;
  margin-bottom: var(--space-xs);
}

.demo-grid-item .item-label {
  font-weight: 600;
  font-size: var(--text-sm);
}

.demo-grid-item .item-size {
  font-size: var(--text-xs);
  opacity: 0.8;
  margin-top: var(--space-xs);
}

.component-features {
  background: var(--gray-50);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  margin-bottom: var(--space-lg);
  border-left: 4px solid var(--primary);
}

.component-features h4 {
  margin-bottom: var(--space-md);
  color: var(--gray-900);
}

.component-features ul {
  margin: 0;
  padding-left: var(--space-lg);
  color: var(--gray-700);
}

.component-features li {
  margin-bottom: var(--space-sm);
  line-height: 1.6;
}

.component-features li:last-child {
  margin-bottom: 0;
}

/* 甘特图演示样式 */
.gantt-demo {
  overflow-x: auto;
  padding: var(--space-md);
  background: var(--gray-50);
  border-radius: var(--radius-md);
}

@media (max-width: 768px) {
  .demo-group {
    flex-direction: column;
  }

  .demo-toolbar {
    flex-direction: column;
  }

  .demo-toolbar .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
