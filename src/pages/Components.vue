<template>
  <div class="components-page">
    <div class="container">
      <div class="page-header">
        <h1>组件库文档</h1>
        <p>完整的设计系统组件库和使用指南</p>
      </div>

      <!-- 可拖拽网格布局组件 -->
      <section class="component-section">
        <h2>可拖拽网格布局 GridLayout</h2>
        <p class="section-description">支持网格对齐、碰撞检测与挤压、自动向上吸附的智能布局组件</p>
        <div class="component-demo">
          <GridLayout
            :items="gridItems"
            :container-width="800"
            :container-height="400"
            :cols="20"
            :rows="10"
            :cell-width="40"
            :cell-height="40"
            :show-grid="true"
            @update:items="gridItems = $event"
          >
            <template #item="{ item }">
              <div class="grid-item-demo" :style="{ background: item.color }">
                <div class="grid-item-title">{{ item.title }}</div>
                <div class="grid-item-info">{{ item.info }}</div>
              </div>
            </template>
          </GridLayout>
        </div>
        <div class="grid-demo-tips">
          <span>💡 提示：拖拽组件到其他组件上会触发碰撞挤压，移走组件后下方组件会自动向上吸附</span>
        </div>
        <div class="code-example">
          <pre><code>&lt;GridLayout
  :items="items"
  :container-width="800"
  :container-height="400"
  :cols="20"
  :rows="10"
  :cell-width="40"
  :cell-height="40"
  :show-grid="true"
  @update:items="items = $event"
&gt;
  &lt;template #item="{ item }"&gt;
    {{ item.content }}
  &lt;/template&gt;
&lt;/GridLayout&gt;</code></pre>
        </div>
      </section>

      <!-- 甘特图组件 -->
      <section class="component-section">
        <h2>甘特图 GanttChart</h2>
        <p class="section-description">用于项目管理的甘特图组件，支持拖拽调整任务时间、缩放等功能</p>
        <div class="component-demo">
          <GanttChart
            :tasks="ganttTasks"
            :dependencies="ganttDependencies"
            title="项目计划"
            start-date="2025-01-01"
            end-date="2025-03-31"
            @task-moved="handleTaskMoved"
            @task-resized="handleTaskResized"
          />
        </div>
        <div class="code-example">
          <pre><code>&lt;GanttChart
  :tasks="tasks"
  :dependencies="dependencies"
  title="项目计划"
  start-date="2025-01-01"
  end-date="2025-03-31"
  @task-moved="onTaskMoved"
  @task-resized="onTaskResized"
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

<script setup>
import { ref } from 'vue';
import GridLayout from '../components/GridLayout.vue';
import GanttChart from '../components/GanttChart.vue';

const gridItems = ref([
  {
    id: 1,
    x: 0,
    y: 0,
    width: 160,
    height: 80,
    title: '组件 A',
    info: '拖拽我试试',
    color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    id: 2,
    x: 200,
    y: 0,
    width: 120,
    height: 120,
    title: '组件 B',
    info: '可调整大小',
    color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  {
    id: 3,
    x: 360,
    y: 0,
    width: 200,
    height: 80,
    title: '组件 C',
    info: '碰撞检测',
    color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  },
  {
    id: 4,
    x: 0,
    y: 120,
    width: 280,
    height: 100,
    title: '组件 D',
    info: '自动吸附',
    color: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
  },
  {
    id: 5,
    x: 320,
    y: 120,
    width: 160,
    height: 120,
    title: '组件 E',
    info: '智能布局',
    color: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
  }
]);

const ganttTasks = ref([
  {
    id: 1,
    name: '需求分析',
    startDate: '2025-01-01',
    endDate: '2025-01-15',
    progress: 100,
    color: '#667eea',
    level: 0
  },
  {
    id: 2,
    name: '设计阶段',
    startDate: '2025-01-10',
    endDate: '2025-01-25',
    progress: 80,
    color: '#f093fb',
    level: 0
  },
  {
    id: 3,
    name: '前端开发',
    startDate: '2025-01-20',
    endDate: '2025-02-15',
    progress: 50,
    color: '#4facfe',
    level: 0
  },
  {
    id: 4,
    name: '后端开发',
    startDate: '2025-01-20',
    endDate: '2025-02-20',
    progress: 40,
    color: '#43e97b',
    level: 0
  },
  {
    id: 5,
    name: '测试阶段',
    startDate: '2025-02-10',
    endDate: '2025-02-28',
    progress: 0,
    color: '#fa709a',
    level: 0
  },
  {
    id: 6,
    name: '项目上线',
    startDate: '2025-03-01',
    endDate: '2025-03-05',
    progress: 0,
    color: '#a8edea',
    level: 0,
    isMilestone: true
  }
]);

const ganttDependencies = ref([
  { id: 1, from: 1, to: 2 },
  { id: 2, from: 2, to: 3 },
  { id: 3, from: 2, to: 4 },
  { id: 4, from: 3, to: 5 },
  { id: 5, from: 4, to: 5 },
  { id: 6, from: 5, to: 6 }
]);

const handleTaskMoved = (event) => {
  const task = ganttTasks.value.find(t => t.id === event.task.id);
  if (task) {
    task.startDate = event.newStartDate;
    task.endDate = event.newEndDate;
  }
};

const handleTaskResized = (event) => {
  const task = ganttTasks.value.find(t => t.id === event.task.id);
  if (task) {
    task.startDate = event.startDate;
    task.endDate = event.endDate;
  }
};
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

.section-description {
  color: var(--gray-600);
  margin-bottom: var(--space-lg);
  font-size: var(--text-base);
}

.grid-demo-tips {
  background: var(--gray-50);
  padding: var(--space-md);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-xl);
  border-left: 3px solid var(--primary);
  font-size: var(--text-sm);
  color: var(--gray-700);
}

.grid-item-demo {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  border-radius: var(--radius-md);
}

.grid-item-title {
  font-weight: 600;
  font-size: var(--text-base);
  margin-bottom: var(--space-xs);
}

.grid-item-info {
  font-size: var(--text-sm);
  opacity: 0.9;
}

@media (max-width: 768px) {
  .demo-group {
    flex-direction: column;
  }
}
</style>
