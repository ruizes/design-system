<template>
  <div class="preview-card">
    <div v-if="config.category" class="card-badge">
      <span class="badge badge-primary">{{ config.category }}</span>
    </div>
    <h3 class="card-title">{{ config.title }}</h3>
    <p v-if="config.description" class="card-description">{{ config.description }}</p>
    <div v-if="config.price" class="card-price">
      <span class="price-value">{{ config.price }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  config: {
    type: Object,
    default: () => ({
      title: '卡片标题',
      description: '卡片描述内容',
      price: null,
      category: null
    })
  }
})
</script>

<style scoped>
.preview-card {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.card-badge {
  display: flex;
  gap: var(--space-xs);
  flex-wrap: wrap;
}

.card-title {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--gray-900);
  margin: 0;
}

.card-description {
  font-size: var(--text-sm);
  color: var(--gray-600);
  margin: 0;
  line-height: 1.5;
  flex: 1;
}

.card-price {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-top: var(--space-xs);
}

.price-value {
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--primary);
}
</style>
