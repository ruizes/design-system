<template>
  <div class="preview-badge">
    <div class="badge-group">
      <span 
        v-for="(badge, index) in config.badges" 
        :key="index"
        class="badge"
        :class="getBadgeClass(badge.variant)"
      >
        {{ badge.text }}
      </span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  config: {
    type: Object,
    default: () => ({
      badges: [
        { text: '默认', variant: 'default' },
        { text: '主要', variant: 'primary' },
        { text: '成功', variant: 'success' },
        { text: '警告', variant: 'warning' }
      ]
    })
  }
})

const getBadgeClass = (variant) => {
  const map = {
    default: '',
    primary: 'badge-primary',
    success: 'badge-success',
    warning: 'badge-warning',
    danger: 'badge-danger',
    info: 'badge-info'
  }
  return map[variant] || ''
}
</script>

<style scoped>
.preview-badge {
  width: 100%;
}

.badge-group {
  display: flex;
  gap: var(--space-sm);
  flex-wrap: wrap;
  justify-content: center;
}

.badge-warning {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning);
}

.badge-danger {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
}

.badge-info {
  background: rgba(59, 130, 246, 0.1);
  color: var(--info);
}
</style>
