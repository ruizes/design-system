<template>
  <div class="home-page">
    <div class="container">
      <div class="hero">
        <h1>设计系统组件库</h1>
        <p class="subtitle">GridLayout 可拖拽网格布局 + GanttChart 甘特图组件</p>
        <router-link to="/components" class="btn btn-primary btn-lg">查看组件演示</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
}

.hero {
  text-align: center;
  padding: var(--space-3xl);
}

.hero h1 {
  font-size: var(--text-5xl);
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: var(--space-lg);
}

.subtitle {
  font-size: var(--text-xl);
  color: var(--gray-600);
  margin-bottom: var(--space-2xl);
}
</style>
