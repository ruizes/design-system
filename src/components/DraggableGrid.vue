<template>
  <div class="draggable-grid-container">
    <div class="grid-toolbar">
      <div class="toolbar-title">
        <span class="toolbar-icon">🎯</span>
        <span>可拖拽组件网格</span>
      </div>
      <div class="toolbar-actions">
        <button 
          class="btn btn-primary btn-sm" 
          @click="openComponentPalette"
        >
          <span class="btn-icon">➕</span>
          添加组件
        </button>
        <button 
          class="btn btn-outline btn-sm" 
          @click="clearAll"
          v-if="items.length > 0"
        >
          <span class="btn-icon">🗑️</span>
          清空全部
        </button>
      </div>
    </div>

    <div 
      class="grid-area"
      :class="{ 'grid-empty': items.length === 0 }"
      @dragover.prevent
      @drop="handleDrop"
    >
      <div 
        v-if="items.length === 0" 
        class="empty-state"
      >
        <div class="empty-icon">📦</div>
        <div class="empty-text">暂无组件</div>
        <div class="empty-hint">点击上方"添加组件"按钮开始</div>
        <button 
          class="btn btn-primary btn-sm" 
          @click="openComponentPalette"
        >
          添加第一个组件
        </button>
      </div>

      <transition-group 
        name="grid"
        tag="div"
        class="grid-items"
        :class="{ 'compact-mode': compactMode }"
      >
        <DraggableGridItem
          v-for="(item, index) in items"
          :key="item.id"
          :item="item"
          :index="index"
          :is-dragging="draggedItemId === item.id"
          :is-drop-target="dropTargetIndex === index"
          @drag-start="handleDragStart"
          @drag-end="handleDragEnd"
          @drag-over="handleDragOverItem"
          @delete="handleDeleteItem"
          @duplicate="handleDuplicateItem"
        />
      </transition-group>
    </div>

    <div 
      class="component-palette-overlay"
      :class="{ 'is-open': isPaletteOpen }"
      @click="closeComponentPalette"
    >
      <div 
        class="component-palette"
        @click.stop
      >
        <div class="palette-header">
          <div class="palette-title">
            <span class="palette-icon">🎨</span>
            选择组件
          </div>
          <button 
            class="palette-close"
            @click="closeComponentPalette"
          >
            ✕
          </button>
        </div>
        
        <div class="palette-search">
          <input 
            type="text" 
            class="input" 
            placeholder="搜索组件..."
            v-model="searchQuery"
          >
        </div>

        <div class="palette-categories">
          <button 
            v-for="category in categories"
            :key="category.id"
            class="category-btn"
            :class="{ 'is-active': activeCategory === category.id }"
            @click="activeCategory = category.id"
          >
            <span class="category-icon">{{ category.icon }}</span>
            <span class="category-label">{{ category.label }}</span>
            <span class="category-count">{{ getCategoryCount(category.id) }}</span>
          </button>
        </div>

        <div class="palette-components">
          <div 
            v-for="component in filteredComponents"
            :key="component.id"
            class="component-card"
            :class="{ 'disabled': isComponentDisabled(component) }"
            @click="addComponent(component)"
          >
            <div class="component-preview" :style="getComponentPreviewStyle(component)">
              <component :is="getPreviewComponent(component)" :config="component.defaultConfig" />
            </div>
            <div class="component-info">
              <div class="component-name">
                <span class="component-icon">{{ component.icon }}</span>
                {{ component.name }}
              </div>
              <div class="component-desc">{{ component.description }}</div>
              <div class="component-meta">
                <span class="component-size">
                  {{ component.defaultConfig.width }}×{{ component.defaultConfig.height }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div 
      class="grid-settings"
      v-if="items.length > 0"
    >
      <div class="settings-row">
        <label class="setting-label">
          <input 
            type="checkbox" 
            v-model="compactMode"
            class="setting-checkbox"
          >
          紧凑模式（自动吸附）
        </label>
        <div class="setting-info">
          <span class="setting-hint">组件数量: {{ items.length }}</span>
          <span class="setting-hint">网格列数: {{ gridColumns }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, nextTick } from 'vue'
import DraggableGridItem from './DraggableGridItem.vue'
import GridPreviewCard from './previews/GridPreviewCard.vue'
import GridPreviewButton from './previews/GridPreviewButton.vue'
import GridPreviewForm from './previews/GridPreviewForm.vue'
import GridPreviewStats from './previews/GridPreviewStats.vue'
import GridPreviewImage from './previews/GridPreviewImage.vue'
import GridPreviewText from './previews/GridPreviewText.vue'
import GridPreviewBadge from './previews/GridPreviewBadge.vue'
import GridPreviewList from './previews/GridPreviewList.vue'

const items = ref([
  {
    id: 'item-1',
    type: 'card',
    name: '产品卡片',
    icon: '🃏',
    config: {
      title: '企业版设计系统',
      description: '完整的企业级设计系统解决方案，包含所有组件和模板',
      price: '¥9,999',
      category: '企业版'
    },
    width: 1,
    height: 1
  },
  {
    id: 'item-2',
    type: 'stats',
    name: '统计面板',
    icon: '📊',
    config: {
      items: [
        { value: '50+', label: '组件数量' },
        { value: '100%', label: '响应式' },
        { value: '10KB', label: '核心大小' }
      ]
    },
    width: 2,
    height: 1
  },
  {
    id: 'item-3',
    type: 'form',
    name: '表单组件',
    icon: '📝',
    config: {
      title: '联系我们',
      fields: [
        { type: 'text', label: '姓名', placeholder: '请输入姓名' },
        { type: 'email', label: '邮箱', placeholder: '请输入邮箱' }
      ]
    },
    width: 1,
    height: 2
  },
  {
    id: 'item-4',
    type: 'button',
    name: '按钮组',
    icon: '🔘',
    config: {
      buttons: [
        { text: '主要按钮', variant: 'primary' },
        { text: '次要按钮', variant: 'secondary' },
        { text: '边框按钮', variant: 'outline' }
      ]
    },
    width: 1,
    height: 1
  }
])

const isPaletteOpen = ref(false)
const searchQuery = ref('')
const activeCategory = ref('all')
const compactMode = ref(true)

const draggedItemId = ref(null)
const draggedIndex = ref(-1)
const dropTargetIndex = ref(-1)

const categories = [
  { id: 'all', label: '全部', icon: '📦' },
  { id: 'layout', label: '布局', icon: '📐' },
  { id: 'data', label: '数据', icon: '📊' },
  { id: 'form', label: '表单', icon: '📝' },
  { id: 'media', label: '媒体', icon: '🖼️' },
  { id: 'interactive', label: '交互', icon: '🔘' }
]

const availableComponents = [
  {
    id: 'card',
    name: '卡片组件',
    icon: '🃏',
    category: 'layout',
    description: '基础卡片组件，用于展示内容',
    defaultConfig: {
      title: '卡片标题',
      description: '这是卡片的描述内容，可以包含详细信息。',
      price: null,
      category: null
    },
    width: 1,
    height: 1,
    previewType: 'card'
  },
  {
    id: 'stats',
    name: '统计面板',
    icon: '📊',
    category: 'data',
    description: '展示统计数据的面板组件',
    defaultConfig: {
      items: [
        { value: '1,234', label: '用户数' },
        { value: '567', label: '订单数' },
        { value: '89%', label: '满意度' }
      ]
    },
    width: 2,
    height: 1,
    previewType: 'stats'
  },
  {
    id: 'form',
    name: '表单组件',
    icon: '📝',
    category: 'form',
    description: '包含输入框、按钮的表单组件',
    defaultConfig: {
      title: '表单标题',
      fields: [
        { type: 'text', label: '姓名', placeholder: '请输入姓名' },
        { type: 'email', label: '邮箱', placeholder: '请输入邮箱' }
      ]
    },
    width: 1,
    height: 2,
    previewType: 'form'
  },
  {
    id: 'button',
    name: '按钮组',
    icon: '🔘',
    category: 'interactive',
    description: '多种样式的按钮组合',
    defaultConfig: {
      buttons: [
        { text: '主要按钮', variant: 'primary' },
        { text: '次要按钮', variant: 'secondary' },
        { text: '边框按钮', variant: 'outline' }
      ]
    },
    width: 1,
    height: 1,
    previewType: 'button'
  },
  {
    id: 'image',
    name: '图片组件',
    icon: '🖼️',
    category: 'media',
    description: '图片展示组件',
    defaultConfig: {
      src: null,
      alt: '图片描述',
      aspectRatio: '16:9'
    },
    width: 2,
    height: 1,
    previewType: 'image'
  },
  {
    id: 'text',
    name: '文本组件',
    icon: '📄',
    category: 'data',
    description: '富文本展示组件',
    defaultConfig: {
      title: '标题文本',
      content: '这是一段示例文本内容，可以包含多行文字。支持基本的格式化。',
      variant: 'default'
    },
    width: 1,
    height: 1,
    previewType: 'text'
  },
  {
    id: 'badge',
    name: '标签组',
    icon: '🏷️',
    category: 'data',
    description: '多种样式的标签组件',
    defaultConfig: {
      badges: [
        { text: '默认', variant: 'default' },
        { text: '主要', variant: 'primary' },
        { text: '成功', variant: 'success' },
        { text: '警告', variant: 'warning' }
      ]
    },
    width: 1,
    height: 1,
    previewType: 'badge'
  },
  {
    id: 'list',
    name: '列表组件',
    icon: '📋',
    category: 'data',
    description: '项目列表展示组件',
    defaultConfig: {
      title: '列表示例',
      items: [
        { text: '列表项 1', icon: '✨' },
        { text: '列表项 2', icon: '🚀' },
        { text: '列表项 3', icon: '💡' }
      ]
    },
    width: 1,
    height: 1,
    previewType: 'list'
  }
]

const filteredComponents = computed(() => {
  let result = availableComponents
  
  if (activeCategory.value !== 'all') {
    result = result.filter(c => c.category === activeCategory.value)
  }
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(c => 
      c.name.toLowerCase().includes(query) ||
      c.description.toLowerCase().includes(query)
    )
  }
  
  return result
})

const gridColumns = computed(() => {
  return 3
})

const getCategoryCount = (categoryId) => {
  if (categoryId === 'all') return availableComponents.length
  return availableComponents.filter(c => c.category === categoryId).length
}

const isComponentDisabled = (component) => {
  return false
}

const getComponentPreviewStyle = (component) => {
  return {}
}

const getPreviewComponent = (component) => {
  const map = {
    card: GridPreviewCard,
    button: GridPreviewButton,
    form: GridPreviewForm,
    stats: GridPreviewStats,
    image: GridPreviewImage,
    text: GridPreviewText,
    badge: GridPreviewBadge,
    list: GridPreviewList
  }
  return map[component.previewType] || GridPreviewCard
}

const generateId = () => {
  return `item-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

const openComponentPalette = () => {
  isPaletteOpen.value = true
  searchQuery.value = ''
  activeCategory.value = 'all'
}

const closeComponentPalette = () => {
  isPaletteOpen.value = false
}

const addComponent = (component) => {
  const newItem = {
    id: generateId(),
    type: component.id,
    name: component.name,
    icon: component.icon,
    config: JSON.parse(JSON.stringify(component.defaultConfig)),
    width: component.width,
    height: component.height
  }
  
  items.value.push(newItem)
  closeComponentPalette()
  
  if (compactMode.value) {
    nextTick(() => {
      compactItems()
    })
  }
}

const handleDeleteItem = (itemId) => {
  const index = items.value.findIndex(item => item.id === itemId)
  if (index !== -1) {
    items.value.splice(index, 1)
    
    if (compactMode.value) {
      nextTick(() => {
        compactItems()
      })
    }
  }
}

const handleDuplicateItem = (itemId) => {
  const index = items.value.findIndex(item => item.id === itemId)
  if (index !== -1) {
    const original = items.value[index]
    const newItem = {
      ...JSON.parse(JSON.stringify(original)),
      id: generateId(),
      name: `${original.name} (副本)`
    }
    items.value.splice(index + 1, 0, newItem)
  }
}

const handleDragStart = (item, index) => {
  draggedItemId.value = item.id
  draggedIndex.value = index
}

const handleDragEnd = () => {
  draggedItemId.value = null
  draggedIndex.value = -1
  dropTargetIndex.value = -1
}

const handleDragOverItem = (index) => {
  if (draggedIndex.value !== index && draggedIndex.value !== -1) {
    dropTargetIndex.value = index
  }
}

const handleDrop = () => {
  if (draggedIndex.value !== -1 && dropTargetIndex.value !== -1 && draggedIndex.value !== dropTargetIndex.value) {
    const [draggedItem] = items.value.splice(draggedIndex.value, 1)
    items.value.splice(dropTargetIndex.value, 0, draggedItem)
  }
  
  handleDragEnd()
}

const compactItems = () => {
  // 自动向上吸附：保持现有顺序，只是视觉上紧凑排列
  // 当前实现已经通过 CSS transition 实现了平滑动画
  // 这里可以添加额外的布局逻辑
}

const clearAll = () => {
  if (confirm('确定要清空所有组件吗？')) {
    items.value = []
  }
}
</script>

<style scoped>
.draggable-grid-container {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.grid-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-lg);
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
}

.toolbar-title {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: var(--text-xl);
  font-weight: 600;
  color: var(--gray-900);
}

.toolbar-icon {
  font-size: 1.5rem;
}

.toolbar-actions {
  display: flex;
  gap: var(--space-md);
}

.btn-icon {
  margin-right: var(--space-xs);
}

.grid-area {
  min-height: 300px;
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  padding: var(--space-xl);
}

.grid-area.grid-empty {
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-md);
  text-align: center;
  padding: var(--space-3xl);
}

.empty-icon {
  font-size: 4rem;
  opacity: 0.5;
}

.empty-text {
  font-size: var(--text-xl);
  font-weight: 600;
  color: var(--gray-700);
}

.empty-hint {
  color: var(--gray-500);
  font-size: var(--text-sm);
}

.grid-items {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-xl);
  grid-auto-flow: dense;
}

.grid-items.compact-mode {
  /* 紧凑模式下自动填充空隙 */
}

/* Grid 过渡动画 */
.grid-move {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.grid-enter-active,
.grid-leave-active {
  transition: all 0.3s ease;
}

.grid-enter-from {
  opacity: 0;
  transform: scale(0.8);
}

.grid-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

/* 组件选择面板 */
.component-palette-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: var(--transition);
}

.component-palette-overlay.is-open {
  opacity: 1;
  visibility: visible;
}

.component-palette {
  width: 90%;
  max-width: 900px;
  max-height: 80vh;
  background: white;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  display: flex;
  flex-direction: column;
  transform: translateY(20px);
  transition: var(--transition);
}

.component-palette-overlay.is-open .component-palette {
  transform: translateY(0);
}

.palette-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-xl);
  border-bottom: 1px solid var(--gray-200);
}

.palette-title {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: var(--text-xl);
  font-weight: 600;
  color: var(--gray-900);
}

.palette-icon {
  font-size: 1.5rem;
}

.palette-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  color: var(--gray-500);
  font-size: var(--text-lg);
  transition: var(--transition);
}

.palette-close:hover {
  background: var(--gray-100);
  color: var(--gray-700);
}

.palette-search {
  padding: var(--space-lg);
  border-bottom: 1px solid var(--gray-200);
}

.palette-categories {
  display: flex;
  gap: var(--space-sm);
  padding: var(--space-lg);
  border-bottom: 1px solid var(--gray-200);
  flex-wrap: wrap;
}

.category-btn {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  border: 1px solid var(--gray-200);
  background: white;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition);
  font-size: var(--text-sm);
}

.category-btn:hover {
  border-color: var(--primary);
  background: rgba(37, 99, 235, 0.05);
}

.category-btn.is-active {
  border-color: var(--primary);
  background: rgba(37, 99, 235, 0.1);
  color: var(--primary);
}

.category-count {
  background: var(--gray-100);
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  color: var(--gray-600);
}

.category-btn.is-active .category-count {
  background: rgba(37, 99, 235, 0.2);
  color: var(--primary-dark);
}

.palette-components {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--space-lg);
  padding: var(--space-xl);
  overflow-y: auto;
  flex: 1;
}

.component-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  padding: var(--space-md);
  border: 2px solid var(--gray-200);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: var(--transition);
  background: white;
}

.component-card:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.component-card.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.component-preview {
  background: var(--gray-50);
  border-radius: var(--radius-md);
  padding: var(--space-md);
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.component-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.component-name {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-weight: 600;
  color: var(--gray-900);
}

.component-icon {
  font-size: 1.2rem;
}

.component-desc {
  font-size: var(--text-sm);
  color: var(--gray-600);
  line-height: 1.4;
}

.component-meta {
  display: flex;
  gap: var(--space-sm);
  margin-top: var(--space-xs);
}

.component-size {
  font-size: var(--text-xs);
  color: var(--gray-500);
  background: var(--gray-100);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
}

/* 设置面板 */
.grid-settings {
  padding: var(--space-lg);
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
}

.settings-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.setting-label {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  cursor: pointer;
  color: var(--gray-700);
}

.setting-checkbox {
  width: 18px;
  height: 18px;
  accent-color: var(--primary);
}

.setting-info {
  display: flex;
  gap: var(--space-lg);
}

.setting-hint {
  font-size: var(--text-sm);
  color: var(--gray-500);
}

@media (max-width: 768px) {
  .grid-toolbar {
    flex-direction: column;
    gap: var(--space-md);
    align-items: stretch;
  }
  
  .toolbar-actions {
    justify-content: center;
  }
  
  .grid-items {
    grid-template-columns: 1fr;
  }
  
  .palette-categories {
    justify-content: center;
  }
  
  .palette-components {
    grid-template-columns: 1fr;
  }
  
  .settings-row {
    flex-direction: column;
    gap: var(--space-md);
    align-items: flex-start;
  }
}
</style>
