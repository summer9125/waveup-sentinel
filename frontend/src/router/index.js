import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Events from '../views/Events.vue'
import Analysis from '../views/Analysis.vue'
import Alerts from '../views/Alerts.vue'
import Settings from '../views/Settings.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/events', name: 'Events', component: Events },
  { path: '/analysis', name: 'Analysis', component: Analysis },
  { path: '/alerts', name: 'Alerts', component: Alerts },
  { path: '/settings', name: 'Settings', component: Settings }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
