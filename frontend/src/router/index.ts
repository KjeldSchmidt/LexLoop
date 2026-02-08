import { createRouter, createWebHistory } from 'vue-router'
import UserStartPage from '@/pages/UserStartPage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import StartPage from '@/pages/StartPage.vue'
import TagPage from '@/pages/TagPage.vue'
import NodePage from '@/pages/NodePage.vue'
import ClassOverviewPage from '@/pages/ClassOverviewPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/node/:id', name: 'NodePage', component: NodePage },
    { path: '/tag/:id', name: 'TagPage', component: TagPage },
    { path: '/class/:id', name: 'ClassOverview', component: ClassOverviewPage },
    { path: '/user-start', component: UserStartPage },
    { path: '/login', component: LoginPage },
    { path: '/', component: StartPage },
  ],
})

export default router
