<template>
  <div class="preview-image">
    <div class="image-placeholder" :style="placeholderStyle">
      <div class="placeholder-content">
        <span class="placeholder-icon">🖼️</span>
        <span class="placeholder-text">{{ config.alt || '图片占位' }}</span>
        <span class="placeholder-ratio">{{ config.aspectRatio || '16:9' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  config: {
    type: Object,
    default: () => ({
      src: null,
      alt: '图片描述',
      aspectRatio: '16:9'
    })
  }
})

const placeholderStyle = computed(() => {
  const ratio = props.config.aspectRatio || '16:9'
  const [w, h] = ratio.split(':').map(Number)
  return {
    paddingBottom: `${(h / w) * 100}%`
  }
})
</script>

<style scoped>
.preview-image {
  width: 100%;
}

.image-placeholder {
  position: relative;
  width: 100%;
  background: var(--gray-100);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.placeholder-content {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  color: var(--gray-400);
}

.placeholder-icon {
  font-size: 2rem;
}

.placeholder-text {
  font-size: var(--text-sm);
}

.placeholder-ratio {
  font-size: var(--text-xs);
  background: var(--gray-200);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
}
</style>
