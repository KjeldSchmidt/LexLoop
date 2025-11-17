import { createRouter, createWebHistory } from 'vue-router'
import UserStartPage from '@/pages/UserStartPage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import StartPage from '@/pages/StartPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/user-start', component: UserStartPage },
    { path: '/login', component: LoginPage },
    { path: '/', component: StartPage },
  ],
})

export default router
