import { createRouter, createWebHistory } from 'vue-router'
import LoginView from './views/LoginView.vue'
import VaultDashboard from './views/VaultDashboard.vue'
import AdminDashboard from './views/AdminDashboard.vue'

const routes = [
  {
    path: '/login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/vault',
    component: VaultDashboard,
    meta: { requiresAuth: true, requiredRole: 'employee' }
  },
  {
    path: '/admin',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiredRole: 'admin' }
  },
  {
    path: '/',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const userRole = localStorage.getItem('user_role')

  if (to.meta.requiresAuth) {
    if (!token) {
      next('/login')
      return
    }

    if (to.meta.requiredRole && userRole !== to.meta.requiredRole) {
      next('/login')
      return
    }
  }

  next()
})

export default router
