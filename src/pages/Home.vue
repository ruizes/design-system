<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <div class="hero-content fade-in">
          <h1 class="hero-title">在线业务展示设计系统</h1>
          <p class="hero-subtitle">统一的视觉设计规范、交互模式、组件库及样式指南</p>
          <div class="hero-actions">
            <router-link to="/components" class="btn btn-primary btn-lg">查看组件库</router-link>
            <router-link to="/products" class="btn btn-outline btn-lg">浏览产品</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <div class="container">
        <h2 class="section-title text-center">核心特性</h2>
        <div class="grid grid-3">
          <div class="card feature-card fade-in" style="animation-delay: 0.1s">
            <div class="feature-icon">🎨</div>
            <h3>统一设计规范</h3>
            <p>完整的设计令牌系统，包含配色、字体、间距等规范</p>
          </div>
          <div class="card feature-card fade-in" style="animation-delay: 0.2s">
            <div class="feature-icon">📱</div>
            <h3>响应式布局</h3>
            <p>支持桌面端、平板及移动端，确保各设备良好展示</p>
          </div>
          <div class="card feature-card fade-in" style="animation-delay: 0.3s">
            <div class="feature-icon">⚡</div>
            <h3>高性能组件</h3>
            <p>轻量级组件库，快速加载，流畅交互体验</p>
          </div>
          <div class="card feature-card fade-in" style="animation-delay: 0.4s">
            <div class="feature-icon">🔧</div>
            <h3>易于使用</h3>
            <p>清晰的文档和代码示例，快速上手</p>
          </div>
          <div class="card feature-card fade-in" style="animation-delay: 0.5s">
            <div class="feature-icon">📚</div>
            <h3>业务组件</h3>
            <p>丰富的业务场景组件，满足各类需求</p>
          </div>
          <div class="card feature-card fade-in" style="animation-delay: 0.6s">
            <div class="feature-icon">✨</div>
            <h3>现代化设计</h3>
            <p>简洁协调的视觉风格，未来感十足</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats">
      <div class="container">
        <div class="grid grid-4">
          <div class="stat-card">
            <div class="stat-value">50+</div>
            <div class="stat-label">组件数量</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">100%</div>
            <div class="stat-label">响应式</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">10KB</div>
            <div class="stat-label">核心大小</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">99%</div>
            <div class="stat-label">满意度</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta">
      <div class="container">
        <div class="cta-content">
          <h2>开始使用设计系统</h2>
          <p>立即体验完整的组件库和设计规范</p>
          <router-link to="/components" class="btn btn-primary btn-lg">立即开始</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero {
  padding: var(--space-3xl) 0;
  text-align: center;
}

.hero-title {
  font-size: var(--text-5xl);
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: var(--space-lg);
}

.hero-subtitle {
  font-size: var(--text-xl);
  color: var(--gray-600);
  margin-bottom: var(--space-2xl);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.hero-actions {
  display: flex;
  gap: var(--space-lg);
  justify-content: center;
  flex-wrap: wrap;
}

.features {
  padding: var(--space-3xl) 0;
}

.section-title {
  font-size: var(--text-4xl);
  font-weight: 700;
  margin-bottom: var(--space-2xl);
  color: var(--gray-900);
}

.feature-card {
  text-align: center;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: var(--space-lg);
}

.feature-card h3 {
  font-size: var(--text-xl);
  margin-bottom: var(--space-md);
  color: var(--gray-900);
}

.feature-card p {
  color: var(--gray-600);
  line-height: 1.6;
}

.stats {
  padding: var(--space-3xl) 0;
  background: white;
}

.stat-card {
  text-align: center;
  padding: var(--space-xl);
}

.stat-value {
  font-size: var(--text-4xl);
  font-weight: 700;
  color: var(--primary);
  margin-bottom: var(--space-sm);
}

.stat-label {
  font-size: var(--text-lg);
  color: var(--gray-600);
}

.cta {
  padding: var(--space-3xl) 0;
}

.cta-content {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  padding: var(--space-3xl);
  border-radius: var(--radius-xl);
  text-align: center;
}

.cta-content h2 {
  font-size: var(--text-4xl);
  margin-bottom: var(--space-md);
}

.cta-content p {
  font-size: var(--text-xl);
  margin-bottom: var(--space-2xl);
  opacity: 0.9;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: var(--text-3xl);
  }
  
  .hero-subtitle {
    font-size: var(--text-lg);
  }
  
  .hero-actions {
    flex-direction: column;
  }
}
</style>
