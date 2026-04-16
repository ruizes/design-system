<template>
  <div class="preview-text" :class="`variant-${config.variant}`">
    <h3 v-if="config.title" class="text-title">{{ config.title }}</h3>
    <div v-if="config.content" class="text-content">
      {{ config.content }}
    </div>
  </div>
</template>

<script setup>
defineProps({
  config: {
    type: Object,
    default: () => ({
      title: '标题文本',
      content: '这是一段示例文本内容，可以包含多行文字。',
      variant: 'default'
    })
  }
})
</script>

<style scoped>
.preview-text {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.text-title {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--gray-900);
  margin: 0;
}

.text-content {
  font-size: var(--text-sm);
  color: var(--gray-600);
  line-height: 1.6;
}

.variant-lead .text-content {
  font-size: var(--text-base);
  color: var(--gray-700);
  line-height: 1.8;
}

.variant-quote {
  border-left: 3px solid var(--primary);
  padding-left: var(--space-md);
  font-style: italic;
}

.variant-quote .text-title {
  color: var(--primary);
}
</style>
