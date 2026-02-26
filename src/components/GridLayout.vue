<template>
  <div 
    class="grid-layout-container"
    :style="containerStyle"
    ref="containerRef"
  >
    <div 
      v-if="showGrid"
      class="grid-background"
      :style="gridBackgroundStyle"
    ></div>
    
    <div
      v-for="item in items"
      :key="item.id"
      class="grid-item"
      :class="{
        'grid-item-dragging': draggingId === item.id,
        'grid-item-resizing': resizingId === item.id,
        'grid-item-placeholder': item.placeholder
      }"
      :style="getItemStyle(item)"
      @mousedown.stop="startDrag($event, item)"
    >
      <div class="grid-item-content">
        <component 
          v-if="item.component" 
          :is="item.component" 
          v-bind="item.props || {}"
        />
        <slot v-else :name="item.id" :item="item">
          <div class="grid-item-default">
            <div class="grid-item-header">
              <span class="grid-item-title">{{ item.title || item.id }}</span>
            </div>
            <div class="grid-item-body">
              {{ item.content || '' }}
            </div>
          </div>
        </slot>
      </div>
      
      <div 
        v-if="!item.static && !item.placeholder"
        class="resize-handle resize-handle-se"
        @mousedown.stop="startResize($event, item)"
      ></div>
    </div>
    
    <div 
      v-if="dragOverItem"
      class="grid-item-placeholder"
      :style="getPlaceholderStyle()"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  colNum: {
    type: Number,
    default: 12
  },
  rowHeight: {
    type: Number,
    default: 50
  },
  colWidth: {
    type: Number,
    default: 80
  },
  gap: {
    type: Number,
    default: 10
  },
  showGrid: {
    type: Boolean,
    default: true
  },
  gridColor: {
    type: String,
    default: '#e5e7eb'
  },
  autoSize: {
    type: Boolean,
    default: true
  },
  compactUp: {
    type: Boolean,
    default: true
  },
  preventCollision: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'resize', 'move'])

const containerRef = ref(null)
const containerWidth = ref(props.colNum * props.colWidth + (props.colNum - 1) * props.gap)
const containerHeight = ref(0)
const draggingId = ref(null)
const resizingId = ref(null)
const dragStartPos = ref({ x: 0, y: 0 })
const dragStartItem = ref(null)
const dragOverItem = ref(null)
const items = ref([])

const initItems = () => {
  items.value = props.modelValue.map(item => ({
    ...item,
    x: item.x ?? 0,
    y: item.y ?? 0,
    w: item.w ?? 1,
    h: item.h ?? 1
  }))
  compactLayout()
}

watch(() => props.modelValue, (newVal) => {
  if (!draggingId.value && !resizingId.value) {
    initItems()
  }
}, { deep: true })

onMounted(() => {
  initItems()
  if (containerRef.value) {
    const rect = containerRef.value.parentElement.getBoundingClientRect()
    if (rect.width > 0) {
      const availableWidth = rect.width - 40
      const newColWidth = Math.floor((availableWidth - (props.colNum - 1) * props.gap) / props.colNum)
      if (newColWidth > 0) {
        containerWidth.value = availableWidth
      }
    }
  }
  updateContainerHeight()
})

const containerStyle = computed(() => ({
  width: `${containerWidth.value}px`,
  minHeight: `${containerHeight.value}px`,
  position: 'relative'
}))

const gridBackgroundStyle = computed(() => {
  const size = actualColWidth.value + props.gap
  return {
    backgroundImage: `
      linear-gradient(to right, ${props.gridColor} 1px, transparent 1px),
      linear-gradient(to bottom, ${props.gridColor} 1px, transparent 1px)
    `,
    backgroundSize: `${size}px ${props.rowHeight + props.gap}px`,
    backgroundPosition: `${-props.gap / 2}px ${-props.gap / 2}px`
  }
})

const actualColWidth = computed(() => {
  return (containerWidth.value - (props.colNum - 1) * props.gap) / props.colNum
})

const snapToGrid = (value, gridSize) => {
  return Math.round(value / gridSize) * gridSize
}

const getPixelPosition = (gridX, gridY, gridW, gridH) => {
  const x = gridX * (actualColWidth.value + props.gap)
  const y = gridY * (props.rowHeight + props.gap)
  const w = gridW * actualColWidth.value + (gridW - 1) * props.gap
  const h = gridH * props.rowHeight + (gridH - 1) * props.gap
  return { x, y, w, h }
}

const getItemStyle = (item) => {
  const pos = getPixelPosition(item.x, item.y, item.w, item.h)
  return {
    position: 'absolute',
    left: `${pos.x}px`,
    top: `${pos.y}px`,
    width: `${pos.w}px`,
    height: `${pos.h}px`,
    transition: draggingId.value || resizingId.value ? 'none' : 'all 0.2s ease',
    zIndex: draggingId.value === item.id ? 1000 : 1,
    cursor: item.static ? 'default' : 'move'
  }
}

const getPlaceholderStyle = () => {
  if (!dragOverItem.value) return {}
  return getItemStyle({ ...dragOverItem.value, id: 'placeholder' })
}

const checkCollision = (item, exceptId = null) => {
  for (const other of items.value) {
    if (other.id === item.id || other.id === exceptId || other.placeholder) continue
    if (
      item.x < other.x + other.w &&
      item.x + item.w > other.x &&
      item.y < other.y + other.h &&
      item.y + item.h > other.y
    ) {
      return other
    }
  }
  return null
}

const moveItemDown = (collidingItem, amount, draggedItem) => {
  const newY = collidingItem.y + amount
  
  const movedItem = { ...collidingItem, y: newY }
  const nextCollision = checkCollision(movedItem, draggedItem.id)
  
  if (nextCollision) {
    moveItemDown(nextCollision, amount, draggedItem)
  }
  
  const itemIndex = items.value.findIndex(i => i.id === collidingItem.id)
  if (itemIndex !== -1) {
    items.value[itemIndex].y = newY
  }
}

const pushItemsAway = (movingItem) => {
  let iterations = 0
  const maxIterations = 100
  let collision = checkCollision(movingItem)
  while (collision && iterations < maxIterations) {
    iterations++
    const overlapY = Math.min(
      movingItem.y + movingItem.h - collision.y,
      collision.y + collision.h - movingItem.y
    )
    const overlapX = Math.min(
      movingItem.x + movingItem.w - collision.x,
      collision.x + collision.w - movingItem.x
    )
    
    if (overlapY <= overlapX) {
      const pushAmount = Math.ceil(overlapY / 1)
      if (collision.y < movingItem.y) {
        moveItemDown(movingItem, pushAmount, collision)
      } else {
        moveItemDown(collision, pushAmount, movingItem)
      }
    } else {
      if (collision.x < movingItem.x) {
        movingItem.x = collision.x + collision.w
      } else {
        collision.x = movingItem.x + movingItem.w
      }
    }
    
    fixItemBounds(movingItem)
    fixItemBounds(collision)
    collision = checkCollision(movingItem)
  }
  if (iterations >= maxIterations) {
    console.warn('pushItemsAway: max iterations reached')
  }
}

const fixItemBounds = (item) => {
  if (item.x < 0) item.x = 0
  if (item.x + item.w > props.colNum) {
    item.x = props.colNum - item.w
  }
  if (item.y < 0) item.y = 0
}

const compactLayout = () => {
  if (!props.compactUp) return
  
  let moved = true
  while (moved) {
    moved = false
    for (const item of items.value) {
      if (item.static || item.placeholder) continue
      
      let canMoveUp = true
      while (canMoveUp && item.y > 0) {
        const testItem = { ...item, y: item.y - 1 }
        const collision = checkCollision(testItem, item.id)
        if (!collision) {
          item.y--
          moved = true
        } else {
          canMoveUp = false
        }
      }
      
      let canMoveLeft = true
      while (canMoveLeft && item.x > 0) {
        const testItem = { ...item, x: item.x - 1 }
        const collision = checkCollision(testItem, item.id)
        if (!collision) {
          item.x--
          moved = true
        } else {
          canMoveLeft = false
        }
      }
    }
  }
  
  updateContainerHeight()
}

const updateContainerHeight = () => {
  let maxY = 0
  for (const item of items.value) {
    const bottom = item.y + item.h
    if (bottom > maxY) maxY = bottom
  }
  containerHeight.value = maxY * (props.rowHeight + props.gap) + 20
}

const startDrag = (event, item) => {
  if (item.static) return
  
  event.preventDefault()
  event.stopPropagation()
  draggingId.value = item.id
  dragStartPos.value = { x: event.clientX, y: event.clientY }
  dragStartItem.value = { x: item.x, y: item.y, w: item.w, h: item.h }
  
  document.addEventListener('mousemove', handleMouseMoveEvent)
  document.addEventListener('mouseup', handleMouseUpEvent)
}

const startResize = (event, item) => {
  if (item.static) return
  
  event.preventDefault()
  event.stopPropagation()
  resizingId.value = item.id
  dragStartPos.value = { x: event.clientX, y: event.clientY }
  dragStartItem.value = { x: item.x, y: item.y, w: item.w, h: item.h }
  
  document.addEventListener('mousemove', handleMouseMoveEvent)
  document.addEventListener('mouseup', handleMouseUpEvent)
}

const handleMouseMoveEvent = (event) => {
  if (draggingId.value) {
    const dx = event.clientX - dragStartPos.value.x
    const dy = event.clientY - dragStartPos.value.y
    
    const gridDx = snapToGrid(dx, actualColWidth.value + props.gap) / (actualColWidth.value + props.gap)
    const gridDy = snapToGrid(dy, props.rowHeight + props.gap) / (props.rowHeight + props.gap)
    
    const itemIndex = items.value.findIndex(i => i.id === draggingId.value)
    if (itemIndex !== -1) {
      const item = items.value[itemIndex]
      item.x = Math.max(0, Math.min(props.colNum - item.w, dragStartItem.value.x + gridDx))
      item.y = Math.max(0, dragStartItem.value.y + gridDy)
      
      fixItemBounds(item)
      
      if (props.preventCollision) {
        pushItemsAway(item)
      }
    }
  } else if (resizingId.value) {
    const dx = event.clientX - dragStartPos.value.x
    const dy = event.clientY - dragStartPos.value.y
    
    const gridDw = Math.max(1, Math.round(dx / (actualColWidth.value + props.gap)) + dragStartItem.value.w)
    const gridDh = Math.max(1, Math.round(dy / (props.rowHeight + props.gap)) + dragStartItem.value.h)
    
    const itemIndex = items.value.findIndex(i => i.id === resizingId.value)
    if (itemIndex !== -1) {
      const item = items.value[itemIndex]
      item.w = Math.min(props.colNum - item.x, gridDw)
      item.h = gridDh
      
      if (props.preventCollision) {
        pushItemsAway(item)
      }
    }
  }
}

const handleMouseUpEvent = () => {
  if (draggingId.value || resizingId.value) {
    compactLayout()
    updateContainerHeight()
    
    emit('update:modelValue', items.value)
    emit('change', items.value)
    
    if (draggingId.value) {
      emit('move', items.value.find(i => i.id === draggingId.value))
    }
    if (resizingId.value) {
      emit('resize', items.value.find(i => i.id === resizingId.value))
    }
  }
  
  draggingId.value = null
  resizingId.value = null
  dragStartItem.value = null
  dragOverItem.value = null
  
  document.removeEventListener('mousemove', handleMouseMoveEvent)
  document.removeEventListener('mouseup', handleMouseUpEvent)
}

defineExpose({
  compactLayout,
  updateContainerHeight
})
</script>

<style scoped>
.grid-layout-container {
  position: relative;
  background: #fafafa;
  border-radius: 8px;
  padding: 10px;
  user-select: none;
}

.grid-background {
  position: absolute;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  pointer-events: none;
  z-index: 0;
}

.grid-item {
  box-sizing: border-box;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  z-index: 1;
}

.grid-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.grid-item-dragging {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
  z-index: 1000 !important;
  opacity: 0.95;
}

.grid-item-resizing {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
  z-index: 1000 !important;
}

.grid-item-content {
  width: 100%;
  height: 100%;
  overflow: auto;
}

.grid-item-default {
  padding: 12px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.grid-item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 8px;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 8px;
}

.grid-item-title {
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

.grid-item-body {
  flex: 1;
  color: #6b7280;
  font-size: 13px;
}

.grid-item-placeholder {
  background: rgba(59, 130, 246, 0.1);
  border: 2px dashed #3b82f6;
  pointer-events: none;
}

.resize-handle {
  position: absolute;
  width: 16px;
  height: 16px;
  background: #3b82f6;
  border-radius: 4px 0 4px 0;
  cursor: nwse-resize;
  display: flex;
  align-items: center;
  justify-content: center;
}

.resize-handle::after {
  content: '';
  width: 8px;
  height: 8px;
  border-right: 2px solid white;
  border-bottom: 2px solid white;
  margin-bottom: 2px;
  margin-left: 2px;
}

.resize-handle-se {
  bottom: 0;
  right: 0;
}
</style>