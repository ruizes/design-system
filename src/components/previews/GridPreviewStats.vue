<template>
  <div class="preview-stats">
    <div class="stats-grid">
      <div class="stat-item" v-for="(stat, index) in config.items" :key="index">
        <div class="stat-value">{{ stat.value }}</div>
        <div class="stat-label">{{ stat.label }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  config: {
    type: Object,
    default: () => ({
      items: [
        { value: '1,234', label: '用户数' },
        { value: '567', label: '订单数' },
        { value: '89%', label: '满意度' }
      ]
    })
  }
})
</script>

<style scoped>
.preview-stats {
  width: 100%;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
  gap: var(--space-md);
}

.stat-item {
  text-align: center;
  padding: var(--space-md);
  background: var(--gray-50);
  border-radius: var(--radius-md);
}

.stat-value {
  font-size: var(--text-2xl);
  font-weight: 700;
  color: var(--primary);
  margin-bottom: var(--space-xs);
}

.stat-label {
  font-size: var(--text-sm);
  color: var(--gray-600);
}
</style>
