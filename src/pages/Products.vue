<template>
  <div class="products-page">
    <div class="container">
      <div class="page-header">
        <h1>产品展示</h1>
        <p>探索我们的优质产品和服务</p>
      </div>

      <!-- 搜索和筛选区域 -->
      <div class="filter-section">
        <div class="search-box">
          <input 
            type="text" 
            class="input" 
            v-model="searchQuery" 
            placeholder="搜索产品..."
          >
        </div>
        <div class="filter-buttons">
          <button 
            class="btn" 
            :class="selectedCategory === '' ? 'btn-primary' : 'btn-outline'"
            @click="selectCategory('')"
          >
            全部
          </button>
          <button 
            v-for="category in categories" 
            :key="category"
            class="btn" 
            :class="selectedCategory === category ? 'btn-primary' : 'btn-outline'"
            @click="selectCategory(category)"
          >
            {{ category }}
          </button>
        </div>
      </div>

      <div class="grid grid-3">
        <div class="card product-card" v-for="product in filteredProducts" :key="product.id">
          <div class="product-image">{{ product.icon }}</div>
          <span class="badge badge-primary">{{ product.category }}</span>
          <h3>{{ product.name }}</h3>
          <p>{{ product.description }}</p>
          <div class="product-price">¥{{ product.price }}</div>
          <div class="product-actions">
            <button class="btn btn-primary btn-sm" @click="viewProduct(product)">查看详情</button>
            <button class="btn btn-outline btn-sm" @click="addToCart(product)">加入购物车</button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="filteredProducts.length === 0" class="empty-state">
        <div class="empty-icon">🔍</div>
        <h3>未找到产品</h3>
        <p>尝试使用其他关键词或筛选条件</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const products = ref([
  {
    id: 1,
    name: '企业版设计系统',
    description: '完整的企业级设计系统解决方案，包含所有组件和模板',
    price: '9,999',
    category: '企业版',
    icon: '🔫'
  },
  {
    id: 2,
    name: '专业版组件库',
    description: '专业级组件库，适合中小型项目快速开发',
    price: '4,999',
    category: '专业版',
    icon: '📦'
  },
  {
    id: 3,
    name: '基础版模板',
    description: '包含基础组件和页面模板，适合个人开发者',
    price: '1,999',
    category: '基础版',
    icon: '🆕'
  },
  {
    id: 4,
    name: 'UI设计资源包',
    description: '完整的UI设计资源，包含Figma和Sketch文件',
    price: '2,999',
    category: '设计资源',
    icon: '🎒'
  },
  {
    id: 5,
    name: '技术支持服务',
    description: '一对一技术支持，帮助您快速解决问题',
    price: '3,999',
    category: '服务',
    icon: '🛠️'
  },
  {
    id: 6,
    name: '定制开发服务',
    description: '根据您的需求定制专属的设计系统',
    price: '19,999',
    category: '定制',
    icon: '😊'
  }
])

// 搜索和筛选状态
const searchQuery = ref('')
const selectedCategory = ref('')

// 获取所有分类
const categories = computed(() => {
  return [...new Set(products.value.map(p => p.category))]
})

// 筛选后的产品
const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = selectedCategory.value === '' || product.category === selectedCategory.value
    return matchesSearch && matchesCategory
  })
})

// 选择分类
const selectCategory = (category) => {
  selectedCategory.value = category
}

// 查看产品详情
const viewProduct = (product) => {
  alert(`查看产品: ${product.name}\n\n${product.description}\n\n价格: ¥${product.price}`)
}

// 加入购物车
const addToCart = (product) => {
  alert(`已将 "${product.name}" 加入购物车！\n价格: ¥${product.price}`)
}
</script>

<style scoped>
.products-page {
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

.filter-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
  margin-bottom: var(--space-2xl);
  padding: var(--space-xl);
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
}

.search-box {
  max-width: 400px;
}

.filter-buttons {
  display: flex;
  gap: var(--space-sm);
  flex-wrap: wrap;
}

.product-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.product-image {
  font-size: 4rem;
  text-align: center;
  padding: var(--space-xl);
  background: var(--gray-50);
  border-radius: var(--radius-md);
}

.product-card h3 {
  font-size: var(--text-xl);
  color: var(--gray-900);
}

.product-card p {
  color: var(--gray-600);
  line-height: 1.6;
  flex-grow: 1;
}

.product-price {
  font-size: var(--text-2xl);
  font-weight: 700;
  color: var(--primary);
}

.product-actions {
  display: flex;
  gap: var(--space-sm);
  flex-direction: column;
}

.empty-state {
  text-align: center;
  padding: var(--space-3xl);
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: var(--space-lg);
}

.empty-state h3 {
  font-size: var(--text-xl);
  color: var(--gray-900);
  margin-bottom: var(--space-md);
}

.empty-state p {
  color: var(--gray-600);
}

@media (min-width: 768px) {
  .filter-section {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }

  .product-actions {
    flex-direction: row;
  }
}
</style>
