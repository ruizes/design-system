<template>
  <div class="tabs">
    <div class="tabs-nav" :class="{ 'tabs-nav-vertical': vertical }">
      <button
        v-for="(tab, index) in tabs"
        :key="index"
        class="tab-item"
        :class="{
          'tab-active': activeIndex === index,
          'tab-disabled': tab.disabled
        }"
        @click="handleTabClick(index)"
        :disabled="tab.disabled"
      >
        <span v-if="tab.icon" class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-text">{{ tab.label }}</span>
        <span v-if="tab.badge !== undefined" class="tab-badge" :class="getBadgeClass(tab.badgeType)">{{ tab.badge }}</span>
      </button>
    </div>
    <div class="tabs-content">
      <div v-for="(tab, index) in tabs" :key="index" v-show="activeIndex === index">
        <slot :name="'tab-' + index"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  tabs: {
    type: Array,
    required: true,
    validator: (val) => {
      return val.every(tab => typeof tab === 'object' && 'label' in tab)
    }
  },
  modelValue: {
    type: Number,
    default: 0
  },
  vertical: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const activeIndex = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  activeIndex.value = val
})

const handleTabClick = (index) => {
  if (props.tabs[index].disabled) return
  activeIndex.value = index
  emit('update:modelValue', index)
  emit('change', index)
}

const getBadgeClass = (type) => {
  const classes = {
    primary: 'badge-primary',
    success: 'badge-success',
    warning: 'badge-warning',
    error: 'badge-error'
  }
  return classes[type] || ''
}
</script>

<style scoped>
.tabs {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}

.tabs-nav {
  display: flex;
  gap: var(--space-sm);
  border-bottom: 2px solid var(--gray-200);
  overflow-x: auto;
}

.tabs-nav-vertical {
  flex-direction: column;
  border-bottom: none;
  border-right: 2px solid var(--gray-200);
  padding-right: var(--space-lg);
}

.tab-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-md) var(--space-lg);
  font-size: var(--text-base);
  font-weight: 500;
  color: var(--gray-600);
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
  transition: var(--transition);
  white-space: nowrap;
  margin-bottom: -2px;
}

.tabs-nav-vertical .tab-item {
  border-bottom: none;
  border-right: 2px solid transparent;
  margin-bottom: 0;
  margin-right: -2px;
  justify-content: flex-start;
}

.tab-item:hover:not(.tab-disabled):not(.tab-active) {
  color: var(--primary);
  background: rgba(37, 99, 235, 0.05);
}

.tab-item.tab-active {
  color: var(--primary);
  border-bottom-color: var(--primary);
}

.tabs-nav-vertical .tab-item.tab-active {
  border-bottom-color: transparent;
  border-right-color: var(--primary);
}

.tab-item.tab-disabled {
  color: var(--gray-400);
  cursor: not-allowed;
}

.tab-icon {
  font-size: var(--text-lg);
}

.tab-badge {
  padding: var(--space-xs) var(--space-sm);
  font-size: var(--text-xs);
  border-radius: var(--radius-full);
  background: var(--gray-200);
  color: var(--gray-700);
}

.tab-badge.badge-primary {
  background: rgba(37, 99, 235, 0.1);
  color: var(--primary);
}

.tab-badge.badge-success {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success);
}

.tab-badge.badge-warning {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning);
}

.tab-badge.badge-error {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
}

.tabs-content {
  flex: 1;
}

@media (max-width: 768px) {
  .tabs-nav {
    gap: 0;
  }
  
  .tab-item {
    padding: var(--space-sm) var(--space-md);
    font-size: var(--text-sm);
  }
}
</style>
