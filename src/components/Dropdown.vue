<template>
  <div class="dropdown" ref="dropdownRef">
    <button class="dropdown-trigger" @click="toggle" :class="triggerClass">
      <slot name="trigger">
        {{ triggerText }}
        <svg class="dropdown-arrow" :class="{ 'rotated': visible }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="6 9 12 15 18 9"></polyline>
        </svg>
      </slot>
    </button>
    
    <Transition name="dropdown">
      <div v-if="visible" class="dropdown-menu" :class="[placementClass, { 'dropdown-menu-fullwidth': fullwidth }]">
        <slot></slot>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  triggerText: {
    type: String,
    default: '下拉菜单'
  },
  placement: {
    type: String,
    default: 'bottom',
    validator: (val) => ['bottom', 'bottom-left', 'bottom-right', 'top', 'top-left', 'top-right'].includes(val)
  },
  fullwidth: {
    type: Boolean,
    default: false
  },
  triggerClass: {
    type: String,
    default: 'btn btn-outline'
  }
})

const emit = defineEmits(['open', 'close'])

const visible = ref(false)
const dropdownRef = ref(null)

const placementClass = {
  'bottom': 'dropdown-menu-bottom',
  'bottom-left': 'dropdown-menu-bottom-left',
  'bottom-right': 'dropdown-menu-bottom-right',
  'top': 'dropdown-menu-top',
  'top-left': 'dropdown-menu-top-left',
  'top-right': 'dropdown-menu-top-right'
}[props.placement]

const toggle = () => {
  visible.value = !visible.value
  if (visible.value) {
    emit('open')
  } else {
    emit('close')
  }
}

const close = () => {
  visible.value = false
  emit('close')
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    close()
  }
}

const handleKeydown = (event) => {
  if (event.key === 'Escape') {
    close()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
})

defineExpose({
  open: () => {
    visible.value = true
    emit('open')
  },
  close,
  toggle
})
</script>

<style scoped>
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-trigger {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.dropdown-arrow {
  transition: transform 0.2s ease;
}

.dropdown-arrow.rotated {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  min-width: 200px;
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: var(--space-sm) 0;
  z-index: 100;
  animation: dropdownIn 0.2s ease-out;
}

.dropdown-menu-fullwidth {
  width: 100%;
}

.dropdown-menu-bottom {
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-top: var(--space-sm);
}

.dropdown-menu-bottom-left {
  top: 100%;
  left: 0;
  margin-top: var(--space-sm);
}

.dropdown-menu-bottom-right {
  top: 100%;
  right: 0;
  margin-top: var(--space-sm);
}

.dropdown-menu-top {
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: var(--space-sm);
}

.dropdown-menu-top-left {
  bottom: 100%;
  left: 0;
  margin-bottom: var(--space-sm);
}

.dropdown-menu-top-right {
  bottom: 100%;
  right: 0;
  margin-bottom: var(--space-sm);
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@keyframes dropdownIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
