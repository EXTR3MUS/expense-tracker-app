import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import RouterApp from './RouterApp.vue'
import App from './App.vue'
import AuditLogs from './views/AuditLogs.vue'
import Unauthorized from './views/Unauthorized.vue'

console.log('Main.js loading...')

const routes = [
  { path: '/', name: 'home', component: App },
  { path: '/audit', name: 'audit', component: AuditLogs },
  { path: '/unauthorized', name: 'unauthorized', component: Unauthorized }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  console.log('Navigating from', from.path, 'to', to.path)
  next()
})

const app = createApp(RouterApp)
app.use(router)
app.mount('#app')

console.log('App mounted with router')
