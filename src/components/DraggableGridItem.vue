<template>
  <div 
    class="grid-item-wrapper"
    :class="{ 
      'is-dragging': isDragging,
      'is-drop-target': isDropTarget,
      'is-wide': item.width > 1,
      'is-tall': item.height > 1
    }"
    :style="gridItemStyle"
    draggable="true"
    @dragstart="handleDragStart"
    @dragend="handleDragEnd"
    @dragover="handleDragOver"
    @dragenter="handleDragEnter"
    @dragleave="handleDragLeave"
  >
    <div class="grid-item">
      <div class="item-header">
        <div class="item-title">
          <span class="item-icon">{{ item.icon }}</span>
          <span class="item-name">{{ item.name }}</span>
        </div>
        <div class="item-actions">
          <button 
            class="action-btn" 
            title="复制"
            @click.stop="handleDuplicate"
          >
            📋
          </button>
          <button 
            class="action-btn action-btn-danger" 
            title="删除"
            @click.stop="handleDelete"
          >
            ✕
          </button>
        </div>
      </div>
      
      <div class="item-content">
        <component :is="getRenderComponent" :config="item.config" />
      </div>
      
      <div class="item-footer">
        <div class="item-handle" @mousedown="handleMouseDown">
          <span class="handle-icon">⠿</span>
          <span class="handle-text">拖拽排序</span>
        </div>
        <div class="item-size">
          {{ item.width }}×{{ item.height }}
        </div>
      </div>
    </div>
    
    <div 
      class="drop-indicator"
      v-if="isDropTarget && !isDragging"
    >
      <span class="drop-icon">↓</span>
      <span class="drop-text">放置到这里</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import GridPreviewCard from './previews/GridPreviewCard.vue'
import GridPreviewButton from './previews/GridPreviewButton.vue'
import GridPreviewForm from './previews/GridPreviewForm.vue'
import GridPreviewStats from './previews/GridPreviewStats.vue'
import GridPreviewImage from './previews/GridPreviewImage.vue'
import GridPreviewText from './previews/GridPreviewText.vue'
import GridPreviewBadge from './previews/GridPreviewBadge.vue'
import GridPreviewList from './previews/GridPreviewList.vue'

const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  index: {
    type: Number,
    required: true
  },
  isDragging: {
    type: Boolean,
    default: false
  },
  isDropTarget: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'drag-start',
  'drag-end',
  'drag-over',
  'delete',
  'duplicate'
])

const gridItemStyle = computed(() => {
  const style = {}
  if (props.item.width > 1) {
    style.gridColumn = `span ${props.item.width}`
  }
  if (props.item.height > 1) {
    style.gridRow = `span ${props.item.height}`
  }
  return style
})

const getRenderComponent = computed(() => {
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
  return map[props.item.type] || GridPreviewCard
})

const handleDragStart = (event) => {
  event.dataTransfer.effectAllowed = 'move'
  event.dataTransfer.setData('text/plain', JSON.stringify({
    id: props.item.id,
    index: props.index
  }))
  
  emit('drag-start', props.item, props.index)
  
  // 设置拖拽图像
  setTimeout(() => {
    const target = event.target
    if (target) {
      target.style.opacity = '0.5'
    }
  }, 0)
}

const handleDragEnd = (event) => {
  const target = event.target
  if (target) {
    target.style.opacity = '1'
  }
  emit('drag-end')
}

const handleDragOver = (event) => {
  event.preventDefault()
  event.dataTransfer.dropEffect = 'move'
}

const handleDragEnter = (event) => {
  event.preventDefault()
  emit('drag-over', props.index)
}

const handleDragLeave = (event) => {
  // 可以在这里处理离开效果
}

const handleDelete = () => {
  emit('delete', props.item.id)
}

const handleDuplicate = () => {
  emit('duplicate', props.item.id)
}

const handleMouseDown = (event) => {
  // 可以在这里处理自定义拖拽逻辑
}
</script>

<style scoped>
.grid-item-wrapper {
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.grid-item-wrapper.is-wide {
  grid-column: span 2;
}

.grid-item-wrapper.is-tall {
  grid-row: span 2;
}

.grid-item-wrapper.is-dragging {
  opacity: 0.5;
  transform: scale(1.02);
  z-index: 10;
}

.grid-item-wrapper.is-drop-target {
  transform: scale(1.02);
}

.grid-item {
  background: white;
  border: 2px solid var(--gray-200);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: var(--transition);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.grid-item:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-md);
}

.grid-item-wrapper.is-drop-target .grid-item {
  border-color: var(--primary);
  border-style: dashed;
  background: rgba(37, 99, 235, 0.02);
}

.item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-sm) var(--space-md);
  background: var(--gray-50);
  border-bottom: 1px solid var(--gray-200);
}

.item-title {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--gray-700);
}

.item-icon {
  font-size: 1rem;
}

.item-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 120px;
}

.item-actions {
  display: flex;
  gap: var(--space-xs);
  opacity: 0;
  transition: var(--transition-fast);
}

.grid-item:hover .item-actions {
  opacity: 1;
}

.action-btn {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.75rem;
  transition: var(--transition-fast);
  color: var(--gray-500);
}

.action-btn:hover {
  background: var(--gray-200);
  color: var(--gray-700);
}

.action-btn-danger:hover {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
}

.item-content {
  flex: 1;
  padding: var(--space-md);
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-xs) var(--space-md);
  background: var(--gray-50);
  border-top: 1px solid var(--gray-200);
}

.item-handle {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  cursor: grab;
  color: var(--gray-500);
  font-size: var(--text-xs);
  transition: var(--transition-fast);
  user-select: none;
}

.item-handle:hover {
  color: var(--primary);
}

.item-handle:active {
  cursor: grabbing;
}

.handle-icon {
  font-size: 1rem;
  line-height: 1;
}

.handle-text {
  opacity: 0.7;
}

.item-size {
  font-size: var(--text-xs);
  color: var(--gray-400);
  background: var(--gray-200);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
}

/* 放置指示器 */
.drop-indicator {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 2px dashed var(--primary);
  border-radius: var(--radius-lg);
  background: rgba(37, 99, 235, 0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  pointer-events: none;
  z-index: 5;
}

.drop-icon {
  font-size: 2rem;
  color: var(--primary);
  animation: bounce 1s ease-in-out infinite;
}

.drop-text {
  font-size: var(--text-sm);
  color: var(--primary);
  font-weight: 500;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .grid-item-wrapper.is-wide,
  .grid-item-wrapper.is-tall {
    grid-column: span 1;
    grid-row: span 1;
  }
  
  .item-actions {
    opacity: 1;
  }
  
  .item-name {
    max-width: 80px;
  }
}
</style>
