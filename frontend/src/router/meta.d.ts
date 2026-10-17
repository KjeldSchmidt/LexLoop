import 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    /**
     * true — any authenticated principal (teacher or student)
     * 'teacher' / 'student' — that role only
     */
    requiresAuth?: boolean | 'teacher' | 'student'
  }
}
