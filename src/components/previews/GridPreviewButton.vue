<template>
  <div class="preview-button-group">
    <div class="button-row" v-for="(row, rowIndex) in buttonRows" :key="rowIndex">
      <button 
        v-for="(button, btnIndex) in row" 
        :key="btnIndex"
        class="btn"
        :class="getButtonClass(button.variant)"
        :disabled="button.disabled"
      >
        {{ button.text }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  config: {
    type: Object,
    default: () => ({
      buttons: [
        { text: '主要按钮', variant: 'primary' },
        { text: '次要按钮', variant: 'secondary' },
        { text: '边框按钮', variant: 'outline' }
      ]
    })
  }
})

const buttonRows = computed(() => {
  const buttons = props.config.buttons || []
  const rows = []
  const maxPerRow = 3
  
  for (let i = 0; i < buttons.length; i += maxPerRow) {
    rows.push(buttons.slice(i, i + maxPerRow))
  }
  
  return rows
})

const getButtonClass = (variant) => {
  const map = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    outline: 'btn-outline',
    success: 'btn-success',
    warning: 'btn-warning',
    danger: 'btn-danger'
  }
  return map[variant] || 'btn-primary'
}
</script>

<style scoped>
.preview-button-group {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.button-row {
  display: flex;
  gap: var(--space-sm);
  flex-wrap: wrap;
  justify-content: center;
}

.btn {
  padding: var(--space-sm) var(--space-lg);
  font-size: var(--text-sm);
}

.btn-success {
  background: linear-gradient(135deg, var(--success), #059669);
  color: white;
}

.btn-warning {
  background: linear-gradient(135deg, var(--warning), #d97706);
  color: white;
}

.btn-danger {
  background: linear-gradient(135deg, var(--error), #dc2626);
  color: white;
}
</style>
