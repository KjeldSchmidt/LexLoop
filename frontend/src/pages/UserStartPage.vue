<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getCourses } from '@/api'
import { useRouter } from 'vue-router'
import type { components } from '@/api/schema.ts'

type Course = components['schemas']['CourseOut']

const router = useRouter()
const courses = ref<Course[]>([])

onMounted(async () => {
  const coursesRes = await getCourses()
  if (coursesRes && Array.isArray(coursesRes)) {
    courses.value = coursesRes as Course[]
  }
})

function goToClass(course_uuid: string) {
  console.log(course_uuid)
  router.push({
    name: 'ClassOverview',
    params: { id: course_uuid },
  })
}
</script>

<template>
  <div class="user-start-container">
    <div class="content">
      <h2 class="prompt">Choose Course:</h2>
      <div class="course-list">
        <button
          v-for="course in courses"
          :key="course.uuid"
          class="course-button"
          @click="goToClass(course.uuid)"
        >
          <span class="course-name">{{ course.name }}</span>
          <span class="arrow">→</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.user-start-container {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  padding: 2rem;
  background: #fff;
}

.content {
  width: 100%;
  max-width: 600px;
}

.prompt {
  font-size: 1.25rem;
  font-weight: 500;
  margin-bottom: 1.5rem;
  color: #333;
}

.course-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.course-button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border: 1px solid #333;
  border-radius: 12px;
  background: #fff;
  cursor: pointer;
  transition: background-color 0.15s;
  text-align: left;
  width: 100%;
}

.course-button:hover {
  background-color: #f0f0f0;
}

.course-name {
  font-size: 1rem;
  color: #333;
}

.arrow {
  font-size: 1.25rem;
  color: #333;
  margin-left: auto;
}
</style>
