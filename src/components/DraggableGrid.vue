<template>
  <div
    class="draggable-grid"
    :style="gridStyle"
    @mousemove="handleMouseMove"
    @mouseup="handleMouseUp"
    @mouseleave="handleMouseUp"
  >
    <!-- 网格背景 -->
    <div class="grid-background" :style="gridBackgroundStyle"></div>

    <!-- 网格项 -->
    <div
      v-for="item in layoutItems"
      :key="item.id"
      class="grid-item"
      :class="{
        'is-dragging': draggingId === item.id,
        'is-animating': isAnimating && draggingId !== item.id
      }"
      :style="getItemStyle(item)"
      @mousedown="handleMouseDown($event, item)"
    >
      <slot :item="item" :is-dragging="draggingId === item.id">
        <div class="grid-item-default">
          <span class="grid-item-label">{{ item.label || item.id }}</span>
        </div>
      </slot>
    </div>

    <!-- 拖拽时的占位符 -->
    <div
      v-if="draggingId && placeholderPosition"
      class="grid-placeholder"
      :style="placeholderStyle"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'

const props = defineProps({
  // 初始布局数据
  modelValue: {
    type: Array,
    default: () => []
  },
  // 网格列数
  cols: {
    type: Number,
    default: 4
  },
  // 网格行高 (px)
  rowHeight: {
    type: Number,
    default: 80
  },
  // 网格间距 (px)
  gap: {
    type: Number,
    default: 16
  },
  // 网格单元格宽度
  cellWidth: {
    type: Number,
    default: 100
  },
  // 是否启用自动吸附
  autoCompact: {
    type: Boolean,
    default: true
  },
  // 是否显示网格线
  showGridLines: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// 内部布局状态
const layoutItems = ref([])

// 拖拽状态
const draggingId = ref(null)
const dragStartPos = ref({ x: 0, y: 0 })
const dragOffset = ref({ x: 0, y: 0 })
const dragCurrentPos = ref({ x: 0, y: 0 })
const placeholderPosition = ref(null)
const isAnimating = ref(false)

// 碰撞检测
const isColliding = (rect1, rect2) => {
  return (
    rect1.x < rect2.x + rect2.w &&
    rect1.x + rect1.w > rect2.x &&
    rect1.y < rect2.y + rect2.h &&
    rect1.y + rect1.h > rect2.y
  )
}

// 自动向上吸附（紧凑布局）- 提前定义以避免暂时性死区
const compactLayout = () => {
  if (!props.autoCompact) return

  // 按Y坐标排序，然后按X坐标排序
  const sortedItems = [...layoutItems.value].sort((a, b) => {
    if (a.y !== b.y) return a.y - b.y
    return a.x - b.x
  })

  // 为每个项找到最高的可用位置
  sortedItems.forEach((item, index) => {
    const otherItems = sortedItems.slice(0, index)

    // 尝试向上移动
    let newY = item.y
    while (newY > 0) {
      const testY = newY - 1
      const testRect = { x: item.x, y: testY, w: item.w, h: item.h }

      // 检查是否与任何其他项碰撞
      const hasCollision = otherItems.some(other => isColliding(testRect, other))

      if (hasCollision) break
      newY = testY
    }

    if (newY !== item.y) {
      item.y = newY
    }
  })

  // 更新原始数组
  layoutItems.value = sortedItems
}

// 初始化布局
const initLayout = () => {
  if (!props.modelValue || !Array.isArray(props.modelValue)) {
    layoutItems.value = []
    return
  }
  layoutItems.value = props.modelValue.filter(item => item != null).map((item, index) => ({
    ...item,
    x: item.x ?? (index % props.cols),
    y: item.y ?? Math.floor(index / props.cols),
    w: item.w ?? 1,
    h: item.h ?? 1,
    id: item.id ?? `item-${index}`,
    label: item.label || item.id || `Item ${index}`
  }))
  if (props.autoCompact) {
    compactLayout()
  }
}

// 监听外部数据变化
watch(() => props.modelValue, (newVal) => {
  initLayout()
}, { immediate: true, deep: true })

// 网格容器样式
const gridStyle = computed(() => ({
  position: 'relative',
  width: '100%',
  minHeight: `${calculateGridHeight()}px`,
  userSelect: 'none'
}))

// 网格背景样式
const gridBackgroundStyle = computed(() => {
  if (!props.showGridLines) return { display: 'none' }

  const totalCellWidth = props.cellWidth + props.gap
  const totalRowHeight = props.rowHeight + props.gap

  return {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundImage: `
      linear-gradient(to right, var(--gray-200) 1px, transparent 1px),
      linear-gradient(to bottom, var(--gray-200) 1px, transparent 1px)
    `,
    backgroundSize: `${totalCellWidth}px ${totalRowHeight}px`,
    pointerEvents: 'none',
    zIndex: 0
  }
})

// 计算网格高度
const calculateGridHeight = () => {
  if (layoutItems.value.length === 0) return props.rowHeight * 4
  const maxY = Math.max(...layoutItems.value.map(item => item.y + item.h))
  return maxY * (props.rowHeight + props.gap) + props.gap
}

// 获取网格项样式
const getItemStyle = (item) => {
  const isDragging = draggingId.value === item.id
  const x = item.x * (props.cellWidth + props.gap) + props.gap
  const y = item.y * (props.rowHeight + props.gap) + props.gap

  const style = {
    position: 'absolute',
    left: `${x}px`,
    top: `${y}px`,
    width: `${item.w * props.cellWidth + (item.w - 1) * props.gap}px`,
    height: `${item.h * props.rowHeight + (item.h - 1) * props.gap}px`,
    zIndex: isDragging ? 1000 : 1,
    transition: isDragging ? 'none' : (isAnimating.value ? 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)' : 'none'),
    cursor: isDragging ? 'grabbing' : 'grab'
  }

  if (isDragging) {
    style.transform = `translate(${dragOffset.value.x}px, ${dragOffset.value.y}px) scale(1.02)`
    style.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.2)'
  }

  return style
}

// 占位符样式
const placeholderStyle = computed(() => {
  if (!placeholderPosition.value) return {}

  const { x, y, w, h } = placeholderPosition.value
  return {
    position: 'absolute',
    left: `${x * (props.cellWidth + props.gap) + props.gap}px`,
    top: `${y * (props.rowHeight + props.gap) + props.gap}px`,
    width: `${w * props.cellWidth + (w - 1) * props.gap}px`,
    height: `${h * props.rowHeight + (h - 1) * props.gap}px`,
    background: 'rgba(37, 99, 235, 0.1)',
    border: '2px dashed var(--primary)',
    borderRadius: 'var(--radius-md)',
    zIndex: 0,
    transition: 'all 0.15s ease'
  }
})

// 鼠标按下
const handleMouseDown = (event, item) => {
  event.preventDefault()
  draggingId.value = item.id
  dragStartPos.value = { x: event.clientX, y: event.clientY }
  dragOffset.value = { x: 0, y: 0 }
  dragCurrentPos.value = { x: item.x, y: item.y }
  placeholderPosition.value = { x: item.x, y: item.y, w: item.w, h: item.h }
  isAnimating.value = false
}

// 鼠标移动
const handleMouseMove = (event) => {
  if (!draggingId.value) return

  const deltaX = event.clientX - dragStartPos.value.x
  const deltaY = event.clientY - dragStartPos.value.y
  dragOffset.value = { x: deltaX, y: deltaY }

  // 计算当前拖拽位置对应的网格坐标
  const draggedItem = layoutItems.value.find(item => item.id === draggingId.value)
  if (!draggedItem) return

  const totalCellWidth = props.cellWidth + props.gap
  const totalRowHeight = props.rowHeight + props.gap

  // 计算新的网格位置（考虑偏移量）
  const newX = Math.round((draggedItem.x * totalCellWidth + deltaX) / totalCellWidth)
  const newY = Math.round((draggedItem.y * totalRowHeight + deltaY) / totalRowHeight)

  // 边界检查
  const clampedX = Math.max(0, Math.min(newX, props.cols - draggedItem.w))
  const clampedY = Math.max(0, newY)

  // 如果位置发生变化，更新占位符并处理碰撞
  if (clampedX !== placeholderPosition.value.x || clampedY !== placeholderPosition.value.y) {
    placeholderPosition.value = { x: clampedX, y: clampedY, w: draggedItem.w, h: draggedItem.h }

    // 处理碰撞挤压
    handleCollision(draggedItem, clampedX, clampedY)
  }
}

// 鼠标释放
const handleMouseUp = () => {
  if (!draggingId.value) return

  const draggedItem = layoutItems.value.find(item => item.id === draggingId.value)
  if (draggedItem && placeholderPosition.value) {
    // 更新拖拽项的位置到占位符位置
    draggedItem.x = placeholderPosition.value.x
    draggedItem.y = placeholderPosition.value.y

    // 触发自动吸附
    if (props.autoCompact) {
      isAnimating.value = true
      nextTick(() => {
        compactLayout()
        emitChange()
      })
    } else {
      emitChange()
    }
  }

  draggingId.value = null
  dragOffset.value = { x: 0, y: 0 }
  placeholderPosition.value = null
}

// 处理碰撞检测与挤压
const handleCollision = (draggedItem, newX, newY) => {
  const otherItems = layoutItems.value.filter(item => item.id !== draggedItem.id)

  // 检查是否与任何其他项碰撞
  const collidingItems = otherItems.filter(item =>
    isColliding(
      { x: newX, y: newY, w: draggedItem.w, h: draggedItem.h },
      item
    )
  )

  if (collidingItems.length > 0) {
    // 为碰撞的项寻找新位置
    collidingItems.forEach(item => {
      const newPosition = findNewPosition(item, draggedItem, newX, newY)
      if (newPosition) {
        item.x = newPosition.x
        item.y = newPosition.y
      }
    })

    // 级联处理：检查被移动的项是否又与其他项碰撞
    resolveCollisionsCascade(otherItems)
  }
}

// 为新位置寻找合适的位置
const findNewPosition = (item, draggedItem, dragX, dragY) => {
  const otherItems = layoutItems.value.filter(i => i.id !== item.id && i.id !== draggedItem.id)

  // 尝试不同的位置，优先向下移动
  for (let offsetY = 1; offsetY < 20; offsetY++) {
    const testY = item.y + offsetY

    // 检查这个位置是否可用
    const testRect = { x: item.x, y: testY, w: item.w, h: item.h }
    const hasCollision = otherItems.some(other => isColliding(testRect, other))

    if (!hasCollision) {
      return { x: item.x, y: testY }
    }
  }

  // 如果向下找不到位置，尝试向右
  for (let offsetX = 1; offsetX < props.cols - item.x; offsetX++) {
    const testX = item.x + offsetX
    const testRect = { x: testX, y: item.y, w: item.w, h: item.h }
    const hasCollision = otherItems.some(other => isColliding(testRect, other))

    if (!hasCollision) {
      return { x: testX, y: item.y }
    }
  }

  return null
}

// 级联碰撞解决
const resolveCollisionsCascade = (items) => {
  let hasChanges = true
  let iterations = 0
  const maxIterations = 10

  while (hasChanges && iterations < maxIterations) {
    hasChanges = false
    iterations++

    for (let i = 0; i < items.length; i++) {
      for (let j = i + 1; j < items.length; j++) {
        if (isColliding(items[i], items[j])) {
          // 移动后面的项向下
          const newY = items[j].y + items[i].h
          items[j].y = newY
          hasChanges = true
        }
      }
    }
  }
}

// 触发更新事件
const emitChange = () => {
  emit('update:modelValue', layoutItems.value)
  emit('change', layoutItems.value)
}

// 添加新项
const addItem = (item) => {
  const newItem = {
    ...item,
    id: item.id || `item-${Date.now()}`,
    x: item.x ?? 0,
    y: item.y ?? 0,
    w: item.w ?? 1,
    h: item.h ?? 1
  }

  // 找到合适的位置
  const position = findEmptyPosition(newItem.w, newItem.h)
  newItem.x = position.x
  newItem.y = position.y

  layoutItems.value.push(newItem)

  if (props.autoCompact) {
    compactLayout()
  }

  emitChange()
}

// 查找空位置
const findEmptyPosition = (w, h) => {
  const maxY = Math.max(...layoutItems.value.map(item => item.y + item.h), 0)

  for (let y = 0; y <= maxY + 1; y++) {
    for (let x = 0; x <= props.cols - w; x++) {
      const testRect = { x, y, w, h }
      const hasCollision = layoutItems.value.some(item => isColliding(testRect, item))

      if (!hasCollision) {
        return { x, y }
      }
    }
  }

  return { x: 0, y: maxY + 1 }
}

// 删除项
const removeItem = (id) => {
  const index = layoutItems.value.findIndex(item => item.id === id)
  if (index > -1) {
    layoutItems.value.splice(index, 1)

    if (props.autoCompact) {
      isAnimating.value = true
      nextTick(() => {
        compactLayout()
        emitChange()
      })
    } else {
      emitChange()
    }
  }
}

// 暴露方法
defineExpose({
  addItem,
  removeItem,
  compactLayout,
  getLayout: () => layoutItems.value
})
</script>

<style scoped>
.draggable-grid {
  border-radius: var(--radius-lg);
  background: var(--gray-50);
  overflow: hidden;
}

.grid-item {
  touch-action: none;
}

.grid-item-default {
  width: 100%;
  height: 100%;
  background: white;
  border: 2px solid var(--gray-200);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: var(--gray-700);
  transition: all 0.2s ease;
}

.grid-item:hover .grid-item-default {
  border-color: var(--primary-light);
  background: var(--gray-50);
}

.grid-item.is-dragging .grid-item-default {
  border-color: var(--primary);
  background: white;
}

.grid-item-label {
  pointer-events: none;
  user-select: none;
}

.grid-placeholder {
  pointer-events: none;
}
</style>
