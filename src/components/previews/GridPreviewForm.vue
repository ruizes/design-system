<template>
  <div class="preview-form">
    <h4 v-if="config.title" class="form-title">{{ config.title }}</h4>
    <div class="form-fields">
      <div class="form-group" v-for="(field, index) in config.fields" :key="index">
        <label class="form-label">{{ field.label }}</label>
        <input 
          v-if="field.type !== 'textarea'"
          :type="field.type || 'text'"
          class="input"
          :placeholder="field.placeholder"
          disabled
        />
        <textarea 
          v-else
          class="input"
          :placeholder="field.placeholder"
          rows="2"
          disabled
        ></textarea>
      </div>
    </div>
    <div class="form-actions">
      <button class="btn btn-primary btn-sm">提交</button>
      <button class="btn btn-outline btn-sm">重置</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  config: {
    type: Object,
    default: () => ({
      title: '表单',
      fields: [
        { type: 'text', label: '姓名', placeholder: '请输入姓名' },
        { type: 'email', label: '邮箱', placeholder: '请输入邮箱' }
      ]
    })
  }
})
</script>

<style scoped>
.preview-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.form-title {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--gray-900);
  margin: 0;
}

.form-fields {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.form-label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--gray-700);
}

.input {
  padding: var(--space-sm) var(--space-md);
  font-size: var(--text-sm);
}

.form-actions {
  display: flex;
  gap: var(--space-sm);
}
</style>
