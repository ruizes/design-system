<template>
  <button
    class="dropdown-item"
    :class="{
      'dropdown-item-active': active,
      'dropdown-item-danger': danger,
      'dropdown-item-disabled': disabled
    }"
    @click="handleClick"
    :disabled="disabled"
  >
    <span v-if="icon" class="dropdown-item-icon">{{ icon }}</span>
    <span class="dropdown-item-text"><slot></slot></span>
    <span v-if="shortcut" class="dropdown-item-shortcut">{{ shortcut }}</span>
  </button>
</template>

<script setup>
const props = defineProps({
  icon: {
    type: String,
    default: ''
  },
  active: {
    type: Boolean,
    default: false
  },
  danger: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  shortcut: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['click'])

const handleClick = () => {
  if (!props.disabled) {
    emit('click')
  }
}
</script>

<style scoped>
.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-sm) var(--space-lg);
  font-size: var(--text-base);
  color: var(--gray-700);
  background: transparent;
  border: none;
  text-align: left;
  cursor: pointer;
  transition: var(--transition-fast);
}

.dropdown-item:hover:not(.dropdown-item-disabled) {
  background: var(--gray-50);
  color: var(--gray-900);
}

.dropdown-item-active {
  background: rgba(37, 99, 235, 0.1) !important;
  color: var(--primary) !important;
}

.dropdown-item-danger {
  color: var(--error);
}

.dropdown-item-danger:hover:not(.dropdown-item-disabled) {
  background: rgba(239, 68, 68, 0.1);
  color: var(--error);
}

.dropdown-item-disabled {
  color: var(--gray-400);
  cursor: not-allowed;
}

.dropdown-item-icon {
  font-size: var(--text-lg);
  width: 20px;
  text-align: center;
}

.dropdown-item-text {
  flex: 1;
}

.dropdown-item-shortcut {
  font-size: var(--text-sm);
  color: var(--gray-400);
  font-family: var(--font-mono);
}
</style>
