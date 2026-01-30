<template>
  <div class="components-page">
    <div class="container">
      <div class="page-header">
        <h1>组件库文档</h1>
        <p>完整的设计系统组件库和使用指南</p>
      </div>

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

      <!-- 网格布局组件 -->
      <section class="component-section">
        <h2>网格布局组件 GridLayout</h2>
        <p>一个支持拖拽、网格对齐、碰撞检测和自动吸附的网格布局组件。</p>
        <div class="component-demo">
          <GridLayout
            :width="800"
            :height="400"
            :grid-size="20"
            v-model="gridLayoutItems"
            @item-move="onItemMove"
          >
            <template #item="{ item }">
              <div class="custom-grid-item">
                <div class="item-header">{{ item && item.content ? item.content : '' }}</div>
                <div class="item-body">
                  <p>大小: {{ item && item.width ? item.width : 0 }} × {{ item && item.height ? item.height : 0 }}</p>
                  <p>位置: {{ item && item.x ? item.x : 0 }}, {{ item && item.y ? item.y : 0 }}</p>
                </div>
              </div>
            </template>
          </GridLayout>
        </div>
        <div class="component-features">
          <h3>主要功能</h3>
          <ul>
            <li>网格对齐：拖拽时自动对齐到网格</li>
            <li>碰撞检测：拖拽组件时会推动其他组件</li>
            <li>自动吸附：移走组件后，下方组件自动向上填充空缺</li>
            <li>自定义内容：支持插槽自定义每个网格项的内容</li>
          </ul>
        </div>
        <div class="code-example">
          <pre><code>&lt;GridLayout
  :width="800"
  :height="400"
  :grid-size="20"
  v-model="gridLayoutItems"
  @item-move="onItemMove"
&gt;
  &lt;template #item="{ item }"&gt;
    &lt;div class="custom-item"&gt;{{ item && item.content ? item.content : '' }}&lt;/div&gt;
  &lt;/template&gt;
&lt;/GridLayout&gt;</code></pre>
        </div>
      </section>

      <!-- 甘特图组件 -->
      <section class="component-section">
        <h2>甘特图组件 GanttChart</h2>
        <p>一个用于项目进度管理的甘特图组件，支持任务展示、进度跟踪和详情查看。</p>
        <div class="component-demo">
          <GanttChart
            :tasks="ganttTasks"
            :start-date="ganttStartDate"
            :end-date="ganttEndDate"
            :width="900"
            :row-height="50"
            :day-width="25"
            @task-select="onTaskSelect"
          />
        </div>
        <div class="component-features">
          <h3>主要功能</h3>
          <ul>
            <li>时间轴展示：按月份和日期显示时间轴</li>
            <li>任务条形图：可视化展示任务时间跨度</li>
            <li>进度显示：每个任务条内显示完成进度</li>
            <li>周末标记：区分工作日和周末</li>
            <li>今日线：标记当前日期位置</li>
            <li>任务详情：点击任务查看详细信息</li>
          </ul>
        </div>
        <div class="code-example">
          <pre><code>&lt;GanttChart
  :tasks="tasks"
  :start-date="startDate"
  :end-date="endDate"
  :width="900"
  :row-height="50"
  :day-width="25"
  @task-select="onTaskSelect"
/&gt;</code></pre>
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

<script>
import { ref } from 'vue'
import GridLayout from '../components/GridLayout.vue'
import GanttChart from '../components/GanttChart.vue'

export default {
  name: 'ComponentsPage',
  components: {
    GridLayout,
    GanttChart
  },
  setup() {
    // 网格布局示例数据
    const gridLayoutItems = ref([
      { id: '1', x: 0, y: 0, width: 200, height: 150, content: '项目 1' },
      { id: '2', x: 220, y: 0, width: 180, height: 150, content: '项目 2' },
      { id: '3', x: 0, y: 170, width: 200, height: 120, content: '项目 3' },
      { id: '4', x: 220, y: 170, width: 180, height: 120, content: '项目 4' },
      { id: '5', x: 420, y: 0, width: 160, height: 100, content: '项目 5' }
    ])
    
    // 甘特图示例数据
    const ganttTasks = ref([
      {
        id: '1',
        name: '需求分析',
        assignee: '张三',
        startDate: '2025-01-01',
        endDate: '2025-01-15',
        progress: 100,
        critical: true,
        description: '收集和分析项目需求，制定项目计划'
      },
      {
        id: '2',
        name: 'UI设计',
        assignee: '李四',
        startDate: '2025-01-10',
        endDate: '2025-01-25',
        progress: 80,
        critical: false,
        description: '设计用户界面和交互流程'
      },
      {
        id: '3',
        name: '前端开发',
        assignee: '王五',
        startDate: '2025-01-20',
        endDate: '2025-02-10',
        progress: 60,
        critical: true,
        description: '实现前端功能和用户界面'
      },
      {
        id: '4',
        name: '后端开发',
        assignee: '赵六',
        startDate: '2025-01-15',
        endDate: '2025-02-05',
        progress: 70,
        critical: true,
        description: '实现后端API和数据库设计'
      },
      {
        id: '5',
        name: '测试',
        assignee: '钱七',
        startDate: '2025-02-05',
        endDate: '2025-02-20',
        progress: 20,
        critical: false,
        description: '进行功能测试和性能测试'
      }
    ])
    
    // 甘特图时间范围
    const ganttStartDate = ref(new Date('2025-01-01'))
    const ganttEndDate = ref(new Date('2025-02-28'))
    
    // 网格布局项目移动事件
    const onItemMove = (event) => {
      console.log('项目移动:', event)
    }
    
    // 甘特图任务选择事件
    const onTaskSelect = (task) => {
      console.log('任务选择:', task)
    }
    
    return {
      gridLayoutItems,
      ganttTasks,
      ganttStartDate,
      ganttEndDate,
      onItemMove,
      onTaskSelect
    }
  }
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

.component-features {
  background: var(--gray-50);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  margin-bottom: var(--space-xl);
  border-left: 4px solid var(--primary);
}

.component-features h3 {
  margin-top: 0;
  margin-bottom: var(--space-md);
  color: var(--primary);
}

.component-features ul {
  margin: 0;
  padding-left: var(--space-xl);
}

.component-features li {
  margin-bottom: var(--space-sm);
  color: var(--gray-700);
}

.custom-grid-item {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border-radius: var(--radius-md);
  padding: var(--space-md);
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow);
}

.item-header {
  font-weight: 600;
  margin-bottom: var(--space-sm);
  font-size: var(--text-lg);
}

.item-body {
  font-size: var(--text-sm);
  opacity: 0.9;
}

.item-body p {
  margin: 0;
  margin-bottom: var(--space-xs);
}

@media (max-width: 768px) {
  .demo-group {
    flex-direction: column;
  }
}
</style>
