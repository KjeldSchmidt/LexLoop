<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { createCourse, getCourses } from '@/api'
import type { components } from '@/api/schema.ts'
import { useAuthStore } from '@/stores/auth'

type Course = components['schemas']['CourseOut']

const router = useRouter()
const auth = useAuthStore()
const { isTeacher } = storeToRefs(auth)
const courses = ref<Course[]>([])
const showCreate = ref(false)
const newName = ref('')
const newDescription = ref('')
const busy = ref(false)
const error = ref('')

async function refresh() {
  const coursesRes = await getCourses()
  if (coursesRes?.items) {
    courses.value = coursesRes.items
  }
}

onMounted(refresh)

function goToClass(course_uuid: string) {
  router.push({
    name: 'ClassOverview',
    params: { id: course_uuid },
  })
}

function goToSettings(course_uuid: string, event: Event) {
  event.stopPropagation()
  router.push({
    name: 'TeacherCourseSettings',
    params: { id: course_uuid },
  })
}

async function onCreate() {
  error.value = ''
  busy.value = true
  try {
    const created = await createCourse(newName.value.trim(), newDescription.value.trim())
    newName.value = ''
    newDescription.value = ''
    showCreate.value = false
    await refresh()
    await router.push({
      name: 'TeacherCourseSettings',
      params: { id: created.uuid },
    })
  } catch {
    error.value = 'Could not create course'
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="user-start">
    <header class="page-header">
      <div>
        <p class="eyebrow">Your workspace</p>
        <h1>Choose a course</h1>
        <p class="ll-muted">
          {{
            isTeacher
              ? 'Open a class you own, or create a new one.'
              : 'Open a class you are enrolled in.'
          }}
        </p>
      </div>
      <div class="header-actions">
        <button
          v-if="isTeacher"
          type="button"
          class="ll-btn ll-btn-primary"
          @click="showCreate = !showCreate"
        >
          {{ showCreate ? 'Cancel' : 'Create course' }}
        </button>
        <router-link v-if="isTeacher" class="ll-btn" to="/teacher/students">
          Manage students
        </router-link>
      </div>
    </header>

    <form v-if="isTeacher && showCreate" class="ll-panel create" @submit.prevent="onCreate">
      <h2>New course</h2>
      <label class="ll-field">
        Name
        <input v-model="newName" required maxlength="100" placeholder="e.g. Year 9 English" />
      </label>
      <label class="ll-field">
        Description
        <textarea
          v-model="newDescription"
          class="ll-input"
          rows="2"
          placeholder="Optional short description"
        />
      </label>
      <p v-if="error" class="ll-error">{{ error }}</p>
      <button type="submit" class="ll-btn ll-btn-primary" :disabled="busy || !newName.trim()">
        {{ busy ? 'Creating…' : 'Create' }}
      </button>
    </form>

    <div v-if="courses.length" class="course-list">
      <div v-for="course in courses" :key="course.uuid" class="course-row">
        <button type="button" class="course-button" @click="goToClass(course.uuid)">
          <span class="course-text">
            <span class="course-name">{{ course.name }}</span>
            <span v-if="course.description" class="course-desc">{{ course.description }}</span>
          </span>
          <span class="arrow" aria-hidden="true">→</span>
        </button>
        <button
          v-if="isTeacher"
          type="button"
          class="ll-btn ll-btn-ghost manage-btn"
          @click="goToSettings(course.uuid, $event)"
        >
          Manage
        </button>
      </div>
    </div>
    <p v-else class="ll-muted empty">
      {{
        isTeacher
          ? 'No courses yet — create one to get started.'
          : 'You are not enrolled in any courses yet. Ask your teacher to add you.'
      }}
    </p>
  </div>
</template>

<style scoped>
.user-start {
  width: min(100% - 2rem, 40rem);
  margin: 0 auto;
  padding: var(--ll-space-page) 0 3rem;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.page-header {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
}

.page-header > div:first-child {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.header-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.eyebrow {
  margin: 0;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--ll-accent);
}

.create {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.course-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.course-row {
  display: flex;
  gap: 0.5rem;
  align-items: stretch;
}

.course-button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.1rem 1.25rem;
  border: 1.5px solid var(--ll-border);
  border-radius: calc(var(--ll-radius) + 4px);
  background: var(--ll-surface);
  box-shadow: var(--ll-shadow);
  cursor: pointer;
  text-align: left;
  flex: 1;
  min-width: 0;
  transition:
    border-color 0.15s ease,
    background-color 0.15s ease,
    transform 0.15s ease;
}

.course-button:hover {
  border-color: var(--ll-accent);
  background: #f8fffd;
  transform: translateY(-1px);
}

.course-text {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 0;
}

.course-name {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--ll-ink);
}

.course-desc {
  font-size: 0.875rem;
  color: var(--ll-ink-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.arrow {
  font-size: 1.25rem;
  color: var(--ll-accent);
  flex-shrink: 0;
}

.manage-btn {
  flex-shrink: 0;
  align-self: center;
}

.empty {
  padding: 1.5rem;
  border: 1px dashed var(--ll-border);
  border-radius: var(--ll-radius);
  text-align: center;
}

textarea.ll-input {
  resize: vertical;
}
</style>
