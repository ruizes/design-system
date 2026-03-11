<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="modal-overlay" @click.self="handleOverlayClick">
        <div class="modal" :class="[sizeClass, { 'modal-center': center }]">
          <div class="modal-header">
            <slot name="header">
              <h3>{{ title }}</h3>
            </slot>
            <button v-if="closable" class="modal-close" @click="close">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <slot></slot>
          </div>
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: '弹窗标题'
  },
  size: {
    type: String,
    default: 'md',
    validator: (val) => ['sm', 'md', 'lg', 'xl'].includes(val)
  },
  closable: {
    type: Boolean,
    default: true
  },
  center: {
    type: Boolean,
    default: false
  },
  closeOnOverlay: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'close'])

const visible = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  visible.value = val
})

const sizeClass = {
  sm: 'modal-sm',
  md: 'modal-md',
  lg: 'modal-lg',
  xl: 'modal-xl'
}[props.size]

const close = () => {
  visible.value = false
  emit('update:modelValue', false)
  emit('close')
}

const handleOverlayClick = () => {
  if (props.closeOnOverlay) {
    close()
  }
}

defineExpose({
  open: () => {
    visible.value = true
    emit('update:modelValue', true)
  },
  close
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: var(--space-xl);
  z-index: 1000;
  overflow-y: auto;
}

.modal-overlay.modal-center {
  align-items: center;
}

.modal {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  animation: modalIn 0.3s ease-out;
}

.modal-sm {
  max-width: 400px;
}

.modal-md {
  max-width: 600px;
}

.modal-lg {
  max-width: 800px;
}

.modal-xl {
  max-width: 1000px;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-lg) var(--space-xl);
  border-bottom: 1px solid var(--gray-200);
}

.modal-header h3 {
  font-size: var(--text-xl);
  font-weight: 600;
  color: var(--gray-900);
  margin: 0;
}

.modal-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  color: var(--gray-500);
  transition: var(--transition);
}

.modal-close:hover {
  background: var(--gray-100);
  color: var(--gray-700);
}

.modal-body {
  padding: var(--space-xl);
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-md);
  padding: var(--space-lg) var(--space-xl);
  border-top: 1px solid var(--gray-200);
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal,
.modal-leave-active .modal {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal,
.modal-leave-to .modal {
  transform: scale(0.95) translateY(-20px);
}

@keyframes modalIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
</style>
