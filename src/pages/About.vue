<template>
  <div class="about-page">
    <div class="container">
      <div class="page-header">
        <h1>关于我们</h1>
        <p>致力于打造最优秀的设计系统</p>
      </div>

      <section class="about-content">
        <div class="card">
          <h2>我们的使命</h2>
          <p>我们致力于为开发者和设计师提供一套完整、易用、美观的设计系统，帮助团队快速构建高质量的产品界面。</p>
        </div>

        <div class="card">
          <h2>核心价值</h2>
          <div class="values-grid">
            <div class="value-item">
              <div class="value-icon">🎯</div>
              <h3>专注品质</h3>
              <p>每个组件都经过精心设计和测试</p>
            </div>
            <div class="value-item">
              <div class="value-icon">🚀</div>
              <h3>持续创新</h3>
              <p>不断更新和优化设计系统</p>
            </div>
            <div class="value-item">
              <div class="value-icon">🤝</div>
              <h3>开放协作</h3>
              <p>欢迎社区贡献和反馈</p>
            </div>
          </div>
        </div>

        <div class="card">
          <h2>团队成员</h2>
          <div class="team-grid">
            <div class="team-member" v-for="member in team" :key="member.id">
              <div class="member-avatar">{{ member.avatar }}</div>
              <h3>{{ member.name }}</h3>
              <p class="member-role">{{ member.role }}</p>
              <p>{{ member.bio }}</p>
            </div>
          </div>
        </div>

        <div class="card">
          <h2>联系我们</h2>
          <div class="contact-info">
            <div class="contact-item">
              <strong>📧 邮箱：</strong>
              <span>contact@designsystem.com</span>
            </div>
            <div class="contact-item">
              <strong>🌐 网站：</strong>
              <span>www.designsystem.com</span>
            </div>
            <div class="contact-item">
              <strong>📱 电话：</strong>
              <span>400-123-4567</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const team = ref([
  {
    id: 1,
    name: '张设计',
    role: '首席设计师',
    avatar: '👨‍🎨',
    bio: '10年UI/UX设计经验'
  },
  {
    id: 2,
    name: '李开发',
    role: '技术负责人',
    avatar: '👨‍💻',
    bio: '前端架构专家'
  },
  {
    id: 3,
    name: '王产品',
    role: '产品经理',
    avatar: '👩‍💼',
    bio: '用户体验倡导者'
  }
])
</script>

<style scoped>
.about-page {
  padding: var(--space-3xl) 0;
}

.page-header {
  text-align: center;
  margin-bottom: var(--space-3xl);
}

.page-header h1 {
  font-size: var(--text-4xl);
  font-weight: 700;
  margin-bottom: var(--space-md);
  color: var(--gray-900);
}

.page-header p {
  font-size: var(--text-xl);
  color: var(--gray-600);
}

.about-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-2xl);
}

.about-content .card {
  padding: var(--space-2xl);
}

.about-content h2 {
  font-size: var(--text-2xl);
  margin-bottom: var(--space-lg);
  color: var(--gray-900);
}

.about-content p {
  color: var(--gray-600);
  line-height: 1.8;
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-xl);
  margin-top: var(--space-lg);
}

.value-item {
  text-align: center;
}

.value-icon {
  font-size: 3rem;
  margin-bottom: var(--space-md);
}

.value-item h3 {
  font-size: var(--text-lg);
  margin-bottom: var(--space-sm);
  color: var(--gray-900);
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-xl);
  margin-top: var(--space-lg);
}

.team-member {
  text-align: center;
  padding: var(--space-xl);
  background: var(--gray-50);
  border-radius: var(--radius-lg);
}

.member-avatar {
  font-size: 4rem;
  margin-bottom: var(--space-md);
}

.team-member h3 {
  font-size: var(--text-xl);
  margin-bottom: var(--space-xs);
  color: var(--gray-900);
}

.member-role {
  color: var(--primary);
  font-weight: 600;
  margin-bottom: var(--space-md);
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  margin-top: var(--space-lg);
}

.contact-item {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-md);
  background: var(--gray-50);
  border-radius: var(--radius-md);
}

.contact-item strong {
  color: var(--gray-900);
  min-width: 100px;
}

.contact-item span {
  color: var(--gray-600);
  word-break: break-word;
}

@media (max-width: 768px) {
  .contact-item {
    flex-direction: column;
    gap: var(--space-sm);
  }
  
  .contact-item strong {
    min-width: auto;
  }
}
</style>
