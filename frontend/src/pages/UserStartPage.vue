<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getCourses } from '@/api'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import type { components } from '@/api/schema.ts'
import { useAuthStore } from '@/stores/auth'

type Course = components['schemas']['CourseOut']

const router = useRouter()
const auth = useAuthStore()
const { isTeacher } = storeToRefs(auth)
const courses = ref<Course[]>([])

onMounted(async () => {
  const coursesRes = await getCourses()
  if (coursesRes?.items) {
    courses.value = coursesRes.items
  }
})

function goToClass(course_uuid: string) {
  router.push({
    name: 'ClassOverview',
    params: { id: course_uuid },
  })
}
</script>

<template>
  <div class="user-start">
    <header class="page-header">
      <div>
        <p class="eyebrow">Your workspace</p>
        <h1>Choose a course</h1>
        <p class="ll-muted">Open a class to browse tags and vocabulary.</p>
      </div>
      <router-link v-if="isTeacher" class="ll-btn" to="/teacher/students">
        Manage students
      </router-link>
    </header>

    <div v-if="courses.length" class="course-list">
      <button
        v-for="course in courses"
        :key="course.uuid"
        class="course-button"
        @click="goToClass(course.uuid)"
      >
        <span class="course-name">{{ course.name }}</span>
        <span class="arrow" aria-hidden="true">→</span>
      </button>
    </div>
    <p v-else class="ll-muted empty">No courses yet.</p>
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

.course-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.course-button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.1rem 1.25rem;
  border: 1.5px solid var(--ll-border);
  border-radius: calc(var(--ll-radius) + 4px);
  background: var(--ll-surface);
  box-shadow: var(--ll-shadow);
  cursor: pointer;
  text-align: left;
  width: 100%;
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

.course-name {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--ll-ink);
}

.arrow {
  font-size: 1.25rem;
  color: var(--ll-accent);
  margin-left: auto;
}

.empty {
  padding: 1.5rem;
  border: 1px dashed var(--ll-border);
  border-radius: var(--ll-radius);
  text-align: center;
}
</style>
