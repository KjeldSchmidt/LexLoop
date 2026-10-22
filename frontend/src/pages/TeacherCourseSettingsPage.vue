<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  deleteCourse,
  enrollStudents,
  getCourse,
  getCourseStudents,
  getStudents,
  unenrollStudents,
  updateCourse,
} from '@/api'
import type { components } from '@/api/schema.ts'

type Course = components['schemas']['CourseOut']
type Student = components['schemas']['StudentOut']

const route = useRoute()
const router = useRouter()
const courseId = route.params.id as string

const course = ref<Course | null>(null)
const name = ref('')
const description = ref('')
const allStudents = ref<Student[]>([])
const enrolledIds = ref<Set<string>>(new Set())
const busy = ref(false)
const error = ref('')
const savedFlash = ref(false)

const enrolled = computed(() => allStudents.value.filter((s) => enrolledIds.value.has(s.uuid)))
const available = computed(() => allStudents.value.filter((s) => !enrolledIds.value.has(s.uuid)))

async function load() {
  error.value = ''
  try {
    const [courseRes, enrolledRes, studentsRes] = await Promise.all([
      getCourse(courseId),
      getCourseStudents(courseId),
      getStudents(),
    ])
    course.value = courseRes
    name.value = courseRes.name
    description.value = courseRes.description
    enrolledIds.value = new Set(enrolledRes.map((s) => s.uuid))
    allStudents.value = studentsRes ?? []
  } catch {
    error.value = 'Could not load course'
  }
}

onMounted(load)

async function onSave() {
  error.value = ''
  busy.value = true
  savedFlash.value = false
  try {
    course.value = await updateCourse(courseId, {
      name: name.value,
      description: description.value,
    })
    savedFlash.value = true
  } catch {
    error.value = 'Could not save course'
  } finally {
    busy.value = false
  }
}

async function onDelete() {
  if (
    !window.confirm(
      `Delete “${name.value}” and all of its words, tags, and links? This cannot be undone.`,
    )
  ) {
    return
  }
  error.value = ''
  busy.value = true
  try {
    await deleteCourse(courseId)
    await router.push('/user-start')
  } catch {
    error.value = 'Could not delete course'
    busy.value = false
  }
}

async function enroll(studentUuid: string) {
  error.value = ''
  busy.value = true
  try {
    await enrollStudents(courseId, [studentUuid])
    enrolledIds.value = new Set([...enrolledIds.value, studentUuid])
  } catch {
    error.value = 'Could not enroll student'
  } finally {
    busy.value = false
  }
}

async function unenroll(studentUuid: string) {
  error.value = ''
  busy.value = true
  try {
    await unenrollStudents(courseId, [studentUuid])
    const next = new Set(enrolledIds.value)
    next.delete(studentUuid)
    enrolledIds.value = next
  } catch {
    error.value = 'Could not remove student'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="settings">
    <header class="page-header">
      <div>
        <p class="eyebrow">Teacher tools</p>
        <h1>Course settings</h1>
        <p class="ll-muted">Edit details, enroll students, or delete this course.</p>
      </div>
      <router-link class="ll-btn ll-btn-ghost" to="/user-start">← Courses</router-link>
    </header>

    <p v-if="error" class="ll-error">{{ error }}</p>

    <form class="ll-panel" @submit.prevent="onSave">
      <h2>Details</h2>
      <label class="ll-field">
        Name
        <input v-model="name" required maxlength="100" />
      </label>
      <label class="ll-field">
        Description
        <textarea v-model="description" rows="3" class="ll-input" />
      </label>
      <div class="row-actions">
        <button type="submit" class="ll-btn ll-btn-primary" :disabled="busy">
          {{ busy ? 'Saving…' : 'Save' }}
        </button>
        <span v-if="savedFlash" class="ll-muted saved">Saved</span>
      </div>
    </form>

    <section class="ll-panel">
      <h2>Enrolled ({{ enrolled.length }})</h2>
      <ul v-if="enrolled.length" class="student-list">
        <li v-for="s in enrolled" :key="s.uuid" class="student-row">
          <span>{{ s.username }}</span>
          <button
            type="button"
            class="ll-btn ll-btn-ghost"
            :disabled="busy"
            @click="unenroll(s.uuid)"
          >
            Remove
          </button>
        </li>
      </ul>
      <p v-else class="ll-muted">No students enrolled yet.</p>
    </section>

    <section class="ll-panel">
      <h2>Add students</h2>
      <ul v-if="available.length" class="student-list">
        <li v-for="s in available" :key="s.uuid" class="student-row">
          <span>{{ s.username }}</span>
          <button type="button" class="ll-btn" :disabled="busy" @click="enroll(s.uuid)">
            Enroll
          </button>
        </li>
      </ul>
      <p v-else class="ll-muted">
        All of your students are enrolled, or you have not created any yet.
        <router-link to="/teacher/students">Manage students</router-link>
      </p>
    </section>

    <section class="ll-panel danger-zone">
      <h2>Delete course</h2>
      <p class="ll-muted">Permanently removes this course and all of its vocabulary content.</p>
      <button type="button" class="ll-btn ll-btn-danger" :disabled="busy" @click="onDelete">
        Delete course
      </button>
    </section>
  </div>
</template>

<style scoped>
.settings {
  width: min(100% - 2rem, 42rem);
  margin: 0 auto;
  padding: var(--ll-space-page) 0 3rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.page-header {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
}

.page-header > div {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.eyebrow {
  margin: 0;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--ll-accent);
}

.ll-panel {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.row-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.saved {
  font-size: 0.9rem;
}

.student-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.student-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.45rem 0.55rem;
  border-radius: var(--ll-radius);
  border: 1px solid transparent;
}

.student-row:hover {
  background: var(--ll-paper);
  border-color: var(--ll-border);
}

textarea.ll-input {
  resize: vertical;
  min-height: 4.5rem;
}

.danger-zone {
  border-color: color-mix(in srgb, var(--ll-danger) 35%, var(--ll-border));
}
</style>
