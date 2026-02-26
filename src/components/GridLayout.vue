<template>
  <div
    ref="gridRef"
    class="grid-layout"
    :style="gridStyle"
    @mousedown="onMouseDown"
    @mousemove="onMouseMove"
    @mouseup="onMouseUp"
    @mouseleave="onMouseUp"
  >
    <div
      v-for="item in layoutItems"
      :key="item.id"
      class="grid-item"
      :class="{ 'dragging': draggingItem?.id === item.id }"
      :style="getItemStyle(item)"
      @mousedown.stop="startDrag($event, item)"
    >
      <div class="grid-item-content">
        <slot :name="item.id" :item="item">
          <div class="default-content">
            {{ item.title || item.id }}
          </div>
        </slot>
      </div>
    </div>
    
    <div
      v-if="draggingItem"
      class="drag-placeholder"
      :style="placeholderStyle"
    ></div>
    
    <svg class="grid-lines" v-if="showGridLines">
      <defs>
        <pattern id="grid-pattern" :width="cellWidth" :height="cellHeight" patternUnits="userSpaceOnUse">
          <path :d="`M ${cellWidth} 0 L 0 0 0 ${cellHeight}`" fill="none" stroke="rgba(0,0,0,0.05)" stroke-width="1"/>
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#grid-pattern)" />
    </svg>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  cols: {
    type: Number,
    default: 12
  },
  rowHeight: {
    type: Number,
    default: 60
  },
  cellWidth: {
    type: Number,
    default: 80
  },
  cellHeight: {
    type: Number,
    default: 60
  },
  gap: {
    type: Number,
    default: 8
  },
  showGridLines: {
    type: Boolean,
    default: true
  },
  maxRows: {
    type: Number,
    default: 100
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'drag-start', 'drag-end'])

const gridRef = ref(null)
const layoutItems = ref([...props.modelValue])
const draggingItem = ref(null)
const dragOffset = ref({ x: 0, y: 0 })
const placeholderPosition = ref({ x: 0, y: 0, w: 0, h: 0 })
const isDragging = ref(false)

const cellHeight = computed(() => props.cellHeight)
const cellWidth = computed(() => props.cellWidth)

const gridStyle = computed(() => ({
  position: 'relative',
  minHeight: `${props.maxRows * (cellHeight.value + props.gap)}px`,
  width: '100%',
  background: '#fafafa',
  borderRadius: '8px',
  overflow: 'hidden'
}))

const getItemStyle = computed(() => (item) => {
  if (draggingItem.value?.id === item.id) {
    return {
      position: 'absolute',
      left: `${item._dragX || item.x * (cellWidth.value + props.gap)}px`,
      top: `${item._dragY || item.y * (cellHeight.value + props.gap)}px`,
      width: `${item.w * cellWidth.value + (item.w - 1) * props.gap}px`,
      height: `${item.h * cellHeight.value + (item.h - 1) * props.gap}px`,
      zIndex: 1000,
      opacity: 0.9,
      cursor: 'grabbing',
      transition: 'none'
    }
  }
  return {
    position: 'absolute',
    left: `${item.x * (cellWidth.value + props.gap)}px`,
    top: `${item.y * (cellHeight.value + props.gap)}px`,
    width: `${item.w * cellWidth.value + (item.w - 1) * props.gap}px`,
    height: `${item.h * cellHeight.value + (item.h - 1) * props.gap}px`,
    zIndex: 1,
    transition: isDragging.value ? 'none' : 'all 0.2s ease-out',
    cursor: 'grab'
  }
})

const placeholderStyle = computed(() => ({
  position: 'absolute',
  left: `${placeholderPosition.value.x * (cellWidth.value + props.gap)}px`,
  top: `${placeholderPosition.value.y * (cellHeight.value + props.gap)}px`,
  width: `${placeholderPosition.value.w * cellWidth.value + (placeholderPosition.value.w - 1) * props.gap}px`,
  height: `${placeholderPosition.value.h * cellHeight.value + (placeholderPosition.value.h - 1) * props.gap}px`,
  background: 'rgba(37, 99, 235, 0.1)',
  border: '2px dashed var(--primary)',
  borderRadius: '8px',
  zIndex: 0,
  transition: 'all 0.15s ease-out'
}))

watch(() => props.modelValue, (newVal) => {
  layoutItems.value = [...newVal]
}, { deep: true })

function startDrag(event, item) {
  event.preventDefault()
  
  const rect = gridRef.value.getBoundingClientRect()
  const itemRect = event.target.closest('.grid-item').getBoundingClientRect()
  
  dragOffset.value = {
    x: event.clientX - itemRect.left,
    y: event.clientY - itemRect.top
  }
  
  draggingItem.value = { ...item }
  isDragging.value = true
  
  placeholderPosition.value = {
    x: item.x,
    y: item.y,
    w: item.w,
    h: item.h
  }
  
  const itemData = layoutItems.value.find(i => i.id === item.id)
  if (itemData) {
    itemData._dragX = item.x * (cellWidth.value + props.gap)
    itemData._dragY = item.y * (cellHeight.value + props.gap)
  }
  
  emit('drag-start', { item, event })
}

function onMouseDown(event) {
}

function onMouseMove(event) {
  if (!draggingItem.value || !gridRef.value) return
  
  const rect = gridRef.value.getBoundingClientRect()
  const x = event.clientX - rect.left - dragOffset.value.x
  const y = event.clientY - rect.top - dragOffset.value.y
  
  const itemData = layoutItems.value.find(i => i.id === draggingItem.value.id)
  if (itemData) {
    itemData._dragX = x
    itemData._dragY = y
  }
  
  const gridX = Math.round(x / (cellWidth.value + props.gap))
  const gridY = Math.round(y / (cellHeight.value + props.gap))
  
  const newX = Math.max(0, Math.min(gridX, props.cols - draggingItem.value.w))
  const newY = Math.max(0, gridY)
  
  if (placeholderPosition.value.x !== newX || placeholderPosition.value.y !== newY) {
    placeholderPosition.value = {
      x: newX,
      y: newY,
      w: draggingItem.value.w,
      h: draggingItem.value.h
    }
    
    handleCollision(newX, newY, draggingItem.value)
  }
}

function handleCollision(newX, newY, draggedItem) {
  const items = layoutItems.value.filter(i => i.id !== draggedItem.id)
  
  for (const item of items) {
    if (isOverlapping(newX, newY, draggedItem.w, draggedItem.h, item.x, item.y, item.w, item.h)) {
      pushItemDown(item, newX, newY, draggedItem)
    }
  }
}

function isOverlapping(x1, y1, w1, h1, x2, y2, w2, h2) {
  return !(x1 + w1 <= x2 || x2 + w2 <= x1 || y1 + h1 <= y2 || y2 + h2 <= y1)
}

function pushItemDown(item, dragX, dragY, draggedItem) {
  const targetY = dragY + draggedItem.h
  
  if (targetY !== item.y) {
    item.y = targetY
    
    const items = layoutItems.value.filter(i => i.id !== draggedItem.id && i.id !== item.id)
    for (const other of items) {
      if (isOverlapping(item.x, item.y, item.w, item.h, other.x, other.y, other.w, other.h)) {
        pushItemDown(other, item.x, item.y, item)
      }
    }
  }
}

function checkAndFillGaps() {
  compactLayout()
}

function onMouseUp(event) {
  if (!draggingItem.value) return
  
  const itemData = layoutItems.value.find(i => i.id === draggingItem.value.id)
  if (itemData) {
    delete itemData._dragX
    delete itemData._dragY
    
    itemData.x = placeholderPosition.value.x
    itemData.y = placeholderPosition.value.y
  }
  
  compactLayout()
  
  isDragging.value = false
  emit('drag-end', { item: itemData, event })
  emit('update:modelValue', [...layoutItems.value])
  emit('change', [...layoutItems.value])
  
  draggingItem.value = null
}

function compactLayout() {
  const sortedItems = [...layoutItems.value].sort((a, b) => a.y - b.y)
  
  for (const item of sortedItems) {
    let newY = findLowestValidY(item, sortedItems)
    item.y = newY
  }
}

function findLowestValidY(item, allItems) {
  for (let y = 0; y <= item.y; y++) {
    let hasCollision = false
    
    for (const other of allItems) {
      if (other.id === item.id) continue
      
      if (isOverlapping(item.x, y, item.w, item.h, other.x, other.y, other.w, other.h)) {
        hasCollision = true
        break
      }
    }
    
    if (!hasCollision) {
      return y
    }
  }
  
  return item.y
}

function addItem(item) {
  layoutItems.value.push({
    ...item,
    x: item.x ?? 0,
    y: item.y ?? 0,
    w: item.w ?? 1,
    h: item.h ?? 1
  })
  emit('update:modelValue', [...layoutItems.value])
}

function removeItem(id) {
  const index = layoutItems.value.findIndex(i => i.id === id)
  if (index > -1) {
    layoutItems.value.splice(index, 1)
    compactLayout()
    emit('update:modelValue', [...layoutItems.value])
  }
}

function getItemById(id) {
  return layoutItems.value.find(i => i.id === id)
}

defineExpose({
  addItem,
  removeItem,
  getItemById,
  compactLayout
})
</script>

<style scoped>
.grid-layout {
  user-select: none;
  touch-action: none;
}

.grid-item {
  box-sizing: border-box;
}

.grid-item-content {
  width: 100%;
  height: 100%;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: box-shadow 0.2s ease;
}

.grid-item:hover .grid-item-content {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.grid-item.dragging .grid-item-content {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  transform: scale(1.02);
}

.default-content {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  color: var(--gray-700);
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
}

.grid-lines {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.drag-placeholder {
  pointer-events: none;
}
</style>
