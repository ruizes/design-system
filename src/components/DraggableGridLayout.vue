<template>
  <div class="draggable-grid-layout" ref="layoutRef" :style="containerStyle">
    <!-- 网格背景 -->
    <div 
      class="grid-background" 
      v-if="showGrid" 
      :style="gridBackgroundStyle"
    ></div>
    
    <!-- 网格项 -->
    <div
      v-for="item in items"
      :key="item.id"
      class="grid-item"
      :class="{
        'is-dragging': draggingId === item.id,
        'is-resizing': resizingId === item.id
      }"
      :style="getItemStyle(item)"
      @mousedown="startDrag($event, item)"
    >
      <div class="grid-item-header" @mousedown.stop>
        <span class="grid-item-title">{{ item.title }}</span>
        <div class="grid-item-actions">
          <button class="btn btn-sm btn-outline" @click="removeItem(item.id)">×</button>
        </div>
      </div>
      <div class="grid-item-content">
        <slot :item="item">{{ item.content }}</slot>
      </div>
      <!-- 调整大小的手柄 -->
      <div
        class="resize-handle resize-handle-se"
        @mousedown="startResize($event, item)"
      ></div>
    </div>
    
    <!-- 添加组件按钮 -->
    <div class="add-item-btn" @click="addItem">
      <span>+ 添加组件</span>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  cols: {
    type: Number,
    default: 12
  },
  rows: {
    type: Number,
    default: 20
  },
  cellWidth: {
    type: Number,
    default: 60
  },
  cellHeight: {
    type: Number,
    default: 60
  },
  gap: {
    type: Number,
    default: 8
  },
  showGrid: {
    type: Boolean,
    default: true
  },
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'item-drag-start', 'item-drag-end', 'item-resize-start', 'item-resize-end'])

const layoutRef = ref(null)
const draggingId = ref(null)
const resizingId = ref(null)
const dragStartPos = ref({ x: 0, y: 0 })
const dragStartItem = ref(null)
const resizeStartPos = ref({ x: 0, y: 0 })
const resizeStartItem = ref(null)

// 如果没有传入数据，使用默认数据
const items = ref(props.modelValue && props.modelValue.length > 0 
  ? [...props.modelValue] 
  : getDefaultItems())

function getDefaultItems() {
  return [
    { id: 'item-1', x: 0, y: 0, w: 3, h: 2, title: '组件 1', content: '可拖拽内容区域' },
    { id: 'item-2', x: 3, y: 0, w: 2, h: 3, title: '组件 2', content: '碰撞时自动让路' },
    { id: 'item-3', x: 0, y: 2, w: 2, h: 2, title: '组件 3', content: '自动向上吸附' },
    { id: 'item-4', x: 5, y: 0, w: 3, h: 2, title: '组件 4', content: '网格对齐拖拽' },
    { id: 'item-5', x: 2, y: 2, w: 3, h: 2, title: '组件 5', content: '支持调整大小' },
  ]
}

const totalCols = computed(() => props.cols)
const totalRows = computed(() => props.rows)

const containerStyle = computed(() => ({
  width: totalCols.value * props.cellWidth + 'px',
  minHeight: totalRows.value * props.cellHeight + 'px',
  position: 'relative'
}))

// 使用 CSS 背景实现网格
const gridBackgroundStyle = computed(() => {
  const color = 'var(--gray-200)'
  return {
    width: totalCols.value * props.cellWidth + 'px',
    height: totalRows.value * props.cellHeight + 'px',
    backgroundImage: `
      linear-gradient(to right, ${color} 1px, transparent 1px),
      linear-gradient(to bottom, ${color} 1px, transparent 1px)
    `,
    backgroundSize: `${props.cellWidth}px ${props.cellHeight}px`,
    backgroundPosition: '0 0'
  }
})

const getItemStyle = (item) => {
  const isDragging = draggingId.value === item.id
  return {
    position: 'absolute',
    left: item.x * props.cellWidth + props.gap + 'px',
    top: item.y * props.cellHeight + props.gap + 'px',
    width: item.w * props.cellWidth - props.gap * 2 + 'px',
    height: item.h * props.cellHeight - props.gap * 2 + 'px',
    zIndex: isDragging ? 1000 : 1,
    transition: isDragging ? 'none' : 'all 0.2s ease',
    opacity: isDragging ? 0.9 : 1
  }
}

// 碰撞检测
const checkCollision = (item1, item2) => {
  return (
    item1.x < item2.x + item2.w &&
    item1.x + item1.w > item2.x &&
    item1.y < item2.y + item2.h &&
    item1.y + item1.h > item2.y
  )
}

// 获取所有与指定项碰撞的项
const getCollidingItems = (item, excludeId = null) => {
  return items.value.filter(i => {
    if (i.id === item.id || i.id === excludeId) return false
    return checkCollision(item, i)
  })
}

// 检查位置是否有效
const isValidPosition = (item, excludeId = null) => {
  // 检查边界
  if (item.x < 0 || item.y < 0) return false
  if (item.x + item.w > totalCols.value) return false
  if (item.y + item.h > totalRows.value) return false
  
  // 检查碰撞
  return getCollidingItems(item, excludeId).length === 0
}



// 自动向上吸附 - 紧凑排列算法（俄罗斯方块风格）
const compactItems = () => {
  let hasChanged = true
  let iterations = 0
  const maxIterations = 100
  
  // 持续压缩直到没有项目可以上移
  while (hasChanged && iterations < maxIterations) {
    hasChanged = false
    iterations++
    
    // 按Y坐标排序，从上到下处理
    const sortedItems = [...items.value].sort((a, b) => a.y - b.y)
    
    for (const item of sortedItems) {
      // 尝试向上移动项目直到碰到边界或其他项目
      while (canMoveUp(item)) {
        item.y--
        hasChanged = true
      }
      
      // 如果不能向上，尝试向左移动
      while (canMoveLeft(item)) {
        item.x--
        hasChanged = true
      }
    }
  }
}

// 检查项目是否可以向上移动
const canMoveUp = (item) => {
  if (item.y <= 0) return false
  
  const testItem = { ...item, y: item.y - 1 }
  
  // 检查与其他项目的碰撞
  for (const other of items.value) {
    if (other.id === item.id) continue
    if (checkCollision(testItem, other)) {
      return false
    }
  }
  
  return true
}

// 检查项目是否可以向左移动
const canMoveLeft = (item) => {
  if (item.x <= 0) return false
  
  const testItem = { ...item, x: item.x - 1 }
  
  // 检查与其他项目的碰撞
  for (const other of items.value) {
    if (other.id === item.id) continue
    if (checkCollision(testItem, other)) {
      return false
    }
  }
  
  return true
}

// 开始拖拽
const startDrag = (e, item) => {
  if (e.target.closest('.resize-handle') || e.target.closest('.grid-item-actions')) return
  
  e.preventDefault()
  draggingId.value = item.id
  dragStartPos.value = { x: e.clientX, y: e.clientY }
  dragStartItem.value = { ...item }
  
  emit('item-drag-start', item)
  
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}

const onDrag = (e) => {
  if (!draggingId.value || !dragStartItem.value) return
  
  const deltaX = e.clientX - dragStartPos.value.x
  const deltaY = e.clientY - dragStartPos.value.y
  
  const item = items.value.find(i => i.id === draggingId.value)
  if (!item) return
  
  // 计算新位置，对齐网格
  const newX = Math.round(deltaX / props.cellWidth) + dragStartItem.value.x
  const newY = Math.round(deltaY / props.cellHeight) + dragStartItem.value.y
  
  // 边界检查
  const boundedX = Math.max(0, Math.min(newX, totalCols.value - item.w))
  const boundedY = Math.max(0, Math.min(newY, totalRows.value - item.h))
  
  // 保存当前位置
  const prevX = item.x
  const prevY = item.y
  
  // 先移动拖拽项
  item.x = boundedX
  item.y = boundedY
  
  // 处理碰撞 - 使用更智能的碰撞解决
  resolveCollisionsWithPriority(item, prevX, prevY)
}

// 带优先级的碰撞解决 - 拖拽项优先
const resolveCollisionsWithPriority = (movingItem, prevX, prevY) => {
  let iterations = 0
  const maxIterations = 50
  
  // 保存除了拖拽项之外的所有项目的位置
  const otherItems = items.value.filter(i => i.id !== movingItem.id)
  const originalPositions = new Map()
  otherItems.forEach(item => {
    originalPositions.set(item.id, { x: item.x, y: item.y })
  })
  
  // 使用队列来处理碰撞传播
  const collisionQueue = [movingItem.id]
  const processed = new Set()
  
  while (collisionQueue.length > 0 && iterations < maxIterations) {
    iterations++
    const currentId = collisionQueue.shift()
    
    if (processed.has(currentId)) continue
    processed.add(currentId)
    
    const currentItem = items.value.find(i => i.id === currentId)
    if (!currentItem) continue
    
    // 获取所有碰撞的项目
    const collidingItems = getCollidingItems(currentItem)
    
    for (const other of collidingItems) {
      // 不要推挤正在拖拽的项目
      if (other.id === draggingId.value) continue
      
      // 计算推挤方向
      const direction = getOptimalPushDirection(currentItem, other, prevX, prevY)
      
      // 推挤被碰撞的项目
      const pushed = pushItemAway(other, direction, currentItem)
      
      if (pushed) {
        collisionQueue.push(other.id)
        processed.delete(other.id)
      }
    }
  }
  
  // 检查拖拽项是否还有碰撞，如果有则回退
  const dragItem = items.value.find(i => i.id === draggingId.value)
  if (dragItem && getCollidingItems(dragItem).length > 0) {
    // 尝试寻找替代位置
    findAlternativePosition(dragItem, prevX, prevY)
  }
}

// 计算最佳推挤方向
const getOptimalPushDirection = (pusher, item, pusherPrevX, pusherPrevY) => {
  // 计算移动方向
  const moveDirX = pusher.x - pusherPrevX
  const moveDirY = pusher.y - pusherPrevY
  
  // 如果有明确的移动方向，沿着该方向推挤
  if (Math.abs(moveDirX) > Math.abs(moveDirY)) {
    return moveDirX > 0 ? 'right' : 'left'
  } else if (Math.abs(moveDirY) > 0) {
    return moveDirY > 0 ? 'down' : 'up'
  }
  
  // 默认根据相对位置推挤
  const pusherCenterX = pusher.x + pusher.w / 2
  const pusherCenterY = pusher.y + pusher.h / 2
  const itemCenterX = item.x + item.w / 2
  const itemCenterY = item.y + item.h / 2
  
  const dx = itemCenterX - pusherCenterX
  const dy = itemCenterY - pusherCenterY
  
  if (Math.abs(dx) > Math.abs(dy)) {
    return dx > 0 ? 'right' : 'left'
  } else {
    return dy > 0 ? 'down' : 'up'
  }
}

// 为拖拽项寻找替代位置
const findAlternativePosition = (item, prevX, prevY) => {
  // 尝试回退到之前的位置
  item.x = prevX
  item.y = prevY
  
  // 如果之前的位置也有碰撞，尝试附近的位置
  if (getCollidingItems(item).length > 0) {
    const directions = [
      { dx: 1, dy: 0 }, { dx: -1, dy: 0 },
      { dx: 0, dy: 1 }, { dx: 0, dy: -1 },
      { dx: 1, dy: 1 }, { dx: -1, dy: 1 },
      { dx: 1, dy: -1 }, { dx: -1, dy: -1 }
    ]
    
    for (const dir of directions) {
      const testX = item.x + dir.dx
      const testY = item.y + dir.dy
      
      if (testX >= 0 && testY >= 0 && 
          testX + item.w <= totalCols.value && 
          testY + item.h <= totalRows.value) {
        const testItem = { ...item, x: testX, y: testY }
        if (getCollidingItems(testItem).length === 0) {
          item.x = testX
          item.y = testY
          return
        }
      }
    }
  }
}

// 调整大小时的碰撞处理
const onResize = (e) => {
  if (!resizingId.value || !resizeStartItem.value) return
  
  const deltaX = e.clientX - resizeStartPos.value.x
  const deltaY = e.clientY - resizeStartPos.value.y
  
  const item = items.value.find(i => i.id === resizingId.value)
  if (!item) return
  
  // 计算新尺寸，对齐网格
  const newW = Math.max(1, Math.round(deltaX / props.cellWidth) + resizeStartItem.value.w)
  const newH = Math.max(1, Math.round(deltaY / props.cellHeight) + resizeStartItem.value.h)
  
  // 边界检查
  const boundedW = Math.min(newW, totalCols.value - item.x)
  const boundedH = Math.min(newH, totalRows.value - item.y)
  
  // 保存当前尺寸
  const prevW = item.w
  const prevH = item.h
  
  // 先调整大小
  item.w = boundedW
  item.h = boundedH
  
  // 处理碰撞
  resolveCollisionsForResize(item, prevW, prevH)
}

// 调整大小时的碰撞解决
const resolveCollisionsForResize = (resizingItem, prevW, prevH) => {
  let iterations = 0
  const maxIterations = 50
  
  const collisionQueue = [resizingItem.id]
  const processed = new Set()
  
  while (collisionQueue.length > 0 && iterations < maxIterations) {
    iterations++
    const currentId = collisionQueue.shift()
    
    if (processed.has(currentId)) continue
    processed.add(currentId)
    
    const currentItem = items.value.find(i => i.id === currentId)
    if (!currentItem) continue
    
    const collidingItems = getCollidingItems(currentItem)
    
    for (const other of collidingItems) {
      if (other.id === resizingId.value) continue
      
      // 调整大小时总是向下/向右推挤
      const direction = 'down'
      const pushed = pushItemAway(other, direction, currentItem)
      
      if (pushed) {
        collisionQueue.push(other.id)
        processed.delete(other.id)
      }
    }
  }
}

// 将项目推离
const pushItemAway = (item, direction, pusher) => {
  const originalX = item.x
  const originalY = item.y
  
  switch (direction) {
    case 'right':
      item.x = pusher.x + pusher.w
      break
    case 'left':
      item.x = pusher.x - item.w
      break
    case 'down':
      item.y = pusher.y + pusher.h
      break
    case 'up':
      item.y = pusher.y - item.h
      break
  }
  
  // 边界检查和处理
  if (item.x + item.w > totalCols.value) {
    // 如果右边超出边界，尝试换行到下一行
    item.x = 0
    item.y = pusher.y + pusher.h
  }
  
  if (item.x < 0) {
    item.x = 0
  }
  
  if (item.y + item.h > totalRows.value) {
    // 如果底部超出边界，尝试向上找空间
    item.y = Math.max(0, totalRows.value - item.h)
  }
  
  if (item.y < 0) {
    item.y = 0
  }
  
  // 如果这个位置还有碰撞，尝试其他方向
  const newCollisions = getCollidingItems(item, pusher.id)
  if (newCollisions.length > 0) {
    // 尝试向下推挤作为备选
    if (direction !== 'down') {
      item.y = pusher.y + pusher.h
      item.x = originalX
    }
  }
  
  return item.x !== originalX || item.y !== originalY
}

const stopDrag = () => {
  if (draggingId.value) {
    const item = items.value.find(i => i.id === draggingId.value)
    if (item) {
      // 确保所有项目都在边界内
      for (const i of items.value) {
        i.x = Math.max(0, Math.min(i.x, totalCols.value - i.w))
        i.y = Math.max(0, Math.min(i.y, totalRows.value - i.h))
      }
      
      // 压缩整理
      compactItems()
      emit('item-drag-end', item)
      emitChange()
    }
  }
  
  draggingId.value = null
  dragStartItem.value = null
  
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}

// 开始调整大小
const startResize = (e, item) => {
  e.preventDefault()
  e.stopPropagation()
  
  resizingId.value = item.id
  resizeStartPos.value = { x: e.clientX, y: e.clientY }
  resizeStartItem.value = { ...item }
  
  emit('item-resize-start', item)
  
  document.addEventListener('mousemove', onResize)
  document.addEventListener('mouseup', stopResize)
}

const stopResize = () => {
  if (resizingId.value) {
    const item = items.value.find(i => i.id === resizingId.value)
    if (item) {
      compactItems()
      emit('item-resize-end', item)
      emitChange()
    }
  }
  
  resizingId.value = null
  resizeStartItem.value = null
  
  document.removeEventListener('mousemove', onResize)
  document.removeEventListener('mouseup', stopResize)
}

// 添加新项目
let itemIdCounter = 1
const addItem = () => {
  const newItem = {
    id: `item-${Date.now()}-${itemIdCounter++}`,
    x: 0,
    y: 0,
    w: 2,
    h: 2,
    title: `组件 ${items.value.length + 1}`,
    content: '可拖拽内容'
  }
  
  // 找到一个空位
  let placed = false
  for (let y = 0; y < totalRows.value && !placed; y++) {
    for (let x = 0; x <= totalCols.value - newItem.w && !placed; x++) {
      newItem.x = x
      newItem.y = y
      if (isValidPosition(newItem)) {
        placed = true
      }
    }
  }
  
  items.value.push(newItem)
  compactItems()
  emitChange()
}

// 移除项目
const removeItem = (id) => {
  items.value = items.value.filter(i => i.id !== id)
  compactItems()
  emitChange()
}

const emitChange = () => {
  emit('update:modelValue', items.value)
  emit('change', items.value)
}

// 监听 props 变化
watch(() => props.modelValue, (newVal) => {
  items.value = [...newVal]
}, { deep: true })

onUnmounted(() => {
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('mousemove', onResize)
  document.removeEventListener('mouseup', stopResize)
})

defineExpose({
  items,
  addItem,
  removeItem,
  compactItems
})
</script>

<style scoped>
.draggable-grid-layout {
  position: relative;
  background: var(--gray-50);
  border: 1px solid var(--gray-200);
  border-radius: var(--radius-lg);
  overflow: auto;
}

.grid-background {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 0;
}

.grid-item {
  background: white;
  border: 2px solid var(--gray-200);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow);
  cursor: move;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  z-index: 1;
}

.grid-item:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-md);
}

.grid-item.is-dragging,
.grid-item.is-resizing {
  border-color: var(--primary);
  box-shadow: var(--shadow-lg);
  cursor: grabbing;
}

.grid-item-header {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  padding: var(--space-sm) var(--space-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: move;
  user-select: none;
}

.grid-item-title {
  font-weight: 600;
  font-size: var(--text-sm);
}

.grid-item-actions .btn {
  padding: var(--space-xs) var(--space-sm);
  font-size: var(--text-xs);
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.grid-item-actions .btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.grid-item-content {
  flex: 1;
  padding: var(--space-md);
  overflow: auto;
  font-size: var(--text-sm);
  color: var(--gray-600);
}

.resize-handle {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 20px;
  height: 20px;
  cursor: se-resize;
  background: linear-gradient(135deg, transparent 50%, var(--primary) 50%);
  opacity: 0;
  transition: opacity 0.2s;
}

.grid-item:hover .resize-handle,
.grid-item.is-resizing .resize-handle {
  opacity: 1;
}

.add-item-btn {
  position: absolute;
  bottom: 20px;
  right: 20px;
  width: 120px;
  height: 40px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-weight: 500;
  font-size: var(--text-sm);
  box-shadow: var(--shadow-lg);
  transition: var(--transition);
  z-index: 100;
}

.add-item-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-xl);
}
</style>
