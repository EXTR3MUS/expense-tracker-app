import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import AuditLogs from './views/AuditLogs.vue'
import Unauthorized from './views/Unauthorized.vue'

const routes = [
  { path: '/', name: 'home', component: App },
  { path: '/audit', name: 'audit', component: AuditLogs },
  { path: '/unauthorized', name: 'unauthorized', component: Unauthorized }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
