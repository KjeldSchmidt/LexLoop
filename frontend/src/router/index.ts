import { createRouter, createWebHistory } from 'vue-router'
import UserStartPage from '@/pages/UserStartPage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import StartPage from '@/pages/StartPage.vue'
import TagPage from '@/pages/TagPage.vue'
import NodePage from '@/pages/NodePage.vue'
import ClassOverviewPage from '@/pages/ClassOverviewPage.vue'
import TeacherStudentsPage from '@/pages/TeacherStudentsPage.vue'
import TeacherCourseSettingsPage from '@/pages/TeacherCourseSettingsPage.vue'
import OAuthPopupDonePage from '@/pages/OAuthPopupDonePage.vue'
import { useAuthStore } from '@/stores/auth'
import { safeRedirectPath } from '@/router/authRedirect'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/node/:id',
      name: 'NodePage',
      component: NodePage,
      meta: { requiresAuth: true },
    },
    {
      path: '/tag/:id',
      name: 'TagPage',
      component: TagPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/class/:id',
      name: 'ClassOverview',
      component: ClassOverviewPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/user-start',
      component: UserStartPage,
      meta: { requiresAuth: true },
    },
    {
      path: '/teacher/students',
      component: TeacherStudentsPage,
      meta: { requiresAuth: 'teacher' },
    },
    {
      path: '/teacher/courses/:id',
      name: 'TeacherCourseSettings',
      component: TeacherCourseSettingsPage,
      meta: { requiresAuth: 'teacher' },
    },
    { path: '/oauth/popup-done', component: OAuthPopupDonePage },
    { path: '/login', name: 'Login', component: LoginPage },
    { path: '/', component: StartPage },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  await auth.ensureSession()

  if (to.name === 'Login' && auth.isAuthenticated) {
    return safeRedirectPath(to.query.redirect)
  }

  const requirement = to.meta.requiresAuth
  if (!requirement) {
    return true
  }

  const roleOk =
    requirement === true
      ? auth.isAuthenticated
      : requirement === 'teacher'
        ? auth.isTeacher
        : auth.isStudent

  if (roleOk) {
    return true
  }

  return {
    name: 'Login',
    query: {
      redirect: safeRedirectPath(to.fullPath),
      reason: 'auth',
    },
  }
})

export default router
