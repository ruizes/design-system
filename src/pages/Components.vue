<template>
  <div class="components-page">
    <div class="container">
      <div class="page-header">
        <h1>组件库文档</h1>
        <p>完整的设计系统组件库和使用指南</p>
      </div>

      <section class="component-section">
        <h2>DsButton 按钮组件</h2>
        <p class="section-description">
          DsButton 是一个功能完整的 Vue 按钮组件，支持多种变体、尺寸、状态和图标。
        </p>

        <div class="component-subsection">
          <h3>按钮变体 Variants</h3>
          <div class="demo-group">
            <DsButton variant="primary">主要按钮</DsButton>
            <DsButton variant="secondary">次要按钮</DsButton>
            <DsButton variant="outline">边框按钮</DsButton>
            <DsButton variant="text">文本按钮</DsButton>
            <DsButton variant="ghost">幽灵按钮</DsButton>
          </div>
          <div class="code-example">
            <pre><code>&lt;DsButton variant="primary"&gt;主要按钮&lt;/DsButton&gt;
&lt;DsButton variant="secondary"&gt;次要按钮&lt;/DsButton&gt;
&lt;DsButton variant="outline"&gt;边框按钮&lt;/DsButton&gt;
&lt;DsButton variant="text"&gt;文本按钮&lt;/DsButton&gt;
&lt;DsButton variant="ghost"&gt;幽灵按钮&lt;/DsButton&gt;</code></pre>
          </div>
        </div>

        <div class="component-subsection">
          <h3>语义按钮 Semantic Buttons</h3>
          <div class="demo-group">
            <DsButton variant="success">成功按钮</DsButton>
            <DsButton variant="warning">警告按钮</DsButton>
            <DsButton variant="danger">危险按钮</DsButton>
          </div>
          <div class="code-example">
            <pre><code>&lt;DsButton variant="success"&gt;成功按钮&lt;/DsButton&gt;
&lt;DsButton variant="warning"&gt;警告按钮&lt;/DsButton&gt;
&lt;DsButton variant="danger"&gt;危险按钮&lt;/DsButton&gt;</code></pre>
          </div>
        </div>

        <div class="component-subsection">
          <h3>按钮尺寸 Sizes</h3>
          <div class="demo-group demo-group-aligned">
            <DsButton variant="primary" size="sm">小按钮</DsButton>
            <DsButton variant="primary" size="default">默认按钮</DsButton>
            <DsButton variant="primary" size="lg">大按钮</DsButton>
          </div>
          <div class="code-example">
            <pre><code>&lt;DsButton variant="primary" size="sm"&gt;小按钮&lt;/DsButton&gt;
&lt;DsButton variant="primary" size="default"&gt;默认按钮&lt;/DsButton&gt;
&lt;DsButton variant="primary" size="lg"&gt;大按钮&lt;/DsButton&gt;</code></pre>
          </div>
        </div>

        <div class="component-subsection">
          <h3>禁用状态 Disabled</h3>
          <div class="demo-group">
            <DsButton variant="primary" disabled>禁用按钮</DsButton>
            <DsButton variant="secondary" disabled>禁用按钮</DsButton>
            <DsButton variant="outline" disabled>禁用按钮</DsButton>
            <DsButton variant="text" disabled>禁用按钮</DsButton>
          </div>
          <div class="code-example">
            <pre><code>&lt;DsButton variant="primary" disabled&gt;禁用按钮&lt;/DsButton&gt;
&lt;DsButton variant="secondary" disabled&gt;禁用按钮&lt;/DsButton&gt;
&lt;DsButton variant="outline" disabled&gt;禁用按钮&lt;/DsButton&gt;</code></pre>
          </div>
        </div>

        <div class="component-subsection">
          <h3>加载状态 Loading</h3>
          <div class="demo-group">
            <DsButton variant="primary" loading>加载中</DsButton>
            <DsButton variant="secondary" loading>加载中</DsButton>
            <DsButton variant="outline" loading>加载中</DsButton>
            <DsButton @click="toggleLoading">
              {{ isLoading ? '加载中' : '点击加载' }}
              <template v-if="isLoading" :loading="true"></template>
            </DsButton>
          </div>
          <div class="code-example">
            <pre><code>&lt;DsButton variant="primary" loading&gt;加载中&lt;/DsButton&gt;
&lt;DsButton variant="secondary" loading&gt;加载中&lt;/DsButton&gt;
&lt;DsButton variant="outline" loading&gt;加载中&lt;/DsButton&gt;</code></pre>
          </div>
        </div>

        <div class="component-subsection">
          <h3>图标按钮 Icon Buttons</h3>
          <div class="demo-group">
            <DsButton variant="primary" icon="❤️">收藏</DsButton>
            <DsButton variant="secondary" icon="⭐">收藏</DsButton>
            <DsButton variant="outline" icon="🔍">搜索</DsButton>
            <DsButton variant="text" icon="⚙️">设置</DsButton>
          </div>
          <div class="code-example">
            <pre><code>&lt;DsButton variant="primary" icon="❤️"&gt;收藏&lt;/DsButton&gt;
&lt;DsButton variant="secondary" icon="⭐"&gt;收藏&lt;/DsButton&gt;
&lt;DsButton variant="outline" icon="🔍"&gt;搜索&lt;/DsButton&gt;</code></pre>
          </div>
        </div>

        <div class="component-subsection">
          <h3>纯图标按钮 Icon Only Buttons</h3>
          <div class="demo-group">
            <DsButton variant="primary" icon="❤️" size="sm"></DsButton>
            <DsButton variant="primary" icon="⭐"></DsButton>
            <DsButton variant="primary" icon="🔍" size="lg"></DsButton>
            <DsButton variant="outline" icon="⚙️"></DsButton>
            <DsButton variant="ghost" icon="✏️"></DsButton>
            <DsButton variant="text" icon="🗑️"></DsButton>
          </div>
          <div class="code-example">
            <pre><code>&lt;DsButton variant="primary" icon="❤️" size="sm"&gt;&lt;/DsButton&gt;
&lt;DsButton variant="primary" icon="⭐"&gt;&lt;/DsButton&gt;
&lt;DsButton variant="outline" icon="⚙️"&gt;&lt;/DsButton&gt;
&lt;DsButton variant="ghost" icon="✏️"&gt;&lt;/DsButton&gt;</code></pre>
          </div>
        </div>

        <div class="component-subsection">
          <h3>圆形图标按钮 Circle Icon Buttons</h3>
          <div class="demo-group">
            <DsButton variant="primary" icon="❤️" circle size="sm"></DsButton>
            <DsButton variant="primary" icon="⭐" circle></DsButton>
            <DsButton variant="primary" icon="🔍" circle size="lg"></DsButton>
            <DsButton variant="outline" icon="⚙️" circle></DsButton>
            <DsButton variant="ghost" icon="✏️" circle></DsButton>
            <DsButton variant="text" icon="🗑️" circle></DsButton>
          </div>
          <div class="code-example">
            <pre><code>&lt;DsButton variant="primary" icon="❤️" circle size="sm"&gt;&lt;/DsButton&gt;
&lt;DsButton variant="primary" icon="⭐" circle&gt;&lt;/DsButton&gt;
&lt;DsButton variant="outline" icon="⚙️" circle&gt;&lt;/DsButton&gt;</code></pre>
          </div>
        </div>

        <div class="component-subsection">
          <h3>右侧图标按钮 Right Icon Buttons</h3>
          <div class="demo-group">
            <DsButton variant="primary" icon-right="➡️">下一步</DsButton>
            <DsButton variant="outline" icon-right="🡒">继续</DsButton>
            <DsButton variant="text" icon-right="→">查看更多</DsButton>
          </div>
          <div class="code-example">
            <pre><code>&lt;DsButton variant="primary" icon-right="➡️"&gt;下一步&lt;/DsButton&gt;
&lt;DsButton variant="outline" icon-right="🡒"&gt;继续&lt;/DsButton&gt;</code></pre>
          </div>
        </div>

        <div class="component-subsection">
          <h3>块级按钮 Block Buttons</h3>
          <div class="demo-blocks">
            <DsButton variant="primary" block>块级主要按钮</DsButton>
            <DsButton variant="outline" block>块级边框按钮</DsButton>
            <DsButton variant="text" block>块级文本按钮</DsButton>
          </div>
          <div class="code-example">
            <pre><code>&lt;DsButton variant="primary" block&gt;块级主要按钮&lt;/DsButton&gt;
&lt;DsButton variant="outline" block&gt;块级边框按钮&lt;/DsButton&gt;</code></pre>
          </div>
        </div>

        <div class="component-subsection">
          <h3>组件属性 Props</h3>
          <div class="props-table-container">
            <table class="props-table">
              <thead>
                <tr>
                  <th>属性</th>
                  <th>类型</th>
                  <th>默认值</th>
                  <th>说明</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>variant</code></td>
                  <td>String</td>
                  <td><code>'primary'</code></td>
                  <td>按钮变体：primary, secondary, outline, text, ghost, danger, success, warning</td>
                </tr>
                <tr>
                  <td><code>size</code></td>
                  <td>String</td>
                  <td><code>'default'</code></td>
                  <td>按钮尺寸：sm, default, lg</td>
                </tr>
                <tr>
                  <td><code>disabled</code></td>
                  <td>Boolean</td>
                  <td><code>false</code></td>
                  <td>是否禁用</td>
                </tr>
                <tr>
                  <td><code>loading</code></td>
                  <td>Boolean</td>
                  <td><code>false</code></td>
                  <td>是否加载中</td>
                </tr>
                <tr>
                  <td><code>icon</code></td>
                  <td>String</td>
                  <td><code>null</code></td>
                  <td>左侧图标（emoji）</td>
                </tr>
                <tr>
                  <td><code>icon-right</code></td>
                  <td>String</td>
                  <td><code>null</code></td>
                  <td>右侧图标（emoji）</td>
                </tr>
                <tr>
                  <td><code>block</code></td>
                  <td>Boolean</td>
                  <td><code>false</code></td>
                  <td>是否为块级按钮</td>
                </tr>
                <tr>
                  <td><code>circle</code></td>
                  <td>Boolean</td>
                  <td><code>false</code></td>
                  <td>是否为圆形按钮</td>
                </tr>
                <tr>
                  <td><code>tag</code></td>
                  <td>String</td>
                  <td><code>'button'</code></td>
                  <td>渲染标签：button, a, router-link</td>
                </tr>
                <tr>
                  <td><code>native-type</code></td>
                  <td>String</td>
                  <td><code>'button'</code></td>
                  <td>原生按钮类型：button, submit, reset</td>
                </tr>
                <tr>
                  <td><code>href</code></td>
                  <td>String</td>
                  <td><code>null</code></td>
                  <td>链接地址（tag 为 a 时）</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="component-subsection">
          <h3>事件 Events</h3>
          <div class="props-table-container">
            <table class="props-table">
              <thead>
                <tr>
                  <th>事件名</th>
                  <th>参数</th>
                  <th>说明</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>click</code></td>
                  <td><code>event</code></td>
                  <td>点击事件（禁用和加载状态时不触发）</td>
                </tr>
              </tbody>
            </table>
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
import { ref } from 'vue'
import DsButton from '../components/DsButton.vue'

const isLoading = ref(false)

const toggleLoading = () => {
  isLoading.value = true
  setTimeout(() => {
    isLoading.value = false
  }, 2000)
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

.component-section > h2 {
  font-size: var(--text-2xl);
  margin-bottom: var(--space-xl);
  color: var(--gray-900);
  padding-bottom: var(--space-md);
  border-bottom: 2px solid var(--gray-200);
}

.section-description {
  margin-bottom: var(--space-xl);
  color: var(--gray-600);
  font-size: var(--text-base);
  line-height: 1.6;
}

.component-subsection {
  margin-bottom: var(--space-2xl);
}

.component-subsection:last-child {
  margin-bottom: 0;
}

.component-subsection h3 {
  font-size: var(--text-lg);
  font-weight: 600;
  margin-bottom: var(--space-lg);
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
  align-items: flex-start;
}

.demo-group-aligned {
  align-items: center;
}

.demo-blocks {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  max-width: 400px;
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
  white-space: pre-wrap;
  line-height: 1.6;
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

.props-table-container {
  overflow-x: auto;
}

.props-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);
}

.props-table th,
.props-table td {
  padding: var(--space-md);
  text-align: left;
  border-bottom: 1px solid var(--gray-200);
}

.props-table th {
  background: var(--gray-50);
  font-weight: 600;
  color: var(--gray-700);
}

.props-table td {
  color: var(--gray-600);
}

.props-table code {
  background: var(--gray-100);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--primary);
}

.props-table tr:hover td {
  background: var(--gray-50);
}

@media (max-width: 768px) {
  .demo-group {
    flex-direction: column;
  }
  
  .demo-group-aligned {
    align-items: stretch;
  }
  
  .props-table {
    font-size: var(--text-xs);
  }
  
  .props-table th,
  .props-table td {
    padding: var(--space-sm);
  }
}
</style>
