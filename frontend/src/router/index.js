import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import ManageGroup from '../components/ManageGroup.vue'
import ManageGame from '../components/ManageGame.vue'
import store from '../store'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/manage-group',
    name: 'ManageGroup',
    component: ManageGroup,
    meta: { requiresAuth: true }
  },
  {
    path: '/manage-game',
    name: 'ManageGame',
    component: ManageGame,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.isLoggedIn) {
      next('/')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router