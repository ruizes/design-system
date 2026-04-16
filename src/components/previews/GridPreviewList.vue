<template>
  <div class="preview-list">
    <h4 v-if="config.title" class="list-title">{{ config.title }}</h4>
    <ul class="list-items">
      <li v-for="(item, index) in config.items" :key="index" class="list-item">
        <span v-if="item.icon" class="item-icon">{{ item.icon }}</span>
        <span class="item-text">{{ item.text }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  config: {
    type: Object,
    default: () => ({
      title: '列表示例',
      items: [
        { text: '列表项 1', icon: '✨' },
        { text: '列表项 2', icon: '🚀' },
        { text: '列表项 3', icon: '💡' }
      ]
    })
  }
})
</script>

<style scoped>
.preview-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.list-title {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--gray-900);
  margin: 0;
}

.list-items {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.list-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background: var(--gray-50);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  color: var(--gray-700);
}

.item-icon {
  font-size: 1rem;
}

.item-text {
  flex: 1;
}
</style>
