<template>
  <div 
    class="grid-layout-container"
    :style="containerStyle"
    @mousedown="handleMouseDown"
    @mousemove="handleMouseMove"
    @mouseup="handleMouseUp"
    @mouseleave="handleMouseUp"
  >
    <!-- 网格背景 -->
    <div class="grid-background" :style="gridBackgroundStyle"></div>
    
    <!-- 网格项 -->
    <div
      v-for="(item, index) in items"
      :key="item && item.id ? item.id : index"
      class="grid-item"
      :class="{ 'dragging': item && item.isDragging }"
      :style="item && getItemStyle(item)"
      @mousedown="item && startDrag($event, item)"
      v-if="item"
    >
      <div class="grid-item-content">
        <slot name="item" :item="item" :index="index">
          <div class="default-item">
            {{ item && item.content ? item.content : `Item ${index + 1}` }}
          </div>
        </slot>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

export default {
  name: 'GridLayout',
  props: {
    // 网格大小（像素）
    gridSize: {
      type: Number,
      default: 20
    },
    // 容器宽度
    width: {
      type: Number,
      default: 800
    },
    // 容器高度
    height: {
      type: Number,
      default: 600
    },
    // 初始项目列表
    modelValue: {
      type: Array,
      default: () => []
    }
  },
  emits: ['update:modelValue', 'item-move', 'item-resize'],
  setup(props, { emit }) {
    const items = ref([])
    const draggedItem = ref(null)
    const dragOffset = ref({ x: 0, y: 0 })
    const isDragging = ref(false)
    const containerRef = ref(null)
    
    // 初始化项目
    const initializeItems = () => {
      if (props.modelValue && props.modelValue.length > 0) {
        items.value = props.modelValue.map(item => ({
          ...item,
          isDragging: false
        }))
      } else {
        // 默认示例项目
        items.value = [
          { id: '1', x: 0, y: 0, width: 200, height: 150, content: '项目 1' },
          { id: '2', x: 220, y: 0, width: 180, height: 150, content: '项目 2' },
          { id: '3', x: 0, y: 170, width: 200, height: 120, content: '项目 3' },
          { id: '4', x: 220, y: 170, width: 180, height: 120, content: '项目 4' }
        ]
      }
    }
    
    // 监听modelValue变化
    watch(() => props.modelValue, (newValue) => {
      if (newValue && newValue.length > 0) {
        items.value = newValue.map(item => ({
          ...item,
          isDragging: false
        }))
      }
    }, { deep: true, immediate: true })
    
    // 容器样式
    const containerStyle = computed(() => ({
      width: `${props.width}px`,
      height: `${props.height}px`,
      position: 'relative'
    }))
    
    // 网格背景样式
    const gridBackgroundStyle = computed(() => ({
      backgroundImage: `
        linear-gradient(to right, rgba(200, 200, 200, 0.3) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(200, 200, 200, 0.3) 1px, transparent 1px)
      `,
      backgroundSize: `${props.gridSize}px ${props.gridSize}px`
    }))
    
    // 获取项目样式
    const getItemStyle = (item) => {
      // 对齐到网格
      const x = Math.round(item.x / props.gridSize) * props.gridSize
      const y = Math.round(item.y / props.gridSize) * props.gridSize
      
      return {
        position: 'absolute',
        left: `${x}px`,
        top: `${y}px`,
        width: `${item.width}px`,
        height: `${item.height}px`,
        zIndex: item.isDragging ? 1000 : 1
      }
    }
    
    // 对齐到网格
    const snapToGrid = (value) => {
      return Math.round(value / props.gridSize) * props.gridSize
    }
    
    // 开始拖拽
    const startDrag = (event, item) => {
      event.preventDefault()
      event.stopPropagation()
      
      draggedItem.value = item
      isDragging.value = true
      
      const rect = event.currentTarget.getBoundingClientRect()
      dragOffset.value = {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top
      }
      
      // 标记为拖拽中
      item.isDragging = true
    }
    
    // 处理鼠标移动
    const handleMouseMove = (event) => {
      if (!isDragging.value || !draggedItem.value) return
      
      const containerRect = containerRef.value?.getBoundingClientRect()
      if (!containerRect) return
      
      // 计算新位置
      let newX = event.clientX - containerRect.left - dragOffset.value.x
      let newY = event.clientY - containerRect.top - dragOffset.value.y
      
      // 限制在容器内
      newX = Math.max(0, Math.min(newX, props.width - draggedItem.value.width))
      newY = Math.max(0, Math.min(newY, props.height - draggedItem.value.height))
      
      // 对齐到网格
      newX = snapToGrid(newX)
      newY = snapToGrid(newY)
      
      // 检查碰撞并执行挤压
      const adjustedPosition = checkCollisionAndAdjust(
        draggedItem.value,
        newX,
        newY
      )
      
      // 更新位置
      draggedItem.value.x = adjustedPosition.x
      draggedItem.value.y = adjustedPosition.y
      
      // 触发事件
      emit('item-move', {
        item: draggedItem.value,
        x: adjustedPosition.x,
        y: adjustedPosition.y
      })
    }
    
    // 检查碰撞并调整位置
    const checkCollisionAndAdjust = (draggedItem, newX, newY) => {
      const draggedRect = {
        left: newX,
        top: newY,
        right: newX + draggedItem.width,
        bottom: newY + draggedItem.height
      }
      
      for (const item of items.value) {
        if (item.id === draggedItem.id || item.isDragging) continue
        
        const itemRect = {
          left: item.x,
          top: item.y,
          right: item.x + item.width,
          bottom: item.y + item.height
        }
        
        // 检查碰撞
        if (isColliding(draggedRect, itemRect)) {
          // 计算推动方向和距离
          const pushDistance = getPushDistance(draggedRect, itemRect)
          
          // 根据拖拽方向决定推动方向
          const dragDirection = getDragDirection(draggedItem, newX, newY)
          
          if (dragDirection.horizontal === 'right') {
            // 向右拖拽，向右推动
            item.x = draggedRect.right + props.gridSize
          } else if (dragDirection.horizontal === 'left') {
            // 向左拖拽，向左推动
            item.x = draggedRect.left - item.width - props.gridSize
          }
          
          if (dragDirection.vertical === 'down') {
            // 向下拖拽，向下推动
            item.y = draggedRect.bottom + props.gridSize
          } else if (dragDirection.vertical === 'up') {
            // 向上拖拽，向上推动
            item.y = draggedRect.top - item.height - props.gridSize
          }
          
          // 确保被推动的项目仍在容器内
          item.x = Math.max(0, Math.min(item.x, props.width - item.width))
          item.y = Math.max(0, Math.min(item.y, props.height - item.height))
          
          // 递归检查被推动的项目是否与其他项目碰撞
          checkCollisionAndAdjust(item, item.x, item.y)
        }
      }
      
      return { x: newX, y: newY }
    }
    
    // 检查两个矩形是否碰撞
    const isColliding = (rect1, rect2) => {
      return !(
        rect1.right <= rect2.left ||
        rect1.left >= rect2.right ||
        rect1.bottom <= rect2.top ||
        rect1.top >= rect2.bottom
      )
    }
    
    // 获取推动距离
    const getPushDistance = (draggedRect, itemRect) => {
      const horizontalPush = Math.min(
        Math.abs(draggedRect.right - itemRect.left),
        Math.abs(draggedRect.left - itemRect.right)
      )
      
      const verticalPush = Math.min(
        Math.abs(draggedRect.bottom - itemRect.top),
        Math.abs(draggedRect.top - itemRect.bottom)
      )
      
      return {
        horizontal: horizontalPush,
        vertical: verticalPush
      }
    }
    
    // 获取拖拽方向
    const getDragDirection = (item, newX, newY) => {
      return {
        horizontal: newX > item.x ? 'right' : newX < item.x ? 'left' : 'none',
        vertical: newY > item.y ? 'down' : newY < item.y ? 'up' : 'none'
      }
    }
    
    // 处理鼠标释放
    const handleMouseUp = () => {
      if (draggedItem.value) {
        draggedItem.value.isDragging = false
        emit('update:modelValue', items.value)
      }
      
      isDragging.value = false
      draggedItem.value = null
      
      // 执行自动向上吸附
      setTimeout(() => {
        performAutoSnapUp()
      }, 100)
    }
    
    // 执行自动向上吸附
    const performAutoSnapUp = () => {
      // 按Y坐标排序项目
      const sortedItems = [...items.value].sort((a, b) => a.y - b.y)
      
      for (let i = 0; i < sortedItems.length; i++) {
        const item = sortedItems[i]
        
        // 查找可以上移的空间
        let canMoveUp = true
        let newY = 0
        
        // 从顶部开始，检查每个可能的位置
        for (let y = 0; y < item.y; y += props.gridSize) {
          const testRect = {
            left: item.x,
            top: y,
            right: item.x + item.width,
            bottom: y + item.height
          }
          
          // 检查这个位置是否与其他项目碰撞
          let hasCollision = false
          for (const otherItem of items.value) {
            if (otherItem.id === item.id) continue
            
            const otherRect = {
              left: otherItem.x,
              top: otherItem.y,
              right: otherItem.x + otherItem.width,
              bottom: otherItem.y + otherItem.height
            }
            
            if (isColliding(testRect, otherRect)) {
              hasCollision = true
              break
            }
          }
          
          if (!hasCollision) {
            newY = y
          } else {
            break
          }
        }
        
        // 如果可以上移，更新位置
        if (newY < item.y) {
          item.y = newY
        }
      }
      
      emit('update:modelValue', items.value)
    }
    
    // 处理鼠标按下（用于捕获全局事件）
    const handleMouseDown = (event) => {
      containerRef.value = event.currentTarget
    }
    
    // 初始化
    onMounted(() => {
      initializeItems()
      
      // 添加全局事件监听器
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
    })
    
    onUnmounted(() => {
      // 移除全局事件监听器
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
    })
    
    return {
      items,
      containerStyle,
      gridBackgroundStyle,
      getItemStyle,
      startDrag,
      handleMouseDown,
      handleMouseMove,
      handleMouseUp
    }
  }
}
</script>

<style scoped>
.grid-layout-container {
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  user-select: none;
}

.grid-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.grid-item {
  background-color: white;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: move;
  transition: box-shadow 0.2s, transform 0.2s;
}

.grid-item:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.grid-item.dragging {
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
  opacity: 0.8;
  z-index: 1000;
}

.grid-item-content {
  padding: 16px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.default-item {
  font-weight: 500;
  color: #374151;
}
</style>