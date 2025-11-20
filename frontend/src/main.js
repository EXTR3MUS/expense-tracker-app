import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './views/Home.vue'
import Categories from './views/Categories.vue'
import Expenses from './views/Expenses.vue'
import Statistics from './views/Statistics.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/categories', component: Categories },
  { path: '/expenses', component: Expenses },
  { path: '/statistics', component: Statistics }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
