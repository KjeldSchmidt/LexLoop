import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { getStudentMe, getTeacherMe, studentLogout, teacherLogout } from '@/api'
import type { components } from '@/api/schema.ts'

type Teacher = components['schemas']['UserRead']
type Student = components['schemas']['StudentOut']
export type AuthKind = 'teacher' | 'student'

export const useAuthStore = defineStore('auth', () => {
  const kind = ref<AuthKind | null>(null)
  const teacher = ref<Teacher | null>(null)
  const student = ref<Student | null>(null)
  const ready = ref(false)
  let inflight: Promise<void> | null = null

  const isAuthenticated = computed(() => kind.value !== null)
  const isTeacher = computed(() => kind.value === 'teacher')
  const isStudent = computed(() => kind.value === 'student')

  async function refreshSession(): Promise<void> {
    if (inflight) {
      await inflight
      return
    }
    inflight = (async () => {
      teacher.value = null
      student.value = null
      kind.value = null
      try {
        const meTeacher = await getTeacherMe()
        if (meTeacher) {
          teacher.value = meTeacher
          kind.value = 'teacher'
          return
        }
        const meStudent = await getStudentMe()
        if (meStudent) {
          student.value = meStudent
          kind.value = 'student'
        }
      } finally {
        ready.value = true
        inflight = null
      }
    })()
    await inflight
  }

  /** Load session once per app boot (or after logout cleared `ready`). */
  async function ensureSession(): Promise<void> {
    if (ready.value) {
      return
    }
    await refreshSession()
  }

  async function logout(): Promise<void> {
    try {
      if (kind.value === 'teacher') {
        await teacherLogout()
      } else if (kind.value === 'student') {
        await studentLogout()
      } else {
        await Promise.allSettled([teacherLogout(), studentLogout()])
      }
    } finally {
      teacher.value = null
      student.value = null
      kind.value = null
      ready.value = true
    }
  }

  return {
    kind,
    teacher,
    student,
    ready,
    isAuthenticated,
    isTeacher,
    isStudent,
    refreshSession,
    ensureSession,
    logout,
  }
})
