import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './styles/main.css'

import Home from './pages/Home.vue'
import Components from './pages/Components.vue'

const routes = [
    { path: '/', component: Home },
    { path: '/components', component: Components }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

createApp(App).use(router).mount('#app')
