<template>
  <div id="app">
    <nav class="navbar">
      <div class="container">
        <div class="nav-content">
          <router-link to="/" class="logo">
            <span class="logo-icon">🎨</span>
            <span class="logo-text">组件库</span>
          </router-link>
          <ul class="nav-links">
            <li><router-link to="/" class="nav-link">首页</router-link></li>
            <li><router-link to="/components" class="nav-link">组件演示</router-link></li>
          </ul>
        </div>
      </div>
    </nav>
    
    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.navbar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-lg) 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  text-decoration: none;
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--gray-900);
}

.logo-icon {
  font-size: var(--text-2xl);
}

.nav-links {
  display: flex;
  gap: var(--space-xl);
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-link {
  text-decoration: none;
  color: var(--gray-600);
  font-weight: 500;
  transition: var(--transition);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--primary);
  background: rgba(37, 99, 235, 0.1);
}

main {
  min-height: calc(100vh - 100px);
}

@media (max-width: 768px) {
  .nav-content {
    flex-direction: column;
    gap: var(--space-sm);
    padding: var(--space-md) 0;
  }
  
  .nav-links {
    justify-content: center;
    gap: var(--space-sm);
    width: 100%;
  }
}
</style>
