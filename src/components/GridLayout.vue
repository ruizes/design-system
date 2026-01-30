<template>
  <div class="grid-layout-wrapper">
    <div
      class="grid-layout-container"
      ref="containerRef"
      @mousemove="handleMouseMove"
      @mouseup="handleMouseUp"
      @mouseleave="handleMouseUp"
    >
      <div class="grid-background" v-if="showGrid">
        <div
          v-for="i in gridCells"
          :key="i"
          class="grid-cell"
          :style="getGridCellStyle(i - 1)"
        ></div>
      </div>

      <div
        v-for="item in items"
        :key="item.id"
        class="grid-item"
        :class="{
          'grid-item-dragging': draggingItem?.id === item.id,
          'grid-item-resizing': resizingItem?.id === item.id
        }"
        :style="getItemStyle(item)"
        @mousedown="startDrag($event, item)"
      >
        <div class="grid-item-content">
          <slot name="item" :item="item">{{ item?.content || item?.title || '' }}</slot>
        </div>
        <div
          class="resize-handle resize-handle-se"
          @mousedown.stop="startResize($event, item)"
        ></div>
      </div>

      <div
        v-if="dragPreview"
        class="drag-preview"
        :style="getPreviewStyle()"
      ></div>
    </div>
  </div>
</template>

<script setup>import { ref, computed, onMounted } from 'vue';
const props = defineProps({
 items: {
 type: Array,
 required: true
 },
 gridSize: {
 type: Number,
 default: 20
 },
 containerWidth: {
 type: Number,
 default: 800
 },
 containerHeight: {
 type: Number,
 default: 600
 },
 cols: {
 type: Number,
 default: 20
 },
 rows: {
 type: Number,
 default: 15
 },
 showGrid: {
 type: Boolean,
 default: true
 },
 cellWidth: {
 type: Number,
 default: 40
 },
 cellHeight: {
 type: Number,
 default: 40
 }
});
const emit = defineEmits(['update:items', 'item-moved', 'item-resized']);
const containerRef = ref(null);
const draggingItem = ref(null);
const resizingItem = ref(null);
const dragStartPos = ref({ x: 0, y: 0 });
const itemStartPos = ref({ x: 0, y: 0 });
const itemStartSize = ref({ width: 0, height: 0 });
const dragPreview = ref(null);
const currentMousePos = ref({ x: 0, y: 0 });
const gridCells = computed(() => props.cols * props.rows);
const snapToGrid = (value, gridSize) => {
 return Math.round(value / gridSize) * gridSize;
};
const getGridCellStyle = (index) => {
 const col = index % props.cols;
 const row = Math.floor(index / props.cols);
 return {
 left: `${col * props.cellWidth}px`,
 top: `${row * props.cellHeight}px`,
 width: `${props.cellWidth}px`,
 height: `${props.cellHeight}px`
 };
};
const getItemStyle = (item) => {
 return {
 left: `${item.x}px`,
 top: `${item.y}px`,
 width: `${item.width}px`,
 height: `${item.height}px`,
 zIndex: draggingItem.value?.id === item.id ? 1000 : item.zIndex || 1
 };
};
const getPreviewStyle = () => {
 if (!dragPreview.value)
 return {};
 return {
 left: `${dragPreview.value.x}px`,
 top: `${dragPreview.value.y}px`,
 width: `${dragPreview.value.width}px`,
 height: `${dragPreview.value.height}px`
 };
};
const checkCollision = (itemA, itemB, excludeId = null) => {
 if (itemB.id === excludeId)
 return false;
 return !(itemA.x + itemA.width <= itemB.x ||
 itemA.x >= itemB.x + itemB.width ||
 itemA.y + itemA.height <= itemB.y ||
 itemA.y >= itemB.y + itemB.height);
};
const findCollidingItems = (movingItem, newPosition) => {
 const testItem = { ...movingItem, ...newPosition };
 return props.items.filter(item => checkCollision(testItem, item, movingItem.id));
};
const pushItemsAway = (movingItem, collidingItems, direction) => {
 const updatedItems = [...props.items];
 const processed = new Set();
 const pushItem = (item, pushDirection, depth = 0) => {
 if (depth > 10 || processed.has(item.id))
 return;
 processed.add(item.id);
 const itemIndex = updatedItems.findIndex(i => i.id === item.id);
 if (itemIndex === -1)
 return;
 const currentItem = updatedItems[itemIndex];
 let newX = currentItem.x;
 let newY = currentItem.y;
 if (pushDirection === 'right') {
 newX = snapToGrid(movingItem.x + movingItem.width + props.cellWidth, props.cellWidth);
 }
 else if (pushDirection === 'left') {
 newX = snapToGrid(movingItem.x - currentItem.width - props.cellWidth, props.cellWidth);
 }
 else if (pushDirection === 'down') {
 newY = snapToGrid(movingItem.y + movingItem.height + props.cellHeight, props.cellHeight);
 }
 else if (pushDirection === 'up') {
 newY = snapToGrid(movingItem.y - currentItem.height - props.cellHeight, props.cellHeight);
 }
 newX = Math.max(0, Math.min(newX, props.containerWidth - currentItem.width));
 newY = Math.max(0, Math.min(newY, props.containerHeight - currentItem.height));
 const testItem = { ...currentItem, x: newX, y: newY };
 const newCollisions = props.items.filter(other => checkCollision(testItem, other, item.id) &&
 other.id !== movingItem.id &&
 !processed.has(other.id));
 updatedItems[itemIndex] = { ...currentItem, x: newX, y: newY };
 newCollisions.forEach(colliding => {
 pushItem(colliding, pushDirection, depth + 1);
 });
 };
 collidingItems.forEach(item => {
 const centerX = item.x + item.width / 2;
 const centerY = item.y + item.height / 2;
 const movingCenterX = movingItem.x + movingItem.width / 2;
 const movingCenterY = movingItem.y + movingItem.height / 2;
 const dx = centerX - movingCenterX;
 const dy = centerY - movingCenterY;
 let pushDirection;
 if (Math.abs(dx) > Math.abs(dy)) {
 pushDirection = dx > 0 ? 'right' : 'left';
 }
 else {
 pushDirection = dy > 0 ? 'down' : 'up';
 }
 pushItem(item, pushDirection);
 });
 return updatedItems;
};
const compactItemsUp = () => {
 const sortedItems = [...props.items].sort((a, b) => {
 if (a.y !== b.y)
 return a.y - b.y;
 return a.x - b.x;
 });
 const updatedItems = [];
 for (const item of sortedItems) {
 let newY = item.y;
 let canMoveUp = true;
 while (canMoveUp && newY > 0) {
 const testY = newY - props.cellHeight;
 if (testY < 0)
 break;
 const testItem = { ...item, y: testY };
 let hasCollision = false;
 for (const other of updatedItems) {
 if (checkCollision(testItem, other, item.id)) {
 hasCollision = true;
 break;
 }
 }
 if (hasCollision) {
 canMoveUp = false;
 }
 else {
 newY = testY;
 }
 }
 updatedItems.push({ ...item, y: newY });
 }
 return updatedItems;
};
const startDrag = (event, item) => {
 event.preventDefault();
 draggingItem.value = item;
 dragStartPos.value = { x: event.clientX, y: event.clientY };
 itemStartPos.value = { x: item.x, y: item.y };
 dragPreview.value = { ...item };
};
const startResize = (event, item) => {
 event.preventDefault();
 resizingItem.value = item;
 dragStartPos.value = { x: event.clientX, y: event.clientY };
 itemStartSize.value = { width: item.width, height: item.height };
 itemStartPos.value = { x: item.x, y: item.y };
};
const handleMouseMove = (event) => {
 currentMousePos.value = { x: event.clientX, y: event.clientY };
 if (draggingItem.value) {
 const deltaX = event.clientX - dragStartPos.value.x;
 const deltaY = event.clientY - dragStartPos.value.y;
 let newX = itemStartPos.value.x + deltaX;
 let newY = itemStartPos.value.y + deltaY;
 newX = snapToGrid(newX, props.cellWidth);
 newY = snapToGrid(newY, props.cellHeight);
 newX = Math.max(0, Math.min(newX, props.containerWidth - draggingItem.value.width));
 newY = Math.max(0, Math.min(newY, props.containerHeight - draggingItem.value.height));
 const newPosition = { x: newX, y: newY };
 dragPreview.value = { ...dragPreview.value, ...newPosition };
 const collidingItems = findCollidingItems(draggingItem.value, newPosition);
 if (collidingItems.length > 0) {
 const movingItem = { ...draggingItem.value, ...newPosition };
 const pushedItems = pushItemsAway(movingItem, collidingItems);
 const finalItems = pushedItems.map(item => item.id === draggingItem.value.id ? { ...item, ...newPosition } : item);
 emit('update:items', finalItems);
 }
 else {
 const updatedItems = props.items.map(item => item.id === draggingItem.value.id ? { ...item, ...newPosition } : item);
 emit('update:items', updatedItems);
 }
 }
 if (resizingItem.value) {
 const deltaX = event.clientX - dragStartPos.value.x;
 const deltaY = event.clientY - dragStartPos.value.y;
 let newWidth = itemStartSize.value.width + deltaX;
 let newHeight = itemStartSize.value.height + deltaY;
 newWidth = snapToGrid(newWidth, props.cellWidth);
 newHeight = snapToGrid(newHeight, props.cellHeight);
 newWidth = Math.max(props.cellWidth, newWidth);
 newHeight = Math.max(props.cellHeight, newHeight);
 newWidth = Math.min(newWidth, props.containerWidth - resizingItem.value.x);
 newHeight = Math.min(newHeight, props.containerHeight - resizingItem.value.y);
 const updatedItems = props.items.map(item => item.id === resizingItem.value.id
 ? { ...item, width: newWidth, height: newHeight }
 : item);
 emit('update:items', updatedItems);
 emit('item-resized', resizingItem.value);
 }
};
const handleMouseUp = () => {
 if (draggingItem.value) {
 emit('item-moved', draggingItem.value);
 const compacted = compactItemsUp();
 emit('update:items', compacted);
 }
 draggingItem.value = null;
 resizingItem.value = null;
 dragPreview.value = null;
};
onMounted(() => {
 const compacted = compactItemsUp();
 if (JSON.stringify(compacted) !== JSON.stringify(props.items)) {
 emit('update:items', compacted);
 }
});
</script>

<style scoped>
.grid-layout-wrapper {
  display: inline-block;
}

.grid-layout-container {
  position: relative;
  background: var(--gray-50);
  border: 2px solid var(--gray-200);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: default;
}

.grid-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.grid-cell {
  position: absolute;
  border: 1px dashed var(--gray-200);
  box-sizing: border-box;
}

.grid-item {
  position: absolute;
  background: white;
  border: 2px solid var(--gray-300);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow);
  cursor: move;
  transition: box-shadow 0.2s, border-color 0.2s;
  overflow: hidden;
}

.grid-item:hover {
  border-color: var(--primary);
  box-shadow: var(--shadow-lg);
}

.grid-item-dragging {
  opacity: 0.9;
  box-shadow: var(--shadow-xl);
  border-color: var(--primary);
  z-index: 1000;
}

.grid-item-resizing {
  opacity: 0.9;
}

.grid-item-content {
  width: 100%;
  height: 100%;
  padding: var(--space-md);
  box-sizing: border-box;
  overflow: auto;
}

.resize-handle {
  position: absolute;
  width: 12px;
  height: 12px;
  background: var(--primary);
  border-radius: 2px;
}

.resize-handle-se {
  right: -6px;
  bottom: -6px;
  cursor: se-resize;
}

.resize-handle-se:hover {
  background: var(--primary-dark);
}

.drag-preview {
  position: absolute;
  border: 2px dashed var(--primary);
  background: rgba(37, 99, 235, 0.1);
  border-radius: var(--radius-md);
  pointer-events: none;
  z-index: 999;
}
</style>
