import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './styles/main.css'

// 导入页面
import Home from './pages/Home.vue'
import Components from './pages/Components.vue'
import Products from './pages/Products.vue'
import About from './pages/About.vue'

const routes = [
    { path: '/', component: Home },
    { path: '/components', component: Components },
    { path: '/products', component: Products },
    { path: '/about', component: About }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

createApp(App).use(router).mount('#app')
