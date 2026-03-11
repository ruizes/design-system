<template>
  <div class="components-page">
    <div class="container">
      <div class="page-header">
        <h1>组件库文档</h1>
        <p>完整的设计系统组件库和使用指南</p>
      </div>

      <!-- 模态框组件 -->
      <section class="component-section">
        <h2>模态框 Modal</h2>
        <div class="component-demo">
          <div class="demo-group">
            <button class="btn btn-primary" @click="openModal('basic')">基础模态框</button>
            <button class="btn btn-primary" @click="openModal('form')">表单模态框</button>
            <button class="btn btn-primary" @click="openModal('confirm')">确认对话框</button>
          </div>
        </div>
        <div class="code-example">
          <pre><code>&lt;Modal v-model="visible" title="模态框标题"&gt;
  &lt;p&gt;模态框内容&lt;/p&gt;
  &lt;template #footer&gt;
    &lt;button class="btn btn-outline" @click="visible = false"&gt;取消&lt;/button&gt;
    &lt;button class="btn btn-primary" @click="handleConfirm"&gt;确认&lt;/button&gt;
  &lt;/template&gt;
&lt;/Modal&gt;</code></pre>
        </div>
      </section>

      <!-- 标签页组件 -->
      <section class="component-section">
        <h2>标签页 Tabs</h2>
        <div class="component-demo">
          <Tabs :tabs="tabs" v-model="activeTab">
            <template #tab-0>
              <div class="tab-content">
                <h3>基础用法</h3>
                <p>这是第一个标签页的内容。标签页组件支持图标、徽章和禁用状态。</p>
              </div>
            </template>
            <template #tab-1>
              <div class="tab-content">
                <h3>高级功能</h3>
                <p>标签页组件支持多种配置选项，可以满足不同场景的需求。</p>
              </div>
            </template>
            <template #tab-2>
              <div class="tab-content">
                <h3>使用示例</h3>
                <p>这里展示了标签页组件的各种使用方式和最佳实践。</p>
              </div>
            </template>
          </Tabs>
        </div>
        <div class="code-example">
          <pre><code>&lt;Tabs :tabs="tabs" v-model="activeTab"&gt;
  &lt;template #tab-0&gt;第一个标签页内容&lt;/template&gt;
  &lt;template #tab-1&gt;第二个标签页内容&lt;/template&gt;
&lt;/Tabs&gt;</code></pre>
        </div>
      </section>

      <!-- 下拉菜单组件 -->
      <section class="component-section">
        <h2>下拉菜单 Dropdown</h2>
        <div class="component-demo">
          <div class="demo-group">
            <Dropdown trigger-text="基础下拉">
              <DropdownItem @click="handleAction">选项一</DropdownItem>
              <DropdownItem @click="handleAction">选项二</DropdownItem>
              <DropdownItem @click="handleAction">选项三</DropdownItem>
            </Dropdown>
            
            <Dropdown trigger-text="带图标菜单">
              <DropdownItem icon="📄" @click="handleAction">新建文件</DropdownItem>
              <DropdownItem icon="📂" @click="handleAction">打开文件夹</DropdownItem>
              <DropdownItem icon="💾" @click="handleAction">保存</DropdownItem>
              <hr class="dropdown-divider">
              <DropdownItem icon="🗑️" danger @click="handleAction">删除</DropdownItem>
            </Dropdown>
          </div>
        </div>
        <div class="code-example">
          <pre><code>&lt;Dropdown trigger-text="下拉菜单"&gt;
  &lt;DropdownItem @click="handleAction"&gt;选项一&lt;/DropdownItem&gt;
  &lt;DropdownItem icon="📄" @click="handleAction"&gt;新建文件&lt;/DropdownItem&gt;
  &lt;hr class="dropdown-divider"&gt;
  &lt;DropdownItem danger @click="handleAction"&gt;删除&lt;/DropdownItem&gt;
&lt;/Dropdown&gt;</code></pre>
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

    <!-- 模态框实例 -->
    <Modal v-model="basicModalVisible" title="基础模态框">
      <p>这是一个基础模态框的内容。您可以在这里放置任何内容，包括文本、表单或其他组件。</p>
      <template #footer>
        <button class="btn btn-outline" @click="closeModal">取消</button>
        <button class="btn btn-primary" @click="handleConfirm">确认</button>
      </template>
    </Modal>

    <Modal v-model="formModalVisible" title="表单模态框" size="lg">
      <div class="form-group">
        <label>姓名</label>
        <input type="text" class="input" v-model="formData.name" placeholder="请输入姓名">
      </div>
      <div class="form-group">
        <label>邮箱</label>
        <input type="email" class="input" v-model="formData.email" placeholder="请输入邮箱">
      </div>
      <template #footer>
        <button class="btn btn-outline" @click="closeModal">取消</button>
        <button class="btn btn-primary" @click="submitForm">提交</button>
      </template>
    </Modal>

    <Modal v-model="confirmModalVisible" title="确认操作" size="sm">
      <p>您确定要执行此操作吗？此操作不可撤销。</p>
      <template #footer>
        <button class="btn btn-outline" @click="closeModal">取消</button>
        <button class="btn btn-danger" @click="handleConfirm">确认删除</button>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Modal from '../components/Modal.vue'
import Tabs from '../components/Tabs.vue'
import Dropdown from '../components/Dropdown.vue'
import DropdownItem from '../components/DropdownItem.vue'

// 模态框状态
const modalType = ref('')
const basicModalVisible = ref(false)
const formModalVisible = ref(false)
const confirmModalVisible = ref(false)

const openModal = (type) => {
  modalType.value = type
  if (type === 'basic') basicModalVisible.value = true
  if (type === 'form') formModalVisible.value = true
  if (type === 'confirm') confirmModalVisible.value = true
}

const closeModal = () => {
  basicModalVisible.value = false
  formModalVisible.value = false
  confirmModalVisible.value = false
}

const handleConfirm = () => {
  alert('确认操作已执行！')
  closeModal()
}

// 标签页数据
const activeTab = ref(0)
const tabs = ref([
  { label: '基础用法', icon: '📋' },
  { label: '高级功能', icon: '⚡', badge: 3 },
  { label: '使用示例', icon: '📝' },
  { label: '禁用状态', disabled: true }
])

// 下拉菜单操作
const handleAction = () => {
  console.log('菜单项被点击')
}

// 表单数据
const formData = ref({
  name: '',
  email: ''
})

const submitForm = () => {
  alert(`表单提交成功！\n姓名: ${formData.value.name}\n邮箱: ${formData.value.email}`)
  closeModal()
  formData.value = { name: '', email: '' }
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

@media (max-width: 768px) {
  .demo-group {
    flex-direction: column;
  }
}
</style>
