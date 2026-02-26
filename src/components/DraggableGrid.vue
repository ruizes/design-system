<template>
  <div
    ref="gridContainer"
    class="draggable-grid-container"
    :style="gridContainerStyle"
    @mousedown="handleContainerMouseDown"
  >
    <div
      class="draggable-grid-content"
      :style="gridStyle"
    >
      <template v-if="gridItems && gridItems.length">
        <div
          v-for="item in gridItems"
          :key="item.id"
          class="grid-item"
          :class="{
            'is-dragging': draggingId === item.id,
            'is-animating': isAnimating && draggingId !== item.id
          }"
          :style="getItemStyle(item)"
          @mousedown="handleItemMouseDown($event, item)"
        >
          <slot :item="item" :isDragging="draggingId === item.id">
            <div class="grid-item-default">
              <span class="grid-item-label">{{ item.label || item.id }}</span>
            </div>
          </slot>
        </div>
      </template>

      <!-- 网格背景 -->
      <div
        v-if="showGrid"
        class="grid-background"
        :style="gridBackgroundStyle"
      >
        <div
          v-for="row in actualGridRows"
          :key="`row-${row}`"
          class="grid-row"
        >
          <div
            v-for="col in cols"
            :key="`cell-${row}-${col}`"
            class="grid-cell"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  cols: {
    type: Number,
    default: 4
  },
  rowHeight: {
    type: Number,
    default: 100
  },
  gap: {
    type: Number,
    default: 16
  },
  showGrid: {
    type: Boolean,
    default: true
  },
  compact: {
    type: Boolean,
    default: true
  },
  maxRows: {
    type: Number,
    default: 0 // 0 表示不限制行数，根据内容自动扩展
  },
  containerHeight: {
    type: [Number, String],
    default: 'auto' // 可以设置为固定高度如 400 或 '400px'
  }
})

const emit = defineEmits(['update:items', 'change'])

// 响应式状态
const gridContainer = ref(null)
const draggingId = ref(null)
const dragOffset = ref({ x: 0, y: 0 })
const dragPosition = ref({ x: 0, y: 0 })
const isAnimating = ref(false)
const containerWidth = ref(0)

// 计算网格单元格宽度
const cellWidth = computed(() => {
  if (!containerWidth.value) return 0
  const totalGap = (props.cols - 1) * props.gap
  return (containerWidth.value - totalGap) / props.cols
})

// 计算实际需要的网格行数
const actualGridRows = computed(() => {
  if (!gridItems.value.length) return 4 // 默认最小行数
  const maxRow = Math.max(...gridItems.value.map(item => item.row + item.h - 1))
  return maxRow + 2 // 添加一些空白行方便拖拽
})

// 计算网格行数（考虑最大行数限制）
const gridRows = computed(() => {
  if (props.maxRows > 0) {
    return props.maxRows
  }
  return actualGridRows.value
})

// 计算容器高度
const computedContainerHeight = computed(() => {
  if (props.containerHeight === 'auto') {
    return 'auto'
  }
  if (typeof props.containerHeight === 'number') {
    return `${props.containerHeight}px`
  }
  return props.containerHeight
})

// 计算内容高度
const contentHeight = computed(() => {
  const rows = actualGridRows.value
  return rows * props.rowHeight + (rows - 1) * props.gap + props.gap * 2
})

// 网格容器样式
const gridContainerStyle = computed(() => {
  const height = computedContainerHeight.value
  return {
    position: 'relative',
    height: height,
    overflowY: height === 'auto' ? 'visible' : 'auto',
    overflowX: 'hidden'
  }
})

// 网格内容样式
const gridStyle = computed(() => {
  return {
    position: 'relative',
    minHeight: `${contentHeight.value}px`,
    padding: `${props.gap}px`
  }
})

// 网格背景样式
const gridBackgroundStyle = computed(() => ({
  position: 'absolute',
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
  pointerEvents: 'none',
  zIndex: 0,
  display: 'grid',
  gridTemplateColumns: `repeat(${props.cols}, 1fr)`,
  gridTemplateRows: `repeat(${actualGridRows.value}, ${props.rowHeight}px)`,
  gap: `${props.gap}px`,
  padding: `${props.gap}px`
}))

// 内部维护的网格项
const gridItems = ref([])

// 初始化网格项
const initializeGridItems = () => {
  gridItems.value = props.items.map((item, index) => ({
    ...item,
    w: item.w || 1,
    h: item.h || 1,
    col: item.col ?? (index % props.cols),
    row: item.row ?? Math.floor(index / props.cols),
    id: item.id || `item-${index}`
  }))
}

// 监听 props.items 变化
watch(() => props.items, initializeGridItems, { immediate: true, deep: true })

// 获取项目样式
const getItemStyle = (item) => {
  const isDragging = draggingId.value === item.id

  if (isDragging) {
    return {
      position: 'absolute',
      left: `${dragPosition.value.x}px`,
      top: `${dragPosition.value.y}px`,
      width: `${item.w * cellWidth.value + (item.w - 1) * props.gap}px`,
      height: `${item.h * props.rowHeight + (item.h - 1) * props.gap}px`,
      zIndex: 1000,
      transform: 'scale(1.02)',
      boxShadow: '0 10px 40px rgba(0, 0, 0, 0.2)'
    }
  }

  return {
    position: 'absolute',
    left: `${item.col * (cellWidth.value + props.gap) + props.gap}px`,
    top: `${item.row * (props.rowHeight + props.gap) + props.gap}px`,
    width: `${item.w * cellWidth.value + (item.w - 1) * props.gap}px`,
    height: `${item.h * props.rowHeight + (item.h - 1) * props.gap}px`,
    zIndex: 1,
    transition: isAnimating.value ? 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)' : 'none'
  }
}

// 获取滚动偏移
const getScrollOffset = () => {
  if (!gridContainer.value) return { x: 0, y: 0 }
  return {
    x: gridContainer.value.scrollLeft || 0,
    y: gridContainer.value.scrollTop || 0
  }
}

// 将像素坐标转换为网格坐标
const pixelToGrid = (x, y) => {
  const scrollOffset = getScrollOffset()
  const adjustedX = x + scrollOffset.x
  const adjustedY = y + scrollOffset.y

  const col = Math.round((adjustedX - props.gap) / (cellWidth.value + props.gap))
  const row = Math.round((adjustedY - props.gap) / (props.rowHeight + props.gap))
  return {
    col: Math.max(0, Math.min(col, props.cols - 1)),
    row: Math.max(0, row)
  }
}

// 将网格坐标转换为像素坐标
const gridToPixel = (col, row) => ({
  x: col * (cellWidth.value + props.gap) + props.gap,
  y: row * (props.rowHeight + props.gap) + props.gap
})

// 检查两个项目是否碰撞
const checkCollision = (item1, item2) => {
  return !(
    item1.col + item1.w <= item2.col ||
    item2.col + item2.w <= item1.col ||
    item1.row + item1.h <= item2.row ||
    item2.row + item2.h <= item1.row
  )
}

// 获取与指定项目碰撞的所有项目
const getCollisions = (item, excludeId = null) => {
  return gridItems.value.filter(other => {
    if (other.id === item.id || other.id === excludeId) return false
    return checkCollision(item, other)
  })
}

// 移动项目并处理碰撞
const moveItem = (item, newCol, newRow) => {
  const oldCol = item.col
  const oldRow = item.row

  // 边界检查
  newCol = Math.max(0, Math.min(newCol, props.cols - item.w))
  newRow = Math.max(0, newRow)

  // 如果没有变化，直接返回
  if (oldCol === newCol && oldRow === newRow) return

  // 更新位置
  item.col = newCol
  item.row = newRow

  // 检测并解决所有碰撞
  resolveAllCollisions()

  // 如果启用了紧凑模式，执行向上吸附
  if (props.compact) {
    nextTick(() => {
      compactGrid()
    })
  }
}

// 解决碰撞 - 推动被碰撞的项目
const resolveCollision = (movingItem, staticItem, visited = new Set()) => {
  // 防止循环递归
  if (visited.has(staticItem.id)) return
  visited.add(staticItem.id)

  // 计算重叠情况
  const overlapX = Math.min(
    movingItem.col + movingItem.w - staticItem.col,
    staticItem.col + staticItem.w - movingItem.col
  )
  const overlapY = Math.min(
    movingItem.row + movingItem.h - staticItem.row,
    staticItem.row + staticItem.h - movingItem.row
  )

  let newCol = staticItem.col
  let newRow = staticItem.row

  // 选择推动方向：优先推动重叠较小的方向
  if (overlapX < overlapY) {
    // 水平方向推动
    const movingCenter = movingItem.col + movingItem.w / 2
    const staticCenter = staticItem.col + staticItem.w / 2

    if (movingCenter <= staticCenter) {
      newCol = movingItem.col + movingItem.w
    } else {
      newCol = movingItem.col - staticItem.w
    }
    // 边界检查
    newCol = Math.max(0, Math.min(newCol, props.cols - staticItem.w))
  } else {
    // 垂直方向推动
    if (movingItem.row <= staticItem.row) {
      newRow = movingItem.row + movingItem.h
    } else {
      newRow = movingItem.row - staticItem.h
    }
    newRow = Math.max(0, newRow)
  }

  // 如果被推动的位置超出边界，尝试另一个方向
  if (newCol + staticItem.w > props.cols || newCol < 0) {
    if (movingItem.row <= staticItem.row) {
      newRow = movingItem.row + movingItem.h
    } else {
      newRow = movingItem.row - staticItem.h
    }
    newRow = Math.max(0, newRow)
    newCol = staticItem.col // 恢复原来的列
  }

  // 更新位置
  staticItem.col = newCol
  staticItem.row = newRow

  // 递归处理被推动项目的碰撞
  const furtherCollisions = getCollisions(staticItem, movingItem.id)
  if (furtherCollisions.length > 0) {
    furtherCollisions.forEach(item => {
      resolveCollision(staticItem, item, visited)
    })
  }
}

// 解决所有碰撞 - 确保没有重叠
const resolveAllCollisions = () => {
  let hasCollision = true
  let iterations = 0
  const maxIterations = 100 // 防止无限循环

  while (hasCollision && iterations < maxIterations) {
    hasCollision = false
    iterations++

    for (let i = 0; i < gridItems.value.length; i++) {
      const item = gridItems.value[i]
      const collisions = getCollisions(item)

      if (collisions.length > 0) {
        hasCollision = true
        collisions.forEach(other => {
          resolveCollision(item, other, new Set())
        })
      }
    }
  }
}

// 紧凑网格 - 自动向上吸附
const compactGrid = () => {
  isAnimating.value = true

  // 按行排序项目
  const sortedItems = [...gridItems.value].sort((a, b) => {
    if (a.row !== b.row) return a.row - b.row
    return a.col - b.col
  })

  // 尝试将每个项目向上移动
  sortedItems.forEach(item => {
    let bestRow = item.row

    // 从当前位置向上查找可以放置的位置
    for (let testRow = item.row - 1; testRow >= 0; testRow--) {
      const testItem = { ...item, row: testRow }
      const collisions = getCollisions(testItem, item.id)

      if (collisions.length === 0) {
        bestRow = testRow
      } else {
        break
      }
    }

    if (bestRow !== item.row) {
      item.row = bestRow
    }
  })

  setTimeout(() => {
    isAnimating.value = false
  }, 300)
}

// 处理项目鼠标按下
const handleItemMouseDown = (event, item) => {
  event.preventDefault()
  event.stopPropagation()

  const rect = gridContainer.value.getBoundingClientRect()
  const itemRect = event.currentTarget.getBoundingClientRect()

  draggingId.value = item.id
  dragOffset.value = {
    x: event.clientX - itemRect.left,
    y: event.clientY - itemRect.top
  }
  dragPosition.value = {
    x: itemRect.left - rect.left,
    y: itemRect.top - rect.top
  }

  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleMouseUp)
}

// 处理鼠标移动
const handleMouseMove = (event) => {
  if (!draggingId.value) return

  const rect = gridContainer.value.getBoundingClientRect()

  dragPosition.value = {
    x: event.clientX - rect.left - dragOffset.value.x,
    y: event.clientY - rect.top - dragOffset.value.y
  }

  // 实时碰撞检测和挤压
  const gridPos = pixelToGrid(dragPosition.value.x, dragPosition.value.y)
  const draggedItem = gridItems.value.find(item => item.id === draggingId.value)

  if (draggedItem) {
    // 保存原始位置
    const originalCol = draggedItem.col
    const originalRow = draggedItem.row

    // 临时更新位置用于碰撞检测
    draggedItem.col = gridPos.col
    draggedItem.row = gridPos.row

    // 解决所有碰撞
    resolveAllCollisions()

    // 恢复位置（拖拽结束时会正式更新）
    draggedItem.col = originalCol
    draggedItem.row = originalRow
  }
}

// 处理鼠标释放
const handleMouseUp = () => {
  if (!draggingId.value) return

  const draggedItem = gridItems.value.find(item => item.id === draggingId.value)

  if (draggedItem) {
    const gridPos = pixelToGrid(dragPosition.value.x, dragPosition.value.y)
    moveItem(draggedItem, gridPos.col, gridPos.row)

    // 触发更新事件
    emit('update:items', gridItems.value)
    emit('change', gridItems.value)
  }

  draggingId.value = null
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)
}

// 处理容器鼠标按下
const handleContainerMouseDown = (event) => {
  // 可以在这里添加点击空白区域的处理逻辑
}

// 更新容器宽度
const updateContainerWidth = () => {
  if (gridContainer.value) {
    containerWidth.value = gridContainer.value.clientWidth
  }
}

// 监听窗口大小变化
const handleResize = () => {
  updateContainerWidth()
  nextTick(() => {
    if (props.compact) {
      compactGrid()
    }
  })
}

onMounted(() => {
  updateContainerWidth()
  window.addEventListener('resize', handleResize)

  // 初始紧凑
  if (props.compact) {
    nextTick(() => {
      compactGrid()
    })
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleMouseUp)
})
</script>

<style scoped>
.draggable-grid-container {
  position: relative;
  background: var(--gray-50);
  border-radius: var(--radius-lg);
  border: 2px dashed var(--gray-200);
}

.draggable-grid-container::-webkit-scrollbar {
  width: 8px;
}

.draggable-grid-container::-webkit-scrollbar-track {
  background: var(--gray-100);
  border-radius: var(--radius-md);
}

.draggable-grid-container::-webkit-scrollbar-thumb {
  background: var(--gray-400);
  border-radius: var(--radius-md);
}

.draggable-grid-container::-webkit-scrollbar-thumb:hover {
  background: var(--gray-500);
}

.draggable-grid-content {
  position: relative;
}

.grid-background {
  opacity: 0.3;
}

.grid-cell {
  border: 1px dashed var(--gray-300);
  border-radius: var(--radius-sm);
  min-height: v-bind('`${rowHeight}px`');
}

.grid-item {
  cursor: grab;
  user-select: none;
  touch-action: none;
}

.grid-item:active {
  cursor: grabbing;
}

.grid-item.is-dragging {
  cursor: grabbing;
}

.grid-item.is-animating {
  pointer-events: none;
}

.grid-item-default {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 500;
  box-shadow: var(--shadow);
  transition: box-shadow 0.2s ease;
}

.grid-item:hover .grid-item-default {
  box-shadow: var(--shadow-lg);
}

.grid-item-label {
  font-size: var(--text-sm);
  padding: var(--space-sm);
  text-align: center;
}
</style>
