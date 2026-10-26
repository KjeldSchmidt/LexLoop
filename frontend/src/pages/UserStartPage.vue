<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { createCourse, getCourses, getMyJoinRequests, requestCourseJoin } from '@/api'
import type { components } from '@/api/schema.ts'
import { useAuthStore } from '@/stores/auth'

type Course = components['schemas']['CourseOut']
type PendingJoin = components['schemas']['StudentPendingJoinOut']

const router = useRouter()
const auth = useAuthStore()
const { isTeacher, isStudent } = storeToRefs(auth)
const courses = ref<Course[]>([])
const pendingJoins = ref<PendingJoin[]>([])
const showCreate = ref(false)
const newName = ref('')
const newDescription = ref('')
const busy = ref(false)
const loading = ref(true)
const pendingLoading = ref(false)
const error = ref('')
const joinCode = ref('')
const joinBusy = ref(false)
const joinError = ref('')
const joinMessage = ref('')

async function refreshPending() {
  if (!isStudent.value) {
    pendingJoins.value = []
    return
  }
  pendingLoading.value = true
  try {
    pendingJoins.value = await getMyJoinRequests()
  } catch {
    pendingJoins.value = []
  } finally {
    pendingLoading.value = false
  }
}

async function refresh() {
  loading.value = true
  try {
    const coursesRes = await getCourses()
    if (coursesRes?.items) {
      courses.value = coursesRes.items
    }
    await refreshPending()
  } finally {
    loading.value = false
  }
}

onMounted(refresh)

async function onJoinViaCode() {
  joinError.value = ''
  joinMessage.value = ''
  const code = joinCode.value.trim().toUpperCase()
  if (!/^[A-Z]{4}$/.test(code)) {
    joinError.value = 'Enter a 4-letter code.'
    return
  }
  joinBusy.value = true
  try {
    const result = await requestCourseJoin(code)
    if (result.status === 'pending' || result.status === 'already_pending') {
      joinMessage.value = `Request sent for “${result.course_name}”. Waiting for teacher approval.`
      await refreshPending()
    } else if (result.status === 'already_enrolled') {
      joinMessage.value = `You are already enrolled in “${result.course_name}”.`
      await refresh()
    } else {
      joinMessage.value = `Done for “${result.course_name}”.`
      await refresh()
    }
    joinCode.value = ''
  } catch {
    joinError.value = 'Invalid code or request failed.'
  } finally {
    joinBusy.value = false
  }
}

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

    <form v-if="isStudent" class="ll-panel join" @submit.prevent="onJoinViaCode">
      <h2>Enroll via code</h2>
      <label class="ll-field">
        Signup code
        <input
          v-model="joinCode"
          maxlength="4"
          placeholder="ABCD"
          class="code-input"
          autocomplete="off"
          spellcheck="false"
        />
      </label>
      <p v-if="joinError" class="ll-error">{{ joinError }}</p>
      <p v-else-if="joinMessage" class="join-ok">{{ joinMessage }}</p>
      <button type="submit" class="ll-btn ll-btn-primary" :disabled="joinBusy || !joinCode.trim()">
        {{ joinBusy ? 'Sending…' : 'Request enrollment' }}
      </button>
    </form>

    <section v-if="isStudent" class="pending-section">
      <h2>Pending requests</h2>
      <p v-if="loading || pendingLoading" class="ll-loading" aria-live="polite">
        Loading requests…
      </p>
      <ul v-else-if="pendingJoins.length" class="pending-list">
        <li v-for="req in pendingJoins" :key="req.course_uuid" class="pending-item">
          <span class="course-name">{{ req.course_name }}</span>
          <span class="ll-muted pending-status">Waiting for approval</span>
        </li>
      </ul>
      <p v-else class="ll-muted empty-pending">No pending enrollment requests.</p>
    </section>

    <p v-if="loading" class="ll-loading" aria-live="polite">Loading courses…</p>
    <div v-else-if="courses.length" class="course-list">
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
          : 'You are not enrolled in any courses yet. Use a signup code above, or ask your teacher.'
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

.create,
.join {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.code-input {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  max-width: 8rem;
}

.join-ok {
  margin: 0;
  font-weight: 500;
}

.pending-section {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.pending-section h2 {
  margin: 0;
  font-family: var(--ll-font-display);
  font-size: 1.15rem;
}

.pending-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.pending-item {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: 0.5rem 1rem;
  padding: 0.85rem 1rem;
  border: 1.5px dashed var(--ll-border);
  border-radius: calc(var(--ll-radius) + 4px);
  background: var(--ll-surface);
}

.pending-status {
  font-size: 0.875rem;
  font-weight: 500;
}

.empty-pending {
  margin: 0;
  font-size: 0.9rem;
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
