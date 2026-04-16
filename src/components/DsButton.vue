<template>
  <component
    :is="tag"
    :class="buttonClasses"
    :disabled="isDisabled || loading"
    :type="tag === 'button' ? nativeType : undefined"
    :href="tag === 'a' ? href : undefined"
    @click="handleClick"
  >
    <span v-if="loading" class="btn-spinner"></span>
    <span v-else-if="icon && !iconRight" class="btn-icon-content">{{ icon }}</span>
    <span v-if="$slots.default && !loading" class="btn-text">
      <slot></slot>
    </span>
    <span v-if="iconRight && !loading" class="btn-icon-content">{{ iconRight }}</span>
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => {
      return ['primary', 'secondary', 'outline', 'text', 'ghost', 'danger', 'success', 'warning'].includes(value)
    }
  },
  size: {
    type: String,
    default: 'default',
    validator: (value) => {
      return ['sm', 'default', 'lg'].includes(value)
    }
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  icon: {
    type: String,
    default: null
  },
  iconRight: {
    type: String,
    default: null
  },
  block: {
    type: Boolean,
    default: false
  },
  circle: {
    type: Boolean,
    default: false
  },
  tag: {
    type: String,
    default: 'button',
    validator: (value) => {
      return ['button', 'a', 'router-link'].includes(value)
    }
  },
  nativeType: {
    type: String,
    default: 'button',
    validator: (value) => {
      return ['button', 'submit', 'reset'].includes(value)
    }
  },
  href: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['click'])

const isDisabled = computed(() => props.disabled || props.loading)

const buttonClasses = computed(() => {
  const classes = ['btn']
  
  switch (props.variant) {
    case 'primary':
      classes.push('btn-primary')
      break
    case 'secondary':
      classes.push('btn-secondary')
      break
    case 'outline':
      classes.push('btn-outline')
      break
    case 'text':
      classes.push('btn-text')
      break
    case 'ghost':
      classes.push('btn-ghost')
      break
    case 'danger':
      classes.push('btn-danger')
      break
    case 'success':
      classes.push('btn-success')
      break
    case 'warning':
      classes.push('btn-warning')
      break
  }
  
  if (props.size === 'sm') {
    classes.push('btn-sm')
  } else if (props.size === 'lg') {
    classes.push('btn-lg')
  }
  
  if (props.block) {
    classes.push('btn-block')
  }
  
  if (props.circle) {
    classes.push('btn-circle')
  }
  
  if (props.icon && !props.$slots?.default) {
    classes.push('btn-icon')
  }
  
  if (props.loading) {
    classes.push('btn-loading')
  }
  
  if (props.disabled) {
    classes.push('btn-disabled')
  }
  
  return classes
})

const handleClick = (event) => {
  if (!isDisabled.value) {
    emit('click', event)
  }
}
</script>

<style scoped>
.btn-spinner {
  margin-right: var(--space-sm);
}

.btn-icon + .btn-text,
.btn-text + .btn-icon-content {
  margin-left: var(--space-sm);
}
</style>
